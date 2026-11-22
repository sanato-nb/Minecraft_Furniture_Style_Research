#!/usr/bin/env python3
"""INT-4-E: join fixed 1-5 cases/applications/findings to INT-4 A/C/D evidence.

New work: per-key cross-stage correspondence, provenance, exception & scope
recording. Historical independent original JSON/PNG audits are source evidence;
this run does NOT reopen upstream archives or redo F2/AI/rights approval.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import gzip
import hashlib
import io
import json
import lzma
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[2]
B="research/furniture_mods/phase_1-5/B/"
C="research/furniture_mods/phase_1-5/C/"
E="research/furniture_mods/phase_1-5/E/"
F="research/furniture_mods/phase_1-3/F/"
I="project/integration/"
FILES={
    B+"CASES.csv":"aebf449326b1e015c91b40417dde6e3e2dddd4f3",
    B+"APPLICATIONS.csv":"56e6f4c21c50714b97079ec61f7219bea845f179",
    B+"B_AUDIT.json":"856fe5e4407187f9604a32c33007c84d19188ec3",
    B+"INDEPENDENT_AUDIT.json":"3fbc5151f9fb3fdc22100c5d991fb6d5d5f41c93",
    C+"CROSS_CATEGORY_FINDINGS.csv":"6c4964c64dc738fe89f859982c17308f2359e2b0",
    C+"C_AUDIT.json":"cc0ad68549e90d556efe9b37fcd33a8b2f550174",
    E+"PHASE2_HANDOFF.csv":"466d5abcd56c93d397fbe5b51223e2dfb6d026db",
    E+"review_conditions.csv":"5149aa27ad46009b72017b3e263978d77f78abcb",
    E+"E_AUDIT.json":"0dfba78e0832182ea1b3b05fe4eb4b3ed6d29d75",
    E+"INDEPENDENT_AUDIT.json":"56db0f8e8950f4d54b55b0d7d171a0bb7b91b7aa",
    F+"furniture_research.sqlite.xz":"e54839615278dba39cadb463b9988e0371d37ea9",
    I+"INT2_1_5_SUMMARY.json":"e139ed9babe08cfd0b3d842445274dd04800877d",
    I+"INT2_1_5_21_FINDING_CHECKS.csv":"5b05951f9f20509df1ad17e78cabb06e8137b22f",
    I+"INT3_KNOWLEDGE_SUMMARY.json":"90724c37361f96367429b6ca6443ccc5c8768fa9",
    I+"INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":"9b1baf3e3756e44bbe94759b928c2cd30f98cac1",
    I+"INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz":"a23b2adba91b604dfbce6c4ef06cc25935a66e56",
    I+"INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz":"26dae26cfde72566b77906565ec94f9d803b4073",
    I+"INT4_D_SOURCE_AUDIT_V1.json":"7617caf488ef2fd2a115c3ae1f3f7350fe1ba8d8",
    I+"INT4_F_RENDER_TARGETS_V1.csv":"bf5d2caa3bfed68cec7cde9f2771e2b6f7944c92",
}
CASE_FIELDS=[
 "case","cohort","minecraft","category","block","historical_case_source_blob",
 "historical_source_applications","crosschecked_application_rows",
 "historical_elements","crosschecked_application_elements",
 "historical_faces","crosschecked_application_faces",
 "historical_geometry_status_counts","selected_model_ids","selected_provider_ids",
 "original_model_sha_set","original_blockstate_sha_set",
 "int4_d_mod_state_join","int4_d_option_count","int4_c_exception_affected_applications",
 "prior_int3_source_link_scope","original_F2_target_state",
 "new_actual_game_F2_review_status","research_disposition","followup"
]
APP_FIELDS=[
 "case","cohort","minecraft","category","original_block","original_state",
 "rule_index","option_index","model_key_or_path","provider_key_or_path",
 "original_state_path","original_state_sha","original_model_path",
 "original_model_sha","original_provider_path","original_provider_sha",
 "original_model_hash_kind","historical_declared_elements",
 "historical_declared_faces","historical_x","historical_y","historical_uvlock",
 "historical_weight","int4_d_option_join","int4_d_selected_model_key",
 "int4_d_state_sha_match","int4_d_model_sha_match","int4_d_x_y_uvlock_weight_match",
 "int4_a_model_source_sha_match","int4_a_static_geometry_elements",
 "int4_a_static_geometry_faces","int4_c_face_exception_count_for_model",
 "int4_c_face_exception_reasons","pinned_F_model_sha_match",
 "pinned_F_provider_sha_match","pinned_F_geometry_count_match",
 "historical_INT2_original_source_verification",
 "new_original_asset_bytes_reopened","in_game_model_render_newly_verified",
 "evidence_scope","disposition","followup"
]
FINDING_FIELDS=[
 "finding_id","category","classification","axis","source_case_keys",
 "source_case_count","source_cohorts","historical_measurement_json",
 "historical_observation","historical_scope_limit",
 "historical_E_review_condition","historical_E_runtime_checks",
 "original_INT2_check_status","original_INT2_disposition",
 "case_keys_integrity","case_source_SHA_linkage",
 "application_linkage","int4_d_mod_state_scope","int4_c_face_exception_case_count",
 "research_disposition","universal_modeling_rule_approved",
 "int5_semantic_approved","int6_rights_approved",
 "runtime_retested_this_run","followup"
]
DISCREPANCY_FIELDS=["layer","resource_key","field","expected","observed","reason","handling"]
CLASSES={"MOD_SPECIFIC":5,"MULTI_MOD_SHARED":3,"UNVERIFIED_OR_COUNTEREXAMPLE":7,"VANILLA_SHARED":6}
HANDOFF={"CANDIDATE_REQUIRES_REVIEW":14,"SCOPE_LIMIT_ONLY":7}


def git_blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def pin(path):
    raw=(ROOT/path).read_bytes()
    actual=git_blob(raw)
    assert actual==FILES[path],("PINNED_RESEARCH_BLOB_CHANGED",path,actual,FILES[path])
    return raw


def rows(path):
    b=pin(path)
    if path.endswith(".gz"):
        b=gzip.decompress(b)
    elif path.endswith(".xz"):
        b=lzma.decompress(b)
    return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))


def jdata(path):
    return json.loads(pin(path).decode("utf-8-sig"))


def keyed(table,fn,name):
    lookup={}
    for record in table:
        key=fn(record)
        assert key not in lookup,("DUPLICATE",name,key)
        lookup[key]=record
    return lookup


def write_csv(table,fields):
    f=io.StringIO(newline="")
    w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
    w.writeheader()
    w.writerows(table)
    return f.getvalue().encode("utf-8")


def preserve_classification(classification,disposition):
    assert classification in CLASSES
    assert disposition in HANDOFF
    if classification=="UNVERIFIED_OR_COUNTEREXAMPLE":
        assert disposition=="SCOPE_LIMIT_ONLY"
        return "SCOPE_LIMIT_ONLY_NOT_UNIVERSAL_MODELING_RULE"
    assert disposition=="CANDIDATE_REQUIRES_REVIEW"
    return "CONDITIONAL_RESEARCH_CANDIDATE_NOT_AI_APPROVED"


def application_decision(cohort,d_join,has_pixel_exceptions):
    if cohort=="VANILLA":
        assert d_join=="NOT_IN_1158_MOD_BLOCKSTATE_COHORT"
        return "VANILLA_1_21_11_ORIGINAL_SOURCE_AUDITED_HISTORICALLY"
    assert cohort in ("AF","HC","MACAW")
    if d_join!="SOURCE_SELECTED_MODEL_EXACT_MATCH":
        return "HOLD_UNMATCHED_MOD_SOURCE_OPTION"
    if has_pixel_exceptions:
        return "CONDITIONAL_MOD_SOURCE_MODEL_WITH_PIXEL_EXCEPTION"
    return "PINNED_MOD_STATE_MODEL_SOURCE_JOINED_RUNTIME_PENDING"


def build():
    b_audit=jdata(B+"B_AUDIT.json")
    b_independent=jdata(B+"INDEPENDENT_AUDIT.json")
    c_audit=jdata(C+"C_AUDIT.json")
    e_audit=jdata(E+"E_AUDIT.json")
    e_independent=jdata(E+"INDEPENDENT_AUDIT.json")
    prior=jdata(I+"INT2_1_5_SUMMARY.json")
    knowledge=jdata(I+"INT3_KNOWLEDGE_SUMMARY.json")
    dsummary=jdata(I+"INT4_D_SOURCE_AUDIT_V1.json")
    assert all(x["status"]=="PASS" for x in (
        b_audit,b_independent,c_audit,e_audit,e_independent))
    assert prior["status"]=="PASS_PINNED_COMPARISON_21_CLAIMS_SOURCED_AND_REDERIVED"
    assert knowledge["table_counts"]["study_case"]==62
    assert knowledge["table_counts"]["case_application"]==74
    assert knowledge["table_counts"]["comparison_finding"]==21
    assert knowledge["case_source_model_links"]=={"MODEL_LINKED":52,"UNMATCHED_SCOPE":22}
    assert dsummary["option_rows"]==78456

    case_rows=rows(B+"CASES.csv")
    app_rows=rows(B+"APPLICATIONS.csv")
    findings=rows(C+"CROSS_CATEGORY_FINDINGS.csv")
    handoffs=rows(E+"PHASE2_HANDOFF.csv")
    checks=rows(I+"INT2_1_5_21_FINDING_CHECKS.csv")
    review=rows(E+"review_conditions.csv")
    model_a=rows(I+"INT4_A_MODEL_DISPOSITIONS_V2.csv.gz")
    faces_c=rows(I+"INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz")
    options_d=rows(I+"INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz")
    ftargets=rows(I+"INT4_F_RENDER_TARGETS_V1.csv")
    assert (len(case_rows),len(app_rows),len(findings),len(handoffs),len(checks))==(62,74,21,21,21)
    assert len(faces_c)==6343 and len(options_d)==78456
    cases=keyed(case_rows,lambda x:x["case"],"CASES")
    findings_idx=keyed(findings,lambda x:x["finding_id"],"C_FINDINGS")
    handoff=keyed(handoffs,lambda x:x["finding_id"],"E_HANDOFF")
    checker=keyed(checks,lambda x:x["finding_id"],"INT2_21_AUDIT")
    reviewer=keyed(review,lambda x:x["finding_id"],"E_REVIEW_CONDITIONS")
    a_index=keyed(model_a,lambda x:x["model_key"],"A_16572_MODELS")
    d_index=keyed(options_d,lambda x:(
        x["mod"],x["state_id"],int(x["rule_index"]),int(x["option_index"])),"D_78456_OPTIONS")
    ft_index=keyed([x for x in ftargets if x["target_kind"]=="HISTORICAL_1_5_CASE"],
                   lambda x:x["target_id"],"F_62_TARGETS")
    assert len(ft_index)==62 and set(ft_index)==set(cases)
    assert set(findings_idx)==set(handoff)==set(checker)==set(reviewer)
    assert {c for c in cases if c.startswith("V")}=={f"V{i:02d}" for i in range(1,16)}
    assert {c for c in cases if c.startswith("S")}=={f"S{i:02d}" for i in range(1,48)}
    assert len(a_index)==16572
    assert all(c["cohort"]=="VANILLA" if k.startswith("V") else c["cohort"]!="VANILLA" for k,c in cases.items())
    assert sum(int(x["applications"]) for x in case_rows)==74
    assert sum(int(x["elements"]) for x in case_rows)==390
    assert sum(int(x["faces"]) for x in case_rows)==1844
    assert len([a for a in app_rows if a["cohort"]=="VANILLA"])==22
    assert len([a for a in app_rows if a["cohort"]!="VANILLA"])==52
    assert len({(a["case"],int(a["rule_index"]),int(a["option_index"])) for a in app_rows})==74

    counts_c=Counter(x["model_key"] for x in faces_c)
    reasons_c=defaultdict(Counter)
    for row in faces_c:
        a=a_index[row["model_key"]]
        assert a["source_sha"]==row["model_original_sha"]
        assert a["resource_id"]==row["model_resource_id"]
        reasons_c[row["model_key"]][row["exception_reason"]]+=1
    assert sum(counts_c.values())==6343

    db=sqlite3.connect(":memory:")
    app_final=[]
    mod_d_links=0
    mod_f_links=0
    exception_case_count=0
    per_case=defaultdict(list)
    reconciled_element_count=0
    reconciled_face_count=0
    try:
        db.deserialize(lzma.decompress(pin(F+"furniture_research.sqlite.xz")))
        assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        assert db.execute("PRAGMA foreign_key_check").fetchall()==[]
        for b in app_rows:
            case=cases[b["case"]]
            mod=b["cohort"]
            is_mod=mod!="VANILLA"
            assert (mod,b["block"],b["minecraft"],b["category"])==(
                case["cohort"],case["block"],case["minecraft"],case["category"])
            assert b["state_sha"] and b["model_sha"]
            assert b["model_path"] and b["state_path"]
            assert int(b["weight"])==1
            assert int(b["uvlock"]) in (0,1)
            special_bed=b["case"]=="V11" and b["cohort"]=="VANILLA"
            if special_bed:
                # The vanilla bed is rendered outside the ordinary cuboid
                # model path: no provider, zero regular elements and faces.
                assert b["block"]=="white_bed" and b["geometry_status"]=="NO_ORDINARY_ELEMENTS"
                assert not b["provider"] and not b["provider_path"] and not b["provider_sha"]
                assert int(b["elements"])==int(b["faces"])==0
            else:
                assert b["provider_sha"] and b["provider_path"]
                assert b["geometry_status"]=="STATIC_SOURCE"
            model_id=b["model"]
            model_sha=b["model_sha"]
            d_join="NOT_IN_1158_MOD_BLOCKSTATE_COHORT"
            d_state_sha="NOT_APPLICABLE_VANILLA"
            d_model_sha="NOT_APPLICABLE_VANILLA"
            d_rotation="NOT_APPLICABLE_VANILLA"
            a_sha="NOT_APPLICABLE_VANILLA"
            a_el=a_fc=""
            c_exception=0
            c_reason=""
            f_model_sha="NOT_APPLICABLE_VANILLA"
            f_provider_sha="NOT_APPLICABLE_VANILLA"
            f_geo="NOT_APPLICABLE_VANILLA"
            if is_mod:
                # 1-5 B stores the model/provider as F's stable source keys.
                a=a_index.get(model_id)
                assert a is not None,("MOD_MODEL_ABSENT",b["case"],model_id)
                assert a["source_sha"]==model_sha,("MOD_SHA_DRIFT",b["case"],model_id)
                assert a["mod"]==mod
                assert a["source_path"]==b["model_path"],("MOD_PATH_DRIFT",b["case"],model_id)
                a_sha="PASS"
                a_el=a["effective_elements"]
                a_fc=a["effective_faces"]
                dkey=(mod,b["block"],int(b["rule_index"]),int(b["option_index"]))
                d=d_index.get(dkey)
                assert d is not None,("D_OPTION_NOT_FOUND",b["case"],dkey)
                assert d["reference_status"]=="LOCAL"
                assert d["original_model_key"]==model_id
                assert d["original_model_source_sha"]==model_sha
                assert (d["state_path"],d["state_source_sha"])==(
                    b["state_path"],b["state_sha"]),("D_STATE_SHA_MISMATCH",b["case"],dkey)
                assert (int(d["x_original"]),int(d["y_original"]),d["uvlock"],int(d["weight"]))==(
                    int(b["x"]),int(b["y"]),str(bool(int(b["uvlock"]))).lower(),int(b["weight"])),(
                    "D_ROTATION_UVLOCK_MISMATCH",b["case"],dkey)
                d_join="SOURCE_SELECTED_MODEL_EXACT_MATCH"
                d_state_sha=d_model_sha=d_rotation="PASS"
                mod_d_links+=1
                fmod=db.execute(
                    "SELECT m.sha,m.path,g.provider_key,g.element_instances,g.face_instances "
                    "FROM model m JOIN geometry g USING(model_key) WHERE m.model_key=?",(model_id,)).fetchone()
                assert fmod,("F_MODEL_NOT_FOUND",model_id)
                f_model_sha="PASS" if (fmod[0],fmod[1])==(model_sha,b["model_path"]) else "FAIL"
                assert f_model_sha=="PASS",("F_MODEL_SHA_PATH_CHANGED",model_id)
                assert fmod[2]==b["provider"],("F_GEOMETRY_PROVIDER_MISMATCH",b["case"],fmod[2],b["provider"])
                assert (int(fmod[3]),int(fmod[4]))==(int(b["elements"]),int(b["faces"])),(
                    "F_GEOMETRY_COUNT_MISMATCH",b["case"],model_id)
                f_geo="PASS"
                fp=db.execute(
                    "SELECT sha,path FROM model WHERE model_key=?",(b["provider"],)).fetchone()
                assert fp and (fp[0],fp[1])==(b["provider_sha"],b["provider_path"])
                f_provider_sha="PASS"
                mod_f_links+=1
                c_exception=counts_c[model_id]
                c_reason="|".join(f"{k}:{v}" for k,v in sorted(reasons_c[model_id].items()))
            decision=application_decision(mod,d_join,c_exception)
            app_final.append({
                "case":b["case"],"cohort":mod,"minecraft":b["minecraft"],
                "category":b["category"],"original_block":b["block"],"original_state":b["state"],
                "rule_index":b["rule_index"],"option_index":b["option_index"],
                "model_key_or_path":model_id,"provider_key_or_path":b["provider"],
                "original_state_path":b["state_path"],"original_state_sha":b["state_sha"],
                "original_model_path":b["model_path"],"original_model_sha":model_sha,
                "original_provider_path":b["provider_path"],"original_provider_sha":b["provider_sha"],
                "original_model_hash_kind":b["model_hash_kind"],
                "historical_declared_elements":b["elements"],"historical_declared_faces":b["faces"],
                "historical_x":b["x"],"historical_y":b["y"],
                "historical_uvlock":b["uvlock"],"historical_weight":b["weight"],
                "int4_d_option_join":d_join,"int4_d_selected_model_key":model_id if is_mod else "",
                "int4_d_state_sha_match":d_state_sha,"int4_d_model_sha_match":d_model_sha,
                "int4_d_x_y_uvlock_weight_match":d_rotation,
                "int4_a_model_source_sha_match":a_sha,
                "int4_a_static_geometry_elements":a_el,
                "int4_a_static_geometry_faces":a_fc,
                "int4_c_face_exception_count_for_model":c_exception,
                "int4_c_face_exception_reasons":c_reason,
                "pinned_F_model_sha_match":f_model_sha,
                "pinned_F_provider_sha_match":f_provider_sha,
                "pinned_F_geometry_count_match":f_geo,
                "historical_INT2_original_source_verification":"PASS_HISTORIC_74_74_RECHECK_NOT_REEXECUTED",
                "new_original_asset_bytes_reopened":"false",
                "in_game_model_render_newly_verified":"false",
                "evidence_scope":"PINNED_MOD_A_D_EXACT_OPTION_GEOMETRY_MATCH" if is_mod
                else "PINNED_VANILLA_1_5_AND_INT2_PRIOR_SOURCE_AUDIT_ONLY",
                "disposition":decision,
                "followup":"INT4_F_GAME_CLIENT_RELEASE_AND_EXACT_STATE_F2"
            })
            per_case[b["case"]].append(app_final[-1])
            reconciled_element_count+=int(b["elements"])
            reconciled_face_count+=int(b["faces"])
    finally:
        db.close()
    assert (len(app_final),mod_d_links,mod_f_links)==(74,52,52)
    assert (reconciled_element_count,reconciled_face_count)==(390,1844)

    case_out=[]
    source_categories=Counter()
    for key,case in sorted(cases.items()):
        apps=per_case[key]
        assert len(apps)==int(case["applications"]),("CASE_APPLICATION_COUNT",key)
        elems=sum(int(x["historical_declared_elements"]) for x in apps)
        faces=sum(int(x["historical_declared_faces"]) for x in apps)
        assert elems==int(case["elements"]) and faces==int(case["faces"]),(
            "CASE_ELEMENT_FACE_BALANCE",key)
        target=ft_index[key]
        assert (target["cohort"],target["minecraft_version"],target["block"])==(
            case["cohort"],case["minecraft"],case["block"])
        assert int(target["source_applications"])==len(apps)
        assert int(target["source_faces"])==faces
        joins=sum(a["int4_d_option_join"]=="SOURCE_SELECTED_MODEL_EXACT_MATCH" for a in apps)
        if case["cohort"]=="VANILLA":
            assert joins==0
        else:
            assert joins==len(apps)
        affected=sum(int(a["int4_c_face_exception_count_for_model"])>0 for a in apps)
        if affected:exception_case_count+=1
        case_out.append({
            "case":key,"cohort":case["cohort"],"minecraft":case["minecraft"],
            "category":case["category"],"block":case["block"],
            "historical_case_source_blob":FILES[B+"CASES.csv"],
            "historical_source_applications":case["applications"],
            "crosschecked_application_rows":len(apps),
            "historical_elements":case["elements"],
            "crosschecked_application_elements":elems,
            "historical_faces":case["faces"],
            "crosschecked_application_faces":faces,
            "historical_geometry_status_counts":case["status_counts"],
            "selected_model_ids":"|".join(a["model_key_or_path"] for a in apps),
            "selected_provider_ids":"|".join(a["provider_key_or_path"] for a in apps),
            "original_model_sha_set":"|".join(sorted(set(a["original_model_sha"] for a in apps))),
            "original_blockstate_sha_set":"|".join(sorted(set(a["original_state_sha"] for a in apps))),
            "int4_d_mod_state_join":"ALL_MOD_APPLICATIONS_MATCH_D" if joins else "VANILLA_NOT_IN_MOD_D",
            "int4_d_option_count":joins,
            "int4_c_exception_affected_applications":affected,
            "prior_int3_source_link_scope":"MOD_MODEL_MATCHED_INT4_A_D" if joins
                else "VANILLA_HISTORICAL_1_5_INT2_ONLY",
            "original_F2_target_state":target["int4_f_disposition"],
            "new_actual_game_F2_review_status":"NOT_NEWLY_REOPENED_OR_ACCEPTED",
            "research_disposition":"PINNED_SOURCE_CASE_LINKED_NOT_F2_ACCEPTED",
            "followup":"INT4_F_REVIEW_HISTORICAL_EVIDENCE_AND_ACTUAL_GAME",
        })
        source_categories[case["category"]]+=1
    assert len(case_out)==62 and len(source_categories)==9
    assert sum(int(x["int4_d_option_count"]) for x in case_out)==52

    finding_out=[]
    classes=Counter()
    handoffs_counts=Counter()
    finding_cases=0
    finding_runtime_ids=set()
    cases_claimed=set()
    source_claim_d_mod_app_counter=Counter()
    for id_,source in sorted(findings_idx.items()):
        h=handoff[id_]
        pre=checker[id_]
        rv=reviewer[id_]
        assert all(source[field]==h[field] for field in (
            "finding_id","category","classification","axis","cases","cohorts",
            "measurement","observation","scope_limit")),("FINDING_HISTORY_CHANGED",id_)
        assert (pre["category"],pre["classification"],pre["axis"],pre["cases"])==(
            source["category"],source["classification"],source["axis"],source["cases"]),(
            "INT2_FINDING_SCOPE_DRIFT",id_)
        assert (h["runtime_checks"],h["review_condition"])==(
            rv["runtime_checks"],rv["review_condition"])
        assert pre["status"]=="PASS" and pre["differences"]==""
        assert pre["disposition"]==h["disposition"]
        claim_cases=source["cases"].split("|")
        assert claim_cases and len(set(claim_cases))==len(claim_cases)
        assert all(case in cases for case in claim_cases)
        assert set(source["cohorts"].split("|"))==set(cases[x]["cohort"] for x in claim_cases),(
            "COHORT_FINDING_CASE_MISMATCH",id_)
        assert source["scope_limit"].strip()
        case_mod_apps=sum(len(per_case[c]) for c in claim_cases if cases[c]["cohort"]!="VANILLA")
        source_claim_d_mod_app_counter[id_]=case_mod_apps
        finding_cases+=len(claim_cases)
        cases_claimed.update(claim_cases)
        if h["runtime_checks"]:
            finding_runtime_ids.update(h["runtime_checks"].split("|"))
        cl=source["classification"]
        disposition=h["disposition"]
        decision=preserve_classification(cl,disposition)
        classes[cl]+=1
        handoffs_counts[disposition]+=1
        affected_case_count=sum(bool(int(x["int4_c_exception_affected_applications"]))
            for x in case_out if x["case"] in claim_cases)
        finding_out.append({
            "finding_id":id_,"category":source["category"],
            "classification":cl,"axis":source["axis"],
            "source_case_keys":source["cases"],"source_case_count":len(claim_cases),
            "source_cohorts":source["cohorts"],
            "historical_measurement_json":source["measurement"],
            "historical_observation":source["observation"],
            "historical_scope_limit":source["scope_limit"],
            "historical_E_review_condition":h["review_condition"],
            "historical_E_runtime_checks":h["runtime_checks"],
            "original_INT2_check_status":pre["status"],
            "original_INT2_disposition":pre["disposition"],
            "case_keys_integrity":"PASS_EXACT_HISTORICAL_CASE_IDS",
            "case_source_SHA_linkage":"PASS_VIA_1_5_B_APPLICATIONS_SOURCE_AND_PRIOR_INT2",
            "application_linkage":"PASS_ALL_RELEVANT_1_5_MODEL_APPLICATIONS",
            "int4_d_mod_state_scope":f"MOD_APPLICATIONS:{case_mod_apps}|VANILLA_SEPARATE",
            "int4_c_face_exception_case_count":affected_case_count,
            "research_disposition":decision,
            "universal_modeling_rule_approved":"false",
            "int5_semantic_approved":"false",
            "int6_rights_approved":"false",
            "runtime_retested_this_run":"false",
            "followup":h["review_condition"],
        })

    assert classes==CLASSES,classes
    assert handoffs_counts==HANDOFF,handoffs_counts
    assert finding_cases==70
    assert len(cases_claimed)==62,("SOME_CASES_NOT_IN_ANY_FINDING",sorted(set(cases)-cases_claimed))
    assert not exception_case_count
    assert e_audit["table_rows"]["finding_case"]==70
    assert len(finding_runtime_ids)<=e_audit["table_rows"]["runtime_check"]
    assert prior["observed"]["study_cases"]==62
    assert prior["observed"]["applications"]==74
    assert prior["observed"]["claim_rows"]==21
    assert prior["observed"]["findings_rederived_from_B_measurements"]==21
    assert prior["observed"]["classification_counts"]==dict(classes)
    assert prior["observed"]["handoff_dispositions"]==dict(handoffs_counts)
    assert prior["observed"]["source_applications_reverified"]==74
    assert e_independent["confirmed_runtime_checks"]==0
    assert prior["observed"]["runtime_checks_reexecuted_in_this_audit"]==0
    assert all(x["universal_modeling_rule_approved"]=="false" for x in finding_out)
    assert all(x["int6_rights_approved"]=="false" for x in finding_out)

    case_blob=write_csv(case_out,CASE_FIELDS)
    app_blob=write_csv(app_final,APP_FIELDS)
    finding_blob=write_csv(finding_out,FINDING_FIELDS)
    app_gz=gzip.compress(app_blob,compresslevel=9,mtime=0)
    discrepancy_blob=write_csv([],DISCREPANCY_FIELDS)
    stats={
        "schema":"MCFR_INT4_E_62_CASE_74_APPLICATION_21_FINDING_A_D_SOURCE_JOIN/v1",
        "status":"PASS_HISTORIC_STATIC_CASE_APPLICATION_CLAIM_RECONCILIATION_NOT_LIVE_CLIENT",
        "base_draft_pr":55,
        "counts":{
            "case_records_joined":62,
            "model_application_records_joined":74,
            "mod_case_applications_independently_joined_to_A_F_D":52,
            "vanilla_1_21_11_application_cases_historic_source_accepted_not_D_mod":22,
            "finding_source_rows":21,
            "distinct_finding_case_links":finding_cases,
            "distinct_cases_referenced_by_findings":len(cases_claimed),
            "element_instance_sum_across_74_applications":reconciled_element_count,
            "face_instance_sum_across_74_applications":reconciled_face_count,
            "historical_handoff_disposition_counts":dict(sorted(handoffs_counts.items())),
            "historical_finding_classification_counts":dict(sorted(classes.items())),
            "C_model_pixel_exception_affected_case_count":exception_case_count,
            "C_face_pixel_exception_affected_model_applications":
                sum(int(x["int4_c_face_exception_count_for_model"])>0 for x in app_final),
            "original_input_discrepancy_rows":0,
            "known_research_scope_limited_findings":7,
            "historical_runtime_pass_references":10,
            "runtime_checks_newly_run":0,
            "new_original_json_or_png_bytes_reopened":0,
            "live_screenshots_newly_observed":0,
            "universal_AI_style_or_part_semantics_approved":0,
            "original_asset_AI_training_or_redistribution_rights_approved":0,
        },
        "provenance":{
            "version_specific_original_source_evidence":"INT2_1_5_SUMMARY prior independent recheck",
            "mod_source_A_F_D_join":"52 matched by source state rule option model SHA provider SHA geometry count",
            "vanilla_scope":"22 application references to prior 1-5/INT2 Minecraft 1.21.11 original audit; not found in mod D",
            "historical_run_id":prior["ci_run"],
            "F_70_targets":"62 case IDs linked to historical case targets, 8 risks left to F",
            "research_only_not_game_runtime":True,
        },
        "finding_review_ids":{
            "candidate_ids":[x["finding_id"] for x in finding_out if x["original_INT2_disposition"]=="CANDIDATE_REQUIRES_REVIEW"],
            "scope_limit_ids":[x["finding_id"] for x in finding_out if x["original_INT2_disposition"]=="SCOPE_LIMIT_ONLY"],
        },
        "evidence_input_git_blob_sha1":FILES,
        "files":{
            "cases":{"rows":len(case_out),"sha256":sha256(case_blob)},
            "applications":{"rows":len(app_final),"csv_sha256":sha256(app_blob),"gz_sha256":sha256(app_gz)},
            "findings":{"rows":len(finding_out),"sha256":sha256(finding_blob)},
            "discrepancies":{"rows":0,"sha256":sha256(discrepancy_blob)}
        },
        "progress":{
            "E_cases_source_relationships_documented":{"numerator":62,"denominator":62},
            "E_applications_cross_stage_original_source_links":{"numerator":74,"denominator":74},
            "E_claim_scope_and_counterexample_review_documented":{"numerator":21,"denominator":21},
            "E_all_applications_live_3D_render_confirmed":{"numerator":0,"denominator":74},
            "E_AI_modeling_or_rights_approved":{"numerator":0,"denominator":21},
            "E_full_stage_exit":"CONDITIONAL_SOURCE_INTEGRATION_ONLY_RUNTIME_SEMANTIC_RIGHTS_HOLD",
            "F_real_client_case_acceptance":"NOT_REEVALUATED",
        },
        "limitations":[
            "This run joins previously original-verified 1-5 CSV, A/D ledgers and F SQLite, not new original ZIP/JAR or JSON/PNG reads.",
            "22 vanilla applications are 1.21.11 controls, intentionally excluded from 1,158 mod blockstates in D.",
            "52 mod applications match A/D selected source model SHA, state SHA, x/y rotation, uvlock/weight, F provider SHA and element/face totals.",
            "A model with C pixel exceptions is not necessarily a live visually faulty selected state.",
            "21 statements remain strictly original measurement-specific; 7 scope/counterexamples are never converted to positive rules.",
            "Old R01-R10 runtime PASS refers to historic versions only and is NOT 10 new tests.",
            "F2 visual review/registered state reachability/release equivalence, INT5 semantics and INT6 source rights remain separate.",
        ],
    }
    summary=(json.dumps(stats,ensure_ascii=False,indent=2,sort_keys=True)+"\n").encode("utf-8")
    report=("\n".join([
        "# INT-4-E — 1-5 62사례·74모델 적용·21연구 판정 정적 출처 통합 재감사",
        "",
        "이번 실행은 기존 1-5-B/C/E의 **고정 원본 검증 결과**를 1-3-F DB와 INT-4-A/D 선택 모델 출처에 새로 조인하는 작업이다.",
        "이번에 Minecraft 원본 JSON/JAR/PNG 또는 과거 F2 화면을 재실행·재열람했다고 선언하지 않는다.",
        "",
        "## 행 단위 결과",
        "",
        "- 역사 사례 62개에 모델 적용 74건이 정확히 연결됨: 모드 52 / 바닐라 1.21.11 대조 22.",
        "- 모드 52개는 INT-4 A의 모델/출처 SHA, D 78,456건 선택 행, F 원본 SQLite의 제공자·모델 SHA·요소/면 수를 직접 교차 검증.",
        "- 바닐라 22개는 모드용 INT-4-D 분모 밖이므로 이전 INT2-1-5 원본 독립 검증으로 별도 기록.",
        "- 74 적용의 요소/면 합계 390 / 1,844를 62개 사례 원장과 재합산.",
        "- C의 21개 판정은 원본 사례 ID·범주·축·측정 JSON·관찰·범위 제한과 E 인계 검토 조건이 일치함.",
        "- 21판정의 사례 연결 70행, 모든 62사례 인용. 범위 제한 7개 유지, 후보 14개는 승인 전 후보.",
        "- F의 70개 대상 중 역사 사례 ID 62개를 새 출처 원장에 연결. F2 수락 상태는 신규 심사하지 않음.",
        "",
        "## 엄격한 경계",
        "",
        "- 21개의 과거 측정/비교 PASS는 범용 AI 가구 모델링 지침 승인이나 게임 출력 PASS가 아니다.",
        "- 기존 R01-R10 10건의 역사 런타임 검사는 새 런타임 검사 0건과 합산하지 않는다.",
        "- 연구 Git/배포 JAR 버전 차이는 별도 사용 조건으로 보존한다.",
        "- 모델의 face exception은 정적 원본 소스 증거이며 렌더 결함 인정을 뜻하지 않는다.",
        "- INT-4-E 출처 조인 기록은 완료지만 실제 게임/F2·의미·학습·재배포 권리 승인은 보류.",
        "",
        "## 산출물",
        "",
        "- INT4_E_62_CASE_SOURCE_LINKS_V1.csv",
        "- INT4_E_74_APPLICATION_A_D_LINKS_V1.csv.gz",
        "- INT4_E_21_FINDING_DISPOSITIONS_V1.csv",
        "- INT4_E_DISCREPANCIES_V1.csv (출처 불일치 발견 시 검출, 빈 결과라도 분모와 함께 유지)",
        "- INT4_E_CROSS_AUDIT_SUMMARY_V1.json / INT4_E_SOURCE_REPORT_V1.md",
        "",
        "다음 작업 INT-4-F에서 70개 검증 단위의 **정확한 기존 F2 증거 매핑과 원본 이미지 직접 확인**이 필요하다.",
        "",
    ])).encode("utf-8")
    return {
        Path(I+"INT4_E_62_CASE_SOURCE_LINKS_V1.csv"):case_blob,
        Path(I+"INT4_E_74_APPLICATION_A_D_LINKS_V1.csv.gz"):app_gz,
        Path(I+"INT4_E_21_FINDING_DISPOSITIONS_V1.csv"):finding_blob,
        Path(I+"INT4_E_DISCREPANCIES_V1.csv"):discrepancy_blob,
        Path(I+"INT4_E_CROSS_AUDIT_SUMMARY_V1.json"):summary,
        Path(I+"INT4_E_SOURCE_REPORT_V1.md"):report,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    for path,body in build().items():
        dest=ROOT/path
        if args.verify:
            assert dest.is_file() and dest.read_bytes()==body,("OUTPUT_NOT_BYTE_DETERMINISTIC",str(path))
        else:
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(body)
        print("VERIFIED" if args.verify else "CREATED",path,len(body))
    print("PASS 62 cases, 74 applications, 21 findings, 70 claim-case links")


if __name__=="__main__":
    main()
