#!/usr/bin/env python3
"""TEX01-R006 exact reproducibility on user-supplied 1.21.11/ extracted JAR assets. 
Run: python REPRODUCE_D4.py /path/to/Minecraft_Furniture_Style_Research
Needs: Pillow, numpy. Never claims runtime/world UV verification.
"""
import sys, hashlib, zlib, csv, json, io
from pathlib import Path
from PIL import Image
import numpy as np

root = Path(sys.argv[1] if len(sys.argv)>1 else ".")
state = json.loads((root/"docs/vanilla_texture_1-1/stages/1-1-01/STATE.json").read_text(encoding="utf-8"))
items = state["items"]
names = ("rot90","rot180","rot270","flip_lr","flip_tb","transpose","anti_transpose")
cols = ["texture_id","source_PNG_SHA256_against_live_STATE","verified_png_chunk_count"]
for n in names: cols += [n+"_changed_pixels",n+"_RGB_MAE"]
rows = []
for item in items:
    p = root/"1.21.11"/item["source_path"]
    raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == item["v4_sha256"], p
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    cur = 8; chunks = 0
    while cur < len(raw):
        length = int.from_bytes(raw[cur:cur+4], "big")
        kind, body = raw[cur+4:cur+8], raw[cur+8:cur+8+length]
        stored_crc = int.from_bytes(raw[cur+8+length:cur+12+length], "big")
        assert (zlib.crc32(kind+body)&0xffffffff) == stored_crc
        cur += 12+length; chunks += 1
    assert cur == len(raw)
    rgba = np.asarray(Image.open(io.BytesIO(raw)).convert("RGBA"))
    assert rgba.shape == (16,16,4) and np.all(rgba[:,:,3]==255)
    im = rgba[:,:,:3].astype(np.int16)
    transforms = [np.rot90(im,1),np.rot90(im,2),np.rot90(im,3),
                  np.fliplr(im),np.flipud(im),np.transpose(im,(1,0,2)),
                  np.transpose(im,(1,0,2))[::-1,::-1]]
    row = [item["texture_id"],hashlib.sha256(raw).hexdigest(),chunks]
    for v in transforms:
        row += [int(np.any(im!=v,axis=2).sum()),round(float(np.abs(im-v).mean()),4)]
    rows.append(row)
    if item["texture_id"]=="oak_log_top":
        changed = np.any(im!=transforms[1],axis=2)
        mask = "".join(f"{int(''.join('1' if b else '0' for b in line),2):04x}" for line in changed)
        print("oak_log_top changed",int(changed.sum()),"mask",mask)
assert len(rows)==18
out = Path("R006_REPRODUCED_D4.csv")
with out.open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f); w.writerow(cols); w.writerows(rows)
print("wrote",out,"rows",len(rows))
