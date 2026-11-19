"""Replay historical audits from outside the checkout without modifying their evidence."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
VANILLA_SCRIPT = Path("scripts/phase_1_2_g_global_exit_audit.py")
VANILLA_ROOT = Path("research/vanilla_models")
VANILLA_FINAL = VANILLA_ROOT / "phase_1-2-G/final"
VANILLA_OUTPUTS = (
    "G_GLOBAL_INDEPENDENT_RECOUNT.json",
    "G_FINAL_SOURCE_SHA_4669.csv",
    "G_FINAL_MCMETA_99.csv",
)


def run_audit(command, cwd):
    return json.loads(subprocess.check_output([sys.executable, *command], cwd=cwd, text=True))


def verify(result, published):
    expected = json.loads(published.read_text(encoding="utf-8"))
    if result.get("status") != "PASS" or result != expected:
        raise ValueError(f"Replayed result differs from {published}")
    return result


def replay_vanilla(scratch):
    # This legacy entry point resolves paths from __file__ and writes to its root.
    # Export its fixed inputs as a separate tree with the original layout.
    exported = scratch / "vanilla"
    exported.mkdir()
    archive = scratch / "vanilla.tar"
    paths = [
        VANILLA_SCRIPT,
        "1.21.11/assets/minecraft",
        "docs/vanilla_models_1-2/1-2-G_ACCEPTANCE_CONTRACT.json",
        "handoff/STATE.json",
        *(VANILLA_ROOT / name for name in (
            "v34", "phase_1-2-B/entry6/B_SCOPE_2390_STATUS.csv", "phase_1-2-C/entry5", "phase_1-2-D", "phase_1-2-E/E_FIXED_SCOPE_86.csv",
            "phase_1-2-F", "phase_1-2-G",
        )),
    ]
    subprocess.run(
        ["git", "-C", ROOT, "archive", "--output", archive, "HEAD", "--", *paths], check=True,
    )
    with tarfile.open(archive) as stream:
        stream.extractall(exported, filter="data")

    for name in VANILLA_OUTPUTS:
        (exported / VANILLA_FINAL / name).unlink()
    result = run_audit([exported / VANILLA_SCRIPT], cwd=scratch)
    if result["status"] != "G1_G5_SOURCE_PASS_G6_REMOTE_PENDING" or result["errors"]:
        raise ValueError(f"Vanilla source replay did not pass: {result}")
    for name in VANILLA_OUTPUTS:
        regenerated = exported / VANILLA_FINAL / name
        if regenerated.read_bytes() != (ROOT / VANILLA_FINAL / name).read_bytes():
            raise ValueError(f"Replayed Vanilla evidence differs: {name}")
    return {**result, "byte_identical_outputs": list(VANILLA_OUTPUTS)}


def replay_mods(scratch):
    mods = ROOT / "research/furniture_mods"
    phase_3 = mods / "phase_1-3"
    handoff = phase_3 / "F"
    comparison = mods / "phase_1-5/E"
    # The 1-3-F audit uses explicit phase paths and writes beside its DB.
    # The 1-5-E audit resolves sibling inputs and pinned Git objects itself.
    handoff_copy = scratch / "handoff"
    shutil.copytree(handoff, handoff_copy)
    published = "F_INDEPENDENT_AUDIT.json"
    (handoff_copy / published).unlink()
    handoff_result = verify(run_audit([
        handoff / "audit_handoff.py",
        "--b", phase_3 / "B/source_verification",
        "--c", phase_3 / "C",
        "--d", phase_3 / "D",
        "--e", phase_3 / "E",
        "--out", handoff_copy,
    ], cwd=scratch), handoff / published)
    verify(handoff_result, handoff_copy / published)
    comparison_result = verify(
        run_audit([comparison / "audit_comparison_db.py"], cwd=scratch),
        comparison / "INDEPENDENT_AUDIT.json",
    )
    return {"1-3-F": handoff_result, "1-5-E": comparison_result}


def main():
    with TemporaryDirectory(prefix="mcfr-path-replay-") as temporary:
        scratch = Path(temporary)
        result = {"1-2-G": replay_vanilla(scratch), **replay_mods(scratch)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
