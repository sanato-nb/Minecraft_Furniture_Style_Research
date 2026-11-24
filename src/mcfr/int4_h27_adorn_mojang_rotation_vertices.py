"""H27: original Mojang 1.21.11 element and blockstate model vertex rotations.

Invoke official compiled Variant.SimpleModelState, BlockElementRotation,
Transformation and FaceBakery.rotateVertexBy on 136 selected source elements.
This is NOT a full baked quad: face windings, UV lock, atlas and F2 remain unproved.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from zipfile import ZipFile

from . import int4_h25_adorn_release_source as h25
from . import int4_h26_adorn_mojang_default_uv as h26
from . import int4_h20_v11_bed_mesh_uv as h20

ROOT = Path(__file__).resolve().parents[2]
I = ROOT / "project/integration"
OUTPUT = I / "INT4_H27_ADORN_ORIGINAL_MOJANG_ROTATED_VERTICES_V1.json"
CASES_CSV = I / "INT4_H27_ADORN_21_STATE_ROTATED_BOUNDS_V1.csv"
PROBE = ROOT / "tools/research/H27MojangElementStateRotationProbe.java"
PARENT_JSON_BLOB = "e7dbb1c17e4fa9bd8f6b4cc7d09e0282c4c739ab"
PARENT_CSV_BLOB = "e722131593a883f713f300eefc8846b06f4766a7"
CSV_COLUMNS = (
    "case_id", "block", "state", "selected_model_applications",
    "source_elements", "source_faces", "source_uv_face_records",
    "source_y_rotations", "original_element_rotations", "rotated_corners",
    "bbox_min_x", "bbox_min_y", "bbox_min_z", "bbox_max_x", "bbox_max_y", "bbox_max_z",
    "source_provenance", "original_full_quad_bake", "native_F2_verified"
)
ORIGINAL_CLASSES = {
    "bakery": "net.minecraft.client.renderer.block.model.FaceBakery",
    "variant": "net.minecraft.client.renderer.block.model.Variant$SimpleModelState",
    "quadrant": "com.mojang.math.Quadrant",
    "model_state": "net.minecraft.client.resources.model.ModelState",
    "transformation": "com.mojang.math.Transformation",
    "element_rotation": "net.minecraft.client.renderer.block.model.BlockElementRotation",
    "single_axis": "net.minecraft.client.renderer.block.model.BlockElementRotation$SingleAxisRotation",
    "axis": "net.minecraft.core.Direction$Axis",
}


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError("H27 original Minecraft rotation: " + message)


def official_mapping(mapping_text: str) -> dict:
    sections = {}
    for k, name in ORIGINAL_CLASSES.items():
        obf, members = h26.mapped_section(mapping_text, name)
        sections[k] = {"class": obf, "members": members}
    def method(kind, original, args):
        return h26.mapped_member(sections[kind]["members"], original, args)
    def field(kind, name):
        return h26.mapped_member(sections[kind]["members"], name)
    values = {
        "classes": {k: v["class"] for k, v in sections.items()},
        "rotate_vertex_by": method("bakery", "rotateVertexBy",
                                   "(org.joml.Vector3f,org.joml.Vector3fc,org.joml.Matrix4fc)"),
        "block_center_field": field("bakery", "BLOCK_MIDDLE"),
        "variant_as_model_state": method("variant", "asModelState", "()"),
        "model_state_transformation": method("model_state", "transformation", "()"),
        "transformation_matrix": method("transformation", "getMatrix", "()"),
        "element_transform": method("element_rotation", "transform", "()"),
        "quadrant_fields": [
            field("quadrant", "R" + str(x)) for x in (0, 90, 180, 270)
        ],
        "element_axis_fields": [field("axis", x) for x in ("X", "Y", "Z")],
    }
    require(len(set(values["quadrant_fields"])) == 4, "original Quadrant names ambiguous")
    require(len(set(values["element_axis_fields"])) == 3, "original Axis names ambiguous")
    for cls, method_name in (
        ("variant", "asModelState"),
        ("element_rotation", "transform"),
        ("bakery", "rotateVertexBy"),
    ):
        require(values["classes"][cls] and method_name, "Mojang class mapping incomplete")
    return values


def load_parent() -> tuple[dict, dict]:
    p = I / "INT4_H26_ADORN_MOJANG_DEFAULT_UV_RESULT_V1.json"
    c = I / "INT4_H26_ADORN_139_ORIGINAL_SOURCE_FACE_UV_V1.csv"
    require(h25.git_blob(p.read_bytes()) == PARENT_JSON_BLOB, "parent H26 JSON source drift")
    require(h25.git_blob(c.read_bytes()) == PARENT_CSV_BLOB, "parent H26 face CSV source drift")
    old = json.loads(p.read_text(encoding="utf-8"))
    h26.verify_face_csv(old)
    require(old["counts"]["source_unique_faces"] == 139 and
            old["counts"]["source_unique_mojang_default_uv_faces"] == 107 and
            old["counts"]["state_weighted_original_mojang_default_uv"] == 400,
            "H26 source UV counts differ")
    h25data = h26.load_h25()
    require(old["preserved_approvals"] == h25data["legacy_gates_unchanged"],
            "H25/H26 approval boundary changed")
    return old, h25data


def source_elements(h26result: dict, h25result: dict, adorn_jar: Path) -> dict:
    require(hashlib.sha256(adorn_jar.read_bytes()).hexdigest() == h25.RELEASE_SHA256,
            "official Adorn release JAR SHA changed")
    original = h26result["five_model_unique_source_faces"]
    indexed = {x["id"]: x for x in original}
    require(len(original) == len(indexed) == 139, "H26 face IDs not unique")
    with ZipFile(adorn_jar) as z:
        require(z.testzip() is None, "Adorn archive CRC failed")
        observed = h26.original_model_faces(z, h25result)
    require(len(observed) == 139, "official Adorn face count changed")
    grouped = {}
    for face in observed:
        parent = indexed[face["id"]]
        for k in ("model", "geometry_provider", "element", "direction", "from",
                  "to", "texture", "element_rotation_declaration"):
            require(face[k] == parent[k], "source face provenance differs " + face["id"] + " " + k)
        model = face["model"]
        element = face["element"]
        slot = grouped.setdefault(model, {})
        old = slot.get(element)
        payload = {
            "element_index": element,
            "from": face["from"],
            "to": face["to"],
            "original_element_rotation": face["element_rotation_declaration"],
        }
        if old is not None:
            require(old == payload, "source element varies between original faces")
        slot[element] = payload
    out = {m: [d[k] for k in sorted(d)] for m, d in grouped.items()}
    require(len(out) == 5 and sum(len(v) for v in out.values()) == 29,
            "5 original source models must have 29 unique elements")
    require([len(out[m]) for m in h25.MODELS] == [12, 3, 3, 3, 8],
            "Adorn five model source elements differ")
    for m in out:
        for i, element in enumerate(out[m]):
            require(element["element_index"] == i, "source element index not contiguous")
    return out


def build_selected_elements(h25result: dict, elements: dict) -> tuple[list[dict], list[dict]]:
    by_case, selected = [], []
    for ci, case in enumerate(h25result["selected_state_cases"], start=1):
        cid = "ADORN" + str(ci).zfill(2)
        ids = []
        for ai, app in enumerate(case["selected"]):
            require(app["model"] in elements and app["y"] in (0, 90, 180, 270),
                    "H25 exact selected model/state rotation changed")
            require(app["uvlock"] is False, "H27 untested UV-lock state")
            require(len(elements[app["model"]]) == app["source_elements"],
                    "selected model element count differs")
            for e in elements[app["model"]]:
                rotation = e["original_element_rotation"]
                if rotation is None:
                    axis, angle, origin, rescale = "none", 0, [0, 0, 0], False
                else:
                    axis = rotation["axis"]
                    angle = rotation["angle"]
                    origin = rotation["origin"]
                    rescale = rotation.get("rescale", False)
                    require(axis in ("x", "y", "z") and len(origin) == 3,
                            "unsupported original element rotation declaration")
                id = "C" + str(ci).zfill(2) + "A" + str(ai) + "E" + str(e["element_index"])
                d = dict(
                    id=id, case_id=cid, model=app["model"],
                    model_application_index=ai, element_index=e["element_index"],
                    source_from=e["from"], source_to=e["to"],
                    state_y_degrees=app["y"], uvlock=False,
                    element_rotation_axis=axis,
                    element_rotation_angle_degrees=angle,
                    element_rotation_origin=origin,
                    element_rotation_rescale=bool(rescale),
                )
                selected.append(d)
                ids.append(id)
        by_case.append({
            "case_id": cid, "block": case["block"], "state": case["state"],
            "selected_models": [x["model"] for x in case["selected"]],
            "model_applications": len(case["selected"]),
            "source_elements": case["sum_source_elements"],
            "source_faces": case["sum_source_faces"],
            "source_y_rotations": [x["y"] for x in case["selected"]],
            "element_ids": ids,
        })
    require(len(by_case) == 21 and len(selected) == 136 and
            len({x["id"] for x in selected}) == 136,
            "21 states must select exactly 136 original element instances")
    require(sum(x["element_rotation_axis"] != "none" for x in selected) == 8,
            "four iron shelves must reuse two -45 degree rotated elements")
    require(all(x["element_rotation_axis"] == "z" and
                x["element_rotation_angle_degrees"] == -45 and
                not x["element_rotation_rescale"]
                for x in selected if x["element_rotation_axis"] != "none"),
            "original Adorn shelf -45 Z element rotations drift")
    require(sum(c["model_applications"] for c in by_case) == 29 and
            sum(c["source_faces"] for c in by_case) == 656,
            "H25 model applications or 21-state source face counts changed")
    return by_case, selected


def native_arguments(mapping: dict) -> list[str]:
    c = mapping["classes"]
    return [
        c["bakery"], mapping["rotate_vertex_by"], c["variant"], c["quadrant"],
        c["model_state"], c["transformation"], c["element_rotation"],
        c["single_axis"], c["axis"], mapping["variant_as_model_state"],
        mapping["model_state_transformation"], mapping["transformation_matrix"],
        mapping["element_transform"], ",".join(mapping["quadrant_fields"]),
        ",".join(mapping["element_axis_fields"]), mapping["block_center_field"],
    ]


def run_original_mojang_jvm(selected: list[dict], client: Path,
                            mapping: dict, libpaths: list[str]) -> tuple[dict, dict]:
    fields = []
    for s in selected:
        fields.append(s["id"] + "\t" + "\t".join(str(v).lower() for v in (
            s["state_y_degrees"], s["uvlock"],
            *s["source_from"], *s["source_to"],
            s["element_rotation_axis"], s["element_rotation_angle_degrees"],
            *s["element_rotation_origin"], s["element_rotation_rescale"],
        )))
    require(all(len(x.split("\t")) == 15 for x in fields),
            "original Mojang rotation probe TSV schema mismatch")
    with tempfile.TemporaryDirectory(prefix="h27_mojang_jvm_") as td:
        out = Path(td)
        subprocess.run(["javac", "-d", str(out), str(PROBE)],
                       check=True, capture_output=True, text=True, timeout=60)
        cmd = [
            "java", "-cp", str(out) + ":" + str(client) + ":" + ":".join(libpaths),
            "mcfr.research.H27MojangElementStateRotationProbe",
            *native_arguments(mapping),
        ]
        proc = subprocess.run(cmd, input="\n".join(fields) + "\n",
                              capture_output=True, text=True, timeout=150)
        require(proc.returncode == 0, "original Mojang rotations JVM failed: " + proc.stderr[-3500:])
        require("H27_MOJANG_ORIGINAL_ROTATED_ELEMENTS=136" in proc.stderr and
                "H27_MOJANG_ORIGINAL_ROTATED_SHELF_ELEMENTS=8" in proc.stderr,
                "real Mojang element rotation invocation count changed")
    vertices = {}
    for line in proc.stdout.splitlines():
        row = line.split("\t")
        require(row[0] == "VERTICES" and len(row) == 26,
                "original Minecraft vertex response not 8x3 float")
        id = row[1]
        require(id not in vertices, "duplicate official Mojang vertex source")
        verts = [[float(x) for x in row[2+i:5+i]] for i in range(0, 24, 3)]
        require(len(verts) == 8 and all(math.isfinite(v) for corner in verts for v in corner),
                "original Mojang vertex not finite")
        vertices[id] = verts
    require(set(vertices) == {s["id"] for s in selected},
            "JVM did not return all selected original model elements")
    return vertices, {
        "invocations": 136,
        "rotated_source_element_instances": 8,
        "output_source_corners": 1088,
        "original_methods": [
            "Variant.SimpleModelState.asModelState",
            "ModelState.transformation",
            "Transformation.getMatrix",
            "BlockElementRotation.SingleAxisRotation",
            "BlockElementRotation.transform",
            "FaceBakery.rotateVertexBy",
        ],
        "probe_git_blob_sha1": h25.git_blob(PROBE.read_bytes()),
        "not_full_bake_quad": True,
        "not_minecraft_real_game_F2": True,
    }


def summarize_vertices(by_case: list[dict], selected: list[dict], vertices: dict) -> list[dict]:
    index = {r["id"]: r for r in selected}
    for s in selected:
        coords = vertices[s["id"]]
        flat = [v for point in coords for v in point]
        s["original_jvm_rotated_corners_xyz_pixel_units"] = coords
        s["rotated_bounds_min_xyz_pixel_units"] = [min(p[i] for p in coords) for i in range(3)]
        s["rotated_bounds_max_xyz_pixel_units"] = [max(p[i] for p in coords) for i in range(3)]
        require(all(-16.001 < x < 32.001 for x in flat),
                "unexpected world-space transform or impossible unit bounds")
        if s["state_y_degrees"] == 0 and s["element_rotation_axis"] == "none":
            for i, xyz in enumerate(coords):
                source = [
                    s["source_to"][axis] if (i & (1 << axis)) else s["source_from"][axis]
                    for axis in range(3)
                ]
                require(all(math.isclose(a, b, abs_tol=1e-4) for a, b in zip(source, xyz)),
                        "original Mojang zero-state vertex not identical to input source: " + s["id"])
    for c in by_case:
        vs = [p for id in c["element_ids"] for p in vertices[id]]
        require(len(vs) == c["source_elements"] * 8, "selected original corner count mismatch")
        c["rotated_bounds_min_xyz_pixel_units"] = [min(x[i] for x in vs) for i in range(3)]
        c["rotated_bounds_max_xyz_pixel_units"] = [max(x[i] for x in vs) for i in range(3)]
        c["rotated_corners"] = len(vs)
        c["element_rotations_applied"] = sum(index[id]["element_rotation_axis"] != "none"
                                              for id in c["element_ids"])
    return by_case


def audit(args: argparse.Namespace) -> dict:
    h26report, h25report = load_parent()
    manifest = args.version_json.read_bytes()
    require(hashlib.sha1(manifest).hexdigest() == h26.MOJANG_MANIFEST_SHA1,
            "official Mojang version manifest changed")
    meta = json.loads(manifest)
    require(meta["id"] == "1.21.11", "official Minecraft version changed")
    client = args.official_client.read_bytes()
    require(hashlib.sha1(client).hexdigest() == h26.MOJANG_CLIENT_SHA1 and
            hashlib.sha256(client).hexdigest() == h26.MOJANG_CLIENT_SHA256,
            "original Mojang client digest changed")
    mapping_file = args.client_mappings.read_bytes()
    require(hashlib.sha256(mapping_file).hexdigest() == h26.MOJANG_MAPPINGS_SHA256 and
            hashlib.sha1(mapping_file).hexdigest() == meta["downloads"]["client_mappings"]["sha1"],
            "original Mojang mapping digest changed")
    mapping = official_mapping(mapping_file.decode("utf-8"))
    element_models = source_elements(h26report, h25report, args.adorn_jar)
    by_case, selected = build_selected_elements(h25report, element_models)
    with tempfile.TemporaryDirectory(prefix="h27_original_libs_") as td:
        libraries, library_sha = h20.download_libraries(meta, Path(td))
        require(len(libraries) == len(library_sha) == 55,
                "original Mojang 1.21.11 55 library pins not verified")
        vertices, proof = run_original_mojang_jvm(selected, args.official_client, mapping, libraries)
    cases = summarize_vertices(by_case, selected, vertices)
    require(sum(c["rotated_corners"] for c in cases) == 1088,
            "expected 136x8 original source corners")
    require(sum(c["element_rotations_applied"] for c in cases) == 8,
            "original 2 shelf rotations x 4 states not complete")
    require(all(c["element_rotations_applied"] == 0 for c in cases if c["block"] != "adorn:iron_shelf"),
            "unexpected non-shelf source element rotation")
    return {
        "schema": "MCFR_INT4_H27_ORIGINAL_MOJANG_STATE_ELEMENT_ROTATED_VERTICES_V1",
        "original_inputs": {
            "mojang_1_21_11_manifest_sha1": h26.MOJANG_MANIFEST_SHA1,
            "mojang_client_jar_sha256": h26.MOJANG_CLIENT_SHA256,
            "mojang_mapping_sha256": h26.MOJANG_MAPPINGS_SHA256,
            "adorn_761_jar_sha256": h25.RELEASE_SHA256,
            "H26_json_git_blob": PARENT_JSON_BLOB,
            "H26_csv_git_blob": PARENT_CSV_BLOB,
        },
        "official_mojang_original_mapping": mapping,
        "official_jvm_proof": proof,
        "official_mojang_library_sha1": library_sha,
        "selected_state_cases": cases,
        "original_selected_element_vertices": selected,
        "counts": {
            "source_models": len(element_models),
            "source_unique_elements": sum(len(v) for v in element_models.values()),
            "selected_state_cases": len(cases),
            "selected_model_applications": 29,
            "state_weighted_source_element_instances": len(selected),
            "state_weighted_element_rotations": 8,
            "original_jvm_rotated_corners": 1088,
            "previous_H26_unique_source_faces": 139,
            "previous_H26_original_default_uv_calls": 107,
            "previous_H26_state_weighted_source_faces": 656,
            "new_actual_game_runs": 0,
            "new_native_F2": 0,
        },
        "preserved_approvals": h26report["preserved_approvals"],
        "limitations": [
            "Original Mojang Variant state matrix and element transform were executed in isolated JVM.",
            "Original FaceBakery.rotateVertexBy was invoked for 1088 element corner positions.",
            "The original model state selector and element vertices are source-level, not full baked BakedQuad output.",
            "FaceBakery.bakeQuad, face winding/culling, uvlock, atlas coordinates and actual F2 were NOT run.",
            "Recorded corners are in source 0-16 pixel units, not true world-space placed block positions.",
            "No native texture/PNG binary, original Mojang game JAR or Adorn model asset redistributed.",
            "H23 modeling-only F70 70/70 and existing strict F70/H03/H05/INT5/INT6 boundaries unchanged.",
        ],
    }


def csv_rows(report: dict) -> list[dict[str, str]]:
    entries = []
    for c in report["selected_state_cases"]:
        row = {
            "case_id": c["case_id"], "block": c["block"],
            "state": ";".join(k + "=" + str(v).lower() for k, v in sorted(c["state"].items())) or "(default)",
            "selected_model_applications": str(c["model_applications"]),
            "source_elements": str(c["source_elements"]),
            "source_faces": str(c["source_faces"]),
            "source_uv_face_records": str(c["source_faces"]),
            "source_y_rotations": "|".join(str(x) for x in c["source_y_rotations"]),
            "original_element_rotations": str(c["element_rotations_applied"]),
            "rotated_corners": str(c["rotated_corners"]),
            "source_provenance": "OFFICIAL_MOJANG_JVM_ORIGINAL_FACEBAKERY_VERTEX_TRANSFORM",
            "original_full_quad_bake": "false", "native_F2_verified": "false",
        }
        for axis, label in enumerate("xyz"):
            row["bbox_min_" + label] = str(float(c["rotated_bounds_min_xyz_pixel_units"][axis]))
            row["bbox_max_" + label] = str(float(c["rotated_bounds_max_xyz_pixel_units"][axis]))
        entries.append({key: row[key] for key in CSV_COLUMNS})
    return entries


def verify_csv(report: dict, path: Path = CASES_CSV) -> None:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        require(tuple(reader.fieldnames or ()) == CSV_COLUMNS,
                "H27 selected state CSV columns changed")
        rows = list(reader)
    require(rows == csv_rows(report), "H27 stored state model rotations differ from original JVM")
    print("H27_21_STATE_ROTATED_BOUNDS_PERSISTED_CSV_MATCH")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--version-json", type=Path, required=True)
    p.add_argument("--official-client", type=Path, required=True)
    p.add_argument("--client-mappings", type=Path, required=True)
    p.add_argument("--adorn-jar", type=Path, required=True)
    p.add_argument("--output", type=Path, default=OUTPUT)
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    result = audit(a)
    if a.verify:
        require(json.loads(a.output.read_text(encoding="utf-8")) == result,
                "persisted original Mojang rotation JSON differs on independent replay")
        verify_csv(result)
        print("H27_21_STATES_136_ELEMENTS_1088_ORIGINAL_MOJANG_ROTATED_CORNERS_PASS")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                            encoding="utf-8")
        print("H27_ORIGINAL_ROTATIONS_JSON_START")
        print(json.dumps(result, sort_keys=True, ensure_ascii=False, separators=(",", ":")))
        print("H27_ORIGINAL_ROTATIONS_JSON_END")


if __name__ == "__main__":
    main()
