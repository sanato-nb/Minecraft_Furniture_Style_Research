#!/usr/bin/env python3
"""TEX06-R006 reproducible side-world UV/RGB hypotheses. Not in-game certification.
Run from repository root; requires Pillow; writes R006_*.csv in current directory."""
from pathlib import Path
from PIL import Image
from io import BytesIO
import hashlib, itertools, json, zlib, csv
ROOT=Path("1.21.11/assets/minecraft")
TEX=("black_glazed_terracotta","white_glazed_terracotta")
SHA={"black_glazed_terracotta":"214ce8ca46c60a42b8863655b3895aca839c7ef7cfa511a192dc1974a0ca2758","white_glazed_terracotta":"cb1ebf9f3f3e93009ff4cab1b2b2b70d41fd87caa40c71942ae51996d12498b4"}
SIDES=("north","east","south","west");STATES=("south","west","north","east")
N={"north":(0,0,-1),"east":(1,0,0),"south":(0,0,1),"west":(-1,0,0)}
U={"north":(1,0,0),"east":(0,0,1),"south":(-1,0,0),"west":(0,0,-1)}
def rot(v,d):
 x,y,z=v
 return {0:(x,y,z),90:(z,y,-x),180:(-x,y,-z),270:(-z,y,x)}[d]
def inv(x,y,d):return {0:(x,y),90:(y,15-x),180:(15-x,15-y),270:(15-y,x)}[d]
def chk(data):
 assert data[:8]==bytes.fromhex("89504e470d0a1a0a")
 pos=8
 while pos<len(data):
  n=int.from_bytes(data[pos:pos+4],"big");kind=data[pos+4:pos+8];payload=data[pos+8:pos+8+n]
  assert zlib.crc32(kind+payload)==int.from_bytes(data[pos+8+n:pos+12+n],"big");pos+=12+n
 assert pos==len(data)
template=json.loads((ROOT/"models/block/template_glazed_terracotta.json").read_text())
assert template["elements"][0]["from"]==[0,0,0] and template["elements"][0]["to"]==[16,16,16]
faces=template["elements"][0]["faces"]
ims={};M={}
for tex in TEX:
 data=(ROOT/"textures/block"/(tex+".png")).read_bytes()
 assert hashlib.sha256(data).hexdigest()==SHA[tex];chk(data)
 ims[tex]=Image.open(BytesIO(data)).convert("RGBA")
 assert ims[tex].size==(16,16)
 leaf=json.loads((ROOT/"models/block"/(tex+".json")).read_text())
 assert leaf["parent"]=="minecraft:block/template_glazed_terracotta" and leaf["textures"]["pattern"]=="minecraft:block/"+tex
 variants=json.loads((ROOT/"blockstates"/(tex+".json")).read_text())["variants"]
 for w in SIDES:
  for state in STATES:
   y=variants["facing="+state].get("y",0)
   src=next(f for f in SIDES if rot(N[f],y)==N[w])
   assert rot(U[src],y)==U[w] and faces[src]["uv"]==[0,0,16,16]
   M[tex,w,state]=(src,y,faces[src].get("rotation",0))
def pixel(t,w,f,sign,x,y):
 src,model_y,uv=M[t,w,f];sx,sy=inv(x,y,(sign*uv)%360)
 return ims[t].getpixel((sx,sy)),sx,sy
def edge(t,w,sgn,axis,a,b):
 total=eq=0
 for j in range(16):
  x1,y1,x2,y2=(15,j,0,j) if axis=="horizontal" else (j,15,j,0)
  p,_,_=pixel(t,w,a,sgn,x1,y1);q,_,_=pixel(t,w,b,sgn,x2,y2)
  d=sum(abs(p[k]-q[k]) for k in range(3));total+=d;eq+=int(d==0)
 return total,eq
maps=[];pairs=[];panels=[]
for t in TEX:
 for w in SIDES:
  for sign in (1,-1):
   D={}
   for f in STATES:
    src,y,uv=M[t,w,f];p,x,yx=pixel(t,w,f,sign,0,0)
    maps.append([t,w,f,y,src,uv,sign,x,yx,"|".join(map(str,p)),False])
   for axis in ("horizontal","vertical"):
    for a,b in itertools.product(STATES,repeat=2):
     l1,eq=edge(t,w,sign,axis,a,b);D[axis,a,b]=(l1,eq)
     pairs.append([t,w,sign,axis,a,b,l1,f"{l1/48:.6f}",eq,16])
   best=None;ties=0
   for a,b,c,d in itertools.product(STATES,repeat=4):
    cuts=(D["horizontal",a,b],D["horizontal",c,d],D["vertical",a,c],D["vertical",b,d])
    l1=sum(x[0] for x in cuts);eq=sum(x[1] for x in cuts)
    if best is None or l1<best[0]:best=(l1,eq,a,b,c,d);ties=1
    elif l1==best[0]:ties+=1
   l1,eq,a,b,c,d=best
   assert (l1,eq)==((916,28) if t.startswith("black") else (412,44)) and ties==1
   panels.append([t,w,sign,a,b,c,d,l1,f"{l1/192:.6f}",eq,64,ties,False])
def write(name,h,rows):
 with open(name,"w",encoding="utf-8",newline="") as f:
  writer=csv.writer(f);writer.writerow(h);writer.writerows(rows)
write("R006_SIDE_FACE_SOURCE_MAP.csv",["texture_id","world_face","placed_facing","model_y_deg","source_local_face","declared_UV_rotation_deg","assumed_UV_CW_sign","screen_NW_source_x","screen_NW_source_y","source_RGBA_R005_inherited","ingame_verified"],maps)
write("R006_SIDE_EDGE_PAIRWISE.csv",["texture_id","world_face","assumed_UV_CW_sign","seam_axis","first_facing","second_facing","RGB_L1_sum_48_channels","RGB_MAE","exact_pairs","pairs_per_edge"],pairs)
write("R006_SIDE_PANEL_OPTIMA.csv",["texture_id","world_face","assumed_UV_CW_sign","TL_facing","TR_facing","BL_facing","BR_facing","RGB_L1","RGB_MAE","exact_pairs","pairs","number_of_minima","ingame_verified"],panels)
assert len(maps)==64 and len(pairs)==512 and len(panels)==16
print("R006:",len(maps),"map rows,",len(pairs),"pair rows,",len(panels),"optimal rows; 4096 tested layouts")
