#!/usr/bin/env python3
"""INT-4-G4: six Handcrafted base models vs *original* 16572 model parent chains.

Independent source-level audit, not an in-game renderer or license approval.
The original 1-3-C CSV chain_keys includes self then parent keys in order.
D options are explicit static selectors only; "not selected" never rules out
Java, item, block-entity, resource pack or runtime-only model use.
"""
from __future__ import annotations

import argparse,csv,gzip,hashlib,io,json
from collections import Counter,defaultdict
from pathlib import Path
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
CHAIN=Path("research/furniture_mods/phase_1-3/C/MODEL_PARENT_CHAINS.csv.gz")
CAUDIT=Path("research/furniture_mods/phase_1-3/C/C_AUDIT.json")
A_MODELS=OUT/"INT4_G2_16572_MODEL_SOURCE_SCOPE_DISPOSITIONS_V1.csv.gz"
D_OPTIONS=OUT/"INT4_D_78456_OPTION_PROVENANCE_V1.csv.gz"
G3_SIX=OUT/"INT4_G3_112_MODEL_EXCEPTION_SOURCE_USE_IMPACT_V1.csv"
G3_AUDIT=OUT/"INT4_G3_EXCEPTION_SOURCE_REACHABILITY_AUDIT_V1.json"
PINS={
 str(CHAIN):"9a4eeddf419f502bb8fc7808272c7c8336ff9695",
 str(CAUDIT):"32de17199b77d818230ffdb0664555a11d78794f",
 str(A_MODELS):"8266579dc9a59ed65ce77e6dd33855a796f7d5b621a28bf1d3c74528f46d0549",
 str(D_OPTIONS):"d8a007500262cee3e7ae2e24f1891ed640f2eac33cff6cd779a0352ece191301",
 str(G3_SIX):"7be7e98f462754dcf766450708fc57d23e5065f6",
 str(G3_AUDIT):"5224ff016e32f5a431b922bce629c2e0aa6bbc2f",
}
HC_COMMIT="8d21d1665916850c3fa3bdaf1370c50ec2ca7035"
HC_REPO="terrarium-earth/Handcrafted"
BASE_DIR="common/src/main/resources/assets/handcrafted/models/block/base/"
BASE={
 "HC1":("bed_block.json","cafe3cbb37372ddfda78e2278a95ace6f638ef25"),
 "HC2":("bench_block.json","5059b95cd6d83d842dc28e6ad926d0a152b9d868"),
 "HC3":("chair_block.json","ec450539d9c3d829e606397d230372c0814ba946"),
 "HC4":("couch_block.json","d75cf52d57d3952b8079c93c46bcb1538a82f287"),
 "HC5":("phantom_trophy_block.json","03b824b1a2df52b990f47f3041a3dd3701e09cc1"),
 "HC6":("statue_trophy_block.json","f2ad62650703efdbdec636c276cc5de379149a09"),
}
OUT_BASE=OUT/"INT4_G4_HC6_BASE_SOURCE_PARENT_DISPOSITIONS_V1.csv"
OUT_DESC=OUT/"INT4_G4_HC6_DESCENDANT_PARENT_EVIDENCE_V1.csv.gz"
OUT_SUMMARY=OUT/"INT4_G4_HC6_PARENT_CHAIN_AND_ORIGINAL_GIT_AUDIT_V1.json"
OUT_MD=OUT/"INT4_G4_HC_SIX_BASE_PARENT_SCOPE_REPORT_V1.md"

def sha256(b):return hashlib.sha256(b).hexdigest()
def blob_sha1(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def read_pinned(path):
    b=(ROOT/path).read_bytes()
    pin=PINS[str(path)]
    got=sha256(b) if str(path).endswith(".gz") and path in (A_MODELS,D_OPTIONS) else blob_sha1(b)
    assert got==pin,("ORIGINAL_PIN_DRIFT",str(path),got,pin)
    return b
def csv_records(b):
    return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def read_gz(path,expected):
    b=read_pinned(path)
    with gzip.GzipFile(fileobj=io.BytesIO(b)) as stream:
        rows=list(csv.DictReader(io.TextIOWrapper(stream,encoding="utf-8-sig",newline="")))
    assert len(rows)==expected,("ROW_COUNT_CHANGED",str(path),len(rows),expected)
    return rows
def csvb(rows,fields):
    buf=io.StringIO(newline="")
    writer=csv.DictWriter(buf,fieldnames=fields,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue().encode("utf-8")
def jsonb(document):
    return (json.dumps(document,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
def save(path,blob,verify):
    p=ROOT/path
    if verify:
        assert p.is_file() and p.read_bytes()==blob,("NONDETERMINISTIC",str(path))
    else:
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(blob)
    return {"sha256":sha256(blob),"size":len(blob)}
def get_upstream(key,cache):
    filename,expected_sha=BASE[key]
    source=BASE_DIR+filename
    path=cache/filename
    if path.is_file():
        blob=path.read_bytes()
    else:
        u=f"https://raw.githubusercontent.com/{HC_REPO}/{HC_COMMIT}/{source}"
        with urlopen(Request(u,headers={"User-Agent":"MCFR-int4-G4-research-source-audit"}),timeout=90) as resp:
            blob=resp.read()
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(blob)
    got=blob_sha1(blob)
    assert got==expected_sha,("UPSTREAM_HC_JSON_BLOB_CHANGED",source,got)
    parsed=json.loads(blob)
    assert parsed.get("parent")=="block/block",("NOT_BASE_DISPLAY_TEMPLATE",source,parsed.get("parent"))
    assert "elements" not in parsed and isinstance(parsed.get("display",{}).get("gui"),dict),(
        "EXPECTED_NO_OWN_CUBOIDS_WITH_GUI_DISPLAY",source)
    return {"path":source,"sha1":got,"parent":parsed["parent"],
            "own_elements":0,"gui_transform_keys":sorted(parsed["display"]["gui"])}

def build(cache,verify=False):
    caudit=json.loads(read_pinned(CAUDIT))
    g3=json.loads(read_pinned(G3_AUDIT))
    assert caudit["all_model_paths"]==16572 and caudit["model_paths"]["HC"]==12394
    assert caudit["rows_by_file"]["MODEL_PARENT_CHAINS.csv.gz"]==16572
    assert g3["status"]=="PASS_G3_STATIC_OPTION_IMPACT_WITH_PINNED_UPSTREAM_JAVA_AND_NO_RUNTIME_EXIT"
    chains=read_gz(CHAIN,16572)
    models=read_gz(A_MODELS,16572)
    options=read_gz(D_OPTIONS,78456)
    previous=csv_records(read_pinned(G3_SIX))
    assert len(previous)==112
    by_model={r["model_key"]:r for r in models}
    assert len(by_model)==16572
    by_chain={r["model_key"]:r for r in chains}
    assert set(by_model)==set(by_chain)
    old={r["model_key"]:r for r in previous}
    assert all(k in old and old[k]["G3_scoped_disposition"]=="HOLD_HANDCRAFTED_BASE_MODEL_USAGE_AND_JAVA_UNKNOWN"
               for k in BASE)
    # Independently reopen six precise original author Git JSON models.
    originals={key:get_upstream(key,cache) for key in BASE}
    for key in BASE:
        model=by_model[key]
        chain=by_chain[key]
        assert model["mod"]=="HC"
        assert model["original_source_SHA"]==originals[key]["sha1"]
        assert model["original_source_path"]==originals[key]["path"]
        assert chain["chain_keys"]==key
        assert chain["declared_parent"]=="block/block"
        assert chain["terminal_status"]=="BUILTIN"
        assert model["B_expanded_source_faces_observed"]=="0"
        assert model["G2_source_scope_disposition"]=="HOLD_BASE_MODEL_USAGE_UNKNOWN"
        assert old[key]["D_direct_option_count"]=="0"
    d_count=Counter()
    d_states=defaultdict(set)
    for row in options:
        if row["reference_status"]!="LOCAL":continue
        key=row["original_model_key"]
        assert key in by_model
        d_count[key]+=1
        d_states[key].add(row["state_id"])
    assert sum(d_count.values())==78420
    parent_desc=defaultdict(list)
    depth_counter=Counter()
    descendants=[]
    for row in chains:
        parts=[x for x in row["chain_keys"].split("|") if x]
        assert parts and parts[0]==row["model_key"]
        for index,parent in enumerate(parts[1:],1):
            if parent not in BASE:continue
            assert parent != row["model_key"]
            assert row["model_key"] in by_model
            child=by_model[row["model_key"]]
            assert child["mod"]=="HC"
            if index==1:
                expected_resource="handcrafted:block/base/"+BASE[parent][0][:-5]
                assert row["declared_parent"]==expected_resource,(
                    "DIRECT_PARENT_REFERENCE_MISMATCH",row["model_key"],row["declared_parent"],expected_resource)
            desc={
                "base_key":parent,
                "base_resource_id":"handcrafted:block/base/"+BASE[parent][0][:-5],
                "descendant_key":row["model_key"],
                "descendant_model_id":row["model_id"],
                "descendant_declared_parent":row["declared_parent"],
                "parent_chain_depth_to_base":index,
                "direct_child_of_base":str(index==1).lower(),
                "child_source_path":child["original_source_path"],
                "child_source_git_blob_sha1":child["original_source_SHA"],
                "child_A_static_source_disposition":child["G2_source_scope_disposition"],
                "child_B_expanded_faces":child["B_expanded_source_faces_observed"],
                "child_static_D_option_count":d_count[row["model_key"]],
                "child_static_D_state_count":len(d_states[row["model_key"]]),
                "child_selected_actual_runtime_F2_proven":"false",
                "base_own_geometry_0_means_descendant_unrendered":"false",
            }
            parent_desc[parent].append(desc)
            descendants.append(desc)
            depth_counter[str(index)]+=1
    base_result=[]
    categorical=Counter()
    for key in BASE:
        desc=sorted(parent_desc[key],key=lambda r:(r["parent_chain_depth_to_base"],r["descendant_key"]))
        directly=[d for d in desc if d["direct_child_of_base"]=="true"]
        geom=[d for d in desc if int(d["child_B_expanded_faces"])>0]
        selected=[d for d in desc if d["child_static_D_option_count"]>0]
        visible_selected=[d for d in selected if int(d["child_B_expanded_faces"])>0]
        if selected and geom:
            scope="VERIFIED_HC_BASE_DISPLAY_PARENT_WITH_STATIC_D_SELECTED_DESCENDANTS"
        elif desc:
            scope="CONDITIONAL_HC_BASE_AS_PARENT_NO_DIRECT_STATIC_SELECTED_DESCENDANT"
        else:
            scope="HOLD_HC_BASE_NO_RECORDED_CHILD_PARENT_CHAIN"
        categorical[scope]+=1
        base_result.append({
            "model_key":key,"original_model_id":"handcrafted:block/base/"+BASE[key][0][:-5],
            "original_source_path":originals[key]["path"],
            "original_HC_git_commit":HC_COMMIT,
            "original_source_git_blob_SHA1":originals[key]["sha1"],
            "base_parent":originals[key]["parent"],
            "base_own_static_elements":0,
            "base_gui_display_keys":"|".join(originals[key]["gui_transform_keys"]),
            "direct_descendant_models":len(directly),
            "all_transitive_descendant_models":len(desc),
            "descendants_with_source_faces":len(geom),
            "descendants_selected_by_static_D":len(selected),
            "descendants_with_faces_selected_by_D":len(visible_selected),
            "descendant_static_D_option_occurrences":sum(d["child_static_D_option_count"] for d in desc),
            "G4_source_model_scope_disposition":scope,
            "base_parent_geometry_absence_proves_game_defect":"false",
            "full_in_game_runtime_render_approved":"false",
            "required_followup":"Source GUI/base ancestry is evidenced; Minecraft registered/texture/UV/full-state behavior only by original client and renderer proof",
        })
    assert len(base_result)==6
    # Stable source-to-parent rows; a descendant may appear under multiple
    # bases in principle. Preserve the parent key for accurate references.
    descendants.sort(key=lambda r:(r["base_key"],r["descendant_key"]))
    a_bytes=csvb(base_result,list(base_result[0]))
    if descendants:
        d_bytes=gzip.compress(csvb(descendants,list(descendants[0])),mtime=0)
    else:
        raise AssertionError("NO_HANDCRAFTED_PARENT_REFERENCES_IN_HISTORICAL_PARENT_CHAINS")
    saved={}
    for path,data in ((OUT_BASE,a_bytes),(OUT_DESC,d_bytes)):
        saved[path.name]=save(path,data,verify)
    summary={
        "schema":"MCFR_INT4_G4_HC6_BASE_PARENT_CHAIN_CENSUS/v1",
        "status":"PASS_ORIGINAL_HC_GIT_SIX_EMPTY_GUI_BASE_MODELS_REVIEWED_PARENT_CHILD_SCOPE",
        "original_HC_Git_commit":HC_COMMIT,
        "source_parent_chain_git_blob_sha1":PINS[str(CHAIN)],
        "pinned_input_digests":PINS,
        "six_original_HC_base_model_git_sha1":{x:originals[x]["sha1"] for x in BASE},
        "original_parent_chain_rows":len(chains),
        "original_HC_model_paths":caudit["model_paths"]["HC"],
        "original_D_option_rows":len(options),
        "local_model_D_selected_options":sum(d_count.values()),
        "six_source_base_model_count":len(base_result),
        "base_scope_disposition_counts":dict(categorical),
        "base_descendant_total_pairs":len(descendants),
        "descendant_parent_chain_depth_distribution":dict(depth_counter),
        "bases":base_result,
        "source_static_scope_verified":True,
        "G4_game_runtime_or_baked_UV_approved":False,
        "G_final_approved":0,"H_final_approved":0,
        "INT5_part_semantics_approved":0,"INT6_training_or_redistribution_rights_approved":0,
        "limits":[
            "Parent model with no cuboids can legitimately provide display transforms while child/descendant declares geometry.",
            "C original parent chain source is reused but exact six author Git original JSON SHA are freshly reopened.",
            "D explicitly selected descendants demonstrate static registered-model JSON references, not a new native F2 experiment.",
            "Generated item, resource packs and dynamic renderer possible paths remain outside this exact source parent census.",
            "A original HOLD classifications have not been overwritten; G4 source-role classification is a separate layered verdict.",
            "G/H final exit requires independent source, runtime, rights, and risk contracts; do not promote source scope to full completion.",
        ],
        "outputs":saved,
    }
    sumblob=jsonb(summary)
    save(OUT_SUMMARY,sumblob,verify)
    lines=[
        "# INT-4-G4 Handcrafted 기초 모델 6개 원본 부모·자식 경로 감사",
        "",
        "고정 HC Git 8d21d166 원본 JSON 6개를 직접 열어 Git blob SHA를 검증함.",
        "6개 모두 block/block 부모 및 display.gui 변환값을 정의하고, 자체 elements는 없음.",
        "이 결과는 일반 블록 JSON 입체 요소 없음이 렌더 불량을 증명하지 않음을 보여준다.",
        "과거 1-3-C 부모 체인 16,572행과 D 옵션 78,456행을 출처 해시 확인 후 재개방해 해당 base의 자손·정적 선택을 계산.",
        "",
        "| HC 모델 | 직접 자식 | 전체 하위 모델 | D 선택 하위 모델 | 판정 |",
        "|---|---:|---:|---:|---|",
    ]
    for b in base_result:
        lines.append(f"| {b['model_key']} {b['original_model_id']} | {b['direct_descendant_models']} | {b['all_transitive_descendant_models']} | {b['descendants_selected_by_static_D']} | {b['G4_source_model_scope_disposition']} |")
    lines.extend([
        "",
        "**원래 A HOLD는 변경하지 않았고, 이번 G4는 부모 템플릿의 정적 소스 역할만 평가한 것입니다.**",
        "자바/아이템/렌더러 선택·라이브 베이크 UV·기능·의미·재배포 권리의 승인은 없음.",
        "G/H 최종 종료 승인 0, INT5 및 INT6 권리 승인 0.",
        "",
    ])
    save(OUT_MD,("\n".join(lines)+"\n").encode("utf-8"),verify)
    print(json.dumps({"status":summary["status"],"categorical":dict(categorical),
                      "base_counts":[{"key":r["model_key"],"desc":r["all_transitive_descendant_models"],
                                      "Dselected":r["descendants_selected_by_static_D"],
                                      "disposition":r["G4_source_model_scope_disposition"]}
                                     for r in base_result]},ensure_ascii=False))
    return summary

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--cache",required=True,type=Path)
    parser.add_argument("--verify",action="store_true")
    a=parser.parse_args()
    build(a.cache,a.verify)
if __name__=="__main__":
    main()
