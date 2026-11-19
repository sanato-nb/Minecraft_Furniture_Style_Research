"""Read-only research-profile validation and plan preview (H1 foundation)."""
from __future__ import annotations

import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

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
    if shared.get("default_execution") != "hybrid_phased":
        raise ValueError("Expected phased hybrid execution")
    if shared.get("visual_validation") != "existing_runtime_probe_first":
        raise ValueError("Expected existing runtime probe first")
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
    return {
        "status": "PASS",
        "schema_version": 1,
        "profiles": profiles,
        "modes": sorted(MODES),
        "scope": "foundation_configuration_only",
        "execution_policy": shared["default_execution"],
        "publication_policy": shared["default_write_policy"],
        "visual_validation_policy": shared["visual_validation"],
    }


def preview_plan(root: Path, profile: str, mode: str, target_id: str, release: str, baseline_release: str | None = None) -> dict:
    settings = validate(root)
    mode = mode.upper()
    if profile not in PROFILES or mode not in MODES:
        raise ValueError("Unsupported profile/mode")
    if not target_id.strip() or not release.strip():
        raise ValueError("target_id and release are required")
    if mode == "INCREMENTAL" and (baseline_release is None or not baseline_release.strip()):
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
        "execution_policy": settings["execution_policy"],
        "publication_policy": settings["publication_policy"],
        "visual_validation_policy": settings["visual_validation_policy"],
        "writes_repository": False,
        "execution_enabled": False
    }


def preview_runtime(root: Path, minecraft_version: str) -> dict:
    validate(root)
    probe = _load_json(root / "harness/mods/profile.json")["existing_runtime_probe"]
    if minecraft_version not in probe["minecraft_versions"]:
        raise ValueError(f"No existing mod fixture for Minecraft {minecraft_version}")
    for key in ("script", "workflow", "evidence"):
        if not (root / probe[key]).is_file():
            raise ValueError(f"Missing existing runtime probe {key}: {probe[key]}")
    return {
        "status": "PLAN_ONLY",
        "profile": "mods",
        "minecraft_version": minecraft_version,
        "scope": ["registered_states", "state_rule_matching", "collision_boxes"],
        "screenshot_capture": False,
        "workflow": probe["workflow"],
        "evidence": probe["evidence"],
        "command": [
            "python", probe["script"], "--version", minecraft_version,
            "--work", "<scratch-work-dir>", "--output", "<scratch-output-dir>",
        ],
    }


def check_catalog(root: Path, db_path: Path) -> dict:
    from .research_db import db_identity, open_db, relative_path, require_schema

    root = root.resolve()
    with closing(open_db(db_path, "ro")) as db:
        db.execute("BEGIN")
        require_schema(db)
        if [row[0] for row in db.execute("PRAGMA integrity_check")] != ["ok"]:
            raise ValueError("Research catalog failed SQLite integrity check")
        if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise ValueError("Research catalog contains an invalid foreign key")
        releases = db.execute("SELECT count(*) FROM release").fetchone()[0]
        assets, linked = db.execute("SELECT count(*), count(evidence_path) FROM asset").fetchone()
        evidence = [relative_path(row[0]) for row in db.execute(
            "SELECT DISTINCT evidence_path FROM asset WHERE evidence_path IS NOT NULL ORDER BY evidence_path"
        )]
        schema = db_identity(db)[1]
    if not evidence:
        raise ValueError("Research catalog has no evidence paths. Import the legacy catalog first.")
    for path in evidence:
        target = (root / path).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            raise ValueError(f"Invalid or missing catalog evidence: {path}")
    return {"schema_version": schema, "integrity": "ok", "foreign_key_violations": 0,
            "releases": releases, "assets": assets, "assets_with_evidence": linked, "evidence_paths": evidence}


def replay_history(root: Path, db_path: Path) -> dict:
    settings = validate(root)
    catalog = check_catalog(root, db_path)
    script = root.resolve() / "scripts/migration/replay_evidence.py"
    output = subprocess.check_output([sys.executable, script], text=True)
    return {"status": "PASS", "profiles": settings["profiles"], "catalog": catalog, "audits": json.loads(output)}


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
    runtime = sub.add_parser("runtime-plan", help="Preview invocation of the existing fixed Mods runtime fixture")
    runtime.add_argument("--minecraft-version", required=True)
    history = sub.add_parser("replay-history", help="Check a research catalog and replay the three historical audits")
    history.add_argument("--db", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate(args.root)
        elif args.command == "runtime-plan":
            result = preview_runtime(args.root, args.minecraft_version)
        elif args.command == "replay-history":
            result = replay_history(args.root, args.db)
        else:
            result = preview_plan(args.root, args.profile, args.mode, args.target_id, args.release, args.baseline_release)
    except (ValueError, OSError, KeyError, sqlite3.Error, subprocess.CalledProcessError) as err:
        parser.error(str(err))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
