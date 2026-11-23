#!/usr/bin/env python3
"""INT-4-G1 independent cross-layer A-F source coverage and exception audit.

G1 ONLY establishes the frozen source/report scope and explicit evidence
handoff; it does NOT run a game, review 592k UV pixels or approve a final G/H
exit. Keep unrelated denominator populations and historical source SHA separate.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv,gzip,hashlib,io,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PINS={
 "INT4_A_ADJUDICATION_SUMMARY_V2.json":"621cce07862bbc5bb051809eeeef8df9607c0a37",
 "INT4_A_EXCEPTION_DISPOSITIONS_V2.csv":"26c5764a37700626f3bfadba01fc229e49aadfc4",
 "INT4_B_SOURCE_JOIN_SUMMARY_V1.json":"93c07092f683aaaacdb5b3e22c2754376439ca88",
 "INT4_C_SOURCE_AUDIT_V1.json":"ace40f7aab319f61dc4d614f52aa01cae12f6cc0",
 "INT4_D_SOURCE_AUDIT_V1.json":"7617caf488ef2fd2a115c3ae1f3f7350fe1ba8d8",
 "INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv":"75d61821a732ddec271314396e6c11335f40d4c3",
 "INT4_E_CROSS_AUDIT_SUMMARY_V1.json":"6483b0fbd14d2b389a311a73201c1b160956f5c1",
 "INT4_E_21_FINDING_DISPOSITIONS_V1.csv":"ff3025ffc9d924cc00b7d58cf05212b6dc5e08da",
 "INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json":"dbf5118138851f664468e5bcb8ef84e1edde6fd5",
 "INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv":"0cfbf3b1b174efc968de35c8466e2af8a9cd41c7",
}
GZIP={
 "INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":("9bf1dc45cca4d85d4bf7ebdc60755910801adf1664b94ee38b28eb9082e3aeb3",16572),
 "INT4_B_592312_FACE_PROVENANCE_V1.csv.gz":("d5fe7708a194db723b49d4dbfe8bfd256a9c1bfbd00001d1ed17e1f9d760c578",592312),
 "INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz":("1bd4b9a670eb05a34be93d2569d22519f06463d8d52de3cf560859e68c6517cc",6343),
 "INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz":("d8a007500262cee3e7ae2e24f1891ed640f2eac33cff6cd779a0352ece191301",78456),
}
REPORT=I/"INT4_G1_SOURCE_LAYER_GATE_SUMMARY_V1.json"
FINDINGS=I/"INT4_G1_21_FINDING_CASE_F2_GATES_V1.csv"
AEXCEPT=I/"INT4_G1_112_MODEL_EXCEPTION_REVIEW_QUEUE_V1.csv"
DEXCEPT=I/"INT4_G1_6_BLOCKSTATE_EXCEPTION_REVIEW_QUEUE_V1.csv"
DOC=I/"INT4_G1_SOURCE_SCOPE_PRELIMINARY_REPORT_V1.md"

def digest(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def blob(name):
    b=(ROOT/I/name).read_bytes()
    assert gitblob(b)==PINS[name],("ORIGINAL_SHA_DRIFT",name,gitblob(b))
    return b
def jsonin(name):return json.loads(blob(name))
def readcsv(name):
    return list(csv.DictReader(io.StringIO(blob(name).decode("utf-8-sig"),newline="")))
def csvbytes(records,fields):
    out=io.StringIO(newline="")
    w=csv.DictWriter(out,fieldnames=fields,lineterminator="\n")
    w.writeheader();w.writerows(records)
    return out.getvalue().encode("utf-8")
def jsonbytes(doc):return (json.dumps(doc,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
def read_gz():
    result={}
    for name,(sha,count) in GZIP.items():
        b=(ROOT/I/name).read_bytes()
        assert digest(b)==sha,("GZIP_ORIGINAL_SHA_DRIFT",name)
        with gzip.GzipFile(fileobj=io.BytesIO(b)) as file:
            reader=csv.DictReader(io.TextIOWrapper(file,encoding="utf-8-sig",newline=""))
            headers=reader.fieldnames
            assert headers and len(headers)==len(set(headers)),name
            actual=sum(1 for row in reader if None not in row)
        assert actual==count,("GZIP_SOURCE_ROW_COUNT",name,actual)
        result[name]={"rows":actual,"gzip_sha256":sha,"csv_columns":headers,
                      "source_scope":"PRIOR_PINNED_SOURCE_ONLY_NOT_NEW_ORIGINAL_UPSTREAM"}
    return result

def build():
    compressed=read_gz()
    A=jsonin("INT4_A_ADJUDICATION_SUMMARY_V2.json")
    B=jsonin("INT4_B_SOURCE_JOIN_SUMMARY_V1.json")
    C=jsonin("INT4_C_SOURCE_AUDIT_V1.json")
    D=jsonin("INT4_D_SOURCE_AUDIT_V1.json")
    E=jsonin("INT4_E_CROSS_AUDIT_SUMMARY_V1.json")
    F=jsonin("INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
    aexceptions=readcsv("INT4_A_EXCEPTION_DISPOSITIONS_V2.csv")
    dexceptions=readcsv("INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv")
    findings=readcsv("INT4_E_21_FINDING_DISPOSITIONS_V1.csv")
    f70=readcsv("INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv")
    assert len(aexceptions)==112 and len(dexceptions)==6
    assert len(findings)==21 and len(f70)==70
    assert len({r["model_key"] for r in aexceptions})==112
    assert len({r["finding_id"] for r in findings})==21
    assert len({r["target_id"] for r in f70})==70
    assert A["all_model_source_paths"]==16572
    acount=A["review_results"]
    assert acount=={"CONDITIONAL_STATIC_SOURCE_EXCEPTION":48,
                   "HOLD_MODEL_USAGE_AND_RENDER_PATH":6,
                   "NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY":58,
                   "VERIFIED_REUSED_STATIC_SCOPE":16460}
    assert sum(acount.values())==16572
    assert A["source_parent_missing_remains"]==48 and A["static_geometry_na_generated_items"]==58
    assert A["history_static_reachability_unreachable_48"]==48
    assert A["exception_rows"]==112
    assert B["expanded_element_instances"]==105383 and B["expanded_face_instances"]==592312
    assert B["face_uv_declared"]+B["face_uv_implicit"]==592312
    assert C["face_total"]==592312 and C["face_pixel_support_from_original_historic_check"]==585969
    assert C["face_without_own_pixel_support"]==6343
    assert sum(C["face_exception_reason_counts"].values())==6343
    assert C["model_slot_records"]==81641 and C["model_face_texture_registry"]==2256
    assert D["state_denominator"]==1158 and D["option_rows"]==78456
    assert D["original_reference_status_counts"]=={"LOCAL":78420,"UNRESOLVED_MODEL_REF":4,"VANILLA_JAR":32}
    assert sum(D["state_source_dispositions"].values())==1158
    assert E["counts"]["case_records_joined"]==62
    assert E["counts"]["model_application_records_joined"]==74
    assert E["counts"]["finding_source_rows"]==21
    assert E["counts"]["original_input_discrepancy_rows"]==0
    assert E["counts"]["historical_handoff_disposition_counts"]=={
        "CANDIDATE_REQUIRES_REVIEW":14,"SCOPE_LIMIT_ONLY":7}
    assert F["counts"]["F_targets"]==70 and F["counts"]["F_conditional_after"]==70
    assert F["counts"]["F_HOLD_after"]==F["counts"]["F_unconditional_final_approvals"]==0
    assert sum(r["target_kind"]=="HISTORICAL_1_5_CASE" for r in f70)==62
    assert all(r["final_disposition"].startswith("CONDITIONAL") and
               r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in f70)
    fc={r["target_id"]:r for r in f70}
    finding_rows=[]
    for r in findings:
        cases=r["source_case_keys"].split("|")
        assert len(cases)==int(r["source_case_count"]) and len(set(cases))==len(cases)
        assert set(cases)<=set(fc),("FINDING_REF_ABSENT_IN_F70",r["finding_id"])
        assert all(fc[c]["target_kind"]=="HISTORICAL_1_5_CASE" for c in cases)
        assert all(fc[c]["image_sha256s"] and fc[c]["image_run_ids"] and fc[c]["image_artifact_ids"] for c in cases)
        assert all(fc[c]["final_disposition"].startswith("CONDITIONAL") for c in cases)
        assert r["original_INT2_check_status"]=="PASS"
        assert r["case_keys_integrity"]=="PASS_EXACT_HISTORICAL_CASE_IDS"
        assert r["int5_semantic_approved"]==r["int6_rights_approved"]=="false"
        assert r["universal_modeling_rule_approved"]=="false"
        gate=("HISTORICAL_SCOPE_LIMIT_ONLY" if r["original_INT2_disposition"]=="SCOPE_LIMIT_ONLY"
              else "RESEARCH_CANDIDATE_NEEDS_INDEPENDENT_PART_UV_SEMANTIC_REVIEW")
        finding_rows.append({
            "finding_id":r["finding_id"],
            "category":r["category"],
            "classification":r["classification"],
            "axis":r["axis"],
            "original_1_5_case_ids":"|".join(cases),
            "referenced_case_count":len(cases),
            "F_referenced_case_conditionally_evidenced_count":len(cases),
            "source_case_Sha_linkage":r["case_source_SHA_linkage"],
            "historical_E_disposition":r["original_INT2_disposition"],
            "G1_source_to_F_gate":"ALL_REFERENCED_CASES_HAS_CONDITIONAL_F2_NOT_FULL_F_EXIT",
            "G1_research_disposition":gate,
            "any_semantic_or_training_approval":False,
            "required_followup":r["followup"],
        })
    assert Counter(x["G1_research_disposition"] for x in finding_rows)=={
        "RESEARCH_CANDIDATE_NEEDS_INDEPENDENT_PART_UV_SEMANTIC_REVIEW":14,
        "HISTORICAL_SCOPE_LIMIT_ONLY":7}
    a_rows=[]
    for r in aexceptions:
        review=r["int4_a_review_result"]
        assert review in acount
        a_rows.append({
            "model_key":r["model_key"],"mod":r["mod"],"minecraft":r["minecraft"],
            "resource_id":r["resource_id"],
            "original_source_path":r["source_path"],
            "original_source_SHA":r["source_sha"],
            "exception_class":r["exception_class"],
            "parent_status":r["parent_status"],
            "geometry_status":r["geometry_status"],
            "A_review_disposition":review,
            "G1_conditional_evidence_gate":"STATIC_EXCEPTION_SCOPE_RECORDED_NOT_RUNTIME_SELECTED_OR_SEMANTIC_FULL_EXIT",
            "original_static_reachability":r["static_blockstate_item_reachability"],
            "required_followup_stage":r["required_followup_stage"],
            "followup":r["next_action"],
            "source_license_or_semantic_approved":False,
        })
    assert Counter(r["A_review_disposition"] for r in a_rows)=={
      "CONDITIONAL_STATIC_SOURCE_EXCEPTION":48,
      "HOLD_MODEL_USAGE_AND_RENDER_PATH":6,
      "NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY":58}
    d_rows=[]
    for r in dexceptions:
        assert r["runtime_defect_proven"]=="false"
        assert r["original_json_modified"]=="false"
        d_rows.append({
           "mod":r["mod"],"state_id":r["state_id"],
           "state_source_SHA":r["state_source_sha"],
           "source_selector":r["source_selector"],
           "model_key":r["model_key"],"exception_type":r["exception_type"],
           "historic_disposition":r["disposition"],
           "G1_disposition":"STATIC_SOURCE_ANOMALY_NOT_REAL_GAME_BUG_PROVEN",
           "required_followup":r["followup"],
        })
    # The full 592312 faces, 16572 models, 78456 D options are read from
    # ORIGINAL compressed ledgers and counted. They are NOT independently
    # marked as UV/display/semantically VERIFIED just because they have rows.
    baselines={
       "A":{"model_denominator":16572,"model_static_scope_verified":16460,
            "parent_missing_conditional":48,"model_use_hold":6,"generated_item_NA":58},
       "B":{"face_denominator":592312,"element_denominator":105383,
            "reused_source_face_links":592312,"live_baked_UV_approved":0},
       "C":{"face_denominator":592312,"historic_PNG_pixel_supported":585969,
            "source_PNG_pixel_exceptions":6343,
            "source_PNG_exception_reason_counts":C["face_exception_reason_counts"]},
       "D":{"mod_state_paths":1158,"source_option_rows":78456,
            "unresolved_option_refs":4,"not_claimed_runtime_resolved":True},
       "E":{"historic_cases":62,"model_applications":74,
            "finding_disposition_rows":21,
            "claim_candidates_conditional":14,"counterexamples_or_scope_limit":7,
            "source_discrepancies":0},
       "F":{"verification_units":70,"historical_cases":62,"risk_scenarios":8,
            "with_conditional_real_client_or_source_evidence":70,
            "unconditionally_final_F_pass":0},
    }
    rawfindings=csvbytes(finding_rows,list(finding_rows[0]))
    rawa=csvbytes(a_rows,list(a_rows[0]))
    rawd=csvbytes(d_rows,list(d_rows[0]))
    report={
        "schema":"MCFR_INT4_G1_SOURCE_LAYERS_A_TO_F_PRELIMINARY_DECISION_GATES/v1",
        "status":"PASS_G1_ALL_FROZEN_SOURCE_SCOPE_AND_F70_CROSS_LINKED_G_FINAL_EXIT_NOT_ASSESSED",
        "frozen_Git_blob_SHA1":PINS,
        "frozen_compressed_ledgers":compressed,
        "fixed_layer_denominators_and_scoped_dispositions":baselines,
        "source_disposition_counts":{
            "A_parent_missing_also_no_static_overlap":44,
            "A_missing_parents":48,
            "A_no_static":108,
            "A_exception_union_distinct_models":112,
            "C_face_pixel_exception_categories_total":6343,
            "D_option_exceptions":6,
            "E_findings_referenced_distinct_cases":E["counts"]["distinct_cases_referenced_by_findings"],
        },
        "findings_gate_total":21,
        "finding_scope_restriction":{
            "all_finding_cases_conditionally_evidenced":True,
            "findings_universally_approved":0,
            "finding_claims_reclassified_as_verified_new_G":0},
        "G_stage_final_disposition_approved":0,
        "H_exit_gate_approved":0,
        "INT5_semantics_approved":0,
        "INT6_AI_training_and_redistribution_approved":0,
        "uncertainties_and_explicit_non_acceptance":[
            "A parent missing 48 are pinned static ancestry unreachable; dynamic loader and resource pack usage not proven.",
            "A six HC base models lack effective cuboids and have unresolved registered-state use.",
            "A 58 generated item models are N/A static cuboids, not an observed renderer defect.",
            "B source 592312 faces are structural provenance, NOT pixel-baked live UV verification.",
            "C 6343 unsupported pixel-source faces include child slots, missing PNG and nonintersection; not all game visible.",
            "D 78456 rule options are static source choices; 4 unresolved refs, no version-wide registered runtime equality claim.",
            "E 21 conclusions remain 14 conditional candidates and 7 scope limits; no universal style rules automatically.",
            "F 70/70 conditional evidence does not establish all original acceptance contracts or full F exit.",
            "Official Another Furniture 4.0.3 NeoForge release NOT game tested by F11F; Git 4.0.3 Fabric self-build one state only.",
            "Original 2026 INT-2/3 CI environment regressions fixed in Draft PR73, but unrelated chair UI capture failures remain.",
            "G independent disposition needs source exception ownership, version scope, selected render applicability, conflict triage; H gates not started.",
        ],
        "outputs_sha256":{
            "finding_gates":digest(rawfindings),
            "A_exception_review":digest(rawa),
            "D_option_exception_review":digest(rawd),
        },
    }
    rawsummary=jsonbytes(report)
    lines=[
       "# INT-4-G1 A~F 고정 원본 출처·예외·F2 연결 증거 감사",
       "",
       "이 작업은 **G 단계의 첫 번째 출처/범위 검사**이며 16,572개 모델, 592,312면, 70개 F, 21개 발견을 곧바로 VERIFIED로 승격하지 않습니다.",
       "",
       "| 분모 | 기초 출처 재검증 및 분류 |",
       "|---|---|",
       "| 모델 16,572 | 고정 A 원장 gzip SHA/행수 재확인, 정상 정적 16,460, parent 누락 48, 등록 사용 보류 6, generated-item N/A 58 (예외 union 112) |",
       "| 요소 105,383 / 면 592,312 | B 정적 부모/면 원장 gzip 재대조; 라이브 UV·베이크 판정은 별도 |",
       "| C 면 592,312 | 원본 PNG 지원 585,969 / 화소 지원 제외 6,343; 출처/slot 예외는 실제 게임 파손 근거 아님 |",
       "| D 상태 1,158 / 옵션 78,456 | 정적 선택 출처·이력; 모델 참조 미해결 4개와 기타 예외 6건 별도 보류 |",
       "| E 사례 62 / 적용 74 / 연구 발견 21 | 14개 후보 + 7개 반례·적용 범위 제한. 21개 전부 F 원본 사례 연결 확인 |",
       "| F 검증 단위 70 | 70/70 조건부, 최종 무조건 승인 0, 공식 4.0.3 NeoForge R08 구분 |",
       "",
       "**G 최종 개별 VERIFIED/CONDITIONAL/HOLD/CONFLICT/N/A 재판정은 추가 진행 필요. H 독립 종료 8게이트도 미승인.**",
       "모델/면/사례/발견은 분모가 달라 한 개의 총합 완성률로 합산하지 않습니다.",
       "원본 JSON/PNG/JAR를 이 G1 회차에서 다시 실행·검수했다는 주장은 하지 않습니다.",
       "INT5 부품 역할·재질 의미·INT6 학습 및 재배포권 승인은 여전히 0.",
       "",
    ]
    rawmarkdown=("\n".join(lines)+"\n").encode("utf-8")
    return {REPORT:rawsummary,FINDINGS:rawfindings,AEXCEPT:rawa,DEXCEPT:rawd,DOC:rawmarkdown}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    for path,data in build().items():
        f=ROOT/path
        if args.verify:assert f.is_file() and f.read_bytes()==data,("NONDETERMINISTIC_G1_RESULT",str(path))
        else:f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
        print("VERIFIED" if args.verify else "CREATED",str(path),len(data))
    print("G1 source scope checked; 0 new G/H/INT5/INT6 final approvals")

if __name__=="__main__":
    main()
