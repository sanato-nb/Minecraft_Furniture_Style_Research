CREATE TABLE source_job (
    job_id TEXT PRIMARY KEY NOT NULL,
    run_id TEXT NOT NULL REFERENCES research_run(run_id),
    engine_version INTEGER NOT NULL,
    scope_sha256 TEXT NOT NULL,
    source_path TEXT NOT NULL,
    source_kind TEXT NOT NULL CHECK (source_kind IN ('directory', 'archive')),
    total INTEGER NOT NULL CHECK (total >= 0),
    next_asset INTEGER NOT NULL DEFAULT 0 CHECK (next_asset BETWEEN 0 AND total),
    execution_id TEXT UNIQUE REFERENCES research_execution(execution_id)
);

CREATE TABLE source_checkpoint (
    job_id TEXT NOT NULL REFERENCES source_job(job_id),
    position INTEGER NOT NULL,
    result_json TEXT NOT NULL,
    PRIMARY KEY (job_id, position)
);

CREATE TABLE ai_review (
    review_id TEXT PRIMARY KEY NOT NULL,
    execution_id TEXT NOT NULL REFERENCES research_execution(execution_id),
    request_json TEXT NOT NULL,
    approval_sha256 TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'PREPARED'
        CHECK (state IN ('PREPARED', 'DISPATCHING', 'COMPLETE', 'UNCONFIRMED')),
    result_json TEXT
);
