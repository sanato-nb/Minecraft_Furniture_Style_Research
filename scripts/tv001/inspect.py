#!/usr/bin/env python3
"""TV-001 bounded checks for actual render artifacts and replay behavior."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--renders", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    state = json.loads((args.renders / "render_checkpoint.json").read_text(encoding="utf-8"))
    issues, image_info = [], []
    if len(manifest["cases"]) != 12 or len(manifest["jobs"]) != 25:
        issues.append("fixed denominator mismatch")
    if any(c["result"] != "PASS" for c in manifest["cases"]):
        issues.append("static case failure")
    if len(state.get("jobs", {})) != 25:
        issues.append("checkpoint count mismatch")
    for job in manifest["jobs"]:
        name = job["id"]
        path = args.renders / (name + ".png")
        if not path.exists():
            issues.append("missing render: " + name)
            continue
        with Image.open(path) as img:
            rgba = img.convert("RGBA")
            if rgba.size != (256, 256):
                issues.append("wrong image size: " + name)
            alpha = rgba.getchannel("A")
            if alpha.getbbox() is None:
                issues.append("fully transparent render: " + name)
            image_info.append({"id": name, "size": list(rgba.size),
                               "nonempty": alpha.getbbox() is not None, "sha256": sha(path)})
        if state["jobs"].get(name, {}).get("png_sha256") != sha(path):
            issues.append("checkpoint sha mismatch: " + name)
    ids = {j["id"] for j in manifest["jobs"]}
    for left, right in (("R02-none", "R02-north"), ("R03-straight", "R03-inner"),
                        ("P05-n0e0", "P05-n1e1")):
        if left in ids and right in ids:
            pair = {v["id"]: v["sha256"] for v in image_info if v["id"] in (left, right)}
            if len(pair) == 2 and pair[left] == pair[right]:
                issues.append("visual states identical: " + left + " vs " + right)
    # Existence and differing renders are smoke tests, not a proof of Minecraft fidelity.
    report = {
        "contract": "TV-001-v1.1",
        "status": "PASS" if not issues else "FAIL",
        "static_cases": len(manifest["cases"]),
        "expected_png": 25,
        "actual_png": len(image_info),
        "issues": issues,
        "independent_visual_reference_verified": False,
        "blockbench_cross_check_verified": False,
        "tv001_overall_pass": False,
        "scope_note": "CI success does not mean full TV-001 PASS; T4 reference and T5 Blockbench pending.",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
