"""INT-4-F11B vanilla fence, pressure plate, open barrel, chiseled bookshelf and wool native F2.

Five original V03/V04/V06/V08/V09 study cases; source multipart selects 12 models for 5 states. Uses official-server
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
from .chair_capture_isolation_audit import specimen_color_pixels,CENTER_RECT
from . import int4_macaw_kitchen_capture as kitchen

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.11"
ORDER=("V03","V04","V06","V08","V09")
POSITIONS=(-40,-20,0,20,40)
EXPECTED={
    "V03":("oak_fence",{"east":"false","north":"true","south":"false","west":"false"},2,3,16),
    "V04":("oak_pressure_plate",{"powered":"false"},1,1,6),
    "V06":("barrel",{"facing":"north","open":"true"},1,1,6),
    "V08":("chiseled_bookshelf",{"facing":"north",
           "slot_0_occupied":"true","slot_1_occupied":"false",
           "slot_2_occupied":"false","slot_3_occupied":"false",
           "slot_4_occupied":"false","slot_5_occupied":"false"},7,7,11),
    "V09":("white_wool",{},1,1,6),
}
APPS="research/furniture_mods/phase_1-5/B/APPLICATIONS.csv"
PIN_LEDGER_SHA256="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
MOJANG_CLIENT_SHA1="ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd"
MOJANG_CLIENT_SHA256="1473c9489ac50fda3c435049a76a70d61a10b8610db27f5ba9d8756b686cd3bd"
MANIFEST="INT4_F11B_VANILLA_FIVE_REAL_F2_CAPTURE.json"
AUDIT_FILE="INT4_F11B_VANILLA_FIVE_F2_AUDIT.json"
CONTACT="INT4_F11B_VANILLA_FIVE_F2_CONTACT.png"

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
    check(sha(raw)==PIN_LEDGER_SHA256,"Frozen original 1-5 applications SHA changed")
    all_rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    selected={key:[r for r in all_rows if r["case"]==key] for key in ORDER}
    for key,(block,state,count,elements,faces) in EXPECTED.items():
        group=selected[key]
        check(len(group)==count,f"Original 1-5 model application count changed: {key}")
        check(len({(r["cohort"],r["minecraft"],r["block"],r["state"],r["state_sha"]) for r in group})==1,
              "Original case row properties inconsistent: "+key)
        first=group[0]
        check(first["cohort"]=="VANILLA" and first["minecraft"]==VERSION and
              first["block"]==block and json.loads(first["state"])==state,
              "Original exact 1-5 vanilla case diverged "+key)
        check(sum(int(r["elements"]) for r in group)==elements and
              sum(int(r["faces"]) for r in group)==faces and
              all(r["geometry_status"]=="STATIC_SOURCE" and
                  r["model_hash_kind"]=="GIT_BLOB_SHA1" and
                  all(len(r[k+"_sha"])==40 for k in ("state","model","provider"))
                  for r in group),"Original geometry/source Git blob invalid "+key)
        check(len({r["model_path"] for r in group})==count,
              "Unexpected repeated selected model "+key)
    check(sum(len(x) for x in selected.values())==12 and
          sum(v[3] for v in EXPECTED.values())==13 and
          sum(v[4] for v in EXPECTED.values())==45,
          "F11B original denominators changed")
    return selected,sha(raw)


def capture_cases(version=VERSION,root=ROOT):
    check(version==VERSION,"F11B strictly requires official Minecraft 1.21.11")
    source,_=source_rows(root)
    cases=tuple(SourceCase(k,VERSION,"VANILLA_F11B_"+k,
           "minecraft:"+source[k][0]["block"],
           ";".join(a+"="+b for a,b in json.loads(source[k][0]["state"]).items()),
           x,Y,40)
           for k,x in zip(ORDER,POSITIONS))
    check(len(cases)==5 and len({c.case_id for c in cases})==5 and
          all(abs(c.x-other.x)>=16 for i,c in enumerate(cases)
              for other in cases[i+1:]),"F11B locations overlap")
    return cases


def prepare_fence_neighbor_datapack(pack):
    """Add a REAL north fence neighbor before V03; do not fake north=true.

    The exact historical multi-part case requires a northern connected segment.
    The neighbor is placed physically in the disposable world, NOT as a model
    or texture manipulation. Exact final server properties remain required.
    """
    location=Path(pack)/"data/mcfr_chair/function/place.mcfunction"
    data=location.read_text(encoding="utf-8")
    fence=next(c for c in capture_cases() if c.case_id=="V03")
    line=f"setblock {fence.x} {fence.y} {fence.z} {fence.state()}"
    check(data.count(line)==1,"F11B fence historical placement not unique")
    before=f"setblock {fence.x} {fence.y} {fence.z-1} minecraft:oak_fence"
    # Put neighbor after V03 base to force both adjacent connections; this
    # triggers Minecraft's ordinary neighbor rule in the actual game.
    data=data.replace(line,line+"\n"+before)
    location.write_text(data,encoding="utf-8")
    return before


def matches_when(value,properties):
    if value is None:return True
    check(isinstance(value,dict),"Multipart when must be object or omitted")
    if "OR" in value:
        return any(matches_when(v,properties) for v in value["OR"])
    if "AND" in value:
        return all(matches_when(v,properties) for v in value["AND"])
    return all(str(properties.get(k,"")).lower() in {s.lower() for s in str(v).split("|")}
               for k,v in value.items())


def verify_running_source(command,root=ROOT):
    check("-cp" in command,"Official Mojang client classpath unavailable")
    import os
    client=Path(command[command.index("-cp")+1].split(os.pathsep)[0])
    check(client.is_file(),"Official running 1.21.11 Mojang client not found")
    data=client.read_bytes()
    check(hashlib.sha1(data).hexdigest()==MOJANG_CLIENT_SHA1 and
          sha(data)==MOJANG_CLIENT_SHA256,"Official Mojang client version/SHA changed")
    study,ledger=source_rows(root)
    states={}
    with ZipFile(client) as archive:
        for case in capture_cases(root=root):
            group=study[case.case_id]
            properties=json.loads(group[0]["state"])
            source_state=group[0]["state_path"]
            state_data=archive.read(source_state)
            check(git_blob(state_data)==group[0]["state_sha"],
                  "Original blockstate SHA changed "+case.case_id)
            state_rules=json.loads(state_data.decode("utf-8-sig"))
            selected={}
            if "variants" in state_rules:
                check(len(group)==1,"Only single model expected for vanilla variants")
                options=list(state_rules["variants"].items())
                r=group[0]
                index=int(r["rule_index"])
                check(index<len(options),"Source variant index absent")
                selector,choices=options[index]
                check(kitchen.parse_selector(selector)==properties,
                      "Frozen original selector differs from Mojang "+case.case_id)
                check(sum(kitchen.parse_selector(key)==properties
                          for key,_ in options)==1,
                      "Exactly one variant must select historic state")
                if isinstance(choices,list):choice=choices[int(r["option_index"])]
                else:
                    check(int(r["option_index"])==0,"Unexpected weighted vanilla variant")
                    choice=choices
                selected[index]=choice
            else:
                check("multipart" in state_rules,"Vanilla multipart or variant source missing")
                rules=state_rules["multipart"]
                enabled={index for index,entry in enumerate(rules)
                         if matches_when(entry.get("when"),properties)}
                expected={int(r["rule_index"]) for r in group}
                check(enabled==expected,
                      f"Actual multipart selection differs: {case.case_id} expected={expected} actual={enabled}")
                for r in group:
                    index=int(r["rule_index"])
                    choices=rules[index]["apply"]
                    if isinstance(choices,list):choice=choices[int(r["option_index"])]
                    else:
                        check(int(r["option_index"])==0,"Unexpected multipart weighted option")
                        choice=choices
                    selected[index]=choice
            results=[]
            for r in group:
                choice=selected[int(r["rule_index"])]
                check(kitchen.model_path(choice["model"])==r["model_path"] and
                      int(choice.get("x",0))==int(r["x"]) and
                      int(choice.get("y",0))==int(r["y"]) and
                      int(bool(choice.get("uvlock",False)))==int(r["uvlock"]) and
                      int(choice.get("weight",1))==int(r["weight"]),
                      "Original model/rotation/uvlock differs "+case.case_id+"/"+r["model_path"])
                source_files={}
                for target in (r["model_path"],r["provider_path"]):
                    if target not in source_files:
                        content=archive.read(target)
                        check(git_blob(content)==r["model_sha" if target==r["model_path"] else "provider_sha"],
                              "Original selected model or provider SHA changed "+target)
                        source_files[target]=json.loads(content.decode("utf-8-sig"))
                path=r["model_path"]
                provider=r["provider_path"]
                chain=[]
                if path!=provider:
                    ancestor=source_files[path];seen={path}
                    for _ in range(16):
                        ref=ancestor.get("parent")
                        check(ref,"Original provider not reached: "+path)
                        parent=kitchen.model_path(ref)
                        check(parent not in seen,"Cyclic Mojang source inheritance")
                        seen.add(parent)
                        raw=archive.read(parent)
                        chain.append({"path":parent,"git_blob_sha1":git_blob(raw)})
                        ancestor=json.loads(raw.decode("utf-8-sig"))
                        if parent==provider:break
                    check(chain and chain[-1]["path"]==provider and
                          chain[-1]["git_blob_sha1"]==r["provider_sha"],
                          "Original frozen geometry provider not in actual source ancestry: "+path)
                elements=source_files[provider].get("elements",[])
                check(len(elements)==int(r["elements"]) and
                      sum(len(e.get("faces",{})) for e in elements)==int(r["faces"]),
                      "Original model geometry changed "+path)
                results.append({
                    "original_rule_index":int(r["rule_index"]),
                    "original_option_index":int(r["option_index"]),
                    "model_path":path,
                    "model_git_blob_sha1":r["model_sha"],
                    "provider_path":provider,
                    "provider_git_blob_sha1":r["provider_sha"],
                    "model_y":int(r["y"]),
                    "model_uvlock":int(r["uvlock"]),
                    "model_x":int(r["x"]),
                    "elements":int(r["elements"]),
                    "faces":int(r["faces"]),
                    "official_parent_chain_git_blob_sha1":chain,
                })
            states[case.case_id]={
                "original_state":case.state(),
                "blockstate_path":source_state,
                "blockstate_git_blob_sha1":group[0]["state_sha"],
                "multipart_source":len(group)>1,
                "original_applications":results,
                "selected_model_application_count":len(results),
                "elements":sum(x["elements"] for x in results),
                "faces":sum(x["faces"] for x in results),
            }
    check(set(states)==set(ORDER) and
          sum(x["selected_model_application_count"] for x in states.values())==12 and
          sum(x["elements"] for x in states.values())==13 and
          sum(x["faces"] for x in states.values())==45,
          "Original V03/V08 12 applications/13 elements/45 faces not validated")
    return {"official_client_jar_sha1":MOJANG_CLIENT_SHA1,
            "official_client_jar_sha256":MOJANG_CLIENT_SHA256,
            "source_ledger_sha256":ledger,
            "hash_algorithm":"GIT_BLOB_SHA1",
            "states":states,
            "original_multipart_selection_independently_checked":True,
            "no_minecraft_copyright_assets_committed":True}


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
                    check(size==[1024,684],"Real game F2 resolution changed")
                    visible=(chroma >= (25 if case.case_id=="V04" else 100) or
                             (case.case_id=="V09" and neutral_white>=300))
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
                    "original_model_applications":source["original_applications"],
                    "original_blockstate_sha1":source["blockstate_git_blob_sha1"],
                    "original_model_application_count":source["selected_model_application_count"],
                    "original_source_elements":source["elements"],
                    "original_source_faces":source["faces"],
                    "server_state_verified":True,"native_f2_verified":True,
                    "screen_foreground_chroma_pixels":chroma,
                    "screen_foreground_neutral_white_pixels":neutral_white,
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
    check(len(rows)==5,"Not all five F11 original source cases generated real F2 images")
    output_doc={
        "schema":"MCFR_INT4_F11B_VANILLA_MULTIPART_FIVE_REAL_F2/v1",
        "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
        "minecraft_version":VERSION,"actual_game_capture":True,
        "source_state_verified_count":5,"minecraft_native_f2_screenshot_count":5,
        "original_source_registry":registry,
        "states":rows,"client_log_sha256":sha(log.read_bytes()),
        "semantic_part_roles_approved":0,"material_style_approved":0,
        "copyright_or_ai_training_approved":0,
        "limitations":[
            "Static model states were explicitly placed with /setblock, not assembled via natural adjacency",
            "V03 physical north fence neighbor is placed and final source state read; natural player construction transitions are not broadly approved",
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
    check(doc["status"]=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED" and
          doc["minecraft_version"]==VERSION and
          doc["source_state_verified_count"]==doc["minecraft_native_f2_screenshot_count"]==5,
          "Five exact original vanilla source state trials not complete")
    source=doc["original_source_registry"]
    check(source["official_client_jar_sha1"]==MOJANG_CLIENT_SHA1 and
          source["official_client_jar_sha256"]==MOJANG_CLIENT_SHA256 and
          source["source_ledger_sha256"]==source_rows()[1] and
          source["original_multipart_selection_independently_checked"] is True,
          "Original Mojang SHA/multipart source selection not verified")
    cases={item["case_id"]:item for item in doc["states"]}
    check(set(cases)==set(ORDER) and len(doc["states"])==5,
          "Five cases missing/duplicated")
    for key in ORDER:
        row=cases[key];original=source["states"][key]
        check(row["original_state"]==original["original_state"] and
              row["original_model_applications"]==original["original_applications"] and
              row["original_blockstate_sha1"]==original["blockstate_git_blob_sha1"] and
              row["original_model_application_count"]==len(original["original_applications"]) and
              row["original_source_elements"]==original["elements"] and
              row["original_source_faces"]==original["faces"] and
              row["server_state_verified"] and row["native_f2_verified"] and
              row["screen_foreground_visible_by_color_or_white_proxy"] is True and
              row["screenshot_dimensions"]==[1024,684] and
              row["semantic_or_rights_approved"] is False,
              "F11B original source case game/source pair did not match "+key)
        if key=="V09":
            check(row["screen_foreground_neutral_white_pixels"]>=300,
                  "V09 requires actual visible white foreground, color-only proxy insufficient")
        picture=folder/(key+".png")
        check(sha(picture.read_bytes())==row["screenshot_sha256"],
              "Original game screenshot SHA drift "+key)
        with Image.open(picture) as im:
            im.verify()
        with Image.open(picture) as im:
            check(im.format=="PNG" and im.size==(1024,684),
                  "Actual F2 dimensions invalid "+key)
    check(sha((folder/"client.log").read_bytes())==doc["client_log_sha256"],
          "Actual game source log SHA mismatches")
    result={
        "schema":"MCFR_INT4_F11B_FIVE_VANILLA_MULTIPART_SOURCE_F2/v1",
        "status":"PASS_FIVE_VANILLA_MULTIPART_12111_EXACT_STATE_NATIVE_F2_NOT_FINAL",
        "original_historical_case_ids":list(ORDER),
        "original_model_applications":12,
        "original_source_elements":13,
        "original_source_faces":45,
        "real_game_server_exact_states":5,
        "real_game_native_F2_count":5,
        "official_client_sha1":MOJANG_CLIENT_SHA1,
        "official_client_sha256":MOJANG_CLIENT_SHA256,
        "original_applications_source_sha256":source_rows()[1],
        "source_cases":source["states"],
        "native_F2_sha256":{key:cases[key]["screenshot_sha256"] for key in ORDER},
        "native_F2_visible_pixel_counts":{key:{
            "chroma":cases[key]["screen_foreground_chroma_pixels"],
            "neutral_white":cases[key]["screen_foreground_neutral_white_pixels"]
        } for key in ORDER},
        "client_log_sha256":doc["client_log_sha256"],
        "full_F_approved":0,
        "INT5_part_semantics_approved":0,
        "INT6_AI_training_or_redistribution_rights_approved":0,
        "limitations":[
            "Two-model V03 fence and seven-model V08 chiseled bookshelf source multipart selected in official client.",
            "V03 northern neighbor was a real placed fence block but natural gameplay updates outside this trial not proven.",
            "V08 inventory contents, actual book insertion, pixel UV and item rendering not approved.",
            "V06 open=true /setblock verified, but player-driven opening, inventory and behavior not tested.",
            "V04 pressure plate power dynamics and V09 white wool semantic roles not approved.",
            "PNG and client log SHA does not prove image causal or AI asset redistribution rights."
        ],
    }
    (folder/AUDIT_FILE).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--directory",required=True,type=Path)
    args=p.parse_args(argv)
    print(json.dumps(audit(args.directory),sort_keys=True,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
