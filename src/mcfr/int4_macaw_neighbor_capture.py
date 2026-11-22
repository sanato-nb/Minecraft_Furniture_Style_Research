"""INT-4 original Macaw table *neighbor update* trial in real Fabric 1.21.11.

This is NOT player-item placement. /setblock requests block placement and
neighbor updates, and the game's integrated server reports resulting states.
Do not assume dynamic connection succeeds from source blockstate names.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from time import sleep

from .chair_runtime_fixture import Y
from .runtime_capture import wait_for
from .int4_macaw_table_shelf_capture import verify_running_source, MACAW_SHA256

VERSION="1.21.11"
STAGES=("reset","join","remove")
CENTRE=(0,Y,40)
EAST=(1,Y,40)
OUTCOME="INT4_MACAW_TABLE_NEIGHBOR_ACTUAL_GAME.json"
AUDIT="INT4_MACAW_TABLE_NEIGHBOR_AUDIT.json"
CONTACT="INT4_MACAW_TABLE_NEIGHBOR_F2_CONTACT.png"
TABLE="mcwfurnitures:oak_table"
SIGNAL="MCFR_NEIGHBOR_"

def check(cond,message):
    if not cond:raise ValueError(message)
def digest(blob):return hashlib.sha256(blob).hexdigest()

def pack_lines():
    x,y,z=CENTRE
    rx,ry,rz=EAST
    steps={
      "reset":[
          "time set noon","weather clear","difficulty peaceful",
          "forceload add -5 34 7 46",
          "fill -4 119 35 5 119 46 minecraft:smooth_stone",
          "fill -3 120 36 4 122 44 minecraft:air",
          f"setblock {x} {y} {z} {TABLE}",
          f"say {SIGNAL}reset_STAGE_DONE"],
      "join":[f"setblock {rx} {ry} {rz} {TABLE}",
              f"say {SIGNAL}join_STAGE_DONE"],
      "remove":[f"setblock {rx} {ry} {rz} minecraft:air",
                f"say {SIGNAL}remove_STAGE_DONE"]
    }
    for stage in STAGES:
        commands=[]
        for label,(bx,by,bz) in (("CENTRE",CENTRE),("EAST",EAST)):
            for property in ("east","west","north","south"):
                for value in ("true","false"):
                    commands.append(
                        f"execute if block {bx} {by} {bz} {TABLE}[{property}={value}] "
                        f"run say {SIGNAL}{stage}_{label}_{property.upper()}_{value.upper()}")
            commands.append(
                f"execute if block {bx} {by} {bz} {TABLE} "
                f"run say {SIGNAL}{stage}_{label}_TABLE_PRESENT")
            commands.append(
                f"execute if block {bx} {by} {bz} minecraft:air "
                f"run say {SIGNAL}{stage}_{label}_AIR_PRESENT")
        commands.append(f"say {SIGNAL}{stage}_OBSERVED")
        steps["verify_"+stage]=commands
    return steps

def make_pack(version,pack):
    check(version==VERSION,"Macaw table natural neighbor experiment requires 1.21.11")
    pack=Path(pack)
    check(not pack.exists(),"Do not modify an existing experiment datapack")
    folder=pack/"data/mcfr_neighbor/function"
    folder.mkdir(parents=True,exist_ok=False)
    meta={"pack":{"description":"INT-4 Macaw source pinned east-table neighbor updates",
                  "min_format":[94,1],"max_format":[94,1]}}
    (pack/"pack.mcmeta").write_text(json.dumps(meta)+"\n",encoding="utf-8")
    scripts=pack_lines()
    for label,commands in scripts.items():
        (folder/(label+".mcfunction")).write_text("\n".join(commands)+"\n",encoding="utf-8")
    return {"schema":"MCFR_INT4_TABLE_NEIGHBOR_PACK/v1",
            "files_sha256":{p.relative_to(pack).as_posix():digest(p.read_bytes())
                            for p in sorted(pack.rglob("*")) if p.is_file()},
            "stages":list(STAGES),"player_item_placement_tested":False}

def source_signature(mods):
    # Verify fixed installed 3.4.2 JAR and all preexisting S18/S19/S28/S29
    # chosen source models, state rule selectors, provider faces and hashes.
    fixed=verify_running_source(Path(mods))
    check(fixed["mod_jar_sha256"]==MACAW_SHA256 and
          fixed["states"]["S18"]["faces"]==31 and
          fixed["states"]["S19"]["faces"]==6,
          "Pinned original Macaw table model source changed")
    return {"macaw_jar_sha256":fixed["mod_jar_sha256"],
            "original_application_csv_sha256":fixed["historical_application_sha256"],
            "source_selected_cases":{"S18":fixed["states"]["S18"],
                                     "S19":fixed["states"]["S19"]}}

def extract(log,stage):
    check(stage in STAGES,"Unknown neighbor test stage")
    found={}
    for line in log.splitlines():
        if "[Server thread/" not in line or "[RenderAudit] "+SIGNAL+stage+"_" not in line:
            continue
        suffix=line.split("[RenderAudit] "+SIGNAL+stage+"_",1)[1].strip()
        if suffix.endswith("_STAGE_DONE") or suffix.endswith("_OBSERVED"):
            continue
        found[suffix]=found.get(suffix,0)+1
    check(f"{SIGNAL}{stage}_OBSERVED" in log,
          "Real server observation stage marker missing: "+stage)
    # Each observed state property is one of exactly true/false for table.
    outcome={}
    for label in ("CENTRE","EAST"):
        present=found.get(label+"_TABLE_PRESENT",0)
        air=found.get(label+"_AIR_PRESENT",0)
        check((present,air) in ((1,0),(0,1)),
              "Block was not unambiguously observed as table/air: "+stage+" "+label+
              " "+str({"table":present,"air":air}))
        entry={"block":"table" if present else "air"}
        for prop in ("EAST","WEST","NORTH","SOUTH"):
            true_count=found.get(f"{label}_{prop}_TRUE",0)
            false_count=found.get(f"{label}_{prop}_FALSE",0)
            check((true_count,false_count)==((1,0) if present else (0,0)) or
                  (present and (true_count,false_count)==(0,1)),
                  "Game server emitted missing/ambiguous property: "+
                  stage+"/"+label+"/"+prop+
                  " "+str((true_count,false_count)))
            entry[prop.lower()]=(True if true_count else False) if present else None
        outcome[label.lower()]=entry
    check(found and all(count==1 for count in found.values()),
          "Duplicate Minecraft server output in trial "+stage)
    return outcome

def summarize(states):
    check(set(states)==set(STAGES),"Server neighbor update timeline incomplete")
    before=states["reset"];joined=states["join"];removed=states["remove"]
    check(before["centre"]["block"]=="table" and before["east"]["block"]=="air",
          "Baseline requires isolated centre table and east air")
    check(joined["centre"]["block"]=="table" and joined["east"]["block"]=="table",
          "Both table blocks must be present during adjacency test")
    check(removed["centre"]["block"]=="table" and removed["east"]["block"]=="air",
          "Removal must leave centre table and east air")
    return {
      "centre_east_baseline":before["centre"]["east"],
      "centre_east_with_neighbor":joined["centre"]["east"],
      "neighbor_west_with_centre":joined["east"]["west"],
      "centre_east_after_remove":removed["centre"]["east"],
      "joined_bidirectionally":joined["centre"]["east"] is True and joined["east"]["west"] is True,
      "automatically_disconnected_after_remove":joined["centre"]["east"] is True and
               removed["centre"]["east"] is False,
      "state_changed_after_adjacent_setblock":
            before["centre"]["east"] != joined["centre"]["east"],
      "player_item_placement_tested":False,
      "natural_server_block_neighbor_updates_observed":True
    }

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"Actual neighbor trial requires Fabric 1.21.11")
    provenance=source_signature(game/"mods")
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    log=output/"client.log";shots=game/"screenshots"
    records={};state_records={}
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],
                                           env=env,timeout=18,text=True).strip()
        def send(value):
            xdo("key","--clearmodifiers","t");sleep(.35)
            xdo("type","--clearmodifiers","--delay","14",value)
            xdo("key","--clearmodifiers","Return")
        def cmd(value,marker,description):
            for attempt in range(3):
                offset=len(read())
                xdo("windowfocus","--sync",window[0]);sleep(0.8)
                send(value)
                try:
                    wait_for(proc,lambda:marker in read()[offset:],
                             description,32)
                    sleep(1.5)
                    return
                except ValueError as failure:
                    if "Timed out waiting" not in str(failure) or attempt==2:raise
                    sleep(4)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "actual Fabric 1.21.11 world joined",160)
            window=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                       "--name","^Minecraft").split()
            check(len(window)==1,"Expected a single visible Minecraft 1.21.11 window")
            xdo("windowfocus","--sync",window[0]);sleep(3)
            send("/gamemode spectator");sleep(1)
            cmd("/tp @s 0.5 124 43.5 180 18",
                "[RenderAudit: Teleported RenderAudit to","table neighborhood initial camera")
            shots.mkdir(exist_ok=True)
            for stage in STAGES:
                cmd("/function mcfr_neighbor:"+stage,
                    "[RenderAudit] "+SIGNAL+stage+"_STAGE_DONE",
                    "game stage "+stage)
                cmd("/function mcfr_neighbor:verify_"+stage,
                    "[RenderAudit] "+SIGNAL+stage+"_OBSERVED",
                    "game server stage observation "+stage)
                state_records[stage]=extract(read(),stage)
                # F2 screenshots are supplementary independent artifacts.
                # The actual server states above are primary evidence.
                before=set(shots.glob("*.png"))
                xdo("key","--clearmodifiers","F1");sleep(1.0)
                xdo("key","--clearmodifiers","F2")
                valid=wait_for(proc,lambda:[
                    p for p in shots.glob("*.png") if p not in before and
                    p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
                ],"real neighboring table F2 "+stage,85)
                xdo("key","--clearmodifiers","F1")
                check(len(valid)==1,"Expected exactly one new native F2 image")
                with Image.open(valid[0]) as picture:
                    picture.load();dimensions=list(picture.size)
                check(dimensions==[1024,684],"Native F2 screenshot dimensions unexpected")
                saved=output/(stage+".png")
                shutil.copyfile(valid[0],saved)
                records[stage]={"file":saved.name,"sha256":digest(saved.read_bytes()),
                                "dimensions":dimensions}
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=25)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    transitions=summarize(state_records)
    document={
      "schema":"MCFR_INT4_MACAW_TABLE_NEIGHBOR_REAL_GAME/v1",
      "status":"SERVER_NEIGHBOR_STATES_RECORDED_NO_ASSUMED_CONNECTION",
      "minecraft":"1.21.11","actual_fabric_game":True,
      "source_registry":provenance,"observed_server_states":state_records,
      "transitions":transitions,"native_F2":records,
      "client_log_sha256":digest(log.read_bytes()),
      "int4_full_completed":False,"int5_part_roles_approved":0,
      "int6_ai_training_rights_approved":0
    }
    (output/OUTCOME).write_text(json.dumps(document,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    return document

def audit(path):
    from PIL import Image,ImageDraw
    path=Path(path)
    output=path/OUTCOME
    doc=json.loads(output.read_text(encoding="utf-8"))
    check(doc.get("schema")=="MCFR_INT4_MACAW_TABLE_NEIGHBOR_REAL_GAME/v1" and
          doc.get("status")=="SERVER_NEIGHBOR_STATES_RECORDED_NO_ASSUMED_CONNECTION" and
          doc.get("actual_fabric_game") is True and
          doc.get("int4_full_completed") is False and
          doc.get("int5_part_roles_approved")==doc.get("int6_ai_training_rights_approved")==0,
          "Actual game claim or scope boundaries invalid")
    registry=doc["source_registry"]
    check(registry["macaw_jar_sha256"]==MACAW_SHA256,
          "Source original Macaw release pin changed")
    logs=(path/"client.log").read_bytes()
    check(digest(logs)==doc["client_log_sha256"],"Minecraft log SHA tampered")
    seen={stage:extract(logs.decode("utf-8",errors="replace"),stage) for stage in STAGES}
    check(seen==doc["observed_server_states"],"Actual integrated server logs disagree with claimed states")
    result=summarize(seen)
    check(result==doc["transitions"],"Neighbor state transition classification differs")
    check(set(doc["native_F2"])==set(STAGES),"Three stage F2 photos missing")
    pictures=[]
    for stage in STAGES:
        record=doc["native_F2"][stage]
        check(record["file"]==stage+".png" and record["dimensions"]==[1024,684],
              "Stage F2 metadata invalid: "+stage)
        screenshot=path/record["file"]
        check(digest(screenshot.read_bytes())==record["sha256"],
              "Original screenshot SHA mismatch: "+stage)
        with Image.open(screenshot) as im:im.verify()
        with Image.open(screenshot) as im:pictures.append(im.convert("RGB"))
    contact=Image.new("RGB",(3*512,378),(240,240,240))
    draw=ImageDraw.Draw(contact)
    for i,(im,stage) in enumerate(zip(pictures,STAGES)):
        contact.paste(im.resize((512,342),resample=Image.Resampling.BILINEAR),(i*512,0))
        draw.text((i*512+8,350),stage,fill=(10,10,10))
    contact.save(path/CONTACT)
    audit_doc={
      "schema":"MCFR_INT4_MACAW_NEIGHBOR_REAL_SERVER_TRANSITIONS_AUDIT/v1",
      "status":"REAL_GAME_SERVER_TRANSITIONS_REPRODUCED_NOT_ITEM_PLACEMENT",
      "macaw_jar_sha256":MACAW_SHA256,
      "source_state_sha256":registry["original_application_csv_sha256"],
      "observed_server_states":seen,
      "neighbor_transition_observation":result,
      "real_F2_count":3,
      "per_F2_sha256":{s:doc["native_F2"][s]["sha256"] for s in STAGES},
      "client_log_sha256":doc["client_log_sha256"],
      "capture_manifest_sha256":digest(output.read_bytes()),
      "contact_sha256":digest((path/CONTACT).read_bytes()),
      "scope":{
        "server_neighbor_updates_observed":True,
        "state_changed_only_if_measured":result["state_changed_after_adjacent_setblock"],
        "player_manual_item_placement_verified":False,
        "actual_bed_or_bookshelf_natural_connection_tested":False,
        "int4_all_complete":False,"int5_semantic_approvals":0,"int6_rights_approvals":0}
    }
    (path/AUDIT).write_text(json.dumps(audit_doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    return audit_doc

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory",required=True,type=Path)
    args=parser.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
