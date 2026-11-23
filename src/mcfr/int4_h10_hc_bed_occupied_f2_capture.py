"""INT-4-H10: actual Fabric Handcrafted occupied foot model versus false and air.

One real Minecraft 1.21.1 Fabric client / same block / same camera / three
native F2 frames. No player sleep, wake, crafting, placement or destruction
testing. Failure closed: if occupied=true is unstable on the integrated
server we DO NOT claim an occupied model F2.

Only original study provenance, GPU screenshot contrasts and model source
matching are reported; per-face pixel-to-UV and part semantics not approved.
"""
from __future__ import annotations
from pathlib import Path
from time import sleep
from zipfile import ZipFile
import argparse,csv,hashlib,json,os,shutil,subprocess
from . import int4_handcrafted_bed_capture as hc
from .runtime_capture import wait_for

VERSION=hc.VERSION
MODEL="handcrafted:oak_fancy_bed"
SOURCE_GIT_COMMIT=hc.HC_COMMIT
RELEASE_SHA1=hc.HC_RELEASE_SHA1
S0="color=white,facing=north,occupied=false,part=foot,shape=single"
S1="color=white,facing=north,occupied=true,part=foot,shape=single"
CASES=("false","true","air")
C=hc.cases()[0]
XYZ=(C.x,C.y,C.z)
POSE=C.camera()
PACK="mcfr_chair"
MODEL_ROOT="common/src/main/generated/resources/assets/handcrafted/models/block/"
PARENT_ROOT="common/src/main/resources/assets/handcrafted/models/block/fancy_bed/"
STATE_FILE="common/src/main/generated/resources/assets/handcrafted/blockstates/oak_fancy_bed.json"
H9_LEDGER=Path("project/integration/INT4_H9_512_OCCUPIED_SOURCE_MODEL_PAIRS_V1.csv")
H9_REPORT=Path("project/integration/INT4_H9_HC_BED_OCCUPIED_SOURCE_AUDIT_V1.json")
MANIFEST="INT4_H10_OCCUPIED_FOOT_NATIVE_F2_CAPTURE_V1.json"
AUDIT="INT4_H10_OCCUPIED_FOOT_REAL_GAME_INDEPENDENT_AUDIT_V1.json"
CONTACT="INT4_H10_OCCUPIED_FALSE_TRUE_AIR_CONTACT.png"

def check(cond,msg):
    if not cond:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()

def capture_case():
    # Only the ORIGINAL S37 false source case is initially set by the data
    # pack. The true source state is later set at the exact SAME coordinate
    # by one explicit /setblock, separately server verified.
    return (C,)

def static_preflight(game):
    rows=list(csv.DictReader((hc.ROOT/H9_LEDGER).open(encoding="utf-8",newline="")))
    selected=[r for r in rows if all((r[k]==v for k,v in
              {"color":"white","facing":"north","shape":"single","part":"foot"}.items()))]
    check(len(selected)==1,"H9 frozen 512 occupied pairs contain no single white north foot")
    row=selected[0]
    h9=json.loads((hc.ROOT/H9_REPORT).read_text(encoding="utf-8"))
    check(h9["status"]=="PASS_1024_STATE_512_PAIR_256_MODEL_FOOT_GEOMETRY_SOURCE_VALIDATED" and
          h9["counts"]["occupied_false_true_pairs"]==512 and
          h9["counts"]["foot_parent_geometry_changed_pairs"]==256,
          "Frozen H9 1024/512 original source study unavailable")
    prior=hc.preflight(game/"mods",os.environ.get("MCFR_HC_SOURCE_ZIP"))
    check(set(prior["cases"])=={"S37","S38"} and prior["source_git_commit"]==SOURCE_GIT_COMMIT and
          prior["HC_release_SHA1"]==RELEASE_SHA1,
          "Original unoccupied study and release provenance missing")
    jars=[]
    for file in (game/"mods").glob("*.jar"):
        with ZipFile(file) as z:
            if "assets/handcrafted/blockstates/oak_fancy_bed.json" in z.namelist():jars.append(file)
    check(len(jars)==1 and hashlib.sha1(jars[0].read_bytes()).hexdigest()==RELEASE_SHA1,
          "Unknown Handcrafted runtime JAR")
    source_zip=Path(os.environ["MCFR_HC_SOURCE_ZIP"])
    selected_model={}
    with ZipFile(source_zip) as orig,ZipFile(jars[0]) as run:
        state=STATE_FILE
        original_json=json.loads(hc.source_zip_file(orig,state))
        installed_json=json.loads(run.read(hc.ref(state)))
        check(original_json==installed_json,"Original and release occupied blockstates differ")
        for occupied, model,sha_git,expected_parent in [
          ("false",row["model_unoccupied"],row["model_unoccupied_git_sha1"],
           "handcrafted:block/fancy_bed/bed_single"),
          ("true",row["model_occupied"],row["model_occupied_git_sha1"],
           "handcrafted:block/fancy_bed/bed_single_occupied"),
        ]:
            key=S1 if occupied=="true" else S0
            _,selector,entry=hc.selected_options(original_json,key.replace(",",";"))
            _,_,installed_entry=hc.selected_options(installed_json,key.replace(",",";"))
            check(entry==installed_entry and entry["model"]==model,
                  "Source/release selected runtime model mismatch")
            path=MODEL_ROOT+model.split(":",1)[1].split("block/",1)[1]+".json"
            original=hc.source_zip_file(orig,path)
            actual=run.read(hc.ref(path))
            check(hc.git_sha(original)==sha_git and json.loads(original)==json.loads(actual),
                  "Source/release occupied leaf model mismatch")
            leaf=json.loads(original)
            check(leaf.get("parent")==expected_parent,
                  "Occupied parent model not selected as source study proved")
            parent=PARENT_ROOT+expected_parent.split("/")[-1]+".json"
            parent_source=hc.source_zip_file(orig,parent)
            parent_runtime=run.read(hc.ref(parent))
            check(json.loads(parent_source)==json.loads(parent_runtime),
                  "Original occupancy parent geometry differs from JAR")
            expected_n=14 if occupied=="true" else 12
            expected_f=84 if occupied=="true" else 72
            parts=json.loads(parent_source)["elements"]
            check(len(parts)==expected_n and sum(len(e["faces"]) for e in parts)==expected_f,
                  "Occupied foot source face counts changed")
            selected_model[occupied]={
                "state":MODEL+"["+key+"]",
                "model":model,
                "model_git_sha1":sha_git,
                "parent":expected_parent,
                "parent_git_sha1":hc.git_sha(parent_source),
                "runtime_leaf_JSON_equal":True,
                "runtime_parent_JSON_equal":True,
                "elements":expected_n,"faces":expected_f,
            }
    return {"original_study":prior,"models":selected_model,
            "release_jar_SHA1":RELEASE_SHA1,
            "H9_source_git_commit":SOURCE_GIT_COMMIT,
            "H9_report_sha256":digest((hc.ROOT/H9_REPORT).read_bytes())}

def command_state(occupied):
    check(occupied in ("false","true"),"Invalid source occupancy state")
    return MODEL+"["+(S0 if occupied=="false" else S1)+"]"

def image_delta(a,b):
    # Counts only RGB changes in the established bed ROI; moving sky/lighting
    # and aliasing can produce extra differences. It is a screening signal,
    # not GPU per-face attribution or a semantic label.
    x=a.convert("RGB").crop((350,275,675,620))
    y=b.convert("RGB").crop((350,275,675,620))
    check(x.size==y.size,"Mismatch in identical camera ROI")
    return sum(max(abs(p[i]-q[i]) for i in range(3))>=24
               for p,q in zip(x.getdata(),y.getdata()))

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"Expected Minecraft 1.21.1")
    source=static_preflight(game)
    dest=Path(output)
    dest.mkdir(parents=True,exist_ok=False)
    log=dest/"client.log"
    shots=game/"screenshots"
    records={}
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,timeout=18,text=True).strip()
        def cmd(text):
            xdo("windowfocus","--sync",window)
            xdo("key","--clearmodifiers","t");sleep(.35)
            xdo("type","--clearmodifiers","--delay","14",text)
            xdo("key","--clearmodifiers","Return")
        def server_cmd(text,marker,label,timeout=50):
            offset=len(read())
            cmd(text)
            wait_for(proc,lambda:marker in read()[offset:],label,timeout)
            sleep(1.4)
        def check_server(name):
            state=command_state(name)
            x,y,z=XYZ
            key=f"MCFR_H10_SOURCE_OCCUPIED_{name.upper()}_SERVER"
            server_cmd(f"/execute if block {x} {y} {z} {state} run say {key}=PASS",
                       "[RenderAudit] "+key+"=PASS",name+" server state",70)
            records[name]={"blockstate":state,"integrated_server_exact":True,
                           "server_log_marker":key+"=PASS"}
        def capture_frame(name):
            before=set(shots.glob("*.png"))
            xdo("key","--clearmodifiers","F1");sleep(.8)
            xdo("key","--clearmodifiers","F2")
            found=wait_for(proc,lambda:[
                p for p in shots.glob("*.png") if p not in before and
                p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
            ],"original native Minecraft F2 "+name,85)
            xdo("key","--clearmodifiers","F1")
            check(len(found)==1,"Not exactly one F2 "+name)
            p=dest/(name+".png")
            shutil.copyfile(found[0],p)
            with Image.open(p) as im:
                im.load();check(im.format=="PNG" and im.size==(1024,684),
                                "Invalid original native F2 dimensions")
            records[name].update({"F2_png":p.name,"F2_sha256":digest(p.read_bytes()),
                                  "dimensions":[1024,684]})
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "actual Fabric Handcrafted world join",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in read(),
                     "original Fabric client GUI fully joined",70)
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"Expected single original Minecraft window")
            window=windows[0]
            xdo("windowfocus","--sync",window);sleep(3)
            server_cmd("/gamemode spectator",
                       "[RenderAudit: Set own game mode to Spectator Mode]",
                       "spectator GUI")
            # One calibrated camera pose is set ONCE; do not alter its
            # position between false, true, or air.
            server_cmd("/tp @s "+POSE,"[RenderAudit: Teleported RenderAudit to",
                       "same F2 camera pose")
            server_cmd("/function mcfr_chair:place",
                       "[RenderAudit] MCFR_CHAIR_PLACED",
                       "original baseline state place",90)
            server_cmd("/function mcfr_chair:verify",
                       "[RenderAudit] MCFR_CHAIR_STATES_READ",
                       "original pinned false source readback")
            check_server("false")
            shots.mkdir(exist_ok=True)
            sleep(7);capture_frame("false")
            x,y,z=XYZ
            # Direct occupancy *source state* override is intentionally
            # separate from player interaction. If the game normalizes to
            # false, integrated server exact-state probe will fail.
            server_cmd(f"/setblock {x} {y} {z} {command_state('true')}",
                       "[RenderAudit: Changed the block at",
                       "occupied true model staging")
            check_server("true")
            sleep(7);capture_frame("true")
            server_cmd(f"/setblock {x} {y} {z} minecraft:air",
                       "[RenderAudit: Changed the block at",
                       "air-only same camera control")
            server_cmd(f"/execute if block {x} {y} {z} minecraft:air run say MCFR_H10_AIR_SERVER=PASS",
                       "[RenderAudit] MCFR_H10_AIR_SERVER=PASS",
                       "original air control server")
            records["air"]={"blockstate":"minecraft:air","integrated_server_exact":True,
                             "server_log_marker":"MCFR_H10_AIR_SERVER=PASS"}
            sleep(6);capture_frame("air")
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    check(set(records)==set(CASES),"Missing source state screenshots")
    frames={}
    with Image.open(dest/"false.png") as a,Image.open(dest/"true.png") as b,Image.open(dest/"air.png") as c:
        frames={
            "occupied_false_vs_true":image_delta(a,b),
            "occupied_false_vs_air":image_delta(a,c),
            "occupied_true_vs_air":image_delta(b,c),
        }
    # Rendering may show different shapes while pixels stay unchanged if
    # buried/occluded. Treat that as CONDITIONAL, not a fake success.
    status=("CAPTURED_OCCUPIED_F2_SOURCE_STATES_WITH_NONZERO_ROI_DIFF"
            if frames["occupied_false_vs_true"]>=100 else
            "CAPTURED_OCCUPIED_F2_BUT_VISIBLE_SOURCE_DIFF_NOT_PROVEN")
    report={
       "schema":"MCFR_INT4_H10_HC_S37_FOOT_OCCUPIED_F2_SAME_CAMERA/v1",
       "status":status,
       "source":source,
       "original_client_log_sha256":digest(log.read_bytes()),
       "minecraft_version":VERSION,"real_Fabric_game_session":True,
       "same_camera_pose_all_three":POSE,
       "native_F2_states":records,
       "roi_RGB_max_channel_threshold":24,
       "roi_pixels":frames,
       "new_game_sessions":1,
       "new_original_native_F2_files":3,
       "gameplay_sleep_wake_destroy_tested":False,
       "per_face_UV_pixel_attribution_approved":False,
       "full_F_H_approvals":0,
       "INT5_semantics_approved":0,
       "INT6_training_or_redistribution_approved":0,
       "limitations":[
          "Occupied state staged by /setblock, explicitly not by sleeping.",
          "Only one pinned white/north/single FOOT state pair, not all 512 pairs.",
          "Same source camera and controlled world does not exclude GPU temporal lighting, aliasing or animations.",
          "Even source geometry change plus screenshot ROI contrast does not prove exact face-to-texture UV mapping.",
          "Original PNGs and game client log must remain in short-lived Actions artifact, not Git repository.",
       ],
    }
    (dest/MANIFEST).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return report

def audit(directory):
    from PIL import Image,ImageDraw
    root=Path(directory)
    doc=json.loads((root/MANIFEST).read_text(encoding="utf-8"))
    check(doc["schema"]=="MCFR_INT4_H10_HC_S37_FOOT_OCCUPIED_F2_SAME_CAMERA/v1" and
          doc["minecraft_version"]==VERSION and doc["real_Fabric_game_session"] is True and
          doc["same_camera_pose_all_three"]==POSE,
          "Original source occupied real-game provenance changed")
    check(set(doc["native_F2_states"])==set(CASES),"Three same-camera frames absent")
    check(doc["source"]["release_jar_SHA1"]==RELEASE_SHA1 and
          doc["source"]["H9_source_git_commit"]==SOURCE_GIT_COMMIT and
          doc["source"]["models"]["false"]["elements"]==12 and
          doc["source"]["models"]["true"]["elements"]==14,
          "Original model parent and runtime JAR evidence missing")
    check(digest((root/"client.log").read_bytes())==doc["original_client_log_sha256"],
          "Actual integrated client log SHA mismatch")
    actual=(root/"client.log").read_text(encoding="utf-8",errors="replace")
    for name in CASES:
        state=doc["native_F2_states"][name]
        check(state["integrated_server_exact"] is True and
              "[RenderAudit] "+state["server_log_marker"] in actual,
              "Game server exact state source evidence missing "+name)
        check(state["F2_png"]==name+".png" and state["dimensions"]==[1024,684],
              "Original native F2 incorrect identity "+name)
        blob=(root/state["F2_png"]).read_bytes()
        check(digest(blob)==state["F2_sha256"],"Actual native F2 SHA mismatch "+name)
        with Image.open(root/state["F2_png"]) as im:
            im.load()
            check(im.format=="PNG" and im.size==(1024,684),"Original actual game PNG invalid")
    with Image.open(root/"false.png") as a,Image.open(root/"true.png") as b,Image.open(root/"air.png") as c:
        contrast={
          "occupied_false_vs_true":image_delta(a,b),
          "occupied_false_vs_air":image_delta(a,c),
          "occupied_true_vs_air":image_delta(b,c),
        }
    check(contrast==doc["roi_pixels"],"Independent reparse ROI changed")
    check(contrast["occupied_false_vs_air"]>=100 and
          contrast["occupied_true_vs_air"]>=100,
          "Source bed not visibly different from air")
    # Captured true/false without visual difference is still valid source
    # but NOT accepted as proof of perceptible model deformation.
    visually_distinct=contrast["occupied_false_vs_true"]>=100
    check(doc["status"]==("CAPTURED_OCCUPIED_F2_SOURCE_STATES_WITH_NONZERO_ROI_DIFF"
          if visually_distinct else "CAPTURED_OCCUPIED_F2_BUT_VISIBLE_SOURCE_DIFF_NOT_PROVEN"),
          "Incorrect color visibility disposition")
    panel=Image.new("RGB",(1024,380),(237,237,237))
    paint=ImageDraw.Draw(panel)
    for i,name in enumerate(CASES):
        with Image.open(root/(name+".png")) as im:
            panel.paste(im.convert("RGB").resize((341,342),Image.Resampling.BILINEAR),(341*i,0))
        paint.text((341*i+6,353),name+" (actual F2)",fill=(22,22,22))
    panel.save(root/CONTACT)
    result={
       "schema":"MCFR_INT4_H10_OCCUPIED_MODEL_FOOT_F2_INDEPENDENT_AUDIT/v1",
       "status":("PASS_SOURCE_STATE_AND_SAME_CAMERA_F2_VISUAL_CONTRAST" if visually_distinct
                 else "CONDITIONAL_SOURCE_STATE_F2_VISUAL_DIFF_NOT_PROVEN"),
       "source_reproduction":doc["source"],
       "minecraft_version":VERSION,
       "source_camera_exact_same_pose":POSE,
       "original_native_F2_sha256":{name:doc["native_F2_states"][name]["F2_sha256"] for name in CASES},
       "original_client_log_sha256":doc["original_client_log_sha256"],
       "original_manifest_sha256":digest((root/MANIFEST).read_bytes()),
       "contact_sheet_sha256":digest((root/CONTACT).read_bytes()),
       "screen_ROI_changed_pixels":contrast,
       "new_gameplay_sleeps_or_breaks":0,
       "full_F70_unconditional_approvals":0,
       "H03_H05_full_exit_approved":False,
       "face_by_face_texture_UV_pixel_causality_approved":False,
       "INT5_semantic_approved":0,
       "INT6_AI_training_redistribution_approved":0,
    }
    (root/AUDIT).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--directory",type=Path,required=True)
    args=ap.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
