"""Verify paired Adorn runtime captures with the BWG overlay active."""

import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import re
from zipfile import ZipFile

from audit_adorn_runtime import OVERLAY, engine_report
from replay_adorn_runtime import BWG_PINS, LOADER, ROOT, VERSION, pinned_adorn
from replay_h67 import require

PREFIX = "adorn:biomeswevegone/"
MARKERS = ("BWG_ASPEN_CHAIR_LOWER", "BWG_ASPEN_CHAIR_UPPER", "BWG_ASPEN_TABLE", "ADORN_OAK_TABLE_CONTROL")
RECIPE = f"{PREFIX}aspen_chair"


def verify_overlay(path, engine, without_bwg):
    overlay = f"{OVERLAY}/assets/adorn/blockstates/"
    with ZipFile(path) as jar:
        expected = {
            "adorn:" + name.removeprefix(overlay).removesuffix(".json")
            for name in jar.namelist()
            if name.startswith(overlay + "biomeswevegone/") and name.endswith(".json")
        }

    ordinary_lines = []
    bwg_states = Counter()
    for line in engine.splitlines(keepends=True):
        if line.startswith(PREFIX.encode()):
            bwg_states[line.split(b"\t", 1)[0].decode()] += 1
        else:
            ordinary_lines.append(line)

    require(expected and expected == bwg_states.keys(), "Overlay blockstate paths differ from registered BWG IDs")
    require(b"".join(ordinary_lines) == lzma.decompress(without_bwg.read_bytes()),
            "Ordinary block state rows differ from the run without BWG")
    representative_states = {block: bwg_states[block] for block in (RECIPE, f"{PREFIX}aspen_table")}
    require(all(representative_states.values()), "A representative BWG block is missing")
    return {"blockstate_jsons_matching_registry": len(expected), "registered_states": bwg_states.total(),
            "ordinary_rows_match_without_bwg": True, "representative_states": representative_states}


def verify_visual(work):
    from PIL import Image

    visual = work / "updated-visual"
    log = (visual / "client.log").read_text(encoding="utf-8")
    history = (visual / "command_history.txt").read_text(encoding="utf-8").splitlines()
    require("RenderAudit joined the game" in log, "World did not load")
    require(re.search(r"Reloading ResourceManager: [^\n]*\bbiomeswevegone\b", log), "BWG resources did not load")
    require(all(f"[RenderAudit] {marker}" in log for marker in MARKERS), "A fixture state did not match")
    require([cmd for cmd in history if cmd.startswith("/recipe give ")] == [f"/recipe give @s {RECIPE}"]
            and "Unlocked 1 recipe(s) for RenderAudit" in log, "Expected the BWG chair recipe to unlock")
    require(not re.search(r"Couldn't parse data file '[^']*biomeswevegone[^']*'", log),
            "BWG data parse error detected")

    screenshot = work / "updated.png"
    with Image.open(screenshot) as picture:
        require(picture.size == (1024, 684), "Unexpected visual fixture dimensions")
        picture.verify()
    return {"state_markers": list(MARKERS), "unlocked_recipe": RECIPE, "bwg_data_parse_errors": 0,
            "screenshot_size": [1024, 684], "screenshot_sha256": hashlib.sha256(screenshot.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("updated_jar", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    require(pinned_adorn(args.updated_jar) == "updated", "Expected the pinned updated Adorn release")

    baseline, updated = [args.work / label / "ENGINE_STATES.tsv" for label in ("baseline-engine", "updated-engine")]
    identical_tsv = updated.read_bytes()
    require(baseline.read_bytes() == identical_tsv, "Engine state TSV differs between Adorn releases")
    without_bwg = ROOT / "project/audits/adorn_runtime/engine-states.tsv.xz"
    report = {
        "minecraft": VERSION, "fabric_loader": LOADER, "fabric_api": "0.141.6",
        "bundle": {item["id"]: item["version"] for item in json.loads(BWG_PINS.read_text(encoding="utf-8"))},
        "engine": {**engine_report(updated), "identical_tsv_between_releases": True},
        "overlay": verify_overlay(args.updated_jar, identical_tsv, without_bwg),
        "visual_updated": verify_visual(args.work),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
