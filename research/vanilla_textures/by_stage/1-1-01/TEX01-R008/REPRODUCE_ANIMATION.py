#!/usr/bin/env python3
"""Reproduce stage 1-1-01 animation/source frame measurements on a local checkout.
Usage: python REPRODUCE_ANIMATION.py /path/to/Minecraft_Furniture_Style_Research
Requires Pillow and numpy; no Minecraft runtime and no network required.
"""
import io, json, zlib, hashlib, sys, csv
from pathlib import Path
import numpy as np
from PIL import Image
repo = Path(sys.argv[1] if len(sys.argv)>1 else ".")
texture_root = repo/"1.21.11/assets/minecraft/textures/block"
stage = json.loads((repo/"docs/vanilla_texture_1-1/stages/1-1-01/STATE.json").read_text(encoding="utf-8"))
target_names = [x["texture_id"] for x in stage["items"]] + ["spruce_log_top","birch_log_top","stripped_oak_log_top"]
assert len(target_names)==21 and len(set(target_names))==21
for name in target_names:
    p=texture_root/(name+".png")
    assert p.is_file() and not p.with_name(p.name+".mcmeta").exists(), p
    with Image.open(p) as image: assert image.size==(16,16)
names=["crimson_stem","warped_stem","campfire_log_lit","soul_campfire_log_lit"]
frames={}
rows=[]
stats=[]
for name in names:
    src=texture_root/(name+".png")
    meta=json.loads((texture_root/(name+".png.mcmeta")).read_text(encoding="utf-8"))
    a=meta["animation"]
    raw=src.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    cur=8; chunks=0
    while cur<len(raw):
        size=int.from_bytes(raw[cur:cur+4],"big")
        assert (zlib.crc32(raw[cur+4:cur+size+8])&0xffffffff)==int.from_bytes(raw[cur+size+8:cur+size+12],"big")
        chunks+=1;cur+=size+12
    assert cur==len(raw) and chunks==4
    im=np.asarray(Image.open(io.BytesIO(raw)).convert("RGBA"))
    assert im.shape[1]==16 and im.shape[0]%16==0 and np.all(im[:,:,3]==255)
    fr=[im[i:i+16,:,:3].astype(np.int16) for i in range(0,im.shape[0],16)]
    frames[name]=fr
    assert "frames" not in a and a["interpolate"] is True
    hashes=[hashlib.sha256(f.astype(np.uint8).tobytes()).hexdigest() for f in fr]
    assert len(set(hashes))==len(fr)
    stats.append((name,hashlib.sha256(raw).hexdigest(),im.shape[0],len(fr),a["frametime"],len(fr)*a["frametime"]))
    for i in range(len(fr)):
        nxt=fr[(i+1)%len(fr)]
        rows.append((name,i,(i+1)%len(fr),int(np.any(fr[i]!=nxt,axis=2).sum()),round(float(np.abs(fr[i]-nxt).mean()),4),hashes[i]))
assert len(rows)==18
for l,r in [("crimson_stem","warped_stem"),("campfire_log_lit","soul_campfire_log_lit")]:
    for i in range(len(frames[l])):
        x,y=frames[l],frames[r]
        assert np.array_equal(np.any(x[i]!=x[(i+1)%len(x)],axis=2),np.any(y[i]!=y[(i+1)%len(y)],axis=2))
with open("TEX01_R008_recomputed_transitions.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["texture_id","frame_index","next_frame_index_with_wrap","changed_RGB_pixels_16x16","mean_absolute_RGB_channel_difference","frame_RGB_bytes_SHA256"]);w.writerows(rows)
print("audited_static",len(target_names),"animated",len(stats),"frame_transitions",len(rows))
for stat in stats:print(stat)
