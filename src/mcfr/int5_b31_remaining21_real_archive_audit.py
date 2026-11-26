"""B31: re-download the 21 remaining B27 source-experiment ZIP archives.

Unlike B29 static ledger joins this opens original Actions ZIP bytes and verifies
each original F2 PNG and log SHA against the audit/manifest JSON inside the archive.
B26's other 24 archives are NOT downloaded by this job.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile


RECORD_PATH = "INT5_B27_FULL_45_ORIGINAL_F2_SOURCE_VISUAL_SPATIAL_INDEPENDENT_EVIDENCE_V1.csv"


def ensure(cond, why):
    if not cond:
        raise ValueError("B31_ORIGINAL_ARCHIVE_REJECT: " + why)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def original_cases(directory):
    with (directory / RECORD_PATH).open(encoding="utf-8", newline="") as file:
        cases = [row for row in csv.DictReader(file)
                 if row["direct_visual_audit_batch"] == "B27"]
    ensure(len(cases) == 21, "Expected 21 original B27 archive cases")
    ensure(len({(row["model"], row["source_element_index"]) for row in cases}) == 21, "Duplicate case")
    ensure({row["model"] for row in cases} == {"AF121", "AF123", "HC11210"}, "Original model scope changed")
    return cases


def audit_one(row, directory):
    key = row["model"] + "_" + row["source_element_index"]
    path = directory / ("INT5_B31_" + key + ".zip")
    ensure(path.is_file(), "Missing unmodified GitHub ZIP " + key)
    expected = row["original_GitHub_artifact_ZIP_sha256"]
    ensure(sha(path.read_bytes()) == expected, "Original archive SHA256 " + key)
    from PIL import Image
    with ZipFile(path) as z:
        ensure(z.testzip() is None, "ZIP CRC " + key)
        names = z.namelist()
        ensure(len(names) == len(set(names)), "Duplicate original archive member")
        ensure(not any(name.startswith("/") or ".." in Path(name).parts for name in names),
               "Unsafe original archive path")
        logs = [x for x in names if x.endswith(".log")]
        imgs = [x for x in names if x.endswith(".png")]
        auditors = [x for x in names if x.endswith(".json")]
        ensure(len(imgs) == int(row["per_case_native_F2_SHA256_verified"]), "Native F2 count " + key)
        ensure(len(logs) == int(row["per_case_real_client_logs_SHA256_verified"]), "Client log count " + key)
        ensure(auditors and len(auditors) in (2, 4), "Original audit manifest(s) missing")
        audit_values = [json.loads(z.read(name)) for name in auditors]
        # Independent byte verification: file SHA must be found in original embedded
        # evidence JSON, which can differ structurally between B8/B15/B16 captures.
        embedded = json.dumps(audit_values, sort_keys=True)
        for member in imgs:
            raw = z.read(member)
            ensure(sha(raw) in embedded, "F2 SHA not in original JSON: " + key + "/" + member)
            with Image.open(io.BytesIO(raw)) as image:
                ensure(image.format == "PNG" and image.size == (1024, 684),
                       "Native F2 image format/dimensions " + member)
                image.verify()
        for member in logs:
            log = z.read(member)
            ensure(sha(log) in embedded, "Client log SHA not in original JSON: " + key)
            ensure(b"RenderAudit joined the game" in log, "No actual original server join " + key)
        for f in ("physical_role_material_style_approved",
                  "original_face_UV_GPU_exclusive_pixel_owner_approved",
                  "third_party_training_redistribution_rights_approved"):
            ensure(row[f] == "false", "Unauthorized strict approval " + key)
    return {
        "source_element_key": row["model"] + "#" + row["source_element_index"],
        "official_artifact_id": int(row["original_GitHub_artifact_id"]),
        "archive_sha256": expected,
        "archive_crc_verified": True,
        "native_F2_png_sha256_verified": len(imgs),
        "client_log_sha256_verified": len(logs),
        "embedded_source_audit_json_count": len(auditors),
        "original_screen_change_south": int(row["original_removed_south_changed_pixels"]),
        "original_screen_change_north": int(row["original_removed_north_changed_pixels"]),
        "not_newly_recalculated_screen_pixel_causal_metric": True,
        "original_source_face_or_material_final_approved": False,
    }


def audit(directory, zip_directory):
    rows = [audit_one(row, zip_directory) for row in original_cases(directory)]
    ensure(len(rows) == 21 and sum(x["native_F2_png_sha256_verified"] for x in rows) == 176,
           "Original archive count/F2 mismatch")
    ensure(sum(x["client_log_sha256_verified"] for x in rows) == 22, "Original log count mismatch")
    return {
        "schema": "MCFR_INT5_B31_B27_21_ORIGINAL_ZIP_DIRECT_REAUDIT/v1",
        "archive_count_sha256_crc_verified": 21,
        "actual_native_F2_png_sha256_verified": 176,
        "actual_client_log_sha256_verified": 22,
        "scope": "B27 21 original archive IDs not previously B26 24; hash/CRC/F2/log metadata audit only",
        "source_B26_24_not_redownloaded_in_this_batch": True,
        "original_45_corpus_individually_downloaded_in_different_batches": True,
        "H03": "HOLD", "H05": "CONDITIONAL",
        "F70_unconditional_approved": 0,
        "physical_role_material_style_approved": 0,
        "original_face_UV_exclusive_pixel_ownership_approved": 0,
        "third_party_training_and_redistribution_rights_approved": 0,
        "cases": rows,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=Path("project/integration"))
    p.add_argument("--zip-directory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = audit(args.source, args.zip_directory)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("B31_ORIGINAL_21_ZIP_176_F2_22_LOG_SHA_INDEPENDENT_PASS")


if __name__ == "__main__":
    main()
