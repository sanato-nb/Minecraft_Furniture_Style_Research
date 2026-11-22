#!/usr/bin/env python3
"""INT-4-C fixed-version slots / texture queue / exact 6,343 unsupported faces.

Uses the immutable phase-1-3 F SQLite DB as original model/face registry and the
previously source-rechecked phase-1-4 C_followup outcomes; no original PNG bytes
are fetched/redecoded here. This stage ADOPTS historical evidence, not new
Minecraft client render validation. Refuses changed Git blobs.
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
F="research/furniture_mods/phase_1-3/F/"
C="research/furniture_mods/phase_1-4/C_followup/"
OUT=Path("project/integration")
PATHS={
    F+"furniture_research.sqlite.xz":"e54839615278dba39cadb463b9988e0371d37ea9",
    F+"1-3_TEXTURE_UV_HANDOFF.csv":"1c2c403cb723a7c121a04e17bb851621edad4cfa",
    C+"SLOT_CHILD_CONTEXT.csv.xz":"74fabd4628916687c5dc99fb8000ed4f4382aba2",
    C+"UV_SOURCE_SUPPORT.csv.xz":"f62da0f51a84f6c953e52a4e07e6670189025aff",
    C+"MISSING_TEXTURE_RELEASE_CHECK.csv":"677be20db100faedff9516cd47adce13aed8e113",
    C+"SUMMARY.json":"658e4a2c309d524c9fac25cebc205a5a69f5514d",
    "project/integration/INT2_1_4_SUMMARY.json":"1f066cf1f9c9528a684534539a2e35a8c97e8c91",
    "project/integration/INT2_1_4_FULL_LINKS_SUMMARY.json":"47fd376ec0c4514277b66b0905bccb4fd9706ef3",
    "project/integration/INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":"9b1baf3e3756e44bbe94759b928c2cd30f98cac1",
    "project/integration/INT4_B_SOURCE_JOIN_SUMMARY_V1.json":"93c07092f683aaaacdb5b3e22c2754376439ca88",
    "research/furniture_mods/phase_1-3/F/DB_VALIDATION.json":"f83ffe2941afc8a007b325fd29a2d7063f129fdc",
}
EXPECTED={"STATIC_RECT":506614,"ANIMATED_FRAME_RECTS":5095,
          "ZERO_UV_AREA":69118,"OUTSIDE_TEXTURE_UV":5144,
          "SLOT_UNBOUND":6202,"MISSING_PINNED_PNG":139}
FACE_FIELDS=[
    "model_key","model_resource_id","model_original_sha","source_id","model_path",
    "geometry_provider","element_index","face_direction","source_slot","uv",
    "uv_declared","uv_rotation","texture_id","texture_resource_id",
    "texture_original_sha","original_status","source_sample_status",
    "exception_reason","exception_subtype","evidence_source",
    "static_child_context","direct_model_blockstate_selected",
    "pinned_original_png_path","pinned_release_check","int4_a_model_disposition",
    "followup","int4_c_disposition",
]
SLOT_FIELDS=[
    "model_key","model_resource_id","model_original_sha","source_id",
    "slot","texture_id","texture_resource_id","resolution","face_instances",
    "static_cuboid_face_slot","historical_slot_child_context",
    "int4_c_binding_disposition",
]
TEXTURE_FIELDS=[
    "texture_id","resource_id","minecraft","source_id","texture_status",
    "source_png_path","source_png_sha","source_hash_kind","face_instances",
    "non_face_slot_count","historical_disposition",
    "previous_pixel_ledger","int4_c_source_scope",
]
CATEGORIES={
    "SLOT_UNBOUND_BOUND_CHILD_CONTEXT":6196,
    "SLOT_UNBOUND_NO_BOUND_CHILD":6,
    "MISSING_PINNED_PNG":139,
    "NO_PINNED_SPRITE_INTERSECTION":2,
}
SUPPORT_CATEGORIES={
    "CLIPPED_RECT_SUPPORT":5142,
    "EDGE_CONTACT_SUPPORT":8,
    "LINE_SUPPORT":68850,
    "POINT_SUPPORT":260,
    "NO_PINNED_SPRITE_INTERSECTION":2,
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+bytes([0])+data).hexdigest()


def locked(path: str) -> bytes:
    body=(ROOT/path).read_bytes()
    sha=blob_sha(body)
    assert sha==PATHS[path], ("HISTORICAL_INPUT_BLOB_DRIFT",path,sha)
    return body


def read_table(path: str):
    body=locked(path)
    if path.endswith(".xz"):
        body=lzma.decompress(body)
    elif path.endswith(".gz"):
        body=gzip.decompress(body)
    return list(csv.DictReader(io.StringIO(body.decode("utf-8-sig"),newline="")))


def locked_json(path: str) -> dict:
    return json.loads(locked(path).decode("utf-8"))


def unique(rows,key,label):
    out={}
    for x in rows:
        k=x[key]
        assert k not in out,("DUPLICATE",label,k)
        out[k]=x
    return out


def dump_csv(rows,fields):
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream,fieldnames=fields,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def uv_values(uv):
    numbers=[float(t) for t in uv.split("|")]
    assert len(numbers)==4,("INVALID_UV",uv)
    return numbers


def face_classification(tid: int|None, path: str, uv: str):
    """Ordering fixed by earlier independently re-executed original-source audit."""
    if tid is None:
        return "SLOT_UNBOUND"
    if not path:
        return "MISSING_PINNED_PNG"
    a,b,c,d=uv_values(uv)
    if a==c or b==d:
        return "ZERO_UV_AREA"
    if any(x<0 or x>16 for x in (a,b,c,d)):
        return "OUTSIDE_TEXTURE_UV"
    return "RENDERABLE_RECT_FROM_SOURCE_DECLARATION"


def compose_exception(status,ctx,outcome):
    """The result is a source exception, NOT an observed Minecraft defect."""
    if status=="SLOT_UNBOUND":
        assert ctx in ("BOUND_CHILD_CONTEXT","UNBOUND_NO_BOUND_CHILD")
        return (
            "SLOT_UNBOUND_BOUND_CHILD_CONTEXT" if ctx=="BOUND_CHILD_CONTEXT"
            else "SLOT_UNBOUND_NO_BOUND_CHILD",
            "PARENT_TEMPLATE_SLOT_ONLY" if ctx=="BOUND_CHILD_CONTEXT" else "NO_BOUND_CHILD_SOURCE_EVIDENCE",
            "INT4_D_MODEL_BINDING_AND_STATIC_REACHABILITY",
            "CONDITIONAL_TEMPLATE_SOURCE_NOT_DIRECT_PIXEL_SUPPORT"
            if ctx=="BOUND_CHILD_CONTEXT" else "HOLD_UNRESOLVED_SLOT_SOURCE",
        )
    if status=="MISSING_PINNED_PNG":
        return (
            "MISSING_PINNED_PNG","MISSING_EXACT_PNG_PATH_IN_PINNED_ORIGINALS",
            "INT4_D_RUNTIME_STATE_AND_RESOURCEPACK_MAPPING",
            "HOLD_MISSING_PINNED_SOURCE_PNG",
        )
    assert status=="OUTSIDE_TEXTURE_UV" and outcome=="NO_PINNED_SPRITE_INTERSECTION"
    return (
        "NO_PINNED_SPRITE_INTERSECTION","NO_IN_SPRITE_UV_INTERSECTION",
        "INT4_D_MODEL_STATIC_OR_DYNAMIC_REACHABILITY",
        "HOLD_UV_NO_SOURCE_PIXEL_INTERSECTION",
    )


def build():
    baseline=locked_json(F+"DB_VALIDATION.json")
    assert baseline["counts"]["texture"]==2256
    assert baseline["counts"]["model_slot"]==81641
    assert baseline["effective_face_instances"]==592312
    assert baseline["counts"]["model"]==16579

    c=locked_json(C+"SUMMARY.json")
    first=locked_json("project/integration/INT2_1_4_SUMMARY.json")
    face_recheck=locked_json("project/integration/INT2_1_4_FULL_LINKS_SUMMARY.json")
    b=locked_json("project/integration/INT4_B_SOURCE_JOIN_SUMMARY_V1.json")
    assert b["expanded_face_instances"]==592312
    assert face_recheck["observed"]["reconstructed_faces"]==592312
    assert c["fixed_faces"]==592312
    assert c["left_without_own_source_samples"]==6343
    assert c["unbound_face_contexts"]=={"BOUND_CHILD_CONTEXT":6196,"UNBOUND_NO_BOUND_CHILD":6}
    assert first["face_evidence_reconciliation"]["observed"]["unsupported"]==6343
    assert first["face_evidence_reconciliation"]["observed"]["sampled"]==585969

    queue=unique(read_table(F+"1-3_TEXTURE_UV_HANDOFF.csv"),"texture_id","2256_TEXTURES")
    assert len(queue)==2256 and set(map(int,queue))==set(range(1,2257))
    missing=unique(read_table(C+"MISSING_TEXTURE_RELEASE_CHECK.csv"),"texture_id","PNG_RELEASE")
    assert len(missing)==8
    assert {k for k,x in queue.items() if x["disposition"]=="SOURCE_EXCEPTION"}==set(missing)
    assert all(x["pinned_git_exists"]=="0" and x["fabric_402_exists"]=="0"
               and x["neoforge_403_exists"]=="0" for x in missing.values())
    assert sum(int(x["face_instances"]) for x in missing.values())==139

    child_context=read_table(C+"SLOT_CHILD_CONTEXT.csv.xz")
    ctx={}
    for row in child_context:
        key=(row["model_key"],row["slot"])
        assert key not in ctx,("DUPLICATE_CHILD_SLOT",key)
        ctx[key]=row
        assert row["outcome"] in ("BOUND_CHILD_CONTEXT","UNBOUND_NO_BOUND_CHILD")
        assert row["direct_blockstate_selection"]=="0"
    assert sum(int(x["face_instances"]) for x in ctx.values())==6202

    region=read_table(C+"UV_SOURCE_SUPPORT.csv.xz")
    region_index={}
    for row in region:
        key=(row["texture_id"],row["uv"],row["original_status"])
        prior=region_index.get(key)
        if prior:
            assert prior["outcome"]==row["outcome"]
            assert prior["face_instances"]==row["face_instances"]
        else:
            region_index[key]=row
    assert len(region_index)==c["distinct_uv_exception_groups"]==1298
    assert len(region)==c["uv_support_frame_rows"]==1306
    assert Counter({
        kind:sum(int(row["face_instances"]) for row in region_index.values() if row["outcome"]==kind)
        for kind in SUPPORT_CATEGORIES
    })==Counter(SUPPORT_CATEGORIES)
    assert sum(int(r["face_instances"]) for r in region_index.values())==74262

    a_models=unique(read_table("project/integration/INT4_A_MODEL_DISPOSITIONS_V2.csv.gz"),
                    "model_key","INT4_A_MODEL")
    assert len(a_models)==16572

    db=sqlite3.connect(":memory:")
    try:
        db.deserialize(lzma.decompress(locked(F+"furniture_research.sqlite.xz")))
        assert db.execute("PRAGMA integrity_check").fetchone()[0]=="ok"
        assert db.execute("PRAGMA foreign_key_check").fetchall()==[]
        assert db.execute("SELECT count(*) FROM model").fetchone()[0]==16579
        assert db.execute("SELECT count(*) FROM texture").fetchone()[0]==2256
        assert db.execute("SELECT count(*) FROM model_slot").fetchone()[0]==81641
        reg=db.execute("SELECT id,resource_id,minecraft,source_id,texture_status,path,sha FROM texture").fetchall()
        assert len(reg)==2256
        texture_rows=[]
        for tid,res,mc,source,texture_status,path,sha in reg:
            record=queue[str(tid)]
            assert record["resource_id"]==res
            assert record["minecraft"]==mc
            assert record["texture_status"]==texture_status
            assert record["path"]==(path or "")
            assert record["source_sha"]==(sha or "")
            assert record["source_id"]==(source or "")
            texture_rows.append({
                "texture_id":tid,"resource_id":res,"minecraft":mc,"source_id":source or "",
                "texture_status":texture_status,"source_png_path":path or "",
                "source_png_sha":sha or "","source_hash_kind":record["source_hash_kind"],
                "face_instances":record["face_instances"],
                "non_face_slot_count":record["non_face_slot_count"],
                "historical_disposition":record["disposition"],
                "previous_pixel_ledger":record["previous_ledger"],
                "int4_c_source_scope":"HISTORIC_ORIGINAL_PNG_REGISTRY_NOT_NEW_PNG_REDECODE",
            })
        assert sum(int(row["face_instances"]) for row in texture_rows)==592312-6202

        source_models={}
        for mod,resource,path,sha,source in db.execute(
                "SELECT model_key,resource_id,path,sha,source_id FROM model"):
            source_models[mod]=(resource,path,sha,source)
            a=a_models.get(mod)
            if a is not None:
                assert a["resource_id"]==resource and a["source_sha"]==sha
        assert len(source_models)==16579
        assert all(key in source_models for key in a_models)

        slot_rows=[]
        no_binding_total=0
        for model,slot,tid,resolution,count,resource,sha,source,texture_res in db.execute(
                "SELECT s.model_key,s.slot,s.texture_id,s.resolution,s.face_count,"
                "m.resource_id,m.sha,m.source_id,t.resource_id "
                "FROM model_slot s JOIN model m ON s.model_key=m.model_key "
                "LEFT JOIN texture t ON t.id=s.texture_id "
                "ORDER BY s.model_key,s.slot"):
            child=ctx.get((model,slot))
            if tid is None:
                no_binding_total+=int(count)
                assert child is not None,("UNBOUND_SLOT_CONTEXT_MISSING",model,slot)
                assert int(child["face_instances"])==int(count),("CHILD_SLOT_WEIGHT_MISMATCH",model,slot)
            else:
                assert child is None,("BOUND_SLOT_WITH_UNBOUND_CONTEXT",model,slot)
            slot_rows.append({
                "model_key":model,"model_resource_id":resource,"model_original_sha":sha,
                "source_id":source,"slot":slot,
                "texture_id":"" if tid is None else tid,
                "texture_resource_id":texture_res or "",
                "resolution":resolution,"face_instances":count,
                "static_cuboid_face_slot":"true" if count else "false",
                "historical_slot_child_context":child["outcome"] if child else "NOT_IN_UNBOUND_6202",
                "int4_c_binding_disposition":"HISTORICALLY_UNBOUND_SOURCE_SLOT" if tid is None
                else "HISTORICALLY_BOUND_TEXTURE_RESOURCE",
            })
        assert len(slot_rows)==81641 and no_binding_total==6202

        rows=[]
        total=0
        face_status=Counter()
        exception_count=Counter()
        evidence_scope=Counter()
        region_weights=Counter()
        no_intersection_examples=[]
        for model,provider,idx,side,slot,tid,uv,declared,rotation,resolution in db.execute(
                "SELECT model_key,provider_key,element_index,direction,slot,texture_id,"
                "uv,uv_declared,uv_rotation,resolution FROM effective_face_texture "
                "ORDER BY model_key,provider_key,element_index,direction"):
            total+=1
            texture=queue[str(tid)] if tid is not None else None
            status=face_classification(tid,texture["path"] if texture else "",uv)
            if status=="RENDERABLE_RECT_FROM_SOURCE_DECLARATION":
                assert texture and texture["path"],("NO_PNG_RECT",model,provider,idx)
                texture_status="ANIMATED_FRAME_RECTS" if (
                    # Rechecked frame count is not inferred from '.mcmeta' filename:
                    # determine via historical source status proportions downstream.
                    False
                ) else "STATIC_OR_ANIMATED_RECT_SOURCE"
                evidence_scope[texture_status]+=1
                continue

            face_status[status]+=1
            outcome=""
            if status in ("ZERO_UV_AREA","OUTSIDE_TEXTURE_UV"):
                group=region_index.get((str(tid),uv,status))
                assert group is not None,("UV_SUPPORT_GROUP_NOT_FOUND",model,tid,uv,status)
                region_weights[(str(tid),uv,status)]+=1
                outcome=group["outcome"]
                if outcome!="NO_PINNED_SPRITE_INTERSECTION":
                    evidence_scope[outcome]+=1
                    continue
            elif status=="SLOT_UNBOUND":
                outcome=ctx[(model,slot)]["outcome"]
            else:
                assert status=="MISSING_PINNED_PNG"
                assert str(tid) in missing
                outcome="PINNED_ALL_THREE_SOURCE_RELEASES_MISSING"

            reason,subtype,followup,disposition=compose_exception(
                status,outcome if status=="SLOT_UNBOUND" else "",outcome)
            exception_count[reason]+=1
            m=source_models[model]
            a=a_models.get(model)
            if status=="NO_PINNED_SPRITE_INTERSECTION":
                no_intersection_examples.append({"model_key":model,"resource_id":m[0],"uv":uv,
                                                 "texture_id":tid,"model_original_sha":m[2]})
            rows.append({
                "model_key":model,"model_resource_id":m[0],
                "model_original_sha":m[2],"source_id":m[3],"model_path":m[1],
                "geometry_provider":provider,"element_index":idx,"face_direction":side,
                "source_slot":slot,"uv":uv,"uv_declared":declared,
                "uv_rotation":rotation,"texture_id":"" if tid is None else tid,
                "texture_resource_id":texture["resource_id"] if texture else "",
                "texture_original_sha":texture["source_sha"] if texture else "",
                "original_status":status,
                "source_sample_status":outcome,
                "exception_reason":reason,
                "exception_subtype":subtype,
                "evidence_source":C+"SUMMARY.json|"+F+"furniture_research.sqlite.xz",
                "static_child_context":ctx[(model,slot)]["outcome"] if status=="SLOT_UNBOUND" else "",
                "direct_model_blockstate_selected":
                    ctx[(model,slot)]["direct_blockstate_selection"] if status=="SLOT_UNBOUND" else "NOT_ASSESSED_BY_THIS_EXCEPTION_IMPORT",
                "pinned_original_png_path":texture["path"] if texture else "",
                "pinned_release_check":"ALL_THREE_PINNED_ORIGINALS_ABSENT"
                    if status=="MISSING_PINNED_PNG" else "NOT_APPLICABLE",
                "int4_a_model_disposition":a["int4_a_review_result"] if a else "VANILLA_CONTROL",
                "followup":followup,"int4_c_disposition":disposition,
            })

        assert total==592312,total
        assert face_status==Counter({
            "SLOT_UNBOUND":6202,"MISSING_PINNED_PNG":139,
            "ZERO_UV_AREA":69118,"OUTSIDE_TEXTURE_UV":5144,
        }),face_status
        assert len(rows)==6343,len(rows)
        assert dict(exception_count)==CATEGORIES,exception_count
        assert sum(evidence_scope.values())==585969
        assert evidence_scope["STATIC_OR_ANIMATED_RECT_SOURCE"]==511709
        assert all(region_weights[key]==int(v["face_instances"]) for key,v in region_index.items()), "REGION_WEIGHT_MISMATCH"
        assert evidence_scope["NO_PINNED_SPRITE_INTERSECTION"]==0
        assert len(no_intersection_examples)==2
        assert len({(r["model_key"],r["geometry_provider"],r["element_index"],r["face_direction"]) for r in rows})==6343
    finally:
        db.close()

    exceptions_body=dump_csv(rows,FACE_FIELDS)
    slots_body=dump_csv(slot_rows,SLOT_FIELDS)
    textures_body=dump_csv(texture_rows,TEXTURE_FIELDS)
    exceptions_gz=gzip.compress(exceptions_body,compresslevel=9,mtime=0)
    slots_gz=gzip.compress(slots_body,compresslevel=9,mtime=0)
    result={
        "schema":"MCFR_INT4_C_EXACT_UNSUPPORTED_FACE_SOURCE_ADOPTION/v1",
        "status":"PASS_6343_PIXEL_UNSUPPORTED_IN_HISTORICAL_STATIC_SOURCE_WITHOUT_RUNTIME_APPROVAL",
        "baseline_pr":53,
        "face_total":total,
        "face_pixel_support_from_original_historic_check":585969,
        "face_without_own_pixel_support":len(rows),
        "face_exception_reason_counts":dict(sorted(exception_count.items())),
        "original_uv_status_counts":dict(sorted(EXPECTED.items())),
        "supported_uv_subtypes":dict(sorted((k,v) for k,v in evidence_scope.items() if k!="STATIC_OR_ANIMATED_RECT_SOURCE")),
        "model_face_texture_registry":2256,
        "model_slot_records":len(slot_rows),
        "historical_source_model_registry":16579,
        "mod_models_originals_linked_int4_a":16572,
        "vanilla_auxiliary_model_keys_separate":7,
        "historic_png_redecoded":2001,
        "historic_original_uv_texture_pairs":2171,
        "historical_pixel_support_percent":round(100*585969/592312,5),
        "historical_face_disposition_documented":total,
        "face_exception_individual_disposition_documented":len(rows),
        "face_exception_full_resolution_approved":False,
        "no_intersection_model_examples":no_intersection_examples,
        "missing_png_resource_rows":len(missing),
        "missing_png_with_faces":sum(int(x["face_instances"])>0 for x in missing.values()),
        "original_png_bytes_reopened_this_run":0,
        "minecraft_game_screenshots_examined":0,
        "texture_rights_approved":0,
        "source_artifacts_modified":0,
        "historical_version_mismatch_merged":False,
        "input_git_blob_sha1":PATHS,
        "output":{
            "face_exception_rows":len(rows),
            "face_exception_csv_sha256":sha256(exceptions_body),
            "face_exception_gz_sha256":sha256(exceptions_gz),
            "model_slot_rows":len(slot_rows),
            "model_slot_csv_sha256":sha256(slots_body),
            "model_slot_gz_sha256":sha256(slots_gz),
            "texture_registry_rows":len(texture_rows),
            "texture_registry_csv_sha256":sha256(textures_body),
        },
        "progress":{
            "C_face_exception_reason_documented":{"numerator":len(rows),"denominator":6343},
            "C_source_texture_pair_registry_joined":{"numerator":len(texture_rows),"denominator":2256},
            "C_source_model_slot_registry_joined":{"numerator":len(slot_rows),"denominator":81641},
            "C_pixel_supported_faces":{"numerator":585969,"denominator":592312},
            "C_full_stage_exit":"CONDITIONAL_HISTORICAL_SOURCE_SCOPE_NOT_RUNTIME_OR_RIGHTS_EXIT",
            "F_runtime_acceptance":"NOT_EVALUATED",
        },
        "interpretation_limits":[
            "Evidence comes from immutable prior original-source PNG and UV audits, not newly opened 2,256 PNG pairs.",
            "6,196 source-template unbound faces have child context, not own original PNG samples.",
            "139 missing PNG faces are not proven visible or broken in actual selected runtime states.",
            "Two no-intersection faces have no pinned source PNG texel intersection, not a proven screen defect.",
            "Minecraft atlas/shader/tint/texture overrides and live release availability not tested.",
            "2,001 prior pixel-redecoded PNG, 2,171 UV-audited pairs, 2,256 registry entries have different denominators.",
        ],
    }
    summary=(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode()
    report=("\n".join([
        "# INT-4-C — 원본 텍스처 슬롯·PNG와 6,343개 화소 미연결 면 전수 처분",
        "",
        "고정 1-3-F SQLite의 592,312개 원형 면 레코드와 과거 1-4-C 원본 PNG·UV 검증 지원표를 직접 연결했다.",
        "**이번 실행은 기존 증거의 개별 원장 인수이며 신규 PNG 바이트 재다운로드·픽셀 디코딩이나 Minecraft 렌더 검증은 아니다.**",
        "",
        "## 전수 판정",
        "",
        "- 원본 면 수 592,312, 과거 화소 근거를 갖는 면 585,969, 직접 화소 근거가 없는 면 6,343.",
        "- 슬롯 미결합 6,202: 동일 기하의 자식 결합 근거 6,196 / 자식 결합 근거 없는 6.",
        "- 고정 정확 경로 PNG 누락 139면: 7개 face-used ID, 별도로 face 없이 참조된 1개를 포함한 8개 누락 자원 등록.",
        "- 원본 UV-스프라이트 비접촉 2면: 코드에 원본 모델 ID/텍스처 ID·UV·출처 SHA를 기록.",
        "- 모델별 슬롯 등록 81,641개와 버전별 텍스처 등록 2,256쌍 전체를 출처 원장과 연결.",
        "- 과거 직접 픽셀 재디코딩 PNG 2,001과 원본 UV 영역 PNG 2,171은 별도 분모다.",
        "",
        "## 잘못된 승격 차단",
        "",
        "- 자식 모델에서 결합되는 템플릿 슬롯이라고 해서 원래 템플릿이 자기 PNG 픽셀을 갖는다고 계산하지 않음.",
        "- 부모/아이템/블록상태가 실제 선택되는지 또는 실게임에서 화면 오류가 발생했는지는 이 단계에서 승인하지 않음.",
        "- 원본 PNG가 경로에 없더라도 커스텀 동적 로더/리소스팩/렌더 경로를 배제하지 않음.",
        "- 정적 UV의 2면에 대한 원본 픽셀 비접촉은 atlas/실게임 고장 판정이 아님.",
        "",
        "## 새 파일",
        "",
        "- INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz: 모델·면별 상세 예외 6,343행.",
        "- INT4_C_81641_SLOT_LINKS_V1.csv.gz: 모델별 슬롯 81,641행.",
        "- INT4_C_2256_TEXTURE_SCOPE_V1.csv: 버전별 텍스처 2,256쌍.",
        "- INT4_C_SOURCE_AUDIT_V1.json: 판정 분모/원본 SHA/산출물 SHA/기술 경계.",
        "",
        "**INT-4-C 상태:** 고정 원본 화소 지원의 출처·예외 기록은 100%지만, 예외 해결율이나 실게임 및 권리 검증 완료율은 아니다.",
        "원본 자료와 main은 변경하지 않는다. 후속 D에서 사용 모델·선택 상태·리소스팩을 확인한다.",
        "",
    ])).encode("utf-8")
    return {
        OUT/"INT4_C_6343_FACE_PIXEL_EXCEPTIONS_V1.csv.gz":exceptions_gz,
        OUT/"INT4_C_81641_SLOT_LINKS_V1.csv.gz":slots_gz,
        OUT/"INT4_C_2256_TEXTURE_SCOPE_V1.csv":textures_body,
        OUT/"INT4_C_SOURCE_AUDIT_V1.json":summary,
        OUT/"INT4_C_SOURCE_REPORT_V1.md":report,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    outputs=build()
    for path,data in outputs.items():
        target=ROOT/path
        if args.verify:
            assert target.exists() and target.read_bytes()==data,("OUTPUT_DIFF",str(path))
        else:
            target.parent.mkdir(exist_ok=True,parents=True)
            target.write_bytes(data)
        print("VERIFY" if args.verify else "CREATE",path,len(data))
    print("PASS INT4-C: 6343 exceptions, 81641 slots, 2256 texture identities")


if __name__=="__main__":
    main()
