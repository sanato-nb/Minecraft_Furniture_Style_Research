#!/usr/bin/env python3
"""INT-4-F4 audit: real F2 images are NOT accepted if the requested state failed.

Reuses one original GitHub Actions artifact without new Minecraft execution.
Writes only derived metadata. SHA verification and source lineage are repeatable
in CI; visual observations are a dated manual interpretation of reopened PNGs.
"""
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
import zipfile
from urllib.parse import urlsplit

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
REPO="sanato-nb/Minecraft_Furniture_Style_Research"
I=Path("project/integration")
BASE=I/"INT4_F3_70_TARGET_EVIDENCE_DISPOSITIONS_V3.csv"
PRIOR=I/"INT4_F3_7_DIRECT_IMAGE_VISUAL_AUDIT_V1.json"
APPLICATIONS=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PIN={
 str(BASE):"86ea53a985f7da40a26f171894746a96f7f0ea36",
 str(PRIOR):"f272df1bf8ab4c4db9516e63f4e36f4a10e96747",
 str(APPLICATIONS):"56e6f4c21c50714b97079ec61f7219bea845f179",
}
RUN=45024608289
ARTIFACT=14755665621
ARCHIVE="int4-f4-seven-native-f2-including-state-exception.zip"
ZIP_SHA256="858aa23336a4dd206188fdcab0a5609e05d77845780a1e586cca5a2645eb79e0"
CASES=("S01","S02","S31","S32","S33","S34","S47")
EXACT={"S01","S31","S32","S33","S47"}
NOT_EXACT={"S02","S34"}
OBS={
 "S01":"실제 F2에서 작은 목제 의자와 등받이가 보임. 서버 tucked=false 정확한 상태 확인",
 "S02":"S01과 실제 F2의 픽셀이 동일한 목제 의자. tucked=true 요청 후 서버 정확 상태 불일치; 구별 외형은 입증하지 못함",
 "S31":"실제 F2에서 낮은 목재 벤치형 상판과 지지 구조 확인; 기능·연결 의미는 미승인",
 "S32":"실제 F2에서 밝은 좌판과 목재 팔걸이 형태의 단독 소파가 보임; 충돌·사용 기능은 미승인",
 "S33":"실제 F2에서 밝은 좌판과 목재 측면의 소파형 구조 확인; 단일 상태 서버 정확성 확인",
 "S34":"S33과 동일 픽셀의 소파 화면 확인. inner_left 요청 후 서버 정확 상태 불일치; 코너 외형은 미증명",
 "S47":"실제 F2에서 흰색 윗면과 줄무늬 몸체를 가진 작은 도기형 물체가 보임; 부품 재질 의미는 미승인",
}
RELEASE={"AF":{"state":False,"model":False,"provider":False},
         "HC":{"state":True,"model":True,"provider":True}}

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def pinned(path):
    b=(ROOT/path).read_bytes()
    assert blob(b)==PIN[str(path)],("INPUT_BLOB_DRIFT",str(path),blob(b))
    return b

def read_csv(b):
    return list(csv.DictReader(io.StringIO(b.decode("utf-8"),newline="")))

def serialize_csv(rows,columns):
    b=io.StringIO(newline="")
    w=csv.DictWriter(b,fieldnames=columns,lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return b.getvalue().encode("utf-8")

def serialize_json(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")

def download_if_missing(p):
    if p.is_file():return p.read_bytes()
    token=os.environ.get("GH_TOKEN","")
    if not token:
        raise FileNotFoundError(f"Original artifact missing: {p}, set GH_TOKEN to retrieve")
    url=f"https://api.github.com/repos/{REPO}/actions/artifacts/{ARTIFACT}/zip"
    headers={"Authorization":f"Bearer {token}","Accept":"application/vnd.github+json",
             "X-GitHub-Api-Version":"2022-11-28","User-Agent":"mcfr-int4f4-visual-audit"}
    request=urllib.request.Request(url,headers=headers)
    class BlockRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,location):
            return None
    no_redirect=urllib.request.build_opener(BlockRedirect)
    try:
        with no_redirect.open(request,timeout=90) as resp:
            raw=resp.read()
    except urllib.error.HTTPError as exc:
        if exc.code not in (301,302,303,307,308):raise
        location=exc.headers.get("Location","")
        parsed=urlsplit(location)
        assert parsed.scheme=="https" and parsed.netloc and parsed.netloc!="api.github.com",(
            "INVALID_ARTIFACT_REDIRECT",location[:100])
        with urllib.request.urlopen(
                urllib.request.Request(location,headers={"User-Agent":"mcfr-int4f4-visual-audit"}),
                timeout=90) as resp:
            raw=resp.read()
    assert sha(raw)==ZIP_SHA256,("ZIP_PIN_DRIFT",sha(raw))
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_bytes(raw)
    return raw

def unique(rows,key):
    result={}
    for row in rows:
        name=row[key]
        assert name not in result,("DUPLICATE_KEY",key,name)
        result[name]=row
    return result

def build(archive_file):
    baseline=pinned(BASE)
    previous=json.loads(pinned(PRIOR).decode("utf-8"))
    source=pinned(APPLICATIONS)
    prior_rows=read_csv(baseline)
    hdr=list(prior_rows[0])
    byid=unique(prior_rows,"target_id")
    orig=read_csv(source)
    orig_by={}
    for row in orig:
        if row["case"] in CASES:orig_by.setdefault(row["case"],[]).append(row)
    assert len(prior_rows)==len(byid)==70
    assert previous["counts"]["F_targets_with_conditional_evidence"]==32
    assert previous["counts"]["F_targets_hold"]==38
    assert previous["counts"]["historic_case_exact_F2_mapped_now"]==26
    assert set(orig_by)==set(CASES)
    assert all(len(orig_by[k])==1 for k in CASES)
    assert all(byid[k]["final_disposition"].startswith("HOLD") for k in CASES)
    assert sha(source)=="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
    raw=download_if_missing(archive_file)
    assert sha(raw)==ZIP_SHA256,("ZIP_SHA_MISMATCH",sha(raw))
    cases={}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        assert len(names)==len(set(names)),("DUPLICATE_ZIP_MEMBERS",names)
        assert set(names)=={"manifest.json","client.log",*(k+".png" for k in CASES)}
        report=json.loads(z.read("manifest.json"))
        assert report["status"]=="SERVER_STATES_AND_F2_RECORDED"
        assert report["minecraft"]=="1.21.1"
        assert report["f_source_only"] is True
        assert report["f_target_case_ids"]==list(CASES)
        assert set(report["native_f2_sha256"])==set(CASES)
        assert set(report["server_states"])==set(CASES)
        assert set(report["source"]["representative_states"])==set(CASES)
        assert report["source"]["ledger_sha256"]==sha(source)
        assert sha(z.read("client.log"))==report["client_log_sha256"]
        assert set(OBS)==set(CASES)
        for case in CASES:
            old=orig_by[case][0]
            lineage=report["source"]["representative_states"][case]
            shot=z.read(case+".png")
            assert sha(shot)==report["native_f2_sha256"][case],("PNG_SOURCE_HASH_DRIFT",case)
            with Image.open(io.BytesIO(shot)) as im:
                im.load()
                assert im.format=="PNG" and im.size==(1024,684)
            actual=report["server_states"][case]["subject"]["exact"]
            assert actual is (case in EXACT),("UNEXPECTED_GAME_BLOCK_STATE",case,actual)
            assert lineage["cohort"]==old["cohort"]==byid[case]["cohort"]
            assert lineage["historical_selection_matches_release"] is True
            assert lineage["historical_model_geometry"]=={
                "elements":int(old["elements"]),"faces":int(old["faces"])}
            assert lineage["state"]==old["block"]+(
                "["+old["state"].replace(";",",")+"]" if old["state"] else "")
            expected_files={old[k+"_path"]:old[k+"_sha"] for k in ("state","model","provider")}
            assert set(lineage["source_files"])==set(expected_files)
            matched={}
            for k in ("state","model","provider"):
                p=old[k+"_path"]
                file=lineage["source_files"][p]
                assert file["historical_git_blob_sha1"]==old[k+"_sha"]
                assert not file.get("release_path_absent",False)
                matched[k]=file["git_blob_byte_match"]
            assert matched==RELEASE[lineage["cohort"]],("JAR_VERSION_BYTE_MISMATCH",case,matched)
            cases[case]={
                "cohort":old["cohort"],"original_block":old["block"],
                "original_properties":old["state"],"original_model_key":old["model"],
                "original_state_git_blob":old["state_sha"],
                "original_model_git_blob":old["model_sha"],
                "original_parent_git_blob":old["provider_sha"],
                "historical_elements":int(old["elements"]),"historical_faces":int(old["faces"]),
                "source_model_selector_matches_game_JAR":True,
                "research_release_state_model_parent_byte_equality":matched,
                "server_exact_requested_state":actual,
                "native_png_sha256":sha(shot),"image_size":[1024,684],
                "image_directly_opened_and_reviewed":True,
                "visual_observation_ko":OBS[case],
                "baked_UV_or_part_semantics_approved":False,
            }
    assert sum(v["historical_elements"] for v in cases.values())==60
    assert sum(v["historical_faces"] for v in cases.values())==293
    assert len(set(v["native_png_sha256"] for v in cases.values()))==5
    assert cases["S01"]["native_png_sha256"]==cases["S02"]["native_png_sha256"]
    assert cases["S33"]["native_png_sha256"]==cases["S34"]["native_png_sha256"]
    assert cases["S31"]["native_png_sha256"]!=cases["S32"]["native_png_sha256"]
    before={k:dict(v) for k,v in byid.items()}
    for row in prior_rows:
        cid=row["target_id"]
        if cid not in CASES:continue
        case=cases[cid]
        good=cid in EXACT
        row.update({
            "prior_f2_evidence_status":("REAL_CLIENT_EXACT_STATE_F2_SHA_AND_DIRECT_IMAGE_REVIEW"
                if good else "REAL_CLIENT_ATTEMPT_EXACT_STATE_FAILED_F2_NOT_ACCEPTED"),
            "image_artifact_ids":str(ARTIFACT),
            "image_run_ids":str(RUN),
            "image_files":ARCHIVE+":"+cid+".png",
            "image_sha256s":case["native_png_sha256"],
            "original_zip_sha256s":ZIP_SHA256,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":OBS[cid],
            "source_state_and_release_assessment":(
                "EXACT_SERVER_ORIGINAL_STATE_AND_MODEL_SELECTOR_MATCH"
                if good else "SOURCE_SELECTOR_MATCH_BUT_EXACT_SERVER_REQUESTED_STATE_NOT_PRESENT"),
            "final_disposition":(
                "CONDITIONAL_F4_EXACT_SERVER_STATE_AND_NATIVE_F2_SOURCE_MATCHED"
                if good else "HOLD_F4_REQUESTED_PROPERTY_STATE_NOT_PERSISTED_IN_REAL_GAME"),
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":(
                "단일 원형 상태는 서버·원본 모델·F2 대응 PASS; UV·부품 의미·상호작용·출처 권리 최종 승인 별도"
                if good else
                "블록 ID만 존재하고 정확 속성 일치 실패. 단독 배치의 속성 자동 교정 가능성을 조사하고 "
                "인접 배치 또는 조작 후 상태와 F2를 새 촬영해야 함"),
        })
    changed={k for k,r in unique(prior_rows,"target_id").items() if r!=before[k]}
    assert changed==set(CASES),("UNEXPECTED_HISTORY_MUTATION",changed)
    assert len(prior_rows)==70
    n_cond=sum(x["final_disposition"].startswith("CONDITIONAL") for x in prior_rows)
    n_hold=sum(x["final_disposition"].startswith("HOLD") for x in prior_rows)
    assert (n_cond,n_hold)==(37,33)
    hist=[x for x in prior_rows if x["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(hist)==62
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in hist)==31
    assert sum(x["final_disposition"].startswith("HOLD") for x in hist)==31
    risks=[x for x in prior_rows if x["target_kind"]=="RISK_SCENARIO"]
    assert len(risks)==8 and {x["target_id"] for x in risks if x["final_disposition"].startswith("HOLD")}=={"R06","R08"}
    queue=[x for x in prior_rows if x["final_disposition"].startswith("HOLD")]
    bycohort=Counter(x["cohort"] or "RISK" for x in queue)
    assert bycohort==Counter({"VANILLA":15,"AF":4,"HC":2,"MACAW":10,"RISK":2})
    assert all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in prior_rows)
    pending=[]
    for x in queue:
        group=x["cohort"] or "RISK"
        pending.append({
            "target_id":x["target_id"],"cohort":group,
            "minecraft_version":x["minecraft_version"],"category":x["category"],
            "source_block":x["block"],"original_faces":x["original_source_faces"],
            "hold_reason":x["final_disposition"],
            "next_batch":("F4_PROPERTY_NEIGHBOR_DIAGNOSTIC" if x["target_id"] in NOT_EXACT
                          else "MOD_MULTI_MODEL_OR_VERSION_DIFFERENCE" if group in ("AF","HC")
                          else "VANILLA_1_21_11" if group=="VANILLA"
                          else "MACAW_1_21_11" if group=="MACAW"
                          else "R06_WATER_TIME_OR_R08_VERSION_JARS"),
            "followup_requirement":x["additional_required_before_full_acceptance"],
        })
    exceptions=[
      {"case":"S02","paired_control":"S01",
       "requested_state":"tucked=true","server_state_exact":False,
       "image_equal_to_control":True,
       "image_sha256":cases["S02"]["native_png_sha256"],
       "disposition":"HOLD_SERVER_STATE_MISMATCH",
       "cause":"미확정: 단독 배치에서 상태가 유지되지 않음; 실제 속성값과 조작 조건 추가 검사 필요"},
      {"case":"S34","paired_control":"S33",
       "requested_state":"shape=inner_left","server_state_exact":False,
       "image_equal_to_control":True,
       "image_sha256":cases["S34"]["native_png_sha256"],
       "disposition":"HOLD_SERVER_STATE_MISMATCH",
       "cause":"미확정: 단독 배치에서 코너 상태가 유지되지 않음; 연결 배치와 실제 속성값 추가 검사 필요"},
    ]
    report={
        "schema":"MCFR_INT4_F4_REAL_F2_PARTIAL_ACCEPTANCE_AND_STATE_EXCEPTION/v1",
        "status":"PASS_7_REVIEWED_PNG_5_EXACT_STATE_2_HOLD_NOT_FULL_F_EXIT",
        "date_kst":"2026-11-22",
        "source_git_blob_sha1":PIN,
        "source_game_workflow_run":RUN,
        "source_game_workflow_url":f"https://github.com/{REPO}/actions/runs/{RUN}",
        "source_game_workflow_conclusion":"failure_due_to_STRICT_all_7_exact_state_gate",
        "source_artifact_id":ARTIFACT,
        "source_artifact_url":f"https://github.com/{REPO}/actions/runs/{RUN}/artifacts/{ARTIFACT}",
        "source_artifact_zip_sha256":ZIP_SHA256,
        "actual_game_client_ran":True,
        "new_game_client_ran_in_this_audit":False,
        "source_historical_1_5_elements":60,
        "source_historical_1_5_faces":293,
        "source_client_log_sha256":report["client_log_sha256"],
        "cases":cases,"exceptions":exceptions,
        "counts":{
          "fixed_F_target_units":70,
          "historic_1_5_cases":62,
          "new_original_F2_png_occurrences":7,
          "new_unique_original_png_sha":5,
          "new_game_exact_state_case_evidence":5,
          "new_game_inexact_state_case_holds":2,
          "historic_case_exact_F2_mapped_previous":26,
          "historic_case_exact_F2_mapped_now":31,
          "historic_case_exact_F2_missing":31,
          "conditional":37,"hold":33,"unconditional_accepted":0,
          "new_semantic_part_approvals":0,
          "new_training_redistribution_rights_approvals":0,
          "original_F2_png_committed_to_Git":0,
        },
        "hold_by_cohort":dict(sorted(bycohort.items())),
        "limits":[
          "Failure of strict original 7/7 CI run was real and remains visible; derived 5/7 status is a separate casewise evidence audit, not a retroactive change of CI outcome.",
          "Images S02/S34 exist but the corresponding exact requested original server states failed; do not mark as 1-5 game evidence completed.",
          "Original F2 screenshots and game logs opened from GitHub Actions archive; image bytes SHA verified, subjective visual review not machine-verifiable.",
          "AF 4.0.3 study Git files differ from actual 4.0.2 JAR even where model selector matches; HC 4.0.3 selected source byte match retained.",
          "Exact-world placement does not prove native interaction behavior, pixelwise baked UV, parts meaning, release intention or permissions.",
          "Original image/JAR assets are not redistributed through repository; Actions artifact retention may expire.",
          "G/H not started and F remains open; previous 70-target rows preserved except seven affected rows."
        ]
    }
    csv70=serialize_csv(prior_rows,hdr)
    qfields=["target_id","cohort","minecraft_version","category","source_block","original_faces","hold_reason","next_batch","followup_requirement"]
    csvq=serialize_csv(pending,qfields)
    exfields=["case","paired_control","requested_state","server_state_exact","image_equal_to_control","image_sha256","disposition","cause"]
    csvex=serialize_csv(exceptions,exfields)
    report["outputs"]={
      "f70":{"rows":70,"sha256":sha(csv70)},
      "pending":{"rows":33,"sha256":sha(csvq)},
      "exceptions":{"rows":2,"sha256":sha(csvex)}
    }
    md="\n".join([
      "# INT-4-F4 실제 Fabric F2 7개 원본 검증 및 2개 실패 예외 분리",
      "",
      "- 연구 기준: Minecraft 1.21.1 / AF, HC / 기존 1-5 원본 60요소·293면.",
      "- 실제 클라이언트에서 7개 네이티브 F2 캡처(해시 고유 5개). 7개 원본 모델 경로·SHA 및 릴리스 선택 확인.",
      "- **정확한 게임 서버 상태 일치 5개**: S01, S31, S32, S33, S47. 원본 F2 직접 열람·SHA 검수 후 조건부 재사용.",
      "- **정확한 상태 불일치 2개**: S02 tucked=true, S34 shape=inner_left. 단독 캡처에서는 S01/S33과 각각 F2 PNG가 완전히 동일하므로 정확 상태의 시각 증거로 수용 금지.",
      "- 엄격한 7/7 CI 최초 실행은 이 두 불일치 중 첫 S02에서 FAIL. 해당 실패를 삭제/수정하지 않았으며, 원본 아티팩트에서 사례별 재감사를 추가로 실행.",
      "- S02/S34의 실제 정규화 원인은 미확정. 인접 배치·속성 상태 프로브 및 조작 후 새 F2 필요.",
      "- 전체 고정 F 대상: 기존 조건부 32 + 신규 5 = **조건부 37 / 보류 33 / 무조건 승인 0**.",
      "- 역사 1-5 정확한 F2: **31/62**. 보류: 바닐라 15, AF 4, HC 2, Macaw 10, 위험 R06/R08 2.",
      "- 원본 PNG·모드 JAR는 Git에 복사하지 않고 링크·SHA·원장만 남김. INT-5 의미 및 INT-6 권한 신규 승인 0.",
      ""
    ]).encode("utf-8")
    return {
      I/"INT4_F4_70_TARGET_EVIDENCE_DISPOSITIONS_V4.csv":csv70,
      I/"INT4_F4_33_PENDING_EXACT_F2_TARGETS_V1.csv":csvq,
      I/"INT4_F4_TWO_REAL_SERVER_STATE_EXCEPTIONS_V1.csv":csvex,
      I/"INT4_F4_DIRECT_VISUAL_PARTIAL_ACCEPTANCE_SUMMARY_V1.json":serialize_json(report),
      I/"INT4_F4_REAL_CLIENT_REPORT_V1.md":md
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifact-dir",type=Path,default=Path("temporary-artifacts"))
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    archive=args.artifact_dir/ARCHIVE
    for path,raw in build(archive).items():
        out=ROOT/path
        if args.verify:
            assert out.exists() and out.read_bytes()==raw,("NONDETERMINISTIC_OUTPUT",str(path))
        else:
            out.parent.mkdir(parents=True,exist_ok=True)
            out.write_bytes(raw)
        print("VERIFIED" if args.verify else "CREATED",path,len(raw))
    print("PASS_ORIGINAL_ARTIFACT_5_EXACT_2_HOLD_70_37_33")

if __name__=="__main__":main()
