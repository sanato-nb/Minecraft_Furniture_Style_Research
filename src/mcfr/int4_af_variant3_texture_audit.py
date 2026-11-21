"""INT-4 original-source investigation of AF acacia_chair variant=3 south.

Compare source-pinned 4.0.3 Git resources with actual 4.0.2 runtime JAR.
The anomaly is four *review directions* with one south model divergence.
Compare chosen child models, inherited geometry, UV, resolved face texture
slots, and actual RGBA source/runtime PNG pixels. NO Minecraft client render,
copyright grant, semantic approval, or automatic source correction.
Original source assets are read only in temp directories and never exported.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile

from . import af_release_version_audit as af
from .chair_runtime_fixture import digest_bytes

ROOT = Path(__file__).resolve().parents[2]
DIRECTIONS = af.DIRS
STATES_PATH = Path("project/integration/INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json")
AF_DIFF_PATH = Path("project/integration/INT3_AF_RELEASE_VERSION_COMPARISON.json")

EXPECTED_SHA = {
    "blockstates/acacia_chair.json": af.EXPECTED_SOURCE_BLOB,
    "models/block/chair/acacia_1.json": "609dea1eda246be610ed0a5762f3bb5f0ce9db92",
    "models/block/chair/acacia_3.json": "ef6b6e633205b62768cbc60d1c1731ab7d219c66",
    "models/block/template/chair.json": af.PINNED_PARENT_BLOBS["models/block/template/chair.json"],
    "textures/block/chair/back_1/acacia.png": "55f3bbf986c0c10b731cc0e67038402f30340972",
    "textures/block/chair/back_3/acacia.png": "e2282f2620fc8fbbcfd3bb69ab2a435e5421bbe8",
}
CHILDREN = ("models/block/chair/acacia_1.json", "models/block/chair/acacia_3.json")
TEXTURES = ("textures/block/chair/back_1/acacia.png",
            "textures/block/chair/back_3/acacia.png")
PARENT = "models/block/template/chair.json"
BACK_SOURCE = {
    "another_furniture:block/chair/acacia_1": "another_furniture:block/chair/back_1/acacia",
    "another_furniture:block/chair/acacia_3": "another_furniture:block/chair/back_3/acacia",
}


class EvidenceError(ValueError):
    pass


def require(cond, msg):
    if not cond:
        raise EvidenceError(msg)


def stable(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def selector(direction):
    require(direction in DIRECTIONS, "Unsupported cardinal direction")
    return f"facing={direction},tucked=false,variant=3"


def expected_model(direction):
    return ("another_furniture:block/chair/acacia_1" if direction == "south" else
            "another_furniture:block/chair/acacia_3")


def state_rows(study, runtime):
    require(set(study) == {"variants"} and set(runtime) == {"variants"},
            "Unexpected blockstate root shape")
    require(len(study["variants"]) == len(runtime["variants"]) == 88,
            "Original 88 source selectors incomplete")
    require(study == runtime,
            "4.0.2/4.0.3 selector semantic difference: cannot assume AF version parity")
    rows = []
    for direction in DIRECTIONS:
        key = selector(direction)
        s = study["variants"].get(key)
        r = runtime["variants"].get(key)
        require(isinstance(s, dict) and s == r and s.get("model") == expected_model(direction),
                "Anomalous original direction/model combination differs: " + key)
        require(s.get("y", 0) == DIRECTIONS.index(direction) * 90,
                "Unexpected direction rotation: " + key)
        rows.append({
            "selector": key, "direction": direction, "model": s["model"],
            "y": s.get("y", 0),
            "back_texture_slot": BACK_SOURCE[s["model"]],
            "different_model_from_variant3_majority": direction == "south",
            "not_observed_in_pr33_or_pr34_variant1_variant10_f2": True,
            "game_client_visual_verified": False,
        })
    require(sum(x["different_model_from_variant3_majority"] for x in rows) == 1,
            "Review group is four source rows but must contain one anomalous direction")
    return rows


def compare_inherited_models(docs):
    x, y = (af.effective(path, docs) for path in CHILDREN)
    require(x["geometry"] == y["geometry"] and x["uv"] == y["uv"],
            "Original acacia_1/acacia_3 geometry or per-face UV mismatch")
    require(x["render_type"] == y["render_type"] and
            x["ambientocclusion"] == y["ambientocclusion"] and
            x["element_count"] == y["element_count"] and
            x["face_count"] == y["face_count"],
            "Original effective parent structure changed")
    require(x["element_count"] == 10 and x["face_count"] == 46,
            "Historical AF chair geometry/face count changed")
    left, right = x["face_bindings"], y["face_bindings"]
    require(len(left) == len(right), "Face source geometry lists differ")
    rows, equal_faces = [], 0
    for element_i, (lfaces, rfaces) in enumerate(zip(left, right)):
        require(set(lfaces) == set(rfaces), "Different face names in inherited template")
        for face in sorted(lfaces):
            lv, rv = lfaces[face], rfaces[face]
            if lv == rv:
                equal_faces += 1
                continue
            require(set(lv) == set(rv) and lv.get("texture") != rv.get("texture") and
                    {k:v for k,v in lv.items() if k!="texture"} ==
                    {k:v for k,v in rv.items() if k!="texture"},
                    "Unexpected geometry-face material/cull/tint difference")
            require(lv["texture"] == BACK_SOURCE["another_furniture:block/chair/acacia_1"]
                    and rv["texture"] == BACK_SOURCE["another_furniture:block/chair/acacia_3"],
                    "Different texture slot beyond back_1/back_3")
            rows.append({
                "element_index": element_i, "face": face,
                "acacia_1_texture_resource": lv["texture"],
                "acacia_3_texture_resource": rv["texture"],
                "same_face_uv": True,
                "same_inherited_geometry": True,
                "observed_game_pixel_change": "NOT_TESTED",
            })
    require(rows and len(rows) + equal_faces == x["face_count"],
            "No evidence of source back-face binding discontinuity")
    return rows, {
        "element_count_each": x["element_count"],
        "face_count_each": x["face_count"],
        "changed_texture_binding_faces": len(rows),
        "unchanged_texture_binding_faces": equal_faces,
        "geometry_equal": True, "uv_equal": True,
        "render_type_equal": True,
        "changed_element_indices": sorted(set(x["element_index"] for x in rows)),
    }


def composite(pixel, background):
    alpha = pixel[3]
    return tuple((pixel[c] * alpha + background * (255 - alpha) + 127) // 255
                 for c in range(3))


def image_difference(img1, img2):
    """Return strict original pixel differences without exporting image contents."""
    from PIL import Image
    with Image.open(BytesIO(img1)) as src1, Image.open(BytesIO(img2)) as src2:
        src1.load()
        src2.load()
        require(src1.size == src2.size, "Original texture images have different dimensions")
        rgba1, rgba2 = src1.convert("RGBA"), src2.convert("RGBA")
        pixels1, pixels2 = list(rgba1.getdata()), list(rgba2.getdata())
        rgba_diff = sum(a != b for a, b in zip(pixels1, pixels2))
        black_diff = sum(composite(a, 0) != composite(b, 0)
                         for a, b in zip(pixels1, pixels2))
        white_diff = sum(composite(a, 255) != composite(b, 255)
                         for a, b in zip(pixels1, pixels2))
        return {
            "width": src1.width, "height": src1.height,
            "pixel_count": len(pixels1),
            "rgba_different_pixel_count": rgba_diff,
            "black_background_different_pixel_count": black_diff,
            "white_background_different_pixel_count": white_diff,
            "equal_rgba_pixels": rgba_diff == 0,
            "equal_visible_composite_black_white": black_diff == 0 and white_diff == 0,
        }


def verify_historical(root):
    source = json.loads((root / STATES_PATH).read_text(encoding="utf-8"))
    require(source["totals"]["source_anomaly_rows"] == 4 and
            source["totals"]["original_variant_rules"] == 228,
            "Historical 4 review-direction rows or 228 source rules changed")
    state = next((x for x in source["source_states"] if x["mod"] == "AF"), None)
    require(state is not None and state["source_sha"] == af.EXPECTED_SOURCE_BLOB and
            state["review_anomalous_selector_rows"] == 4,
            "Original source historical AF anomaly input not the pinned version")
    require({x["selector"] for x in state["review_groups"]} ==
            {selector(d) for d in DIRECTIONS},
            "Historical AF four-review-direction set changed")
    prior = json.loads((root / AF_DIFF_PATH).read_text(encoding="utf-8"))
    require(prior["research"]["git_commit"] == af.UPSTREAM and
            prior["research"]["blockstate_git_blob_sha1"] == af.EXPECTED_SOURCE_BLOB and
            prior["runtime"]["jar_sha1"] == "c2f992081bdc4795ed6d87771a3b5f7c71103785" and
            prior["states"]["same"] == 88 and prior["models"]["json_identical"] == 24 and
            prior["boundary"]["part_roles_approved"] == 0 and
            prior["boundary"]["ai_training_rights_approved"] == 0,
            "Prior pinned runtime/study comparison identity drifted")
    return {
        str(STATES_PATH): digest((root / STATES_PATH).read_bytes()),
        str(AF_DIFF_PATH): digest((root / AF_DIFF_PATH).read_bytes()),
    }


def read_originals(work):
    jar, pin = af.original_jar(work)
    blobs = {"study": {}, "runtime": {}}
    with ZipFile(jar) as z:
        names = set(z.namelist())
        for relative, expected in EXPECTED_SHA.items():
            upstream = af.fetch_research(relative)
            require(upstream is not None and
                    digest_bytes(upstream, "GIT_BLOB_SHA1") == expected,
                    "4.0.3 original source Git blob mismatch: " + relative)
            inside = af.PREFIX + relative
            require(inside in names,
                    "4.0.2 pinned original JAR missing resource: " + relative)
            blobs["study"][relative] = upstream
            blobs["runtime"][relative] = z.read(inside)
    return blobs, pin


def read_models(blobs):
    models = {}
    for side in ("study", "runtime"):
        models[side] = {relative: json.loads(blobs[side][relative].decode("utf-8-sig"))
                        for relative in (*CHILDREN, PARENT)}
        require(all(models[side][x].get("parent") ==
                    "another_furniture:block/template/chair" for x in CHILDREN),
                "Missing original chair parent reference on " + side)
        require(models[side][CHILDREN[0]]["textures"]["back"] ==
                BACK_SOURCE["another_furniture:block/chair/acacia_1"] and
                models[side][CHILDREN[1]]["textures"]["back"] ==
                BACK_SOURCE["another_furniture:block/chair/acacia_3"],
                "Original source back texture slot changed on " + side)
        require(models[side][CHILDREN[0]]["textures"]["bottom"] ==
                models[side][CHILDREN[1]]["textures"]["bottom"] and
                models[side][CHILDREN[0]]["textures"]["seat"] ==
                models[side][CHILDREN[1]]["textures"]["seat"],
                "Other original chair seat/bottom texture bindings differ")
    require(models["study"] == models["runtime"],
            "Fixed 4.0.2/4.0.3 acacia child models or parent differ semantically")
    return models


def audit(work, out, root=ROOT):
    root, work, out = Path(root), Path(work), Path(out)
    require(not out.exists(), "Do not replace an earlier audit output")
    prior_sha = verify_historical(root)
    work.mkdir(parents=True, exist_ok=True)
    raw, jar_sha = read_originals(work)
    research = json.loads(raw["study"]["blockstates/acacia_chair.json"].decode("utf-8-sig"))
    runtime = json.loads(raw["runtime"]["blockstates/acacia_chair.json"].decode("utf-8-sig"))
    require(digest_bytes(raw["runtime"]["blockstates/acacia_chair.json"], "GIT_BLOB_SHA1") ==
            "3a806533856f169a502373bda43a76eeabc1e689",
            "Runtime 4.0.2 blockstate source blob changed")
    rows = state_rows(research, runtime)
    docs = read_models(raw)
    faces, face_summary = compare_inherited_models(docs["study"])
    runtime_faces, runtime_face_summary = compare_inherited_models(docs["runtime"])
    require(faces == runtime_faces and face_summary == runtime_face_summary,
            "Runtime face texture binding discontinuity differs from study source")
    image_comparisons, source_image_bytes = {}, {}
    for side in ("study", "runtime"):
        left, right = (raw[side][path] for path in TEXTURES)
        source_image_bytes[side] = {
            path: {"git_blob_sha1": digest_bytes(raw[side][path], "GIT_BLOB_SHA1"),
                   "byte_sha256": digest(raw[side][path]),
                   "byte_length": len(raw[side][path])}
            for path in TEXTURES
        }
        image_comparisons[side] = image_difference(left, right)
        require(image_comparisons[side]["pixel_count"] > 0,
                "Original source images not decoded")
    cross_version_pixels = {
        path: image_difference(raw["study"][path], raw["runtime"][path])
        for path in TEXTURES
    }
    out.mkdir(parents=True)
    def write_rows(filename, records):
        path = out / filename
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(records[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(records)
        return digest(path.read_bytes())
    hashes = {
        "variant3_directions.csv": write_rows("variant3_directions.csv", rows),
        "back_face_binding_differences.csv": write_rows("back_face_binding_differences.csv", faces),
    }
    report = {
        "schema": "MCFR_INT4_AF_VARIANT3_BACK_TEXTURE_SOURCE_AUDIT/v1",
        "status": "COMPLETE_SOURCE_TEXTURE_DIFFERENCE_NOT_GAME_PIXEL_OR_INT5_APPROVAL",
        "review_rows_not_distinct_errors": 4,
        "source_selector_discontinuities": 1,
        "discontinuous_direction": "south",
        "variant3_direction_rows": len(rows),
        "study_release_commit": af.UPSTREAM,
        "runtime_jar_sha1": jar_sha,
        "source_git_blob_sha1": {
            path: digest_bytes(raw["study"][path], "GIT_BLOB_SHA1")
            for path in EXPECTED_SHA
        },
        "runtime_git_blob_sha1": {
            path: digest_bytes(raw["runtime"][path], "GIT_BLOB_SHA1")
            for path in EXPECTED_SHA
        },
        "study_runtime_models_json_semantically_equal": True,
        "study_runtime_blockstate_json_semantically_equal": True,
        "model_face_comparison": face_summary,
        "texture_png_study": image_comparisons["study"],
        "texture_png_runtime": image_comparisons["runtime"],
        "textures_study_vs_runtime": cross_version_pixels,
        "two_source_pngs_each_release": source_image_bytes,
        "historical_evidence_file_sha256": prior_sha,
        "csv_sha256": hashes,
        "limits": {
            "int4_all_furniture_complete": False,
            "int5_screenshot_variant3_taken": False,
            "minecraft_client_baked_geometry_uv_and_pixel_match": False,
            "mod_author_intent_for_south_selection": "UNKNOWN",
            "automatic_correction_applied": False,
            "part_roles_verified": 0,
            "material_style_approved": 0,
            "asset_rights_or_ai_training_approved": 0,
            "original_jar_models_png_checked_into_repo": False,
        },
    }
    (out / "AF_VARIANT3_TEXTURE_AUDIT.json").write_text(
        json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--work", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args(argv)
    result = audit(args.work, args.output, args.root)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
