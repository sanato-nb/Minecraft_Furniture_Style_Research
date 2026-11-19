"""Launch a pinned Adorn release for an engine probe or a copied visual world."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
PINS = ROOT / "project/audits/h67/ADORN_PINS.json"
HISTORICAL = ROOT / "research/furniture_mods/phase_1-3/runtime_actions"
VERSION = "1.21.11"
LOADER = "0.19.3"
PROFILE_SHA1 = "70f0578ca2eb9048dc5a4bbf5aec603be619a96a"
FABRIC_HASHES = {
    f"net.fabricmc:fabric-loader:{LOADER}": "354dfaa02d0552e11867f85dff7cdbfaf813ba3e",
    f"net.fabricmc:intermediary:{VERSION}": "f1e2033afc8b637150c223b2bfd352d37544bc96",
}
WORLD = "Adorn Research Fixture"


def outside_repository(path):
    resolved = Path(path).resolve()
    if resolved.is_relative_to(ROOT):
        raise argparse.ArgumentTypeError("Use a path outside the research repository")
    return resolved


def pinned_adorn(path):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    pins = json.loads(PINS.read_text(encoding="utf-8"))
    for label, release in pins.items():
        if release["files"][0]["hashes"]["sha256"] == digest:
            return label
    raise ValueError("Adorn JAR does not match an audited pin")


def prepare_runtime(cache, client_cache):
    tools = runpy.run_path(str(HISTORICAL / "run_probe.py"))
    download = tools["download"]
    profile_path = cache / VERSION / "profile.json"
    # The historical helper consumes this profile from its cache.
    download(f"https://meta.fabricmc.net/v2/versions/loader/{VERSION}/{LOADER}/profile/json",
             profile_path, PROFILE_SHA1)
    profile = json.loads(profile_path.read_bytes())
    for entry in profile["libraries"]:
        expected = entry.get("sha1") or FABRIC_HASHES[entry["name"]]
        group, artifact, version = entry["name"].split(":")
        path = f"{group.replace('.', '/')}/{artifact}/{version}/{artifact}-{version}.jar"
        download(entry["url"] + path, cache / "libs" / path, expected)

    prepare = tools["prepare"]
    # Use the existing pinned Fabric API, without the historical furniture mods.
    api = [mod for mod in tools["MODS"][VERSION] if "/fabric-api-" in mod[0]]
    if len(api) != 1:
        raise ValueError("Expected a single pinned Fabric API")
    prepare.__globals__["MODS"] = {VERSION: api}
    run, client, assets, index, libraries = prepare(VERSION, cache, client_cache)
    api_file = run / "probe_game/mods" / "fabric-api-0.141.6+1.21.11.jar"
    return client, assets, index, libraries, api_file


def build_probe(game, loader, ecj):
    source = (HISTORICAL / "StateProbe.java").read_text(encoding="utf-8")
    target = 'Set.of("mcwfurnitures")'
    if source.count(target) != 1:
        raise ValueError("The historical probe namespace selector changed")
    compiler = ["javac", "--release", "21"] if ecj is None else ["java", "-jar", str(ecj), "-21", "-proc:none"]
    with TemporaryDirectory(prefix="mcfr-adorn-build-") as temporary:
        build = Path(temporary)
        src = build / "StateProbe.java"
        src.write_text(source.replace(target, 'Set.of("adorn")'), encoding="utf-8")
        subprocess.run([*compiler, "-cp", str(loader), "-d", str(build), str(src)], check=True)
        with ZipFile(game / "mods/research-probe.jar", "w", ZIP_DEFLATED) as jar:
            for path in build.rglob("*.class"):
                jar.write(path, path.relative_to(build))
            jar.writestr("fabric.mod.json", json.dumps({
                "schemaVersion": 1, "id": "research_state_probe", "version": "1.0.0", "environment": "client",
                "entrypoints": {"client": ["research.StateProbe"]},
                "depends": {"fabricloader": f">={LOADER}", "fabric-lifecycle-events-v1": "*"},
            }))


def launch(args):
    label = pinned_adorn(args.jar)
    client, assets, index, libraries, api = prepare_runtime(args.cache, args.client_cache)
    game = args.work / f"{label}-{args.mode}"
    if game.exists():
        raise ValueError("Choose a new work directory for this run")
    mods = game / "mods"
    mods.mkdir(parents=True)
    shutil.copy2(args.jar, mods / args.jar.name)
    shutil.copy2(api, mods / api.name)
    (game / "options.txt").write_text(
        "renderDistance:4\nsimulationDistance:5\nmaxFps:30\nguiScale:2\n", encoding="utf-8",
    )
    options, flags = [], []
    if args.mode == "engine":
        loader = next(path for path in libraries if path.name == f"fabric-loader-{LOADER}.jar")
        build_probe(game, loader, args.ecj)
        flags = [f"-Dresearch.mc={VERSION}", f"-Dresearch.output={game / 'ENGINE_STATES.tsv'}"]
    else:
        if args.world is None or not (args.world / "level.dat").is_file():
            raise ValueError("Visual mode requires a saved local creative world")
        shutil.copytree(args.world, game / "saves" / WORLD, ignore=shutil.ignore_patterns("session.lock", "datapacks"))
        options = ["--quickPlaySingleplayer", WORLD]

    env = {**os.environ, "LIBGL_ALWAYS_SOFTWARE": "1", "ALSOFT_DRIVERS": "null"}
    if args.display:
        env["DISPLAY"] = args.display
    command = [
        "java", "-Xmx2G", "-XX:ActiveProcessorCount=4", *flags,
        "-cp", os.pathsep.join(map(str, [client, *libraries])),
        "net.fabricmc.loader.impl.launch.knot.KnotClient", "--username", "RenderAudit",
        "--version", VERSION, "--gameDir", str(game), "--assetsDir", str(assets), "--assetIndex", index,
        "--accessToken", "0", "--width", "1024", "--height", "684", *options,
    ]
    if not env.get("DISPLAY"):
        command = ["xvfb-run", "-a", *command]
    with (game / "client.log").open("w", encoding="utf-8") as log:
        subprocess.run(command, cwd=game, env=env, stdout=log, stderr=subprocess.STDOUT, check=True,
                       timeout=240 if args.mode == "engine" else None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("engine", "visual"))
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--cache", type=outside_repository, required=True)
    parser.add_argument("--work", type=outside_repository, required=True)
    parser.add_argument("--client-cache", type=outside_repository)
    parser.add_argument("--ecj", type=Path)
    parser.add_argument("--world", type=Path)
    parser.add_argument("--display")
    args = parser.parse_args()
    args.jar = args.jar.resolve()
    try:
        launch(args)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
