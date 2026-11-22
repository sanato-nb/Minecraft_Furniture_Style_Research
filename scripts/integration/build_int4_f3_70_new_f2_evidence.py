#!/usr/bin/env python3
"""INT-4-F3: update exact 70-case F2 ledger from seven real Fabric screenshots.

Source: original F2 image ZIP directly reopened and visually inspected
2026-11-22; case SHA values are checked against the real capture JSON's
original screenshots and server logs. The original image ZIP itself remains
a GitHub Actions retention-limited artifact, not committed to this repository.

Do not convert screenshots or historical 1-5 source model evidence into
game-wide F completion, part semantics, pixelwise UV causality or rights.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
BASE=I/"INT4_F2_70_TARGET_EVIDENCE_DISPOSITIONS_V2.csv"
RUNTIME=I/"INT4_F3_NEW7_ACTUAL_CLIENT_SOURCE_SUMMARY_V1.json"
PRIOR=I/"INT4_F2_4_DIRECT_IMAGE_VISUAL_AUDIT_V1.json"
PINS={
 BASE:"fa6b659e54e2343229de0a6943e45b59342977b9",
 RUNTIME:"b389ff860ecc0346e6e1dd143ea20d676fa259da",
 PRIOR:"25edf176560e54dc4457f7d201f0f4360a756518",
}
CASE_IDS=("S20","S21","S26","S27","S44","S45","S46")
RUN=45008591423
ARTIFACT=14748847662
ZIP_SHA256="5cadfa474d75de4d71078a2159008a6f52b6073e1e8a7ef8f3dcb51865f65ffa"
VISUAL={
 "S20":"나무 상자형 서랍이 보임. 열림=false인데 S21 열림=true와 F2 원본 이미지 바이트가 완전히 동일함; 실제 외형 차이는 입증하지 못함",
 "S21":"나무 상자형 서랍이 보임. 게임 서버 open=true 확인, 그러나 S20(open=false)과 동일한 PNG SHA; 열린 서랍의 시각적 차이 증명 불가",
 "S26":"상판과 짧은 지지다리처럼 보이는 목재 구조 확인. 원본 분류는 선반이지만 저장 기능이나 연결 형태를 영상만으로 승인하지 않음",
 "S27":"목재 상자형의 수평 줄무늬 상단 구조 확인. 선반의 사용 목적·충돌·연결형 동작은 승인하지 않음",
 "S44":"나무 다리 같은 받침과 흰색 테두리를 가진 작은 조명 형태가 보임. 발광·점등 효과 원인 추론 보류",
 "S45":"S44와 같은 계열의 작은 조명이 보이고 스크린샷 밝기가 다름. 점등 상태가 서버에서 확인되지만 인과적 광원 검증은 아님",
 "S46":"바닥에 가까운 낮은 긴 나무 상자와 패턴 상단이 보임. 식물·수납 역할은 화면만으로 승인 불가",
}
CASE_FIELDS=[
 "target_id","target_kind","cohort","minecraft_version","category","block",
 "original_source_applications","original_source_faces","original_acceptance_contract",
 "prior_f2_evidence_status","source_E_case_match","image_artifact_ids","image_run_ids",
 "image_files","image_sha256s","original_zip_sha256s","newly_reopened_original_png",
 "direct_visual_observation_this_turn","human_observation_text",
 "source_state_and_release_assessment","final_disposition",
 "runtime_evidence_accepted_as_full_F_PASS","additional_required_before_full_acceptance",
]
QUEUE_FIELDS=["target_id","cohort","minecraft_version","category","source_block",
              "original_faces","exact_F2_current_status","next_batch","priority"]
EX_FIELDS=["exception_id","affected_case_ids","expected_original_source","actual_F2_evidence",
           "interpretation","acceptance_disposition","followup"]
RELEASE_EXPECTED={"AF":{"state":False,"model":False,"provider":False},
                  "HC":{"state":True,"model":True,"provider":True}}


def git_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()


def pin(path):
    b=(ROOT/path).read_bytes()
    assert git_sha(b)==PINS[path],("SOURCE_BLOB_CHANGED",str(path),git_sha(b))
    return b


def orig_rows():
    return list(csv.DictReader(io.StringIO(pin(BASE).decode("utf-8"),newline="")))


def original_run():
    return json.loads(pin(RUNTIME).decode("utf-8"))


def previous_review():
    return json.loads(pin(PRIOR).decode("utf-8"))


def unique(table,key):
    d={}
    for x in table:
        k=x[key]
        assert k not in d,("DUPLICATE_TARGET",k)
        d[k]=x
    return d


def csv_data(table,fields):
    buf=io.StringIO(newline="")
    writer=csv.DictWriter(buf,fieldnames=fields,lineterminator="\n")
    writer.writeheader()
    writer.writerows(table)
    return buf.getvalue().encode("utf-8")


def json_data(value):
    return (json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode("utf-8")


def run_audit():
    base=orig_rows()
    runtime=original_run()
    prev=previous_review()
    assert len(base)==70 and len(unique(base,"target_id"))==70
    assert runtime["status"]=="PASS_EXACT_SEVEN_ORIGINAL_MOD_CASE_SERVER_F2_SHA_NOT_SEMANTIC_RENDER_EXIT"
    assert runtime["cases"]==list(CASE_IDS)
    assert runtime["native_f2_png_count"]==7
    assert (runtime["original_research_case_model_elements"],
            runtime["original_research_case_model_faces"])==(30,144)
    assert runtime["minecraft"]=="1.21.1"
    assert runtime["evidence_limits"]["actual_games_7_cases_tested"] is True
    assert runtime["evidence_limits"]["human_visual_approval_automated"] is False
    assert runtime["evidence_limits"]["original_case_F2_proves_pixelwise_UV_equivalence"] is False
    assert runtime["evidence_limits"]["int5_semantic_approvals"]==0
    assert runtime["evidence_limits"]["int6_training_redistribution_rights_approved"]==0
    assert prev["reconciled_counts"]["conditional_targets"]==25
    assert prev["reconciled_counts"]["hold_targets"]==45
    assert prev["reconciled_counts"]["exact_hist_source_case_F2_after"]==19
    assert set(prev["reconciled_counts"]["risk_hold_ids"])=={"R06","R08"}
    assert set(runtime["source_files_by_case"])==set(CASE_IDS)
    assert set(VISUAL)==set(CASE_IDS)
    raw_shas=[runtime["source_files_by_case"][x]["native_f2_sha256"] for x in CASE_IDS]
    assert len(set(raw_shas))==6,("F2_UNIQUE_SCREENSHOT_COUNT",len(set(raw_shas)))
    assert raw_shas[0]==raw_shas[1],("DRAWER_STATE_SCREENSHOT_SHA_DISTINCT_FROM_OBSERVATION")
    assert len(set(raw_shas[2:]))==5
    assert raw_shas[4]!=raw_shas[5],("LAMP_IMAGES_UNEXPECTEDLY_IDENTICAL")
    snapshots={}
    for case in CASE_IDS:
        item=runtime["source_files_by_case"][case]
        assert item["case"]==case
        assert item["minecraft_version"]=="1.21.1"
        assert item["server_exact_state_readback"] is True
        assert item["original_source_model_selection_equals_release"] is True
        assert item["native_f2_dimensions"]==[1024,684]
        assert item["actual_baked_UV_or_screenshot_to_source_causal_approval"] is False
        assert len(item["native_f2_sha256"])==64
        assert item["cohort"] in ("AF","HC")
        assert item["pinned_release_file_equality"]==RELEASE_EXPECTED[item["cohort"]],(
            "JAR_VS_GIT_BYTE_EQ_UNEXPECTED",case)
        snapshots[case]={
            "case":case,
            "cohort":item["cohort"],
            "minecraft":"1.21.1",
            "original_exact_block_state":item["block_and_exact_state"],
            "original_model_key":item["original_model_key"],
            "original_state_sha1":item["original_blockstate_git_blob_sha1"],
            "original_model_sha1":item["original_model_git_blob_sha1"],
            "original_provider_sha1":item["original_provider_git_blob_sha1"],
            "original_game_native_f2_png_sha256":item["native_f2_sha256"],
            "visible_image_reopened_at_original_resolution":"true",
            "direct_visual_observation_KO":VISUAL[case],
            "server_readback_exact":"PASS",
            "model_selection_matches_release":"PASS",
            "research_model_state_provider_bytes_equal_release":item["pinned_release_file_equality"],
            "baked_uv_or_semantic_approved":"false",
            "licensing_approved":"false",
        }

    old={x["target_id"]:dict(x) for x in base}
    for row in base:
        case=row["target_id"]
        if case not in CASE_IDS:
            continue
        original=runtime["source_files_by_case"][case]
        assert row["final_disposition"].startswith("HOLD"),("PREVIOUSLY_NOT_HOLD",case)
        assert row["target_kind"]=="HISTORICAL_1_5_CASE"
        assert (row["cohort"],row["minecraft_version"])==(original["cohort"],"1.21.1")
        assert row["image_sha256s"]==""
        row.update({
            "prior_f2_evidence_status":"NEW_ACTUAL_FABRIC_EXACT_F2_PNG_SHA_AND_MANUAL_IMAGE_REVIEW_20261122",
            "image_artifact_ids":str(ARTIFACT),
            "image_run_ids":str(RUN),
            "image_files":f"int4-f3-seven-original-native-f2.zip:{case}.png",
            "image_sha256s":original["native_f2_sha256"],
            "original_zip_sha256s":ZIP_SHA256,
            "newly_reopened_original_png":"true",
            "direct_visual_observation_this_turn":"true",
            "human_observation_text":VISUAL[case],
            "source_state_and_release_assessment":(
                "AF_4_0_3_RESEARCH_GIT_TO_4_0_2_RELEASE_SOURCE_BYTES_DIFFER_MODEL_SELECTOR_MATCHES"
                if row["cohort"]=="AF"
                else "HC_4_0_3_SOURCE_STATE_MODEL_PROVIDER_GIT_BYTES_EQUAL_RELEASE"),
            "final_disposition":(
                "CONDITIONAL_F3_TWO_DISTINCT_DRAWER_STATES_SAME_F2_PNG_VISUAL_DIFFERENCE_UNPROVEN"
                if case in ("S20","S21")
                else "CONDITIONAL_F3_EXACT_GAME_F2_VISIBLE_NOT_FINAL_F_STAGE_EXIT"),
            "runtime_evidence_accepted_as_full_F_PASS":"false",
            "additional_required_before_full_acceptance":(
                "S20/S21 서버 open 속성은 서로 다르지만 PNG는 원본 바이트가 동일. "
                "화면 상태 차이·정확한 JAR 렌더 선택 결과·여닫기 조작·UV/의도 재검증 필수"
                if case in ("S20","S21")
                else "원본 모델 선택·서버 상태·실제 F2 대응 PASS. "
                "UV/광원/충돌·의미와 배포본/저작권 수용은 추가 검증 필요"),
        })
    diff={k for k,v in unique(base,"target_id").items() if v!=old[k]}
    assert diff==set(CASE_IDS),("ACCIDENTAL_PRIOR_EVIDENCE_DRIFT",sorted(diff))
    assert [x["target_id"] for x in base]==list(old)
    state_disposition=Counter(
        "CONDITIONAL" if x["final_disposition"].startswith("CONDITIONAL")
        else "HOLD" if x["final_disposition"].startswith("HOLD")
        else "OTHER" for x in base)
    assert state_disposition=={"CONDITIONAL":32,"HOLD":38},state_disposition
    hist=[x for x in base if x["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(hist)==62
    assert sum(x["final_disposition"].startswith("CONDITIONAL") for x in hist)==26
    assert sum(x["final_disposition"].startswith("HOLD") for x in hist)==36
    risk=[x for x in base if x["target_kind"]=="RISK_SCENARIO"]
    assert len(risk)==8
    assert {x["target_id"] for x in risk if x["final_disposition"].startswith("HOLD")}=={"R06","R08"}
    assert all(x["runtime_evidence_accepted_as_full_F_PASS"]=="false" for x in base)

    pending=[x for x in base if x["final_disposition"].startswith("HOLD")]
    by_cohort=Counter(x["cohort"] or "RISK" for x in pending)
    assert by_cohort==Counter({"VANILLA":15,"AF":7,"HC":4,"MACAW":10,"RISK":2}),by_cohort
    queue=[]
    for x in pending:
        kind=x["cohort"]
        queue.append({
            "target_id":x["target_id"],
            "cohort":kind or "RISK",
            "minecraft_version":x["minecraft_version"],
            "category":x["category"],
            "source_block":x["block"],
            "original_faces":x["original_source_faces"],
            "exact_F2_current_status":x["final_disposition"],
            "next_batch":("VANILLA_1_21_11" if kind=="VANILLA" else
                "MACAW_1_21_11" if kind=="MACAW" else
                "MOD_1_21_1" if kind in ("AF","HC") else
                "WATER_TWO_TIMED_F2" if x["target_id"]=="R06" else
                "AF_DUAL_RELEASE_F2"),
            "priority":("P0_RISK" if x["target_id"] in ("R06","R08") else
                "P1_CHANGING_CONNECTED_STATE" if x["target_id"] in ("S01","S02","S03","S04") else
                "P1_VANILLA_SPECIAL_RENDER" if x["target_id"]=="V11" else
                "P2_ORIGINAL_CASE_STATE"),
        })
    assert len(queue)==38 and len(unique(queue,"target_id"))==38

    exceptions=[
        {
            "exception_id":"EX01_DRAWER_OPEN_FALSE_TRUE_SAME_F2_SHA",
            "affected_case_ids":"S20|S21",
            "expected_original_source":"Distinct static source model keys AF491/AF492 and open=false vs open=true",
            "actual_F2_evidence":f"Both original 1024x684 F2 PNGs are byte-identical; sha256 {raw_shas[0]}; server exact states separately verified",
            "interpretation":"Exact target images captured, but visual change between the states is NOT established",
            "acceptance_disposition":"CONDITIONAL_NO_VISUAL_DIFFERENCE_APPROVED",
            "followup":"Reconfirm render selection from actual AF 4.0.2 JAR and capture before/after player interaction at same camera",
        },
        {
            "exception_id":"EX02_ANOTHER_FURNITURE_RELEASE_SOURCE_BYTE_DIFFERENCE",
            "affected_case_ids":"S20|S21|S26|S44|S45|S46",
            "expected_original_source":"Research Git 4.0.3 state/model/provider SHA",
            "actual_F2_evidence":"Fabric AF 4.0.2 selected same path/rule/model but all three file byte comparisons differ from research Git",
            "interpretation":"Source selector equivalence is not byte-equivalence, not version-wide release approval",
            "acceptance_disposition":"CONDITIONAL_RELEASE_SOURCE_DIFFERENCE",
            "followup":"Retain per-file release SHA and compare exact change per model, not whole-mod generalization",
        },
        {
            "exception_id":"EX03_LAMP_LIT_DIFF_NOT_FULL_LIGHTING_PROOF",
            "affected_case_ids":"S44|S45",
            "expected_original_source":"lit=false and lit=true distinct exact server states with distinct model source",
            "actual_F2_evidence":f"Distinct original PNG hashes: {raw_shas[4]} vs {raw_shas[5]}",
            "interpretation":"Visible frame difference is real, but emitted lighting physics, dynamic behavior and pixel causal source remain unproven",
            "acceptance_disposition":"CONDITIONAL_LIGHTING_INFERENCE_HOLD",
            "followup":"Controlled fixed camera/lighting and time experiments, compare face UV and light-level outcomes",
        },
    ]
    assert len(exceptions)==3
    raw_old=csv_data(base,CASE_FIELDS)
    raw_queue=csv_data(queue,QUEUE_FIELDS)
    raw_ex=csv_data(exceptions,EX_FIELDS)
    report={
        "schema":"MCFR_INT4_F3_70_TARGETS_7_NEW_REAL_FABRIC_F2_SOURCE_RECONCILIATION/v1",
        "status":"PASS_7_NEW_NATIVE_F2_REAL_GAME_SOURCE_AUDIT_70_TARGETS_NOT_FULL_F_EXIT",
        "base_draft_pr":59,
        "base_prior_evidence_git_blob_sha1":{str(k):v for k,v in PINS.items()},
        "source_Github_Actions_run":RUN,
        "source_Github_Actions_run_url":f"https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/{RUN}",
        "source_Github_Actions_artifact_id":ARTIFACT,
        "source_Github_Actions_artifact_zip_sha256":ZIP_SHA256,
        "source_runtime_client_log_sha256":runtime["client_log_sha256"],
        "cases":snapshots,
        "counts":{
            "pinned_1_5_cases":62,
            "fixed_f_targets":70,
            "new_case_original_server_F2":7,
            "new_case_png_occurrences":7,
            "new_case_distinct_png_sha":len(set(raw_shas)),
            "new_case_artifact_verified_sha":7,
            "new_F2_human_observed_original_images":7,
            "original_research_elements_new":30,
            "original_research_faces_new":144,
            "historic_case_exact_F2_mapped_before":19,
            "historic_case_exact_F2_mapped_now":26,
            "historic_case_not_yet_exact_F2_mapped":36,
            "F_targets_with_conditional_evidence":32,
            "F_targets_hold":38,
            "F_targets_unconditionally_accepted":0,
            "source_release_bytes_different_cases":6,
            "source_release_bytes_identical_cases":1,
            "different_source_state_same_F2_png_case_pairs":1,
            "drawers_same_png_unique_case_count":2,
            "R06_R08_remaining_hold":2,
            "new_game_sessions_executed":1,
            "new_AI_part_semantics_approved":0,
            "new_original_asset_AI_training_or_redistribution_rights_approved":0,
            "new_original_game_PNG_committed_to_Git":0,
        },
        "remaining_hold_by_cohort":dict(sorted(by_cohort.items())),
        "known_exceptions":[x["exception_id"] for x in exceptions],
        "boundaries":[
            "Actual Minecraft Fabric client was newly launched and seven server readback states were recorded with seven original PNGs.",
            "S20 and S21 are distinct original server states but same PNG hash; no opening animation or visually distinct drawer model was demonstrated.",
            "AF 4.0.3 research original Git state/model/provider bytes do not match 4.0.2 Fabric JAR; selected model rule equality is narrower.",
            "S27 Handcrafted 4.0.3 state/model/provider source byte SHA matches original Git source.",
            "No block functionality, part meaning, baked pixelwise UV, light causation or user item interaction is approved.",
            "All 70 targets remain conditional or HOLD, 0 final accepted. R06/R08 remain HOLD.",
            "Original ZIP/PNG is retained as a temporary Github Actions artifact only; hashes and visual observation text in repository.",
        ],
        "progress":{
            "F_70_target_disposition_documented":{"numerator":70,"denominator":70},
            "F_62_original_study_exact_F2_evidence_mapped":{"numerator":26,"denominator":62},
            "F_70_conditional_evidence":{"numerator":32,"denominator":70},
            "F_70_final_unconditional_acceptance":{"numerator":0,"denominator":70},
            "F_full_exit":"BLOCKED_38_HOLD_AND_32_CONDITIONAL_NOT_FULL_ACCEPTED",
            "G_and_H_independent_final_audit":"NOT_STARTED",
        },
        "outputs":{
            "target_v3":{"rows":len(base),"sha256":hashlib.sha256(raw_old).hexdigest()},
            "pending_38":{"rows":len(queue),"sha256":hashlib.sha256(raw_queue).hexdigest()},
            "exceptions_3":{"rows":len(exceptions),"sha256":hashlib.sha256(raw_ex).hexdigest()},
        },
    }
    raw_summary=json_data(report)
    md="\n".join([
        "# INT-4-F3 — 원본 모드 7개 실게임 F2 직접 검수 및 70개 판정 재정합",
        "",
        "- 실제 Fabric Minecraft 1.21.1 CI 실행: S20/S21/S26/S27/S44/S45/S46 **7개 모두 원본 서버 블록 상태·선택 모델·원본 F2 PNG SHA 검수 성공**.",
        "- 새 네이티브 F2 원본 이미지: 7발생/고유해시 6; GIF/합성 이미지가 아닌 원본 1024×684 F2를 직접 육안 확인.",
        "- 연구 원본 1-5-B의 30요소·144면 일치. 기존 역사 자료는 수정하지 않음.",
        "- **중요 반례:** S20 \`open=false\` / S21 \`open=true\` 서로 다른 모델 키와 서버 상태를 갖지만 두 실제 F2는 PNG SHA까지 완전히 동일함. '서랍 열림 외형 입증'으로 승격하지 않음.",
        "- AF 6건은 연구 Git 4.0.3과 실제 실행 JAR 4.0.2의 원본 JSON 바이트가 다르며 선택 규칙만 맞음. HC S27은 연구/릴리스 state/model/provider 바이트 동일.",
        "- S44/S45 조명은 원본 F2 차이가 있지만 광원 인과·시간 변화·UV 검증 아님.",
        "- 전체 고정 분모 70: 기존 조건부 25+신규 7=**조건부 32, HOLD 38, 최종 수용 0**. 역사 사례 F2 26/62, 나머지 36 미매핑.",
        "- HOLD 38: 바닐라 15, AF 7, HC 4, Macaw 10, 위험 R06/R08 2.",
        "- 원본 캡처 ZIP/PNG는 Actions 보관기한 제한. Git에는 source SHA·사진 관찰·조건부 검증 기록만 커밋.",
        "- INT-4-F 전체 종료 및 INT-4-G/H 최종 승인 **보류**. INT-5 의미/INT-6 권리 승인 **0 유지**.",
        "",
        "## 산출 파일",
        "- \`INT4_F3_70_TARGET_EVIDENCE_DISPOSITIONS_V3.csv\` : 수정 사례 7개 외 기존 증거 원장 그대로",
        "- \`INT4_F3_38_PENDING_EXACT_F2_CASES_V1.csv\` : 남은 보류 사례·우선순위",
        "- \`INT4_F3_3_RENDER_SOURCE_EXCEPTIONS_V1.csv\` : 동일 이미지, AF 릴리스 차이, 조명 인과 미확정",
        "- \`INT4_F3_7_DIRECT_IMAGE_VISUAL_AUDIT_V1.json\` : 원본 상태별 해시·그림 관찰·수용 제한",
        "- \`INT4_F3_SOURCE_REPORT_V1.md\` : 경계 보고",
        "",
    ]).encode("utf-8")
    return {
        I/"INT4_F3_70_TARGET_EVIDENCE_DISPOSITIONS_V3.csv":raw_old,
        I/"INT4_F3_38_PENDING_EXACT_F2_CASES_V1.csv":raw_queue,
        I/"INT4_F3_3_RENDER_SOURCE_EXCEPTIONS_V1.csv":raw_ex,
        I/"INT4_F3_7_DIRECT_IMAGE_VISUAL_AUDIT_V1.json":raw_summary,
        I/"INT4_F3_SOURCE_REPORT_V1.md":md,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    for filename,raw in run_audit().items():
        path=ROOT/filename
        if a.verify:
            assert path.exists() and path.read_bytes()==raw,("BYTE_NONDETERMINISM",str(filename))
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(raw)
        print("VERIFIED" if a.verify else "CREATED",filename,len(raw))
    print("PASS F3 source evidence cross-reconciliation 70=32 conditional+38 HOLD, accepted=0")


if __name__=="__main__":
    main()
