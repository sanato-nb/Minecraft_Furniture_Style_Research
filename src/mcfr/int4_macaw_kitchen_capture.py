"""INT-4 real original Fabric F2 experiment: Macaw S41 counter, S42/S43 sink.

This is the NEXT experiment after the 15-case pinned source cross-check.
The original model selection, 1-5 B state, actual installed Macaw JAR SHA,
model and provider SHA are all checked before launching the real Minecraft
1.21.11 client. The disposable world uses an isolated chair *fixture engine*
as a generic single-block /setblock and /execute source-state check; historical
chair case evidence is not changed or reused as kitchen output.

The resulting three native F2 PNGs prove captured states, not physical water
behavior, texture causal equality, object purpose, or rights to train AI.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from time import sleep
from zipfile import ZipFile

from .chair_runtime_fixture import ChairCase,Y
from .runtime_capture import wait_for

ROOT=Path(__file__).resolve().parents[2]
APPS="research/furniture_mods/phase_1-5/B/APPLICATIONS.csv"
PRIOR="project/integration/INT4_NONCHAIR_15_CASES_AUDIT_RESULT.json"
MACAW_SHA256="e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e"
VERSION="1.21.11"
ORDER=("S41","S42","S43")
POSITIONS=(-24,-8,8)
ORIGINAL_EXPECTED={
    "S41":("mcwfurnitures:oak_counter","facing=north",2,11),
    "S42":("mcwfurnitures:oak_kitchen_sink","facing=north;water=false",16,55),
    "S43":("mcwfurnitures:oak_kitchen_sink","facing=north;water=true",17,56),
}
MANIFEST="INT4_MACAW_KITCHEN_REAL_F2_CAPTURE.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check(cond,what):
    if not cond:
        raise ValueError(what)


def source_rows(root=ROOT):
    root=Path(root)
    raw=(root/APPS).read_bytes()
    lock=json.loads((root/PRIOR).read_text(encoding="utf-8"))
    evidence=lock["observed"]
    check(evidence["results"]["cases_checked"]==15 and
          evidence["results"]["application_options_reopened"]==19 and
          evidence["results"]["faces"]==431 and
          evidence["results"]["png_missing_face_refs"]==0 and
          evidence["source_ledger_sha256"][APPS]==sha(raw) and
          lock["boundary"]["int5_semantic_parts_approved"]==0,
          "Historical 15-case original source SHA/scope changed")
    rows=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    matching={r["case"]:r for r in rows if r["case"] in ORDER}
    check(len(matching)==3 and sum(r["case"] in ORDER for r in rows)==3,
          "Macaw kitchen source cases are missing or duplicated")
    for cid in ORDER:
        r=matching[cid]
        block,state,elems,faces=ORIGINAL_EXPECTED[cid]
        check(r["cohort"]=="MACAW" and r["minecraft"]==VERSION and
              r["category"]=="KITCHEN" and r["block"]==block and
              r["state"]==state and r["model_hash_kind"]=="SHA256" and
              r["geometry_status"]=="STATIC_SOURCE" and
              int(r["elements"])==elems and int(r["faces"])==faces,
              "Macaw 1-5 historical kitchen row changed: "+cid)
    return matching,sha(raw),sha((root/PRIOR).read_bytes())


def capture_cases(version=VERSION,root=ROOT):
    if version!=VERSION:raise ValueError("Macaw kitchen study requires Minecraft 1.21.11")
    data,_,_=source_rows(root)
    cases=[]
    for cid,x in zip(ORDER,POSITIONS):
        row=data[cid]
        props={k:v for k,v in
               (s.split("=",1) for s in row["state"].split(";"))}
        check(props.pop("facing",None)=="north","Unverified camera/orientation state")
        selector=",".join(k+"="+v for k,v in props.items())
        cases.append(ChairCase(cid,VERSION,"MACAW_KITCHEN_"+cid,row["block"],
                               selector,"north",x,Y,40))
    check(len(cases)==3 and all(abs(a.x-b.x)>=16
                                for i,a in enumerate(cases) for b in cases[i+1:]),
          "Kitchen staging scene overlap or case loss")
    return tuple(cases)


def parse_selector(selector):
    out={}
    for token in selector.split(","):
        if not token:continue
        k,sep,v=token.partition("=")
        check(sep and k and v and k not in out,"Malformed original source property selector")
        out[k]=v
    return out


def model_path(ref):
    check(isinstance(ref,str) and ref and ".." not in ref,
          "Invalid source model reference")
    if ":" not in ref:ref="minecraft:"+ref
    ns,path=ref.split(":",1)
    check(ns and path and not path.startswith("/"),"Malformed source model path")
    return f"assets/{ns}/models/{path}.json"


def validate_running_source(mod_dir,root=ROOT):
    rows,ledger_sha,prior_sha=source_rows(root)
    jars=[]
    for jar in sorted(Path(mod_dir).glob("*.jar")):
        with ZipFile(jar) as archive:
            if ("assets/mcwfurnitures/blockstates/oak_kitchen_sink.json"
                in archive.namelist()):
                jars.append(jar)
    check(len(jars)==1,"Pinned Macaw 3.4.2 source must appear in one real mod JAR")
    jar=jars[0]
    check(sha(jar.read_bytes())==MACAW_SHA256,
          "Installed Macaw 3.4.2 JAR binary differs from original fixed study")
    result={}
    with ZipFile(jar) as archive:
        for case in capture_cases(root=root):
            row=rows[case.case_id]
            expected={
                row["state_path"]:row["state_sha"],
                row["model_path"]:row["model_sha"],
                row["provider_path"]:row["provider_sha"]
            }
            loaded={}
            for path,expected_sha in expected.items():
                blob=archive.read(path)
                check(sha(blob)==expected_sha,
                      "Pinned source JAR blockstate/leaf/provider SHA changed: "+path)
                loaded[path]=json.loads(blob.decode("utf-8-sig"))
            state=loaded[row["state_path"]]
            check(set(state)=={"variants"} and isinstance(state["variants"],dict),
                  "Original Macaw kitchen blockstate is not exactly static variants")
            options=list(state["variants"].items())
            index=int(row["rule_index"])
            check(0<=index<len(options),"Historical selected option rule not present")
            source_selector,option=options[index]
            check(parse_selector(source_selector)==parse_selector(row["state"].replace(";",",")),
                  "Original runtime JAR source properties differ: "+case.case_id)
            if isinstance(option,list):
                n=int(row["option_index"])
                check(0<=n<len(option),"Historical weighted model option absent")
                option=option[n]
            else:
                check(int(row["option_index"])==0,"Original model option index changed")
            check(model_path(option["model"])==row["model_path"] and
                  int(option.get("x",0))==int(row["x"]) and
                  int(option.get("y",0))==int(row["y"]) and
                  bool(option.get("uvlock",False))==bool(int(row["uvlock"])) and
                  int(option.get("weight",1))==int(row["weight"]),
                  "Original runtime model choice/rotation/UV lock changed: "+case.case_id)
            leaf=loaded[row["model_path"]]
            check(model_path(leaf.get("parent"))==row["provider_path"],
                  "Original kitchen model parent not historical source: "+case.case_id)
            elements=loaded[row["provider_path"]].get("elements",[])
            check(len(elements)==int(row["elements"]) and
                  sum(len(el.get("faces",{})) for el in elements)==int(row["faces"]),
                  "Pinned source geometry does not reproduce 1-5 surface count")
            result[case.case_id]={
                "block_id":row["block"],"source_state":case.state(),
                "source_state_sha256":row["state_sha"],
                "source_model_path":row["model_path"],
                "source_model_sha256":row["model_sha"],
                "source_provider_path":row["provider_path"],
                "source_provider_sha256":row["provider_sha"],
                "source_rule_index":index,
                "source_option_index":int(row["option_index"]),
                "source_model_rotation_y":int(row["y"]),
                "source_elements":int(row["elements"]),
                "source_faces":int(row["faces"]),
            }
    check(len(result)==3 and result["S43"]["source_faces"]-
          result["S42"]["source_faces"]==1,
          "Actual sink water state source surface delta must remain +1")
    return {"mod_jar":jar.name,"mod_jar_sha256":MACAW_SHA256,
            "historical_application_csv_sha256":ledger_sha,
            "prior_int4_source_checkpoint_sha256":prior_sha,
            "states":result}


def capture(command,env,game,output,version):
    from PIL import Image
    cases=capture_cases(version)
    sources=validate_running_source(game/"mods")
    output=Path(output)
    output.mkdir(parents=True,exist_ok=False)
    log=output/"client.log"
    screenshots=game/"screenshots"
    rows=[]
    with log.open("wb") as fd,subprocess.Popen(
        command,cwd=game,env=env,stdout=fd,stderr=subprocess.STDOUT
    ) as proc:
        def read_log():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*a):
            return subprocess.check_output(["xdotool",*a],env=env,timeout=15,text=True).strip()
        def cmd(txt):
            xdo("key","--clearmodifiers","t")
            sleep(0.35)
            xdo("type","--clearmodifiers","--delay","14",txt)
            xdo("key","--clearmodifiers","Return")
        def camera(pos):
            before=len(read_log())
            cmd("/tp @s "+pos)
            wait_for(proc,lambda:"[RenderAudit: Teleported RenderAudit to" in read_log()[before:],
                     "kitchen F2 camera teleport",80)
            sleep(2.5)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read_log(),
                     "new game copy loaded in actual Fabric client",140)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"Exactly one actual Fabric Minecraft GUI required")
            xdo("windowfocus","--sync",windows[0])
            sleep(1.4)
            cmd("/gamemode spectator")
            sleep(0.8)
            camera("0.5 124 42.5 180 20")
            cmd("/function mcfr_chair:place")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_PLACED" in read_log(),
                     "kitchen original blockstate placement",100)
            cmd("/function mcfr_chair:verify")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_STATES_READ" in read_log(),
                     "server verification for original kitchen states",100)
            passed=set();failed=[]
            for line in read_log().splitlines():
                tag="[RenderAudit] MCFR_CHAIR_STATE_"
                if "[Server thread/" in line and tag in line:
                    val=line.split(tag,1)[1].strip()
                    if val.endswith("=PASS"):passed.add(val[:-5])
                    if val.endswith("=FAIL"):failed.append(val[:-5])
            check(passed==set(ORDER) and not failed,
                  "Actual game did not retain source kitchen states: "+
                  str({"matched":sorted(passed),"failed":sorted(failed)}))
            screenshots.mkdir(exist_ok=True)
            for case in cases:
                camera(case.camera())
                before=set(screenshots.glob("*.png"))
                xdo("key","--clearmodifiers","F1")
                sleep(0.8)
                xdo("key","--clearmodifiers","F2")
                imgs=wait_for(proc,lambda:[
                    p for p in screenshots.glob("*.png")
                    if p not in before and p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
                ],"native game F2 kitchen "+case.case_id,75)
                xdo("key","--clearmodifiers","F1")
                check(len(imgs)==1,"Expected exactly one kitchen native F2 frame")
                dest=output/(case.case_id+".png")
                shutil.copyfile(imgs[0],dest)
                with Image.open(dest) as frame:
                    frame.verify()
                with Image.open(dest) as frame:
                    size=list(frame.size)
                check(size==[1024,684],"Native Minecraft F2 dimensions differ")
                source=sources["states"][case.case_id]
                rows.append({
                    "case_id":case.case_id,"block_id":source["block_id"],
                    "original_state":case.state(),
                    "original_model_path":source["source_model_path"],
                    "original_model_sha256":source["source_model_sha256"],
                    "original_provider_sha256":source["source_provider_sha256"],
                    "original_model_y":source["source_model_rotation_y"],
                    "server_blockstate_verified":True,
                    "native_F2_client_capture":True,
                    "screenshot_file":dest.name,
                    "screenshot_dimensions":size,
                    "screenshot_sha256":sha(dest.read_bytes()),
                    "semantic_material_or_rights_approved":False
                })
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    proc.kill();proc.wait()
    check(len(rows)==3,"Missing a source-verified game F2 kitchen frame")
    doc={
        "schema":"MCFR_INT4_MACAW_KITCHEN_ACTUAL_GAME_F2/v1",
        "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
        "minecraft_version":VERSION,
        "actual_game_capture":True,
        "source_state_verified_count":3,
        "minecraft_native_f2_screenshot_count":3,
        "original_source_registry":sources,
        "states":rows,
        "client_log_sha256":sha(log.read_bytes()),
        "semantic_part_roles_approved":0,
        "material_style_approved":0,
        "copyright_or_ai_training_approved":0,
        "limitations":[
            "Three separate kitchen block positions are not registered pixelwise and background/light varies",
            "A +1 source face when water is true does not prove animation, physical water mechanics, or user interaction",
            "The source state is verified on the game server and the PNG is native F2, not a human semantic inspection",
            "The historical 15-case comparison, original model/JAR and earlier screenshot evidence remain untouched",
        ],
    }
    (output/MANIFEST).write_text(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                                 encoding="utf-8")
    return doc


def audit(directory):
    from PIL import Image,ImageDraw
    directory=Path(directory)
    manifest=directory/MANIFEST
    doc=json.loads(manifest.read_text(encoding="utf-8"))
    check(doc.get("schema")=="MCFR_INT4_MACAW_KITCHEN_ACTUAL_GAME_F2/v1" and
          doc.get("status")=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED" and
          doc.get("actual_game_capture") is True and
          doc.get("source_state_verified_count")==doc.get("minecraft_native_f2_screenshot_count")==3 and
          doc.get("semantic_part_roles_approved")==doc.get("material_style_approved")==doc.get("copyright_or_ai_training_approved")==0,
          "Actual game evidence count or research nonapproval contract failed")
    cases={c.case_id:c for c in capture_cases()}
    rows={r["case_id"]:r for r in doc["states"]}
    check(len(rows)==len(doc["states"])==3 and set(rows)==set(cases),
          "Kitchen F2 evidence source case set changed")
    pinned=doc["original_source_registry"]
    check(pinned["mod_jar_sha256"]==MACAW_SHA256 and
          pinned["historical_application_csv_sha256"]==source_rows()[1],
          "Running game mod archive provenance not pinned")
    photos=[]
    for cid in ORDER:
        row=rows[cid]
        check(row["server_blockstate_verified"] and row["native_F2_client_capture"]
              and not row["semantic_material_or_rights_approved"] and
              row["original_state"]==cases[cid].state() and
              row["original_model_sha256"]==pinned["states"][cid]["source_model_sha256"] and
              row["screenshot_file"]==cid+".png" and
              row["screenshot_dimensions"]==[1024,684],
              "One actual F2 case mismatches original selected model/state: "+cid)
        path=directory/(cid+".png")
        check(sha(path.read_bytes())==row["screenshot_sha256"],
              "Actual game screenshot SHA mismatch: "+cid)
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            photos.append(image.convert("RGB"))
    width,height=512,342
    panel=Image.new("RGB",(3*width,height+38),(237,238,240))
    labels=("S41 MACAW counter north","S42 sink water=false north",
            "S43 sink water=true north")
    draw=ImageDraw.Draw(panel)
    for i,(photo,label) in enumerate(zip(photos,labels)):
        panel.paste(photo.resize((width,height),resample=Image.Resampling.BILINEAR),(i*width,0))
        draw.text((i*width+8,height+10),label,fill=(5,5,5))
    out=directory/"INT4_MACAW_KITCHEN_3_F2_CONTACT_SHEET.png"
    panel.save(out)
    result={
        "schema":"MCFR_INT4_MACAW_KITCHEN_3_F2_EVIDENCE_AUDIT/v1",
        "status":"PASS_THREE_REAL_CLIENT_F2_AND_SOURCE_STATES_NOT_SEMANTIC_APPROVAL",
        "source_cases":list(ORDER),
        "actual_native_f2_count":3,
        "server_source_verified_count":3,
        "source_water_false_faces":pinned["states"]["S42"]["source_faces"],
        "source_water_true_faces":pinned["states"]["S43"]["source_faces"],
        "source_water_face_delta":pinned["states"]["S43"]["source_faces"]-pinned["states"]["S42"]["source_faces"],
        "actual_f2_manifest_sha256":sha(manifest.read_bytes()),
        "f2_sha256_by_case":{cid:rows[cid]["screenshot_sha256"] for cid in ORDER},
        "contact_sheet_sha256":sha(out.read_bytes()),
        "scope":{
            "actual_game_screenshot_captured":True,
            "game_runtime_water_mechanism_tested":False,
            "pixelwise_texture_causality_proven":False,
            "human_part_role_review_approved":0,
            "style_or_material_approved":0,
            "ai_training_rights_approved":0,
            "int4_all_furniture_complete":False
        }
    }
    check(result["source_water_face_delta"]==1,
          "Pinned water source geometry face count delta differs")
    (directory/"INT4_MACAW_KITCHEN_F2_AUDIT.json").write_text(
        json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory",required=True,type=Path)
    args=parser.parse_args(argv)
    print("INT4_KITCHEN_F2_AUDIT="+json.dumps(audit(args.directory),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
