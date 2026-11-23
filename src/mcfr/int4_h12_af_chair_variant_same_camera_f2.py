"""INT-4-H12: same-camera real Minecraft AF chair back texture model A/B/A + air.

Models: acacia_1 (north variant=1) vs acacia_3 (north variant=3).
Only variant changes. Same position, same facing, same singleplayer Fabric
1.21.1 client, same original pinned AF 4.0.2 official distribution.
Four native F2 frames: A1, B3, A1 repeated control, AIR. Original Git study
4.0.3 source vs actual runtime 4.0.2 resource semantic parity is checked.

Evidence is source-to-visible-A/B texture contrast, never exact GPU
face-to-texel causation, material/part semantics, or redistribution rights.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from time import sleep
from zipfile import ZipFile

from . import af_release_version_audit as af
from . import int4_af_variant3_texture_audit as src
from .chair_runtime_fixture import ChairCase, digest_bytes
from .runtime_capture import wait_for

ROOT=Path(__file__).resolve().parents[2]
VERSION="1.21.1"
MODEL="another_furniture:acacia_chair"
OFFICIAL_JAR="another_furniture-fabric-4.0.2.jar"
RELEASE_SHA1="c2f992081bdc4795ed6d87771a3b5f7c71103785"
SOURCE_GIT="57eb624cbb7f408d43398c7434b0d38d312cb55d"
H11_REPORT=Path("project/integration/INT4_H11_AF_VARIANT3_SOURCE_UV_TEXEL_AUDIT_V1.json")
H11_GIT_SHA1="1869ee05afce779bd37233ba1cc74850d736160f"
X,Y,Z=0,120,40
POSE=f"{X+0.5:g} {Y+2.3:g} {Z+5.5:g} 180 20"
FRAMES=("v1","v3","v1_repeat","air")
STATES={
    "v1":"facing=north,tucked=false,variant=1",
    "v3":"facing=north,tucked=false,variant=3",
}
EXPECTED_MODELS={
    "v1":"another_furniture:block/chair/acacia_1",
    "v3":"another_furniture:block/chair/acacia_3",
}
MANIFEST="INT4_H12_AF_NORTH_VARIANT_F2_REAL_CAPTURE_V1.json"
AUDIT="INT4_H12_AF_NORTH_VARIANT_F2_INDEPENDENT_AUDIT_V1.json"
CONTACT="INT4_H12_AF_NORTH_A_B_A_AIR_CONTACT.png"

def require(cond,message):
    if not cond:raise ValueError(message)
def sha256(b):return hashlib.sha256(b).hexdigest()
def blob(b):return digest_bytes(b,"GIT_BLOB_SHA1")

def original_case():
    return (ChairCase("H12_AF_NORTH_V1",VERSION,"AF121",MODEL,
                      "tucked=false,variant=1","north",X,Y,Z),)

def state(which):
    require(which in STATES,"Unknown source-pinned chair variant")
    return MODEL+"["+STATES[which]+"]"

def study_and_runtime(game):
    """Reopen frozen Git source JSON and actual official runtime JAR contents."""
    p=ROOT/H11_REPORT
    original=p.read_bytes()
    require(blob(original)==H11_GIT_SHA1,"H11 study result SHA was replaced")
    h11=json.loads(original)
    counts=h11["counts"]
    require(h11["status"]=="PASS_12_CHANGED_SOURCE_FACES_UV_TEXEL_COVERAGE_WITHOUT_GPU_CAUSAL_APPROVAL"
            and counts["face_texture_bindings_changed"]==12
            and counts["changed_binding_faces_with_any_different_texel"]==2
            and counts["changed_texels_in_union_of_12_face_UV_footprints"]==54,
            "H11 12 source faces/2 UV-active faces/54 texels no longer pinned")
    jar=game/"mods"/OFFICIAL_JAR
    require(jar.is_file(),"Official AF mod version missing from original game")
    require(hashlib.sha1(jar.read_bytes()).hexdigest()==RELEASE_SHA1,
            "AF official 4.0.2 Modrinth release JAR SHA1 changed")
    require(len(list((game/"mods").glob("another_furniture*.jar")))==1,
            "Multiple AF runtime JAR versions are loaded together")
    original_paths=src.EXPECTED_SHA
    study={}
    with ZipFile(jar) as release:
        require(release.testzip() is None,"Original official runtime JAR CRC failed")
        runtime={}
        for rel,pin in original_paths.items():
            raw=(src.fetch_pinned_png(rel) if rel in src.TEXTURES
                 else af.fetch_research(rel))
            require(raw is not None and blob(raw)==pin,
                    "Pinned AF study Git source file changed: "+rel)
            name=af.PREFIX+rel
            require(name in release.namelist(),"Pinned AF runtime resource missing: "+rel)
            runtime[rel]=release.read(name)
            study[rel]=raw
    source_states=json.loads(study["blockstates/acacia_chair.json"])
    release_states=json.loads(runtime["blockstates/acacia_chair.json"])
    require(source_states==release_states and len(source_states["variants"])==88,
            "4.0.2 runtime selector semantics differ from 4.0.3 fixed study")
    docs0={k:json.loads(study[k]) for k in (*src.CHILDREN,src.PARENT)}
    docs1={k:json.loads(runtime[k]) for k in (*src.CHILDREN,src.PARENT)}
    require(docs0==docs1,"AF original/runtime selected child or parent JSON differ")
    changed,compare=src.compare_inherited_models(docs0)
    require(len(changed)==12 and compare["geometry_equal"] and
            compare["uv_equal"] and compare["face_count_each"]==46,
            "Original 12 changed face texture bindings no longer reproducible")
    rgba=src.image_difference(study[src.TEXTURES[0]],study[src.TEXTURES[1]])
    require(rgba["rgba_different_pixel_count"]==54,"AF original 54 changed RGBA texels failed")
    require(all(study[x]==runtime[x] for x in src.TEXTURES),
            "Runtime AF 4.0.2 source textures have different PNG bytes")
    choices={}
    for key,selector in STATES.items():
        source_choice=source_states["variants"].get(selector)
        runtime_choice=release_states["variants"].get(selector)
        require(source_choice==runtime_choice and
                source_choice.get("model")==EXPECTED_MODELS[key] and
                source_choice.get("y",0)==0,
                "Incorrect exact north model selection: "+key)
        model_name="models/block/chair/"+("acacia_1" if key=="v1" else "acacia_3")+".json"
        choices[key]={
            "original_blockstate":state(key),
            "original_model":source_choice["model"],
            "model_Y_rotation":source_choice.get("y",0),
            "study_git_blob_sha1":src.EXPECTED_SHA[model_name],
            "runtime_git_blob_sha1":blob(runtime[model_name]),
            "runtime_JSON_equals_pinned_study":True,
            "same_10_elements_46_faces_and_face_UV_as_other_choice":True,
        }
    return {
       "source_study_git_commit":SOURCE_GIT,
       "study_version":"4.0.3",
       "runtime_version":"4.0.2",
       "official_JAR_name":OFFICIAL_JAR,
       "official_JAR_sha1":RELEASE_SHA1,
       "H11_frozen_original_audit_git_sha1":H11_GIT_SHA1,
       "original_16x16_back_texture_differing_RGBA_texels":54,
       "source_faces_with_texture_binding_change":12,
       "source_faces_UV_overlapping_different_texels":2,
       "model_source_options":choices,
    }

def diff_mask(a,b,threshold=24):
    from PIL import ImageChops,Image
    require(a.size==b.size==(1024,684),"Original F2 image dimensions differ")
    a=a.convert("RGB");b=b.convert("RGB")
    # Raw RGB is verified; threshold on max channel difference
    va=a.getdata();vb=b.getdata()
    return [max(abs(p[0]-q[0]),abs(p[1]-q[1]),abs(p[2]-q[2]))>=threshold
            for p,q in zip(va,vb)]

def compare_frames(directory):
    from PIL import Image
    originals={}
    for name in FRAMES:
        with Image.open(directory/(name+".png")) as img:
            img.load()
            require(img.format=="PNG" and img.size==(1024,684),
                    "Damaged or wrong-sized genuine F2: "+name)
            originals[name]=img.convert("RGB")
    a=originals["v1"];b=originals["v3"]
    a2=originals["v1_repeat"];sky=originals["air"]
    ab=diff_mask(a,b)
    aa=diff_mask(a,a2)
    a_air=diff_mask(a,sky)
    b_air=diff_mask(b,sky)
    union=[x or y for x,y in zip(a_air,b_air)]
    # A visible control is independently measured; no fabricated static ROI.
    visible=sum(ab)
    in_foreground=sum(x and y for x,y in zip(ab,union))
    repeat_noise=sum(aa)
    same_background=max(0,visible-in_foreground)
    qualifying=(visible>=30 and visible>=3*repeat_noise+20 and
                in_foreground*100>=visible*85 and
                sum(a_air)>=100 and sum(b_air)>=100)
    return {
       "RGB_channel_difference_threshold":24,
       "variant1_vs_variant3_full_frame_pixels":visible,
       "variant1_vs_variant1_repeat_pixels":repeat_noise,
       "variant1_vs_air_pixels":sum(a_air),
       "variant3_vs_air_pixels":sum(b_air),
       "model_changed_pixels_in_F2_air_control_union":in_foreground,
       "model_changed_pixels_outside_air_control_union":same_background,
       "conservative_visible_model_difference":qualifying,
       "actual_face_to_exact_GPU_texel_match_approved":False,
    }

def capture(command,env,game,output,version):
    from PIL import Image
    require(version==VERSION,"H12 requires actual Minecraft 1.21.1")
    provenance=study_and_runtime(Path(game))
    out=Path(output)
    out.mkdir(parents=True,exist_ok=False)
    logfile=out/"client.log"
    shots=Path(game)/"screenshots"
    observed={}
    with logfile.open("wb") as stream,subprocess.Popen(
         command,cwd=game,env=env,stdout=stream,stderr=subprocess.STDOUT
    ) as proc:
        def log():return logfile.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,timeout=18,text=True).strip()
        def cmd(message):
            xdo("windowfocus","--sync",window)
            xdo("key","--clearmodifiers","t");sleep(.35)
            xdo("type","--clearmodifiers","--delay","14",message)
            xdo("key","--clearmodifiers","Return")
        def server(message,marker,label,timeout=65):
            previous=len(log())
            cmd(message)
            wait_for(proc,lambda:marker in log()[previous:],label,timeout)
            sleep(1.5)
        def verify(label,expected):
            tag="MCFR_H12_"+label.upper()+"_EXACT_SERVER"
            server(f"/execute if block {X} {Y} {Z} {expected} run say {tag}=PASS",
                   "[RenderAudit] "+tag+"=PASS",label+" pinned source selector")
            observed[label]={"exact_server_blockstate":expected,
                             "integrated_server_confirmed":True,
                             "server_log_marker":tag+"=PASS"}
        def snap(label):
            originals=set(shots.glob("*.png"))
            xdo("key","--clearmodifiers","F1");sleep(.8)
            xdo("key","--clearmodifiers","F2")
            generated=wait_for(proc,lambda:[
                 p for p in shots.glob("*.png")
                 if p not in originals and
                 p.read_bytes().endswith(b"IEND\xaeB\x60\x82")
            ],"original native Minecraft F2 "+label,85)
            xdo("key","--clearmodifiers","F1")
            require(len(generated)==1,"Native F2 count not exactly one")
            target=out/(label+".png")
            shutil.copyfile(generated[0],target)
            with Image.open(target) as original:
                original.load()
                require(original.format=="PNG" and original.size==(1024,684),
                        "Original game native F2 format incorrect")
            observed[label].update({"PNG_name":target.name,
                                    "PNG_sha256":sha256(target.read_bytes()),
                                    "PNG_dimensions":[1024,684]})
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in log(),
                     "actual Fabric AF original chair world join",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in log(),
                     "actual client ready",70)
            sleep(7)
            matches=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            require(len(matches)==1,"Exactly one Minecraft window required")
            window=matches[0]
            xdo("windowfocus","--sync",window);sleep(3)
            server("/gamemode spectator",
                   "[RenderAudit: Set own game mode to Spectator Mode]",
                   "same spectator mode")
            server("/tp @s "+POSE,
                   "[RenderAudit: Teleported RenderAudit to",
                   "single fixed camera pose")
            server("/function mcfr_chair:place",
                   "[RenderAudit] MCFR_CHAIR_PLACED","original north variant1 pack")
            server("/function mcfr_chair:verify",
                   "[RenderAudit] MCFR_CHAIR_STATES_READ","original pinned variant1 server")
            verify("v1",state("v1"))
            shots.mkdir(exist_ok=True)
            sleep(5);snap("v1")
            server(f"/setblock {X} {Y} {Z} {state('v3')}",
                   "[RenderAudit: Changed the block at","variant3 exact source model")
            verify("v3",state("v3"))
            sleep(5);snap("v3")
            server(f"/setblock {X} {Y} {Z} {state('v1')}",
                   "[RenderAudit: Changed the block at","repeat original model baseline")
            verify("v1_repeat",state("v1"))
            sleep(5);snap("v1_repeat")
            server(f"/setblock {X} {Y} {Z} minecraft:air",
                   "[RenderAudit: Changed the block at","air baseline")
            verify("air","minecraft:air")
            sleep(5);snap("air")
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    require(set(observed)==set(FRAMES),"Cannot claim game native F2 without four original cases")
    stats=compare_frames(out)
    state_status=("PASS_REAL_GAME_SOURCE_SELECTORS_AND_CONTRAST_SCREENED"
                  if stats["conservative_visible_model_difference"] else
                  "CONDITIONAL_REAL_GAME_F2_CAPTURED_BUT_VISIBLE_MODEL_DIFF_NOT_PROVEN")
    result={
       "schema":"MCFR_INT4_H12_AF_NORTH_VARIANT1_VARIANT3_SAME_CAMERA_F2_CAPTURE/v1",
       "status":state_status,
       "actual_Fabric_Minecraft_1_21_1":True,
       "fixed_camera_pose":POSE,
       "same_coordinates":[X,Y,Z],
       "same_facing":"north","same_tucked":False,
       "only_changed_blockstate_property":"variant",
       "runtime_and_study_sources":provenance,
       "client_log_sha256":sha256(logfile.read_bytes()),
       "actual_native_F2_files":observed,
       "native_F2_count":4,
       "new_game_sessions":1,
       "contrast":stats,
       "player_interaction_tests":0,
       "F70_unconditional_approvals":0,
       "H03_H05_full_exit":False,
       "INT5_part_semantics_approved":0,
       "INT6_training_and_asset_redistribution_approved":0,
       "limits":[
          "Only one fixed north-facing chair; does not establish visibility in every possible view.",
          "Native F2 RGB difference + identical source geometry/UV does not map exact screenshot pixels to exact model faces.",
          "The repeated A frame controls temporal background changes; small differences remain conditional.",
          "Actual runtime is official 4.0.2 Fabric, while pinned study reference is 4.0.3 Git resource data.",
          "Original game image and JAR bytes are preserved in temporary Actions artifact, not committed to Git.",
          "No mod author bug intention, part roles, F/H full exit or AI redistribution rights are approved.",
       ],
    }
    (out/MANIFEST).write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                               encoding="utf-8")
    return result

def audit(directory):
    from PIL import Image,ImageDraw
    directory=Path(directory)
    raw=(directory/MANIFEST).read_bytes()
    manifest=json.loads(raw)
    require(manifest["schema"]=="MCFR_INT4_H12_AF_NORTH_VARIANT1_VARIANT3_SAME_CAMERA_F2_CAPTURE/v1"
            and manifest["actual_Fabric_Minecraft_1_21_1"] is True
            and manifest["same_coordinates"]==[X,Y,Z]
            and manifest["same_facing"]=="north"
            and manifest["only_changed_blockstate_property"]=="variant"
            and manifest["fixed_camera_pose"]==POSE,
            "F2 audit source, camera or model scope drifted")
    require(set(manifest["actual_native_F2_files"])==set(FRAMES) and
            manifest["native_F2_count"]==4,
            "Four original AF F2 files required")
    provenance=manifest["runtime_and_study_sources"]
    require(provenance["official_JAR_sha1"]==RELEASE_SHA1 and
            provenance["H11_frozen_original_audit_git_sha1"]==H11_GIT_SHA1 and
            provenance["source_faces_UV_overlapping_different_texels"]==2 and
            provenance["original_16x16_back_texture_differing_RGBA_texels"]==54 and
            provenance["model_source_options"]["v1"]["original_model"]==EXPECTED_MODELS["v1"] and
            provenance["model_source_options"]["v3"]["original_model"]==EXPECTED_MODELS["v3"],
            "Original two selected models not source-pinned")
    log= (directory/"client.log").read_bytes()
    require(sha256(log)==manifest["client_log_sha256"],
            "Runtime integrated game client log SHA mismatch")
    text=log.decode("utf-8",errors="replace")
    for key in FRAMES:
        record=manifest["actual_native_F2_files"][key]
        expected=("minecraft:air" if key=="air" else
                  state("v1") if key in ("v1","v1_repeat") else state("v3"))
        require(record["exact_server_blockstate"]==expected and
                record["integrated_server_confirmed"] is True and
                "[RenderAudit] "+record["server_log_marker"] in text,
                "Exact source state was not proven by actual server: "+key)
        img=directory/(key+".png")
        require(record["PNG_name"]==img.name and
                sha256(img.read_bytes())==record["PNG_sha256"] and
                record["PNG_dimensions"]==[1024,684],
                "Original native F2 PNG corrupt or substituted: "+key)
        with Image.open(img) as im:
            im.load()
            require(im.format=="PNG" and im.size==(1024,684),
                    "Original game F2 dimensions or format incorrect")
    actual=compare_frames(directory)
    require(actual==manifest["contrast"],"Independent AF screenshot RGB/ROI mismatch")
    require(actual["variant1_vs_air_pixels"]>=100 and
            actual["variant3_vs_air_pixels"]>=100,
            "Actual chair foreground could not be distinguished from AIR")
    expected_status=("PASS_REAL_GAME_SOURCE_SELECTORS_AND_CONTRAST_SCREENED"
                     if actual["conservative_visible_model_difference"] else
                     "CONDITIONAL_REAL_GAME_F2_CAPTURED_BUT_VISIBLE_MODEL_DIFF_NOT_PROVEN")
    require(manifest["status"]==expected_status,
            "Captured state status was incorrectly promoted")
    canvas=Image.new("RGB",(1024,720),(242,242,242))
    draw=ImageDraw.Draw(canvas)
    for i,key in enumerate(FRAMES):
        with Image.open(directory/(key+".png")) as image:
            canvas.paste(image.convert("RGB").resize((512,342),Image.Resampling.BILINEAR),
                         ((i%2)*512,(i//2)*360))
        draw.text(((i%2)*512+10,(i//2)*360+344),key+" (real F2)",fill=(20,20,20))
    canvas.save(directory/CONTACT)
    final={
       "schema":"MCFR_INT4_H12_AF_NORTH_VARIANT1_V3_REAL_GAME_INDEPENDENT_AUDIT/v1",
       "status":expected_status,
       "original_capture_manifest_sha256":sha256(raw),
       "original_client_log_sha256":sha256(log),
       "original_F2_sha256":{key:manifest["actual_native_F2_files"][key]["PNG_sha256"]
                             for key in FRAMES},
       "original_contact_sheet_sha256":sha256((directory/CONTACT).read_bytes()),
       "source_models":provenance["model_source_options"],
       "official_runtime_jar_sha1":RELEASE_SHA1,
       "H11_source_gitblob_sha1":H11_GIT_SHA1,
       "minecraft":VERSION,
       "exact_server_states_verified":4,
       "same_camera":POSE,
       "same_world_coordinate":[X,Y,Z],
       "observed_RGB_diff_counts":actual,
       "face_by_face_GPU_UV_causality_approved":False,
       "new_real_game_sessions":1,
       "new_native_game_F2":4,
       "F70_full_approval":0,
       "H03_H05_full_exit":False,
       "INT5_semantic_approval":0,
       "INT6_AI_training_redistribution_approval":0,
    }
    (directory/AUDIT).write_text(json.dumps(final,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                                 encoding="utf-8")
    return final

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(audit(a.directory),ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
