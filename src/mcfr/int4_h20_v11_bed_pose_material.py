"""H20 follow-up: original engine pose and white bed atlas lookup."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
from zipfile import ZipFile

from . import int4_h18_v11_bed_renderer_bytecode as h18
from . import int4_h20_v11_bed_mesh_uv as mesh

EXTRA={
"PoseStack":"com.mojang.blaze3d.vertex.PoseStack",
"Pose":"com.mojang.blaze3d.vertex.PoseStack$Pose",
"Direction":"net.minecraft.core.Direction",
"DyeColor":"net.minecraft.world.item.DyeColor",
"Sheets":"net.minecraft.client.renderer.Sheets",
"Material":"net.minecraft.client.resources.model.Material",
"SharedConstants":"net.minecraft.SharedConstants",
"Bootstrap":"net.minecraft.server.Bootstrap",
}
METHODS={
"PoseStack":{"pushPose":"","popPose":"","last":""},
"Pose":{"pose":""},
"ModelPart":{"translateAndRotate":EXTRA["PoseStack"]},
"Vertex":{"worldX":"","worldY":"","worldZ":""},
"BedRenderer":{"preparePose":EXTRA["PoseStack"]+",boolean,"+EXTRA["Direction"]},
"Sheets":{"getBedMaterial":EXTRA["DyeColor"]},
"Material":{"texture":"","atlasLocation":""},
"SharedConstants":{"tryDetectVersion":""},
"Bootstrap":{"bootStrap":""},
}
FIELDS={"Direction":["NORTH","EAST","SOUTH","WEST"],"DyeColor":["WHITE"]}

def check(ok,msg):mesh.need(ok,msg)
def mapped_names(raw):
    cls=h18.parse_class_mappings(raw)
    result=mesh.member_names(raw)
    owners=mesh.OWNER|EXTRA
    for short in set(METHODS)|set(FIELDS):
        full=owners[short]
        obf=cls[full]
        result[short]=obf
        section=raw.split(full+" -> "+obf+":",1)[1].splitlines()[1:]
        lines=[]
        for line in section:
            if line and not line.startswith((" ","#")):break
            if line.startswith("    "):lines.append(line.strip())
        for member in FIELDS.get(short,[]):
            pat=r"(?:^|\s)"+re.escape(member)+r"\s+->\s+(\w+)$"
            hits=[m.group(1) for line in lines if (m:=re.search(pat,line))]
            check(len(hits)==1,"field mapping "+short+"."+member+" "+str(hits))
            result[short+"."+member]=hits[0]
        for name,params in METHODS.get(short,{}).items():
            pat=r"(?:^|\s)"+re.escape(name)+r"\("+re.escape(params)+r"\)\s+->\s+(\w+)$"
            hits=[m.group(1) for line in lines if (m:=re.search(pat,line))]
            if len(hits)!=1:
                print("H20_EXTRA_MAPPING_DIAGNOSTIC",short,name,lines[:70],flush=True)
            check(len(hits)==1,"method mapping "+short+"."+name+" "+str(hits))
            result[short+"."+name]=hits[0]
    return result

def resource(value):
    if ":" in value:return value.split(":",1)
    return "minecraft",value

def atlas_resolves(z,atlas,sprite):
    ns,a=resource(atlas)
    check(a.startswith("textures/atlas/") and a.endswith(".png"),"unexpected atlas "+atlas)
    atlas_path="assets/"+ns+"/atlases/"+a.removeprefix("textures/atlas/").removesuffix(".png")+".json"
    raw=z.read(atlas_path)
    sources=json.loads(raw)["sources"]
    sn,sp=resource(sprite)
    found=[]
    for row in sources:
        kind=row["type"].split(":")[-1]
        if kind=="directory":
            prefix=row["prefix"]
            if sp.startswith(prefix):
                tail=sp[len(prefix):]
                source_ns,source=resource(row["source"])
                if source_ns==sn:
                    path=f"assets/{source_ns}/textures/{source}/{tail}.png"
                    if path in z.namelist():found.append((path,row))
        elif kind=="single":
            if resource(row.get("sprite",row["resource"]))==[sn,sp]:
                rn,rp=resource(row["resource"])
                found.append((f"assets/{rn}/textures/{rp}.png",row))
    check(len(found)==1,"sprite atlas resolution not unique "+str(found))
    return {"atlas_resource":atlas,"sprite_resource":sprite,"atlas_definition_path":atlas_path,"atlas_definition_sha256":hashlib.sha256(raw).hexdigest(),"atlas_source":found[0][1],"resolved_png":found[0][0]}

def main(a):
    version=Path(a.version_json).read_bytes();j=Path(a.official_client).resolve();mp=Path(a.client_mappings).read_bytes()
    pins=h18.version_preflight(version,j.read_bytes(),mp)
    old=json.loads(Path("project/integration/INT4_H20_V11_BED_MESH_UV_RESULT_V1.json").read_text())
    check(old["source_pins"]==pins and old["counts"]["vertices"]==144,"base mesh source drift")
    props=mapped_names(mp.decode())
    with tempfile.TemporaryDirectory() as t:
        t=Path(t);libs,_=mesh.download_libraries(json.loads(version),t/"libs")
        p=t/"mapped.properties";p.write_text("\n".join(k+"="+v for k,v in sorted(props.items()))+"\n")
        cp=":".join([str(j)]+libs)
        subprocess.run(["javac","-cp",cp,"-d",str(t),"tools/research/H20BedMeshProbe.java","tools/research/H20BedPoseMaterialProbe.java"],check=True)
        r=subprocess.run(["java","-cp",str(t)+":"+cp,"mcfrprobe.H20BedPoseMaterialProbe",str(p)],capture_output=True,text=True,timeout=180)
        print("H20_WORLD_PROBE_STDERR",r.stderr[-3000:],flush=True)
        check(r.returncode==0,"pose/material JVM failed "+r.stderr[-5000:]+" "+r.stdout[-1800:])
    world={};material=None
    for line in r.stdout.splitlines():
        if "WORLD\t" in line:
            row=line.split("WORLD\t",1)[1].split("\t")
            key=tuple(row[:6]);xyz=list(map(float,row[6:9]))
            check(key not in world and all(math.isfinite(x) for x in xyz),"world key/nonfinite")
            world[key]=xyz
        elif "WHITE_MATERIAL\t" in line:
            material=line.split("WHITE_MATERIAL\t",1)[1].strip().split("\t")
    check(len(world)==576 and material is not None and len(material)==2 and "H20_WORLD_POSE_COMPLETE" in r.stdout and "H20_MATERIAL_COMPLETE" in r.stdout,"world/material output incomplete "+str(len(world))+" "+str(material)+" "+r.stdout[-1800:])
    def bounds(values):
        return [round(min(v[i] for v in values),6) for i in range(3)]+[round(max(v[i] for v in values),6) for i in range(3)]
    groups={}
    for direction in ("NORTH","EAST","SOUTH","WEST"):
        part={}
        for half in ("head","foot"):
            xx=[v for k,v in world.items() if k[:2]==(half,direction)]
            check(len(xx)==72,"half world vertices missing")
            part[half]={"bounds_block_units":bounds(xx),"parts":{path:bounds([v for k,v in world.items() if k[:3]==(half,direction,path)]) for path in ("root/main","root/left_leg","root/right_leg")}}
        groups[direction]=part
    north=[v if k[0]=="foot" else [v[0],v[1],v[2]-1] for k,v in world.items() if k[1]=="NORTH"]
    combined=bounds(north)
    check(all(-1e-5<=v[1]<=1.00001 for v in north),"north vertical extent outside one block")
    check(abs(combined[3]-combined[0]-1)<1e-5 and abs(combined[5]-combined[2]-2)<1e-5,"two-block NORTH shape width/length "+str(combined))
    with ZipFile(j) as z:
        atlas=atlas_resolves(z,material[1],material[0])
        check(atlas["resolved_png"]==old["texture"]["candidate_official_white_png_path"],"material selected different PNG")
        png=z.read(atlas["resolved_png"])
        check(hashlib.sha256(png).hexdigest()==old["texture"]["sha256"],"white material hash drift")
    d={"schema":"MCFR_INT4_H20_V11_WORLD_POSE_AND_MATERIAL_SOURCE_V1","status":"PASS_ORIGINAL_JVM_BED_MODEL_POSE_AND_WHITE_ATLAS_SPRITE","source_pins":pins,
       "official_world_pose_calls":True,"isolated_jvm_not_live_game":True,
       "world_vertex_count":len(world),"direction_half_bounds":groups,"north_foot_origin_head_z_minus_1":combined,
       "material":atlas,"white_png_sha256":old["texture"]["sha256"],"texture_dimensions":old["texture"]["dimensions"],
       "source_mesh_git_blob":mesh.h18.git_blob(Path("project/integration/INT4_H20_V11_BED_MESH_UV_RESULT_V1.json").read_bytes()),
       "source_f2":{"run":45103243455,"images":4,"contrast_pixels":6446,"air_control_pixels":0},
       "new_game_runs":0,"new_F2":0,"live_renderer_call_during_old_F2_verified":False,"exact_GPU_pixel_causality":False,"legacy_F70_unconditional":0,"INT5":0,"INT6":0,
       "modeling_V11_scope_evidence_complete":True}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(d,sort_keys=True,indent=2)+"\n")
    print("H20_POSE_MATERIAL_RESULT",json.dumps(d,sort_keys=True,separators=(",",":")))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for key in ("version-json","official-client","client-mappings","output"):p.add_argument("--"+key,required=True)
    main(p.parse_args())
