#!/usr/bin/env python3
"""INT-4-H1: independent 8 exit-gate audit, not a blanket full exit.

Reopen G5 per-population ledgers and previous A/G/F source SHA, check
specific historical failure/retry Actions and live remote PR/main status.
Retain the difference between reviewing all 8 gates and satisfying all 8.
"""
from __future__ import annotations
import argparse,csv,gzip,hashlib,io,json,os
from collections import Counter
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
REPO="sanato-nb/Minecraft_Furniture_Style_Research"
MAIN_SHA="176f7f34de2336eb7984c4734e97b6eb156c19f4"
AUDITS={
    "INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json":"779e2435b38fbb002437372eabc5198eec39fbeb",
    "INT4_G1_SOURCE_LAYER_GATE_SUMMARY_V1.json":"9772bcb7bb3243b7f0d166b99d7f602c23a2e0fe",
    "INT4_A_ADJUDICATION_SUMMARY_V2.json":"621cce07862bbc5bb051809eeeef8df9607c0a37",
    "INT4_G3_EXCEPTION_SOURCE_REACHABILITY_AUDIT_V1.json":"5224ff016e32f5a431b922bce629c2e0aa6bbc2f",
    "INT4_G4_HC6_PARENT_CHAIN_AND_ORIGINAL_GIT_AUDIT_V1.json":"9de9cd59e5aa4ef6ca5b16932aa31244a4cf488b",
    "INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json":"dbf5118138851f664468e5bcb8ef84e1edde6fd5",
}
ROWS={
    "INT4_G5_16572_MODEL_SCOPED_DISPOSITIONS_V1.csv.gz":16572,
    "INT4_G5_592312_FACE_SCOPED_DISPOSITIONS_V1.csv.gz":592312,
    "INT4_G5_1158_STATE_SCOPED_DISPOSITIONS_V1.csv":1158,
    "INT4_G5_21_FINDING_SCOPED_DISPOSITIONS_V1.csv":21,
    "INT4_G5_70_REAL_F2_SCOPED_DISPOSITIONS_V1.csv":70,
}
ACTIONS={
    "F11F_original_two_F2_real_game":(45108332421,"success"),
    "F11F_original_F2_independent":(45109242418,"success"),
    "G1_source_census":(45109756624,"success"),
    "G2_full_source_join":(45110599720,"success"),
    "G3_source_exception":(45111136606,"success"),
    "G4_first_failed_parent_chain_assumption":(45112877045,"failure"),
    "G4_corrected_parent_chain":(45112966090,"success"),
    "G5_five_population_scope":(45113845823,"success"),
}
PR_CHAIN=(72,74,75,76,77,78)
HOUT=I/"INT4_H1_EIGHT_INDEPENDENT_EXIT_GATES_V1.csv"
JSONOUT=I/"INT4_H1_INDEPENDENT_EXIT_AUDIT_V1.json"
REPORT=I/"INT4_H1_EXIT_AUDIT_AND_HANDOFF_V1.md"
def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def raw_audit(name):
    b=(ROOT/I/name).read_bytes()
    assert gitblob(b)==AUDITS[name],("PRIOR_AUDIT_CHANGED",name)
    return json.loads(b)
def rows(name,sha_pin,count):
    data=(ROOT/I/name).read_bytes()
    assert sha(data)==sha_pin,("G5_LEDGER_SHA_CHANGED",name)
    if name.endswith(".gz"):
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as g:
            result=list(csv.DictReader(io.TextIOWrapper(g,encoding="utf-8-sig",newline="")))
    else:
        result=list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"),newline="")))
    assert len(result)==count,("G5_LEDGER_ROWS_CHANGED",name,len(result))
    return result
def csvout(entries):
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream,fieldnames=list(entries[0]),lineterminator="\n")
    writer.writeheader();writer.writerows(entries)
    return stream.getvalue().encode("utf-8")
def put(name,blob,verify):
    path=ROOT/name
    if verify:assert path.is_file() and path.read_bytes()==blob,("NONDETERMINISTIC_H1",str(name))
    else:path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(blob)
    return {"sha256":sha(blob),"size_bytes":len(blob)}
def get_api(endpoint):
    token=os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    assert token,("GITHUB_READ_TOKEN_REQUIRED")
    req=Request("https://api.github.com/repos/"+REPO+"/"+endpoint,
        headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
                 "X-GitHub-Api-Version":"2022-11-28","User-Agent":"MCFR-INT4-H1-independent-source-audit"})
    with urlopen(req,timeout=50) as resp:
        return json.load(resp)
def check_live():
    head=get_api("branches/main")["commit"]["sha"]
    assert head==MAIN_SHA,("MAIN_BASE_SHA_CHANGED_REVIEW_BEFORE_EXIT",head)
    prs={}
    for number in PR_CHAIN+(73,):
        result=get_api("pulls/"+str(number))
        assert result["number"]==number
        assert result["draft"] is True and result["merged"] is False,("HISTORIC_DRAFT_OR_MERGE_CHANGED",number)
        prs[str(number)]={"draft":result["draft"],"merged":result["merged"],
                          "head_sha":result["head"]["sha"],"base":result["base"]["ref"]}
    assert prs["78"]["head_sha"]=="53cd969e002794542cce2d3400d1f1e3bba62e53"
    actions={}
    for name,(id,expected) in ACTIONS.items():
        a=get_api("actions/runs/"+str(id))
        assert a["id"]==id and a["conclusion"]==expected and a["status"]=="completed",(
            "ACTION_RUN_PROVENANCE_CHANGED",id,a["status"],a["conclusion"])
        actions[name]={"id":id,"conclusion":a["conclusion"],"head_sha":a["head_sha"]}
    assert actions["G4_first_failed_parent_chain_assumption"]["conclusion"]=="failure"
    assert actions["G4_corrected_parent_chain"]["conclusion"]=="success"
    return {"main_head_sha":head,"draft_pull_requests":prs,"checked_actions":actions}

def assess():
    g5=raw_audit("INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json")
    g1=raw_audit("INT4_G1_SOURCE_LAYER_GATE_SUMMARY_V1.json")
    a=raw_audit("INT4_A_ADJUDICATION_SUMMARY_V2.json")
    g3=raw_audit("INT4_G3_EXCEPTION_SOURCE_REACHABILITY_AUDIT_V1.json")
    g4=raw_audit("INT4_G4_HC6_PARENT_CHAIN_AND_ORIGINAL_GIT_AUDIT_V1.json")
    f11=raw_audit("INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
    assert g5["status"]=="PASS_G5_PER_POPULATION_SCOPED_DISPOSITIONS_NOT_FINAL_G_OR_H_EXIT"
    assert g5["G_unconditional_exit_approved"]==g5["H_independent_exit_approved"]==0
    assert len(g5["H_eight_gate_preflight_only"])==8
    assert g4["base_scope_disposition_counts"]=={
       "VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS":6}
    assert f11["counts"]["F_conditional_after"]==70 and f11["counts"]["F_unconditional_final_approvals"]==0
    populations={}
    for name,count in ROWS.items():
        data=rows(name,g5["derived_output_SHA256"][name]["sha256"],count)
        populations[name]=data
    m=populations["INT4_G5_16572_MODEL_SCOPED_DISPOSITIONS_V1.csv.gz"]
    face=populations["INT4_G5_592312_FACE_SCOPED_DISPOSITIONS_V1.csv.gz"]
    state=populations["INT4_G5_1158_STATE_SCOPED_DISPOSITIONS_V1.csv"]
    finding=populations["INT4_G5_21_FINDING_SCOPED_DISPOSITIONS_V1.csv"]
    F=populations["INT4_G5_70_REAL_F2_SCOPED_DISPOSITIONS_V1.csv"]
    bypop={
       "models":Counter(x["G5_disposition"] for x in m),
       "faces":Counter(x["G5_disposition"] for x in face),
       "mod_blockstates":Counter(x["G5_disposition"] for x in state),
       "historic_findings":Counter(x["G5_disposition"] for x in finding),
       "real_F_units":Counter(x["G5_disposition"] for x in F),
    }
    assert {k:dict(v) for k,v in bypop.items()}==g5["dispositions"]
    assert all(x["historical_A_HOLD_modified"]=="false" and x["actual_game_all_models_approved"]=="false" for x in m)
    assert all(x["baked_live_UV_approved"]=="false" for x in face)
    assert all(x["full_game_release_equivalence_approved"]=="false" for x in state)
    assert all(x["new_universal_rule_approved"]=="false" and x["INT6_rights_approved"]=="false" for x in finding)
    assert all(x["full_F_approved"]=="false" and x["full_G_approved"]=="false" for x in F)
    assert all(x["original_F2_run_ids"] and x["original_F2_sha256s"] for x in F)
    assert len({x["target_id"] for x in F})==70
    assert Counter(x["target_kind"] for x in F)=={"HISTORICAL_1_5_CASE":62,"RISK_SCENARIO":8}
    assert Counter(x["C_exception"] for x in face if x["C_exception"])==Counter(g5["C_exception_reasons"])
    a_break=g1["source_disposition_counts"]
    assert {k:a_break[k] for k in ("A_missing_parents","A_no_static","A_parent_missing_also_no_static_overlap","A_exception_union_distinct_models","C_face_pixel_exception_categories_total")}=={
       "A_missing_parents":48,"A_no_static":108,"A_parent_missing_also_no_static_overlap":44,
       "A_exception_union_distinct_models":112,"C_face_pixel_exception_categories_total":6343}
    assert a["review_results"]["HOLD_MODEL_USAGE_AND_RENDER_PATH"]==6
    assert g3["D_6_exception_reasons"]=={"UNRESOLVED_MODEL_REF":4,"PRIOR_CHAIR_VARIANT_3_POINTS_TO_1":2}
    assert [x["state_id"] for x in state if x["G5_disposition"]=="HOLD"]==[
        "another_furniture:unused/white_awning"]
    return g5,a_break,bypop

def audit_all(verify=False):
    g5,exceptions,pop=assess()
    live=check_live()
    # Independent gate decisions. Reviewing 8 gates does NOT mean passing 8.
    decisions=[
      ("H01","A_E_ALL_DISPOSITIONS","PASS_SOURCE_SCOPE",
       "16572 models, 592312 source faces, 1158 state paths, 21 findings, F70 all have exact scoped decisions",
       "STATIC_SOURCE_A_TO_E","DYNAMIC_JAVA_AND_IN_GAME_SUBSETS_REMAIN",
       "INT4-G"),
      ("H02","C_PIXEL_A_PARENT_NO_STATIC_OVERLAP","PASS_EXCEPTIONS_DOCUMENTED",
       "C 6343 exact exception-face linkage; parent missing 48 and no-static 108 overlap 44; 112 union exceptions",
       "C6343_A48_NO_STATIC108_OVERLAP44","ORIGINAL_PNG_PIXEL_OUTLIERS_AND_DYNAMIC_PARENT_USAGE_NOT_RESOLVED",
       "INT4-C_INT4-A"),
      ("H03","F70_MANDATORY_CASE_CONTRACTS","HOLD_FULL_F_EXIT",
       "62 historic and 8 risk units source/F2/run sha documented as CONDITIONAL; unconditional full F PASS 0",
       "F70_F11F_G5","COMPLETE_VERSION_REGISTERED_RUNTIME_PIXEL_RENDER_AND_EXCEPTION_CONTRACTS_PER_CASE",
       "INT4-F"),
      ("H04","G_FIVE_POPULATION_DISPOSITION_PROVENANCE","PASS_SCOPED_G_LEDGER",
       "G5 all 5 population ledgers independently decompressed, recount and negative live/rights claims verified",
       "G5_FIVE_DISPOSITION_LEDGERS","G_UNCONDITIONAL_EXIT_NOT_YET_GRANTED",
       "INT4-G"),
      ("H05","ORIGINAL_LOG_SCREENSHOT_SHA_COMPLETENESS","HOLD_FULL_IMAGE_REOPEN",
       "All F70 have historic run IDs/image SHA, F11F two actual F2 original reopened; not all prior F70 original archives reopened during this H",
       "F70_HISTORICAL_SHA_AND_F11F_ARCHIVE","REOPEN_ALL_MANDATORY_ARCHIVES_AND_VALIDATE_RUN_LOG_SHA_WHILE_ACCESSIBLE",
       "INT4-F_INT4-H"),
      ("H06","INDEPENDENT_CI_AND_PATH_INTEGRITY","CONDITIONAL_PARALLEL_CI_FIX",
       "G1 G2 G3 G4 G5 F11F Actions passed, however PR73 CI dependency fix is separate from stacked PR78; old cross-tests not all green",
       "G1_G2_G3_G4_G5_CI_PR73_SEPARATE","RECONCILE_PARALLEL_CI_AND_COMPLETE_REQUIRED_CROSS_WORKFLOWS",
       "INT4-H_CI"),
      ("H07","FAILURE_RETRY_ARCHIVE","PASS_FAILED_RUN_AND_RETRY_RECORDED",
       "G4 parent-chain first evidence assertion failed, corrected G4 Actions success, no original history overwritten",
       "G4_FAILED_45112877045_CORRECTED_45112966090","RETAIN_FAIL_AND_PATCH_SHA_IN_HANDOFF",
       "INT4-H"),
      ("H08","HISTORIC_INPUTS_AND_MAIN_IMMUTABILITY","PASS_PINNED_HISTORY_AND_MAIN_DRAFT",
       "Original A-G/F Git blob pins and G5 output sha recomputed; remote main remains baseline and research PR72-78 Draft not merged",
       "A_G5_SOURCE_SHA_MAIN_PR_CHAIN","ALL_HISTORY_DATA_RIGHTS_SEMANTICS_STILL_EXCLUDED",
       "INT4-H"),
    ]
    assert len(decisions)==8 and len({x[0] for x in decisions})==8
    result=[]
    for number,kind,status,evidence,ref,remain,owner in decisions:
        result.append({"gate_id":number,"original_gate":kind,"review_status":status,
         "evidence_scope":evidence,"evidence_key":ref,
         "full_unconditional_exit_satisfied":"false",
         "remaining_condition":remain,"next_stage_owner":owner,
         "INT5_semantic_approved":"false","INT6_rights_approved":"false"})
    rcount=Counter(r["review_status"].split("_")[0] for r in result)
    assert rcount=={"PASS":5,"HOLD":2,"CONDITIONAL":1},rcount
    entries=csvout(result)
    outsum={
       "schema":"MCFR_INT4_H1_INDEPENDENT_EIGHT_EXIT_GATE_REVIEW/v1",
       "status":"H1_EIGHT_GATES_INDEPENDENTLY_REVIEWED_FULL_EXIT_BLOCKED",
       "git_original_audit_blob_SHA1":AUDITS,
       "original_G5_ledger_sha256":{k:v["sha256"] for k,v in g5["derived_output_SHA256"].items()},
       "independent_reopened_population_rows":{k:len(ROWS) and ROWS[k] for k in ROWS},
       "scoped_disposition_counts":{k:dict(v) for k,v in pop.items()},
       "A_missing_parents":48,"A_no_static_models":108,
       "A_overlap_missing_parent_and_no_static":44,
       "C_pixel_exception_faces":6343,
       "F_conditionally_documented":70,
       "F_unconditionally_approved":0,
       "H_eight_gates_reviewed":8,"H_gate_scoped_pass":5,
       "H_gate_conditional":1,"H_gate_hold":2,
       "H_eight_gates_unconditionally_approved":0,
       "G_final_unconditional_exit_approved":0,"H_full_exit_approved":0,
       "INT5_part_role_semantics_approved":0,"INT6_training_or_redistribution_rights_approved":0,
       "live_GitHub_provenance":live,
       "gate_summary":[{"gate_id":r["gate_id"],"review_status":r["review_status"],
                        "full_exit_satisfied":False,"owner":r["next_stage_owner"]} for r in result],
       "reason_for_not_accepting_H_full_exit":[
         "70 F case-specific original render contracts remain conditional, not individually fully closed.",
         "This H run verifies archived screenshot SHA metadata and selected independent F11F original image audit, not every historic original image file/scene.",
         "Parallel PR73 CI environment fix must be reconciled with stacked head; unrelated prior CI failures not hidden.",
         "The only held D state is an unused awning JSON with four unresolved references; a missing registration proof cannot be substituted for a full dynamic loader audit.",
         "A-G source-level dispositions permit bounded structural research usage only; no INT5 semantic or INT6 content rights permissions.",
       ],
       "outputs":{"eight_gate_csv_sha256":sha(entries)},
    }
    outdata=(json.dumps(outsum,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    put(HOUT,entries,verify);put(JSONOUT,outdata,verify)
    md=[
      "# INT-4-H1 8개 종료 게이트 **독립 심사**, 최종 종료 보류",
      "",
      "**8/8 게이트를 심사한 사실과 8/8 통과는 다릅니다. 최종 H 무조건 승인 0.**",
      "",
      "| 게이트 | 판정 | 근거와 후속 |",
      "|---|---|---|",
    ]
    for r in result:
        md.append("| "+r["gate_id"]+" "+r["original_gate"]+" | "+r["review_status"]+" | "+r["remaining_condition"]+" |")
    md+=["",
       "실행/출처 검사: 원본 Git blob SHA 고정, G5 CSV/CSV.gz 5종 전수 재독해, GitHub main 커밋/PR Draft 상태/과거 CI 8실행을 API에서 독립 확인.",
       "F70 원본 이미지 SHA와 실행 ID의 존재는 원본 ZIP 70개 전체를 이 회차에서 다시 열었다는 의미가 아닙니다.",
       "종료를 막는 요인은 70건 F 필수 계약·오래된 F2 원본 접근성·별도 CI 수정 PR의 반영 범위입니다.",
       "실패 G4 CI와 수정 성공을 모두 기록. 역사 원본·main 수정 없이 신규 Draft에 감사 내용만 추가.",
       "INT5 부품 의미·INT6 AI 훈련/재배포 권한은 별도 미승인.",
       "",
    ]
    put(REPORT,("\n".join(md)+"\n").encode("utf-8"),verify)
    print(json.dumps({"status":outsum["status"],"H_reviewed":8,
        "scoped_pass":5,"conditional":1,"hold":2,"full_exit":0},ensure_ascii=False))
    return outsum

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--verify",action="store_true")
    args=p.parse_args()
    audit_all(args.verify)
if __name__=="__main__":
    main()
