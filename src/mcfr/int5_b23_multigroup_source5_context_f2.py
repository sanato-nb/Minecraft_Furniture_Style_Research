"""INT-5-B23 multi-context batch: identify which original source groups suppress element5.

Ten independent CI jobs (2 AF targets x 5 contexts), two separate official
Fabric 1.21.1 GUI clients per job, original child JSON only differing in the
presence of original parent source element5. Exact original 10-element ordering,
UV, faces, coordinates, textures and official original parent remain immutable.

Screenshots are original native F2 and are not imported to the Git research DB.
This is a narrow source-raster experiment, NOT physical role/material/style
certification, GPU per-face ownership, z-buffer exclusivity or IP rights.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import shutil
from pathlib import Path
from zipfile import ZipFile

from . import int5_b19_four_unresolved_four_view_f2 as b19
from . import int5_b20_af_reversed_x_three_session_f2 as b20
from . import int5_b21_af_source5_isolation_four_view_f2 as b21
from . import int5_b22_af_source5_source6_pair_four_view_f2 as b22
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15

TARGETS=b22.TARGETS
VERSION=b22.VERSION
CONTEXTS={
    "legs_0_3":(0,1,2,3),
    "seat_4":(4,),
    "back_7_9":(7,8,9),
    "front_0_4":(0,1,2,3,4),
    "all_others":(0,1,2,3,4,7,8,9),
}
MODES=("without_5","with_5")
MANIFEST="INT5_B23_MULTI_CONTEXT_TWO_REAL_FABRIC_CLIENTS_MANIFEST_V1.json"
AUDIT="INT5_B23_MULTI_CONTEXT_FOUR_VIEW_INDEPENDENT_F2_AUDIT_V1.json"
STATUS="INT5_B23_TWO_REAL_FABRIC_CLIENTS_F2_CAPTURED_PENDING_AUDIT"

def need(condition,reason):
    if not condition:
        raise ValueError("INT5-B23: "+reason)

def set_target(target):
    b22.set_target(target)

def source_identity(target):
    return b22.source_identity(target)

def choose(context,mode):
    need(context in CONTEXTS and mode in MODES,"unknown batch context/mode")
    need(5 not in CONTEXTS[context] and 6 not in CONTEXTS[context],
         "context must exclude exact experimental source5 and pinned source6")
    return tuple(i for i in range(10) if i==6 or i in CONTEXTS[context] or
                 (i==5 and mode=="with_5"))

def child_for_context(original_child,original_parent,target,context,mode):
    need(target in TARGETS and context in CONTEXTS and mode in MODES,
         "two originals and five audited context groups only")
    child=json.loads(original_child.decode("utf-8-sig"))
    parent=json.loads(original_parent.decode("utf-8-sig"))
    all_elements=parent.get("elements")
    pin=b20.PIN[target]
    need("elements" not in child and
         child.get("parent")==("another_furniture:block/template/chair"
                             if target=="AF121_5" else
                             "another_furniture:block/template/chair_tucked") and
         isinstance(all_elements,list) and len(all_elements)==10 and
         sum(len(e["faces"]) for e in all_elements)==46,
         "unchanged original child inheritance, exactly 10 elements and 46 faces required")
    five,six=all_elements[5],all_elements[6]
    need(five["from"]==pin["from"] and five["to"]==pin["to"] and
         len(five["faces"])==4 and five["from"][0]>five["to"][0] and
         len(six["faces"])==4 and six["from"][0]<six["to"][0],
         "original source5/source6 from/to/face identity changed")
    selected=choose(context,mode)
    result=copy.deepcopy(child)
    result["elements"]=[copy.deepcopy(all_elements[i]) for i in selected]
    need([result["elements"][j]==all_elements[i] for j,i in enumerate(selected)]==
         [True]*len(selected) and
         {k:v for k,v in result.items() if k!="elements"}==child and
         (5 in selected)==(mode=="with_5") and 6 in selected,
         "original ordered face/UV/coordinates/bindings not copied byte-for-structure")
    expected=sum(len(all_elements[i]["faces"]) for i in selected)
    need(sum(len(e["faces"]) for e in result["elements"])==expected,
         "original exact face count invalid")
    data=json.dumps(result,ensure_ascii=False,separators=(",",":")).encode("utf-8")
    scope={
        "target":target,"context":context,"mode":mode,
        "all_original_parent_elements":10,"all_original_parent_faces":46,
        "selected_original_element_indices":list(selected),
        "selected_original_face_count":expected,
        "original_source5_from":list(five["from"]),
        "original_source5_to":list(five["to"]),
        "original_parent_git_blob":pin["parent_blob"],
        "original_child_git_blob":pin["child_blob"],
        "faces_uv_textures_coordinates_identical_to_original_parent":True,
        "selected_element_order_maintained":True,
        "original_child_parent_and_textures_identical":True,
        "changed_member_only_child":pin["child"],
        "original_or_patched_JAR_distributed":False,
        "physical_function_material_style_approved":False,
        "original_face_exclusive_GPU_pixels_approved":False,
        "third_party_training_or_redistribution_approved":False,
    }
    return data,scope

def install_variant(modjar,official,target,context,mode):
    pin=b20.PIN[target]
    need(hashlib.sha1(official).hexdigest()==h12.JAR_SHA1,
         "official Another Furniture 4.0.2 input SHA1 differs")
    with ZipFile(io.BytesIO(official)) as z:
        infos=z.infolist()
        need(z.testzip() is None and len(infos)==len(set(i.filename for i in infos)),
             "original ZIP CRC and duplicate member guard")
        original={i.filename:z.read(i.filename) for i in infos}
    child,scope=child_for_context(original[pin["child"]],original[pin["parent"]],
                                  target,context,mode)
    temporary=modjar.with_suffix(".b23-disposable")
    with ZipFile(temporary,"w") as z:
        for member in infos:
            z.writestr(member,child if member.filename==pin["child"]
                       else original[member.filename])
    with ZipFile(temporary) as z:
        need(z.testzip() is None and z.namelist()==list(original) and
             [name for name in original if z.read(name)!=original[name]]==
             [pin["child"]] and z.read(pin["parent"])==original[pin["parent"]],
             "only exact original AF child may be patched, shared parent immutable")
        decoded=json.loads(z.read(pin["child"]))
        need(decoded["elements"]==json.loads(child)["elements"] and
             "elements" not in json.loads(original[pin["child"]]) and
             list(decoded["elements"]) and
             decoded["elements"]==
             [json.loads(original[pin["parent"]])["elements"][i]
              for i in scope["selected_original_element_indices"]],
             "exact original child and selected original parent elements reread failed")
    disposable_sha1=hashlib.sha1(temporary.read_bytes()).hexdigest()
    temporary.replace(modjar)
    need(disposable_sha1==hashlib.sha1(modjar.read_bytes()).hexdigest() and
         disposable_sha1!=h12.JAR_SHA1,"disposable source child installation failed")
    return {**scope,"official_JAR_SHA1":h12.JAR_SHA1,
            "disposable_JAR_SHA1_local_only":disposable_sha1,
            "changed_uncompressed_JAR_members":[pin["child"]]}

def capture(command,env,game,out,version,target,context):
    need(version==VERSION and target in TARGETS and context in CONTEXTS,
         "exact original targets, context groups, Minecraft 1.21.1 only")
    set_target(target)
    source=source_identity(target)
    jar,official=b21.pin_official_jar(game,target)
    original_check=b19.preflight(game)
    game,out=Path(game),Path(out)
    need(not out.exists(),"B23 original screenshot directory must be fresh")
    out.mkdir(parents=True)
    worlds=[p for p in (game/"saves").iterdir()
            if p.is_dir() and (p/"level.dat").is_file()]
    need(len(worlds)==1,"exact one official creative fixture world")
    world=worlds[0]
    pristine=game/"int5-b23-world-original-snapshot"
    need(not pristine.exists(),"pristine world snapshot cannot exist")
    shutil.copytree(world,pristine,ignore=shutil.ignore_patterns("session.lock"))
    interventions={}
    try:
        for mode in MODES:
            shutil.rmtree(world)
            shutil.copytree(pristine,world,
                            ignore=shutil.ignore_patterns("session.lock"))
            interventions[mode]=install_variant(jar,official,target,context,mode)
            session=b19.capture_session(command,env,game,out/mode,
                                         mode,original_check)
            need(session["new_real_native_F2"]==16,
                 "each of the two source5-on/off real clients must capture 16 real F2")
        doc={
            "schema":"MCFR_INT5_B23_TWO_CONTEXT_CLIENTS/v1","status":STATUS,
            "target":target,"context":context,"source":source,
            "original_minecraft":VERSION,
            "official_AF_release_JAR_SHA1":h12.JAR_SHA1,
            "modes":list(MODES),"four_cameras":list(b19.VIEWS),
            "four_original_stages":list(b19.stages()),
            "world_restored_from_same_pristine_snapshot_for_each_mode":True,
            "original_child_only_interventions":interventions,
            "real_Fabric_clients":2,"real_native_F2_total":32,
            "real_server_exact_chair_state_proofs":32,
            "real_server_exact_support_slab_proofs":32 if target=="AF123_5" else 0,
            "real_client_manifests":{m:m+"/manifest.json" for m in MODES},
            "original_45_element_role_material_semantic_approvals":0,
            "GPU_face_UV_exclusive_pixel_approvals":0,
            "third_party_training_or_redistribution_approvals":0,
        }
        (out/MANIFEST).write_text(
            json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
            encoding="utf-8")
        return doc
    finally:
        if jar.is_file():
            jar.write_bytes(official)
        if pristine.exists():
            shutil.rmtree(pristine)

def compare_frames(scenes):
    need(set(scenes)==set(MODES),"both independently rendered sources required")
    a,negative,b,empty=b19.stages()
    metrics={}
    for view in b19.VIEWS:
        old=scenes["without_5"][view]
        new=scenes["with_5"][view]
        changed=h15.pixel_changes(old[a],new[a])
        changed_after=h15.pixel_changes(old[b],new[b])
        old_fg=h15.pixel_changes(old[a],old[empty])
        new_fg=h15.pixel_changes(new[a],new[empty])
        metrics[view]={
            "five_addition_before_pixels":len(changed),
            "five_addition_after_pixels":len(changed_after),
            "without5_chair_foreground_pixels":len(old_fg),
            "with5_chair_foreground_pixels":len(new_fg),
            "diff_outside_union_of_both_foregrounds_pixels":
                len(changed-(old_fg|new_fg)),
            "negative_unchanged_pixels":
                len(h15.pixel_changes(old[negative],new[negative])),
            "empty_air_or_slab_unchanged_pixels":
                len(h15.pixel_changes(old[empty],new[empty])),
            "without5_original_A_A_pixels":
                len(h15.pixel_changes(old[a],old[b])),
            "with5_original_A_A_pixels":
                len(h15.pixel_changes(new[a],new[b])),
            "before_full_RGB_images_equal":old[a].tobytes()==new[a].tobytes(),
            "after_full_RGB_images_equal":old[b].tobytes()==new[b].tobytes(),
        }
    return metrics

def decide(metrics):
    need(set(metrics)==set(b19.VIEWS),"four original cardinal cameras mandatory")
    if not all(m["five_addition_before_pixels"]==
               m["five_addition_after_pixels"] and
               m["negative_unchanged_pixels"]==0 and
               m["empty_air_or_slab_unchanged_pixels"]==0 and
               m["without5_original_A_A_pixels"]==0 and
               m["with5_original_A_A_pixels"]==0 and
               m["diff_outside_union_of_both_foregrounds_pixels"]==0
               for m in metrics.values()):
        return "CONDITIONAL_B23_TEMPORAL_NEGATIVE_OR_BACKGROUND_DRIFT"
    if not all(m["with5_chair_foreground_pixels"]>0 and
               m["without5_chair_foreground_pixels"]>0 for m in metrics.values()):
        return "CONDITIONAL_B23_ORIGINAL_CHAIR_NOT_VISIBLE_IN_ALL_CAMERAS"
    if any(m["five_addition_before_pixels"]>0 for m in metrics.values()):
        return "PASS_SOURCE5_ADDS_PIXELS_IN_ORIGINAL_CONTEXT"
    return "PASS_SOURCE5_NO_ADDITIONAL_PIXELS_IN_ORIGINAL_CONTEXT"

def audit(folder,target,context):
    need(context in CONTEXTS and target in TARGETS,"original batch id missing")
    set_target(target)
    folder=Path(folder)
    doc=json.loads((folder/MANIFEST).read_text(encoding="utf-8"))
    source=source_identity(target)
    need(doc["schema"]=="MCFR_INT5_B23_TWO_CONTEXT_CLIENTS/v1" and
         doc["status"]==STATUS and doc["target"]==target and
         doc["context"]==context and doc["source"]==source and
         doc["original_minecraft"]==VERSION and
         doc["official_AF_release_JAR_SHA1"]==h12.JAR_SHA1 and
         doc["modes"]==list(MODES) and
         doc["four_cameras"]==list(b19.VIEWS) and
         doc["four_original_stages"]==list(b19.stages()) and
         doc["world_restored_from_same_pristine_snapshot_for_each_mode"] is True and
         doc["real_Fabric_clients"]==2 and doc["real_native_F2_total"]==32 and
         doc["real_server_exact_chair_state_proofs"]==32 and
         doc["real_server_exact_support_slab_proofs"]==
           (32 if target=="AF123_5" else 0) and
         doc["original_45_element_role_material_semantic_approvals"]==0 and
         doc["GPU_face_UV_exclusive_pixel_approvals"]==0 and
         doc["third_party_training_or_redistribution_approvals"]==0,
         "official original two-client source intervention control invalid")
    overrides=doc["original_child_only_interventions"]
    need(set(overrides)==set(MODES) and doc["real_client_manifests"]==
         {m:m+"/manifest.json" for m in MODES},
         "required two independent original client manifests missing")
    pin=b20.PIN[target]
    for mode in MODES:
        o=overrides[mode]
        need(o["target"]==target and o["context"]==context and o["mode"]==mode
             and o["all_original_parent_elements"]==10
             and o["all_original_parent_faces"]==46
             and o["selected_original_element_indices"]==list(choose(context,mode))
             and o["original_source5_from"]==pin["from"]
             and o["original_source5_to"]==pin["to"]
             and o["original_parent_git_blob"]==pin["parent_blob"]
             and o["original_child_git_blob"]==pin["child_blob"]
             and o["faces_uv_textures_coordinates_identical_to_original_parent"] is True
             and o["selected_element_order_maintained"] is True
             and o["original_child_parent_and_textures_identical"] is True
             and o["changed_uncompressed_JAR_members"]==[pin["child"]]
             and o["original_or_patched_JAR_distributed"] is False,
             "original source5 only and unchanged other elements not established")
    scenes={};logs={};pngs={}
    for mode in MODES:
        scenes[mode],logs[mode],pngs[mode]=b20.frames_and_proofs(
            folder,mode,source,target)
    results=compare_frames(scenes)
    verdict=decide(results)
    out={
        "schema":"MCFR_INT5_B23_SOURCE5_ORIGINAL_FIVE_CONTEXT_BATCH_AUDIT/v1",
        "target":target,"source_key":source["source_key"],
        "context":context,"context_original_indices":list(CONTEXTS[context]),
        "status":verdict,"original_Fabric_release_JAR_SHA1":h12.JAR_SHA1,
        "real_Fabric_clients":2,"new_F2_sha256_verified":32,
        "client_log_sha256_verified":2,"real_original_server_chair_states":32,
        "real_original_server_support_states":32 if target=="AF123_5" else 0,
        "source_child_only_proofs":overrides,
        "original_real_F2_SHA256":pngs,"real_client_log_SHA256":logs,
        "original_four_camera_source5_addition_metrics":results,
        "B19_full_10_original_elements_source5_removal_status_unchanged":True,
        "B19_43_of_45_bounded_source_removals_unchanged":True,
        "role_function_material_style_approved_45":0,
        "original_face_UV_exclusive_GPU_pixel_owner_approved":0,
        "third_party_training_or_redistribution_rights_approved":0,
        "H03":"HOLD","H05":"CONDITIONAL","F70_unconditional_approved":0,
        "note":"Context isolates only screen contribution of original source5 relative to exact same original additional parent element set. Cannot alone identify physical role, material or unique renderer occlusion cause.",
    }
    (folder/AUDIT).write_text(
        json.dumps(out,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target",required=True,choices=TARGETS)
    p.add_argument("--context",required=True,choices=CONTEXTS)
    p.add_argument("--directory",required=True,type=Path)
    v=p.parse_args()
    result=audit(v.directory,v.target,v.context)
    print(json.dumps({"target":v.target,"context":v.context,"decision":result["status"],
                      "real_original_f2_pixels":result["original_four_camera_source5_addition_metrics"]},
                     ensure_ascii=False,sort_keys=True))
    if result["status"].startswith("CONDITIONAL"):
        raise SystemExit(1)

if __name__=="__main__":
    main()
