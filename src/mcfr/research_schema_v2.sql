CREATE TABLE research_execution (
    execution_id TEXT PRIMARY KEY NOT NULL,
    run_id TEXT NOT NULL REFERENCES research_run(run_id),
    engine_version INTEGER NOT NULL,
    backend TEXT NOT NULL CHECK (backend IN ('source', 'legacy')),
    scope_sha256 TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PASS', 'FAIL')),
    report_json TEXT NOT NULL,
    finished_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
CREATE INDEX research_execution_run_index ON research_execution(run_id, finished_at, execution_id);
