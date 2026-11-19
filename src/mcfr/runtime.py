"""Run the pinned 1-3-D engine probe or open its in-game visual fixture."""
from __future__ import annotations

import argparse
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


def open_visual_client(args: argparse.Namespace, script: Path, prepare) -> None:
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
    subprocess.run(command, cwd=game, env=env, check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    engine = sub.add_parser("engine", help="run the historical registry and collision probe")
    visual = sub.add_parser("visual-client", help="open a copied local world for in-game capture")
    for command in (engine, visual):
        command.add_argument("--version", required=True)
        command.add_argument("--work", type=_scratch_path, required=True)
        command.add_argument("--client-cache", type=_scratch_path)
        command.add_argument("--display", help="X11 display, for example :99")
    engine.add_argument("--output", type=_scratch_path, required=True)
    engine.add_argument("--ecj", type=Path)
    visual.add_argument("--world", type=Path, required=True)
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

        if args.command == "visual-client":
            if not (args.display or os.environ.get("DISPLAY")):
                raise ValueError("An X11 display is required for visual capture")
            open_visual_client(args, script, prepare["prepare"])
        else:
            command = [sys.executable, str(script), "--version", args.version,
                       "--work", str(args.work), "--output", str(args.output)]
            for option in ("client_cache", "display", "ecj"):
                value = getattr(args, option)
                if value is not None:
                    command.extend(("--" + option.replace("_", "-"), str(value)))
            subprocess.run(command, check=True)
    except (KeyError, OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
