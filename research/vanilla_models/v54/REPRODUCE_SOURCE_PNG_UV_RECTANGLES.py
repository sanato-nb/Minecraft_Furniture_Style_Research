#!/usr/bin/env python3
"""Reproduce v54 exact original-PNG source-UV rectangle samples.

Requires Python 3, Pillow, repo root containing the extracted 1.21.11 assets.
This checks SOURCE PNG pixels in source-declared explicit UV rectangles.
It does NOT simulate Minecraft's face orientation, rendering, interpolation,
texture mipmaps, lighting, resource-pack overrides, or runtime block entities.
"""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SOURCE_FACE_CSV = ROOT / "research/vanilla_models/v53/05_EFFECTIVE_FACE_APPLICATIONS_3413.csv"
SOURCE_PNG_MANIFEST = ROOT / "research/vanilla_models/v53/10_ORIGINAL_PNG_RGBA_4.json"
OUTPUT = ROOT / "research/vanilla_models/v54/REPRODUCED_SOURCE_UV_RGBA_226.csv"

manifest = json.loads(SOURCE_PNG_MANIFEST.read_text(encoding="utf-8"))
image_cache = {}
for src in manifest["records"]:
    path = ROOT / src["source_path"]
    data = path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    assert actual == src["git_blob_sha"], f"Git SHA mismatch: {path}"
    with Image.open(path) as im:
        image_cache[src["source_path"]] = im.convert("RGBA").copy()

out = []
with SOURCE_FACE_CSV.open(newline="", encoding="utf-8") as fp:
    for face in csv.DictReader(fp):
        if face["original_UV_key_present"] != "true":
            continue
        image = image_cache.get(face["texture_path_after_slot_resolution"])
        if image is None:
            continue
        u1, v1, u2, v2 = json.loads(face["original_explicitUV"])
        assert all(isinstance(q, int) for q in (u1, v1, u2, v2))
        x1, x2 = sorted((u1, u2))
        y1, y2 = sorted((v1, v2))
        assert 0 <= x1 < x2 <= image.width and 0 <= y1 < y2 <= image.height
        rgba = [image.getpixel((x, y)) for y in range(y1, y2) for x in range(x1, x2)]
        out.append({
            "source_model": face["source_model"],
            "source_path": face["source_path"],
            "source_sha": face["source_sha"],
            "geometry_source_model": face["geometry_source_model"],
            "element_index": face["element_index"],
            "face_side": face["face_side"],
            "source_png_path": face["texture_path_after_slot_resolution"],
            "original_explicit_uv": face["original_explicitUV"],
            "source_rectangle_pixel_count": len(rgba),
            "alpha0": sum(px[3] == 0 for px in rgba),
            "alpha255": sum(px[3] == 255 for px in rgba),
            "alpha_partial": sum(0 < px[3] < 255 for px in rgba),
            "unique_RGBA": len(set(rgba)),
            "u_axis_reversed": u1 > u2,
            "v_axis_reversed": v1 > v2,
            "runtime_renderer_verified": False,
        })

assert len(out) == 226, len(out)
assert sum(x["source_rectangle_pixel_count"] for x in out) == 1736
with OUTPUT.open("w", newline="", encoding="utf-8") as fp:
    writer = csv.DictWriter(fp, fieldnames=out[0].keys())
    writer.writeheader()
    writer.writerows(out)
print("verified source face rectangles:", len(out))
print("source texture pixel observations (includes repeats):", sum(x["source_rectangle_pixel_count"] for x in out))
