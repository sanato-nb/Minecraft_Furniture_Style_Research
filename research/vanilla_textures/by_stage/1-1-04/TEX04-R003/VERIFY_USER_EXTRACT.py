#!/usr/bin/env python3
"""TEX04-R003: verify nine wool textures and static model JSON in a LOCAL checkout.

Reads only; no network, no animation, no file edits.
The user-provided extraction can match the mirror without proving the original JAR SHA-1.
"""
import argparse
import csv
import hashlib
import json
import struct
import zlib
from pathlib import Path

COLORS = ("white", "red", "blue", "black", "green", "yellow", "purple", "cyan", "orange")
CORRECT_BLACK_BLOB_SHA = "7fea63ff530cad3b51435e662daa2c4d6324bd8a"
FACES = {"up", "down", "north", "south", "east", "west"}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def check_png(data: bytes) -> dict:
    assert data.startswith(PNG_SIGNATURE), "PNG signature mismatch"
    off, types, crc_count = len(PNG_SIGNATURE), [], 0
    width = height = color_type = None
    while off < len(data):
        assert len(data) - off >= 12, "truncated PNG chunk"
        n = struct.unpack(">I", data[off:off+4])[0]
        end = off + 12 + n
        assert end <= len(data), "out-of-bounds PNG chunk"
        kind = data[off+4:off+8]
        payload = data[off+8:off+8+n]
        actual = zlib.crc32(kind + payload) & 0xffffffff
        stated = struct.unpack(">I", data[off+8+n:end])[0]
        assert actual == stated, f"CRC mismatch {kind!r}"
        types.append(kind.decode("ascii")); crc_count += 1
        if kind == b"IHDR":
            width, height, bit_depth, color_type, _, _, _ = struct.unpack(">IIBBBBB", payload)
            assert bit_depth == 8, "unexpected bit depth"
        off = end
        if kind == b"IEND": break
    assert off == len(data) and types == ["IHDR", "PLTE", "IDAT", "IEND"], types
    assert (width, height, color_type) == (16, 16, 3), (width, height, color_type)
    return {"bytes": len(data), "width":width, "height":height,
            "color_type":color_type, "png_chunk_crc_passed":crc_count}

def load_json(root: Path, path: str):
    data = (root / path).read_bytes()
    return json.loads(data.decode("utf-8")), git_blob_sha(data)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository_checkout", type=Path, help="root of Minecraft_Furniture_Style_Research checkout")
    args = parser.parse_args()
    repo = args.repository_checkout
    src = repo / "1.21.11"
    ledger = repo / "research/vanilla_textures/by_stage/1-1-04/TEX04-R001/SOURCE_LEDGER.csv"
    with ledger.open(encoding="utf-8-sig", newline="") as f:
        records = {r["texture_id"]: r for r in csv.DictReader(f)}
    assert set(records) == {c + "_wool" for c in COLORS}, "ledger has unexpected scope"

    version, _ = load_json(src, "version.json")
    assert version["id"] == "1.21.11", "extracted version.json ID mismatch"

    cube_all, _ = load_json(src, "assets/minecraft/models/block/cube_all.json")
    cube, _ = load_json(src, "assets/minecraft/models/block/cube.json")
    base, _ = load_json(src, "assets/minecraft/models/block/block.json")
    assert cube_all["parent"] == "block/cube"
    assert cube["parent"] == "block/block"
    assert cube["elements"][0]["from"] == [0, 0, 0]
    assert cube["elements"][0]["to"] == [16, 16, 16]
    assert set(cube["elements"][0]["faces"]) == FACES
    assert set(cube_all["textures"][f] for f in FACES) == {"#all"}
    assert isinstance(base.get("display"), dict)

    status = []
    for color in COLORS:
        name = color + "_wool"
        rec = records[name]
        png_path = "assets/minecraft/textures/block/" + name + ".png"
        data = (src / png_path).read_bytes()
        png = check_png(data)
        actual_sha = hashlib.sha256(data).hexdigest()
        assert actual_sha == rec["new_source_sha256"], "PNG SHA256 mismatch: " + name
        assert actual_sha == rec["v4_source_sha256"]
        blob = git_blob_sha(data)
        assert blob == rec["source_git_blob_sha"], "PNG Git blob mismatch: " + name

        model, model_blob = load_json(src, "assets/minecraft/models/block/" + name + ".json")
        state, state_blob = load_json(src, "assets/minecraft/blockstates/" + name + ".json")
        expected_model = (CORRECT_BLACK_BLOB_SHA if color == "black"
                          else rec["model_git_blob_sha"])
        assert model_blob == expected_model, "model blob mismatch: " + name
        assert state_blob == rec["blockstate_git_blob_sha"], "blockstate blob mismatch: " + name
        assert model["parent"] == "minecraft:block/cube_all"
        assert model["textures"]["all"] == "minecraft:block/" + name
        assert set(state["variants"]) == {""}
        assert state["variants"][""]["model"] == "minecraft:block/" + name
        status.append({"texture_id": name, "png_SHA256": actual_sha,
                       "png_git_blob_sha":blob, "model_git_blob_sha":model_blob,
                       "blockstate_git_blob_sha":state_blob, **png})

    result = {
        "source": "user_provided_1.21.11_jar_extraction",
        "version_json_id":version["id"],
        "user_extraction_png_checked":len(status),
        "mirror_git_blob_reference_matching":len(status),
        "static_face_bindings_resolved":len(status)*len(FACES),
        "r001_black_wool_model_sha_erratum":"39-character typo in old ledger; corrected only in R003",
        "mojang_official_client_jar_authenticated_count":0,
        "ingame_static_verified_count":0,
        "animation_study_deferred":True,
        "items":status,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
