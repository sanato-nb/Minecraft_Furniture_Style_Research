#!/usr/bin/env python3
"""Reproduce v58 source-PNG metrics from ORIGINAL local GitHub checkout files.
Requires Pillow; does NOT validate Minecraft engine UV generation or rendering.
Usage from anywhere: python research/vanilla_models/v58/REPRODUCE_V58_ORIGINAL_PNG_AUDIT.py
"""
from pathlib import Path
from collections import Counter
from io import BytesIO
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).resolve().parent / "04_ORIGINAL_PNG_4_SOURCE_RGBA_UV.json"
evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
m = evidence["metrics"]
photos = {}
source_rgba = 0
for r in evidence["Pillow_source_path_records"]:
    full_path = ROOT / r["full_source_path"]
    raw = full_path.read_bytes()
    git_sha = hashlib.sha1(("blob " + str(len(raw)) + "\0").encode() + raw).hexdigest()
    sha256 = hashlib.sha256(raw).hexdigest()
    assert git_sha == r["git_blob_sha"], (str(full_path), "git SHA")
    assert sha256 == r["independent_source_SHA256"], (str(full_path), "sha256")
    assert len(raw) == r["source_bytes"], (str(full_path), "byte length")
    with Image.open(BytesIO(raw)) as src:
        im = src.convert("RGBA")
    assert list(im.size) == r["image_size"], (str(full_path), "dimensions")
    pix = [im.getpixel((x, y)) for y in range(im.height) for x in range(im.width)]
    alpha = Counter(v[3] for v in pix)
    assert len(pix) == r["Pillow_RGBA_full_pixel_count"]
    assert alpha[0] == r["source_alpha0_pixels"]
    assert alpha[255] == r["source_alpha255_pixels"]
    assert sum(v for k, v in alpha.items() if 0 < k < 255) == r["source_partial_alpha_pixels"]
    assert len(set(pix)) == r["distinct_RGBA"]
    photos[r["full_source_path"]] = im
    source_rgba += len(pix)

explicit = candidate = explicit_pixels = candidate_pixels = 0
unique_source_coords = set()
for f in evidence["face_pixel_sample_records"]:
    im = photos[f["source_PNG_path"]]
    x0, y0, x1, y1 = f["uv_source_pixel_rectangle"]
    assert 0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height
    pixels = [im.getpixel((x, y)) for y in range(y0, y1) for x in range(x0, x1)]
    assert len(pixels) == f["source_rgba_rect_pixel_uses"]
    assert sum(px[3] == 255 for px in pixels) == f["source_rgba_alpha255_uses"]
    assert sum(px[3] == 0 for px in pixels) == f["source_rgba_alpha0_uses"]
    for y in range(y0, y1):
        for x in range(x0, x1):
            unique_source_coords.add((f["source_PNG_path"], x, y))
    if f["uv_evidence_class"] == "original_source_explicit_uv":
        assert f["original_declared_UV"] is not None and f["computed_candidate_UV"] is None
        explicit += 1
        explicit_pixels += len(pixels)
    elif f["uv_evidence_class"] == "geometry_candidate_not_engine_authenticated":
        assert f["computed_candidate_UV"] is not None and f["original_declared_UV"] is None
        candidate += 1
        candidate_pixels += len(pixels)
    else:
        raise AssertionError(f["uv_evidence_class"])

assert source_rgba == m["source_png_pixels_rgba_total"] == 1024
assert explicit == m["explicit_source_face_refs"] == 13
assert candidate == m["candidate_source_face_refs"] == 8
assert explicit_pixels == m["explicit_source_pixel_uses"] == 768
assert candidate_pixels == m["candidate_source_pixel_uses"] == 1152
assert len(unique_source_coords) == m["unique_PNG_source_coords"] == 800
print(json.dumps({
    "status": "PASS", "source_png_paths": len(photos),
    "original_png_rgba_pixels": source_rgba,
    "original_explicit_uv_faces": explicit,
    "original_explicit_uv_texel_uses": explicit_pixels,
    "geometry_derived_candidate_uv_faces": candidate,
    "candidate_uv_texel_uses": candidate_pixels,
    "unique_png_source_coordinates": len(unique_source_coords),
    "engine_uv_authenticated": False, "runtime_render_checked": False
}, ensure_ascii=False, indent=2))
