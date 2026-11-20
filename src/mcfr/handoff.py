"""Export, verify and restore an operational MCFR SQLite research handoff.

Snapshots are local artifacts, not public GitHub evidence. They may contain
absolute file paths, user-authored prompts and provider response metadata.
"""
from __future__ import annotations

import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
from tempfile import TemporaryDirectory

from . import research_db as catalog

SNAPSHOT = "research.sqlite"
MANIFEST = "handoff.json"
TABLES = ("release", "asset", "research_run", "research_execution",
          "source_job", "source_checkpoint", "ai_review", "upstream_observation")


def outside_repository(path: Path) -> Path:
    path = path.resolve()
    root = catalog.ROOT.resolve()
    if path == root or path.is_relative_to(root):
        raise ValueError("Handoff data may contain private paths; choose a destination outside the Git repository")
    return path


def db_checks(path: Path) -> dict:
    with closing(catalog.open_db(path, "ro")) as db:
        catalog.require_schema(db, minimum=4)
        if [r[0] for r in db.execute("PRAGMA integrity_check")] != ["ok"]:
            raise ValueError("SQLite integrity check failed")
        if db.execute("PRAGMA foreign_key_check").fetchone():
            raise ValueError("SQLite foreign key check failed")
        counts = {table: db.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in TABLES}
        pending = db.execute("SELECT count(*) FROM source_job WHERE execution_id IS NULL").fetchone()[0]
        paths_with_sources = db.execute("SELECT count(DISTINCT source_path) FROM source_job").fetchone()[0]
        return {"schema_version": catalog.db_identity(db)[1], "counts": counts,
                "pending_jobs": pending, "saved_source_paths": paths_with_sources}


def checksum(path: Path) -> str:
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def export(source: Path, destination: Path) -> dict:
    destination = outside_repository(destination)
    if destination.exists():
        raise FileExistsError(f"Handoff destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    source = source.resolve()
    # Avoid mutating or copying the original database file into the repository.
    with TemporaryDirectory(prefix="mcfr-handoff-", dir=destination.parent) as tmp:
        working = Path(tmp)
        snapshot = working / SNAPSHOT
        with closing(catalog.open_db(source, "ro")) as db:
            catalog.require_schema(db, minimum=4)
            with closing(sqlite3.connect(snapshot)) as backup:
                db.backup(backup)
        checked = db_checks(snapshot)
        try:
            commit = subprocess.check_output(
                ["git", "-C", str(catalog.ROOT), "rev-parse", "HEAD"],
                text=True, stderr=subprocess.DEVNULL, timeout=5,
            ).strip()
        except (OSError, subprocess.SubprocessError):
            commit = None
        manifest = {
            "format": "mcfr-operational-handoff-v1", "repository_commit": commit,
            "snapshot_file": SNAPSHOT, "snapshot_sha256": checksum(snapshot),
            **checked,
            "notes": [
                "Keep this directory outside the public repository; SQLite may contain private paths or AI responses.",
                "Restoration preserves records but original source paths must still be available to resume a job.",
                "Reference GitHub PRs and pinned source files separately for published, shareable research evidence.",
            ],
        }
        (working / MANIFEST).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        working.rename(destination)
    return {"status": "EXPORTED", "location": str(destination), **manifest}


def verify(directory: Path) -> dict:
    directory = directory.resolve()
    manifest_path = directory / MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("format") != "mcfr-operational-handoff-v1" or manifest.get("snapshot_file") != SNAPSHOT:
        raise ValueError("Unsupported handoff manifest")
    expected = manifest.get("snapshot_sha256")
    if not isinstance(expected, str) or len(expected) != 64:
        raise ValueError("Invalid handoff digest")
    snapshot = directory / SNAPSHOT
    if checksum(snapshot) != expected:
        raise ValueError("Handoff snapshot SHA256 mismatch")
    checked = db_checks(snapshot)
    for key, value in checked.items():
        if manifest.get(key) != value:
            raise ValueError(f"Handoff metadata mismatch: {key}")
    return {"status": "VERIFIED", "snapshot_sha256": expected, **checked}


def restore(directory: Path, destination: Path) -> dict:
    checked = verify(directory)
    destination = outside_repository(destination)
    if destination.exists():
        raise FileExistsError(f"Will not overwrite existing research DB: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="mcfr-restore-", dir=destination.parent) as tmp:
        working = Path(tmp) / SNAPSHOT
        shutil.copyfile(directory.resolve() / SNAPSHOT, working)
        if checksum(working) != checked["snapshot_sha256"]:
            raise ValueError("Copied snapshot differs from verified handoff")
        working.rename(destination)
    return {"status": "RESTORED", "db": str(destination), **checked}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    ex = sub.add_parser("export")
    ex.add_argument("--db", required=True, type=Path)
    ex.add_argument("--out", required=True, type=Path, help="New local folder outside repository")
    ve = sub.add_parser("verify")
    ve.add_argument("--input", required=True, type=Path)
    res = sub.add_parser("restore")
    res.add_argument("--input", required=True, type=Path)
    res.add_argument("--db", required=True, type=Path, help="New local DB path outside repository")
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            result = export(args.db, args.out)
        elif args.command == "verify":
            result = verify(args.input)
        else:
            result = restore(args.input, args.db)
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
