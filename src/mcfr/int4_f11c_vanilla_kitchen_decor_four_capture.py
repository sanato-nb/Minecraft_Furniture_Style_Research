"""INT-4-F11C source-pinned vanilla cauldron, water cauldron, lantern and flower pot F2.

Four historical 1-5 source rows V12–V15 (36 elements/154 faces) are
verified against the actual Mojang client. V11 bed has ZERO ordinary model
elements and is deliberately not in this normal-model capture path.
Original F2 and client logs stay in GitHub Actions artifacts; no final
UV/semantic/animation/licensing approvals.
"""from __future__ import annotations

import argparse
from dataclasses import dataclass
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from time import sleep
from zipfile import ZipFile

from .chair_runtime_fixture import Y
from .runtime_capture import wait_for
from .chair_capture_isolation_audit import specimen_color_pixels,CENTER_RECT
from . import int4_macaw_kitchen_capture as kitchen

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.11"
ORDER=("V12","V13","V14","V15")
POSITIONS=(-30,-10,10,30)
EXPECTED={
    "V12":("cauldron",{},13,58),
    "V13":("water_cauldron",{"level":"3"},14,59),
    "V14":("lantern",{"hanging":"false"},4,15),
    "V15":("flower_pot",{},5,22),
}
APPS="research/furniture_mods/phase_1-5/B/APPLICATIONS.csv"
PIN_LEDGER_SHA256="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
MOJANG_CLIENT_SHA1="ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
MOJANG_CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
MANIFEST="INT4_F11C_VANILLA_FOUR_REAL_F2_CAPTURE.json"
AUDIT_FILE="INT4_F11C_VANILLA_FOUR_F2_AUDIT.json"
CONTACT="INT4_F11C_VANILLA_FOUR_F2_CONTACT.png"

def neutral_dark_specimen_pixels(image):
    """Dark gray cauldron proxy, independently checked against the real PNG."""
    region=image.crop(CENTER_RECT).convert("RGB")
    return sum(1 for r,g,b in region.getdata()
               if 28<max(r,g,b)<158 and max(r,g,b)-min(r,g,b)<21)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def check(condition,message):
    if not condition:raise ValueError(message)

def neutral_white_specimen_pixels(image):
    """Second foreground proxy for white couches; never proves UV or semantics."""
    region=image.crop(CENTER_RECT).convert("RGB")
    return sum(1 for r,g,b in region.getdata()
               if min(r,g,b)>205 and max(r,g,b)-min(r,g,b)<26)

@dataclass(frozen=True)
class SourceCase:
    case_id:str
    version:str
    model_key:str
    block_id:str
    properties:str
    x:int
    y:int
    z:int
    facing:str="north"
    def state(self):
        return self.block_id+("["+self.properties.replace(";",",")+"]" if self.properties else "")
    def camera(self):
        return f"{self.x+0.5:g} {self.y+2.3:g} {self.z+5.5:g} 180 20"

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


def source_rows(root=ROOT):
    raw=(Path(root)/APPS).read_bytes()
    check(sha(raw)==PIN_LEDGER_SHA256,"Historic 1-5 original 74-applications source changed")
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    selected={key:[r for r in rows if r["case"]==key] for key in ORDER}
    check(all(len(v)==1 for v in selected.values()),"F11 original case count mismatch")
    for case,(block,state,elements,faces) in EXPECTED.items():
        r=selected[case][0]
        check(r["cohort"]=="VANILLA" and r["minecraft"]==VERSION and
              r["block"]==block and json.loads(r["state"])==state and
              r["model_hash_kind"]=="GIT_BLOB_SHA1" and
              r["geometry_status"]=="STATIC_SOURCE" and
              int(r["elements"])==elements and int(r["faces"])==faces,
              "Original vanilla study row mismatch "+case)
        check(all(len(r[k+"_sha"])==40 for k in ("state","model","provider")),
              "Expected source Git blob SHA1 not plain SHA256: "+case)
    check((sum(v[2] for v in EXPECTED.values()),sum(v[3] for v in EXPECTED.values()))
          ==(36,154),"Research model denominators changed")
    return {k:v[0] for k,v in selected.items()},sha(raw)


def capture_cases(version=VERSION,root=ROOT):
    check(version==VERSION,"Vanilla F11 strictly requires official Minecraft 1.21.11")
    rows,_=source_rows(root)
    cases=tuple(SourceCase(k,VERSION,"VANILLA_F11_"+k,
           "minecraft:"+rows[k]["block"],
           ";".join(a+"="+b for a,b in json.loads(rows[k]["state"]).items()),
           x,Y,40)
           for k,x in zip(ORDER,POSITIONS))
    check(len(cases)==4 and len({c.case_id for c in cases})==4 and
          all(abs(c.x-other.x)>=16 for i,c in enumerate(cases)
              for other in cases[i+1:]),"F11 original states overlap")
    return cases


def verify_running_source(command,root=ROOT):
    check("-cp" in command,"Mojang client classpath not supplied")
    cp=command[command.index("-cp")+1]
    import os
    client=Path(cp.split(os.pathsep)[0])
    check(client.is_file(),"Official running Minecraft client JAR missing")
    jar_bytes=client.read_bytes()
    check(hashlib.sha1(jar_bytes).hexdigest()==MOJANG_CLIENT_SHA1 and
          sha(jar_bytes)==MOJANG_CLIENT_SHA256,
          "Running Minecraft client differs from Mojang 1.21.11 pinned JAR")
    rows,ledger=source_rows(root)
    cases=capture_cases(root=root)
    records={}
    with ZipFile(client) as zip_:
        for case in cases:
            original=rows[case.case_id]
            files={original[a+"_path"]:original[a+"_sha"]
                   for a in ("state","model","provider")}
            loaded={}
            for path,hash_ in files.items():
                raw=zip_.read(path)
                check(git_blob(raw)==hash_,"Official vanilla source Git blob differs: "+path)
                loaded[path]=json.loads(raw.decode("utf-8-sig"))
            blockstate=loaded[original["state_path"]]
            check("variants" in blockstate and isinstance(blockstate["variants"],dict),
                  "F11 non-variant special source not eligible "+case.case_id)
            rules=list(blockstate["variants"].items())
            ri=int(original["rule_index"])
            check(0<=ri<len(rules),"Original variant selector index missing")
            selector,options=rules[ri]
            check(kitchen.parse_selector(selector)==json.loads(original["state"]),
                  "Original variant source selection differs "+case.case_id)
            if isinstance(options,list):
                oi=int(original["option_index"])
                check(0<=oi<len(options),"Missing historical model option")
                option=options[oi]
            else:
                check(int(original["option_index"])==0,"Unexpected vanilla option index")
                option=options
            check(kitchen.model_path(option["model"])==original["model_path"] and
                  int(option.get("x",0))==int(original["x"]) and
                  int(option.get("y",0))==int(original["y"]) and
                  int(bool(option.get("uvlock",False)))==int(original["uvlock"]) and
                  int(option.get("weight",1))==int(original["weight"]),
                  "Official vanilla selected model/rotation/uvlock changed: "+case.case_id)
            leaf=loaded[original["model_path"]]
            # Historical provider is the geometry carrier, which need not be
            # the selected leaf's DIRECT parent. Follow actual official JSON
            # parents and retain an evidence hash of each intervening model.
            parent_chain=[]
            seen={original["model_path"]}
            ancestor=leaf
            for _depth in range(16):
                ref=ancestor.get("parent")
                if not ref:
                    break
                path=kitchen.model_path(ref)
                check(path not in seen,"Vanilla source model has cyclic parent: "+path)
                seen.add(path)
                raw=zip_.read(path)
                parent_chain.append({"path":path,"git_blob_sha1":git_blob(raw)})
                ancestor=json.loads(raw.decode("utf-8-sig"))
                if path==original["provider_path"]:
                    break
            if original["model_path"]!=original["provider_path"]:
                check(any(x["path"]==original["provider_path"] for x in parent_chain),
                      "Original study geometry provider not found in official parent chain "+case.case_id+
                      " direct="+str(parent_chain[:2])+
                      " expected="+original["provider_path"])
            provider=loaded[original["provider_path"]]
            elements=provider.get("elements",[])
            check(len(elements)==int(original["elements"]) and
                  sum(len(e.get("faces",{})) for e in elements)==int(original["faces"]),
                  "Original vanilla selected model source geometry differs "+case.case_id)
            records[case.case_id]={
                "original_state":case.state(),
                "model_path":original["model_path"],
                "model_git_blob_sha1":original["model_sha"],
                "provider_git_blob_sha1":original["provider_sha"],
                "blockstate_git_blob_sha1":original["state_sha"],
                "original_model_y":int(original["y"]),
                "official_parent_chain_git_blob_sha1":parent_chain,
                "elements":int(original["elements"]),
                "faces":int(original["faces"]),
            }
    check(set(records)==set(ORDER) and
          sum(x["faces"] for x in records.values())==154,
          "Original F11 five-model source registry incomplete")
    return {
        "official_client_jar_sha1":MOJANG_CLIENT_SHA1,
        "official_client_jar_sha256":MOJANG_CLIENT_SHA256,
        "source_ledger_sha256":ledger,
        "hash_algorithm":"GIT_BLOB_SHA1",
        "states":records,
        "no_original_minecraft_assets_committed":True,
    }

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"Wrong Minecraft client version")
    cases=capture_cases()
    registry=verify_running_source(command)
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    log=output/"client.log"
    screenshots=game/"screenshots"
    rows=[]
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def read_log():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(
                ["xdotool",*args],env=env,text=True,timeout=15).strip()
        def send(text):
            # Minecraft may join the integrated server before Xvfb reliably
            # directs keyboard events to the GLFW client window. Always
            # refocus before sending any server command.
            xdo("windowfocus","--sync",windows[0])
            sleep(.35)
            xdo("key","--clearmodifiers","t")
            sleep(.55)
            xdo("type","--clearmodifiers","--delay","22",text)
            xdo("key","--clearmodifiers","Return")
        def camera(pose):
            for attempt in range(3):
                n=len(read_log())
                send("/tp @s "+pose)
                try:
                    wait_for(proc,lambda:"[RenderAudit: Teleported RenderAudit to" in read_log()[n:],
                             "real F11 camera teleport",26)
                    sleep(3)
                    return
                except ValueError as exc:
                    if "Timed out waiting" not in str(exc) or attempt==2:
                        raise
                    sleep(2)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read_log(),
                     "pinned vanilla client started and joined world",150)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"Exactly one real Minecraft GUI required")
            xdo("windowfocus","--sync",windows[0])
            # Click the real GLFW client surface after the first chunk render
            # (not a guaranteed UI action, so all commands still need log ACK).
            sleep(4)
            xdo("mousemove","--window",windows[0],"512","342")
            xdo("click","1")
            sleep(1.2)
            send("/gamemode spectator")
            sleep(1.0)
            camera("0.5 124 42.5 180 20")
            send("/function mcfr_chair:place")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_PLACED" in read_log(),
                     "four pinned source states placed",100)
            send("/function mcfr_chair:verify")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_STATES_READ" in read_log(),
                     "server state verification",100)
            passed=set();failed=set()
            for line in read_log().splitlines():
                prefix="[RenderAudit] MCFR_CHAIR_STATE_"
                if "[Server thread/" in line and prefix in line:
                    result=line.split(prefix,1)[1].strip()
                    if result.endswith("=PASS"):passed.add(result[:-5])
                    if result.endswith("=FAIL"):failed.add(result[:-5])
            check(passed==set(ORDER) and not failed,
                  "Original F11 source states not retained by real game: "+
                  str({"passed":sorted(passed),"failed":sorted(failed)}))
            screenshots.mkdir(exist_ok=True)
            for case in cases:
                camera(case.camera())
                for attempt in range(3):
                    before=set(screenshots.glob("*.png"))
                    xdo("key","--clearmodifiers","F1")
                    sleep(.75)
                    xdo("key","--clearmodifiers","F2")
                    files=wait_for(proc,lambda:[
                        p for p in screenshots.glob("*.png")
                        if p not in before and p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
                    ],"actual F2 F11 screenshot "+case.case_id,85)
                    xdo("key","--clearmodifiers","F1")
                    check(len(files)==1,"Unexpected Minecraft screenshot count")
                    with Image.open(files[0]) as picture:
                        picture.load()
                        size=list(picture.size)
                        chroma=specimen_color_pixels(picture)
                        neutral_white=neutral_white_specimen_pixels(picture)
                        dark_gray=neutral_dark_specimen_pixels(picture)
                    check(size==[1024,684],"Real game F2 resolution changed")
                    visible=(chroma>=100 or
                             (case.case_id=="V12" and dark_gray>=200))
                    if visible:
                        break
                    if attempt==2:
                        # Save source F2 even when automated visibility gate
                        # rejects it. The run still fails closed.
                        shutil.copyfile(files[0],output/(case.case_id+"_DIAGNOSTIC.png"))
                        raise ValueError("Native F2 not visible via either color proxy: "+
                                         case.case_id+" chroma="+str(chroma)+
                                         " neutral_white="+str(neutral_white))
                    sleep(5)
                dst=output/(case.case_id+".png")
                shutil.copyfile(files[0],dst)
                source=registry["states"][case.case_id]
                rows.append({
                    "case_id":case.case_id,"original_state":case.state(),
                    "original_model_path":source["model_path"],
                    "original_model_git_blob_sha1":source["model_git_blob_sha1"],
                    "original_provider_git_blob_sha1":source["provider_git_blob_sha1"],
                    "original_model_y":source["original_model_y"],
                    "server_state_verified":True,"native_f2_verified":True,
                    "screen_foreground_chroma_pixels":chroma,
                    "screen_foreground_neutral_white_pixels":neutral_white,
                    "screen_foreground_neutral_dark_pixels":dark_gray,
                    "screen_foreground_visible_by_color_or_white_proxy":visible,
                    "screenshot_file":dst.name,"screenshot_dimensions":size,
                    "screenshot_sha256":sha(dst.read_bytes()),
                    "connection_formed_naturally_tested":False,
                    "semantic_or_rights_approved":False
                })
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    proc.kill();proc.wait()
    check(len(rows)==4,"Not all four F11C original source cases generated real F2 images")
    output_doc={
        "schema":"MCFR_INT4_F11C_VANILLA_FOUR_REAL_F2/v1",
        "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
        "minecraft_version":VERSION,"actual_game_capture":True,
        "source_state_verified_count":4,"minecraft_native_f2_screenshot_count":4,
        "original_source_registry":registry,
        "states":rows,"client_log_sha256":sha(log.read_bytes()),
        "semantic_part_roles_approved":0,"material_style_approved":0,
        "copyright_or_ai_training_approved":0,
        "limitations":[
            "Static model states were explicitly placed with /setblock, not assembled via natural adjacency",
            "Four exact original states were verified; V11 bed renderer and dynamic animation are outside this batch",
            "F2 verifies displayed screenshot and foreground proxy, not semantic roles, GPU face mapping, texture causality or licensing",
        ]
    }
    (output/MANIFEST).write_text(json.dumps(output_doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                                 encoding="utf-8")
    return output_doc

def audit(folder):
    from PIL import Image
    folder=Path(folder)
    doc=json.loads((folder/MANIFEST).read_text(encoding="utf-8"))
    check(doc.get("status")=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED" and
          doc.get("actual_game_capture") is True and
          doc.get("minecraft_version")==VERSION and
          doc.get("source_state_verified_count")==4 and
          doc.get("minecraft_native_f2_screenshot_count")==4,
          "Four real client 1.21.11 exact server-state captures missing")
    registry=doc["original_source_registry"]
    check(registry["official_client_jar_sha1"]==MOJANG_CLIENT_SHA1 and
          registry["official_client_jar_sha256"]==MOJANG_CLIENT_SHA256 and
          registry["source_ledger_sha256"]==source_rows()[1] and
          registry["hash_algorithm"]=="GIT_BLOB_SHA1",
          "Original Mojang client or study SHA drift")
    cases={r["case_id"]:r for r in doc["states"]}
    check(set(cases)==set(ORDER) and len(doc["states"])==4,
          "Four historical cases not all present")
    for cid in ORDER:
        record=cases[cid];frozen=registry["states"][cid]
        check(record["original_state"]==frozen["original_state"] and
              record["original_model_path"]==frozen["model_path"] and
              record["original_model_git_blob_sha1"]==frozen["model_git_blob_sha1"] and
              record["original_provider_git_blob_sha1"]==frozen["provider_git_blob_sha1"] and
              record["original_model_y"]==frozen["original_model_y"] and
              record["server_state_verified"] and record["native_f2_verified"] and
              record["screenshot_dimensions"]==[1024,684] and
              record["screen_foreground_visible_by_color_or_white_proxy"] is True and
              record["semantic_or_rights_approved"] is False,
              "Original case F11C game/server model/F2 mismatch "+cid)
        if cid=="V12":
            check(record["screen_foreground_neutral_dark_pixels"]>=200,
                  "Dark cauldron is not visible via independent gray foreground proxy")
        picture=folder/(cid+".png")
        check(sha(picture.read_bytes())==record["screenshot_sha256"],
              "Original F2 SHA changed "+cid)
        with Image.open(picture) as im:
            im.verify()
        with Image.open(picture) as im:
            check(im.format=="PNG" and im.size==(1024,684),
                  "Original native F2 screenshot dimensions invalid "+cid)
    check(sha((folder/"client.log").read_bytes())==doc["client_log_sha256"],
          "Original Minecraft client log SHA mismatch")
    result={
        "schema":"MCFR_INT4_F11C_FOUR_VANILLA_REAL_CLIENT_SOURCE_F2/v1",
        "status":"PASS_FOUR_MOJANG_12111_EXACT_VANILLA_STATES_NATIVE_F2_NOT_FINAL",
        "historical_case_ids":list(ORDER),
        "real_game_exact_server_states":4,
        "original_native_F2_PNG":4,
        "original_source_model_applications":4,
        "original_source_elements":36,
        "original_source_faces":154,
        "official_client_sha1":MOJANG_CLIENT_SHA1,
        "official_client_sha256":MOJANG_CLIENT_SHA256,
        "original_1_5_ledger_sha256":source_rows()[1],
        "source_cases":registry["states"],
        "native_F2_sha256":{k:cases[k]["screenshot_sha256"] for k in ORDER},
        "native_F2_visibility_pixels":{k:{
            "chroma":cases[k]["screen_foreground_chroma_pixels"],
            "dark_gray":cases[k]["screen_foreground_neutral_dark_pixels"]
        } for k in ORDER},
        "client_log_sha256":doc["client_log_sha256"],
        "unconditionally_full_F_approved":0,
        "INT5_part_semantics_approved":0,
        "INT6_training_or_redistribution_rights_approved":0,
        "limitations":[
          "V11 white bed has no ordinary JSON elements, stays HOLD under a separately designed renderer audit.",
          "V13 one animated liquid face and V14 lantern animated texture were not time-separated pixel verified.",
          "Source geometry, runtime state and screenshots do not certify causal UV or UI gameplay.",
          "No semantic/functional/right-to-train/reuse or redistribution approval."
        ]
    }
    (folder/AUDIT_FILE).write_text(
        json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--directory",required=True,type=Path)
    args=p.parse_args(argv)
    print(json.dumps(audit(args.directory),sort_keys=True,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
