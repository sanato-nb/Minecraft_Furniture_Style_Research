"""INT-3: four original *child* chairs, actual verified PNG and per-face UV.

This reuses 1-3-F / 1-4 origin SHA ledgers, the already audited 1-3
chair geometry reader, and INT-2 source UV calculations. It intentionally
does not implement the Minecraft client model bakery or special renderer.
Painted orthographic projections are diagnostic only, not gameplay images.

Select a bounded fixed set of descendants of the four PR#29 templates:
 AF121, AF123, HC11210, MACAW67. These four must each have 100% of
their actual face slots resolved to original pinned PNGs, not substituted
color palettes. No JARs, original model JSONs or PNG files are exported.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageChops
from audit_int2_mod_textures import Sources, raw_source_sha, verify_png_crc
from audit_int2_full_face_links import default_uv, resolve_slot, canon
import render_int3_chair_geometry as geo

ROOT=Path(__file__).resolve().parents[2]
MODEL_KEYS={
    "AF1393":"AF121",
    "AF1394":"AF123",
    "HC13":"HC11210",
    "MACAW1424":"MACAW67",
}
FACE_TOTALS={"AF121":46,"AF123":46,"HC11210":78,"MACAW67":59}
EXPECTED_FACES=229
YAW=(45,-135)
PANEL=(640,615)
FACES=geo.FACE_CORNERS

def uvs(t,rotation):
    if len(t)!=4:raise ValueError("Invalid source UV tuple")
    u0,v0,u1,v1=t
    corners=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
    if rotation not in (0,90,180,270):raise ValueError("Face UV rotation not 90-degree multiple")
    r=rotation//90
    return corners[r:]+corners[:r]

def original_hash(mod,data):
    return raw_source_sha(data,"GIT_BLOB_SHA1" if mod in ("AF","HC") else "SHA256")

def read_original_shapes(db,sources):
    # This is the existing PR#29 source-vs-F 45-element independent audit.
    entries,provider_report,role_counts=geo.read_providers(db,sources)
    assert len(entries)==4 and sum(len(x["shapes"]) for x in entries)==45
    return {x["provider_key"]:x for x in entries},provider_report,role_counts

def assemble_model(db,sources,providers,parent_key,child_key):
    model=db.execute("""
        SELECT model_key,source_id,resource_id,path,sha
        FROM model WHERE model_key=?""",(child_key,)).fetchone()
    if model is None:raise ValueError("Missing fixed descendant "+child_key)
    if model["source_id"]!=providers[parent_key]["mod"]:
        raise ValueError("Unexpected change to descendant's mod or parent")
    actual=db.execute("SELECT provider_key,face_instances FROM geometry WHERE model_key=?",(child_key,)).fetchone()
    if actual is None or actual[0]!=parent_key or int(actual[1])!=FACE_TOTALS[child_key]:
        raise ValueError("Child model points to a different shape provider "+child_key)
    body_raw=sources.fetch(model["source_id"],model["path"])
    if original_hash(model["source_id"],body_raw)!=model["sha"]:
        raise ValueError("Fixed original child model source SHA mismatched "+child_key)
    body=json.loads(body_raw.decode("utf-8-sig"))
    # A child can inherit one or more texture slots through its parent
    # chain. Build the exact source JSON bindings from root to leaf; testing
    # only the leaf 'textures' object would incorrectly flag valid aliases.
    chain=list(db.execute("""
       SELECT l.position,m.model_key,m.source_id,m.path,m.sha
       FROM lineage l JOIN model m ON m.model_key=l.ancestor_key
       WHERE l.model_key=? ORDER BY l.position""",(child_key,)))
    if not chain or chain[0]["model_key"]!=child_key:
        raise ValueError("Pinned original model lineage missing leaf")
    bindings={}
    for ancestor in reversed(chain):
        raw=sources.fetch(ancestor["source_id"],ancestor["path"])
        if original_hash(ancestor["source_id"],raw)!=ancestor["sha"]:
            raise ValueError("Pinned original source SHA differs in child lineage")
        inherited=json.loads(raw.decode("utf-8-sig")).get("textures",{})
        if not isinstance(inherited,dict):
            raise ValueError("Original lineage texture bindings are not a dictionary")
        bindings.update(inherited)

    shapes=providers[parent_key]["shapes"]
    original_parent=db.execute("SELECT path,sha FROM model WHERE model_key=?",(parent_key,)).fetchone()
    p_raw=sources.fetch(model["source_id"],original_parent["path"])
    if original_hash(model["source_id"],p_raw)!=original_parent["sha"]:
        raise ValueError("Original parent SHA differs from audited PR#29")
    original_elements=json.loads(p_raw.decode("utf-8-sig")).get("elements",[])
    if len(original_elements)!=len(shapes):raise ValueError("Provider JSON elements changed")
    shape_by_id={r["index"]:r for r in shapes}
    slot_map={
        r["slot"]:(r["texture_id"],r["resolution"],r["face_count"])
        for r in db.execute("SELECT slot,texture_id,resolution,face_count FROM model_slot WHERE model_key=?",(child_key,))
    }
    selected=[]
    source_pixels={}
    stats=Counter()
    for element in shapes:
        idx=element["index"]
        orig=original_elements[idx]
        faces=orig.get("faces",{})
        rows=list(db.execute("""
          SELECT f.direction,f.slot,f.uv,f.uv_declared,f.uv_rotation,
                 f.cullface,f.tintindex
          FROM face f WHERE f.provider_key=? AND f.element_index=?
          ORDER BY f.direction""",(parent_key,idx)))
        if len(faces)!=len(rows):
            raise ValueError("Original source face count differs from 1-3-F")
        for face in rows:
            direction=face["direction"]
            declared=faces.get(direction)
            if declared is None or declared.get("texture")!=face["slot"]:
                raise ValueError("Original face slot mapping mismatches F source")
            rotate=int(declared.get("rotation",0))
            if rotate!=int(face["uv_rotation"]):
                raise ValueError("Original texture rotation differs in F")
            rawuv=declared.get("uv")
            if bool(rawuv)!=bool(face["uv_declared"]):
                raise ValueError("Original UV declared flag mismatch")
            if rawuv:
                uv=tuple(float(v) for v in rawuv)
                # F's original format is decimal text for some files and
                # rational text for others; compare semantic UV values, not
                # superficial rendering (e.g. 0.75 == 3/4).
                recorded=tuple(float(Fraction(part)) for part in face["uv"].split("|"))
                if len(recorded)!=4 or any(
                    not math.isfinite(a) or not math.isfinite(b)
                    or abs(a-b)>1e-7 for a,b in zip(uv,recorded)
                ):
                    raise ValueError("Original explicit UV differs from F: "
                                     +child_key+"/"+str(idx)+"/"+direction)
            else:
                uv=tuple(float(v) for v in default_uv(orig["from"],orig["to"],direction))
            texref,texres=resolve_slot(declared["texture"],bindings)
            if texref!="RESOURCE_ID":
                raise ValueError("Original child model does not resolve a texture face")
            slot=declared["texture"]
            registered=slot_map.get(slot)
            if not registered or registered[0] is None or registered[1]!="RESOURCE_ID":
                raise ValueError("Fixed source child face has an unbound texture")
            rec=db.execute("SELECT id,source_id,resource_id,path,sha,texture_status FROM texture WHERE id=?",(registered[0],)).fetchone()
            if rec is None or rec["resource_id"]!=texres or rec["texture_status"] not in ("PINNED_MOD_PNG","PINNED_VANILLA_PNG"):
                raise ValueError("Original source texture alias/ID mismatched 1-3-F")
            if rec["source_id"] not in ("AF","HC","MACAW","MC1.21.1","MC1.21.11"):
                raise ValueError("Unrecognized pinned original texture source")
            if rec["id"] not in source_pixels:
                data=sources.fetch(rec["source_id"],rec["path"])
                if original_hash(rec["source_id"],data)!=rec["sha"]:
                    raise ValueError("Original PNG SHA mismatch: "+rec["path"])
                verify_png_crc(data,rec["path"])
                with Image.open(io.BytesIO(data)) as file:
                    file.load()
                    png=file.convert("RGBA")
                # These fixed chair textures are expected to be static PNGs.
                mcmeta=sources.fetch(rec["source_id"],rec["path"]+".mcmeta",required=False)
                if mcmeta and json.loads(mcmeta.decode("utf-8-sig")).get("animation"):
                    raise ValueError("Animated texture needs temporal review, not fixed-face static render")
                source_pixels[rec["id"]]={"image":png,"source":rec["source_id"],"path":rec["path"],
                                         "sha":rec["sha"],"resource":rec["resource_id"]}
            selected.append({
                "child_key":child_key,"parent_key":parent_key,"element":idx,
                "face":direction,"face_uv":uv,"uv_rotation":rotate,
                "texture_id":rec["id"],"texture_path":rec["path"],"texture_sha":rec["sha"],
                "source_slot":slot,"shape":element
            })
            stats["faces"]+=1
            stats["explicit_uv" if rawuv else "default_uv"]+=1
            stats["uv_rotation_"+str(rotate)]+=1
    if len(selected)!=FACE_TOTALS[child_key]:
        raise ValueError("Expected all original source faces for "+child_key)
    return {
       "model_key":child_key,"resource_id":model["resource_id"],
       "model_sha":model["sha"],"model_path":model["path"],
       "parent_key":parent_key,"parent_sha":original_parent["sha"],
       "source_id":model["source_id"],
       "selected_faces":selected,"textures":source_pixels,
       "stats":dict(stats),"shapes":shapes
    }

def eye_vector(yaw,pitch=30):
    a=math.radians(yaw)
    b=math.radians(pitch)
    return (math.sin(a)*math.cos(b),math.sin(b),math.cos(a)*math.cos(b))

def blockstate_rotate_point(point,angle):
    """Source blockstate JSON 'y' quarter turns about the cube center.

    Geometry-only bake approximation; no uvlock, atlas or client renderer.
    """
    if angle not in (0,90,180,270):
        raise ValueError("Diagnostic block rotation must be a quarter-turn")
    if angle==0:return point
    x,y,z=point
    sn=round(math.sin(math.radians(angle)))
    cs=round(math.cos(math.radians(angle)))
    return (8+cs*(x-8)+sn*(z-8),y,8-sn*(x-8)+cs*(z-8))

def blockstate_rotate_normal(normal,angle):
    if angle not in (0,90,180,270):
        raise ValueError("Diagnostic normal rotation must be a quarter-turn")
    if angle==0:return normal
    x,y,z=normal
    sn=round(math.sin(math.radians(angle)))
    cs=round(math.cos(math.radians(angle)))
    return (cs*x+sn*z,y,-sn*x+cs*z)

def visible(normal,shape,yaw,block_y=0):
    if shape["angle"] and shape["axis"]:
        n=geo.transform(normal,{"axis":shape["axis"],"angle":shape["angle"],
                                "pivot":(0,0,0),"rescale":shape["rescale"]})
    else:n=normal
    n=blockstate_rotate_normal(n,block_y)
    return sum(a*b for a,b in zip(n,eye_vector(yaw)))>0.0001

NORMALS={"north":(0,0,-1),"south":(0,0,1),"east":(1,0,0),"west":(-1,0,0),
         "up":(0,1,0),"down":(0,-1,0)}

def polygon_texture(out,png,screen,corners_uv):
    """Rasterize an affine face using Pillow NEAREST and an exact face mask.

    This maps 4 per-face UV corners onto an orthographic quad. It is not the
    Minecraft texture-atlas baker (no uvlock, atlas stitching or mipmapping).
    """
    if len(screen)!=4:raise ValueError("A single baked face must have four points")
    x0=max(0,math.floor(min(x for x,y in screen))-2)
    y0=max(0,math.floor(min(y for x,y in screen))-2)
    x1=min(out.width,math.ceil(max(x for x,y in screen))+2)
    y1=min(out.height,math.ceil(max(y for x,y in screen))+2)
    w,h=x1-x0,y1-y0
    if w<1 or h<1:return 0
    q0,q1,q2,q3=screen
    a=q1[0]-q0[0];b=q3[0]-q0[0]
    c=q1[1]-q0[1];d=q3[1]-q0[1]
    det=a*d-b*c
    if abs(det)<0.00002:return 0
    # affine screen -> source texture pixel coordinates
    def origin(u):
        return (u[0]-corners_uv[0][0],u[1]-corners_uv[0][1])
    du=origin(corners_uv[1])
    dv=origin(corners_uv[3])
    scale_u=png.width/16
    scale_v=png.height/16
    ua=scale_u*(du[0]*d-dv[0]*c)/det
    ub=scale_u*(-du[0]*b+dv[0]*a)/det
    va=scale_v*(du[1]*d-dv[1]*c)/det
    vb=scale_v*(-du[1]*b+dv[1]*a)/det
    uc=scale_u*corners_uv[0][0]+ua*(x0-q0[0])+ub*(y0-q0[1])
    vc=scale_v*corners_uv[0][1]+va*(x0-q0[0])+vb*(y0-q0[1])
    # PIL affine coefficients map local destination x,y -> source x,y.
    layer=png.transform((w,h),Image.Transform.AFFINE,(ua,ub,uc,va,vb,vc),
                         resample=Image.Resampling.NEAREST,fillcolor=(0,0,0,0))
    mask=Image.new("L",(w,h),0)
    d=ImageDraw.Draw(mask)
    d.polygon([(x-x0,y-y0) for x,y in screen],fill=255)
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"),mask))
    out.alpha_composite(layer,(x0,y0))
    return 1

def preview(entry,yaw,block_y=0):
    W,H=PANEL
    canvas=Image.new("RGBA",(W,H),(246,248,251,255))
    d=ImageDraw.Draw(canvas)
    shapes=entry["shapes"]
    corners3={s["index"]:[blockstate_rotate_point(p,block_y) for p in geo.cube_points(s)]
              for s in shapes}
    views={idx:[geo.camera(p,yaw) for p in points] for idx,points in corners3.items()}
    xs=[p[0] for ps in views.values() for p in ps]
    ys=[p[1] for ps in views.values() for p in ps]
    spanx=max(1,max(xs)-min(xs))
    spany=max(1,max(ys)-min(ys))
    scale=min((W-75)/spanx,(H-125)/spany,24)
    cx=(max(xs)+min(xs))/2
    cy=(max(ys)+min(ys))/2
    def px(p):return ((p[0]-cx)*scale+W/2, (cy-p[1])*scale+(H/2)+10)
    drawlist=[]
    for face in entry["selected_faces"]:
        s=face["shape"]
        direction=face["face"]
        if not visible(NORMALS[direction],s,yaw,block_y):continue
        vert=[views[s["index"]][i] for i in FACES[direction]]
        depth=sum(p[2] for p in vert)/4
        pts=[px(p) for p in vert]
        drawlist.append((depth,pts,face))
    rendered=0
    for _,pts,face in sorted(drawlist,key=lambda t:t[0]):
        tex=entry["textures"][face["texture_id"]]["image"]
        if polygon_texture(canvas,tex,pts,uvs(face["face_uv"],face["uv_rotation"])):
            rendered+=1
    d=ImageDraw.Draw(canvas)
    label=f'{entry["source_id"]} / {entry["model_key"]} / {entry["resource_id"].split("/")[-1]}'
    d.rectangle((6,6,W-6,65),fill=(255,255,255,236),outline=(215,220,228))
    d.text((18,16),label,fill=(30,45,57))
    annotation=(f'original PNG + source UV | view {yaw:+d} | NOT IN-GAME'
                if block_y==0 else
                f'original PNG + UV | state y={block_y} | view {yaw:+d} | NOT IN-GAME')
    d.text((18,38),annotation,fill=(84,99,118))
    d.text((18,H-24),f'visual diagnosis only | {rendered} visible faces of {len(entry["selected_faces"])} source faces',
           fill=(60,79,92))
    return canvas.convert("RGB"),rendered

def run(args):
    root=Path(args.root)
    output=Path(args.out)
    output.mkdir(parents=True,exist_ok=True)
    source=Sources(args)
    db=geo.load_db(root)
    try:
        provider,original_models,roles=read_original_shapes(db,source)
        if set(provider)!=set(MODEL_KEYS):
            raise ValueError("Source provider set changed since PR29")
        charts=[]
        audits=[]
        face_ledger=[]
        all_texture_sha={}
        face_total=Counter()
        for parent,child in MODEL_KEYS.items():
            entry=assemble_model(db,source,provider,parent,child)
            face_total[child]=len(entry["selected_faces"])
            for tid,data in entry["textures"].items():
                all_texture_sha[data["source"]+":"+data["path"]]=data["sha"]
            for record in entry["selected_faces"]:
                face_ledger.append({
                    "model_key":child,"provider_key":parent,
                    "element_index":record["element"],"face_direction":record["face"],
                    "texture_id":record["texture_id"],"original_png_path":record["texture_path"],
                    "original_png_sha":record["texture_sha"],
                    "source_slot":record["source_slot"],
                    "uv":"|".join(str(x) for x in record["face_uv"]),
                    "uv_rotation":record["uv_rotation"],
                    "source_evidence":"ORIGINAL_CHILD_MODEL_AND_ORIGINAL_PROVIDER_AND_F_DB_AND_PNG_SHA",
                    "game_visual_verified":"NO"})
            rendered_count=[]
            for yaw in YAW:
                pane,visible_count=preview(entry,yaw)
                rendered_count.append(visible_count)
                charts.append(pane)
            audits.append({
                "source":entry["source_id"],"child_key":child,
                "child_resource":entry["resource_id"],"child_sha":entry["model_sha"],
                "parent_key":parent,"parent_sha":entry["parent_sha"],
                "original_png_count":len(entry["textures"]),
                "total_faces_source":len(entry["selected_faces"]),
                "visible_faces_diagram":rendered_count,
                "uv_stats":entry["stats"]})
        if dict(face_total)!=FACE_TOTALS or sum(face_total.values())!=EXPECTED_FACES:
            raise ValueError("Four children missing an original face")
        if len(charts)!=8:raise ValueError("Four chairs times two views expected")
        # Contact sheet uses original PNG pixels but does not contain raw PNG
        # source files, model JSON or JAR archives.
        sheet=Image.new("RGB",(PANEL[0]*2,PANEL[1]*4),(240,244,248))
        for idx,im in enumerate(charts):
            sheet.paste(im,((idx%2)*PANEL[0],(idx//2)*PANEL[1]))
        png=output/"INT3_4_CHAIRS_ORIGINAL_UV_TEXTURE_DIAGNOSTIC.png"
        sheet.save(png,optimize=False)
        rows=sorted(face_ledger,key=lambda r:(r["model_key"],r["element_index"],r["face_direction"]))
        csvfile=output/"INT3_229_ORIGINAL_FACE_UV_TEXTURE_EVIDENCE.csv"
        with csvfile.open("w",encoding="utf-8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        report={
            "schema":"MCFR_INT3_4_CHAIRS_TEXTURED_SOURCE_UV/v1",
            "status":"PASS_SOURCE_PINNED_CHILD_TEXTURE_FACES_DIAGNOSTIC_NOT_MINECRAFT_CLIENT",
            "models":audits,"original_faces":EXPECTED_FACES,
            "four_child_source_face_counts":dict(sorted(face_total.items())),
            "model_providers":original_models,
            "source_png_count":len(all_texture_sha),
            "verified_original_png_hashes":dict(sorted(all_texture_sha.items())),
            "contact_sheet_sha256":hashlib.sha256(png.read_bytes()).hexdigest(),
            "face_csv_sha256":hashlib.sha256(csvfile.read_bytes()).hexdigest(),
            "visible_diagram_panels":len(charts),
            "boundary":{
                "source_child_model_sha_check":"PASS",
                "source_provider_model_sha_check":"PASS_VIA_EXISTING_PR29_ORIGINAL_AUDITOR",
                "face_slots_uv_rotation_pixel_png_sha_check":"PASS",
                "actual_minecraft_client_render_verified":False,
                "part_function_approved":0,
                "style_or_material_classification_approved":0,
                "source_license_or_training_approved":0,
                "source_original_png_json_jar_exported":False,
                "known_limitations":[
                    "Orthographic face polygons and nearest-PNG sampling, not Minecraft blockstate rotations, texture atlas, UV lock, AO or engine culling",
                    "Colors come from pinned original PNG pixels but visual shading and surface order are diagnostic",
                    "Takes four explicit source-bound child chairs, not all descendants, mods, or furniture",
                    "A source-level face/UV match does not certify gameplay rendering or function",
                ],
            },
        }
        (output/"INT3_TEXTURED_CHAIRS_SOURCE_REPORT.json").write_text(
             json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("INT3_TEXTURED_CHAIRS_RESULT:"+json.dumps(report,ensure_ascii=False,sort_keys=True))
        return report
    finally:
        db.close()
        source.close()

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("root","af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+name,type=Path,required=name!="root",default=ROOT if name=="root" else None)
    args=parser.parse_args(argv)
    run(args)

if __name__=="__main__":
    main()
