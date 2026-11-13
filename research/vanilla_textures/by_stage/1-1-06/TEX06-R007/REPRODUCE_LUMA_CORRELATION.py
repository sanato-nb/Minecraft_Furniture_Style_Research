#!/usr/bin/env python3
"""TEX06-R007: 8 source PNGs x 28 unordered pairs x 1024 transforms; source only.
Run from repository root: python research/vanilla_textures/by_stage/1-1-06/TEX06-R007/REPRODUCE_LUMA_CORRELATION.py
Requires Pillow and NumPy. Writes local R007_PAIRWISE_LUMA_28.csv.
No gameplay or Mojang compressed JAR certification.
"""
from pathlib import Path
from PIL import Image
from io import BytesIO
from itertools import combinations
import csv, hashlib, numpy as np, zlib
ROOT=Path("1.21.11/assets/minecraft/textures/block")
IDS=("terracotta","white_terracotta","orange_terracotta","blue_terracotta",
     "green_terracotta","yellow_terracotta","black_glazed_terracotta","white_glazed_terracotta")
SHA=(
"b2458267eac6b6f35d02990ee3244edf1f43fbe258bd6dfe15189cf2eaf42ae8",
"9feeb13f19514ea58a5b6e942df7a8595330e61173f8d0a13c83b78acd1bd62e",
"3074d90b0a27d1c149df2f3eacc9c6895c4cc0548999f864146dc18f64bcab5a",
"99b4ec0a8a02a9d609d4987cbb7ba594a59f93c76b5fd98e3a1f12c2df1f9a70",
"ffe10089bcef9873c74f18be35e605c5d035f472c06bf677746d39ff8a656c07",
"7c00bf901f78ad628a06335d47310a6b18c1419243d4150e32cdf01d51bafca6",
"214ce8ca46c60a42b8863655b3895aca839c7ef7cfa511a192dc1974a0ca2758",
"cb1ebf9f3f3e93009ff4cab1b2b2b70d41fd87caa40c71942ae51996d12498b4")
def check_crc(data):
 assert data[:8]==bytes.fromhex("89504e470d0a1a0a")
 pos=8
 while pos<len(data):
  n=int.from_bytes(data[pos:pos+4],"big")
  typ=data[pos+4:pos+8];payload=data[pos+8:pos+8+n]
  assert zlib.crc32(typ+payload)==int.from_bytes(data[pos+8+n:pos+12+n],"big")
  pos+=12+n
 assert pos==len(data)
lum={}
for identifier,sha in zip(IDS,SHA):
 data=(ROOT/(identifier+".png")).read_bytes()
 assert hashlib.sha256(data).hexdigest()==sha
 check_crc(data)
 rgb=np.asarray(Image.open(BytesIO(data)).convert("RGB"),dtype=np.float64)
 assert rgb.shape==(16,16,3)
 lum[identifier]=rgb @ np.array([.2126,.7152,.0722])
def category(a,b):
 dyed=set(IDS[1:6])
 if a in dyed and b in dyed:return "ordinary_dyed_5"
 if a=="terracotta" and b in dyed:return "ordinary_uncolored_vs_dyed"
 if "glazed" in a and "glazed" in b:return "glazed_pair"
 return "ordinary_vs_glazed"
header=["texture_a","texture_b","category","aligned_pearson_r","aligned_r_squared",
        "best_r_over_1024","best_rotate_CCW_deg","best_cyclic_dx","best_cyclic_dy","runner_up_r","identity_best"]
rows=[];counts={}
for a,b in combinations(IDS,2):
 x=lum[a];y=lum[b]
 x=(x-x.mean())/x.std();y=(y-y.mean())/y.std()
 r0=float(np.mean(x*y))
 trials=[]
 for rot in range(4):
  yr=np.rot90(y,k=rot)
  for dy in range(16):
   for dx in range(16):
    trials.append((float(np.mean(x*np.roll(yr,(dy,dx),axis=(0,1)))),rot*90,dx,dy))
 trials.sort(reverse=True)
 best,runner=trials[:2]
 cl=category(a,b);counts[cl]=counts.get(cl,0)+1
 rows.append([a,b,cl,f"{r0:.6f}",f"{r0*r0:.6f}",f"{best[0]:.6f}",
              best[1],best[2],best[3],f"{runner[0]:.6f}",str(best[1:]==(0,0,0)).lower()])
assert len(rows)==28 and counts=={"ordinary_uncolored_vs_dyed":5,"ordinary_vs_glazed":12,"ordinary_dyed_5":10,"glazed_pair":1}
assert sum(row[-1]=="true" for row in rows)==15
with open("R007_PAIRWISE_LUMA_28.csv","w",newline="",encoding="utf-8") as f:
 writer=csv.writer(f);writer.writerow(header);writer.writerows(rows)
print("8 verified source PNGs; 28 pairs; 28672 transforms; 15 zero-transform maxima")
