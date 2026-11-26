"""B29: independent static cross-audit of B24, B26 and B27 45 source elements.

Preserves original role hypotheses without claiming physical function, material,
style, unique GPU face attribution or third-party training rights.
"""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

FILES = {
    "b24": "INT5_B24_45_PART_ORIGINAL_SOURCE_ROLE_SEMANTICS_EVIDENCE_REVIEW_V1.csv",
    "b26": "INT5_B26_HC_MACAW_24_ORIGINAL_F2_SCREEN_SPACE_ELEMENT_REMOVAL_EVIDENCE_V1.csv",
    "b27": "INT5_B27_FULL_45_ORIGINAL_F2_SOURCE_VISUAL_SPATIAL_INDEPENDENT_EVIDENCE_V1.csv",
}
COUNTS = {"AF121": 10, "AF123": 10, "HC11210": 13, "MACAW67": 12}
ROLE_COUNTS = {"LEG_OR_LOWER_POST": 16, "SEAT_LAYER": 6, "LOWER_FRAME": 7, "BACKREST_ASSEMBLY": 16}


def need(ok, why):
    if not ok:
        raise ValueError("INT5_B29_CROSSLEDGER_REJECT: " + why)


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        records = list(csv.DictReader(handle))
    need(records and all(None not in rec for rec in records), "invalid CSV fields " + str(path))
    return records


def key(row, field="source_element_index"):
    return row["model"], int(row[field])


def unique(records, field, name):
    result = {key(row, field): row for row in records}
    need(len(result) == len(records), "duplicate source key in " + name)
    return result


def audit(folder):
    b24, b26, b27 = (rows(folder / FILES[k]) for k in ("b24", "b26", "b27"))
    a = unique(b24, "source_element_index", "B24")
    b = unique(b26, "original_source_element_index", "B26")
    c = unique(b27, "source_element_index", "B27")
    need(len(a) == len(c) == 45 and set(a) == set(c), "45 source keys not identical")
    need(len(b) == 24 and set(b).issubset(set(c)), "B26 must have 24 of 45 original keys")
    need(dict(Counter(rec["model"] for rec in b27)) == COUNTS, "four model population changed")
    need(dict(Counter(rec["source_role_hypothesis_not_approved"] for rec in b24)) == ROLE_COUNTS, "role counts changed")
    texture_cues = Counter(rec["source_texture_cue"] for rec in b24)
    need(texture_cues["GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF"] == 35 and
         sum(texture_cues.values()) == 45, "texture-cue provenance changed")
    need(sum(int(rec["original_source_face_count"]) for rec in b27) == 229, "229 source faces changed")
    need(sum(int(rec["per_case_native_F2_SHA256_verified"]) for rec in b27) == 560, "560 original F2 not accounted")
    need(sum(int(rec["per_case_real_client_logs_SHA256_verified"]) for rec in b27) == 70, "70 original logs not accounted")
    need(sum(int(rec["original_native_F2_SHA256_verified_count"]) for rec in b26) == 384, "B26 384 original F2")
    need(sum(int(rec["original_client_logs_SHA256_verified_count"]) for rec in b26) == 48, "B26 48 original logs")
    visible = set()
    for id, rec in c.items():
        old = a[id]
        need(old["face_count"] == rec["original_source_face_count"], "face count mismatch " + str(id))
        need(old["source_role_hypothesis_not_approved"] == rec["role_hypothesis_not_verified"], "role label mismatch " + str(id))
        need(len(rec["original_GitHub_artifact_ZIP_sha256"]) == 64 and
             rec["original_GitHub_artifact_ZIP_sha256"].isalnum(), "original archive SHA missing")
        if rec["original_element_render_change_bounded_observed"] == "true":
            visible.add(id)
        else:
            need(rec["original_element_render_change_bounded_observed"] == "false", "bad render value")
        for k in ("physical_role_material_style_approved",
                  "original_face_UV_GPU_exclusive_pixel_owner_approved",
                  "third_party_training_redistribution_rights_approved"):
            need(rec[k] == "false", "unauthorized B27 approval " + str(id) + " " + k)
        for k in ("original_element_to_F2_unique_face_pixel_attributed",
                  "role_function_semantics_approved", "material_or_style_approved",
                  "third_party_training_or_redistribution_rights_approved"):
            need(old[k] == "false", "unauthorized B24 approval " + str(id) + " " + k)
        for col in ("south_screen_bbox_xyxy", "north_screen_bbox_xyxy"):
            bbox = rec[col]
            if bbox:
                xy = [int(v) for v in bbox.split("|")]
                need(len(xy) == 4 and 0 <= xy[0] <= xy[2] <= 1024 and
                     0 <= xy[1] <= xy[3] <= 684, "bbox invalid " + str(id))
        if id in b:
            src = b[id]
            for a_name, b_name in (
                ("original_removed_south_changed_pixels", "B26_south_original_F2_removed_pixel_count"),
                ("original_removed_north_changed_pixels", "B26_north_original_F2_removed_pixel_count"),
                ("original_GitHub_artifact_ZIP_sha256", "B26_artifact_original_ZIP_sha256"),
                ("original_removed_east_pixels_if_B19_tested", "B19_additional_east_pixels"),
                ("original_removed_west_pixels_if_B19_tested", "B19_additional_west_pixels"),
            ):
                need(rec[a_name] == src[b_name], "B26↔B27 source discrepancy " + str(id) + ": " + a_name)
            need(rec["direct_visual_audit_batch"] == "B26", "B26 evidence lineage missing")
        else:
            need(rec["direct_visual_audit_batch"] == "B27", "B27 evidence lineage missing")
    need(len(visible) == 43 and set(c) - visible == {("AF121", 5), ("AF123", 5)},
         "bounded source response or 2 exception roles unexpectedly promoted")
    for id in (("AF121", 5), ("AF123", 5)):
        rec = c[id]
        need(int(rec["original_removed_south_changed_pixels"]) == 0 and
             int(rec["original_removed_north_changed_pixels"]) == 0,
             "original two source5 negative controls changed")
    return {
        "schema": "MCFR_INT5_B29_B24_B26_B27_CROSSLEDGER/v1",
        "source_files": FILES,
        "source_rows": {"B24": 45, "B26": 24, "B27": 45},
        "unique_four_model_elements": COUNTS,
        "source_faces": 229,
        "original_native_F2_SHA256_verified_record_sum": 560,
        "original_client_logs_SHA256_verified_record_sum": 70,
        "B26_direct_source_matches": 24,
        "B26_native_F2_sha256_record_sum": 384,
        "B26_logs_sha256_record_sum": 48,
        "source_role_hypothesis_counts_not_approved": ROLE_COUNTS,
        "named_or_contrast_texture_cues_not_material_proof": 10,
        "generic_or_shared_texture_cues": 35,
        "bounded_original_element_removal_visual_response": 43,
        "bounded_original_unchanged_source5": ["AF121#5", "AF123#5"],
        "individual_source_face_UV_GPU_exclusive_owner_approved": 0,
        "role_function_material_style_approved": 0,
        "third_party_training_redistribution_approved": 0,
        "H03": "HOLD", "H05": "CONDITIONAL", "F70_unconditional_approved": 0,
        "scope_note": "Cross-ledger static verification, not re-download of B27 45 original ZIPs and not source-texture semantic proof."
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("project/integration"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    outcome = audit(args.directory)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print("B29_SOURCE45_B24_B26_B27_INDEPENDENT_CROSSLEDGER_PASS", json.dumps(outcome, ensure_ascii=False))


if __name__ == "__main__":
    main()
