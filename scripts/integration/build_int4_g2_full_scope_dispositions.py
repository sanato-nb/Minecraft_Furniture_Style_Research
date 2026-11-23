#!/usr/bin/env python3
"""INT-4-G2: independently cross-join frozen A/B/C/D/E/F source ledgers.

This is an exact original-evidence SOURCE applicability and exception audit.
It is NOT new Minecraft live observation, atlas/UV approval, an AI training
license, or a final G/H exit. Each count retains its own population.
"""
from __future__ import annotations
import argparse,csv,gzip,hashlib,io,json
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PINS={
 "INT4_G1_SOURCE_LAYER_GATE_SUMMARY_V1.json":"9772bcb7bb3243b7f0d166b99d7f602c23a2e0fe",
 "INT4_A_ADJUDICATION_SUMMARY_V2.json":"621cce07862bbc5bb051809eeeef8df9607c0a37",
 "INT4_A_EXCEPTION_DISPOSITIONS_V2.csv":"26c5764a37700626f3bfadba01fc229e49aadfc4",
 "INT4_C_SOURCE_AUDIT_V1.json":"ace40f7aab319f61dc4d614f52aa01cae12f6cc0",
 "INT4_D_SOURCE_AUDIT_V1.json":"7617caf488ef2fd2a115c3ae1f3f7350fe1ba8d8",
 "INT4_D_1158_STATE_DISPOSITIONS_V1.csv":"db3ebc8b8df039bc334701bcf1f559fd48fd68c5",
 "INT4_E_21_FINDING_DISPOSITIONS_V1.csv":"ff3025ffc9d924cc00b7d58cf05212b6dc5e08da",
 "INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv":"0cfbf3b1b174efc968de35c8466e2af8a9cd41c7",
}
COMP={
 "INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":("9bf1dc45cca4d85d4bf7ebdc60755910801adf1664b94ee38b28eb9082e3aeb3",16572),
 "INT4_B_592312_FACE_PROVENANCE_V1.csv.gz":("d5fe7708a194db723b49d4dbfe8bfd256a9c1bfbd00001d1ed17e1f9d760c578",592312),
 "INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz":("1bd4b9a670eb05a34be93d2569d22519f06463d8d52de3cf560859e68c6517cc",6343),
 "INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz":("d8a007500262cee3e7ae2e24f1891ed640f2eac33cff6cd779a0352ece191301",78456),
}
A_OUT=I/"INT4_G2_16572_MODEL_SOURCE_SCOPE_DISPOSITIONS_V1.csv.gz"
B_OUT=I/"INT4_G2_592312_FACE_SOURCE_APPLICABILITY_V1.csv.gz"
C_OUT=I/"INT4_G2_6343_FACE_PIXEL_EXCEPTION_CROSSWALK_V1.csv.gz"
D_OUT=I/"INT4_G2_1158_STATE_RUNTIME_SOURCE_GATES_V1.csv"
E_OUT=I/"INT4_G2_21_FINDING_F70_EVIDENCE_GATES_V1.csv"
F_OUT=I/"INT4_G2_70_F_CONTRACT_NONAPPROVAL_V1.csv"
AUDIT=I/"INT4_G2_SOURCE_CROSSJOIN_AUDIT_V1.json"
REPORT=I/"INT4_G2_EXCEPTION_IMPACT_REPORT_V1.md"

def sha256(b):return hashlib.sha256(b).hexdigest()
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def pinned(name):
    b=(ROOT/I/name).read_bytes()
    assert gitblob(b)==PINS[name],("SOURCE_SHA_DRIFT",name,gitblob(b))
    return b
def fromjson(name):return json.loads(pinned(name))
def csvrows(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def csvout(rows,fields):
    s=io.StringIO(newline="")
    w=csv.DictWriter(s,fieldnames=fields,lineterminator="\n",extrasaction="ignore")
    w.writeheader();w.writerows(rows)
    return s.getvalue().encode("utf-8")
def writebytes(path,data,verify):
    p=ROOT/path
    if verify:
        assert p.is_file() and p.read_bytes()==data,("NONDETERMINISTIC_OUTPUT",str(path))
    else:
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(data)
    return {"sha256":sha256(data),"size_bytes":len(data)}
def readgz(name):
    b=(ROOT/I/name).read_bytes()
    expected,count=COMP[name]
    assert sha256(b)==expected,("GZIP_ORIGINAL_SHA_DRIFT",name,sha256(b))
    with gzip.GzipFile(fileobj=io.BytesIO(b)) as g:
        result=list(csv.DictReader(io.TextIOWrapper(g,encoding="utf-8-sig",newline="")))
    assert len(result)==count,("GZIP_ORIGINAL_ROWS_CHANGED",name,len(result))
    return result
def plain(s):return str(s or "").strip()
def face_key(r):
    return (plain(r["model_key"]),plain(r["element_index"]),plain(r["face_direction"]))
def exact_key(r,from_c=False):
    return (*face_key(r),
            plain(r["source_slot"] if from_c else r["source_texture_slot"]),
            plain(r["uv"] if from_c else r["source_uv"]))
def disposition_for_A(val):
    return {
      "VERIFIED_REUSED_STATIC_SCOPE":"VERIFIED_STATIC_SOURCE_ONLY",
      "CONDITIONAL_STATIC_SOURCE_EXCEPTION":"CONDITIONAL_MISSING_PARENT_STATIC_UNREACHABLE_DYNAMIC_UNKNOWN",
      "HOLD_MODEL_USAGE_AND_RENDER_PATH":"HOLD_BASE_MODEL_USAGE_UNKNOWN",
      "NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY":"NOT_APPLICABLE_GENERATED_ITEM_CUBOID",
    }[val]

def build(verify=False):
    old=fromjson("INT4_G1_SOURCE_LAYER_GATE_SUMMARY_V1.json")
    A=fromjson("INT4_A_ADJUDICATION_SUMMARY_V2.json")
    C=fromjson("INT4_C_SOURCE_AUDIT_V1.json")
    D=fromjson("INT4_D_SOURCE_AUDIT_V1.json")
    E=csvrows(pinned("INT4_E_21_FINDING_DISPOSITIONS_V1.csv"))
    F=csvrows(pinned("INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"))
    oldexc=csvrows(pinned("INT4_A_EXCEPTION_DISPOSITIONS_V2.csv"))
    models=readgz("INT4_A_MODEL_DISPOSITIONS_V2.csv.gz")
    faces=readgz("INT4_B_592312_FACE_PROVENANCE_V1.csv.gz")
    exceptions=readgz("INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz")
    options=readgz("INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz")
    assert old["status"]=="PASS_G1_ALL_FROZEN_SOURCE_SCOPE_AND_F70_CROSS_LINKED_G_FINAL_EXIT_NOT_ASSESSED"
    assert len(E)==21 and len(F)==70 and len(oldexc)==112
    Amap={r["model_key"]:r for r in models}
    assert len(Amap)==len(models)==A["all_model_source_paths"]==16572
    assert Counter(r["int4_a_review_result"] for r in models)==A["review_results"]
    assert Counter(r["exception_reason"] for r in exceptions)==C["face_exception_reason_counts"]
    assert len({r["target_id"] for r in F})==70
    assert all(r["final_disposition"].startswith("CONDITIONAL") and
               r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in F)
    fcase={r["target_id"]:r for r in F}
    assert sum(v["target_kind"]=="HISTORICAL_1_5_CASE" for v in F)==62
    bcounts=Counter()
    bkey=Counter()
    bfull=Counter()
    bad_b_source_sha=Counter()
    for r in faces:
        key=r["model_key"]
        if key not in Amap:
            bad_b_source_sha["MODEL_ABSENT_IN_A"]+=1
            continue
        bcounts[key]+=1
        bkey[face_key(r)]+=1
        bfull[exact_key(r)]+=1
        if plain(r["model_source_sha"])!=plain(Amap[key]["source_sha"]):
            bad_b_source_sha["MODEL_SOURCE_SHA_MISMATCH"]+=1
    assert sum(bcounts.values())+bad_b_source_sha["MODEL_ABSENT_IN_A"]==592312
    cby_model=Counter()
    cface_match=Counter()
    c_rows=[]
    for row in exceptions:
        model=row["model_key"]
        cby_model[model]+=1
        exact=bfull[exact_key(row,True)]
        coarse=bkey[face_key(row)]
        relation=("FACE_SOURCE_SLOT_UV_MATCH" if exact else
                  "FACE_POSITION_ONLY_SLOT_UV_DIFFERENT" if coarse else
                  "MODEL_ONLY_B_FACE_KEY_MISSING" if model in Amap else
                  "MODEL_NOT_IN_A_HISTORY")
        cface_match[relation]+=1
        a=Amap.get(model)
        c_rows.append({
         "model_key":model,"source_face_model_original_sha":row["model_original_sha"],
         "source_model_path":row["model_path"],
         "element_index":row["element_index"],"face_direction":row["face_direction"],
         "source_slot":row["source_slot"],"uv":row["uv"],
         "exception_reason":row["exception_reason"],
         "exception_subtype":row["exception_subtype"],
         "source_texture_id":row["texture_resource_id"],
         "pinned_original_png_path":row["pinned_original_png_path"],
         "C_historical_disposition":row["int4_c_disposition"],
         "B_source_face_relation":relation,
         "B_face_key_count":coarse,
         "B_exact_source_face_key_count":exact,
         "A_model_review_scope":a["int4_a_review_result"] if a else "UNMATCHED",
         "D_original_direct_selected":row["direct_model_blockstate_selected"],
         "G2_face_pixel_disposition":"CONDITIONAL_PINNED_PIXEL_SOURCE_EXCEPTION_NOT_PROVEN_RENDER_DEFECT",
         "G2_runtime_visual_approved":"false",
         "required_followup":row["followup"],
        })
    assert sum(cface_match.values())==6343 and sum(cby_model.values())==6343
    # D is an explicit model option reference edge. Reopen all 78,456 source
    # options and verify source_sha against the original model ledger where
    # identity can be represented; preserve all unresolved/nonlocal refs.
    dstate_count=Counter()
    drefs=Counter()
    d_links=Counter()
    state_issues=defaultdict(Counter)
    for row in options:
        state=row["state_id"]
        dstate_count[state]+=1
        status=row["reference_status"]
        drefs[status]+=1
        if status=="LOCAL":
            a=Amap.get(row["original_model_key"])
            if a is None:
                rel="A_MODEL_KEY_NOT_FOUND"
            elif plain(a["source_sha"])!=plain(row["original_model_source_sha"]):
                rel="A_D_MODEL_SOURCE_SHA_CONFLICT"
            else:
                rel="A_D_PINNED_MODEL_SHA_JOIN"
        elif status=="VANILLA_JAR":
            rel="VANILLA_MODEL_OUTSIDE_MOD_A_PROVENANCE"
        elif status=="UNRESOLVED_MODEL_REF":
            rel="UNRESOLVED_ORIGINAL_MODEL_REFERENCE"
        else:
            rel="UNEXPECTED_REFERENCE_STATUS"
        d_links[rel]+=1
        if rel!="A_D_PINNED_MODEL_SHA_JOIN":
            state_issues[state][rel]+=1
        if row["parent_missing"] in ("true","True","1"):
            state_issues[state]["PARENT_MISSING_OPTION"]+=1
        if plain(row["selected_model_source_pixel_exception_rows"]).isdigit() and int(row["selected_model_source_pixel_exception_rows"])>0:
            state_issues[state]["C_SOURCE_PIXEL_EXCEPTION_OPTION"]+=1
    assert len(dstate_count)==D["state_denominator"]==1158
    assert sum(dstate_count.values())==78456
    assert dict(drefs)==D["original_reference_status_counts"],(drefs,D["original_reference_status_counts"])
    assert not d_links["UNEXPECTED_REFERENCE_STATUS"]
    original_D=(ROOT/I/"INT4_D_1158_STATE_DISPOSITIONS_V1.csv").read_bytes()
    d_states=csvrows(original_D)
    assert len(d_states)==1158
    assert len({r["state_id"] for r in d_states})==1158
    state_output=[]
    d_source_status=Counter()
    for row in d_states:
        key=row["state_id"]
        assert dstate_count[key]==int(row["option_count"]),("D_OPTION_SOURCE_CENSUS_DRIFT",key)
        count=state_issues[key]
        result=("HOLD_SOURCE_MODEL_REFERENCE_AND_RELEASE" if
                count["UNRESOLVED_ORIGINAL_MODEL_REFERENCE"] or
                count["A_MODEL_KEY_NOT_FOUND"] or count["A_D_MODEL_SOURCE_SHA_CONFLICT"]
                else "CONDITIONAL_DECLARED_SELECTOR_NOT_RUNTIME_PROVEN")
        d_source_status[result]+=1
        state_output.append({
          "state_id":key,"mod":row["mod"],"minecraft":row["minecraft"],
          "state_original_path":row["source_path"],"state_source_SHA":row["source_sha"],
          "original_kind":row["kind"],"verified_option_row_count":dstate_count[key],
          "historic_anomaly_option_count":row["anomaly_option_count"],
          "model_reference_missing_count":count["UNRESOLVED_ORIGINAL_MODEL_REFERENCE"],
          "A_model_key_absent_count":count["A_MODEL_KEY_NOT_FOUND"],
          "A_D_model_sha_conflict_count":count["A_D_MODEL_SOURCE_SHA_CONFLICT"],
          "source_parent_missing_selected_options":count["PARENT_MISSING_OPTION"],
          "source_C_pixel_exception_selected_options":count["C_SOURCE_PIXEL_EXCEPTION_OPTION"],
          "vanilla_reference_option_count":count["VANILLA_MODEL_OUTSIDE_MOD_A_PROVENANCE"],
          "source_link_disposition":result,
          "actual_registered_state_reached":"NOT_PROVEN_EACH_ONE",
          "release_equivalence":"NOT_VERSION_WIDE_PROVEN",
          "G2_final_G_stage_approved":"false",
          "required_followup":row["next_step"],
        })
    # Source model status is a provenance-level result, NOT a live render
    # success count. Keep all historically generated-item N/A and HOLD rows.
    model_output=[]
    amodel_scope=Counter()
    for r in models:
        scope=disposition_for_A(r["int4_a_review_result"])
        amodel_scope[scope]+=1
        model_output.append({
          "model_key":r["model_key"],"mod":r["mod"],"minecraft":r["minecraft"],
          "resource_id":r["resource_id"],"original_source_path":r["source_path"],
          "original_source_SHA":r["source_sha"],"original_source_hash_kind":r["source_hash_kind"],
          "parent_status":r["parent_status"],"geometry_status":r["geometry_status"],
          "A_historical_review":r["int4_a_review_result"],
          "B_expanded_source_faces_observed":bcounts[r["model_key"]],
          "C_pixel_exception_source_faces":cby_model[r["model_key"]],
          "B_source_model_SHA_conflict_total":0,
          "G2_source_scope_disposition":scope,
          "runtime_dynamic_model_use_proven":"false",
          "full_release_model_semantic_UV_approved":"false",
          "followup":r["next_action"],
        })
    # Large B face census exported by original provider/model key. No automatic
    # one-to-one C intersection: model element/face keys can be ambiguous.
    b_output=[]
    face_scope=Counter()
    for row in faces:
        key=row["model_key"]
        a=Amap.get(key)
        model_scope=disposition_for_A(a["int4_a_review_result"]) if a else "CONFLICT_NO_A_MODEL"
        conflict=(not a or plain(row["model_source_sha"])!=plain(a["source_sha"]))
        # C exception evidence is retained at its own original face level;
        # do not infer a pixel/UV failure from the model key alone.
        s="CONFLICT_A_B_SOURCE_SHA" if conflict else "VERIFIED_STATIC_FACE_PROVENANCE_ONLY"
        face_scope[s]+=1
        b_output.append({
           "model_key":key,"source_model_SHA":row["model_source_sha"],
           "provider_original_source_SHA":row["provider_source_sha"],
           "element_index":row["element_index"],"face_direction":row["face_direction"],
           "texture_slot":row["source_texture_slot"],"source_uv":row["source_uv"],
           "B_original_evidence_method":row["evidence_method"],
           "A_model_static_scope":model_scope,
           "G2_face_provenance":s,
           "G2_live_baked_UV_or_3D_render_approved":"false",
        })
    finding_gate=Counter()
    finding_output=[]
    for r in E:
        caseids=r["source_case_keys"].split("|")
        assert len(caseids)==int(r["source_case_count"]) and set(caseids)<=set(fcase)
        assert all(fcase[c]["target_kind"]=="HISTORICAL_1_5_CASE" for c in caseids)
        assert all(fcase[c]["image_sha256s"] and
                   fcase[c]["final_disposition"].startswith("CONDITIONAL") for c in caseids)
        res=("NOT_APPLICABLE_AS_UNIVERSAL_RULE_SCOPE_LIMIT_STILL_VALUABLE_AS_COUNTEREXAMPLE"
             if r["original_INT2_disposition"]=="SCOPE_LIMIT_ONLY"
             else "CONDITIONAL_MEASURED_HISTORIC_SOURCE_REVIEW_REQUIRED")
        finding_gate[res]+=1
        assert r["universal_modeling_rule_approved"]=="false"
        finding_output.append({
            "finding_id":r["finding_id"],"classification":r["classification"],
            "axis":r["axis"],"source_case_ids":"|".join(caseids),
            "F_conditional_case_evidence_links":len(caseids),
            "historical_source_case_SHA_linkage":r["case_source_SHA_linkage"],
            "E_historical_claim_review":r["original_INT2_disposition"],
            "G2_scoped_finding_disposition":res,
            "G2_new_general_rule_approved":"false",
            "G2_INT5_semantic_approved":"false","G2_INT6_rights_approved":"false",
            "followup":r["followup"],
        })
    assert sorted(finding_gate.values())==[7,14]
    f_out=[]
    for r in F:
        f_out.append({
           "target_id":r["target_id"],"target_kind":r["target_kind"],
           "minecraft_version":r["minecraft_version"],"block":r["block"],
           "original_acceptance_contract":r["original_acceptance_contract"],
           "F_historic_status":r["final_disposition"],
           "F_original_run_ids":r["image_run_ids"],
           "F_original_image_sha256s":r["image_sha256s"],
           "G2_evidence_disposition":"CONDITIONAL_PREVIOUS_ACTUAL_F2_NOT_COMPLETE_FULL_F_CONTRACT",
           "full_F_approved":"false",
           "full_G_approved":"false",
           "remaining_contract_risk":r["additional_required_before_full_acceptance"],
        })
    assert len(f_out)==70
    output_data={
        A_OUT:gzip.compress(csvout(model_output,list(model_output[0])),mtime=0),
        B_OUT:gzip.compress(csvout(b_output,list(b_output[0])),mtime=0),
        C_OUT:gzip.compress(csvout(c_rows,list(c_rows[0])),mtime=0),
        D_OUT:csvout(state_output,list(state_output[0])),
        E_OUT:csvout(finding_output,list(finding_output[0])),
        F_OUT:csvout(f_out,list(f_out[0])),
    }
    saved={}
    for path,data in output_data.items():
        saved[path.name]=writebytes(path,data,verify)
    summary={
       "schema":"MCFR_INT4_G2_FULL_SCOPE_CONSERVATIVE_DISPOSITIONS/v1",
       "status":"PASS_G2_PINNED_A_B_C_D_E_F_SOURCE_CROSSJOIN_WITH_REMAINING_LIMITS_NOT_FINAL_G",
       "original_git_blob_pins":PINS,
       "source_compressed_sha256":{k:v[0] for k,v in COMP.items()},
       "population_checks":{
          "models":len(models),"faces":len(faces),"pixel_source_exceptions":len(exceptions),
          "mod_state_options":len(options),"mod_state_sources":len(d_states),
          "historic_findings":len(E),"F_verification_units":len(F),
       },
       "A_model_source_dispositions":dict(amodel_scope),
       "B_face_source_dispositions":dict(face_scope),
       "B_unknown_A_model_rows":bad_b_source_sha["MODEL_ABSENT_IN_A"],
       "B_source_sha_mismatch_rows":bad_b_source_sha["MODEL_SOURCE_SHA_MISMATCH"],
       "C_historic_pixel_source_reason_counts":dict(Counter(x["exception_reason"] for x in exceptions)),
       "C_B_face_crosslink_status":dict(cface_match),
       "C_exception_models_unique":len(cby_model),
       "D_reference_status":dict(drefs),
       "D_option_to_A_provenance":dict(d_links),
       "D_state_source_gate_counts":dict(d_source_status),
       "D_state_source_exception_6_from_prior_audit":6,
       "E_findings_disposition":dict(finding_gate),
       "F_exact_case_conditional":len(F),
       "F_unconditional_full_exit_approved":0,
       "G_final_exit_approved":0,"H_final_exit_approved":0,
       "INT5_semantics_approved":0,"INT6_AI_training_rights_approved":0,
       "misinterpretation_guards":[
          "A static-source VERIFIED is NOT actual in-game model success.",
          "B original face provenance is NOT an observed baked atlas or UV live render.",
          "C original pixel-source exception is NOT a proven broken face on screen.",
          "D selector source identity is NOT registered reachability nor version-wide equivalence.",
          "F 70/70 conditional proof is NOT full-F PASS.",
          "E 7 negative scope cases must not become universal modeling rules.",
          "F11F study Git self-built Fabric 4.0.3 is NOT official published 4.0.3 NeoForge.",
          "No model screenshot, upstream original JAR, or semantics newly observed in G2.",
       ],
       "artifacts":saved,
    }
    raw=json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2).encode()+b"\n"
    saved[AUDIT.name]=writebytes(AUDIT,raw,verify)
    report=("\n".join([
        "# INT-4-G2 원본 전체 범위 개별 판정/교차 연결 감사",
        "",
        "원본 A/B/C/D 압축 원장 4개를 재개방해 행별 검증; E 21·F 70과 연결. 이것은 G의 정적 범위 근거를 평가하는 작업이며 실제 게임 전체 승인이 아니다.",
        "",
        "- A 16,572개 모델: 정적 출처 검증 16,460, parent 누락 조건부 48, 모델 등록·렌더 경로 HOLD 6, generated item 58 N/A.",
        "- B 592,312면: 역사 원본 geometry/UV 선언 출처 재확인. Minecraft 실제 baked UV, 투명/틴트/라이팅 증명 아님.",
        "- C 6,343 출처 화소 예외: 역사 오류 유형과 A/B 모델/면 출처의 키 단위 대조를 기록. 파일 누락·unbound template slot은 게임 버그라고 확정하지 않음.",
        "- D 78,456 선택 옵션을 모델 SHA에 맞춰 교차하고 1,158 상태별 runtime 등록·릴리스 동등성 gate를 분리.",
        "- E 21건 연구 발표: 조건부 후보 14, 보편 규칙 N/A·반례 7. F 사례 62개 중 각 발견에 인용된 상태만 연결.",
        "- F 70건: 조건부 원본 F2와 최종 게임/UV·의미/권리 승인 사이를 분리.",
        "- **전체 G/H 종료 승인 0, INT5 의미 승인 0, INT6 저작권/AI 학습 승인 0.**",
        "",
    ])+"\n").encode()
    writebytes(REPORT,report,verify)
    print(json.dumps({"status":summary["status"],"populations":summary["population_checks"],
                      "A":summary["A_model_source_dispositions"],"C_B":summary["C_B_face_crosslink_status"],
                      "D":summary["D_option_to_A_provenance"],"E":summary["E_findings_disposition"],
                      "outputs":list(saved)},ensure_ascii=False))
    return summary

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    build(verify=args.verify)
if __name__=="__main__":
    main()
