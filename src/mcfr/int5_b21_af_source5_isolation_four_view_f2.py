"""INT-5-B21: original AF source element5 isolation vs element6 visibility control.

Four independent real Fabric 1.21.1 clients for each unresolved B19/B20 target:
  no_faces_5 (one inherited original element5 with no faces, NOT elements=[]),
  original_5 (sole original 4-face element5),
  normalized_5 (sole original element5, only X endpoints exchanged),
  positive_6 (sole original element6, whose removal had B15/B16 response).
All four are child-model-only disposable variants from the same pinned official
4.0.2 JAR, with an identical pristine world and south/north/east/west cameras.
F2, logs, original server states and CRC/SHA independently audited. No assets
or disposable release JAR committed/uploaded. No semantic/rights promotion.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
from pathlib import Path
import shutil
from zipfile import ZipFile

from . import int5_b19_four_unresolved_four_view_f2 as b19
from . import int5_b20_af_reversed_x_three_session_f2 as b20
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15

VERSION = "1.21.1"
TARGETS = b20.TARGETS
MODES = ("no_faces_5", "original_5", "normalized_5", "positive_6")
MANIFEST = "INT5_B21_SOURCE5_ISOLATION_FOUR_FABRIC_SESSION_MANIFEST_V1.json"
AUDIT = "INT5_B21_SOURCE5_ISOLATION_INDEPENDENT_F2_AUDIT_V1.json"

def need(ok, msg):
    if not ok:
        raise ValueError("INT5-B21: " + msg)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def set_target(target):
    need(target in TARGETS, "B21 only targets two B19/B20 unresolved AF source5")
    b19.set_target(target)

def source_identity(target):
    return b20.source_identity(target)

def patch_child(child_bytes, parent_bytes, target, mode):
    """One-element child override. Never use elements=[] (can inherit parent)."""
    need(target in TARGETS and mode in MODES, "invalid original target or intervention")
    pin = b20.PIN[target]
    original_child = json.loads(child_bytes.decode("utf-8-sig"))
    parent = json.loads(parent_bytes.decode("utf-8-sig"))
    elements = parent.get("elements")
    need(isinstance(original_child, dict) and "elements" not in original_child
         and original_child.get("parent") ==
         ("another_furniture:block/template/chair"
          if target == "AF121_5" else "another_furniture:block/template/chair_tucked")
         and isinstance(elements, list) and len(elements) == 10
         and sum(len(x["faces"]) for x in elements) == 46,
         "official original child inheritance or 10 original elements / 46 faces drift")
    old5 = elements[5]
    old6 = elements[6]
    need(old5["from"] == pin["from"] and old5["to"] == pin["to"]
         and len(old5["faces"]) == 4 and old5["from"][0] > old5["to"][0]
         and len(old6["faces"]) == 4,
         "exact two original source5/source6 elements or face identities changed")

    selected_index = 6 if mode == "positive_6" else 5
    selected = copy.deepcopy(elements[selected_index])
    if mode == "no_faces_5":
        selected["faces"] = {}
    elif mode == "normalized_5":
        selected["from"][0], selected["to"][0] = (
            old5["to"][0], old5["from"][0])
    need(len(selected["faces"]) == (0 if mode == "no_faces_5" else 4),
         "unexpected isolated source face count")
    if mode in ("original_5", "no_faces_5"):
        need(selected["from"] == old5["from"] and
             selected["to"] == old5["to"], "original source5 coordinates not preserved")
    if mode == "normalized_5":
        need(selected["from"] == [old5["to"][0], *old5["from"][1:]]
             and selected["to"] == [old5["from"][0], *old5["to"][1:]]
             and selected["faces"] == old5["faces"],
             "normalized isolated source5 changed non-X coordinates or source faces")
    if mode == "positive_6":
        need(selected == old6,
             "positive control must preserve original source6 verbatim")
    if mode == "no_faces_5":
        need({k:v for k,v in selected.items() if k != "faces"} ==
             {k:v for k,v in old5.items() if k != "faces"},
             "no-face control changed source5 beyond face declarations")
    new_child = dict(original_child)
    new_child["elements"] = [selected]
    need(len(new_child["elements"]) == 1 and
         {k:v for k,v in new_child.items() if k != "elements"} == original_child,
         "child-only original texture/parent/properties changed")
    payload = json.dumps(new_child, ensure_ascii=False, separators=(",",":")).encode()
    meta = {
        "target":target, "mode":mode,
        "original_child_git_blob":pin["child_blob"],
        "original_parent_git_blob":pin["parent_blob"],
        "original_element5_index":5, "original_element6_index":6,
        "original_element5_from":list(old5["from"]),
        "original_element5_to":list(old5["to"]),
        "selected_original_element_index":selected_index,
        "original_source5_face_count":len(old5["faces"]),
        "result_element_count":1, "result_face_count":len(selected["faces"]),
        "result_from":list(selected["from"]), "result_to":list(selected["to"]),
        "unselected_original_elements_removed":9,
        "all_result_face_objects_from_original_source": mode != "no_faces_5",
        "parent_and_texture_bindings_unchanged":True,
        "no_empty_elements_array_inheritance_fallback":True,
    }
    return payload,meta

def pin_official_jar(game, target):
    # Includes original JAR SHA1, ZIP CRC, both original Git blob pins,
    # child/parent model identity, and two B20 one-child flattening proofs.
    return b20.pin_official_jar(game,target)

def install_case(file, official, target, mode):
    need(mode in MODES and hashlib.sha1(official).hexdigest() == h12.JAR_SHA1,
         "B21 must start every intervention from exact official release bytes")
    pin = b20.PIN[target]
    with ZipFile(io.BytesIO(official)) as z:
        need(z.testzip() is None, "original mod ZIP CRC failed")
        infos = z.infolist()
        originals = {i.filename:z.read(i.filename) for i in infos}
    new_child,scope = patch_child(originals[pin["child"]],
                                  originals[pin["parent"]],target,mode)
    disposable=file.with_suffix(".b21-disposable")
    with ZipFile(disposable,"w") as z:
        for info in infos:
            z.writestr(info, new_child if info.filename == pin["child"]
                       else originals[info.filename])
    with ZipFile(disposable) as z:
        names = z.namelist()
        need(z.testzip() is None and names == list(originals)
             and [x for x in names if z.read(x) != originals[x]] == [pin["child"]],
             "only one original JAR child model member may change")
        decoded = json.loads(z.read(pin["child"]))
        need(len(decoded["elements"]) == 1
             and len(decoded["elements"][0]["faces"]) == scope["result_face_count"]
             and decoded["elements"][0]["from"] == scope["result_from"]
             and decoded["elements"][0]["to"] == scope["result_to"]
             and z.read(pin["parent"]) == originals[pin["parent"]],
             "reread of exact one-element child or parent control failed")
    disposable_sha1 = hashlib.sha1(disposable.read_bytes()).hexdigest()
    disposable.replace(file)
    need(disposable_sha1 == hashlib.sha1(file.read_bytes()).hexdigest()
         and disposable_sha1 != h12.JAR_SHA1,
         "disposable child-model variant was not installed")
    return {
        **scope,
        "official_release_JAR_sha1":h12.JAR_SHA1,
        "disposable_JAR_sha1_only_local":disposable_sha1,
        "changed_uncompressed_JAR_members":[pin["child"]],
        "original_JAR_or_modified_JAR_distributed":False,
    }

def capture(command, env, game, out, version, target):
    need(version == VERSION and target in TARGETS,
         "only AF 1.21.1 source5 B21 original isolation supported")
    set_target(target)
    source = source_identity(target)
    file,official = pin_official_jar(game,target)
    checked = b19.preflight(game)
    game,out = Path(game),Path(out)
    out.mkdir(parents=True,exist_ok=False)
    worlds = [p for p in (game/"saves").iterdir()
              if p.is_dir() and (p/"level.dat").is_file()]
    need(len(worlds) == 1, "exactly one original pinned creative world required")
    world = worlds[0]
    snapshot = game/"int5-b21-pristine-world"
    need(not snapshot.exists(), "pristine world snapshot already exists")
    shutil.copytree(world,snapshot,ignore=shutil.ignore_patterns("session.lock"))
    case_meta = {}
    try:
        for mode in MODES:
            # All four sessions restore the same world and the original official
            # JAR before installing the single-child-only case.
            shutil.rmtree(world)
            shutil.copytree(snapshot,world,
                            ignore=shutil.ignore_patterns("session.lock"))
            case_meta[mode] = install_case(file,official,target,mode)
            manifest = b19.capture_session(
                command,env,game,out/mode,mode,checked)
            need(manifest["new_real_native_F2"] == 16,
                 "every real Fabric client must produce sixteen native F2 PNG")
        doc = {
            "schema":"MCFR_INT5_B21_FOUR_INDEPENDENT_REAL_FABRIC_CLIENTS/v1",
            "status":"REAL_NATIVE_F2_CAPTURED_PENDING_INDEPENDENT_AUDIT",
            "target":target, "source":source, "real_minecraft":VERSION,
            "official_release_JAR_sha1":h12.JAR_SHA1,
            "sessions":list(MODES),"four_cameras":list(b19.VIEWS),
            "stages":list(b19.stages()),
            "world_restored_from_same_original_snapshot_all_four_sessions":True,
            "native_F2_total":64,"real_server_chair_proofs":64,
            "real_server_support_proofs":64 if target == "AF123_5" else 0,
            "original_child_only_interventions":case_meta,
            "native_F2_manifests":{m:m+"/manifest.json" for m in MODES},
            "source_element_function_material_style_approved":False,
            "exclusive_original_face_UV_GPU_pixel_ownership_approved":False,
            "third_party_AI_training_and_redistribution_rights_approved":False,
        }
        (out/MANIFEST).write_text(
            json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
            encoding="utf-8")
        return doc
    finally:
        if snapshot.exists():
            shutil.rmtree(snapshot)

def metrics_for_views(sessions):
    need(set(sessions) == set(MODES), "original four model variants required")
    a,control,b,air = b19.stages()
    result = {}
    for view in b19.VIEWS:
        blank = sessions["no_faces_5"][view]
        obs={}
        for mode in MODES:
            frames=sessions[mode][view]
            original = h15.pixel_changes(frames[a],blank[a])
            repeated = h15.pixel_changes(frames[b],blank[b])
            ctrl = h15.pixel_changes(frames[control],blank[control])
            environment = h15.pixel_changes(frames[air],blank[air])
            own_a_a = h15.pixel_changes(frames[a],frames[b])
            obs[mode]={
                "isolation_before_changed_pixels":len(original),
                "isolation_after_changed_pixels":len(repeated),
                "same_source_change_position_repeated":original == repeated,
                "unchanged_other_model_negative_pixels":len(ctrl),
                "unchanged_air_and_support_pixels":len(environment),
                "same_session_A_A_temporal_pixels":len(own_a_a),
            }
        result[view]=obs
    return result

def decision(metrics):
    control_ok=all(
        all(m["isolation_before_changed_pixels"] ==
            m["isolation_after_changed_pixels"] and
            m["same_source_change_position_repeated"] is True and
            m["unchanged_other_model_negative_pixels"] == 0 and
            m["unchanged_air_and_support_pixels"] == 0 and
            m["same_session_A_A_temporal_pixels"] == 0
            for m in metrics[v].values())
        and metrics[v]["no_faces_5"]["isolation_before_changed_pixels"] == 0
        for v in b19.VIEWS)
    if not control_ok:
        return "CONDITIONAL_FAILED_TEMPORAL_OR_NEGATIVE_F2_CONTROLS"
    positive=any(metrics[v]["positive_6"]["isolation_before_changed_pixels"]>0
                 for v in b19.VIEWS)
    if not positive:
        return "CONDITIONAL_FAILED_POSITIVE6_VISIBLE_MODEL_CONTROL"
    original=any(metrics[v]["original_5"]["isolation_before_changed_pixels"]>0
                 for v in b19.VIEWS)
    normalized=any(metrics[v]["normalized_5"]["isolation_before_changed_pixels"]>0
                   for v in b19.VIEWS)
    if original:
        return "VISIBLE_ORIGINAL_SOURCE5_ONLY_NOT_VISIBLE_IN_FULL_MODEL"
    if normalized:
        return "ONLY_NORMALIZED_SOURCE5_VISIBLE_IN_ISOLATION"
    return "ORIGINAL_AND_NORMALIZED_SOURCE5_NOT_VISIBLE_EVEN_ISOLATED"

def audit(folder,target):
    set_target(target)
    folder=Path(folder)
    doc=json.loads((folder/MANIFEST).read_text(encoding="utf-8"))
    source=source_identity(target)
    need(doc["schema"]=="MCFR_INT5_B21_FOUR_INDEPENDENT_REAL_FABRIC_CLIENTS/v1"
         and doc["status"]=="REAL_NATIVE_F2_CAPTURED_PENDING_INDEPENDENT_AUDIT"
         and doc["source"]==source and doc["target"]==target
         and doc["real_minecraft"]==VERSION
         and doc["official_release_JAR_sha1"]==h12.JAR_SHA1
         and doc["sessions"]==list(MODES)
         and doc["four_cameras"]==list(b19.VIEWS)
         and doc["stages"]==list(b19.stages())
         and doc["world_restored_from_same_original_snapshot_all_four_sessions"] is True
         and doc["native_F2_total"]==64 and
         doc["real_server_chair_proofs"]==64 and
         doc["real_server_support_proofs"]==(64 if target=="AF123_5" else 0),
         "original pinned four-session experiment or exact game proof drift")
    variants=doc["original_child_only_interventions"]
    need(set(variants)==set(MODES) and
         doc["native_F2_manifests"]=={m:m+"/manifest.json" for m in MODES},
         "four distinct original-source isolated models missing")
    for mode in MODES:
        v=variants[mode]
        pin=b20.PIN[target]
        need(v["mode"]==mode and v["target"]==target
             and v["original_child_git_blob"]==pin["child_blob"]
             and v["original_parent_git_blob"]==pin["parent_blob"]
             and v["original_element5_from"]==pin["from"]
             and v["original_element5_to"]==pin["to"]
             and v["original_element5_index"]==5
             and v["original_element6_index"]==6
             and v["selected_original_element_index"]==(6 if mode=="positive_6" else 5)
             and v["result_element_count"]==1
             and v["result_face_count"]==(0 if mode=="no_faces_5" else 4)
             and v["unselected_original_elements_removed"]==9
             and v["all_result_face_objects_from_original_source"]==(mode!="no_faces_5")
             and v["parent_and_texture_bindings_unchanged"] is True
             and v["no_empty_elements_array_inheritance_fallback"] is True
             and v["original_JAR_or_modified_JAR_distributed"] is False
             and v["changed_uncompressed_JAR_members"]==[pin["child"]]
             and v["official_release_JAR_sha1"]==h12.JAR_SHA1,
             "per-model original source/face/child provenance missing")
    sessions,logs,pngs={},{},{}
    for mode in MODES:
        sessions[mode],logs[mode],pngs[mode]=b20.frames_and_proofs(
            folder,mode,source,target)
    metrics=metrics_for_views(sessions)
    status=decision(metrics)
    result={
        "schema":"MCFR_INT5_B21_ORIGINAL_SOURCE5_ISOLATION_REAL_F2_AUDIT/v1",
        "target":target,"source_key":source["source_key"],
        "official_release_JAR_sha1":h12.JAR_SHA1,
        "real_Fabric_version":VERSION,"real_game_sessions":4,
        "native_F2_SHA256_verified":64,"client_log_SHA256_verified":4,
        "real_server_chair_proofs":64,
        "real_server_support_slab_proofs":64 if target=="AF123_5" else 0,
        "source_child_only_variant_pins":variants,
        "actual_native_F2_sha256":pngs,"actual_client_log_sha256":logs,
        "four_camera_isolated_model_metrics":metrics,
        "result":status,
        "original_element5_root_cause_exclusively_proven":False,
        "source5_function_material_style_approved":False,
        "source5_exclusive_original_face_UV_GPU_pixel_ownership_approved":False,
        "third_party_AI_training_and_redistribution_rights_approved":False,
        "B19_source_removal_four_view_no_visible_preserved":True,
        "B20_source5_X_endpoint_full_model_no_visible_preserved":True,
        "B19_43_of_45_bounded_render_response_unchanged":True,
        "H03":"HOLD","H05":"CONDITIONAL","F70_unconditional_approved":0,
        "limitations":[
            "A positive isolated element5 against faceless control plus B19 whole-chair 0 pixels supports model-context hiding/overlap, not exclusive occlusion.",
            "A no-response isolated element5 with positive source6 is a bounded real-screen observation; geometry/face orientation/baking remains unresolved.",
            "Do not use an empty elements array as an empty inherited model: it can fall back to parent elements.",
            "Changing only X endpoints cannot prove the official mod source has a defect.",
            "No unique per-face GPU pixel attribution, physical seat/back function, original material/style or third-party rights approved.",
        ]
    }
    (folder/AUDIT).write_text(json.dumps(result,ensure_ascii=False,
                                        sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target",choices=TARGETS,required=True)
    p.add_argument("--directory",type=Path,required=True)
    a=p.parse_args()
    result=audit(a.directory,a.target)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    if result["result"].startswith("CONDITIONAL_FAILED"):
        raise SystemExit(1)

if __name__=="__main__":
    main()
