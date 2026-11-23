#!/usr/bin/env python3
"""INT-4-G5: separate source-scoped G disposition ledgers; NO full G/H exit."""
from __future__ import annotations
import argparse,csv,gzip,hashlib,io,json
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PIN={
 "INT4_G2_16572_MODEL_SOURCE_SCOPE_DISPOSITIONS_V1.csv.gz":"8266579dc9a59ed65ce77e6dd33855a796f7d5b621a28bf1d3c74528f46d0549",
 "INT4_G2_592312_FACE_SOURCE_APPLICABILITY_V1.csv.gz":"d752fd1f37dac41f338b97054a4a68a3ecab4d872731af9c0dde69fd54e0dd32",
 "INT4_G2_6343_FACE_PIXEL_EXCEPTION_CROSSWALK_V1.csv.gz":"bba8d7e9357827587913a74bcd3ccfd28cf808e0e4ac3424af85a5df06179026",
 "INT4_G2_1158_STATE_RUNTIME_SOURCE_GATES_V1.csv":"3c03bfb5bd2e8709a03f08d704584ed7f0ce4fa2846f957b8d0bfac55e1868f0",
 "INT4_G2_21_FINDING_F70_EVIDENCE_GATES_V1.csv":"f9e14b7a8009f36307698002acd7df4e17e95ceb071ebe72769b10043ad5e1b3",
 "INT4_G2_70_F_CONTRACT_NONAPPROVAL_V1.csv":"8103055f8d2f8baa9de4684318205828886a72a4a6d71ec0d8e7142b3b21db71",
 "INT4_G4_HC6_BASE_SOURCE_PARENT_DISPOSITIONS_V1.csv":"d91abd4664866e21e9555cc9dcc1e7cd323443c08804fcdbfb6198ab118e3d52",
}
GIT={
 "INT4_G2_SOURCE_CROSSJOIN_AUDIT_V1.json":"0514015a4bca32f497ffc8cb86a8d9e6d8b30d08",
 "INT4_G3_EXCEPTION_SOURCE_REACHABILITY_AUDIT_V1.json":"5224ff016e32f5a431b922bce629c2e0aa6bbc2f",
 "INT4_G4_HC6_PARENT_CHAIN_AND_ORIGINAL_GIT_AUDIT_V1.json":"9de9cd59e5aa4ef6ca5b16932aa31244a4cf488b",
 "INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json":"dbf5118138851f664468e5bcb8ef84e1edde6fd5",
}
O_MODEL=I/"INT4_G5_16572_MODEL_SCOPED_DISPOSITIONS_V1.csv.gz"
O_FACE=I/"INT4_G5_592312_FACE_SCOPED_DISPOSITIONS_V1.csv.gz"
O_STATE=I/"INT4_G5_1158_STATE_SCOPED_DISPOSITIONS_V1.csv"
O_FINDING=I/"INT4_G5_21_FINDING_SCOPED_DISPOSITIONS_V1.csv"
O_F=I/"INT4_G5_70_REAL_F2_SCOPED_DISPOSITIONS_V1.csv"
O_JSON=I/"INT4_G5_FOUR_DENOMINATORS_SCOPED_DECISIONS_V1.json"
O_MD=I/"INT4_G5_SCOPED_DECISIONS_AND_H_PREFLIGHT_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def blobsha(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def source(name):
    b=(ROOT/I/name).read_bytes()
    assert sha(b)==PIN[name],("SOURCE_SHA_DRIFT",name,sha(b))
    return b
def prior(name):
    b=(ROOT/I/name).read_bytes()
    assert blobsha(b)==GIT[name],("PRIOR_AUDIT_GIT_BLOB_DRIFT",name)
    return json.loads(b)
def csvparse(b):
    return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def gzparse(name,count):
    with gzip.GzipFile(fileobj=io.BytesIO(source(name))) as g:
        rows=list(csv.DictReader(io.TextIOWrapper(g,encoding="utf-8-sig",newline="")))
    assert len(rows)==count,("GZIP_ROWS_CHANGED",name)
    return rows
def csvb(rows):
    buf=io.StringIO(newline="")
    w=csv.DictWriter(buf,fieldnames=list(rows[0]),lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return buf.getvalue().encode("utf-8")
def save(path,data,verify):
    p=ROOT/path
    if verify:assert p.is_file() and p.read_bytes()==data,("NONDETERMINISTIC",str(path))
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    return {"sha256":sha(data),"size":len(data)}
def Bkey(r):
    return (r["model_key"],r["element_index"],r["face_direction"],r["texture_slot"],r["source_uv"])
def Ckey(r):
    return (r["model_key"],r["element_index"],r["face_direction"],r["source_slot"],r["uv"])

def build(verify=False):
    g2=prior("INT4_G2_SOURCE_CROSSJOIN_AUDIT_V1.json")
    g3=prior("INT4_G3_EXCEPTION_SOURCE_REACHABILITY_AUDIT_V1.json")
    g4=prior("INT4_G4_HC6_PARENT_CHAIN_AND_ORIGINAL_GIT_AUDIT_V1.json")
    f11=prior("INT4_F11F_R08_TWO_FABRIC_ORIGINAL_F2_INDEPENDENT_AUDIT_V1.json")
    assert g2["status"]=="PASS_G2_PINNED_A_B_C_D_E_F_SOURCE_CROSSJOIN_WITH_REMAINING_LIMITS_NOT_FINAL_G"
    assert g3["status"]=="PASS_G3_STATIC_OPTION_IMPACT_WITH_PINNED_UPSTREAM_JAVA_AND_NO_RUNTIME_EXIT"
    assert g4["status"]=="PASS_ORIGINAL_HC_GIT_SIX_EMPTY_GUI_BASE_MODELS_REVIEWED_PARENT_CHILD_SCOPE"
    assert f11["counts"]["F_conditional_after"]==70 and f11["counts"]["F_unconditional_final_approvals"]==0
    models=gzparse("INT4_G2_16572_MODEL_SOURCE_SCOPE_DISPOSITIONS_V1.csv.gz",16572)
    faces=gzparse("INT4_G2_592312_FACE_SOURCE_APPLICABILITY_V1.csv.gz",592312)
    exc=gzparse("INT4_G2_6343_FACE_PIXEL_EXCEPTION_CROSSWALK_V1.csv.gz",6343)
    states=csvparse(source("INT4_G2_1158_STATE_RUNTIME_SOURCE_GATES_V1.csv"))
    studies=csvparse(source("INT4_G2_21_FINDING_F70_EVIDENCE_GATES_V1.csv"))
    f70=csvparse(source("INT4_G2_70_F_CONTRACT_NONAPPROVAL_V1.csv"))
    hc=csvparse(source("INT4_G4_HC6_BASE_SOURCE_PARENT_DISPOSITIONS_V1.csv"))
    assert (len(states),len(studies),len(f70),len(hc))==(1158,21,70,6)
    hcmap={r["model_key"]:r for r in hc}
    assert set(hcmap)=={"HC1","HC2","HC3","HC4","HC5","HC6"}
    assert all(r["G4_source_model_scope_disposition"]=="VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS" for r in hc)
    mresult=[]; mc=Counter()
    for r in models:
        s=r["G2_source_scope_disposition"]
        if s=="VERIFIED_STATIC_SOURCE_ONLY":
            grade="VERIFIED";scope="STATIC_ORIGINAL_MODEL_PARENT_ONLY"
        elif s=="HOLD_BASE_MODEL_USAGE_UNKNOWN":
            assert r["model_key"] in hcmap
            grade="VERIFIED";scope="HC_DISPLAY_BASE_PARENT_AND_SELECTED_DESCENDANTS_STATIC_ONLY"
        elif s=="CONDITIONAL_MISSING_PARENT_STATIC_UNREACHABLE_DYNAMIC_UNKNOWN":
            grade="CONDITIONAL";scope="MISSING_PARENT_STATIC_D_UNREACHED_DYNAMIC_UNKNOWN"
        elif s=="NOT_APPLICABLE_GENERATED_ITEM_CUBOID":
            grade="NOT_APPLICABLE";scope="GENERATED_ITEM_IS_NOT_STATIC_JSON_CUBOID"
        else:raise AssertionError(("UNKNOWN_A",s))
        mc[grade]+=1
        mresult.append({
          "model_key":r["model_key"],"mod":r["mod"],"original_path":r["original_source_path"],
          "original_source_sha":r["original_source_SHA"],"A_historic_status":r["A_historical_review"],
          "G2_status":s,"G4_HC_base_parent_role":hcmap.get(r["model_key"],{}).get("G4_source_model_scope_disposition",""),
          "G5_disposition":grade,"G5_scope":scope,
          "historical_A_HOLD_modified":"false","actual_game_all_models_approved":"false",
          "INT5_semantic_INT6_rights_approved":"false",
        })
    assert mc=={"VERIFIED":16466,"CONDITIONAL":48,"NOT_APPLICABLE":58},mc
    reasons=defaultdict(list)
    for r in exc:
        assert r["B_source_face_relation"]=="FACE_SOURCE_SLOT_UV_MATCH"
        reasons[Ckey(r)].append(r["exception_reason"])
    fresult=[];fc=Counter();c_why=Counter()
    for r in faces:
        assert r["G2_face_provenance"]=="VERIFIED_STATIC_FACE_PROVENANCE_ONLY"
        key=Bkey(r)
        if reasons[key]:
            reason=reasons[key].pop();grade="CONDITIONAL"
            scope="PINNED_B_SOURCE_VALID_C_PIXEL_SOURCE_EXCEPTION"
            c_why[reason]+=1
        else:
            reason="";grade="VERIFIED"
            scope="B_SOURCE_AND_HISTORIC_PINNED_PIXEL_LINK_ONLY"
        fc[grade]+=1
        fresult.append({
          "model_key":r["model_key"],"source_model_sha":r["source_model_SHA"],
          "provider_source_sha":r["provider_original_source_SHA"],
          "element_index":r["element_index"],"face_direction":r["face_direction"],
          "source_slot":r["texture_slot"],"original_UV":r["source_uv"],
          "G5_disposition":grade,"G5_scope":scope,
          "C_exception":reason,"C_exception_source_key_method":"MODEL_ELEMENT_FACE_SLOT_UV_MULTISET",
          "baked_live_UV_approved":"false","INT5_INT6_approved":"false",
        })
    leftovers=sum(len(v) for v in reasons.values())
    assert leftovers==0,("C_EXCEPTIONS_NOT_COVERED",leftovers)
    assert fc=={"VERIFIED":585969,"CONDITIONAL":6343},fc
    assert c_why==Counter(g2["C_historic_pixel_source_reason_counts"]),(c_why,g2["C_historic_pixel_source_reason_counts"])
    assert g3["C_6343_pixel_face_source_selection_dispositions"]=={
        "CONDITIONAL_C_EXCEPTION_NOT_DIRECTLY_SELECTED_IN_STATIC_D_OPTIONS":6343}
    dresult=[];dc=Counter()
    for r in states:
        old=r["source_link_disposition"]
        if old=="CONDITIONAL_DECLARED_SELECTOR_NOT_RUNTIME_PROVEN":
            grade="CONDITIONAL";follow="REGISTERED_DYNAMIC_STATE_AND_RELEASE_EQUIVALENCE_NOT_ALL_LIVE_CHECKED"
        elif old=="HOLD_SOURCE_MODEL_REFERENCE_AND_RELEASE":
            assert r["state_id"]=="another_furniture:unused/white_awning"
            assert r["model_reference_missing_count"]=="4"
            grade="HOLD";follow="UNRESOLVED_WHITE_AWNING_DOUBLE_MODEL_FOUR_RULES;GLOBAL_REGISTRY_NOT_EXHAUSTED"
        else:raise AssertionError(("UNKNOWN_D",old))
        dc[grade]+=1
        dresult.append({
          "state_id":r["state_id"],"mod":r["mod"],"source_path":r["state_original_path"],
          "source_sha":r["state_source_SHA"],"static_option_count":r["verified_option_row_count"],
          "unresolved_model_ref_count":r["model_reference_missing_count"],
          "G5_disposition":grade,"G5_scope":"SOURCE_SELECTOR_WITHOUT_ALL_REGISTERED_LIVE_RUNTIME",
          "required_followup":follow,"full_game_release_equivalence_approved":"false",
        })
    assert dc=={"CONDITIONAL":1157,"HOLD":1},dc
    eout=[];ec=Counter()
    for r in studies:
        old=r["G2_scoped_finding_disposition"]
        if old=="CONDITIONAL_MEASURED_HISTORIC_SOURCE_REVIEW_REQUIRED":
            grade="CONDITIONAL";scope="HISTORIC_F2_REFERENCES_NOT_GENERAL_RULE"
        elif old=="NOT_APPLICABLE_AS_UNIVERSAL_RULE_SCOPE_LIMIT_STILL_VALUABLE_AS_COUNTEREXAMPLE":
            grade="NOT_APPLICABLE";scope="UNIVERSAL_RULE_INAPPLICABLE_COUNTEREXAMPLE_RETAINED"
        else:raise AssertionError(("UNKNOWN_E",old))
        assert r["G2_new_general_rule_approved"]=="false"
        ec[grade]+=1
        eout.append({
          "finding_id":r["finding_id"],"axis":r["axis"],"source_case_ids":r["source_case_ids"],
          "F_conditional_case_links":r["F_conditional_case_evidence_links"],
          "G5_disposition":grade,"G5_scope":scope,"new_universal_rule_approved":"false",
          "INT5_part_semantic_approved":"false","INT6_rights_approved":"false",
          "followup":r["followup"],
        })
    assert ec=={"CONDITIONAL":14,"NOT_APPLICABLE":7},ec
    fout=[]
    for r in f70:
        assert r["F_historic_status"].startswith("CONDITIONAL")
        assert r["full_F_approved"]==r["full_G_approved"]=="false"
        fout.append({
          "target_id":r["target_id"],"target_kind":r["target_kind"],
          "minecraft_version":r["minecraft_version"],"block":r["block"],
          "source_F_evidence_disposition":r["F_historic_status"],
          "original_F2_run_ids":r["F_original_run_ids"],"original_F2_sha256s":r["F_original_image_sha256s"],
          "G5_disposition":"CONDITIONAL",
          "G5_scope":"EXACT_CASE_OR_SCENARIO_F2_EVIDENCE_ONLY_NOT_FULL_CONTRACT",
          "full_F_approved":"false","full_G_approved":"false",
          "remaining_contract":r["remaining_contract_risk"],
        })
    assert len(fout)==70
    generated={
      O_MODEL:gzip.compress(csvb(mresult),mtime=0),
      O_FACE:gzip.compress(csvb(fresult),mtime=0),
      O_STATE:csvb(dresult),O_FINDING:csvb(eout),O_F:csvb(fout),
    }
    saved={p.name:save(p,b,verify) for p,b in generated.items()}
    h_gates=[
        ("A_E_SOURCE_DISPOSITIONS","REVIEW","A/source provenance and 48 dynamic missing-parent cases"),
        ("C_6343_AND_NO_STATIC_OVERLAP","REVIEW","6343 C face exception reasons; 48 parent missing/108 no-static overlap preserved"),
        ("F_70_CONTRACTS","BLOCKED","70 conditional native F2 evidence, 0 unconditional contracts"),
        ("G_POPULATIONS","REVIEW","5 distinct population ledgers produced, exact G5 scoped decisions only"),
        ("ORIGINAL_SHA_EXECUTION_LOGS","REVIEW","original SHA pins but independent F2 artifact/runner retention still needs H"),
        ("INDEPENDENT_CI_PATH_INTEGRITY","REVIEW","G5 CI plus unrelated INT2 old branch regressions and parallel PR73"),
        ("FAILURE_AND_RETRY_HISTORY","REVIEW","G4 failed parent chain assumption then corrected; provenance preserved"),
        ("HISTORICAL_IMMUTABILITY_AND_MAIN","REVIEW","main and original files to be independently checked in H"),
    ]
    report={
       "schema":"MCFR_INT4_G5_SCOPED_FOUR_POPULATIONS_AND_F70/v1",
       "status":"PASS_G5_PER_POPULATION_SCOPED_DISPOSITIONS_NOT_FINAL_G_OR_H_EXIT",
       "original_file_SHA256":PIN,
       "original_audit_Git_blob_SHA1":GIT,
       "denominators":{"models":16572,"faces":592312,"mod_blockstate_sources":1158,
                       "historic_findings":21,"real_F_units":70},
       "dispositions":{
           "models":dict(mc),"faces":dict(fc),"mod_blockstates":dict(dc),
           "historic_findings":dict(ec),"real_F_units":{"CONDITIONAL":70}},
       "C_exception_exact_source_face_matching":6343,
       "C_exception_reasons":dict(c_why),
       "G4_six_HC_static_display_base_roles_considered":True,
       "original_A_six_HOLD_retained_and_not_edited":True,
       "F_unconditional_exit_approved":0,"G_unconditional_exit_approved":0,
       "H_independent_exit_approved":0,"INT5_semantic_approved":0,
       "INT6_training_and_redistribution_rights_approved":0,
       "H_eight_gate_preflight_only":[{"gate":k,"status":s,"reason":reason} for k,s,reason in h_gates],
       "limits":[
         "Model VERIFIED refers to original static source/parent role only; not all Minecraft game meshes.",
         "Face VERIFIED refers to source and historical pixel link only; not per-face baked 3D texture render.",
         "G4 HC6 source role is an additional provenance judgment; historic A HOLD is preserved.",
         "48 missing parents and 6343 pixel exceptions are not registered in direct D selections, but dynamic/item use remains open.",
         "Seven historical counterexamples N/A for universal rules remain useful historical research examples.",
         "F 70/70 conditional is not equivalent to 70 fully accepted original F contracts.",
         "H preflight explicitly is not an independent H exit audit.",
       ],
       "derived_output_SHA256":saved,
    }
    save(O_JSON,(json.dumps(report,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode(),verify)
    md=[
      "# INT-4-G5 다층 원본 범위 한정 최종 판정",
      "",
      "| 원장 | VERIFIED (정적 출처·원본 화소 한정) | CONDITIONAL | HOLD | NOT_APPLICABLE | 합계 |",
      "|---|---:|---:|---:|---:|---:|",
      "| A 모델 | 16,466 | 48 | 0 | 58 | 16,572 |",
      "| B/C 면 | 585,969 | 6,343 | 0 | 0 | 592,312 |",
      "| D 모드 상태 | 0 | 1,157 | 1 | 0 | 1,158 |",
      "| E 역사 발견 | 0 | 14 | 0 | 7 | 21 |",
      "| F 실제 게임 검증 목표 | 0 | 70 | 0 | 0 | 70 |",
      "",
      "A 16,466 정적 VERIFIED는 기존 16,460과 G4 HC6 기초 GUI/부모 템플릿 출처 역할 근거를 합한 것이며, 과거 A HOLD 6개 파일은 수정하지 않았습니다.",
      "B/C 585,969 verified는 원본 화소/정적 source 연결에 한정. 6,343 예외는 원본 면·텍스처 슬롯·UV 정확 키로 대조됐지만 실제 게임에서 깨진 면이라는 뜻이 아닙니다.",
      "D HOLD 1은 unused/white_awning 원본 모델 참조 미해결 4건을 포함합니다.",
      "E N/A 7은 보편 모델링 규칙으로 승격 금지한 역사 반례이며, 삭제/오류 취급하지 않습니다.",
      "F 70개는 조건부 F2 증거에 연결되지만 필수 계약 모두 완결된 F PASS는 0입니다.",
      "**G 최종 무조건 승인 0, H 독립 종료 0, INT5 의미 및 INT6 저작물 AI 학습/재배포 권리 승인 0.**",
      "H 8개 게이트는 예비심사 항목으로만 기록하고 실제 H 감사를 대신하지 않습니다.",
      "",
    ]
    save(O_MD,("\n".join(md)+"\n").encode(),verify)
    print(json.dumps({"status":report["status"],"counts":report["dispositions"],
                      "C_exact_match":report["C_exception_exact_source_face_matching"]},ensure_ascii=False))
    return report
def main():
    p=argparse.ArgumentParser();p.add_argument("--verify",action="store_true")
    a=p.parse_args();build(a.verify)
if __name__=="__main__":main()
