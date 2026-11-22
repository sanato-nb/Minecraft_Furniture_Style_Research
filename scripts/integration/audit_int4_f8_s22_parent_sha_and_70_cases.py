#!/usr/bin/env python3
"""F8 independent SHA-locked audit: update ONLY S22 based on official cube SHA256.

Historical 1-5 CSV is NEVER modified. Conditional source approval is not
baked UV, semantic, functional, copyright or final INT-4-F approval.
"""
import argparse,csv,hashlib,io,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
I=Path("project/integration")
PREV=I/"INT4_F7_70_TARGET_EVIDENCE_DISPOSITIONS_V6.csv"
F7=I/"INT4_F7_ORIGINAL_NATIVE_F2_INDEPENDENT_AUDIT_V1.json"
EX=I/"INT4_F7_S22_VANILLA_PARENT_EXTERNAL_EXCEPTION_V1.json"
OFFICIAL=I/"INT4_F8_S22_OFFICIAL_VANILLA_PARENT_BYTES_V1.json"
SOURCE=Path("research/furniture_mods/phase_1-5/B/APPLICATIONS.csv")
PINS={
 str(PREV):"cd2442ebb5294459041f4931d294e2353e8a84a6",
 str(F7):"a7882c43bafe0f5a4b0adbe0ee6b3597eee4e739",
 str(EX):"e6eacf276641e9688c8fc35a7aec4af57d643302",
 str(OFFICIAL):"a38193951cfbe1842a82871e27e025355caefa08",
 str(SOURCE):"56e6f4c21c50714b97079ec61f7219bea845f179",
}
ORIGINAL_HASH="3e4aacd02e816aeba38f83076596e18ded4cf49c01e17c62d1fce79850ffb84e"
CORRECT_GIT_BLOB="1b9780b479aee527f79bde950656b82f1524128b"
ORIGINAL_SOURCE_SHA256="da2a2c907dfe1fde0a9c5118feaa74efcdb1f91e33533147c9e6c237cb72581e"
PARENT="assets/minecraft/models/block/cube.json"
OUT70=I/"INT4_F8_70_TARGET_EVIDENCE_DISPOSITIONS_V7.csv"
OUT27=I/"INT4_F8_27_PENDING_EXACT_F2_TARGETS_V1.csv"
CORRECTION=I/"INT4_F8_S22_HASH_ALGORITHM_CORRECTION_V1.json"
SUMMARY=I/"INT4_F8_S22_OFFICIAL_PARENT_INDEPENDENT_AUDIT_V1.json"
REPORT=I/"INT4_F8_S22_REVIEW_REPORT_V1.md"

def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def pin(path):
    b=(ROOT/path).read_bytes()
    assert blob(b)==PINS[str(path)],("PINNED_INPUT_CHANGED",str(path),blob(b))
    return b
def rows(b):return list(csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline="")))
def write_csv(data,columns):
    s=io.StringIO(newline="")
    w=csv.DictWriter(s,fieldnames=columns,lineterminator="\n")
    w.writeheader();w.writerows(data)
    return s.getvalue().encode("utf-8")
def write_json(d):return (json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")

def build():
    baseline=rows(pin(PREV))
    audit=json.loads(pin(F7))
    old_ex=json.loads(pin(EX))
    official=json.loads(pin(OFFICIAL))
    source=pin(SOURCE)
    assert sha(source)==ORIGINAL_SOURCE_SHA256
    study=[r for r in rows(source) if r["case"]=="S22"]
    assert len(study)==1 and (
        study[0]["provider_path"],study[0]["provider_sha"],study[0]["model_hash_kind"],
        study[0]["provider"],study[0]["elements"],study[0]["faces"]
    )==(PARENT,ORIGINAL_HASH,"GIT_BLOB_SHA1","V1211-5","1","6")
    assert len(ORIGINAL_HASH)==64 and len(CORRECT_GIT_BLOB)==40
    assert len(baseline)==70 and len({r["target_id"] for r in baseline})==70
    assert (sum(r["final_disposition"].startswith("CONDITIONAL") for r in baseline),
            sum(r["final_disposition"].startswith("HOLD") for r in baseline))==(42,28)
    assert audit["counts"]["F_conditional_now"]==42 and audit["counts"]["F_HOLD_now"]==28
    assert audit["cases"]["S22"]["server_exact_original_state"] is True
    assert audit["cases"]["S22"]["release_model_selection_matches_original"] is True
    assert audit["cases"]["S22"]["disposition"]=="HOLD_EXTERNAL_VANILLA_PARENT"
    assert old_ex["real_client_vanilla_parent_bytes_independently_verified"] is False
    assert old_ex["original_study_parent_git_blob_sha1"]==ORIGINAL_HASH
    base_s22=next(r for r in baseline if r["target_id"]=="S22")
    assert base_s22["final_disposition"].startswith("HOLD")
    assert base_s22["image_sha256s"]==audit["cases"]["S22"]["original_native_F2_sha256"]
    assert base_s22["image_run_ids"]==str(audit["original_game_action_run"])
    assert base_s22["image_artifact_ids"]==str(audit["original_game_artifact_id"])

    assert official["status"]=="PASS_TWO_OFFICIAL_JAR_VERIFIED_S22_PARENT_COMPARISON"
    assert official["historical_case"]=="S22"
    assert official["historical_original_file_SHA256"]==ORIGINAL_SOURCE_SHA256
    assert official["historical_parent_path"]==PARENT
    assert official["historical_original_parent_recorded_hash"]==ORIGINAL_HASH
    assert official["historical_row_declared_hash_kind"]=="GIT_BLOB_SHA1"
    assert official["historical_row_provider_sha_cannot_be_git_blob_sha1"] is True
    assert official["corrected_provider_sha_algorithm_by_official_source"]=="SHA256"
    assert official["F8_S22_parent_binary_exact_eligibility"] is True
    assert set(official["official_versions"])=={"1.21.1","1.21.11"}
    for v,pin_sha1 in (
       ("1.21.1","30c73b1c5da787909b2f73340419fdf13b9def88"),
       ("1.21.11","ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd")
    ):
        x=official["official_versions"][v]
        assert x["official_client_jar_sha1_verified"]==pin_sha1
        assert x["pinned_MCFR_client_sha1"]==pin_sha1
        assert x["cube_asset_path"]==PARENT
        assert x["cube_sha256"]==ORIGINAL_HASH
        assert x["cube_git_blob_sha1"]==CORRECT_GIT_BLOB
        assert (x["cube_element_count"],x["cube_face_count"])==(1,6)
        assert x["cube_parent_block_model_ref"]=="block/block"
        assert x["next_parent_in_official_client"] is True
        assert x["next_parent_top_level_fields"]==["display","gui_light"]
    c=official["comparison"]
    assert c["runtime_1_21_1_cube_SHA256_equals_frozen_1_5_recorded_hash"] is True
    assert c["archived_1_21_11_cube_SHA256_equals_frozen_1_5_recorded_hash"] is True
    assert c["runtime_and_archived_cube_bytes_SHA256_equal"] is True
    assert c["runtime_and_archived_parent_block_semantically_equal"] is False
    assert c["runtime_and_archived_parent_block_world_fields_equal"] is True
    assert c["parent_block_changes_only_item_display_metadata"] is True
    assert official["inherited_block_block_changed_JSON_property_paths"]==["display.on_shelf"]

    old={r["target_id"]:dict(r) for r in baseline}
    for row in baseline:
        if row["target_id"]!="S22":continue
        row["source_state_and_release_assessment"]=(
          "F8_TWO_OFFICIAL_CLIENT_CUBE_SHA256_EQUALS_HISTORICAL_PROVIDER_SHA_"
          "GIT_BLOB_SHA1_LABEL_MISCLASSIFIED;PARENT_DISPLAY_ON_SHELF_ONLY")
        row["final_disposition"]=(
          "CONDITIONAL_F8_EXACT_F2_OFFICIAL_CUBE_SHA256_AND_INHERITED_WORLD_FIELDS_MATCH")
        row["additional_required_before_full_acceptance"]=(
          "공식 1.21.1·1.21.11 cube.json SHA256 원본과 연구 S22 provider_sha 동일. "
          "model_hash_kind GIT_BLOB_SHA1은 64자리 SHA256의 잘못된 표기이며 원본 CSV 보존. "
          "상위 block/block.json의 차이는 display.on_shelf뿐. UV 픽셀 인과·아이템 표시·기능·권리·최종 F 종료 별도.")
    changed={r["target_id"] for r in baseline if r!=old[r["target_id"]]}
    assert changed=={"S22"},("UNRELATED_CASE_CHANGED",changed)
    counts=(sum(r["final_disposition"].startswith("CONDITIONAL") for r in baseline),
            sum(r["final_disposition"].startswith("HOLD") for r in baseline))
    assert counts==(43,27)
    historic=[r for r in baseline if r["target_kind"]=="HISTORICAL_1_5_CASE"]
    assert len(historic)==62
    assert sum(r["final_disposition"].startswith("CONDITIONAL") for r in historic)==37
    assert all(r["runtime_evidence_accepted_as_full_F_PASS"]=="false" for r in baseline)
    hold=[r for r in baseline if r["final_disposition"].startswith("HOLD")]
    groups=dict(sorted(Counter(r["cohort"] or "RISK" for r in hold).items()))
    assert groups=={"MACAW":10,"RISK":2,"VANILLA":15}
    raw70=write_csv(baseline,list(baseline[0].keys()))
    fields=["target_id","cohort","minecraft_version","category","block",
            "original_source_applications","original_source_faces","final_disposition",
            "additional_required_before_full_acceptance"]
    raw27=write_csv([{k:r[k] for k in fields} for r in hold],fields)
    corrected={
        "schema":"MCFR_INT4_F8_S22_HASH_KIND_SOURCE_CORRECTION/v1",
        "case_id":"S22","frozen_1_5_source_path":str(SOURCE),
        "frozen_source_SHA256":ORIGINAL_SOURCE_SHA256,
        "original_label":"GIT_BLOB_SHA1",
        "recorded_original_parent_SHA":ORIGINAL_HASH,
        "actual_recorded_hash_algorithm":"SHA256",
        "official_1_21_1_parent_file_SHA256":official["official_versions"]["1.21.1"]["cube_sha256"],
        "official_1_21_11_parent_file_SHA256":official["official_versions"]["1.21.11"]["cube_sha256"],
        "official_parent_git_blob_SHA1":CORRECT_GIT_BLOB,
        "original_research_csv_modified":False,
        "inherited_parent_changed_paths":["display.on_shelf"],
        "inherited_parent_world_fields_stable":True,
        "conditional_but_no_full_render_semantics_approval":True,
    }
    raw_corrected=write_json(corrected)
    summary={
        "schema":"MCFR_INT4_F8_S22_OFFICIAL_PARENT_INDEPENDENT_70_CASE_AUDIT/v1",
        "status":"PASS_SOURCE_CORRECTION_S22_CONDITIONAL_43_HOLD27_FINAL0",
        "pinned_source_git_blob_SHA1":PINS,
        "f7_original_real_game_run":audit["original_game_action_run"],
        "f7_original_real_game_artifact":audit["original_game_artifact_id"],
        "f7_original_F2_SHA256":audit["cases"]["S22"]["original_native_F2_sha256"],
        "f8_official_Mojang_client_SHA_audit_run":45034370140,
        "official_cube_original_SHA256":ORIGINAL_HASH,
        "official_cube_git_blob_SHA1":CORRECT_GIT_BLOB,
        "case_changed_only":"S22",
        "remaining_HOLD_by_cohort":groups,
        "counts":{
            "F_targets":70,"original_study_cases":62,
            "new_F2_images":0,"new_official_Mojang_versions_verified":2,
            "new_conditional_cases":1,
            "conditional_before":42,"conditional_after":43,
            "HOLD_before":28,"HOLD_after":27,
            "original_historic_conditional_F2_before":36,
            "original_historic_conditional_F2_after":37,
            "F_full_unconditional_approval":0,
            "new_INT5_part_semantic_approval":0,
            "new_INT6_AI_training_and_redistribution_rights":0,
            "historic_1_5_research_source_files_changed":0,
        },
        "limits":[
            "64-hex historical S22 parent SHA is SHA256, not a 40-hex Git blob SHA1; source label is inconsistent.",
            "Official 1.21.1 and 1.21.11 cube raw bytes match, parent block/block differs only in display.on_shelf.",
            "F7 original actual-game server state/F2 previously verified; F8 performs no new client game F2 session.",
            "Conditional source provenance does not approve UV pixel causality, item display equivalence, use behavior or rights.",
            "Only S22 disposition metadata changed; all other 69 historical rows remain byte content identical.",
        ],
        "output":{
            "F70":{"rows":70,"sha256":sha(raw70)},
            "pending":{"rows":27,"sha256":sha(raw27)},
            "correction":{"sha256":sha(raw_corrected)},
        },
    }
    report="\n".join([
        "# INT-4-F8 S22 공식 바닐라 cube 부모 SHA 정정과 독립 검증",
        "",
        "- F7에서 실게임 Minecraft 1.21.1 S22 정확 서버 상태 및 모델 선택·원본 F2 확보.",
        "- F8 공식 Mojang 1.21.1/1.21.11 클라이언트 SHA1 검증 후 cube.json 원본 SHA256 비교.",
        "- 연구 S22 provider_sha(64자리)는 SHA256와 일치함. 동일 행 model_hash_kind=GIT_BLOB_SHA1은 오류. 원본 CSV 불변.",
        "- 두 버전 cube.json 바이트 동일; 후속 block/block.json은 display.on_shelf만 다르며 월드 구조 필드 같음.",
        "- S22 HOLD에서 조건부 출처 증거 확보로 전환. 추가 UV·아이템 표시·기능·권리·의미 검증은 별도.",
        "- F70 조건부42→43, HOLD28→27, 역사 사례 조건부 F2 36/62→37/62, 최종 승인0.",
        "- 남은 보류 바닐라15·Macaw10·위험 시나리오2. 본 단계 새 F2 캡처0.",
        "",
    ]).encode("utf-8")
    return {OUT70:raw70,OUT27:raw27,CORRECTION:raw_corrected,
            SUMMARY:write_json(summary),REPORT:report}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--verify",action="store_true")
    a=p.parse_args()
    for name,data in build().items():
        path=ROOT/name
        if a.verify:
            assert path.is_file() and path.read_bytes()==data,("NONDETERMINISTIC",str(name))
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
        print("VERIFIED" if a.verify else "CREATED",name,len(data))
    print("PASS F8 70=43 conditional +27 HOLD. Full accept=0")

if __name__=="__main__":main()
