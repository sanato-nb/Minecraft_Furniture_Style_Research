#!/usr/bin/env python3
"""INT-4-H14: pinned AF chair source-face sidedness vs original H12 Minecraft F2.

Reopens the original H12 Actions ZIP and pinned upstream parent and texture
files. The result contains structural and aggregate observations only, not
original mod textures, game screenshots, JAR bytes, or client log contents.
A camera-facing source-normal candidate is NOT GPU face/pixel attribution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
INT = ROOT / "project/integration"
UPSTREAM = "57eb624cbb7f408d43398c7434b0d38d312cb55d"
BASE = ("https://raw.githubusercontent.com/crispytwig/AnotherFurniture/" + UPSTREAM
        + "/common/src/main/resources/assets/another_furniture/")
PINS = {
    "models/block/template/chair.json": "d9b64a818021f1a64b0cba13d16d18d6fea65d01",
    "textures/block/chair/back_1/acacia.png": "55f3bbf986c0c10b731cc0e67038402f30340972",
    "textures/block/chair/back_3/acacia.png": "e2282f2620fc8fbbcfd3bb69ab2a435e5421bbe8",
}
PRIOR_PINS = {
    "INT4_H11_AF_VARIANT3_SOURCE_UV_TEXEL_AUDIT_V1.json": "1869ee05afce779bd37233ba1cc74850d736160f",
    "INT4_H12_AF_MODEL1_MODEL3_NATIVE_F2_INDEPENDENT_RESULT_V1.json": "5e40040a13146ae08b97cf9d4747a6a08bc1d208",
}
ARCHIVE_SHA256 = "6b305bda1f8d9e02f417cb2b2f4c3600936ed7bb11e6e3d494d6c448e3a0d2a4"
STAGES = ("model1_before", "model3", "model1_after", "air")
EXPECTED_CAMERA = "-87.5 122.3 45.5 180 20"
XYZ = (-88, 120, 40)
ROI = (350, 275, 675, 620)
THRESHOLD = 24


def check(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def source_inputs(source_dir: Path | None = None) -> dict[str, bytes]:
    """Original pinned upstream bytes only; never use unpinned repository HEAD."""
    found = {}
    for relative, pin in PINS.items():
        if source_dir is None:
            req = Request(BASE + relative, headers={"User-Agent": "MCFR-H14-source/1.0"})
            with urlopen(req, timeout=35) as response:
                data = response.read()
        else:
            data = (source_dir / relative).read_bytes()
        check(blob(data) == pin, "UNPINNED_AF_ORIGINAL_SOURCE " + relative)
        found[relative] = data
    return found


def historical_inputs(root: Path = INT) -> tuple[dict, dict]:
    docs = []
    for name, pin in PRIOR_PINS.items():
        data = (root / name).read_bytes()
        check(blob(data) == pin, "H11_H12_RESEARCH_IDENTITY_DRIFT " + name)
        docs.append(json.loads(data))
    h11, h12 = docs
    check(h11["counts"]["different_original_back_texture_RGBA_texels"] == 54 and
          h11["counts"]["changed_binding_faces_with_any_different_texel"] == 2 and
          h11["counts"]["equal_inherited_elements_each"] == 10 and
          h11["counts"]["equal_inherited_faces_each"] == 46 and
          h11["counts"]["F70_unconditional_approvals"] == 0 and
          h12["source_2_UV_overlapping_changed_texel_faces"] == 2 and
          h12["UV_face_to_GPU_pixel_causal_proof"] is False and
          h12["F70_unconditional_approvals"] == 0,
          "H11_H12_SCOPE_OR_SOURCE_COUNTS_DRIFTED")
    return h11, h12


def original_back_texel_delta(left: bytes, right: bytes) -> dict:
    with Image.open(BytesIO(left)) as one, Image.open(BytesIO(right)) as three:
        one.load()
        three.load()
        check(one.size == three.size == (16, 16) and
              one.format == three.format == "PNG", "ORIGINAL_PNG_NOT_16x16")
        one = one.convert("RGBA")
        three = three.convert("RGBA")
        diff = {(x, y): (one.getpixel((x, y)), three.getpixel((x, y)))
                for y in range(16) for x in range(16)
                if one.getpixel((x, y)) != three.getpixel((x, y))}
    by_row = Counter(y for x, y in diff)
    alpha = sum(a[3] != b[3] for a, b in diff.values())
    check(len(diff) == 54 and alpha == 38 and len(diff) - alpha == 16,
          "ORIGINAL_54_TEXTURE_DIFF_OR_ALPHA_SUBSETS_DRIFTED")
    check(set(diff) == {(x, y) for y in range(7) for x in range(8)}
          - {(0, 0), (7, 0)}, "SOURCE_BACK_TEXTURE_DIFF_MASK_DRIFTED")
    return {
        "changed_RGBA_texels": len(diff),
        "changed_texels_with_alpha_change": alpha,
        "changed_texels_only_RGB_change": len(diff)-alpha,
        "diff_texel_bounds_xyxy": [0, 0, 7, 6],
        "diff_texels_by_texture_row_y": {str(y): by_row[y] for y in sorted(by_row)},
        "original_RGBA_differences_not_committed": True,
    }


def source_camera_face(parent: dict, h11: dict, changed: dict) -> dict:
    elements = parent.get("elements")
    check(isinstance(elements, list) and len(elements) == 10,
          "ORIGINAL_PARENT_NOT_TEN_ELEMENTS")
    plane = elements[7]
    check(plane["from"] == [4, 7, 13] and plane["to"] == [12, 16, 13] and
          set(plane["faces"]) == {"north", "south"},
          "ORIGINAL_BACKREST_CENTER_PLANE_GEOMETRY_DRIFTED")
    check(plane["faces"]["north"]["uv"] == [0, 0, 8, 9] and
          plane["faces"]["south"]["uv"] == [8, 0, 0, 9],
          "ORIGINAL_BACKREST_CENTER_UV_DRIFTED")
    camera_z = float(EXPECTED_CAMERA.split()[2])
    plane_z = XYZ[2] + 13/16
    check(camera_z > plane_z, "CAMERA_NOT_ON_SOURCE_SOUTH_SIDE")
    faces = []
    for face, normal in (("north", -1), ("south", 1)):
        source_uv = plane["faces"][face]["uv"]
        candidate = normal * (camera_z - plane_z) > 0
        faces.append({
            "element_index": 7,
            "face": face,
            "source_uv": source_uv,
            "source_changed_texels_overlapping_UV": changed["changed_RGBA_texels"],
            "source_plane_normal_z": normal,
            "camera_on_face_normal_side": candidate,
            "gpu_visibility_confirmed": False,
            "exact_screen_pixel_to_face_approved": False,
        })
    check(sum(row["camera_on_face_normal_side"] for row in faces) == 1 and
          next(r for r in faces if r["camera_on_face_normal_side"])["face"] == "south" and
          h11["counts"]["changed_binding_faces_with_any_different_texel"] == 2,
          "CAMERA_FACING_CANDIDATE_NOT_ONE_OF_TWO_SOURCE_UV_FACES")
    return {
        "fixed_camera": EXPECTED_CAMERA,
        "camera_world_z": camera_z,
        "center_plane_world_z": plane_z,
        "source_2_faces_intersect_original_delta": 2,
        "source_faces_on_camera_side": 1,
        "camera_side_source_face_candidate": "south",
        "camera_opposite_source_face": "north",
        "source_backrest_is_zero_thickness_two_sided_plane": True,
        "gpu_raster_face_visibility_or_exact_pixel_attribution_proven": False,
        "faces": faces,
    }


def pixels_changed(a: Image.Image, b: Image.Image) -> set[tuple[int, int]]:
    check(a.size == b.size == (1024, 684), "ORIGINAL_F2_FRAME_DIMENSIONS_DRIFTED")
    pa = a.convert("RGB").crop(ROI)
    pb = b.convert("RGB").crop(ROI)
    changed = set()
    for i, (v, w) in enumerate(zip(pa.getdata(), pb.getdata())):
        if max(abs(v[c]-w[c]) for c in range(3)) >= THRESHOLD:
            changed.add((ROI[0]+i%pa.width, ROI[1]+i//pa.width))
    return changed


def original_f2_archive_metrics(archive: bytes, expected: dict) -> dict:
    check(sha(archive) == ARCHIVE_SHA256, "NOT_THE_PINNED_ORIGINAL_H12_ACTIONS_ZIP")
    with ZipFile(BytesIO(archive)) as z:
        check(z.testzip() is None, "H12_ARTIFACT_ZIP_CRC_FAILURE")
        names = set(z.namelist())
        required = {"client.log", "INT4_H12_AF_SAME_CAMERA_REAL_NATIVE_F2_SOURCE_MANIFEST_V1.json"}
        required |= {s + ".png" for s in STAGES}
        check(required <= names, "ORIGINAL_H12_NATIVE_F2_OR_LOG_MISSING")
        manifest_raw = z.read("INT4_H12_AF_SAME_CAMERA_REAL_NATIVE_F2_SOURCE_MANIFEST_V1.json")
        manifest = json.loads(manifest_raw)
        check(sha(manifest_raw) == expected["original_manifest_sha256"] and
              manifest["fixed_camera"] == EXPECTED_CAMERA and
              manifest["source_model_coordinates"] == list(XYZ) and
              manifest["real_game_single_session"] is True and
              manifest["same_position_facing_camera_all_four"] is True,
              "H12_MANIFEST_OR_CAMERA_NOT_AUTHENTIC")
        log = z.read("client.log")
        check(sha(log) == expected["original_client_log_sha256"],
              "H12_ORIGINAL_SERVER_LOG_MISMATCH")
        log_text = log.decode("utf-8", "replace")
        imgs = {}
        for stage in STAGES:
            record = manifest["states"][stage]
            original_png = z.read(stage + ".png")
            check(sha(original_png) == record["sha256"] ==
                  expected["native_original_F2_sha256"][stage] and
                  record["exact_server_verified"] is True and
                  "[RenderAudit] " + record["server_marker"] in log_text,
                  "ORIGINAL_GAME_NATIVE_F2_SHA_OR_SERVER_STATE_MISMATCH_" + stage)
            with Image.open(BytesIO(original_png)) as im:
                im.load()
                check(im.format == "PNG" and im.size == (1024, 684),
                      "ORIGINAL_GAME_F2_NOT_NATIVE_1024x684")
                imgs[stage] = im.convert("RGB")
    before, model3, after, air = (imgs[s] for s in STAGES)
    delta = pixels_changed(before, model3)
    repeat = pixels_changed(before, after)
    foreground = pixels_changed(before, air) | pixels_changed(model3, air)
    by_row = Counter(y for _, y in delta)
    metrics = expected["pixel_measurement"]
    check(len(delta) == metrics["model1_to_model3"] == 808 and
          len(repeat) == metrics["model1_before_to_model1_after_temporal_control"] == 0 and
          len(delta-foreground) == metrics["model_difference_outside_foreground"] == 0 and
          [min(x for x,y in delta),min(y for x,y in delta),
           max(x for x,y in delta),max(y for x,y in delta)] ==
          metrics["changed_pixel_bounds"] == [493,433,530,461],
          "H12_ACTUAL_PIXEL_METRICS_DRIFTED")
    return {
        "original_H12_run_id": 45183488267,
        "original_H12_artifact_id": 14822712371,
        "original_archive_SHA256": ARCHIVE_SHA256,
        "original_F2_native_PNG_verified": len(STAGES),
        "original_exact_server_states_verified": len(STAGES),
        "RGB_channel_threshold": THRESHOLD,
        "ROI_xyxy_exclusive": list(ROI),
        "variant1_variant3_changed_pixels": len(delta),
        "variant1_repeat_temporal_changed_pixels": len(repeat),
        "variant1_variant3_changed_pixels_outside_foreground_mask": len(delta-foreground),
        "changed_screen_pixel_bounds_xyxy_inclusive": [493,433,530,461],
        "changed_screen_pixels_by_image_row_y": {str(y):by_row[y] for y in sorted(by_row)},
        "screen_difference_aggregates_not_raw_PNGs_committed": True,
    }


def research(h11: dict, h12: dict, parent: dict, texture1: bytes,
             texture3: bytes, archive: bytes) -> dict:
    check(h12["same_camera"] == EXPECTED_CAMERA and
          h12["same_source_coordinates"] == list(XYZ) and
          h12["source_54_RGBA_changed_texels"] == 54 and
          h12["source_12_different_texture_binding_faces"] == 12,
          "PINNED_PREVIOUS_SOURCE_COUNTS_OR_CAMERA_CHANGED")
    tex = original_back_texel_delta(texture1, texture3)
    face = source_camera_face(parent, h11, tex)
    f2 = original_f2_archive_metrics(archive, h12)
    return {
        "schema":"MCFR_INT4_H14_AF_CAMERA_SIDE_SOURCE_UV_REAL_F2_BRIDGE/v1",
        "status":"PASS_PINNED_SOURCE_CAMERA_SIDE_ONE_CANDIDATE_AND_ORIGINAL_F2_DIFF_NO_GPU_FACE_PROOF",
        "source":{"repo":"crispytwig/AnotherFurniture", "upstream_git_commit":UPSTREAM,
                  "pinned_git_blob_sha1":PINS,
                  "H11_prior_git_blob_sha1":PRIOR_PINS["INT4_H11_AF_VARIANT3_SOURCE_UV_TEXEL_AUDIT_V1.json"],
                  "H12_prior_git_blob_sha1":PRIOR_PINS["INT4_H12_AF_MODEL1_MODEL3_NATIVE_F2_INDEPENDENT_RESULT_V1.json"],
                  "in_game_mod_release":"4.0.2", "in_game_mod_JAR_sha1":h12["real_runtime_AF_JAR_sha1"]},
        "source_texture_change":tex,
        "source_backrest_camera_side":face,
        "actual_F2_independent_reanalysis":f2,
        "conclusion":{"single_source_normal_side_candidate_identified":True,
                      "changed_RGBA_54_texels_with_38_alpha_changes_verified":True,
                      "H12_same_pose_808_changed_pixels_reproduced":True,
                      "source_face_to_screen_pixel_GPU_causality_approved":False,
                      "other_camera_angles_or_south_variant3_original_F2_tested":False,
                      "all_mods_or_versions_generalization_approved":False,
                      "F70_conditionally_evidenced":70,
                      "F70_unconditional_approvals":0,
                      "H03_exit_approved":False,"H05_exit_approved":False,
                      "INT5_semantics_approved":0,"INT6_training_or_redistribution_rights_approved":0},
        "limits":[
           "Camera on the +Z side of a zero-thickness parent element yields one source-normal candidate (south), NOT verified Minecraft GPU face selection or pixel UV lookup.",
           "Differences in 38 texture alpha texels can change which background pixels are visible; screenshot RGB colors alone do not identify the sampled face or texel.",
           "This is an independent reanalysis of the same original H12 run and four screenshots, not a new Minecraft game run.",
           "The H12 archive is an expiring GitHub Actions artifact, so its availability must not be assumed indefinitely.",
           "Original screenshots, mod textures, JAR and client.log bytes are not committed; no gameplay tests or automatic model corrections.",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--h12-archive", type=Path, required=True,
                   help="Previously downloaded ORIGINAL H12 Actions ZIP #14822712371")
    p.add_argument("--source-dir", type=Path,
                   help="Optional offline directory holding pinned 3 original source resources")
    p.add_argument("--output", type=Path, default=INT/"INT4_H14_AF_CAMERA_FACE_UV_F2_SOURCE_BRIDGE_V1.json")
    p.add_argument("--verify", action="store_true", help="Require committed derived evidence to agree exactly in fields and values")
    args = p.parse_args()
    sources = source_inputs(args.source_dir)
    h11, h12 = historical_inputs()
    doc = research(h11,h12,json.loads(sources["models/block/template/chair.json"]),
                   sources["textures/block/chair/back_1/acacia.png"],
                   sources["textures/block/chair/back_3/acacia.png"],
                   args.h12_archive.read_bytes())
    data = (json.dumps(doc, sort_keys=True, indent=2, ensure_ascii=False)+"\n").encode()
    if args.verify:
        check(args.output.is_file() and json.loads(args.output.read_text(encoding="utf-8")) == doc,
              "H14_COMMITTED_DERIVED_REPORT_NOT_DETERMINISTIC")
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_bytes(data)
    print(json.dumps({"status":doc["status"],
                      "changed_texels":doc["source_texture_change"]["changed_RGBA_texels"],
                      "camera_facing_source_candidate":doc["source_backrest_camera_side"]["camera_side_source_face_candidate"],
                      "original_F2_changed_pixels":doc["actual_F2_independent_reanalysis"]["variant1_variant3_changed_pixels"],
                      "unconditional_approvals":doc["conclusion"]["F70_unconditional_approvals"]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
