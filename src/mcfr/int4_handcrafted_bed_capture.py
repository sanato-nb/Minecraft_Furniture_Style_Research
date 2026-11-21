"""INT-4 Handcrafted S37/S38 actual 1.21.1 Fabric diagnostic F2 experiment.

Original Git blob SHA and runtime JAR selected model semantics are checked
independently. Each part is placed alone, not a naturally assembled bed.
Real F2 photos and server verified states are required. No semantic/rights
approval follows from rendering or from source names.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile
from time import sleep
import argparse,csv,hashlib,json,os,shutil,subprocess

from .chair_runtime_fixture import Y
from .runtime_capture import wait_for
# Bed-specific visual proxy: excludes blue sky and green superflat ground.
# Neither a semantic classifier nor proof of specific textures/material.
def bed_visible_proxy(im):
    roi=im.crop((385,265,640,625)).convert("RGB")
    return sum(1 for rr,gg,bb in roi.getdata()
               if (rr>gg+17 and rr>bb+26 and rr>65) or
                  (rr>125 and abs(rr-gg)<22 and abs(gg-bb)<22))


ROOT=Path(__file__).resolve().parents[2]
APPS="research/furniture_mods/phase_1-5/B/APPLICATIONS.csv"
PRIOR="project/integration/INT4_NONCHAIR_15_CASES_AUDIT_RESULT.json"
VERSION="1.21.1"
HC_COMMIT="8d21d1665916850c3fa3bdaf1370c50ec2ca7035"
HC_RELEASE_SHA1="a9579fecd7ed429c282be21d5c921d220197acc6"
ORDER=("S37","S38")
EXPECTED={
 "S37":("handcrafted:oak_fancy_bed","color=white;facing=north;occupied=false;part=foot;shape=single",12,72),
 "S38":("handcrafted:oak_fancy_bed","color=white;facing=north;occupied=false;part=head;shape=single",1,6)
}
MANIFEST="INT4_HC_BED_SOURCE_F2_CAPTURE.json"
AUDIT="INT4_HC_BED_SOURCE_F2_AUDIT.json"
CONTACT="INT4_HC_BED_TWO_F2_CONTACT.png"

def check(cond,msg):
    if not cond:raise ValueError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def git_sha(raw):return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def ref(path):
    check("assets/" in path and ".." not in path,"Invalid original asset path")
    return "assets/"+path.split("assets/",1)[1]
def source_zip_file(z,path):
    hits=[name for name in z.namelist() if name.endswith("/"+path)]
    check(len(hits)==1,"Original Handcrafted Git archive path missing/ambiguous: "+path)
    return z.read(hits[0])
def selected_options(blob,properties):
    variants=blob.get("variants")
    check(isinstance(variants,dict),"Expected original bed variant declarations")
    expected=dict(part.split("=",1) for part in properties.split(";"))
    hits=[(i,name,v) for i,(name,v) in enumerate(variants.items())
          if dict(token.split("=",1) for token in name.split(","))==expected]
    check(len(hits)==1,"Original or release bed selector not unique: "+properties)
    return hits[0]

def source_rows(root=ROOT):
    raw=(Path(root)/APPS).read_bytes()
    lock=json.loads((Path(root)/PRIOR).read_text())
    proof=lock["observed"]
    check(proof["results"]["cases_checked"]==15 and
          proof["results"]["faces"]==431 and
          proof["results"]["png_missing_face_refs"]==0 and
          proof["source_ledger_sha256"][APPS]==sha(raw) and
          lock["boundary"]["int5_semantic_parts_approved"]==0,
          "Historical INT-4 1-5 15 case checkpoint changed")
    entries=list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    rows={r["case"]:r for r in entries if r["case"] in ORDER}
    check(len(rows)==2 and sum(x["case"] in ORDER for x in entries)==2,
          "Pinned bed case IDs missing/duplicated")
    for cid in ORDER:
        row=rows[cid];block,props,elements,faces=EXPECTED[cid]
        check((row["cohort"],row["minecraft"],row["category"],
               row["block"],row["state"],row["model_hash_kind"],
               row["geometry_status"],int(row["elements"]),int(row["faces"]))==
              ("HC",VERSION,"BED",block,props,"GIT_BLOB_SHA1",
               "STATIC_SOURCE",elements,faces),
              "Original bed source application changed: "+cid)
    return rows,sha(raw)

@dataclass(frozen=True)
class BedCase:
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
        return self.block_id+"["+self.properties.replace(";",",")+"]"
    def camera(self):
        return f"{self.x+0.5:g} {self.y+2.3:g} {self.z+5.5:g} 180 20"

def cases(version=VERSION):
    check(version==VERSION,"Pinned Handcrafted bed experiment requires Minecraft 1.21.1")
    rows,_=source_rows()
    return tuple(BedCase(cid,VERSION,"HC_BED_"+cid,rows[cid]["block"],
                         rows[cid]["state"],x,Y,40)
                 for cid,x in zip(ORDER,(-16,16)))

def preflight(mod_dir,source_zip):
    rows,ledger=source_rows()
    jars=[]
    for file in sorted(Path(mod_dir).glob("*.jar")):
        with ZipFile(file) as z:
            if "assets/handcrafted/blockstates/oak_fancy_bed.json" in z.namelist():
                jars.append(file)
    check(len(jars)==1,"Exactly one pinned Handcrafted 4.0.3 JAR required")
    jar=jars[0]
    check(hashlib.sha1(jar.read_bytes()).hexdigest()==HC_RELEASE_SHA1,
          "Original Handcrafted 4.0.3 release binary SHA-1 changed")
    check(source_zip and Path(source_zip).is_file(),"Pinned original Handcrafted source ZIP required")
    found={}
    with ZipFile(source_zip) as origin,ZipFile(jar) as release:
        for cid in ORDER:
            row=rows[cid]
            originals={}
            execution={}
            comparisons={}
            for key in ("state","model","provider"):
                path=row[key+"_path"];expected=row[key+"_sha"]
                blob=source_zip_file(origin,path)
                check(git_sha(blob)==expected,
                      "Original Handcrafted pinned Git blob SHA mismatch: "+path)
                runtime=release.read(ref(path))
                originals[key]=json.loads(blob.decode("utf-8-sig"))
                execution[key]=json.loads(runtime.decode("utf-8-sig"))
                comparisons[key]={
                    "git_blob_sha1":expected,
                    "runtime_sha256":sha(runtime),
                    "byte_equal":blob==runtime,
                    "json_equal":originals[key]==execution[key]}
            selected={}
            for context,state in (("original",originals["state"]),
                                  ("release",execution["state"])):
                index,selector,option=selected_options(state,row["state"])
                if context=="original":
                    check(index==int(row["rule_index"]),"Historical source rule index changed")
                if isinstance(option,list):
                    option=option[int(row["option_index"])]
                else:check(int(row["option_index"])==0,"Unexpected model option index")
                optmodel=option.get("model")
                check(isinstance(optmodel,str) and ":" in optmodel,
                      "Selected bed model resource has no full namespace")
                model_resource="assets/"+optmodel.replace(":","/models/",1)+".json"
                check(model_resource==ref(row["model_path"]) and
                      int(option.get("y",0))==int(row["y"]) and
                      int(option.get("x",0))==int(row["x"]) and
                      bool(option.get("uvlock",False))==bool(int(row["uvlock"])) and
                      int(option.get("weight",1))==int(row["weight"]),
                      "Different source vs actual Handcrafted bed selected model: "+cid)
                selected[context]={"rule_index":index,"selected_model":model_resource}
            check(originals["model"]==execution["model"] and
                  originals["provider"]==execution["provider"],
                  "Bed selected leaf/provider changed structurally in published JAR: "+cid)
            parent=execution["model"].get("parent","")
            check(isinstance(parent,str) and ":" in parent and
                  "assets/"+parent.replace(":","/models/",1)+".json"==ref(row["provider_path"]),
                  "Bed model parent link not pinned source")
            parts=execution["provider"].get("elements",[])
            check(len(parts)==int(row["elements"]) and
                  sum(len(part.get("faces",{})) for part in parts)==int(row["faces"]),
                  "Bed original provider element or face counts differ in real JAR")
            found[cid]={
                "state":rows[cid]["state"],"model_path":row["model_path"],
                "model_git_blob_sha1":row["model_sha"],
                "provider_git_blob_sha1":row["provider_sha"],
                "state_git_blob_sha1":row["state_sha"],
                "model_rotation_y":int(row["y"]),
                "elements":int(row["elements"]),"faces":int(row["faces"]),
                "selection":selected,"source_vs_release":comparisons}
    check(found["S37"]["faces"]==72 and found["S38"]["faces"]==6,
          "Original 1-5 bed foot/head face count mismatch")
    return {"HC_release_SHA1":HC_RELEASE_SHA1,"source_git_commit":HC_COMMIT,
            "original_1_5_application_csv_sha256":ledger,"cases":found}

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"Wrong Minecraft client version")
    scenarios=cases()
    provenance=preflight(game/"mods",os.environ.get("MCFR_HC_SOURCE_ZIP"))
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    log=output/"client.log";screens=game/"screenshots";captured=[]
    with log.open("wb") as stream,subprocess.Popen(
        command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],
                                           env=env,timeout=15,text=True).strip()
        def command_text(value):
            xdo("key","--clearmodifiers","t");sleep(.35)
            xdo("type","--clearmodifiers","--delay","14",value)
            xdo("key","--clearmodifiers","Return")
        def camera(pose):
            # Client GUI sometimes joins before its command widget receives focus.
            # Retry the *same* requested pose without ever treating missing
            # server confirmation as a valid visual capture.
            for attempt in range(3):
                offset=len(read())
                xdo("windowfocus","--sync",windows[0])
                sleep(1.0)
                command_text("/tp @s "+pose)
                try:
                    wait_for(proc,lambda:"[RenderAudit: Teleported RenderAudit to" in read()[offset:],
                             "Handcrafted bed F2 camera teleport",32)
                except ValueError as failure:
                    if "Timed out waiting" not in str(failure) or attempt==2:
                        raise
                    sleep(3)
                    continue
                sleep(8)
                return
            raise ValueError("No server-confirmed bed camera pose")
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "Handcrafted 1.21.1 actual Fabric client",150)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),"--name","^Minecraft").split()
            check(len(windows)==1,"Exactly one Minecraft GUI required")
            xdo("windowfocus","--sync",windows[0]);sleep(1.5)
            command_text("/gamemode spectator");sleep(1)
            camera("0.5 124 42.5 180 20")
            command_text("/function mcfr_chair:place")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_PLACED" in read(),
                     "bed two source blocks placed",100)
            command_text("/function mcfr_chair:verify")
            wait_for(proc,lambda:"[RenderAudit] MCFR_CHAIR_STATES_READ" in read(),
                     "bed server source-state verification",100)
            passed=set();failed=set()
            for line in read().splitlines():
                tag="[RenderAudit] MCFR_CHAIR_STATE_"
                if "[Server thread/" in line and tag in line:
                    value=line.split(tag,1)[1].strip()
                    if value.endswith("=PASS"):passed.add(value[:-5])
                    if value.endswith("=FAIL"):failed.add(value[:-5])
            check(passed==set(ORDER) and not failed,
                  "Real bed foot/head source blockstate rejected/updated: "+
                  str({"pass":sorted(passed),"fail":sorted(failed)}))
            screens.mkdir(exist_ok=True)
            for case in scenarios:
                camera(case.camera())
                for attempt in range(3):
                    before=set(screens.glob("*.png"))
                    xdo("key","--clearmodifiers","F1");sleep(.8)
                    xdo("key","--clearmodifiers","F2")
                    photos=wait_for(proc,lambda:[
                        p for p in screens.glob("*.png") if p not in before and
                        p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
                    ],"actual F2 bed "+case.case_id,75)
                    xdo("key","--clearmodifiers","F1")
                    check(len(photos)==1,"Native Minecraft F2 file count not one")
                    with Image.open(photos[0]) as im:
                        im.load();dims=list(im.size)
                        colors=bed_visible_proxy(im)
                    check(dims==[1024,684],"Real F2 bed PNG dimensions changed")
                    if colors>=120:break
                    # Keep the actual invalid F2 attempt as diagnostic evidence;
                    # never silently discard or mark sky/grass-only as furniture.
                    shutil.copyfile(photos[0],output/(case.case_id+
                                     "_invalid_F2_attempt_"+str(attempt+1)+".png"))
                    if attempt==2:
                        raise ValueError("Bed original model not detectable (sky/grass-only F2): "+case.case_id)
                    sleep(5)
                dest=output/(case.case_id+".png")
                shutil.copyfile(photos[0],dest)
                source=provenance["cases"][case.case_id]
                captured.append({
                    "case_id":case.case_id,"original_state":case.state(),
                    "source_model_path":source["model_path"],
                    "source_model_git_blob_sha1":source["model_git_blob_sha1"],
                    "source_provider_git_blob_sha1":source["provider_git_blob_sha1"],
                    "source_faces":source["faces"],"server_source_state_verified":True,
                    "native_F2_verified":True,"foreground_chroma_pixels":colors,
                    "screenshot_file":dest.name,"screenshot_dimensions":dims,
                    "screenshot_sha256":sha(dest.read_bytes()),
                    "natural_bed_pair_placement_tested":False,
                    "semantic_or_ai_rights_approved":False})
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=20)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    check(len(captured)==2,"F2 evidence incomplete for bed original cases")
    doc={
      "schema":"MCFR_INT4_HC_BED_FOOT_HEAD_ACTUAL_F2/v1",
      "status":"CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED",
      "minecraft_version":VERSION,
      "actual_Fabric_client":True,
      "server_state_confirmed":2,"native_F2_count":2,
      "original_source_registry":provenance,
      "states":captured,
      "client_log_sha256":sha(log.read_bytes()),
      "semantic_part_roles_approved":0,"material_style_approved":0,
      "ai_training_and_redistribution_rights_approved":0,
      "limitations":[
        "Bed parts are staged separately with /setblock rather than placed through natural double-bed interaction",
        "Source foot mesh may extend across two blocks; separately captured F2 is not a joined bed screenshot",
        "No bed sleeping/gameplay, UV pixel-level agreement, material/part semantics or training rights approved"]
    }
    (output/MANIFEST).write_text(json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    return doc

def audit(directory):
    from PIL import Image,ImageDraw
    root=Path(directory)
    manifest=root/MANIFEST
    doc=json.loads(manifest.read_text(encoding="utf-8"))
    check(doc.get("schema")=="MCFR_INT4_HC_BED_FOOT_HEAD_ACTUAL_F2/v1" and
          doc.get("status")=="CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED" and
          doc.get("actual_Fabric_client") is True and
          doc.get("server_state_confirmed")==doc.get("native_F2_count")==2 and
          doc.get("semantic_part_roles_approved")==
          doc.get("material_style_approved")==
          doc.get("ai_training_and_redistribution_rights_approved")==0,
          "Bed F2 source/approval proof incomplete")
    rows={row["case_id"]:row for row in doc["states"]}
    check(len(rows)==len(doc["states"])==2 and set(rows)==set(ORDER),
          "Missing or duplicate native bed F2 case")
    provenance=doc["original_source_registry"]
    check(provenance["HC_release_SHA1"]==HC_RELEASE_SHA1 and
          provenance["original_1_5_application_csv_sha256"]==source_rows()[1],
          "Bed original source/JAR SHA not pinned")
    photos=[]
    for c in cases():
        row=rows[c.case_id];origin=provenance["cases"][c.case_id]
        check(row["original_state"]==c.state() and
              row["source_model_path"]==origin["model_path"] and
              row["source_model_git_blob_sha1"]==origin["model_git_blob_sha1"] and
              row["source_provider_git_blob_sha1"]==origin["provider_git_blob_sha1"] and
              row["source_faces"]==origin["faces"] and
              row["server_source_state_verified"] and row["native_F2_verified"] and
              row["natural_bed_pair_placement_tested"] is False and
              row["semantic_or_ai_rights_approved"] is False and
              row["foreground_chroma_pixels"]>=120 and
              row["screenshot_file"]==c.case_id+".png" and
              row["screenshot_dimensions"]==[1024,684],
              "Bed F2 case provenance mismatch")
        p=root/row["screenshot_file"]
        check(sha(p.read_bytes())==row["screenshot_sha256"],
              "Actual Handcrafted F2 image SHA mismatch: "+c.case_id)
        with Image.open(p) as im:im.verify()
        with Image.open(p) as im:photos.append(im.convert("RGB"))
    panel=Image.new("RGB",(1024,378),(239,239,239));draw=ImageDraw.Draw(panel)
    for i,(im,label) in enumerate(zip(photos,("S37 foot source alone","S38 head source alone"))):
        panel.paste(im.resize((512,342),resample=Image.Resampling.BILINEAR),(512*i,0))
        draw.text((512*i+8,350),label,fill=(10,10,10))
    panel.save(root/CONTACT)
    result={
      "schema":"MCFR_INT4_HC_BED_TWO_REAL_F2_AUDIT/v1",
      "status":"PASS_TWO_REAL_FABRIC_F2_PINNED_BED_SOURCE_STATES_NOT_NATURAL_ASSEMBLY",
      "source_cases":list(ORDER),
      "original_face_counts":{"S37":72,"S38":6},
      "actual_F2_count":2,"server_verified":2,
      "native_f2_sha256":{c:rows[c]["screenshot_sha256"] for c in ORDER},
      "original_JAR_sha1":HC_RELEASE_SHA1,
      "original_git_commit":HC_COMMIT,
      "manifest_sha256":sha(manifest.read_bytes()),
      "contact_sha256":sha((root/CONTACT).read_bytes()),
      "limitations":{
        "natural_bed_two_part_behavior_tested":False,
        "client_F2_pinned_and_server_confirmed":True,
        "texture_pixelwise_uv_color_approved":False,
        "int4_entire_scope_complete":False,
        "int5_part_roles_approved":0,
        "int6_rights_approved":0}}
    (root/AUDIT).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--directory",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":main()
