"""INT-2 independent 1-2-B element coordinates, rotations and AABB math audit.

Two independent methods are used for the rotated axis-aligned bounds:
(1) rotate all 8 box corners, (2) transformed centre plus absolute-matrix
half-extents. Rechecks B historical per-element source coordinates and
rotation flags. This is *element JSON rotation only*, not baked blockstate
x/y transforms, engine runtime geometry, collision shape or visuals.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
C_SCOPE = "research/vanilla_models/phase_1-2-C/entry5/C_SCOPE_2390_FINAL_STATUS.csv"
G_SCOPE = "research/vanilla_models/phase_1-2-G/final/G_FINAL_SOURCE_SHA_4669.csv"
B_FILES = tuple(
    f"research/vanilla_models/phase_1-2-B/entry10/ELEMENTS_P{idx}_ALL.csv"
    for idx in (1, 2, 3)
)
FIELDS = (
    "leaf_path", "provider_path", "element_index", "rotation_axis",
    "angle_degrees", "rescale", "source_from", "source_to", "rotation_origin",
    "bbox_min", "bbox_max", "cross_method_max_abs_error", "prior_B_check",
)
TOLERANCE = 1e-9


def get_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def git_sha(content):
    return hashlib.sha1(b"blob " + str(len(content)).encode() + bytes([0]) + content).hexdigest()


def model_path(ref):
    ns, sep, name = ref.partition(":")
    if not sep:
        ns, name = "minecraft", ns
    if ns != "minecraft" or not name.startswith("block/"):
        raise ValueError(f"Non-vanilla block parent {ref!r}")
    return "1.21.11/assets/minecraft/models/" + name + ".json"


def walk(start, models):
    seen = set()
    path = start
    while True:
        if path in seen:
            raise ValueError(f"Parent cycle: {start}")
        if path not in models:
            raise ValueError(f"Missing parent: {path}")
        seen.add(path)
        yield path
        parent = models[path].get("parent")
        if not parent:
            return
        path = model_path(parent)


def geometry_provider(start, models):
    for path in walk(start, models):
        if "elements" in models[path]:
            return path
    return ""


def _real_numbers(values, name):
    if not isinstance(values, list) or len(values) != 3:
        raise ValueError(f"Invalid coordinate {name}: {values!r}")
    if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) for v in values):
        raise ValueError(f"Nonfinite/non-numeric {name}: {values}")
    return tuple(float(v) for v in values)


def affine(rotation):
    if not rotation:
        return ((1., 0., 0.), (0., 1., 0.), (0., 0., 1.)), (0., 0., 0.), "", 0., False
    angle = float(rotation["angle"])
    axis = rotation["axis"]
    if axis not in {"x", "y", "z"} or not math.isfinite(angle):
        raise ValueError(f"Invalid element rotation: {rotation}")
    pivot = _real_numbers(rotation["origin"], "rotation origin")
    rad = math.radians(angle)
    c, s = math.cos(rad), math.sin(rad)
    rescale = bool(rotation.get("rescale", False))
    if rescale and abs(c) < 1e-10:
        raise ValueError("Unsupported singular rescale at near-90-degree rotation")
    factor = 1. / c if rescale else 1.
    if axis == "x":
        matrix = ((1.,0.,0.), (0.,c*factor,-s*factor), (0.,s*factor,c*factor))
    elif axis == "y":
        matrix = ((c*factor,0.,s*factor), (0.,1.,0.), (-s*factor,0.,c*factor))
    else:
        matrix = ((c*factor,-s*factor,0.), (s*factor,c*factor,0.), (0.,0.,1.))
    return matrix, pivot, axis, angle, rescale


def corner_bounds(from_xyz, to_xyz, rotation):
    """Directly rotate each corner around the declared origin."""
    lo = tuple(min(a, b) for a, b in zip(from_xyz, to_xyz))
    hi = tuple(max(a, b) for a, b in zip(from_xyz, to_xyz))
    m, pivot, _, _, _ = affine(rotation)
    corners = []
    for vertex in itertools.product(*[(lo[i], hi[i]) for i in range(3)]):
        local = [vertex[j]-pivot[j] for j in range(3)]
        corners.append(tuple(pivot[i] + sum(m[i][j]*local[j] for j in range(3)) for i in range(3)))
    return tuple(min(p[i] for p in corners) for i in range(3)), tuple(max(p[i] for p in corners) for i in range(3))


def center_extents_bounds(from_xyz, to_xyz, rotation):
    """Independent closed-form AABB from affine centre and half extents."""
    lo = tuple(min(a, b) for a, b in zip(from_xyz, to_xyz))
    hi = tuple(max(a, b) for a, b in zip(from_xyz, to_xyz))
    center = [(lo[i]+hi[i])/2. for i in range(3)]
    half = [(hi[i]-lo[i])/2. for i in range(3)]
    m, pivot, _, _, _ = affine(rotation)
    c2 = [pivot[i]+sum(m[i][j]*(center[j]-pivot[j]) for j in range(3)) for i in range(3)]
    h2 = [sum(abs(m[i][j])*half[j] for j in range(3)) for i in range(3)]
    return tuple(c2[i]-h2[i] for i in range(3)), tuple(c2[i]+h2[i] for i in range(3))


def audit(root):
    c = get_csv(root / C_SCOPE)
    g = get_csv(root / G_SCOPE)
    if len(c) != 2390 or len(g) != 4669:
        raise ValueError("Unexpected original model/asset denominator")
    models = {}
    g_by_path = {r["path"]: r for r in g if r["type"] == "BLOCK_MODEL_JSON"}
    for p, row in g_by_path.items():
        raw = (root / p).read_bytes()
        if git_sha(raw) != row["sha"]:
            raise ValueError(f"Model bytes differ from G: {p}")
        obj = json.loads(raw)
        if not isinstance(obj, dict):
            raise ValueError(f"Invalid model root: {p}")
        models[p] = obj
    original_records = {}
    for file in B_FILES:
        for record in get_csv(root / file):
            key = (record["leaf_path"], int(record["element_index"]))
            if key in original_records:
                raise ValueError(f"Historical duplicate element key: {key}")
            original_records[key] = record

    tally = Counter()
    diffs = []
    rotation_evidence = []
    observed_keys = set()
    for record in c:
        path = record["source_path"]
        if record["C_assignment"] == "E_EXCEPTION":
            tally["e_exceptions"] += 1
            continue
        tally["static_models"] += 1
        provider = geometry_provider(path, models)
        if not provider:
            raise ValueError(f"C model without geometry provider: {path}")
        elements = models[provider].get("elements", [])
        if not isinstance(elements, list):
            raise ValueError(f"Non-list elements for {provider}")
        for index, element in enumerate(elements):
            key = (path, index)
            observed_keys.add(key)
            prior = original_records.get(key)
            if prior is None:
                if len(diffs) < 100:
                    diffs.append({"leaf_path": path, "element_index": index, "reason": "MISSING_B_ELEMENT"})
                continue
            if prior["provider_path"] != provider:
                if len(diffs) < 100:
                    diffs.append({"leaf_path": path, "element_index": index, "reason": "PROVIDER_MISMATCH"})
            low = _real_numbers(element.get("from"), "from")
            high = _real_numbers(element.get("to"), "to")
            has_rotation = "rotation" in element
            rotation = element.get("rotation") if has_rotation else None
            face_count = len(element.get("faces", {}))
            verified = (
                json.loads(prior["raw_from"]) == element["from"]
                and json.loads(prior["raw_to"]) == element["to"]
                and prior["rotation_present"].lower() == str(has_rotation).lower()
                and int(prior["face_count"]) == face_count
                and prior["provider_path"] == provider
                and (not has_rotation or json.loads(prior["rotation_raw_json"]) == rotation)
            )
            if not verified and len(diffs) < 100:
                diffs.append({"leaf_path": path, "element_index": index, "reason": "B_SOURCE_ELEMENT_DIFFERENCE"})
            tally["elements"] += 1
            tally["faces"] += face_count
            tally["elements_matching_B"] += int(verified)
            tally["rotation_elements"] += int(has_rotation)
            tally["zero_thickness_elements"] += int(any(a == b for a, b in zip(low, high)))
            tally["inverted_coordinate_elements"] += int(any(a > b for a, b in zip(low, high)))
            tally["outside_0_16_elements"] += int(any(x < 0 or x > 16 for x in (*low, *high)))
            if has_rotation:
                a, b = corner_bounds(low, high, rotation)
                cmin, cmax = center_extents_bounds(low, high, rotation)
                delta = max(abs(a[i]-cmin[i]) for i in range(3))
                delta = max(delta, *(abs(b[i]-cmax[i]) for i in range(3)))
                tally["aabb_cross_methods_pass"] += int(delta <= TOLERANCE)
                if delta > TOLERANCE and len(diffs) < 100:
                    diffs.append({"leaf_path":path, "element_index":index,"reason":"ROTATED_AABB_METHOD_DISAGREEMENT","error":delta})
                matrix, origin, axis, angle, rescale = affine(rotation)
                rotation_evidence.append({
                    "leaf_path": path, "provider_path": provider,
                    "element_index": index, "rotation_axis": axis,
                    "angle_degrees": angle, "rescale": rescale,
                    "source_from": json.dumps(element["from"], separators=(",",":")),
                    "source_to": json.dumps(element["to"], separators=(",",":")),
                    "rotation_origin": json.dumps(origin, separators=(",",":")),
                    "bbox_min": json.dumps(a, separators=(",",":")),
                    "bbox_max": json.dumps(b, separators=(",",":")),
                    "cross_method_max_abs_error": f"{delta:.14g}",
                    "prior_B_check": "PASS" if verified else "DIFFERENCE",
                })
    extra_old = set(original_records) - observed_keys
    expected = {
        "static_models": 2304, "e_exceptions": 86,
        "elements": 5689, "faces": 23090,
        "rotation_elements": 1548,
        "zero_thickness_elements": 1965,
        "inverted_coordinate_elements": 18,
        "outside_0_16_elements": 413,
        "elements_matching_B": 5689,
        "aabb_cross_methods_pass": 1548,
    }
    actual = {key: tally[key] for key in expected}
    mismatch = {k:{"computed":actual[k],"expected":v} for k,v in expected.items() if actual[k] != v}
    result = {
        "schema": "MCFR_INT2_B_ROTATION_AABB/v1",
        "baseline_sha": "176f7f34de2336eb7984c4734e97b6eb156c19f4",
        "scope": "source-element-coordinate-matching and mathematical-rotated-AABB-internal-consistency",
        "expected": expected, "observed": actual,
        "historical_element_rows": len(original_records),
        "original_history_extra_element_keys": len(extra_old),
        "mismatched_denominators": mismatch,
        "discrepancy_examples": diffs,
        "not_verified": [
            "Minecraft renderer baked mesh positions",
            "blockstate x/y transforms and uvlock",
            "in-game collision/VoxelShapes",
            "numeric UV atlas rasterisation",
            "render screenshots and runtime",
        ],
        "ai_training_approved": False,
    }
    result["status"] = "PASS_B_ELEMENT_EVIDENCE_AND_DUAL_AABB_MATH" if not mismatch and not diffs and not extra_old else "DIFFERENCE_REQUIRES_INVESTIGATION"
    return rotation_evidence, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--print-csv", action="store_true", help="Print rotated element rows once for archiving")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    items, report = audit(args.root)
    output = args.out / "INT2_B_ROTATED_ELEMENTS.csv"
    with output.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(items)
    (args.out / "INT2_B_ROTATION_SUMMARY.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print("INT2_B_RESULT:" + json.dumps(report, ensure_ascii=False, sort_keys=True))
    if args.print_csv:
        print("INT2_B_CSV_BEGIN")
        print(output.read_text(encoding="utf-8"), end="")
        print("INT2_B_CSV_END")
    if report["status"] != "PASS_B_ELEMENT_EVIDENCE_AND_DUAL_AABB_MATH":
        raise SystemExit("INT-2 B source/AABB discrepancy; consult report")


if __name__ == "__main__":
    main()
