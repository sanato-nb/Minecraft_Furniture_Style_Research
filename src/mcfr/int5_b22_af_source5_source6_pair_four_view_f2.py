"""INT-5-B22: pair-vs-single original AF source5+source6 native Fabric F2.

Use three actually separate official Fabric 1.21.1 game clients per target:
original source5 ONLY, original source6 ONLY, original source5+6 PAIR.
All source faces/UV/texture data remain verbatim. For each original target,
the only mod JAR member temporarily replaced is the selected child model.
Four original cardinal cameras x 4 original/negative/A-A/empty stages.

The goal is pair-level overlap/suppression evidence, NOT GPU face ownership,
original defect diagnosis, physical/material/style semantics or training rights.
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
from . import int5_b21_af_source5_isolation_four_view_f2 as b21
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15

VERSION="1.21.1"
TARGETS=b21.TARGETS
MODES=("original_5","positive_6","pair_5_6")
MANIFEST="INT5_B22_AF5_AF6_PAIR_REAL_FABRIC_SESSION_MANIFEST_V1.json"
AUDIT="INT5_B22_AF5_AF6_PAIR_FOUR_VIEW_INDEPENDENT_F2_AUDIT_V1.json"

def need(ok,why):
    if not ok:
        raise ValueError("INT5-B22: "+why)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def set_target(target):
    b21.set_target(target)

def source_identity(target):
    return b21.source_identity(target)

def pair_child(child_bytes,parent_bytes,target):
    """Copy exactly source parent elements index5,index6; no other mutation."""
    need(target in TARGETS,"only two B21 original source5 unresolved cases")
    pin=b20.PIN[target]
    child=json.loads(child_bytes.decode("utf-8-sig"))
    parent=json.loads(parent_bytes.decode("utf-8-sig"))
    source=parent.get("elements")
    need(isinstance(child,dict) and "elements" not in child
         and isinstance(source,list) and len(source)==10
         and sum(len(e["faces"]) for e in source)==46
         and child.get("parent") ==
            ("another_furniture:block/template/chair" if target=="AF121_5"
             else "another_furniture:block/template/chair_tucked"),
         "original source child or 10 parent elements / 46 faces drift")
    five,six=source[5],source[6]
    need(five["from"]==pin["from"] and five["to"]==pin["to"]
         and five["from"][0]>five["to"][0] and len(five["faces"])==4
         and len(six["faces"])==4
         and six["from"][0]<six["to"][0],
         "parent original source5/source6 orientation or four faces changed")
    # Individual elements and their faces may not be normalized or reauthored.
    result=dict(child)
    result["elements"]=[copy.deepcopy(five),copy.deepcopy(six)]
    need(result["elements"][0]==five and result["elements"][1]==six
         and all(result[k]==v for k,v in child.items())
         and len(result["elements"])==2
         and sum(len(e["faces"]) for e in result["elements"])==8,
         "two independent original source elements or child metadata drift")
    payload=json.dumps(result,ensure_ascii=False,separators=(",",":")).encode()
    meta={
        "target":target,"mode":"pair_5_6",
        "selected_original_source_elements":[5,6],
        "source_element5_original_from":list(five["from"]),
        "source_element5_original_to":list(five["to"]),
        "source_element6_original_from":list(six["from"]),
        "source_element6_original_to":list(six["to"]),
        "result_element_count":2,"result_face_count":8,
        "original_parent_git_blob":pin["parent_blob"],
        "original_child_git_blob":pin["child_blob"],
        "all_faces_textures_UV_copied_verbatim":True,
        "all_other_original_source_elements_excluded":True,
        "child_parent_and_texture_properties_unchanged":True,
    }
    return payload,meta

def install_pair_child(file,official,target):
    need(hashlib.sha1(official).hexdigest()==h12.JAR_SHA1,
         "input must be the official pinned 4.0.2 Fabric release")
    pin=b20.PIN[target]
    with ZipFile(io.BytesIO(official)) as z:
        infos=z.infolist()
        need(z.testzip() is None and len(infos)==len({i.filename for i in infos}),
             "official ZIP CRC or duplicate source member")
        original={i.filename:z.read(i.filename) for i in infos}
    patched,meta=pair_child(original[pin["child"]],original[pin["parent"]],
                            target)
    disposable=file.with_suffix(".b22-disposable")
    with ZipFile(disposable,"w") as z:
        for info in infos:
            z.writestr(info,patched if info.filename==pin["child"]
                       else original[info.filename])
    with ZipFile(disposable) as z:
        need(z.testzip() is None and z.namelist()==list(original),
             "disposable source ZIP drift")
        need([name for name in original if z.read(name)!=original[name]]==
             [pin["child"]],"only exact original child model may be changed")
        need(z.read(pin["parent"])==original[pin["parent"]],
             "shared official parent must never be patched")
        verified=json.loads(z.read(pin["child"]))
        need(verified["elements"]==
             json.loads(patched)["elements"] and
             verified["elements"][0]["from"]==pin["from"] and
             len(verified["elements"])==2,
             "pair source elements reread failed")
    replaced_hash=hashlib.sha1(disposable.read_bytes()).hexdigest()
    disposable.replace(file)
    need(hashlib.sha1(file.read_bytes()).hexdigest()==replaced_hash
         and replaced_hash!=h12.JAR_SHA1,
         "independent original-child-only patch was not installed")
    return {**meta,"official_release_jar_sha1":h12.JAR_SHA1,
            "disposable_jar_sha1_only_local":replaced_hash,
            "changed_uncompressed_jar_members":[pin["child"]],
            "original_or_modified_mod_jar_distributed":False}

def capture(command,env,game,out,version,target):
    need(version==VERSION and target in TARGETS,
         "only original AF 1.21.1 two-target case is in B22 scope")
    set_target(target)
    source=source_identity(target)
    file,official=b21.pin_official_jar(game,target)
    checked=b19.preflight(game)
    game,out=Path(game),Path(out)
    out.mkdir(parents=True,exist_ok=False)
    worlds=[p for p in (game/"saves").iterdir()
            if p.is_dir() and (p/"level.dat").is_file()]
    need(len(worlds)==1,"exactly one official original generated world")
    world=worlds[0]
    snapshot=game/"int5-b22-pristine-world"
    need(not snapshot.exists(),"world snapshot already exists")
    shutil.copytree(world,snapshot,ignore=shutil.ignore_patterns("session.lock"))
    meta={}
    sessions={}
    try:
        for mode in MODES:
            shutil.rmtree(world)
            shutil.copytree(snapshot,world,
                            ignore=shutil.ignore_patterns("session.lock"))
            if mode=="pair_5_6":
                meta[mode]=install_pair_child(file,official,target)
            else:
                meta[mode]=b21.install_case(file,official,target,mode)
                need(meta[mode]["selected_original_element_index"]==
                     (5 if mode=="original_5" else 6)
                     and meta[mode]["result_element_count"]==1
                     and meta[mode]["result_face_count"]==4,
                     "original B21 single-element positive/source5 scope drift")
            sessions[mode]=b19.capture_session(
                command,env,game,out/mode,mode,checked)
            need(sessions[mode]["new_real_native_F2"]==16,
                 "each of three independent official clients must provide 16 F2")
        doc={
            "schema":"MCFR_INT5_B22_PAIR5_6_THREE_REAL_FABRIC_CLIENTS/v1",
            "status":"B22_THREE_REAL_SOURCE5_SOURCE6_PAIR_NATIVE_F2_PENDING_INDEPENDENT_AUDIT",
            "target":target,"source":source,
            "original_minecraft_version":VERSION,
            "official_release_jar_sha1":h12.JAR_SHA1,
            "sessions":list(MODES),"four_cardinal_cameras":list(b19.VIEWS),
            "four_exact_stages":list(b19.stages()),
            "pristine_original_world_restored_for_each_session":True,
            "real_native_F2_total":48,"real_game_client_sessions":3,
            "real_server_exact_chair_checks":48,
            "real_server_additional_support_checks":48 if target=="AF123_5" else 0,
            "single_child_only_disposable_source_variants":meta,
            "individual_real_client_manifests":{
                x:x+"/manifest.json" for x in MODES},
            "physical_furniture_function_material_style_verified":False,
            "unique_GPU_original_face_UV_pixel_ownership_verified":False,
            "third_party_training_and_redistribution_rights_approved":False,
        }
        (out/MANIFEST).write_text(
            json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
            encoding="utf-8")
        return doc
    finally:
        if file.is_file():
            file.write_bytes(official)
        if snapshot.exists():
            shutil.rmtree(snapshot)

def compare_three(sessions):
    need(set(sessions)==set(MODES),"three original target source scenes required")
    before,negative,after,empty=b19.stages()
    results={}
    for view in b19.VIEWS:
        five=sessions["original_5"][view]
        six=sessions["positive_6"][view]
        pair=sessions["pair_5_6"][view]
        result={
            "original5_vs_original6_before_pixels":
                len(h15.pixel_changes(five[before],six[before])),
            "original5_vs_original6_after_pixels":
                len(h15.pixel_changes(five[after],six[after])),
            "pair5_6_vs_original6_before_pixels":
                len(h15.pixel_changes(pair[before],six[before])),
            "pair5_6_vs_original6_after_pixels":
                len(h15.pixel_changes(pair[after],six[after])),
            "pair5_6_vs_original5_before_pixels":
                len(h15.pixel_changes(pair[before],five[before])),
            "pair5_6_vs_original5_after_pixels":
                len(h15.pixel_changes(pair[after],five[after])),
            "original5_only_foreground_pixels":
                len(h15.pixel_changes(five[before],five[empty if
                    b19.CHOSEN=="AF121_5" else negative])),
            "original6_only_foreground_pixels":
                len(h15.pixel_changes(six[before],six[empty if
                    b19.CHOSEN=="AF121_5" else negative])),
            "pair5_6_foreground_pixels":
                len(h15.pixel_changes(pair[before],pair[empty if
                    b19.CHOSEN=="AF121_5" else negative])),
            "negative_other_model_pixels":
                {mode:len(h15.pixel_changes(sessions[mode][view][negative],
                                             pair[negative]))
                 for mode in MODES},
            "negative_air_or_slab_pixels":
                {mode:len(h15.pixel_changes(sessions[mode][view][empty],
                                             pair[empty]))
                 for mode in MODES},
            "same_client_before_after_temporal_pixels":
                {mode:len(h15.pixel_changes(sessions[mode][view][before],
                                             sessions[mode][view][after]))
                 for mode in MODES},
            "identical_pair_and_original6_full_RGB_original_F2":
                (pair[before].tobytes()==six[before].tobytes()),
            "identical_pair_and_original6_full_RGB_after_F2":
                (pair[after].tobytes()==six[after].tobytes()),
        }
        results[view]=result
    return results

def decision(metrics):
    need(set(metrics)==set(b19.VIEWS),"all four camera source masks required")
    controls=all(
        m["original5_vs_original6_before_pixels"]==
        m["original5_vs_original6_after_pixels"] and
        m["pair5_6_vs_original6_before_pixels"]==
        m["pair5_6_vs_original6_after_pixels"] and
        m["pair5_6_vs_original5_before_pixels"]==
        m["pair5_6_vs_original5_after_pixels"] and
        all(v==0 for v in m["negative_other_model_pixels"].values()) and
        all(v==0 for v in m["negative_air_or_slab_pixels"].values()) and
        all(v==0 for v in m["same_client_before_after_temporal_pixels"].values())
        for m in metrics.values())
    if not controls:
        return "CONDITIONAL_B22_NEGATIVE_OR_TEMPORAL_CONTROLS_UNSTABLE"
    original5_visible=any(m["original5_only_foreground_pixels"]>0
                          for m in metrics.values())
    positive6_visible=any(m["original6_only_foreground_pixels"]>0
                          for m in metrics.values())
    five6different=any(m["original5_vs_original6_before_pixels"]>0
                       for m in metrics.values())
    if not (original5_visible and positive6_visible and five6different):
        return "CONDITIONAL_B22_ORIGINAL5_OR_POSITIVE6_SINGLE_CONTROL_INVALID"
    if all(m["pair5_6_vs_original6_before_pixels"]==0
           for m in metrics.values()):
        return "PASS_PAIR5_6_MATCHES_ORIGINAL6_ONLY_AT_FOUR_CARDINAL_VIEWS"
    return "PASS_PAIR5_6_HAS_ADDITIONAL_RENDER_PIXELS_OVER_ORIGINAL6_ONLY"

def audit(folder,target):
    set_target(target)
    folder=Path(folder)
    doc=json.loads((folder/MANIFEST).read_text(encoding="utf-8"))
    source=source_identity(target)
    need(doc["schema"]=="MCFR_INT5_B22_PAIR5_6_THREE_REAL_FABRIC_CLIENTS/v1"
         and doc["status"]=="B22_THREE_REAL_SOURCE5_SOURCE6_PAIR_NATIVE_F2_PENDING_INDEPENDENT_AUDIT"
         and doc["target"]==target and doc["source"]==source
         and doc["original_minecraft_version"]==VERSION
         and doc["official_release_jar_sha1"]==h12.JAR_SHA1
         and doc["sessions"]==list(MODES)
         and doc["four_cardinal_cameras"]==list(b19.VIEWS)
         and doc["four_exact_stages"]==list(b19.stages())
         and doc["pristine_original_world_restored_for_each_session"] is True
         and doc["real_native_F2_total"]==48
         and doc["real_game_client_sessions"]==3
         and doc["real_server_exact_chair_checks"]==48
         and doc["real_server_additional_support_checks"]==
             (48 if target=="AF123_5" else 0),
         "original three-client world or 48 F2/real-server contract drift")
    variants=doc["single_child_only_disposable_source_variants"]
    need(set(variants)==set(MODES) and
         doc["individual_real_client_manifests"]==
             {x:x+"/manifest.json" for x in MODES},
         "source5, source6, pair source proof missing")
    pin=b20.PIN[target]
    pair=variants["pair_5_6"]
    need(pair["mode"]=="pair_5_6"
         and pair["target"]==target
         and pair["selected_original_source_elements"]==[5,6]
         and pair["source_element5_original_from"]==pin["from"]
         and pair["source_element5_original_to"]==pin["to"]
         and pair["result_element_count"]==2
         and pair["result_face_count"]==8
         and pair["original_parent_git_blob"]==pin["parent_blob"]
         and pair["original_child_git_blob"]==pin["child_blob"]
         and pair["all_faces_textures_UV_copied_verbatim"] is True
         and pair["all_other_original_source_elements_excluded"] is True
         and pair["child_parent_and_texture_properties_unchanged"] is True
         and pair["changed_uncompressed_jar_members"]==[pin["child"]]
         and pair["original_or_modified_mod_jar_distributed"] is False,
         "exact original parent two-element source membership not proven")
    for mode,index in (("original_5",5),("positive_6",6)):
        item=variants[mode]
        need(item["target"]==target and item["mode"]==mode
             and item["selected_original_element_index"]==index
             and item["result_element_count"]==1
             and item["result_face_count"]==4
             and item["original_parent_git_blob"]==pin["parent_blob"]
             and item["original_child_git_blob"]==pin["child_blob"]
             and item["original_JAR_or_modified_JAR_distributed"] is False,
             "B21 original exact one-element single-game control drift")
    scenes,logs,pngs={},{},{}
    for mode in MODES:
        scenes[mode],logs[mode],pngs[mode]=b20.frames_and_proofs(
            folder,mode,source,target)
    metrics=compare_three(scenes)
    result=decision(metrics)
    audit_data={
        "schema":"MCFR_INT5_B22_EXACT_SOURCE5_SOURCE6_PAIR_3GAME_REAL_F2_AUDIT/v1",
        "target":target,"original_source_key":source["source_key"],
        "Minecraft_version":VERSION,"official_original_release_JAR_sha1":h12.JAR_SHA1,
        "original_real_game_clients":3,"real_F2_PNG_SHA256_verified":48,
        "game_client_logs_SHA256_verified":3,"real_exact_chair_state_proofs":48,
        "real_exact_extra_top_slab_proofs":48 if target=="AF123_5" else 0,
        "source_child_variants":variants,"PNG_hashes":pngs,"log_sha256":logs,
        "actual_four_camera_pair_and_single_source_RGB_metrics":metrics,
        "decision":result,
        "original_B19_source5_unobserved_4_camera_removal_kept":True,
        "B21_source5_solo_positive_and_x_normalization_research_kept":True,
        "B19_cumulative_bounded_render_source_removals_43_of_45_kept":True,
        "original_element5_exclusive_occlusion_or_root_cause_proven":False,
        "individual_original_face_UV_exclusive_GPU_pixel_ownership_proven":False,
        "physical_function_material_style_approved":False,
        "third_party_training_redistribution_rights_approved":False,
        "H03":"HOLD","H05":"CONDITIONAL","F70_unconditional_approved":0,
        "caveats":[
            "Two-component pair visual response is a controlled camera- and state-bounded screen result, not exclusive original source5 face pixels.",
            "If pair matches source6 alone, source5 influence is not visible in this pair at the four original F2 cameras; this does not identify the sole GPU occlusion mechanism.",
            "Original position, face keys, original UV, source parent and other game JAR members kept exact; external rights and physical material/function not inferred.",
            "B22 cannot change B19 original full-model element5 deletion four-view 0 result or prior strict gates."
        ],
    }
    (folder/AUDIT).write_text(
        json.dumps(audit_data,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8")
    return audit_data

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target",choices=TARGETS,required=True)
    parser.add_argument("--directory",type=Path,required=True)
    args=parser.parse_args()
    result=audit(args.directory,args.target)
    print(json.dumps({"target":result["target"],"decision":result["decision"],
                      "four_view_metrics":result["actual_four_camera_pair_and_single_source_RGB_metrics"]},
                     sort_keys=True,ensure_ascii=False))
    if result["decision"].startswith("CONDITIONAL"):
        raise SystemExit(1)

if __name__=="__main__":
    main()
