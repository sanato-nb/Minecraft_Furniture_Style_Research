"""Capture ACTUAL Minecraft client F2 screenshots of 4 fixed chair models x 4 facings.

Unlike texture/geometry diagnostics, these files MUST come from a launched
pinned Fabric Minecraft client. Success requires exact original blockstate
source in installed JAR, explicit /setblock, verified server echo, native
1024x684 F2 PNGs, and a per-capture hash. Human visual/semantic confirmation
is deliberately NOT implied by successful screenshot creation.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from time import monotonic,sleep
from zipfile import ZipFile


from .chair_runtime_fixture import (CHAIRS,DIRS,cases,ORIGINAL_BLOCKSTATE,
                                    digest_bytes,verify_installed_mod_sources)
from .runtime_capture import wait_for

RESOURCE_BY_MODEL={
    "AF121":"another_furniture:block/chair/acacia_1",
    "AF123":"another_furniture:block/chair/acacia_10_tucked",
    "HC11210":"handcrafted:block/warped_chair_black",
    "MACAW67":"mcwfurnitures:block/chair/acacia_chair",
}
MODELS_YPOS={
  "AF121":(0,90,180,270),
  "AF123":(0,90,180,270),
  "HC11210":(0,90,180,270),
  "MACAW67":(90,180,270,0),
}

def property_map(selector):
    pieces=selector.split(",")
    data={}
    for piece in pieces:
        if not piece:continue
        k,sep,v=piece.partition("=")
        if not sep or not k or not v or k in data:
            raise ValueError("Invalid original source blockstate selector")
        data[k]=v
    return data

def validate_source_targets(version,mod_dir,selected_cases=None,expected_case_models=None):
    active=tuple(selected_cases) if selected_cases is not None else cases(version)
    if not active or len({c.case_id for c in active})!=len(active):
        raise ValueError("Selected original source cases are empty/duplicated")
    if expected_case_models is not None and set(expected_case_models)!={c.case_id for c in active}:
        raise ValueError("Explicit pinned model expectations do not cover the source cases")
    pinned=verify_installed_mod_sources(version,mod_dir)
    choices={}
    for block,ident in ORIGINAL_BLOCKSTATE[version].items():
        internal="assets/"+block.split(":")[0]+"/blockstates/"+ident["file"]
        jar=mod_dir/pinned[block]["jar"]
        with ZipFile(jar) as archive:
            src=json.loads(archive.read(internal).decode("utf-8-sig"))
        if set(src)!={"variants"}:
            raise ValueError("Source blockstate not static variant table: "+block)
        for case in (c for c in active if c.block_id==block):
            model=(expected_case_models[case.case_id]["model"] if expected_case_models is not None
                   else RESOURCE_BY_MODEL[case.model_key])
            state=property_map("facing="+case.facing+(","+case.selector if case.selector else ""))
            found=[v for k,v in src["variants"].items() if property_map(k)==state]
            if len(found)!=1:
                raise ValueError("Minecraft fixture properties do not identify exactly one source option: "+case.case_id)
            actual=found[0]
            expected_y=(expected_case_models[case.case_id]["y"] if expected_case_models is not None
                        else MODELS_YPOS[case.model_key][DIRS.index(case.facing)])
            if actual["model"]!=model or actual.get("y",0)!=expected_y or actual.get("x",0)!=0 or actual.get("uvlock",False):
                raise ValueError("Fixture is not the pinned source model/rotation: "+case.case_id)
            choices[case.case_id]={
                "block_id":case.block_id,"selector":case.state(),
                "model_target":model,"rotation_y":expected_y,
                "original_blockstate_source_hash":pinned[block]["research_source_hash"],
                "running_mod_blockstate_hash":pinned[block]["runtime_source_hash"],
                "source_version_equivalence":pinned[block]["scope"],
            }
    if len(choices)!=len(active):
        raise ValueError("One or more test cases were not validated against installed source JAR")
    return choices,pinned

def send_minecraft_command(xdo, command_line, pause=sleep):
    """Open the vanilla command box directly, avoiding chat-focus timing races."""
    if not command_line.startswith("/") or len(command_line)<2:
        raise ValueError("Minecraft GUI command must start with /")
    xdo("key","--clearmodifiers","slash")
    pause(0.45)
    xdo("type","--clearmodifiers","--delay","14",command_line[1:])
    xdo("key","--clearmodifiers","Return")


def confirmed_camera_teleport(proc, textlog, command_text, refocus, pos,
                              pause=sleep, waiter=wait_for):
    """Retry ONE unacknowledged GUI command, but never accept an unverified camera."""
    marker="[RenderAudit: Teleported RenderAudit to"
    for attempt, timeout in enumerate((25, 35), start=1):
        refocus()
        checkpoint=len(textlog())
        command_text("/tp @s "+pos)
        try:
            waiter(proc,lambda: marker in textlog()[checkpoint:],
                   "original-source chair camera teleport",timeout)
        except ValueError as exc:
            # Process exit / any unrelated error is not a retryable input race.
            if not str(exc).startswith("Timed out waiting for"):
                raise
            if attempt==2:
                raise ValueError(
                    "Camera teleport unconfirmed after two focused GUI commands; "
                    "original-source chair evidence remains unapproved. "
                    "Inspect the archived client.log for server acknowledgement."
                ) from exc
            print("INT3_CAMERA_GUI_ACK_MISSING: focused retry 1/1",flush=True)
            continue
        pause(2.5)
        return


def capture_chairs(command,env,game,output,version,selected_cases=None,
                   expected_case_models=None,report_name="INT3_REAL_GAME_CAPTURE.json"):
    # Optional image decoder is required only when real Fabric F2 capture runs;
    # importing this module for the core knowledge DB must not pull Pillow.
    from PIL import Image
    cases_to_capture=tuple(selected_cases) if selected_cases is not None else cases(version)
    if report_name not in ("INT3_REAL_GAME_CAPTURE.json",
                           "INT4_AF_VARIANT3_REAL_F2_CAPTURE.json"):
        raise ValueError("Unrecognized isolated client manifest name")
    target_manifest,pinned=validate_source_targets(
        version,game/"mods",selected_cases=cases_to_capture,
        expected_case_models=expected_case_models)
    output.mkdir(parents=True,exist_ok=False)
    log=output/"client.log"
    screenshot_root=game/"screenshots"
    output_rows=[]
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def textlog():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*parts):
            return subprocess.check_output(
                ["xdotool",*parts],env=env,timeout=15,text=True).strip()
        def command_text(command_line):
            send_minecraft_command(xdo,command_line)
        def camera_at(pos):
            confirmed_camera_teleport(
                proc,textlog,command_text,
                lambda:xdo("windowfocus","--sync",windows[0]),pos)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in textlog(),
                     "original test world first client load",135)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),"--name","^Minecraft").split()
            if len(windows)!=1:
                raise ValueError("Exactly one actual Minecraft client window was required")
            xdo("windowfocus","--sync",windows[0])
            sleep(1.5)
            command_text("/gamemode spectator")
            sleep(0.8)
            camera_at("0.5 124 42.5 180 20")
            command_text("/function mcfr_chair:place")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_PLACED" in textlog(),
                     "all source chair block placement",95)
            command_text("/function mcfr_chair:verify")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_STATES_READ" in textlog(),
                     "actual Minecraft server property matching",90)
            contents=textlog()
            expected={case.case_id for case in cases_to_capture}
            passed=set()
            failed=[]
            for line in contents.splitlines():
                token="[RenderAudit] MCFR_CHAIR_STATE_"
                if "[Server thread/" in line and token in line:
                    result=line.split(token,1)[1].strip()
                    if result.endswith("=PASS"):
                        passed.add(result[:-5])
                    elif result.endswith("=FAIL"):
                        failed.append(result[:-5])
            if passed!=expected or failed:
                raise ValueError("Game server block states did not match pinned source selections: "+
                                 repr({"missing":sorted(expected-passed),"failed":sorted(failed)}))
            if not screenshot_root.is_dir():
                screenshot_root.mkdir(exist_ok=True)
            for case in cases_to_capture:
                camera_at(case.camera())
                before=set(screenshot_root.glob("*.png"))
                xdo("key","--clearmodifiers","F1")
                sleep(0.8)
                xdo("key","--clearmodifiers","F2")
                files=wait_for(proc,lambda:[
                    path for path in screenshot_root.glob("*.png")
                    if path not in before and path.read_bytes().endswith(b"IEND\xaeB\x60\x82")
                ],"native Minecraft F2 screenshot for "+case.case_id,70)
                xdo("key","--clearmodifiers","F1")
                if len(files)!=1:
                    raise ValueError("Expected exactly one native F2 screenshot: "+case.case_id)
                output_file=output/(case.case_id+".png")
                shutil.copyfile(files[0],output_file)
                with Image.open(output_file) as screenshot:
                    screenshot.verify()
                with Image.open(output_file) as screenshot:
                    dimensions=tuple(screenshot.size)
                if dimensions!=(1024,684):
                    raise ValueError("Original Minecraft game screenshot size changed: "+str(dimensions))
                output_rows.append({
                   "case_id":case.case_id,"version":version,"model_key":case.model_key,
                   "original_state":case.state(),
                   "original_model_target":target_manifest[case.case_id]["model_target"],
                   "original_model_y":target_manifest[case.case_id]["rotation_y"],
                   "source_blockstate_digest":target_manifest[case.case_id]["original_blockstate_source_hash"],
                   "running_mod_source_digest":target_manifest[case.case_id]["running_mod_blockstate_hash"],
                   "source_version_equivalence":target_manifest[case.case_id]["source_version_equivalence"],
                   "screenshot_file":output_file.name,
                   "screenshot_sha256":hashlib.sha256(output_file.read_bytes()).hexdigest(),
                   "screenshot_dimensions":list(dimensions),
                   "native_F2_client_capture":True,
                   "server_blockstate_verified":True,
                   "visual_semantic_approved":False,
                })
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()

    if len(output_rows)!=len(cases_to_capture):
        raise ValueError("Client screenshots missing expected chair directions")
    report={
      "schema":"MCFR_INT3_REAL_GAME_CHAIR_CAPTURE/v1",
      "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
      "version":version,
      "models":sorted(set(c.model_key for c in cases_to_capture)),
      "source_state_verified_count":len(expected),
      "minecraft_native_f2_screenshot_count":len(output_rows),
      "original_blockstate_source_registry":pinned,
      "unverified_full_research_release_source_differences":[
          item for item,value in pinned.items() if not value["byte_identical_to_research"]
      ],
      "scope_restriction":"Each of the 12/4 selected original model targets and y rotations checked; release-wide JSON equality not asserted when hashes differ.",
      "states":output_rows,
      "client_log_sha256":hashlib.sha256(log.read_bytes()).hexdigest(),
      "client_version_verified":version,
      "actual_game_capture":True,
      "manual_sprite_comparison_complete":False,
      "human_verified_roles":0,"materials_or_styles_approved":0,
      "copyright_or_ai_training_approved":0,
      "comparability_note":"Client screenshots of fixed state and one camera placement each; NOT pixel-aligned to 16 independent orthographic UV renders."
    }
    if report_name=="INT4_AF_VARIANT3_REAL_F2_CAPTURE.json":
        report["schema"]="MCFR_INT4_AF_VARIANT3_REAL_F2_CAPTURE/v1"
        report["capture_profile"]="INT4_AF_VARIANT3_4_FACING_PLUS_2_VARIANT1_CONTROLS"
        report["scope_restriction"]=(
            "Only six source states, models and rotations checked against pinned AF runtime JAR;"
            " F2 files are not semantic or pixel-causal approval.")
    (output/report_name).write_text(
        json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report
