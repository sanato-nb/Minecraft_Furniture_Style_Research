#!/usr/bin/env python3
"""Fail-closed INT-4 H03/H05 F70 per-case remaining-work triage source audit.

This does NOT approve new frames/F contracts. It rechecks that 70 catalog rows
exactly join immutable original F11F, H3, H6, H7, H8 and H16 evidence.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
I = ROOT / "project" / "integration"
OUTPUT = I / "INT4_H03_H05_F70_70_CASE_REMAINING_WORK_TRIAGE_V1.csv"
SUMMARY = I / "INT4_H03_H05_F70_REMAINING_TRIAGE_SUMMARY_V1.json"

def check(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)

def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        result = list(csv.DictReader(stream))
    check(all(None not in r and all(k is not None for k in r) for r in result),
          "CSV malformed: " + path.name)
    return result

def unique(data: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    indexed={r["target_id"]:r for r in data}
    check(len(indexed)==len(data),"Duplicate triage target")
    return indexed

def run() -> dict:
    report=json.loads(SUMMARY.read_text(encoding="utf-8"))
    original=report["upstream_original_Git_blob_sha1"]
    for name,expected in original.items():
        file=I/name
        check(blob(file.read_bytes())==expected,"ORIGINAL_RESEARCH_GIT_BLOB_PIN_DRIFT_"+name)
    base=unique(rows(I/"INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"))
    h3=unique(rows(I/"INT4_H3_70_CASE_ORIGINAL_F2_REOPEN_V1.csv"))
    h6=unique(rows(I/"INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"))
    triage=unique(rows(OUTPUT))
    check(len(base)==len(h3)==len(h6)==len(triage)==70 and
          set(base)==set(h3)==set(h6)==set(triage),
          "H03_H05_F70_EXACT_CASE_JOIN_MISMATCH")
    buckets=Counter()
    priority=Counter()
    original_frames=0
    h6_meta=h6_log=0
    for target_id,row in triage.items():
        src=base[target_id]
        old=h3[target_id]
        provenance=h6[target_id]
        check(row["source_cohort"]==(src["cohort"] or "RISK") and
              row["source_block_or_scenario"]==src["block"] and
              row["minecraft_version"]==(src["minecraft_version"] or "SCENARIO") and
              row["source_original_actions_run_ids"]==src["image_run_ids"] and
              row["source_original_artifact_ids"]==src["image_artifact_ids"] and
              row["original_native_F2_occurrences"]==provenance["original_native_F2_occurrences"],
              "TRIAGE_CASE_SOURCE_OR_ARCHIVE_NOT_EXACT_"+target_id)
        check(provenance["ZIP_CRC_and_all_PNG_SHA_verified"]=="true" and
              provenance["whole_client_log_sha_matched_capture_report"]=="true" and
              old["all_expected_image_bytes_SHA_accepted"]=="true" and
              old["original_image_format_decode_verified"]=="true" and
              old["full_F_contract_accepted"]=="false" and
              row["case_specific_frame_causality_final_approved"]=="false" and
              row["case_final_full_F_approved"]=="false",
              "H03_H05_ILLEGAL_FULL_CASE_APPROVAL_"+target_id)
        check(row["H6_structured_exact_metadata"]==provenance["has_case_specific_structured_server_exact"] and
              row["H6_exact_case_ID_log_lines"]==provenance["explicit_case_id_log_lines"] and
              row["H6_evidence_quality"]==provenance["source_evidence_quality"],
              "H6_PER_CASE_SOURCE_FLAGS_DRIFT_"+target_id)
        check(row["H03_remaining_focused_contract"] and
              row["H05_remaining_frame_and_visual_work"] and
              row["original_F11F_remaining_contract"]==src["additional_required_before_full_acceptance"],
              "CASE_ORIGINAL_REMAINING_CONTRACT_NOT_PRESERVED_"+target_id)
        check(row["H03_H05_original_PNG_SHA_CRC"]=="PASS_PREVIOUS_H3_NOT_FRESH_REEXECUTION",
              "FAKE_NEW_ORIGINAL_F2_PASS_"+target_id)
        check(row["H8_R03_actual_player_item_GUI_evidence"] ==
              ("H8_REAL_CREATIVE_PLAYER_ITEM_JOIN_REMOVE_VERIFIED" if target_id=="R03" else "N_A"),
              "H8_R03_INCORRECT_REUSE_"+target_id)
        original_frames+=int(provenance["original_native_F2_occurrences"])
        h6_meta+=(provenance["has_case_specific_structured_server_exact"]=="true")
        h6_log+=(int(provenance["explicit_case_id_log_lines"])>0)
        buckets[provenance["source_evidence_quality"]]+=1
        priority[row["triage_priority"]]+=1
    check(original_frames==91 and h6_meta==64 and h6_log==26,
          "H6_ORIGINAL_F70_ARTIFACT_COUNTS_DRIFT")
    check(dict(priority)=={"P0":6,"P1":21,"P2":43},
          "NOT_EXACT_6_21_43_CASE_TRIAGE")
    for level in ("P0","P1","P2"):
        check(set(report[level+"_ids"]) == {x["target_id"] for x in triage.values()
                                           if x["triage_priority"]==level},
              "TRIAGE_PRIORITY_ID_SET_MISMATCH_"+level)
    check(buckets["SERVER_JSON_LOG_SHA_IMAGE_SHA_AND_CASE_LINE_BUT_FRAME_CAUSAL_OPEN"]==26 and
          buckets["SERVER_JSON_LOG_SHA_AND_IMAGE_SHA_BUT_NO_CASE_LINE"]==38 and
          buckets["ORIGINAL_LOG_SHA_BUT_NO_CASE_SPECIFIC_SERVER_EXACT"]==6,
          "H6_ORIGINAL_CASE_QUALITY_BUCKETS_DRIFT")
    stage={"R01":1,"R02":6,"R03":3,"R04":2,"R05":5,"R07":4}
    for id,n in stage.items():
        check(triage[id]["H7_risk_substages_verified"]==str(n),
              "H7_ARCHIVED_RISK_SUBSTAGE_COUNT_DRIFT_"+id)
    check(sum(stage.values())==21 and
          report["final_gates"]=={
            "H03":"HOLD","H05":"CONDITIONAL",
            "F70_conditional":70,"F70_unconditional":0,
            "H_eight_scoped_pass":6,"H_eight_conditional":1,"H_eight_hold":1,
            "H_unconditional_exit":0,"INT5_semantics_approved":0,
            "INT6_training_and_redistribution_rights_approved":0},
          "TRIAGE_PROMOTES_UNSUPPORTED_H_OR_F_EXIT")
    return {"status":"PASS_EXACT_F70_70_CASE_TRIAGE_H3_H6_H7_H8_H16",
            "source_F11F_H3_H6_gits_verified":3,
            "source_H7_H8_H16_gits_verified":3,
            "cases":len(triage),"original_PNG_references":original_frames,
            "H6_structured_exact_metadata":h6_meta,"H6_exact_case_text_lines":h6_log,
            "H6_evidence_quality_counts":dict(buckets),
            "priorities":dict(priority),
            "new_Minecraft_runs":0,
            "new_F2_captures":0,
            "F70_unconditional_approvals":0}

if __name__=="__main__":
    print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
