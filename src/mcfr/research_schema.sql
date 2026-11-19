CREATE TABLE release (
    release_key TEXT PRIMARY KEY NOT NULL,
    profile TEXT NOT NULL CHECK (profile IN ('vanilla', 'mods')),
    target_id TEXT NOT NULL,
    version TEXT NOT NULL,
    minecraft_version TEXT NOT NULL,
    loader TEXT NOT NULL,
    pin_algorithm TEXT NOT NULL CHECK (pin_algorithm IN ('GIT_COMMIT_SHA1', 'SHA1', 'SHA256')),
    pin_digest TEXT NOT NULL CHECK (
        pin_digest NOT GLOB '*[^0-9a-f]*' AND
        length(pin_digest) = CASE pin_algorithm WHEN 'SHA256' THEN 64 ELSE 40 END
    ),
    source TEXT NOT NULL,
    UNIQUE (profile, target_id, version, minecraft_version, loader, pin_algorithm, pin_digest)
);

CREATE TABLE asset (
    release_key TEXT NOT NULL REFERENCES release(release_key),
    source_path TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('model', 'blockstate', 'texture', 'texture_sidecar', 'item_definition')),
    resource_id TEXT NOT NULL,
    hash_algorithm TEXT NOT NULL CHECK (hash_algorithm IN ('GIT_BLOB_SHA1', 'SHA1', 'SHA256')),
    digest TEXT NOT NULL CHECK (
        digest NOT GLOB '*[^0-9a-f]*' AND
        length(digest) = CASE hash_algorithm WHEN 'SHA256' THEN 64 ELSE 40 END
    ),
    byte_count INTEGER CHECK (byte_count IS NULL OR byte_count >= 0),
    evidence_path TEXT,
    PRIMARY KEY (release_key, source_path)
);
CREATE INDEX asset_kind_index ON asset(release_key, kind, source_path);

CREATE TABLE research_run (
    run_id TEXT PRIMARY KEY NOT NULL,
    release_key TEXT NOT NULL REFERENCES release(release_key),
    mode TEXT NOT NULL CHECK (mode IN ('NEW', 'INCREMENTAL', 'REVALIDATE', 'FRESH')),
    baseline_release_key TEXT REFERENCES release(release_key),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    CHECK (
        (mode = 'INCREMENTAL' AND baseline_release_key IS NOT NULL AND baseline_release_key <> release_key)
        OR (mode <> 'INCREMENTAL' AND baseline_release_key IS NULL)
    )
);
CREATE INDEX research_run_release_index ON research_run(release_key, created_at);
