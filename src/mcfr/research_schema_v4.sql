CREATE TABLE upstream_observation (
    observation_id INTEGER PRIMARY KEY,
    target TEXT NOT NULL,
    game_version TEXT NOT NULL,
    loader TEXT NOT NULL,
    release_json TEXT NOT NULL,
    observed_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
CREATE INDEX upstream_watch_index ON upstream_observation(target, game_version, loader, observation_id);

ALTER TABLE ai_review ADD COLUMN reused_from TEXT REFERENCES ai_review(review_id);
CREATE INDEX ai_review_request_index ON ai_review(approval_sha256, state);
