"""INT-4 H03/H05: evidence-bounded modeling exit, preserving strict history.

This gate does not create new game observations or approve GPU face pixels,
semantic furniture roles, or third-party AI training / redistribution rights.
All inputs are pinned to their actual Git blobs and cross-checked by case ID.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REL = Path("project/integration")
OUT = REL / "INT4_H03_H05_MODELING_SCOPED_EXIT_V1.json"

PINS = {
    "INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V5.csv": "95ee0efa5dda895a8ce08e1291286e775d9a73dd",
    "INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json": "2c7092534d377cdbb5676fa3b96df2ef6b4615bd",
    "INT4_DF_ORIGINAL_EXIT_CONTRACT_REAUDIT_V1.json": "8aef3f0b561cda49b2adb1f32cf96a5d8aa2b149",
    "INT4_DF_F70_CASE_ORIGINAL_EXIT_BLOCKERS_V1.csv": "d3f595a95f812e3f04f5c41c218b6d68299d23a8",
    "INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json": "e67f9c5f2ca4bac01f3e878811ed433f9713109b",
    "INT4_H6_70_CASE_LOG_SOURCE_AUDIT_V1.json": "9a63e0058ccd3344560c4283fbd0551e718feb11",
    "INT4_H5_H03_H05_H06_EXIT_GATE_REASSESSMENT_V1.json": "b4af9222fb3ba5e0713b7dd55bc890a3f01fb777",
}
EXPECTED_GAPS = {
    "ORIGINAL_LOG_SHA_BUT_NO_CASE_SPECIFIC_SERVER_EXACT": 6,
    "SERVER_JSON_LOG_SHA_AND_IMAGE_SHA_BUT_NO_CASE_LINE": 38,
    "SERVER_JSON_LOG_SHA_IMAGE_SHA_AND_CASE_LINE_BUT_FRAME_CAUSAL_OPEN": 26,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError("INT4 scoped exit: " + message)


def git_blob_sha(payload: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()


def pinned_inputs(root: Path = ROOT) -> dict[str, bytes]:
    found = {}
    for filename, sha in PINS.items():
        data = (root / REL / filename).read_bytes()
        require(git_blob_sha(data) == sha, "frozen source drift: " + filename)
        found[filename] = data
    return found


def rows(payload: bytes, label: str) -> dict[str, dict]:
    result = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))
    require(len(result) == 70, label + " is not 70 cases")
    keys = [x["target_id"] for x in result]
    require(len(set(keys)) == len(keys), label + " duplicate target_id")
    return {row["target_id"]: row for row in result}


def adjudicate(pinned: dict[str, bytes]) -> dict:
    def doc(name):
        return json.loads(pinned[name].decode("utf-8"))

    model = rows(pinned["INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V5.csv"], "modeling V5")
    blocks = rows(pinned["INT4_DF_F70_CASE_ORIGINAL_EXIT_BLOCKERS_V1.csv"], "strict F blockers")
    summary = doc("INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json")
    strict = doc("INT4_DF_ORIGINAL_EXIT_CONTRACT_REAUDIT_V1.json")
    h3 = doc("INT4_H3_ALL_F70_ORIGINAL_ARTIFACT_REOPEN_AUDIT_V1.json")
    h6 = doc("INT4_H6_70_CASE_LOG_SOURCE_AUDIT_V1.json")
    h5 = doc("INT4_H5_H03_H05_H06_EXIT_GATE_REASSESSMENT_V1.json")

    require(set(model) == set(blocks), "modeling and original case IDs disagree")
    require(set(model) == {x["target_id"] for x in strict["F"]["original_per_case_classifications"]},
            "modeling and independent strict F results disagree")
    kind = Counter(x["unit_kind"] for x in model.values())
    statuses = Counter(x["modeling_status"] for x in model.values())
    require(kind == {"HISTORICAL_1_5_CASE": 62, "RISK_SCENARIO": 8},
            "F70 modeling population unexpectedly changed")
    require(statuses == {"PASS_MODELING_SCOPE": 62, "PASS_RISK_QUESTION_SCOPE": 8},
            "modeling source does not approve all 70 scoped cases")

    require(summary["combined_review_scope_only"] ==
            {"closed_units": 70, "conditional": 0, "denominator": 70, "hold": 0},
            "H23 modeling V5 summary altered")
    require(summary["historical_modeling"]["pass"] == 62 and
            summary["risk_questions"]["pass"] == 8, "H23 populations drift")
    require(summary["legacy_F70"]["H03"] == "HOLD" and
            summary["legacy_F70"]["H05"] == "CONDITIONAL" and
            summary["legacy_F70"]["unconditional"] == 0,
            "historical strict H/F statuses cannot be promoted")

    require(strict["F"]["original_exact_case_ids"] == 70 and
            strict["F"]["original_F2_image_links"] == 70 and
            strict["F"]["original_strict_F_unconditional"] == 0 and
            strict["F"]["original_strict_F_conditional"] == 70 and
            strict["original_H_gates"] == {"H03": "HOLD", "H05": "CONDITIONAL"},
            "strict F/H original result changed")
    require(strict["F"]["source_quality_bucket_counts"] == EXPECTED_GAPS,
            "strict 6/38/26 buckets modified")
    require(not strict["F"]["full_F_unconditional_approved"] and
            not strict["cross_gate_not_approved"]["INT4_H_full_exit"],
            "strict approval guards modified")

    require(h3["all_20_archive_CRC_checked"] and
            h3["all_20_archive_expected_zip_sha256_verified"] and
            h3["all_91_PNG_decoded"] and
            h3["all_91_native_F2_PNG_sha256_verified"] and
            h3["original_distinct_actions_archive_downloaded"] == 20 and
            h3["recorded_original_PNG_occurrences"] == 91,
            "historical image archive verification missing")
    require(not h3["every_original_case_server_state_log_reopened_and_reapproved"] and
            not h3["native_F2_new_visual_human_per_case_review_performed"],
            "unapproved direct visual work cannot be silently marked completed")

    counts = h6["counts"]
    require(counts["original_client_logs"] == 21 and
            counts["cases_with_capture_image_filename_sha_match"] == 70 and
            counts["archives_with_matching_pinned_client_log"] == 20,
            "historical client log/capture provenance is incomplete")
    require(h6["per_case_evidence_quality"] == EXPECTED_GAPS and
            counts["new_full_frame_causality_approvals"] == 0 and
            counts["full_F_unconditional_approvals"] == 0,
            "legacy F evidence grading changed")
    require(h5["H_gate_scoped_pass"] == 6 and
            h5["H_gate_conditional"] == 1 and h5["H_gate_hold"] == 1 and
            not h5["H_all_eight_gates_fully_satisfied"],
            "historical eight-gate state unexpectedly changed")

    by_strict = {x["target_id"]: x for x in strict["F"]["original_per_case_classifications"]}
    for ident, row in model.items():
        blocker, former = blocks[ident], by_strict[ident]
        require(row["original_f2_run_ids"] == blocker["original_F2_run_ids"] ==
                former["original_F2_run_ids"], ident + " run ID mismatch")
        require(row["original_f2_sha256s"] == blocker["original_F2_sha256s"] ==
                former["original_F2_sha256s"], ident + " PNG SHA mismatch")
        require(bool(row["original_f2_run_ids"] and row["original_f2_sha256s"] and
                     row["evidence_refs"] and row["reason"]),
                ident + " missing mandatory source evidence")
        require(row["legacy_unconditional_F"] == "false" and
                row["runtime_GPU_per_face_approved"] == "false" and
                row["INT5_meaning_approved"] == "false" and
                row["INT6_rights_approved"] == "false",
                ident + " unauthorized approval flag")
        require(row["legacy_disposition"].startswith("CONDITIONAL") and
                blocker["original_F_strict_disposition"] == "CONDITIONAL" and
                blocker["full_F_unconditional_approved"] == "false",
                ident + " original strict disposition changed")
        expected_status = ("PASS_RISK_QUESTION_SCOPE" if row["unit_kind"] == "RISK_SCENARIO"
                           else "PASS_MODELING_SCOPE")
        require(row["modeling_status"] == expected_status,
                ident + " model-only evidence classification changed")

    return {
        "schema": "MCFR_INT4_H03_H05_MODELING_SCOPED_EXIT_V1",
        "decision": "PASS_PINNED_MODELING_RESEARCH_SCOPE_ONLY",
        "modeling_case_count": 70,
        "modeling_historical_pass": 62,
        "modeling_risk_question_pass": 8,
        "modeling_H03": "PASS_SCOPED_MODEL_RENDER_EVIDENCE",
        "modeling_H05": "PASS_SCOPED_HISTORICAL_PROVENANCE",
        "historical_original_ZIP_verified": 20,
        "historical_original_F2_PNG_verified": 91,
        "historical_original_client_logs_indexed": 21,
        "original_strict_H03": "HOLD",
        "original_strict_H05": "CONDITIONAL",
        "original_strict_F_unconditional": 0,
        "original_strict_F_conditional": 70,
        "original_F_evidence_gaps": dict(EXPECTED_GAPS),
        "full_INT4_unconditional_exit": False,
        "full_GPU_face_to_pixel_causality_approved": False,
        "INT5_semantics_approved": 0,
        "INT6_asset_training_redistribution_rights_approved": 0,
        "new_game_executions": 0,
        "new_human_F2_scene_reapprovals": 0,
        "source_git_blobs": dict(sorted(PINS.items())),
        "limits": [
            "Research-only closure for 62 specific models and 8 bounded risk questions, not all future furniture or all game states.",
            "H05 accepts historical ZIP/PNG/log provenance and case-linked source observations; NOT renewed per-case exact frame/server log plus visual causality.",
            "H03 accepts source geometry/UV/blockstate and existing bounded native F2 modeling evidence; NOT per-face GPU pixel reconstruction or exhaustive runtime.",
            "Legacy strict F70 remains 0/70 unconditional, H03 HOLD, H05 CONDITIONAL; INT-4 original full exit remains unapproved.",
            "Existing fixed third-party assets are referenced by source/sha only; no license, AI training or redistribution permission is inferred.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / OUT)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    result = adjudicate(pinned_inputs())
    if args.verify:
        require(json.loads(args.out.read_text(encoding="utf-8")) == result,
                "committed modeling scoped decision is not reproducible")
        print("INT4_MODELING_H03_H05_SCOPED_EXIT_REPLAY_PASS_70_70")
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                            encoding="utf-8")
        print("INT4_MODELING_H03_H05_SCOPED_EXIT_GENERATED_70_70")


if __name__ == "__main__":
    main()
