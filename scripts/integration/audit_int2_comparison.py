"""INT-2 1-5 independent, scoped model comparison and findings audit.

Source methods:
  - pinned AF/HC Git archive and Macaw/Mojang JARs: actual SHA, model,
    provider, selected state variant/multipart and basic geometry count;
  - saved B per-case/element/face table: recompute all 21 C measurements,
    not import any historical 1-5 comparison script;
  - E sqlite and handoff: independent keys/foreign keys/limitations check.
This is source/record verification, NOT a newly run Minecraft client or
a claim that 21 findings are universal AI modeling rules.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import lzma
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
import sqlite3

from audit_int2_mod_textures import Sources,raw_source_sha

ROOT=Path(__file__).resolve().parents[2]
BASE="research/furniture_mods/phase_1-5/"
APPS=BASE+"B/APPLICATIONS.csv"
CASES=BASE+"B/CASES.csv"
ELEMENTS=BASE+"B/ELEMENTS.csv"
FACES=BASE+"B/FACES.csv.xz"
FRAMES=BASE+"B/ANIMATION_FRAMES.csv.xz"
FINDINGS=BASE+"C/CROSS_CATEGORY_FINDINGS.csv"
COVERAGE=BASE+"C/CATEGORY_COVERAGE.csv"
HANDOFF=BASE+"E/PHASE2_HANDOFF.csv"
REVIEW=BASE+"E/review_conditions.csv"
DB=BASE+"E/comparison.sqlite.xz"
VANILLA_ASSETS=BASE+"A/VANILLA_SOURCE_PROVENANCE.csv"
STATIC_EXAMPLES=BASE+"D/STATIC_COUNTEREXAMPLES.json"
RUNTIME=BASE+"runtime_followup/RUNTIME_VERIFICATION.csv"
OUT_COLS=("finding_id","category","classification","axis","cases","measurements_verified",
          "limitations_preserved","model_source_verified","runtime_evidence_status",
          "disposition","status","differences")
EXPECTED_DB={
"application":74,"application_source":221,"asset":272,"asset_hash":346,
"case_category":72,"category":9,"control_asset":102,"element":390,
"face":1844,"face_frame":109,"finding":21,"finding_case":70,
"handoff_runtime":16,"parent_exception":48,"phase2_handoff":21,
"phase_gate":3,"runtime_case":30,"runtime_check":10,"source_artifact":18,
"state_exception":6,"study_case":62,"texture_exception":85,
}
CLASSIFICATION=("MOD_SPECIFIC","MULTI_MOD_SHARED","VANILLA_SHARED","UNVERIFIED_OR_COUNTEREXAMPLE")
SAMPLES=("applications","elements","faces","zero_thickness_elements","faces_measured","faces_at_density_1x1")
APPKEY=("case","rule_index","option_index")
ELKEY=APPKEY+("element_index",)
FACEKEY=ELKEY+("direction",)


def rows(path):
    opener=lzma.open if str(path).endswith(".xz") else open
    with opener(path,"rt",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def idkey(row,columns):
    return tuple(row[key] for key in columns)

def unique(table,keys,label):
    result={}
    for row in table:
        key=idkey(row,keys)
        if key in result:
            raise ValueError(f"Duplicate {label} key {key}")
        result[key]=row
    return result

def gitsha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()

def sample(case):
    return {col:int(case[col]) for col in SAMPLES}

def spans(case_lookup,*ids):
    return {key:case_lookup[key]["span_blocks"] for key in ids}

def samples(case_lookup,*ids):
    return {key:sample(case_lookup[key]) for key in ids}

def face_diff(a,b,faces_by_case,app_by_case):
    if len(app_by_case[a])!=1 or len(app_by_case[b])!=1:
        raise ValueError("Local element correspondence requires one model option each")
    left={(x["element_index"],x["direction"]):x for x in faces_by_case[a]}
    right={(x["element_index"],x["direction"]):x for x in faces_by_case[b]}
    if set(left)!=set(right):
        raise ValueError(f"Face index population differs: {a} / {b}")
    return {field:["/".join(k) for k in sorted(left) if left[k][field]!=right[k][field]]
            for field in ("resource_id","uv","rgba_sha256")}

def face_signature(face,element_map):
    parent=element_map[idkey(face,ELKEY)]
    return tuple([parent["assembly_bbox"]]+[face[f] for f in (
        "direction","resource_id","uv","uv_rotation","cullface",
        "tintindex","status","rgba_sha256"
    )])

def surface_compare(a,b,faces_by_case,element_map):
    old=Counter(face_signature(f,element_map) for f in faces_by_case[a])
    new=Counter(face_signature(f,element_map) for f in faces_by_case[b])
    return {
        "unchanged":sum((old&new).values()),
        "removed":sum((old-new).values()),
        "added":sum((new-old).values()),
    }

def derive_claim(claim,case_lookup,faces_by_case,elem_by_case,app_by_case,element_map):
    axis=claim["axis"]
    def span(*ids):return spans(case_lookup,*ids)
    def measured(*ids):return samples(case_lookup,*ids)
    def transparent(cid):
        return sum(bool(r["pixels"]) and int(r["pixels"])==int(r["alpha_zero"])
                   for r in faces_by_case[cid])
    if axis=="STAIR_ANALOGUE_HEIGHT":
        return span("V01","S01","S06","S08")
    if axis=="TUCKED_GEOMETRY":
        return {"bounds":{i:case_lookup[i]["bbox"] for i in ("S01","S02")},
                "changed_faces":face_diff("S01","S02",faces_by_case,app_by_case)}
    if axis=="CUSHION_SLOT":
        return face_diff("S06","S07",faces_by_case,app_by_case)
    if axis=="SLAB_COMPONENT":
        return span("V02","S12","S13")
    if axis=="OVERLAY_AND_CONNECTION":
        return {"samples":measured("S10","S11","S12","S13"),
                "hc_fully_transparent_faces":transparent("S10")}
    if axis=="CONNECTED_TABLE_TOP":
        heights={}
        for cid in ("S15","S17","S19"):
            heights[cid]=str(max(Fraction(x["local_size"].split("|")[1])
                                 for x in elem_by_case[cid])/16)
        return {"samples":measured("S14","S15","S16","S17","S18","S19"),
                "connected_positive_y_blocks":heights}
    if axis=="MULTIPART_AND_THIN_PART":
        return {"samples":measured("V03","V04","S14","S15"),
                "spans":span("V04","S15")}
    if axis=="OPEN_SURFACE_SWAP":
        return {"af":face_diff("S20","S21",faces_by_case,app_by_case),
                "vanilla":face_diff("V05","V06",faces_by_case,app_by_case)}
    if axis=="HANDLE_PART_COUNTEREXAMPLE":
        handle=next(x for x in faces_by_case["S23"] if "oak_handle" in x["resource_id"])
        return {"samples":measured("S20","S22","S23","S24","S25"),
                "macaw_handle_model_units":element_map[idkey(handle,ELKEY)]["local_size"]}
    if axis=="SHARED_BOOKSHELF_PNG":
        control={i:{x["png_sha"] for x in faces_by_case[i]
                    if x["resource_id"]=="minecraft:block/bookshelf"} for i in ("V07","S28")}
        if not control["V07"] or control["V07"]!=control["S28"] or len(control["V07"])!=1:
            raise ValueError("Claimed same bookshelf source texture is not supported")
        return {"samples":measured("V07","S28"),
                "shared_source_sha256":next(iter(control["V07"]))}
    if axis=="ZERO_THICKNESS_OVERLAY":
        return {"samples":measured("V08","S27"),
                "hc_fully_transparent_faces":transparent("S27")}
    if axis=="BOOKSHELF_CONNECTION":
        return surface_compare("S28","S29",faces_by_case,element_map)
    if axis=="CORNER_COUCH_LAYOUT":
        return measured("S33","S34","S35","S36")
    if axis=="BENCH_BACK_AND_STAIR":
        # C14 uses S32 only as an additional sample, not a stated span
        # comparison. Keep exact historical claim scope; do not broaden.
        return {"samples":measured("V01","V02","S30","S31","S32"),
                "spans":span("V01","V02","S30","S31")}
    if axis=="BED_SPECIAL_RENDER":
        return measured("V09","V11","S37","S38")
    if axis=="BED_FOOT_HEAD":
        return {"samples":measured("S37","S38"),"spans":span("S37","S38")}
    if axis=="WATER_SURFACE_ADDITION":
        return {"face_multisets":{
                    "V12/V13":surface_compare("V12","V13",faces_by_case,element_map),
                    "S42/S43":surface_compare("S42","S43",faces_by_case,element_map)},
                "spans":span("V12","V13","S42","S43")}
    if axis=="COUNTER_FINISH":
        return face_diff("S39","S40",faces_by_case,app_by_case)
    if axis=="COUNTER_TWO_PARTS":
        return measured("S39","S40","S41")
    if axis=="LAMP_UV_AND_EMISSION":
        return {"af_changed":face_diff("S44","S45",faces_by_case,app_by_case),
                "samples":measured("V14","S44","S45")}
    if axis=="PLANT_CONTAINER_SUBTYPES":
        return {"samples":measured("V15","S46","S47"),
                "spans":span("V15","S46","S47")}
    raise ValueError("Unknown claim axis: "+axis)

def eval_multipart(when,props):
    if not when:return True
    if not isinstance(when,dict):raise ValueError("Malformed multipart condition")
    return all(
        any(eval_multipart(branch,props) for branch in value) if key=="OR" else
        all(eval_multipart(branch,props) for branch in value) if key=="AND" else
        props.get(key) in str(value).split("|")
        for key,value in when.items()
    )

def matching_rules(source,state):
    if "variants" in source:
        matches=[]
        for n,(sel,raw) in enumerate(source["variants"].items()):
            selector={}
            if sel:
                for term in sel.split(","):
                    name,sep,value=term.partition("=")
                    if not sep:raise ValueError("Invalid variants property")
                    selector[name]=value
            if all(state.get(k)==v for k,v in selector.items()):
                matches.append((n,raw))
        return matches
    if "multipart" in source:
        return [(n,row["apply"]) for n,row in enumerate(source["multipart"])
                if eval_multipart(row.get("when",{}),state)]
    raise ValueError("No static model selector in source blockstate")

def option_model_path(option):
    ref=option["model"]
    namespace,sep,part=ref.partition(":")
    if not sep:namespace,part="minecraft",namespace
    return f"assets/{namespace}/models/{part}.json"

def audit_source(root,args,app_list):
    original=Sources(args)
    provenance=rows(root/VANILLA_ASSETS)
    verified_assets=0
    errors=[]
    by_case=defaultdict(list)
    source_cache={}
    selected_option_pairs=0
    per_mod=Counter()
    applications_source_valid={}
    missing_declared_options=Counter()
    try:
        def original_source(mod,path):
            source_mod=mod
            if path.startswith("assets/minecraft/"):
                source_mod="MC1.21.11" if mod in ("VANILLA","MACAW") else "MC1.21.1"
            key=(source_mod,path)
            if key not in source_cache:
                content=original.fetch(source_mod,path)
                source_cache[key]=content
            return source_cache[key],source_mod

        for entry in provenance:
            if entry["kind"] not in ("BLOCKSTATE","MODEL","PNG"):
                raise ValueError("Unexpected vanilla source type")
            b=original.fetch("MC1.21.11",entry["path"])
            if (len(b)!=int(entry["bytes"]) or gitsha(b)!=entry["git_blob_sha1"]
                    or hashlib.sha256(b).hexdigest()!=entry["sha256"]):
                raise ValueError("Frozen 1-5 vanilla source provenance differs "+entry["path"])
            verified_assets+=1
        if verified_assets!=74:
            raise ValueError("Vanilla comparison source set was not 74")

        for app in app_list:
            cid=app["case"]
            mod=app["cohort"]
            state_bytes,_=original_source(mod,app["state_path"])
            kind="SHA256" if mod=="MACAW" else "GIT_BLOB_SHA1"
            state_kind="GIT_BLOB_SHA1" if mod=="VANILLA" else kind
            if raw_source_sha(state_bytes,state_kind)!=app["state_sha"]:
                raise ValueError(f"1-5 source blockstate SHA differs {cid}")
            state=json.loads(state_bytes)
            if mod=="VANILLA":
                props=json.loads(app["state"])
            else:
                props={}
                if app["state"]:
                    for assignment in app["state"].split(";"):
                        k,sep,v=assignment.partition("=")
                        if not sep:raise ValueError("Malformed mod source state selector "+cid)
                        props[k]=v
            matches=matching_rules(state,props)
            rule_index=int(app["rule_index"])
            chosen={idx:raw for idx,raw in matches}.get(rule_index)
            why=[]
            if chosen is None:
                why.append("STATE_SELECTOR_RULE_MISMATCH")
            else:
                opts=chosen if isinstance(chosen,list) else [chosen]
                idx=int(app["option_index"])
                if idx<0 or idx>=len(opts):
                    why.append("OPTION_INDEX_NOT_IN_ORIGINAL")
                else:
                    option=opts[idx]
                    wanted=option_model_path(option)
                    if not app["model_path"].endswith("/"+wanted) and app["model_path"]!=wanted:
                        why.append("OPTION_MODEL_PATH_NOT_FROM_SOURCE")
                    for field,default in (("x",0),("y",0),("weight",1)):
                        if int(option.get(field,default))!=int(app[field]):
                            why.append("OPTION_"+field.upper()+"_DIFFERS")
                    if int(bool(option.get("uvlock",False)))!=int(app["uvlock"]):
                        why.append("OPTION_UVLOCK_DIFFERS")
                    selected_option_pairs+=1
            model_bytes,model_scope=original_source(mod,app["model_path"])
            prov_bytes,provider_scope=(b"",None)
            model_hash_kind="GIT_BLOB_SHA1" if mod=="VANILLA" else kind
            if raw_source_sha(model_bytes,model_hash_kind)!=app["model_sha"]:
                why.append("MODEL_BYTES_SHA_MISMATCH")
            if app["provider_path"]:
                prov_bytes,provider_scope=original_source(mod,app["provider_path"])
                expected_kind="GIT_BLOB_SHA1" if provider_scope in ("AF","HC") else "SHA256"
                if mod=="VANILLA":expected_kind="GIT_BLOB_SHA1"
                if raw_source_sha(prov_bytes,expected_kind)!=app["provider_sha"]:
                    why.append("PROVIDER_BYTES_SHA_MISMATCH")
                els=json.loads(prov_bytes)["elements"]
                nfaces=sum(len(e.get("faces",{})) for e in els)
                if (len(els),nfaces)!=(int(app["elements"]),int(app["faces"])):
                    why.append("PROVIDER_ELEMENTS_OR_FACES_DIFFER")
            elif cid!="V11" or (int(app["elements"]),int(app["faces"]))!=(0,0):
                why.append("UNEXPECTED_MISSING_ORDINARY_GEOMETRY")
            if why and len(errors)<100:
                errors.append({"case":cid,"mod":mod,"rule":app["rule_index"],"option":app["option_index"],"problems":why})
            applications_source_valid[idkey(app,APPKEY)]=not why
            by_case[cid].append(app)
            per_mod[mod]+=1
        if selected_option_pairs!=len(app_list):
            missing_declared_options["count"]=len(app_list)-selected_option_pairs
    finally:
        original.close()
    return {
      "verified_vanilla_source_assets":verified_assets,
      "original_source_model_applications":len(app_list),
      "matching_original_selector_and_model_options":selected_option_pairs,
      "fully_reverified_source_application_rows":sum(applications_source_valid.values()),
      "mod_application_counts":dict(sorted(per_mod.items())),
      "original_source_discrepancy_examples":errors,
      "unmatched_option_counts":dict(missing_declared_options),
      "not_checked":["full runtime Minecraft model bake","baked UV/tint/gpu","complete source parent-graph re-traversal"],
    },applications_source_valid

def audit(root,args):
    case_list=rows(root/CASES)
    app_list=rows(root/APPS)
    element_list=rows(root/ELEMENTS)
    face_list=rows(root/FACES)
    frame_list=rows(root/FRAMES)
    claim_list=rows(root/FINDINGS)
    handoff_list=rows(root/HANDOFF)
    review_list=rows(root/REVIEW)
    coverage_list=rows(root/COVERAGE)
    runtime_list=rows(root/RUNTIME)
    if tuple(map(len,(case_list,app_list,element_list,face_list,frame_list,claim_list,handoff_list,review_list,coverage_list,runtime_list)))!=(62,74,390,1844,109,21,21,21,9,10):
        raise ValueError("Frozen 1-5 population unexpectedly changed")
    cases={r["case"]:r for r in case_list}
    findings={r["finding_id"]:r for r in claim_list}
    handoff={r["finding_id"]:r for r in handoff_list}
    review={r["finding_id"]:r for r in review_list}
    apps=unique(app_list,APPKEY,"application")
    elements=unique(element_list,ELKEY,"element")
    faces=unique(face_list,FACEKEY,"face")
    framekeys=unique(frame_list,FACEKEY+("frame",),"animation frame")
    if len(cases)!=62 or len(findings)!=21 or len(handoff)!=21 or len(review)!=21:
        raise ValueError("Duplicate case/finding key")
    app_by_case=defaultdict(list)
    elem_by_case=defaultdict(list)
    face_by_case=defaultdict(list)
    frame_by_case=defaultdict(list)
    for r in app_list:app_by_case[r["case"]].append(r)
    for r in element_list:
        if idkey(r,APPKEY) not in apps:
            raise ValueError("Orphan element application key")
        elem_by_case[r["case"]].append(r)
    for r in face_list:
        if idkey(r,ELKEY) not in elements:
            raise ValueError("Orphan face element key")
        face_by_case[r["case"]].append(r)
    for r in frame_list:
        if idkey(r,FACEKEY) not in faces:
            raise ValueError("Orphan animated-frame source face key")
        frame_by_case[r["case"]].append(r)
    relation_diffs=[]
    observed_status=Counter()
    for eid,element in elements.items():
        observed=sum(1 for face in face_list if idkey(face,ELKEY)==eid)
        if observed!=int(element["faces"]):
            relation_diffs.append({"element":eid,"reason":"ELEMENT_FACE_DEGREE_DIFFERS"})
    for cid,case in cases.items():
        attached=(app_by_case[cid],elem_by_case[cid],face_by_case[cid])
        if tuple(map(len,attached))!=tuple(int(case[k]) for k in ("applications","elements","faces")):
            relation_diffs.append({"case":cid,"reason":"CASE_DIMENSION_DIFFERS"})
        if sum(int(r["elements"]) for r in app_by_case[cid])!=len(elem_by_case[cid]):
            relation_diffs.append({"case":cid,"reason":"APPLICATION_ELEMENT_TOTAL_DIFFERS"})
        if sum(int(r["faces"]) for r in app_by_case[cid])!=len(face_by_case[cid]):
            relation_diffs.append({"case":cid,"reason":"APPLICATION_FACE_TOTAL_DIFFERS"})
        statuses=Counter(x["status"] for x in face_by_case[cid])
        observed_status.update(statuses)
        if statuses!=Counter(json.loads(case["status_counts"])):
            relation_diffs.append({"case":cid,"reason":"CASE_FACE_STATUSES_DIFFER"})
        measured=sum(x["status"] in ("STATIC_RECT","ANIMATED_FRAME_RECTS") for x in face_by_case[cid])
        if measured!=int(case["faces_measured"]):
            relation_diffs.append({"case":cid,"reason":"CASE_PIXEL_MEASURED_DIFFERS"})
    source,source_valid=audit_source(root,args,app_list)
    all_diffs=[]
    finding_rows=[]
    disposition=Counter()
    class_counts=Counter()
    claim_verified=0
    for row in claim_list:
        fid=row["finding_id"]
        cases_for=row["cases"].split("|")
        cohorts=set(cases[cid]["cohort"] for cid in cases_for)
        why=[]
        category=row["category"]
        if row["classification"] not in CLASSIFICATION:why.append("UNKNOWN_CLASSIFICATION")
        if len(set(cases_for))!=len(cases_for):why.append("DUPLICATE_CASE")
        if any(category not in cases[cid]["category"].split("|") for cid in cases_for):
            why.append("CLAIM_CASE_CATEGORY_MISMATCH")
        if "|".join(sorted(cohorts))!=row["cohorts"]:
            why.append("CLAIM_COHORT_SET_DIFFERS")
        label=row["classification"]
        if label=="VANILLA_SHARED" and ("VANILLA" not in cohorts or len(cohorts)<2):
            why.append("CLAIM_VANILLA_COHORT_NOT_PRESENT")
        if label=="MULTI_MOD_SHARED" and ("VANILLA" in cohorts or len(cohorts)<2):
            why.append("MULTI_MOD_COHORT_RULE_BROKEN")
        if label=="MOD_SPECIFIC" and (len(cohorts)!=1 or "VANILLA" in cohorts):
            why.append("MOD_SPECIFIC_COHORT_RULE_BROKEN")
        try:
            recomputed=derive_claim(row,cases,face_by_case,elem_by_case,app_by_case,elements)
            previous=json.loads(row["measurement"])
            if previous!=recomputed:why.append("COMPARISON_MEASUREMENT_RECALC_DIFFERS")
        except Exception as exc:
            why.append("DERIVE_ERROR:"+str(exc)[:140])
        h=handoff[fid]
        for key,value in row.items():
            if h[key]!=value:
                why.append("HANDOFF_SOURCE_FIELD_CHANGED:"+key)
        if h["review_condition"]!=review[fid]["review_condition"] or h["runtime_checks"]!=review[fid]["runtime_checks"]:
            why.append("REVIEW_CONDITION_DIFFERS")
        if not row["scope_limit"].strip() or not h["review_condition"].strip():
            why.append("SCOPE_LIMIT_OR_REVIEW_ABSENT")
        expected_disp="SCOPE_LIMIT_ONLY" if label=="UNVERIFIED_OR_COUNTEREXAMPLE" else "CANDIDATE_REQUIRES_REVIEW"
        if h["disposition"]!=expected_disp:
            why.append("FINDING_PROMOTED_PAST_SCOPE_LIMIT")
        for token in filter(None,h["runtime_checks"].split("|")):
            if token not in {x["test_id"] for x in runtime_list}:
                why.append("RUNTIME_ID_UNDECLARED")
        source_present=all(source_valid.get(idkey(app,APPKEY),False)
                           for cid in cases_for for app in app_by_case[cid])
        if not source_present:why.append("ORIGINAL_SOURCE_NOT_VERIFIED")
        if why and len(all_diffs)<100:
            all_diffs.append({"finding_id":fid,"issues":why})
        class_counts[label]+=1
        disposition[h["disposition"]]+=1
        claim_verified+=int(not why)
        finding_rows.append({
            "finding_id":fid,"category":category,"classification":label,"axis":row["axis"],
            "cases":row["cases"],"measurements_verified":"YES" if "COMPARISON_MEASUREMENT_RECALC_DIFFERS" not in why and not any(x.startswith("DERIVE_ERROR") for x in why) else "NO",
            "limitations_preserved":"YES" if not any("SCOPE_LIMIT" in x or "REVIEW" in x or "PROMOTED" in x for x in why) else "NO",
            "model_source_verified":"YES" if source_present else "NO",
            "runtime_evidence_status":"HISTORIC_ONLY_NOT_REEXECUTED",
            "disposition":h["disposition"],
            "status":"PASS" if not why else "DIFFERENCE",
            "differences":"|".join(why),
        })
    coverage_diffs=[]
    for cat in coverage_list:
        category=cat["category"]
        expect={k:sorted([cid for cid,c in cases.items() if c["cohort"]=="VANILLA" if category in c["category"].split("|")])
                for k in ["vanilla_cases"]}
        expect["mod_cases"]=sorted(cid for cid,c in cases.items() if c["cohort"]!="VANILLA" and category in c["category"].split("|"))
        expect["findings"]=sorted(fid for fid,row in findings.items() if row["category"]==category)
        expect["mod_cohorts"]=sorted({cases[cid]["cohort"] for cid in expect["mod_cases"]})
        for key,value in expect.items():
            if sorted(filter(None,cat[key].split("|")))!=value:
                coverage_diffs.append({"category":category,"field":key,"expected":value,"historic":cat[key]})
    conn=sqlite3.connect(":memory:")
    try:
        conn.deserialize(lzma.decompress((root/DB).read_bytes()))
        if conn.execute("PRAGMA integrity_check").fetchone()[0]!="ok":raise ValueError("E comparison DB corruption")
        fks=conn.execute("PRAGMA foreign_key_check").fetchall()
        if fks:raise ValueError("E foreign-key errors")
        counts={table:conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
                for table in EXPECTED_DB}
        if counts!=EXPECTED_DB:
            raise ValueError("E normalized database row count inconsistency")
        db_findings=dict(conn.execute("SELECT finding_id,classification FROM finding"))
        if db_findings!={r["finding_id"]:r["classification"] for r in claim_list}:
            raise ValueError("E finding classification differs from C")
    finally:
        conn.close()
    # The 10 R01-R10 statuses are historical observations; do not count them
    # as an independent Minecraft client run in this 1-5 re-audit.
    history_runtime_pass=sum(r["status"]=="PASS" for r in runtime_list)
    d=json.loads((root/STATIC_EXAMPLES).read_text(encoding="utf-8"))
    app_uvlocked=sum(int(a["uvlock"]) for a in app_list)
    cullfaces=sum(bool(x["cullface"]) for x in face_list)
    tintfaces=sum(bool(x["tintindex"]) for x in face_list)
    declaration_differences={
        key:{"computed":v,"historic":d[key]}
        for key,v in [
            ("uvlock_declared_applications",app_uvlocked),
            ("cullface_declared_face_instances",cullfaces),
            ("tint_declared_face_instances",tintfaces)
        ] if v!=d[key]
    }
    observed={
        "study_cases":len(cases),"applications":len(apps),"elements":len(elements),
        "faces":len(faces),"animation_frame_rows":len(framekeys),
        "cross_mod_categories":len(coverage_list),"claim_rows":len(claim_list),
        "findings_rederived_from_B_measurements":claim_verified,
        "classification_counts":dict(sorted(class_counts.items())),
        "handoff_dispositions":dict(sorted(disposition.items())),
        "historic_runtime_PASS_ids":history_runtime_pass,
        "runtime_checks_reexecuted_in_this_audit":0,
        "vanilla_assets_reopened_and_rehashed":source["verified_vanilla_source_assets"],
        "source_applications_reverified":source["fully_reverified_source_application_rows"],
        "face_status_counts":dict(sorted(observed_status.items())),
        "sqlite_rows":counts,
    }
    passed=(not relation_diffs and not coverage_diffs and not all_diffs and
            not declaration_differences and not source["original_source_discrepancy_examples"] and
            observed["findings_rederived_from_B_measurements"]==21 and
            disposition==Counter({"CANDIDATE_REQUIRES_REVIEW":14,"SCOPE_LIMIT_ONLY":7}) and
            class_counts==Counter({"VANILLA_SHARED":6,"MULTI_MOD_SHARED":3,"MOD_SPECIFIC":5,"UNVERIFIED_OR_COUNTEREXAMPLE":7}) and
            source["fully_reverified_source_application_rows"]==74)
    report={
        "schema":"MCFR_INT2_1_5_COMPARISON_REAUDIT/v1",
        "baseline":"84842b0516af1aaa9a4dcc7b1fb73ee798b96f87",
        "method":"original_pinned_JSON_state_model_provider_SHA_and_B_row_based_21_claim_rederivation",
        "observed":observed,
        "source":source,
        "discrepancy_examples":{
            "model_element_face_relations":relation_diffs[:40],
            "cross_category_coverage":coverage_diffs[:40],
            "finding_recalculations":all_diffs[:40],
            "source_declarations":declaration_differences,
        },
        "ai_training_approved":False,
        "not_independently_verified":[
            "21 general universal modeling rules / production AI skill",
            "1-5 B face RGBA sampled pixels directly from all original texture files",
            "Minecraft live game runtime; R01-R10 are historical PASS references",
            "model parent chain full independent traversal",
            "upstream content reuse and AI training license grants",
        ],
        "status":"PASS_PINNED_COMPARISON_21_CLAIMS_SOURCED_AND_REDERIVED" if passed
                 else "DIFFERENCE_REQUIRES_REVIEW",
    }
    return finding_rows,report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=ROOT)
    for name in ("af","hc","macaw","mc1211","mc12111","out"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--print-csv",action="store_true",help="Print 21-row evidence CSV once for pinned snapshot")
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    result,report=audit(args.root,args)
    output=args.out/"INT2_1_5_21_FINDING_CHECKS.csv"
    with output.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=OUT_COLS,lineterminator="\n")
        writer.writeheader()
        writer.writerows(result)
    report["finding_csv_sha256"]=hashlib.sha256(output.read_bytes()).hexdigest()
    (args.out/"INT2_1_5_SUMMARY.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8"
    )
    print("INT2_1_5_RESULT:"+json.dumps(report,ensure_ascii=False,sort_keys=True))
    if args.print_csv:
        print("INT2_1_5_CSV_BEGIN")
        print(output.read_text(encoding="utf-8"),end="")
        print("INT2_1_5_CSV_END")
    if report["status"]!="PASS_PINNED_COMPARISON_21_CLAIMS_SOURCED_AND_REDERIVED":
        raise SystemExit("INT-2 1-5 independent audit found discrepancies; preserve artifacts")

if __name__=="__main__":
    main()
