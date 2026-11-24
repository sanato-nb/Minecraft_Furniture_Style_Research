"""INT-4 H25 — Adorn 7.6.1 Fabric release/source model and UV audit.

Source-first, exact upstream git-blobs + actual official mod JAR pinned.
No game runtime proof, no asset copying or INT5/INT6 rights promotion.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import struct
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "project/integration/INT4_H25_ADORN_761_SELECTED_MODEL_SOURCE_V1.json"
UPSTREAM_REPO = "Juuxel/Adorn"
UPSTREAM_TAG = "7.6.1"
UPSTREAM_COMMIT = "6bfee0ee1ec2c259a577c5cde0b038641874fb2c"
RELEASE_FILE = "Adorn-7.6.1+1.21.11-fabric.jar"
RELEASE_SHA256 = "d431be4ee89d0d71b1ababedaa5275f478cfff5de94eba1165f5cd10d1b676d3"
SOURCE_PREFIX = "common/src/main/resources/assets/adorn"
SOURCE_BLOBS = {
    "blockstates/brewer.json": "74fbd445677c8f94379df8e88a65a8f97f2d5856",
    "blockstates/iron_shelf.json": "59dac5476515cae40791b73a113a82162249039b",
    "models/block/acacia_coffee_table.json": "98dd595f3bd0060c1a17868d8aac5abea3362ebd",
    "models/block/brewer.json": "40fac2d74c56f086ef056ca50221c29debee05e4",
    "models/block/brewer_active.json": "15d548856f306ecbd2727f10d758fc560019969b",
    "models/block/brewer_mug.json": "9b5f3b0cdecb7fa9a62883e2391ec6c684dac38f",
    "models/block/iron_shelf.json": "1bfa8c5533a19e5d09224beddf20497571009131",
    "models/block/templates/coffee_table.json": "ecf0ae2a63d621f4d76667b48bb0559a9f02c8d9",
    "models/block/templates/shelf.json": "449aa0c5c13adf0bf78030b417bd9dd9153e2e57",
}
GENERATED_ONLY = "blockstates/acacia_coffee_table.json"
MODELS = (
    "adorn:block/acacia_coffee_table",
    "adorn:block/iron_shelf",
    "adorn:block/brewer",
    "adorn:block/brewer_active",
    "adorn:block/brewer_mug",
)
FACING_Y = {"east": 0, "south": 90, "north": 270, "west": 180}
BREWER_Y = {"north": 0, "east": 90, "south": 180, "west": 270}


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError("H25 official Adorn audit: " + message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def model_member(resource_id: str) -> str | None:
    if ":" in resource_id:
        namespace, path = resource_id.split(":", 1)
    else:
        namespace, path = "minecraft", resource_id
    require(namespace in {"adorn", "minecraft"} and path.startswith("block/") and
            ".." not in path and not path.endswith(".json"), "unrecognized model parent")
    if namespace == "minecraft":
        require(path == "block/block", "unverified external geometry parent")
        return None
    return "assets/adorn/models/" + path + ".json"


def resolve_texture(name: str, textures: dict) -> str:
    seen = set()
    while name.startswith("#"):
        key = name[1:]
        require(key not in seen and key in textures, "unresolved/circular texture variable " + name)
        seen.add(key)
        name = textures[key]
    require(":" in name, "texture missing namespace")
    ns, key = name.split(":", 1)
    require(ns in ("adorn", "minecraft") and key.startswith("block/") and ".." not in key,
            "invalid texture resource")
    return name


def model_profile(resource_id: str, files: dict[str, dict]) -> dict:
    path = model_member(resource_id)
    require(path is not None, "root model is external")
    chain = []
    seen = set()
    while path is not None:
        require(path not in seen, "cyclic parent model")
        seen.add(path)
        require(path in files, "selected model not present: " + path)
        data = files[path]
        chain.append((path, data))
        path = model_member(data["parent"]) if "parent" in data else None
    textures = {}
    elements = None
    for _, data in reversed(chain):
        textures.update(data.get("textures", {}))
    for _, data in chain:
        if "elements" in data:
            elements = data["elements"]
            break
    require(isinstance(elements, list) and bool(elements), "model has no traceable geometry")
    face_tex = Counter()
    explicit, implicit, zero_area, rotated = 0, 0, 0, 0
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    face_total = 0
    for element in elements:
        coords = element["from"], element["to"]
        require(all(len(a) == 3 for a in coords), "not a 3-axis source element")
        for k in range(3):
            lo[k] = min(lo[k], coords[0][k])
            hi[k] = max(hi[k], coords[1][k])
            require(coords[0][k] < coords[1][k], "empty/reversed source element")
        if "rotation" in element:
            rotated += 1
        for face, item in element.get("faces", {}).items():
            require(face in {"up", "down", "east", "west", "north", "south"},
                    "unsupported source face")
            face_total += 1
            resolved = resolve_texture(item["texture"], textures)
            face_tex[resolved] += 1
            if "uv" in item:
                uv = item["uv"]
                require(len(uv) == 4 and all(isinstance(v, (int, float)) for v in uv),
                        "invalid explicit UV")
                explicit += 1
                if (uv[2] - uv[0]) * (uv[3] - uv[1]) == 0:
                    zero_area += 1
            else:
                implicit += 1
    require(face_total == explicit + implicit and face_total > 0, "face UV accounting mismatch")
    return {
        "model": resource_id,
        "source_parent_chain_leaf_first": [p for p, _ in chain],
        "source_elements": len(elements),
        "source_faces": face_total,
        "explicit_uv_faces": explicit,
        "implicit_uv_faces_require_bake": implicit,
        "documented_zero_area_explicit_uv_faces": zero_area,
        "elements_with_rotation": rotated,
        "unrotated_source_bounds": {"from": lo, "to": hi},
        "resolved_face_textures": dict(sorted(face_tex.items())),
        "external_minecraft_face_count": sum(n for k, n in face_tex.items()
                                             if k.startswith("minecraft:")),
    }


def matches(when: dict, state: dict) -> bool:
    require(isinstance(when, dict) and all(k in state for k in when),
            "unsupported/missing multipart state keys")
    for key, expected in when.items():
        value = state[key]
        normalize = lambda x: str(x).lower()
        if normalize(value) != normalize(expected):
            return False
    return True


def selected_parts(blockstate: dict, state: dict) -> list[dict]:
    if "variants" in blockstate:
        require("multipart" not in blockstate, "variant/multipart conflict")
        key = ",".join(k + "=" + str(state[k]).lower() for k in sorted(state))
        # Source variants can be serialized in non-alphabetic property order.
        options = []
        for case, applied in blockstate["variants"].items():
            parsed = dict(kv.split("=", 1) for kv in case.split(",") if kv)
            if parsed == {k: str(v).lower() for k, v in state.items()}:
                options.append(applied)
        require(len(options) == 1, "ambiguous/missing exact blockstate variant: " + key)
        selected = options[0]
        require(isinstance(selected, dict) and "model" in selected,
                "unsupported weighted variants")
        return [selected]
    require("multipart" in blockstate, "missing blockstate mapping")
    models = []
    for x in blockstate["multipart"]:
        require(isinstance(x["when"], dict) and isinstance(x["apply"], dict),
                "unsupported multipart declaration")
        if matches(x["when"], state):
            models.append(x["apply"])
    require(models, "no selected multipart model")
    return models


def source_download(path: str) -> bytes:
    url = "https://raw.githubusercontent.com/" + UPSTREAM_REPO + "/" + UPSTREAM_COMMIT + "/" + SOURCE_PREFIX + "/" + path
    request = urllib.request.Request(url, headers={"User-Agent": "MCFR-H25-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def audit(jar: Path, downloads: dict[str, bytes] | None = None) -> dict:
    require(jar.is_file(), "official release JAR not found")
    jar_raw = jar.read_bytes()
    require(sha256(jar_raw) == RELEASE_SHA256, "official release JAR SHA-256 mismatch")
    if downloads is None:
        downloads = {p: source_download(p) for p in SOURCE_BLOBS}
    require(set(downloads) == set(SOURCE_BLOBS), "source file pin set drift")
    source_json = {}
    for p, expected_blob in SOURCE_BLOBS.items():
        b = downloads[p]
        require(git_blob(b) == expected_blob, "upstream tagged Git blob mismatch: " + p)
        source_json[p] = json.loads(b)
    with zipfile.ZipFile(jar) as z:
        require(z.testzip() is None, "broken official release archive")
        members = z.namelist()
        require(len(members) == len(set(members)), "duplicate release ZIP members")
        root = "assets/adorn/"
        require(root + GENERATED_ONLY in members, "generated coffee table blockstate not in JAR")
        files = {}
        comparison = {}
        for rel, raw in downloads.items():
            b = z.read(root + rel)
            data = json.loads(b)
            require(data == source_json[rel],
                    "tagged source/official release JSON mismatch: " + rel)
            files[root + rel] = data
            comparison[rel] = {
                "upstream_git_blob_sha1": SOURCE_BLOBS[rel],
                "released_sha256": sha256(b),
                "raw_bytes_equal": b == raw,
                "JSON_semantics_equal": True,
            }
        generated = z.read(root + GENERATED_ONLY)
        files[root + GENERATED_ONLY] = json.loads(generated)
        profiles = {k: model_profile(k, files) for k in MODELS}
        textures = {}
        for p in profiles.values():
            for resource in p["resolved_face_textures"]:
                if resource.startswith("minecraft:"):
                    textures[resource] = {"status": "EXTERNAL_VANILLA_TEXTURE_NOT_IN_ADORN_JAR"}
                else:
                    k = "assets/adorn/textures/" + resource.split(":", 1)[1] + ".png"
                    require(k in members, "missing Adorn texture: " + k)
                    raw = z.read(k)
                    require(raw.startswith(b"\x89PNG\r\n\x1a\n"), "invalid PNG signature")
                    w, h = struct.unpack(">II", raw[16:24])
                    textures[resource] = {
                        "status": "OFFICIAL_RELEASE_PNG_PRESENT",
                        "path": k,
                        "sha256": sha256(raw),
                        "size": [w, h],
                    }
        meta = json.loads(z.read("fabric.mod.json"))
        require(meta["id"] == "adorn" and meta["version"] == "7.6.1+1.21.11" and
                meta["depends"]["minecraft"] == "=1.21.11",
                "official Fabric release metadata mismatch")
        coffee = files[root + GENERATED_ONLY]
        require(set(coffee) == {"variants"} and set(coffee["variants"]) == {""},
                "generated coffee table source state is not singleton")
        cases = []
        def record(block, state, kind):
            path = root + "blockstates/" + block + ".json"
            parts = selected_parts(files[path], state)
            selected = []
            for part in parts:
                m = part["model"]
                require(m in profiles, "selected model not under tested original scope")
                p = profiles[m]
                selected.append({"model": m, "y": int(part.get("y", 0)),
                                 "uvlock": bool(part.get("uvlock", False)),
                                 "source_elements": p["source_elements"],
                                 "source_faces": p["source_faces"]})
            require(len({(m["model"], m["y"]) for m in selected}) == len(selected),
                    "duplicate selected model")
            cases.append({
                "block": "adorn:" + block,
                "state": dict(state), "case_kind": kind,
                "selected": selected, "selected_applications": len(selected),
                "sum_source_elements": sum(p["source_elements"] for p in selected),
                "sum_source_faces": sum(p["source_faces"] for p in selected),
            })
        record("acacia_coffee_table", {}, "SINGLETON_GENERATED_BLOCKSTATE")
        for facing in ("north", "east", "south", "west"):
            record("iron_shelf", {"facing": facing}, "VARIANTS_FACING_ROTATION")
        for facing in ("north", "east", "south", "west"):
            for active in (False, True):
                for has_mug in (False, True):
                    record("brewer", {"facing": facing, "active": active, "has_mug": has_mug},
                           "MULTIPART_BASE_WITH_OPTIONAL_MUG")
        require(len(cases) == 21, "exact state cases are not 21")
        require([(c["state"]["facing"], c["selected"][0]["y"])
                 for c in cases[1:5]] ==
                [(f, FACING_Y[f]) for f in ("north", "east", "south", "west")],
                "iron shelf directional rotations changed")
        for c in cases[5:]:
            state = c["state"]
            expected_base = "adorn:block/brewer_active" if state["active"] else "adorn:block/brewer"
            want = [expected_base] + (["adorn:block/brewer_mug"] if state["has_mug"] else [])
            require([s["model"] for s in c["selected"]] == want,
                    "brewer active/mug selected source changed")
            require(all(s["y"] == BREWER_Y[state["facing"]] for s in c["selected"]),
                    "brewer facing selected rotation changed")
            require(c["sum_source_elements"] == (11 if state["has_mug"] else 3) and
                    c["sum_source_faces"] == (51 if state["has_mug"] else 16),
                    "brewer active and mug geometry accounting mismatch")
        # Compare original inactive vs active inheritance, without asserting visible GPU pixels.
        require(profiles["adorn:block/brewer"]["source_elements"] ==
                profiles["adorn:block/brewer_active"]["source_elements"] == 3,
                "active brewer geometry mismatch")
        require(profiles["adorn:block/brewer"]["source_faces"] ==
                profiles["adorn:block/brewer_active"]["source_faces"] == 16,
                "active brewer face count mismatch")
        require(profiles["adorn:block/brewer"]["resolved_face_textures"] !=
                profiles["adorn:block/brewer_active"]["resolved_face_textures"],
                "active brewer source texture override missing")
        require(profiles["adorn:block/acacia_coffee_table"]["source_elements"] == 12 and
                profiles["adorn:block/acacia_coffee_table"]["source_faces"] == 56,
                "generated coffee table model inheritance mismatch")
        require(profiles["adorn:block/iron_shelf"]["source_elements"] == 3 and
                profiles["adorn:block/iron_shelf"]["source_faces"] == 16,
                "iron shelf template geometry mismatch")
        return {
            "schema": "MCFR_INT4_H25_ADORN_761_OFFICIAL_SOURCE_SELECTORS_V1",
            "source_repo": "https://github.com/Juuxel/Adorn",
            "upstream_release_tag": UPSTREAM_TAG,
            "upstream_tag_commit": UPSTREAM_COMMIT,
            "official_jar_name": RELEASE_FILE,
            "official_jar_sha256": RELEASE_SHA256,
            "official_jar_size": len(jar_raw),
            "official_jar_members": len(members),
            "official_fabric_metadata": {k: meta[k] for k in ("id", "version")},
            "source_json_comparisons": comparison,
            "generated_only_blockstate": {
                "path": root + GENERATED_ONLY, "sha256": sha256(generated),
                "status": "JAR_EXISTS_GIT_STATIC_SOURCE_FILE_ABSENT",
                "variants": list(coffee["variants"]),
            },
            "resolved_models": profiles,
            "resolved_texture_paths": textures,
            "selected_state_cases": cases,
            "scope": {
                "verified_source_model_profiles": len(profiles),
                "verified_exact_selected_states": len(cases),
                "shelf_rotations": 4,
                "brewer_state_combinations": 16,
                "mod_cohort": "ADORN",
                "new_game_runs": 0,
                "new_native_F2": 0,
                "official_jar_checked": True,
                "tagged_json_and_release_semantic_match": True,
            },
            "legacy_gates_unchanged": {
                "modeling_F70_scope_from_H23": "70/70",
                "strict_F70_unconditional": 0, "H03": "HOLD", "H05": "CONDITIONAL",
                "INT5": 0, "INT6": 0, "GPU_per_face_approved": False,
            },
            "limits": [
                "Static source selectors and model JSON only. No real Minecraft native F2 or GPU evidence.",
                "Implicit/default face UV is counted but cannot be called exact baked UV without Mojang bake.",
                "External minecraft:block textures require separately pinned Mojang source assets.",
                "Element from/to bounds precede any element rotation, not exact world-space AABB.",
                "Mod upstream code license does not prove AI training or redistribution rights for all assets.",
            ],
        }



CSV_FILE = ROOT / "project/integration/INT4_H25_ADORN_761_STATE_SELECTOR_CASES_V1.csv"
CSV_FIELDS = (
    "case_id", "block", "blockstate", "selection_kind", "selected_source_models",
    "y_rotation_degrees", "model_applications", "source_elements", "source_faces",
    "explicit_uv_faces", "implicit_uv_faces", "external_vanilla_texture_faces",
    "source_status", "new_F2", "GPU_per_face_approved",
)


def selector_rows(result: dict) -> list[dict[str, str]]:
    profiles = result["resolved_models"]
    rows = []
    for index, case in enumerate(result["selected_state_cases"], start=1):
        selected = case["selected"]
        models = [profiles[p["model"]] for p in selected]
        state = ";".join(k + "=" + str(v).lower()
                         for k, v in sorted(case["state"].items())) or "(default)"
        row = {
            "case_id": "ADORN" + str(index).zfill(2),
            "block": case["block"],
            "blockstate": state,
            "selection_kind": case["case_kind"],
            "selected_source_models": "|".join(p["model"] for p in selected),
            "y_rotation_degrees": "|".join(str(p["y"]) for p in selected),
            "model_applications": str(case["selected_applications"]),
            "source_elements": str(case["sum_source_elements"]),
            "source_faces": str(case["sum_source_faces"]),
            "explicit_uv_faces": str(sum(p["explicit_uv_faces"] for p in models)),
            "implicit_uv_faces": str(sum(p["implicit_uv_faces_require_bake"] for p in models)),
            "external_vanilla_texture_faces": str(sum(
                p["external_minecraft_face_count"] for p in models
            )),
            "source_status": "OFFICIAL_JAR_AND_TAG_SOURCE_PINNED",
            "new_F2": "false",
            "GPU_per_face_approved": "false",
        }
        require(list(row) == list(CSV_FIELDS), "CSV schema changed")
        rows.append(row)
    require(len(rows) == 21 and len({r["case_id"] for r in rows}) == 21,
            "not 21 source state rows")
    require(all(int(x["explicit_uv_faces"]) + int(x["implicit_uv_faces"]) ==
                int(x["source_faces"]) for x in rows),
            "per-state explicit/implicit UV face sum mismatch")
    return rows


def verify_csv(result: dict, path: Path = CSV_FILE) -> None:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames == list(CSV_FIELDS), "CSV column schema drift")
        actual = list(reader)
    require(actual == selector_rows(result), "saved 21-row CSV differs from JAR audit")
    print("H25_PERSISTED_21_CASE_CSV_SOURCE_MODEL_UV_MATCH")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--jar", type=Path, required=True)
    p.add_argument("--verify", action="store_true")
    p.add_argument("--output", type=Path, default=OUT)
    a = p.parse_args()
    result = audit(a.jar)
    if a.verify:
        require(a.output.is_file(), "saved H25 output missing")
        require(json.loads(a.output.read_text(encoding="utf-8")) == result,
                "saved output differs from independent JAR/source recomputation")
        verify_csv(result)
        print("H25_ADORN_7_6_1_OFFICIAL_JAR_21_STATES_5_MODELS_INDEPENDENT_VERIFIED")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) +
                            "\n", encoding="utf-8")
        print("H25_ADORN_RESULT_JSON_START")
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        print("H25_ADORN_RESULT_JSON_END")


if __name__ == "__main__":
    main()
