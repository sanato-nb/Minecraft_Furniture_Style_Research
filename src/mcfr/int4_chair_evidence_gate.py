"""INT-3 fixed-scope exit and INT-4 source-to-F2 evidence cross-check.

Joins original metadata ONLY: 45 geometry part hypotheses, 4 child chairs,
229 UV faces, 228 source options and 16 PR33 Minecraft screenshots.
PR34 recaptures have only a cohort manifest in Git: do not claim that their
individual PNGs have the PR33 hashes. No visual/role/rights approval.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
INPUTS = {
    "db": "project/integration/INT3_KNOWLEDGE_SUMMARY.json",
    "sem": "project/integration/INT3_SEMANTIC_SUMMARY.json",
    "parts": "project/integration/INT3_45_CHAIR_GEOMETRY_REVIEW.csv",
    "uv": "project/integration/INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json",
    "states": "project/integration/INT3_CHAIR_BLOCKSTATE_SOURCE_SUMMARY.json",
    "f2": "project/integration/INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json",
    "iso": "project/integration/INT3_ISOLATED_F2_FINAL_SUMMARY.json",
    "af": "project/integration/INT3_AF_RELEASE_VERSION_COMPARISON.json",
}
DIRECTIONS = ("north", "east", "south", "west")
Y = dict(zip(DIRECTIONS, (0, 90, 180, 270)))
MACAW_Y = dict(zip(DIRECTIONS, (90, 180, 270, 0)))
COUNTS = {"AF121": 10, "AF123": 10, "HC11210": 13, "MACAW67": 12}
ROLES = {"BACKREST_ASSEMBLY": 16, "LEG_OR_LOWER_POST": 16, "LOWER_FRAME": 7, "SEAT_LAYER": 6}


class AuditError(ValueError):
    pass


def ensure(ok, message):
    if not ok:
        raise AuditError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def sha64(data):
    return isinstance(data, str) and bool(re.fullmatch("[0-9a-f]{64}", data))


def read(root=ROOT):
    root = Path(root)
    obj, hashes = {}, {}
    for key, path in INPUTS.items():
        blob = (root / path).read_bytes()
        hashes[path] = sha256(blob)
        if key == "parts":
            obj[key] = list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig"))))
        else:
            obj[key] = json.loads(blob.decode("utf-8-sig"))
    obj["input_sha256"] = hashes
    return obj


def audit(e):
    db, sem, parts = e["db"], e["sem"], e["parts"]
    uv, states, f2, iso, af = e["uv"], e["states"], e["f2"], e["iso"], e["af"]

    ensure(db["status"] == "PASS_FIXED_SCOPE_SOURCE_LINKS_AND_RESEARCH_INTEGRATION",
           "INT3 fixed-source status changed")
    t = db["table_counts"]
    ensure(t["model"] == 16579 and t["model_face_link"] == 592312
           and t["comparison_finding"] == 21 and t["case_application"] == 74
           and t["evidence_exception"] == 139,
           "INT3 integrated database counts changed")
    ensure(db["case_source_model_links"] == {"MODEL_LINKED": 52, "UNMATCHED_SCOPE": 22},
           "INT3 original-case scope-only links lost")
    ensure(db["face_pixel_support"] == {
        "NO_SOURCE_INTERSECTION": 2, "SLOT_UNBOUND": 6202,
        "SOURCE_PNG_MISSING": 139, "SOURCE_REGION_REMEASURED": 585969
    }, "INT3 PNG/UV pixel support distinctions changed")
    ensure(db["historical_sources_overwritten"] is False and
           db["rights_approval_count"] == 0 and db["ai_training_eligible_models"] == 0,
           "INT3 originals or learning rights wrongly changed")
    ensure(sem["counts"]["part_role_candidate"] == 45 and
           sem["role_candidate_counts"] == ROLES and
           sem["role_candidates_visual_verified"] == 0 and
           sem["human_review_approval_count"] == 0 and
           sem["material_style_verified"] == 0 and
           sem["ai_training_eligible_models"] == 0,
           "INT5 semantics silently approved or original role census changed")
    ensure(uv["status"] == "PASS_SOURCE_PINNED_CHILD_TEXTURE_FACES_DIAGNOSTIC_NOT_MINECRAFT_CLIENT"
           and uv["original_faces"] == 229 and uv["source_png_count"] == 8
           and len(uv["models"]) == len(uv["model_providers"]) == 4,
           "Original UV/texture source evidence scope changed")
    ensure(states["totals"]["original_variant_rules"] == 228
           and states["totals"]["source_anomaly_rows"] == 4
           and states["boundaries"]["visually_verified_chair_role_count"] == 0,
           "Unresolved 4 anomalous original selectors or 228 states disappeared")
    ensure(af["status"] == "COMPLETE_VERSION_DIFF_RECORDED_NOT_SEMANTIC_APPROVAL"
           and af["states"]["same"] == 88 and af["states"]["changed"] == 0
           and af["models"]["evaluated"] == 22 and af["models"]["json_identical"] == 24
           and af["models"]["geometry_changed"] == af["models"]["uv_changed"] ==
           af["models"]["face_bindings_changed"] == 0
           and af["boundary"]["part_roles_approved"] == 0
           and af["boundary"]["ai_training_rights_approved"] == 0,
           "AF 4.0.2/4.0.3 acacia-chair comparison evidence changed")
    count = f2["count"]
    ensure(count["total_native_screenshots"] == count["server_state_verified"] ==
           count["selected_source_targets_y_matched"] == 16
           and count["approved_parts"] == count["approved_style_or_material"] ==
           count["source_license_training_approvals"] == 0,
           "PR33 16 real F2 states no longer source-verified")
    ensure(iso["newly_recaptured_native_game_F2_photos"] == 16
           and iso["newly_recaptured_1_21_1_background_platform_photos"] == 0
           and iso["original_evidence_unchanged"] is True
           and iso["visually_approved_new_roles"] == 0
           and iso["ai_training_rights_approved"] == 0,
           "PR34 recapture cohort was incorrectly approved")

    source_states = {s["mod"]: s for s in states["source_states"]}
    ensure(set(source_states) == {"AF", "HC", "MACAW"}, "Blockstate release set changed")
    for mod, n in (("AF", 88), ("HC", 136), ("MACAW", 4)):
        ensure(source_states[mod]["options"] == n, "Blockstate option count changed: " + mod)

    providers = {x["sha"]: x for x in uv["model_providers"]}
    children = {x["child_key"]: x for x in uv["models"]}
    ensure(len(providers) == 4 and set(children) == set(COUNTS),
           "Original four parent providers or child models are missing")
    parent_by_child = {}
    for key, child in children.items():
        parent = providers.get(child["parent_sha"])
        ensure(parent is not None and parent["mod"] == child["source"]
               and child["total_faces_source"] == uv["four_child_source_face_counts"][key],
               "Child-to-provider SHA/UV-face identity mismatch: " + key)
        parent_by_child[key] = parent
    ensure(sum(x["total_faces_source"] for x in children.values()) == 229,
           "Child source face count no longer 229")

    by_sha, seen = defaultdict(list), set()
    for row in parts:
        p = providers.get(row["original_model_sha"])
        ensure(p is not None and row["source_id"] == p["mod"] and
               row["resource_id"] == p["resource"], "Candidate source model SHA/provider mismatch")
        ensure(row["source_role_candidate"] in ROLES and
               row["material_runtime_status"] == "PENDING_TEXTURE_AND_GAME_VISUAL" and
               row["asset_rights_status"] == "PENDING_ORIGINAL_LICENSE_REVIEW",
               "An unreviewed element was silently approved")
        index = int(row["element_index"])
        identity = (row["original_model_sha"], index)
        ensure(index >= 0 and identity not in seen,
               "Duplicate or invalid source element key")
        seen.add(identity)
        by_sha[p["sha"]].append(row)
    ensure(len(parts) == 45 and set(by_sha) == set(providers)
           and Counter(x["source_role_candidate"] for x in parts) == ROLES,
           "45-role original provider, role distribution or element count changed")
    for key, parent in parent_by_child.items():
        ensure(sorted(int(x["element_index"]) for x in by_sha[parent["sha"]]) ==
               list(range(COUNTS[key])), "Missing original model element: " + key)

    shots = {x["case_id"]: x for x in f2["collected"]["per_image"]}
    ensure(len(shots) == len(f2["collected"]["per_image"]) == 16,
           "PR33 exact screenshot file list duplicated or missing")
    for key, child in children.items():
        for direction in DIRECTIONS:
            case = key + "_" + direction
            x = shots.get(case)
            ensure(x is not None, "PR33 missing F2 case: " + case)
            y = MACAW_Y[direction] if child["source"] == "MACAW" else Y[direction]
            version = "1.21.11" if child["source"] == "MACAW" else "1.21.1"
            ensure(x["model"] == child["child_resource"] and x["y"] == y and
                   x["version"] == version and x["file"] == case + ".png" and
                   sha64(x["sha256"]) and x["native_game_F2"] is True and
                   x["in_game_state_verified"] is True,
                   "PR33 original model/F2 hash/rotation mismatch: " + case)
            st = source_states[child["source"]]
            ensure(x["source_research_sha"] == st["source_sha"],
                   "PR33 research blockstate original SHA mismatch: " + case)
            if child["source"] == "AF":
                ensure(st["source_sha"] == af["research"]["blockstate_git_blob_sha1"]
                       and x["source_runtime_sha"] == af["runtime"]["blockstate_git_blob_sha1"]
                       and x["source_equivalence_scope"] ==
                       "RELEASE_SOURCE_DIFF_MUST_VALIDATE_EACH_SELECTED_STATE",
                       "AF version/source release identity mismatch: " + case)
            else:
                ensure(x["source_runtime_sha"] == st["source_sha"] and
                       x["source_equivalence_scope"] == "BYTE_IDENTICAL_TO_PINNED_RESEARCH",
                       "HC/Macaw original runtime source SHA mismatch: " + case)
    ensure(set(shots) == {k + "_" + d for k in children for d in DIRECTIONS},
           "PR33 has unexpected additional game state")

    cohorts = {x["version"]: x for x in iso["source_runtime_results"]}
    ensure(set(cohorts) == {"1.21.1", "1.21.11"} and
           cohorts["1.21.1"]["native_f2_count"] == 12 and
           cohorts["1.21.11"]["native_f2_count"] == 4,
           "PR34 recapture version/cohort mismatch")
    for x in cohorts.values():
        ensure(sha64(x["native_source_manifest_sha256"]) and
               x["semantic_role_approved"] == 0 and
               x["ai_training_rights_approved"] == 0,
               "PR34 independent cohort hash missing")

    rows = []
    for key in sorted(children):
        child, parent = children[key], parent_by_child[key]
        version = "1.21.11" if child["source"] == "MACAW" else "1.21.1"
        for part in sorted(by_sha[parent["sha"]], key=lambda p: int(p["element_index"])):
            ensure(sha64(part["visual_contact_sheet_sha256"]),
                   "Original geometric contact sheet hash missing")
            row = {
                "child_key": key, "mod": child["source"],
                "provider_resource": parent["resource"], "provider_sha": parent["sha"],
                "element_index": part["element_index"],
                "role_hypothesis": part["source_role_candidate"],
                "child_resource": child["child_resource"],
                "child_original_sha": child["child_sha"],
                "original_source_face_count": child["total_faces_source"],
                "game_version": version,
                "geometry_contact_sheet_sha256": part["visual_contact_sheet_sha256"],
                "pr34_recapture_cohort_manifest_sha256": cohorts[version]["native_source_manifest_sha256"],
                "pr34_evidence_scope": "COHORT_NOT_PR33_INDIVIDUAL_IMAGE_BYTES",
                "pr35_af_release_scope": ("ACACIA_CHAIR_STATIC_GEOMETRY_UV_ONLY"
                                          if child["source"] == "AF" else "BYTE_IDENTICAL_SOURCE_STATE"),
                "role_visual_status": "PENDING_INT5_INDIVIDUAL_COMPARISON",
                "individual_role_approved": 0, "style_material_approved": 0,
                "training_rights_approved": 0,
            }
            for d in DIRECTIONS:
                photo = shots[key + "_" + d]
                row["pr33_" + d + "_file"] = photo["file"]
                row["pr33_" + d + "_sha256"] = photo["sha256"]
            rows.append(row)
    ensure(len(rows) == 45, "45 original element-to-game evidence rows not generated")
    summary = {
        "schema": "MCFR_INT3_EXIT_INT4_CHAIR_PROVENANCE/v1",
        "status": "PASS_INT3_STRUCTURAL_ONLY_INT4_F2_SOURCE_ANCHORS_NOT_VISUAL_APPROVAL",
        "int3_exit": "PASS_FIXED_SOURCE_RELATIONSHIPS_ONLY",
        "int4_full_completed": False,
        "int5_role_approved": 0,
        "counts": {
            "model_records": 16579, "model_face_links": 592312,
            "supported_source_pixel_regions_faces": 585969,
            "unresolved_pixel_source_faces": 6343,
            "vanilla_scope_only_model_links": 22, "source_exceptions": 139,
            "source_blockstate_options": 228, "unresolved_selector_anomalies": 4,
            "four_child_texture_faces": 229, "original_png_sources": 8,
            "original_provider_models": 4, "element_role_hypotheses": 45,
            "pr33_actual_f2_images": 16, "pr33_element_direction_metadata_links": 180,
            "pr34_isolated_recapture_cohort_images": 16,
            "individually_verified_roles": 0, "verified_material_style": 0,
            "training_or_rights_approved_models": 0,
        },
        "source_input_sha256": e["input_sha256"],
        "limits": [
            "PR33 individual F2 SHA metadata is linked; original PNG bytes are not checked here",
            "PR34 corrected recapture has a cohort manifest SHA only, not matching PR33 per-image hashes",
            "180 links are provenance associations, not element visibility, per-face GPU UV or function",
            "AF release parity checked only for acacia_chair 88 selectors and 22 inherited targets",
            "4 pre-existing AF variant=3 anomalous selectors are recorded, not corrected",
            "Research evidence does not confer copyright, redistribution or AI training permission",
        ],
    }
    return rows, summary


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    rows, summary = audit(read(args.root))
    args.out.mkdir(parents=True, exist_ok=True)
    file = args.out / "INT4_45_CHAIR_ELEMENT_F2_LINKS.csv"
    with file.open("w", encoding="utf-8", newline="") as stream:
        w = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    summary["csv_sha256"] = sha256(file.read_bytes())
    (args.out / "INT3_EXIT_INT4_CHAIR_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps({"status": summary["status"], "counts": summary["counts"],
                      "csv_sha256": summary["csv_sha256"]}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
