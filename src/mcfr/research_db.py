"""SQLite catalog for pinned releases, source assets, and planned research runs."""

from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
import json
from pathlib import Path
import sqlite3

from .foundation import MODES

ROOT = Path(__file__).resolve().parents[2]
APP_ID = 0x4D434652  # MCFR
SCHEMA_VERSION = 3
RELEASE_FIELDS = (
    "release_key", "profile", "target_id", "version", "minecraft_version",
    "loader", "pin_algorithm", "pin_digest", "source",
)
ASSET_FIELDS = ("source_path", "kind", "resource_id", "hash_algorithm", "digest", "byte_count", "evidence_path")


def open_db(path: Path, mode: str) -> sqlite3.Connection:
    db = sqlite3.connect(f"{path.resolve().as_uri()}?mode={mode}", uri=True)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def db_identity(db: sqlite3.Connection) -> tuple[int, int]:
    return db.execute("PRAGMA application_id").fetchone()[0], db.execute("PRAGMA user_version").fetchone()[0]


def require_schema(db: sqlite3.Connection, minimum: int = 1) -> None:
    app, version = db_identity(db)
    if app != APP_ID or not minimum <= version <= SCHEMA_VERSION:
        raise ValueError(f"Expected MCFR DB schema {minimum}–{SCHEMA_VERSION}. Run init to upgrade an older MCFR DB")


@contextmanager
def write_transaction(db: sqlite3.Connection):
    with db:
        db.execute("BEGIN IMMEDIATE")
        yield


def apply_schema(db: sqlite3.Connection, filename: str) -> None:
    schema = Path(__file__).with_name(filename).read_text(encoding="utf-8")
    for statement in schema.split(";"):
        if statement.strip():
            db.execute(statement)


def initialize(path: Path) -> None:
    with closing(open_db(path, "rwc")) as db, write_transaction(db):
        app, version = db_identity(db)
        if (app, version) == (0, 0) and not db.execute("SELECT name FROM sqlite_schema LIMIT 1").fetchone():
            apply_schema(db, "research_schema.sql")
            db.execute(f"PRAGMA application_id = {APP_ID}")
            db.execute("PRAGMA user_version = 1")
            version = 1
        elif app != APP_ID:
            raise ValueError("Cannot initialize an existing database from another application")
        else:
            require_schema(db)
        for next_version in range(version + 1, SCHEMA_VERSION + 1):
            apply_schema(db, f"research_schema_v{next_version}.sql")
            db.execute(f"PRAGMA user_version = {next_version}")


def nonempty(value):
    if not isinstance(value, str) or not value.strip() or value != value.strip() or "\0" in value:
        raise ValueError(f"Expected a non-empty trimmed string: {value!r}")
    return value


def relative_path(value):
    path = nonempty(value)
    if any(part in {"", ".", ".."} for part in path.split("/")) or "\\" in path or ":" in path:
        raise ValueError(f"Expected a relative POSIX path: {path}")
    return path


def register_release(db: sqlite3.Connection, release: dict, assets) -> int:
    values = tuple(nonempty(release[key]) for key in RELEASE_FIELDS)
    release_key = values[0]
    db.execute(
        f"INSERT INTO release ({', '.join(RELEASE_FIELDS)}) VALUES ({', '.join('?' for _ in values)}) "
        "ON CONFLICT(release_key) DO NOTHING", values,
    )
    if tuple(db.execute("SELECT * FROM release WHERE release_key = ?", (release_key,)).fetchone()) != values:
        raise ValueError(f"Conflicting metadata for release {release_key}")

    added = 0
    for asset in assets:
        path = relative_path(asset["source_path"])
        size = asset.get("byte_count")
        if size is not None and (type(size) is not int or not 0 <= size < (1 << 63)):
            raise ValueError(f"Invalid byte_count for {path}")
        evidence = asset.get("evidence_path")
        row = (
            release_key, path, nonempty(asset["kind"]), nonempty(asset["resource_id"]),
            nonempty(asset["hash_algorithm"]), nonempty(asset["digest"]), size,
            None if evidence is None else relative_path(evidence),
        )
        inserted = db.execute(
            f"INSERT INTO asset (release_key, {', '.join(ASSET_FIELDS)}) VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(release_key, source_path) DO NOTHING", row,
        ).rowcount
        if not inserted:
            previous = db.execute(
                "SELECT * FROM asset WHERE release_key = ? AND source_path = ?", (release_key, path),
            ).fetchone()
            if tuple(previous) != row:
                raise ValueError(f"Conflicting asset metadata for {release_key}: {path}")
        added += inserted
    return added


def create_run(db: sqlite3.Connection, run_id: str, release_key: str, mode: str, baseline: str | None) -> dict:
    nonempty(run_id)
    release = db.execute("SELECT profile, target_id FROM release WHERE release_key = ?", (release_key,)).fetchone()
    if release is None:
        raise ValueError(f"Unknown release: {release_key}")
    if mode == "INCREMENTAL":
        previous = db.execute(
            "SELECT profile, target_id FROM release WHERE release_key = ?", (baseline,),
        ).fetchone()
        if previous != release or baseline == release_key:
            raise ValueError("INCREMENTAL requires a distinct baseline release for the same profile and target")
    elif baseline is not None:
        raise ValueError("Only INCREMENTAL accepts a baseline release")

    values = (run_id, release_key, mode, baseline)
    db.execute(
        "INSERT INTO research_run (run_id, release_key, mode, baseline_release_key) VALUES (?, ?, ?, ?) "
        "ON CONFLICT(run_id) DO NOTHING", values,
    )
    record = db.execute("SELECT * FROM research_run WHERE run_id = ?", (run_id,)).fetchone()
    if tuple(record)[:4] != values:
        raise ValueError(f"Conflicting metadata for research run {run_id}")
    return dict(record)


def summary(db: sqlite3.Connection) -> dict:
    by_release = {}
    for row in db.execute("SELECT release_key, kind, count(*) AS total FROM asset GROUP BY release_key, kind ORDER BY kind"):
        by_release.setdefault(row["release_key"], {})[row["kind"]] = row["total"]
    return {
        "schema_version": db_identity(db)[1],
        "releases": [dict(row, assets_by_kind=by_release.get(row["release_key"], {}))
                     for row in db.execute("SELECT * FROM release ORDER BY release_key")],
        "runs": [dict(row) for row in db.execute("SELECT * FROM research_run ORDER BY created_at, run_id")],
    }


def nonnegative_int(value: str) -> int:
    number = int(value)
    if number < 0 or number > (1 << 63) - 1:
        raise argparse.ArgumentTypeError("Expected a non-negative SQLite integer")
    return number


def main(argv: list[str] | None = None) -> int:
    from . import legacy_catalog

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, help="Operational SQLite database")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository containing legacy evidence")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("summary")
    sub.add_parser("import-legacy")
    inspect = sub.add_parser("legacy-info", help="Inspect an existing SQLite evidence artifact read-only")
    inspect.add_argument("artifact", choices=legacy_catalog.DATABASES)
    register = sub.add_parser("register")
    register.add_argument("manifest", type=Path)
    assets = sub.add_parser("assets")
    assets.add_argument("release_key")
    assets.add_argument("--offset", type=nonnegative_int, default=0)
    assets.add_argument("--limit", type=nonnegative_int, default=20)
    run = sub.add_parser("run-create")
    run.add_argument("run_id")
    run.add_argument("release_key")
    run.add_argument("--mode", choices=sorted(MODES), required=True)
    run.add_argument("--baseline")
    args = parser.parse_args(argv)
    try:
        if args.command == "legacy-info":
            result = legacy_catalog.database_info(args.root, args.artifact)
        elif args.db is None:
            parser.error("--db is required")
        elif args.command == "init":
            initialize(args.db)
            result = {"schema_version": SCHEMA_VERSION}
        else:
            read_only = args.command in {"summary", "assets"}
            with closing(open_db(args.db, "ro" if read_only else "rw")) as db:
                require_schema(db)
                if args.command == "summary":
                    db.execute("BEGIN")  # keep all summary reads on the same SQLite snapshot
                    result = summary(db)
                elif args.command == "assets":
                    result = [dict(row) for row in db.execute(
                        "SELECT * FROM asset WHERE release_key = ? ORDER BY source_path LIMIT ? OFFSET ?",
                        (args.release_key, args.limit, args.offset),
                    )]
                else:
                    with write_transaction(db):
                        if args.command == "import-legacy":
                            result = legacy_catalog.import_catalog(db, args.root, register_release)
                        elif args.command == "register":
                            manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
                            result = {"assets_added": register_release(db, manifest["release"], manifest["assets"])}
                        else:
                            result = create_run(db, args.run_id, args.release_key, args.mode, args.baseline)
    except (OSError, KeyError, TypeError, ValueError, RuntimeError, sqlite3.Error) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
