#!/usr/bin/env python3
"""Reproduce v60 lantern source PNG / model face / animation-metadata audit.

Requirements: Pillow and a full checkout of this repository including
1.21.11/assets/minecraft/. The original face.uv is used literally and cropped
after min/max normalization (UV flips/orientation are NOT engine certified).
No Minecraft client code is executed.
"""
from __future__ import annotations
import hashlib, io, json
from collections import Counter
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = json.loads((HERE / "03_LANTERN_SOURCE_PNG_6_RGBA_3FRAMES.json").read_text(encoding="utf-8"))
SOURCES = []
for source_file in ("00A_LANTERN_SOURCE_MODELS_7.json", "00B_LANTERN_SOURCE_MODELS_7.json"):
    SOURCES.extend(json.loads((HERE / source_file).read_text(encoding="utf-8"))["files"])
SOURCES_BY_PATH = {record["full_source_path"]: record for record in SOURCES}

def git_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

for model in SOURCES:
    content = (ROOT / model["full_source_path"]).read_bytes()
    assert git_sha(content) == model["git_blob_sha"], model["full_source_path"]
    assert json.loads(content.decode("utf-8")) == model["original"], model["full_source_path"]

total_alpha0 = total_alpha255 = full_rgba_pixels = 0
images = {}
for tex in EVIDENCE["records"]:
    raw = (ROOT / tex["full_source_path"]).read_bytes()
    assert git_sha(raw) == tex["git_blob_sha"], tex["full_source_path"]
    assert hashlib.sha256(raw).hexdigest() == tex["original_binary_sha256"]
    assert len(raw) == tex["original_png_bytes"]
    im = Image.open(io.BytesIO(raw)).convert("RGBA")
    assert [im.width, im.height] == tex["original_resolution"] == [16,48]
    assert hashlib.sha256(im.tobytes()).hexdigest() == tex["Pillow_RGBA_sha256"]
    hist = Counter(px[3] for px in im.get_flattened_data())
    assert hist[0] == tex["RGBA_alpha_zero_pixels"]
    assert hist[255] == tex["RGBA_alpha_255_pixels"]
    assert len(set(im.get_flattened_data())) == tex["original_RGBA_unique_colors"]
    assert sum(hist.values()) == 768
    assert len({hashlib.sha256(im.crop((0,y*16,16,(y+1)*16)).tobytes()).hexdigest() for y in range(3)}) == 3
    full_rgba_pixels += im.width*im.height
    total_alpha0 += hist[0]
    total_alpha255 += hist[255]
    images[tex["full_source_path"]] = im
    mcp = tex["full_source_path"] + ".mcmeta"
    assert json.loads((ROOT / mcp).read_text(encoding="utf-8"))["animation"]["frametime"] == 8

checked_face_frames = weighted = opaque = transparent = 0
coords = set()
for audit in EVIDENCE["leaf_face_pixel_audits"]:
    model = SOURCES_BY_PATH[audit["leaf_model_full_source_path"]]
    parent = SOURCES_BY_PATH[audit["parent_template_path"]]
    assert model["original"]["parent"].split("/")[-1] == audit["parent_template_path"].split("/")[-1].removesuffix(".json")
    assert not model["original"].get("elements")
    slot = model["original"]["textures"]["lantern"].removeprefix("minecraft:")
    path = "1.21.11/assets/minecraft/textures/" + slot + ".png"
    im = images[path]
    sha = hashlib.sha256()
    local_coords = set()
    local_weighted = local_opaque = local_transparent = local_count = 0
    for frame in range(3):
        for el in parent["original"]["elements"]:
            for face in el["faces"].values():
                uv = face["uv"]
                u0,u1 = sorted((uv[0],uv[2]))
                v0,v1 = sorted((uv[1],uv[3]))
                assert all(float(q).is_integer() for q in (u0,u1,v0,v1))
                u0,u1,v0,v1 = map(int,(u0,u1,v0,v1))
                assert 0 <= u0 < u1 <= 16 and 0 <= v0 < v1 <= 16
                crop = im.crop((u0, v0 + frame*16, u1, v1 + frame*16))
                raw = crop.tobytes()
                sha.update(raw)
                local_count += 1
                local_weighted += crop.width * crop.height
                alpha = Counter(px[3] for px in crop.get_flattened_data())
                local_opaque += alpha[255]
                local_transparent += alpha[0]
                assert sum(alpha.values()) == crop.width*crop.height
                for y in range(v0+frame*16, v1+frame*16):
                    for x in range(u0,u1):
                        local_coords.add((x,y))
                        coords.add((path,x,y))
    assert local_count == audit["face_frame_pixel_checks"]
    assert local_weighted == audit["weighted_RGBA_source_pixel_uses"]
    assert local_opaque == audit["opaque_uses"]
    assert local_transparent == audit["transparent_uses"]
    assert len(local_coords) == audit["unique_PNG_source_pixel_coordinates"]
    assert sha.hexdigest() == audit["all_frame_crop_group_RGBA_sha256"]
    checked_face_frames += local_count
    weighted += local_weighted
    opaque += local_opaque
    transparent += local_transparent

overall = EVIDENCE["overall"]
assert full_rgba_pixels == overall["original_full_RGBA_pixels"] == 4608
assert total_alpha0 == overall["original_full_RGBA_alpha0"] == 2700
assert total_alpha255 == overall["original_full_RGBA_alpha255"] == 1908
assert checked_face_frames == overall["explicitUV_face_frame_pixel_checks"] == 558
assert weighted == overall["weighted_original_source_RGBA_pixel_uses"] == 12168
assert opaque == overall["weighted_opaque_uses"] == 11736
assert transparent == overall["weighted_transparent_uses"] == 432
assert len(coords) == overall["unique_original_PNG_file_pixel_coordinates_across_both_models_and_three_frames"] == 2088
print("PASSED: 14 original model SHA, 6 PNG SHA/Pillow RGBA, 6 mcmeta frametime,",
      checked_face_frames, "face/frame checks,", weighted, "pixel uses,", len(coords), "unique file/pixel coords")
