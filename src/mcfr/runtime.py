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
    if args.command in ("chair-capture", "af-variant3-capture", "macaw-kitchen-capture", "macaw-table-shelf-capture", "hc-bed-capture"):
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
        elif args.command=="hc-bed-capture":
            from .int4_handcrafted_bed_capture import cases
            selected=cases(args.version)
        make_pack(args.version, copied_world / "datapacks/mcfr_chair",
                  selected_cases=selected)
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
    if args.command=="hc-bed-capture":
        from .int4_handcrafted_bed_capture import capture
        return capture(command,env,game,args.output,args.version)
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
    hcbed = sub.add_parser("hc-bed-capture", help="pinned Handcrafted 1.21.1 bed foot/head individual native F2")
    for command in (engine, visual, capture, chairs, af3, kitchen, table_shelf, hcbed):
        command.add_argument("--version", required=True)
        command.add_argument("--work", type=_scratch_path, required=True)
        command.add_argument("--client-cache", type=_scratch_path)
        command.add_argument("--display", help="X11 display, for example :99")
    engine.add_argument("--output", type=_scratch_path, required=True)
    engine.add_argument("--ecj", type=Path)
    for command in (visual, capture, chairs, af3, kitchen, table_shelf, hcbed):
        command.add_argument("--world", type=Path, required=True)
    capture.add_argument("--output", type=_scratch_path, required=True)
    chairs.add_argument("--output", type=_scratch_path, required=True)
    af3.add_argument("--output", type=_scratch_path, required=True)
    kitchen.add_argument("--output", type=_scratch_path, required=True)
    table_shelf.add_argument("--output", type=_scratch_path, required=True)
    hcbed.add_argument("--output", type=_scratch_path, required=True)
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
            if args.command in ("visual-capture", "chair-capture", "af-variant3-capture", "macaw-kitchen-capture", "macaw-table-shelf-capture", "hc-bed-capture"):
                if shutil.which("xdotool") is None:
                    raise ValueError("Automatic visual capture requires xdotool")
                if args.output.exists():
                    raise FileExistsError(f"Choose a new capture output directory: {args.output}")
            report = open_visual_client(args, script, prepare["prepare"])
            if report is not None:
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return int(report["status"] not in ("MATCH", "CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED"))
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
