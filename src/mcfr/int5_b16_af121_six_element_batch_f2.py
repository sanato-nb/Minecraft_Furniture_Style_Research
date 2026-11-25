"""INT-5-B16 isolated AF121 acacia_1 selected_element removal with actual Minecraft F2.

Original 4.0.2 child inherits the shared template/chair with ten elements.
Only the *acacia_1 child JSON* is changed in one disposable verified JAR to
override inherited elements with precisely one selected original element removed.
The original parent and acacia_3 child stay byte-identical, giving a genuinely
independent variant3 negative control. Compare against the original H15 eight
real native F2 frames at identical camera/stages. Never treat a removal-induced
screen response as pixel ownership, physical function, material, style or rights.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import shutil
import subprocess
from pathlib import Path
from time import sleep
from zipfile import ZipFile

from PIL import Image

from .runtime_capture import wait_for
from .chair_runtime_capture import (send_minecraft_command,confirmed_camera_teleport,
                                    confirmed_spectator_mode,archive_gui_diagnostic)
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15
from . import int4_h16_af_single_texel_f2 as h16
from . import int5_b6_element_causal_evidence_ledger as b6

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.1"
JAR_NAME="another_furniture-fabric-4.0.2.jar"
MODEL="another_furniture:block/chair/acacia_1"
CHILD="assets/another_furniture/models/block/chair/acacia_1.json"
CONTROL="assets/another_furniture/models/block/chair/acacia_3.json"
PARENT="assets/another_furniture/models/block/template/chair.json"
SOURCE_INDEX=0
FACES={0:5,1:5,2:5,3:5,5:4,6:4}
ROLES={0:'LEG_OR_LOWER_POST',1:'LEG_OR_LOWER_POST',2:'LEG_OR_LOWER_POST',3:'LEG_OR_LOWER_POST',5:'LOWER_FRAME',6:'LOWER_FRAME'}
STAGES=h15.STAGES
VIEWS=h15.VIEWS
CAMERAS=h15.EXPECTED_CAMERAS
BLOCK_XYZ=h15.BLOCK_XYZ
BASELINE_ARTIFACT_SHA256=h16.H15_SHA
ORIGINAL="INT5_B16_AF121_ELEMENT_SELECTED_REAL_F2_MANIFEST_V1.json"
AUDIT="INT5_B16_AF121_ELEMENT_SELECTED_INDEPENDENT_CAUSAL_AUDIT_V1.json"
SOURCE_KEY=("AF121","AF1393",0)


def select_index(index):
    """Select one original source element for this isolated CI process."""
    global SOURCE_INDEX,SOURCE_KEY
    need(index in FACES,"not a selected untested AF121 source element")
    SOURCE_INDEX=index
    SOURCE_KEY=("AF121","AF1393",index)


def need(ok, msg):
    if not ok:
        raise ValueError("INT5-B16: "+msg)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def original_role():
    """Pinned B3 source, plus B15 45-row status: no name-based promotion."""
    source=ROOT/"project/integration/INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv"
    latest=ROOT/"project/integration/INT5_B15_FOUR_MODEL_45_PART_BATCH_STATUS_V1.csv"
    need(blob(source.read_bytes())=="d314941b950b70fa637536f86182eb4866b7aed1",
         "B3 fixed source 45-element role ledger git blob drift")
    with source.open(encoding="utf-8-sig",newline="") as stream:
        rows=list(csv.DictReader(stream))
    with latest.open(encoding="utf-8-sig",newline="") as stream:
        status=list(csv.DictReader(stream))
    need(len(rows)==len(status)==45,"B3/B15 full 45-elements not available")
    matches=[x for x in rows if (x["child_model_key"],x["provider_key"],
              int(x["original_source_element_index"]))==SOURCE_KEY]
    verified=[x for x in status if (x["model"],x["provider"],
              int(x["index"]))==SOURCE_KEY]
    need(len(matches)==len(verified)==1 and
         verified[0]["state"]=="NOT_YET_TESTED" and
         matches[0]["original_role_hypothesis"]==ROLES[SOURCE_INDEX] and
         int(matches[0]["source_element_original_face_count"])==FACES[SOURCE_INDEX] and
         matches[0]["role_discriminating_texture_cue"]=="GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF" and
         all(matches[0][field]=="false" for field in (
             "individual_element_to_original_F2_pixels_approved",
             "part_function_verified","material_or_style_verified",
             "training_or_redistribution_rights_approved")),
         "Original AF121 source/face/role/case status drift or unauthorized approval")
    return matches[0]

def isolated_child_override(original_child,original_control,original_parent):
    """Return ONLY modified acacia_1, retaining original template for all siblings."""
    child=json.loads(original_child.decode("utf-8-sig"))
    negative=json.loads(original_control.decode("utf-8-sig"))
    parent=json.loads(original_parent.decode("utf-8-sig"))
    need(isinstance(child,dict) and isinstance(negative,dict) and
         child.get("parent")=="another_furniture:block/template/chair" and
         negative.get("parent")=="another_furniture:block/template/chair" and
         "elements" not in child and "elements" not in negative,
         "original acacia1/acacia3 children do not both inherit pinned template")
    elements=parent.get("elements")
    need(isinstance(elements,list) and len(elements)==10 and
         sum(len(e["faces"]) for e in elements)==46 and
         len(elements[SOURCE_INDEX]["faces"])==FACES[SOURCE_INDEX] and
         all("from" in e and "to" in e and isinstance(e.get("faces"),dict)
             for e in elements),
         "pinned source parent not original 10-element/46-face template")
    revised=dict(child)
    revised["elements"]=[e for i,e in enumerate(elements) if i!=SOURCE_INDEX]
    need(len(revised["elements"])==9 and
         sum(len(e["faces"]) for e in revised["elements"])==46-FACES[SOURCE_INDEX] and
         all(e==elements[i] for j,e in enumerate(revised["elements"])
             for i in ([j] if j<SOURCE_INDEX else [j+1])),
         "child selected_element-only exclusion changed another geometry element")
    need({k:v for k,v in revised.items() if k!="elements"}==child,
         "the original acacia_1 child textures or parent changed")
    encoded=json.dumps(revised,ensure_ascii=False,separators=(",",":")).encode()
    need(encoded!=original_child,"no effective model patch generated")
    return encoded,{"original_child_parent":child["parent"],
                     "original_child_keys":sorted(child),
                     "parent_original_element_count":10,
                     "parent_original_face_count":46,
                     "child_new_element_count":9,
                     "child_new_face_count":46-FACES[SOURCE_INDEX],
                     "removed_source_index":SOURCE_INDEX,
                     "removed_source_element_from":elements[SOURCE_INDEX]["from"],
                     "removed_source_element_to":elements[SOURCE_INDEX]["to"],
                     "removed_source_element_faces":sorted(elements[SOURCE_INDEX]["faces"]),
                     "nonremoved_original_element_indices":[i for i in range(10)
                                                           if i!=SOURCE_INDEX],
                     "original_parent_unmodified":True,
                     "acacia3_negative_control_unmodified":True}

def prepare_disposable_child(game):
    source=h12.static_preflight(game)
    original_role()
    jar=Path(game)/"mods"/JAR_NAME
    data=jar.read_bytes()
    original_sha=hashlib.sha1(data).hexdigest()
    need(original_sha==h12.JAR_SHA1,
         "official Fabric 4.0.2 JAR release is not original")
    with ZipFile(io.BytesIO(data)) as z:
        infos=z.infolist()
        names=z.namelist()
        need(len(names)==len(set(names)) and z.testzip() is None and
             all(n in names for n in (CHILD,CONTROL,PARENT)),
             "official original JAR file identity/CRC invalid")
        content={n:z.read(n) for n in names}
    # The research Git 4.0.3 blobs differ from official Fabric 4.0.2
    # serialized JSON bytes despite H12's confirmed semantic model parity.
    # Require the PINNED 4.0.2 runtime Git blobs verified by H12 preflight.
    runtime_pins={
        CHILD:("models/block/chair/acacia_1.json",
               "2261460299d13a15220f4fecfe059628ac28e813"),
        CONTROL:("models/block/chair/acacia_3.json",
                 "1c5ef86b8413f7c8d246869cb63b21dfd8f6853e"),
        PARENT:("models/block/template/chair.json",
                "31c643617a7178ac5113702e785620f4d1150adf"),
    }
    need(all(blob(content[member])==expected and
             source["actual_runtime_provenance"][rel]["git_blob_sha1"]==expected
             for member,(rel,expected) in runtime_pins.items()),
         "official released 4.0.2 model JSON pin mismatched H12 certified runtime")
    patch,scope=isolated_child_override(content[CHILD],content[CONTROL],content[PARENT])
    before_hashes={n:sha(content[n]) for n in (CHILD,CONTROL,PARENT)}
    contents={**content,CHILD:patch}
    tmp=jar.with_suffix(".b7-ephemeral-test-copy")
    with ZipFile(tmp,"w") as z:
        for inf in infos:
            z.writestr(inf,contents[inf.filename])
    with ZipFile(tmp) as z:
        need(z.testzip() is None and z.namelist()==names,
             "temporary modified AF JAR CRC or member list invalid")
        changed=[name for name in names if z.read(name)!=content[name]]
        need(changed==[CHILD] and
             z.read(PARENT)==content[PARENT] and
             z.read(CONTROL)==content[CONTROL] and
             z.read(CHILD)==patch,
             "ephemeral test copy changes non-target resources")
        reread=json.loads(z.read(CHILD).decode())
        need(len(reread["elements"])==9 and
             reread["parent"]=="another_furniture:block/template/chair",
             "reread temporary acacia1 child not single source-element override")
    patched_sha=hashlib.sha1(tmp.read_bytes()).hexdigest()
    need(patched_sha!=original_sha,"patched release JAR is byte-identical")
    tmp.replace(jar)
    need(hashlib.sha1(jar.read_bytes()).hexdigest()==patched_sha,
         "actual disposable Fabric JAR not installed")
    return {
        "schema":"MCFR_INT5_B16_DISPOSABLE_CHILD_ONLY_ELEMENT_SELECTED_REMOVAL/v1",
        "verified_official_JAR_sha1":original_sha,
        "disposable_runtime_JAR_sha1":patched_sha,
        "game_version":VERSION,
        "release_mod":JAR_NAME,
        "tested_original_blockstate":h12.state("model1"),
        "tested_child_resource":MODEL,
        "modified_only_JAR_member":CHILD,
        "original_unmodified_control_child":CONTROL,
        "original_unmodified_template_parent":PARENT,
        "original_source_git_blob_sha1":{
            key:blob(content[key]) for key in (CHILD,PARENT,CONTROL)},
        "original_resource_sha256":before_hashes,
        "patched_child_sha256":sha(patch),
        "original_h11_source_sha1":source["h11_git_blob_sha1"],
        "one_and_only_one_uncompressed_JAR_member_modified":True,
        "all_other_uncompressed_members_byte_identical":True,
        "original_mod_resource_or_texture_committed":False,
        "temporary_modified_JAR_or_model_in_output_artifact":False,
        "source_4_0_3_vs_release_4_0_2_not_assumed_byte_equivalent":True,
        **scope,
    }

def capture(command,env,game,output,version):
    need(version==VERSION,"must run actual pinned official Fabric 1.21.1")
    case=h12.original_case()[0]
    need((case.x,case.y,case.z)==BLOCK_XYZ and
         case.camera()==CAMERAS["south"],
         "original AF121 source chair case/cameras changed")
    provenance=prepare_disposable_child(game)
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    shots=Path(game)/"screenshots"
    log=output/"client.log"
    states={v:{} for v in VIEWS}
    with log.open("wb") as sink,subprocess.Popen(
        command,cwd=game,env=env,stdout=sink,stderr=subprocess.STDOUT
    ) as proc:
        def txt():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,
                                           timeout=18,text=True).strip()
        def focus():xdo("windowfocus","--sync",window)
        def send(cmd):send_minecraft_command(xdo,cmd)
        def ack(cmd,marker,reason):
            for attempt,tlimit in enumerate((25,35),1):
                focus();p=len(txt());send(cmd)
                try:
                    wait_for(proc,lambda:marker in txt()[p:],
                             reason+" focused attempt "+str(attempt),tlimit)
                except ValueError as e:
                    if not str(e).startswith("Timed out waiting for") or attempt==2:
                        raise
                    continue
                sleep(.7)
                return
            raise ValueError("INT5_B16_SERVER_ACK_MISSING "+reason)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in txt(),
                     "B16 original AF121 actual Minecraft world join",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in txt(),
                     "B16 original actual Minecraft client ready",90)
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            need(len(windows)==1,"B16 did not locate exactly one real Minecraft window")
            window=windows[0];focus();sleep(2)
            confirmed_spectator_mode(proc,txt,send,focus)
            ack("/function mcfr_chair:place",
                "[RenderAudit] MCFR_CHAIR_PLACED",
                "actual variant1 starting chair fixture")
            ack("/function mcfr_chair:verify",
                "[RenderAudit] MCFR_CHAIR_STATES_READ",
                "actual original pinned source state")
            shots.mkdir(exist_ok=True)
            for view in VIEWS:
                confirmed_camera_teleport(proc,txt,send,focus,CAMERAS[view])
                for stage in STAGES:
                    name=h15.label(view,stage)
                    state=h15.stage_state(stage)
                    if name!="south_model1_before":
                        x,y,z=BLOCK_XYZ
                        ack(f"/setblock {x} {y} {z} {state}",
                            "[RenderAudit: Changed the block at",
                            "B16 real stage change "+name)
                    marker="MCFR_INT5_B16_"+name.upper()+"_EXACT_SERVER=PASS"
                    x,y,z=BLOCK_XYZ
                    ack(f"/execute if block {x} {y} {z} {state} run say {marker}",
                        "[RenderAudit] "+marker,
                        "B16 exact server source block "+name)
                    sleep(5)
                    shot=h12.screenshot(xdo,window,shots,output,name,{"proc":proc})
                    states[view][stage]={"blockstate":state,"marker":marker,
                                         "exact_server_verified":True,**shot}
                    print("INT5_B16_ACTUAL_NATIVE_F2 "+name,flush=True)
        except Exception:
            archive_gui_diagnostic(output,"B16_ACTUAL_FABRIC_CLIENT_SOURCE_OR_F2_FAILURE")
            raise
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    need(all(set(states[v])==set(STAGES) for v in VIEWS),
         "B16 source states or eight F2 not complete")
    manifest={
        "schema":"MCFR_INT5_B16_AF121_REAL_FABRIC_CHILD_ELEMENT_SELECTED_F2/v1",
        "status":"ACTUAL_SOURCE_ELEMENT_SELECTED_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT",
        "version":VERSION,"game_sessions":1,"F2_count":8,
        "case_id":"AF121_north",
        "source_model":MODEL,
        "block_xyz":list(BLOCK_XYZ),
        "same_two_cameras_as_unmodified_H15":CAMERAS,
        "views":states,
        "patch_provenance":provenance,
        "client_log_sha256":sha(log.read_bytes()),
        "all_AIR_and_model3_negative_controls_independent_audit_pending":True,
        "original_element_unique_F2_pixel_ownership_approved":False,
        "new_function_material_style_approvals":0,
        "INT6_training_or_redistribution_approvals":0,
    }
    (output/ORIGINAL).write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
        encoding="utf-8")
    return manifest

def open_frame(binary,reason):
    with Image.open(io.BytesIO(binary)) as img:
        img.load()
        need(img.format=="PNG" and img.size==(1024,684),
             "original native real F2 PNG invalid "+reason)
        return img.convert("RGB")

def compare_frames(original,modified):
    metrics={}
    for v in VIEWS:
        original_frames=original[v];current=modified[v]
        fg=h15.pixel_changes(original_frames["model1_before"],
                             original_frames["air"])
        before=h15.pixel_changes(original_frames["model1_before"],
                                 current["model1_before"])
        after=h15.pixel_changes(original_frames["model1_after"],
                                current["model1_after"])
        model3=h15.pixel_changes(original_frames["model3"],
                                 current["model3"])
        air=h15.pixel_changes(original_frames["air"],current["air"])
        modified_temporal=h15.pixel_changes(current["model1_before"],
                                            current["model1_after"])
        original_temporal=h15.pixel_changes(original_frames["model1_before"],
                                            original_frames["model1_after"])
        metrics[v]={
            "original_chair_model1_foreground_pixels_vs_AIR":len(fg),
            "removed_selected_element_original_vs_patched_model1_before_pixels":len(before),
            "removed_selected_element_original_vs_patched_model1_after_pixels":len(after),
            "original_model3_untouched_child_negative_pixels":len(model3),
            "original_AIR_untouched_world_negative_pixels":len(air),
            "original_model1_A_A_temporal_pixels":len(original_temporal),
            "patched_model1_A_A_temporal_pixels":len(modified_temporal),
            "patched_model1_changed_pixels_outside_original_foreground":len(before-fg),
            "intervention_changed_pixels_are_NOT_exclusive_original_element_pixels":True,
        }
    return metrics

def audit(directory,baseline_zip):
    target=Path(directory)
    baseline_zip=Path(baseline_zip)
    need(sha(baseline_zip.read_bytes())==BASELINE_ARTIFACT_SHA256,
         "original H15 baseline artifact whole ZIP SHA mismatch")
    document=json.loads((target/ORIGINAL).read_text(encoding="utf-8"))
    need(document["schema"]=="MCFR_INT5_B16_AF121_REAL_FABRIC_CHILD_ELEMENT_SELECTED_F2/v1" and
         document["status"]=="ACTUAL_SOURCE_ELEMENT_SELECTED_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT" and
         document["version"]==VERSION and document["game_sessions"]==1 and
         document["F2_count"]==8 and document["case_id"]=="AF121_north" and
         document["source_model"]==MODEL and
         document["same_two_cameras_as_unmodified_H15"]==CAMERAS and
         document["block_xyz"]==list(BLOCK_XYZ),
         "new modified native F2 source/camera identity changed")
    p=document["patch_provenance"]
    need(p["schema"]=="MCFR_INT5_B16_DISPOSABLE_CHILD_ONLY_ELEMENT_SELECTED_REMOVAL/v1" and
         p["verified_official_JAR_sha1"]==h12.JAR_SHA1 and
         p["tested_original_blockstate"]==h12.state("model1") and
         p["tested_child_resource"]==MODEL and
         p["modified_only_JAR_member"]==CHILD and
         p["original_unmodified_control_child"]==CONTROL and
         p["original_unmodified_template_parent"]==PARENT and
         p["one_and_only_one_uncompressed_JAR_member_modified"] is True and
         p["all_other_uncompressed_members_byte_identical"] is True and
         p["original_parent_unmodified"] is True and
         p["acacia3_negative_control_unmodified"] is True and
         p["parent_original_element_count"]==10 and
         p["parent_original_face_count"]==46 and
         p["child_new_element_count"]==9 and
         p["child_new_face_count"]==46-FACES[SOURCE_INDEX] and
         p["removed_source_index"]==SOURCE_INDEX and
         len(p["removed_source_element_faces"])==FACES[SOURCE_INDEX] and
         p["temporary_modified_JAR_or_model_in_output_artifact"] is False and
         p["original_mod_resource_or_texture_committed"] is False and
         p["source_4_0_3_vs_release_4_0_2_not_assumed_byte_equivalent"] is True,
         "single isolated AF121 child selected_element experiment provenance missing")
    log=(target/"client.log").read_bytes()
    need(sha(log)==document["client_log_sha256"],
         "modified real Fabric game log SHA different from manifest")
    txt=log.decode("utf-8",errors="replace")
    mod_entries=[x for x in txt.splitlines() if
                 "Reloading ResourceManager:" in x and "another_furniture" in x]
    need(bool(mod_entries),"actual Fabric did not load Another Furniture mod resources")
    model_frames={}
    original_frames={}
    with ZipFile(baseline_zip) as z:
        need(z.testzip() is None and len(z.namelist())==len(set(z.namelist())),
             "original baseline ZIP invalid CRC or duplicate")
        baseline=json.loads(z.read(h15.ORIGINAL))
        need(baseline["schema"]=="MCFR_INT4_H15_AF_OPPOSING_NATIVE_F2_GAME_SOURCE/v1" and
             baseline["status"]=="ORIGINAL_REAL_FABRIC_TWO_CAMERA_F2_CAPTURED_REQUIRES_INDEPENDENT_AUDIT" and
             baseline["pinned_provenance"]["actual_af_jar_sha1"]==h12.JAR_SHA1 and
             baseline["source_model1"]==MODEL and
             baseline["source_model3"]==h12.MODELS["model3"] and
             baseline["cameras"]==CAMERAS and
             baseline["source_block_coordinates"]==list(BLOCK_XYZ) and
             baseline["native_F2_count"]==8 and
             baseline["runtime_version"]==VERSION,
             "H15 exact official baseline camera/model source not proven")
        original_log=z.read("client.log")
        need(sha(original_log)==baseline["client_log_sha256"],
             "H15 original game client log hash drift")
        original_text=original_log.decode("utf-8",errors="replace")
        for view in VIEWS:
            need(set(baseline["views"][view])==set(STAGES) and
                 set(document["views"][view])==set(STAGES),
                 "paired H15 and B16 source state stages differ")
            original_frames[view]={}
            model_frames[view]={}
            for stage in STAGES:
                key=h15.label(view,stage)
                state=h15.stage_state(stage)
                old=baseline["views"][view][stage]
                new=document["views"][view][stage]
                need(old["blockstate"]==new["blockstate"]==state and
                     old["exact_server_verified"] is True and
                     new["exact_server_verified"] is True and
                     "[RenderAudit] "+old["server_marker"] in original_text and
                     "[RenderAudit] "+new["marker"] in txt and
                     old["image"]==new["image"]==key+".png" and
                     old["dimensions"]==new["dimensions"]==[1024,684],
                     "original vs modified server state / F2 labeling mismatch "+key)
                old_bytes=z.read(old["image"])
                new_bytes=(target/new["image"]).read_bytes()
                need(sha(old_bytes)==old["sha256"] and
                     sha(new_bytes)==new["sha256"],
                     "H15 or new actual F2 SHA changed "+key)
                original_frames[view][stage]=open_frame(old_bytes,"original "+key)
                model_frames[view][stage]=open_frame(new_bytes,"patched "+key)
    measurements=compare_frames(original_frames,model_frames)
    controls=all(
       m["original_model3_untouched_child_negative_pixels"]==0 and
       m["original_AIR_untouched_world_negative_pixels"]==0 and
       m["original_model1_A_A_temporal_pixels"]==0 and
       m["patched_model1_A_A_temporal_pixels"]==0 and
       m["patched_model1_changed_pixels_outside_original_foreground"]==0
       for m in measurements.values()
    )
    response=any(
       m["removed_selected_element_original_vs_patched_model1_before_pixels"]>0 and
       m["removed_selected_element_original_vs_patched_model1_after_pixels"]>0 and
       m["removed_selected_element_original_vs_patched_model1_before_pixels"]==
       m["removed_selected_element_original_vs_patched_model1_after_pixels"]
       for m in measurements.values()
    )
    consistent=all(
        m["removed_selected_element_original_vs_patched_model1_before_pixels"]==
        m["removed_selected_element_original_vs_patched_model1_after_pixels"]
        for m in measurements.values())
    decision=("PASS_BOUNDED_AF121_SINGLE_SOURCE_RENDER_RESPONSE"
              if controls and consistent and response else
              "NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS"
              if controls and consistent and not response else
              "CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS")
    result={
       "schema":"MCFR_INT5_B16_AF121_ELEMENT_SELECTED_CHILD_ONLY_NATIVE_F2_CAUSAL_AUDIT/v1",
       "decision":decision,
       "runtime_version":VERSION,
       "tested_case":"AF121_north",
       "original_source_part_key":"/".join([SOURCE_KEY[0],SOURCE_KEY[1],str(SOURCE_INDEX)]),
       "source_role_hypothesis_not_function":ROLES[SOURCE_INDEX],
       "official_baseline_H15_zip_sha256":BASELINE_ARTIFACT_SHA256,
       "original_H15_native_F2_verified":8,
       "new_disposable_native_F2_verified":8,
       "two_separate_game_sessions_in_comparison":2,
       "new_exact_server_state_confirmations":8,
       "original_H15_game_log_sha256":baseline["client_log_sha256"],
       "new_disposable_game_log_sha256":document["client_log_sha256"],
       "original_F2_sha256":{h15.label(v,s):baseline["views"][v][s]["sha256"]
                             for v in VIEWS for s in STAGES},
       "modified_F2_sha256":{h15.label(v,s):document["views"][v][s]["sha256"]
                             for v in VIEWS for s in STAGES},
       "source_provenance":p,
       "per_camera_screen_response":measurements,
       "model3_negative_control_stayed_unchanged":all(
           m["original_model3_untouched_child_negative_pixels"]==0
           for m in measurements.values()),
       "air_and_temporal_negative_controls_stayed_unchanged":controls,
       "any_real_AF121_selected_element_removal_render_response":response,
       "unique_original_element_pixel_ownership_approved":False,
       "part_seating_or_function_approved":False,
       "part_material_or_style_approved":False,
       "INT5_final_semantics_approvals":0,
       "INT6_AI_training_or_redistribution_rights_approved":0,
       "original_F70_unconditional_approvals":0,
       "limits":[
           "Only AF121 north variant1 has a source-selected_element removal trial; other facings, modules and parts remain untested.",
           "Modified child overrides original inherited geometry in ONE disposable JAR member. Template and variant3 control child remain byte-identical.",
           "Removal screen changes may include revealed faces, occlusion and lighting; no direct exclusive original per-face/F2 pixel ownership proven.",
           "Four original H15 stages are unchanged baseline native PNGs, not newly reproduced source assets.",
           "No role-name-based physical function, texture material, style, training rights, or redistribution rights granted.",
           "B6 historical snapshot retained; previous B5/B7/B8/B9/B10 render responses never substitute for B16 real F2 evidence.",
       ],
    }
    (target/AUDIT).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--index",type=int,choices=tuple(FACES),required=True)
    parser.add_argument("--directory",type=Path,required=True)
    parser.add_argument("--h15-original-zip",type=Path,required=True)
    a=parser.parse_args()
    select_index(a.index)
    result=audit(a.directory,a.h15_original_zip)
    print(json.dumps(result,ensure_ascii=False))
    if result["decision"]=="CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS":
        raise SystemExit(1)

if __name__=="__main__":
    main()
