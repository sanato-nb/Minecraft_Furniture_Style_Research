PRAGMA foreign_keys=ON;
CREATE TABLE input_artifact(path TEXT PRIMARY KEY, sha256 TEXT NOT NULL);
CREATE TABLE texture(
    id INTEGER PRIMARY KEY, resource_id TEXT NOT NULL, minecraft TEXT NOT NULL,
    source_id TEXT, path TEXT, sha TEXT, hash_kind TEXT, disposition TEXT NOT NULL,
    UNIQUE(resource_id,minecraft)
);
CREATE TABLE texture_uv_counts(
    texture_id INTEGER PRIMARY KEY REFERENCES texture(id),
    frame_width INTEGER NOT NULL, frame_height INTEGER NOT NULL, frame_count INTEGER NOT NULL,
    regions INTEGER NOT NULL, static_faces INTEGER NOT NULL, animated_faces INTEGER NOT NULL,
    zero_uv_faces INTEGER NOT NULL, outside_uv_faces INTEGER NOT NULL
);
CREATE TABLE texture_exception(
    texture_id INTEGER PRIMARY KEY REFERENCES texture(id), finding TEXT NOT NULL,
    model_slots INTEGER NOT NULL, particle_slots INTEGER NOT NULL, face_instances INTEGER NOT NULL,
    blockstate_option_faces INTEGER NOT NULL, blockstate_models INTEGER NOT NULL,
    item_model_faces INTEGER NOT NULL
);
CREATE TABLE exception_slot(
    texture_id INTEGER NOT NULL REFERENCES texture_exception(texture_id),
    model_key TEXT NOT NULL, model_resource TEXT NOT NULL, model_path TEXT NOT NULL,
    model_sha TEXT NOT NULL, slot TEXT NOT NULL, face_instances INTEGER NOT NULL,
    blockstate_options INTEGER NOT NULL,
    PRIMARY KEY(texture_id,model_key,slot)
);
CREATE TABLE alternate_asset(
    texture_id INTEGER NOT NULL REFERENCES texture_exception(texture_id), path TEXT NOT NULL,
    sha TEXT NOT NULL, rationale TEXT NOT NULL, PRIMARY KEY(texture_id,path)
);
CREATE TABLE prior_face(
    ledger_path TEXT NOT NULL REFERENCES input_artifact(path), ledger_row INTEGER NOT NULL,
    finding TEXT NOT NULL, model_key TEXT, provider_key TEXT, element_index INTEGER,
    direction TEXT, texture_id INTEGER REFERENCES texture(id), uv TEXT,
    entry02_rgba_sha256 TEXT, PRIMARY KEY(ledger_path,ledger_row)
);
CREATE TABLE comparison_application(
    case_id TEXT NOT NULL, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
    category TEXT NOT NULL, mod TEXT NOT NULL, state_id TEXT NOT NULL, state_sha TEXT NOT NULL,
    model_key TEXT NOT NULL, model_sha TEXT NOT NULL, provider_key TEXT NOT NULL,
    provider_sha TEXT NOT NULL, x INTEGER NOT NULL, y INTEGER NOT NULL, uvlock INTEGER NOT NULL,
    PRIMARY KEY(case_id,rule_index,option_index)
);
CREATE TABLE comparison_face(
    case_id TEXT NOT NULL, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
    element_index INTEGER NOT NULL, direction TEXT NOT NULL, texture_id INTEGER REFERENCES texture(id),
    uv TEXT NOT NULL, status TEXT NOT NULL, frames INTEGER NOT NULL, density_u TEXT, density_v TEXT,
    frame0_rgba_sha256 TEXT,
    PRIMARY KEY(case_id,rule_index,option_index,element_index,direction),
    FOREIGN KEY(case_id,rule_index,option_index) REFERENCES comparison_application
);
