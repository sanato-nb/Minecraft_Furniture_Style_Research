"""INT-5-B20: 2 reversed-X AF source5 elements, original/flatten/normalized F2.

Three actual separate Fabric 1.21.1 game sessions per original target:
official inherited child, same original elements flattened into that child,
then ONLY source element 5's reversed X endpoints normalized in the child.
The flattening control is essential: changing inheritance representation
must not be mistaken for a geometric cause.
No original mod assets or patched JAR are included in Git/artifacts.
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
from . import int5_b16_af121_six_element_batch_f2 as af1
from . import int5_b15_af123_six_element_batch_f2 as af10
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15

VERSION="1.21.1"
TARGETS=("AF121_5","AF123_5")
MANIFEST="INT5_B20_THREE_REAL_FABRIC_SESSION_MANIFEST_V1.json"
AUDIT="INT5_B20_AF_REVERSED_X_FOUR_VIEW_INDEPENDENT_AUDIT_V1.json"
PIN={
    "AF121_5":{
        "child":af1.CHILD,"parent":af1.PARENT,
        "child_blob":"2261460299d13a15220f4fecfe059628ac28e813",
        "parent_blob":"31c643617a7178ac5113702e785620f4d1150adf",
        "from":[13,2,3],"to":[3,4,13],
    },
    "AF123_5":{
        "child":af10.CHILD,"parent":af10.PARENT,
        "child_blob":"71fd514e28b36b47b45cc6a38594b4d11059e6ff",
        "parent_blob":"bbfd54f73fd764015ce320082ba531bd314a6dfd",
        "from":[13,2,-6],"to":[3,4,4],
    },
}

def need(ok,why):
    if not ok:raise ValueError("INT5-B20: "+why)

def sha(data):return hashlib.sha256(data).hexdigest()
def blob(data):return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\\0"+data).hexdigest()

def set_target(target):
    need(target in TARGETS,"only two B19 stable four-view not-visible AF source5 cases")
    b19.set_target(target)

def source_identity(target):
    set_target(target)
    info=b19.source()
    need(info["source_key"] in ("AF121/AF1393/5","AF123/AF1394/5")
         and info["source_faces"]==4 and
         info["B18_prior_south_pixels"]==info["B18_prior_north_pixels"]==0,
         "B18/B19 original source5 identity or initial zero observations drift")
    return info

def patch_child(child_bytes,parent_bytes,target,mode):
    """Return pure one-child override. All non-element5 objects are identical."""
    need(target in TARGETS and mode in ("flattened","normalized"),
         "unknown model/mode")
    pins=PIN[target]
    child=json.loads(child_bytes.decode("utf-8-sig"))
    parent=json.loads(parent_bytes.decode("utf-8-sig"))
    elems=parent.get("elements")
    need(isinstance(child,dict) and child.get("parent")==
         ("another_furniture:block/template/chair" if target=="AF121_5"
          else "another_furniture:block/template/chair_tucked") and
         "elements" not in child and
         isinstance(elems,list) and len(elems)==10 and
         sum(len(x["faces"]) for x in elems)==46,
         "source child inheritance / original ten elements, 46 faces mismatch")
    original=elems[5]
    need(original["from"]==pins["from"] and original["to"]==pins["to"] and
         len(original["faces"])==4 and original["from"][0]>original["to"][0],
         "original reversed-X source element5 must be preserved before experiment")
    revised=copy.deepcopy(elems)
    if mode=="normalized":
        revised[5]["from"][0],revised[5]["to"][0]=(
            original["to"][0],original["from"][0])
    need(len(revised)==10 and
         sum(len(x["faces"]) for x in revised)==46 and
         all(revised[i]==elems[i] for i in range(10) if i!=5) and
         {k:v for k,v in revised[5].items() if k not in ("from","to")}==
         {k:v for k,v in original.items() if k not in ("from","to")} and
         revised[5]["from"][1:]==original["from"][1:] and
         revised[5]["to"][1:]==original["to"][1:],
         "source elements or face/UV/texture changed outside original X endpoints")
    if mode=="flattened":
        need(revised==elems,"flattened inheritance control changed original geometry")
    else:
        need(revised[5]["from"][0]<revised[5]["to"][0],
             "X normalization failed")
    copy_child=dict(child)
    copy_child["elements"]=revised
    need({k:v for k,v in copy_child.items() if k!="elements"}==child,
         "changed child top-level model properties")
    payload=json.dumps(copy_child,ensure_ascii=False,separators=(",",":")).encode()
    return payload,{
        "target":target,"mode":mode,"original_index":5,"source_faces":4,
        "original_from":list(original["from"]),"original_to":list(original["to"]),
        "result_from":list(revised[5]["from"]),"result_to":list(revised[5]["to"]),
        "changed_X_endpoints_only":mode=="normalized",
        "all_other_source_elements_identical":True,
        "all_faces_UV_texture_and_parent_reference_unchanged":True,
    }

def pin_official_jar(game,target):
    source_identity(target)
    b19.preflight(game)
    file=Path(game)/"mods"/af1.JAR_NAME
    original=file.read_bytes()
    need(hashlib.sha1(original).hexdigest()==h12.JAR_SHA1,
         "official Another Furniture 4.0.2 released JAR changed")
    pins=PIN[target]
    with ZipFile(io.BytesIO(original)) as z:
        names=z.namelist()
        need(z.testzip() is None and len(names)==len(set(names))
             and all(x in names for x in (pins["child"],pins["parent"])),
             "official JAR source member integrity failed")
        entries={name:z.read(name) for name in names}
    need(blob(entries[pins["child"]])==pins["child_blob"] and
         blob(entries[pins["parent"]])==pins["parent_blob"],
         "official runtime child/parent Git source pin drift")
    # Validate both pure interventions before altering a live official JAR.
    patch_child(entries[pins["child"]],entries[pins["parent"]],target,"flattened")
    patch_child(entries[pins["child"]],entries[pins["parent"]],target,"normalized")
    return file,original

def install_child_only_jar(file,official,target,mode):
    pins=PIN[target]
    need(mode in ("flattened","normalized"),"illegal comparison mode")
    need(hashlib.sha1(official).hexdigest()==h12.JAR_SHA1,
         "input is not pinned official original release")
    with ZipFile(io.BytesIO(official)) as z:
        infos=z.infolist()
        entries={i.filename:z.read(i.filename) for i in infos}
    patched,scope=patch_child(entries[pins["child"]],entries[pins["parent"]],
                              target,mode)
    output=file.with_suffix(".b20-disposable")
    with ZipFile(output,"w") as z:
        for info in infos:
            z.writestr(info,patched if info.filename==pins["child"]
                       else entries[info.filename])
    with ZipFile(output) as z:
        names=z.namelist()
        need(z.testzip() is None and names==list(entries) and
             [n for n in names if z.read(n)!=entries[n]]==[pins["child"]],
             "not exactly one changed disposable JAR member")
        need(z.read(pins["parent"])==entries[pins["parent"]],
             "source shared parent unexpectedly changed")
        reloaded=json.loads(z.read(pins["child"]))
        need(len(reloaded["elements"])==10 and
             reloaded["elements"][5]["from"]==scope["result_from"],
             "JAR reread changed original source5 target")
    new_sha=hashlib.sha1(output.read_bytes()).hexdigest()
    output.replace(file)
    need(hashlib.sha1(file.read_bytes()).hexdigest()==new_sha
         and new_sha!=h12.JAR_SHA1,
         "disposable patched JAR not installed")
    return {**scope,"official_JAR_sha1":h12.JAR_SHA1,
            "disposable_JAR_sha1_not_for_distribution":new_sha,
            "changed_uncompressed_JAR_members":[pins["child"]],
            "original_parent_git_blob":pins["parent_blob"],
            "original_child_git_blob":pins["child_blob"],
            "original_release_JAR_or_artwork_distributed":False}

def capture(command,env,game,out,version,target):
    need(version==VERSION and target in TARGETS,
         "B20 requires original AF 1.21.1 source case")
    source=source_identity(target)
    file,official=pin_official_jar(game,target)
    checked=b19.preflight(game)
    game,out=Path(game),Path(out)
    out.mkdir(parents=True,exist_ok=False)
    worlds=[p for p in (game/"saves").iterdir()
            if p.is_dir() and (p/"level.dat").is_file()]
    need(len(worlds)==1,"exactly one pinned original creative world")
    world=worlds[0]
    snapshot=game/"int5-b20-pristine-world"
    need(not snapshot.exists(),"B20 pristine world snapshot already exists")
    shutil.copytree(world,snapshot,ignore=shutil.ignore_patterns("session.lock"))
    results={}
    overrides={}
    try:
        for session in ("baseline","flattened","normalized"):
            if session!="baseline":
                shutil.rmtree(world)
                shutil.copytree(snapshot,world,
                                ignore=shutil.ignore_patterns("session.lock"))
                overrides[session]=install_child_only_jar(file,official,target,session)
            results[session]=b19.capture_session(
                command,env,game,out/session,session,checked)
        need(all(x["new_real_native_F2"]==16 for x in results.values()),
             "three independent game sessions must each provide 16 native F2")
        doc={
            "schema":"MCFR_INT5_B20_THREE_REAL_FABRIC_GAMES/v1",
            "status":"THREE_ORIGINAL_FLATTENED_NORMALIZED_REAL_F2_PENDING_INDEPENDENT_AUDIT",
            "target":target,"source":source,"version":VERSION,
            "official_release_jar_sha1":h12.JAR_SHA1,
            "sessions":["baseline","flattened","normalized"],
            "world_restored_from_same_pristine_snapshot_for_each_session":True,
            "real_native_F2_total":48,
            "exact_server_chair_state_checks":48,
            "top_slab_extra_state_checks":48 if target=="AF123_5" else 0,
            "only_child_one_member_changed":overrides,
            "independent_session_manifests":{
                name:name+"/manifest.json" for name in results},
            "original_source_semantic_function_material_style_approved":False,
            "exclusive_GPU_face_UV_pixel_ownership_approved":False,
            "third_party_training_redistribution_rights_approved":False,
        }
        (out/MANIFEST).write_text(json.dumps(doc,indent=2,sort_keys=True,
                                              ensure_ascii=False)+"\\n",
                                  encoding="utf-8")
        return doc
    finally:
        if snapshot.exists():shutil.rmtree(snapshot)

def frames_and_proofs(folder,session,source,target):
    manifest=json.loads((folder/session/"manifest.json").read_text(encoding="utf-8"))
    need(manifest["schema"]=="MCFR_INT5_B19_FOUR_VIEW_ONE_REAL_FABRIC_CLIENT/v1"
         and manifest["session"]==session and manifest["target"]==target
         and manifest["source"]==source
         and manifest["new_real_native_F2"]==16
         and manifest["exact_server_state_proofs"]==
             (32 if target=="AF123_5" else 16),
         "real Fabric client/session source evidence missing")
    raw_log=(folder/session/"client.log").read_bytes()
    need(sha(raw_log)==manifest["client_log_sha256"],
         "B20 original client log SHA mismatch")
    log=raw_log.decode("utf-8",errors="replace")
    need("Reloading ResourceManager:" in log and "another_furniture" in log,
         "real original Minecraft resource reload not proven")
    frames={}
    png_sha={}
    for view in b19.VIEWS:
        rows=manifest["f2_records"][view]
        need(set(rows)==set(b19.stages()),"4 real original stages missing")
        frames[view]={}
        for stage,item in rows.items():
            label=b19.label(view,stage)
            need(item["image"]==label+".png" and item["dimensions"]==[1024,684]
                 and item["chair_state"]==b19.block(stage)
                 and item["slab_state"]==b19.support(stage)
                 and item["exact_state_checked"] is True and
                 set(item["server_markers"])==
                     ({"CHAIR","SUPPORT"} if target=="AF123_5" else {"CHAIR"}) and
                 all("[RenderAudit] "+marker in log for marker in
                     item["server_markers"].values()),
                 "original real server marker or screenshot state missing")
            data=(folder/session/item["image"]).read_bytes()
            need(sha(data)==item["sha256"],
                 "original game native PNG SHA mismatch")
            frames[view][stage]=b19.image_bytes(data)
            png_sha[label]=item["sha256"]
    return frames,sha(raw_log),png_sha

def compare_three(base,flat,norm):
    flat_control=b19.compare(base,flat)
    normalize=b19.compare(flat,norm)
    before,control,after,air=b19.stages()
    data={}
    for v in b19.VIEWS:
        flattened=flat_control[v]
        changed=normalize[v]
        fg_old=h15.pixel_changes(flat[v][before],flat[v][air])
        fg_new=h15.pixel_changes(norm[v][before],norm[v][air])
        changed_set=h15.pixel_changes(flat[v][before],norm[v][before])
        data[v]={
            "original_vs_flattened_all_four_stage_pixels":{
                stage:len(h15.pixel_changes(base[v][stage],flat[v][stage]))
                for stage in b19.stages()},
            "normalized_vs_flattened_before_pixels":
                changed["new_source_intervention_before_pixels"],
            "normalized_vs_flattened_after_pixels":
                changed["new_source_intervention_after_pixels"],
            "unmodified_negative_control_pixels":
                changed["unchanged_negative_control_pixels"],
            "unmodified_air_and_slab_pixels":
                changed["unchanged_air_and_support_pixels"],
            "flattened_A_A_temporal_pixels":
                changed["baseline_A_A_temporal_pixels"],
            "normalized_A_A_temporal_pixels":
                changed["modified_A_A_temporal_pixels"],
            "normalized_difference_outside_union_of_both_chair_foregrounds_pixels":
                len(changed_set-(fg_old|fg_new)),
            "original_chair_foreground_pixels":len(fg_old),
            "normalized_chair_foreground_pixels":len(fg_new),
        }
    return data

def decision(metrics):
    control_ok=all(
        all(p==0 for p in m["original_vs_flattened_all_four_stage_pixels"].values())
        and m["unmodified_negative_control_pixels"]==0
        and m["unmodified_air_and_slab_pixels"]==0
        and m["flattened_A_A_temporal_pixels"]==0
        and m["normalized_A_A_temporal_pixels"]==0
        and m["normalized_vs_flattened_before_pixels"]==
            m["normalized_vs_flattened_after_pixels"]
        and m["normalized_difference_outside_union_of_both_chair_foregrounds_pixels"]==0
        for m in metrics.values())
    positive=any(m["normalized_vs_flattened_before_pixels"]>0 for m in metrics.values())
    return ("PASS_BOUNDED_REVERSED_X_ENDPOINT_NORMALIZATION_RENDER_RESPONSE"
            if control_ok and positive else
            "NO_VISIBLE_RESPONSE_AFTER_ORIGINAL_X_ENDPOINT_NORMALIZATION"
            if control_ok else "CONDITIONAL_FAILED_FLATTEN_OR_RENDER_CONTROLS")

def audit(folder,target):
    set_target(target)
    folder=Path(folder)
    doc=json.loads((folder/MANIFEST).read_text(encoding="utf-8"))
    source=source_identity(target)
    need(doc["schema"]=="MCFR_INT5_B20_THREE_REAL_FABRIC_GAMES/v1" and
         doc["status"]=="THREE_ORIGINAL_FLATTENED_NORMALIZED_REAL_F2_PENDING_INDEPENDENT_AUDIT"
         and doc["target"]==target and doc["source"]==source and
         doc["official_release_jar_sha1"]==h12.JAR_SHA1 and
         doc["world_restored_from_same_pristine_snapshot_for_each_session"] is True
         and doc["sessions"]==["baseline","flattened","normalized"] and
         doc["real_native_F2_total"]==48 and
         doc["exact_server_chair_state_checks"]==48 and
         doc["top_slab_extra_state_checks"]==(48 if target=="AF123_5" else 0),
         "B20 original pinned three-game design/manifest drift")
    overrides=doc["only_child_one_member_changed"]
    need(set(overrides)=={"flattened","normalized"},
         "independent original/flatten/normalized experiment scopes missing")
    for mode,meta in overrides.items():
        pin=PIN[target]
        need(meta["mode"]==mode and meta["target"]==target and
             meta["source_faces"]==4 and meta["original_index"]==5 and
             meta["original_from"]==pin["from"] and
             meta["original_to"]==pin["to"] and
             meta["changed_uncompressed_JAR_members"]==[pin["child"]] and
             meta["original_parent_git_blob"]==pin["parent_blob"] and
             meta["original_child_git_blob"]==pin["child_blob"] and
             meta["all_other_source_elements_identical"] is True and
             meta["all_faces_UV_texture_and_parent_reference_unchanged"] is True and
             meta["original_release_JAR_or_artwork_distributed"] is False,
             "original source5 X-only intervention or release provenance unproven")
    sessions={}
    logs={}
    pngs={}
    for session in doc["sessions"]:
        need(doc["independent_session_manifests"][session]==session+"/manifest.json",
             "modified original game session path")
        sessions[session],logs[session],pngs[session]=frames_and_proofs(
            folder,session,source,target)
    metrics=compare_three(sessions["baseline"],sessions["flattened"],
                          sessions["normalized"])
    result={
        "schema":"MCFR_INT5_B20_REVERSED_X_SOURCE5_THREE_SESSION_AUDIT/v1",
        "source_key":source["source_key"],"target":target,
        "original_from":PIN[target]["from"],"original_to":PIN[target]["to"],
        "real_Fabric_minecraft_version":VERSION,
        "official_release_JAR_sha1":h12.JAR_SHA1,
        "three_real_game_sessions":3,"real_native_F2_verified":48,
        "original_server_chair_state_proofs":48,
        "additional_support_slab_server_state_proofs":(
            48 if target=="AF123_5" else 0),
        "individual_real_F2_SHA256":pngs,"original_client_log_SHA256":logs,
        "single_child_only_model_scope":overrides,
        "four_camera_pixel_metrics":metrics,"decision":decision(metrics),
        "original_X_reversed_source5_root_cause_exclusively_proven":False,
        "removed_original_source5_original_F2_nonresponse_B19_preserved":True,
        "source_face_UV_exclusive_GPU_pixel_ownership_approved":False,
        "physical_function_material_style_approved":False,
        "INT6_AI_training_redistribution_rights_approved":False,
        "H03":"HOLD","H05":"CONDITIONAL","F70_unconditional_approved":0,
        "limits":[
            "Changing source5 X endpoints is an intentional model variant, not proof a released mod bug exists.",
            "Flattening source inheritance must be pixel-identical to the original for causal interpretation.",
            "New geometry may occupy pixels outside the old original chair silhouette; compare against union foreground.",
            "One-element endpoint normalization is not proof of original face UV/GPU pixel exclusivity.",
            "Source roles, functional use, material/style and any third-party training rights remain unapproved.",
        ],
    }
    (folder/AUDIT).write_text(json.dumps(result,indent=2,sort_keys=True,
                                         ensure_ascii=False)+"\\n",encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target",choices=TARGETS,required=True)
    p.add_argument("--directory",type=Path,required=True)
    args=p.parse_args()
    r=audit(args.directory,args.target)
    print(json.dumps(r,sort_keys=True,ensure_ascii=False))
    if r["decision"]=="CONDITIONAL_FAILED_FLATTEN_OR_RENDER_CONTROLS":
        raise SystemExit(1)

if __name__=="__main__":
    main()
