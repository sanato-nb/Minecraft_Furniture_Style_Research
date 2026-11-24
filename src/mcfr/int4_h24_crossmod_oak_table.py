"""INT-4 H24: independent selected-source cross-mod oak_table comparison.

This measures six *different states*, not equivalent player-facing functionality.
Every input is pinned to the already audited H21/H22/V5 Git blob, with exact
historical native F2 hashes and old approval boundaries preserved. No original
JAR, texture, or game screenshot is redistributed.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
I = Path("project/integration")
PINS = {
    "INT4_H21_AF16_RELEASE_SOURCE_UV_RESULT_V1.json": "8b6ba58b0fcdd6f6681019dd1f8b58047c8b9d97",
    "INT4_H22_HC_MACAW12_SOURCE_RESULT_V1.json": "b659e12153d0d2c12710bb4e24e236c934b06c14",
    "INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V5.csv": "95ee0efa5dda895a8ce08e1291286e775d9a73dd",
    "INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json": "2c7092534d377cdbb5676fa3b96df2ef6b4615bd",
}
COHORT_CASES = {
    "AF": ("S14", "S15"),
    "HC": ("S16", "S17"),
    "MACAW": ("S18", "S19"),
}
COHORT_NS = {"AF": "another_furniture", "HC": "handcrafted", "MACAW": "mcwfurnitures"}
COHORT_MINECRAFT = {"AF": "1.21.1", "HC": "1.21.1", "MACAW": "1.21.11"}
PAIR_KEYS = {
    "AF": ("leg_1", "leg_2", "leg_3", "leg_4"),
    "HC": ("shape",),
    "MACAW": ("east", "north", "south", "west"),
}
CSV_FIELDS = [
    "target_id", "cohort", "minecraft_version", "block", "state",
    "source_applications", "source_elements", "source_faces",
    "source_uv_measured_faces", "documented_zero_uv_faces",
    "animated_source_faces", "selected_model_paths", "provider_paths",
    "source_component_count", "original_f2_run_ids", "original_f2_sha256s",
    "modeling_status", "legacy_unconditional_F", "INT5_meaning_approved",
    "INT6_rights_approved",
]


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError("H24 source comparison: " + reason)


def git_blob(b: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def load_sources(root: Path = ROOT) -> tuple[dict, dict, list[dict], dict]:
    contents = {}
    for filename, expected in PINS.items():
        p = root / I / filename
        b = p.read_bytes()
        require(git_blob(b) == expected, "pinned original blob changed: " + filename)
        contents[filename] = b
    h21 = json.loads(contents["INT4_H21_AF16_RELEASE_SOURCE_UV_RESULT_V1.json"])
    h22 = json.loads(contents["INT4_H22_HC_MACAW12_SOURCE_RESULT_V1.json"])
    v5 = json.loads(contents["INT4_F70_MODELING_CONTRACT_SUMMARY_V5.json"])
    raw = contents["INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V5.csv"].decode("utf-8-sig")
    rows = list(csv.DictReader(raw.splitlines()))
    return h21, h22, rows, v5


def parse_state(s: str) -> dict[str, str]:
    result = {}
    for part in s.split(";"):
        require(part.count("=") == 1, "invalid state property")
        k, v = part.split("=", 1)
        require(bool(k and v) and k not in result, "duplicate or missing state property")
        result[k] = v
    return result


def reconcile(h21: dict, h22: dict, ledger: list[dict], summary: dict) -> dict:
    require(h21["case_count"] == 16 and h21["face_count"] == 535, "H21 scope drift")
    require(h22["case_count"] == 12 and h22["faces"] == 311, "H22 scope drift")
    require(len(ledger) == 70 and len({x["target_id"] for x in ledger}) == 70,
            "the historical 70-row denominator changed")
    require(Counter(x["modeling_status"] for x in ledger) ==
            {"PASS_MODELING_SCOPE": 62, "PASS_RISK_QUESTION_SCOPE": 8},
            "V5 model contract status changed")
    require(summary["combined_review_scope_only"] ==
            {"denominator": 70, "closed_units": 70, "conditional": 0, "hold": 0},
            "V5 scope not closed")
    expected_legacy = {
        "conditional": 70, "unconditional": 0, "H03": "HOLD",
        "H05": "CONDITIONAL", "INT5": 0, "INT6": 0,
    }
    require(summary["legacy_F70"] == expected_legacy, "original approvals changed")
    by_id = {x["target_id"]: x for x in ledger}
    cases = []
    for cohort, ids in COHORT_CASES.items():
        source = h21 if cohort == "AF" else h22
        for target in ids:
            raw = source["cases"][target]
            row = by_id[target]
            require(raw["block"] == row["block"] and raw["state"] == row["block"] * 0 + raw["state"],
                    "block/state source field is invalid")
            require(raw["block"].split(":")[0] == COHORT_NS[cohort],
                    "wrong source namespace for " + target)
            require(row["cohort"] == cohort and row["minecraft_version"] == COHORT_MINECRAFT[cohort],
                    "V5 source version/cohort mismatch: " + target)
            require(row["modeling_status"] == raw["modeling_status"] == "PASS_MODELING_SCOPE",
                    "source modeling scope not passed: " + target)
            require(all(row[f] == "false" for f in
                    ("legacy_unconditional_F", "runtime_GPU_per_face_approved",
                     "INT5_meaning_approved", "INT6_rights_approved")),
                    "approval boundary violation")
            parse_state(raw["state"])
            if cohort == "AF":
                apps = raw["applications"]
                require(len(apps) > 0 and raw["entire_blockstate_JSON_equal"] and
                        raw["selected_options_equal"] and not raw["issues"],
                        "H21 AF original model selector mismatch")
                require(all(a["chain_json_equal"] and a["elements_equal"] and
                            a["face_uv_bindings_equal"] and
                            a["historical_face_png_hash_and_uv_rows_verified"] == a["faces"]
                            for a in apps), "AF selected original UV proof incomplete")
                elements = sum(int(a["elements"]) for a in apps)
                faces = sum(int(a["faces"]) for a in apps)
                uv_verified = sum(int(a["historical_face_png_hash_and_uv_rows_verified"])
                                  for a in apps)
                selected = sorted({a["leaf"] for a in apps})
                providers = sorted({a["provider"] for a in apps})
                assets = raw["all_compared_paths"]
                observed = raw["existing_visual_evidence"]
                capture_run = observed["existing_run"]
                capture_sha = observed["existing_F2_sha256"]
                require(observed["existing_exact_capture_evidence"],
                        "AF original F2 lacks exact state")
                require(all(h21["asset_comparisons"][p]["equivalent"] is True
                            for p in assets), "AF source assets not equal to official release")
            else:
                require(raw["all_selected_JSON_bytes_equal"] and
                        raw["all_selected_texture_bytes_equal"] and
                        raw["historical_uv_and_png_hash_faces_verified"] == raw["faces"],
                        "H22 source bytes or face UV mismatch")
                elements, faces = int(raw["elements"]), int(raw["faces"])
                uv_verified = raw["historical_face_status_counts"].get("STATIC_RECT", 0)
                selected = [raw["selected_option"][0]]
                providers = [raw["provider"]]
                assets = raw["assets"]
                capture_run = raw["existing_capture"]["run"]
                capture_sha = raw["existing_capture"]["F2_sha256"]
                require(all(h22["asset_comparisons"][cohort][p]["equivalent"] is True
                            for p in assets), "H22 source asset differs from official release")
            require(len(assets) == len(set(assets)) and bool(assets), "source asset duplicate")
            require(str(capture_run) == row["original_f2_run_ids"] and
                    capture_sha == row["original_f2_sha256s"] and len(capture_sha) == 64,
                    "original native F2 identity mismatch: " + target)
            require(int(row["source_applications"]) == (len(apps) if cohort == "AF" else 1) and
                    int(row["source_elements"]) == elements and int(row["source_faces"]) == faces,
                    "original selected-model geometry differs: " + target)
            require(int(row["source_uv_measured_faces"]) == uv_verified and
                    faces == uv_verified + int(row["documented_zero_uv_faces"]) +
                    int(row["animated_source_faces"]),
                    "original UV face accounting differs: " + target)
            if cohort != "AF":
                require(int(row["documented_zero_uv_faces"]) ==
                        raw["historical_face_status_counts"].get("ZERO_UV_AREA", 0) and
                        int(row["animated_source_faces"]) ==
                        raw["historical_face_status_counts"].get("ANIMATED_FRAME_RECTS", 0),
                        "H22 detailed UV status mismatch")
            case = {key: row[key] for key in CSV_FIELDS if key in row}
            case.update(
                state=raw["state"],
                selected_model_paths=selected,
                provider_paths=providers,
                source_component_count=len(assets),
            )
            for k in ("source_applications", "source_elements", "source_faces",
                      "source_uv_measured_faces", "documented_zero_uv_faces",
                      "animated_source_faces"):
                case[k] = int(case[k])
            cases.append(case)
    cases.sort(key=lambda x: x["target_id"])
    indexed = {x["target_id"]: x for x in cases}
    pairs = []
    for cohort, (more, less) in COHORT_CASES.items():
        a, b = indexed[more], indexed[less]
        require(a["block"] == b["block"] and
                a["minecraft_version"] == b["minecraft_version"],
                "paired block/release not identical")
        states_a, states_b = parse_state(a["state"]), parse_state(b["state"])
        require(set(states_a) == set(states_b), "state dimension changed")
        changed = sorted(k for k in states_a if states_a[k] != states_b[k])
        require(changed == sorted(PAIR_KEYS[cohort]), "selected-state difference changed")
        diff = {
            f: a[f] - b[f] for f in
            ("source_applications", "source_elements", "source_faces",
             "source_uv_measured_faces", "documented_zero_uv_faces")
        }
        require(diff["source_elements"] > 0 and diff["source_faces"] > 0,
                "high-detail case must have more original source geometry")
        pairs.append({
            "cohort": cohort, "block": a["block"],
            "more_geometry_case": more, "less_geometry_case": less,
            "changed_state_keys": changed,
            "more_geometry_state_values": {k: states_a[k] for k in changed},
            "less_geometry_state_values": {k: states_b[k] for k in changed},
            "selected_model_delta": diff,
        })
    return {
        "schema": "MCFR_INT4_H24_CROSSMOD_OAK_TABLE_SOURCE_V1",
        "parent_H23_head": "07925fbee8758e64bbbfc532587eb035821c6c3a",
        "source_blob_pins": dict(sorted(PINS.items())),
        "research_scope": {
            "verified_original_states": 6, "paired_comparisons": 3,
            "cohorts": ["AF", "HC", "MACAW"],
            "new_game_runs": 0, "new_F2": 0,
            "reuses_original_F2": True, "not_claimed_as_equivalent_state": True,
        },
        "cases": cases, "within_mod_comparisons": pairs,
        "strict_legacy_F70": expected_legacy,
        "interpretation": [
            "Same oak_table lexical ID does not identify interchangeable models or state properties.",
            "AF legs, HC shape, and Macaw cardinal neighbor connections select different model structures.",
            "Only pinned exact original source face-UV, selected state and F2 identities are compared.",
        ],
        "limitations": [
            "No cross-mod pixel correspondence or same-camera equivalence is established.",
            "No new client captures, exact GPU texel-to-pixel claim, semantic/INT5 or IP/INT6 approval.",
            "Different MC and mod releases prevent treating measured states as direct visual substitutes.",
            "The H24 six-case subset does not change the 70/70 V5 modeling scope denominator.",
        ],
    }


def to_csv_rows(result: dict) -> list[dict]:
    rows = []
    for c in result["cases"]:
        row = dict(c)
        row["selected_model_paths"] = "|".join(row["selected_model_paths"])
        row["provider_paths"] = "|".join(row["provider_paths"])
        rows.append({k: str(row[k]) for k in CSV_FIELDS})
    return rows


def verify_saved(result: dict, root: Path = ROOT) -> None:
    out = root / I
    j = json.loads((out / "INT4_H24_CROSSMOD_OAK_TABLE_RESULT_V1.json").read_text(encoding="utf-8"))
    require(j == result, "saved JSON differs from independently calculated result")
    with (out / "INT4_H24_CROSSMOD_OAK_TABLE_CASES_V1.csv").open(
            encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames == CSV_FIELDS, "saved CSV column drift")
        got = list(reader)
    require(got == to_csv_rows(result), "saved CSV differs from original source")
    print("H24_CROSSMOD_6_OF_6_SOURCE_RECONCILED_3_PAIRS_CSV_JSON_VERIFIED")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true",
                   help="Validate committed results against pinned original inputs")
    p.add_argument("--output", type=Path, default=ROOT / I)
    a = p.parse_args()
    result = reconcile(*load_sources())
    if a.verify:
        verify_saved(result)
    else:
        a.output.mkdir(parents=True, exist_ok=True)
        with (a.output / "INT4_H24_CROSSMOD_OAK_TABLE_RESULT_V1.json").open(
                "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, sort_keys=True, ensure_ascii=False)
            f.write("\n")
        with (a.output / "INT4_H24_CROSSMOD_OAK_TABLE_CASES_V1.csv").open(
                "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_FIELDS, lineterminator="\n")
            w.writeheader()
            w.writerows(to_csv_rows(result))
        print("H24_CROSSMOD_6_CASES_3_PAIRS_RECALCULATED_NOT_NEW_F70_APPROVAL")


if __name__ == "__main__":
    main()
