#!/usr/bin/env python3
"""INT-4-H4 H06: exact PR73 CI environment fixes integrated with H3 source.

Checks the 5 original fixed workflow Git blob identities and H3 original ZIP
proof. The GitHub Actions workflow separately runs both complete shared
tests/integration and tests/knowledge suites. This does not waive legacy
runtime F2 errors or approve any INT-4 F/G/H full exit.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PINS={
 ".github/workflows/integration-int2-audit.yml":"2965bc53ed85ced5805e0c9e98d3cae7c3a73786",
 ".github/workflows/integration-int2-rotation.yml":"0bfeaad25950c32913efa2557e516cde7c552b57",
 ".github/workflows/integration-int2-states.yml":"0ed969e4954d058714ce5f2f0ddd8556037093fb",
 ".github/workflows/integration-int2-structure.yml":"ca394cb184c626792c71887ca3cf2fa211d68f9a",
 ".github/workflows/integration-int3-knowledge.yml":"f0d966186670fea6859a040809061152e8854ff2",
}
H3="INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json"
H3_SHA="e67f9c5f2ca4bac01f3e878811ed433f9713109b"
H1="INT4_H1_INDEPENDENT_EXIT_AUDIT_V1.json"
H1_SHA="b6cd345000630079f670146466a1c0a5f8ace165"
OUT=I/"INT4_H4_H06_CI_ENVIRONMENT_INTEGRATED_SOURCE_AUDIT_V1.json"
DOC=I/"INT4_H4_H06_CI_ENVIRONMENT_INTEGRATION_REPORT_V1.md"
def blobsha(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def sha(b):return hashlib.sha256(b).hexdigest()
def load_json(name,expected):
    b=(ROOT/I/name).read_bytes()
    assert blobsha(b)==expected,("ORIGINAL_STAGE_AUDIT_DRIFT",name)
    return json.loads(b)
def source_assess(verify=False):
    report={}
    for path,pin in PINS.items():
        b=(ROOT/path).read_bytes()
        actual=blobsha(b)
        assert actual==pin,("ORIGINAL_PR73_FIXED_WORKFLOW_CONTENT_CHANGED",path,pin,actual)
        body=b.decode("utf-8")
        if "int2-" in path:
            assert "      PYTHONPATH: src" in body
            assert "python -m unittest discover -s tests/integration" in body
            assert "Pillow" in body
            suite="ALL_INTEGRATION_TESTS_ORIGINAL"
        else:
            assert "Pillow>=10,<13" in body and "nbtlib>=2,<3" in body
            assert "python -m unittest discover -s tests/knowledge" in body
            suite="ALL_KNOWLEDGE_TESTS_ORIGINAL"
        report[path]={"git_blob_sha1":actual,"original_PR73_exact_file_sha_matched":True,
                      "shared_test_suite":suite}
    h3=load_json(H3,H3_SHA)
    h1=load_json(H1,H1_SHA)
    assert h3["status"]=="PASS_ALL_F70_ORIGINAL_PNG_ARCHIVE_SHA_AND_CRC_NO_FULL_F_CONTRACT"
    assert h3["recorded_original_PNG_occurrences"]==91 and h3["original_distinct_actions_archive_downloaded"]==20
    assert h3["F_unconditional_full_exit_approved"]==0
    assert h1["H_eight_gates_reviewed"]==8 and h1["H_full_exit_approved"]==0
    assert h1["H_gate_conditional"]==1 and h1["H_gate_hold"]==2
    document={
        "schema":"MCFR_INT4_H4_H06_PARALLEL_PR73_ENVIRONMENT_INTEGRATED_IN_H3_STACK/v1",
        "status":"PASS_PR73_FIVE_EXACT_FIXES_PRESENT_ON_H3_STACK_H4_FULL_SUITES_RUN_SEPARATELY",
        "verified_original_PR73_fixed_workflows":report,
        "original_H1_Git_blob_SHA1":H1_SHA,
        "original_H3_Git_blob_SHA1":H3_SHA,
        "H3_original_archive_20_and_PNG_91_sha_accepted":True,
        "legacy_INT2_test_collection_fix_path":"PYTHONPATH src",
        "legacy_INT3_knowledge_test_dependency_fix":"Pillow and nbtlib",
        "actual_H4_shared_suite_run_contract":{
           "tests_integration":"python -m unittest discover -s tests/integration -p test_*.py -v",
           "tests_knowledge":"python -m unittest discover -s tests/knowledge -p test_*.py -v",
           "installation":"python -m pip install Pillow>=10,<13 nbtlib>=2,<3",
           "result_evidence":"GitHub Actions run result; source audit JSON cannot independently declare a workflow run successful",
        },
        "F70_original_png_reopen_pass_without_game_semantics":91,
        "F_unconditional_final_approved":0,"G_unconditional_final_approved":0,
        "H_full_exit_approved":0,"INT5_semantics_approved":0,"INT6_rights_approved":0,
        "limits":[
            "Five exact PR73 workflow-content fixes are included on the current stacked research branch.",
            "Passing shared unit suites is not a substitute for live Minecraft UI/renderer screenshots or missing F70 server log/UV semantics.",
            "H1 H06 may gain CI environment source proof after this run, but H03/H05 gameplay causality remains independently open.",
            "Do not call original H1 8/8 full success: H1 5 scope pass, 1 conditional, 2 hold and full H exit zero.",
        ],
    }
    b=(json.dumps(document,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
    md=("\n".join([
       "# INT-4-H4 H06 CI 실행환경 소스 동기화 및 전체 공유 회귀시험",
       "",
       "- 병렬 PR73에서 성공한 원본 CI 환경 수정 파일 5개를 각 Git blob SHA로 H3 스택에서 독립 재검증.",
       "- INT2 전체 integration 테스트와 INT3 전체 knowledge 테스트는 각각 새 GitHub Actions에서 재실행되어야 함.",
       "- G/H 최종 승인과 새로 실행된 GUI/UV 근거는 서로 다른 판정 범위임.",
       "- F70 원본 ZIP20/PNG91 SHA는 이전 H3 실제 원본 검수 결과로 유지; F 계약의 전체 서버 상태·화면 의미 여전히 분리.",
       "- INT4 전체 무조건 종료, INT5 모델 부품 의미, INT6 학습/재배포 권리 승인 0.",
       "",
    ])+"\n").encode()
    for target,data in ((OUT,b),(DOC,md)):
        dst=ROOT/target
        if verify:
            assert dst.is_file() and dst.read_bytes()==data,("NOT_REPRODUCIBLE",str(dst))
        else:
            dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
    print(json.dumps({"status":document["status"],"PR73_workflows":5,
      "H3_png":91,"full_exit":0},ensure_ascii=False))
    return document
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true")
    args=p.parse_args();source_assess(args.verify)
if __name__=="__main__":main()
