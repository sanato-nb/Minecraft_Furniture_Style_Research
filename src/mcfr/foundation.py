"""Read-only research-profile validation and plan preview (H1 foundation)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MODES = frozenset(("NEW", "INCREMENTAL", "REVALIDATE", "FRESH"))
PROFILES = frozenset(("vanilla", "mods"))


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def validate(root: Path) -> dict:
    root = Path(root)
    shared = _load_json(root / "harness/shared/config.json")
    if shared.get("schema_version") != 1:
        raise ValueError("Unsupported shared schema")
    if set(shared.get("research_modes", [])) != MODES:
        raise ValueError("Research modes mismatch")
    if set(shared.get("profiles", [])) != PROFILES:
        raise ValueError("Research profile mismatch")
    if shared.get("default_write_policy") != "branch_pr_only":
        raise ValueError("Unexpected write policy")
    if shared.get("automatic_main_merge") is not False:
        raise ValueError("Main auto merge must be disabled")
    if shared.get("automatic_inbox_delete") is not False:
        raise ValueError("Inbox auto delete must be disabled")
    profiles = {}
    for name in sorted(PROFILES):
        p = _load_json(root / "harness" / name / "profile.json")
        if p.get("schema_version") != 1 or p.get("id") != name:
            raise ValueError(f"Invalid profile: {name}")
        if not (root / p["instructions"]).is_file():
            raise ValueError(f"Profile instructions missing: {name}")
        profiles[name] = p["target_kind"]
    if not (root / "inbox/README.md").is_file():
        raise ValueError("Missing public inbox safety policy")
    return {"status": "PASS", "schema_version": 1, "profiles": profiles, "modes": sorted(MODES), "scope": "foundation_configuration_only"}


def preview_plan(root: Path, profile: str, mode: str, target_id: str, release: str, baseline_release: str | None = None) -> dict:
    validate(root)
    mode = mode.upper()
    if profile not in PROFILES or mode not in MODES:
        raise ValueError("Unsupported profile/mode")
    if not target_id.strip() or not release.strip():
        raise ValueError("target_id and release are required")
    if mode == "INCREMENTAL" and not baseline_release:
        raise ValueError("Incremental research requires baseline_release")
    return {
        "schema_version": 1,
        "status": "PLAN_ONLY",
        "profile": profile,
        "target_id": target_id,
        "release": release,
        "baseline_release": baseline_release,
        "mode": mode,
        "prior_result_policy": "do_not_use_prior_conclusions" if mode == "FRESH" else "verify_before_reuse",
        "writes_repository": False,
        "execution_enabled": False
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="H1 read-only harness foundation")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    p = sub.add_parser("plan")
    p.add_argument("--profile", choices=sorted(PROFILES), required=True)
    p.add_argument("--mode", choices=sorted(MODES), required=True)
    p.add_argument("--target-id", required=True)
    p.add_argument("--release", required=True)
    p.add_argument("--baseline-release")
    args = parser.parse_args(argv)
    try:
        result = validate(args.root) if args.command == "validate" else preview_plan(
            args.root, args.profile, args.mode, args.target_id, args.release, args.baseline_release
        )
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as err:
        parser.error(str(err))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
