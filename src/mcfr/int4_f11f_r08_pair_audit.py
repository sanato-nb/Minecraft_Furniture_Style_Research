"""F11F R08 original dual-Fabric F2 evidence; never equate source-build with released NeoForge 4.0.3."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from .int4_f11f_r08_af_dual_fabric_capture import (
    CASE_ID,MANIFEST,UPSTREAM,BLOCK_STATE,ORIGINAL_STUDY_STATE_BLOB,
    OFFICIAL_RUNTIME_STATE_BLOB,MODEL_TARGET,sha
)

ROI=(320,225,715,620)

def verify(b,msg):
    if not b:raise ValueError(msg)

def load(folder,expected):
    root=Path(folder)
    report=json.loads((root/MANIFEST).read_text(encoding="utf-8"))
    verify(report["schema"]=="MCFR_INT4_F11F_R08_SINGLE_FABRIC_SOURCE_ACTUAL_GAME/v1",
           "Wrong F11F manifest")
    verify(report["status"]=="ONE_REAL_FABRIC_SOURCE_RELEASE_F2_CAPTURED_NOT_CROSS_RELEASE_APPROVED",
           "Real game capture not complete")
    verify(report["minecraft"]=="1.21.1" and report["risk_case"]=="R08",
           "Wrong game/risk scope")
    verify(report["release"]["version"]==expected,
           "Wrong source/release role")
    verify(report["release"]["selected_exact_original_state"]==BLOCK_STATE and
           report["release"]["selected_model"]==MODEL_TARGET and
           report["actual_server_original_state_PASS"] is True,
           "Original server source state or selected model did not match")
    verify(report["release"]["selected_blockstate_git_blob_sha1"]==
           (OFFICIAL_RUNTIME_STATE_BLOB if expected=="4.0.2" else ORIGINAL_STUDY_STATE_BLOB),
           "Pinned original model state source hash not matched")
    if expected=="4.0.3":
        verify(report["release"]["not_an_official_published_Fabric_4_0_3"] is True and
               report["release"]["source_study_Git_commit"]==UPSTREAM,
               "Source-built research artifact incorrectly labeled official")
    name=root/(CASE_ID+".png")
    verify(name.is_file() and sha(name.read_bytes())==report["native_F2_sha256"],
           "Original F2 SHA changed or missing")
    verify(report["native_F2_dimensions"]==[1024,684],"Wrong source F2 size")
    with Image.open(name) as img:
        img.load()
        verify(img.format=="PNG" and img.size==(1024,684),
               "Original F2 image unavailable or wrong size")
        rgb=img.convert("RGB")
    verify(sha((root/"client.log").read_bytes())==report["client_log_sha256"],
           "Original game client log changed")
    return report,rgb

def compare(baseline,study,output=None):
    old,a=load(baseline,"4.0.2")
    new,b=load(study,"4.0.3")
    assert a.size==b.size
    px=list(a.crop(ROI).getdata())
    qx=list(b.crop(ROI).getdata())
    changed=sum(max(abs(x-y) for x,y in zip(p,q))>=24 for p,q in zip(px,qx))
    # Note separate runs can differ in lighting/time/chunk state. This metric
    # is descriptive only and cannot attribute pixels to the release.
    verdict={
        "schema":"MCFR_INT4_F11F_R08_TWO_REAL_FABRIC_STUDY_VS_PUBLISHED_F2_AUDIT/v1",
        "status":"DUAL_FABRIC_NATIVE_F2_SOURCE_BUILD_COMPARISON_NOT_OFFICIAL_403_RELEASE",
        "minecraft_version":"1.21.1",
        "historical_risk_case":"R08",
        "same_loader":"fabric",
        "exact_same_original_state":BLOCK_STATE,
        "selected_model":MODEL_TARGET,
        "original_4_0_3_study_git_commit":UPSTREAM,
        "runs":{
            "published_fabric_4_0_2":old["release"]|{
                "native_F2_sha256":old["native_F2_sha256"],
                "client_log_sha256":old["client_log_sha256"],
                "real_server_state_PASS":True},
            "git_source_built_fabric_4_0_3":new["release"]|{
                "native_F2_sha256":new["native_F2_sha256"],
                "client_log_sha256":new["client_log_sha256"],
                "real_server_state_PASS":True},
        },
        "descriptive_image_noncausal":{
            "roi":list(ROI),
            "difference_channel_threshold":24,
            "roi_changed_pixel_count":changed,
            "roi_pixel_count":len(px),
            "different_client_sessions_not_pixel_aligned":True,
            "difference_proves_version_caused_visual_change":False,
        },
        "gates":{
            "two_real_same_loader_Fabric_1_21_1_client_F2":True,
            "published_official_fabric_4_0_2":True,
            "source_built_fabric_4_0_3_matches_pinned_Git_state_and_model":True,
            "published_official_fabric_4_0_3":False,
            "official_4_0_3_NeoForge_client_F2":False,
            "all_88_source_option_visual_parity":False,
            "direct_pixel_attribution_to_model_UV":False,
            "INT4_F_final_unconditional_approval":False,
            "INT5_semantics":False,
            "INT6_training_or_redistribution_rights":False,
        },
        "limits":[
            "4.0.3 research-built Fabric jar is not the official published 4.0.3 NeoForge jar.",
            "One north facing variant=1 state only; source/screenshot pairs cannot certify all 88 selectors.",
            "Different Minecraft render sessions are not a controlled pixel-identical projection.",
            "Do not promote R08 beyond original HOLD without an independent scope gate decision.",
        ],
    }
    if output:
        path=Path(output)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(verdict,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return verdict

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--baseline",required=True,type=Path)
    p.add_argument("--study",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    print(json.dumps(compare(args.baseline,args.study,args.output),ensure_ascii=False,sort_keys=True,indent=2))

if __name__=="__main__":
    main()
