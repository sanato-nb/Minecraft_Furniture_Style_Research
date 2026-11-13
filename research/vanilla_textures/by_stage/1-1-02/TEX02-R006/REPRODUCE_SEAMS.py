#!/usr/bin/env python3
"""TEX02-R006 source-PNG-only seam experiment. Requires Pillow. NOT an in-game renderer."""
import argparse,csv,hashlib,io,struct,zlib
from pathlib import Path
from PIL import Image

NAMES = ["bricks","stone_bricks","deepslate_bricks","deepslate","deepslate_top","stone"]
TRANSFORMS = ["I","H_UV_reverse","R90_screen_CW","R180_screen"]
def verify_png(raw):
    assert raw[:8] == bytes.fromhex("89504e470d0a1a0a")
    i=8
    while i<len(raw):
        n=int.from_bytes(raw[i:i+4],"big")
        typ=raw[i+4:i+8];payload=raw[i+8:i+8+n]
        crc=int.from_bytes(raw[i+8+n:i+12+n],"big")
        assert zlib.crc32(typ+payload)&0xffffffff==crc,typ
        i+=n+12
        if typ==b"IEND": break
    assert i==len(raw)
def transformed(img,code):
    if code=="I": return img
    if code=="H_UV_reverse": return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if code=="R90_screen_CW": return img.transpose(Image.Transpose.ROTATE_270)
    if code=="R180_screen": return img.transpose(Image.Transpose.ROTATE_180)
    raise ValueError(code)
def boundary(img,direction,first):
    p=img.load()
    if direction=="east_to_west":
        return [p[15 if first else 0,y] for y in range(16)]
    return [p[x,15 if first else 0] for x in range(16)]
def run(root,output):
    path=root/"assets/minecraft/textures/block"
    rows=[]
    for name in NAMES:
        raw=(path/(name+".png")).read_bytes()
        verify_png(raw)
        im=Image.open(io.BytesIO(raw)).convert("RGBA")
        assert im.size==(16,16) and all(p[3]==255 for p in im.getdata())
        arr={t:transformed(im,t) for t in TRANSFORMS}
        for a in TRANSFORMS:
            for b in TRANSFORMS:
                for d in ("east_to_west","south_to_north"):
                    v1=boundary(arr[a],d,True);v2=boundary(arr[b],d,False)
                    sm=sum(abs(x[c]-y[c]) for x,y in zip(v1,v2) for c in range(3))
                    mismatch=sum(any(x[c]!=y[c] for c in range(3)) for x,y in zip(v1,v2))
                    rows.append([name,a,b,d,f"{sm/48:.6f}",sm,mismatch,16,3,"user_GitHub_1.21.11_extracted_PNG","source_pixel_hypothetical_tiled_2D_not_ingame"])
    assert len(rows)==192
    with output.open("w",newline="",encoding="utf-8") as f:
        writer=csv.writer(f)
        writer.writerow(["texture","left_or_top_transform","right_or_bottom_transform","adjacency","mean_absolute_rgb_per_channel","sum_absolute_rgb_16x3","mismatched_edge_pixels_16","pixels_compared","rgb_channels","source_provenance","evidence_type"])
        writer.writerows(rows)
    print(f"{len(rows)} measured hypothetical 2D seam rows written to {output}")
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[5]/"1.21.11",help="User-provided extracted 1.21.11 directory")
    parser.add_argument("--output",type=Path,default=Path("HYPOTHETICAL_UV_SEAMS.csv"))
    args=parser.parse_args()
    run(args.root,args.output)
