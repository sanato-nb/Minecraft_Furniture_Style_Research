"""INT-4 new original-game experiment: AF variant3 × 4 facings + two controls.

Use only previously pinned 1.21.1 Fabric + AF runtime. Native Minecraft F2
screenshots are made by existing chair_runtime_capture, on a disposable
server-derived flat world. This file owns *experiment-specific* cases and
review logic; historic 16-case PR33/34 screenshot manifests are not changed.

Native images and contact sheets remain temporary CI artifacts; only their
source-state IDs/hashes and cautious observations are suitable for Git.
Image differences between different world positions are NOT causal proof of
texture differences or game-baked UV correctness.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

from .chair_runtime_fixture import ChairCase, DIRS, Y
from .chair_capture_isolation_audit import stone_pixels, specimen_color_pixels
from .int4_af_variant3_texture_audit import selector as source_selector

ROOT = Path(__file__).resolve().parents[2]
VERSION="1.21.1"
MODEL_1="another_furniture:block/chair/acacia_1"
MODEL_3="another_furniture:block/chair/acacia_3"
BLOCK="another_furniture:acacia_chair"
MANIFEST="INT4_AF_VARIANT3_REAL_F2_CAPTURE.json"
SOURCE_AUDIT="project/integration/INT4_AF_VARIANT3_PIXEL_AUDIT_RESULT.json"
CAMERA="FIXED_RELATIVE_TO_SOURCE_CHAIR_FROM_SOUTH_LOOK_NORTH"
EXPECTED_SHA_RUNTIME="3a806533856f169a502373bda43a76eeabc1e689"
EXPECTED_SHA_STUDY="37643398d7a49fdcfc6f2308ca04c13fb0b43aed"

def digest(blob):
    return hashlib.sha256(blob).hexdigest()

def capture_cases(version=VERSION):
    if version!=VERSION:
        raise ValueError("INT-4 AF original game experiment is pinned to 1.21.1")
    keys=[("AFV3",dir,"tucked=false,variant=3") for dir in DIRS]
    keys.extend([("AFV1",dir,"tucked=false,variant=1") for dir in ("north","south")])
    xs=(-40,-24,-8,8,24,40)
    result=tuple(
        ChairCase(f"{kind}_{direction}",VERSION,kind,BLOCK,properties,direction,x,Y,40)
        for (kind,direction,properties),x in zip(keys,xs)
    )
    if len(result)!=6 or len({c.case_id for c in result})!=6:
        raise ValueError("INT-4 source experiment missing or repeated source IDs")
    if any(abs(a.x-b.x)<16 for i,a in enumerate(result) for b in result[i+1:]):
        raise ValueError("Independent original screenshot stages overlap")
    return result

def exact_expected_models():
    out={}
    for case in capture_cases():
        model=(MODEL_1 if case.model_key=="AFV1" or case.facing=="south"
               else MODEL_3)
        out[case.case_id]={"model":model,"y":DIRS.index(case.facing)*90}
    return out

def assert_original_pinned_record(root=ROOT):
    path=Path(root)/SOURCE_AUDIT
    d=json.loads(path.read_text(encoding="utf-8"))
    a=d["evidence"]
    if (d["status"] if "status" in d else a["status"]) != a["status"]:
        raise ValueError("Original INT4 frozen evidence status inconsistent")
    if (a["status"]!="COMPLETE_SOURCE_TEXTURE_DIFFERENCE_NOT_GAME_PIXEL_OR_INT5_APPROVAL"
        or a["source_selector_discontinuities"]!=1
        or a["discontinuous_direction"]!="south"
        or a["model_face_comparison"]["changed_texture_binding_faces"]!=12
        or a["texture_png_study"]["rgba_different_pixel_count"]!=54
        or a["texture_png_runtime"]["rgba_different_pixel_count"]!=54
        or any(x["rgba_different_pixel_count"]!=0
               for x in a["textures_study_vs_runtime"].values())
        or a["limits"]["int5_screenshot_variant3_taken"]
        or a["limits"]["part_roles_verified"]
        or a["limits"]["asset_rights_or_ai_training_approved"]):
        raise ValueError("Original INT-4 source pixels, model selection, or approval boundary changed")
    return digest(path.read_bytes())

def paired_pixel_diagnostics(image_a,image_b):
    """Unaligned same-camera relative views; NO texture causality inference."""
    from PIL import ImageChops, ImageStat
    from .chair_capture_isolation_audit import CENTER_RECT
    a=image_a.convert("RGB").crop(CENTER_RECT)
    b=image_b.convert("RGB").crop(CENTER_RECT)
    delta=ImageChops.difference(a,b)
    rgb_stat=ImageStat.Stat(delta)
    return {
        "crop_rect":list(CENTER_RECT),
        "crop_pixel_count":a.width*a.height,
        "unaligned_different_rgb_pixels":sum(x != (0,0,0) for x in delta.getdata()),
        "unaligned_mean_abs_rgb_difference":[round(x,5) for x in rgb_stat.mean],
        "comparison_scope":"DIAGNOSTIC_ONLY_WORLD_X_BACKGROUND_AND_LIGHT_NOT_PIXEL_ALIGNED",
        "diff_caused_by_back_texture_approved":False,
    }

def audit(folder,root=ROOT):
    from PIL import Image, ImageDraw, ImageOps
    folder,root=Path(folder),Path(root)
    evidence_sha=assert_original_pinned_record(root)
    src_path=folder/MANIFEST
    src=json.loads(src_path.read_text(encoding="utf-8"))
    active=capture_cases()
    targets=exact_expected_models()
    expected={c.case_id:c for c in active}
    if (src.get("schema")!="MCFR_INT4_AF_VARIANT3_REAL_F2_CAPTURE/v1"
        or src.get("capture_profile")!="INT4_AF_VARIANT3_4_FACING_PLUS_2_VARIANT1_CONTROLS"
        or src.get("status")!="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED"
        or src.get("version")!=VERSION
        or not src.get("actual_game_capture")
        or src.get("minecraft_native_f2_screenshot_count")!=6
        or src.get("source_state_verified_count")!=6
        or src.get("human_verified_roles")!=0
        or src.get("materials_or_styles_approved")!=0
        or src.get("copyright_or_ai_training_approved")!=0):
        raise ValueError("INT4 actual Fabric client six-case proof or safe evidence boundary failed")
    rows_by_id={x["case_id"]:x for x in src.get("states",[])}
    if len(rows_by_id)!=6 or len(src["states"])!=6 or set(rows_by_id)!=set(expected):
        raise ValueError("Unexpected/missing original variant3 or control F2 screenshot IDs")
    original_registry=src["original_blockstate_source_registry"][BLOCK]
    if (original_registry["runtime_source_hash"]!=EXPECTED_SHA_RUNTIME or
        original_registry["research_source_hash"]!=EXPECTED_SHA_STUDY or
        original_registry["scope"]!="RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE"):
        raise ValueError("Actual AF runtime JAR blockstate source SHA does not match pinned release")

    photos={}
    rows=[]
    for case in active:
        item=rows_by_id[case.case_id]
        target=targets[case.case_id]
        path=folder/(case.case_id+".png")
        if (item["screenshot_file"]!=path.name or item["original_state"]!=case.state()
            or item["original_model_target"]!=target["model"]
            or item["original_model_y"]!=target["y"]
            or item["source_blockstate_digest"]!=EXPECTED_SHA_STUDY
            or item["running_mod_source_digest"]!=EXPECTED_SHA_RUNTIME
            or item["server_blockstate_verified"] is not True
            or item["native_F2_client_capture"] is not True
            or item["visual_semantic_approved"] is not False
            or item["screenshot_dimensions"]!=[1024,684]
            or digest(path.read_bytes())!=item["screenshot_sha256"]):
            raise ValueError("Source model, actual server state or screenshot SHA invalid: "+case.case_id)
        with Image.open(path) as photo:
            photo.load()
            if photo.size!=(1024,684):
                raise ValueError("Actual client F2 resolution changed")
            stone_count=stone_pixels(photo)
            chair_color=specimen_color_pixels(photo)
            photos[case.case_id]=photo.convert("RGB")
        if stone_count>=1000 or chair_color<150:
            raise ValueError("Foreign source floor intrusion or chair missing: "+case.case_id+
                             f", sky_stone={stone_count}, foreground={chair_color}")
        rows.append({
            "case_id":case.case_id,"facing":case.facing,
            "variant":3 if case.model_key=="AFV3" else 1,
            "source_model":target["model"],"source_y_rotation":target["y"],
            "server_state_verified":True,
            "screenshot_sha256":item["screenshot_sha256"],
            "original_state":case.state(),
            "camera":case.camera(),
            "stone_proxy_upper_sky_pixels":stone_count,
            "center_foreground_chroma_pixels":chair_color,
            "actual_f2_client_approved":True,
            "back_texture_causality_approved":False,
            "semantic_role_approved":0,
            "material_style_approved":0,
            "training_rights_approved":0
        })
    pairs={}
    for direction in ("north","south"):
        a,b=photos[f"AFV3_{direction}"],photos[f"AFV1_{direction}"]
        pairs[direction]=paired_pixel_diagnostics(a,b)
        pairs[direction]["variant3_model"]=targets[f"AFV3_{direction}"]["model"]
        pairs[direction]["variant1_model"]=targets[f"AFV1_{direction}"]["model"]
        pairs[direction]["same_source_model"]=pairs[direction]["variant3_model"]==pairs[direction]["variant1_model"]
    if pairs["north"]["same_source_model"] or not pairs["south"]["same_source_model"]:
        raise ValueError("North/south model control pair source distinction lost")
    csv_path=folder/"INT4_AF_VARIANT3_REAL_F2_STATES.csv"
    with csv_path.open("w",encoding="utf-8",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    width,height=512,342
    canvas=Image.new("RGB",(3*width,2*(height+32)),(238,240,241))
    draw=ImageDraw.Draw(canvas)
    for i,case in enumerate(active):
        frame=photos[case.case_id]
        thumb=frame.resize((width,height),resample=Image.Resampling.BILINEAR)
        col,row=i%3,i//3
        origin=(col*width,row*(height+32))
        canvas.paste(thumb,origin)
        draw.text((origin[0]+8,origin[1]+height+8),
                  f"{case.case_id} / {targets[case.case_id]['model'].split('/')[-1]} / y={targets[case.case_id]['y']}",
                  fill=(10,10,10))
    contact=folder/"INT4_AF_VARIANT3_F2_6_CONTACT_SHEET.png"
    canvas.save(contact)
    doc={
        "schema":"MCFR_INT4_AF_VARIANT3_ACTUAL_CLIENT_F2_AUDIT/v1",
        "status":"PASS_SIX_REAL_F2_SERVER_STATES_AND_ISOLATED_VIEWS_NOT_CAUSAL_IMAGE_PROOF",
        "source_checkpoints":{
            "int4_original_texture_source_record_sha256":evidence_sha,
            "actual_f2_manifest_sha256":digest(src_path.read_bytes()),
            "actual_f2_states_csv_sha256":digest(csv_path.read_bytes()),
            "six_capture_contact_sheet_sha256":digest(contact.read_bytes())
        },
        "scope":{
            "minecraft_version":VERSION,
            "fabric_real_client":True,
            "actual_f2_screenshots":6,
            "variant3_cardinal_directions":4,
            "variant1_control_directions":2,
            "server_verified_blocks":6,
            "source_model_targets_checked":6,
            "source_model_discontinuity_south":True,
            "all_six_stages_same_z":len({c.z for c in active})==1,
            "min_case_x_separation":min(abs(x.x-y.x) for i,x in enumerate(active) for y in active[i+1:]),
            "max_stone_proxy_upper_sky_pixels":max(x["stone_proxy_upper_sky_pixels"] for x in rows),
            "min_foreground_chroma_pixels":min(x["center_foreground_chroma_pixels"] for x in rows)
        },
        "f2_sha256_by_case":{x["case_id"]:x["screenshot_sha256"] for x in rows},
        "control_pair_diagnostics":pairs,
        "nonapprovals":{
            "observed_back_texture_difference_caused_by_source_model":False,
            "baked_mesh_uv_lock_pixel_equivalence":False,
            "part_roles_approved":0,"style_material_approved":0,
            "source_license_or_ai_training_approved":0,
            "intent_or_upstream_bug_status":"NOT_DETERMINED"
        },
        "limitations":[
            "Source models and blocks were matched to pinned mod JAR, but source PNG 54-pixel differences do not prove those exact pixels visible in F2",
            "The camera is at identical relative coordinates for each test, while different world positions can change grass and lighting pixels",
            "Native screenshot center crop differences are unregistered diagnostics, not a causal texture test",
            "No original PR33/34 F2 file, source model, mod JAR or copyrighted PNG is committed or replaced",
            "Real-world seating, collision, style, material function and rights are outside this experiment"
        ]
    }
    (folder/"INT4_AF_VARIANT3_CLIENT_AUDIT.json").write_text(
        json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return doc

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--directory",type=Path,required=True)
    p.add_argument("--root",type=Path,default=ROOT)
    args=p.parse_args(argv)
    result=audit(args.directory,args.root)
    print("INT4_REAL_CLIENT_VARIANT3:"+json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
