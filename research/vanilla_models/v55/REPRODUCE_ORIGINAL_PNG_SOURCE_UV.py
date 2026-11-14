#!/usr/bin/env python3
"""Verify v55 SOURCE PNG pixels, source face UV areas, and cake UV candidates.

Run with the checked-out original 1.21.11 assets in this repository and Pillow.
This does not verify in-game rendered UV orientation, alpha blending, or lighting.
Cake implicit UV rectangles are DERIVED CANDIDATES, not original UV properties.
"""
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
source = json.loads((HERE / "01_DIRECT_ORIGINAL_PNG_RGBA_9.json").read_text())["records"]
images = {}
for entry in source:
    path = ROOT / entry["source_path"]
    raw = path.read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    assert sha == entry["source_git_blob_sha"], f"original PNG SHA mismatch {path}"
    with Image.open(path) as img:
        assert img.size == (16, 16)
        image = img.convert("RGBA").copy()
    pixels = [image.getpixel((x, y)) for y in range(16) for x in range(16)]
    assert sum(px[3] == 255 for px in pixels) == entry["alpha_255_count"]
    assert sum(px[3] == 0 for px in pixels) == entry["alpha_0_count"]
    assert sum(0 < px[3] < 255 for px in pixels) == entry["alpha_partial_count"]
    assert len(set(pixels)) == entry["unique_RGBA_colors"]
    images[entry["source_path"]] = image

with (HERE / "03_SOURCE_UV_FACE_APPLICATIONS_241.csv").open(newline="", encoding="utf-8") as f:
    faces = list(csv.DictReader(f))
assert len(faces) == 241
source_texels = 0
rectangles = set()
explicit = 0
inferred = 0
for face in faces:
    image = images[face["PNG_source_path"]]
    uv = json.loads(face["measured_source_UV_rectangle"])
    u1, v1, u2, v2 = uv
    assert all(isinstance(v, int) for v in uv)
    if face["original_UV_key_present"] == "true":
        assert uv == json.loads(face["original_explicit_UV_if_present"])
        assert face["UV_evidence_class"] == "original_explicit_face_uv"
        explicit += 1
    else:
        assert face["original_explicit_UV_if_present"] == ""
        assert uv == json.loads(face["calculated_implicit_UV_candidate"])
        assert face["UV_evidence_class"] == "computed_implicit_UV_candidate_not_in_source"
        inferred += 1
    x1, x2 = sorted((u1, u2))
    y1, y2 = sorted((v1, v2))
    assert 0 <= x1 < x2 <= 16 and 0 <= y1 < y2 <= 16
    selected = [image.getpixel((x, y)) for y in range(y1, y2) for x in range(x1, x2)]
    assert len(selected) == int(face["sampled_RGBA_pixel_count_per_face"])
    assert sum(px[3] == 0 for px in selected) == int(face["source_alpha0_pixels_per_face"])
    assert sum(px[3] == 255 for px in selected) == int(face["source_alpha255_pixels_per_face"])
    assert sum(0 < px[3] < 255 for px in selected) == int(face["source_alpha_partial_pixels_per_face"])
    assert len(set(selected)) == int(face["sampled_distinct_RGBA_colors"])
    rectangles.add((face["PNG_source_path"], tuple(uv)))
    source_texels += len(selected)

assert (explicit, inferred, len(rectangles), source_texels) == (73, 168, 21, 28076)
for suffix, uv in {"cake_side": [1, 8, 15, 16], "cake_top": [1, 1, 15, 15],
                   "cake_bottom": [1, 1, 15, 15]}.items():
    image = images["1.21.11/assets/minecraft/textures/block/" + suffix + ".png"]
    opaque_mask = {(x, y) for y in range(16) for x in range(16)
                   if image.getpixel((x, y))[3] == 255}
    u1, v1, u2, v2 = uv
    candidate = {(x, y) for y in range(v1, v2) for x in range(u1, u2)}
    assert opaque_mask == candidate, suffix
print("v55 PASS: 9 original Git SHA PNGs, 241 face refs, 21 UV regions, 28,076 source samples")
