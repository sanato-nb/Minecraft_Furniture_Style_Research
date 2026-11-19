"""Reproduce H6–H7 with two pinned Adorn JARs supplied by the operator."""

import argparse
from collections import Counter
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
PINS = ROOT / "project/audits/h67/ADORN_PINS.json"
KINDS = {
    ("models", ".json"): "model", ("blockstates", ".json"): "blockstate",
    ("items", ".json"): "item_definition", ("textures", ".png"): "texture",
    ("textures", ".mcmeta"): "texture_sidecar",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def manifest(jar_path, pin):
    artifact = pin["files"][0]
    with jar_path.open("rb") as stream:
        for algorithm, expected in artifact["hashes"].items():
            stream.seek(0)
            require(hashlib.file_digest(stream, algorithm).hexdigest() == expected, f"{algorithm} mismatch: {jar_path}")
        require(stream.tell() == artifact["size"], f"Size mismatch: {jar_path}")
        stream.seek(0)
        with ZipFile(stream) as jar:
            names = jar.namelist()
            require(len(names) == len(set(names)), "Duplicate member paths")
            metadata = json.loads(jar.read("fabric.mod.json"))
            require(metadata["id"] == "adorn" and metadata["version"] == pin["fabric_version"]
                    and metadata["depends"]["minecraft"] == "=1.21.11", "Unexpected Fabric metadata")
            assets = []
            for member in sorted(jar.infolist(), key=lambda entry: entry.filename):
                parts = member.filename.split("/", 3)
                if len(parts) != 4 or parts[:2] != ["assets", "adorn"] or member.is_dir():
                    continue
                name = Path(parts[3])
                kind = KINDS.get((parts[2], name.suffix))
                if kind is None or (kind == "texture_sidecar" and not name.name.endswith(".png.mcmeta")):
                    continue
                stem = parts[3].removesuffix(name.suffix)
                if kind == "texture_sidecar":
                    stem = stem.removesuffix(".png")
                body = jar.read(member)
                assets.append({
                    "source_path": member.filename, "resource_id": f"adorn:{stem}",
                    "kind": kind, "hash_algorithm": "SHA256", "digest": hashlib.sha256(body).hexdigest(),
                    "byte_count": len(body),
                })
    release = {
        "release_key": f"adorn-{pin['version_number']}-1.21.11", "profile": "mods", "target_id": "adorn",
        "version": pin["fabric_version"].split("+")[0], "minecraft_version": "1.21.11", "loader": "fabric",
        "pin_algorithm": "SHA256", "pin_digest": artifact["hashes"]["sha256"],
        "source": f"https://modrinth.com/mod/adorn/version/{pin['id']}",
    }
    return {"release": release, "assets": assets}


def replay(work, sources, pins):
    from mcfr import research_db, update_watch

    db = work / "research.sqlite"

    def call(module, *args, expected_status=0):
        process = subprocess.run([sys.executable, "-m", f"mcfr.{module}", "--db", str(db), *map(str, args)],
                                 cwd=ROOT, env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                                 capture_output=True, text=True, check=False)
        require(process.returncode == expected_status, f"{module} {args[0]} failed: {process.stderr}")
        return json.loads(process.stdout) if process.stdout.strip() else process.stderr

    require(call("research_db", "init")["schema_version"] == 4, "Unexpected DB schema")
    call("research_db", "import-legacy")
    releases = {}
    inventories = {}
    for label, path in sources.items():
        data = manifest(path, pins[label])
        file = work / f"{label}.json"
        file.write_text(json.dumps(data), encoding="utf-8")
        require(call("research_db", "register", file)["assets_added"] == len(data["assets"]), "Incomplete registration")
        require(call("research_db", "register", file)["assets_added"] == 0, "Registration was not idempotent")
        releases[label] = data["release"]["release_key"]
        inventories[label] = {row["source_path"]: row for row in data["assets"]}

    observations = []
    with closing(research_db.open_db(db, "rw")) as connection:
        for feed in ([pins["baseline"]], [pins["updated"], pins["baseline"]], [pins["updated"], pins["baseline"]]):
            result = update_watch.check(connection, "adorn", "1.21.11", "fabric", load=lambda _: feed)
            observations.append(result["status"])
    require(observations == ["BASELINE", "UPDATE_DETECTED", "UNCHANGED"], "Incorrect pinned update replay")

    def run(name, release, mode, source, *extra, pause=False):
        call("research_db", "run-create", name, release, "--mode", mode, *extra)
        scan = ("scan", name, f"{name}-job", "--source", source)
        if pause:
            partial = call("workflow", *scan, "--max-assets", "64")
            require(partial["status"] == "PENDING" and partial["next_asset"] == 64, "Checkpoint was not written")
        finished = call("workflow", *scan)
        require(finished["status"] == "PASS", "Source workflow failed")
        require(call("workflow", *scan)["execution_id"] == finished["execution_id"], "Rerun created a duplicate execution")
        report = call("research_engine", "show", name, "--details")
        require(len(report) == 1 and report[0]["scope_sha256"] == finished["scope_sha256"], "Execution ledger mismatch")
        return finished["execution_id"], report[0]["report"], call("extensions", "coverage", name)

    old, new = inventories["baseline"], inventories["updated"]
    removed = old.keys() - new.keys()
    added = new.keys() - old.keys()
    changed = {path for path in old.keys() & new.keys() if old[path]["digest"] != new[path]["digest"]}
    _, previous, _ = run("adorn-new", releases["baseline"], "NEW", sources["baseline"], pause=True)
    _, incremental, increment_coverage = run(
        "adorn-update", releases["updated"], "INCREMENTAL", sources["updated"], "--baseline", releases["baseline"],
    )
    require(incremental["pin_check"] == "archive_and_asset_hashes", "Updated archive pin was not checked")
    require(set(incremental["removed"]) == removed and
            {row["source_path"] for row in incremental["assets"]} == added | changed, "Incorrect incremental scope")
    fresh_id, fresh, fresh_coverage = run("adorn-fresh", releases["updated"], "FRESH", sources["updated"], pause=True)
    require(previous["verified"] == len(old) and fresh["verified"] == len(new)
            and {row["source_path"] for row in fresh["assets"]} == set(new), "Whole-run verification incomplete")

    vanilla_id, vanilla, _ = run("vanilla-reference", "minecraft-java-1.21.11-git", "REVALIDATE", ROOT)
    comparison = call("extensions", "compare", vanilla_id, fresh_id)
    require(sum(row["left"] for row in comparison["profiles"]) == vanilla["verified"] and
            sum(row["right"] for row in comparison["profiles"]) == fresh["verified"], "Comparison omitted assets")

    texture = next(path for path in sorted(old.keys() & new.keys())
                   if new[path]["kind"] == "texture" and old[path]["digest"] == new[path]["digest"])
    for label, jar_path in sources.items():
        with ZipFile(jar_path) as jar:
            (work / f"{label}.png").write_bytes(jar.read(texture))
    pixels = call("extensions", "visual", work / "baseline.png", work / "updated.png",
                  "--reference-sha256", old[texture]["digest"])
    require(pixels["status"] == "MATCH", "Identical pinned texture produced a visual mismatch")

    preview = call("workflow", "review-prepare", "h67-review", fresh_id, "--model", "fixture-preview",
                   "--max-output-tokens", "128", "--asset", texture)
    require(preview["state"] == "PREPARED", "Expected a staged AI request")
    refusal = call("workflow", "review-send", "h67-review", "--approve", "0" * 64, expected_status=2)
    require("Approval digest does not match" in refusal, "Incorrect approval was not rejected")
    usage = call("extensions", "usage")
    require(usage["models"] == {"fixture-preview": {"prepared": 1}}, "Unexpected AI transmission")

    return {
        "schema_version": 4, "update_replay": observations,
        "new": {"verified": previous["verified"], "checkpoint_at": 64},
        "incremental": {"scope_counts": increment_coverage["scope_counts"], "verified": incremental["verified"],
                        "removed_by_kind": dict(Counter(old[path]["kind"] for path in removed)),
                        "removed_paths_sha256": hashlib.sha256("\n".join(sorted(removed)).encode()).hexdigest(),
                        "archive_pin_verified": incremental["pin_check"] == "archive_and_asset_hashes"},
        "fresh": {"verified": fresh["verified"], "checkpoint_at": 64, "coverage": fresh_coverage["total"]},
        "cross_research": {"vanilla_assets": vanilla["verified"], "adorn_assets": fresh["verified"],
                           "shared_profiles": comparison["shared_profiles"], "profiles": len(comparison["profiles"])},
        "texture_control": {**pixels, "path": texture, "evidence_class": "ASSET_TEXTURE_PIXEL_COMPARISON"},
        "ai_preview": {"state": preview["state"], "wrong_approval_rejected": True, "outbound_requests": 0},
        "catalog_by_release": {
            label: dict(Counter(row["kind"] for row in entries.values())) for label, entries in inventories.items()
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline_jar", type=Path)
    parser.add_argument("updated_jar", type=Path)
    options = parser.parse_args()
    sys.path.insert(0, str(ROOT / "src"))
    sources = {"baseline": options.baseline_jar.resolve(), "updated": options.updated_jar.resolve()}
    with TemporaryDirectory(prefix="mcfr-h67-") as folder:
        print(json.dumps(replay(Path(folder), sources, json.loads(PINS.read_text(encoding="utf-8"))), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
