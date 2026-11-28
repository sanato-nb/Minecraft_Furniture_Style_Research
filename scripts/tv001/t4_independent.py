#!/usr/bin/env python3
"""TV-001 T4 independent, bounded geometry and UV evidence checks.

Uses raw fixtures/vanilla blockstate files and an analytic 2-D orthographic
projection. Does NOT import the Blender renderer or the prepare.py resolver.
Silhouette agreement is not full Minecraft visual fidelity.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CAMERAS = {
    "north": (0, 2.5, .25), "south": (0, -2.5, .25),
    "east": (2.5, 0, .25), "west": (-2.5, 0, .25),
    "up": (0, 0, 2.5), "down": (0, 0, -2.5),
    "iso": (2.2, -2.7, 2.0),
}
EXPECTED = {
    "P01": 6, "P02": 2, "P03": 2, "P04": 4, "P05": 4,
    "P06": 2, "R01": 1, "R02": 2, "R03": 2,
}
PIN = "176f7f34de2336eb7984c4734e97b6eb156c19f4"


def unit(v):
    return v / np.linalg.norm(v)


def axes(view):
    pos = np.array(CAMERAS[view], dtype=float)
    forward = unit(-pos)
    if abs(forward[2]) > .999:  # top/bottom screen basis independent of Blender API
        right = np.array((1., 0., 0.))
        up = unit(np.cross(right, forward))
    else:
        right = unit(np.cross(forward, np.array((0, 0, 1.))))
        up = unit(np.cross(right, forward))
    return right, up


def matrix(axis, degrees):
    a = math.radians(degrees)
    c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return np.array(((1, 0, 0), (0, c, -s), (0, s, c)), float)
    if axis == "y":
        return np.array(((c, 0, s), (0, 1, 0), (-s, 0, c)), float)
    if axis == "z":
        return np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)), float)
    raise AssertionError("invalid axis " + axis)


def cube_faces(element):
    lo, hi = element["from"], element["to"]
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    return {
        "down": ((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)),
        "up": ((x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)),
        "north": ((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)),
        "south": ((x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)),
        "west": ((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)),
        "east": ((x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)),
    }


def geometric_quads(element, instance):
    for face, points in cube_faces(element).items():
        if face not in element["faces"]:
            continue
        pts = np.array(points, dtype=float)
        rotate = element.get("rotation")
        if rotate:
            pivot = np.array(rotate.get("origin", (8, 8, 8)), float)
            pts = (pts - pivot) @ matrix(rotate["axis"], rotate["angle"]).T + pivot
        if instance["x"]:
            pts = (pts - 8) @ matrix("x", instance["x"]).T + 8
        if instance["y"]:
            pts = (pts - 8) @ matrix("y", instance["y"]).T + 8
        # Minecraft coordinates -> geometrically equivalent Blender display frame
        yield np.column_stack(((pts[:, 0] - 8) / 16,
                               -(pts[:, 2] - 8) / 16,
                               (pts[:, 1] - 8) / 16))


def expected_mask(job):
    right, up = axes(job["camera"])
    mask = Image.new("L", (256, 256), 0)
    painter = ImageDraw.Draw(mask)
    for inst in job["instances"]:
        for element in inst["elements"]:
            for quad in geometric_quads(element, inst):
                screen = [(128 + np.dot(v, right) * 256 / 1.8,
                           128 - np.dot(v, up) * 256 / 1.8) for v in quad]
                painter.polygon(screen, fill=255)
    return mask


def shifted_correlation(cutouts, dx, dy):
    """Corr of binary transparent pixels after a known nine-pixel shift."""
    h, w = cutouts.shape
    x0, x1 = max(0, dx), min(w, w + dx)
    y0, y1 = max(0, dy), min(h, h + dy)
    a = cutouts[y0:y1, x0:x1].astype(float).ravel()
    b = cutouts[y0 - dy:y1 - dy, x0 - dx:x1 - dx].astype(float).ravel()
    if a.std() == 0 or b.std() == 0:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def inspect_sources(repo, fixture, jobs):
    issues = []
    def check(cond, issue):
        if not cond:
            issues.append(issue)
    def load(path):
        return json.loads(path.read_text(encoding="utf-8"))
    models = fixture / "assets/test/models/block"
    states = fixture / "assets/test/blockstates"
    vanilla = repo / "1.21.11/assets/minecraft"
    by_id = {j["id"]: j for j in jobs}
    check(load(models / "p01.json")["elements"][0]["from"] == [2, 2, 2], "P01 origin mismatch")
    p02 = load(models / "p02.json")["elements"]
    check(len(p02) == 2 and p02[1]["rotation"] == {
        "origin": [8, 8, 8], "axis": "y", "angle": 22.5}, "P02 rotation mismatch")
    check(load(models / "p03.json").get("parent") == "test:block/p03_middle" and
          load(models / "p03_middle.json").get("parent") == "test:block/p03_base",
          "P03 parent chain mismatch")
    check({k: v.get("y", 0) for k, v in load(states / "p04.json")["variants"].items()} == {
        "facing=north": 0, "facing=east": 90,
        "facing=south": 180, "facing=west": 270}, "P04 four-state mismatch")
    check(len(load(states / "p05.json")["multipart"]) == 3, "P05 multipart mismatch")
    check(load(models / "p06.json")["elements"][0]["faces"]["north"]["rotation"] == 90,
          "P06 UV rotation not present")
    tex = fixture / "assets/test/textures/block/alpha.png"
    with Image.open(tex) as img:
        sample = np.array(img.convert("RGBA"))
        check(sample.shape == (16, 16, 4) and (sample[:, :, 3] == 0).sum() == 64,
              "P06 texture alpha pattern mismatch")
    check(load(vanilla / "models/block/acacia_planks.json").get("parent") ==
          "minecraft:block/cube_all", "R01 vanilla parent mismatch")
    fence = load(vanilla / "blockstates/acacia_fence.json")["multipart"]
    check(len(fence) == 5 and fence[1].get("when") == {"north": "true"} and
          fence[1]["apply"].get("uvlock") is True, "R02 vanilla north part mismatch")
    stair = load(vanilla / "blockstates/acacia_stairs.json")["variants"]
    check(stair["facing=east,half=bottom,shape=straight"] == {
        "model": "minecraft:block/acacia_stairs"}, "R03 straight source mismatch")
    check(stair["facing=east,half=top,shape=inner_left"] == {
        "model": "minecraft:block/acacia_stairs_inner", "uvlock": True, "x": 180},
        "R03 inner source mismatch")
    check([(x["model"], x["x"], x["y"], x["uvlock"]) for x in
           by_id["R03-inner"]["instances"]] == [
               ("minecraft:block/acacia_stairs_inner", 180, 0, True)],
          "R03 inner resolved state mismatch")
    check([(x["model"], x["y"], x["uvlock"]) for x in
           by_id["R02-north"]["instances"]] == [
               ("minecraft:block/acacia_fence_post", 0, False),
               ("minecraft:block/acacia_fence_side", 0, True)],
          "R02 multipart resolved state mismatch")
    check([(x["model"], len(x["elements"])) for x in
           by_id["R03-straight"]["instances"]] == [
               ("minecraft:block/acacia_stairs", 2)],
          "R03 straight element count mismatch")
    check([(x["model"], len(x["elements"])) for x in
           by_id["R03-inner"]["instances"]] == [
               ("minecraft:block/acacia_stairs_inner", 3)],
          "R03 inner element count mismatch")
    return issues


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--renders", required=True, type=Path)
    p.add_argument("--report", required=True, type=Path)
    args = p.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    jobs = manifest["jobs"]
    issues = []
    if manifest.get("source_commit") != PIN:
        issues.append("pinned source commit mismatch")
    if len(jobs) != 25 or len(manifest.get("cases", [])) != 12:
        issues.append("fixed denominator mismatch")
    if {k: sum(j["case"] == k for j in jobs) for k in EXPECTED} != EXPECTED:
        issues.append("fixed 9 positive case counts mismatch")
    source_issues = inspect_sources(args.repo, args.manifest.parent / "fixtures", jobs)
    outcomes = []
    for job in jobs:
        pic = args.renders / (job["id"] + ".png")
        with Image.open(pic) as img:
            alpha = np.array(img.convert("RGBA"))[:, :, 3]
        mask = expected_mask(job)
        inside = np.array(mask.filter(ImageFilter.MinFilter(5))) > 0
        outside = np.array(mask.filter(ImageFilter.MaxFilter(5))) > 0
        observed = alpha > 200
        extra = int(np.logical_and(observed, ~outside).sum())
        missing = int(np.logical_and(inside, ~observed).sum())
        if job["case"] == "P06":
            # Cut-out faces can expose other cube faces; avoid false expectation
            # that every interior pixel must be opaque.
            passed = extra == 0 and 0 < int((alpha == 0).sum()) < 65536
            missing = None
        else:
            passed = extra == 0 and missing == 0
        outcomes.append({"id": job["id"], "geometry_mask_pass": bool(passed),
                         "unexpected_opaque_pixels_outside_2px": extra,
                         "missing_opaque_pixels_inside_2px": missing})
    if any(not o["geometry_mask_pass"] for o in outcomes):
        issues.append("independent silhouette mismatch")
    orientations = {}
    for suffix in ("north", "south"):
        arr = np.array(Image.open(args.renders / ("P06-" + suffix + ".png")).convert("RGBA"))
        cutouts = arr[70:185, 70:185, 3] < 64
        orientations[suffix] = {
            "down_right_9": round(shifted_correlation(cutouts, 9, 9), 4),
            "up_right_9": round(shifted_correlation(cutouts, 9, -9), 4),
        }
    uv_rotation_pass = (
        orientations["north"]["down_right_9"] > .65 and
        orientations["north"]["up_right_9"] < .35 and
        orientations["south"]["up_right_9"] > .65 and
        orientations["south"]["down_right_9"] < .35
    )
    if not uv_rotation_pass:
        issues.append("P06 90-degree face UV transparency orientation mismatch")
    rotated_uvlocked_ids = [j["id"] for j in jobs if any(
        x["uvlock"] and (x["x"] or x["y"]) for x in j["instances"])]
    limitations = []
    mesh_report_path = args.manifest.parent / "r03_uv_mesh.json"
    mesh_uv = json.loads(mesh_report_path.read_text(encoding="utf-8")) if mesh_report_path.is_file() else {}
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    mesh_uv_ok = (
        rotated_uvlocked_ids == ["R03-inner"] and mesh_uv.get("case") == "R03-inner"
        and mesh_uv.get("status") == "PASS" and mesh_uv.get("face_total") == 15
        and mesh_uv.get("face_pass") == 15 and mesh_uv.get("loop_total") == 60
        and mesh_uv.get("loop_pass") == 60 and mesh_uv.get("negative_control_changed_faces_rejected") == 11
        and mesh_uv.get("renderer_sha256") == sha(args.repo / "scripts/tv001/blender_batch.py")
        and mesh_uv.get("manifest_sha256") == sha(args.manifest)
        and mesh_uv.get("reference_sha256") == sha(args.repo / "project/audits/tv001/TV001_B_R03_UV_REFERENCE_2026-11-28.json")
    )
    if not mesh_uv_ok:
        issues.append("R03 independent mesh UV evidence missing or failed")
        limitations.append({"category":"UVLOCK_MESH_NOT_VERIFIED","affected":rotated_uvlocked_ids})
    limitations.append({
        "category": "PER_FACE_TEXTURE_ORACLE_NOT_COMPLETE",
        "affected": [j["id"] for j in jobs],
        "evidence": "analytic silhouette and P06 cutout orientation verified; "
                    "independent full per-face Minecraft texel-accurate reference not supplied"
    })
    image_pass_count = sum(x["geometry_mask_pass"] for x in outcomes)
    t4 = {
        "scope": "TV-001-v1.1, exact 12 cases / 25 images",
        "status": "PARTIAL" if not issues else "FAIL",
        "source_spot_checks_pass": not source_issues,
        "source_issues": source_issues,
        "geometry_mask_pass": image_pass_count,
        "geometry_mask_total": len(outcomes),
        "rendered_pixel_coverage_tolerance": "inside/outside 2px edge band, alpha>200",
        "p06_uv_rotation_pattern_pass": bool(uv_rotation_pass),
        "r03_uv_mesh_pass": bool(mesh_uv_ok),
        "r03_uv_mesh_faces": mesh_uv.get("face_pass", 0),
        "r03_uv_mesh_loops": mesh_uv.get("loop_pass", 0),
        "p06_uv_orientation_evidence": orientations,
        "image_results": outcomes,
        "unverified_or_known_incorrect": limitations,
        "full_minecraft_visual_fidelity_verified": False,
        "false_success_prevention": "No automatic TV-001 PASS from renderer images alone."
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(t4, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("TV001_T4 " + json.dumps({k: v for k, v in t4.items()
                                  if k not in ("image_results",)}, ensure_ascii=False))
    if source_issues or issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
