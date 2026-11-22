#!/usr/bin/env python3
"""INT-4-A: 고정 1-3 모델 원본/부모 체인의 비파괴 증거 인수 감사.

인터넷 다운로드·원본 수정·실게임 실행을 하지 않는다.
기존 B 원본 본문 해시 원장과 C 모델/부모 원장의 16,572개 키를 독립 재조합한다.
이는 *기존 원본 감사의 재사용*이지 상위 모드 소스의 신규 재다운로드가 아니다.
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
INPUT_BLOBS = {
    "research/furniture_mods/phase_1-3/C/mod_furniture_catalog.csv.gz": "412470e5512b7af93f3c91e2db060612f72650e7",
    "research/furniture_mods/phase_1-3/C/MODEL_PARENT_CHAINS.csv.gz": "9a4eeddf419f502bb8fc7808272c7c8336ff9695",
    "research/furniture_mods/phase_1-3/B/source_verification/B_AF_SOURCE_BODIES.csv.gz": "e452cdb71cbe76909b4663c5c40f7a8d7ddd6c68",
    "research/furniture_mods/phase_1-3/B/source_verification/B_HC_SOURCE_BODIES.csv.gz": "21b2f65bfb1fda4f53caca7199ab667ed5ee38c8",
    "research/furniture_mods/phase_1-3/B/source_verification/B_MACAW_SOURCE_BODIES.csv.gz": "983360ac9ced8aff1ee69c85e4fec7426ed71f37",
    "project/integration/INT2_MOD_EXCEPTIONS.csv": "ef1d1f27a5419265084f5bea7be9eecc028f2327",
    "project/integration/INT2_MOD_SOURCE_SUMMARY.json": "5afcc958d89af358bdcc747efaf3cdcf3423608c",
}
COUNTS = {"AF": 1629, "HC": 12394, "MACAW": 2549}
C = "research/furniture_mods/phase_1-3/C/"
B = "research/furniture_mods/phase_1-3/B/source_verification/"
FIELDS = [
    "mod","minecraft","model_key","model_id","path","original_model_sha","original_sha_kind",
    "source_json_bytes","historical_b_source_sha","historical_c_source_sha",
    "declared_parent","chain_keys","terminal_status","terminal_ref","depth",
    "geometry_status","geometry_source_key","own_elements","inherited_elements",
    "effective_elements","effective_faces","parent_missing","no_static",
    "exception_disposition","source_link_status","new_upstream_original_read",
    "history_link","audit_scope"
]


def git_blob_sha(payload: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\\0" + payload).hexdigest()


def load_bytes(path: str) -> bytes:
    value = (ROOT / path).read_bytes()
    observed = git_blob_sha(value)
    assert observed == INPUT_BLOBS[path], f"PINNED_BLOB_CHANGED {path}: {observed}"
    return value


def read_rows(path: str) -> list[dict[str, str]]:
    payload = load_bytes(path)
    if path.endswith(".gz"):
        payload = gzip.decompress(payload)
    return list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"), newline="")))


def sole_key(rows: list[dict[str, str]], field: str, scope: str):
    out = {}
    for row in rows:
        key = row[field]
        if key in out:
            raise AssertionError(f"DUPLICATE_KEY {scope} {key}")
        out[key] = row
    return out


def build():
    catalog = read_rows(C + "mod_furniture_catalog.csv.gz")
    chains = read_rows(C + "MODEL_PARENT_CHAINS.csv.gz")
    assert len(catalog) == len(chains) == 16572, (len(catalog), len(chains))
    chain_index = sole_key(chains, "model_key", "parent_chain")
    id_index = {}
    path_index = {}
    for row in catalog:
        path = (row["mod"], row["path"])
        assert path not in path_index, ("duplicate_c_path", path)
        path_index[path] = row
        id_key = row["model_key"]
        assert id_key not in id_index, ("duplicate_model_key", id_key)
        id_index[id_key] = row
    assert set(chain_index) == set(id_index), "parent chains and catalog keys differ"

    previous = json.loads(load_bytes("project/integration/INT2_MOD_SOURCE_SUMMARY.json"))
    assert previous["measures"]["source_verified_model_files"] == 16572
    assert previous["measures"]["parent_missing"] == 48
    assert previous["measures"]["no_static_models"] == 108

    verified_b = {}
    for mod in COUNTS:
        original = read_rows(B + f"B_{mod}_SOURCE_BODIES.csv.gz")
        models = [r for r in original if r["family"] == "models"]
        assert len(models) == COUNTS[mod], (mod, len(models))
        for row in models:
            key = (mod, row["path"])
            assert key not in verified_b, ("duplicate_b_path", key)
            verified_b[key] = row
    assert len(verified_b) == len(catalog) and set(verified_b) == set(path_index), "B and C model paths differ"

    exceptions = read_rows("project/integration/INT2_MOD_EXCEPTIONS.csv")
    parent_missing = set()
    no_static = set()
    for x in exceptions:
        assert x["exception_type"] in {"PARENT_MISSING", "NO_STATIC_OR_UNRESOLVED"}
        group = parent_missing if x["exception_type"] == "PARENT_MISSING" else no_static
        assert x["resource_id"] not in group, ("duplicate_exception", x)
        group.add(x["resource_id"])
    assert len(parent_missing) == 48 and len(no_static) == 108
    assert len(parent_missing & no_static) == 44

    # The initial exception union is independently recorded; verify it before using it.
    union_path = ROOT / OUT / "INT4_A_EXCEPTION_UNION_V1.csv"
    union_rows = list(csv.DictReader(union_path.open(encoding="utf-8", newline="")))
    union = sole_key(union_rows, "resource_id", "exception_union")
    assert len(union) == 112 and set(union) == parent_missing | no_static

    result = []
    by_mod = Counter()
    status_count = Counter()
    issues = []
    for row in catalog:
        mod = row["mod"]
        key = (mod, row["path"])
        b = verified_b[key]
        ch = chain_index[row["model_key"]]
        resource = row["model_id"]
        assert b["asset_id"] == resource, ("model_id_b_c", key)
        assert b["sha"] == row["source_hash"], ("model_sha_b_c", key)
        assert int(b["bytes"]) > 0
        assert ch["model_id"] == resource, ("model_id_chain", key)
        pm = resource in parent_missing
        ns = resource in no_static
        # Source expectations are explicitly separated from current rendering.
        term = ch["terminal_status"]
        elem = int(row["effective_elements"])
        if bool(term == "PARENT_MISSING") != pm:
            issues.append(["PARENT_TERMINAL_DISCREPANCY",mod,resource,term,pm])
        if bool(elem == 0) != ns:
            issues.append(["NO_STATIC_ELEMENT_DISCREPANCY",mod,resource,elem,ns])
        if pm or ns:
            u = union[resource]
            if int(u["historical_parent_missing"]) != int(pm) or int(u["historical_no_static"]) != int(ns):
                issues.append(["EXCEPTION_UNION_FLAG_MISMATCH",mod,resource])
        code = "PARENT_MISSING_AND_NO_STATIC" if pm and ns else (
            "PARENT_MISSING_ONLY" if pm else ("NO_STATIC_ONLY" if ns else "NO_DECLARED_EXCEPTION")
        )
        by_mod[mod] += 1
        status_count[code] += 1
        result.append({
            "mod": mod, "minecraft":row["minecraft"], "model_key":row["model_key"],
            "model_id":resource, "path":row["path"], "original_model_sha":row["source_hash"],
            "original_sha_kind":"SHA256" if mod=="MACAW" else "GIT_BLOB_SHA1",
            "source_json_bytes":b["bytes"],"historical_b_source_sha":b["sha"],
            "historical_c_source_sha":row["source_hash"],
            "declared_parent":ch["declared_parent"],"chain_keys":ch["chain_keys"],
            "terminal_status":term,"terminal_ref":ch["terminal_ref"],"depth":ch["depth"],
            "geometry_status":row["geometry_status"],"geometry_source_key":row["geometry_source_key"],
            "own_elements":row["own_elements"],"inherited_elements":row["inherited_elements"],
            "effective_elements":row["effective_elements"],"effective_faces":row["effective_faces"],
            "parent_missing":int(pm),"no_static":int(ns),"exception_disposition":code,
            "source_link_status":"MATCHED_HISTORICAL_B_C_AND_CHAIN" if not issues or issues[-1][2] != resource else "REVIEW_CONFLICT",
            "new_upstream_original_read":0,
            "history_link":"INT2_MOD_SOURCE_SUMMARY.json;C/MODEL_PARENT_CHAINS.csv.gz",
            "audit_scope":"STATIC_HISTORY_RECONCILIATION_NOT_NEW_GAME_RENDER"
        })
    assert dict(by_mod) == COUNTS, by_mod
    assert sum(by_mod.values()) == 16572
    assert status_count["PARENT_MISSING_AND_NO_STATIC"] == 44
    assert status_count["PARENT_MISSING_ONLY"] == 4
    assert status_count["NO_STATIC_ONLY"] == 64
    assert status_count["NO_DECLARED_EXCEPTION"] == 16460
    if issues:
        raise AssertionError("SOURCE_HISTORY_CONFLICTS " + json.dumps(issues[:12],ensure_ascii=False))

    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\\n")
    writer.writeheader()
    writer.writerows(result)
    logical = stream.getvalue().encode("utf-8")
    binary = gzip.compress(logical, compresslevel=9, mtime=0)
    assert gzip.decompress(binary) == logical
    summary = {
        "schema":"MCFR_INT4_A_HISTORY_B_C_MODEL_PARENT_LEDGER/v1",
        "status":"PASS_HISTORY_SOURCE_SHA_AND_PARENT_CHAIN_16572_NOT_NEW_ORIGINAL_RUNTIME",
        "baseline_pr":50,
        "baseline_source_sha":"10d205c6fba019c15fed30fde6f4015ca99fb69c",
        "mod_models": dict(sorted(by_mod.items())),
        "model_rows":len(result),
        "unique_model_keys":len(id_index),
        "model_source_B_C_sha_equal":len(result),
        "model_parent_chain_joined":len(result),
        "exception_status_counts":dict(sorted(status_count.items())),
        "distinct_exception_models":112,
        "parent_missing":48,
        "no_static":108,
        "overlap_missing_and_no_static":44,
        "exception_union_sha256":hashlib.sha256(union_path.read_bytes()).hexdigest(),
        "input_git_blob_sha1": INPUT_BLOBS,
        "ledger_csv_uncompressed_sha256": hashlib.sha256(logical).hexdigest(),
        "ledger_gzip_sha256": hashlib.sha256(binary).hexdigest(),
        "ledger_uncompressed_bytes":len(logical),
        "ledger_compressed_bytes":len(binary),
        "new_original_json_opened":0,
        "new_game_F2_opened":0,
        "int4_A_exit_approved":False,
        "exceptions_terminally_resolved":False,
        "all_int4_completed":False,
        "int5_semantic_approvals":0,
        "int6_ai_rights_approvals":0,
        "limitations":[
            "Reconciles pinned historic B byte/hash ledgers and C parent tables; original upstream ZIP/JAR not reopened this run.",
            "PARENT_MISSING is a source path status, not an observed broken runtime mesh.",
            "Historical 48 parent missing are not reached from pinned static blockstate/item parent chains; dynamic loaders not excluded.",
            "Reused full-history source matching is not equivalent to INT-4-A final exception disposition/independent exit.",
            "The original B/C historical gz, JSON, CSV, and PR runtime artifacts remain unchanged."
        ]
    }
    summary_text = json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True) + "\\n"
    report = f"""# INT-4-A 고정 모델·부모 원장 재연결 실행 결과

- 범위: AF {by_mod['AF']:,}, HC {by_mod['HC']:,}, MACAW {by_mod['MACAW']:,}, 총 **{len(result):,}개 모델**.
- 기존 B 원본 SHA 레코드와 C 모델 SHA·부모 체인: **{len(result):,}/{len(result):,}개 대응**.
- 부모 누락 모델 **48개**, 정적 기하 없음/미해결 **108개**, 중복 **44개**, 서로 다른 예외 모델 **112개**.
- 일반 모델 **16,460개**, 부모 누락 단독 4개, 정적 미해결 단독 64개, 두 조건 동시 44개.
- 예외 112개에는 원본 소스 경로/해시와 부모 종단·정적 요소 수를 연결했다. 예외의 존재 자체는 렌더 실패의 증거가 아니다.

## 검증 수준
**과거 원본 B·C 데이터를 새 단계의 개별 원장으로 교차 연결한 결과**이며, 새 모드 원본 JAR/ZIP을 다운로드해 각 모델을 다시 열거나 Minecraft F2를 촬영한 결과는 아니다. source SHA는 과거 성공한 독립 원본 감사의 B값이며, 현재 그 기록과 C 파일·부모체인이 일치했음을 의미한다.

## 파일
- \`INT4_A_MODEL_PARENT_LEDGER_V1.csv.gz\`: 모델 {len(result):,}행 (모델 경로, source SHA, 제공자, parent chain, 기하/예외 상태, 감사 방법).
- \`INT4_A_EXCEPTION_UNION_V1.csv\`: 중복 제거 112모델의 보존형 선행 예외 목록.
- \`INT4_A_MODEL_PARENT_AUDIT_V1.json\`: 분모/검사 수/원본 파일 Git blob SHA/결과 SHA/해석 경계.
- 기존 원본은 변경하지 않는다.

## 남은 INT-4-A 완료 게이트
원본 감사 재사용을 별도 인수 승인으로 기록하고, 112예외의 기하/도달 가능성/동적 모델 의미를 분리하여 각 예외의 사유·후속 담당·조건부 종료 가능 여부를 독립 심사해야 한다. 이 보고서만으로 INT-4-A 전체 종료/INT-4 최종 종료는 승인하지 않는다.

## 후속 단계
A 확정 후 B의 105,383 요소·592,312면 검증으로 넘어간다. INT-5 의미 판단·INT-6 학습/재배포 권리는 모두 별도이며 승인 0건.
"""
    return {OUT / "INT4_A_MODEL_PARENT_LEDGER_V1.csv.gz":binary,
            OUT / "INT4_A_MODEL_PARENT_AUDIT_V1.json":summary_text.encode("utf-8"),
            OUT / "INT4_A_MODEL_PARENT_REPORT_V1.md":report.encode("utf-8")}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args()
    outputs=build()
    for relative, data in outputs.items():
        full=ROOT/relative
        if args.verify:
            assert full.exists(), f"MISSING_GENERATED {relative}"
            assert full.read_bytes()==data, f"REPRODUCIBILITY_MISMATCH {relative}"
        else:
            full.parent.mkdir(parents=True,exist_ok=True)
            full.write_bytes(data)
        print(f"{'VERIFIED' if args.verify else 'CREATED'} {relative}: {len(data):,} bytes")
    print("PASS_INT4_A_HISTORY_B_C_16572_WITH_112_EXCEPTIONS")


if __name__=="__main__":
    main()
