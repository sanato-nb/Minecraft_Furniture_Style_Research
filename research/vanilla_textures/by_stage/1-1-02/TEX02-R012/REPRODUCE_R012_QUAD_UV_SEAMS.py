#!/usr/bin/env python3
"""R012 fixed-cube UV / north-face PNG seam reprojection (NOT an in-game render).
Requires Python >=3.9 and Pillow. Run on the same user-extracted 1.21.11 tree
and frozen R007/R010/R011 CSV inputs, not on unknown game-version assets.
--pixels-only permits an isolated two-PNG sample check.
"""
import argparse,csv,hashlib,json
from pathlib import Path
from PIL import Image

CLASS_SHA={
 "f.class":"f2723f067abf293075e66021711ce37387c92def",
 "h.class":"c4594ee6c1938cf051fcb5968a3c108788ffe1ac",
 "g.class":"f4883aaac8f997dceb60b8f5e9a076e7a16c6fef",
 "inm.class":"672b186c8a8457082fec756114b443a48dc151d1",
 "hoa.class":"6841dfb26d63d166dac1d261c78805e00dfb2fc2",
 "hoa$a.class":"776c249d3ed2490e1968894a1ea5fd0a2c681a02",
 "hoa$b.class":"1eaad856846155a63bbd56c3ff895fc73150dde7",
 "hqc$b.class":"7cf58ffc0114cf9c90c275317697da0834e5d8a1",
 "hqi.class":"5b64584e8cc09a8db90f802e0021bc0533e81ab1",
 "ioc.class":"6063a49dabf4cda7816dc570babd1a1b2e57e6e0",
}
PNG_SHA={
 "deepslate.png":"bb7dc9ced1943d1dc86ab0cded598e8541fd280a",
 "deepslate_top.png":"a560ccfb90cae70a1df6d2fd89d0c6405c2c4347",
}
# Enumerations read from hoa.class <clinit>, hoa$a.class MIN_/MAX_XYZ:
HOA={
 "down": [(0,0,1),(0,0,0),(1,0,0),(1,0,1)],
 "up":   [(0,1,0),(0,1,1),(1,1,1),(1,1,0)],
 "north":[(1,1,0),(1,0,0),(0,0,0),(0,1,0)],
 "south":[(0,1,1),(0,0,1),(1,0,1),(1,1,1)],
 "west": [(0,1,0),(0,0,0),(0,0,1),(0,1,1)],
 "east": [(1,1,1),(1,0,1),(1,0,0),(1,1,0)]
}
NORMAL={
 "down": (0,-1,0),"up":(0,1,0),"north":(0,0,-1),
 "south":(0,0,1),"west":(-1,0,0),"east":(1,0,0)
}
MAT={
 (0,0,0):((1,0,0),(0,1,0),(0,0,1)),
 (0,180,0):((-1,0,0),(0,1,0),(0,0,-1)),
 (90,0,0):((1,0,0),(0,0,1),(0,-1,0)),
 (90,180,0):((-1,0,0),(0,0,1),(0,1,0)),
 (90,90,0):((0,1,0),(0,0,1),(1,0,0)),
}
def gitsha(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()
def readcsv(path):
 with path.open(encoding="utf8",newline="") as stream:
  return list(csv.DictReader(stream))
def writecsv(path,rows):
 assert rows
 with path.open(encoding="utf8",newline="",mode="w") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def matmulvec(M,v):
 return tuple(sum(a*b for a,b in zip(row,v)) for row in M)
def transform(M,pos):
 return tuple(round(z+.5) for z in matmulvec(M,tuple(x-.5 for x in pos)))
def worldface(M,face):
 vec=matmulvec(M,NORMAL[face])
 return next(k for k,v in NORMAL.items() if v==vec)
def recalcface(M,local,mirror):
 world=worldface(M,local)
 moved=[transform(M,p) for p in HOA[local]]
 dst=[moved.index(v) for v in HOA[world]]
 u1,u2=(16,0) if mirror else (0,16)
 srcuv=[(u1,0),(u1,16),(u2,16),(u2,0)]
 # FaceBakery's no-element-rotation sort swaps vertex AND packed UV
 return world,dst,[srcuv[dst[i]] for i in (0,3,2,1)]
def getpixels(root):
 images={}
 for name,sha in PNG_SHA.items():
  path=root/"assets/minecraft/textures/block"/name
  raw=path.read_bytes()
  assert gitsha(raw)==sha,(name,"source png SHA differs")
  im=Image.open(path).convert("RGB")
  assert im.size==(16,16)
  images[name]=im
 return images
def project(img,uv):
 tl,tr,br,bl=uv
 out=[]
 for y in range(16):
  row=[]
  v=(y+.5)/16
  for x in range(16):
   u=(x+.5)/16
   X=tl[0]*(1-u)*(1-v)+tr[0]*u*(1-v)+br[0]*u*v+bl[0]*(1-u)*v
   Y=tl[1]*(1-u)*(1-v)+tr[1]*u*(1-v)+br[1]*u*v+bl[1]*(1-u)*v
   X=int(round(X-.5));Y=int(round(Y-.5))
   assert 0<=X<16 and 0<=Y<16
   row.append(img.getpixel((X,Y)))
  out.append(row)
 return out
def pairmetric(left,right,mode):
 total=0;different=0
 for i in range(16):
  A=left[i][15] if mode=="east_to_west" else left[15][i]
  B=right[i][0] if mode=="east_to_west" else right[0][i]
  diff=tuple(abs(a-b) for a,b in zip(A,B))
  total+=sum(diff);different+=any(diff)
 return total,different
def north(source,axis,i):
 if axis=="axis=x":rot=(90,90,0);local="west";png="deepslate.png"
 elif axis=="axis=z":
  rot=(90,0,0) if i<2 else (90,180,0)
  local="up" if i<2 else "down";png="deepslate_top.png"
 else:raise ValueError(axis)
 world,idx,uv=recalcface(MAT[rot],local,i%2==1)
 assert world=="north"
 return dict(axis=axis,variant=i,local=local,png=png,uv=uv,
             perm=idx,image=project(source[png],uv))
def pixelcheck(source):
 allpairs=[]
 for axis in ("axis=x","axis=z"):
  variants=[north(source,axis,i) for i in range(4)]
  for L in range(4):
   for R in range(4):
    for direction in ("east_to_west","south_to_north"):
     total,different=pairmetric(variants[L]["image"],variants[R]["image"],direction)
     allpairs.append(dict(axis=axis,left=L,right=R,direction=direction,
                 rgb_diff_sum=total,mismatched_pixels=different))
 assert len(allpairs)==64
 lookup={(r["axis"],r["left"],r["right"],r["direction"]):r for r in allpairs}
 assert lookup["axis=x",0,0,"east_to_west"]["rgb_diff_sum"]==616
 assert lookup["axis=x",0,0,"south_to_north"]["rgb_diff_sum"]==745
 assert lookup["axis=x",0,1,"east_to_west"]["rgb_diff_sum"]==1078
 assert lookup["axis=x",0,1,"south_to_north"]["rgb_diff_sum"]==0
 assert lookup["axis=z",0,0,"east_to_west"]["rgb_diff_sum"]==646
 assert lookup["axis=z",0,0,"south_to_north"]["rgb_diff_sum"]==822
 return allpairs
def run(args):
 source=getpixels(args.root)
 pixel=pixelcheck(source)
 if args.pixels_only:
  print(json.dumps(dict(R012_isolated_PNG_sha_verified=2,
            corrected_north_seam_sample_pairs=64,ingame_verified=0,
            sample_0=pixel[0],sample_z=pixel[32]),indent=2));return
 for name,sha in CLASS_SHA.items():
  data=(args.root/name).read_bytes()
  assert gitsha(data)==sha,("classfile SHA mismatch",name)
 old=readcsv(args.r007_faces);states=readcsv(args.r010_states)
 matrices=readcsv(args.r011_matrices);seams=readcsv(args.r007_seams)
 assert len(old)==186 and len(states)==31 and len(matrices)==5 and len(seams)==134
 for m in matrices:
  key=tuple(map(int,(m["x"],m["y"],m["z"])))
  assert key in MAT
  got=tuple(tuple(int(x) for x in m[f"matrix_row{axis}"].split(":"))
            for axis in "XYZ")
  assert got==MAT[key]
 prior={(r["texture_id"],r["prop"],r["index"],r["local_face"]):r for r in old}
 full=[];errors=[]
 for s in states:
  rotation=MAT[int(s["x"]),int(s["y"]),int(s["z"])]
  for local in HOA:
   before=prior[s["block"],s["property"],s["variant_index"],local]
   world,perm,UV=recalcface(rotation,local,before["source_uv"]=="explicit_U_reverse")
   b=[(int(before[p+"_u"]),int(before[p+"_v"])) for p in
      ("top_left","top_right","bottom_right","bottom_left")]
   diff=UV!=b
   row=dict(block=s["block"],axis=s["property"],variant=s["variant_index"],
     local_face=local,previous_world=before["world_face_math"],
     corrected_world=world,world_diff=world!=before["world_face_math"],
     previous_uv=str(b),corrected_uv=str(UV),UV_diff=diff,
     vertex_permutation=str(perm),not_ingame=True)
   full.append(row)
   if diff:errors.append(row)
 assert len(full)==186 and len(errors)==40
 assert sum(x["world_diff"] for x in full)==32
 keyed={(r["property"],int(r["left_variant_index"]),int(r["right_variant_index"]),
         r["direction"]):r for r in seams if r["texture_group"]=="deepslate"}
 reread=[]
 for row in pixel:
  old=keyed[row["axis"],row["left"],row["right"],row["direction"]]
  reread.append(dict(**row,old_rgb_sum=int(old["rgb_diff_sum"]),
       old_different_pixels=int(old["edge_pixels_mismatched"]),
       aggregate_equal=row["rgb_diff_sum"]==int(old["rgb_diff_sum"])
        and row["mismatched_pixels"]==int(old["edge_pixels_mismatched"]),
       not_ingame=True))
 assert len(reread)==64 and all(x["aggregate_equal"] for x in reread)
 args.out.mkdir(parents=True,exist_ok=True)
 writecsv(args.out/"R012_REGENERATED_186_UV.csv",full)
 writecsv(args.out/"R012_REGENERATED_40_UV_DIFFERENCES.csv",errors)
 writecsv(args.out/"R012_REGENERATED_64_NORTH_SEAMS.csv",reread)
 print(json.dumps(dict(source_classfiles_SHA_verified=len(CLASS_SHA),
   source_png_sha_verified=len(PNG_SHA),total_faces=186,
   source_uv_differences=40,source_world_direction_differences=32,
   reprojected_seam_rows=64,aggregate_metrics_equal=64,
   ingame_verified=0),indent=2))
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--root",type=Path,required=True,help="User extracted 1.21.11 root")
 p.add_argument("--r007-faces",type=Path)
 p.add_argument("--r010-states",type=Path)
 p.add_argument("--r011-matrices",type=Path)
 p.add_argument("--r007-seams",type=Path)
 p.add_argument("--out",type=Path)
 p.add_argument("--pixels-only",action="store_true")
 a=p.parse_args()
 if not a.pixels_only and not all((a.r007_faces,a.r010_states,a.r011_matrices,a.r007_seams,a.out)):
  p.error("full mode requires --r007-faces --r010-states --r011-matrices --r007-seams --out")
 run(a)
