"""Recompute the 1-5 runtime tables from the two captured game client outputs."""
import csv
import hashlib
import io
import json
import lzma
import math
import struct
from collections import Counter
from pathlib import Path
import sys
from zipfile import ZipFile

from run_comparison_probe import input_rows, targets

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
VERSIONS = ("1.21.1", "1.21.11")
BED_PNG = "assets/minecraft/textures/entity/bed/white.png"


def vertices(value):
    return [tuple(float(num) for num in vertex.split(",")) for vertex in value.split(";")]


def bounds(points):
    return [round(fn(p[axis] for p in points), 6)
            for fn in (min, max) for axis in range(3)]


def spans(points):
    box = bounds(points)
    return [round(box[i + 3] - box[i], 6) for i in range(3)]


def read_engine():
    data = {}
    sizes = {}
    for version in VERSIONS:
        raw = lzma.decompress((HERE / f"ENGINE_{version}.tsv.xz").read_bytes())
        rows = list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
        expected = {(kind, case) for kind, case, *_ in targets(version)}
        assert expected <= {(r["kind"], r["case"]) for r in rows}
        keys = [(r["kind"], r["case"], r["key"]) for r in rows]
        assert len(keys) == len(set(keys))
        assert not set(keys) & data.keys()
        data.update(zip(keys, (row["value"] for row in rows), strict=True))
        sizes[version] = {"rows": len(rows), "sha256": hashlib.sha256(raw).hexdigest()}
    return data, sizes


def write_csv(name, fields, rows):
    with (HERE / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)


def main(jar_path):
    engine, captures = read_engine()

    def group(kind, case):
        return {key: value for (k, c, key), value in engine.items() if k == kind and c == case}

    def quads(case):
        for key, value in group("QUAD", case).items():
            direction, sprite, tint, frames, points = value.split("|")
            yield key.split("/")[0], direction, sprite, int(tint), int(frames), vertices(points)

    base_cases = [r["case"] for r in input_rows(PHASE / "B/CASES.csv")]
    assert len(base_cases) == 62 and all(group("BLOCK", c)["registry"] != "NOT_REGISTERED" for c in base_cases)
    for case in base_cases:
        for *_, points in quads(case):
            assert len(points) == 4 and all(len(v) == 5 and all(map(math.isfinite, v)) for v in points)
    for case in ("V01", "V02", "S01"):
        assert all(-0.01 <= n <= 1.01 for *_, points in quads(case) for v in points for n in v[3:])

    with ZipFile(jar_path) as archive:
        png = archive.read(BED_PNG)
    width, height = struct.unpack(">II", png[16:24])
    assert (width, height) == (64, 64)
    bed_rows = []
    bed_points = []
    for part in ("foot", "head"):
        for name, value in group("BED", part).items():
            for idx, (x, y, z, u, v) in enumerate(vertices(value)):
                wx, wy, wz = (round(n, 6) for n in (x, y, z - (part == "head")))
                bed_points.append((wx, wy, wz))
                bed_rows.append((part, name, idx, wx, wy, wz, round(u * width, 6), round(v * height, 6)))
    assert len(bed_rows) == 144
    body = [(x, y, z - (case == "S38")) for case in ("S37", "S38")
            for *_, points in quads(case) for x, y, z, _, _ in points]
    def placed_faces(case, include_sprite):
        z_offset = int(case == "S38")
        return Counter((sprite if include_sprite else "", tuple(sorted(
            (round(x, 5), round(y, 5), round(z - z_offset, 5)) for x, y, z, _, _ in points)))
            for _, _, sprite, _, _, points in quads(case))

    bed_overlap = sum((placed_faces("S37", False) & placed_faces("S38", False)).values())
    bed_same_sprite = sum((placed_faces("S37", True) & placed_faces("S38", True)).values())
    assert (bed_overlap, bed_same_sprite) == (6, 0)
    assert group("ITEM", "ITEM_WHITE_BED")["special_0"] == "net.minecraft.class_10500"
    write_csv("WHITE_BED_VERTICES.csv", ("part", "quad", "vertex", "block_x", "block_y", "block_z",
                                          "texture_u_px", "texture_v_px"), bed_rows)

    shape = {case: {"span": spans([v for *_, ps in quads(case) for v in ps]),
                    "quads": sum(1 for _ in quads(case))}
             for case in base_cases if list(quads(case))}
    states = ("S44", "S45")
    lamps = [[int(group("BLOCK", f"LAMP_{level}_{lit}")["emission"]) for lit in ("false", "true")]
             for level in range(1, 4)]
    assert lamps == [[0, 5], [0, 10], [0, 15]]

    def face_signatures(case):
        return Counter((side, face, sprite, tuple(sorted(tuple(round(n, 5) for n in v) for v in points)))
                       for side, face, sprite, _, _, points in quads(case))

    a, b = map(face_signatures, states)
    lamp_changed = {key[1] for key in (a - b)}
    assert lamp_changed == {"north", "east", "south", "west"} and sum((a-b).values()) == 4
    rotations = {case: sum((face_signatures(case) - face_signatures(case + "_EAST")).values())
                 for case in ("V01", "V03", "V08", "S35", "S36")}
    assert all(rotations.values())
    pairs = {}
    for first, second in (("V12", "V13"), ("S42", "S43")):
        differences = face_signatures(second) - face_signatures(first)
        assert sum(differences.values()) == 1
        sprite = next(iter(differences))[2]
        pairs[second] = [{"sprite": resource, "tint_index": tint, "frames": frames,
                          "y_blocks": sorted({v[1] for v in points})}
                         for _, _, resource, tint, frames, points in quads(second) if sprite == resource]
    exposures = input_rows(PHASE / "D/TEXTURE_EXPOSURE.csv")
    sprite_readback = Counter()
    exposure_rows = []
    for r in exposures:
        actual = group("SPRITE", "T" + r["texture_id"])
        matched = actual["id"] == r["resource_id"]
        sprite_readback[(r["finding"], matched)] += 1
        exposure_rows.append((r["texture_id"], r["finding"], r["resource_id"], actual["id"], actual["frame_count"]))
    assert sum(sprite_readback.values()) == 85
    assert sum(v for (kind, matched), v in sprite_readback.items() if "MISSING" in kind and not matched) == 8
    write_csv("ATLAS_READBACK.csv", ("texture_id", "finding", "requested", "actual", "frames"), exposure_rows)

    summary = {
        "captures": captures,
        "fixed_case_count": len(base_cases),
        "vanilla_bed": {"cuboids": len({(r[0], r[1].rsplit("/", 1)[0]) for r in bed_rows}),
                        "quads": len(bed_rows) // 4, "bounds": bounds(bed_points), "span": spans(bed_points),
                        "uv_px_bounds": [fn(r[k] for r in bed_rows) for fn in (min, max) for k in (6, 7)],
                        "png": BED_PNG, "png_size": [width, height], "sha256": hashlib.sha256(png).hexdigest()},
        "hc_bed": {"bounds": bounds(body), "span": spans(body),
                   "quads": {case: shape[case]["quads"] for case in ("S37", "S38")},
                   "coincident_geometry_quads": bed_overlap, "coincident_same_sprite_quads": bed_same_sprite},
        "lamp_emission": lamps,
        "lamp_changed_uv_faces": sorted(lamp_changed),
        "water_surfaces": pairs,
        "rotated_faces_from_original": rotations,
        "changed_open_faces": {f"{first}:{second}":
                               sum((face_signatures(first) - face_signatures(second)).values())
                               for first, second in (("V05", "V06"), ("S20", "S21"))},
        "chair_mesh_variant_1_equals_3": {case: face_signatures(case) == face_signatures(case + "_VAR1")
                                          for case in ("S03", "S04")},
        "atlas": {f"{finding}:{'same_id' if match else 'fallback'}": count
                  for (finding, match), count in sorted(sprite_readback.items())},
        "four_unresolved_state_options": {"branches": 4, "case_registry": {
            case: group("BLOCK", case).get("registry")
            for case in ("REG_unused/white_awning", "REG_stone_tombstone", "REG_service_bell")}},
        "baked_shapes": shape,
    }
    check_counts = Counter(row["status"] for row in input_rows(HERE / "RUNTIME_VERIFICATION.csv"))
    assert sum(check_counts.values()) == 10
    summary["runtime_check_counts"] = dict(check_counts)
    (HERE / "SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
                                      encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
