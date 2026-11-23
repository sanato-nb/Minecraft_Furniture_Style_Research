"""INT-4-F11D V11 actual vanilla 1.21.11 white bed special-render evidence.

Historical V11 selected block model has ZERO ordinary JSON elements. This
experiment verifies official Mojang JSON SHA, actual two-block head/foot
server states, and pixel differences from two same-camera AIR-control F2.
Evidence for rendered bed != a direct renderer call-site or rights approval.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from time import sleep
from zipfile import ZipFile

from .chair_runtime_fixture import Y
from .runtime_capture import wait_for
from . import int4_macaw_kitchen_capture as kitchen
from .int4_f11c_vanilla_kitchen_decor_four_capture import SourceCase

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.11"
APPS="research/furniture_mods/phase_1-5/B/APPLICATIONS.csv"
STUDY_SHA256="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
MOJANG_CLIENT_SHA1="ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
MOJANG_CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
MODEL_SHA1="9406a8491ed2532d4878b0a91b16a0e5f8d93d80"
STATE_SHA1="6577c90a27efb34a7099150253c0bf557d75214c"
CASE="V11"
X=0
Z=40
MANIFEST="INT4_F11D_V11_WHITE_BED_REAL_F2_CAPTURE.json"
AUDIT="INT4_F11D_V11_WHITE_BED_NATIVE_F2_AUDIT.json"
ROI=(345,260,680,600)
MIN_BED_AIR_CHANGED=700
MAX_AIR_CONTROL_CHANGED=250

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def check(value,message):
    if not value:raise ValueError(message)

def original_case(root=ROOT):
    data=(Path(root)/APPS).read_bytes()
    check(sha(data)==STUDY_SHA256,"Historical 1-5 application ledger SHA changed")
    rows=list(csv.DictReader(data.decode("utf-8-sig").splitlines()))
    matching=[r for r in rows if r["case"]==CASE]
    check(len(matching)==1,"V11 original application not uniquely present")
    row=matching[0]
    check((row["cohort"],row["minecraft"],row["category"],
           row["block"],row["state"],row["geometry_status"],
           row["model_hash_kind"],int(row["elements"]),int(row["faces"]))==
          ("VANILLA",VERSION,"BED","white_bed","{}","NO_ORDINARY_ELEMENTS",
           "GIT_BLOB_SHA1",0,0),"Original V11 study exact state or geometry was changed")
    check(row["state_sha"]==STATE_SHA1 and row["model_sha"]==MODEL_SHA1,
          "Exact historical V11 model or blockstate Git blob drift")
    check(not row["provider_path"] and not row["provider_sha"],
          "Historical V11 must have NO ordinary geometry provider")
    return row

def feet():
    return SourceCase(CASE,VERSION,"VANILLA_F11D_BED_SPECIAL",
        "minecraft:white_bed","facing=north;part=foot;occupied=false",X,Y,Z)

def head():
    return f"minecraft:white_bed[facing=north,part=head,occupied=false]"

def capture_cases(version=VERSION):
    check(version==VERSION,"F11D requires official Minecraft 1.21.11 only")
    original_case()
    return (feet(),)

def prepare_bed_datapack(pack):
    """A bed is physically two blocks. Stage only the stone AIR control.

    Official Java 1.21.11 strict setblock preserves both original bed halves
    without intermediate shape update; actual final state of BOTH blocks is
    independently queried via the real integrated server.
    """
    p=Path(pack)
    place=p/"data/mcfr_chair/function/place.mcfunction"
    raw=place.read_text(encoding="utf-8")
    case=feet()
    original=f"setblock {X} {Y} {Z} {case.state()}"
    check(raw.count(original)==1,"Original fixture foot placement not unique")
    raw=raw.replace(original,f"setblock {X} {Y} {Z} minecraft:air strict")
    raw=raw.replace("say MCFR_CHAIR_PLACED",
                    f"setblock {X} {Y} {Z-1} minecraft:air strict\nsay MCFR_CHAIR_PLACED")
    place.write_text(raw,encoding="utf-8")
    namespace=p/"data/mcfr_bed/function"
    namespace.mkdir(parents=True,exist_ok=False)
    commands={
        "confirm_air":[
            f"execute if block {X} {Y} {Z} minecraft:air run say MCFR_BED_AIR_FOOT=PASS",
            f"execute if block {X} {Y} {Z-1} minecraft:air run say MCFR_BED_AIR_HEAD=PASS",
            "say MCFR_BED_AIR_VERIFIED",
        ],
        "construct":[
            f"setblock {X} {Y} {Z} {case.state()} strict",
            f"setblock {X} {Y} {Z-1} {head()} strict",
            "say MCFR_BED_CONSTRUCTED",
        ],
        "verify":[
            f"execute if block {X} {Y} {Z} {case.state()} run say MCFR_BED_FOOT=PASS",
            f"execute unless block {X} {Y} {Z} {case.state()} run say MCFR_BED_FOOT=FAIL",
            f"execute if block {X} {Y} {Z-1} {head()} run say MCFR_BED_HEAD=PASS",
            f"execute unless block {X} {Y} {Z-1} {head()} run say MCFR_BED_HEAD=FAIL",
            "say MCFR_BED_STATES_READ",
        ],
    }
    for name,lines in commands.items():
        (namespace/(name+".mcfunction")).write_text("\n".join(lines)+"\n",encoding="utf-8")
    return {name:sha((namespace/(name+".mcfunction")).read_bytes())
            for name in commands}

def verify_running_source(command):
    check("-cp" in command,"Official client classpath absent")
    import os
    client=Path(command[command.index("-cp")+1].split(os.pathsep)[0])
    check(client.is_file(),"Actual client JAR not found")
    content=client.read_bytes()
    check(hashlib.sha1(content).hexdigest()==MOJANG_CLIENT_SHA1 and
          sha(content)==MOJANG_CLIENT_SHA256,
          "Actual Mojang client JAR is not source-pinned 1.21.11")
    study=original_case()
    with ZipFile(client) as jar:
        block=jar.read(study["state_path"])
        model=jar.read(study["model_path"])
        check(git_blob(block)==STATE_SHA1 and git_blob(model)==MODEL_SHA1,
              "Original white-bed model/state bytes SHA differ from official client")
        state=json.loads(block.decode("utf-8-sig"))
        leaf=json.loads(model.decode("utf-8-sig"))
        check(isinstance(state.get("variants"),dict),"Actual bed state variants missing")
        options=list(state["variants"].items())
        index=int(study["rule_index"])
        check(len(options)>index,"Historical selected variant index unavailable")
        selector,choice=options[index]
        check(kitchen.parse_selector(selector)=={} and
              len([s for s,_ in options if kitchen.parse_selector(s)=={}])==1,
              "Exact historical V11 variant selector must be unique")
        if isinstance(choice,list):
            choice=choice[int(study["option_index"])]
        else:
            check(int(study["option_index"])==0,"Invalid historical bed option")
        check(kitchen.model_path(choice["model"])==study["model_path"] and
              all(int(choice.get(k,0))==int(study[k]) for k in ("x","y")) and
              int(bool(choice.get("uvlock",False)))==int(study["uvlock"]),
              "Original bed model selection or rotation changed")
        check(not leaf.get("elements") and not study["provider_path"],
              "V11 has ordinary model elements unexpectedly: NOT special renderer pathway")
        # BedRenderer is named in mapping, but a distributed JAR can obfuscate
        # class names. A class name guess is NOT treated as execution proof.
        renderer_matches=[name for name in jar.namelist()
                          if name.endswith(("/BedRenderer.class",
                                            "/BedBlockEntityRenderer.class"))]
        texture="assets/minecraft/textures/entity/bed/white.png"
        texture_sha=sha(jar.read(texture)) if texture in jar.namelist() else None
    return {
        "official_client_sha1":MOJANG_CLIENT_SHA1,
        "official_client_sha256":MOJANG_CLIENT_SHA256,
        "historical_study_sha256":STUDY_SHA256,
        "blockstate_path":study["state_path"],"blockstate_git_blob_sha1":STATE_SHA1,
        "model_path":study["model_path"],"model_git_blob_sha1":MODEL_SHA1,
        "model_ordinary_elements":0,"model_ordinary_faces":0,
        "ordinary_geometry_provider":None,
        "variant_selector":selector,
        "bed_renderer_mapped_class_name_matches_not_proof":renderer_matches,
        "bed_white_entity_texture_in_client_sha256_if_bundled":texture_sha,
        "block_entity_renderer_direct_instrumentation_approved":False,
        "source_renderer_inference_only":True,
    }

def changed_pixels(left,right,rectangle=ROI,cutoff=24):
    a=left.convert("RGB").crop(rectangle)
    b=right.convert("RGB").crop(rectangle)
    check(a.size==b.size,"Bed F2 paired rectangle dimension mismatch")
    return sum(1 for p,q in zip(a.getdata(),b.getdata())
               if max(abs(x-y) for x,y in zip(p,q))>=cutoff)

def image_metrics(directory):
    from PIL import Image
    directory=Path(directory)
    images={}
    for key in ("V11_AIR_A","V11_AIR_B","V11_BED","V11_BED_SIDE"):
        path=directory/(key+".png")
        check(path.is_file(),"Original Minecraft native F2 missing "+key)
        with Image.open(path) as png:
            png.load()
            check(png.format=="PNG" and png.size==(1024,684),
                  "Real Minecraft native F2 dimensions not exact "+key)
            images[key]=png.convert("RGB")
    air_jitter=changed_pixels(images["V11_AIR_A"],images["V11_AIR_B"])
    bed_delta=changed_pixels(images["V11_AIR_B"],images["V11_BED"])
    check(air_jitter<=MAX_AIR_CONTROL_CHANGED,
          "AIR control frames differ too much to attribute visual effect: "+str(air_jitter))
    check(bed_delta>=MIN_BED_AIR_CHANGED and bed_delta>air_jitter*5,
          "Original bed F2 shows no distinguishable new geometry over air control: "+
          str({"air_jitter":air_jitter,"bed_delta":bed_delta}))
    return {"air_control_changed_pixels":air_jitter,
            "bed_vs_air_changed_pixels":bed_delta,
            "roi":list(ROI),
            "threshold":24,
            "baseline_air_control_max":MAX_AIR_CONTROL_CHANGED,
            "bed_min_changed":MIN_BED_AIR_CHANGED,
            "air_same_camera_verified":True}

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"Bed requires official 1.21.11")
    original=verify_running_source(command)
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    log=output/"client.log"
    screenshots=game/"screenshots"
    screenshots.mkdir(exist_ok=True)
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,
                                           text=True,timeout=18).strip()
        def focus():
            xdo("windowfocus","--sync",windows[0]);sleep(.35)
        def send(command_text):
            focus()
            xdo("key","--clearmodifiers","t")
            sleep(.55)
            xdo("type","--clearmodifiers","--delay","22",command_text)
            xdo("key","--clearmodifiers","Return")
        def camera(pose):
            for attempt in range(3):
                n=len(read())
                send("/tp @s "+pose)
                try:
                    wait_for(proc,lambda:"[RenderAudit: Teleported RenderAudit to" in read()[n:],
                             "V11 camera teleport",27)
                    sleep(3)
                    return
                except ValueError as exc:
                    if "Timed out waiting" not in str(exc) or attempt==2:raise
                    sleep(2)
        def snap(key):
            target=output/(key+".png")
            before=set(screenshots.glob("*.png"))
            focus()
            xdo("key","--clearmodifiers","F1")
            sleep(.7)
            xdo("key","--clearmodifiers","F2")
            files=wait_for(proc,lambda:[
                p for p in screenshots.glob("*.png")
                if p not in before and p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
            ],"actual vanilla bed native F2 "+key,90)
            xdo("key","--clearmodifiers","F1")
            check(len(files)==1,"Exactly one actual F2 screenshot required")
            with Image.open(files[0]) as im:
                im.load()
                check(im.format=="PNG" and im.size==(1024,684),
                      "Original F2 screenshot dimensions wrong")
            shutil.copyfile(files[0],target)
            return sha(target.read_bytes())
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "Official Mojang client joined world",165)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"One real Minecraft GUI required")
            focus();sleep(4)
            xdo("mousemove","--window",windows[0],"512","342")
            xdo("click","1");sleep(1.2)
            send("/gamemode spectator");sleep(1)
            camera("0.5 124 42.5 180 20")
            send("/function mcfr_chair:place")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_PLACED" in read(),
                     "stone bed stage prepared",100)
            send("/function mcfr_bed:confirm_air")
            wait_for(proc,lambda:"[RenderAudit] MCFR_BED_AIR_VERIFIED" in read(),
                     "AIR baseline server state read",40)
            check("MCFR_BED_AIR_FOOT=PASS" in read() and
                  "MCFR_BED_AIR_HEAD=PASS" in read(),
                  "Both original bed coordinates not AIR before placement")
            camera(feet().camera())
            hashes={}
            hashes["V11_AIR_A"]=snap("V11_AIR_A")
            sleep(1.5)
            hashes["V11_AIR_B"]=snap("V11_AIR_B")
            send("/function mcfr_bed:construct")
            wait_for(proc,lambda:"[RenderAudit] MCFR_BED_CONSTRUCTED" in read(),
                     "two original bed blocks constructed strict",50)
            send("/function mcfr_bed:verify")
            wait_for(proc,lambda:"[RenderAudit] MCFR_BED_STATES_READ" in read(),
                     "actual bed foot/head states read",50)
            check("MCFR_BED_FOOT=PASS" in read() and "MCFR_BED_HEAD=PASS" in read() and
                  "MCFR_BED_FOOT=FAIL" not in read() and
                  "MCFR_BED_HEAD=FAIL" not in read(),
                  "Real vanilla bed has nonmatching actual foot/head blockstates")
            sleep(4)
            hashes["V11_BED"]=snap("V11_BED")
            camera("3.5 123 39.5 90 28")
            hashes["V11_BED_SIDE"]=snap("V11_BED_SIDE")
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    proc.kill();proc.wait()
    metrics=image_metrics(output)
    doc={
        "schema":"MCFR_INT4_F11D_REAL_MOJANG_12111_WHITE_BED_SPECIAL_F2/v1",
        "status":"ACTUAL_V11_BED_AIR_CONTROL_AND_TWO_PART_F2_NOT_YET_INDEPENDENTLY_AUDITED",
        "minecraft_version":VERSION,
        "original_historical_case_id":CASE,
        "original_study_row_ordinary_elements":0,
        "original_study_row_ordinary_faces":0,
        "server_foot_exact":True,
        "server_head_exact":True,
        "original_foot_state":feet().state(),
        "original_head_state":head(),
        "head_position":[X,Y,Z-1],"foot_position":[X,Y,Z],
        "actual_native_F2_images":hashes,
        "same_camera_air_control_and_bed_pixel_metrics":metrics,
        "original_source_and_renderer_boundary":original,
        "original_client_log_sha256":sha(log.read_bytes()),
        "direct_renderer_callsite_tracing_approved":False,
        "original_two_part_bed_client_render_screenshot_accepted_conditionally":True,
        "full_F_approved":0,"INT5_part_semantics_approved":0,
        "INT6_training_and_redistribution_rights_approved":0,
        "limitations":[
            "V11 historic source blockstate has {} variant; captured facing=north part=foot and part=head are game runtime properties.",
            "Original selected JSON model has 0 elements; actual visual pixels are evidence for a non-ordinary-render pathway, not proof of which Java method executed.",
            "strict setblock preserves two linked parts but does not simulate player placement, sleeping, occupancy or bed explosion.",
            "Control-versus-bed pixel difference is not exact UV face mapping, renderer call-site instrumentation or licensed asset redistribution.",
            "All native PNG and client JAR remain in expiring Actions artifacts, not the Git source tree."
        ],
    }
    (output/MANIFEST).write_text(
        json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return doc

def audit(folder):
    folder=Path(folder)
    report=json.loads((folder/MANIFEST).read_text(encoding="utf-8"))
    check(report["schema"]=="MCFR_INT4_F11D_REAL_MOJANG_12111_WHITE_BED_SPECIAL_F2/v1" and
          report["status"]=="ACTUAL_V11_BED_AIR_CONTROL_AND_TWO_PART_F2_NOT_YET_INDEPENDENTLY_AUDITED" and
          report["minecraft_version"]==VERSION and report["original_historical_case_id"]==CASE and
          report["original_study_row_ordinary_elements"]==0 and
          report["original_study_row_ordinary_faces"]==0 and
          report["server_foot_exact"] and report["server_head_exact"],
          "Historical V11 special render state/bytes incomplete")
    check(report["original_foot_state"]==feet().state() and
          report["original_head_state"]==head(),
          "Original bed exact foot/head server states changed")
    source=report["original_source_and_renderer_boundary"]
    check(source["official_client_sha1"]==MOJANG_CLIENT_SHA1 and
          source["official_client_sha256"]==MOJANG_CLIENT_SHA256 and
          source["historical_study_sha256"]==STUDY_SHA256 and
          source["blockstate_git_blob_sha1"]==STATE_SHA1 and
          source["model_git_blob_sha1"]==MODEL_SHA1 and
          source["model_ordinary_elements"]==0 and source["model_ordinary_faces"]==0 and
          source["block_entity_renderer_direct_instrumentation_approved"] is False,
          "Original model absent ordinary elements/source mismatch")
    check(set(report["actual_native_F2_images"])==
          {"V11_AIR_A","V11_AIR_B","V11_BED","V11_BED_SIDE"},
          "Two AIR + bed frontal + bed side F2 are all required")
    metrics=image_metrics(folder)
    check(metrics==report["same_camera_air_control_and_bed_pixel_metrics"],
          "Native F2 paired pixel metrics are not repeatable")
    for key,digest in report["actual_native_F2_images"].items():
        check(sha((folder/(key+".png")).read_bytes())==digest,
              "Original native F2 PNG SHA drift "+key)
    raw=(folder/"client.log").read_bytes()
    check(sha(raw)==report["original_client_log_sha256"],
          "Actual client log SHA changed")
    log=raw.decode("utf-8",errors="replace")
    for marker in ("MCFR_BED_AIR_FOOT=PASS","MCFR_BED_AIR_HEAD=PASS",
                   "MCFR_BED_FOOT=PASS","MCFR_BED_HEAD=PASS",
                   "MCFR_BED_CONSTRUCTED","MCFR_BED_STATES_READ"):
        check(marker in log,"Native client log missing real server blockstate marker "+marker)
    check("MCFR_BED_FOOT=FAIL" not in log and "MCFR_BED_HEAD=FAIL" not in log,
          "Bed server reported mismatched states")
    check(report["full_F_approved"]==report["INT5_part_semantics_approved"]==
          report["INT6_training_and_redistribution_rights_approved"]==0,
          "No unconditional model/meaning/AI rights approval")
    result={
        "schema":"MCFR_INT4_F11D_REAL_V11_TWO_PART_SPECIAL_F2_SOURCE_AUDIT/v1",
        "status":"PASS_V11_REAL_TWO_PART_BED_AIR_CONTROL_NATIVE_F2_NOT_FINAL_GATE",
        "historical_case_id":CASE,
        "official_client_sha256":MOJANG_CLIENT_SHA256,
        "original_study_sha256":STUDY_SHA256,
        "source_model_git_blob_sha1":MODEL_SHA1,
        "source_blockstate_git_blob_sha1":STATE_SHA1,
        "original_no_ordinary_elements_or_faces":True,
        "real_game_two_exact_server_blockstates":2,
        "actual_original_native_F2_PNG_count":4,
        "same_camera_air_vs_bed_pixel_contrast":metrics,
        "native_F2_png_sha256":report["actual_native_F2_images"],
        "client_log_sha256":report["original_client_log_sha256"],
        "direct_special_renderer_java_call_verified":False,
        "full_F_approved":0,
        "INT5_part_semantics_approved":0,
        "INT6_AI_training_or_redistribution_rights_approved":0,
        "limits":["This is a conditional actual bed visible-source exception with 0 ordinary model faces.",
                  "Native two-part states are strict-staged, NOT player interaction or guaranteed naturally formed bed.",
                  "Java BedRenderer invocation is inferred from state/screenshot, not instrumented.",
                  "No animation, pixel UV causal, gameplay, semantic, asset rights or final F gate approval."]
    }
    (folder/AUDIT).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def main(argv=None):
    parser=argparse.ArgumentParser(description="Audit F11D original V11 native bed F2")
    parser.add_argument("--directory",type=Path,required=True)
    args=parser.parse_args(argv)
    print(json.dumps(audit(args.directory),ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
