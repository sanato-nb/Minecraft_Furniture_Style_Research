"""Read existing evidence ledgers and SQLite artifacts without writing to them."""

from contextlib import closing
import csv
import gzip
import json
import lzma
from pathlib import Path
import sqlite3

VANILLA = Path("research/vanilla_models")
MODS = Path("research/furniture_mods")
MOD_B = MODS / "phase_1-3/B/source_verification"
MOD_F = MODS / "phase_1-3/F"
VANILLA_FINAL = VANILLA / "phase_1-2-G/final"
DATABASES = {
    "stage1-v8": Path("data/MC_Furniture_Style_Stage1_Research_v8.sqlite"),
    "mod-handoff": MOD_F / "furniture_research.sqlite.xz",
    "comparison": MODS / "phase_1-5/E/comparison.sqlite.xz",
}
VANILLA_KINDS = {"BLOCK_MODEL_JSON": "model", "BLOCKSTATE_JSON": "blockstate", "BLOCK_TEXTURE_PNG": "texture"}
MOD_KINDS = {"models": "model", "blockstates": "blockstate", "items": "item_definition"}


def read_rows(root, path):
    file = root / path
    opener = gzip.open if file.suffix == ".gz" else open
    with opener(file, "rt", encoding="utf-8-sig", newline="") as stream:
        yield from csv.DictReader(stream)


def asset(path, kind, resource, algorithm, digest, evidence, size=None):
    return {
        "source_path": path, "kind": kind, "resource_id": resource,
        "hash_algorithm": algorithm, "digest": digest, "byte_count": size,
        "evidence_path": evidence.as_posix(),
    }


def vanilla_resource(path):
    resource = path.split("/assets/minecraft/", 1)[1].split("/", 1)[1]
    stem = resource.removesuffix(".mcmeta").rsplit(".", 1)[0]
    return "minecraft:" + stem


def vanilla_assets(root):
    original = VANILLA_FINAL / "G_FINAL_SOURCE_SHA_4669.csv"
    for row in read_rows(root, original):
        if row["source_sha_match"] != "True":
            raise ValueError(f"Unverified historical Vanilla asset: {row['path']}")
        path, kind = row["path"], VANILLA_KINDS[row["type"]]
        yield asset(path, kind, vanilla_resource(path), "GIT_BLOB_SHA1",
                    row["sha"], original, int(row["bytes"]))
    meta = VANILLA_FINAL / "G_FINAL_MCMETA_99.csv"
    for row in read_rows(root, meta):
        path = row["mcmeta_path"]
        yield asset(path, "texture_sidecar", vanilla_resource(path),
                    "GIT_BLOB_SHA1", row["git_sha"], meta, int(row["bytes"]))


def mod_assets(root, code, algorithm, textures, texture_ledger):
    path = MOD_B / f"B_{code}_SOURCE_BODIES.csv.gz"
    for row in read_rows(root, path):
        if row["mod_id"] != code:
            raise ValueError(f"Unexpected historical mod code in {path}: {row['mod_id']}")
        yield asset(row["path"], MOD_KINDS[row["family"]], row["asset_id"], algorithm,
                    row["sha"], path, int(row["bytes"]))
    for row in textures:
        yield asset(row["path"], "texture", row["resource_id"], row["source_hash_kind"],
                    row["source_sha"], texture_ledger)


def import_catalog(db, root, register_release):
    registry = json.loads((root / "registry/legacy-releases.json").read_text(encoding="utf-8"))
    review = json.loads((root / VANILLA / "phase_1-2-review/REVIEW_AUDIT.json").read_text(encoding="utf-8"))
    if review["baseline"] != registry["vanilla"]["pin_digest"]:
        raise ValueError("Vanilla catalog pin differs from the historical review")

    pins = {}
    for row in read_rows(root, MOD_B / "B_FIXED_THREE_SOURCE_SCOPE.csv"):
        code = row["mod_id"]
        if registry[code]["pin_digest"] != row["pinned_git_commit_or_jar_sha256"]:
            raise ValueError(f"Catalog pin differs from the historical source scope: {code}")
        pins[code] = row["file_hash_algorithm"].upper()
    texture_ledger = MOD_F / "1-3_TEXTURE_UV_HANDOFF.csv"
    textures = {code: [] for code in pins}
    for row in read_rows(root, texture_ledger):
        if row["texture_status"] == "PINNED_MOD_PNG":
            textures[row["source_id"]].append(row)

    added = {registry["vanilla"]["release_key"]: register_release(db, registry["vanilla"], vanilla_assets(root))}
    for code, algorithm in pins.items():
        release = registry[code]
        added[release["release_key"]] = register_release(
            db, release, mod_assets(root, code, algorithm, textures[code], texture_ledger),
        )
    return {"assets_added": sum(added.values()), "assets_added_by_release": added}


def database_info(root, name):
    relative = DATABASES[name]
    path = (root / relative).resolve()
    with closing(sqlite3.connect(":memory:" if path.suffix == ".xz" else f"{path.as_uri()}?mode=ro",
                                 uri=True)) as db:
        if path.suffix == ".xz":
            with lzma.open(path, "rb") as stream:
                db.deserialize(stream.read())
        db.execute("PRAGMA query_only = ON")
        integrity = db.execute("PRAGMA quick_check").fetchall()
        if integrity != [("ok",)]:
            raise ValueError(f"Legacy database quick_check failed: {relative}")
        return {
            "artifact": relative.as_posix(),
            "integrity": "ok",
            "user_version": db.execute("PRAGMA user_version").fetchone()[0],
            "tables": [row[0] for row in db.execute(
                "SELECT name FROM sqlite_schema WHERE type = 'table' AND name NOT GLOB 'sqlite_*' ORDER BY name"
            )],
        }
