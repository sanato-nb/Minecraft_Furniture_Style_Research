"""B32 texture source SHA / caveat / hypothesis, B33 full-vs-intervention context.

All outputs are bounded research evidence. Neither a named texture PNG nor a changed
F2 screen pixel verifies physical function, material, style or GPU-face pixel ownership.
"""
import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

from .int5_b31_remaining21_real_archive_audit import RECORD_PATH

B24 = "INT5_B24_45_PART_ORIGINAL_SOURCE_ROLE_SEMANTICS_EVIDENCE_REVIEW_V1.csv"
B23 = "INT5_B23_FULL10_CONTEXTS_320_REAL_F2_FINAL_INDEPENDENT_AUDIT_V1.json"
B28 = "INT5_B28_B25_ALL8_ORIGINAL_ARTIFACTS_INDEPENDENT_FINAL_AUDIT_V1.json"
CUE = {
    "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF": 35,
    "ROLE_NAMED_ORIGINAL_SEAT_PNG": 2,
    "ROLE_NAMED_ORIGINAL_BACK_PNG": 6,
    "ROLE_NAMED_ORIGINAL_CUSHION_PNG": 1,
    "UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME": 1,
}
CAVEATS = {
    "AF_SOURCE_4_0_3_RELEASE_4_0_2_NOT_BYTE_IDENTICAL": 20,
    "BLOCKSTATE_SHA_EQUAL_PARENT_JSON_RUNTIME_NOT_FULLY_PROVEN": 25,
}
VIEWS = ("south", "north", "east", "west")


def need(ok, why):
    if not ok:
        raise ValueError("INT5_B32_B33_EVIDENCE_REJECT: " + why)


def csv_rows(path):
    with path.open(encoding="utf8", newline="") as f:
        data = list(csv.DictReader(f))
    need(data and all(None not in row for row in data), "Bad original CSV")
    return data


def keys(records):
    keyed = {(x["model"], int(x["source_element_index"])): x for x in records}
    need(len(keyed) == len(records), "Duplicate source keys")
    return keyed


def verify_source_hex_hashes(tokens):
    # Source strings can contain SHA-1 (40 hex) and SHA-256 (64 hex);
    # these are original source provenance checksums, not role classifiers.
    return all(len(token) in (40, 64) and
               all(c in "0123456789abcdef" for c in token)
               for token in tokens)


def audit_texture(directory):
    role = keys(csv_rows(directory / B24))
    screen = keys(csv_rows(directory / RECORD_PATH))
    need(len(role) == len(screen) == 45 and role.keys() == screen.keys(), "45-element source join")
    cues = Counter(x["source_texture_cue"] for x in role.values())
    caveats = Counter(x["source_runtime_version_caveat"] for x in role.values())
    need(dict(cues) == CUE and dict(caveats) == CAVEATS, "Texture/caveat lineage changed")
    groups = defaultdict(list)
    atomic = set()
    by_model = defaultdict(lambda: Counter())
    selected = []
    for key, src in sorted(role.items()):
        view = screen[key]
        hash_group = src["original_texture_source_hashes"]
        tokens = hash_group.split("|")
        need(verify_source_hex_hashes(tokens), "Non-checksum original texture source " + str(key))
        need(src["face_count"] == view["original_source_face_count"], "Face count drift")
        need(src["source_role_hypothesis_not_approved"] == view["role_hypothesis_not_verified"], "Role mismatch")
        need(src["source_texture_cue"] in CUE and hash_group, "Texture cue unrecognized")
        for approval in ("original_element_to_F2_unique_face_pixel_attributed",
                         "role_function_semantics_approved", "material_or_style_approved",
                         "third_party_training_or_redistribution_rights_approved"):
            need(src[approval] == "false", "Source semantics/right incorrectly approved")
        for approval in ("physical_role_material_style_approved",
                         "original_face_UV_GPU_exclusive_pixel_owner_approved",
                         "third_party_training_redistribution_rights_approved"):
            need(view[approval] == "false", "Screen semantics/right incorrectly approved")
        groups[hash_group].append(key[0] + "#" + str(key[1]))
        atomic.update(tokens)
        by_model[key[0]][src["source_texture_cue"]] += 1
        if src["source_texture_cue"] != "GENERIC_OR_SHARED_TEXTURE_NOT_ROLE_PROOF":
            selected.append({
                "source": key[0] + "#" + str(key[1]),
                "source_role_hypothesis_not_approved": src["source_role_hypothesis_not_approved"],
                "source_texture_cue_not_material_proof": src["source_texture_cue"],
                "source_texture_checksum_string": hash_group,
                "source_runtime_version_caveat": src["source_runtime_version_caveat"],
                "original_f2_artifact_id": int(view["original_GitHub_artifact_id"]),
                "screen_change_south_north": [
                    int(view["original_removed_south_changed_pixels"]),
                    int(view["original_removed_north_changed_pixels"])
                ],
                "semantic_function_material_style_approved": False,
                "GPU_face_exclusive_pixel_attribution_approved": False,
            })
    need(len(groups) == 8 and len(atomic) == 9 and len(selected) == 10,
         "8 checksum groups / 9 tokens / 10 cue-positive rows changed")
    return {
        "schema": "MCFR_INT5_B32_45_ELEMENT_SOURCE_TEXTURE_CUE_AND_VERSION_BOUNDS/v1",
        "original_elements": 45, "source_faces": 229,
        "texture_hash_group_count": len(groups),
        "atomic_sha1_sha256_checksum_count": len(atomic),
        "checksum_reuse_groups": [
            {"checksum_string": group, "source_count": len(k), "source_keys": k}
            for group, k in sorted(groups.items())
        ],
        "source_texture_cue_counts": dict(cues), "source_runtime_version_caveats": dict(caveats),
        "per_model_cues": {m: dict(x) for m, x in sorted(by_model.items())},
        "named_or_contrast_texture_evidence_not_semantic_approval": selected,
        "no_new_original_texel_or_uv_gpu_exclusive_pixel_test": True,
        "physical_role_material_style_approved": 0,
        "GPU_original_face_UV_exclusive_pixel_approved": 0,
        "third_party_training_and_distribution_rights_approved": 0,
        "H03": "HOLD", "H05": "CONDITIONAL", "F70_unconditional_approved": 0
    }


def audit_context(directory):
    screen = keys(csv_rows(directory / RECORD_PATH))
    b23 = json.loads((directory / B23).read_text(encoding="utf8"))
    b28 = json.loads((directory / B28).read_text(encoding="utf8"))
    need(len(b23["results"]) == 10 and len(b28["records"]) == 8, "B23/B28 number of contexts")
    need(b23["original_native_F2_PNG_SHA256_verified"] == 320, "B23 native F2 count")
    need(b28["native_F2_PNG_SHA256_verified"] == 256, "B28 native F2 count")
    original_full = {(r["target"], r["context"]): r for r in b23["results"]}
    need(len(original_full) == 10, "Duplicate original B23 context")
    recs = sorted(b28["records"], key=lambda r: (r["target"], r["omitted_original_index"]))
    need({r["target"] for r in recs} == {"AF121_5", "AF123_5"}, "Two AF original source5 models")
    valid = {}
    for target in ("AF121_5", "AF123_5"):
        model = target[:-2]
        original = screen[(model, 5)]
        need(all(int(original["original_removed_" + view + "_changed_pixels"]) == 0
                 for view in ("south", "north")), "B27 intact original source5 changed")
        for context in ("all_others", "front_0_4"):
            old = original_full[(target, context)]
            need(old["original_source_element5_added_vs_absent_pixels_south_north_east_west"] == [0,0,0,0],
                 "Original B23 no-effect controls overridden")
            need(old["four_view_temporal_and_negative_controls_all_zero"] is True, "B23 temporal control")
        valid[target] = {"B27_full_original_south_north": [0,0],
                         "B23_all_others_four_views": [0,0,0,0],
                         "B23_front_0_4_four_views": [0,0,0,0]}
    pixels = positive = camera_positive = 0
    positions = set()
    grouped = defaultdict(list)
    for r in recs:
        target, omitted = r["target"], r["omitted_original_index"]
        need(type(omitted) is int and omitted in range(4), "Omitted original index")
        need((target, omitted) not in positions, "Duplicated B28 intervention")
        positions.add((target, omitted))
        need(r["source6_and_source4_pinned"] and r["source5_is_only_added_original_index"],
             "Only one original source-element intervention")
        need(r["temporal_per_camera_A_A_controls_zero"] and
             r["negative_air_or_slab_controls_zero"], "Original controls")
        need(r["zip_crc_passed"] is True and
             r["original_native_F2_SHA256_verified"] == 32 and
             r["original_client_logs_SHA256_verified"] == 2, "Original artifact proof")
        need(r["exact_original_chair_server_markers_verified"] == 32 and
             r["exact_original_support_slab_markers_verified"] == (32 if target == "AF123_5" else 0),
             "Original server source state proof")
        for flag in ("source5_unique_occlusion_cause_proven", "physical_part_role_proven",
                     "material_style_proven", "individual_GPU_face_or_UV_exclusive_pixel_owner_proven",
                     "third_party_AI_training_redistribution_rights_approved"):
            need(r[flag] is False, "Unauthorized physical source/rights approval")
        px = r["pixels_south_north_east_west"]
        need(len(px) == 4 and all(type(n) is int and 0 <= n <= 2 for n in px),
             "B25 micro screen pixel range")
        camera_positive += sum(x>0 for x in px)
        pixels += sum(px)
        positive += int(any(px))
        grouped[target].append({"omitted": omitted, "four_view_pixels": px})
        named = r["changed_pixel_positions_xy"]
        for v,n in zip(VIEWS, px):
            points = named.get(v, [])
            need(len(points) == n, "B28 pixel coordinate count differs from source metrics")
            for x,y in points:
                need(350<=x<675 and 275<=y<620, "Pixel outside original ROI")
    need(len(positions) == 8 and positive == 7 and camera_positive == 8 and pixels == 10,
         "B28 original micro response aggregate changed")
    return {
        "schema": "MCFR_INT5_B33_B23_B27_B28_ORIGINAL_SOURCE5_CONTEXT_CONDITIONALITY/v1",
        "original_full_model_and_B23_controls": valid,
        "different_context_B28_two_model_eight_dropouts": dict(grouped),
        "B23_F2_recorded": 320, "B28_F2_directly_reaudited": 256,
        "B28_positive_intervention_cases": positive,
        "B28_nonzero_camera_comparisons": camera_positive,
        "B28_total_micro_changed_screen_pixels": pixels,
        "one_or_two_pixel_screen_response_is_not_unique_physical_leg_or_UV_face_owner": True,
        "original_B27_full_model_render_responses_43_of_45_unchanged": True,
        "source5_unchanged_in_B27_full_model": ["AF121#5", "AF123#5"],
        "physical_role_material_style_approved": 0,
        "GPU_original_face_UV_exclusive_pixel_approved": 0,
        "third_party_training_and_distribution_rights_approved": 0,
        "H03": "HOLD", "H05": "CONDITIONAL", "F70_unconditional_approved": 0
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, default=Path("project/integration"))
    p.add_argument("--output-directory", type=Path, required=True)
    args = p.parse_args()
    args.output_directory.mkdir(parents=True, exist_ok=True)
    for name, work in (("B32", audit_texture), ("B33", audit_context)):
        result = work(args.source)
        out = args.output_directory / ("INT5_" + name + "_INDEPENDENT_RESEARCH_RESULT_V1.json")
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf8")
        print(name, "INDEPENDENT_SOURCE_GUARD_PASS")


if __name__ == "__main__":
    main()
