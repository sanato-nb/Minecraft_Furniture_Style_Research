#!/usr/bin/env python3
"""INT-4-A: 고정 증거를 인수해 112개 예외와 16,572 모델별 처분을 기록한다.

원본 JAR 재다운로드, 실제 게임 F2 검사, 보이지 않는 부모 모델 합성은 수행하지 않는다.
기존 역사 증거의 Git blob SHA를 고정하고 누락/정적 비도달/생성 아이템을 구분한다.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import gzip
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path("project/integration")
FILES = {
    "project/integration/INT4_A_MODEL_PARENT_LEDGER_V1.csv.gz":
        "d72c2f07fcbbba09dc610f09a95bfced84c51930",
    "project/integration/INT4_A_MODEL_PARENT_AUDIT_V1.json":
        "3959a0af39445a272ae4eadc461fc94f669eb178",
    "project/integration/INT4_A_EXCEPTION_UNION_V1.csv":
        "f297c308a4012fc12d78739d10e3e660554c6f5d",
    "project/integration/INT4_PARENT_48_ORIGINAL_AUDIT_RESULT.json":
        "6b2aefda483058d84aa7d65327656fe6db137581",
    "project/integration/INT4_PARENT_48_BLOCKSTATE_AUDIT_RESULT.json":
        "919bb491eb63f93e216caf0dbc32b8c27fcafc75",
    "research/furniture_mods/phase_1-3/C/C_AUDIT.json":
        "32de17199b77d818230ffdb0664555a11d78794f",
}
EVIDENCE = {
    "source": "project/integration/INT4_A_MODEL_PARENT_AUDIT_V1.json",
    "parent48": "project/integration/INT4_PARENT_48_ORIGINAL_AUDIT_RESULT.json",
    "static48": "project/integration/INT4_PARENT_48_BLOCKSTATE_AUDIT_RESULT.json",
    "geometry": "research/furniture_mods/phase_1-3/C/C_AUDIT.json",
}
CASES = {
    "STATIC_REUSED": 16460,
    "PARENT_MISSING_PARTIAL_STATIC_UNREACHABLE": 4,
    "PARENT_MISSING_NO_ELEMENTS_STATIC_UNREACHABLE": 44,
    "BASE_MODEL_NO_EXPLICIT_ELEMENTS": 6,
    "GENERATED_ITEM_NO_STATIC_CUBOIDS": 58,
}
MODEL_FIELDS = [
    "mod", "minecraft", "model_key", "resource_id", "source_path", "source_sha",
    "source_hash_kind", "parent_status", "missing_parent_resource",
    "geometry_status", "own_elements", "effective_elements", "effective_faces",
    "exception_class", "static_blockstate_item_reachability", "source_disposition",
    "int4_a_review_result", "runtime_visual_status", "required_followup_stage",
    "next_action", "evidence_refs", "source_scope", "generated_in_int4_a_v2"
]
EXTRA_FIELDS = [
    "exception_cause", "parent_missing_original_verified",
    "static_blockstate_item_unreachable_verified", "new_runtime_test",
    "eligible_for_static_cuboid_geometry", "auto_parent_repaired",
    "semantic_or_rights_approved"
]
COUNT_MODS = {"AF": 1629, "HC": 12394, "MACAW": 2549}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + bytes([0]) + data).hexdigest()


def locked_bytes(path: str) -> bytes:
    body = (ROOT / path).read_bytes()
    current = git_blob_sha(body)
    assert current == FILES[path], ("SOURCE_BLOB_DRIFT", path, current)
    return body


def locked_json(path: str) -> dict:
    return json.loads(locked_bytes(path).decode("utf-8"))


def rows_from_bytes(content: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(content.decode("utf-8-sig"), newline="")))


def csv_bytes(rows: list[dict], fields: list[str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def classify(row: dict, historical: dict | None) -> dict:
    """원본 재생성 사실과 실행 전제/추론을 혼동하지 않는 결정 트리."""
    mod = row["mod"]
    resource = row["model_id"]
    geometry = row["geometry_status"]
    term = row["terminal_status"]
    own = int(row["own_elements"])
    effective = int(row["effective_elements"])
    pm = bool(int(row["parent_missing"]))
    ns = bool(int(row["no_static"]))
    if historical is None:
        assert not pm and not ns
        assert geometry in {"LOCAL", "VANILLA"}, (resource, geometry)
        assert effective > 0 and term != "PARENT_MISSING"
        return {
            "exception_class": "STATIC_REUSED",
            "static_blockstate_item_reachability": "NOT_ASSESSED_FOR_NORMAL_16460",
            "source_disposition": "REUSED_SOURCE_SHA_PARENT_CHAIN_AND_EFFECTIVE_GEOMETRY",
            "int4_a_review_result": "VERIFIED_REUSED_STATIC_SCOPE",
            "required_followup_stage": "INT4_B_C_D_WHEN_APPLICABLE",
            "next_action": "Retain exact source identity; evaluate faces, textures, blockstates separately",
            "exception_cause": "NONE_DECLARED",
        }

    assert int(historical["historical_parent_missing"]) == int(pm)
    assert int(historical["historical_no_static"]) == int(ns)
    assert historical["resource_id"] == resource
    if pm:
        assert term == "PARENT_MISSING"
        assert historical["static_selection_reachability"] == "NOT_REACHED_IN_PINNED_STATIC_BLOCKSTATE_OR_ITEM_CHAIN"
        if mod == "AF":
            assert not ns and geometry == "PARTIAL_OWN_OR_LOCAL_GEOMETRY"
            assert effective > 0 and own > 0
            assert row["terminal_ref"] == "minecraft:lantern"
            category = "PARENT_MISSING_PARTIAL_STATIC_UNREACHABLE"
            cause = "Missing minecraft:lantern parent; pinned child retains geometry"
        else:
            assert mod == "MACAW" and ns and own == effective == 0
            assert geometry == "UNRESOLVED_PARENT"
            assert row["terminal_ref"] in {
                "mcwfurnitures:block/parent/desk",
                "mcwfurnitures:block/parent/drawer_base",
            }
            category = "PARENT_MISSING_NO_ELEMENTS_STATIC_UNREACHABLE"
            cause = "Pinned parent file absent and no child cuboids"
        return {
            "exception_class": category,
            "static_blockstate_item_reachability": "UNREACHABLE_ALL_48_IN_PRIOR_PINNED_STATIC_SOURCE_SCAN",
            "source_disposition": "PARENT_FILE_ABSENT_IN_PINNED_ORIGINAL_NOT_MODIFIED",
            "int4_a_review_result": "CONDITIONAL_STATIC_SOURCE_EXCEPTION",
            "required_followup_stage": "INT4_D_DYNAMIC_CODE_REFERENCE_IF_RELEVANT",
            "next_action": "Do not synthesize fake blockstates/F2; check dynamic code registration or loader references before optional runtime tests",
            "exception_cause": cause,
        }

    assert ns and not pm and effective == 0
    assert historical["static_selection_reachability"] == "NOT_CHECKED_BY_PARENT48_AUDIT"
    if geometry == "NONE":
        assert mod == "HC" and resource.startswith("handcrafted:block/base/") and own == 0
        return {
            "exception_class": "BASE_MODEL_NO_EXPLICIT_ELEMENTS",
            "static_blockstate_item_reachability": "NOT_EVALUATED_FOR_THIS_6_MODEL_SET",
            "source_disposition": "EMPTY_STATIC_MODEL_CHAIN_CONFIRMED_HISTORICALLY",
            "int4_a_review_result": "HOLD_MODEL_USAGE_AND_RENDER_PATH",
            "required_followup_stage": "INT4_D_BLOCKSTATE_AND_DYNAMIC_CODE",
            "next_action": "Check source-state use and model assembly; no runtime defect inferred from empty JSON cuboids",
            "exception_cause": "Handcrafted base model contains no explicit effective static elements",
        }
    assert geometry == "GENERATED_ITEM_RUNTIME" and term == "BUILTIN" and own == 0
    assert ":item/" in resource
    return {
        "exception_class": "GENERATED_ITEM_NO_STATIC_CUBOIDS",
        "static_blockstate_item_reachability": "NOT_EVALUATED_FOR_THIS_58_MODEL_SET",
        "source_disposition": "ITEM_GENERATED_BUILTIN_NO_STATIC_CUBOID_CHAIN",
        "int4_a_review_result": "NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY",
        "required_followup_stage": "INT4_D_ITEM_DEFINITIONS_AND_OPTIONAL_F_RUNTIME",
        "next_action": "Assess generated/item renderer and item definitions separately; do not call this a missing 3D mesh",
        "exception_cause": "Generated-item path; not a cuboid model in pinned JSON chain",
    }


def build() -> dict[Path, bytes]:
    audit = locked_json(EVIDENCE["source"])
    original = locked_json(EVIDENCE["parent48"])["observed"]
    reach = locked_json(EVIDENCE["static48"])["observed"]
    geometry_audit = locked_json(EVIDENCE["geometry"])
    assert audit["status"] == "PASS_HISTORY_SOURCE_SHA_AND_PARENT_CHAIN_16572_NOT_NEW_ORIGINAL_RUNTIME"
    assert audit["model_rows"] == audit["model_parent_chain_joined"] == 16572
    assert audit["distinct_exception_models"] == 112
    assert audit["exception_status_counts"] == {
        "NO_DECLARED_EXCEPTION": 16460, "NO_STATIC_ONLY": 64,
        "PARENT_MISSING_AND_NO_STATIC": 44, "PARENT_MISSING_ONLY": 4,
    }
    assert original["summary"]["still_missing_exact_parent_targets"] == 48
    assert original["summary"]["with_own_source_geometry"] == 4
    assert original["summary"]["without_own_source_geometry"] == 44
    assert original["summary"]["unresolved_parent_ref_occurrences"] == {
        "minecraft:lantern": 4,
        "mcwfurnitures:block/parent/desk": 22,
        "mcwfurnitures:block/parent/drawer_base": 22,
    }
    assert reach["summary"]["historical_missing_parent_model_paths"] == 48
    assert reach["summary"]["in_static_blockstate_source_selection_or_parent_chain"] == 0
    assert reach["summary"]["item_model_or_parent_chain_reachable"] == 0
    assert reach["summary"]["not_reachable_from_static_blockstates"] == 48
    assert geometry_audit["geometry_status"] == {
        "AF|GENERATED_ITEM_RUNTIME": 1,
        "AF|LOCAL": 1624,
        "AF|PARTIAL_OWN_OR_LOCAL_GEOMETRY": 4,
        "HC|GENERATED_ITEM_RUNTIME": 55,
        "HC|LOCAL": 12110,
        "HC|NONE": 6,
        "HC|VANILLA": 223,
        "MACAW|GENERATED_ITEM_RUNTIME": 2,
        "MACAW|LOCAL": 2503,
        "MACAW|UNRESOLVED_PARENT": 44,
    }
    ledger_raw = locked_bytes("project/integration/INT4_A_MODEL_PARENT_LEDGER_V1.csv.gz")
    assert sha256(ledger_raw) == audit["ledger_gzip_sha256"]
    ledger = rows_from_bytes(gzip.decompress(ledger_raw))
    union = rows_from_bytes(locked_bytes("project/integration/INT4_A_EXCEPTION_UNION_V1.csv"))
    assert len(ledger) == 16572 and len(union) == 112
    union_by_id = {r["resource_id"]: r for r in union}
    assert len(union_by_id) == 112
    assert len({r["model_id"] for r in ledger}) == 16572

    mod_count = Counter()
    classification = Counter()
    dispositions = Counter()
    evidence_counters = Counter()
    out_rows = []
    exception_rows = []
    for row in ledger:
        mod_count[row["mod"]] += 1
        resource = row["model_id"]
        historical = union_by_id.get(resource)
        found = classify(row, historical)
        category = found["exception_class"]
        classification[category] += 1
        dispositions[found["int4_a_review_result"]] += 1
        if historical:
            evidence_counters["exception_rows_with_original_sha"] += 1
        if row["source_link_status"] != "MATCHED_HISTORICAL_B_C_AND_CHAIN":
            raise AssertionError(("upstream_model_history_sha_disagreement", resource))
        assert row["historical_b_source_sha"] == row["historical_c_source_sha"] == row["original_model_sha"]
        assert row["new_upstream_original_read"] == "0"
        base = {
            "mod":row["mod"], "minecraft":row["minecraft"],
            "model_key":row["model_key"], "resource_id":resource,
            "source_path":row["path"],"source_sha":row["original_model_sha"],
            "source_hash_kind":row["original_sha_kind"],
            "parent_status":row["terminal_status"],
            "missing_parent_resource":row["terminal_ref"] if bool(int(row["parent_missing"])) else "",
            "geometry_status":row["geometry_status"],
            "own_elements":row["own_elements"],"effective_elements":row["effective_elements"],
            "effective_faces":row["effective_faces"],
            "exception_class":category,
            "static_blockstate_item_reachability":found["static_blockstate_item_reachability"],
            "source_disposition":found["source_disposition"],
            "int4_a_review_result":found["int4_a_review_result"],
            "runtime_visual_status":"NOT_VERIFIED_BY_THIS_STATIC_REVIEW",
            "required_followup_stage":found["required_followup_stage"],
            "next_action":found["next_action"],
            "evidence_refs":"|".join(EVIDENCE.values()),
            "source_scope":"HISTORICAL_ORIGINAL_SHA_REUSED_NOT_NEW_JAR_READ",
            "generated_in_int4_a_v2":"true",
        }
        out_rows.append(base)
        if historical:
            exception_rows.append({
                **base,
                "exception_cause":found["exception_cause"],
                "parent_missing_original_verified":"true" if bool(int(row["parent_missing"])) else "false",
                "static_blockstate_item_unreachable_verified":"true" if bool(int(row["parent_missing"])) else "not_checked",
                "new_runtime_test":"false",
                "eligible_for_static_cuboid_geometry":"true" if int(row["effective_elements"]) > 0 else "false",
                "auto_parent_repaired":"false",
                "semantic_or_rights_approved":"false",
            })
    assert dict(mod_count) == COUNT_MODS, dict(mod_count)
    assert dict(classification) == CASES, dict(classification)
    assert len(exception_rows) == 112
    assert len({r["resource_id"] for r in exception_rows}) == 112
    assert len(out_rows) == 16572
    assert set(union_by_id) == {r["resource_id"] for r in exception_rows}
    assert all(r["runtime_visual_status"] == "NOT_VERIFIED_BY_THIS_STATIC_REVIEW" for r in out_rows)

    # The disposition cannot promote partial/static absence to a game defect.
    assert dispositions["VERIFIED_REUSED_STATIC_SCOPE"] == 16460
    assert dispositions["CONDITIONAL_STATIC_SOURCE_EXCEPTION"] == 48
    assert dispositions["HOLD_MODEL_USAGE_AND_RENDER_PATH"] == 6
    assert dispositions["NOT_APPLICABLE_TO_JSON_CUBOID_GEOMETRY"] == 58

    exception_blob = csv_bytes(exception_rows, MODEL_FIELDS + EXTRA_FIELDS)
    model_csv = csv_bytes(out_rows, MODEL_FIELDS)
    model_gz = gzip.compress(model_csv, compresslevel=9, mtime=0)
    assert gzip.decompress(model_gz) == model_csv
    summary = {
        "schema":"MCFR_INT4_A_112_EXCEPTION_DISPOSITION_ADOPTION/v2",
        "baseline_pr":51,
        "source_audit_evidence":"INT4_A_MODEL_PARENT_AUDIT_V1.json",
        "all_model_source_paths":16572,
        "model_level_dispositions_recorded":len(out_rows),
        "model_disposition_documentation_percent":100.0,
        "models_by_mod":dict(sorted(mod_count.items())),
        "exception_rows":112,
        "exception_evidence_categories":dict(sorted(classification.items())),
        "review_results":dict(sorted(dispositions.items())),
        "source_sha_joined":16572,
        "independent_original_parent_paths_reopened_historically":48,
        "history_static_reachability_unreachable_48":48,
        "new_upstream_model_originals_opened":0,
        "new_real_client_F2_screenshots_reviewed":0,
        "source_parent_paths_repaired":0,
        "source_parent_missing_remains":48,
        "unresolved_dynamic_runtime_usages":48,
        "model_usage_hold_remaining":6,
        "static_geometry_na_generated_items":58,
        "rights_approvals":0,
        "int5_semantic_approvals":0,
        "progress": {
            "A_model_provenance_reconnected": {"numerator":16572, "denominator":16572},
            "A_model_disposition_documented": {"numerator":16572, "denominator":16572},
            "A_exception_individual_cause_and_followup_documented": {"numerator":112, "denominator":112},
            "A_original_parent_missing_unresolved": 48,
            "A_runtime_usage_unverified": "NOT_MEASURED_ALL_MODELS",
            "A_full_exit": "CONDITIONAL_STATIC_SCOPE_DOCUMENTED_NOT_INDEPENDENT_FULL_EXIT",
            "B_face_evidence_stage_exit": "NOT_EVALUATED",
            "F_real_client_acceptance": "NOT_EVALUATED",
        },
        "inputs_git_blob_sha1":FILES,
        "outputs": {
            "model_dispositions_gz_sha256":sha256(model_gz),
            "model_dispositions_csv_sha256":sha256(model_csv),
            "model_dispositions_row_count":len(out_rows),
            "exception_dispositions_sha256":sha256(exception_blob),
            "exception_dispositions_row_count":len(exception_rows),
        },
        "restrictions": [
            "All 48 source parent paths are still absent; 0 were repaired.",
            "Their pinned static blockstate/item ancestry was not reachable, but Java/dynamic/pack usage is untested.",
            "Six Handcrafted base source models lack effective cuboid elements; use in registered state not verified.",
            "58 generated-item JSON models are outside static cuboid geometry; item rendering correctness not proven.",
            "16460 normal models have reused historical original source hashes, not newly read upstream originals.",
            "No screenshot inspection, game client render claim, semantic approval, or AI training rights."
        ]
    }
    summary_bytes = (json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    report_lines = [
        "# INT-4-A 예외 112개 모델별 판정 및 전체 16,572개 상태 인수",
        "",
        "이 문서는 PR #51의 전수 출처·부모 체인 원장을 읽고, 과거 독립 원본 감사 증거를 예외별로 재연결한 정적 연구 판단이다.",
        "새 원본 ZIP/JAR 또는 실게임 F2를 읽은 실행이 아니다.",
        "",
        "## 모델별 처리 결과",
        "",
        "| 구분 | 수량 | 정적 원본 판정 | 후속 |",
        "|---|---:|---|---|",
        "| 정상 정적 경로 | 16,460 | 기존 B/C 원본 SHA·부모/기하 계보 일치 | B/C/D |",
        "| Another Furniture 랜턴 | 4 | 부모 minecraft:lantern 누락, 자체 기하 있음, 고정 상태·아이템 정적 경로 비도달 | D 동적 참조 여부 |",
        "| Macaw 책상·서랍 | 44 | 부모 2경로 누락, 자체 정적 요소 없음, 고정 상태·아이템 정적 경로 비도달 | D 동적 참조 여부 |",
        "| Handcrafted 기본 모델 | 6 | 체인에 유효 정적 요소 없음; 사용 경로 미검증 | D 모델/상태/코드 |",
        "| 생성 아이템 | 58 | JSON cuboid 모델의 적용 대상 아님; 실제 아이템 렌더 정상 여부 미확인 | D 아이템 정의, 필요시 F |",
        "| 합계 | 16,572 | 16,572개 각각 정적 분류와 후속 조건을 문서화 | 최종 INT-4 종료와 별개 |",
        "",
        "## 원본 증거의 정확한 범위",
        "",
        "- 과거 원본 독립 감사에서 부모 누락 자식 48개를 직접 재개봉하고 총 3종의 누락 부모 ID를 확인했다.",
        "- 그 48개에 대해 기존 고정 AF/Macaw blockstates 및 명시적 item root의 직접 선택/부모 상속 도달이 모두 0이었다.",
        "- 따라서 임의의 블록상태를 만들어 이 48개 자산을 게임에서 실제 깨진 가구로 시연하면 안 된다.",
        "- 이 검사의 범위 밖인 Java/Kotlin 코드, 커스텀 모델 로더, 리소스팩, 실제 동적 선택은 앞으로의 연구 대상으로 남는다.",
        "- Handcrafted 기본 모델 6과 생성 아이템 58은 과거 parent48 사용 여부 조사 대상이 아니므로 해당 48의 0건 결론을 확대 적용하지 않는다.",
        "",
        "## 기록된 산출물",
        "",
        "- INT4_A_MODEL_DISPOSITIONS_V2.csv.gz: 16,572개별 원본 출처 SHA·부모/기하 분류·판정·후속 단계",
        "- INT4_A_EXCEPTION_DISPOSITIONS_V2.csv: 112개별 원본 누락/해당 여부/증거·제약·후속",
        "- INT4_A_ADJUDICATION_SUMMARY_V2.json: 범위·상호배타적 집계·원본/산출물 해시·게이트",
        "",
        "## 단계 상태 / 정직한 분모",
        "",
        "- A 모델별 정적 증거 연결 16,572/16,572, 예외별 처분 사유 기록 112/112 = 문서 기록 완결.",
        "- A 원본 부모 누락 48개는 그대로 보존; 48건의 동적 사용 여부와 여타 런타임 결과는 여전히 미검증.",
        "- 따라서 정적 원장 범위를 조건부 수용하지만 A 독립 최종 종료와 실제 게임 정상 렌더를 100%로 표시하지 않는다.",
        "- INT-4-B/C/D/F/G/H 단계 종료 또는 INT-5/INT-6 의미·권리 승인은 이 결과에서 발생하지 않는다.",
        "",
        "## 다음 실제 작업",
        "",
        "INT-4-B에서 105,383 유효 요소/592,312 면을 원본 제공자·UV·좌표와 행별 연결한다.",
        "INT-4-D에서는 부모 누락 48건의 동적 코드 참조 여부와 Handcrafted 기본 모델 6의 사용 경로를 분리 확인한다.",
        "",
    ]
    report_bytes = ("\n".join(report_lines)).encode("utf-8")
    return {
        OUT / "INT4_A_MODEL_DISPOSITIONS_V2.csv.gz":model_gz,
        OUT / "INT4_A_EXCEPTION_DISPOSITIONS_V2.csv":exception_blob,
        OUT / "INT4_A_ADJUDICATION_SUMMARY_V2.json":summary_bytes,
        OUT / "INT4_A_EXCEPTION_REVIEW_V2.md":report_bytes,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    options = parser.parse_args()
    outputs = build()
    for relative, content in outputs.items():
        path = ROOT / relative
        if options.verify:
            assert path.is_file(), ("NO_GENERATED_FILE", str(relative))
            assert path.read_bytes() == content, ("GENERATED_CONTENT_DRIFT", str(relative))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        print(("VERIFIED" if options.verify else "CREATED"), relative, len(content))
    print("PASS: 16572 models / 112 exceptions / distinct 4+44+6+58")


if __name__ == "__main__":
    main()
