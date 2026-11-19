"""Re-run two historical audits and compare their outputs with the published evidence."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


def verify(command, published):
    result = json.loads(subprocess.check_output([sys.executable, *command], text=True))
    if result.get("status") != "PASS" or result != json.loads(published.read_text(encoding="utf-8")):
        raise ValueError(f"Replayed result differs from {published}")
    return result


def main():
    root = Path(__file__).resolve().parents[2]
    mods = root / "research/furniture_mods"
    phase_3 = mods / "phase_1-3"
    handoff = phase_3 / "F"
    comparison = mods / "phase_1-5/E"
    with TemporaryDirectory(prefix="mcfr-handoff-audit-") as temporary:
        # The historical F audit writes beside its DB. Give it a scratch copy.
        scratch = Path(temporary) / "F"
        shutil.copytree(handoff, scratch)
        handoff_result = verify([
            handoff / "audit_handoff.py",
            "--b", phase_3 / "B/source_verification",
            "--c", phase_3 / "C",
            "--d", phase_3 / "D",
            "--e", phase_3 / "E",
            "--out", scratch,
        ], handoff / "F_INDEPENDENT_AUDIT.json")
    comparison_result = verify(
        [comparison / "audit_comparison_db.py"], comparison / "INDEPENDENT_AUDIT.json"
    )
    print(json.dumps({"1-3-F": handoff_result, "1-5-E": comparison_result}, indent=2))


if __name__ == "__main__":
    main()
