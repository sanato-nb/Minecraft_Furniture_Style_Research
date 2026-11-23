"""INT-4-H12 actual Fabric 1.21.1 Another Furniture model/texture A/B/A/air F2.

Same original block, coordinate, facing, camera, lighting and game session:
tucked=false variant=1 -> acacia_1, variant=3 -> acacia_3,
variant=1 again as temporal drift control, and air as a foreground mask.

Source model/parent/PNG identity is independently pinned to actual AF 4.0.2
JAR and the immutable H11 upstream Git source audit. No gameplay tests,
no mod asset bytes committed, no pixel-to-face UV causality approval.
"""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile
from time import sleep
import argparse,hashlib,json,os,shutil,subprocess

from .chair_runtime_fixture import cases,digest_bytes
from .runtime_capture import wait_for
from . import int4_af_variant3_texture_audit as source
from . import af_release_version_audit as af

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.1"
BLOCK="another_furniture:acacia_chair"
SELECTIONS={"model1":"facing=north,tucked=false,variant=1",
            "model3":"facing=north,tucked=false,variant=3"}
MODELS={"model1":"another_furniture:block/chair/acacia_1",
        "model3":"another_furniture:block/chair/acacia_3"}
STAGES=("model1_before","model3","model1_after","air")
SOURCE_AUDIT=ROOT/"project/integration/INT4_AF_VARIANT3_PIXEL_AUDIT_RESULT.json"
H11=ROOT/"project/integration/INT4_H11_AF_VARIANT3_SOURCE_UV_TEXEL_AUDIT_V1.json"
OLD_SHA1="7530144389e1589af4c1c891ded3e9531886519d"
H11_SHA1="1869ee05afce779bd37233ba1cc74850d736160f"
JAR_SHA1="c2f992081bdc4795ed6d87771a3b5f7c71103785"
ORIGINAL="INT4_H12_AF_SAME_CAMERA_REAL_NATIVE_F2_SOURCE_MANIFEST_V1.json"
AUDIT="INT4_H12_AF_MODEL1_MODEL3_REAL_GAME_INDEPENDENT_AUDIT_V1.json"
CONTACT="INT4_H12_AF_MODEL1_MODEL3_MODEL1_AIR_NATIVE_F2_CONTACT.png"
ROI=(350,275,675,620)
PIXEL_THRESHOLD=24

def check(predicate,message):
    if not predicate:raise ValueError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return digest_bytes(b,"GIT_BLOB_SHA1")

def original_case():
    selected=tuple(x for x in cases(VERSION) if x.case_id=="AF121_north")
    check(len(selected)==1 and selected[0].block_id==BLOCK and
          selected[0].state()==state("model1"),
          "Original AF 4.0.2 north variant1 source fixture changed")
    return selected

def state(key):
    check(key in SELECTIONS,"Unknown original north chair model selector")
    return BLOCK+"["+SELECTIONS[key]+"]"

def static_preflight(game):
    check(blob(SOURCE_AUDIT.read_bytes())==OLD_SHA1,
          "Prior AF original source PNG/face audit changed")
    check(blob(H11.read_bytes())==H11_SHA1,
          "Prior H11 original face UV/texel audit changed")
    old=json.loads(SOURCE_AUDIT.read_text(encoding="utf-8"))["evidence"]
    h11=json.loads(H11.read_text(encoding="utf-8"))
    check(old["study_runtime_models_json_semantically_equal"] and
          old["study_runtime_blockstate_json_semantically_equal"] and
          old["texture_png_study"]["rgba_different_pixel_count"]==54 and
          old["texture_png_runtime"]["rgba_different_pixel_count"]==54 and
          h11["counts"]["changed_binding_faces_with_any_different_texel"]==2 and
          h11["counts"]["changed_texels_in_union_of_12_face_UV_footprints"]==54,
          "Original fixed research source coverage changed")
    jar=game/"mods"/"another_furniture-fabric-4.0.2.jar"
    check(jar.is_file() and hashlib.sha1(jar.read_bytes()).hexdigest()==JAR_SHA1,
          "Unpinned actual AF 4.0.2 runtime JAR")
    checked={}
    with ZipFile(jar) as archive:
        for rel,expected in old["runtime_git_blob_sha1"].items():
            check(rel in source.EXPECTED_SHA,"Unknown original runtime provenance resource")
            b=archive.read(source.af.PREFIX+rel)
            check(blob(b)==expected,"Actual runtime original file Git blob changed "+rel)
            checked[rel]={"git_blob_sha1":expected,"sha256":sha(b)}
        blockstate=json.loads(archive.read(source.af.PREFIX+"blockstates/acacia_chair.json"))
        check(len(blockstate["variants"])==88,"Runtime original AF acacia blockstates not 88")
        expected_models={"model1":MODELS["model1"],"model3":MODELS["model3"]}
        chosen={}
        for name,resource in expected_models.items():
            actual=blockstate["variants"].get(SELECTIONS[name])
            check(actual=={"model":resource},
                  "Original north AF source does not select expected paired model "+name)
            chosen[name]=actual
        docs={p:json.loads(archive.read(source.af.PREFIX+p))
              for p in (*source.CHILDREN,source.PARENT)}
        changed,summary=source.compare_inherited_models(docs)
        check(len(changed)==12 and summary["element_count_each"]==10 and
              summary["face_count_each"]==46 and
              summary["geometry_equal"] and summary["uv_equal"],
              "Original runtime source model geometry, UV or 12 face texture slots changed")
        back1=archive.read(source.af.PREFIX+source.TEXTURES[0])
        back3=archive.read(source.af.PREFIX+source.TEXTURES[1])
        check(source.image_difference(back1,back3)["rgba_different_pixel_count"]==54,
              "Original actual runtime back textures do not have 54 RGBA differences")
    return {"h11_git_blob_sha1":H11_SHA1,"older_source_git_blob_sha1":OLD_SHA1,
            "actual_af_jar_sha1":JAR_SHA1,
            "actual_runtime_provenance":checked,
            "pinned_source_upstream_git_commit":af.UPSTREAM,
            "fixed_variant1_variant3_north":chosen,
            "same_10_elements_46_faces_and_UV":True,
            "changed_texture_binding_face_count":12,
            "changed_source_back_texels":54,
            "visible_source_texel_overlap_faces_from_H11":2}

def changes(a,b):
    pa=a.convert("RGB").crop(ROI)
    pb=b.convert("RGB").crop(ROI)
    if pa.size!=pb.size:raise ValueError("Screenshots are not same ROI size")
    changed=set()
    for pos,(x,y) in enumerate(zip(pa.getdata(),pb.getdata())):
        if max(abs(x[i]-y[i]) for i in range(3))>=PIXEL_THRESHOLD:
            changed.add((ROI[0]+pos%pa.width,ROI[1]+pos//pa.width))
    return changed

def metrics(images):
    b=images["model1_before"];n=images["model3"]
    a=images["model1_after"];air=images["air"]
    changed=changes(b,n)
    temporal=changes(b,a)
    foreground=changes(b,air)|changes(n,air)
    return {
      "model1_to_model3":len(changed),
      "model1_before_to_model1_after_temporal_control":len(temporal),
      "model1_to_air":len(changes(b,air)),
      "model3_to_air":len(changes(n,air)),
      "model_difference_overlapping_foreground":len(changed&foreground),
      "model_difference_outside_foreground":len(changed-foreground),
      "model_difference_not_explained_by_temporal_control":len(changed-temporal),
      "changed_pixel_bounds":[min(x for x,y in changed),min(y for x,y in changed),
                              max(x for x,y in changed),max(y for x,y in changed)]
                             if changed else None,
      "ROI":list(ROI),"channel_threshold":PIXEL_THRESHOLD,
    }

def screenshot(session,window,shots,dest,label,record):
    from PIL import Image
    xdo=session
    before=set(shots.glob("*.png"))
    xdo("key","--clearmodifiers","F1");sleep(.8)
    xdo("key","--clearmodifiers","F2")
    proc=record["proc"]
    found=wait_for(proc,lambda:[
       p for p in shots.glob("*.png")
       if p not in before and p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
    ],"original Fabric native Minecraft F2 "+label,85)
    xdo("key","--clearmodifiers","F1")
    check(len(found)==1,"Not exactly one original Minecraft native F2 "+label)
    output=dest/(label+".png")
    shutil.copyfile(found[0],output)
    with Image.open(output) as im:
        im.load()
        check(im.format=="PNG" and im.size==(1024,684),
              "Original F2 image not exactly PNG 1024x684")
    return {"image":output.name,"sha256":sha(output.read_bytes()),"dimensions":[1024,684]}

def capture(command,env,game,output,version):
    from PIL import Image
    check(version==VERSION,"AF source study pinned to Minecraft Fabric 1.21.1")
    src=static_preflight(game)
    dest=Path(output)
    dest.mkdir(parents=True,exist_ok=False)
    log=dest/"client.log"
    shots=game/"screenshots"
    case=original_case()[0]
    pose=case.camera()
    xyz=(case.x,case.y,case.z)
    states={}
    with log.open("wb") as sink,subprocess.Popen(
            command,cwd=game,env=env,stdout=sink,stderr=subprocess.STDOUT) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,timeout=18,text=True).strip()
        def cmd(text):
            xdo("windowfocus","--sync",window)
            xdo("key","--clearmodifiers","t");sleep(.35)
            xdo("type","--clearmodifiers","--delay","14",text)
            xdo("key","--clearmodifiers","Return")
        def server_cmd(text,marker,description,timeout=75):
            previous=len(read())
            cmd(text)
            wait_for(proc,lambda:marker in read()[previous:],description,timeout)
            sleep(1.4)
        def check_state(label,block):
            x,y,z=xyz
            marker="MCFR_H12_"+label.upper()+"_EXACT_SERVER=PASS"
            server_cmd(f"/execute if block {x} {y} {z} {block} run say {marker}",
                       "[RenderAudit] "+marker,"original server exact "+label)
            states[label]={"blockstate":block,"exact_server_verified":True,
                           "server_marker":marker}
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "actual Fabric AF original client world join",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in read(),
                     "actual Fabric client ready",70)
            sleep(7)
            ids=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                    "--name","^Minecraft").split()
            check(len(ids)==1,"Expected one real Minecraft client window")
            window=ids[0]
            xdo("windowfocus","--sync",window);sleep(2)
            server_cmd("/gamemode spectator",
                       "[RenderAudit: Set own game mode to Spectator Mode]",
                       "same camera spectator")
            server_cmd("/tp @s "+pose,"[RenderAudit: Teleported RenderAudit to",
                       "one fixed chair model comparison camera")
            server_cmd("/function mcfr_chair:place",
                       "[RenderAudit] MCFR_CHAIR_PLACED",
                       "pinned original variant1 single chair staging")
            server_cmd("/function mcfr_chair:verify",
                       "[RenderAudit] MCFR_CHAIR_STATES_READ",
                       "baseline original model1 server proof")
            shots.mkdir(exist_ok=True)
            check_state("model1_before",state("model1"))
            sleep(6)
            states["model1_before"].update(screenshot(xdo,window,shots,dest,"model1_before",{"proc":proc}))
            x,y,z=xyz
            server_cmd(f"/setblock {x} {y} {z} {state('model3')}",
                       "[RenderAudit: Changed the block at",
                       "north variant3 model staging")
            check_state("model3",state("model3"))
            sleep(6)
            states["model3"].update(screenshot(xdo,window,shots,dest,"model3",{"proc":proc}))
            server_cmd(f"/setblock {x} {y} {z} {state('model1')}",
                       "[RenderAudit: Changed the block at",
                       "same model1 temporal return control")
            check_state("model1_after",state("model1"))
            sleep(6)
            states["model1_after"].update(screenshot(xdo,window,shots,dest,"model1_after",{"proc":proc}))
            server_cmd(f"/setblock {x} {y} {z} minecraft:air",
                       "[RenderAudit: Changed the block at",
                       "same position air control")
            check_state("air","minecraft:air")
            sleep(6)
            states["air"].update(screenshot(xdo,window,shots,dest,"air",{"proc":proc}))
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    check(set(states)==set(STAGES),"Missing actual F2 or exact server stage")
    frames={}
    for k in STAGES:
        with Image.open(dest/(k+".png")) as im:
            im.load()
            frames[k]=im.convert("RGB")
    measurement=metrics(frames)
    visible=(measurement["model1_to_model3"]>=25 and
             measurement["model_difference_overlapping_foreground"]>=20 and
             measurement["model_difference_not_explained_by_temporal_control"]>=15)
    data={
       "schema":"MCFR_INT4_H12_AF_VARIANT1_VARIANT3_SAME_POSE_REAL_GAME_CAPTURE/v1",
       "status":("ACTUAL_NATIVE_F2_MODEL_TEXTURE_CONTRAST_CANDIDATE" if visible
                 else "REAL_GAME_F2_BUT_VISUAL_DIFFERENCE_NOT_YET_PROVEN"),
       "runtime_minecraft_version":version,
       "real_game_single_session":True,
       "same_position_facing_camera_all_four":True,
       "source_model_coordinates":list(xyz),"fixed_camera":pose,
       "states":states,"runtime_source":src,"ROI_differences":measurement,
       "original_client_log_sha256":sha(log.read_bytes()),
       "new_actual_game_runs":1,"original_F2_count":4,
       "no_gameplay_interactions_tested":True,
       "face_pixel_UV_causality_approved":False,
       "F70_unconditional_approvals":0,
       "H03_H05_full_exit":False,
       "INT5_semantics_approved":0,
       "INT6_training_redistribution_approved":0,
       "limits":[
         "North-facing variant1/variant3 differ by source back texture, but the screenshot is not a per-face rasterizer attribution.",
         "Time-separated screenshots have unavoidable possible temporal lighting or software raster changes; A-B-A controls are diagnostic.",
         "The source 54 texels and two UV overlap faces do not guarantee those specific 54 texels were rendered or sampled.",
         "Game input is /setblock plus native F2: no player sleep/wake/destroy or functional object testing.",
         "Original runtime PNG, JAR, client log bytes and F2 must remain expiring Actions artifact, not source repository."
       ],
    }
    (dest/ORIGINAL).write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return data

def audit(directory):
    from PIL import Image,ImageDraw
    root=Path(directory)
    raw=(root/ORIGINAL).read_bytes()
    doc=json.loads(raw)
    check(doc["schema"]=="MCFR_INT4_H12_AF_VARIANT1_VARIANT3_SAME_POSE_REAL_GAME_CAPTURE/v1" and
          doc["runtime_minecraft_version"]==VERSION and
          doc["real_game_single_session"] is True and
          doc["same_position_facing_camera_all_four"] is True,
          "Actual H12 single-game fixed-camera identity missing")
    case=original_case()[0]
    check(doc["source_model_coordinates"]==[case.x,case.y,case.z] and
          doc["fixed_camera"]==case.camera(),"Same camera/state not pinned to original case")
    src=doc["runtime_source"]
    check(src["h11_git_blob_sha1"]==H11_SHA1 and
          src["actual_af_jar_sha1"]==JAR_SHA1 and
          src["same_10_elements_46_faces_and_UV"] is True and
          src["changed_texture_binding_face_count"]==12 and
          src["changed_source_back_texels"]==54 and
          src["visible_source_texel_overlap_faces_from_H11"]==2,
          "Original runtime model/JAR/H11 source pins changed")
    log=(root/"client.log").read_bytes()
    check(sha(log)==doc["original_client_log_sha256"],"Actual game client log SHA mismatch")
    text=log.decode("utf-8",errors="replace")
    check(set(doc["states"])==set(STAGES),"Not exactly four original F2 state records")
    imgs={}
    for label in STAGES:
        item=doc["states"][label]
        expected=("minecraft:air" if label=="air" else state("model3" if label=="model3" else "model1"))
        check(item["blockstate"]==expected and item["exact_server_verified"] is True and
              "[RenderAudit] "+item["server_marker"] in text,
              "Integrated game server original exact source state missing "+label)
        check(item["image"]==label+".png" and item["dimensions"]==[1024,684],
              "Native screenshot file identity/resolution wrong")
        img_path=root/item["image"]
        check(sha(img_path.read_bytes())==item["sha256"],"Original game screenshot SHA mismatch "+label)
        with Image.open(img_path) as im:
            im.load()
            check(im.format=="PNG" and im.size==(1024,684),"Not 1024x684 native PNG")
            imgs[label]=im.convert("RGB")
    recalc=metrics(imgs)
    check(recalc==doc["ROI_differences"],"Independent screenshot ROI metrics drift")
    check(recalc["model1_to_air"]>=250 and recalc["model3_to_air"]>=250,
          "Actual source chair not detected against AIR baseline")
    visible=(recalc["model1_to_model3"]>=25 and
             recalc["model_difference_overlapping_foreground"]>=20 and
             recalc["model_difference_not_explained_by_temporal_control"]>=15)
    check(doc["status"]==("ACTUAL_NATIVE_F2_MODEL_TEXTURE_CONTRAST_CANDIDATE"
          if visible else "REAL_GAME_F2_BUT_VISUAL_DIFFERENCE_NOT_YET_PROVEN"),
          "Model visibility status incorrectly claimed")
    picture=Image.new("RGB",(4*320,280),(238,239,241))
    pen=ImageDraw.Draw(picture)
    for i,name in enumerate(STAGES):
        picture.paste(imgs[name].resize((320,248),Image.Resampling.BILINEAR),(320*i,0))
        pen.text((320*i+8,254),name+" original F2",fill=(30,30,30))
    picture.save(root/CONTACT)
    result={
      "schema":"MCFR_INT4_H12_AF_SAME_POSE_F2_INDEPENDENT_SOURCE_AUDIT/v1",
      "status":("PASS_REAL_FABRIC_ABA_AIR_SOURCE_MODEL_VISUAL_CONTRAST"
                if visible else "CONDITIONAL_FABRIC_F2_NO_CLEAR_VARIANT_MODEL_CONTRAST"),
      "minecraft_version":VERSION,
      "actual_Fabric_original_game_runs":1,
      "native_original_F2_count":4,
      "same_source_coordinates":[case.x,case.y,case.z],
      "same_camera":case.camera(),
      "source_model1":MODELS["model1"],"source_model3":MODELS["model3"],
      "original_client_log_sha256":doc["original_client_log_sha256"],
      "original_manifest_sha256":sha(raw),
      "native_original_F2_sha256":{k:doc["states"][k]["sha256"] for k in STAGES},
      "pixel_measurement":recalc,
      "H11_previous_source_git_blob_sha1":H11_SHA1,
      "real_runtime_AF_JAR_sha1":JAR_SHA1,
      "contact_sha256":sha((root/CONTACT).read_bytes()),
      "source_12_different_texture_binding_faces":12,
      "source_2_UV_overlapping_changed_texel_faces":2,
      "source_54_RGBA_changed_texels":54,
      "UV_face_to_GPU_pixel_causal_proof":False,
      "F70_unconditional_approvals":0,"H03_H05_full_exit":False,
      "INT5_semantics_approved":0,"INT6_training_rights_approved":0,
      "scope":{
         "native_F2_rendered_variant1_and_variant3_same_position":True,
         "changed_texture_pixel_region_detected":visible,
         "specific_UV_face_pixel_attribution_proven":False,
         "existing_H11_research_data_unchanged":True,
         "mod_author_intent_approved":False,
         "player_sleep_wake_destroy_tests_run":False
      }
    }
    (root/AUDIT).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",required=True,type=Path)
    args=p.parse_args()
    print(json.dumps(audit(args.directory),ensure_ascii=False))
if __name__=="__main__":main()
