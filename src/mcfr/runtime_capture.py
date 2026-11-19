"""Drive the fixed Mods visual fixture and record verified native screenshots."""

import json
from pathlib import Path
import shutil
import subprocess
from time import monotonic, sleep

from .visual_check import compare

REFERENCE = Path(__file__).resolve().parents[2] / "project/audits/runtime"
SCENES = {
    "1.21.1": ("0 122 48", (
        ("another-furniture.png", "4.5 120 37.2 0 20"),
        ("handcrafted.png", "-6.8 120 52.8 0 18"),
    )),
    "1.21.11": ("0 122 215", (("macaws-furniture.png", "1.9 120 214.1 0 13"),)),
}


def wait_for(process, condition, description, timeout=30):
    deadline = monotonic() + timeout
    while monotonic() < deadline:
        if process.poll() is not None:
            raise ValueError(f"Minecraft exited before {description} (code {process.returncode})")
        result = condition()
        if result:
            return result
        sleep(0.25)
    raise ValueError(f"Timed out waiting for {description}")


def capture(command, env, game, output, version):
    staging_camera, scenes = SCENES[version]
    audit = json.loads((REFERENCE / "REPLAY_AUDIT.json").read_text(encoding="utf-8"))
    expected_states = audit["observations"][version]["visual_cases_checked_against_server"]
    output.mkdir(parents=True)
    log = output / "client.log"
    with log.open("wb") as stream, subprocess.Popen(
        command, cwd=game, env=env, stdout=stream, stderr=subprocess.STDOUT,
    ) as process:
        def read_log():
            return log.read_text(encoding="utf-8", errors="replace")

        def input_x11(*args):
            return subprocess.check_output(["xdotool", *args], env=env, timeout=15, text=True)

        def game_command(text):
            input_x11("key", "--clearmodifiers", "t")
            sleep(0.3)
            input_x11("type", "--clearmodifiers", "--delay", "25", text)
            input_x11("key", "--clearmodifiers", "Return")

        def position_camera(camera):
            offset = len(read_log())
            game_command(f"/tp @s {camera}")
            wait_for(process, lambda: "[RenderAudit: Teleported RenderAudit to" in read_log()[offset:],
                     "the camera teleport to complete")
            sleep(4)

        try:
            wait_for(process, lambda: "RenderAudit joined the game" in read_log(), "the fixture world to load", 120)
            window = input_x11("search", "--all", "--onlyvisible", "--pid", str(process.pid),
                               "--name", "^Minecraft").split()
            if len(window) != 1:
                raise ValueError("Expected exactly one visible Minecraft window on the isolated display")
            input_x11("windowfocus", "--sync", window[0])
            sleep(2)
            game_command("/gamemode spectator")
            sleep(1)
            position_camera(f"{staging_camera} 0 10")
            game_command("/function cd_audit:place")
            wait_for(process, lambda: "[RenderAudit] CD_PLACED" in read_log(), "fixture placement")
            game_command("/function cd_audit:verify")
            wait_for(process, lambda: "[RenderAudit] CD_STATES_READ" in read_log(), "fixture state checks")
            observed = {line.split("[RenderAudit] CD_STATE_", 1)[1].strip()
                        for line in read_log().splitlines()
                        if "[Server thread/" in line and "[RenderAudit] CD_STATE_" in line}
            if not all(f"{key}={value}" in observed for key, value in expected_states.items()):
                raise ValueError("Placed furniture states differ from the audited fixture")

            images = []
            screenshots = game / "screenshots"
            for filename, camera in scenes:
                position_camera(camera)
                previous = set(screenshots.glob("*.png"))
                input_x11("key", "--clearmodifiers", "F1")
                sleep(1)
                input_x11("key", "--clearmodifiers", "F2")
                candidates = wait_for(process, lambda: [
                    path for path in screenshots.glob("*.png")
                    if path not in previous and path.read_bytes().endswith(b"IEND\xaeB\x60\x82")
                ], "Minecraft to save a complete PNG")
                input_x11("key", "--clearmodifiers", "F1")
                if len(candidates) != 1:
                    raise ValueError("Expected exactly one new Minecraft screenshot")
                shutil.copyfile(candidates[0], output / filename)
                result = compare(REFERENCE / filename, output / filename,
                                 reference_sha256=audit["captures"][filename]["sha256"])
                images.append({"file": filename, "camera": camera, **result})
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

    report = {"version": version, "status": "MATCH" if all(image["status"] == "MATCH" for image in images) else "DIFFERENCE",
              "states": expected_states, "captures": images}
    (output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
