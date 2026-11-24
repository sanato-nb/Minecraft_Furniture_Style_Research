"""H20: execute the unmodified official BedRenderer layer factories and bakeRoot.

Derive numeric mesh metadata from actual JVM model objects, with official pinned
libraries. This is an isolated model bake, not a live F2 render call.
"""
import argparse
import concurrent.futures
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import tempfile
from zipfile import ZipFile

from . import int4_h18_v11_bed_renderer_bytecode as h18

OWNER={
"BedRenderer":"net.minecraft.client.renderer.blockentity.BedRenderer",
"LayerDefinition":"net.minecraft.client.model.geom.builders.LayerDefinition",
"ModelPart":"net.minecraft.client.model.geom.ModelPart",
"Cube":"net.minecraft.client.model.geom.ModelPart$Cube",
"Polygon":"net.minecraft.client.model.geom.ModelPart$Polygon",
"Vertex":"net.minecraft.client.model.geom.ModelPart$Vertex",
}
FIELDS={
"ModelPart":"x y z xRot yRot zRot xScale yScale zScale cubes children".split(),
"Cube":"minX minY minZ maxX maxY maxZ polygons".split(),
"Polygon":["vertices"],"Vertex":["u","v"],
}
METHODS={"BedRenderer":["createHeadLayer","createFootLayer"],"LayerDefinition":["bakeRoot"]}
I=Path("project/integration")
H19=I/"INT4_H19_V11_BED_TYPE_RENDERER_REGISTRATION_RESULT_V1.json"
BASE=I/"INT4_F70_MODELING_CONTRACT_SUMMARY_V1.json"

def need(ok,msg):
    if not ok:raise ValueError("H20 "+msg)

def member_names(raw):
    cls=h18.parse_class_mappings(raw)
    data={}
    for short,full in OWNER.items():
        obf=cls[full]
        data[short]=obf
        section=raw.split(full+" -> "+obf+":",1)[1].splitlines()[1:]
        members=[]
        for line in section:
            if line and not line.startswith((" ","#")):break
            if line.startswith("    "):members.append(line.strip())
        for name in FIELDS.get(short,[])+METHODS.get(short,[]):
            pat=r"(?:^|\s)"+re.escape(name)+(r"\(\)" if name in METHODS.get(short,[]) else "")+r"\s+->\s+(\w+)$"
            hits=[m.group(1) for line in members if (m:=re.search(pat,line))]
            need(len(hits)==1,"member mapping not unique "+short+"."+name+" "+str(hits))
            data[short+"."+name]=hits[0]
        if short=="Vertex":
            for name in ("x","y","z"):
                hits=[m.group(1) for line in members if (m:=re.search(r"(?:^|\s)"+name+r"\s+->\s+(\w+)$",line))]
                if len(hits)==1:data[short+"."+name]=hits[0]
            print("H20_VERTEX_MAPPED_MEMBER_TYPES",members,flush=True)
    return data

def download_libraries(meta,root):
    artifacts={}
    for lib in meta["libraries"]:
        d=lib.get("downloads",{}).get("artifact")
        if not d or "natives-" in d["path"]:continue
        if d["path"] in artifacts:need(artifacts[d["path"]]==d,"conflicting library")
        artifacts[d["path"]]=d
    def one(d):
        p=root/d["path"]
        p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists():
            subprocess.run(["curl","-fLsS","--retry","2","--max-time","90",d["url"],"-o",str(p)],check=True)
        need(hashlib.sha1(p.read_bytes()).hexdigest()==d["sha1"],"library hash "+d["path"])
        return str(p)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        paths=list(pool.map(one,[artifacts[k] for k in sorted(artifacts)]))
    return paths,{k:v["sha1"] for k,v in sorted(artifacts.items())}

def parse_mesh(text):
    parts={}; cubes={}; faces={}; vertices={}
    for row in text.splitlines():
        s=row.split("\t")
        if s[0]=="PART":
            k=tuple(s[1:3]);need(k not in parts,"duplicate part")
            parts[k]={"translation":list(map(float,s[3:6])),"rotation_rad":list(map(float,s[6:9])),"scale":list(map(float,s[9:12])),"cube_count":int(s[12]),"child_count":int(s[13])}
        elif s[0]=="CUBE":
            k=tuple(s[1:4]);need(k not in cubes,"duplicate cube")
            cubes[k]={"bounds":list(map(float,s[4:10])),"polygon_count":int(s[10])}
        elif s[0]=="FACE":
            k=tuple(s[1:5]);need(k not in faces,"duplicate polygon")
            faces[k]={"normal":list(map(float,s[5:8]))}
        elif s[0]=="VERTEX":
            k=tuple(s[1:6]);need(k not in vertices,"duplicate vertex")
            vertices[k]={"xyz":list(map(float,s[6:9])),"uv_normalized":list(map(float,s[9:11]))}
    need("H20_BAKED_MODEL_FACTORIES_COMPLETE" in text,"isolated factory execution incomplete")
    expected={(h,p) for h in ("head","foot") for p in ("root","root/main","root/left_leg","root/right_leg")}
    need(set(parts)==expected and len(cubes)==6 and len(faces)==36 and len(vertices)==144,"mesh population not complete")
    result={}
    for half in ("head","foot"):
        entries=[]
        for key in sorted(k for k in parts if k[0]==half):
            part=parts[key]
            cc=[k for k in cubes if k[:2]==key]
            need(len(cc)==part["cube_count"] and part["child_count"]==(3 if key[1]=="root" else 0),"part hierarchy mismatch")
            part["path"]=key[1];part["cubes"]=[]
            for k in sorted(cc):
                cube=cubes[k]
                dims=[cube["bounds"][i+3]-cube["bounds"][i] for i in range(3)]
                need(dims==([16.,16.,6.] if key[1]=="root/main" else [3.,3.,3.]),"unexpected cuboid dimensions")
                cube["dimensions"]=dims;cube["faces"]=[]
                ff=[x for x in faces if x[:3]==k]
                need(len(ff)==cube["polygon_count"]==6,"missing cube polygons")
                normal_set=set()
                for fk in sorted(ff):
                    face=faces[fk]
                    vs=[vertices[fk+(str(i),)] for i in range(4)]
                    normal_set.add(tuple(face["normal"]))
                    for v in vs:
                        need(all(math.isfinite(n) for n in v["xyz"]+v["uv_normalized"]),"nonfinite vertex")
                        uv=[round(n*64,6) for n in v["uv_normalized"]]
                        need(all(0<=n<=64 and abs(n-round(n))<1e-5 for n in uv),"nonpixel or out-of-range UV")
                        v["uv_texel_edge"]=uv
                    uv=[v["uv_texel_edge"] for v in vs]
                    face["uv_rect_texels"]=[min(u[0] for u in uv),min(u[1] for u in uv),max(u[0] for u in uv),max(u[1] for u in uv)]
                    face["vertices"]=vs
                    cube["faces"].append(face)
                need(normal_set=={(1.,0.,0.),(-1.,0.,0.),(0.,1.,0.),(0.,-1.,0.),(0.,0.,1.),(0.,0.,-1.)},"normal directions not complete")
                part["cubes"].append(cube)
            entries.append(part)
        result[half]=entries
    return result

def audit(args):
    version=Path(args.version_json).read_bytes()
    client=Path(args.official_client).resolve()
    mappings=Path(args.client_mappings).read_bytes()
    pins=h18.version_preflight(version,client.read_bytes(),mappings)
    prior=json.loads(Path(h18.ORIGINAL_V11).read_text())
    h18.prior_v11_check(prior,client)
    old=json.loads(H19.read_text())
    base=json.loads(BASE.read_text())
    need(old["registration"]["bootstrap_constructor_method_handle_verified"] and old["source_pins"]==pins and not old["exact_model_geometry_and_per_face_UV_extracted"],"H19 boundary changed")
    need(base["historical_modeling"]["remaining_ids"].count("V11")==1 and base["combined_review_scope_only"]["closed_units"]==40,"base review changed")
    names=member_names(mappings.decode())
    # Factory execution uses only original Minecraft libraries and original class
    # files, never a reimplementation of the cuboid UV algorithm.
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        libs,libsha=download_libraries(json.loads(version),td/"libs")
        props=td/"mapped.properties"
        props.write_text("\n".join(k+"="+v for k,v in sorted(names.items()))+"\n")
        cp=":".join([str(client)]+libs)
        subprocess.run(["javac","-cp",cp,"-d",str(td),"tools/research/H20BedMeshProbe.java"],check=True)
        p=subprocess.run(["java","-cp",str(td)+":"+cp,"mcfrprobe.H20BedMeshProbe",str(props)],capture_output=True,text=True,timeout=120)
        need(p.returncode==0,"original JVM factory failed "+p.stderr[-4000:]+" "+p.stdout[-1000:])
        mesh=parse_mesh(p.stdout)
    with ZipFile(client) as z:
        white="assets/minecraft/textures/entity/bed/white.png"
        need(white in z.namelist(),"white bed texture missing")
        png=z.read(white)
        need(png[:8]==b"\x89PNG\r\n\x1a\n","PNG signature")
        size=list(struct.unpack(">II",png[16:24]))
        need(size==[64,64],"texture dimensions "+str(size))
        classes={k:hashlib.sha256(z.read(names[k].replace(".","/")+".class")).hexdigest() for k in OWNER}
    # Source texture lookup linkage via official submit/SHEETS call.
    raw=mappings.decode()
    cmap=h18.parse_class_mappings(raw)
    sheets=cmap["net.minecraft.client.renderer.Sheets"]
    dump=h18.javap_output(client,names["BedRenderer"])
    sheet_dump=h18.javap_output(client,sheets)
    need(re.search(r"Method "+re.escape(sheets)+r"\.\w+:\(L"+re.escape(cmap["net.minecraft.world.item.DyeColor"])+r";\)L",dump),"bed renderer material lookup not found")
    # Record asset presence and material lookup separately; do not assert
    # resolved white sprite identity unless actually checked below.
    out={
      "schema":"MCFR_INT4_H20_V11_ORIGINAL_JVM_BAKED_BED_MESH_UV_V1",
      "status":"PASS_OFFICIAL_ISOLATED_BED_LAYER_FACTORY_BAKE_GEOMETRY_AND_FACE_UV",
      "source_pins":pins,"mapped_class_and_member_names":names,"source_class_sha256":classes,
      "official_library_sha1":libsha,"official_library_count":len(libsha),
      "geometry":mesh,"counts":{"root_parts":2,"child_parts":6,"cubes":6,"polygons":36,"vertices":144},
      "texture":{"candidate_official_white_png_path":white,"sha256":hashlib.sha256(png).hexdigest(),"dimensions":size,"renderer_dye_material_lookup_verified":True,"material_path_resolution_verified":False},
      "source_f2":{"run":45103243455,"native_png_count":4,"bed_vs_air_pixels":6446,"air_control_pixels":0},
      "isolated_original_JVM_model_bake":True,"new_game_runs":0,"new_F2":0,
      "actual_scene_renderer_invocation_verified":False,"GPU_sample_to_screen_causality_verified":False,
      "legacy_F70_unconditional":0,"INT5":0,"INT6":0,
      "modeling_v11_disposition":"CONDITIONAL_PENDING_WHITE_TEXTURE_MATERIAL_PATH_AND_WORLD_POSE",
      "limits":["Model factory and bakeRoot executed in isolation, not a live renderer or game.","Vertex position and UV data are local baked mesh metadata; block orientation/world transforms are not yet extracted.","White PNG identity/dimensions verified; exact runtime atlas sprite resolution remains unproven.","No original assets redistributed."]
    }
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    Path(args.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("H20_GEOMETRY_PASS",json.dumps({"counts":out["counts"],"texture":out["texture"],"modeling_v11_disposition":out["modeling_v11_disposition"],"parts":{h:[{"path":p["path"],"rotation":p["rotation_rad"],"bounds":[c["bounds"] for c in p["cubes"]]} for p in ps] for h,ps in mesh.items()}},sort_keys=True))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for arg in ("version-json","official-client","client-mappings","output"):p.add_argument("--"+arg,required=True)
    audit(p.parse_args())
