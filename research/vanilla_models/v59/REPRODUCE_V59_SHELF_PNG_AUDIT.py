#!/usr/bin/env python3
"""Re-run v59 source PNG and explicit front UV crop checks in a full repository checkout.
Needs Pillow and original 1.21.11 extracted assets present in repo root.
This verifies source evidence, NOT in-game texture sampling/orientation.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image

repo = Path(__file__).resolve().parents[3]
expected = json.loads((Path(__file__).parent / "04_SHELF_PNG_4_RGBA_AND_20_FRONT_UV.json").read_text(encoding="utf-8"))
loaded = {}
for rec in expected["files"]:
    path = repo / rec["path"]
    raw = path.read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    assert sha == rec["git_blob_sha"], (rec["path"], sha)
    assert hashlib.sha256(raw).hexdigest() == rec["sha256"]
    im = Image.open(path).convert("RGBA")
    assert list(im.size) == rec["dimensions"]
    assert hashlib.sha256(im.tobytes()).hexdigest() == rec["pillow_rgba_bytes_sha256"]
    assert sum(a == 255 for *_, a in im.getdata()) == rec["alpha255"]
    loaded[rec["path"]] = im

count = 0
for face in expected["front_sample_crops"]:
    template = repo / face["template_path"]
    uv = json.loads(template.read_text(encoding="utf-8"))["elements"][0]["faces"]["north"]["uv"]
    assert uv == face["uv_original"], (template, uv)
    im = loaded["1.21.11/assets/minecraft/textures/block/" + face["wood"] + "_shelf.png"]
    sample = im.crop(tuple(face["source_pixel_bounds"]))
    assert sample.width * sample.height == 128
    assert hashlib.sha256(sample.tobytes()).hexdigest() == face["source_crop_rgba_sha256"]
    count += 1
assert count == 20
print("v59 source-check PASSED: 4 PNG Git-SHA, SHA256, RGBA checks; 20 original-UV front crops; 2560 sampled pixels.")
