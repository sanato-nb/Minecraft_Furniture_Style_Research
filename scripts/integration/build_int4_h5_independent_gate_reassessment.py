#!/usr/bin/env python3
"""INT-4-H5 independent H01-H08 reassessment after actual H3/H4 successes.

H3: all 20 original artifact ZIPs/91 PNG image bytes SHA+CRC PASS, but NO
new full server-state/visual/UV interpretation. H4: both complete shared
integration/knowledge unit suites succeeded on stacked PR82 and the five
PR73 workflow Git blob fixes match. H03 mandatory F70 remains HOLD.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,os
from collections import Counter
from pathlib import Path
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
REPO="sanato-nb/Minecraft_Furniture_Style_Research"
MAIN_SHA="176f7f34de2336eb7984c4734e97b6eb156c19f4"
FILES={
 "INT4_H1_INDEPENDENT_EXIT_AUDIT_V1.json":"b6cd345000630079f670146466a1c0a5f8ace165",
 "INT4_H1_EIGHT_INDEPENDENT_EXIT_GATES_V1.csv":"2e15bebca37abc9d5adef8f50df7850a65f58488",
 "INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json":"e67f9c5f2ca4bac01f3e878811ed433f9713109b",
 "INT4_H4_H06_CI_ENVIRONMENT_INTEGRATED_SOURCE_AUDIT_V1.json":"8f67265bba38c1a52d764e71185a8cd740e7eea0",
 "INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json":"779e2435b38fbb002437372eabc5198eec39fbeb",
}
RUNS={"H3_20_artifacts_91_PNG":45127083529,"H4_two_shared_suites":45127460697}
OUT_CSV=I/"INT4_H5_EIGHT_REASSESSED_SCOPED_EXIT_GATES_V1.csv"
OUT_JSON=I/"INT4_H5_H03_H05_H06_EXIT_GATE_REASSESSMENT_V1.json"
OUT_MD=I/"INT4_H5_UPDATED_EIGHT_GATE_INDEPENDENT_REVIEW_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def original(name):
    blob=(ROOT/I/name).read_bytes()
    assert gitblob(blob)==FILES[name],("SOURCE_AUDIT_BLOB_CHANGED",name)
    return blob
def table(blob):return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig"),newline="")))
def csvbytes(rows):
    f=io.StringIO(newline="")
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n")
    writer.writeheader();writer.writerows(rows)
    return f.getvalue().encode("utf-8")
def save(path,data,verify):
    file=ROOT/path
    if verify:assert file.is_file() and file.read_bytes()==data,("H5_NOT_DETERMINISTIC",str(path))
    else:file.parent.mkdir(parents=True,exist_ok=True);file.write_bytes(data)
    return sha(data)
def api(path):
    token=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    assert token,("GITHUB_ACTIONS_READ_TOKEN_REQUIRED")
    with urlopen(Request("https://api.github.com/repos/"+REPO+"/"+path,headers={
            "Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
            "User-Agent":"MCFR-INT4-H5-independent-8-gate-reassessment",
            "X-GitHub-Api-Version":"2022-11-28"}),timeout=65) as response:
        return json.load(response)

def build(verify=False):
    h1=json.loads(original("INT4_H1_INDEPENDENT_EXIT_AUDIT_V1.json"))
    h3=json.loads(original("INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json"))
    h4=json.loads(original("INT4_H4_H06_CI_ENVIRONMENT_INTEGRATED_SOURCE_AUDIT_V1.json"))
    g5=json.loads(original("INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json"))
    old=table(original("INT4_H1_EIGHT_INDEPENDENT_EXIT_GATES_V1.csv"))
    assert h1["status"]=="H1_EIGHT_GATES_INDEPENDENTLY_REVIEWED_FULL_EXIT_BLOCKED"
    assert h3["status"]=="PASS_ALL_F70_ORIGINAL_PNG_ARCHIVE_SHA_AND_CRC_NO_FULL_F_CONTRACT"
    assert h4["status"]=="PASS_PR73_FIVE_EXACT_FIXES_PRESENT_ON_H3_STACK_H4_FULL_SUITES_RUN_SEPARATELY"
    assert g5["status"]=="PASS_G5_PER_POPULATION_SCOPED_DISPOSITIONS_NOT_FINAL_G_OR_H_EXIT"
    assert len(old)==8 and {r["gate_id"] for r in old}=={f"H{x:02d}" for x in range(1,9)}
    assert h3["fixed_case_count"]==70 and h3["recorded_original_PNG_occurrences"]==91
    assert h3["original_distinct_actions_archive_downloaded"]==20
    assert h3["all_20_archive_expected_zip_sha256_verified"] is True
    assert h3["all_91_native_F2_PNG_sha256_verified"] is True
    assert h3["every_original_case_server_state_log_reopened_and_reapproved"] is False
    assert h3["native_F2_new_visual_human_per_case_review_performed"] is False
    assert len(h4["verified_original_PR73_fixed_workflows"])==5
    assert all(v["original_PR73_exact_file_sha_matched"] is True
               for v in h4["verified_original_PR73_fixed_workflows"].values())
    assert g5["dispositions"]["real_F_units"]=={"CONDITIONAL":70}
    assert g5["F_unconditional_exit_approved"]==0
    main=api("branches/main")["commit"]["sha"]
    assert main==MAIN_SHA,("MAIN_CHANGED_STOP_REVIEW",main)
    prstatus={}
    for number in (73,79,80,81,82):
        obj=api("pulls/"+str(number))
        assert obj["draft"] is True and obj["merged"] is False,(
            "ORIGINAL_DRAFT_PR_STATUS_CHANGED",number)
        prstatus[str(number)]={"draft":obj["draft"],"merged":obj["merged"],
                             "head_sha":obj["head"]["sha"],
                             "base":obj["base"]["ref"]}
    live={}
    for key,id in RUNS.items():
        run=api("actions/runs/"+str(id))
        assert run["status"]=="completed" and run["conclusion"]=="success",(
            "EXPECTED_SOURCE_RUN_NOT_SUCCESS",id,run["status"],run["conclusion"])
        live[key]={"run_id":id,"conclusion":run["conclusion"],"head_sha":run["head_sha"]}
    jobs=api("actions/runs/"+str(RUNS["H4_two_shared_suites"])+"/jobs?per_page=100")["jobs"]
    relevant={
       "complete-INT2-integration-original-tests",
       "complete-INT3-knowledge-original-tests",
       "independent-H06-source-after-both-suites-success",
    }
    assert {j["name"] for j in jobs}==relevant,(
        "UNEXPECTED_SHARED_SUITE_JOBS",[j["name"] for j in jobs])
    assert all(j["conclusion"]=="success" for j in jobs),(
        "SHARED_SUITE_NOT_ALL_SUCCESS",[j["name"] for j in jobs if j["conclusion"]!="success"])
    results=[]
    for oldrow in old:
        row=dict(oldrow)
        if row["gate_id"]=="H05":
            assert row["review_status"]=="HOLD_FULL_IMAGE_REOPEN"
            row.update({
              "review_status":"CONDITIONAL_ALL_ORIGINAL_ZIP_PNG_SHA_PASS_GAME_LOG_AND_VISUAL_STILL_OPEN",
              "evidence_scope":"All 20 source Action ZIP artifacts SHA/CRC and all 91 native PNG occurrences SHA/decode directly reopened; actual per-case server/log+scene meaning not independently renewed",
              "evidence_key":"H3_ALL20_ZIP_ALL91_PNG_SHA_CRC_PASS",
              "remaining_condition":"PER_CASE_ORIGINAL_SERVER_STATE_LOG_SHA_AND_HUMAN_SCENE_UV_REVIEW_STILL_REQUIRED",
            })
        elif row["gate_id"]=="H06":
            assert row["review_status"]=="CONDITIONAL_PARALLEL_CI_FIX"
            row.update({
              "review_status":"PASS_SHARED_UNIT_SUITE_SCOPE_ONLY",
              "evidence_scope":"PR73 original five workflow Git blob fixes reproduced; latest stacked H4 full integration and full knowledge unittest suites and provenance job all independently SUCCESS",
              "evidence_key":"H4_FULL_INT2_INT3_SUITE_SUCCESS_PR73_5_BLOBS_PINNED",
              "remaining_condition":"EARLIER_UNRELATED_NATIVE_GUI_CI_FAILURES_NOT_REEVALUATED_AS_RESOLVED",
            })
        elif row["gate_id"]=="H03":
            assert row["review_status"]=="HOLD_FULL_F_EXIT"
            assert "CONTRACTS" in row["original_gate"]
        # H01/H02/H04/H07/H08 are preserved from independently recorded H1.
        row["full_unconditional_exit_satisfied"]="false"
        row["INT5_semantic_approved"]=row["INT6_rights_approved"]="false"
        results.append(row)
    assert len(results)==8
    assert {row["gate_id"] for row in results if row["review_status"]!=
          next(x["review_status"] for x in old if x["gate_id"]==row["gate_id"])}=={"H05","H06"}
    c=Counter(r["review_status"].split("_")[0] for r in results)
    assert c=={"PASS":6,"CONDITIONAL":1,"HOLD":1},c
    raw=csvbytes(results)
    summary={
      "schema":"MCFR_INT4_H5_INDEPENDENT_H05_H06_REASSESSMENT/v1",
      "status":"H5_ALL8_REASSESSED_6_SCOPED_PASS_1_CONDITIONAL_1_HOLD_NO_FULL_EXIT",
      "original_audit_Git_blob_SHA1":FILES,
      "G5_F70_original_contracts_conditional_count":70,
      "H3_real_original_ZIP_sha_CRC_verified":20,
      "H3_real_original_PNG_SHA_and_format_decoded":91,
      "H3_all_original_case_server_logs_and_visual_causality_reapproved":False,
      "H4_original_PR73_exact_fixed_workflow_contents":5,
      "H4_complete_INT2_integration_shared_test_suite_success":True,
      "H4_complete_INT3_knowledge_shared_test_suite_success":True,
      "H4_research_environment_provenance_job_success":True,
      "H_eight_gates_reassessed":8,
      "H_gate_scoped_pass":6,"H_gate_conditional":1,"H_gate_hold":1,
      "H_all_eight_gates_fully_satisfied":False,
      "F_unconditional_full_exit_approved":0,
      "G_unconditional_full_exit_approved":0,
      "H_unconditional_full_exit_approved":0,
      "INT5_semantics_approved":0,
      "INT6_AI_training_or_redistribution_rights_approved":0,
      "live_source_run_verified":live,
      "live_H4_all_three_unit_suite_jobs":{j["name"]:j["conclusion"] for j in jobs},
      "live_original_draft_prs":prstatus,
      "main_HEAD_sha":main,
      "remaining_fallthroughs":[
         "H03 F70 individual mandatory full contracts remain conditional/fully approved zero.",
         "H05 all original 20 zip/91 PNG bytes pass, but per-case original server log state and human game-scene causal appraisal not renewed.",
         "H06 two full shared unit suites and 5 fixed workflow bytes pass; separate legacy real GUI/rendering failures still require actual reproduction.",
         "F2 image SHA or CI environment pass do not confer INT5 furniture semantics nor INT6 asset training/redistribution rights.",
      ],
      "updated_eight_gate_csv_sha256":sha(raw),
    }
    out=(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
    save(OUT_CSV,raw,verify)
    save(OUT_JSON,out,verify)
    md=[
      "# INT-4-H5 8개 게이트 재심사 — H05/H06 실제 진전만 반영",
      "",
      "**8개 재심사: 출처 한정 통과 6, 조건부 1, 보류 1. 전체 최종 종료 승인은 0.**",
      "",
      "| 게이트 | 판정 | 남은 증거 |",
      "|---|---|---|",
    ]
    for item in results:
        md.append("| "+item["gate_id"]+" | "+item["review_status"]+" | "+item["remaining_condition"]+" |")
    md+=["",
      "- H05: 20/20 Actions ZIP SHA+CRC 및 91/91 PNG SHA+디코더 검증 성공. 하지만 게임 화면 해석·UV/서버 로그 전부 재승인은 아님.",
      "- H06: INT2 전체 integration 및 INT3 전체 knowledge 단위 시험 별도 SUCCESS, PR73 고정 5파일 SHA 재검증. 기존 별도 실제 GUI 실패까지 수정한 것은 아님.",
      "- H03: F70/70 조건부 증거 연결만이며 완전 F 계약 승인 0. 무조건 F/G/H 종료 승인 0.",
      "- 역사 원본 PR/파일 SHA 불변, main 기존 커밋 확인, Draft만 사용.",
      "- INT5 부품 의미·INT6 원저작물 재배포/AI 학습권한 승인 0.",
      "",
    ]
    save(OUT_MD,("\n".join(md)+"\n").encode("utf-8"),verify)
    print(json.dumps({"status":summary["status"],"reviewed":8,"scoped_PASS":6,
         "CONDITIONAL":1,"HOLD":1,"full_exit":0},ensure_ascii=False))
    return summary
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--verify",action="store_true")
    args=p.parse_args();build(args.verify)
if __name__=="__main__":main()
