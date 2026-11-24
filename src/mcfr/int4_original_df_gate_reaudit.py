"""INT-4 original D/F exit gates: source-grounded adjudication, not silent promotion.

D: 1,158 fixed mod blockstates, 78,456 selector options, six original
exceptions. F: 70 cases linked to real original F2 evidence, independently
cross-linked to historical log/ZIP inspections. Full D/F runtime and H03/H05
approvals remain ungranted unless their required evidence actually exists.

Check original upstream Another Furniture 4.0.3 fixed commit and raw Git blobs.
Never modify history, invent frame causality, or claim that source-unused implies
a conclusive runtime absence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "project/integration"
OUTPUT = DIR / "INT4_DF_ORIGINAL_EXIT_CONTRACT_REAUDIT_V1.json"
CASE_CSV = DIR / "INT4_DF_F70_CASE_ORIGINAL_EXIT_BLOCKERS_V1.csv"
CASE_CSV_COLUMNS = ("target_id", "original_F2_run_ids", "original_F2_sha256s",
 "source_quality", "source_structured_exact_metadata", "exact_case_log_lines",
 "historical_human_visual_text_present", "original_F_strict_disposition",
 "next_required_evidence", "full_F_unconditional_approved")
REMAINING_BY_QUALITY = {
 "ORIGINAL_LOG_SHA_BUT_NO_CASE_SPECIFIC_SERVER_EXACT": "VERIFY_OR_RECAPTURE_CASE_SPECIFIC_SERVER_STATE_AND_FRAME",
 "SERVER_JSON_LOG_SHA_AND_IMAGE_SHA_BUT_NO_CASE_LINE": "REVIEW_STRUCTURED_EXACT_STATE_TO_FRAME_WITH_ORIGINAL_SCENE",
 "SERVER_JSON_LOG_SHA_IMAGE_SHA_AND_CASE_LINE_BUT_FRAME_CAUSAL_OPEN": "INDEPENDENT_FRAME_TO_STATE_VISUAL_CAUSAL_ADJUDICATION",
}
UPSTREAM = "crispytwig/AnotherFurniture"
SOURCE_COMMIT = "57eb624cbb7f408d43398c7434b0d38d312cb55d"
AF_PREFIX = "common/src/main/resources/assets/another_furniture/"
AF_FILES = {
    "blockstates/birch_chair.json": "fb91fe6fca469381b200fd080a671b5a09e77399",
    "blockstates/spruce_chair.json": "c8a57ceb9f34c255cd6b098deca6628c595be0df",
    "blockstates/unused/white_awning.json": "f1330a172a20d47a24d40288317293bc47c59511",
    "java/AFBlocks.java": "380e721488f3f0cd0a717291a185a5a938ed237d",
}
PINNED = {
    "INT4_D_SOURCE_AUDIT_V1.json": "7617caf488ef2fd2a115c3ae1f3f7350fe1ba8d8",
    "INT4_D_1158_STATE_DISPOSITIONS_V1.csv": "db3ebc8b8df039bc334701bcf1f559fd48fd68c5",
    "INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv": "75d61821a732ddec271314396e6c11335f40d4c3",
    "INT4_G3_6_BLOCKSTATE_ANOMALY_ORIGINAL_REGISTRY_V1.csv": "79b0fcef40125fc834b211d069cb62022f361513",
    "INT4_G5_1158_STATE_SCOPED_DISPOSITIONS_V1.csv": "89c517a3b410866139144bb107c66e6eeefc4332",
    "INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv": "0cfbf3b1b174efc968de35c8466e2af8a9cd41c7",
    "INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv": "f820efd9e85c4cee8df4673a2db4f4d868b4de31",
    "INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv": "54fbaa1b89c29c46106ade51638f8170306a15b0",
    "INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json": "2c7092534d377cdbb5676fa3b96df2ef6b4615bd",
}


def ensure(ok: bool, detail: str) -> None:
    if not ok:
        raise ValueError("INT4 original D/F audit: " + detail)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def read_pinned() -> dict[str, bytes]:
    found = {}
    for filename, expected in PINNED.items():
        p = DIR / filename
        content = p.read_bytes()
        ensure(blob_sha(content) == expected, "frozen historical Git blob drift: " + filename)
        found[filename] = content
    return found


def csv_rows(data: bytes) -> list[dict[str, str]]:
    import io
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    rows = list(reader)
    ensure(bool(rows) and len({tuple(x.items()) for x in rows}) == len(rows),
           "empty or identical duplicate source CSV rows")
    return rows


def fetch_upstream() -> tuple[dict, dict]:
    source = {}
    pins = {}
    headers = {"User-Agent": "MCFR-INT4-original-DF/1"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    for filename, expected in AF_FILES.items():
        if filename == "java/AFBlocks.java":
            p = "common/src/main/java/com/starfish_studios/another_furniture/registry/AFBlocks.java"
        else:
            p = AF_PREFIX + filename
        url = "https://raw.githubusercontent.com/" + UPSTREAM + "/" + SOURCE_COMMIT + "/" + p
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=35) as r:
            content = r.read()
        ensure(blob_sha(content) == expected, "external fixed AF source SHA mismatch " + filename)
        source[filename] = content.decode("utf-8")
        pins[filename] = {"path": p, "git_blob_sha1": expected}
    tree_url = "https://api.github.com/repos/" + UPSTREAM + "/git/trees/" + SOURCE_COMMIT + "?recursive=1"
    req = urllib.request.Request(tree_url, headers=headers)
    with urllib.request.urlopen(req, timeout=55) as r:
        tree = json.loads(r.read())
    ensure(tree.get("truncated") is False, "AF Git tree is truncated")
    index = {item["path"]: item for item in tree["tree"] if item.get("type") == "blob"}
    for entry in pins.values():
        ensure(index[entry["path"]]["sha"] == entry["git_blob_sha1"],
               "source Git tree and downloaded file disagree")
    missing = AF_PREFIX + "models/block/awning/white_double.json"
    ensure(missing not in index, "previous missing double model is now present")
    # The source-path is under unused; not evidence that all Java reflection paths are absent.
    ensure(AF_PREFIX + "blockstates/unused/white_awning.json" in index,
           "unused white awning original path not found")
    ensure("awning" not in source["java/AFBlocks.java"].lower(),
           "named awning now appears in this one registry class")
    return source, {
        "upstream_repository": UPSTREAM,
        "commit": SOURCE_COMMIT,
        "git_tree_truncated": False,
        "pinned_blobs": pins,
        "missing_model_path": missing,
        "missing_model_confirmed_in_this_git_tree": True,
        "unused_directory_original_source_confirmed": True,
        "AFBlocks_java_named_awning_reference": False,
        "entire_registry_runtime_reachability_proven": False,
    }


def adjudicate(original: dict[str, bytes], source: dict[str, str], source_proof: dict) -> dict:
    audit = json.loads(original["INT4_D_SOURCE_AUDIT_V1.json"])
    states = csv_rows(original["INT4_D_1158_STATE_DISPOSITIONS_V1.csv"])
    exceptions = csv_rows(original["INT4_D_6_SOURCE_OPTION_EXCEPTIONS_V1.csv"])
    G3 = csv_rows(original["INT4_G3_6_BLOCKSTATE_ANOMALY_ORIGINAL_REGISTRY_V1.csv"])
    G5 = csv_rows(original["INT4_G5_1158_STATE_SCOPED_DISPOSITIONS_V1.csv"])
    F = csv_rows(original["INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"])
    H6 = csv_rows(original["INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"])
    H_case = csv_rows(original["INT4_H03_H05_P0_P1_P2_70_CASE_NEW_ARCHIVE_REAUDIT_V1.csv"])

    ensure(len(states) == len(G5) == 1158 and len(exceptions) == len(G3) == 6,
           "D fixed source/status ledger count mismatch")
    ensure(sum(int(x["option_count"]) for x in states) == 78456,
           "D options do not sum to 78,456")
    ensure(len({x["state_id"] for x in states}) == 1158, "duplicate blockstate ID")
    ensure({x["state_id"] for x in states} == {x["state_id"] for x in G5},
           "D and G5 state keys differ")
    ensure(sum(int(x["anomaly_option_count"]) for x in states) == 6,
           "D anomaly options not exactly six")
    ensure(sum(int(x["unresolved_model_options"]) for x in states) == 4,
           "D unresolved original source refs not exactly four")
    ensure(audit["state_denominator"] == 1158 and audit["option_rows"] == 78456,
           "original D audit denominator changed")
    ensure(audit["original_reference_status_counts"] == {
        "LOCAL": 78420, "VANILLA_JAR": 32, "UNRESOLVED_MODEL_REF": 4,
    }, "D source reference status distribution drift")

    by_G5 = {x["state_id"]: x for x in G5}
    ensure(Counter(x["G5_disposition"] for x in G5) == {"CONDITIONAL": 1157, "HOLD": 1},
           "D historical conditional/HOLD disposition cannot be silently promoted")
    by_name = {x["state_id"]: x for x in states}
    special_ids = {
        "another_furniture:birch_chair",
        "another_furniture:spruce_chair",
        "another_furniture:unused/white_awning",
    }
    ensure({x["state_id"] for x in exceptions} == special_ids, "unexpected D exception target")
    ensure({x["state_id"] for x in G3} == special_ids, "G3 source exception union drift")
    amended = []
    for x in exceptions:
        ident = x["state_id"]
        ensure(x["state_source_sha"] == by_name[ident]["source_sha"], "wrong D original source ref")
        if "chair" in ident:
            species = ident.split(":")[1].split("_")[0]
            selector = "facing=south,tucked=false,variant=3"
            ensure(x["source_selector"] == selector, "wrong exact chair state")
            f = json.loads(source[f"blockstates/{species}_chair.json"])
            selected = f["variants"][selector]
            ensure(selected["model"] == f"another_furniture:block/chair/{species}_1" and
                   selected.get("y") == 180, "source variant3->1 mismatch")
            category = "EXACT_ORIGINAL_SELECTOR_RECONFIRMED_RUNTIME_INTENT_UNPROVEN"
        else:
            assert ident == "another_furniture:unused/white_awning"
            f = json.loads(source["blockstates/unused/white_awning.json"])
            ensure(f["variants"][x["source_selector"]]["model"] ==
                   "another_furniture:block/awning/white_double", "unused source target drift")
            category = "PINNED_UNUSED_DIRECTORY_AND_MISSING_MODEL_NO_GLOBAL_RUNTIME_INFERENCE"
        amended.append({
            "state_id": ident,
            "source_selector": x["source_selector"],
            "original_model_ref": x["model_id"],
            "original_exception_type": x["exception_type"],
            "strict_D_original_disposition": by_G5[ident]["G5_disposition"],
            "new_verified_fact": category,
            "runtime_defect_confirmed": False,
            "full_registered_runtime_state_approved": False,
        })
    ensure(Counter(x["new_verified_fact"] for x in amended) == {
        "EXACT_ORIGINAL_SELECTOR_RECONFIRMED_RUNTIME_INTENT_UNPROVEN": 2,
        "PINNED_UNUSED_DIRECTORY_AND_MISSING_MODEL_NO_GLOBAL_RUNTIME_INFERENCE": 4,
    }, "source controls incomplete")

    ensure(len(F) == len(H6) == len(H_case) == 70,
           "F fixed 70-case evidence ledger count mismatch")
    def by_id(rows):
        d = {x["target_id"]: x for x in rows}
        ensure(len(d) == len(rows), "duplicate F case key")
        return d
    H6_by, Hcase_by = by_id(H6), by_id(H_case)
    F_by = by_id(F)
    ensure(set(F_by) == set(H6_by) == set(Hcase_by), "F/H source case IDs disagree")
    ensure(all(x["image_sha256s"].strip() and x["image_run_ids"].strip() and
               x["image_artifact_ids"].strip() and x["human_observation_text"].strip()
               for x in F), "one or more F records lack native image or historical observation")
    ensure(all(x["runtime_evidence_accepted_as_full_F_PASS"].lower() == "false"
               for x in F), "original strict F ledger changed: no approval without proof")
    ensure(all(x["full_F_exit_approved"].lower() == "false" for x in H6),
           "H6 full F final status changed")
    ensure(all(x["full_F_final_approved"].lower() == "false" for x in H_case),
           "70 independent archive records improperly promoted")
    ensure(all(x["ZIP_CRC_and_all_PNG_SHA_verified"] == "true" and
               x["all_source_artifacts_have_original_logs"] == "true" and
               x["whole_client_log_sha_matched_capture_report"] == "true"
               for x in H6), "F source archive/PNG/log provenance incomplete")
    buckets = Counter(x["source_evidence_quality"] for x in H6)
    ensure(buckets == {
        "SERVER_JSON_LOG_SHA_IMAGE_SHA_AND_CASE_LINE_BUT_FRAME_CAUSAL_OPEN": 26,
        "SERVER_JSON_LOG_SHA_AND_IMAGE_SHA_BUT_NO_CASE_LINE": 38,
        "ORIGINAL_LOG_SHA_BUT_NO_CASE_SPECIFIC_SERVER_EXACT": 6,
    }, "H6 original F quality buckets changed")
    F_rows = []
    for ident, row in sorted(F_by.items()):
        h, archive = H6_by[ident], Hcase_by[ident]
        ensure(row["final_disposition"] == h["original_F70_disposition"],
               "F11F and H6 source target statuses differ " + ident)
        ensure(h["has_capture_record_exact_image_name_and_sha"] == "true",
               "F target lacks exact recorded image filename and SHA")
        F_rows.append({
            "target_id": ident,
            "original_F2_run_ids": row["image_run_ids"],
            "original_F2_sha256s": row["image_sha256s"],
            "source_quality": h["source_evidence_quality"],
            "historical_human_visual_text_present": True,
            "original_archive_zip_png_log_recheck": archive["original_zip20_crc_sha_new_audit"],
            "exact_case_log_lines": int(h["explicit_case_id_and_exact_same_log_lines"]),
            "source_structured_exact_metadata": h["has_case_specific_structured_server_exact"] == "true",
            "strict_original_F_disposition": "CONDITIONAL",
            "full_F_unconditional_approved": False,
            "full_frame_state_or_GPU_face_pixel_causality_approved": False,
        })
    ensure(Counter(x["strict_original_F_disposition"] for x in F_rows) == {"CONDITIONAL": 70},
           "F case strict source disposition mismatch")

    model_summary = json.loads(original["INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json"])
    ensure(model_summary["combined_review_scope_only"] ==
           {"closed_units": 70, "conditional": 0, "denominator": 70, "hold": 0},
           "separate modeling-only contract altered")
    ensure(model_summary["legacy_F70"]["unconditional"] == 0 and
           model_summary["legacy_F70"]["conditional"] == 70 and
           model_summary["legacy_F70"]["H03"] == "HOLD" and
           model_summary["legacy_F70"]["H05"] == "CONDITIONAL",
           "historical original exit gates shifted")
    return {
        "schema": "MCFR_INT4_ORIGINAL_DF_SOURCE_AND_FULL_EXIT_SEPARATION_V1",
        "fixed_source": {
            "repo": "https://github.com/sanato-nb/Minecraft_Furniture_Style_Research",
            "pinned_github_git_blobs": PINNED,
            "AF_403_original_source": source_proof,
        },
        "D": {
            "original_blockstates_examined": 1158,
            "original_selector_options_examined": 78456,
            "source_reference_status": audit["original_reference_status_counts"],
            "source_data_and_exceptions_disposition_coverage": "1158/1158",
            "source_static_scope_exhaustive": True,
            "strict_original_scope_conditional": 1157,
            "strict_original_scope_HOLD": 1,
            "six_exception_rows_actual_source_verified": amended,
            "all_mod_release_registration_and_live_reachability_proven": False,
            "full_D_unconditional_approved": False,
            "decision": "SOURCE_SCOPE_CLOSED_WITH_EXPLICIT_EXCEPTIONS__NOT_FULL_RUNTIME_EXIT",
        },
        "F": {
            "original_exact_case_ids": len(F_rows),
            "original_F2_image_links": 70,
            "original_20_archives_91_PNG_21_logs_historical_reaudit_inherited_not_newly_downloaded": True,
            "source_quality_bucket_counts": dict(buckets),
            "original_per_case_classifications": F_rows,
            "original_strict_F_conditional": 70,
            "original_strict_F_unconditional": 0,
            "new_native_F2": 0,
            "new_independent_human_full_F_review": 0,
            "full_F_unconditional_approved": False,
            "modeling_only_contract_from_H23": "70/70",
            "decision": "CASE_IMAGE_SOURCE_SCOPE_CLOSED_70_OF_70__FULL_F_EXIT_STILL_BLOCKED",
        },
        "original_H_gates": {"H03": "HOLD", "H05": "CONDITIONAL"},
        "cross_gate_not_approved": {
            "INT4_G_unconditional": False,
            "INT4_H_full_exit": False,
            "INT5_semantic": False,
            "INT6_AI_asset_training_and_redistribution_rights": False,
        },
        "limits": [
            "Original D's static source 1158/1158 and F's 70/70 F2 provenance do not prove runtime all-state or GPU-per-face causality.",
            "AF 4.0.3 Git source != official Fabric 4.0.2 JAR across every state; selected comparisons only.",
            "Source path unused and AFBlocks.java absence do not prove no alternate global registrar/reflective renderer.",
            "Historical real PNG, ZIP and client logs are NOT downloaded/reopened in this run; their prior immutable SHA audits are independently joined.",
            "This explicit scoped closure cannot be substituted for strict D/F/H03/H05 unrestricted completion.",
        ],
    }



def blocker_rows(result: dict) -> list[dict[str, str]]:
    rows = []
    for case in result["F"]["original_per_case_classifications"]:
        row = {
            "target_id": case["target_id"],
            "original_F2_run_ids": case["original_F2_run_ids"],
            "original_F2_sha256s": case["original_F2_sha256s"],
            "source_quality": case["source_quality"],
            "source_structured_exact_metadata": str(case["source_structured_exact_metadata"]).lower(),
            "exact_case_log_lines": str(case["exact_case_log_lines"]),
            "historical_human_visual_text_present": str(case["historical_human_visual_text_present"]).lower(),
            "original_F_strict_disposition": case["strict_original_F_disposition"],
            "next_required_evidence": REMAINING_BY_QUALITY[case["source_quality"]],
            "full_F_unconditional_approved": "false",
        }
        ensure(tuple(row) == CASE_CSV_COLUMNS, "F70 blocker row schema drift")
        rows.append(row)
    ensure(len(rows) == 70 and len({x["target_id"] for x in rows}) == 70,
           "F70 blocker records incomplete")
    return rows


def verify_blocker_csv(result: dict, filename: Path = CASE_CSV) -> None:
    with filename.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        ensure(tuple(reader.fieldnames or ()) == CASE_CSV_COLUMNS,
               "F70 blocker CSV column schema changed")
        current = list(reader)
    ensure(current == blocker_rows(result),
           "F70 blocker CSV != immutable source-provenance re-adjudication")
    print("INT4_F70_PERSISTED_70_CASE_BLOCKER_CSV_MATCH")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    p.add_argument("--output", type=Path, default=OUTPUT)
    args = p.parse_args()
    result = adjudicate(read_pinned(), *fetch_upstream())
    if args.verify:
        ensure(json.loads(args.output.read_text(encoding="utf-8")) == result,
               "persistent D/F original gate result differs on independent source replay")
        verify_blocker_csv(result)
        print("INT4_ORIGINAL_D_1158_78456_6_EXCEPTION_F70_REAL_F2_LINKS_REVERIFIED")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                               encoding="utf-8")
        print("INT4_DF_GATE_AUDIT_JSON_START")
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        print("INT4_DF_GATE_AUDIT_JSON_END")


if __name__ == "__main__":
    main()
