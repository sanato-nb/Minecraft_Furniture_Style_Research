#!/usr/bin/env python3
"""INT-4-D: adopt 1,158 pinned mod blockstates / 78,456 rule-option links.

Reconcile historical original JSON-derived D source ledgers against F SQLite
independently by keys, versions, source SHA, explicit transform declarations,
and selected A model SHA. Attach frozen C 6,343 face exceptions to selected
models WITHOUT confusing model option multiplicity with unique face counts.

This run does not reopen 1,158 upstream source JSON or play Minecraft.
Static variant/multipart condition domains are historical audited evidence,
not a newly simulated game's actually reachable registered states.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
import lzma
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[2]
D="research/furniture_mods/phase_1-3/D/"
F="research/furniture_mods/phase_1-3/F/"
INT="project/integration/"
OUT=Path(INT)
FILES={
 D+"D_AUDIT.json":"f57f27ca1e775848f74abe697ae1e0216a8f5fe2",
 D+"D_INDEPENDENT_AUDIT.json":"7a58087a942023b897ec0509e19811ab48911b45",
 D+"D_BLOCKSTATES.csv":"7079e6abec1bfd0c4a4a5e8c45861e5ceea1033d",
 D+"D_STATE_RULES.csv.gz":"9a06279d4ec3cae2b648895151cfed567b93a95e",
 D+"MODEL_STATE_ASSEMBLY.csv.gz":"496d0273129828ec3e5e8f3c16f131aef7c9594c",
 D+"CONNECTION_RULES.csv":"e4d3e08eb5059a92b17fff2a8a171cc3e12ac768",
 D+"D_CODE_EVIDENCE.csv":"b1adc5fe01cce1f4d53d0b3f7d58a2e8ef5affce",
 D+"D_EXCEPTIONS.csv":"2d76e2cd26a091b5493fef79481f1fde9ae8432f",
 D+"D_PROPERTY_DOMAINS.csv.gz":"89c7809d41501f1b535ede1ee2e73c91c502d12e",
 D+"D_MULTIPART_ASSEMBLIES.csv.gz":"45ec8e6248acd8b8c9e0c36d5ffe1a8bf3f011ac",
 F+"furniture_research.sqlite.xz":"e54839615278dba39cadb463b9988e0371d37ea9",
 F+"DB_VALIDATION.json":"f83ffe2941afc8a007b325fd29a2d7063f129fdc",
 INT+"INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":"9b1baf3e3756e44bbe94759b9282e3aeb3" if False else "9b1baf3e3756e44bbe94759b928c2cd30f98cac1",
 INT+"INT4_A_ADJUDICATION_SUMMARY_V2.json":"621cce07862bbc5bb051809eeeef8df9607c0a37",
 INT+"INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz":"a23b2adba91b604dfbce6c4ef06cc25935a66e56",
 INT+"INT4_C_SOURCE_AUDIT_V1.json":"ace40f7aab319f61dc4d614f52aa01cae12f6cc0",
 INT+"INT4_PARENT_48_BLOCKSTATE_AUDIT_RESULT.json":"919bb491eb63f93e216caf0dbc32b8c27fcafc75",
 INT+"INT3_AF_RELEASE_VERSION_COMPARISON.json":"3e0dd87af8baf429580b1f5e44599f0ea0b9a094",
 INT+"INT2_D_SUMMARY.json":"9d9fc5e7470e1a2fb4be9bf3d52f2e4c2732f4ab",
}
COUNTS={"AF":(177,9325),"HC":(267,60921),"MACAW":(714,8210)}
OPTION_FIELDS=[
 "mod","state_id","state_path","state_source_sha","state_kind","rule_index",
 "source_selector","condition","option_index","model_ref","model_id",
 "original_model_key","original_model_source_sha","reference_status",
 "model_geometry_status","parent_missing","x_original","y_original",
 "x_mod_360","y_mod_360","uvlock","weight","explicit_fields",
 "int4_a_model_disposition","model_static_elements","model_static_faces",
 "selected_model_source_pixel_exception_rows","selected_model_pixel_exception_reasons",
 "source_release_bound","release_equivalence_scope","source_evidence_method",
 "runtime_register_or_visual_status","followup",
]
STATE_FIELDS=[
 "mod","minecraft","state_id","source_path","source_sha","source_bytes",
 "kind","rule_count","option_count","variant_observed_domain_assignments",
 "variant_gaps","variant_overlaps","multipart_assignments","observed_properties",
 "static_local_model_options","static_vanilla_model_options",
 "unresolved_model_options","parent_missing_selected_options",
 "no_static_selected_options","selected_model_pixel_exception_option_uses",
 "unique_selected_models_with_pixel_exception",
 "source_declared_y_rotation_options","source_declared_x_rotation_options",
 "uvlock_true_options","offrange_angle_options",
 "historic_code_classification","registered_class_from_prior_code",
 "code_evidence_id","code_evidence_scope","anomaly_option_count",
 "int4_d_source_disposition","minecraft_runtime_state_reachable",
 "release_equivalence_scope","next_step"
]
EXCEPTION_FIELDS=[
 "mod","state_id","state_source_sha","rule_index","option_index",
 "source_selector","model_id","model_key","exception_type",
 "original_detail","crosschecked_d_option_sha","runtime_defect_proven",
 "original_json_modified","disposition","followup"
]


def git_sha(b:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()


def sha256(b:bytes)->str:
    return hashlib.sha256(b).hexdigest()


def lock(p:str)->bytes:
    raw=(ROOT/p).read_bytes()
    got=git_sha(raw)
    assert got==FILES[p],("PINNED_GIT_BLOB_CHANGED",p,got)
    return raw


def data_json(p:str):
    return json.loads(lock(p).decode("utf-8"))


def data_rows(p:str):
    b=lock(p)
    if p.endswith(".gz"):b=gzip.decompress(b)
    if p.endswith(".xz"):b=lzma.decompress(b)
    return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))


def unique(rows,fn,label):
    result={}
    for row in rows:
        k=fn(row)
        assert k not in result,("DUPLICATE",label,k)
        result[k]=row
    return result


def output_csv(rows,cols):
    fp=io.StringIO(newline="")
    wr=csv.DictWriter(fp,fieldnames=cols,lineterminator="\n")
    wr.writeheader()
    wr.writerows(rows)
    return fp.getvalue().encode("utf-8")


def classify_option(target, mod=""):
    if target=="LOCAL":
        return "STATIC_LOCAL_MODEL_TARGET"
    if target=="VANILLA_JAR":
        return "VANILLA_1_21_1_SOURCE_MODEL_REFERENCE"
    assert target=="UNRESOLVED_MODEL_REF",target
    return "HOLD_ORIGINAL_SOURCE_TARGET_MISSING"


def classify_state(unresolved, parent_selected, no_static, abnormal, code_id):
    if unresolved:
        return "CONDITIONAL_SOURCE_HAS_UNRESOLVED_MODEL_TARGET"
    if parent_selected:
        return "HOLD_SELECTED_MODEL_PARENT_MISSING"
    if no_static:
        return "CONDITIONAL_SELECTED_MODEL_NO_STATIC_ELEMENTS"
    if abnormal:
        return "CONDITIONAL_ORIGINAL_SELECTOR_ANOMALY"
    return "REUSED_STATIC_BLOCKSTATE_SOURCE_VERIFIED_ONLY"


def followup_status(status, c_face_count):
    if status=="UNRESOLVED_MODEL_REF":
        return "INT4_D_CODE_STATE_REGISTRATION_AND_F_RENDER_WHEN_TARGET_EXISTS"
    if c_face_count:
        return "INT4_C_PIXEL_EXCEPTION_AND_D_REACHABILITY_F_CASE"
    return "INT4_D_RUNTIME_PROPERTY_VALUES_AND_F_REAL_CLIENT"


def build():
    old=data_json(D+"D_AUDIT.json")
    independent=data_json(D+"D_INDEPENDENT_AUDIT.json")
    fbaseline=data_json(F+"DB_VALIDATION.json")
    csum=data_json(INT+"INT4_C_SOURCE_AUDIT_V1.json")
    asum=data_json(INT+"INT4_A_ADJUDICATION_SUMMARY_V2.json")
    reach=data_json(INT+"INT4_PARENT_48_BLOCKSTATE_AUDIT_RESULT.json")
    release=data_json(INT+"INT3_AF_RELEASE_VERSION_COMPARISON.json")
    vanilla=data_json(INT+"INT2_D_SUMMARY.json")
    assert old["status"]=="STATIC_SOURCE_SCOPE"
    assert (old["states"],old["rules"],old["options"])==(1158,78456,78456)
    assert independent["status"]=="PASS"
    assert independent["options"]==78456 and independent["references_UNRESOLVED_MODEL_REF"]==4
    assert independent["variant_gaps"]==independent["variant_overlaps"]==0
    assert independent["C_missing_parent_model_keys_directly_selected"]==0
    assert fbaseline["counts"]["state"]==1158
    assert fbaseline["counts"]["rule"]==fbaseline["counts"]["option"]==78456
    assert csum["face_without_own_pixel_support"]==6343
    assert asum["all_model_source_paths"]==16572
    assert reach["observed"]["summary"]["in_static_blockstate_source_selection_or_parent_chain"]==0
    assert vanilla["observed"]["source_paths"]==1168
    assert release["states"]["same"]==88 and release["models"]["json_identical"]==24
    assert release["research"]["blockstate_git_blob_sha1"]!=release["runtime"]["blockstate_git_blob_sha1"]

    stated=data_rows(D+"D_BLOCKSTATES.csv")
    rules=data_rows(D+"D_STATE_RULES.csv.gz")
    options=data_rows(D+"MODEL_STATE_ASSEMBLY.csv.gz")
    connections=data_rows(D+"CONNECTION_RULES.csv")
    code_evidence=data_rows(D+"D_CODE_EVIDENCE.csv")
    exceptions=data_rows(D+"D_EXCEPTIONS.csv")
    property_domains=data_rows(D+"D_PROPERTY_DOMAINS.csv.gz")
    multipart_assembly=data_rows(D+"D_MULTIPART_ASSEMBLIES.csv.gz")
    a_models=unique(data_rows(INT+"INT4_A_MODEL_DISPOSITIONS_V2.csv.gz"),
                    lambda r:r["model_key"],"A_MODEL")
    c_faces=data_rows(INT+"INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz")
    assert len(stated)==len(connections)==1158
    assert len(options)==len(rules)==78456
    assert len(exceptions)==6
    assert len(a_models)==16572
    assert len(c_faces)==6343

    states=unique(stated,lambda x:(x["mod"],x["state_id"]),"D_STATE")
    conn=unique(connections,lambda x:(x["mod"],x["state_id"]),"D_CONNECTION")
    rules_index=unique(rules,lambda x:(x["mod"],x["state_id"],int(x["rule_index"])),"D_RULE")
    option_index=unique(options,lambda x:(x["mod"],x["state_id"],int(x["rule_index"]),int(x["option_index"])),"D_OPTION")
    exceptions_index=unique(exceptions,lambda x:(x["mod"],x["state_id"],int(x["rule_index"]),int(x["option_index"])),"D_EXCEPTION")
    assert len(states)==len(conn)==1158 and len(rules_index)==len(option_index)==78456
    assert len(exceptions_index)==6
    assert all(k[:2] in states for k in rules_index)
    assert all(k[:3] in rules_index for k in option_index)
    assert set(exceptions_index)<=set(option_index)
    assert {r["mod"] for r in states.values()}==set(COUNTS)
    mod_counts=Counter(x["mod"] for x in stated)
    assert {k:mod_counts[k] for k in COUNTS}=={mod:v[0] for mod,v in COUNTS.items()}
    code_ids={x["evidence_id"] for x in code_evidence}
    assert all(x for x in code_ids)
    assert len(code_ids)==len(code_evidence)
    code_rows=[x for x in connections if x["evidence_id"]]
    assert len(code_rows)==500
    assert all(x["evidence_id"] in code_ids for x in code_rows)
    assert len(multipart_assembly)==old["multipart_assignments"]==2112
    assert all(x["kind"] in ("multipart","variants") for x in stated)

    face_c_by_model=Counter(x["model_key"] for x in c_faces)
    face_c_reasons=defaultdict(Counter)
    for f in c_faces:
        model=a_models[f["model_key"]]
        assert f["model_original_sha"]==model["source_sha"]
        assert f["model_resource_id"]==model["resource_id"]
        face_c_reasons[f["model_key"]][f["exception_reason"]]+=1
    assert sum(face_c_by_model.values())==6343

    option_by_state=defaultdict(list)
    variant_counts=Counter()
    reference_counts=Counter()
    abnormal_rotation=Counter()
    selected_model_counts=Counter()
    ever_selected=set()
    event_rows=[]
    audit_mismatch=[]
    # F database stores original source state IDs / fields as independently
    # keyed rows. It is an additional *historical materialization*, not
    # another new upstream JSON read.
    db=sqlite3.connect(":memory:")
    try:
        db.deserialize(lzma.decompress(lock(F+"furniture_research.sqlite.xz")))
        assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        assert not db.execute("PRAGMA foreign_key_check").fetchall()
        sqlite_states={}
        for id_,mod,sid,path,sha,kind,code_id,classification in db.execute(
            "SELECT id,source_id,state_id,path,sha,kind,evidence_id,connection_class FROM state"):
            assert (mod,sid) not in sqlite_states
            sqlite_states[mod,sid]=(id_,path,sha,kind,code_id or "",classification)
        assert len(sqlite_states)==1158
        for (mod,sid),state in states.items():
            state_sql=sqlite_states[mod,sid]
            link=conn[mod,sid]
            assert (state_sql[1],state_sql[2],state_sql[3])==(
                state["path"],state["source_sha"],state["kind"])
            assert (state_sql[4],state_sql[5])==(link["evidence_id"],link["classification"])
            assert (link["source_path"],link["source_sha"])==(state["path"],state["source_sha"])
            assert int(link["json_rule_count"])==int(state["rule_count"])
        rule_comparison=0
        for state_numeric,ri,selector,condition,form in db.execute(
            "SELECT state_id,rule_index,selector,condition,form FROM rule"):
            # SQLite id is 1-based index in D_BLOCKSTATES.csv sorted by source;
            # join by actual key, not fragile row position.
            # Use reverse map constructed once.
            if rule_comparison==0:
                id_to_state={v[0]:k for k,v in sqlite_states.items()}
            mod,sid=id_to_state[state_numeric]
            rr=rules_index[mod,sid,int(ri)]
            assert (rr["source_selector"],rr["condition"],rr["apply_form"])==(
                selector,condition,form),("RULE_HISTORY_MISMATCH",mod,sid,ri)
            assert rr["kind"]==states[mod,sid]["kind"]
            rule_comparison+=1
        assert rule_comparison==78456
        option_comparison=0
        for state_numeric,ri,oi,db_key,target,unresolved,x,y,uv,weight,explicit in db.execute(
            "SELECT state_id,rule_index,option_index,model_key,target_status,"
            "unresolved_target,x,y,uvlock,weight,explicit_fields FROM option"):
            mod,sid=id_to_state[state_numeric]
            k=mod,sid,int(ri),int(oi)
            row=option_index[k]
            rr=rules_index[k[:3]]
            assert row["reference_status"]==target,("TARGET_MISMATCH",k)
            assert (int(row["x"]),int(row["y"]),int(row["x_mod_360"]),int(row["y_mod_360"]))==(
                int(x),int(y),x%360,y%360)
            assert (row["uvlock"].lower()=="true")==bool(uv)
            assert int(row["weight"])==weight
            assert row["explicit_fields"]==explicit
            original_model_sha=row["model_source_sha"]
            a=a_models.get(row["model_key"]) if row["model_key"] else None
            if target=="LOCAL":
                assert a is not None and db_key==row["model_key"],("LOCAL_KEY_ORIGINAL_MISMATCH",k)
                assert (a["source_sha"],a["resource_id"])==(original_model_sha,row["model_id"])
                assert not row["missing_parent"],("HISTORIC_PARENT_MISSING_SELECTED",k)
                assert not int(a["effective_elements"])==0,("STATE_SELECTED_NO_STATIC_GEOMETRY",k)
                assert row["geometry_status"]==a["geometry_status"]
                selected_model_counts[db_key]+=1
                ever_selected.add(db_key)
            elif target=="VANILLA_JAR":
                assert not row["model_key"]
                assert db_key is not None
                vanilla_ref=db.execute("SELECT resource_id,sha,source_id FROM model WHERE model_key=?",(db_key,)).fetchone()
                assert vanilla_ref and (vanilla_ref[0],vanilla_ref[1])==(
                    row["model_id"],original_model_sha)
                assert vanilla_ref[2].startswith("MC")
            else:
                assert target=="UNRESOLVED_MODEL_REF"
                assert db_key is None and unresolved==row["model_id"]
                assert not original_model_sha and not row["model_key"]
                assert not a
            # Baseline historical exceptions use exactly the same selector and target.
            historic_anomaly=exceptions_index.get(k)
            if historic_anomaly:
                assert (historic_anomaly["source_sha"],historic_anomaly["model_id"],
                        historic_anomaly["model_key"],historic_anomaly["source_selector"])==(
                    states[mod,sid]["source_sha"],row["model_id"],row["model_key"],rr["source_selector"])
                if target=="UNRESOLVED_MODEL_REF":
                    assert historic_anomaly["category"]=="UNRESOLVED_MODEL_REF"
                else:
                    assert historic_anomaly["category"]=="PRIOR_CHAIR_VARIANT_3_POINTS_TO_1"
            face_exceptions=face_c_by_model.get(db_key,0) if db_key else 0
            reasons="|".join(f"{name}:{n}" for name,n in sorted(face_c_reasons.get(db_key,{}).items()))
            if face_exceptions:
                abnormal_rotation["C_EXCEPTION_APPLIED_OPTION_USES"]+=1
            if (x%360 or y%360):
                abnormal_rotation["NONZERO_SOURCE_MODEL_ROTATION_OPTIONS"]+=1
            if uv:
                abnormal_rotation["UVLOCK_TRUE_SOURCE_OPTION_COUNT"]+=1
            if x!=x%360 or y!=y%360:
                abnormal_rotation["ANGLES_OUTSIDE_0_359"]+=1
            option_by_state[mod,sid].append({
                "mod":mod,"state_id":sid,"state_path":states[mod,sid]["path"],
                "state_source_sha":states[mod,sid]["source_sha"],
                "state_kind":states[mod,sid]["kind"],"rule_index":ri,
                "source_selector":rr["source_selector"],"condition":rr["condition"],
                "option_index":oi,"model_ref":row["model_ref"],"model_id":row["model_id"],
                "original_model_key":row["model_key"],
                "original_model_source_sha":original_model_sha,
                "reference_status":target,"model_geometry_status":row["geometry_status"],
                "parent_missing":row["missing_parent"],
                "x_original":x,"y_original":y,"x_mod_360":x%360,"y_mod_360":y%360,
                "uvlock":str(bool(uv)).lower(),"weight":weight,
                "explicit_fields":explicit,
                "int4_a_model_disposition":a["int4_a_review_result"] if a else (
                    "FIXED_OFFICIAL_VANILLA_PARENT" if target=="VANILLA_JAR" else "UNRESOLVED_ORIGINAL_MODEL_PATH"),
                "model_static_elements":a["effective_elements"] if a else "",
                "model_static_faces":a["effective_faces"] if a else "",
                "selected_model_source_pixel_exception_rows":face_exceptions,
                "selected_model_pixel_exception_reasons":reasons,
                "source_release_bound":"FIXED_1_3_D_RESEARCH_ONLY",
                "release_equivalence_scope":"AF_4_0_3_GIT_VS_FABRIC_4_0_2_ONLY_ACACIA_CHAIR" if
                   sid=="another_furniture:acacia_chair" else "NOT_CHECKED_ACROSS_RELEASES",
                "source_evidence_method":"HISTORICALLY_ORIGINAL_VERIFIED_D_REUSE_AND_F_SQLITE_ROW_CROSSCHECK",
                "runtime_register_or_visual_status":"NOT_NEWLY_VERIFIED_IN_GAME",
                "followup":followup_status(target,face_exceptions),
            })
            reference_counts[target]+=1
            variant_counts[mod]+=1
            option_comparison+=1
        assert option_comparison==78456
    finally:
        db.close()

    assert {m:variant_counts[m] for m in COUNTS}=={m:v[1] for m,v in COUNTS.items()}
    assert reference_counts=={"LOCAL":78420,"VANILLA_JAR":32,"UNRESOLVED_MODEL_REF":4}
    assert abnormal_rotation["UVLOCK_TRUE_SOURCE_OPTION_COUNT"]==1132
    assert abnormal_rotation["ANGLES_OUTSIDE_0_359"]==1736
    assert sum(len(x) for x in option_by_state.values())==78456
    assert len(option_by_state)==1158
    assert all(x not in ever_selected for x in (
        # Do not use this as negative proof about dynamic loaders/Java.
        "AF1451",))  # historical original wall_lantern C exception and missing parent
    assert not any(x["parent_missing"] for vv in option_by_state.values() for x in vv)
    assert sum(1 for x in exceptions if x["category"]=="UNRESOLVED_MODEL_REF")==4
    assert sum(1 for x in exceptions if x["category"]=="PRIOR_CHAIR_VARIANT_3_POINTS_TO_1")==2

    state_rows=[]
    option_rows=[]
    disposition_counts=Counter()
    for k,state in sorted(states.items()):
        mod,sid=k
        opts=option_by_state[k]
        c=conn[k]
        sr={int(r["rule_index"]) for r in rules if r["mod"]==mod and r["state_id"]==sid}
        assert len(sr)==int(state["rule_count"])
        assert len(opts)==int(state["option_count"])
        static=Counter(x["reference_status"] for x in opts)
        anomalies=[e for e in exceptions if (e["mod"],e["state_id"])==k]
        exception_models={x["original_model_key"] for x in opts
                          if int(x["selected_model_source_pixel_exception_rows"])}
        parent_count=sum(bool(x["parent_missing"]) for x in opts)
        no_static=sum(x["model_static_elements"]=="0" for x in opts)
        result=classify_state(static["UNRESOLVED_MODEL_REF"],parent_count,no_static,len(anomalies),c["evidence_id"])
        disposition_counts[result]+=1
        statescope="PRIOR_CODE_SOURCE_LINKED_NOT_LIVE_REGISTRATION" if c["evidence_id"] else "JSON_SELECTION_ONLY_CODE_UNMAPPED"
        state_rows.append({
            "mod":mod,"minecraft":("1.21.11" if mod=="MACAW" else "1.21.1"),
            "state_id":sid,"source_path":state["path"],"source_sha":state["source_sha"],
            "source_bytes":state["bytes"],"kind":state["kind"],
            "rule_count":state["rule_count"],"option_count":state["option_count"],
            "variant_observed_domain_assignments":state["variant_observed_domain_assignments"],
            "variant_gaps":state["variant_observed_domain_gaps"],
            "variant_overlaps":state["variant_observed_domain_overlaps"],
            "multipart_assignments":state["multipart_assignments"],
            "observed_properties":state["observed_properties"],
            "static_local_model_options":static["LOCAL"],
            "static_vanilla_model_options":static["VANILLA_JAR"],
            "unresolved_model_options":static["UNRESOLVED_MODEL_REF"],
            "parent_missing_selected_options":parent_count,
            "no_static_selected_options":no_static,
            "selected_model_pixel_exception_option_uses":
                sum(bool(int(o["selected_model_source_pixel_exception_rows"])) for o in opts),
            "unique_selected_models_with_pixel_exception":len(exception_models),
            "source_declared_y_rotation_options":sum(int(o["y_mod_360"])!=0 for o in opts),
            "source_declared_x_rotation_options":sum(int(o["x_mod_360"])!=0 for o in opts),
            "uvlock_true_options":sum(o["uvlock"]=="true" for o in opts),
            "offrange_angle_options":sum(int(o["x_original"])!=int(o["x_mod_360"]) or
                                          int(o["y_original"])!=int(o["y_mod_360"]) for o in opts),
            "historic_code_classification":c["classification"],
            "registered_class_from_prior_code":c["registered_class"],
            "code_evidence_id":c["evidence_id"],"code_evidence_scope":statescope,
            "anomaly_option_count":len(anomalies),
            "int4_d_source_disposition":result,
            "minecraft_runtime_state_reachable":"NOT_VERIFIED_BY_THIS_STATIC_HISTORIC_RECHECK",
            "release_equivalence_scope":"ACACIA_CHAIR_88_OPTIONS_FIXED_COMPARE_ONLY" if
               sid=="another_furniture:acacia_chair" else "NOT_ASSESSED_DIFFERENT_RELEASE",
            "next_step":"INT4_D_ORIGINAL_DEPLOYED_RELEASE_AND_CODE_RUNTIME_F2_IF_REQUIRED",
        })
        option_rows.extend(opts)
    assert len(state_rows)==1158 and len(option_rows)==78456
    assert sum(int(x["rule_count"]) for x in state_rows)==78456
    assert sum(int(x["option_count"]) for x in state_rows)==78456
    assert sum(int(x["anomaly_option_count"]) for x in state_rows)==6
    assert sum(int(x["unresolved_model_options"]) for x in state_rows)==4
    assert sum(int(x["static_vanilla_model_options"]) for x in state_rows)==32
    assert sum(int(x["static_local_model_options"]) for x in state_rows)==78420
    assert sum(int(x["parent_missing_selected_options"]) for x in state_rows)==0
    assert all(not int(x["variant_gaps"]) and not int(x["variant_overlaps"]) for x in state_rows)
    assert sum(int(x["multipart_assignments"]) for x in state_rows)==2112
    assert sum(int(x["offrange_angle_options"]) for x in state_rows)==1736
    assert sum(int(x["uvlock_true_options"]) for x in state_rows)==1132
    assert len([x for x in state_rows if x["kind"]=="multipart"])==22
    assert len([x for x in state_rows if x["kind"]=="variants"])==1136

    exrows=[]
    for key,x in sorted(exceptions_index.items()):
        op=option_index[key]
        selected=option_by_state[key[:2]]
        opt=next(r for r in selected if int(r["rule_index"])==key[2] and int(r["option_index"])==key[3])
        exrows.append({
            "mod":x["mod"],"state_id":x["state_id"],
            "state_source_sha":x["source_sha"],"rule_index":x["rule_index"],
            "option_index":x["option_index"],"source_selector":x["source_selector"],
            "model_id":x["model_id"],"model_key":x["model_key"],
            "exception_type":x["category"],"original_detail":x["detail"],
            "crosschecked_d_option_sha":opt["original_model_source_sha"],
            "runtime_defect_proven":"false","original_json_modified":"false",
            "disposition":"HOLD_RUNTIME_AND_RELEASE_SEMANTICS" if
                x["category"]=="PRIOR_CHAIR_VARIANT_3_POINTS_TO_1" else
                "HOLD_UNUSED_SOURCE_MODEL_REFERENCE_NOT_RUNTIME_DEFECT",
            "followup":"INT4_D_CODE_REGISTERED_STATE_AND_F_CLIENT_VISUAL",
        })

    states_blob=output_csv(state_rows,STATE_FIELDS)
    options_blob=output_csv(option_rows,OPTION_FIELDS)
    opt_gzip=gzip.compress(options_blob,compresslevel=6,mtime=0)
    exblob=output_csv(exrows,EXCEPTION_FIELDS)
    selected_exception_face_keys={r["model_key"] for r in c_faces if r["model_key"] in ever_selected}
    historic_direct_selection_face_instances=sum(face_c_by_model[k] for k in selected_exception_face_keys)
    report={
        "schema":"MCFR_INT4_D_HISTORIC_BLOCKSTATE_SELECTION_SOURCE_JOIN/v1",
        "status":"PASS_PINNED_1158_STATE_78456_RULE_OPTION_ROW_RECONCILIATION_NOT_RUNTIME",
        "baseline_pr":54,
        "state_denominator":1158,
        "rule_rows":78456,"option_rows":78456,
        "mod_state_counts":dict(sorted(mod_counts.items())),
        "mod_option_counts":dict(sorted(variant_counts.items())),
        "original_reference_status_counts":dict(sorted(reference_counts.items())),
        "state_source_dispositions":dict(sorted(disposition_counts.items())),
        "static_vanilla_12111_blocks_separate":1168,
        "historic_vanilla_12111_source_enumeration_cases":9193,
        "mod_multipart_blockstate_paths":22,
        "mod_variant_blockstate_paths":1136,
        "historic_variant_property_domain_assignments":
            independent["variant_assignments"],
        "historic_variant_property_domain_gap":independent["variant_gaps"],
        "historic_variant_property_domain_overlap":independent["variant_overlaps"],
        "mod_multipart_historic_condition_assignments":2112,
        "model_options_nonzero_source_rotation_count":
            abnormal_rotation["NONZERO_SOURCE_MODEL_ROTATION_OPTIONS"],
        "source_option_angles_outside_0_359":1736,
        "source_option_uvlock_true":1132,
        "source_option_weight_other_than_1":sum(int(o["weight"])!=1 for o in option_rows),
        "model_parent_missing_48_direct_selected":0,
        "model_parent_missing_48_static_parent_chain_reached_historic":0,
        "history_int4_C_pixel_exception_model_count":len(face_c_by_model),
        "direct_selected_models_with_int4_C_exceptions":len(selected_exception_face_keys),
        "unique_int4_C_pixel_exception_faces_in_direct_selected_models":
            historic_direct_selection_face_instances,
        "option_uses_selecting_model_with_int4_C_exception":
            sum(bool(int(o["selected_model_source_pixel_exception_rows"])) for o in option_rows),
        "source_anomalies":dict(sorted(Counter(r["exception_type"] for r in exrows).items())),
        "previous_source_class_file_code_linked_blockstates":len(code_rows),
        "previous_source_json_only_without_code_map":1158-len(code_rows),
        "AF_acacia_chair_only_release_comparison":{
            "research_release":"4.0.3 pinned Git",
            "runtime_release":"Fabric 4.0.2 historical JAR",
            "source_sha_diff":True,
            "identical_selector_rows_checked":88,
            "parent_geometry_source_json_same":True,
            "scope":"one named blockstate only; not all AF blockstates",
        },
        "input_git_blob_sha1":FILES,
        "outputs":{
            "states_rows":len(state_rows),
            "states_csv_sha256":sha256(states_blob),
            "option_rows":len(option_rows),
            "options_csv_sha256":sha256(options_blob),
            "options_csv_gzip_sha256":sha256(opt_gzip),
            "exception_rows":len(exrows),
            "exception_csv_sha256":sha256(exblob),
        },
        "progress":{
            "D_static_source_blockstates_documented":{"numerator":1158,"denominator":1158},
            "D_static_source_selection_options_documented":{"numerator":78456,"denominator":78456},
            "D_original_exception_cases_documented":{"numerator":6,"denominator":6},
            "D_full_stage_exit":"PENDING_RUNTIME_STATE_AND_RELEASE_REACHABILITY_NOT_APPROVED",
            "F_real_client_acceptance":"NOT_MEASURED_HERE",
        },
        "new_original_blockstate_json_opened":0,
        "new_real_client_screenshots_observed":0,
        "source_JSON_synthetically_repaired":0,
        "dynamic_loader_usage_of_unselected_parent48_excluded":False,
        "reached_in_runtime_not_proven":True,
        "int5_semantic_approvals":0,
        "int6_ai_training_rights_approved":0,
        "limitations":[
            "Historical D source JSON was originally opened, but this run only locked and joined its archived rows and F SQLite.",
            "All 1,158 paths are source records; many may be unregistered/unused or states unobtainable in actual games.",
            "Prior variants 80,787 domain assignments and 2,112 multipart assignments are not replayed here from JSON.",
            "Missing-parent 48 were not selected statically, but dynamic Java or resource packs remain untested.",
            "AF research and release versions differ in byte SHA; 88 identical selector applications are acacia chair only.",
            "Original C face exceptions attached to directly selected models are not the same as unique actual visible in-game broken faces.",
            "No new render client, exact current mod update, baked UV/uvlock/tint/animation, licensing or semantic training approval."
        ],
    }
    summary=(json.dumps(report,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
    md=("\n".join([
        "# INT-4-D 고정 블록상태 1,158개·선택 규칙 78,456개와 모델·원본 SHA 전수 인수",
        "",
        "역사 1-3-D 독립 원본 JSON 감사와 1-3-F SQLite를 직접 키/출처 SHA/선택 모델/회전/uvlock별 대조했다.",
        "이번 실행에서 upstream JSON 1,158개를 재다운로드·재파싱하거나 Minecraft 게임을 실행한 것은 아니다.",
        "",
        "## 정적 원본 선택 검증",
        "",
        "- Another Furniture 177 JSON / 9,325 규칙·선택, Handcrafted 267 / 60,921, Macaw 714 / 8,210.",
        "- 1,158 state / 78,456 rule / 78,456 option 개별 키와 원본 model_id·source SHA, 선언 조건과 x/y/uvlock/weight 검산.",
        "- 로컬 78,420선택, 바닐라 1.21.1 모델 32선택, AF unused white_awning 미해결 4선택.",
        "- 역사 원본 declared variants 1,136개 / multipart 22개, 원본 관측 조합 variant 80,787, multipart 2,112.",
        "- 원본 모델 48개 부모 누락은 정적 선택 0개. 이 사실로 동적 런타임 사용 부재까지 단정하지 않음.",
        "- AF birch/spruce chair의 south variant=3→1 모델 선택 2건은 수정하지 않고 intent/F2 검사 보류.",
        "- JSON 상태 중 코드 근거가 기존에 매핑된 500개와 JSON 규칙만 확인된 658개를 구분.",
        "- Handcrafted 회전 각도 원형을 360으로 나누어 별도 보존; 1,736 옵션은 원형이 0~359 범위 밖.",
        "- Macaw uvlock=true 기존 원본 1,132 옵션을 독립 재집계.",
        "",
        "## 고정 연구 버전과 배포본 혼용 제한",
        "",
        "AF 4.0.3 Git 연구본과 Fabric 4.0.2 JAR의 acacia_chair에서 88 선택 규칙은 이전 연구에서 동등성을 확인했지만 SHA는 다르다.",
        "이를 AF 전체 177 blockstates의 배포본 동일성으로 확대하지 않는다.",
        "",
        "## 다음 단계",
        "",
        "- 1,158개별 요약 및 78,456 선택의 출처 원장을 각각 신규 파일로 기록.",
        "- 이전 6 예외를 별도 CSV로 유지. model option별 C 6,343면 출처 예외 연결은 모델의 정적 선택 문맥이며 실제 손상 면이라는 뜻이 아님.",
        "- INT-4-D 실게임 도달 가능 상태/커스텀 Java 렌더/릴리스 비교 최종 승인은 보류. 별도 INT-4-F에서 정확한 버전·F2 필요.",
        "- INT-5 의미 승인, INT-6 가구 소스 AI 학습/배포 권한 0 유지.",
        "",
    ])).encode("utf-8")
    return {
        OUT/"INT4_D_1158_STATE_DISPOSITIONS_V1.csv":states_blob,
        OUT/"INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz":opt_gzip,
        OUT/"INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv":exblob,
        OUT/"INT4_D_SOURCE_AUDIT_V1.json":summary,
        OUT/"INT4_D_SOURCE_REPORT_V1.md":md,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify",action="store_true")
    opts=parser.parse_args()
    outputs=build()
    for path,data in outputs.items():
        dest=ROOT/path
        if opts.verify:
            assert dest.is_file() and dest.read_bytes()==data,("OUTPUT_NONDETERMINISM",str(path))
        else:
            dest.parent.mkdir(exist_ok=True,parents=True)
            dest.write_bytes(data)
        print("VERIFIED" if opts.verify else "CREATED",path,len(data))
    print("PASS INT4-D: 1158 pinned states / 78456 rule options / 6 source anomalies")


if __name__=="__main__":
    main()
