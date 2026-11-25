"""INT-5-B4: native Fabric 1.21.1 AF tucked chair slab A/B/A/AIR control.

AF's tucked=true variant requires an adjacent top slab. Never claim that
removing the slab while leaving the original tucked=true chair is a valid
game state. Instead compare chair+slab (A), slab alone (B), restored A, air,
at the identical camera and original real source state. Repeat from opposite
camera. Pixel contrast is whole-object visibility, not per-element role/function.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path
from time import sleep

from PIL import Image

from .chair_runtime_fixture import cases
from .chair_runtime_capture import (
    validate_source_targets, send_minecraft_command,
    confirmed_camera_teleport, confirmed_spectator_mode,
    archive_gui_diagnostic,
)
from .runtime_capture import wait_for
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15

VERSION="1.21.1"
CHILD="AF123"
BLOCK="another_furniture:acacia_chair"
MODEL="another_furniture:block/chair/acacia_10_tucked"
SLAB="minecraft:oak_slab[type=top]"
STAGES=("chair_plus_slab_before","slab_only","chair_plus_slab_after","empty")
VIEWS=("south","north")
ORIGINAL="INT5_B4_AF_TUCKED_SLAB_REAL_F2_MANIFEST_V1.json"
AUDIT="INT5_B4_AF_TUCKED_SLAB_INDEPENDENT_AUDIT_V1.json"
ROI=(350,275,675,620)
THRESHOLD=24


def require(ok,msg):
    if not ok:raise ValueError("INT5-B4: "+msg)


def sha(b):return hashlib.sha256(b).hexdigest()


def target_case():
    result=tuple(x for x in cases(VERSION) if x.case_id=="AF123_north")
    require(len(result)==1 and result[0].state()==
            "another_furniture:acacia_chair[facing=north,tucked=true,variant=10]",
            "source AF123 north state unexpectedly changed")
    return result[0]


def xyz():
    c=target_case()
    return c.x,c.y,c.z


def slab_xyz():
    c=target_case()
    return c.x,c.y,c.z-1


def cameras():
    c=target_case()
    return {"south":c.camera(),
            "north":f"{c.x+0.5:g} {c.y+2.3:g} {c.z-5.5:g} 0 20"}


def stage_chair_state(name):
    require(name in STAGES,"unknown real chair/slab stage")
    return target_case().state() if name.startswith("chair_plus") else "minecraft:air"


def stage_slab_state(name):
    require(name in STAGES,"unknown real chair/slab stage")
    return SLAB if name!="empty" else "minecraft:air"


def label(view,stage):
    require(view in VIEWS and stage in STAGES,"unknown real camera/stage")
    return view+"_"+stage


def pixel_delta(a,b):
    require(a.size==b.size==(1024,684),"real native F2 dimensions mismatch")
    a=a.convert("RGB").crop(ROI).tobytes()
    b=b.convert("RGB").crop(ROI).tobytes()
    width=ROI[2]-ROI[0]
    out=set()
    for pos in range(0,len(a),3):
        if max(abs(a[pos+k]-b[pos+k]) for k in range(3))>=THRESHOLD:
            idx=pos//3
            out.add((ROI[0]+idx%width,ROI[1]+idx//width))
    return out


def measure(images):
    require(set(images)==set(STAGES),"A/B/A/AIR controls incomplete")
    A,B,A2,air=(images[k] for k in STAGES)
    chair=pixel_delta(A,B)
    slab=pixel_delta(B,air)
    total=pixel_delta(A,air)
    temporal=pixel_delta(A,A2)
    return {
        "ROI":list(ROI),
        "channel_threshold":THRESHOLD,
        "chair_pixel_delta_with_slab_fixed":len(chair),
        "slab_pixel_delta_with_chair_absent":len(slab),
        "chair_plus_slab_pixel_delta_vs_empty":len(total),
        "same_chair_state_temporal_delta":len(temporal),
        "chair_delta_minus_temporal":len(chair-temporal),
        "chair_delta_bounds_xyxy":([min(x for x,y in chair),min(y for x,y in chair),
                                     max(x for x,y in chair),max(y for x,y in chair)]
                                    if chair else None),
        "slab_delta_bounds_xyxy":([min(x for x,y in slab),min(y for x,y in slab),
                                    max(x for x,y in slab),max(y for x,y in slab)]
                                   if slab else None),
        "chair_slab_difference_pixel_intersection":len(chair&slab),
    }


def capture(command,env,game,output,version):
    require(version==VERSION,"must use actual pinned Fabric 1.21.1")
    case=target_case()
    game=Path(game)
    # Release model selector is checked INSIDE actual official 4.0.2 JAR.
    choices,release=validate_source_targets(
        VERSION,game/"mods",selected_cases=(case,),
        expected_case_models={case.case_id:{"model":MODEL,"y":0}})
    original=choices[case.case_id]
    require(original["model_target"]==MODEL and original["rotation_y"]==0,
            "official release tucked north model select mismatch")
    require(original["source_version_equivalence"]==
            "RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE",
            "preserve original study/source AF release drift")
    destination=Path(output)
    destination.mkdir(parents=True,exist_ok=False)
    logfile=destination/"client.log"
    shots=game/"screenshots"
    cam=cameras()
    results={view:{} for view in VIEWS}

    with logfile.open("wb") as sink,subprocess.Popen(
            command,cwd=game,env=env,stdout=sink,stderr=subprocess.STDOUT) as proc:
        def txt():return logfile.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,
                                           timeout=18,text=True).strip()
        def focus():xdo("windowfocus","--sync",window)
        def send(c):send_minecraft_command(xdo,c)
        def acknowledge(command,token,reason):
            for attempt,timeout in enumerate((25,35),1):
                focus()
                start=len(txt())
                send(command)
                try:
                    wait_for(proc,lambda:token in txt()[start:],
                             reason+" attempt "+str(attempt),timeout)
                except ValueError as e:
                    if not str(e).startswith("Timed out waiting for") or attempt==2:
                        raise
                    continue
                sleep(.7)
                return
            raise ValueError("real client command missing "+reason)
        def changed_block(position,new_state,reason):
            x,y,z=position
            acknowledge(f"/setblock {x} {y} {z} {new_state}",
                        "[RenderAudit: Changed the block at",reason)
        def assert_state(view,stage):
            for role,pos,state in (("CHAIR",xyz(),stage_chair_state(stage)),
                                   ("SLAB",slab_xyz(),stage_slab_state(stage))):
                x,y,z=pos
                marker="MCFR_INT5_B4_"+label(view,stage).upper()+"_"+role+"=PASS"
                acknowledge(
                    f"/execute if block {x} {y} {z} {state} run say {marker}",
                    "[RenderAudit] "+marker, "exact original "+role+" "+label(view,stage))
                results[view][stage].setdefault("server_exact",{})[role]=marker
            results[view][stage].update({
                "chair_state":stage_chair_state(stage),
                "slab_state":stage_slab_state(stage),
                "chair_xyz":list(xyz()),"slab_xyz":list(slab_xyz()),
            })
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in txt(),
                     "original 1.21.1 Fabric chair control world join",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in txt(),
                     "original Fabric game ready",90)
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            require(len(windows)==1,"expected one actual Minecraft game window")
            window=windows[0];focus();sleep(2)
            confirmed_spectator_mode(proc,txt,send,focus)
            acknowledge("/function mcfr_chair:place",
                        "[RenderAudit] MCFR_CHAIR_PLACED",
                        "original AF123 top-slab before chair placement")
            acknowledge("/function mcfr_chair:verify",
                        "[RenderAudit] MCFR_CHAIR_STATES_READ",
                        "original AF123 tucked source state read back")
            shots.mkdir(exist_ok=True)
            for v in VIEWS:
                confirmed_camera_teleport(proc,txt,send,focus,cam[v])
                for step in STAGES:
                    if step=="chair_plus_slab_before":
                        if v=="north":
                            changed_block(slab_xyz(),SLAB,
                                          "restore legal top slab before tucked chair")
                            changed_block(xyz(),target_case().state(),
                                          "restore actual tucked chair with legal support")
                    elif step=="slab_only":
                        changed_block(xyz(),"minecraft:air",
                                      "remove only chair keeping support fixed")
                    elif step=="chair_plus_slab_after":
                        changed_block(xyz(),target_case().state(),
                                      "restore real tucked chair with same slab")
                    elif step=="empty":
                        changed_block(xyz(),"minecraft:air",
                                      "remove chair before slab control")
                        changed_block(slab_xyz(),"minecraft:air",
                                      "remove slab after chair for empty control")
                    results[v][step]={}
                    assert_state(v,step)
                    sleep(4)
                    snap=h12.screenshot(xdo,window,shots,destination,label(v,step),
                                        {"proc":proc})
                    results[v][step].update(snap)
                    print("INT5_B4_ACTUAL_ORIGINAL_F2 "+label(v,step),flush=True)
        except Exception:
            archive_gui_diagnostic(destination,"INT5_B4_ACTUAL_FABRIC_CONTROL_FAILURE")
            raise
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    require(set(results)==set(VIEWS) and
            all(set(results[v])==set(STAGES) for v in VIEWS),
            "8 real original native F2 / server states incomplete")
    doc={
        "schema":"MCFR_INT5_B4_AF123_TUCKED_SUPPORT_SLAB_SAMEPOSE_F2/v1",
        "status":"ACTUAL_NATIVE_F2_8_SERVER_STATES_REQUIRES_INDEPENDENT_AUDIT",
        "pinned_minecraft_version":VERSION,
        "pinned_original_source_case":case.case_id,
        "tucked_source_resource":MODEL,
        "source_runtime_selected_state":original,
        "official_release_blockstate_checks":release,
        "original_AF_4_0_2_runtime_jar":"another_furniture-fabric-4.0.2.jar",
        "same_game_session":True,
        "game_runs":1,
        "native_F2_screenshots":8,
        "camera_poses":cam,
        "views":results,
        "client_log_sha256":sha(logfile.read_bytes()),
        "source_premise":"tucked=true requires top slab; never remove support while claiming original valid tucked state",
        "new_source_element_to_F2_pixel_approvals":0,
        "new_semantic_function_approvals":0,
        "INT6_training_redistribution_approvals":0,
        "limits":[
            "Chair+slab vs slab-only reveals visible chair pixels while preserving slab geometry.",
            "Slab-only vs AIR reveals support geometry; chair hidden behind slab is not observed in the slab-fixed difference.",
            "Removing the slab changes neighbor-dependent tuck state and cannot be considered the same original tucked model.",
            "Opposing camera observations are image-level and do not prove an individual JSON element's exact face/UV pixel mapping.",
            "Temporary source game world, official JAR and screenshots stay only in expiring Actions artifacts.",
        ],
    }
    (destination/ORIGINAL).write_text(
        json.dumps(doc,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return doc


def audit(directory):
    root=Path(directory)
    doc=json.loads((root/ORIGINAL).read_text(encoding="utf-8"))
    require(doc["schema"]=="MCFR_INT5_B4_AF123_TUCKED_SUPPORT_SLAB_SAMEPOSE_F2/v1" and
            doc["status"]=="ACTUAL_NATIVE_F2_8_SERVER_STATES_REQUIRES_INDEPENDENT_AUDIT" and
            doc["same_game_session"] is True and
            doc["native_F2_screenshots"]==8 and doc["game_runs"]==1 and
            doc["pinned_original_source_case"]=="AF123_north",
            "invalid actual source manifest")
    require(doc["camera_poses"]==cameras() and
            doc["tucked_source_resource"]==MODEL and
            doc["source_runtime_selected_state"]["model_target"]==MODEL,
            "actual original release model selector or camera changed")
    require(doc["official_release_blockstate_checks"][BLOCK]["jar"]==
            "another_furniture-fabric-4.0.2.jar" and
            doc["official_release_blockstate_checks"][BLOCK]["scope"]==
            "RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE",
            "original official Fabric release provenance drift")
    log=(root/"client.log").read_bytes()
    require(sha(log)==doc["client_log_sha256"],"real client log SHA mismatch")
    txt=log.decode("utf-8",errors="replace")
    require(set(doc["views"])==set(VIEWS),"two opposing real camera views required")
    measurements={}
    total={}
    for v in VIEWS:
        entries=doc["views"][v]
        require(set(entries)==set(STAGES),"original F2 stage set incomplete "+v)
        images={}
        for step in STAGES:
            x=entries[step]
            require(x["chair_state"]==stage_chair_state(step) and
                    x["slab_state"]==stage_slab_state(step) and
                    x["chair_xyz"]==list(xyz()) and
                    x["slab_xyz"]==list(slab_xyz()) and
                    x["image"]==label(v,step)+".png" and
                    x["dimensions"]==[1024,684],
                    "actual scene/model/slab provenance changed "+label(v,step))
            for role in ("CHAIR","SLAB"):
                marker="MCFR_INT5_B4_"+label(v,step).upper()+"_"+role+"=PASS"
                require(x["server_exact"][role]==marker and
                        "[RenderAudit] "+marker in txt,
                        "real game server chair or support state not proven "+label(v,step))
            img_path=root/x["image"]
            require(sha(img_path.read_bytes())==x["sha256"],
                    "real original PNG SHA drift "+label(v,step))
            with Image.open(img_path) as im:
                im.load()
                require(im.format=="PNG" and im.size==(1024,684),
                        "not real native F2 "+label(v,step))
                images[step]=im.convert("RGB")
        m=measure(images)
        measurements[v]=m
        total[v]={"actual_visible_chair_pixels_vs_slab_only":
                    m["chair_pixel_delta_with_slab_fixed"]>30,
                  "actual_visible_support_pixels_vs_empty":
                    m["slab_pixel_delta_with_chair_absent"]>30,
                  "temporal_chair_delta_not_explained_by_drift":
                    m["chair_delta_minus_temporal"]>30}
    outcome=("PASS_REAL_FABRIC_BOTH_VIEW_SUPPORTED_TUCKED_CHAIR_VS_SLAB_CONTROLS"
             if all(all(v.values()) for v in total.values()) else
             "CONDITIONAL_REAL_F2_BUT_ONE_VIEW_NO_CLEAR_DELTA")
    summary={
        "schema":"MCFR_INT5_B4_AF_TUCKED_SLAB_NATIVE_F2_8_INDEPENDENT_AUDIT/v1",
        "decision":outcome,
        "exact_Fabric_client_version":VERSION,
        "source_case":"AF123_north",
        "actual_game_sessions":1,
        "original_native_F2_verified":8,
        "exact_server_chair_state_and_slab_pair_checks":16,
        "original_manifest_sha256":sha((root/ORIGINAL).read_bytes()),
        "original_client_log_sha256":sha(log),
        "native_F2_sha256":{
            label(v,s):doc["views"][v][s]["sha256"] for v in VIEWS for s in STAGES},
        "per_camera_original_screen_pixel_differences":measurements,
        "per_camera_pass_flags":total,
        "tucked_true_without_support_was_tested":False,
        "source_chair_variant_and_model_unchanged_for_A_and_A_return":True,
        "new_individual_element_F2_pixel_identifications":0,
        "new_element_function_approvals":0,
        "INT6_training_redistribution_approvals":0,
        "limits":[
            "With legal top slab fixed, chair vs slab-only screen pixels isolate visible chair assembly but do not reveal parts hidden behind the slab.",
            "Opposing camera views are explicit and exact game state markers correspond to every F2, no illicit unsupported tucked=true inference.",
            "No seat/leg/back element-index pixel attribution, functional occupancy or physical properties proved.",
            "No broad material, style, AI training or redistribution rights approved.",
        ],
    }
    (root/AUDIT).write_text(
        json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False))


if __name__=="__main__":
    main()
