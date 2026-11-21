"""INT-2 independent 1-2 model inheritance, faces, declared UV and blockstate options.

This does not import/reuse the historical B/C/D analyzers. It recomputes
measurements from original Minecraft Java 1.21.11 JSON files and compares
per-model facts with C_SCOPE_2390_FINAL_STATUS and D's exit contract.
It does NOT reproduce all state-case combinatorics (9,193 / 19,440).
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path

C_LEDGER = "research/vanilla_models/phase_1-2-C/entry5/C_SCOPE_2390_FINAL_STATUS.csv"
G_LEDGER = "research/vanilla_models/phase_1-2-G/final/G_FINAL_SOURCE_SHA_4669.csv"
B_CONTRACT = "research/vanilla_models/phase_1-2-B/entry10/B_EXIT_AUDIT.json"
D_CONTRACT = "research/vanilla_models/phase_1-2-D/entry6/D_FINAL_CLOSURE.json"
REPORT_NAME = "INT2_1_2_MODEL_CROSSCHECK.csv"
COLUMNS = ["source_path", "c_assignment", "parent_depth", "geometry_provider",
           "elements", "applied_faces", "explicit_uv_faces", "implicit_uv_faces",
           "bound_png_faces", "unbound_template_faces", "slot_count",
           "comparison", "differences"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def raw_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()


def strict_json(data: bytes, path: str):
    def pairs(items):
        out = {}
        for name, value in items:
            if name in out:
                raise ValueError(f"{path}: duplicate JSON key {name}")
            out[name] = value
        return out
    return json.loads(data.decode("utf-8-sig"), object_pairs_hook=pairs)


def block_model_path(ref: str) -> str | None:
    if not isinstance(ref, str):
        raise ValueError(f"Invalid model reference: {ref!r}")
    ns, sep, path = ref.partition(":")
    if not sep:
        ns, path = "minecraft", ns
    if ns != "minecraft" or not path.startswith("block/"):
        return None
    if ".." in path.split("/") or "\\" in path or path.startswith("/"):
        raise ValueError(f"Illegal model reference: {ref}")
    return f"1.21.11/assets/minecraft/models/{path}.json"


def ancestry(start: str, models: dict[str, dict]) -> list[str]:
    chain = []
    current = start
    while current in models:
        if current in chain:
            raise ValueError(f"Model inheritance cycle: {current}")
        chain.append(current)
        parent = models[current].get("parent")
        if parent is None:
            return chain
        current = block_model_path(parent)
        if current is None:
            return chain
        if current not in models:
            raise ValueError(f"Missing model parent for {start}: {current}")
    raise ValueError(f"Model not found: {start}")


def source_faces(start: str, models: dict[str, dict], png_paths: set[str]):
    chain = ancestry(start, models)
    provider = next((path for path in chain if "elements" in models[path]), "")
    slots = {}
    for path in reversed(chain):
        textures = models[path].get("textures", {})
        if not isinstance(textures, dict):
            raise ValueError(f"{path}: invalid texture bindings")
        slots.update(textures)

    def resolve_face_texture(ref: str):
        seen = set()
        while True:
            if not isinstance(ref, str):
                return False, False
            key = ref.removeprefix("#")
            if key not in slots:
                if ref.startswith("#"):
                    return False, True
                break
            if key in seen:
                return False, True
            seen.add(key)
            ref = slots[key]
        namespace, sep, target = ref.partition(":")
        if not sep:
            namespace, target = "minecraft", namespace
        if namespace != "minecraft" or not target.startswith("block/"):
            return False, True
        png_path = f"1.21.11/assets/minecraft/textures/{target}.png"
        if png_path not in png_paths:
            return False, True
        return True, False

    elements = models[provider].get("elements", []) if provider else []
    if not isinstance(elements, list):
        raise ValueError(f"{provider}: elements is not list")
    explicit = implicit = bound = unbound = faces = 0
    for elem in elements:
        if not isinstance(elem, dict):
            raise ValueError(f"{provider}: invalid element")
        for direction, face in elem.get("faces", {}).items():
            if direction not in ("up", "down", "north", "south", "east", "west"):
                raise ValueError(f"{provider}: invalid face {direction}")
            if not isinstance(face, dict):
                raise ValueError(f"{provider}: invalid face body")
            faces += 1
            explicit += int("uv" in face)
            implicit += int("uv" not in face)
            resolved, missing = resolve_face_texture(face.get("texture"))
            bound += int(resolved)
            unbound += int(missing)
    return {
        "parent_depth": len(chain) - 1,
        "geometry_provider": provider,
        "elements": len(elements),
        "applied_faces": faces,
        "explicit_uv_faces": explicit,
        "implicit_uv_faces": implicit,
        "bound_png_faces": bound,
        "unbound_template_faces": unbound,
        "slot_count": len(slots),
    }


def state_model_options(data: dict) -> list[str]:
    if ("variants" in data) == ("multipart" in data):
        raise ValueError("Blockstate must contain exactly one of variants/multipart")
    if "variants" in data:
        items = list(data["variants"].values())
    else:
        items = [x["apply"] for x in data["multipart"]]
    options = []
    for item in items:
        for option in (item if isinstance(item, list) else [item]):
            ref = option.get("model")
            if not isinstance(ref, str):
                raise ValueError("Blockstate option missing model string")
            options.append(ref)
    return options


def compare_model(row, calculated):
    mapping = [
        ("C_applied_faces", "applied_faces"),
        ("C_explicit_uv_faces", "explicit_uv_faces"),
        ("C_implicit_uv_key_absent_faces", "implicit_uv_faces"),
        ("C_bound_png_face_refs", "bound_png_faces"),
        ("C_template_unbound_face_refs", "unbound_template_faces"),
        ("C_binding_rows", "slot_count"),
    ]
    differences = []
    for original, computed in mapping:
        if int(row[original]) != int(calculated[computed]):
            differences.append(f"{original}:old={row[original]}:new={calculated[computed]}")
    return differences


def audit(root: Path):
    crows = read_csv(root / C_LEDGER)
    grows = read_csv(root / G_LEDGER)
    assert len(crows) == 2390
    assert len(grows) == 4669
    paths = {r["path"]: r for r in grows}
    model_paths = {p for p, r in paths.items() if r["type"] == "BLOCK_MODEL_JSON"}
    state_paths = {p for p, r in paths.items() if r["type"] == "BLOCKSTATE_JSON"}
    png_paths = {p for p, r in paths.items() if r["type"] == "BLOCK_TEXTURE_PNG"}
    assert (len(model_paths), len(state_paths), len(png_paths)) == (2390, 1168, 1111)

    models, states = {}, {}
    for path in sorted(model_paths | state_paths):
        raw = (root / path).read_bytes()
        if raw_blob_sha(raw) != paths[path]["sha"]:
            raise ValueError(f"{path}: original hash differs from G")
        obj = strict_json(raw, path)
        if not isinstance(obj, dict):
            raise ValueError(f"{path}: non-object JSON")
        (models if path in model_paths else states)[path] = obj

    rows_out = []
    tally = Counter()
    discrepancies = []
    for row in crows:
        path = row["source_path"]
        if path not in models:
            raise ValueError(f"C model absent from original G: {path}")
        if row["git_blob_sha"] != paths[path]["sha"]:
            raise ValueError(f"C/G model SHA disagreement: {path}")
        if row["C_assignment"] == "E_EXCEPTION":
            tally["e_exception"] += 1
            # C intentionally records 0 for E-owned special renderers.
            measurements = dict.fromkeys(COLUMNS[2:10], 0)
            measurements["geometry_provider"] = ""
            measurements["slot_count"] = 0
            differences = [] if all(int(row[k]) == 0 for k in (
                "C_applied_faces", "C_explicit_uv_faces", "C_implicit_uv_key_absent_faces",
                "C_bound_png_face_refs", "C_template_unbound_face_refs", "C_binding_rows")) else ["E_EXCEPTION_nonzero_C_measurement"]
            label = "E_OUT_OF_STATIC_SCOPE"
        else:
            tally["c_direct"] += 1
            measurements = source_faces(path, models, png_paths)
            for k in ("elements", "applied_faces", "explicit_uv_faces", "implicit_uv_faces",
                      "bound_png_faces", "unbound_template_faces"):
                tally[k] += measurements[k]
            differences = compare_model(row, measurements)
            label = "PASS" if not differences else "DIFFERENCE"
        if differences:
            discrepancies.append({"path": path, "differences": differences})
        rows_out.append({
            "source_path": path, "c_assignment": row["C_assignment"],
            **measurements, "comparison": label, "differences": "|".join(differences),
        })
    assert tally["c_direct"] + tally["e_exception"] == 2390

    option_count, used_models = 0, set()
    by_style = Counter()
    invalid_state_refs = []
    for path, obj in states.items():
        options = state_model_options(obj)
        by_style["variants" if "variants" in obj else "multipart"] += 1
        option_count += len(options)
        for ref in options:
            model_path = block_model_path(ref)
            if model_path is None or model_path not in models:
                invalid_state_refs.append({"blockstate": path, "model_ref": ref})
            else:
                used_models.add(model_path)
    expected_c = {
        "c_direct": 2304,
        "e_exception": 86,
        "elements": 5689,
        "applied_faces": 23090,
        "explicit_uv_faces": 18808,
        "implicit_uv_faces": 4282,
        "bound_png_faces": 21590,
        "unbound_template_faces": 1500,
    }
    actual_c = {key: tally[key] for key in expected_c}
    expected_d = {"declared_model_options": 7592, "unique_referenced_models": 2136}
    actual_d = {"declared_model_options": option_count, "unique_referenced_models": len(used_models)}

    report = {
        "schema": "MCFR_INT2_MODEL_CROSSCHECK/v1",
        "baseline_commit": "176f7f34de2336eb7984c4734e97b6eb156c19f4",
        "compared_to": [C_LEDGER, G_LEDGER, D_CONTRACT],
        "per_model_rows": len(rows_out),
        "C_computed": actual_c,
        "C_expected": expected_c,
        "C_per_model_discrepancies": len(discrepancies),
        "C_discrepancy_examples": discrepancies[:40],
        "D_computed": actual_d,
        "D_expected": expected_d,
        "D_state_types": dict(by_style),
        "D_unresolved_model_refs": len(invalid_state_refs),
        "D_unresolved_model_ref_examples": invalid_state_refs[:20],
        "not_recomputed": [
            "D_9193_syntactic_state_case_enumeration",
            "D_19440_state_model_option_instances",
            "full_3D_rotated_AABB", "blockstate_transform_baked_quads",
            "implicit_UV_numeric_coordinates", "texture_RGBA", "in_game_rendering",
            "official_distribution_authentication",
        ],
        "ai_training_approved": False,
    }
    aggregated_mismatch = [
        key for key in expected_c if actual_c[key] != expected_c[key]
    ] + [key for key in expected_d if actual_d[key] != expected_d[key]]
    if discrepancies or aggregated_mismatch or invalid_state_refs:
        report["status"] = "DISCREPANCY_REQUIRES_REVIEW"
        report["aggregate_mismatches"] = aggregated_mismatch
    else:
        report["status"] = "PASS_SOURCE_GEOMETRY_UV_DECLARATIONS_AND_STATE_OPTIONS"
    return rows_out, report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--show-csv", action="store_true", help="Also print all per-model rows")
    args = p.parse_args()
    rows, report = audit(args.root)
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / REPORT_NAME).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    (args.out / "INT2_1_2_STRUCTURE_SUMMARY.json").write_text(
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8",
    )
    print("INT2_STRUCTURE_SUMMARY_JSON:" + json.dumps(report, ensure_ascii=False, sort_keys=True))
    if args.show_csv:
        print("INT2_MODEL_CSV_BEGIN")
        print((args.out / REPORT_NAME).read_text(encoding="utf-8"), end="")
        print("INT2_MODEL_CSV_END")
    if report["status"] != "PASS_SOURCE_GEOMETRY_UV_DECLARATIONS_AND_STATE_OPTIONS":
        raise SystemExit("INT-2 geometry/UV audit discrepancies: see JSON report")


if __name__ == "__main__":
    main()
