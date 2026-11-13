#!/usr/bin/env python3
"""TEX06-R005: reproduce source PNG pixel seam metrics (Pillow required).
From repository root: python research/vanilla_textures/by_stage/1-1-06/TEX06-R005/REPRODUCE_TOP_PIXEL_AUDIT.py
Does not execute Minecraft or certify an in-game rotation."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import hashlib, zlib, csv
ROOT=Path("1.21.11/assets/minecraft/textures/block")
SHA={"black_glazed_terracotta":"214ce8ca46c60a42b8863655b3895aca839c7ef7cfa511a192dc1974a0ca2758","white_glazed_terracotta":"cb1ebf9f3f3e93009ff4cab1b2b2b70d41fd87caa40c71942ae51996d12498b4"}
CASES=[["black_A_right_hand","black_glazed_terracotta",["north","west","east","south"],916,28],["black_B_opposite_projection","black_glazed_terracotta",["north","east","west","south"],4474,8],["white_A_right_hand","white_glazed_terracotta",["south","east","west","north"],412,44],["white_B_opposite_projection","white_glazed_terracotta",["south","west","east","north"],17174,14]]
Y={"south":0,"west":90,"north":180,"east":270}
SEAMS=[("upper_horizontal",0,1,"h"),("lower_horizontal",2,3,"h"),("left_vertical",0,2,"v"),("right_vertical",1,3,"v")]
def inv(x,y,d):
    return {0:(x,y),90:(y,15-x),180:(15-x,15-y),270:(15-y,x)}[d]
def check_png(data):
    assert data[:8]==bytes.fromhex("89504e470d0a1a0a")
    pos=8
    while pos<len(data):
        n=int.from_bytes(data[pos:pos+4],"big")
        typ=data[pos+4:pos+8]; payload=data[pos+8:pos+8+n]
        assert zlib.crc32(typ+payload)==int.from_bytes(data[pos+8+n:pos+12+n],"big")
        pos+=12+n
    assert pos==len(data)
IM={}
for tex,sha in SHA.items():
    data=(ROOT/(tex+".png")).read_bytes()
    assert hashlib.sha256(data).hexdigest()==sha
    check_png(data)
    IM[tex]=Image.open(BytesIO(data)).convert("RGBA")
    assert IM[tex].size==(16,16)
records=[]
for name,tex,facing,expected_l1,expected_equal in CASES:
    s=eq=0
    for seam,a,b,axis in SEAMS:
        for i in range(16):
            ax,ay=(15,i) if axis=="h" else (i,15)
            bx,by=(0,i) if axis=="h" else (i,0)
            sx,sy=inv(ax,ay,(360-Y[facing[a]])%360)
            tx,ty=inv(bx,by,(360-Y[facing[b]])%360)
            c1=IM[tex].getpixel((sx,sy));c2=IM[tex].getpixel((tx,ty))
            assert c1[3]==c2[3]==255
            d=sum(abs(c1[k]-c2[k]) for k in range(3))
            s+=d;eq+=(d==0)
            records.append([name,tex,seam,i,facing[a],facing[b],sx,sy,tx,ty,"|".join(map(str,c1)),"|".join(map(str,c2)),d,int(d==0)])
    assert (s,eq)==(expected_l1,expected_equal)
    print(name,"L1",s,"RGB_MAE",round(s/192,6),"exact",eq,"/64")
assert len(records)==256
with open("R005_REPRODUCED_SOURCE_SEAMS.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["panel","texture_id","seam","position","facing_a","facing_b","source_x_a","source_y_a","source_x_b","source_y_b","rgba_a","rgba_b","rgb_l1","exact_match"]);w.writerows(records)
