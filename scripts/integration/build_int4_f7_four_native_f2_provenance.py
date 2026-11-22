#!/usr/bin/env python3
"""F7 audit: original game images + 70 frozen cases; S22 vanilla parent HOLD."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from zipfile import ZipFile

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
BASE=Path("project/integration/INT4_F6_70_TARGET_EVIDENCE_DISPOSITIONS_V5.csv")
CAPTURE=Path("project/integration/INT4_F7_FOUR_NATIVE_GAME_F2_SOURCE_REPORT_V1.json")
STUDY=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PIN={
 str(BASE):"b572b24ffc2a6e694464b89b6558b2e3baa2da92",
 str(CAPTURE):"9804a4dd47118bd458d5c0e25b509f8e4e390281",
 str(STUDY):"56e6f4c21c50714b97079ec61f7219bea845f179",
}
RUN=45031468054
ARTIFACT_ID=14758360785
ZIP_NAME="int4-f7-af-chair-bench-drawer-4case-real-native-F2.zip"
ZIP_SHA="e52990c06605e44db4127c2e2eec0e7a729d817e86f3843d05127435f3aa64d8"
CASES=("S03","S04","S22","S30")
CONDITIONAL=("S03","S04","S30")
VANILLA_PARENT="assets/minecraft/models/block/cube.json"
VANILLA_PARENT_SHA="3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e"
NOTES={
"S03":"실제 F2에서 밝은 목재 등받이와 좌판을 갖춘 작은 의자가 보임",
"S04":"실제 F2에서 어두운 갈색 목재 등받이와 좌판을 갖춘 작은 의자가 보임",
"S22":"실제 F2에서 사각형 목재 서랍형 블록을 관찰. 실행 바닐라 부모 SHA 검증 별도",
"S30":"실제 F2에서 상판과 위쪽 등받이 부품이 모두 있는 낮은 목재 벤치를 관찰",
}
OUTPUT=Path("project/integration")
F70=OUTPUT/"INT4_F7_70_TARGET_EVIDENCE_DISPOSITIONS_V6.csv"
PENDING=OUTPUT/"INT4_F7_28_PENDING_EXACT_F2_TARGETS_V1.csv"
EXCEPTION=OUTPUT/"INT4_F7_S22_VANILLA_PARENT_EXTERNAL_EXCEPTION_V1.json"
SUMMARY=OUTPUT/"INT4_F7_ORIGINAL_NATIVE_F2_INDEPENDENT_AUDIT_V1.json"
REPORT=OUTPUT/"INT4_F7_VISUAL_SOURCE_REVIEW_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def locked(path):
    b=(ROOT/path).read_bytes()
    assert blob(b)==PIN[str(path)],("ORIGINAL_SOURCE_DRIFT",str(path),blob(b))
    return b

def rows(b):
    return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))

def csvb(records,header):
    out=io.StringIO(newline="")
    writer=csv.DictWriter(out,fieldnames=header,lineterminator="\n")
    writer.writeheader();writer.writerows(records)
    return out.getvalue().encode("utf-8")

def jsb(doc):
    return (json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")

def get_zip(path):
    if path.is_file():return path.read_bytes()
    token=os.environ.get("GH_TOKEN")
    if not token:raise FileNotFoundError("F7 original GitHub Actions ZIP missing")
    url=f"https://api.github.com/repos/sanato-nb/Minecraft_Furniture_Style_Research/actions/artifacts/{ARTIFACT_ID}/zip"
    h={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
       "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-INT4-F7-evidence-audit"}
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs):return None
    try:
        with urllib.request.build_opener(NoRedirect).open(
                urllib.request.Request(url,headers=h),timeout=90) as response:
            b=response.read()
    except urllib.error.HTTPError as error:
        if error.code not in (301,302,303,307,308):raise
        redirect=error.headers.get("Location","")
        target=urlsplit(redirect)
        assert target.scheme=="https" and target.netloc and target.netloc!="api.github.com"
        with urllib.request.urlopen(
                urllib.request.Request(redirect,headers={"User-Agent":"MCFR-INT4-F7-evidence-audit"}),
                timeout=90) as response:b=response.read()
    assert sha(b)==ZIP_SHA,("ZIP_SHA_DRIFT",sha(b))
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(b)
    return b

def create(archive_path):
    prior=rows(locked(BASE))
    captured=json.loads(locked(CAPTURE).decode("utf-8"))
    study=rows(locked(STUDY))
    assert len(prior)==70 and len({r["target_id"] for r in prior})==70
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in prior)==39
    assert sum(r["final_disposition"].startswith("HOLD") for r in prior)==31
    assert captured["historical_case_ids"]==list(CASES)
    assert (captured["original_source_applications"],
            captured["original_effective_elements"],
            captured["original_effective_faces"])==(5,31,144)
    assert captured["counts"]["original_model_selection_matched_release"]==4
    assert captured["counts"]["real_game_exact_state"]==4
    assert captured["native_f2_png_count"]==4
    old={r["target_id"]:dict(r) for r in prior}
    studycases={k:[r for r in study if r["case"]==k] for k in CASES}
    assert {k:len(v) for k,v in studycases.items()}=={"S03":1,"S04":1,"S22":1,"S30":2}
    assert all(old[k]["final_disposition"].startswith("HOLD") for k in CASES)
    archive=get_zip(archive_path)
    assert sha(archive)==ZIP_SHA
    checked={}
    with ZipFile(io.BytesIO(archive)) as z:
        assert z.testzip() is None
        filenames=z.namelist()
        assert len(filenames)==len(set(filenames))
        assert set(filenames)=={"manifest.json","client.log",*(k+".png" for k in CASES)}
        manifest=json.loads(z.read("manifest.json"))
        assert manifest["status"]=="SERVER_STATES_AND_F2_RECORDED"
        assert manifest["minecraft"]=="1.21.1"
        assert manifest["f_target_case_ids"]==list(CASES)
        assert manifest["f_source_only"] is True
        assert sha(z.read("client.log"))==(
            manifest["client_log_sha256"]==captured["original_client_log_sha256"])
        assert manifest["source"]["ledger_sha256"]==captured["original_1_5_application_csv_sha256"]
        for key in CASES:
            original=studycases[key]
            r=captured["source_cases"][key]
            source=manifest["source"]["representative_states"][key]
            assert source["state"]==r["requested_exact_original_state"]
            assert source["historical_selection_matches_release"] is True
            assert r["release_selector_matches_all_original_models"] is True
            assert source["historical_model_geometry"]=={
                "elements":r["original_geometry_elements"],
                "faces":r["original_geometry_faces"]}
            assert r["game_server_exact_requested_state"] is True
            assert manifest["server_states"][key]["subject"]["exact"] is True
            assert len(source["release_model_applications"])==len(original)
            assert len(original)==r["original_model_application_count"]
            required={row[k+"_path"]:row[k+"_sha"] for row in original
                      for k in ("state","model","provider")}
            assert r["original_git_source_sha_by_path"]==required
            assert set(source["source_files"])==set(required)
            for path,gsha in required.items():
                assert source["source_files"][path]["historical_git_blob_sha1"]==gsha
            missing=[path for path,meta in source["source_files"].items()
                     if meta.get("release_path_absent",False)]
            if key=="S22":
                assert missing==[VANILLA_PARENT]
                assert required[VANILLA_PARENT]==VANILLA_PARENT_SHA
                assert r["external_vanilla_parent_independent_runtime_sha_approved"] is False
                assert all(meta["git_blob_byte_match"] is True
                    for path,meta in source["source_files"].items() if path!=VANILLA_PARENT)
            else:
                assert not missing
                assert all(meta["git_blob_byte_match"] is False
                           for meta in source["source_files"].values())
            if key=="S30":
                assert {int(x["faces"]) for x in original}=={34,12}
                assert len({x[0] for x in source["release_model_applications"]})==2
            png=z.read(key+".png")
            assert sha(png)==r["native_F2_sha256"]==manifest["native_f2_sha256"][key]
            with Image.open(io.BytesIO(png)) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
            checked[key]={
                "model_application_count":len(original),
                "release_model_selection_matches_original":True,
                "server_exact_original_state":True,
                "original_native_F2_sha256":sha(png),
                "missing_parent_from_mod_jar":missing,
                "qualitative_direct_visual_review":NOTES[key],
                "disposition":"CONDITIONAL" if key in CONDITIONAL else "HOLD_EXTERNAL_VANILLA_PARENT",
            }
    for record in prior:
        k=record["target_id"]
        if k not in CASES:continue
        good=k in CONDITIONAL
        record.update({
            "prior_f2_evidence_status":"ORIGINAL_NATIVE_F2_AND_EXACT_GAME_STATE_REOPENED_F7",
            "image_artifact_ids":str(ARTIFACT_ID),
            "image_run_ids":str(RUN),
            "image_files":ZIP_NAME+":"+k+".png",
            "image_sha256s":checked[k]["original_native_F2_sha256"],
            "original_zip_sha256s":ZIP_SHA,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":NOTES[k],
            "source_state_and_release_assessment":(
                "RELEASE_SELECTOR_MATCH_AF_STUDY_JAR_BYTE_DIFFERENCE_DOCUMENTED"
                if good else "HC_RELEASE_SELECTOR_MATCH_BUT_VANILLA_PARENT_RUNTIME_SHA_UNVERIFIED"),
            "final_disposition":(
                "CONDITIONAL_F7_MODEL_STATE_AND_REAL_F2_ORIGINAL_SOURCE_MATCH"
                if good else "HOLD_F7_EXTERNAL_VANILLA_PARENT_RUNTIME_SHA_PENDING"),
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":(
                "독립 원본 F2와 정확한 서버/선택 모델 확보; AF 연구본과 실행본 바이트 차이 및 UV/의미/권리 검증 별도"
                if good else "바닐라 minecraft:block/cube 부모를 실제 실행 Minecraft 1.21.1에서 읽고 원본 V1211-5 SHA와 별도 검증해야 함"),
        })
    assert {r["target_id"] for r in prior if r!=old[r["target_id"]]}==set(CASES)
    cond=sum(r["final_disposition"].startswith("CONDITIONAL") for r in prior)
    hold=sum(r["final_disposition"].startswith("HOLD") for r in prior)
    assert (cond,hold)==(42,28)
    hist=[r for r in prior if r["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(hist)==62
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in hist)==36
    pend=[r for r in prior if r["final_disposition"].startswith("HOLD")]
    groups=dict(sorted(Counter(r["cohort"] or "RISK" for r in pend).items()))
    assert groups=={"HC":1,"MACAW":10,"RISK":2,"VANILLA":15}
    assert {r["target_id"] for r in pend if r["cohort"]=="HC"}=={"S22"}
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in prior)
    all_bytes=csvb(prior,list(prior[0]))
    fields=("target_id","cohort","minecraft_version","category","block",
            "original_source_applications","original_source_faces","final_disposition",
            "additional_required_before_full_acceptance")
    pending_bytes=csvb([{f:r[f] for f in fields} for r in pend],list(fields))
    exc={
        "schema":"MCFR_INT4_F7_S22_EXTERNAL_VANILLA_PARENT/v1",
        "case":"S22","runtime_version":"1.21.1",
        "frozen_original_research_vanilla_version":"1.21.11 source group V1211-5",
        "parent_asset_path":VANILLA_PARENT,
        "original_study_parent_git_blob_sha1":VANILLA_PARENT_SHA,
        "parent_absent_from_installed_HC_mod_jar":True,
        "HC_state_and_leaf_match_pinned_study":True,
        "real_client_game_state_and_F2_recorded":True,
        "real_client_vanilla_parent_bytes_independently_verified":False,
        "case_disposition":"HOLD_EXTERNAL_VANILLA_PARENT_RUNTIME_GIT_SHA_UNVERIFIED",
        "next_work":"Extract official running Minecraft 1.21.1 cube.json bytes, pin SHA and compare with frozen 1.21.11 parent source",
    }
    exc_bytes=jsb(exc)
    summary={
        "schema":"MCFR_INT4_F7_ORIGINAL_NATIVE_F2_FULL_SOURCE_INDEPENDENT_AUDIT/v1",
        "status":"PASS_FOUR_NATIVE_F2_THREE_CONDITIONAL_ONE_EXTERNAL_PARENT_HOLD",
        "original_git_blob_sha1_pins":PIN,
        "original_game_action_run":RUN,
        "original_game_artifact_id":ARTIFACT_ID,
        "original_game_zip_sha256":ZIP_SHA,
        "original_client_log_sha256":captured["original_client_log_sha256"],
        "cases":checked,
        "remaining_hold_by_cohort":groups,
        "counts":{
            "fixed_F_target_units":70,"historic_source_cases":62,
            "new_original_real_F2_images":4,
            "new_original_model_applications":5,
            "new_source_elements":31,"new_source_faces":144,
            "new_server_exact_game_states":4,"new_model_selector_equals_release":4,
            "new_conditional_cases":3,"new_external_parent_HOLD":1,
            "F_conditional_before":39,"F_conditional_now":42,
            "F_HOLD_before":31,"F_HOLD_now":28,
            "historical_exact_F2_conditional_before":33,
            "historical_exact_F2_conditional_now":36,
            "full_F_unconditional_approvals":0,
            "new_INT5_part_semantic_approvals":0,
            "new_INT6_model_training_or_redistribution_rights":0,
        },
        "limits":[
            "AF source Git and Fabric release JAR bytes differ; model selection matches but byte equality is not asserted.",
            "S30 two models are simultaneously selected in one historical case.",
            "S22 vanilla parent is outside HC JAR; actual 1.21.1 vanilla parent SHA is NOT yet independently checked.",
            "Original F2 images qualitatively reviewed but do not prove UV or semantic causality.",
            "Other 66 source rows and all original source Git documents unchanged; no original game assets committed.",
            "INT-4-F full exit, G/H, INT5/INT6 rights not approved.",
        ],
        "outputs":{
            "F70":{"rows":70,"sha256":sha(all_bytes)},
            "pending":{"rows":28,"sha256":sha(pending_bytes)},
            "S22_exception":{"sha256":sha(exc_bytes)},
        },
    }
    report="\n".join([
        "# INT-4-F7 실제 Minecraft Fabric 1.21.1 네 사례 원본 독립 감사",
        "",
        "- 게임 촬영 Actions: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/"+str(RUN),
        "- 네이티브 F2 4장+클라이언트 로그 GitHub Actions 아티팩트: "+str(ARTIFACT_ID),
        "- S03 자작나무 의자, S04 가문비나무 의자: 원본 variant=3은 *_1 leaf 모델 선택. 실제 릴리스 선택/서버 상태/F2 일치, AF 소스와 JAR 바이트 차이 보존. 조건부.",
        "- S30 등받이 벤치: 단일 원본 사례에서 34면+12면 모델 2개가 동시에 선택됨. F2에서 벤치·등받이를 관찰함. 조건부.",
        "- S22 참나무 서랍: HC leaf/state 및 서버 상태/F2는 일치. 그러나 연구 V1211-5 바닐라 cube 부모와 실행 1.21.1 바닐라 cube 부모 SHA 직접 비교 전까지 HOLD.",
        "- 원본 1-5: 네 역사 사례, 모델 적용 5개, 요소 31, 면 144. 네이티브 이미지 SHA 4개 검증.",
        "- 진행: 조건부 39→42, 보류 31→28, 역사 사례 원본 F2 연결 조건부 33/62→36/62. 최종 무조건 승인 0.",
        "- 이미지 관찰은 실제 PNG 재열람 근거이며 픽셀 UV 인과, 부품 의미 및 AI 학습·재배포권을 승인하지 않음.",
        "",
    ]).encode("utf-8")
    return {F70:all_bytes,PENDING:pending_bytes,EXCEPTION:exc_bytes,
            SUMMARY:jsb(summary),REPORT:report}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--artifact-dir",type=Path,default=Path("temporary-F7"))
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    for path,b in create(args.artifact_dir/ZIP_NAME).items():
        f=ROOT/path
        if args.verify:
            assert f.is_file() and f.read_bytes()==b,("OUTPUT_MISMATCH",str(path))
        else:
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_bytes(b)
        print("VERIFIED" if args.verify else "CREATED",path,len(b))
    print("PASS 70 fixed targets: conditional 42, HOLD 28, full accept 0")

if __name__=="__main__":main()
