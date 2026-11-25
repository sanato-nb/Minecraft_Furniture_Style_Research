"""INT-5-B18 Macaw 12 original-source elements: real Fabric 1.21.11 isolated trials.

Each matrix job launches TWO actual Minecraft clients: original official JAR,
then the same original JAR with exactly one inherited source element removed
from ONE child model JSON. The original model parent, blockstate and vanilla
textures are untouched. Four stages x two cameras x two real sessions.
Screen causality is bounded; no function/material/UV ownership/rights approval.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
from time import sleep
from zipfile import ZipFile

from PIL import Image
from .chair_runtime_capture import (
    confirmed_camera_teleport,confirmed_spectator_mode,
    send_minecraft_command,archive_gui_diagnostic)
from .runtime_capture import wait_for
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15
from . import chair_runtime_fixture as fixture

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.11"
MOD="mcw-furniture-3.4.2-mc1.21.11fabric.jar"
OFFICIAL_SHA256="e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"
CHILD="assets/mcwfurnitures/models/block/chair/acacia_chair.json"
PARENT="assets/mcwfurnitures/models/block/parent/chair.json"
STATE_JSON="assets/mcwfurnitures/blockstates/acacia_chair.json"
ORIGINAL_PARENT_SHA256="26f389f8cc286dcdd97a608adf685294bcc2f60323e7b1ea40755b2110ff1650"
ORIGINAL_CHILD_SHA256="f0aeb2ad025179dfd68c63b3c2ea5a25ab8d4a7e3e161dc43f270772672bda3b"
ORIGINAL_BLOCKSTATE_SHA256="e6405186a33100104cb6dcbddd2cad774f157298cafe8e750dc228cd9ba24b95"
FACES=(5,4,5,5,5,5,5,5,5,4,5,6)
ROLES=("SEAT_LAYER","BACKREST_ASSEMBLY","LEG_OR_LOWER_POST",
       "LEG_OR_LOWER_POST","LEG_OR_LOWER_POST","LEG_OR_LOWER_POST",
       "BACKREST_ASSEMBLY","BACKREST_ASSEMBLY","BACKREST_ASSEMBLY",
       "BACKREST_ASSEMBLY","BACKREST_ASSEMBLY","SEAT_LAYER")
INDICES=tuple(range(12))
STAGES=("chair_before","control","chair_after","air")
VIEWS=("south","north")
CAMERAS={}
SOURCE_INDEX=0
SOURCE_KEY=("MACAW67","MACAW1424",0)
MANIFEST="INT5_B18_MACAW_TWO_GAME_SESSIONS_V1.json"
AUDIT="INT5_B18_MACAW_SINGLE_SOURCE_NATIVE_F2_AUDIT_V1.json"

def need(ok,reason):
    if not ok:
        raise ValueError("INT5-B18: "+reason)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def set_index(index):
    global SOURCE_INDEX,SOURCE_KEY
    need(index in INDICES,"index not in 12 original untested Macaw elements")
    SOURCE_INDEX=index
    SOURCE_KEY=("MACAW67","MACAW1424",index)

def source_role_check():
    source=ROOT/"project/integration/INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv"
    latest=ROOT/"project/integration/INT5_B17_FOUR_MODEL_45_ELEMENT_BATCH_STATUS_V1.csv"
    with source.open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    with latest.open(encoding="utf-8-sig",newline="") as f:
        states=list(csv.DictReader(f))
    need(len(rows)==len(states)==45,"original 45 source rows missing")
    src=[x for x in rows if x["child_model_key"]=="MACAW67" and
         x["provider_key"]=="MACAW1424" and
         x["original_source_element_index"]==str(SOURCE_INDEX)]
    pending=[x for x in states if x["model"]=="MACAW67" and
             x["provider"]=="MACAW1424" and x["index"]==str(SOURCE_INDEX)]
    need(len(src)==len(pending)==1 and
         pending[0]["state"]=="NOT_YET_TESTED" and
         src[0]["original_role_hypothesis"]==ROLES[SOURCE_INDEX] and
         int(src[0]["source_element_original_face_count"])==FACES[SOURCE_INDEX] and
         all(src[0][k]=="false" for k in
             ("individual_element_to_original_F2_pixels_approved",
              "part_function_verified","material_or_style_verified",
              "training_or_redistribution_rights_approved")),
         "source index/role/face count or rights drift")
    return src[0]

def case():
    found=[c for c in fixture.cases(VERSION) if c.case_id=="MACAW67_north"]
    need(len(found)==1,"original Macaw north chair case absent")
    x=found[0]
    need(x.model_key=="MACAW67" and x.state()=="mcwfurnitures:acacia_chair[facing=north]",
         "original north source state altered")
    return x

def coords():
    c=case()
    return c.x,c.y,c.z

def cameras():
    x,y,z=coords()
    return {"south":f"{x+0.5:g} {y+2.3:g} {z+5.5:g} 180 20",
            "north":f"{x+0.5:g} {y+2.3:g} {z-5.5:g} 0 20"}

def state(stage):
    need(stage in STAGES,"unknown Macaw chair/control stage")
    if stage=="control":return "minecraft:oak_stairs[facing=north]"
    if stage=="air":return "minecraft:air"
    return case().state()

def override_child(original_child,parent_raw,index):
    need(index in INDICES,"source index out of bounds")
    child=json.loads(original_child.decode("utf-8-sig"))
    parent=json.loads(parent_raw.decode("utf-8-sig"))
    need(isinstance(child,dict) and "elements" not in child and
         child.get("parent")=="mcwfurnitures:block/parent/chair",
         "original selected child must inherit correct Macaw chair parent")
    elements=parent.get("elements")
    need(isinstance(elements,list) and len(elements)==12 and
         sum(len(el.get("faces",{})) for el in elements)==59 and
         all(isinstance(el.get("faces"),dict) and "from" in el and "to" in el
             for el in elements) and len(elements[index]["faces"])==FACES[index],
         "official Macaw parent 12/59 or selected source faces differ")
    revised={**child,"elements":[e for j,e in enumerate(elements) if j!=index]}
    need(len(revised["elements"])==11 and
         sum(len(e["faces"]) for e in revised["elements"])==59-FACES[index] and
         revised["elements"]==elements[:index]+elements[index+1:] and
         {k:v for k,v in revised.items() if k!="elements"}==child,
         "changed more than one source element or parent/texture alias")
    return json.dumps(revised,ensure_ascii=False,separators=(",",":")).encode(),{
        "removed_source_index":index,
        "source_key":f"MACAW67/MACAW1424/{index}",
        "source_from":elements[index]["from"],
        "source_to":elements[index]["to"],
        "source_faces":sorted(elements[index]["faces"]),
        "source_face_count":FACES[index],
        "original_elements":12,"original_faces":59,
        "disposable_child_elements":11,"disposable_child_faces":59-FACES[index],
        "remaining_source_indices":[i for i in INDICES if i!=index],
        "original_parent_and_child_other_fields_unchanged":True,
    }

def original_release_preflight(game):
    jar=Path(game)/"mods"/MOD
    need(jar.is_file(),"Macaw pinned official 3.4.2 JAR missing")
    orig=jar.read_bytes()
    need(sha(orig)==OFFICIAL_SHA256,"official Macaw 3.4.2 JAR SHA256 mismatch")
    with ZipFile(io.BytesIO(orig)) as z:
        infos=z.infolist()
        names=[i.filename for i in infos]
        need(len(names)==len(set(names)) and z.testzip() is None,
             "official JAR member duplicate/CRC")
        need(all(k in names for k in (CHILD,PARENT,STATE_JSON)),
             "original child/parent/blockstate resource absent")
        b=z.read(CHILD);p=z.read(PARENT);s=z.read(STATE_JSON)
    need(sha(b)==ORIGINAL_CHILD_SHA256 and
         sha(p)==ORIGINAL_PARENT_SHA256 and
         sha(s)==ORIGINAL_BLOCKSTATE_SHA256,
         "released Macaw child, parent or state differs from research source")
    states=json.loads(s)
    need(set(states)=={"variants"} and
         "facing=north" in states["variants"] and
         states["variants"]["facing=north"]["model"]==
             "mcwfurnitures:block/chair/acacia_chair" and
         states["variants"]["facing=north"].get("y",0)==90,
         "actual Minecraft north model selection/rotation not pinned")
    source_role_check()
    child,meta=override_child(b,p,SOURCE_INDEX)
    need(child!=b,"disposable child byte identical")
    return {
        "official_MACAW_JAR_sha256":OFFICIAL_SHA256,
        "original_parent_sha256":sha(p),
        "original_child_sha256":sha(b),
        "original_blockstate_sha256":sha(s),
        "original_model_state":case().state(),
        "selected_source":meta,
        "original_mod_jar_member_count":len(names),
        "parent_model_and_selected_state_study_release_byte_identical":True,
    }

def patch_disposable_jar(game,pin):
    jar=Path(game)/"mods"/MOD
    source=jar.read_bytes()
    need(sha(source)==OFFICIAL_SHA256 and
         pin["official_MACAW_JAR_sha256"]==OFFICIAL_SHA256,
         "official source altered before intervention")
    with ZipFile(io.BytesIO(source)) as z:
        infos=z.infolist()
        members={i.filename:z.read(i.filename) for i in infos}
    revised,part=override_child(members[CHILD],members[PARENT],SOURCE_INDEX)
    tmp=jar.with_suffix(".b18-disposable")
    with ZipFile(tmp,"w") as z:
        for info in infos:
            z.writestr(info,revised if info.filename==CHILD else members[info.filename])
    with ZipFile(tmp) as z:
        need(z.testzip() is None and z.namelist()==[i.filename for i in infos],
             "temporary JAR damaged or member order changed")
        changed=[key for key in members if z.read(key)!=members[key]]
        need(changed==[CHILD] and
             all(z.read(key)==members[key] for key in members if key!=CHILD),
             "other model, state, texture, or file altered in disposable JAR")
    tmp.replace(jar)
    ephemeral=sha(jar.read_bytes())
    need(ephemeral!=OFFICIAL_SHA256,"experiment not patched")
    return {
        "modified_uncompressed_members_only":[CHILD],
        "original_parent_byte_identical":True,
        "original_blockstate_byte_identical":True,
        "all_other_original_zip_members_byte_identical":True,
        "disposable_jar_sha256":ephemeral,
        "official_source_sha256":OFFICIAL_SHA256,
        "modified_child_sha256":sha(revised),
        "modified_jar_or_third_party_textures_never_enter_Git_or_artifact":True,
        **part,
    }

def label(view,stage):
    need(view in VIEWS and stage in STAGES,"invalid view or stage")
    return view+"_"+stage

def capture_session(command,env,game,out,session,pin):
    out=Path(out)
    out.mkdir(parents=True,exist_ok=False)
    shots=Path(game)/"screenshots"
    log=out/"client.log"
    records={v:{} for v in VIEWS}
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(
                ["xdotool",*args],env=env,timeout=18,text=True).strip()
        def focus():xdo("windowfocus","--sync",window)
        def send(cmd):send_minecraft_command(xdo,cmd)
        def ack(cmd,marker,reason):
            for retry,limit in enumerate((25,35),1):
                focus();offset=len(read());send(cmd)
                try:
                    wait_for(proc,lambda:marker in read()[offset:],
                             "Macaw "+session+" "+reason+" attempt"+str(retry),limit)
                except ValueError as exc:
                    if not str(exc).startswith("Timed out waiting for") or retry==2:
                        raise
                    continue
                sleep(.5)
                return
            raise ValueError("Missing original Macaw server acknowledgement")
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "B18 Macaw source Minecraft joined",180)
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            need(len(windows)==1,"expected exactly one real client")
            window=windows[0]
            focus();sleep(2)
            confirmed_spectator_mode(proc,read,send,focus)
            ack("/function mcfr_chair:place","[RenderAudit] MCFR_CHAIR_PLACED","place")
            ack("/function mcfr_chair:verify","[RenderAudit] MCFR_CHAIR_STATES_READ","verify")
            shots.mkdir(exist_ok=True)
            for view in VIEWS:
                confirmed_camera_teleport(proc,read,send,focus,cameras()[view])
                for stage in STAGES:
                    key=label(view,stage)
                    block=state(stage)
                    if key!="south_chair_before":
                        x,y,z=coords()
                        ack(f"/setblock {x} {y} {z} {block}",
                            "[RenderAudit: Changed the block at","set "+key)
                    marker="MCFR_INT5_B18_"+session.upper()+"_"+key.upper()+"_SERVER=PASS"
                    x,y,z=coords()
                    ack(f"/execute if block {x} {y} {z} {block} run say {marker}",
                        "[RenderAudit] "+marker,"verify "+key)
                    sleep(5)
                    shot=h12.screenshot(xdo,window,shots,out,key,{"proc":proc})
                    records[view][stage]={
                        "state":block,"server_marker":marker,
                        "exact_server_verified":True,**shot
                    }
                    print("INT5_B18_REAL_F2",SOURCE_INDEX,session,key,flush=True)
        except Exception:
            archive_gui_diagnostic(out,"INT5_B18_"+session.upper()+"_GAME_FAILURE")
            raise
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    need(all(set(records[v])==set(STAGES) for v in VIEWS),
         "native F2/supported server states incomplete")
    doc={
       "schema":"MCFR_INT5_B18_EIGHT_NATIVE_F2_ONE_REAL_GAME/v1",
       "session":session,"version":VERSION,"source_key":SOURCE_KEY,
       "fixed_state":case().state(),"fixed_cameras":cameras(),
       "native_F2_count":8,"exact_server_states":8,
       "stages":records,
       "client_log_sha256":sha(log.read_bytes()),
       "official_parent_and_source_preflight":pin,
       "semantic_or_rights_approved":False,
    }
    (out/"manifest.json").write_text(
        json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return doc

def capture(command,env,game,out,version):
    need(version==VERSION,"Macaw F2 requires Minecraft Java 1.21.11")
    source_role_check()
    pin=original_release_preflight(game)
    game=Path(game)
    out=Path(out)
    out.mkdir(parents=True,exist_ok=False)
    worlds=[x for x in (game/"saves").iterdir()
            if x.is_dir() and (x/"level.dat").is_file()]
    need(len(worlds)==1,"expected one disposable official vanilla source world")
    world=worlds[0]
    pristine=game/"int5-b18-original-disposable-world-copy"
    need(not pristine.exists(),"world snapshot already exists")
    shutil.copytree(world,pristine,ignore=shutil.ignore_patterns("session.lock"))
    try:
        first=capture_session(command,env,game,out/"baseline","baseline",pin)
        shutil.rmtree(world)
        shutil.copytree(pristine,world,ignore=shutil.ignore_patterns("session.lock"))
        changed=patch_disposable_jar(game,pin)
        second=capture_session(command,env,game,out/"modified","modified",pin)
        need(first["native_F2_count"]==second["native_F2_count"]==8,
             "actual F2 16 screenshots not collected")
        doc={
            "schema":"MCFR_INT5_B18_MACAW_TWO_ACTUAL_GAME_SESSIONS/v1",
            "status":"TWO_ACTUAL_NATIVE_F2_SESSIONS_PENDING_INDEPENDENT_REOPEN",
            "source_key":list(SOURCE_KEY),
            "version":VERSION,
            "baseline_client":1,"modified_client":1,
            "baseline_native_F2":8,"modified_native_F2":8,
            "exact_server_states":16,
            "pristine_original_world_restored":True,
            "official_preflight":pin,
            "one_source_element_change":changed,
            "actual_game_session_files":{"baseline":"baseline/manifest.json",
                                         "modified":"modified/manifest.json"},
            "GPU_element_pixel_ownership_approved":False,
            "material_function_style_approved":False,
            "AI_training_redistribution_rights_approved":False,
        }
        (out/MANIFEST).write_text(
            json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
            encoding="utf-8")
        return doc
    finally:
        if pristine.exists():shutil.rmtree(pristine)

def open_png(raw):
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        need(im.format=="PNG" and im.size==(1024,684),
             "real Minecraft screenshot invalid size/format")
        return im.convert("RGB")

def measure(base,change):
    results={}
    for view in VIEWS:
        a,b=base[view],change[view]
        foreground=h15.pixel_changes(a["chair_before"],a["air"])
        before=h15.pixel_changes(a["chair_before"],b["chair_before"])
        after=h15.pixel_changes(a["chair_after"],b["chair_after"])
        control=h15.pixel_changes(a["control"],b["control"])
        air=h15.pixel_changes(a["air"],b["air"])
        old_time=h15.pixel_changes(a["chair_before"],a["chair_after"])
        new_time=h15.pixel_changes(b["chair_before"],b["chair_after"])
        results[view]={
            "original_macaw_chair_foreground_pixels":len(foreground),
            "selected_source_element_removed_before_pixels":len(before),
            "selected_source_element_removed_after_pixels":len(after),
            "unchanged_vanilla_control_pixels":len(control),
            "air_negative_control_pixels":len(air),
            "original_session_temporal_pixels":len(old_time),
            "modified_session_temporal_pixels":len(new_time),
            "changed_pixels_outside_original_chair_foreground":len(before-foreground),
        }
    return results

def audit(directory):
    out=Path(directory)
    doc=json.loads((out/MANIFEST).read_text(encoding="utf-8"))
    need(doc["schema"]=="MCFR_INT5_B18_MACAW_TWO_ACTUAL_GAME_SESSIONS/v1"
         and doc["status"]=="TWO_ACTUAL_NATIVE_F2_SESSIONS_PENDING_INDEPENDENT_REOPEN"
         and doc["source_key"]==list(SOURCE_KEY) and doc["version"]==VERSION
         and doc["baseline_native_F2"]==doc["modified_native_F2"]==8
         and doc["exact_server_states"]==16
         and doc["pristine_original_world_restored"] is True,
         "two original real game source sessions incomplete")
    pin=doc["official_preflight"]
    patch=doc["one_source_element_change"]
    need(pin["official_MACAW_JAR_sha256"]==OFFICIAL_SHA256 and
         pin["original_parent_sha256"]==ORIGINAL_PARENT_SHA256 and
         pin["original_child_sha256"]==ORIGINAL_CHILD_SHA256 and
         pin["original_blockstate_sha256"]==ORIGINAL_BLOCKSTATE_SHA256 and
         patch["removed_source_index"]==SOURCE_INDEX and
         patch["source_face_count"]==FACES[SOURCE_INDEX] and
         patch["source_key"]==f"MACAW67/MACAW1424/{SOURCE_INDEX}" and
         patch["modified_uncompressed_members_only"]==[CHILD] and
         patch["disposable_child_elements"]==11 and
         patch["disposable_child_faces"]==59-FACES[SOURCE_INDEX] and
         patch["original_parent_byte_identical"] is True and
         patch["original_blockstate_byte_identical"] is True and
         patch["all_other_original_zip_members_byte_identical"] is True,
         "actual pinned original source or only-one-child modification not proven")
    frames={};logs={};manifests={}
    for session in ("baseline","modified"):
        sub=out/session
        m=json.loads((sub/"manifest.json").read_text(encoding="utf-8"))
        need(doc["actual_game_session_files"][session]==session+"/manifest.json"
             and m["schema"]=="MCFR_INT5_B18_EIGHT_NATIVE_F2_ONE_REAL_GAME/v1"
             and m["source_key"]==list(SOURCE_KEY)
             and m["session"]==session and m["version"]==VERSION
             and m["fixed_state"]==case().state()
             and m["fixed_cameras"]==cameras()
             and m["native_F2_count"]==m["exact_server_states"]==8,
             "real source/game session manifest mismatched")
        log=(sub/"client.log").read_bytes()
        need(sha(log)==m["client_log_sha256"] and
             "Reloading ResourceManager:" in log.decode("utf-8",errors="replace")
             and "mcwfurnitures" in log.decode("utf-8",errors="replace"),
             "actual Macaw game client log or SHA missing")
        text=log.decode("utf-8",errors="replace")
        imgs={}
        need(set(m["stages"])==set(VIEWS),"missing original F2 views")
        for view in VIEWS:
            need(set(m["stages"][view])==set(STAGES),"missing native screenshot stages")
            imgs[view]={}
            for stage in STAGES:
                row=m["stages"][view][stage]
                key=label(view,stage)
                need(row["image"]==key+".png" and
                     row["dimensions"]==[1024,684] and
                     row["state"]==state(stage) and
                     row["exact_server_verified"] is True and
                     "[RenderAudit] "+row["server_marker"] in text,
                     "actual server state, native F2 metadata or case drift "+key)
                raw=(sub/row["image"]).read_bytes()
                need(sha(raw)==row["sha256"],"actual native F2 PNG SHA mismatch")
                imgs[view][stage]=open_png(raw)
        frames[session]=imgs;logs[session]=sha(log);manifests[session]=m
    metrics=measure(frames["baseline"],frames["modified"])
    controls=all(
        m["unchanged_vanilla_control_pixels"]==0 and
        m["air_negative_control_pixels"]==0 and
        m["original_session_temporal_pixels"]==0 and
        m["modified_session_temporal_pixels"]==0 and
        m["changed_pixels_outside_original_chair_foreground"]==0
        for m in metrics.values())
    consistent=all(
        m["selected_source_element_removed_before_pixels"]==
        m["selected_source_element_removed_after_pixels"]
        for m in metrics.values())
    visible=any(
        m["selected_source_element_removed_before_pixels"]>0
        for m in metrics.values())
    decision=("PASS_BOUNDED_MACAW_SINGLE_SOURCE_RENDER_RESPONSE"
              if controls and consistent and visible else
              "NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS"
              if controls and consistent and not visible else
              "CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS")
    result={
        "schema":"MCFR_INT5_B18_MACAW_SINGLE_SOURCE_REAL_F2_AUDIT/v1",
        "source_key":f"MACAW67/MACAW1424/{SOURCE_INDEX}",
        "source_index":SOURCE_INDEX,
        "source_faces":FACES[SOURCE_INDEX],
        "source_role_hypothesis_not_function":ROLES[SOURCE_INDEX],
        "decision":decision,
        "official_JAR_sha256":OFFICIAL_SHA256,
        "original_parent_sha256":ORIGINAL_PARENT_SHA256,
        "original_child_sha256":ORIGINAL_CHILD_SHA256,
        "original_state_sha256":ORIGINAL_BLOCKSTATE_SHA256,
        "real_original_native_F2":8,"real_modified_native_F2":8,
        "real_exact_server_checks":16,
        "two_separate_game_sessions":2,
        "original_client_log_sha256":logs["baseline"],
        "modified_client_log_sha256":logs["modified"],
        "baseline_native_F2_sha256":{
            label(v,s):manifests["baseline"]["stages"][v][s]["sha256"]
            for v in VIEWS for s in STAGES},
        "modified_native_F2_sha256":{
            label(v,s):manifests["modified"]["stages"][v][s]["sha256"]
            for v in VIEWS for s in STAGES},
        "single_original_element_change_provenance":patch,
        "per_view":metrics,
        "unchanged_vanilla_and_air_and_time_controls":controls,
        "repeated_A_screen_response_consistent":consistent,
        "detected_render_change":visible,
        "exclusive_GPU_source_face_pixel_ownership_approved":False,
        "part_function_material_style_semantics_approved":False,
        "INT6_AI_training_and_redistribution_rights_approved":False,
        "strict_H03_H05_full_exit":False,"strict_F70_unconditional":0,
        "limits":[
            "Only Macaw acacia chair original 3.4.2, north facing state and two cameras tested.",
            "One-element removal changes visual occlusion; changed pixels are not exclusive original face ownership.",
            "An invisible element at both cameras does not prove unused geometry or a bug.",
            "Original material, seat mechanics, style, training and redistribution permission are not approved.",
            "The official JAR is modified only in disposable CI and never in Git or F2 artifact.",
        ],
    }
    (out/AUDIT).write_text(
        json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--index",type=int,choices=INDICES,required=True)
    p.add_argument("--directory",type=Path,required=True)
    a=p.parse_args()
    set_index(a.index)
    r=audit(a.directory)
    print(json.dumps(r,ensure_ascii=False,sort_keys=True))
    if r["decision"]=="CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS":
        raise SystemExit(1)

if __name__=="__main__":
    main()
