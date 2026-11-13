#!/usr/bin/env python3
"""Reproduce TEX07-R008 on an unmodified, extracted Minecraft 1.21.11/ tree.
Standard library only. Examines source images/metadata/models, NOT game runtime.
Run: python REPRODUCE.py --root ./1.21.11 --output SOURCE_LEDGER.csv
"""
import argparse
import binascii
import csv
import hashlib
import json
from pathlib import Path
import struct

COLORS = ("white","black","red","blue","green","yellow","gray")
COLS = ["texture_id","user_source_path","source_git_blob_sha1","sha256_pinned_R003",
        "png_bytes","width","height","png_indexed_color_type","png_bit_depth",
        "png_chunks","png_all_crc_valid","png_apng_chunk_count","png_image_cells_16x16",
        "companion_mcmeta_path","mcmeta_exists_at_pinned_source","mcmeta_exists_at_main",
        "blockstate_path","blockstate_variant_count","block_model_path","block_model_parent",
        "item_path","item_model_type","shared_parent_chain","frame_or_timeline_json_found",
        "animation_source_result"]

def read_png(file):
    b = file.read_bytes()
    assert b.startswith(b"\x89PNG\r\n\x1a\n"), file
    pos, chunks = 8, []
    width=height=depth=color=interlace=None
    while pos < len(b):
        assert pos + 12 <= len(b), ("truncated",file)
        size = struct.unpack_from(">I",b,pos)[0]
        end = pos + 12 + size
        assert end <= len(b), ("bad chunk length",file)
        kind = b[pos+4:pos+8].decode("ascii")
        crc_expected=struct.unpack_from(">I",b,pos+8+size)[0]
        crc_actual=binascii.crc32(b[pos+4:pos+8+size]) & 0xffffffff
        assert crc_expected == crc_actual, ("CRC mismatch",file,kind)
        chunks.append(kind)
        if kind == "IHDR":
            width,height,depth,color,compression,filter_method,interlace = struct.unpack_from(
                ">IIBBBBB",b,pos+8)
            assert compression == 0 and filter_method == 0
        pos=end
        if kind == "IEND":
            break
    assert pos == len(b), ("trailing data",file)
    assert chunks == ["IHDR","PLTE","IDAT","IEND"], (file,chunks)
    assert width==16 and height==16 and color==3 and interlace==0, file
    return b,width,height,depth,color,chunks

def load_json(root,rel):
    return json.loads((root/rel).read_text(encoding="utf-8"))

def verify(root,color):
    t=color+"_concrete"
    png_rel=f"assets/minecraft/textures/block/{t}.png"
    b,w,h,depth,ctype,chunks=read_png(root/png_rel)
    meta=root/(png_rel+".mcmeta")
    assert not meta.exists(), f"Unexpected texture animation metadata: {meta}"
    bs_rel=f"assets/minecraft/blockstates/{t}.json"
    mod_rel=f"assets/minecraft/models/block/{t}.json"
    item_rel=f"assets/minecraft/items/{t}.json"
    bs=load_json(root,bs_rel)
    mod=load_json(root,mod_rel)
    item=load_json(root,item_rel)
    assert bs=={"variants":{"":{"model":f"minecraft:block/{t}"}}},(t,"blockstate")
    assert mod=={"parent":"minecraft:block/cube_all",
                 "textures":{"all":f"minecraft:block/{t}"}},(t,"block model")
    assert item=={"model":{"type":"minecraft:model",
                  "model":f"minecraft:block/{t}"}},(t,"item")
    blob_sha=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    return dict(texture_id=t,user_source_path="1.21.11/"+png_rel,
        source_git_blob_sha1=blob_sha,sha256_pinned_R003=hashlib.sha256(b).hexdigest(),
        png_bytes=len(b),width=w,height=h,png_indexed_color_type=ctype,
        png_bit_depth=depth,png_chunks="/".join(chunks),png_all_crc_valid="true",
        png_apng_chunk_count=0,png_image_cells_16x16=1,
        companion_mcmeta_path="1.21.11/"+png_rel+".mcmeta",
        mcmeta_exists_at_pinned_source="false",mcmeta_exists_at_main="false",
        blockstate_path="1.21.11/"+bs_rel,blockstate_variant_count=1,
        block_model_path="1.21.11/"+mod_rel,block_model_parent=mod["parent"],
        item_path="1.21.11/"+item_rel,item_model_type=item["model"]["type"],
        shared_parent_chain="minecraft:block/cube_all>block/cube>block/block",
        frame_or_timeline_json_found="false",
        animation_source_result="no_animation_defined_in_the_supplied_source_files")

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True,help="Unmodified extracted 1.21.11 directory")
    p.add_argument("--output",default="SOURCE_LEDGER.csv")
    args=p.parse_args()
    root=Path(args.root)
    a=load_json(root,"assets/minecraft/models/block/cube_all.json")
    b=load_json(root,"assets/minecraft/models/block/cube.json")
    c=load_json(root,"assets/minecraft/models/block/block.json")
    assert a["parent"] == "block/cube"
    assert b["parent"] == "block/block"
    assert len(b["elements"]) == 1 and len(b["elements"][0]["faces"]) == 6
    assert "display" in c and "elements" not in c
    rows=[verify(root,color) for color in COLORS]
    with open(args.output,"w",encoding="utf-8",newline="") as file:
        writer=csv.DictWriter(file,fieldnames=COLS,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("Checked 7 PNG / 7 absent animation .png.mcmeta / 24 JSON (incl parents).")
    print("Source-based texture animation: 0/7 defined; runtime not checked.")
