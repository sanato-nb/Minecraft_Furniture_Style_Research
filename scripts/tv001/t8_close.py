#!/usr/bin/env python3
"""TV-001 T8 bounded closure: PASS only when independent accuracy is proven."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def batch_summary(path):
    lines = [line for line in path.read_text(encoding="utf-8").splitlines()
             if line.startswith("TV001_BATCH ")]
    if not lines:
        raise ValueError("Missing batch summary: " + str(path))
    return json.loads(lines[-1].partition(" ")[2])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    root = a.evidence
    manifest = read(root / "manifest.json")
    smoke = read(root / "inspect_report.json")
    independent = read(root / "t4_independent.json")
    counts = [batch_summary(root / ("batch_" + str(i) + ".log"))
              for i in (1, 2, 3)]
    counts_actual = [(b["rendered"], b["skipped"], b["remaining"]) for b in counts]
    counts_expected = [(12, 0, 13), (13, 12, 0), (0, 25, 0)]
    replay_ok = counts_actual == counts_expected
    smoke_ok = smoke["status"] == "PASS" and smoke["actual_png"] == 25
    t4_partial = independent["status"] == "PARTIAL"
    t4_geometry_ok = independent["geometry_mask_pass"] == 25
    t4_spot_ok = independent["source_spot_checks_pass"]
    t4_uv_pattern_ok = independent["p06_uv_rotation_pattern_pass"]
    # Full PASS is prohibited unless an actual source-independent per-face UV
    # and Minecraft reference comparison verifies every affected item.
    full_verified = bool(independent.get("full_minecraft_visual_fidelity_verified"))
    if not smoke_ok or not replay_ok or not t4_geometry_ok or not t4_spot_ok:
        overall = "FAIL"
    elif t4_partial or not full_verified:
        overall = "PARTIAL"
    else:
        overall = "PASS"
    report = {
        "contract": "TV-001-v1.1", "t8_closure_record": True,
        "overall_status": overall, "closed_scope": "TV-001 fixed 12 cases, 25 images",
        "historical_pilot_run": 45986960067,
        "latest_run_executed_by_this_workflow": True,
        "scope_fixed": len(manifest["cases"]) == 12 and len(manifest["jobs"]) == 25,
        "t0_reuse_audit": "PARTIAL: existing source/DB modules identified but not fully integrated",
        "t1_test_inputs": "PASS" if len(manifest["cases"]) == 12 else "FAIL",
        "t2_static_core": "PASS (fixed fixture classifications only)",
        "t3_render_smoke": "PASS" if smoke_ok else "FAIL",
        "t4_independent_reference": independent["status"],
        "t5_blockbench": "OUT_OF_SCOPE (web interaction excluded; automation optional future research)",
        "t6_github_actions": "PASS (this script reached by CI)",
        "t7_restart_resume": "PASS (within one Actions job)" if replay_ok else "FAIL",
        "t8_closure": "CLOSED_" + overall,
        "basic_pngs_verified": smoke["actual_png"],
        "independent_projected_geometry_images_verified": independent["geometry_mask_pass"],
        "face_uv_transparency_pattern": "PASS" if t4_uv_pattern_ok else "FAIL",
        "independent_full_minecraft_visual_fidelity": full_verified,
        "known_limitations": independent["unverified_or_known_incorrect"],
        "render_batches_actual": counts_actual,
        "not_proven": [
            "Minecraft-exact per-face UV/uvlock on all 25 images",
            "GitHub Actions cross-job checkpoint restoration",
            "Full vanilla/mod research completeness"
        ],
        "next_decision": (
            "TV-001 closure is PARTIAL; record the exact UVLOCK issue and missing "
            "full independent UV oracle as bounded follow-up candidates. "
            "Do not expand TV-001 case count or claim overall PASS."
        ) if overall == "PARTIAL" else "See classified failures before any next step."
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("TV001_T8 " + json.dumps({k: v for k, v in report.items()
                                  if k not in ("known_limitations",)}, ensure_ascii=False))
    if overall == "FAIL":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
