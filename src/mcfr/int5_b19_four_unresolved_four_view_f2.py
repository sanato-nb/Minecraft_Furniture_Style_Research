"""INT-5-B19: four prior 0-pixel original elements, four-view native Fabric F2.

Independent official and disposable game sessions for AF121/5, AF123/5,
HC11210/3 and HC11210/4. Uses pinned, previously proven model-child-only
patches from B15/B16/B17 and exact blockstates/slab/white negative controls.
A removed source can be occluded or fail to produce visible pixels in any view;
no finding promotes function, texture/material/style, face/UV pixel ownership,
training, redistribution or the legacy unconditional F70 gate.
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

from . import int5_b16_af121_six_element_batch_f2 as af1
from . import int5_b15_af123_six_element_batch_f2 as af10
from . import int5_b17_hc_twelve_element_batch_f2 as hc17
from . import int5_b8_hc_cushion_source_preflight as hc
from . import int5_af_tucked_slab_control as slab
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15
from .chair_runtime_capture import (
    confirmed_camera_teleport,confirmed_spectator_mode,
    send_minecraft_command,archive_gui_diagnostic)
from .runtime_capture import wait_for

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.1"
TARGETS={
    "AF121_5":("AF121","AF1393",5,4),
    "AF123_5":("AF123","AF1394",5,4),
    "HC11210_3":("HC11210","HC13",3,6),
    "HC11210_4":("HC11210","HC13",4,6),
}
VIEWS=("south","north","east","west")
ORIGINAL="INT5_B19_FOUR_VIEW_TWO_GAME_SESSION_MANIFEST_V1.json"
AUDIT="INT5_B19_FOUR_VIEW_ORIGINAL_SOURCE_CAUSAL_AUDIT_V1.json"
CHOSEN="AF121_5"

def need(ok,reason):
    if not ok:raise ValueError("INT5-B19: "+reason)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def set_target(value):
    global CHOSEN
    need(value in TARGETS,"target is not one of four previously invisible originals")
    CHOSEN=value

def source():
    m,p,index,faces=TARGETS[CHOSEN]
    b3=ROOT/"project/integration/INT5_B3_45_PART_ROLE_TEXTURE_CUE_DECISIONS_V1.csv"
    previous=ROOT/"project/integration/INT5_B18_FOUR_MODEL_45_ELEMENT_BATCH_STATUS_V1.csv"
    with b3.open(encoding="utf-8-sig",newline="") as s:source=list(csv.DictReader(s))
    with previous.open(encoding="utf-8-sig",newline="") as s:status=list(csv.DictReader(s))
    need(len(source)==len(status)==45,"B3 and completed B18 45-part ledgers required")
    k=(m,p,str(index))
    original=[r for r in source if
              (r["child_model_key"],r["provider_key"],r["original_source_element_index"])==k]
    recent=[r for r in status if (r["model"],r["provider"],r["index"])==k]
    need(len(original)==len(recent)==1 and
         recent[0]["state"].endswith("NO_VISIBLE_RESPONSE") and
         int(recent[0]["faces"])==faces and
         int(original[0]["source_element_original_face_count"])==faces and
         all(original[0][key]=="false" for key in
             ("individual_element_to_original_F2_pixels_approved",
              "part_function_verified","material_or_style_verified",
              "training_or_redistribution_rights_approved")),
         "selected source is not an exact previously unproven original")
    return {"source_key":"/".join(k),"source_element_index":index,
            "source_faces":faces,
            "original_role_hypothesis":original[0]["original_role_hypothesis"],
            "B18_prior_state":recent[0]["state"],
            "B18_prior_south_pixels":int(recent[0]["south_changed_pixels"]),
            "B18_prior_north_pixels":int(recent[0]["north_changed_pixels"])}

def case():
    if CHOSEN.startswith("AF121"):
        from .chair_runtime_fixture import cases
        found=[x for x in cases(VERSION) if x.case_id=="AF121_north"]
        need(len(found)==1 and found[0].state()==h15.stage_state("model1_before"),
             "AF121 original pinned case changed")
        return found[0]
    if CHOSEN.startswith("AF123"):return slab.target_case()
    return hc17.pinned_chair_case()

def coords():
    c=case()
    return (c.x,c.y,c.z)

def cameras():
    x,y,z=coords()
    old=case().camera()
    return {
        "south":old,
        "north":f"{x+0.5:g} {y+2.3:g} {z-5.5:g} 0 20",
        "east":f"{x+5.5:g} {y+2.3:g} {z+0.5:g} 90 20",
        "west":f"{x-5.5:g} {y+2.3:g} {z+0.5:g} -90 20",
    }

def stages():
    if CHOSEN.startswith("AF121"):return ("model1_before","model3","model1_after","air")
    if CHOSEN.startswith("AF123"):return slab.STAGES
    return hc17.STAGES

def block(stage):
    need(stage in stages(),"stage not in original real source family")
    if CHOSEN.startswith("AF121"):return h15.stage_state(stage)
    if CHOSEN.startswith("AF123"):return slab.stage_chair_state(stage)
    return hc17.state(stage)

def support(stage):
    need(stage in stages(),"invalid source stage")
    return slab.stage_slab_state(stage) if CHOSEN.startswith("AF123") else None

def identity():
    info=source()
    c=case()
    need(c.version==VERSION and c.facing=="north" and c.y==120 and
         (c.x,c.z)==((8,40) if CHOSEN.startswith("AF123") else
                      (-88,40) if CHOSEN.startswith("AF121") else (40,40)),
         "original fixture block positions changed")
    return {"target":CHOSEN,"source":info,"source_case":c.case_id,
            "state":c.state(),"coords":list(coords()),"cameras":cameras(),
            "original_source_views":["south","north"],"new_unbiased_side_views":["east","west"],
            "stages":list(stages()),"original_minecraft":VERSION}

def preflight(game):
    info=identity()
    game=Path(game)
    if CHOSEN.startswith("AF"):
        pins=h12.static_preflight(game)
        # Do not assume studied AF 4.0.3 bytes equal running official 4.0.2.
        need(pins["actual_runtime_provenance"] and
             (game/"mods"/af1.JAR_NAME).is_file(),"real official Another Furniture source missing")
        if CHOSEN.startswith("AF121"):
            need(h15.stage_state("model3")!=h15.stage_state("model1_before"),
                 "unaltered model3 negative control is not distinct")
        else:
            need(slab.stage_chair_state("slab_only")=="minecraft:air" and
                 slab.stage_slab_state("slab_only")==slab.SLAB,
                 "legal tucked original top slab stage not pinned")
        checksum=hashlib.sha1((game/"mods"/af1.JAR_NAME).read_bytes()).hexdigest()
        need(checksum==h12.JAR_SHA1,"official AF 4.0.2 JAR changed")
        result={"family":"AF","official_JAR_sha1":checksum,
                "official_source_run_preflight":pins,
                "no_released_artwork_added":True}
    else:
        p=hc.original_release_preflight(game/"mods"/hc.MOD)
        need(p["official_jar_sha1"]==hc.SHA1 and
             p["source_element_index"]==12 and
             p["original_black_13_elements_78_faces"] is True and
             p["white_control_distinct_child"] is True,
             "original official HC parent/black/white source preflight drift")
        result={"family":"HC","official_JAR_sha1":hc.SHA1,
                "official_source_run_preflight":p,
                "no_released_artwork_added":True}
    return {**info,"pinned_original":result}

def patch(game,checked):
    if CHOSEN=="AF121_5":
        af1.select_index(5)
        r=af1.prepare_disposable_child(game)
        need(r["removed_source_index"]==5 and r["child_new_face_count"]==42 and
             r["all_other_uncompressed_members_byte_identical"] is True and
             r["original_parent_unmodified"] is True and
             r["acacia3_negative_control_unmodified"] is True,
             "AF121 original source5 not isolated")
        return {"changed_resource":af1.CHILD,"original_source_scope":r}
    if CHOSEN=="AF123_5":
        r=af10.prepare(game,5)
        need(r["original_element_index"]==5 and
             r["disposable_child_faces"]==42 and
             r["only_one_original_uncompressed_member_changed"] is True and
             r["shared_parent_and_other_resources_byte_identical"] is True,
             "AF123 supported tucked element5 not isolated")
        return {"changed_resource":af10.CHILD,"original_source_scope":r}
    idx=TARGETS[CHOSEN][2]
    hc17.select_index(idx)
    pre=checked["pinned_original"]["official_source_run_preflight"]
    r=hc17.prepare_disposable_child(game,pre)
    need(r["removed_original_element_index"]==idx and
         r["original_parent_elements"]==13 and
         r["isolated_black_child_faces"]==72 and
         r["changed_zip_resource_members"]==[hc.member(hc.CHILD)] and
         r["original_white_control_child_unchanged"] is True and
         r["original_shared_parent_unchanged"] is True,
         "Handcrafted original plane element not isolated")
    return {"changed_resource":hc.member(hc.CHILD),"original_source_scope":r}

def label(view,stage):
    need(view in VIEWS and stage in stages(),"source F2 view/stage label changed")
    return view+"_"+stage

def capture_session(command,env,game,out,session,checked):
    out=Path(out)
    out.mkdir(parents=True,exist_ok=False)
    log=out/"client.log"
    shots=Path(game)/"screenshots"
    rows={view:{} for view in VIEWS}
    initial=stages()[0]
    x,y,z=coords()
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],
                                           env=env,text=True,timeout=18).strip()
        def focus():xdo("windowfocus","--sync",window)
        def send(cmd):send_minecraft_command(xdo,cmd)
        def ack(command,marker,what):
            for attempt,limit in enumerate((25,35),1):
                focus();start=len(read());send(command)
                try:
                    wait_for(proc,lambda:marker in read()[start:],
                             "B19 "+session+" "+what+" "+str(attempt),limit)
                except ValueError as exc:
                    if not str(exc).startswith("Timed out waiting for") or attempt==2:
                        raise
                    continue
                sleep(.6)
                return
            raise ValueError("B19 actual game server did not acknowledge "+what)
        def setblock(pos,target,what):
            cx,cy,cz=pos
            ack(f"/setblock {cx} {cy} {cz} {target}",
                "[RenderAudit: Changed the block at",what)
        def readback(view,stage):
            name=label(view,stage)
            prefix="MCFR_INT5_B19_"+CHOSEN.upper()+"_"+session.upper()+"_"+name.upper()
            records={}
            for title,pos,state in [("CHAIR",(x,y,z),block(stage))]+(
               [("SUPPORT",slab.slab_xyz(),support(stage))]
               if CHOSEN.startswith("AF123") else []):
                marker=prefix+"_"+title+"=PASS"
                cx,cy,cz=pos
                ack(f"/execute if block {cx} {cy} {cz} {state} run say {marker}",
                    "[RenderAudit] "+marker,
                    "actual "+title+" blockstate "+name)
                records[title]=marker
            if CHOSEN.startswith("HC"):
                # Color changes may create dropped item entities that mimic missing pixels.
                focus()
                send("/kill @e[type=minecraft:item]");sleep(.7)
                marker=prefix+"_NO_DROPPED_ITEM=PASS"
                ack(f"/execute unless entity @e[type=minecraft:item] run say {marker}",
                    "[RenderAudit] "+marker,"no entity in real world "+name)
                records["NO_ITEM"]=marker
            return records
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "B19 original game client joined",180)
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            need(len(windows)==1,"exactly one live original Minecraft GUI required")
            window=windows[0];focus();sleep(2)
            confirmed_spectator_mode(proc,read,send,focus)
            ack("/function mcfr_chair:place",
                "[RenderAudit] MCFR_CHAIR_PLACED","source chair placed")
            ack("/function mcfr_chair:verify",
                "[RenderAudit] MCFR_CHAIR_STATES_READ","server source state verified")
            shots.mkdir(exist_ok=True)
            for view in VIEWS:
                confirmed_camera_teleport(proc,read,send,focus,cameras()[view])
                for stage in stages():
                    key=label(view,stage)
                    if CHOSEN.startswith("AF123"):
                        if stage=="chair_plus_slab_before":
                            if view!="south":
                                setblock(slab.slab_xyz(),slab.SLAB,
                                         "restore original legal top-slab before tucked chair")
                                setblock((x,y,z),block(stage),
                                         "restore pinned tucked source chair")
                        elif stage=="slab_only":
                            setblock((x,y,z),"minecraft:air","remove chair retain legal slab")
                        elif stage=="chair_plus_slab_after":
                            setblock((x,y,z),block(stage),"restore source chair same legal slab")
                        elif stage=="empty":
                            setblock((x,y,z),"minecraft:air","remove original tucked chair")
                            setblock(slab.slab_xyz(),"minecraft:air","remove slab after chair")
                    elif not(view=="south" and stage==initial):
                        setblock((x,y,z),block(stage),"restore exact source or negative control")
                    markers=readback(view,stage)
                    sleep(4 if CHOSEN.startswith("AF123") else 5)
                    screen=h12.screenshot(xdo,window,shots,out,key,{"proc":proc})
                    rows[view][stage]={
                        "chair_state":block(stage),
                        "slab_state":support(stage),
                        "server_markers":markers,
                        "exact_state_checked":True,
                        "dropped_items_zero_verified":CHOSEN.startswith("HC"),
                        **screen,
                    }
                    print("INT5_B19_NATIVE_F2",CHOSEN,session,key,flush=True)
        except Exception:
            archive_gui_diagnostic(out,"INT5_B19_"+CHOSEN+"_"+session+"_REAL_GAME_FAILURE")
            raise
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    need(set(rows)==set(VIEWS) and all(set(v)==set(stages()) for v in rows.values()),
         "actual 4 cameras x 4 stages missing")
    doc={
        "schema":"MCFR_INT5_B19_FOUR_VIEW_ONE_REAL_FABRIC_CLIENT/v1",
        "source":checked["source"],"target":CHOSEN,"session":session,
        "exact_game_version":VERSION,"fixed_cameras":cameras(),
        "fixed_stages":list(stages()),"original_world_case":case().case_id,
        "new_real_native_F2":16,"exact_server_state_proofs":16*(2 if CHOSEN.startswith("AF123") else 1),
        "zero_dropped_item_server_proofs":16 if CHOSEN.startswith("HC") else 0,
        "f2_records":rows,"client_log_sha256":sha(log.read_bytes()),
        "element_function_material_style_rights_approved":False,
    }
    (out/"manifest.json").write_text(
        json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return doc

def capture(command,env,game,out,version):
    need(version==VERSION,"B19 original source mods use Java 1.21.1 Fabric")
    checked=preflight(game)
    game,out=Path(game),Path(out)
    out.mkdir(parents=True,exist_ok=False)
    worlds=[x for x in (game/"saves").iterdir() if x.is_dir() and
            (x/"level.dat").is_file()]
    need(len(worlds)==1,"expected exactly one generated disposable world")
    world=worlds[0];snapshot=game/"int5-b19-pristine-world"
    need(not snapshot.exists(),"original pristine snapshot already exists")
    shutil.copytree(world,snapshot,ignore=shutil.ignore_patterns("session.lock"))
    try:
        baseline=capture_session(command,env,game,out/"baseline","baseline",checked)
        shutil.rmtree(world)
        shutil.copytree(snapshot,world,ignore=shutil.ignore_patterns("session.lock"))
        intervention=patch(game,checked)
        modified=capture_session(command,env,game,out/"modified","modified",checked)
        need(baseline["new_real_native_F2"]==modified["new_real_native_F2"]==16,
             "two actual sessions must capture 16 independent F2 each")
        doc={
            "schema":"MCFR_INT5_B19_FOUR_ORIGINAL_UNRESOLVED_EAST_WEST_NATIVE_F2/v1",
            "status":"ORIGINAL_AND_MODIFIED_FOUR_VIEW_F2_AWAITING_INDEPENDENT_AUDIT",
            "selected_source":checked["source"],"target":CHOSEN,
            "game_version":VERSION,
            "pristine_world_restored_between_games":True,
            "game_sessions":2,"actual_native_F2_total":32,
            "four_cameras":cameras(),"stages":list(stages()),
            "original_model_verified_preflight":checked["pinned_original"],
            "only_source_child_element_modified":intervention,
            "GPU_face_pixel_owner_or_semantic_rights_approved":False,
            "manifest_paths":{"baseline":"baseline/manifest.json",
                              "modified":"modified/manifest.json"},
        }
        (out/ORIGINAL).write_text(
            json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
            encoding="utf-8")
        return doc
    finally:
        if snapshot.exists():shutil.rmtree(snapshot)

def image_bytes(raw):
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        need(im.size==(1024,684) and im.format=="PNG",
             "not original native F2 1024x684 PNG")
        return im.convert("RGB")

def compare(base,modified):
    before,control,after,air=stages()
    result={}
    for v in VIEWS:
        a,b=base[v],modified[v]
        fg=h15.pixel_changes(a[before],a[air])
        first=h15.pixel_changes(a[before],b[before])
        again=h15.pixel_changes(a[after],b[after])
        stable_control=h15.pixel_changes(a[control],b[control])
        stable_air=h15.pixel_changes(a[air],b[air])
        old_time=h15.pixel_changes(a[before],a[after])
        new_time=h15.pixel_changes(b[before],b[after])
        result[v]={
            "original_chair_foreground_pixels":len(fg),
            "new_source_intervention_before_pixels":len(first),
            "new_source_intervention_after_pixels":len(again),
            "unchanged_negative_control_pixels":len(stable_control),
            "unchanged_air_and_support_pixels":len(stable_air),
            "baseline_A_A_temporal_pixels":len(old_time),
            "modified_A_A_temporal_pixels":len(new_time),
            "intervention_outside_original_foreground_pixels":len(first-fg),
        }
    return result

def audit(folder):
    folder=Path(folder)
    overall=json.loads((folder/ORIGINAL).read_text(encoding="utf-8"))
    orig=source()
    need(overall["schema"]=="MCFR_INT5_B19_FOUR_ORIGINAL_UNRESOLVED_EAST_WEST_NATIVE_F2/v1"
         and overall["status"]=="ORIGINAL_AND_MODIFIED_FOUR_VIEW_F2_AWAITING_INDEPENDENT_AUDIT"
         and overall["selected_source"]==orig and
         overall["target"]==CHOSEN and overall["game_version"]==VERSION and
         overall["pristine_world_restored_between_games"] is True and
         overall["game_sessions"]==2 and overall["actual_native_F2_total"]==32 and
         overall["four_cameras"]==cameras() and
         overall["stages"]==list(stages()),"actual source or game sessions missing")
    modified=overall["only_source_child_element_modified"]
    child=modified["changed_resource"]
    provenance=modified["original_source_scope"]
    name=provenance.get("removed_source_index",provenance.get("original_element_index",
         provenance.get("removed_original_element_index")))
    need(int(name)==orig["source_element_index"] and
         provenance.get("source_element_face_count",len(provenance.get("removed_source_element_faces",[]))
             if "removed_source_element_faces" in provenance else
             len(provenance.get("original_element_faces",[])))==orig["source_faces"] or
         provenance.get("source_element_face_count")==orig["source_faces"] or
         provenance.get("original_source_element_face_count")==orig["source_faces"],
         "changed original index/face count not pinned")
    need(child in (af1.CHILD,af10.CHILD,hc.member(hc.CHILD)),
         "original child-only resource not selected")
    base_and_changed={};log_sha={};screens_sha={}
    for session in ("baseline","modified"):
        path=folder/session
        doc=json.loads((path/"manifest.json").read_text(encoding="utf-8"))
        need(overall["manifest_paths"][session]==session+"/manifest.json"
             and doc["schema"]=="MCFR_INT5_B19_FOUR_VIEW_ONE_REAL_FABRIC_CLIENT/v1"
             and doc["session"]==session and doc["source"]==orig and
             doc["fixed_cameras"]==cameras() and
             doc["fixed_stages"]==list(stages()) and
             doc["new_real_native_F2"]==16 and
             doc["target"]==CHOSEN and
             doc["exact_server_state_proofs"]==16*(2 if CHOSEN.startswith("AF123") else 1)
             and doc["zero_dropped_item_server_proofs"]==(16 if CHOSEN.startswith("HC") else 0),
             "actual source family real game screenshot/server markers missing")
        log=(path/"client.log").read_bytes()
        need(sha(log)==doc["client_log_sha256"],"actual game client log SHA drift")
        txt=log.decode("utf-8",errors="replace")
        need("Reloading ResourceManager:" in txt and
             ("another_furniture" if CHOSEN.startswith("AF") else "handcrafted") in txt,
             "Minecraft actual source model resource reload missing")
        log_sha[session]=sha(log);frames={};hashes={}
        need(set(doc["f2_records"])==set(VIEWS),"all 4 source cameras absent")
        for v in VIEWS:
            need(set(doc["f2_records"][v])==set(stages()),
                 "all 4 original/control/return/AIR stages missing")
            frames[v]={}
            for step in stages():
                item=doc["f2_records"][v][step]
                key=label(v,step)
                need(item["image"]==key+".png" and
                     item["dimensions"]==[1024,684] and
                     item["chair_state"]==block(step) and
                     item["slab_state"]==support(step) and
                     item["exact_state_checked"] is True,
                     "native screenshot or actual original game-state identity mismatch")
                expected_keys={"CHAIR","SUPPORT"} if CHOSEN.startswith("AF123") else {"CHAIR"}
                if CHOSEN.startswith("HC"):expected_keys.add("NO_ITEM")
                need(set(item["server_markers"])==expected_keys and
                     all("[RenderAudit] "+marker in txt for marker in item["server_markers"].values()),
                     "server block state or dropped-item proof not present in real log")
                data=(path/item["image"]).read_bytes()
                need(sha(data)==item["sha256"],"real F2 image SHA invalid "+key)
                frames[v][step]=image_bytes(data)
                hashes[key]=sha(data)
        base_and_changed[session]=frames
        screens_sha[session]=hashes
    metrics=compare(base_and_changed["baseline"],base_and_changed["modified"])
    stable=all(
        x["unchanged_negative_control_pixels"]==0 and
        x["unchanged_air_and_support_pixels"]==0 and
        x["baseline_A_A_temporal_pixels"]==0 and
        x["modified_A_A_temporal_pixels"]==0 and
        x["intervention_outside_original_foreground_pixels"]==0 and
        x["new_source_intervention_before_pixels"]==
           x["new_source_intervention_after_pixels"]
        for x in metrics.values())
    side=any(metrics[v]["new_source_intervention_before_pixels"]>0
             for v in ("east","west"))
    old=any(metrics[v]["new_source_intervention_before_pixels"]>0
            for v in ("south","north"))
    decision=(
       "PASS_NEW_EAST_WEST_NATIVE_F2_BOUNDED_SOURCE_CAUSAL_RESPONSE"
       if stable and side else
       "PASS_NEW_SOUTH_NORTH_NATIVE_F2_RESPONSE_WITH_NO_SIDE_RESPONSE"
       if stable and old else
       "NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_FOUR_VIEW_CONTROLS"
       if stable else
       "CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS")
    result={
        "schema":"MCFR_INT5_B19_FOUR_CAMERA_FOUR_UNRESOLVED_SOURCE_REAL_F2_INDEPENDENT_AUDIT/v1",
        "source_key":orig["source_key"],"original_source_index":orig["source_element_index"],
        "original_source_face_count":orig["source_faces"],
        "original_role_hypothesis_not_final":orig["original_role_hypothesis"],
        "prior_B18_south_north_status":orig["B18_prior_state"],
        "prior_B18_south_north_pixels":[orig["B18_prior_south_pixels"],orig["B18_prior_north_pixels"]],
        "decision":decision,"actual_game_version":VERSION,
        "official_source_release_preflight":overall["original_model_verified_preflight"],
        "source_model_one_child_intervention":modified,
        "new_actual_native_F2_images":32,
        "baseline_native_F2_verified":16,
        "modified_native_F2_verified":16,
        "server_state_proofs_total":64 if CHOSEN.startswith("AF123") else 32,
        "dropped_item_entity_absent_server_proofs":32 if CHOSEN.startswith("HC") else 0,
        "four_view_pixel_response":metrics,
        "four_camera_poses":cameras(),
        "real_original_and_disposable_client_log_SHA256":log_sha,
        "real_F2_SHA256_by_session":screens_sha,
        "four_view_negative_controls_passed":stable,
        "new_east_west_visually_causal":side if stable else False,
        "additional_south_north_response":old if stable else False,
        "exclusive_source_face_GPU_pixel_ownership_approved":False,
        "physical_function_material_style_approved":False,
        "AI_training_redistribution_rights_approved":False,
        "F70_unconditional_approved":0,
        "legacy_H03_H05_exit_approved":False,
        "caveats":[
          "Single source element deletion only proves bounded visibility of a structural intervention.",
          "Four cameras of one original furniture state do not prove source-face UV exclusive ownership.",
          "Prior zero-delta is retained as an original historical observation, never overwritten.",
          "Functional seating, style/material, and third-party training/redistribution rights remain unapproved.",
        ],
    }
    (folder/AUDIT).write_text(
        json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return result

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target",choices=tuple(TARGETS),required=True)
    p.add_argument("--directory",type=Path,required=True)
    args=p.parse_args(argv)
    set_target(args.target)
    result=audit(args.directory)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))
    if result["decision"]=="CONDITIONAL_FAILED_OR_DRIFTED_SCREEN_CONTROLS":
        raise SystemExit(1)

if __name__=="__main__":
    main()
