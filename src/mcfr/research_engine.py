"""Plan, execute and inspect a deterministic analysis linked to an MCFR run."""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing, contextmanager
import hashlib
import json
from pathlib import Path
import runpy
import sqlite3
import struct
import subprocess
from tempfile import TemporaryDirectory
import uuid
from zipfile import BadZipFile, ZipFile

from . import research_db as catalog

ENGINE_VERSION = 1
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash(asset: dict) -> tuple:
    return tuple(asset[key] for key in ("kind", "resource_id", "hash_algorithm", "digest", "byte_count"))


def plan_run(db: sqlite3.Connection, run_id: str) -> dict:
    row = db.execute("SELECT * FROM research_run WHERE run_id = ?", (run_id,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown research run: {run_id}")

    def assets_for(key):
        return {asset["source_path"]: dict(asset) for asset in db.execute(
            "SELECT * FROM asset WHERE release_key = ? ORDER BY source_path", (key,),
        )}

    run = dict(row)
    key = run["release_key"]
    release = dict(db.execute("SELECT * FROM release WHERE release_key = ?", (key,)).fetchone())
    assets = assets_for(key)
    if not assets:
        raise ValueError(f"No cataloged assets for {key}")
    removed = []
    scope = Counter({"all": 0, "added": 0, "changed": 0, "unchanged": 0, "removed": 0})
    selected = []
    baseline = {}
    if run["mode"] == "INCREMENTAL":
        baseline = assets_for(run["baseline_release_key"])
        if not baseline:
            raise ValueError(f"No cataloged assets for baseline {run['baseline_release_key']}")
        removed = sorted(baseline.keys() - assets.keys())
        scope["removed"] = len(removed)
    for path, asset in assets.items():
        if run["mode"] != "INCREMENTAL":
            disposition = "all"
        elif path not in baseline:
            disposition = "added"
        else:
            disposition = "unchanged" if _hash(baseline[path]) == _hash(asset) else "changed"
        scope[disposition] += 1
        if disposition != "unchanged":
            selected.append({"reason": disposition, **asset})

    snapshot = {
        "mode": run["mode"], "release": release, "baseline_release_key": run["baseline_release_key"],
        "current_assets": assets, "baseline_assets": baseline,
    }
    scope_sha256 = hashlib.sha256(_json(snapshot).encode()).hexdigest()
    return {
        "run": run, "release": release, "scope_sha256": scope_sha256,
        "counts": dict(scope), "selected": selected, "removed": removed,
    }


@contextmanager
def source_reader(source: Path, release: dict):
    source = source.resolve()
    if source.is_dir():
        def read(relative):
            file = (source / catalog.relative_path(relative)).resolve()
            if not file.is_relative_to(source):
                raise ValueError("Source member escapes the input directory")
            return file.read_bytes()

        yield read, "asset_hashes"
        return

    algorithm = release["pin_algorithm"]
    if algorithm not in {"SHA1", "SHA256"}:
        raise ValueError("A ZIP/JAR source requires a SHA1 or SHA256 release pin")
    with source.open("rb") as stream:
        if hashlib.file_digest(stream, algorithm.lower()).hexdigest() != release["pin_digest"]:
            raise ValueError("ZIP/JAR differs from the registered release pin")
        stream.seek(0)
        with ZipFile(stream) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise ValueError("ZIP/JAR contains duplicate member paths")
            yield archive.read, "archive_and_asset_hashes"


def asset_digest(body: bytes, algorithm: str) -> str:
    if algorithm == "GIT_BLOB_SHA1":
        digest = hashlib.sha1(f"blob {len(body)}\0".encode())
        digest.update(body)
        return digest.hexdigest()
    return hashlib.new(algorithm.lower(), body).hexdigest()


def inspect_asset(body: bytes, kind: str) -> dict:
    if kind == "texture":
        if len(body) < 33 or body[:16] != PNG_SIGNATURE + b"\x00\x00\x00\x0dIHDR":
            raise ValueError("Missing PNG IHDR")
        width, height = struct.unpack_from(">II", body, 16)
        if min(width, height) == 0:
            raise ValueError("Invalid PNG dimensions")
        return {"width": width, "height": height}

    def unique_fields(pairs):
        fields = dict(pairs)
        if len(fields) != len(pairs):
            raise ValueError("Duplicate JSON object keys")
        return fields

    def reject_constant(value):
        raise ValueError(f"Invalid JSON constant: {value}")

    data = json.loads(body, object_pairs_hook=unique_fields, parse_constant=reject_constant)
    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object")
    return {"top_level_keys": sorted(data)}


def verify_source(plan: dict, source: Path) -> dict:
    assets = []
    with source_reader(source, plan["release"]) as (read, pin_check):
        for entry in plan["selected"]:
            path = entry["source_path"]
            report = {"source_path": path, "kind": entry["kind"], "reason": entry["reason"]}
            try:
                body = read(path)
                report["digest"] = asset_digest(body, entry["hash_algorithm"])
                if report["digest"] != entry["digest"]:
                    raise ValueError(f"Digest mismatch; expected {entry['digest']}")
                if entry["byte_count"] is not None and len(body) != entry["byte_count"]:
                    raise ValueError(f"Byte count mismatch; expected {entry['byte_count']}")
                report["observations"] = inspect_asset(body, entry["kind"])
                report["status"] = "PASS"
            except (KeyError, OSError, ValueError, RuntimeError, BadZipFile) as exc:
                report.update(status="FAIL", error=str(exc))
            assets.append(report)
    failed = sum(asset["status"] == "FAIL" for asset in assets)
    return {"status": "FAIL" if failed else "PASS", "pin_check": pin_check,
            "verified": len(assets) - failed, "failed": failed, "assets": assets,
            "removed": plan["removed"]}


def verify_legacy(plan: dict) -> dict:
    root = catalog.ROOT
    release = plan["release"]
    registry = json.loads((root / "registry/legacy-releases.json").read_text(encoding="utf-8"))
    if plan["run"]["mode"] != "REVALIDATE" or release not in registry.values():
        raise ValueError("Legacy replay requires REVALIDATE and a matching fixed release")
    runners = runpy.run_path(str(root / "scripts/migration/replay_evidence.py"))
    with TemporaryDirectory(prefix="mcfr-engine-replay-") as directory:
        scratch = Path(directory)
        results = {"1-2-G": runners["replay_vanilla"](scratch)} if release["profile"] == "vanilla" else (
            runners["replay_mods"](scratch)
        )
    git_head = subprocess.check_output(["git", "-C", root, "rev-parse", "HEAD"], text=True).strip()
    return {"status": "PASS", "evidence_scope": "historical_fixed_audit", "checkout_commit": git_head,
            "audits": results}


def record_execution(db, plan: dict, backend: str, report: dict) -> dict:
    report = {**report, "catalog_scope_counts": plan["counts"]}
    execution_id = uuid.uuid4().hex
    with catalog.write_transaction(db):
        db.execute(
            "INSERT INTO research_execution (execution_id, run_id, engine_version, backend, scope_sha256, "
            "status, report_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (execution_id, plan["run"]["run_id"], ENGINE_VERSION, backend, plan["scope_sha256"],
             report["status"], _json(report)),
        )
    return read_executions(db, plan["run"]["run_id"], execution_id=execution_id)[0]


def read_executions(db, run_id: str, *, details=False, execution_id=None) -> list:
    if db.execute("SELECT 1 FROM research_run WHERE run_id = ?", (run_id,)).fetchone() is None:
        raise ValueError(f"Unknown research run: {run_id}")
    records = []
    for row in db.execute(
        "SELECT * FROM research_execution WHERE run_id = ? AND (? IS NULL OR execution_id = ?) "
        "ORDER BY finished_at, execution_id", (run_id, execution_id, execution_id),
    ):
        record = dict(row)
        report = json.loads(record.pop("report_json"))
        if not details:
            report.pop("assets", None)
            report.pop("removed", None)
        records.append(dict(record, report=report))
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "execute", "show"):
        command = commands.add_parser(name)
        command.add_argument("run_id")
        if name == "execute":
            source = command.add_mutually_exclusive_group(required=True)
            source.add_argument("--source", type=Path, help="Source directory or pinned ZIP/JAR")
            source.add_argument("--legacy", action="store_true", help="Replay the fixed historical audit")
        else:
            command.add_argument("--details", action="store_true")
    args = parser.parse_args(argv)

    try:
        with closing(catalog.open_db(args.db, "rw" if args.command == "execute" else "ro")) as db:
            catalog.require_schema(db, minimum=2)
            if args.command == "show":
                result = read_executions(db, args.run_id, details=args.details)
            else:
                db.execute("BEGIN")
                plan = plan_run(db, args.run_id)
                db.commit()
                if args.command == "plan":
                    if not args.details:
                        plan.pop("selected")
                        plan.pop("removed")
                    result = plan
                else:
                    backend = "legacy" if args.legacy else "source"
                    try:
                        report = verify_legacy(plan) if args.legacy else verify_source(plan, args.source)
                    except (OSError, ValueError, RuntimeError, BadZipFile, subprocess.SubprocessError) as exc:
                        report = {"status": "FAIL", "error": str(exc)}
                    result = record_execution(db, plan, backend, report)
    except (OSError, ValueError, sqlite3.Error) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(args.command == "execute" and result["status"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
