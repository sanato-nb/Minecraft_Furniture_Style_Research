"""INT-5-B8: isolated original HC11210 cushion element12 removal in real Fabric.

Two real Minecraft 1.21.1 sessions with identical copied vanilla world:
 - original pinned Handcrafted Fabric 4.0.3, then
 - same official JAR with ONLY black-chair child model JSON modified to override
   its inherited 13 source elements with the first 12, leaving original shared
   parent and the white-chair control child unchanged byte for byte.

Two opposing spectator cameras each capture BLACK/WHITE/BLACK/AIR native F2.
All original vs modified white, AIR, temporal, server-state and SHA controls
must hold before a bounded render response can pass. Never infer pixel
ownership, seating functionality, material/style, or licensing from response.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
from time import sleep
from zipfile import ZipFile

from PIL import Image

from .runtime_capture import wait_for
from .chair_runtime_capture import (
    confirmed_spectator_mode, confirmed_camera_teleport,
    send_minecraft_command, archive_gui_diagnostic,
)
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15
from . import int5_b6_element_causal_evidence_ledger as b6
from . import int5_b8_hc_cushion_source_preflight as hc

ROOT=Path(__file__).resolve().parents[2]
STAGES=("black_before","white","black_after","air")
VIEWS=("south","north")
CASE_XYZ=(40,120,40)
CAMERAS={
    "south":"40.5 122.3 45.5 180 20",
    "north":"40.5 122.3 35.5 0 20",
}
SOURCE_KEY=("HC11210","HC13",12)
ROI=h15.ROI
VERSION="1.21.1"
ORIGINAL="INT5_B8_HC11210_CUSHION12_REAL_F2_MANIFEST_V1.json"
AUDIT="INT5_B8_HC11210_CUSHION12_REAL_F2_CAUSAL_AUDIT_V1.json"

def need(condition,reason):
    if not condition:
        raise ValueError("INT5-B8: "+reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def source_role_check():
    parts,groups,queue,summary=b6.calculate()
    matches=[r for r in parts if
             (r["child_model_key"],r["provider_key"],
              int(r["original_source_element_index"]))==SOURCE_KEY]
    need(len(matches)==1 and
         matches[0]["original_role_hypothesis"]=="SEAT_LAYER" and
         matches[0]["source_texture_role_cue"]=="ROLE_NAMED_ORIGINAL_CUSHION_PNG" and
         int(matches[0]["source_element_original_face_count"])==6 and
         matches[0]["causal_screen_response_status"]=="NOT_INDIVIDUALLY_CAUSAL_TESTED",
         "B6 original HC black cushion index12 role cue changed or pre-approved")
    need(len(queue)>1 and queue[1]["child_model_key"]=="HC11210" and
         queue[1]["original_source_element_index"]=="12" and
         summary["counts"]["part_function_final_approvals"]==0 and
         summary["counts"]["untested_elements"]==44,
         "B6 HC12 source candidate and historical experiment scope changed")
    return matches[0]

def pinned_chair_case():
    from .chair_runtime_fixture import cases
    chosen=[x for x in cases(VERSION) if x.case_id=="HC11210_north"]
    need(len(chosen)==1 and
         (chosen[0].x,chosen[0].y,chosen[0].z)==CASE_XYZ and
         chosen[0].state()==hc.STATE and
         chosen[0].camera()==CAMERAS["south"],
         "original Handcrafted north chair blockstate or camera drift")
    return chosen[0]

def state(stage):
    need(stage in STAGES,"unsupported HC color/control stage")
    if stage=="white":return hc.CTRL_STATE
    if stage=="air":return "minecraft:air"
    return hc.STATE

def label(view,stage):
    need(view in VIEWS and stage in STAGES,"unsupported paired-F2 label")
    return view+"_"+stage

def override_child_only(original_child,original_provider):
    child=json.loads(original_child.decode("utf-8-sig"))
    parent=json.loads(original_provider.decode("utf-8-sig"))
    need(isinstance(child,dict) and "elements" not in child and
         child.get("parent")=="handcrafted:block/chair/chair" and
         isinstance(parent,dict),
         "original black chair must inherit untouched real HC parent")
    elements=parent.get("elements")
    need(isinstance(elements,list) and len(elements)==13 and
         sum(len(x.get("faces",{})) for x in elements)==78 and
         len(elements[hc.ELEMENT].get("faces",{}))==6 and
         all(isinstance(x,dict) and "from" in x and "to" in x and
             isinstance(x.get("faces"),dict) for x in elements),
         "original release parent not exactly 13/78 and element12 6-faced")
    modified={**child,"elements":[x for i,x in enumerate(elements) if i!=hc.ELEMENT]}
    need({k:v for k,v in modified.items() if k!="elements"}==child and
         modified["elements"]==elements[:12] and
         len(modified["elements"])==12 and
         sum(len(x["faces"]) for x in modified["elements"])==72,
         "only index12 removal from black child was not established")
    content=json.dumps(modified,ensure_ascii=False,separators=(",",":")).encode()
    need(content!=original_child,"no actual child model change")
    return content,{"original_parent_elements":13,"original_parent_faces":78,
                    "isolated_black_child_elements":12,
                    "isolated_black_child_faces":72,
                    "removed_original_element_index":12,
                    "removed_original_element_from":elements[12]["from"],
                    "removed_original_element_to":elements[12]["to"],
                    "removed_original_element_faces":sorted(elements[12]["faces"]),
                    "other_original_indices_unchanged":list(range(12)),
                    "child_parent_and_texture_aliases_unchanged":True}

def prepare_disposable_child(game, original_preflight):
    jar=Path(game)/"mods"/hc.MOD
    original=jar.read_bytes()
    need(hashlib.sha1(original).hexdigest()==hc.SHA1 and
         original_preflight["official_jar_sha1"]==hc.SHA1,
         "actual original Handcrafted JAR source SHA drift before patch")
    with ZipFile(io.BytesIO(original)) as arc:
        names=arc.namelist()
        infos=arc.infolist()
        need(arc.testzip() is None and len(names)==len(set(names)),
             "original official JAR CRC or duplicated members invalid")
        members={n:arc.read(n) for n in names}
    black=hc.member(hc.CHILD)
    white=hc.member(hc.CONTROL)
    provider=original_preflight["original_black_provider"]
    need(provider==hc.member("handcrafted:block/chair/chair") and
         original_preflight["black_model_chain"]==[black,provider] and
         original_preflight["white_model_chain"]==[white,provider] and
         all(k in members for k in (black,white,provider)),
         "official released model inheritance not directly pinned to HC source")
    for member,expected in {
        black:"2d989c0059a633a55ebe1386bf5c9547ccd86de7",
        white:"6000caa39ce50c3b71632e59cfb49d0dfe2c9737",
        provider:"c5d9fbc054a897673f972fe2559376123751ba9b",
    }.items():
        need(gitblob(members[member])==expected,
             "original actual Handcrafted source JSON pin changed "+member)
    replacement,scope=override_child_only(members[black],members[provider])
    temporary=Path(game)/"int5-b8-temporary-original-mod-test.zip"
    with ZipFile(temporary,"w") as out:
        for info in infos:
            out.writestr(info,replacement if info.filename==black
                         else members[info.filename])
    with ZipFile(temporary) as arc:
        need(arc.testzip() is None and arc.namelist()==names,
             "modified ZIP CRC/members changed unexpectedly")
        changed=[name for name in names if arc.read(name)!=members[name]]
        need(changed==[black] and arc.read(provider)==members[provider] and
             arc.read(white)==members[white],
             "more than original black-chair child was modified")
        need(arc.read(black)==replacement,
             "modified child source JSON did not round-trip")
    ephemeral_sha=hashlib.sha1(temporary.read_bytes()).hexdigest()
    need(ephemeral_sha!=hc.SHA1,"disposable JAR SHA equals official original")
    temporary.replace(jar)
    need(hashlib.sha1(jar.read_bytes()).hexdigest()==ephemeral_sha,
         "game will not load expected modified Handcrafted JAR")
    return {
        "schema":"MCFR_INT5_B8_HC_CHILD_ONLY_DISPOSABLE_ELEMENT12/v1",
        "official_original_jar_sha1":hc.SHA1,
        "ephemeral_jar_sha1":ephemeral_sha,
        "original_black_child_member":black,
        "original_white_control_member":white,
        "original_shared_parent_member":provider,
        "changed_zip_resource_members":[black],
        "all_other_original_zip_uncompressed_members_unchanged":True,
        "original_shared_parent_unchanged":True,
        "original_white_control_child_unchanged":True,
        "original_black_child_git_blob_sha1":gitblob(members[black]),
        "original_white_child_git_blob_sha1":gitblob(members[white]),
        "original_parent_git_blob_sha1":gitblob(members[provider]),
        "patched_child_sha256":sha(replacement),
        "study_original_provider_byte_identical_to_release":True,
        "modified_jar_and_model_never_in_Git_or_artifact":True,
        "original_F2_black_cushion_source_role_only":True,
        **scope,
    }

def capture_session(command,env,game,output,session,preflight):
    """Capture one genuinely independent real game client from a freshly restored world."""
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    shots=Path(game)/"screenshots"
    client_log=output/"client.log"
    state_rows={v:{} for v in VIEWS}
    with client_log.open("wb") as sink,subprocess.Popen(
        command,cwd=game,env=env,stdout=sink,stderr=subprocess.STDOUT
    ) as proc:
        def read():return client_log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(
                ["xdotool",*args],env=env,timeout=18,text=True).strip()
        def focus():xdo("windowfocus","--sync",window)
        def send(cmd):send_minecraft_command(xdo,cmd)
        def acknowledge(command,marker,reason):
            for attempt,limit in enumerate((25,35),1):
                focus();start=len(read());send(command)
                try:
                    wait_for(proc,lambda:marker in read()[start:],
                             session+" "+reason+" retry "+str(attempt),limit)
                except ValueError as exc:
                    if not str(exc).startswith("Timed out waiting for") or attempt==2:
                        raise
                    continue
                sleep(.7)
                return
            raise ValueError("INT5-B8 no exact server response "+reason)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "B8 "+session+" real Minecraft joined",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in read(),
                     "B8 "+session+" Minecraft ready",90)
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            need(len(windows)==1,"expected exactly one real game window")
            window=windows[0]
            focus();sleep(2)
            confirmed_spectator_mode(proc,read,send,focus)
            acknowledge("/function mcfr_chair:place",
                        "[RenderAudit] MCFR_CHAIR_PLACED",
                        "original HC north test world placed")
            acknowledge("/function mcfr_chair:verify",
                        "[RenderAudit] MCFR_CHAIR_STATES_READ",
                        "original HC north world verified")
            shots.mkdir(exist_ok=True)
            for view in VIEWS:
                confirmed_camera_teleport(proc,read,send,focus,CAMERAS[view])
                for stage in STAGES:
                    key=label(view,stage)
                    block=state(stage)
                    if key!="south_black_before":
                        x,y,z=CASE_XYZ
                        acknowledge(f"/setblock {x} {y} {z} {block}",
                                    "[RenderAudit: Changed the block at",
                                    "set original stage "+key)
                    server_marker="MCFR_INT5_B8_"+session.upper()+"_"+key.upper()+"_EXACT_SERVER=PASS"
                    x,y,z=CASE_XYZ
                    acknowledge(f"/execute if block {x} {y} {z} {block} run say {server_marker}",
                                "[RenderAudit] "+server_marker,
                                "source exact blockstate "+key)
                    sleep(5)
                    screenshot=h12.screenshot(xdo,window,shots,output,key,{"proc":proc})
                    state_rows[view][stage]={
                        "state":block,"server_marker":server_marker,
                        "exact_server_checked":True,**screenshot}
                    print("INT5_B8_NATIVE_F2_"+session.upper()+" "+key,flush=True)
        except Exception:
            archive_gui_diagnostic(output,"INT5_B8_"+session.upper()+"_SOURCE_OR_CLIENT_FAILURE")
            raise
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    need(all(set(state_rows[v])==set(STAGES) for v in VIEWS),
         "actual native F2 8 or exact server state incomplete")
    data={
        "schema":"MCFR_INT5_B8_HC_REAL_NATIVE_8_F2_PER_SESSION/v1",
        "session":session,"game_version":VERSION,
        "original_HC_black_state":hc.STATE,
        "original_HC_white_state":hc.CTRL_STATE,
        "source_case":hc.CASE,
        "source_coordinates":list(CASE_XYZ),
        "fixed_cameras":CAMERAS,
        "native_F2_count":8,
        "exact_game_source_state_checks":8,
        "states":state_rows,
        "original_client_log_sha256":sha(client_log.read_bytes()),
        "real_game_source_model_and_control_preflight":preflight,
        "final_source_element_pixel_ownership_approved":False,
        "part_function_approved":False,
        "INT6_rights_approved":False,
    }
    (output/"manifest.json").write_text(
        json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return data

def capture(command,env,game,output,version):
    need(version==VERSION,"requires original Minecraft Java 1.21.1 Fabric")
    pinned_chair_case()
    source_role_check()
    game=Path(game)
    # Before *any* mutation verify the original released JAR source.
    preflight=hc.original_release_preflight(game/"mods"/hc.MOD)
    need(preflight["original_black_13_elements_78_faces"] is True and
         preflight["original_black_provider_git_blob_sha1"]==hc.SOURCE_PARENT_BLOB and
         preflight["source_provider_study_and_released_bytes_equal"] is True and
         preflight["white_control_distinct_child"] is True,
         "official source model not reliably linked to original source B6")
    out=Path(output)
    out.mkdir(parents=True,exist_ok=False)
    world_candidates=[p for p in (game/"saves").iterdir() if p.is_dir()
                      and (p/"level.dat").is_file()]
    need(len(world_candidates)==1,"B8 expects exactly one isolated vanilla client world")
    world=world_candidates[0]
    pristine=game/"b8-vanilla-world-original-snapshot"
    need(not pristine.exists(),"world snapshot destination must be new")
    shutil.copytree(world,pristine,ignore=shutil.ignore_patterns("session.lock"))
    try:
        first=capture_session(command,env,game,out/"baseline",
                              "baseline",preflight)
        # Avoid previous session's modified world save/time/light between runs.
        shutil.rmtree(world)
        shutil.copytree(pristine,world,ignore=shutil.ignore_patterns("session.lock"))
        patch=prepare_disposable_child(game,preflight)
        second=capture_session(command,env,game,out/"modified",
                               "modified",preflight)
        need(first["native_F2_count"]==second["native_F2_count"]==8,
             "original and patched real F2 not complete")
        manifest={
            "schema":"MCFR_INT5_B8_HC11210_TWO_REAL_FABRIC_SESSIONS/v1",
            "status":"TWO_ACTUAL_NATIVE_F2_SESSIONS_PENDING_INDEPENDENT_REOPEN",
            "original_source_case":"HC11210_north",
            "actual_game_version":VERSION,
            "original_game_sessions":1,
            "disposable_game_sessions":1,
            "original_game_F2_count":8,
            "disposable_game_F2_count":8,
            "exact_server_source_states_total":16,
            "official_HC_preflight":preflight,
            "ephemeral_child_patch":patch,
            "pristine_world_restored_between_sessions":True,
            "real_F2_separate_session_manifests":{
                "baseline":"baseline/manifest.json","modified":"modified/manifest.json",
            },
            "unique_element_pixel_owner_approved":False,
            "gameplay_seating_or_material_approved":False,
            "INT6_rights_approved":False,
        }
        (out/ORIGINAL).write_text(
            json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
            encoding="utf-8")
        return manifest
    finally:
        # The snapshot is the disposable generated vanilla world only; the
        # original official Handcrafted JAR never enters artifact output.
        if pristine.exists():shutil.rmtree(pristine)

def open_real_PNG(data,label):
    with Image.open(io.BytesIO(data)) as image:
        image.load()
        need(image.format=="PNG" and image.size==(1024,684),
             "original Minecraft native F2 PNG invalid "+label)
        return image.convert("RGB")

def measure(baseline,modified):
    measurements={}
    for view in VIEWS:
        original=baseline[view];altered=modified[view]
        foreground=h15.pixel_changes(original["black_before"],original["air"])
        before=h15.pixel_changes(original["black_before"],altered["black_before"])
        after=h15.pixel_changes(original["black_after"],altered["black_after"])
        white=h15.pixel_changes(original["white"],altered["white"])
        air=h15.pixel_changes(original["air"],altered["air"])
        old_temporal=h15.pixel_changes(original["black_before"],original["black_after"])
        new_temporal=h15.pixel_changes(altered["black_before"],altered["black_after"])
        measurements[view]={
            "original_black_chair_foreground_pixels":len(foreground),
            "cushion12_removal_original_vs_modified_black_before_pixels":len(before),
            "cushion12_removal_original_vs_modified_black_after_pixels":len(after),
            "white_control_original_vs_modified_pixels":len(white),
            "air_control_original_vs_modified_pixels":len(air),
            "original_black_before_vs_after_temporal_pixels":len(old_temporal),
            "modified_black_before_vs_after_temporal_pixels":len(new_temporal),
            "changed_pixels_outside_original_black_foreground":len(before-foreground),
            "removal_response_not_exclusive_original_element_pixel_ownership":True,
        }
    return measurements

def audit(directory):
    out=Path(directory)
    doc=json.loads((out/ORIGINAL).read_text(encoding="utf-8"))
    need(doc["schema"]=="MCFR_INT5_B8_HC11210_TWO_REAL_FABRIC_SESSIONS/v1" and
         doc["status"]=="TWO_ACTUAL_NATIVE_F2_SESSIONS_PENDING_INDEPENDENT_REOPEN" and
         doc["original_source_case"]==hc.CASE and
         doc["actual_game_version"]==VERSION and
         doc["original_game_sessions"]==doc["disposable_game_sessions"]==1 and
         doc["original_game_F2_count"]==doc["disposable_game_F2_count"]==8 and
         doc["exact_server_source_states_total"]==16 and
         doc["pristine_world_restored_between_sessions"] is True,
         "B8 two actual game session scope/identity missing")
    p=doc["official_HC_preflight"]
    patch=doc["ephemeral_child_patch"]
    need(p["official_jar_sha1"]==hc.SHA1 and
         p["source_element_index"]==12 and
         p["source_element_face_count"]==6 and
         p["source_provider_study_and_released_bytes_equal"] is True and
         p["original_black_provider_git_blob_sha1"]==hc.SOURCE_PARENT_BLOB and
         p["white_control_distinct_child"] is True and
         patch["official_original_jar_sha1"]==hc.SHA1 and
         patch["changed_zip_resource_members"]==[hc.member(hc.CHILD)] and
         patch["original_white_control_child_unchanged"] is True and
         patch["original_shared_parent_unchanged"] is True and
         patch["all_other_original_zip_uncompressed_members_unchanged"] is True and
         patch["original_parent_elements"]==13 and patch["original_parent_faces"]==78 and
         patch["isolated_black_child_elements"]==12 and
         patch["isolated_black_child_faces"]==72 and
         patch["removed_original_element_index"]==12 and
         patch["original_parent_git_blob_sha1"]==hc.SOURCE_PARENT_BLOB and
         patch["modified_jar_and_model_never_in_Git_or_artifact"] is True,
         "official source or disposable single-element removal not proven")
    frames={}
    manifests={}
    logs={}
    for session in ("baseline","modified"):
        folder=out/session
        session_doc=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
        need(doc["real_F2_separate_session_manifests"][session]==session+"/manifest.json" and
             session_doc["schema"]=="MCFR_INT5_B8_HC_REAL_NATIVE_8_F2_PER_SESSION/v1" and
             session_doc["session"]==session and
             session_doc["game_version"]==VERSION and
             session_doc["original_HC_black_state"]==hc.STATE and
             session_doc["original_HC_white_state"]==hc.CTRL_STATE and
             session_doc["source_case"]==hc.CASE and
             session_doc["source_coordinates"]==list(CASE_XYZ) and
             session_doc["fixed_cameras"]==CAMERAS and
             session_doc["native_F2_count"]==8 and
             session_doc["exact_game_source_state_checks"]==8 and
             session_doc["final_source_element_pixel_ownership_approved"] is False,
             "session manifest exact source/game state not independent")
        log_bytes=(folder/"client.log").read_bytes()
        need(sha(log_bytes)==session_doc["original_client_log_sha256"],
             "real Fabric client game log sha drift "+session)
        log=log_bytes.decode("utf-8",errors="replace")
        require_mod=[line for line in log.splitlines()
                     if "Reloading ResourceManager:" in line and "handcrafted" in line]
        need(bool(require_mod),"actual Handcrafted mod not loaded in real session "+session)
        imgs={}
        for view in VIEWS:
            need(set(session_doc["states"])==set(VIEWS) and
                 set(session_doc["states"][view])==set(STAGES),
                 "native F2 view/stage count missing")
            imgs[view]={}
            for stage in STAGES:
                source=session_doc["states"][view][stage]
                key=label(view,stage)
                need(source["state"]==state(stage) and
                     source["exact_server_checked"] is True and
                     "[RenderAudit] "+source["server_marker"] in log and
                     source["image"]==key+".png" and
                     source["dimensions"]==[1024,684],
                     "real game server original state not confirmed "+session+"/"+key)
                binary=(folder/source["image"]).read_bytes()
                need(sha(binary)==source["sha256"],
                     "real game native original PNG SHA drift "+session+"/"+key)
                imgs[view][stage]=open_real_PNG(binary,session+"/"+key)
        frames[session]=imgs
        manifests[session]=session_doc
        logs[session]=sha(log_bytes)
    per_camera=measure(frames["baseline"],frames["modified"])
    controls=all(m["white_control_original_vs_modified_pixels"]==0 and
                 m["air_control_original_vs_modified_pixels"]==0 and
                 m["original_black_before_vs_after_temporal_pixels"]==0 and
                 m["modified_black_before_vs_after_temporal_pixels"]==0 and
                 m["changed_pixels_outside_original_black_foreground"]==0
                 for m in per_camera.values())
    causal=any(
        m["cushion12_removal_original_vs_modified_black_before_pixels"]>0 and
        m["cushion12_removal_original_vs_modified_black_before_pixels"]==
        m["cushion12_removal_original_vs_modified_black_after_pixels"]
        for m in per_camera.values()
    )
    status=("PASS_HC11210_BLACK_CHILD_ELEMENT12_REMOVAL_REAL_NATIVE_F2_RESPONSE"
            if controls and causal else
            "CONDITIONAL_HC_CUSHION12_RENDER_CAUSAL_OR_NEGATIVE_CONTROL_UNPROVEN")
    result={
        "schema":"MCFR_INT5_B8_HC_CUSHION_ELEMENT12_REAL_GAME_F2_CAUSAL_AUDIT/v1",
        "decision":status,
        "source_child_model_key":"HC11210",
        "source_provider_key":"HC13",
        "original_source_element_index":12,
        "original_source_element_face_count":6,
        "source_role_hypothesis_not_gameplay":"SEAT_LAYER",
        "actual_original_Fabric_release_version":"handcrafted-fabric-1.21.1-4.0.3",
        "actual_client_game_version":VERSION,
        "exact_source_blockstate":hc.STATE,
        "unmodified_control_state":hc.CTRL_STATE,
        "real_original_game_sessions":1,
        "real_disposable_game_sessions":1,
        "real_original_native_F2_verified":8,
        "real_modified_native_F2_verified":8,
        "real_exact_server_state_markers_verified":16,
        "per_camera_pixel_response":per_camera,
        "white_child_and_AIR_negative_controls_equal":controls,
        "any_real_cushion12_element_removal_render_response":causal,
        "original_official_JAR_sha1":hc.SHA1,
        "original_model_provider_git_blob_sha1":hc.SOURCE_PARENT_BLOB,
        "ephemeral_modified_JAR_sha1":patch["ephemeral_jar_sha1"],
        "single_child_member_modified_only":patch["changed_zip_resource_members"],
        "untouched_parent_and_white_child":True,
        "official_source_preflight":p,
        "original_model_intervention_provenance":patch,
        "real_original_client_log_sha256":logs["baseline"],
        "real_modified_client_log_sha256":logs["modified"],
        "original_native_F2_sha256":{
            label(v,stage):manifests["baseline"]["states"][v][stage]["sha256"]
            for v in VIEWS for stage in STAGES},
        "disposable_native_F2_sha256":{
            label(v,stage):manifests["modified"]["states"][v][stage]["sha256"]
            for v in VIEWS for stage in STAGES},
        "original_element_exclusive_visible_pixel_ownership_approved":False,
        "gameplay_seating_or_function_approved":False,
        "part_material_or_style_final_approved":False,
        "INT5_final_semantic_approvals":0,
        "INT6_AI_training_or_redistribution_rights_approved":0,
        "F70_unconditional_approvals":0,
        "strict_H03_H05_full_exit":False,
        "limits":[
            "This is a bounded source-element removal causing screen response only, NOT a direct GPU per-face pixel ownership or exact original face-UV proof.",
            "Black cushion is an original source texture role cue, not proof of sitting, cushion physics, materials, or style.",
            "Only north-facing HC11210 black cushion variant was tested from two observers; other block facings, cushion colors and elements remain untested.",
            "The original 4.0.3 official Fabric JAR parent bytes were SHA matched to research, but do not generalize this equivalence to all mod releases.",
            "The untouched white model state and AIR are exact byte/original client negative controls; separate game sessions require temporal A/A and outside-foreground zero.",
            "Third-party mod JAR, edited model and raw textures never enter Git or the CI screenshot artifact.",
            "Previously established B5 AF123 and B7 AF121 remain independently verified and unchanged.",
        ],
    }
    (out/AUDIT).write_text(
        json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False,sort_keys=True))

if __name__=="__main__":main()
