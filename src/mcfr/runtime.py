"""Run the pinned 1-3-D engine probe or open its in-game visual fixture."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
from urllib.parse import unquote

from .foundation import preview_runtime

ROOT = Path(__file__).resolve().parents[2]
WORLD_NAME = "MCFR Visual Fixture"


def _scratch_path(value: str) -> Path:
    path = Path(value).resolve()
    if ROOT.resolve() == path or ROOT.resolve() in path.parents:
        raise argparse.ArgumentTypeError("Use a scratch path outside the research repository")
    return path


def open_visual_client(args: argparse.Namespace, script: Path, prepare) -> dict | None:
    """Copy an offline creative world and open it with the original pinned input set."""
    world = args.world.resolve()
    if not (world / "level.dat").is_file():
        raise ValueError("The visual fixture needs a saved local creative world")
    game = args.work / args.version / "probe_game"
    copied_world = game / "saves" / WORLD_NAME
    if world == copied_world or world in copied_world.parents:
        raise ValueError("The source world must be outside the disposable destination")
    if copied_world.exists():
        raise FileExistsError(f"Choose a new visual work directory: {copied_world}")

    _, client, assets, index, libraries = prepare(args.version, args.work, args.client_cache)
    shutil.copytree(world, copied_world, ignore=shutil.ignore_patterns("session.lock", "datapacks"))
    fixture = script.parent.parent / "followup/build_runtime_fixture.py"
    subprocess.run(
        [sys.executable, str(fixture), "--version", args.version,
         "--pack", str(copied_world / "datapacks/cd_audit")],
        check=True,
    )
    if args.command in ("chair-capture", "af-variant3-capture", "macaw-kitchen-capture", "macaw-table-shelf-capture", "int4-f9-macaw-five", "int4-f10-macaw-connected-five", "int4-f11-vanilla-five", "hc-bed-capture"):
        from .chair_runtime_fixture import make_pack
        selected=None
        if args.command=="af-variant3-capture":
            from .int4_af_variant3_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="macaw-kitchen-capture":
            from .int4_macaw_kitchen_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="macaw-table-shelf-capture":
            from .int4_macaw_table_shelf_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f9-macaw-five":
            from .int4_f9_macaw_five_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f10-macaw-connected-five":
            from .int4_f10_macaw_connected_five_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f11-vanilla-five":
            from .int4_f11_vanilla_five_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="hc-bed-capture":
            from .int4_handcrafted_bed_capture import cases
            selected=cases(args.version)
        make_pack(args.version, copied_world / "datapacks/mcfr_chair",
                  selected_cases=selected)
    if args.command=="macaw-neighbor-capture":
        from .int4_macaw_neighbor_capture import make_pack as make_neighbor_pack
        make_neighbor_pack(args.version,copied_world/"datapacks/mcfr_neighbor")
    (game / "options.txt").write_text(
        "renderDistance:4\nsimulationDistance:5\nmaxFps:30\nguiScale:2\n", encoding="utf-8"
    )
    env = {**os.environ, "LIBGL_ALWAYS_SOFTWARE": "1", "ALSOFT_DRIVERS": "null"}
    if args.display:
        env["DISPLAY"] = args.display
    command = [
        "java", "-Xmx2G", "-XX:ActiveProcessorCount=4", "-cp", os.pathsep.join(map(str, [client, *libraries])),
        "net.fabricmc.loader.impl.launch.knot.KnotClient", "--username", "RenderAudit",
        "--version", args.version, "--gameDir", str(game), "--assetsDir", str(assets),
        "--assetIndex", index, "--accessToken", "0", "--width", "1024", "--height", "684",
        "--quickPlaySingleplayer", WORLD_NAME,
    ]
    if args.command == "visual-capture":
        from .runtime_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command in ("chair-capture", "af-variant3-capture"):
        from .chair_runtime_capture import capture_chairs
        if args.command=="af-variant3-capture":
            from .int4_af_variant3_capture import capture_cases, exact_expected_models
            return capture_chairs(
                command, env, game, args.output, args.version,
                selected_cases=capture_cases(args.version),
                expected_case_models=exact_expected_models(),
                report_name="INT4_AF_VARIANT3_REAL_F2_CAPTURE.json")
        return capture_chairs(command, env, game, args.output, args.version)
    if args.command=="macaw-kitchen-capture":
        from .int4_macaw_kitchen_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="macaw-table-shelf-capture":
        from .int4_macaw_table_shelf_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f9-macaw-five":
        from .int4_f9_macaw_five_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f10-macaw-connected-five":
        from .int4_f10_macaw_connected_five_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f11-vanilla-five":
        from .int4_f11_vanilla_five_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="hc-bed-capture":
        from .int4_handcrafted_bed_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="macaw-neighbor-capture":
        from .int4_macaw_neighbor_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command == "int4-nonchair-capture":
        from .int4_nonchair_runtime import capture
        return capture(command, env, game, args.output, args.version, interaction=args.interaction)
    if args.command == "int4-f-missing-capture":
        from .int4_f_missing_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f3-mod-capture":
        from .int4_f3_storage_shelf_light_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f4-mod-capture":
        from .int4_f4_chair_bench_couch_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f5-state-diagnostic":
        from .int4_f5_state_diagnostic import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f6-causal-replay":
        from .int4_f6_source_causal_replay import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f7-source-cases":
        from .int4_f7_four_source_cases_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-bed-exterior":
        from .int4_bed_exterior import capture
        return capture(command, env, game, args.output, args.version, uv_probe=args.uv_probe, expanded=args.uv_faces)
    subprocess.run(command, cwd=game, env=env, check=True)
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    engine = sub.add_parser("engine", help="run the historical registry and collision probe")
    visual = sub.add_parser("visual-client", help="open a copied local world for in-game capture")
    capture = sub.add_parser("visual-capture", help="capture and compare pinned in-game scenes on an isolated X11 display")
    chairs = sub.add_parser("chair-capture", help="capture 4 source chairs x 4 facings with verified Minecraft F2 screenshots")
    af3 = sub.add_parser("af-variant3-capture", help="capture AF variant3 four directions plus variant1 controls")
    kitchen = sub.add_parser("macaw-kitchen-capture", help="actual pinned Macaw 1.21.11 kitchen 3-state F2")
    table_shelf = sub.add_parser("macaw-table-shelf-capture", help="actual pinned Macaw 1.21.11 table/bookshelf four source states F2")
    f9macaw = sub.add_parser("int4-f9-macaw-five", help="INT-4-F9 five original Macaw 1.21.11 source states actual native F2")
    f10macaw = sub.add_parser("int4-f10-macaw-connected-five", help="INT-4-F10 five historical connected Macaw 1.21.11 states actual F2")
    f11vanilla = sub.add_parser("int4-f11-vanilla-five", help="INT-4-F11A five official 1.21.11 vanilla historical states source SHA F2")
    hcbed = sub.add_parser("hc-bed-capture", help="pinned Handcrafted 1.21.1 bed foot/head individual native F2")
    neighbor = sub.add_parser("macaw-neighbor-capture", help="actual Macaw table placement/removal adjacent block update trial")
    nonchair = sub.add_parser("int4-nonchair-capture", help="remaining source states and actual shelf/bed transitions")
    fmissing = sub.add_parser("int4-f-missing-capture", help="INT-4-F2 four original 1-5 study cases with native F2")
    f3mod = sub.add_parser("int4-f3-mod-capture", help="INT-4-F3 seven source storage/shelf/lamp cases native F2")
    f4mod = sub.add_parser("int4-f4-mod-capture", help="INT-4-F4 seven chair/bench/couch/pot cases native F2")
    f5mode = sub.add_parser("int4-f5-state-diagnostic", help="INT-4-F5 S02/S34 server property diagnosis and native F2")
    f6mode = sub.add_parser("int4-f6-causal-replay", help="INT-4-F6 S02/S34 source-coded tucked/inner-left game replay")
    f7mode = sub.add_parser("int4-f7-source-cases", help="INT-4-F7 AF variant3, bench double and HC vanilla parent 4 original F2")
    exterior = sub.add_parser("int4-bed-exterior", help="observe occupied bed from an independent client")
    for command in (engine, visual, capture, chairs, af3, kitchen, table_shelf, f9macaw, f10macaw, f11vanilla, hcbed, neighbor, nonchair, fmissing, f3mod, f4mod, f5mode, f6mode, f7mode, exterior):
        command.add_argument("--version", required=True)
        command.add_argument("--work", type=_scratch_path, required=True)
        command.add_argument("--client-cache", type=_scratch_path)
        command.add_argument("--display", help="X11 display, for example :99")
    engine.add_argument("--output", type=_scratch_path, required=True)
    engine.add_argument("--ecj", type=Path)
    for command in (visual, capture, chairs, af3, kitchen, table_shelf, f9macaw, f10macaw, f11vanilla, hcbed, neighbor, nonchair, fmissing, f3mod, f4mod, f5mode, f6mode, f7mode, exterior):
        command.add_argument("--world", type=Path, required=True)
    capture.add_argument("--output", type=_scratch_path, required=True)
    chairs.add_argument("--output", type=_scratch_path, required=True)
    af3.add_argument("--output", type=_scratch_path, required=True)
    kitchen.add_argument("--output", type=_scratch_path, required=True)
    table_shelf.add_argument("--output", type=_scratch_path, required=True)
    f9macaw.add_argument("--output", type=_scratch_path, required=True)
    f10macaw.add_argument("--output", type=_scratch_path, required=True)
    f11vanilla.add_argument("--output", type=_scratch_path, required=True)
    hcbed.add_argument("--output", type=_scratch_path, required=True)
    neighbor.add_argument("--output", type=_scratch_path, required=True)
    nonchair.add_argument("--interaction", action="store_true", help="run player placement and sleeping trials")
    nonchair.add_argument("--output", type=_scratch_path, required=True)
    fmissing.add_argument("--output", type=_scratch_path, required=True)
    f3mod.add_argument("--output", type=_scratch_path, required=True)
    f4mod.add_argument("--output", type=_scratch_path, required=True)
    f5mode.add_argument("--output", type=_scratch_path, required=True)
    f6mode.add_argument("--output", type=_scratch_path, required=True)
    f7mode.add_argument("--output", type=_scratch_path, required=True)
    exterior.add_argument("--uv-probe", action="store_true", help="override the observer texture with a four-tag UV calibration")
    exterior.add_argument("--uv-faces", action="store_true", help="add three exposed occupied-bed faces")
    exterior.add_argument("--output", type=_scratch_path, required=True)
    args = parser.parse_args(argv)

    try:
        plan = preview_runtime(ROOT, args.version)
        script = ROOT / plan["command"][1]
        # The old launcher loads every file under mods/. Keep each run on the pinned inputs.
        mods = args.work / args.version / "probe_game/mods"
        prepare = runpy.run_path(str(script))

        pinned = {unquote(path.rsplit("/", 1)[-1]) for path, _ in prepare["MODS"][args.version]}
        if args.command == "engine":
            pinned.add("research-probe.jar")  # the probe overwrites its own JAR before launch
        if mods.is_symlink() or any(child.name not in pinned or child.is_symlink() for child in mods.glob("*")):
            raise ValueError(f"Use a dedicated work directory containing only the pinned Mods inputs: {mods}")

        if args.command != "engine":
            if not (args.display or os.environ.get("DISPLAY")):
                raise ValueError("An X11 display is required for visual capture")
            if args.command in ("visual-capture", "chair-capture", "af-variant3-capture", "macaw-kitchen-capture", "macaw-table-shelf-capture", "int4-f9-macaw-five", "int4-f10-macaw-connected-five", "int4-f11-vanilla-five", "hc-bed-capture", "macaw-neighbor-capture", "int4-nonchair-capture", "int4-f-missing-capture", "int4-f3-mod-capture", "int4-f4-mod-capture", "int4-f5-state-diagnostic", "int4-f6-causal-replay", "int4-f7-source-cases", "int4-bed-exterior"):
                if shutil.which("xdotool") is None:
                    raise ValueError("Automatic visual capture requires xdotool")
                if args.output.exists():
                    raise FileExistsError(f"Choose a new capture output directory: {args.output}")
            report = open_visual_client(args, script, prepare["prepare"])
            if report is not None:
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return int(report["status"] not in ("MATCH", "CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED", "SERVER_NEIGHBOR_STATES_RECORDED_NO_ASSUMED_CONNECTION", "SERVER_STATES_AND_F2_RECORDED"))
        else:
            command = [sys.executable, str(script), "--version", args.version,
                       "--work", str(args.work), "--output", str(args.output)]
            for option in ("client_cache", "display", "ecj"):
                value = getattr(args, option)
                if value is not None:
                    command.extend(("--" + option.replace("_", "-"), str(value)))
            subprocess.run(command, check=True)
    except (ImportError, KeyError, OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
