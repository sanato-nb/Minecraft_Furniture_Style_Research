#!/usr/bin/env python3
"""INT-4-G3: A 112 / C 6343 / D 6 exceptions vs original 78456 D selections.

Static D absence does not exclude item, parent, Java or dynamic rendering.
Original upstream AF 4.0.3 Java and white_awning JSON are newly reopened and
their fixed Git blob SHA verified, without claiming full runtime registration.
"""
import argparse,csv,gzip,hashlib,io,json
from collections import Counter,defaultdict
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
GIT="57eb624cbb7f408d43398c7434b0d38d312cb55d"
RAW="https://raw.githubusercontent.com/crispytwig/AnotherFurniture/"+GIT+"/"
JAVA="common/src/main/java/com/starfish_studios/another_furniture/registry/AFBlocks.java"
UNUSED="common/src/main/resources/assets/another_furniture/blockstates/unused/white_awning.json"
UPSTREAM={JAVA:"380e721488f3f0cd0a717291a185a5a938ed237d",
          UNUSED:"f1330a172a20d47a24d40288317293bc47c59511"}
PINS={
 "INT4_G2_SOURCE_CROSSJOIN_AUDIT_V1.json":"0514015a4bca32f497ffc8cb86a8d9e6d8b30d08",
 "INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv":"75d61821a732ddec271314396e6c11335f40d4c3",
 "INT4_E_21_FINDING_DISPOSITIONS_V1.csv":"ff3025ffc9d924cc00b7d58cf05212b6dc5e08da",
 "INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv":"0cfbf3b1b174efc968de35c8466e2af8a9cd41c7",
}
COMP={
 "INT4_G2_16572_MODEL_SOURCE_SCOPE_DISPOSITIONS_V1.csv.gz":("8266579dc9a59ed65ce77e6dd33855a796f7d5b621a28bf1d3c74528f46d0549",16572),
 "INT4_G2_6343_FACE_PIXEL_EXCEPTION_CROSSWALK_V1.csv.gz":("bba8d7e9357827587913a74bcd3ccfd28cf808e0e4ac3424af85a5df06179026",6343),
 "INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz":("d8a007500262cee3e7ae24f1891ed640f2eac33cff6cd779a0352ece191301",78456),
}
AOUT=I/"INT4_G3_112_MODEL_EXCEPTION_SOURCE_USE_IMPACT_V1.csv"
COUT=I/"INT4_G3_6343_PIXEL_EXCEPTION_SOURCE_REACHABILITY_V1.csv.gz"
DOUT=I/"INT4_G3_6_BLOCKSTATE_ANOMALY_ORIGINAL_REGISTRY_V1.csv"
AUDIT=I/"INT4_G3_EXCEPTION_SOURCE_REACHABILITY_AUDIT_V1.json"
REPORT=I/"INT4_G3_STATIC_IMPACT_AND_RUNTIME_GATES_V1.md"
def sha(data):return hashlib.sha256(data).hexdigest()
def blobhash(data):return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def pinned(name):
    b=(ROOT/I/name).read_bytes()
    assert blobhash(b)==PINS[name],("ORIGINAL_SOURCE_CHANGED",name)
    return b
def csvrows(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def compressed(name):
    b=(ROOT/I/name).read_bytes()
    digest,n=COMP[name]
    assert sha(b)==digest,("ORIGINAL_GZIP_CHANGED",name)
    with gzip.GzipFile(fileobj=io.BytesIO(b)) as f:
        rows=list(csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig",newline="")))
    assert len(rows)==n,(name,len(rows))
    return rows
def csvout(rows):
    text=io.StringIO(newline="")
    w=csv.DictWriter(text,fieldnames=list(rows[0]),lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return text.getvalue().encode()
def filewrite(path,data,verify):
    p=ROOT/path
    if verify:assert p.is_file() and p.read_bytes()==data,("NONDETERMINISTIC",str(path))
    else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    return {"sha256":sha(data),"bytes":len(data)}
def upstream(file,cache):
    target=cache/Path(file).name
    if target.is_file():data=target.read_bytes()
    else:
        with urlopen(Request(RAW+file,headers={"User-Agent":"MCFR-G3-source-reachability"}),timeout=90) as r:data=r.read()
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    assert blobhash(data)==UPSTREAM[file],("UPSTREAM_VERSION_SOURCE_DRIFT",file)
    return data

def build(cache,verify=False):
    earlier=json.loads(pinned("INT4_G2_SOURCE_CROSSJOIN_AUDIT_V1.json"))
    assert earlier["status"]=="PASS_G2_PINNED_A_B_C_D_E_F_SOURCE_CROSSJOIN_WITH_REMAINING_LIMITS_NOT_FINAL_G"
    models=compressed("INT4_G2_16572_MODEL_SOURCE_SCOPE_DISPOSITIONS_V1.csv.gz")
    cfaces=compressed("INT4_G2_6343_FACE_PIXEL_EXCEPTION_CROSSWALK_V1.csv.gz")
    d_options=compressed("INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz")
    anomalies=csvrows(pinned("INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv"))
    findings=csvrows(pinned("INT4_E_21_FINDING_DISPOSITIONS_V1.csv"))
    f70=csvrows(pinned("INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"))
    assert (len(anomalies),len(findings),len(f70))==(6,21,70)
    java=upstream(JAVA,cache).decode("utf-8")
    white=json.loads(upstream(UNUSED,cache))
    assert "awning" not in java.casefold()
    selectors=white["variants"]
    assert len(selectors)==12
    missing={s for s,x in selectors.items() if x.get("model")=="another_furniture:block/awning/white_double"}
    assert missing=={f"facing={d},type=double" for d in ("north","east","south","west")}
    direct=Counter()
    selected_states=defaultdict(set)
    local=0
    for opt in d_options:
        if opt["reference_status"]!="LOCAL":continue
        local+=1
        key=opt["original_model_key"]
        assert key,("LOCAL_WITHOUT_KEY",opt["state_id"])
        direct[key]+=1
        selected_states[key].add(opt["state_id"])
    assert local==78420
    a_counts=Counter()
    a_out=[]
    for m in models:
        status=m["A_historical_review"]
        if status=="VERIFIED_REUSED_STATIC_SCOPE":continue
        count=direct[m["model_key"]]
        if count and status!="NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY":
            outcome="HOLD_DIRECTLY_SELECTED_STATIC_EXCEPTION_NEEDS_RUNTIME"
        elif status=="CONDITIONAL_STATIC_SOURCE_EXCEPTION":
            outcome="CONDITIONAL_PARENT_MISSING_NOT_DIRECTLY_SELECTED_IN_D"
        elif status=="HOLD_MODEL_USAGE_AND_RENDER_PATH":
            outcome="HOLD_HANDCRAFTED_BASE_MODEL_USAGE_AND_JAVA_UNKNOWN"
        elif status=="NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY":
            outcome="NOT_APPLICABLE_GENERATED_ITEM_STATIC_CUBOID"
        else:raise AssertionError(("UNKNOWN_A_REVIEW",m["model_key"],status))
        a_counts[outcome]+=1
        a_out.append({
         "model_key":m["model_key"],"mod":m["mod"],
         "original_source_path":m["original_source_path"],
         "original_source_sha":m["original_source_SHA"],
         "A_original_review":status,
         "D_direct_option_count":count,
         "D_direct_state_ids":"|".join(sorted(selected_states[m["model_key"]])),
         "B_expanded_face_count":m["B_expanded_source_faces_observed"],
         "C_source_pixel_exception_count":m["C_pixel_exception_source_faces"],
         "G3_scoped_disposition":outcome,
         "Java_item_parent_runtime_excluded":"false",
         "actual_game_mesh_approved":"false",
         "required_followup":"Check item/parent/Java runtime use before interpreting the absent static cuboids",
        })
    assert len(a_out)==112
    c_counts=Counter()
    c_out=[]
    c_model_keys=set()
    for f in cfaces:
        key=f["model_key"]
        c_model_keys.add(key)
        assert f["B_source_face_relation"]=="FACE_SOURCE_SLOT_UV_MATCH"
        count=direct[key]
        result=("HOLD_C_EXCEPTION_DIRECTLY_SELECTED_RUNTIME_REQUIRED" if count else
                "CONDITIONAL_C_EXCEPTION_NOT_DIRECTLY_SELECTED_IN_STATIC_D_OPTIONS")
        c_counts[result]+=1
        c_out.append({
         "model_key":key,"original_model_SHA":f["source_face_model_original_sha"],
         "element_index":f["element_index"],"face_direction":f["face_direction"],
         "original_slot":f["source_slot"],"original_uv":f["uv"],
         "C_original_exception_reason":f["exception_reason"],
         "B_exact_face_source_key_match":f["B_source_face_relation"],
         "static_D_direct_model_option_count":count,
         "G3_static_reachability_disposition":result,
         "runtime_baked_UV_or_texture_defect_proven":"false",
         "required_followup":"Only if item/dynamic runtime uses this model: inspect original PNG and real game UV",
        })
    assert len(c_out)==6343 and len(c_model_keys)==194
    dtypes=Counter()
    d_out=[]
    for row in anomalies:
        k=row["exception_type"]
        dtypes[k]+=1
        if k=="UNRESOLVED_MODEL_REF":
            assert row["state_id"]=="another_furniture:unused/white_awning"
            assert row["model_id"]=="another_furniture:block/awning/white_double"
            assert row["source_selector"] in missing
            scope="HOLD_ORIGINAL_UNUSED_ASSET_REFERENCE_NO_GLOBAL_REGISTRY_CONCLUSION"
        elif k=="PRIOR_CHAIR_VARIANT_3_POINTS_TO_1":
            assert row["state_id"] in ("another_furniture:birch_chair","another_furniture:spruce_chair")
            assert row["source_selector"]=="facing=south,tucked=false,variant=3"
            scope="CONDITIONAL_ORIGINAL_SELECTOR_DIFFERENCE_NOT_RUNTIME_BUG"
        else:raise AssertionError(("UNKNOWN_SOURCE_ANOMALY",k))
        d_out.append({
         "state_id":row["state_id"],"original_source_sha":row["state_source_sha"],
         "source_selector":row["source_selector"],"original_model_ref":row["model_id"],
         "D_exception_type":k,"D_historical_disposition":row["disposition"],
         "G3_source_disposition":scope,
         "original_403_AFBlocks_java_git_sha":UPSTREAM[JAVA],
         "original_403_unused_awning_json_git_sha":UPSTREAM[UNUSED],
         "AFBlocks_java_contains_named_awning":"false",
         "all_registry_or_reflection_paths_reviewed":"false",
         "actual_runtime_bug_proven":"false",
         "required_followup":row["followup"],
        })
    assert dtypes=={"UNRESOLVED_MODEL_REF":4,"PRIOR_CHAIR_VARIANT_3_POINTS_TO_1":2}
    assert all(r["int5_semantic_approved"]==r["int6_rights_approved"]=="false" for r in findings)
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in f70)
    outputs={}
    for path,data in [(AOUT,csvout(a_out)),(COUT,gzip.compress(csvout(c_out),mtime=0)),
                      (DOUT,csvout(d_out))]:
        outputs[path.name]=filewrite(path,data,verify)
    summary={
     "schema":"MCFR_INT4_G3_FROZEN_D_SELECTION_AND_ORIGINAL_AF_403_JAVA_EXCEPTION_SCOPE/v1",
     "status":"PASS_G3_STATIC_OPTION_IMPACT_WITH_PINNED_UPSTREAM_JAVA_AND_NO_RUNTIME_EXIT",
     "original_git_blob_SHA1":PINS,
     "original_source_gzip_sha256":{k:v[0] for k,v in COMP.items()},
     "upstream_AF403_source_git_blob_SHA1":UPSTREAM,
     "original_D_options_reopened":78456,
     "original_local_D_options_joined":local,
     "A_112_exception_model_dispositions":dict(a_counts),
     "C_6343_pixel_face_source_selection_dispositions":dict(c_counts),
     "C_original_affected_models":len(c_model_keys),
     "D_6_exception_reasons":dict(dtypes),
     "AF_403_awning_source_evidence":{
        "unused_asset_selector_count":len(selectors),
        "unresolved_double_model_option_count":len(missing),
        "AFBlocks_java_named_awning_reference":False,
        "proves_global_runtime_registration_absence":False,
     },
     "E_21_findings_semantics_approved":0,
     "F70_full_exit_approved":0,
     "G_final_approved":0,"H_final_approved":0,
     "INT5_semantics_approved":0,"INT6_rights_approved":0,
     "limits":[
       "Direct D static selection absence does not rule out item, parent or Java dynamic rendering.",
       "AFBlocks.java alone does not prove no other module/registration path exists.",
       "No new Minecraft F2 screenshot, material/UV renderer result or source rights inferred.",
       "Variant3->1 differences might be intentional and require real game state analysis.",
       "G3 is source impact review, not INT-4 G/H final exit.",
     ],
     "outputs":outputs,
    }
    filewrite(AUDIT,(json.dumps(summary,sort_keys=True,ensure_ascii=False,indent=2)+"\n").encode(),verify)
    report="\n".join([
      "# INT-4-G3 정적 소스 선택 영향 검수",
      "",
      "기존 A 예외 112 모델, C 예외 6343면 및 D 원본 예외 6건을 실제 78456 선택 옵션과 교차 검증.",
      "AF 4.0.3 고정 Git 원본 AFBlocks.java 및 unused/white_awning.json 직접 재다운로드, Git blob SHA 검사.",
      "",
      "A model review = "+json.dumps(dict(a_counts),ensure_ascii=False,sort_keys=True),
      "C face review = "+json.dumps(dict(c_counts),ensure_ascii=False,sort_keys=True),
      "D anomalies = "+json.dumps(dict(dtypes),ensure_ascii=False,sort_keys=True),
      "",
      "주의: 소스 내 정적 선택 부재가 동적 자바/아이템 렌더 사용의 부재를 의미하지 않는다.",
      "AFBlocks.java에 awning 문자열 부재는 파일 한 곳의 사실이며 전체 등록 경로의 부재가 아니다.",
      "INT-4-G/H 최종 승인 0. INT5 의미 및 INT6 원본 재배포/학습 권한 승인 0.",
      "",
    ])+"\n"
    filewrite(REPORT,report.encode(),verify)
    print(json.dumps({"status":summary["status"],"A":dict(a_counts),"C":dict(c_counts),
                      "D":dict(dtypes),"upstream":UPSTREAM},ensure_ascii=False))
    return summary
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cache",type=Path,required=True)
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    build(a.cache,a.verify)
if __name__=="__main__":main()
