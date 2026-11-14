#!/usr/bin/env python3
"""v61 cauldron source audit. Run from a full original Minecraft 1.21.11 assets checkout with Pillow.
Verifies directly read Git blob identities, 5 static PNG RGBA rasters, original JSON geometry and 8 source blockstate variants.
Animated water/lava PNG IHDR and blob SHA are verified, not decoded for actual frame raster; client renderer not executed.
"""
from pathlib import Path
from PIL import Image
import json, hashlib, struct, io

repo = Path(__file__).resolve().parents[3]
d = Path(__file__).resolve().parent
models = json.loads((d/"00A_ORIGINAL_CAULDRON_MODELS_11.json").read_text(encoding="utf-8"))["models"]
sources = json.loads((d/"00B_ORIGINAL_BLOCKSTATES_4_MCMeta_2.json").read_text(encoding="utf-8"))["sources"]
manifest = json.loads((d/"00C_ORIGINAL_PNG_7_IHDR_PILLOW_STATIC5.json").read_text(encoding="utf-8"))["files"]
geometry = json.loads((d/"01_GEOMETRY_11_APPLIED_MODEL_AND_SOURCE_UV.json").read_text(encoding="utf-8"))
def original_blob(path):
    raw = (repo / path).read_bytes()
    sha = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw).hexdigest()
    return raw, sha
for item in models:
    raw,sha=original_blob(item["path"])
    assert sha==item["sha"] and json.loads(raw)==item["original"]
for item in sources:
    raw,sha=original_blob(item["path"])
    assert sha==item["sha"] and json.loads(raw)==item["original"]
full=0
for item in manifest:
    raw,sha=original_blob(item["path"])
    assert sha==item["git_blob_sha"]
    assert raw[:8]==b"\x89PNG\r\n\x1a\n"
    w,h=struct.unpack(">II",raw[16:24])
    assert [w,h]==[item["original_IHDR_width"],item["original_IHDR_height"]]
    if item["independent_Pillow_RGBA_verified"]:
        im=Image.open(io.BytesIO(raw)).convert("RGBA")
        assert hashlib.sha256(raw).hexdigest()==item["independent_png_sha256"]
        assert hashlib.sha256(im.tobytes()).hexdigest()==item["independent_decodedRGBA_sha256"]
        alpha=[px[3] for px in im.getdata()]
        assert alpha.count(255)==item["original_alpha255"] and alpha.count(0)==item["original_alpha0"]
        full+=w*h
assert len(models)==11 and len(sources)==6 and len(manifest)==7
assert geometry["summary"]["effective_faces"]==648
assert geometry["summary"]["effective_explicit_uv"]==0
assert geometry["summary"]["effective_missing_uv"]==648
assert full==1280
print("PASS: 11 source models, 6 JSON/mcmeta, 7 PNG Git identities/IHDR, 5 decoded PNGs 1280 RGBA pixels, 648 source faces.")
print("WARNING: No client renderer or implicit UV certification; no full-frame water/lava raster pixel audit.")
