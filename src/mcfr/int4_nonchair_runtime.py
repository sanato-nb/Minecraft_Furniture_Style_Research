"""Capture the remaining representative states and two adjacency trials in Fabric."""
from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import ExitStack
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from time import sleep
from zipfile import ZipFile

from . import int4_handcrafted_bed_capture as bed
from . import int4_macaw_table_shelf_capture as shelf
from .chair_runtime_fixture import Y
from .runtime_capture import wait_for
from .int4_macaw_kitchen_capture import model_path, parse_selector

VERSIONS = ("1.21.1", "1.21.11")
REMAINING = ("S14", "S15", "S16", "S17", "S39", "S40")
ORIGIN = (0, Y, 40)
BED = "handcrafted:oak_fancy_bed"
SHELF = "mcwfurnitures:oak_bookshelf"
PREFIX = "[RenderAudit] INT4_NC "
CAMERA = "3.4 123.6 45.7 151 28"
BED_INTERACTION = "0.5 120 42.5 180 35"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def position(x, y, z):
    return f"{x} {y} {z}"


def state(block, properties):
    # Empty state selectors are legal in the original 1-5 source catalogue.
    # Do not send an empty [] suffix to /setblock or execute-if-block.
    return block if not properties else block + "[" + properties.replace(";", ",") + "]"


def applications(case_ids=None):
    raw = (shelf.ROOT / shelf.APPS).read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    digest = sha256(raw)
    require(digest == shelf.source_rows()[1], "Historical application ledger changed")
    active = REMAINING if case_ids is None else tuple(case_ids)
    require(active and len(set(active)) == len(active), "Invalid requested source case IDs")
    by_case = {case: [row for row in rows if row["case"] == case] for case in active}
    for case, entries in by_case.items():
        keys = {(r["block"], r["state"], r["cohort"], r["minecraft"]) for r in entries}
        require(len(entries) == (5 if case == "S14" else 1) and len(keys) == 1 and
                entries[0]["minecraft"] == "1.21.1", f"Inconsistent original case {case}")
    return by_case, digest


def assets_path(path):
    return "assets/" + path.split("assets/", 1)[1]


def release_sources(mods, source_zip, *, case_ids=None):
    from scripts.integration.audit_int4_nonchair_source import match_state

    rows, ledger = applications(case_ids)
    releases = {
        "AF": ("another_furniture-fabric-4.0.2.jar", "c2f992081bdc4795ed6d87771a3b5f7c71103785"),
        "HC": ("handcrafted-fabric-1.21.1-4.0.3.jar", bed.HC_RELEASE_SHA1),
    }
    records = {}
    with ExitStack() as stack:
        archives = {}
        for cohort, (name, expected) in releases.items():
            path = mods / name
            require(hashlib.sha1(path.read_bytes()).hexdigest() == expected, f"Unexpected JAR {name}")
            archives[cohort] = stack.enter_context(ZipFile(path))
        for case, entries in rows.items():
            first = entries[0]
            jar = archives[first["cohort"]]
            raw_state = jar.read(assets_path(first["state_path"]))
            properties = parse_selector(first["state"].replace(";", ","))
            options = match_state(json.loads(raw_state), properties)
            by_application = {
                (model_path(option["model"]), option.get("x", 0), option.get("y", 0),
                 bool(option.get("uvlock", False)), option.get("weight", 1))
                for _, _, option in options
            }
            expected = {
                (assets_path(row["model_path"]), int(row["x"]), int(row["y"]),
                 bool(int(row["uvlock"])), int(row["weight"]))
                for row in entries
            }
            same_selection = (
                len(options) == len(entries) and len(by_application) == len(options)
                and by_application == expected
            )
            paths = {r[k + "_path"]: r[k + "_sha"] for r in entries for k in ("state", "model", "provider")}
            files = {}
            for origin, historical in sorted(paths.items()):
                try:
                    raw = jar.read(assets_path(origin))
                except KeyError:
                    files[origin] = {"historical_git_blob_sha1": historical, "release_path_absent": True}
                    continue
                files[origin] = {
                    "historical_git_blob_sha1": historical,
                    "release_sha256": sha256(raw),
                    "git_blob_byte_match": bed.git_sha(raw) == historical,
                }
            records[case] = {
                "cohort": first["cohort"],
                "state": state(first["block"], first["state"]),
                "historical_selection_matches_release": same_selection,
                "release_model_applications": [list(entry) for entry in sorted(by_application)],
                "historical_model_geometry": {
                    "elements": sum(int(row["elements"]) for row in entries),
                    "faces": sum(int(row["faces"]) for row in entries),
                },
                "source_files": files,
            }
        bed_json = archives["HC"].read("assets/handcrafted/blockstates/oak_fancy_bed.json")
    return {
        "ledger_sha256": ledger,
        "release_jar_sha1": {key: pair[1] for key, pair in releases.items()},
        "representative_states": records,
        "bed_originals": bed.preflight(mods, source_zip),
    }, property_values(bed_json)



def bed_interaction_source(mods, source_zip):
    rows, _ = bed.source_rows()
    with ZipFile(source_zip) as git, ZipFile(mods / "handcrafted-fabric-1.21.1-4.0.3.jar") as release:
        state_path = rows["S37"]["state_path"]
        raw_state = release.read(assets_path(state_path))
        require(bed.source_zip_file(git, state_path) == raw_state, "Bed selectors differ between Git and JAR")
        selectors = json.loads(raw_state)
        parts = {}
        for case, row in rows.items():
            parts[case] = {}
            for occupied in ("false", "true"):
                properties = row["state"].replace("occupied=false", f"occupied={occupied}")
                index, selector, option = bed.selected_options(selectors, properties)
                leaf_path = model_path(option["model"])
                leaf = release.read(leaf_path)
                variant = json.loads(leaf)
                provider_path = model_path(variant["parent"])
                provider = release.read(provider_path)
                require(leaf == bed.source_zip_file(git, "common/src/main/generated/resources/" + leaf_path),
                        f"Bed leaf model differs between Git and JAR: {leaf_path}")
                require(provider == bed.source_zip_file(git, "common/src/main/resources/" + provider_path),
                        f"Bed parent model differs between Git and JAR: {provider_path}")
                elements = json.loads(provider)["elements"]
                parts[case][occupied] = {
                    "selector": selector, "rule_index": index, "option": option,
                    "leaf": leaf_path, "leaf_git_blob_sha1": bed.git_sha(leaf),
                    "leaf_sha256": sha256(leaf), "provider": provider_path,
                    "provider_git_blob_sha1": bed.git_sha(provider), "provider_sha256": sha256(provider),
                    "elements": len(elements), "faces": sum(len(item["faces"]) for item in elements),
                    "textures": variant["textures"], "git_release_bytes_match": True,
                }
    return {"state_git_blob_sha1": bed.git_sha(raw_state), "state_sha256": sha256(raw_state), "parts": parts}

def property_values(raw):
    values = defaultdict(set)
    for selector in json.loads(raw)["variants"]:
        for key, value in parse_selector(selector).items():
            values[key].add(value)
    return {key: sorted(values[key]) for key in sorted(values)}


def probe(block, coords, properties):
    base = position(*coords)
    result = {"air": f"{base} minecraft:air", "present": f"{base} {block}"}
    for key, values in properties.items():
        result.update({f"{key}={value}": f"{base} {block}[{key}={value}]" for value in values})
    return result


def stages(version, values=None, *, interaction=False, case_ids=None, source_only=False, diagnostic_mode=False):
    x, y, z = ORIGIN
    if version == "1.21.11":
        properties = values or {
            "connection": ("base", "bottom", "middle", "top"),
            "facing": ("east", "north", "south", "west"),
        }
        coordinates = ((x, y, z), (x, y + 1, z), (x, y + 2, z))
        checks = {
            label: probe(SHELF, coords, properties)
            for label, coords in zip(("lower", "middle", "upper"), coordinates)
        }
        if interaction:
            return {
                "shelf_before": ([f"give @s {SHELF} 3"], checks),
                "shelf_one": ([], checks),
                "shelf_two": ([], checks),
                "shelf_three": (["setblock 0 120 42 minecraft:smooth_stone"], checks),
                "shelf_remove_middle": ([], checks),
            }
        placed = [f"setblock {position(*coords)} {SHELF}[facing=north]" for coords in coordinates]
        return {
            "shelf_one": (placed[:1], checks),
            "shelf_two": (placed[1:2], checks),
            "shelf_three": (placed[2:], checks),
            "shelf_remove_middle": ([f"setblock {position(*coordinates[1])} minecraft:air"], checks),
        }

    require(version == "1.21.1", f"Unexpected version {version}")
    if diagnostic_mode:
        require(source_only and not interaction and tuple(case_ids or ()) == ("S02", "S34"),
                "INT-4-F5 diagnostic must be isolated two-case source-only capture")
        from . import int4_f5_state_diagnostic as diagnostic
        return diagnostic.stages(values or {})
    rows, _ = applications(case_ids)
    place = position(*ORIGIN)
    result = {}
    for case in (REMAINING if case_ids is None else tuple(case_ids)):
        row = rows[case][0]
        target = state(row["block"], row["state"])
        clear = f"fill {x - 1} {y} {z - 1} {x + 1} {y} {z + 1} air"
        if case in ("S15", "S17"):
            block = row["block"] + ("[facing=north]" if case == "S15" else "")
            moves = [(dx, dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dz) != (0, 0)]
            place_commands = [
                f"setblock {x + dx} {y} {z + dz} {block}" for dx, dz in [*moves, (0, 0)]
            ]
        else:
            place_commands = [f"setblock {place} {target}"]
        result[case] = (
            [clear, *place_commands],
            {"subject": {"exact": f"{place} {target}", "block": f"{place} {row['block']}"}},
        )
    if source_only:
        require(not interaction, "Source-only capture does not include bed or interaction actions")
        return result
    require(values is not None, "Bed property values must come from the pinned release")
    checks = {
        "foot_position": probe(BED, ORIGIN, values),
        "head_position": probe(BED, (x, y, z - 1), values),
    }
    if interaction:
        return {
            "bed_empty": ([f"give @s {BED} 1"], checks),
            "bed_placed": ([], checks),
            "bed_sleeping": ([
                "gamerule doDaylightCycle false",
                "gamerule playersSleepingPercentage 101",
                "time set midnight",
                "schedule function mcfr_nonchair:check_bed_sleeping 10s replace",
            ], checks),
            "bed_awake": ([], checks),
        }
    result.update({
        "bed_empty": ([f"setblock {place} air", f"setblock {x} {y} {z - 1} air",
                       f"give @s {BED} 1"], checks),
        "bed_placed": ([], checks),
        "bed_foot_broken": ([], checks),
    })
    return result


def setup_commands():
    return [
        "time set noon", "weather clear", "difficulty peaceful", "forceload add -5 34 7 47",
        "fill -4 119 34 5 119 47 minecraft:smooth_stone",
        "fill -3 120 35 4 124 46 minecraft:air", "clear @s",
    ]


def function_files(target, version, values, *, interaction=False, case_ids=None, source_only=False, diagnostic_mode=False):
    fmt = {"pack_format": 48} if version == "1.21.1" else {"min_format": [94, 1], "max_format": [94, 1]}
    scripts = target / "data/mcfr_nonchair/function"
    scripts.mkdir(parents=True, exist_ok=False)
    (target / "pack.mcmeta").write_text(json.dumps({"pack": {"description": "INT-4", **fmt}}) + "\n")
    definitions = {"setup": setup_commands()}
    if interaction and version == "1.21.1":
        definitions["setup"].append("scoreboard objectives add int4_sleep dummy")
    for name, (commands, checks) in stages(version, values, interaction=interaction, case_ids=case_ids, source_only=source_only, diagnostic_mode=diagnostic_mode).items():
        if commands:
            definitions[f"place_{name.lower()}"] = commands
        definitions[f"check_{name.lower()}"] = [
            f"execute if block {predicate} run say INT4_NC {name} {label} {token}"
            for label, alternatives in checks.items() for token, predicate in alternatives.items()
        ]
    hashes = {}
    for name, commands in definitions.items():
        done = f"say INT4_NC {name} done"
        if name in ("check_bed_sleeping", "check_bed_awake"):
            commands = ["execute as @p run " + cmd for cmd in commands]
            commands.extend([
                "execute as @p store result score @s int4_sleep run data get entity @s SleepTimer",
                f"execute as @p if score @s int4_sleep matches 1.. run say INT4_NC timer {name} positive",
                f"execute as @p if score @s int4_sleep matches 0 run say INT4_NC timer {name} zero",
            ])
            done = "execute as @p run " + done
        commands = [*commands, done]
        payload = ("\n".join(commands) + "\n").encode()
        (scripts / f"{name}.mcfunction").write_bytes(payload)
        hashes[name] = sha256(payload)
    return hashes


def read_states(log, version, values, *, interaction=False, case_ids=None, source_only=False, diagnostic_mode=False):
    results = {}
    for stage, (_, checks) in stages(version, values, interaction=interaction, case_ids=case_ids, source_only=source_only, diagnostic_mode=diagnostic_mode).items():
        observations = defaultdict(set)
        for line in log.splitlines():
            if "[Server thread/" not in line or PREFIX + stage + " " not in line:
                continue
            label, _, token = line.split(PREFIX + stage + " ", 1)[1].partition(" ")
            require(label in checks and token in checks[label] and token not in observations[label],
                    f"Unexpected or repeated server result for {stage}/{label}/{token}")
            observations[label].add(token)
        require(sum("[Server thread/" in line and
                    PREFIX + f"check_{stage.lower()} done" in line for line in log.splitlines()) == 1,
                f"Missing or repeated observation completion for {stage}")
        results[stage] = {}
        for label, predicates in checks.items():
            tokens = observations[label]
            if label == "subject":
                require("block" in tokens, f"Requested block absent at {stage}")
                results[stage][label] = {"exact": "exact" in tokens}
                continue
            require(("air" in tokens) != ("present" in tokens), f"Ambiguous block at {stage}/{label}")
            found = {key: value for key, _, value in (token.partition("=") for token in tokens if "=" in token)}
            expected = {token.split("=", 1)[0] for token in predicates if "=" in token}
            if "present" in tokens:
                require(len(tokens) == len(expected) + 1 and found.keys() == expected,
                        f"Missing or ambiguous property at {stage}/{label}")
                results[stage][label] = {"block": "present", **found}
            else:
                require(tokens == {"air"}, f"Unexpected air properties at {stage}/{label}")
                results[stage][label] = {"block": "air"}
    return results


def read_sleep_timers(log):
    outcomes = {}
    for line in log.splitlines():
        if "[Server thread/" not in line or PREFIX + "timer " not in line:
            continue
        stage, _, result = line.split(PREFIX + "timer ", 1)[1].partition(" ")
        require(stage in ("check_bed_sleeping", "check_bed_awake") and
                result in ("positive", "zero") and stage not in outcomes,
                "Invalid or duplicated player sleep timer")
        outcomes[stage] = result
    require(outcomes.keys() == {"check_bed_sleeping", "check_bed_awake"}, "Sleep timer readings missing")
    return outcomes


def capture(command, env, game, output, version, *, interaction=False, case_ids=None, source_only=False, diagnostic_mode=False):
    from PIL import Image

    mods = game / "mods"
    if version == "1.21.1":
        source_zip = env.get("MCFR_HC_SOURCE_ZIP")
        source, values = release_sources(mods, source_zip, case_ids=case_ids)
        if diagnostic_mode:
            require(source_only and not interaction and tuple(case_ids or ()) == ("S02", "S34"),
                    "Only F5 two-case source-only diagnostics are supported")
            from . import int4_f5_state_diagnostic as diagnostic
            values, source["diagnostic_release_properties"] = diagnostic.release_properties(mods)
        if interaction:
            source["bed_occupied_variants"] = bed_interaction_source(mods, source_zip)
    else:
        source = shelf.verify_running_source(mods)
        with ZipFile(mods / source["mod_jar_name"]) as jar:
            values = property_values(jar.read("assets/mcwfurnitures/blockstates/oak_bookshelf.json"))
            source["shelf_variant_models"] = {}
            for selector, option in json.loads(jar.read("assets/mcwfurnitures/blockstates/oak_bookshelf.json"))["variants"].items():
                path = model_path(option["model"])
                raw = jar.read(path)
                provider = model_path(json.loads(raw)["parent"])
                provider_bytes = jar.read(provider)
                elements = json.loads(provider_bytes)["elements"]
                source["shelf_variant_models"][selector] = {
                    "model": path, "model_sha256": sha256(raw), "rotation_y": option.get("y", 0),
                    "provider": provider, "provider_sha256": sha256(provider_bytes),
                    "elements": len(elements), "faces": sum(len(part["faces"]) for part in elements),
                }
    files = function_files(game / "saves/MCFR Visual Fixture/datapacks/mcfr_nonchair",
                           version, values, interaction=interaction,
                           case_ids=case_ids, source_only=source_only,
                           diagnostic_mode=diagnostic_mode)
    output.mkdir(parents=True, exist_ok=False)
    log = output / "client.log"
    shots = game / "screenshots"
    captures = {}
    with log.open("wb") as stream, subprocess.Popen(
        command, cwd=game, env=env, stdout=stream, stderr=subprocess.STDOUT,
    ) as proc:
        def read():
            return log.read_text(encoding="utf-8", errors="replace")

        def xdo(*args):
            return subprocess.check_output(["xdotool", *args], env=env, timeout=20, text=True).strip()

        def send(text):
            xdo("windowfocus", "--sync", window)
            xdo("key", "--clearmodifiers", "t")
            sleep(.4)
            xdo("type", "--clearmodifiers", "--delay", "12", text)
            xdo("key", "--clearmodifiers", "Return")

        def command_and_wait(text, marker):
            prior = len(read())
            send(text)
            wait_for(proc, lambda: marker in read()[prior:], text, 48)
            sleep(1.3)

        def function(name):
            command_and_wait(f"/function mcfr_nonchair:{name}", PREFIX + name + " done")

        def camera(pose):
            command_and_wait("/tp @s " + pose, "[RenderAudit: Teleported RenderAudit to")

        def gamemode(mode):
            command_and_wait("/gamemode " + mode, f"[RenderAudit: Set own game mode to {mode.title()} Mode]")

        def player_input(pose, button, *, sneak=False):
            camera(pose)
            gamemode("creative")
            xdo("key", "--clearmodifiers", "1")
            if sneak:
                xdo("keydown", "Shift_L")
                sleep(.6)
            try:
                xdo("click", str(button))
            finally:
                if sneak:
                    xdo("keyup", "Shift_L")
            sleep(1.8)
            gamemode("spectator")
            camera(CAMERA)

        shelf_actions = {
            "shelf_one": (BED_INTERACTION, 3, False),
            "shelf_two": ("0.5 120 42.5 180 8", 3, True),
            "shelf_three": ("0.5 121 42.5 180 8", 3, True),
            "shelf_remove_middle": ("0.5 120 41.65 180 4", 1, False),
        }
        try:
            wait_for(proc, lambda: "RenderAudit joined the game" in read(), "Fabric world loaded", 180)
            windows = xdo("search", "--all", "--onlyvisible", "--pid", str(proc.pid),
                          "--name", "^Minecraft").split()
            require(len(windows) == 1, "Expected one real Minecraft window")
            window = windows[0]
            sleep(5)
            command_and_wait("/gamemode spectator", "[RenderAudit: Set own game mode to Spectator Mode]")
            camera(CAMERA)
            function("setup")
            for name, (actions, _) in stages(version, values, interaction=interaction, case_ids=case_ids, source_only=source_only, diagnostic_mode=diagnostic_mode).items():
                if actions and name != "bed_sleeping":
                    function(f"place_{name.lower()}")
                if name in ("bed_placed", "bed_foot_broken"):
                    player_input(BED_INTERACTION, 3 if name == "bed_placed" else 1)
                if interaction and name in shelf_actions:
                    pose, button, sneak = shelf_actions[name]
                    player_input(pose, button, sneak=sneak)
                if name == "bed_sleeping":
                    camera(BED_INTERACTION)
                    gamemode("creative")
                    xdo("key", "--clearmodifiers", "2")
                    function("place_bed_sleeping")
                    xdo("click", "3")
                    wait_for(proc, lambda: PREFIX + "check_bed_sleeping done" in read(),
                             "scheduled server sleep observation", 30)
                elif name == "bed_awake":
                    xdo("key", "--clearmodifiers", "Escape")
                    sleep(2)
                    function("check_bed_awake")
                    gamemode("spectator")
                    camera(CAMERA)
                else:
                    function(f"check_{name.lower()}")
                before = set(shots.glob("*.png"))
                if name != "bed_sleeping":
                    xdo("key", "--clearmodifiers", "F1")
                sleep(1)
                xdo("key", "--clearmodifiers", "F2")
                pngs = wait_for(proc, lambda: [path for path in shots.glob("*.png")
                                if path not in before and path.read_bytes().endswith(b"IEND\xaeB`\x82")],
                                f"native F2 {name}", 45)
                require(len(pngs) == 1, f"Unexpected F2 count for {name}")
                with Image.open(pngs[0]) as im:
                    require(im.size == (1024, 684), f"Unexpected F2 size for {name}")
                    im.verify()
                if name != "bed_sleeping":
                    xdo("key", "--clearmodifiers", "F1")
                target = output / (name + ".png")
                shutil.copyfile(pngs[0], target)
                captures[name] = sha256(target.read_bytes())
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=20)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()

    report = {
        "status": "SERVER_STATES_AND_F2_RECORDED",
        "minecraft": version,
        "source": source,
        "property_values": values,
        "server_states": read_states(read(), version, values, interaction=interaction,
                                     case_ids=case_ids, source_only=source_only,
                                     diagnostic_mode=diagnostic_mode),
        "function_payload_sha256": files,
        "client_log_sha256": sha256(log.read_bytes()),
        "native_f2_sha256": captures,
    }
    if diagnostic_mode:
        report["diagnostic_mode"] = True
    if case_ids is not None:
        report["f_target_case_ids"] = list(case_ids)
        report["f_source_only"] = bool(source_only)
    if interaction:
        report["interaction"] = True
        if version == "1.21.1":
            report["sleep_timers"] = read_sleep_timers(read())
    (output / "manifest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def audit(folder, checkpoint=None):
    from PIL import Image

    report = json.loads((folder / "manifest.json").read_text())
    raw = (folder / "client.log").read_bytes()
    require(sha256(raw) == report["client_log_sha256"], "Client log SHA mismatch")
    log = raw.decode("utf-8", errors="replace")
    states = read_states(log, report["minecraft"], report["property_values"],
                         interaction=report.get("interaction", False),
                         case_ids=report.get("f_target_case_ids"),
                         source_only=report.get("f_source_only", False),
                         diagnostic_mode=report.get("diagnostic_mode", False))
    if "sleep_timers" in report:
        require(read_sleep_timers(log) == report["sleep_timers"], "Sleep timer differs from original log")
    require(states == report["server_states"], "Server state inventory differs from original log")
    if checkpoint is not None:
        pinned = json.loads(checkpoint.read_text(encoding="utf-8"))["runs"][report["minecraft"]]
        fields = ["source", "property_values", "function_payload_sha256", "server_states"]
        if "sleep_timers" in pinned:
            fields.append("sleep_timers")
        for field in fields:
            require(report[field] == pinned[field], f"Reproduced {field} differs from reviewed run")
    captures = report["native_f2_sha256"]
    require(captures.keys() == states.keys(), "F2 inventory is incomplete")
    for name, digest in captures.items():
        path = folder / (name + ".png")
        require(sha256(path.read_bytes()) == digest, f"F2 SHA mismatch: {name}")
        with Image.open(path) as im:
            require(im.size == (1024, 684), f"F2 dimensions mismatch: {name}")
            im.verify()
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.directory, args.checkpoint), indent=2, sort_keys=True))
