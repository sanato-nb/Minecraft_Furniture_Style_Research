#!/usr/bin/env python3
# v13 PNG pixel study repro: run against locally checked-out, licensed mod source files.
# Original PNGs are NOT included in the research repository and must not be republished.
from __future__ import annotations
import argparse
import csv
import hashlib
from pathlib import Path
from collections import Counter
from PIL import Image
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("Another Furniture", "research/furniture_mods/v11/texture_png_header_12.csv",
     "another", "git_sha"),
    ("Handcrafted", "research/furniture_mods/v12/handcrafted_png_header_12.csv",
     "handcrafted", "git_blob_sha"),
]
COLUMNS = ["mod","name","width","height","png_bytes","png_type","visible",
           "transparent","partial","opaque","coverage","unique_rgba",
           "avg_rgb","luminance","bounds","top_colors","sha","path"]

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\x00"+data).hexdigest()

def measure(data: bytes):
    with Image.open(BytesIO(data)) as img:
        width, height = img.size
        pixels = list(img.convert("RGBA").getdata())
        color_type = {"RGB":2, "P":3, "RGBA":6}.get(img.mode, -1)
    visible = [(i,r,g,b,a) for i,(r,g,b,a) in enumerate(pixels) if a>0]
    transparent = len(pixels)-len(visible)
    partial = sum(1 for i,r,g,b,a in visible if a<255)
    opaque = len(visible)-partial
    colors = {(r,g,b,a) for i,r,g,b,a in visible}
    hist = Counter((r,g,b) for i,r,g,b,a in visible)
    weighted = sum(a/255 for i,r,g,b,a in visible)
    def mean(ch):
        return round(sum((r,g,b)[ch]*(a/255) for i,r,g,b,a in visible)/weighted) if weighted else 0
    lum = (sum((0.2126*r+0.7152*g+0.0722*b)*a/255 for i,r,g,b,a in visible)/weighted
           if weighted else 0)
    xs = [i % width for i,*rest in visible]
    ys = [i // width for i,*rest in visible]
    bounds = f"{min(xs)}:{min(ys)}:{max(xs)}:{max(ys)}" if xs else ""
    top = ";".join(f"#{r:02X}{g:02X}{b:02X}:{n}"
                   for (r,g,b),n in sorted(hist.items(),key=lambda kv:-kv[1])[:3])
    return dict(width=width,height=height,png_bytes=len(data),png_type=color_type,
                visible=len(visible),transparent=transparent,partial=partial,
                opaque=opaque,coverage=round(100*len(visible)/len(pixels),2),
                unique_rgba=len(colors),avg_rgb=";".join(str(mean(i)) for i in range(3)),
                luminance=round(lum,2),bounds=bounds,top_colors=top)

def main():
    parser=argparse.ArgumentParser(description="Recalculate v13 pixel statistics locally.")
    parser.add_argument("--another", type=Path, required=True, help="Local AnotherFurniture repo root at v11 pinned commit")
    parser.add_argument("--handcrafted", type=Path, required=True, help="Local Handcrafted repo root at v12 pinned commit")
    parser.add_argument("--out", type=Path, default=Path("v13_recalculated_pixels.csv"))
    args=parser.parse_args()
    roots={"another":args.another,"handcrafted":args.handcrafted}
    result=[]
    for mod,manifest,root_name,sha_col in SOURCES:
        with (ROOT / manifest).open(encoding="utf-8",newline="") as f:
            rows=list(csv.DictReader(f))
        for record in rows:
            source=roots[root_name]/record["source_path"]
            if not source.is_file():
                raise FileNotFoundError(f"Missing original PNG: {source}")
            data=source.read_bytes()
            expected=record[sha_col].lower()
            actual=blob_sha(data)
            if expected!=actual:
                raise ValueError(f"Wrong source/version for {source}: {actual} != {expected}")
            m=measure(data)
            if (m["width"],m["height"])!=(int(record["width"]),int(record["height"])):
                raise ValueError(f"IHDR mismatch: {source}")
            result.append(dict(mod=mod,name=record["name"],**m,sha=actual,path=record["source_path"]))
    if len(result)!=24:
        raise ValueError(f"Expected 24 files, got {len(result)}")
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=COLUMNS);w.writeheader();w.writerows(result)
    print(f"Validated {len(result)} original PNGs by Git blob SHA-1 and decoded all pixels.")
    print(f"Saved measurements: {args.out}")

if __name__=="__main__":
    main()
