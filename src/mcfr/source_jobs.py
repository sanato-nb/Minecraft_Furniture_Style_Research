"""Persist source verification in bounded SQLite checkpoints."""

import json
from pathlib import Path

from . import research_db as catalog, research_engine as engine

BATCH_SIZE = 64


def status(db, job_id):
    row = db.execute("SELECT * FROM source_job WHERE job_id = ?", (job_id,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown source job: {job_id}")
    record = dict(row)
    if record["execution_id"] is None:
        record["status"] = "PENDING"
    else:
        record["status"] = db.execute(
            "SELECT status FROM research_execution WHERE execution_id = ?", (record["execution_id"],),
        ).fetchone()[0]
    return record


def scan(db, job_id: str, run_id: str, source: Path, limit: int | None = None) -> dict:
    catalog.nonempty(job_id)
    if limit is not None and limit < 1:
        raise ValueError("Asset allowance must be positive")
    source = source.resolve()
    source_kind = "directory" if source.is_dir() else "archive"
    with catalog.write_transaction(db):
        plan = engine.plan_run(db, run_id)
        selected = plan["selected"]
        fields = ("job_id", "run_id", "engine_version", "scope_sha256", "source_path", "source_kind", "total")
        identity = (job_id, run_id, engine.ENGINE_VERSION, plan["scope_sha256"], str(source), source_kind, len(selected))
        db.execute(
            f"INSERT INTO source_job ({', '.join(fields)}) VALUES (?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(job_id) DO NOTHING", identity,
        )
        job = status(db, job_id)
        if tuple(job[field] for field in fields) != identity:
            raise ValueError("Job differs from its saved scope, source or engine version")
    if job["execution_id"] is not None:
        return job

    with engine.source_reader(source, plan["release"]) as (read, pin_check):
        while limit is None or limit > 0:
            with catalog.write_transaction(db):
                job = status(db, job_id)
                if job["execution_id"] is not None:
                    break
                start = job["next_asset"]
                count = min(BATCH_SIZE, len(selected) - start)
                if limit is not None:
                    count = min(count, limit)
                    limit -= count

                results = [
                    (job_id, position, engine._json(engine.verify_entry(entry, read)))
                    for position, entry in enumerate(selected[start:start + count], start=start)
                ]
                db.executemany("INSERT INTO source_checkpoint VALUES (?, ?, ?)", results)
                end = start + count
                db.execute("UPDATE source_job SET next_asset = ? WHERE job_id = ?", (end, job_id))
                if end == len(selected):
                    assets = [json.loads(row[0]) for row in db.execute(
                        "SELECT result_json FROM source_checkpoint WHERE job_id = ? ORDER BY position", (job_id,),
                    )]
                    report = engine.source_report(plan, assets, pin_check)
                    execution_id = engine.insert_execution(db, plan, "source", report)
                    db.execute("UPDATE source_job SET execution_id = ? WHERE job_id = ?", (execution_id, job_id))
                    db.execute("DELETE FROM source_checkpoint WHERE job_id = ?", (job_id,))
                    break
    return status(db, job_id)
