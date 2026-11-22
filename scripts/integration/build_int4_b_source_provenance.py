#!/usr/bin/env python3
"""INT-4-B: frozen 1-3 C element/face declarations -> every model instance.

This is a deterministic SOURCE DECLARATION RECONCILIATION from historically
original-audited C tables, not a new upstream JSON parse, not pixel sampling,
and not a baked Minecraft renderer/atlas/uvlock test. Source files unchanged.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path("project/integration")
SOURCES={
    "project/integration/INT4_A_MODEL_PARENT_LEDGER_V1.csv.gz":"d72c2f07fcbbba09dc610f09a95bfced84c51930",
    "project/integration/INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":"9b1baf3e3756e44bbe94759b928c2cd30f98cac1",
    "project/integration/INT4_A_ADJUDICATION_SUMMARY_V2.json":"621cce07862bbc5bb051809eeeef8df9607c0a37",
    "research/furniture_mods/phase_1-3/C/mod_model_elements.csv.gz":"439c3d278c570749465b7a8c00493784dbe5b3b9",
    "research/furniture_mods/phase_1-3/C/MODEL_FACES.csv.gz":"65d7bd049e8fbac27f85279b1e6a5611f7656037",
    "research/furniture_mods/phase_1-3/C/C_GEOMETRY_REUSE.csv":"fba1bdcdb14a03da352a5b290060708b53902be1",
    "research/furniture_mods/phase_1-3/C/C_VANILLA_PARENTS.csv":"9fe27be8e403c5971111333fc39c23de138d4195",
    "research/furniture_mods/phase_1-3/C/C_AUDIT.json":"32de17199b77d818230ffdb0664555a11d78794f",
    "project/integration/INT2_1_4_FULL_LINKS_SUMMARY.json":"47fd376ec0c4514277b66b0905bccb4fd9706ef3",
}
FACES="research/furniture_mods/phase_1-3/C/MODEL_FACES.csv.gz"
ELEMENTS="research/furniture_mods/phase_1-3/C/mod_model_elements.csv.gz"
REUSE="research/furniture_mods/phase_1-3/C/C_GEOMETRY_REUSE.csv"
VANILLA="research/furniture_mods/phase_1-3/C/C_VANILLA_PARENTS.csv"
MODEL_FIELDS=[
    "model_key","model_resource_id","mod","minecraft","model_source_path",
    "model_source_sha","provider_source_key","provider_resource_id",
    "provider_source_sha","geometry_signature","element_index",
    "face_direction","source_texture_slot","source_uv","uv_declared",
    "uv_rotation","cullface","tintindex","int4_a_source_disposition",
    "evidence_method","uv_pixel_or_runtime_approval",
]
ELEMENT_FIELDS=[
    "model_key","model_resource_id","mod","minecraft","model_source_sha",
    "provider_source_key","provider_resource_id","provider_source_sha",
    "geometry_signature","element_index",
    "source_from","source_to","pivot","axis","angle","rescale",
    "raw_bbox","rotated_bbox","raw_size","zero_axes","reversed_axes",
    "outside_raw","outside_rotated","nearest_element","rotated_aabb_signed_gap",
    "face_count","nonvanilla_1_21_1_angle","outside_vanilla_1_21_1_coord_limit",
    "int4_a_source_disposition","evidence_method",
]
EXPECTED={"models":16572,"providers":300,"provider_elements":1911,
          "provider_faces":9760,"applied_elements":105383,
          "applied_faces":592312,"explicit_uv":590974,"implicit_uv":1338}


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def blob_sha(blob):
    return hashlib.sha1(b"blob "+str(len(blob)).encode()+bytes([0])+blob).hexdigest()


def src(path):
    data=(ROOT/path).read_bytes()
    observed=blob_sha(data)
    assert observed==SOURCES[path], ("PINNED_INPUT_CHANGED",path,observed)
    return data


def load_csv(path):
    content=src(path)
    if path.endswith(".gz"):
        content=gzip.decompress(content)
    return list(csv.DictReader(io.StringIO(content.decode("utf-8-sig"),newline="")))


def json_file(path):
    return json.loads(src(path).decode("utf-8"))


def index_unique(rows,key,label):
    result={}
    for row in rows:
        identity=row[key]
        assert identity not in result, ("DUPLICATE_KEY",label,identity)
        result[identity]=row
    return result


class GzipCSV:
    def __init__(self,fields):
        self.fields=fields
        self.buffer=io.BytesIO()
        self.gz=gzip.GzipFile(filename="",mode="wb",fileobj=self.buffer,compresslevel=6,mtime=0)
        self.txt=io.TextIOWrapper(self.gz,encoding="utf-8",newline="")
        self.writer=csv.DictWriter(self.txt,fieldnames=fields,lineterminator="\n")
        self.writer.writeheader()
        self.count=0
    def write(self,row):
        self.writer.writerow(row)
        self.count+=1
    def close(self):
        self.txt.close()
        return self.buffer.getvalue()


def uv_is_explicit(v):
    assert v in {"0","1","False","True","false","true"}, ("BAD_UV_DECLARED_FLAG",v)
    return v in {"1","True","true"}


def build():
    past=json_file("project/integration/INT2_1_4_FULL_LINKS_SUMMARY.json")
    assert past["status"]=="PASS_ALL_592312_FACE_LINKS_RECONSTRUCTED_FROM_ORIGINALS"
    assert past["observed"]["reconstructed_faces"]==EXPECTED["applied_faces"]
    assert past["observed"]["model_rows_pass"]==EXPECTED["models"]
    original=json_file("research/furniture_mods/phase_1-3/C/C_AUDIT.json")
    assert original["all_model_paths"]==EXPECTED["models"]
    assert original["element_provider_keys"]==EXPECTED["providers"]
    assert original["rows_by_file"]["mod_model_elements.csv.gz"]==EXPECTED["provider_elements"]
    assert original["rows_by_file"]["MODEL_FACES.csv.gz"]==EXPECTED["provider_faces"]
    assert original["effective_elements"]==EXPECTED["applied_elements"]
    assert original["effective_faces"]==EXPECTED["applied_faces"]
    prior_a=json_file("project/integration/INT4_A_ADJUDICATION_SUMMARY_V2.json")
    assert prior_a["model_level_dispositions_recorded"]==EXPECTED["models"]

    models=load_csv("project/integration/INT4_A_MODEL_PARENT_LEDGER_V1.csv.gz")
    a_review=index_unique(load_csv("project/integration/INT4_A_MODEL_DISPOSITIONS_V2.csv.gz"),
                          "model_key","A_v2")
    geometry=index_unique(load_csv(REUSE),"source_key","geometry_provider")
    elements_by=defaultdict(list)
    faces_by=defaultdict(list)
    all_elem=load_csv(ELEMENTS)
    all_face=load_csv(FACES)
    assert len(models)==EXPECTED["models"]
    assert len(a_review)==EXPECTED["models"]
    assert len(geometry)==EXPECTED["providers"]
    assert len(all_elem)==EXPECTED["provider_elements"]
    assert len(all_face)==EXPECTED["provider_faces"]
    element_keys=set()
    face_keys=set()
    for e in all_elem:
        key=(e["source_key"],e["element_index"])
        assert key not in element_keys, ("DUPLICATE_ELEMENT",key)
        element_keys.add(key)
        elements_by[e["source_key"]].append(e)
    for f in all_face:
        key=(f["source_key"],f["element_index"],f["direction"])
        assert key not in face_keys, ("DUPLICATE_FACE",key)
        face_keys.add(key)
        assert (f["source_key"],f["element_index"]) in element_keys, ("FACE_NOT_IN_ELEMENT",key)
        faces_by[f["source_key"]].append(f)
    assert set(elements_by)==set(faces_by)==set(geometry)
    assert len(element_keys)==EXPECTED["provider_elements"]
    assert len(face_keys)==EXPECTED["provider_faces"]
    for prov,g in geometry.items():
        assert len(elements_by[prov])==int(g["elements"]),("PROVIDER_ELEMENT_COUNT",prov)
        assert len(faces_by[prov])==int(g["faces"]),("PROVIDER_FACE_COUNT",prov)
        by_elem=Counter(f["element_index"] for f in faces_by[prov])
        for e in elements_by[prov]:
            assert by_elem[e["element_index"]]==int(e["face_count"]),("ELEMENT_FACE_COUNT",prov,e["element_index"])

    model_index=index_unique(models,"model_key","A_v1")
    assert set(model_index)==set(a_review)
    vanilla=index_unique(load_csv(VANILLA),"source_key","vanilla_parent")
    provider_used=Counter()
    explicit_count=0
    element_total=0
    face_total=0
    valid_models=0
    no_static=0
    by_mod_faces=Counter()
    by_mod_elements=Counter()
    provider_pins={}
    for prov,g in geometry.items():
        orig=model_index.get(prov)
        if orig:
            assert g["model_id"]==orig["model_id"],("PROVIDER_MODEL_ID",prov)
            provider_pins[prov]=(orig["model_id"],orig["original_model_sha"])
        else:
            assert prov in vanilla,("UNMATCHED_SOURCE_PROVIDER",prov)
            v=vanilla[prov]
            assert v["model_id"]==g["model_id"]
            provider_pins[prov]=(v["model_id"],v["sha256"])
    face_csv=GzipCSV(MODEL_FIELDS)
    elem_csv=GzipCSV(ELEMENT_FIELDS)
    try:
        for m in models:
            check=a_review[m["model_key"]]
            assert check["source_sha"]==m["original_model_sha"]
            assert check["resource_id"]==m["model_id"]
            assert check["mod"]==m["mod"]
            ec=int(m["effective_elements"])
            fc=int(m["effective_faces"])
            provider=m["geometry_source_key"]
            if not ec:
                assert fc==0 and not provider,("NO_STATIC_PROVIDER_MISMATCH",m["model_key"],provider)
                no_static+=1
                continue
            assert provider in geometry,("UNKNOWN_PROVIDER",m["model_key"],provider)
            g=geometry[provider]
            assert ec==int(g["elements"]) and fc==int(g["faces"]),("APPLIED_GEOMETRY_COUNTS",m["model_key"])
            valid_models+=1
            provider_used[provider]+=1
            key,provider_sha=provider_pins[provider]
            template={
                "model_key":m["model_key"],
                "model_resource_id":m["model_id"],
                "mod":m["mod"],
                "minecraft":m["minecraft"],
                "model_source_sha":m["original_model_sha"],
                "provider_source_key":provider,
                "provider_resource_id":key,
                "provider_source_sha":provider_sha,
                "geometry_signature":g["ordered_geometry_sha256"],
                "int4_a_source_disposition":check["int4_a_review_result"],
                "evidence_method":"HISTORICAL_C_FACE_ELEMENT_DECLARATION_REUSE",
            }
            for f in faces_by[provider]:
                explicit_count+=int(uv_is_explicit(f["uv_declared"]))
                face_csv.write({
                    **template,"model_source_path":m["path"],
                    "element_index":f["element_index"],"face_direction":f["direction"],
                    "source_texture_slot":f["texture_slot"],"source_uv":f["uv"],
                    "uv_declared":f["uv_declared"],"uv_rotation":f["uv_rotation"],
                    "cullface":f["cullface"],"tintindex":f["tintindex"],
                    "uv_pixel_or_runtime_approval":"NOT_APPROVED_BY_THIS_DECLARATION_JOIN"
                })
            for e in elements_by[provider]:
                elem_csv.write({
                    **template,
                    **{col:e[col] for col in ELEMENT_FIELDS if col in e and col not in template},
                })
            face_total+=fc
            element_total+=ec
            by_mod_faces[m["mod"]]+=fc
            by_mod_elements[m["mod"]]+=ec
        assert no_static==108 and valid_models==16464
        assert len(provider_used)==EXPECTED["providers"]
        for prov,g in geometry.items():
            assert provider_used[prov]==int(g["effective_model_count"]),("REUSE_COUNT_MISMATCH",prov)
        assert sum(by_mod_faces.values())==face_total==face_csv.count==EXPECTED["applied_faces"]
        assert sum(by_mod_elements.values())==element_total==elem_csv.count==EXPECTED["applied_elements"]
        assert explicit_count==EXPECTED["explicit_uv"], ("EXPLICIT_UV_RECOUNT",explicit_count)
        assert face_total-explicit_count==EXPECTED["implicit_uv"]
    finally:
        faces_gz=face_csv.close()
        elements_gz=elem_csv.close()

    summary={
        "schema":"MCFR_INT4_B_HISTORIC_FACE_ELEMENT_SOURCE_PROVENANCE/v1",
        "status":"PASS_HISTORICAL_105383_ELEMENTS_592312_FACES_EXPANDED_NOT_NEW_ORIGINAL",
        "baseline_pr":52,
        "model_paths":len(models),
        "models_with_static_geometry":valid_models,
        "models_with_no_static_geometry":no_static,
        "source_geometry_provider_count":len(provider_used),
        "source_geometry_provider_face_rows":len(all_face),
        "source_geometry_provider_element_rows":len(all_elem),
        "expanded_element_instances":element_total,
        "expanded_face_instances":face_total,
        "face_uv_declared":explicit_count,
        "face_uv_implicit":face_total-explicit_count,
        "expanded_elements_by_mod":dict(sorted(by_mod_elements.items())),
        "expanded_faces_by_mod":dict(sorted(by_mod_faces.items())),
        "source_hash_joined_face_rows":face_total,
        "source_hash_joined_element_rows":element_total,
        "historic_independent_original_replay":{
            "reference":"project/integration/INT2_1_4_FULL_LINKS_SUMMARY.json",
            "status":past["status"],
            "original_source_face_links":past["observed"]["reconstructed_faces"],
            "source_slots":past["observed"]["source_slots"],
            "previous_face_csv_sha256":past["evidence"]["per_face_gzip_sha256"],
        },
        "inputs_git_blob_sha1":SOURCES,
        "output":{
            "face_rows":face_csv.count,
            "face_csv_gz_sha256":sha256(faces_gz),
            "element_rows":elem_csv.count,
            "element_csv_gz_sha256":sha256(elements_gz),
        },
        "progress":{
            "B_original_declared_face_provenance_join":{"numerator":face_total,"denominator":592312},
            "B_original_declared_element_provenance_join":{"numerator":element_total,"denominator":105383},
            "B_source_release_recheck_not_redownloaded":True,
            "B_full_stage_exit":"PENDING_INDEPENDENT_FULL_UV_AND_ACTUAL_GAME_APPLICABILITY",
            "C_original_PNG_pixel_stage_exit":"NOT_ASSESSED",
            "F_real_client_visual_acceptance":"NOT_ASSESSED",
        },
        "new_upstream_model_json_opened":0,
        "new_game_screenshots_examined":0,
        "texture_slot_alias_resolution_per_child_in_this_join":False,
        "minecraft_uvlock_or_baked_atlas_verified":False,
        "original_source_modified":False,
        "int5_semantic_approvals":0,
        "ai_training_rights_approvals":0,
        "limitations":[
            "Declared face geometry/UV are joined from frozen C files, not independently recalculated from upstream JSON.",
            "Existing independently reproduced INT2 full link summary is included as separate evidence, not a new run.",
            "Source face slot declarations are not resolved per leaf child by this structural join; prior independent original source replay did.",
            "Parent-missing AF source models may have declared faces despite static blockstate nonreachability.",
            "No direct PNG pixel scan, UV atlas bake/uvlock, transparency, tint or visual runtime approval."
        ]
    }
    data=json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True).encode("utf-8")+b"\n"
    report=("\n".join([
        "# INT-4-B 모델별 요소 105,383 / 면 592,312 원본 선언 출처 재연결",
        "",
        "고정 1-3 C 모델·기하 제공자·선언 요소·선언 면 원장과 PR #51/#52의 모델 SHA 및 예외 상태를 전수 연결했다.",
        "원본 ZIP/JAR 모델 파일을 이 단계에서 다시 열어 원본 계산을 독립 재구현한 것은 아니다.",
        "",
        "## 실제 재구성",
        "",
        f"- 모델 16,572개 중 정적 기하가 있는 모델 16,464개. 108개는 기존 no-static으로 제외 사유를 유지.",
        f"- 300 제공자, 선언 요소 1,911개, 선언 면 9,760개를 모델별로 적용.",
        f"- 모델에 적용한 요소 **{element_total:,}개**, 모델에 적용한 면 **{face_total:,}개**.",
        f"- 원본 면에 선언된 UV **{explicit_count:,}개**, 암시 기본 UV **{face_total-explicit_count:,}개**.",
        f"- 면·요소마다 모델 파일 SHA와 기하 제공자 파일 SHA, 원본 C 선언 및 PR #52 예외 상태를 연결.",
        "",
        "## 독립 감사와 신규 수행의 경계",
        "",
        "기존 INT2_1_4_FULL_LINKS_SUMMARY.json은 상위 원본을 다시 읽은 별도 독립 분석에서 592,312면을 재생성했으며",
        "부모·슬롯·UV 관계를 검증했다. 이번 단계는 기존 원본 선언 표를 재적용해 새로운 INT-4-B 인수 원장으로 저장한 것이다.",
        "선언에 사용된 texture_slot은 자식별 텍스처 슬롯 합성/PNG 연결을 새로 계산한 값이 아니다.",
        "기본 UV 공식·블록상태 회전·uvlock·픽셀/화면과의 정확성은 B/C/D/F에서 각각 추가 검수한다.",
        "",
        "## 산출물",
        "",
        "- INT4_B_105383_ELEMENT_PROVENANCE_V1.csv.gz: 모델별 요소 105,383행.",
        "- INT4_B_592312_FACE_PROVENANCE_V1.csv.gz: 모델별 선언 면 592,312행.",
        "- INT4_B_SOURCE_JOIN_SUMMARY_V1.json: 행 수·SHA·모드별 분모·제약.",
        "",
        "**판정:** 정적 출처 재연결 100% (분자/분모 각각 요소·면). B 전체 완료·실제 화면 통과 아님.",
        "INT-5 부품 의미, INT-6 AI 학습/재배포 권한은 별도 미승인이다.",
        "",
    ])).encode("utf-8")
    return {
        OUT/"INT4_B_105383_ELEMENT_PROVENANCE_V1.csv.gz":elements_gz,
        OUT/"INT4_B_592312_FACE_PROVENANCE_V1.csv.gz":faces_gz,
        OUT/"INT4_B_SOURCE_JOIN_SUMMARY_V1.json":data,
        OUT/"INT4_B_SOURCE_JOIN_REPORT_V1.md":report,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify",action="store_true")
    options=parser.parse_args()
    for relative,blob in build().items():
        output=ROOT/relative
        if options.verify:
            assert output.is_file() and output.read_bytes()==blob,("GENERATED_FILE_MISMATCH",str(relative))
        else:
            output.parent.mkdir(parents=True,exist_ok=True)
            output.write_bytes(blob)
        print("VERIFIED" if options.verify else "CREATED",relative,len(blob))
    print("PASS B: 105383 element and 592312 face source declarations")


if __name__=="__main__":
    main()
