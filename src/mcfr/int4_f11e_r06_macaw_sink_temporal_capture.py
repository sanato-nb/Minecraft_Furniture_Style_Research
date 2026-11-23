"""INT-4-F11E R06: real Macaw water=true sink time-separated native Minecraft F2.

Reopens original S43 SHA-pinned 1-5 model using real Fabric 1.21.11 runtime.
3 separate original native F2 at >=8s intervals, exact server state checked
at each frame, same camera, pixel water ROI vs stable stone control.
A static observation is permissible; never claim animation unless actually seen.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from time import monotonic_ns,sleep
from zipfile import ZipFile
from .runtime_capture import wait_for
from . import int4_macaw_kitchen_capture as kitchen

VERSION=kitchen.VERSION
MACAW_SHA256=kitchen.MACAW_SHA256
SINK_CASE="S43"
SOURCE_CASE="S42"
MANIFEST="INT4_F11E_R06_TEMPORAL_REAL_F2_CAPTURE.json"
AUDIT_FILE="INT4_F11E_R06_TEMPORAL_REAL_F2_AUDIT.json"
ORDER=("R06_T0","R06_T1","R06_T2")
MIN_INTERVAL_SECONDS=8.0
WATER_ROI=(480,415,545,443)
SINK_ROI=(462,394,564,508)
STONE_CONTROL_ROI=(610,530,690,610)
MAX_STONE_CONTROL_DELTA=40
MIN_WATER_BLUE_PIXELS=200

def sha(b):return hashlib.sha256(b).hexdigest()
def check(ok,msg):
    if not ok:raise ValueError(msg)

def capture_cases(version=VERSION):
    check(version==VERSION,"R06 requires the original Macaw Minecraft 1.21.11 release")
    candidates=[c for c in kitchen.capture_cases(version) if c.case_id==SINK_CASE]
    check(len(candidates)==1,"Original S43 water sink is not uniquely selected")
    candidate=candidates[0]
    check(candidate.state()=="mcwfurnitures:oak_kitchen_sink[facing=north,water=true]",
          "Original historical S43 water=true state differs")
    return tuple(candidates)

def prepare_r06_datapack(pack):
    """Append repeatable actual-server state check without modifying original S43."""
    root=Path(pack)/"data/mcfr_r06/function"
    root.mkdir(parents=True,exist_ok=False)
    case=capture_cases()[0]
    place=Path(pack)/"data/mcfr_chair/function/place.mcfunction"
    content=place.read_text(encoding="utf-8")
    check(content.count("setblock "+str(case.x)+" "+str(case.y)+" "+str(case.z)+" "+case.state())==1,
          "One original 1-5 S43 state must be placed in disposable world")
    commands=[
      f"execute if block {case.x} {case.y} {case.z} {case.state()} run say MCFR_R06_S43_STABLE=PASS",
      f"execute unless block {case.x} {case.y} {case.z} {case.state()} run say MCFR_R06_S43_STABLE=FAIL",
      "say MCFR_R06_STATE_READ",
    ]
    f=root/"verify.mcfunction"
    f.write_text("\n".join(commands)+"\n",encoding="utf-8")
    return {"verify_sha256":sha(f.read_bytes()),"source_state":case.state()}

def pixel_delta(a,b,roi,threshold=24):
    aa=a.convert("RGB").crop(roi)
    bb=b.convert("RGB").crop(roi)
    check(aa.size==bb.size,"R06 same-camera ROI dimensions differ")
    return sum(1 for p,q in zip(aa.getdata(),bb.getdata())
               if max(abs(x-y) for x,y in zip(p,q))>=threshold)

def blue_water_pixels(image):
    source=image.convert("RGB").crop(WATER_ROI)
    return sum(1 for r,g,b in source.getdata()
               if b>r+35 and b>g+10 and b>100)

def compare_frames(folder):
    from PIL import Image
    path=Path(folder)
    images={}
    for case in ORDER:
        p=path/(case+".png")
        check(p.is_file(),"Missing real Minecraft native R06 time frame: "+case)
        with Image.open(p) as im:
            im.load()
            check(im.format=="PNG" and im.size==(1024,684),
                  "Real F2 native R06 resolution/format invalid")
            images[case]=im.convert("RGB")
    water={k:blue_water_pixels(images[k]) for k in ORDER}
    check(min(water.values())>=MIN_WATER_BLUE_PIXELS,
          "Original S43 blue water not visible in every time-separated frame: "+str(water))
    pairs=((ORDER[0],ORDER[1]),(ORDER[1],ORDER[2]),(ORDER[0],ORDER[2]))
    details={}
    for a,b in pairs:
        details[a+"_vs_"+b]={
            "water_changed_pixels":pixel_delta(images[a],images[b],WATER_ROI),
            "sink_changed_pixels":pixel_delta(images[a],images[b],SINK_ROI),
            "stone_control_changed_pixels":pixel_delta(images[a],images[b],STONE_CONTROL_ROI),
        }
    max_control=max(x["stone_control_changed_pixels"] for x in details.values())
    check(max_control<=MAX_STONE_CONTROL_DELTA,
          "R06 stone background control changed; cannot distinguish animation from scene drift: "+
          str(max_control))
    moving=any(x["water_changed_pixels"]>0 for x in details.values())
    return {
        "water_roi":list(WATER_ROI),"sink_roi":list(SINK_ROI),
        "stone_control_roi":list(STONE_CONTROL_ROI),
        "foreground_blue_water_pixels_each_frame":water,
        "paired_pixel_differences":details,
        "max_background_stone_control_delta":max_control,
        "water_pixel_changed_observed":moving,
        "temporal_interpretation":(
            "WATER_REGION_CHANGED_AT_SAMPLED_TIMES_NOT_CAUSAL_ANIMATION_PROOF"
            if moving else "NO_WATER_REGION_CHANGE_AT_SAMPLED_TIMES_NOT_PROOF_ANIMATION_ABSENT"),
        "color_channel_difference_threshold":24,
    }

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"Original pinned Macaw version mismatch")
    case=capture_cases()[0]
    original=kitchen.validate_running_source(Path(game)/"mods")
    model=original["states"][SINK_CASE]
    dry=original["states"][SOURCE_CASE]
    check(original["mod_jar_sha256"]==MACAW_SHA256 and
          model["source_faces"]==56 and dry["source_faces"]==55 and
          model["source_elements"]==17 and dry["source_elements"]==16,
          "Actual source JAR 1-5 S43/S42 water extra face/element differs")
    folder=Path(output)
    folder.mkdir(parents=True,exist_ok=False)
    log=folder/"client.log"
    screenshots=Path(game)/"screenshots"
    times={}
    hashes={}
    verify_events=[]
    with log.open("wb") as out,subprocess.Popen(
       command,cwd=game,env=env,stdout=out,stderr=subprocess.STDOUT
    ) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*arguments):
            return subprocess.check_output(["xdotool",*arguments],env=env,text=True,timeout=18).strip()
        def focus():xdo("windowfocus","--sync",windows[0]);sleep(.35)
        def send(txt):
            focus()
            xdo("key","--clearmodifiers","t");sleep(.55)
            xdo("type","--clearmodifiers","--delay","22",txt)
            xdo("key","--clearmodifiers","Return")
        def camera(pose):
            for retry in range(3):
                offset=len(read())
                send("/tp @s "+pose)
                try:
                    wait_for(proc,lambda:"[RenderAudit: Teleported RenderAudit to" in read()[offset:],
                             "R06 original S43 camera pose",28)
                    sleep(3)
                    return
                except ValueError as exc:
                    if "Timed out waiting" not in str(exc) or retry==2:raise
                    sleep(2)
        def verify_server():
            mark=len(read())
            send("/function mcfr_r06:verify")
            wait_for(proc,lambda:"MCFR_R06_STATE_READ" in read()[mark:],
                     "R06 repeated actual server source state",35)
            data=read()[mark:]
            check("MCFR_R06_S43_STABLE=PASS" in data and
                  "MCFR_R06_S43_STABLE=FAIL" not in data,
                  "Original water=true state changed between F2 time samples")
            verify_events.append({"source_state":case.state(),"PASS":True,
                                  "log_region_sha256":sha(data.encode("utf-8"))})
        def screenshot(key):
            before=set(screenshots.glob("*.png"))
            focus();xdo("key","--clearmodifiers","F1");sleep(.75)
            stamp=monotonic_ns()
            xdo("key","--clearmodifiers","F2")
            imgs=wait_for(proc,lambda:[
                f for f in screenshots.glob("*.png")
                if f not in before and f.read_bytes().endswith(b"IEND\xaeB\x60\x82")
            ],"actual native F2 time "+key,85)
            xdo("key","--clearmodifiers","F1")
            check(len(imgs)==1,"Unexpected original F2 image count")
            dest=folder/(key+".png")
            shutil.copyfile(imgs[0],dest)
            with Image.open(dest) as im:
                im.verify()
            times[key]=stamp
            hashes[key]=sha(dest.read_bytes())
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "Macaw original Fabric world loaded",160)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"Only one real Minecraft window accepted")
            focus();sleep(4)
            xdo("mousemove","--window",windows[0],"512","342");xdo("click","1");sleep(1.2)
            send("/gamemode spectator");sleep(1)
            camera("0.5 124 42.5 180 20")
            send("/function mcfr_chair:place")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_PLACED" in read(),
                     "S43 original sink world stage",100)
            send("/function mcfr_chair:verify")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_STATES_READ" in read(),
                     "original sink world state",40)
            check("MCFR_CHAIR_STATE_S43=PASS" in read() and
                  "MCFR_CHAIR_STATE_S43=FAIL" not in read(),
                  "Original S43 water=true failed its initial server state")
            camera(case.camera())
            screenshots.mkdir(exist_ok=True)
            for i,key in enumerate(ORDER):
                if i:
                    elapsed=(monotonic_ns()-times[ORDER[i-1]])/1e9
                    if elapsed<MIN_INTERVAL_SECONDS:sleep(MIN_INTERVAL_SECONDS-elapsed)
                verify_server()
                screenshot(key)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=20)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    time_intervals=[
        round((times[ORDER[i]]-times[ORDER[i-1]])/1e9,3)
        for i in range(1,len(ORDER))]
    check(len(verify_events)==3 and min(time_intervals)>=MIN_INTERVAL_SECONDS,
          "R06 has no real >=8s separation or 3 server-state checks")
    metrics=compare_frames(folder)
    summary={
      "schema":"MCFR_INT4_F11E_R06_SOURCE_PINNED_MACAW_TEMPORAL_REAL_F2/v1",
      "status":"CAPTURED_REAL_S43_THREE_TIME_SEPARATED_F2_NOT_YET_INDEPENDENTLY_AUDITED",
      "risk_id":"R06","source_historical_case_id":SINK_CASE,
      "minecraft_version":VERSION,"source_state":case.state(),
      "source_jar_sha256":MACAW_SHA256,
      "source_registry":model,
      "historical_source_ledger_sha256":original["historical_application_csv_sha256"],
      "original_source_prior_audit_sha256":original["prior_int4_source_checkpoint_sha256"],
      "dry_source_faces":dry["source_faces"],"wet_source_faces":model["source_faces"],
      "game_integrated_server_state_checks":len(verify_events),
      "state_check_evidence":verify_events,
      "real_monotonic_F2_capture_clock_ns":times,
      "real_time_intervals_seconds":time_intervals,
      "native_F2_png_sha256":hashes,
      "native_F2_count":len(hashes),
      "original_game_client_log_sha256":sha(log.read_bytes()),
      "pixel_analysis":metrics,
      "time_separated_capture_proven":True,
      "time_change_implies_animation":False,
      "full_F_approved":0,"INT5_semantics_approved":0,
      "INT6_training_or_redistribution_rights_approved":0,
      "limitations":[
        "Sampled exact same water=true blockstate 3 times using actual game F2 at >=8 sec intervals.",
        "No pixel difference proves only sampled static appearance, not absence of animation.",
        "Pixel difference can indicate texture/frame changes but needs source/UI causal proof before calling it water animation.",
        "One real original S43 sink at one position; no user water toggle/flow or material semantic approval.",
        "Native PNG/JAR remain in 45-day Actions artifact not Git repository.",
        "No F final, INT5, INT6 or R08 approval."
      ],
    }
    (folder/MANIFEST).write_text(
        json.dumps(summary,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    return summary

def audit(folder):
    from PIL import Image
    folder=Path(folder)
    j=json.loads((folder/MANIFEST).read_text(encoding="utf-8"))
    check(j["status"]=="CAPTURED_REAL_S43_THREE_TIME_SEPARATED_F2_NOT_YET_INDEPENDENTLY_AUDITED"
          and j["schema"]=="MCFR_INT4_F11E_R06_SOURCE_PINNED_MACAW_TEMPORAL_REAL_F2/v1"
          and j["source_state"]==capture_cases()[0].state() and
          j["source_jar_sha256"]==MACAW_SHA256 and
          j["game_integrated_server_state_checks"]==j["native_F2_count"]==3,
          "R06 temporal real Minecraft provenance invalid")
    check(len(j["real_time_intervals_seconds"])==2 and
          min(j["real_time_intervals_seconds"])>=MIN_INTERVAL_SECONDS,
          "R06 original F2 lacks two independent >=8s clock gaps")
    check(len(j["native_F2_png_sha256"])==3 and set(j["native_F2_png_sha256"])==set(ORDER),
          "Not exactly 3 original native R06 frames")
    for key,digest in j["native_F2_png_sha256"].items():
        check(sha((folder/(key+".png")).read_bytes())==digest,
              "Native PNG SHA changed "+key)
        with Image.open(folder/(key+".png")) as img:
            img.verify()
    metrics=compare_frames(folder)
    check(j["pixel_analysis"]==metrics,"R06 original foreground/control pixels not reproducible")
    check(sha((folder/"client.log").read_bytes())==j["original_game_client_log_sha256"],
          "Original Macaw client log changed")
    log=(folder/"client.log").read_text(encoding="utf-8",errors="replace")
    check(log.count("MCFR_R06_S43_STABLE=PASS")>=3 and
          "MCFR_R06_S43_STABLE=FAIL" not in log,
          "Real server checks not all PASS during time-series")
    check((j["full_F_approved"],j["INT5_semantics_approved"],
           j["INT6_training_or_redistribution_rights_approved"])==(0,0,0),
          "Wrongly approved final research/rights")
    verdict={
      "schema":"MCFR_INT4_F11E_R06_THREE_NATIVE_TEMPORAL_F2_AUDIT/v1",
      "status":"PASS_R06_3_TIME_SEPARATED_EXACT_STATE_NATIVE_F2_NO_ANIMATION_CAUSAL_CLAIM",
      "risk_id":"R06","historical_source_case":"S43",
      "source_mod_jar_sha256":MACAW_SHA256,
      "real_exact_server_state_checks":3,
      "original_native_F2_count":3,
      "time_intervals_seconds":j["real_time_intervals_seconds"],
      "pixel_observation":metrics,
      "native_F2_sha256":j["native_F2_png_sha256"],
      "original_client_log_sha256":j["original_game_client_log_sha256"],
      "water_animation_causally_proven":False,
      "full_F_approved":0,"INT5_semantics_approved":0,
      "INT6_training_or_redistribution_rights_approved":0,
    }
    (folder/AUDIT_FILE).write_text(
        json.dumps(verdict,sort_keys=True,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return verdict

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,required=True)
    a=p.parse_args(argv)
    print(json.dumps(audit(a.directory),ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
