"""INT-4 H03/H05 P0/P1/P2: re-open 20 original Actions ZIPs and 91 native F2.

This independent actual-byte audit is intentionally NOT a full GPU/UV, human
semantic or frame exact server-time approval. The on-Git reports never store
original third-party assets. All archive bytes remain in an ephemeral runner.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
S = ROOT / "project" / "integration"
ARCHIVES = "INT4_H3_20_ORIGINAL_ARTIFACT_ZIP_SHA_AUDIT_V1.csv"
PNG91 = "INT4_H3_91_NATIVE_F2_ORIGINAL_PNG_SHA_AUDIT_V1.csv"
H6 = "INT4_H6_70_CASE_LOG_STATE_PROVENANCE_V1.csv"
TRIAGE = "INT4_H03_H05_F70_70_CASE_REMAINING_WORK_TRIAGE_V1.csv"
F11F = "INT4_F11F_70_TARGET_EVIDENCE_DISPOSITIONS_V15.csv"
OUT = "INT4_H03_H05_F70_NEW_ORIGINAL_REOPEN_INDEPENDENT_AUDIT_V1.json"
CSV = "INT4_H03_H05_F70_NEW_70_CASE_ORIGINAL_REOPEN_V1.csv"


def ensure(x, text):
    if not x:
        raise ValueError(text)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def records(name):
    with (S/name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def unique(xs,key):
    d={x[key]:x for x in xs}
    ensure(len(d)==len(xs),"DUPLICATE_ORIGINAL_SOURCE_"+key)
    return d


def mem_hash(zipfile,zmember,expected):
    ensure(zmember in zipfile.namelist(), "SOURCE_ZIP_MISSING_ORIGINAL_PNG_"+zmember)
    raw=zipfile.read(zmember)
    ensure(sha(raw)==expected,"SOURCE_ACTUAL_PNG_SHA_CHANGED_"+zmember)
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        ensure(im.format=="PNG" and im.size==(1024,684),
               "SOURCE_ACTUAL_PNG_NOT_MINECRAFT_F2_"+zmember)
    return raw


def parse_artifacts(folder:Path):
    expected=unique(records(ARCHIVES),"artifact_id")
    ensure(len(expected)==20,"ORIGINAL_ARCHIVE_COUNT_DRIFT")
    source={}
    logs={}
    for aid,row in expected.items():
        path=folder/(aid+".zip")
        ensure(path.is_file(),"ORIGINAL_ACTIONS_ARTIFACT_MISSING_"+aid)
        ensure(sha(path.read_bytes())==row["source_expected_original_zip_sha256"]==
               row["source_reopened_zip_sha256"],
               "ORIGINAL_ACTIONS_ARTIFACT_ZIP_SHA_CHANGED_"+aid)
        with ZipFile(path) as z:
            ensure(z.testzip() is None,"ORIGINAL_ACTIONS_ARTIFACT_ZIP_CRC_FAILED_"+aid)
            source[aid]=set(z.namelist())
            logs[aid]={n:sha(z.read(n)) for n in z.namelist() if n.endswith("client.log")}
    ensure(sum(len(v) for v in logs.values())==21,
           "H6_ORIGINAL_CLIENT_LOGS_COUNT_WRONG")
    return expected, source, logs


def review(folder:Path, output:Path):
    archive_rows,source,logs=parse_artifacts(folder)
    png_rows=records(PNG91)
    h6=unique(records(H6),"target_id")
    triage=unique(records(TRIAGE),"target_id")
    full=unique(records(F11F),"target_id")
    ensure(len(png_rows)==91 and len(h6)==len(triage)==len(full)==70 and
           set(h6)==set(triage)==set(full),"ORIGINAL_70_CASES_OR_91_FRAMES_DRIFT")
    h6_archive=records("INT4_H6_20_REAL_CLIENT_LOG_AND_CAPTURE_SOURCE_V1.csv")
    ensure(len(h6_archive)==20,"H6_20_ARCHIVE_LOG_PROVENANCE_DRIFT")
    for item in h6_archive:
        aid=item["artifact_id"]
        ensure(aid in logs,"H6_REFERENCES_NONEXISTENT_ARCHIVE")
        available=set(logs[aid].values())
        expected=set(item["original_client_log_sha256s"].split("|"))
        ensure(expected==available and item["at_least_one_full_client_log_PIN_matches"]=="true" and
               item["declared_full_client_log_SHA_without_match"]=="0" and
               item["declared_full_client_log_SHA_matches_original_bytes"]==item["original_client_log_count"],
               "H6_REOPENED_CLIENT_LOG_SHA_DIFF_"+aid)
    per_target=defaultdict(list)
    for r in png_rows:
        aid=r["artifact_id"]
        member=r["original_real_zip_png_member"]
        with ZipFile(folder/(aid+".zip")) as z:
            binary=mem_hash(z,member,r["verified_original_png_sha256"])
        ensure(r["verified_original_png_sha256"]==r["expected_original_png_sha256"] and
               r["recorded_zip_sha256"]==archive_rows[aid]["source_expected_original_zip_sha256"] and
               r["actual_png_width"]=="1024" and r["actual_png_height"]=="684" and
               int(r["original_png_bytes"])==len(binary),
               "H3_ORIGINAL_PNG_BYTES_OR_DIMENSION_METADATA_DRIFT_"+aid+":"+member)
        per_target[r["target_id"]].append({
           "artifact_id":aid,
           "member":member,
           "native_F2_sha256":sha(binary),
           "bytes":len(binary),
        })
    ensure(sum(len(v) for v in per_target.values())==91 and len(per_target)==70,
           "F70_91_ORIGINAL_IMAGE_TO_TARGET_MAPPING_BROKEN")
    results=[]
    for case in sorted(full):
        history=full[case]
        trace=h6[case]
        todo=triage[case]
        images=per_target[case]
        expected_shas=[x["native_F2_sha256"] for x in images]
        expected_png_shas=[x for x in history["image_sha256s"].replace("|",";").split(";") if x]
        ensure(Counter(expected_shas)==Counter(expected_png_shas) and
               int(trace["original_native_F2_occurrences"])==len(images) and
               trace["ZIP_CRC_and_all_PNG_SHA_verified"]=="true" and
               trace["whole_client_log_sha_matched_capture_report"]=="true",
               "ORIGINAL_F11F_CASE_SHA_OR_H6_LOG_DRIFT_"+case)
        ids={im["artifact_id"] for im in images}
        ensure(ids==set(todo["source_original_artifact_ids"].split("|")),
               "SOURCE_ACTUAL_GAME_ARTIFACT_WRONG_"+case)
        ensure(history["runtime_evidence_accepted_as_full_F_PASS"]=="false" and
               todo["case_final_full_F_approved"]=="false" and
               history["additional_required_before_full_acceptance"].strip() and
               todo["H03_remaining_focused_contract"].strip() and
               todo["H05_remaining_frame_and_visual_work"].strip(),
               "ORIGINAL_FULL_APPROVAL_WITHOUT_PROOF_"+case)
        text=history["human_observation_text"].strip()
        results.append({
           "target_id":case,
           "priority":todo["triage_priority"],
           "cohort":todo["source_cohort"],
           "source_block":history["block"],
           "version":history["minecraft_version"],
           "original_artifact_ids":"|".join(sorted(ids)),
           "original_F2_reopened_count":len(images),
           "source_status":"ORIGINAL_ZIP_PNG_LOG_SHA_CRC_REOPENED_PASS",
           "h6_structured_server_exact_found":trace["has_case_specific_structured_server_exact"],
           "h6_explicit_case_ID_exact_log_lines":trace["explicit_case_id_and_exact_same_log_lines"],
           "historical_qualitative_observation_recorded":bool(text),
           "old_observation_quote_preserved_in_F11F":bool(text),
           "original_source_release_assessment":history["source_state_and_release_assessment"],
           "new_manual_scene_and_UV_full_reapproval":False,
           "per_frame_game_state_render_causal_full_reapproval":False,
           "source_case_F_full_exit":False,
           "next_step":todo["new_actual_game_run_rule"],
           "screens":images,
        })
    ensure(Counter(x["priority"] for x in results)==Counter({"P0":6,"P1":21,"P2":43}),
           "H03_H05_6_21_43_TRIAGE_ORIGINAL_SCOPE_CHANGED")
    byid={x["target_id"]:x for x in results}
    ensure(byid["S20"]["screens"][0]["native_F2_sha256"]==
           byid["S21"]["screens"][0]["native_F2_sha256"],
           "P0_S20_S21_IDENTICAL_ORIGINAL_F2_COUNTEREXAMPLE_MISSING")
    ensure(set(s["native_F2_sha256"] for s in byid["R07"]["screens"]).issubset(
           set(s["native_F2_sha256"] for s in byid["R02"]["screens"])),
           "P0_R02_R07_FOUR_SHARED_RISK_FRAMES_LOST")
    ensure(byid["R08"]["screens"][0]["native_F2_sha256"]==
           byid["R08"]["screens"][1]["native_F2_sha256"],
           "P0_R08_REPRESENTATIVE_TWO_RELEASE_ORIGINAL_FRAME_CHANGED")
    ensure(len(byid["V11"]["screens"])==4 and
           byid["R05"]["original_F2_reopened_count"]==5 and
           len(byid["R05"]["original_artifact_ids"].split("|"))==2,
           "P0_V11_OR_P1_R05_ORIGINAL_BED_EVIDENCE_COLLAPSED")
    summary={
        "schema":"MCFR_INT4_H03_H05_F70_ALL_ORIGINAL_REOPEN_P0_P1_P2/v1",
        "status":"PASS_REAL_20_ZIPS_21_LOGS_91_PNG_70_CASES_H03_H05_BOUNDED_SOURCE",
        "new_original_zip_downloaded_and_sha_verified":20,
        "real_original_client_log_SHA_verified":21,
        "actual_original_native_F2_independently_read_and_verified":91,
        "case_ids_independently_relinked":70,
        "original_case_count_by_priority":dict(Counter(x["priority"] for x in results)),
        "source_specific_observation_present_count":sum(x["historical_qualitative_observation_recorded"] for x in results),
        "P0_identical_S20_S21_F2_confirmed":True,
        "P0_R02_R07_shared_original_source_frames":4,
        "P0_R08_two_original_F2_identical_one_state_only":True,
        "P0_V11_original_real_frames":4,
        "P1_R05_two_original_game_run_screenshot_groups":True,
        "new_game_runs_this_archive_audit":0,
        "new_original_F2":0,
        "actual_each_frame_server_state_causality_full_reapproved":0,
        "full_F70_approved":0,
        "H03_full_exit":False,"H05_full_exit":False,
        "INT5_semantics_approved":0,"INT6_training_redistribution_rights_approved":0,
        "remaining_boundaries":[
          "This is a NEW independent byte/ZIP/log audit of all archived originals; it does not claim 70 human semantic acceptances.",
          "Existing manual qualitative observations are historical, not new visual renderer/UV attributions.",
          "Case server exact metadata and a screenshot existing in one archive do not independently prove frame-to-state synchrony.",
          "Source/control contradictions and selected new real-Fabric experiments must be logged in a separate result.",
          "Original PNGs, JARs and logs stay in expiring scratch artifacts, never Git."
        ],
        "cases":results,
    }
    output.mkdir(parents=True,exist_ok=True)
    (output/OUT).write_text(json.dumps(summary,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    with (output/CSV).open("w",newline="",encoding="utf-8") as f:
        cols=[k for k in results[0] if k!="screens"]+["per_original_screen_sha256"]
        w=csv.DictWriter(f,fieldnames=cols)
        w.writeheader()
        for x in results:
            w.writerow({**{k:v for k,v in x.items() if k!="screens"},
                        "per_original_screen_sha256":"|".join(s["native_F2_sha256"] for s in x["screens"])})
    return {k:v for k,v in summary.items() if k not in ("cases","remaining_boundaries")}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archives",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(review(args.archives,args.output),ensure_ascii=False,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
