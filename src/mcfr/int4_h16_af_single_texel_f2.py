"""INT-4-H16 original AF source 1-texel disposable JAR intervention.

An external temporary resource pack was loaded but had zero game pixels change;
Fabric pack ordering made actual override inconclusive. The second test verifies
the official JAR SHA first, then changes ONE texture texel in a disposable test
copy, preserving every other uncompressed JAR member. Neither copyrighted JAR
nor modified PNG leaves scratch; only actual native F2 / logs are archived.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import subprocess
from pathlib import Path
from time import sleep
from zipfile import ZipFile

from PIL import Image

from .runtime_capture import wait_for
from .chair_runtime_capture import (
    send_minecraft_command, confirmed_camera_teleport, confirmed_spectator_mode,
    archive_gui_diagnostic,
)
from . import int4_h12_af_chair_samepose_f2_capture as h12
from . import int4_h15_af_opposing_f2_capture as h15

ROOT = Path(__file__).resolve().parents[2]
VERSION = "1.21.1"
TEX_REL = "assets/another_furniture/textures/block/chair/back_1/acacia.png"
TEX_BLOB_PIN = "55f3bbf986c0c10b731cc0e67038402f30340972"
TARGET = (3, 1)
SOURCE_RGBA = (173, 93, 50, 255)
PROBE_RGBA = (255, 0, 255, 255)
VIEWS = h15.VIEWS
STAGES = ("model1_before","model3","model1_after")
BLOCK = h15.BLOCK_XYZ
CAMERAS = h15.EXPECTED_CAMERAS
ORIGINAL = "INT4_H16_SINGLE_TEXEL_REAL_FABRIC_F2_MANIFEST_V1.json"
AUDIT = "INT4_H16_SINGLE_TEXEL_VS_H15_ORIGINAL_F2_AUDIT_V1.json"
H15_ORIGINAL = "INT4_H15_AF_OPPOSING_VIEW_REAL_NATIVE_F2_MANIFEST_V1.json"
H15_SHA = "4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def prepare_one_texel_probe(game: Path) -> dict:
    """Preflight official 4.0.2, then patch ONE texel in disposable runtime JAR.

    A normal external resource pack was observed before Fabric's mod resource
    pack in the live ResourceManager list, and had zero actual F2 effect.
    This new test copy replaces ONE ZIP member and preserves all other
    uncompressed ZIP member bytes. Neither modified JAR nor PNG is uploaded.
    """
    source=h12.static_preflight(game)
    jar=game/"mods"/"another_furniture-fabric-4.0.2.jar"
    original_bytes=jar.read_bytes()
    original_sha=hashlib.sha1(original_bytes).hexdigest()
    check(original_sha==h12.JAR_SHA1,"H16_OFFICIAL_SOURCE_JAR_PIN_MISMATCH")
    with ZipFile(io.BytesIO(original_bytes)) as archive:
        names=archive.namelist()
        check(len(names)==len(set(names)) and TEX_REL in names,
              "H16_JAR_MEMBER_NAMES_NONUNIQUE_OR_TARGET_MISSING")
        metadata=archive.infolist()
        original_resources={name:archive.read(name) for name in names}
    raw=original_resources[TEX_REL]
    check(blob(raw)==TEX_BLOB_PIN, "H16_ORIGINAL_AF_PNG_GIT_SHA_MISMATCH")
    with Image.open(io.BytesIO(raw)) as original:
        original.load()
        check(original.format=="PNG" and original.size==(16,16),
              "H16_ORIGINAL_TEXTURE_NOT_PINNED_16_RGBA")
        rgba=original.convert("RGBA")
    check(rgba.getpixel(TARGET)==SOURCE_RGBA,
          "H16_SOURCE_PIXEL_RGBA_NOT_THE_PINNED_OPAQUE_PIXEL")
    modified=rgba.copy()
    modified.putpixel(TARGET,PROBE_RGBA)
    changed=sum(rgba.getpixel((x,y))!=modified.getpixel((x,y))
                for x in range(16) for y in range(16))
    check(changed==1,"H16_MUST_CHANGE_ONE_AND_ONLY_ONE_SOURCE_TEXEL")
    buffer=io.BytesIO()
    modified.save(buffer,format="PNG")
    patched_png=buffer.getvalue()
    check(sha(patched_png)!=sha(raw),"H16_PROBE_PNG_BYTES_NOT_MODIFIED")
    replacements={**original_resources,TEX_REL:patched_png}
    patched_file=game/"mods"/"another_furniture-h16-modified-disposable.tmp"
    with ZipFile(patched_file,"w") as output_zip:
        for entry in metadata:
            output_zip.writestr(entry,replacements[entry.filename])
    with ZipFile(patched_file) as verified:
        check(verified.testzip() is None and verified.namelist()==names,
              "H16_MODIFIED_TEST_JAR_ZIP_CRC_OR_ENTRIES_DRIFT")
        differences=[name for name in names
                     if verified.read(name)!=original_resources[name]]
        check(differences==[TEX_REL],
              "H16_MORE_THAN_ONE_OR_WRONG_SOURCE_JAR_MEMBER_CHANGED")
        with Image.open(io.BytesIO(verified.read(TEX_REL))) as after:
            after.load()
            pixels=after.convert("RGBA")
            check(sum(pixels.getpixel((x,y))!=rgba.getpixel((x,y))
                      for x in range(16) for y in range(16))==1 and
                  pixels.getpixel(TARGET)==PROBE_RGBA,
                  "H16_REOPENED_MODIFIED_JAR_TARGET_TEXEL_WRONG")
    # Keep the public original release in memory for provenance only; the
    # dedicated disposable Fabric runtime sees the modified test-copy JAR.
    patched_bytes=patched_file.read_bytes()
    patched_sha=hashlib.sha1(patched_bytes).hexdigest()
    check(patched_sha!=original_sha,"H16_MODIFIED_JAR_SAME_AS_OFFICIAL_SHA")
    patched_file.replace(jar)
    check(hashlib.sha1(jar.read_bytes()).hexdigest()==patched_sha,
          "H16_DISPOSABLE_RUNTIME_JAR_PATCH_NOT_INSTALLED")
    return {
        "official_AF_jar_sha1_before_temporary_patch":original_sha,
        "ephemeral_runtime_test_jar_sha1":patched_sha,
        "official_source_JAR_verified_before_patch":True,
        "original_AF_texture_git_blob_sha1":TEX_BLOB_PIN,
        "original_AF_texture_sha256":sha(raw),
        "original_H11_source_sha1":source["h11_git_blob_sha1"],
        "only_original_source_resource_member_modified":TEX_REL,
        "original_texel_xy":list(TARGET),
        "original_texel_rgba":list(SOURCE_RGBA),
        "modified_texel_rgba":list(PROBE_RGBA),
        "source_RGBA_texels_modified":1,
        "changed_uncompressed_JAR_resources":1,
        "all_other_ZIP_member_bytes_unchanged":True,
        "original_JAR_test_copy_is_ephemerally_modified":True,
        "modified_JAR_and_PNG_never_uploaded_to_GitHub":True,
    }


def assert_patched_mod_loaded(log_text: str) -> str:
    """Prove actual Fabric loads AF mod; JAR patch presence is separately SHA pinned."""
    lines=[s for s in log_text.splitlines()
           if "Reloading ResourceManager:" in s and "another_furniture" in s]
    check(bool(lines),"H16_ORIGINAL_AF_MOD_NOT_LOADED_BY_FABRIC")
    return sha(lines[-1].encode("utf-8"))

def model_state(stage: str) -> str:
    check(stage in STAGES,"H16_BAD_MODEL_CONTROL_STAGE")
    return h12.state("model3" if stage=="model3" else "model1")


def label(view,stage):
    check(view in VIEWS and stage in STAGES,"H16_UNKNOWN_STAGE_OR_VIEW")
    return view+"_"+stage


def capture(command, env, game, output, version):
    check(version==VERSION,"H16_PINNED_OFFICIAL_121_FABRIC_CLIENT_REQUIRED")
    case=h12.original_case()[0]
    check((case.x,case.y,case.z)==BLOCK and
          case.camera()==CAMERAS["south"],"H16_ORIGINAL_H15_CASE_CHANGED")
    provenance=prepare_one_texel_probe(Path(game))
    dest=Path(output)
    dest.mkdir(parents=True,exist_ok=False)
    log=dest/"client.log"
    shots=Path(game)/"screenshots"
    states={v:{} for v in VIEWS}
    with log.open("wb") as sink,subprocess.Popen(
            command,cwd=game,env=env,stdout=sink,stderr=subprocess.STDOUT) as proc:
        def read():return log.read_text(encoding="utf-8",errors="replace")
        def xdo(*args):
            return subprocess.check_output(["xdotool",*args],env=env,timeout=18,text=True).strip()
        def refocus():xdo("windowfocus","--sync",window)
        def send(command_line):send_minecraft_command(xdo,command_line)
        def acknowledge(cmd,marker,name):
            for attempt,limit in enumerate((25,35),start=1):
                refocus();point=len(read());send(cmd)
                try:
                    wait_for(proc,lambda:marker in read()[point:],
                             "H16 actual client "+name+" attempt "+str(attempt),limit)
                except ValueError as e:
                    if not str(e).startswith("Timed out waiting for") or attempt==2:
                        raise
                    continue
                sleep(.7)
                return
            raise ValueError("H16_GAME_SERVER_ACK_MISSING "+name)
        try:
            wait_for(proc,lambda:"RenderAudit joined the game" in read(),
                     "H16 actual pinned Fabric world join",180)
            wait_for(proc,lambda:"Loaded 2 advancements" in read(),
                     "H16 actual client fully ready",90)
            mod_loaded_log_sha=assert_patched_mod_loaded(read())
            sleep(7)
            windows=xdo("search","--all","--onlyvisible","--pid",str(proc.pid),
                        "--name","^Minecraft").split()
            check(len(windows)==1,"H16_REAL_CLIENT_WINDOW_NOT_UNIQUE")
            window=windows[0];refocus();sleep(2)
            confirmed_spectator_mode(proc,read,send,refocus)
            acknowledge("/function mcfr_chair:place",
                        "[RenderAudit] MCFR_CHAIR_PLACED",
                        "original north chair placement")
            acknowledge("/function mcfr_chair:verify",
                        "[RenderAudit] MCFR_CHAIR_STATES_READ",
                        "original north chair exact fixture")
            shots.mkdir(exist_ok=True)
            previous_state=h12.state("model1")
            for view in VIEWS:
                confirmed_camera_teleport(proc,read,send,refocus,CAMERAS[view])
                for stage in STAGES:
                    name=label(view,stage)
                    state=model_state(stage)
                    if state!=previous_state:
                        x,y,z=BLOCK
                        acknowledge(f"/setblock {x} {y} {z} {state}",
                                    "[RenderAudit: Changed the block at",
                                    "patched model state "+name)
                    previous_state=state
                    x,y,z=BLOCK
                    marker="MCFR_H16_"+name.upper()+"_EXACT_SERVER=PASS"
                    acknowledge(f"/execute if block {x} {y} {z} {state} run say {marker}",
                                "[RenderAudit] "+marker,
                                "actual original server exact "+name)
                    sleep(5)
                    shot=h12.screenshot(xdo,window,shots,dest,name,{"proc":proc})
                    states[view][stage]={"blockstate":state,"server_marker":marker,
                                         "exact_server_verified":True,**shot}
                    print("H16_ACTUAL_NATIVE_F2_CAPTURED "+name,flush=True)
        except Exception:
            archive_gui_diagnostic(dest,"H16_PACK_OR_CAMERA_OR_FRAME_FAILURE")
            raise
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=30)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
    check(all(set(states[v])==set(STAGES) for v in VIEWS),
          "H16_PINNED_ORIGINAL_F2_SIX_FRAMES_INCOMPLETE")
    check(assert_patched_mod_loaded(log.read_text(encoding="utf-8",errors="replace"))==
          mod_loaded_log_sha,"H16_AF_MOD_LOADED_LOG_CHANGED")
    manifest={
        "schema":"MCFR_INT4_H16_SINGLE_TEXEL_REAL_FABRIC_SOURCE_CAPTURE/v1",
        "status":"H16_SIX_ACTUAL_F2_TEMP_JAR_ONE_TEXEL_REQUIRES_INDEPENDENT_AUDIT",
        "game_version":VERSION,"game_session_count":1,
        "actual_native_F2_count":6,"original_source_facing":"north",
        "original_block_xyz":list(BLOCK),"camera_order":list(VIEWS),
        "cameras":CAMERAS,"models":h12.MODELS,"views":states,
        "provenance":provenance,
        "actual_AF_mod_load_log_line_SHA256":mod_loaded_log_sha,
        "client_log_sha256":sha(log.read_bytes()),
        "one_texel_GPU_screen_effect_approved":False,
        "precise_GPU_face_UV_pixel_attribution_approved":False,
        "F70_unconditional_approvals":0,"H03_H05_full_exit":False,
        "INT5_semantics_approved":0,
        "INT6_AI_training_or_asset_redistribution_rights_approved":0,
    }
    (dest/ORIGINAL).write_text(
        json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
        encoding="utf-8")
    # Do not copy the temporary patched mod JAR or derived PNG into the output.
    return manifest


def audit(directory, h15_original_zip):
    root=Path(directory)
    raw=(root/ORIGINAL).read_bytes()
    doc=json.loads(raw)
    check(doc["schema"]=="MCFR_INT4_H16_SINGLE_TEXEL_REAL_FABRIC_SOURCE_CAPTURE/v1" and
          doc["game_version"]==VERSION and doc["game_session_count"]==1 and
          doc["actual_native_F2_count"]==6 and doc["original_block_xyz"]==list(BLOCK) and
          doc["camera_order"]==list(VIEWS) and doc["cameras"]==CAMERAS and
          doc["original_source_facing"]=="north",
          "H16_ORIGINAL_REAL_MINECRAFT_CAPTURE_IDENTITY_MISSING")
    p=doc["provenance"]
    check(p["source_RGBA_texels_modified"]==1 and
          p["original_texel_xy"]==list(TARGET) and
          p["original_texel_rgba"]==list(SOURCE_RGBA) and
          p["modified_texel_rgba"]==list(PROBE_RGBA) and
          p["official_source_JAR_verified_before_patch"] is True and
          p["official_AF_jar_sha1_before_temporary_patch"]==h12.JAR_SHA1 and
          p["ephemeral_runtime_test_jar_sha1"]!=h12.JAR_SHA1 and
          p["only_original_source_resource_member_modified"]==TEX_REL and
          p["original_AF_texture_git_blob_sha1"]==TEX_BLOB_PIN and
          p["changed_uncompressed_JAR_resources"]==1 and
          p["all_other_ZIP_member_bytes_unchanged"] is True and
          p["modified_JAR_and_PNG_never_uploaded_to_GitHub"] is True,
          "H16_MORE_THAN_ONE_SOURCE_RESOURCE_MUTATED_OR_PROVENANCE_MISSING")
    text=(root/"client.log").read_text(encoding="utf-8",errors="replace")
    check(sha((root/"client.log").read_bytes())==doc["client_log_sha256"] and
          assert_patched_mod_loaded(text)==doc["actual_AF_mod_load_log_line_SHA256"],
          "H16_ACTUAL_FABRIC_AF_MOD_LOG_PROOF_MISSING")
    with ZipFile(h15_original_zip) as z:
        check(z.testzip() is None and
              sha(Path(h15_original_zip).read_bytes())==H15_SHA,
              "H16_BASELINE_H15_ORIGINAL_ZIP_IDENTITY_DRIFT")
        original=json.loads(z.read(H15_ORIGINAL))
        check(original["runtime_version"]==VERSION and
              original["source_block_coordinates"]==list(BLOCK) and
              original["source_block_facing"]=="north" and
              original["cameras"]==CAMERAS and
              original["native_F2_count"]==8,
              "H16_BASELINE_H15_GAME_STATE_OR_CAMERA_MISMATCH")
        log_original=z.read("client.log")
        check(sha(log_original)==original["client_log_sha256"],
              "H16_BASELINE_H15_LOG_SHA_MISMATCH")
        result={}
        for view in VIEWS:
            imgs={}
            for stage in STAGES:
                item=doc["views"][view][stage]
                expected=model_state(stage)
                check(item["blockstate"]==expected and
                      item["exact_server_verified"] is True and
                      "[RenderAudit] "+item["server_marker"] in text and
                      item["image"]==label(view,stage)+".png" and
                      item["dimensions"]==[1024,684],
                      "H16_SERVER_STATE_OR_IMAGE_MARKER_MISMATCH_"+label(view,stage))
                binary=(root/item["image"]).read_bytes()
                check(sha(binary)==item["sha256"],
                      "H16_SOURCE_NATIVE_F2_SHA_MISMATCH_"+label(view,stage))
                with Image.open(io.BytesIO(binary)) as f:
                    f.load()
                    check(f.format=="PNG" and f.size==(1024,684),
                          "H16_NOT_ORIGINAL_MINECRAFT_NATIVE_F2")
                    imgs[stage]=f.convert("RGB")
            base_images={}
            for stage in STAGES:
                prior=original["views"][view][stage]
                data=z.read(view+"_"+stage+".png")
                check(sha(data)==prior["sha256"] and
                      prior["exact_server_verified"] is True,
                      "H16_H15_BASELINE_GAME_NATIVE_F2_PIN_MISSING")
                with Image.open(io.BytesIO(data)) as im:
                    im.load()
                    check(im.format=="PNG" and im.size==(1024,684),
                          "H16_BASELINE_SCREENSHOT_NOT_NATIVE")
                    base_images[stage]=im.convert("RGB")
            # AIR from H15 provides an independent unchanged foreground mask.
            air=z.read(view+"_air.png")
            check(sha(air)==original["views"][view]["air"]["sha256"],
                  "H16_H15_ORIGINAL_AIR_FOREGROUND_SHA_CHANGED")
            with Image.open(io.BytesIO(air)) as im:
                im.load()
                baseline_air=im.convert("RGB")
            patch_pixels=h15.pixel_changes(imgs["model1_before"],base_images["model1_before"])
            repeat_pixels=h15.pixel_changes(imgs["model1_before"],imgs["model1_after"])
            negative_pixels=h15.pixel_changes(imgs["model3"],base_images["model3"])
            baseline_foreground=h15.pixel_changes(base_images["model1_before"],baseline_air)
            outside=patch_pixels-baseline_foreground
            bounds=([min(x for x,y in patch_pixels),min(y for x,y in patch_pixels),
                     max(x for x,y in patch_pixels),max(y for x,y in patch_pixels)]
                    if patch_pixels else None)
            result[view]={
               "target_single_texel_RGBA_intervention_vs_H15_original_pixels":len(patch_pixels),
               "unchanged_model3_negative_control_vs_H15_original_pixels":len(negative_pixels),
               "patched_model1_before_to_after_temporal_control_pixels":len(repeat_pixels),
               "changed_pixels_outside_original_H15_chair_foreground":len(outside),
               "screen_change_bounds_xyxy_inclusive":bounds,
               "patch_change_in_original_model1_model3_delta_region":len(
                  patch_pixels & h15.pixel_changes(base_images["model1_before"],base_images["model3"])),
            }
    tested={view:(v["target_single_texel_RGBA_intervention_vs_H15_original_pixels"]>0 and
                   v["unchanged_model3_negative_control_vs_H15_original_pixels"]==0 and
                   v["patched_model1_before_to_after_temporal_control_pixels"]==0 and
                   v["changed_pixels_outside_original_H15_chair_foreground"]==0)
            for view,v in result.items()}
    conclusion={
       "schema":"MCFR_INT4_H16_AF_ONE_TEXEL_PROBE_VS_H15_REAL_F2/v1",
       "status":("PASS_CONTROLLED_ONE_SOURCE_TEXEL_CHANGED_NATIVE_F2_WITH_TWO_CAMERA_NEGATIVE_CONTROL"
                 if all(tested.values())
                 else "CONDITIONAL_ONE_TEXEL_PROBE_EFFECT_OR_NEGATIVE_CONTROL_NOT_ESTABLISHED"),
       "game":"Minecraft Java 1.21.1 Fabric",
       "source_mod":"Another Furniture 4.0.2",
       "new_actual_game_runs":1,
       "new_actual_native_game_F2":6,
       "exact_server_state_verified":6,
       "confirmed_AF_resource_in_real_Minecraft_log":True,
       "single_original_source_texel_modified":list(TARGET),
       "target_original_RGBA":list(SOURCE_RGBA),
       "target_intervention_RGBA":list(PROBE_RGBA),
       "official_source_JAR_verified_before_ephemeral_patch":True,
       "comparison_original_H15_artifact_zip_SHA256":H15_SHA,
       "native_F2_proof_SHA256":{label(v,s):doc["views"][v][s]["sha256"]
                                  for v in VIEWS for s in STAGES},
       "actual_client_log_SHA256":doc["client_log_sha256"],
       "source_manifest_SHA256":sha(raw),
       "per_camera_screen_intervention_evidence":result,
       "one_texel_screen_effect_supported_by_control":all(tested.values()),
       "specific_GPU_face_to_UV_texel_pixel_attribution_approved":False,
       "source_one_texel_not_material_license_grant":True,
       "F70_unconditional_approvals":0,"H03_H05_full_exit":False,
       "INT5_semantics_approved":0,
       "INT6_training_or_redistribution_rights_approved":0,
       "limits":[
           "A temporary external resource pack loaded but showed zero F2 difference; this follow-up directly patches exactly one RGBA texel in one archive member of a verified disposable test-copy JAR.",
           "A screen difference localized to a chair supports that the changed texel influenced the actual rendered frame, not precise GPU face / UV barycentric attribution.",
           "Both cameras are reviewed as separate evidence; no unproven GPU internals, author intention, model semantics or rights are approved.",
           "Official JAR SHA is verified before ephemeral test-copy patch; modified JAR/PNG never uploaded, only native F2 and game log archived.",
       ],
    }
    (root/AUDIT).write_text(json.dumps(conclusion,ensure_ascii=False,sort_keys=True,indent=2)+"\n",
                            encoding="utf-8")
    return conclusion


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",type=Path,required=True)
    p.add_argument("--h15-original-zip",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(audit(args.directory,args.h15_original_zip),ensure_ascii=False))


if __name__=="__main__":
    main()
