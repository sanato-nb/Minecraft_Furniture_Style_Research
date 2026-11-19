"""Audit paired Adorn runtime captures and the JAR overlay relocation."""

import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from zipfile import ZipFile

from replay_adorn_runtime import LOADER, ROOT, VERSION, pinned_adorn
from replay_h67 import manifest, require

OVERLAY = "adorn_integration_biomeswevegone"
BWG = "biomeswevegone"
FURNITURE_BOX = (270, 270, 750, 465)
STATE_MARKERS = ("ADORN_CHAIR_LOWER", "ADORN_CHAIR_UPPER", "ADORN_TABLE", "ADORN_SOFA")


def relocated_assets(old, new):
    from replay_h67 import PINS

    pins = json.loads(PINS.read_text(encoding="utf-8"))
    old_index = {item["source_path"]: item for item in manifest(old, pins["baseline"])["assets"]}
    new_index = {item["source_path"] for item in manifest(new, pins["updated"])["assets"]}
    removed = sorted(old_index.keys() - new_index)
    with ZipFile(new) as archive:
        overlays = json.loads(archive.read("pack.mcmeta"))["fabric:overlays"]["entries"]
        entry = next(item for item in overlays if item["directory"] == OVERLAY)
        require(entry["condition"] == {"condition": "fabric:all_mods_loaded", "values": [BWG]},
                "Unexpected overlay condition")
        for path in removed:
            payload = archive.read(f"{OVERLAY}/{path}")
            require(hashlib.sha256(payload).hexdigest() == old_index[path]["digest"], f"Overlay bytes differ: {path}")
    return {"relocated": len(removed), "identical_payloads": len(removed), "directory": OVERLAY,
            "requires_mod": BWG, "by_kind": dict(Counter(old_index[path]["kind"] for path in removed))}


def engine_report(path):
    with path.open(newline="", encoding="utf-8") as stream:
        states = list(csv.DictReader(stream, delimiter="\t"))
    keys = {(row["block"], row["properties"]) for row in states}
    controls = {row["block"]: row["boxes"] for row in states if row["block"].startswith("minecraft:")}
    require(controls == {"minecraft:air": "", "minecraft:stone": "0.0,0.0,0.0,1.0,1.0,1.0"},
            "Unexpected collision controls")
    require(len(keys) == len(states) and all(row["status"] == "OK" for row in states),
            "Duplicate state or collision context error")
    own = [row for row in states if row["block"].startswith("adorn:")]
    require(own and len(states) == len(own) + 2, "Unexpected registry namespaces")
    boxes = 0
    for row in own:
        for box in filter(None, row["boxes"].split(";")):
            coordinates = tuple(map(float, box.split(",")))
            require(len(coordinates) == 6 and all(map(math.isfinite, coordinates)) and
                    all(a < b for a, b in zip(coordinates[:3], coordinates[3:])), "Invalid collision bounds")
            boxes += 1
    return {"blocks": len({row["block"] for row in own}), "states": len(own),
            "collision_boxes": boxes, "empty_shapes": sum(not row["boxes"] for row in own),
            "registered_bwg_blocks": len({row["block"] for row in own if BWG in row["block"]}),
            "tsv_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def visual_log(path, recipe_message):
    log = path.read_text(encoding="utf-8")
    require("RenderAudit joined the game" in log, "World did not load")
    require(all(f"[RenderAudit] {marker}" in log for marker in STATE_MARKERS), "A fixture state did not match")
    history = path.with_name("command_history.txt").read_text(encoding="utf-8").splitlines()
    require("/recipe give @s adorn:copper_nugget" in history and recipe_message in log,
            "Expected copper nugget recipe command result")
    errors = set(re.findall(r"Couldn't parse data file '([^']*biomeswevegone[^']*)'", log))
    return {"state_markers": list(STATE_MARKERS), "unique_bwg_data_parse_errors": len(errors),
            "error_example": min(errors) if errors else None, "recipe_message": recipe_message}


def furniture_pixels(old, new):
    from PIL import Image

    with Image.open(old) as left, Image.open(new) as right:
        require(left.size == right.size == (1024, 684), "Unexpected capture dimensions")
        a = left.convert("RGBA").crop(FURNITURE_BOX)
        b = right.convert("RGBA").crop(FURNITURE_BOX)
    return {"box": list(FURNITURE_BOX), "pixels": a.width * a.height, "equal": a.tobytes() == b.tobytes()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline_jar", type=Path)
    parser.add_argument("updated_jar", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT / "src"))
    from mcfr.visual_check import compare

    require((pinned_adorn(args.baseline_jar), pinned_adorn(args.updated_jar)) == ("baseline", "updated"),
            "Expected the baseline and updated Adorn JARs in that order")
    old, new = [engine_report(args.work / f"{label}-engine/ENGINE_STATES.tsv")
                for label in ("baseline", "updated")]
    require(old == new and old["registered_bwg_blocks"] == 0, "Registry or collision scope differs")
    report = {
        "minecraft": VERSION, "fabric_loader": LOADER, "fabric_api": "0.141.6",
        "fixture_has_bwg": False, "relocation": relocated_assets(args.baseline_jar, args.updated_jar),
        "engine": {"baseline": old, "updated": new, "identical_tsv": True},
        "visual_observations": {
            "baseline": visual_log(args.work / "baseline-visual/client.log", "Unlocked 1 recipe(s) for RenderAudit"),
            "updated": visual_log(args.work / "updated-visual/client.log", "Unknown recipe: adorn:copper_nugget"),
        },
        "pixels": compare(args.work / "baseline.png", args.work / "updated.png"),
        "furniture_pixels": furniture_pixels(args.work / "baseline.png", args.work / "updated.png"),
    }
    observations = report["visual_observations"]
    require(observations["baseline"]["unique_bwg_data_parse_errors"] > 0
            and observations["updated"]["unique_bwg_data_parse_errors"] == 0, "Expected overlay log change")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
