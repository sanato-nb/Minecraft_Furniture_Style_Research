"""INT-4 H03/H05 P0 S20/S21 opposite observer drawer front actual native F2.

2014-era archived S20 open=false and S21 open=true were byte-identical
because the original camera was +Z/+X, while north-facing drawer changes its
NORTH "front" texture. Same source states/camera at -Z are a focused test.
This does not test player clicks or animation or certify GPU UV face sampling.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

from . import int4_nonchair_runtime as runner
from . import int4_f3_storage_shelf_light_capture as f3

VERSION="1.21.1"
FACING="north"
CASES=("S20","S21")
CAMERA_OLD=runner.CAMERA
CAMERA_FRONT="0.5 122.3 35.5 0 20"
BLOCK=(0,120,40)
OFFICIAL_AF_SHA1="c2f992081bdc4795ed6d87771a3b5f7c71103785"
RESOURCE="assets/another_furniture/"
OLD_S20_S21_NATIVE_SHA256="02ee02a4b05d0d9877fc12debd214a96823cea734e56e7f60972bb72ff29f566"
ROI=(340,230,690,620)
CH_THRESHOLD=24
AUDIT="INT4_H03_H05_S20_S21_NORTH_FACE_ACTUAL_FABRIC_F2_AUDIT_V1.json"


def check(x,msg):
    if not x: raise ValueError(msg)


def sha(data:bytes):return hashlib.sha256(data).hexdigest()


def source_preflight(game):
    case,source_hash=f3.original_7_cases()
    check(case["S20"]["state"]=="facing=north;open=false" and
          case["S21"]["state"]=="facing=north;open=true","FROZEN_S20_S21_ORIGINAL_SOURCE_DIFFERENT")
    jar=Path(game)/"mods"/"another_furniture-fabric-4.0.2.jar"
    check(hashlib.sha1(jar.read_bytes()).hexdigest()==OFFICIAL_AF_SHA1,
          "S20_S21_RUNTIME_OFFICIAL_AF_SHA1_NOT_PINNED")
    state_path=RESOURCE+"blockstates/oak_drawer.json"
    closed_path=RESOURCE+"models/block/drawer/oak.json"
    open_path=RESOURCE+"models/block/drawer/oak_open.json"
    with ZipFile(jar) as z:
        original_state=json.loads(z.read(state_path))
        closed=json.loads(z.read(closed_path))
        opened=json.loads(z.read(open_path))
        original_tex=z.read(RESOURCE+"textures/block/drawer/oak_front.png")
        opened_tex=z.read(RESOURCE+"textures/block/drawer/oak_front_open.png")
    variants=original_state["variants"]
    check(variants["facing=north,open=false"]["model"]=="another_furniture:block/drawer/oak" and
          variants["facing=north,open=true"]["model"]=="another_furniture:block/drawer/oak_open",
          "S20_S21_ACTUAL_RUNTIME_SELECTED_LEAF_NOT_DISTINCT")
    check(closed["parent"]=="another_furniture:block/template/drawer" and
          opened["parent"]=="another_furniture:block/drawer/oak",
          "S20_S21_ACTUAL_OPEN_INHERITANCE_CHANGED")
    check(opened["textures"]["front"]=="another_furniture:block/drawer/oak_front_open" and
          closed["textures"]["front"]=="another_furniture:block/drawer/oak_front" and
          set(opened["textures"])=={"front"} and
          closed["textures"]["side"]== "another_furniture:block/drawer/oak_side" and
          closed["textures"]["top"]== "another_furniture:block/drawer/oak_top",
          "S20_S21_ONLY_NORTH_FACE_DIFF_CANDIDATE_FAIL")
    check(sha(original_tex)!=sha(opened_tex),
          "S20_S21_RUNTIME_FRONT_TEXTURES_SAME_BINARY")
    return {
        "official_AF_JAR_SHA1":OFFICIAL_AF_SHA1,
        "original_frozen_source_1_5_B_sha256":source_hash,
        "real_runtime_blockstate_SHA256":sha(json.dumps(original_state,sort_keys=True).encode()),
        "real_runtime_model_s20":closed_path,
        "real_runtime_model_s21":open_path,
        "real_runtime_tex_s20_SHA256":sha(original_tex),
        "real_runtime_tex_s21_SHA256":sha(opened_tex),
        "same_source_element_geometry_inherited":True,
        "model_differing_texture_slot":"front",
        "modeled_front_face_direction_for_north_facing_block":"north",
        "original_south_east_camera":CAMERA_OLD,
        "new_front_north_camera":CAMERA_FRONT,
        "original_old_camera_S20_S21_identical_F2_sha256":OLD_S20_S21_NATIVE_SHA256,
    }


def capture(command,env,game,output,version):
    check(version==VERSION,"H03_H05_DRAWER_REQUIRES_PINNED_FABRIC_121")
    pre=source_preflight(game)
    check(runner.CAMERA==CAMERA_OLD and
          runner.state("another_furniture:oak_drawer","facing=north;open=false")==
          "another_furniture:oak_drawer[facing=north,open=false]",
          "H03_H05_ORIGINAL_DRAWER_RUNTIME_CHANGED")
    try:
        runner.CAMERA=CAMERA_FRONT
        manifest=runner.capture(command,env,game,Path(output),version,
                                case_ids=CASES,source_only=True)
    finally:
        runner.CAMERA=CAMERA_OLD
    check(set(manifest["server_states"])==set(CASES) and
          all(manifest["server_states"][c]["subject"]["exact"] is True for c in CASES),
          "H03_H05_DRAWER_ACTUAL_SERVER_STATES_NOT_EXACT")
    (Path(output)/"INT4_H03_H05_S20_S21_SOURCE_PIN_V1.json").write_text(
        json.dumps(pre,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return manifest


def changed_pixels(a,b):
    check(a.size==b.size==(1024,684),"H03_H05_ACTUAL_F2_DIMENSION_DRIFT")
    x0,y0,x1,y1=ROI
    ac=a.convert("RGB").crop(ROI).tobytes()
    bc=b.convert("RGB").crop(ROI).tobytes()
    ret=[]
    for i in range(len(ac)//3):
        j=i*3
        if max(abs(ac[j+k]-bc[j+k]) for k in range(3))>=CH_THRESHOLD:
            ret.append([x0+(i% (x1-x0)),y0+(i//(x1-x0))])
    return ret


def audit(output):
    root=Path(output)
    report=runner.audit(root)
    pre=json.loads((root/"INT4_H03_H05_S20_S21_SOURCE_PIN_V1.json").read_text(encoding="utf-8"))
    check(report["minecraft"]==VERSION and
          report["f_target_case_ids"]==list(CASES) and
          report["f_source_only"] is True and
          set(report["native_f2_sha256"])==set(CASES) and
          set(report["server_states"])==set(CASES) and
          all(report["server_states"][c]["subject"]["exact"] for c in CASES),
          "S20_S21_FROZEN_SOURCE_ACTUAL_SERVER_OR_F2_MISSING")
    with Image.open(root/"S20.png") as a,Image.open(root/"S21.png") as b:
        a.load();b.load()
        diff=changed_pixels(a,b)
    inside=[p for p in diff if 450<=p[0]<=570 and 345<=p[1]<=555]
    outside=[p for p in diff if p not in inside]
    result={
        "schema":"MCFR_INT4_H03_H05_P0_S20_S21_ACTUAL_NORTH_FACING_DRAWER_F2/v1",
        "status":("PASS_ACTUAL_NORTH_FACE_VISIBLE_CHANGE" if len(diff)>24 and not outside
                  else "CONDITIONAL_ACTUAL_F2_CAPTURED_BUT_NOT_FACE_LOCALIZED"),
        "source_original_fixture":"official AF 4.0.2 Fabric 1.21.1",
        "original_archive_14748847662_S20_S21_byte_identical":True,
        "new_actual_Fabric_game_executions":1,
        "new_actual_native_F2":2,
        "exact_original_server_blockstates_verified":2,
        "source_front_texture_slot_diff_in_actual_release":True,
        "selected_open_closed_model_in_original_JAR_distinct":True,
        "camera_from_north_opposing_original_south_east":True,
        "new_s20_s21_screen_diff_at_threshold24":len(diff),
        "new_s20_s21_screen_diff_at_threshold24_in_drawer_ROI":len(inside),
        "new_s20_s21_screen_diff_outside_drawer_ROI":len(outside),
        "new_s20_s21_screen_diff_bounds_inclusive":(
            [min(x for x,y in diff),min(y for x,y in diff),
             max(x for x,y in diff),max(y for x,y in diff)] if diff else None),
        "native_F2_sha256":report["native_f2_sha256"],
        "original_client_log_sha256":report["client_log_sha256"],
        "preflight":pre,
        "face_specific_exact_GPU_texel_to_screen_pixel_causal_approved":False,
        "north_front_face_visibility_geometric_candidate":True,
        "actual_player_open_or_close_tested":False,
        "full_F70_unconditional_approvals":0,
        "H03_full_exit":False,"H05_full_exit":False,
        "INT5_semantics_approved":0,"INT6_asset_rights_approved":0,
        "limitations":[
            "Original S20/S21 old F2 equality from south-east camera does not imply identical all camera views.",
            "Two new exact setblock states captured from the north are evidence of a visible model/texture difference, not player-click behavior.",
            "Only one camera change and two captures; exact GPU UV per-pixel sampler and whole-case functional approval not inferred.",
            "Original AF JAR and mod assets are not modified or distributed; original game F2 kept in temporary Actions artifact.",
        ]
    }
    (root/AUDIT).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
                            encoding="utf-8")
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
