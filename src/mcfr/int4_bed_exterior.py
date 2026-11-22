"""Observe a live bed from a second Minecraft client and capture native F2 evidence."""
from __future__ import annotations

import argparse
import hashlib
from contextlib import ExitStack
import json
from io import BytesIO
from itertools import groupby
import os
from pathlib import Path
import shutil
import socket
import subprocess
from tempfile import mkdtemp
from time import sleep
from zipfile import ZipFile

from . import int4_nonchair_runtime as prior
from .runtime_capture import wait_for

VERSION = "1.21.1"
OBSERVER = "BedObserver"
ISO = "2.65 121.65 43.8 149 30"
OVERHEAD = "0.5 123.5 39.8 180 90"
SHOTS = ("empty", "placed", "sleeping", "sleeping_overhead", "awake")
JAR = "handcrafted-fabric-1.21.1-4.0.3.jar"
UV_TAGS = {
    "nw_red": (34, 60, (255, 20, 20)),
    "ne_green": (46, 60, (20, 255, 20)),
    "sw_blue": (34, 62, (20, 20, 255)),
    "se_yellow": (46, 62, (255, 235, 20)),
}


class Client:
    def __init__(self, command, env, game, log, stack):
        self.game, self.log, self.env = game, log, env
        stream = stack.enter_context(log.open("wb"))
        self.proc = subprocess.Popen(command, cwd=game, env=env, stdout=stream,
                                     stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        stack.callback(self.close)

    def close(self):
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()

    def read(self):
        return self.log.read_text(encoding="utf-8", errors="replace")

    def wait(self, check, description, timeout=60):
        return wait_for(self.proc, check, description, timeout)

    def xdo(self, *args):
        return subprocess.check_output(["xdotool", *args], env=self.env, text=True, timeout=18).strip()

    def find_window(self):
        windows = self.xdo("search", "--all", "--onlyvisible", "--pid", str(self.proc.pid),
                           "--name", "^Minecraft").split()
        prior.require(len(windows) == 1, f"Expected one window for {self.log.name}")
        self.window = windows[0]

    def focus(self):
        self.xdo("windowraise", self.window)
        self.xdo("windowfocus", "--sync", self.window)
        sleep(.35)

    def shot(self, path):
        from PIL import Image

        folder = self.game / "screenshots"
        before = set(folder.glob("*.png"))
        self.focus()
        self.xdo("key", "--clearmodifiers", "F2")
        result = self.wait(lambda: [p for p in folder.glob("*.png")
                            if p not in before and p.read_bytes().endswith(b"IEND\xaeB`\x82")],
                           f"external F2 {path.stem}", 35)
        prior.require(len(result) == 1, "Expected one native F2")
        with Image.open(result[0]) as image:
            prior.require(image.size == (1024, 684), "Unexpected native F2 dimensions")
            image.verify()
        shutil.copyfile(result[0], path)
        return prior.sha256(path.read_bytes())


def connection_command(command, player, game, port):
    result = list(command)
    result[result.index("--username") + 1] = player
    result[result.index("--gameDir") + 1] = str(game)
    index = result.index("--quickPlaySingleplayer")
    result[index:index + 2] = ["--quickPlayMultiplayer", f"127.0.0.1:{port}"]
    return result


def probe_source(mods, source, source_zip, pack, *, apply, expanded=False):
    from PIL import Image

    variant = source["bed_occupied_variants"]["parts"]["S37"]["true"]
    with ZipFile(mods / JAR) as jar:
        model_bytes = jar.read(variant["provider"])
        prior.require(prior.sha256(model_bytes) == variant["provider_sha256"], "Unexpected occupied provider")
        model = json.loads(model_bytes)
        part = model["elements"][5]
        face = part["faces"]["up"]
        prior.require(part["from"] == [0, 7, 13] and part["to"] == [16, 9, 16] and
                      part["rotation"]["angle"] == 0 and face["uv"] == [6.125, 7.875, 4.125, 7.5]
                      and face["rotation"] == 180, "Pinned upper footboard face changed")
        slot = model["textures"][face["texture"][1:]]
        texture = variant["textures"][slot[1:]]
        namespace, name = texture.split(":", 1)
        texture_path = f"assets/{namespace}/textures/{name}.png"
        raw = jar.read(texture_path)
    with ZipFile(source_zip) as git:
        prior.require(prior.bed.source_zip_file(git, "common/src/main/resources/" + texture_path) == raw,
                      "Original Git and JAR frame texture differ")
    with Image.open(BytesIO(raw)) as png:
        image = png.convert("RGBA")
    prior.require(image.size == (128, 128), "Unexpected footboard texture size")
    textures = {texture_path: image}
    result = {
        "source_texture": texture_path, "texture_sha256": prior.sha256(raw), "texture_size": [128, 128],
        "provider": variant["provider"], "provider_sha256": variant["provider_sha256"],
        "element_index_zero_based": 5, "direction": "up", "model_bounds": [part["from"], part["to"]],
        "uv": face["uv"], "uv_rotation": face["rotation"], "slot_chain": [face["texture"], slot, texture],
        "git_and_jar_texture_bytes_match": True, "observer_probe_texture_sha256": None,
    }
    if apply:
        for x, y, color in UV_TAGS.values():
            for col in (x, x + 1):
                image.putpixel((col, y), (*color, 255))
    if expanded:
        from . import int4_bed_uv_faces
        result["additional_faces"] = int4_bed_uv_faces.prepare(mods, source_zip, variant, textures, apply=apply)
    if apply:
        pack.parent.mkdir()
        with ZipFile(pack, "w") as output:
            output.writestr("pack.mcmeta", json.dumps({"pack": {"description": "INT-4 UV sample",
                                                                "pack_format": 34}}))
            for asset, marked in textures.items():
                altered = BytesIO()
                marked.save(altered, format="PNG")
                payload = altered.getvalue()
                output.writestr(asset, payload)
                if asset == texture_path:
                    result["observer_probe_texture_sha256"] = prior.sha256(payload)
    return result


def projected_tags(floor_width):
    # Use the ten-block platform to calibrate the effective vertical-view zoom.
    # The footboard's height changes scale and its reversed UV axes cancel rotation 180.
    cam_x, cam_y, cam_z, _, _ = map(float, OVERHEAD.split())
    eye_y = cam_y + 1.62
    scale = floor_width / 10 * (eye_y - 120) / (eye_y - (120 + 9 / 16))
    return {
        name: (round(512 + (((x + 1) / 8 - 4.125) / 2 - cam_x) * scale),
               round(342 + (40 + 13 / 16 + ((y + .5) / 8 - 7.5) / .375 * (3 / 16) - cam_z) * scale))
        for name, (x, y, _) in UV_TAGS.items()
    }


def read_tags(path):
    from PIL import Image

    with Image.open(path) as im:
        image = im.convert("RGB")
    runs = groupby(max(image.getpixel((x, 526))) >= 45 for x in range(image.width))
    floor_width = max((sum(1 for _ in group) for bright, group in runs if bright), default=0)
    prior.require(600 <= floor_width <= 1000, f"Overhead platform projection missing: {floor_width}")
    return {
        "floor_width_pixels": floor_width,
        "tags": {name: {"xy": [x, y], "rgb": list(image.getpixel((x, y)))}
                 for name, (x, y) in projected_tags(floor_width).items()},
    }


def capture(command, env, game, output, version, *, uv_probe=False, expanded=False):
    prior.require(version == VERSION, "The occupied Handcrafted bed fixture is fixed to Minecraft 1.21.1")
    output.mkdir(parents=True, exist_ok=False)
    observer_game = Path(mkdtemp(prefix="bed-observer-", dir=game.parent))
    shutil.copytree(game / "mods", observer_game / "mods")
    prior.require({(p.name, prior.sha256(p.read_bytes())) for p in (observer_game / "mods").glob("*.jar")} ==
                  {(p.name, prior.sha256(p.read_bytes())) for p in (game / "mods").glob("*.jar")},
                  "Observer and host do not share the same mod JARs")
    source_zip = env.get("MCFR_HC_SOURCE_ZIP")
    source, values = prior.release_sources(game / "mods", source_zip)
    source["bed_occupied_variants"] = prior.bed_interaction_source(game / "mods", source_zip)
    pack = observer_game / "resourcepacks/int4_uv_probe.zip"
    uv_source = probe_source(game / "mods", source, source_zip, pack, apply=uv_probe, expanded=expanded)
    server_game = Path(mkdtemp(prefix="bed-server-", dir=game.parent))
    shutil.copytree(game / "mods", server_game / "mods")
    shutil.copytree(game / "saves/MCFR Visual Fixture", server_game / "world")
    functions = server_game / "world/datapacks/mcfr_nonchair"
    files = prior.function_files(functions, VERSION, values, interaction=True)
    for stage in ("check_bed_sleeping", "check_bed_awake"):
        file = functions / f"data/mcfr_nonchair/function/{stage}.mcfunction"
        payload = file.read_bytes().replace(b"execute as @p", b"execute as RenderAudit")
        file.write_bytes(payload)
        files[stage] = prior.sha256(payload)
    options = "renderDistance:4\nsimulationDistance:5\nmaxFps:24\nguiScale:2\npauseOnLostFocus:false\nfov:0.0\nmipmapLevels:0\n"
    for directory in (game, observer_game):
        configured = options
        if uv_probe and directory == observer_game:
            configured += 'resourcePacks:["fabric","file/int4_uv_probe.zip"]\n'
        (directory / "options.txt").write_text(configured, encoding="utf-8")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    server_jar = Path(env["MCFR_BED_SERVER_JAR"]).resolve()
    server_sha1 = hashlib.sha1(server_jar.read_bytes()).hexdigest()
    prior.require(server_sha1 == "59353fb40c36d304f2035d51e7d6e6baa98dc05c", "Unexpected server JAR")
    (server_game / "eula.txt").write_text("eula=true\n")
    (server_game / "server.properties").write_text(
        f"server-ip=127.0.0.1\nserver-port={port}\nonline-mode=false\n"
        "gamemode=creative\nview-distance=4\nsimulation-distance=5\n"
        "spawn-protection=0\nlevel-name=world\n", encoding="utf-8")
    # Keep the Fabric loader/dependencies and use the official bundled server as the game JAR.
    dependencies = command[command.index("-cp") + 1].split(os.pathsep)[1:]
    server_command = [
        "java", "-Xmx2G", "-XX:ActiveProcessorCount=4", f"-Dfabric.gameJarPath={server_jar}",
        "-cp", os.pathsep.join([str(server_jar), *dependencies]),
        "net.fabricmc.loader.impl.launch.knot.KnotServer", "nogui",
    ]
    results = {}
    with ExitStack() as stack:
        server = Client(server_command, env, server_game, output / "server.log", stack)
        server.wait(lambda: "For help, type" in server.read(), "Fabric localhost server ready", 150)
        host = Client(connection_command(command, "RenderAudit", game, port), env,
                      game, output / "host.log", stack)
        obs = Client(connection_command(command, OBSERVER, observer_game, port), env,
                     observer_game, output / "observer.log", stack)
        server.wait(lambda: all(f"{name} joined the game" in server.read()
                                for name in ("RenderAudit", OBSERVER)), "both local clients joined", 180)
        host.find_window()
        obs.find_window()
        sleep(5)

        def console(command, marker=None):
            offset = len(server.read())
            server.proc.stdin.write((command + "\n").encode())
            server.proc.stdin.flush()
            if marker:
                server.wait(lambda: marker in server.read()[offset:], command, 45)

        def fn(name):
            console(f"execute as RenderAudit run function mcfr_nonchair:{name}", prior.PREFIX + name + " done")

        def tp(name, pose):
            console(f"tp {name} {pose}", f"Teleported {name} to")
            sleep(1.8)

        console(f"gamemode spectator {OBSERVER}", f"Set {OBSERVER}")
        console("gamemode spectator RenderAudit", "Set RenderAudit")
        tp(OBSERVER, ISO)
        tp("RenderAudit", "0.5 121 44.7 180 35")
        fn("setup")
        console("gamerule doDaylightCycle false")
        console("time set midnight", "Set the time to")
        console("fill -2 123 37 2 123 43 minecraft:light[level=15]", "Successfully filled")
        obs.focus()
        obs.xdo("key", "--clearmodifiers", "F1")
        fn("place_bed_empty")
        fn("check_bed_empty")
        results["empty"] = obs.shot(output / "empty.png")
        tp("RenderAudit", prior.BED_INTERACTION)
        console("gamemode creative RenderAudit", "Set RenderAudit")
        sleep(1)
        host.focus()
        host.xdo("key", "--clearmodifiers", "1")
        host.xdo("click", "3")
        sleep(1.5)
        fn("check_bed_placed")
        prior.require(all(prior.PREFIX + f"bed_placed {part}_position present" in server.read()
                          for part in ("foot", "head")), "Player's use did not install both bed halves")
        tp("RenderAudit", "0.5 120 44.7 180 35")
        results["placed"] = obs.shot(output / "placed.png")
        tp("RenderAudit", prior.BED_INTERACTION)
        host.focus()
        host.xdo("key", "--clearmodifiers", "2")
        fn("place_bed_sleeping")
        host.xdo("click", "3")
        server.wait(lambda: prior.PREFIX + "check_bed_sleeping done" in server.read(),
                    "scheduled occupied-state observation", 35)
        results["sleeping"] = obs.shot(output / "sleeping.png")
        tp(OBSERVER, OVERHEAD)
        console(f"execute if block 0 120 40 {prior.BED}[part=foot,occupied=true] "
                f"if block 0 120 39 {prior.BED}[part=head,occupied=true] "
                "run say INT4 EXTERIOR OVERHEAD OCCUPIED", "INT4 EXTERIOR OVERHEAD OCCUPIED")
        results["sleeping_overhead"] = obs.shot(output / "sleeping_overhead.png")
        if expanded:
            from . import int4_bed_uv_faces
            for name, pose in int4_bed_uv_faces.VIEWS.items():
                tp(OBSERVER, pose)
                console(f"execute if block 0 120 40 {prior.BED}[part=foot,occupied=true] "
                        f"if block 0 120 39 {prior.BED}[part=head,occupied=true] run say INT4 VIEW {name} OCCUPIED",
                        f"INT4 VIEW {name} OCCUPIED")
                results[name] = obs.shot(output / f"{name}.png")
        host.focus()
        host.xdo("key", "--clearmodifiers", "Escape")
        sleep(2)
        fn("check_bed_awake")
        tp("RenderAudit", "0.5 120 44.7 180 35")
        tp(OBSERVER, ISO)
        results["awake"] = obs.shot(output / "awake.png")

    mode_states = prior.read_states(server.read(), VERSION, values, interaction=True)
    timers = prior.read_sleep_timers(server.read())
    report = {
        "status": "SERVER_STATES_AND_F2_RECORDED", "minecraft": VERSION, "source": source,
        "property_values": values, "function_payload_sha256": files, "server_states": mode_states,
        "sleep_timers": timers, "native_f2_sha256": results,
        "log_sha256": {p.stem: prior.sha256(p.read_bytes()) for p in output.glob("*.log")},
        "observer": OBSERVER, "server_jar_sha1": server_sha1, "uv_probe": uv_probe, "uv_source": uv_source,
        "observer_camera": {"iso": ISO, "overhead": OVERHEAD},
    }
    if expanded:
        report["observer_camera"].update(int4_bed_uv_faces.VIEWS)
    (output / "manifest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report


def tag_matches(rgb, tag):
    peak = max(rgb)
    if peak < 24:
        return False
    target = UV_TAGS[tag][2]
    return max(abs(observed / peak - reference / max(target))
               for observed, reference in zip(rgb, target)) <= .27


def audit(folder, checkpoint=None):
    from PIL import Image

    record = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    for name in ("server", "host", "observer"):
        path = folder / f"{name}.log"
        prior.require(prior.sha256(path.read_bytes()) == record["log_sha256"][name], f"{name} log SHA mismatch")
    host = (folder / "server.log").read_text(encoding="utf-8")
    observer = (folder / "observer.log").read_text(encoding="utf-8")
    occupied = [line for line in host.splitlines() if "INT4 EXTERIOR OVERHEAD OCCUPIED" in line
                and "[Server thread/" in line]
    prior.require(len(occupied) == 1 and f"{OBSERVER} joined the game" in host,
                  "Observer join or occupied overhead in server log missing")
    states = prior.read_states(host, VERSION, record["property_values"], interaction=True)
    prior.require(states == record["server_states"], "Server state mismatch")
    for part in ("foot_position", "head_position"):
        occupancy = [states[stage][part]["occupied"] for stage in ("bed_placed", "bed_sleeping", "bed_awake")]
        prior.require(occupancy == ["false", "true", "false"], f"Unexpected {part} occupancy sequence")
    timers = prior.read_sleep_timers(host)
    prior.require(timers == record["sleep_timers"] == {
        "check_bed_sleeping": "positive", "check_bed_awake": "zero"}, "Sleep timer mismatch")
    expected_shots = set(SHOTS)
    expanded = "additional_faces" in record["uv_source"]
    if expanded:
        from . import int4_bed_uv_faces
        expected_shots.update(int4_bed_uv_faces.VIEWS)
        for view, pose in int4_bed_uv_faces.VIEWS.items():
            xyz = ", ".join(f"{float(n):.6f}" for n in pose.split()[:3])
            prior.require(record["observer_camera"][view] == pose and
                          f"Teleported {OBSERVER} to {xyz}" in host, f"Camera location differs for {view}")
            prior.require(sum("[Server thread/" in line and f"INT4 VIEW {view} OCCUPIED" in line
                              for line in host.splitlines()) == 1, f"Bed occupancy evidence missing for {view}")
    prior.require(set(record["native_f2_sha256"]) == expected_shots, "F2 inventory mismatch")
    for name in sorted(expected_shots):
        path = folder / f"{name}.png"
        prior.require(prior.sha256(path.read_bytes()) == record["native_f2_sha256"][name], f"F2 SHA mismatch: {name}")
        with Image.open(path) as picture:
            prior.require(picture.size == (1024, 684), f"F2 dimensions mismatch: {name}")
            picture.verify()
    pack_lines = [line for line in observer.splitlines() if "Reloading ResourceManager:" in line]
    applied = any(line.rfind("file/int4_uv_probe.zip") > line.rfind("handcrafted") >= 0 for line in pack_lines)
    prior.require(applied == record["uv_probe"], "Observer probe pack did not have priority over the mod")
    projection = read_tags(folder / "sleeping_overhead.png")
    matches = {tag: tag_matches(sample["rgb"], tag) for tag, sample in projection["tags"].items()}
    record.pop("projected_samples", None)
    record["uv_projection"] = projection
    prior.require(all(value == record["uv_probe"] for value in matches.values()),
                  f"Projected UV tags did not distinguish probe from original: {matches}")
    if expanded:
        record["additional_face_samples"] = int4_bed_uv_faces.audit(folder, record, OVERHEAD, tag_matches)
    if checkpoint:
        data = json.loads(checkpoint.read_text(encoding="utf-8"))
        expected = data["runs"]["uv_probe" if record["uv_probe"] else "native"]
        for key in ("source", "function_payload_sha256", "server_states", "sleep_timers", "observer_camera", "server_jar_sha1"):
            prior.require(expected[key] == record[key], f"Reproduction differs for {key}")
        # PNG encoders can differ across Pillow versions. Original PNG and declared probe pixels stay pinned.
        for key in expected["uv_source"].keys() - {"observer_probe_texture_sha256"}:
            prior.require(expected["uv_source"][key] == record["uv_source"][key],
                          f"UV source differs for {key}")
    return record


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--directory", type=Path, required=True)
    p.add_argument("--checkpoint", type=Path)
    args = p.parse_args()
    print(json.dumps(audit(args.directory, args.checkpoint), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
