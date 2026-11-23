"""INT-4-H15: actual pinned Fabric AF chair model1/model3 two-sided native F2.

Two actual observer positions with SAME source block, SAME block-facing north
and SAME models; at EACH observer use original model1 -> model3 -> model1
temporal return -> AIR. Screenshots and client log remain Actions artifacts.
Only limited source/model/texture/UV evidence; no face-to-GPU texel claim.
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

from .runtime_capture import wait_for
from .chair_runtime_capture import (
    send_minecraft_command, confirmed_spectator_mode, confirmed_camera_teleport,
    archive_gui_diagnostic,
)
from . import int4_h12_af_chair_samepose_f2_capture as h12

ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.21.1"
ORIGINAL = "INT4_H15_AF_OPPOSING_VIEW_REAL_NATIVE_F2_MANIFEST_V1.json"
AUDIT = "INT4_H15_AF_OPPOSING_VIEW_INDEPENDENT_RESULT_V1.json"
VIEWS = ("south", "north")
STAGES = h12.STAGES
EXPECTED_CAMERAS = {
    "south": "-87.5 122.3 45.5 180 20",
    "north": "-87.5 122.3 35.5 0 20",
}
# South observer in H12 is +5.5 Z from block; opposite observer is -4.5
# Z from block, both 4.6875/5.3125 away from backrest at z=40.8125.
BLOCK_XYZ = (-88, 120, 40)
ROI = (350, 275, 675, 620)
CHANNEL_THRESHOLD = 24


def check(value, message):
    if not value:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def label(view: str, stage: str) -> str:
    check(view in VIEWS and stage in STAGES, "INVALID_H15_VIEW_OR_STAGE")
    return view + "_" + stage


def stage_state(stage: str) -> str:
    if stage == "air":
        return "minecraft:air"
    return h12.state("model3" if stage == "model3" else "model1")


def camera_face_candidate(view: str) -> str:
    check(view in EXPECTED_CAMERAS, "INVALID_H15_CAMERA_VIEW")
    camera_z = float(EXPECTED_CAMERAS[view].split()[2])
    parent_z = BLOCK_XYZ[2] + 13/16
    check(camera_z != parent_z, "CAMERA_ON_ORIGINAL_BACKREST_PLANE")
    return "south" if camera_z > parent_z else "north"


def pixel_changes(a: Image.Image, b: Image.Image) -> set[tuple[int, int]]:
    check(a.size == b.size == (1024, 684), "H15_NATIVE_FRAME_DIMENSION_MISMATCH")
    left = a.convert("RGB").crop(ROI)
    right = b.convert("RGB").crop(ROI)
    al,bl = left.tobytes(),right.tobytes()
    check(len(al) == len(bl) == left.width*left.height*3,
          "H15_NATIVE_RGB_CHANNEL_BYTES_MISMATCH")
    ret=set()
    for i in range(left.width*left.height):
        j=i*3
        if max(abs(al[j+c]-bl[j+c]) for c in range(3))>=CHANNEL_THRESHOLD:
            ret.add((ROI[0]+i%left.width,ROI[1]+i//left.width))
    return ret


def measure_view(images: dict[str, Image.Image]) -> dict:
    check(set(images) == set(STAGES), "H15_FOUR_STAGE_IMAGES_REQUIRED")
    m1,m3,restore,air = (images[s] for s in STAGES)
    delta=pixel_changes(m1,m3)
    temporal=pixel_changes(m1,restore)
    foreground=pixel_changes(m1,air)|pixel_changes(m3,air)
    unexplained=delta-temporal
    return {
        "ROI":list(ROI),
        "channel_threshold":CHANNEL_THRESHOLD,
        "model1_to_model3_changed_pixels":len(delta),
        "model1_to_model1_temporal_changed_pixels":len(temporal),
        "model1_to_air_changed_pixels":len(pixel_changes(m1,air)),
        "model3_to_air_changed_pixels":len(pixel_changes(m3,air)),
        "model_delta_outside_air_foreground":len(delta-foreground),
        "model_delta_not_in_temporal_control":len(unexplained),
        "model_delta_bounds_xyxy_inclusive":(
           [min(x for x,y in delta),min(y for x,y in delta),
            max(x for x,y in delta),max(y for x,y in delta)] if delta else None),
    }


def capture(command, env, game, output, version):
    check(version==VERSION,"H15_REQUIRES_PINNED_121_FABRIC_CLIENT")
    provenance=h12.static_preflight(game)
    case=h12.original_case()[0]
    check((case.x,case.y,case.z)==BLOCK_XYZ and case.camera()==EXPECTED_CAMERAS["south"],
          "H12_ORIGINAL_FIXTURE_CHANGED")
    destination=Path(output)
    destination.mkdir(parents=True,exist_ok=False)
    client_log=destination/"client.log"
    screenshots=Path(game)/"screenshots"
    records={view:{} for view in VIEWS}

    with client_log.open("wb") as stream, subprocess.Popen(
            command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT) as proc:
        def logtext():
            return client_log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,timeout=18,text=True).strip()
        def refocus():
            xdo("windowfocus","--sync",window)
        def send(cmd):
            send_minecraft_command(xdo,cmd)
        def acknowledge(cmd,marker,description):
            # No old server-log success reuse; one focused retry then fail.
            for attempt,timeout in enumerate((25,35)):
                refocus()
                start=len(logtext())
                send(cmd)
                try:
                    wait_for(proc,lambda:marker in logtext()[start:],
                             description+" attempt "+str(attempt+1),timeout)
                except ValueError as exc:
                    if not str(exc).startswith("Timed out waiting for") or attempt:
                        raise
                    continue
                sleep(0.6)
                return
            raise ValueError("H15_SOURCE_COMMAND_ACK_MISSING "+description)
        def exact(view,stage):
            state=stage_state(stage)
            marker="MCFR_H15_"+label(view,stage).upper()+"_EXACT_SERVER=PASS"
            x,y,z=BLOCK_XYZ
            acknowledge(f"/execute if block {x} {y} {z} {state} run say {marker}",
                        "[RenderAudit] "+marker, "exact blockstate "+label(view,stage))
            records[view][stage]={
                "blockstate":state,"server_marker":marker,"exact_server_verified":True,
            }
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in logtext(),
                     "H15 real pinned Minecraft Fabric world joined",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in logtext(),
                     "H15 native client session fully ready",90)
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"H15_REQUIRES_EXACTLY_ONE_REAL_GAME_WINDOW")
            window=windows[0]
            refocus();sleep(2)
            confirmed_spectator_mode(proc,logtext,send,refocus)
            acknowledge("/function mcfr_chair:place",
                        "[RenderAudit] MCFR_CHAIR_PLACED",
                        "pinned original single AF north chair placed")
            acknowledge("/function mcfr_chair:verify",
                        "[RenderAudit] MCFR_CHAIR_STATES_READ",
                        "pinned original source chair verified")
            screenshots.mkdir(exist_ok=True)
            for view in VIEWS:
                pos=EXPECTED_CAMERAS[view]
                confirmed_camera_teleport(proc,logtext,send,refocus,pos)
                for stage in STAGES:
                    name=label(view,stage)
                    state=stage_state(stage)
                    x,y,z=BLOCK_XYZ
                    if not (view == "south" and stage == "model1_before"):
                        # The original pinned world pack already placed this exact
                        # model. /setblock with an unchanged state may yield no
                        # "Changed" acknowledgement in the actual server.
                        acknowledge(f"/setblock {x} {y} {z} {state}",
                                    "[RenderAudit: Changed the block at",
                                    "new model stage "+name)
                    exact(view,stage)
                    sleep(5)
                    screenshot=h12.screenshot(xdo,window,screenshots,destination,name,{"proc":proc})
                    records[view][stage].update(screenshot)
                    print("H15_ORIGINAL_F2_CAPTURED "+name,flush=True)
        except Exception:
            archive_gui_diagnostic(destination,"H15_REAL_FABRIC_FAILURE")
            raise
        finally:
            if proc.poll() is None:
                proc.terminate()
                try: proc.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()

    check(all(set(rows)==set(STAGES) for rows in records.values()),
          "H15_REAL_NATIVE_F2_8_OR_SERVER_STATES_INCOMPLETE")
    manifest={
        "schema":"MCFR_INT4_H15_AF_OPPOSING_NATIVE_F2_GAME_SOURCE/v1",
        "status":"ORIGINAL_REAL_FABRIC_TWO_CAMERA_F2_CAPTURED_REQUIRES_INDEPENDENT_AUDIT",
        "runtime_version":VERSION,
        "real_single_game_session":True,
        "original_game_runs":1,
        "native_F2_count":8,
        "camera_view_order":list(VIEWS),
        "source_block_coordinates":list(BLOCK_XYZ),
        "source_block_facing":"north",
        "cameras":EXPECTED_CAMERAS,
        "camera_source_face_candidates":{v:camera_face_candidate(v) for v in VIEWS},
        "source_model1":h12.MODELS["model1"],
        "source_model3":h12.MODELS["model3"],
        "pinned_provenance":provenance,
        "views":records,
        "client_log_sha256":sha(client_log.read_bytes()),
        "no_player_interactions_tested":True,
        "source_face_to_screen_pixel_GPU_causality_approved":False,
        "F70_unconditional_approvals":0,
        "H03_H05_full_exit":False,
        "INT5_semantics_approved":0,
        "INT6_training_or_redistribution_approved":0,
    }
    (destination/ORIGINAL).write_text(
        json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return manifest


def audit(directory):
    root=Path(directory)
    raw=(root/ORIGINAL).read_bytes()
    doc=json.loads(raw)
    check(doc["schema"]=="MCFR_INT4_H15_AF_OPPOSING_NATIVE_F2_GAME_SOURCE/v1" and
          doc["status"]=="ORIGINAL_REAL_FABRIC_TWO_CAMERA_F2_CAPTURED_REQUIRES_INDEPENDENT_AUDIT" and
          doc["runtime_version"]==VERSION and
          doc["real_single_game_session"] is True and
          doc["original_game_runs"]==1 and doc["native_F2_count"]==8,
          "H15_ORIGINAL_GAME_MANIFEST_SCHEMA_SCOPE_FAILURE")
    check(doc["source_block_coordinates"]==list(BLOCK_XYZ) and
          doc["source_block_facing"]=="north" and
          doc["camera_view_order"]==list(VIEWS) and
          doc["cameras"]==EXPECTED_CAMERAS and
          doc["camera_source_face_candidates"]=={v:camera_face_candidate(v) for v in VIEWS},
          "H15_ORIGINAL_TWO_OPPOSING_CAMERA_SOURCE_DRIFT")
    check(doc["pinned_provenance"]["actual_af_jar_sha1"]==h12.JAR_SHA1 and
          doc["pinned_provenance"]["h11_git_blob_sha1"]==h12.H11_SHA1 and
          doc["source_model1"]==h12.MODELS["model1"] and
          doc["source_model3"]==h12.MODELS["model3"],
          "H15_ORIGINAL_AF_4_0_2_MODEL_AND_UV_PINS_MISSING")
    log=(root/"client.log").read_bytes()
    check(sha(log)==doc["client_log_sha256"],"H15_ACTUAL_GAME_CLIENT_LOG_SHA_CHANGED")
    logtext=log.decode("utf-8",errors="replace")
    check(set(doc["views"])==set(VIEWS),"H15_ORIGINAL_TWO_CAMERA_VIEWS_MISSING")
    metrics={}
    for view in VIEWS:
        items=doc["views"][view]
        check(set(items)==set(STAGES),"H15_FOUR_NATIVE_FRAME_SEQUENCE_MISSING_"+view)
        imgs={}
        for stage in STAGES:
            item=items[stage]
            check(item["blockstate"]==stage_state(stage) and
                  item["exact_server_verified"] is True and
                  "[RenderAudit] "+item["server_marker"] in logtext and
                  item["image"]==label(view,stage)+".png" and
                  item["dimensions"]==[1024,684],
                  "H15_EXACT_GAME_SOURCE_STATE_OR_SCREEN_IDENTITY_WRONG_"+label(view,stage))
            binary=(root/item["image"]).read_bytes()
            check(sha(binary)==item["sha256"],
                  "H15_ACTUAL_GAME_NATIVE_F2_SHA_MISMATCH_"+label(view,stage))
            with Image.open(root/item["image"]) as im:
                im.load()
                check(im.format=="PNG" and im.size==(1024,684),
                      "H15_NON_NATIVE_SCREENSHOT_"+label(view,stage))
                imgs[stage]=im.convert("RGB")
        metrics[view]=measure_view(imgs)
    visible={view:(metrics[view]["model1_to_model3_changed_pixels"]>25 and
                   metrics[view]["model_delta_not_in_temporal_control"]>20 and
                   metrics[view]["model_delta_outside_air_foreground"]==0)
             for view in VIEWS}
    result={
       "schema":"MCFR_INT4_H15_AF_OPPOSING_CAMERA_REAL_F2_INDEPENDENT_AUDIT/v1",
       "status":("PASS_TWO_ORIGINAL_FABRIC_CAMERA_SOURCE_MODEL_CONTRAST" if all(visible.values())
                 else "CONDITIONAL_ORIGINAL_F2_OBTAINED_CONTRAST_NOT_BOTH_ESTABLISHED"),
       "runtime_version":VERSION,
       "actual_game_runs":1,
       "original_game_native_F2_verified":8,
       "original_game_exact_server_states_verified":8,
       "source_block_coordinates":list(BLOCK_XYZ),
       "same_original_source_block_facing_north":True,
       "source_camera_face_candidates":doc["camera_source_face_candidates"],
       "source_original_manifest_sha256":sha(raw),
       "source_game_client_log_sha256":sha(log),
       "original_native_F2_SHA256":{
           label(view,stage):doc["views"][view][stage]["sha256"]
           for view in VIEWS for stage in STAGES},
       "per_view_original_RGB_ROI":metrics,
       "model_contrast_visually_detected_by_camera":visible,
       "source_parent_two_sided_UV_candidates":["north","south"],
       "verified_GPU_face_texel_pixel_attribution":False,
       "new_model_semantic_or_license_approval":False,
       "F70_unconditional_approvals":0,
       "H03_H05_full_exit":False,
       "INT5_semantics_approved":0,
       "INT6_training_or_redistribution_approved":0,
       "limits":[
          "Opposing observer images and source face-normal candidates do not themselves prove exact GPU face UV texel sampling.",
          "Use original PNG alpha, model parent, source variants, exact server log and temporal AIR controls separately.",
          "North-facing chair state remains pinned; only spectator camera world Z and yaw are changed between groups.",
          "All actual native F2/JAR/client.log bytes stay in temporary Actions artifacts.",
       ],
    }
    (root/AUDIT).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                            encoding="utf-8")
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--directory",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False))


if __name__=="__main__":
    main()
