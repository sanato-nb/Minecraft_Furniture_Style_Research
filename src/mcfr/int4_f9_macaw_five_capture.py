"""INT-4-F9 Macaw chair stool table drawer source-staged real Fabric F2.

Five historical S08/S09/S11/S12/S23 1-5 source cases. Uses official-server
world fixture and original Fabric 1.21.11 client. States are explicitly
placed with /setblock and verified, NOT claimed to arise via natural
adjacency mechanics. Source SHA, JAR identity, actual PNG SHA and
foreground visibility are fail-closed. No semantic, AI, material or
license approval; original assets/images not committed to the repo.
"""
from __future__ import annotations

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
from .chair_capture_isolation_audit import specimen_color_pixels
from . import int4_macaw_kitchen_capture as kitchen

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.11"
ORDER=("S08","S09","S11","S12","S23")
POSITIONS=(-40,-20,0,20,40)
EXPECTED={
    "S08":("mcwfurnitures:oak_chair","facing=north",12,59),
    "S09":("mcwfurnitures:oak_stool_chair","",6,31),
    "S11":("mcwfurnitures:oak_end_table","east=false;north=false;south=false;west=false",14,52),
    "S12":("mcwfurnitures:oak_coffee_table","connection=with_leg",2,11),
    "S23":("mcwfurnitures:oak_drawer","connection=single;facing=north",5,26),
}
APPS=kitchen.APPS
PRIOR=kitchen.PRIOR
MACAW_SHA256=kitchen.MACAW_SHA256
MANIFEST="INT4_F9_MACAW_FIVE_REAL_F2_CAPTURE.json"
AUDIT_FILE="INT4_F9_MACAW_FIVE_F2_AUDIT.json"
CONTACT="INT4_F9_MACAW_FIVE_F2_CONTACT.png"

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def check(condition,message):
    if not condition:raise ValueError(message)

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

def source_rows(root=ROOT):
    root=Path(root)
    raw=(root/APPS).read_bytes()
    lock=json.loads((root/PRIOR).read_text(encoding="utf-8"))
    proof=lock["observed"]
    check(proof["results"]["cases_checked"]==15 and
          proof["results"]["application_options_reopened"]==19 and
          proof["results"]["faces"]==431 and
          proof["results"]["png_missing_face_refs"]==0 and
          proof["source_ledger_sha256"][APPS]==sha(raw) and
          lock["boundary"]["int5_semantic_parts_approved"]==0,
          "Pinned INT4 15 case source ledger changed")
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    subset={x["case"]:x for x in rows if x["case"] in ORDER}
    check(len(subset)==len(ORDER) and sum(x["case"] in ORDER for x in rows)==5,
          "Original five source cases missing or duplicated")
    for cid,req in EXPECTED.items():
        row=subset[cid]
        block,state,elems,faces=req
        check(row["block"]==block and row["state"]==state and
              int(row["elements"])==elems and int(row["faces"])==faces and
              row["cohort"]=="MACAW" and row["minecraft"]==VERSION and
              row["geometry_status"]=="STATIC_SOURCE" and
              row["model_hash_kind"]=="SHA256",
              "Pinned Macaw original source case changed: "+cid)
    return subset,sha(raw),sha((root/PRIOR).read_bytes())

def capture_cases(version=VERSION,root=ROOT):
    check(version==VERSION,"Macaw F9 F2 experiment pinned to Minecraft 1.21.11")
    rows,_,_=source_rows(root)
    cases=tuple(SourceCase(cid,VERSION,"MACAW_TS_"+cid,
            rows[cid]["block"],rows[cid]["state"],x,Y,40)
            for cid,x in zip(ORDER,POSITIONS))
    check(len(cases)==5 and len({case.case_id for case in cases})==5 and
          all(abs(x.x-y.x)>=16 for i,x in enumerate(cases) for y in cases[i+1:]),
          "Table/bookshelf trial positions overlap")
    return cases

def verify_running_source(mod_dir,root=ROOT):
    cases=capture_cases(root=root)
    expected,ledger_sha,prior_sha=source_rows(root)
    candidates=[]
    for jar in sorted(Path(mod_dir).glob("*.jar")):
        with ZipFile(jar) as source:
            if "assets/mcwfurnitures/blockstates/oak_bookshelf.json" in source.namelist():
                candidates.append(jar)
    check(len(candidates)==1,"Exactly one pinned Macaw bookshelf mod JAR required")
    jar=candidates[0]
    check(sha(jar.read_bytes())==MACAW_SHA256,"Pinned original Macaw JAR SHA256 differs")
    result={}
    with ZipFile(jar) as source:
        for case in cases:
            row=expected[case.case_id]
            files={p:expect for p,expect in (
                (row["state_path"],row["state_sha"]),
                (row["model_path"],row["model_sha"]),
                (row["provider_path"],row["provider_sha"])
            )}
            loaded={}
            for path,hash_ in files.items():
                raw=source.read(path)
                check(sha(raw)==hash_,"Original Macaw source SHA changed: "+path)
                loaded[path]=json.loads(raw.decode("utf-8-sig"))
            states=loaded[row["state_path"]]
            check("variants" in states and isinstance(states["variants"],dict),
                  "Original F9 blockstate not static variants")
            state_selector,options=list(states["variants"].items())[int(row["rule_index"])]
            check(kitchen.parse_selector(state_selector)==
                  kitchen.parse_selector(row["state"].replace(";",",")),
                  "Selected runtime state selector mismatch: "+case.case_id)
            if isinstance(options,list):
                option=options[int(row["option_index"])]
            else:
                check(int(row["option_index"])==0,"Unexpected weighted option index")
                option=options
            check(kitchen.model_path(option["model"])==row["model_path"] and
                  int(option.get("x",0))==int(row["x"]) and
                  int(option.get("y",0))==int(row["y"]) and
                  bool(option.get("uvlock",False))==bool(int(row["uvlock"])) and
                  int(option.get("weight",1))==int(row["weight"]),
                  "Actual selected model/rotation/uvlock differs: "+case.case_id)
            leaf=loaded[row["model_path"]]
            check(kitchen.model_path(leaf["parent"])==row["provider_path"],
                  "Original selected model parent/provenance different: "+case.case_id)
            elements=loaded[row["provider_path"]].get("elements",[])
            check(len(elements)==int(row["elements"]) and
                  sum(len(el.get("faces",{})) for el in elements)==int(row["faces"]),
                  "Original model elements/faces do not reproduce historic case")
            result[case.case_id]={
                "original_state":case.state(),
                "model_path":row["model_path"],
                "model_sha256":row["model_sha"],
                "provider_sha256":row["provider_sha"],
                "blockstate_sha256":row["state_sha"],
                "original_model_y":int(row["y"]),
                "elements":int(row["elements"]),
                "faces":int(row["faces"]),
            }
    check({k:(v["elements"],v["faces"]) for k,v in result.items()}==
          {k:(row[2],row[3]) for k,row in EXPECTED.items()},
          "Original Macaw five-case model geometry drift")
    return {
        "mod_jar_name":jar.name,"mod_jar_sha256":MACAW_SHA256,
        "historical_application_sha256":ledger_sha,
        "previous_int4_checkpoint_sha256":prior_sha,
        "states":result
    }

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"Wrong Minecraft client version")
    cases=capture_cases()
    registry=verify_running_source(game/"mods")
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
            xdo("key","--clearmodifiers","t")
            sleep(.35)
            xdo("type","--clearmodifiers","--delay","14",text)
            xdo("key","--clearmodifiers","Return")
        def camera(pose):
            n=len(read_log())
            send("/tp @s "+pose)
            wait_for(proc,lambda:"[RenderAudit: Teleported RenderAudit to" in read_log()[n:],
                     "real F9 camera teleport",90)
            sleep(3)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read_log(),
                     "pinned Macaw client started and joined world",150)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"Exactly one real Minecraft GUI required")
            xdo("windowfocus","--sync",windows[0])
            sleep(1.6)
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
                  "Original F9 source states not retained by real game: "+
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
                    ],"actual F2 F9 screenshot "+case.case_id,85)
                    xdo("key","--clearmodifiers","F1")
                    check(len(files)==1,"Unexpected Minecraft screenshot count")
                    with Image.open(files[0]) as picture:
                        picture.load()
                        size=list(picture.size)
                        chroma=specimen_color_pixels(picture)
                    check(size==[1024,684],"Real game F2 resolution changed")
                    if chroma>=150:
                        break
                    if attempt==2:
                        raise ValueError("F2 image remained sky-only / foreground absent: "+
                                         case.case_id+" chroma="+str(chroma))
                    sleep(5)
                dst=output/(case.case_id+".png")
                shutil.copyfile(files[0],dst)
                source=registry["states"][case.case_id]
                rows.append({
                    "case_id":case.case_id,"original_state":case.state(),
                    "original_model_path":source["model_path"],
                    "original_model_sha256":source["model_sha256"],
                    "original_provider_sha256":source["provider_sha256"],
                    "original_model_y":source["original_model_y"],
                    "server_state_verified":True,"native_f2_verified":True,
                    "screen_foreground_chroma_pixels":chroma,
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
    check(len(rows)==5,"Not all five F9 original source cases generated real F2 images")
    output_doc={
        "schema":"MCFR_INT4_F9_MACAW_FIVE_REAL_F2/v1",
        "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
        "minecraft_version":VERSION,"actual_game_capture":True,
        "source_state_verified_count":5,"minecraft_native_f2_screenshot_count":5,
        "original_source_registry":registry,
        "states":rows,"client_log_sha256":sha(log.read_bytes()),
        "semantic_part_roles_approved":0,"material_style_approved":0,
        "copyright_or_ai_training_approved":0,
        "limitations":[
            "Static model states were explicitly placed with /setblock, not assembled via natural adjacency",
            "Five F9 source states are game-verified; automatic connected-state transitions were NOT tested",
            "F2 verifies displayed screenshot and foreground proxy, not semantic roles, GPU face mapping, texture causality or licensing",
        ]
    }
    (output/MANIFEST).write_text(json.dumps(output_doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                                 encoding="utf-8")
    return output_doc

def audit(folder):
    from PIL import Image,ImageDraw
    folder=Path(folder)
    manifest=folder/MANIFEST
    document=json.loads(manifest.read_text(encoding="utf-8"))
    check(document.get("schema")=="MCFR_INT4_F9_MACAW_FIVE_REAL_F2/v1" and
          document.get("status")=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED" and
          document.get("actual_game_capture") is True and
          document.get("source_state_verified_count")==
          document.get("minecraft_native_f2_screenshot_count")==5 and
          document.get("semantic_part_roles_approved")==
          document.get("material_style_approved")==
          document.get("copyright_or_ai_training_approved")==0,
          "Original real client / no semantic approvals proof invalid")
    case_map={c.case_id:c for c in capture_cases()}
    rows={r["case_id"]:r for r in document["states"]}
    check(len(rows)==len(document["states"])==5 and set(rows)==set(case_map),
          "Five source case records incomplete")
    source=document["original_source_registry"]
    check(source["mod_jar_sha256"]==MACAW_SHA256 and
          source["historical_application_sha256"]==source_rows()[1],
          "Original running Macaw JAR/source ledger identity unpinned")
    images=[]
    for cid in ORDER:
        record=rows[cid];case=case_map[cid];original=source["states"][cid]
        check(record["original_state"]==case.state() and
              record["original_model_path"]==original["model_path"] and
              record["original_model_sha256"]==original["model_sha256"] and
              record["original_provider_sha256"]==original["provider_sha256"] and
              record["original_model_y"]==original["original_model_y"] and
              record["server_state_verified"] is True and
              record["native_f2_verified"] is True and
              record["connection_formed_naturally_tested"] is False and
              record["semantic_or_rights_approved"] is False and
              record["screen_foreground_chroma_pixels"]>=150 and
              record["screenshot_file"]==cid+".png" and
              record["screenshot_dimensions"]==[1024,684],
              "Pinned source blockstate/f2 evidence mismatch: "+cid)
        file=folder/(cid+".png")
        check(sha(file.read_bytes())==record["screenshot_sha256"],
              "Real F2 PNG image SHA changed: "+cid)
        with Image.open(file) as im:
            im.verify()
        with Image.open(file) as im:
            images.append(im.convert("RGB"))
    width,height=512,342
    panel=Image.new("RGB",(5*width,height+35),(240,240,241))
    draw=ImageDraw.Draw(panel)
    labels=("S08:chair","S09:stool chair","S11:end table","S12:coffee table","S23:drawer")
    for i,(im,label) in enumerate(zip(images,labels)):
        panel.paste(im.resize((width,height),resample=Image.Resampling.BILINEAR),(width*i,0))
        draw.text((width*i+7,height+9),label,fill=(14,14,14))
    picture=folder/CONTACT
    panel.save(picture)
    result={
        "schema":"MCFR_INT4_F9_MACAW_FIVE_F2_AUDIT/v1",
        "status":"PASS_FIVE_ORIGINAL_MACAW_F9_NATIVE_F2_AND_EXACT_SERVER_STATE_NOT_FINAL",
        "source_cases":list(ORDER),
        "source_1_5_face_counts":{cid:source["states"][cid]["faces"] for cid in ORDER},
        "original_source_sha256":source["historical_application_sha256"],
        "native_f2_count":5,"server_verified_states":5,
        "f2_sha256":{cid:rows[cid]["screenshot_sha256"] for cid in ORDER},
        "f2_manifest_sha256":sha(manifest.read_bytes()),
        "contact_sheet_sha256":sha(picture.read_bytes()),
        "visibility_foreground_chroma":{cid:rows[cid]["screen_foreground_chroma_pixels"] for cid in ORDER},
        "boundaries":{
            "explicit_setblock_source_states_verified":True,
            "natural_connected_block_update_rules_tested":False,
            "face_uv_render_pixel_causality_proven":False,
            "int4_all_cases_done":False,
            "int5_part_roles_approved":0,
            "int6_training_or_redistribution_rights_approved":0
        }
    }
    check(result["source_1_5_face_counts"]==
          {k:row[3] for k,row in EXPECTED.items()},
          "Five original selected geometry face counts changed")
    (folder/AUDIT_FILE).write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+"\n",
                                  encoding="utf-8")
    return result

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--directory",required=True,type=Path)
    args=p.parse_args(argv)
    print(json.dumps(audit(args.directory),sort_keys=True,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
