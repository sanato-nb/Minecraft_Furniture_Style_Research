"""INT-3: source-pinned chair geometry contact sheets for genuine visual review.

Renders four historical chair *providers* (45 component-role candidates)
from the ORIGINAL pinned model JSON, not from heuristic meshes. Cross-check
the raw element coordinates, rotations and faces against 1-3-F, and attach
the original model Git blob / JAR entry SHA. Render colors represent the
historical *candidate function*, NOT actual PNG pixels, materials, or
Minecraft baked / game appearance. This tool does not approve any role.

Images are geometry diagrams, not reproductions of upstream art textures.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter,defaultdict
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import sqlite3
import zipfile
import lzma

from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
F_DB=ROOT/"research/furniture_mods/phase_1-3/F/furniture_research.sqlite.xz"
ROLE_ORDER=("LEG_OR_LOWER_POST","SEAT_LAYER","BACKREST_ASSEMBLY","LOWER_FRAME")
PALETTE={
 "LEG_OR_LOWER_POST":(36,131,179),
 "SEAT_LAYER":(232,153,55),
 "BACKREST_ASSEMBLY":(106,166,88),
 "LOWER_FRAME":(164,114,176),
 "UNDETERMINED":(170,172,180),
}
PIN={"MACAW":"e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"}
FACE_CORNERS={
 "up":(3,2,6,7),"down":(0,4,5,1),
 "north":(0,1,2,3),"south":(4,7,6,5),
 "west":(0,3,7,4),"east":(1,5,6,2),
}
# 0=(x0,y0,z0), 1=(x1,y0,z0), 2=(x1,y1,z0), 3=(x0,y1,z0)
# 4=(x0,y0,z1), 5=(x1,y0,z1), 6=(x1,y1,z1), 7=(x0,y1,z1)


def load_db(root):
    conn=sqlite3.connect(":memory:")
    conn.deserialize(lzma.decompress((root/"research/furniture_mods/phase_1-3/F/furniture_research.sqlite.xz").read_bytes()))
    if conn.execute("PRAGMA integrity_check").fetchone()[0]!="ok":
        raise ValueError("F source DB corrupt")
    if conn.execute("PRAGMA foreign_key_check").fetchall():
        raise ValueError("F source DB foreign key failed")
    conn.row_factory=sqlite3.Row
    return conn

class Original:
    def __init__(self,af,hc,macaw):
        self.zips={}
        self.idx={}
        for name,path in (("AF",af),("HC",hc),("MACAW",macaw)):
            if name=="MACAW" and hashlib.sha256(path.read_bytes()).hexdigest()!=PIN["MACAW"]:
                raise ValueError("Macaw official JAR SHA not pinned")
            z=zipfile.ZipFile(path)
            if z.testzip() is not None:raise ValueError("Upstream ZIP CRC invalid "+name)
            self.zips[name]=z
            if name=="MACAW":
                self.idx[name]={x:x for x in z.namelist()}
            else:
                self.idx[name]={x.partition("/")[2]:x for x in z.namelist() if not x.endswith("/")}
    def fetch(self,mod,path):
        return self.zips[mod].read(self.idx[mod][path])
    def close(self):
        for z in self.zips.values():z.close()

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

def read_providers(db,source):
    providers=list(db.execute("""
     SELECT DISTINCT e.provider_key,m.source_id,m.resource_id,m.path,m.sha
     FROM element e JOIN model m ON m.model_key=e.provider_key
     WHERE e.part_candidate!='UNDETERMINED'
     ORDER BY m.source_id,m.resource_id
    """))
    if len(providers)!=4:raise ValueError("Expected exactly four historical chair providers")
    all_shapes=[]
    report=[]
    counted=Counter()
    for model in providers:
        mod=model["source_id"]
        if mod not in ("AF","HC","MACAW"):raise ValueError("Unexpected source provider")
        raw=source.fetch(mod,model["path"])
        actual_sha=git_blob(raw) if mod in ("AF","HC") else hashlib.sha256(raw).hexdigest()
        if actual_sha!=model["sha"]:
            raise ValueError("Original model SHA mismatch: "+model["path"])
        obj=json.loads(raw.decode("utf-8-sig"))
        elem=obj.get("elements",[])
        rows=list(db.execute("""SELECT element_index,source_from,source_to,pivot,axis,
                angle,rescale,part_candidate,part_evidence
              FROM element WHERE provider_key=? ORDER BY element_index""",(model["provider_key"],)))
        if len(rows)!=len(elem):raise ValueError("Historical element count differs from original JSON")
        shapes=[]
        for row,e in zip(rows,elem):
            i=int(row["element_index"])
            if i!=len(shapes):raise ValueError("Historical element order differs")
            vals="|".join(str(v) for v in e["from"])
            target="|".join(str(v) for v in e["to"])
            if [float(x) for x in row["source_from"].split("|")]!=[float(x) for x in vals.split("|")]:
                raise ValueError("Original model element from coordinate mismatch")
            if [float(x) for x in row["source_to"].split("|")]!=[float(x) for x in target.split("|")]:
                raise ValueError("Original model element to coordinate mismatch")
            rot=e.get("rotation",{})
            if round(float(rot.get("angle",0)),8)!=round(float(row["angle"]),8):
                raise ValueError("Original rotation declaration differs")
            if (rot.get("axis","") or "")!=row["axis"]:
                raise ValueError("Original rotation axis differs")
            if int(bool(rot.get("rescale",False)))!=row["rescale"]:
                raise ValueError("Original rotation rescale differs")
            if [float(x) for x in rot.get("origin",[])]!=[float(x) for x in row["pivot"].split("|") if x]:
                raise ValueError("Original pivot differs")
            if row["part_evidence"]!="GEOMETRY_AND_FACE_SLOTS" or row["part_candidate"] not in ROLE_ORDER:
                raise ValueError("Historical part claim isn't an evidenced chair candidate")
            if len(e.get("faces",{})) != db.execute(
                "SELECT COUNT(*) FROM face WHERE provider_key=? AND element_index=?",
                (model["provider_key"],i)).fetchone()[0]:
                raise ValueError("Raw model and F face direction count differ")
            counted[row["part_candidate"]]+=1
            shapes.append({
                "index":i,"a":e["from"],"b":e["to"],"role":row["part_candidate"],
                "axis":rot.get("axis",""),"angle":float(rot.get("angle",0)),
                "pivot":rot.get("origin",[8,8,8]),"rescale":bool(rot.get("rescale",False)),
                "faces":tuple(e.get("faces",{}))
            })
        all_shapes.append({"mod":mod,"resource":model["resource_id"],"sha":actual_sha,
                           "provider_key":model["provider_key"],"shapes":shapes})
        report.append({"mod":mod,"resource":model["resource_id"],"source_path":model["path"],
                       "sha":actual_sha,"element_count":len(shapes),
                       "role_counts":dict(Counter(s["role"] for s in shapes))})
    if dict(counted)!={"BACKREST_ASSEMBLY":16,"LEG_OR_LOWER_POST":16,"LOWER_FRAME":7,"SEAT_LAYER":6}:
        raise ValueError("Not the 45 originally studied elements")
    return all_shapes,report,dict(counted)

def transform(p,shape):
    axis=shape["axis"];a=math.radians(shape["angle"])
    if not axis or not a:return p
    ox,oy,oz=shape["pivot"]
    x,y,z=[value-origin for value,origin in zip(p,(ox,oy,oz))]
    c,s=math.cos(a),math.sin(a)
    f=1/c if shape["rescale"] and abs(c)>1e-5 else 1
    if axis=="x":y,z=f*(y*c-z*s),f*(y*s+z*c)
    elif axis=="y":x,z=f*(x*c+z*s),f*(-x*s+z*c)
    elif axis=="z":x,y=f*(x*c-y*s),f*(x*s+y*c)
    else:raise ValueError("Unrecognized original angle axis")
    return (x+ox,y+oy,z+oz)

def cube_points(shape):
    x0,y0,z0=shape["a"];x1,y1,z1=shape["b"]
    cube=[
        (x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
        (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    return [transform(p,shape) for p in cube]

def camera(point,yaw,pitch=30):
    rad=math.radians(yaw);e=math.radians(pitch)
    x,y,z=point
    u=x*math.cos(rad)-z*math.sin(rad)
    depth=x*math.sin(rad)+z*math.cos(rad)
    v=y*math.cos(e)-depth*math.sin(e)
    d=depth*math.cos(e)+y*math.sin(e)
    return (u,v,d)

def mix_rgb(c,factor):
    return tuple(max(0,min(255,int(value*factor))) for value in c)

def render_one(draw,rect,entry,yaw):
    x0,y0,x1,y1=rect
    all_cubes=[cube_points(s) for s in entry["shapes"]]
    trans=[[camera(p,yaw) for p in cube] for cube in all_cubes]
    ux=[p[0] for verts in trans for p in verts]
    vy=[p[1] for verts in trans for p in verts]
    # tight fitting with uniform scale, leaves room for text & legend
    usable=(x1-x0-45,y1-y0-110)
    w=max(1,max(ux)-min(ux));h=max(1,max(vy)-min(vy))
    scale=min(usable[0]/w,usable[1]/h,19)
    cx=(min(ux)+max(ux))/2;cy=(min(vy)+max(vy))/2
    midx=(x0+x1)/2;midy=(y0+y1)/2+25
    def pixel(v):return (midx+(v[0]-cx)*scale,midy-(v[1]-cy)*scale)
    polygons=[]
    for s,pts in zip(entry["shapes"],trans):
        for name,ids in FACE_CORNERS.items():
            if name not in s["faces"]:continue
            surface=[pts[i] for i in ids]
            depth=sum(p[2] for p in surface)/len(surface)
            center=(sum(p[0] for p in surface)/4,sum(p[1] for p in surface)/4)
            polygons.append((depth,s["index"],name,[pixel(p) for p in surface],s["role"]))
    for depth,index,name,poly,role in sorted(polygons):
        rolecolor=PALETTE[role]
        factor={"up":1.14,"down":0.60,"north":0.84,"south":0.94,"west":0.74,"east":1.0}[name]
        color=mix_rgb(rolecolor,factor)
        draw.polygon(poly,fill=color)
        draw.line(poly+[poly[0]],fill=(45,45,51),width=1)
    title=entry["mod"]+"  "+entry["resource"].split(":")[-1]
    draw.text((x0+14,y0+14),title,fill=(40,40,45))
    draw.text((x0+14,y0+38),f"{len(entry['shapes'])} raw elements / yaw {yaw} deg",fill=(85,85,90))
    # Each label points to its element's center in model-space, not rendered face.
    labels=[]
    for s,verts in zip(entry["shapes"],trans):
        centroid=tuple(sum(p[j] for p in verts)/len(verts) for j in range(3))
        pt=pixel(centroid)
        labels.append((pt,str(s["index"])))
    for pt,number in labels:
        xx,yy=pt
        draw.ellipse((xx-8,yy-8,xx+8,yy+8),fill=(245,245,242),outline=(20,20,25),width=1)
        draw.text((xx-4 if len(number)==1 else xx-6,yy-6),number,fill=(5,5,5))
    draw.rectangle((x0+5,y0+5,x1-5,y1-5),outline=(215,215,220),width=1)

def make_sheet(entries,out):
    width,height=1360,1960
    im=Image.new("RGB",(width,height),(250,251,253))
    d=ImageDraw.Draw(im)
    d.text((24,14),"Minecraft Furniture Style Research  |  geometry-only candidate role review",fill=(20,20,24))
    d.text((24,39),"Raw pinned source elements / no game textures, lighting, or collision baked; role labels are hypotheses.",fill=(68,68,74))
    for i,entry in enumerate(entries):
        y0=72+i*449
        render_one(d,(12,y0,678,y0+439),entry,45)
        render_one(d,(682,y0,1348,y0+439),entry,-135)
    y=1877
    x=18
    for role in ROLE_ORDER:
        d.rectangle((x,y,x+15,y+15),fill=PALETTE[role])
        d.text((x+21,y-1),role,fill=(30,30,36))
        x+=325 if role!="BACKREST_ASSEMBLY" else 340
    d.text((18,1907),"NOTE: geometry correspondence review only; not final in-game or texture-based validation.",fill=(80,80,90))
    out.parent.mkdir(parents=True,exist_ok=True)
    im.save(out,optimize=True)
    return im

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ("af","hc","macaw","out"):p.add_argument("--"+k,required=True,type=Path)
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--log-preview-base64",action="store_true")
    a=p.parse_args()
    original=Original(a.af,a.hc,a.macaw)
    try:
        with load_db(a.root) as db:
            entries,rows,counts=read_providers(db,original)
    finally:
        original.close()
    out=a.out;a.out.mkdir(parents=True,exist_ok=True)
    png=out/"INT3_45_CHAIR_GEOMETRY_CONTACT_SHEET.png"
    image=make_sheet(entries,png)
    report={
       "schema":"MCFR_INT3_45_CHAIR_GEOMETRY_CONTACT_SHEET/v1",
       "status":"PASS_RAW_SOURCE_FOUR_PROVIDER_GEOMETRY_RECONSTRUCTED",
       "four_provider_sha_verified":True,
       "providers":rows,
       "total_original_elements":sum(len(x["shapes"]) for x in entries),
       "original_role_candidates":counts,
       "original_pinned_model_sha_included":True,
       "sheet_sha256":hashlib.sha256(png.read_bytes()).hexdigest(),
       "sheet_image_size":list(image.size),
       "role_candidate_visual_approval":0,
       "runtime_recheck":False,
       "render_scope":"RAW_MODEL_GEOMETRY_COLOR_BY_HISTORIC_ROLE_ONLY",
       "limits":["No source textures displayed","No Minecraft engine bake/uvlock","No collision or custom renderer","No original screenshots"],
    }
    (out/"INT3_45_GEOMETRY_RENDER_SUMMARY.json").write_text(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    # Preview is a smaller JPEG for one-time independent human inspection in a
    # GitHub Actions log. It consists only of geometry polygons and role colors.
    if a.log_preview_base64:
        preview=image.copy()
        preview.thumbnail((840,1250))
        buf=io.BytesIO()
        preview.save(buf,"JPEG",quality=78,optimize=True)
        print("INT3_PREVIEW_JPEG_BEGIN")
        print(base64.b64encode(buf.getvalue()).decode("ascii"))
        print("INT3_PREVIEW_JPEG_END")
    print("INT3_GEOMETRY_RENDER_RESULT:"+json.dumps(report,sort_keys=True,ensure_ascii=False))

if __name__=="__main__":
    main()
