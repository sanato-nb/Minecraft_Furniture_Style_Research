PRAGMA foreign_keys = ON;
CREATE TABLE source(
 id TEXT PRIMARY KEY, version TEXT NOT NULL, minecraft TEXT NOT NULL,
 pin TEXT NOT NULL, pin_kind TEXT NOT NULL, asset_hash_kind TEXT NOT NULL, origin TEXT NOT NULL
) WITHOUT ROWID;
CREATE TABLE model(
 model_key TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES source,
 resource_id TEXT NOT NULL, path TEXT NOT NULL, sha TEXT NOT NULL,
 kind TEXT NOT NULL, entry_id TEXT, static_grade TEXT NOT NULL,
 UNIQUE(source_id,path), UNIQUE(source_id,resource_id)
) WITHOUT ROWID;
CREATE TABLE lineage(
 model_key TEXT NOT NULL REFERENCES model, position INTEGER NOT NULL,
 ancestor_key TEXT NOT NULL REFERENCES model, PRIMARY KEY(model_key,position)
) WITHOUT ROWID;
CREATE TABLE geometry(
 model_key TEXT PRIMARY KEY REFERENCES model, provider_key TEXT REFERENCES model,
 terminal_status TEXT NOT NULL, terminal_resource TEXT NOT NULL,
 element_instances INTEGER NOT NULL, face_instances INTEGER NOT NULL
) WITHOUT ROWID;
CREATE TABLE element(
 provider_key TEXT NOT NULL REFERENCES model, element_index INTEGER NOT NULL,
 source_from TEXT NOT NULL, source_to TEXT NOT NULL, pivot TEXT NOT NULL,
 axis TEXT NOT NULL, angle REAL NOT NULL, rescale INTEGER NOT NULL, rotated_bbox TEXT NOT NULL,
 part_candidate TEXT NOT NULL, part_evidence TEXT NOT NULL,
 PRIMARY KEY(provider_key,element_index)
) WITHOUT ROWID;
CREATE TABLE face(
 provider_key TEXT NOT NULL, element_index INTEGER NOT NULL, direction TEXT NOT NULL,
 slot TEXT NOT NULL, uv TEXT NOT NULL, uv_declared INTEGER NOT NULL,
 uv_rotation INTEGER NOT NULL, cullface TEXT NOT NULL, tintindex TEXT NOT NULL,
 PRIMARY KEY(provider_key,element_index,direction),
 FOREIGN KEY(provider_key,element_index) REFERENCES element
) WITHOUT ROWID;
CREATE TABLE texture(
 id INTEGER PRIMARY KEY, resource_id TEXT NOT NULL, minecraft TEXT NOT NULL,
 source_id TEXT REFERENCES source, texture_status TEXT NOT NULL, path TEXT, sha TEXT,
 UNIQUE(resource_id,minecraft)
);
CREATE TABLE model_slot(
 model_key TEXT NOT NULL REFERENCES model, slot TEXT NOT NULL, texture_id INTEGER REFERENCES texture,
 resolution TEXT NOT NULL, face_count INTEGER NOT NULL CHECK(face_count>=0),
 PRIMARY KEY(model_key,slot)
) WITHOUT ROWID;
CREATE TABLE state(
 id INTEGER PRIMARY KEY, source_id TEXT NOT NULL REFERENCES source, state_id TEXT NOT NULL,
 path TEXT NOT NULL, sha TEXT NOT NULL, kind TEXT NOT NULL, evidence_id TEXT, connection_class TEXT NOT NULL,
 UNIQUE(source_id,state_id), UNIQUE(source_id,path)
);
CREATE TABLE rule(
 state_id INTEGER NOT NULL REFERENCES state, rule_index INTEGER NOT NULL,
 selector TEXT NOT NULL, condition TEXT NOT NULL, form TEXT NOT NULL,
 PRIMARY KEY(state_id,rule_index)
) WITHOUT ROWID;
CREATE TABLE option(
 state_id INTEGER NOT NULL, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
 model_key TEXT REFERENCES model, target_status TEXT NOT NULL, unresolved_target TEXT,
 x INTEGER NOT NULL, y INTEGER NOT NULL, uvlock INTEGER NOT NULL, weight INTEGER NOT NULL,
 explicit_fields TEXT NOT NULL,
 CHECK ((model_key IS NULL) = (unresolved_target IS NOT NULL)),
 PRIMARY KEY(state_id,rule_index,option_index),
 FOREIGN KEY(state_id,rule_index) REFERENCES rule
) WITHOUT ROWID;
CREATE TABLE sample(
 id TEXT PRIMARY KEY, category TEXT NOT NULL, state_id INTEGER NOT NULL REFERENCES state,
 assignment TEXT NOT NULL, bbox TEXT NOT NULL, front_fill REAL NOT NULL,
 side_fill REAL NOT NULL, top_fill REAL NOT NULL,
 UNIQUE(id,state_id)
) WITHOUT ROWID;
CREATE TABLE sample_option(
 sample_id TEXT NOT NULL, state_id INTEGER NOT NULL,
 rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
 PRIMARY KEY(sample_id,rule_index,option_index),
 FOREIGN KEY(sample_id,state_id) REFERENCES sample(id,state_id),
 FOREIGN KEY(state_id,rule_index,option_index) REFERENCES option
) WITHOUT ROWID;
CREATE TABLE sample_part(
 sample_id TEXT NOT NULL REFERENCES sample, rule_index INTEGER NOT NULL, provider_key TEXT NOT NULL,
 element_index INTEGER NOT NULL, part_candidate TEXT NOT NULL, basis TEXT NOT NULL,
 PRIMARY KEY(sample_id,rule_index,element_index),
 FOREIGN KEY(provider_key,element_index) REFERENCES element
) WITHOUT ROWID;
CREATE TABLE prior_texture(
 texture_id INTEGER PRIMARY KEY REFERENCES texture, ledger TEXT NOT NULL,
 ledger_blob_sha TEXT NOT NULL, ledger_line INTEGER NOT NULL, prior_sha TEXT NOT NULL
);
CREATE VIEW effective_face_texture AS
 SELECT g.model_key, f.provider_key, f.element_index, f.direction, f.uv,
        f.uv_declared, f.uv_rotation, f.slot, s.texture_id, s.resolution
 FROM geometry g JOIN face f ON f.provider_key=g.provider_key
 JOIN model_slot s ON s.model_key=g.model_key AND s.slot=f.slot;
CREATE TABLE exception(
 stage TEXT NOT NULL, resource_key TEXT NOT NULL, category TEXT NOT NULL,
 detail TEXT NOT NULL, PRIMARY KEY(stage,resource_key,category,detail)
) WITHOUT ROWID;
