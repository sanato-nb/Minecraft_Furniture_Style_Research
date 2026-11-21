-- INT-3 v1: provenance-first research knowledge, not a training corpus.
-- No original PNG/JAR/model JSON bytes are stored. All source uses require
-- explicit licensing review and later explicit human approval.
PRAGMA foreign_keys=ON;
PRAGMA user_version=1;

CREATE TABLE source_release(
    source_id TEXT PRIMARY KEY,
    version TEXT NOT NULL,
    minecraft_version TEXT NOT NULL,
    origin TEXT NOT NULL,
    pin_kind TEXT NOT NULL,
    pin_digest TEXT NOT NULL,
    asset_hash_kind TEXT NOT NULL,
    license_review TEXT NOT NULL DEFAULT 'NOT_REVIEWED'
        CHECK(license_review IN ('NOT_REVIEWED','REQUIRES_RESTRICTIONS','CLEARED','PROHIBITED')),
    training_approved INTEGER NOT NULL DEFAULT 0 CHECK(training_approved IN (0,1)),
    redistribution_approved INTEGER NOT NULL DEFAULT 0 CHECK(redistribution_approved IN (0,1)),
    CHECK(license_review='CLEARED' OR (training_approved=0 AND redistribution_approved=0))
);
CREATE TABLE evidence_manifest(
    evidence_id TEXT PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    sha256 TEXT NOT NULL,
    audit_status TEXT NOT NULL,
    check_kind TEXT NOT NULL,
    note TEXT NOT NULL
);
CREATE TABLE knowledge_provenance(
    record_family TEXT PRIMARY KEY,
    source_table TEXT NOT NULL,
    identity_rule TEXT NOT NULL,
    audit_evidence_id TEXT NOT NULL REFERENCES evidence_manifest(evidence_id),
    confidence TEXT NOT NULL CHECK(confidence IN (
        'STATIC_ORIGINAL_REPLAY_VERIFIED',
        'PIXEL_SOURCE_REGION_REMEASURED',
        'COMPARISON_SAMPLE_REDERIVED',
        'HISTORIC_RUNTIME_ONLY',
        'UNRESOLVED_EXCEPTION'))
);

CREATE TABLE model(
    model_key TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES source_release(source_id),
    resource_id TEXT NOT NULL,
    source_path TEXT NOT NULL,
    source_sha TEXT NOT NULL,
    model_kind TEXT NOT NULL,
    static_grade TEXT NOT NULL,
    provider_key TEXT REFERENCES model(model_key) DEFERRABLE INITIALLY DEFERRED,
    terminal_status TEXT NOT NULL,
    terminal_resource TEXT NOT NULL,
    effective_elements INTEGER NOT NULL CHECK(effective_elements>=0),
    effective_faces INTEGER NOT NULL CHECK(effective_faces>=0),
    audit_evidence_id TEXT NOT NULL REFERENCES evidence_manifest(evidence_id),
    UNIQUE(source_id,source_path),
    UNIQUE(source_id,resource_id)
);
CREATE INDEX model_provider_idx ON model(provider_key);
CREATE INDEX model_resource_idx ON model(resource_id,source_id);

CREATE TABLE model_parent(
    model_key TEXT NOT NULL REFERENCES model(model_key),
    depth INTEGER NOT NULL CHECK(depth>=0),
    ancestor_key TEXT NOT NULL REFERENCES model(model_key),
    PRIMARY KEY(model_key,depth)
) WITHOUT ROWID;
CREATE TABLE geometry_element(
    provider_key TEXT NOT NULL REFERENCES model(model_key),
    element_index INTEGER NOT NULL,
    source_from TEXT NOT NULL,
    source_to TEXT NOT NULL,
    rotated_bbox TEXT NOT NULL,
    angle REAL NOT NULL,
    axis TEXT NOT NULL,
    part_candidate TEXT NOT NULL,
    part_evidence TEXT NOT NULL,
    PRIMARY KEY(provider_key,element_index)
) WITHOUT ROWID;
CREATE TABLE provider_face(
    provider_key TEXT NOT NULL,
    element_index INTEGER NOT NULL,
    direction TEXT NOT NULL,
    source_slot TEXT NOT NULL,
    declared_uv TEXT NOT NULL,
    uv_declared INTEGER NOT NULL CHECK(uv_declared IN(0,1)),
    uv_rotation INTEGER NOT NULL,
    cullface TEXT NOT NULL,
    tintindex TEXT NOT NULL,
    PRIMARY KEY(provider_key,element_index,direction),
    FOREIGN KEY(provider_key,element_index) REFERENCES geometry_element(provider_key,element_index)
) WITHOUT ROWID;

CREATE TABLE texture(
    texture_id INTEGER PRIMARY KEY,
    resource_id TEXT NOT NULL,
    minecraft_version TEXT NOT NULL,
    source_id TEXT REFERENCES source_release(source_id),
    source_path TEXT,
    source_sha TEXT,
    texture_status TEXT NOT NULL,
    disposition TEXT NOT NULL,
    frame_width INTEGER,
    frame_height INTEGER,
    frame_count INTEGER,
    pixel_evidence TEXT NOT NULL CHECK(pixel_evidence IN (
        'ORIGINAL_PNG_REDECODED','HISTORIC_RGBA_SNAPSHOT',
        'SOURCE_REGION_ONLY','SOURCE_MISSING','DECLARED_ONLY')),
    audit_evidence_id TEXT NOT NULL REFERENCES evidence_manifest(evidence_id),
    UNIQUE(resource_id,minecraft_version),
    CHECK((frame_count IS NULL AND frame_width IS NULL AND frame_height IS NULL) OR
          (frame_count>0 AND frame_width>0 AND frame_height>0))
);
CREATE TABLE model_slot(
    model_key TEXT NOT NULL REFERENCES model(model_key),
    slot TEXT NOT NULL,
    texture_id INTEGER REFERENCES texture(texture_id),
    resolution TEXT NOT NULL,
    face_count INTEGER NOT NULL CHECK(face_count>=0),
    PRIMARY KEY(model_key,slot)
) WITHOUT ROWID;

CREATE TABLE model_face_link(
    model_key TEXT NOT NULL REFERENCES model(model_key),
    provider_key TEXT NOT NULL,
    element_index INTEGER NOT NULL,
    direction TEXT NOT NULL,
    texture_id INTEGER REFERENCES texture(texture_id),
    source_slot TEXT NOT NULL,
    uv TEXT NOT NULL,
    uv_method TEXT NOT NULL CHECK(uv_method IN ('EXPLICIT','DEFAULT')),
    uv_rotation INTEGER NOT NULL,
    cullface TEXT NOT NULL,
    tintindex TEXT NOT NULL,
    source_pixels_per_local_u TEXT,
    source_pixels_per_local_v TEXT,
    face_status TEXT NOT NULL CHECK(face_status IN (
        'STATIC_RECT','ANIMATED_FRAME_RECTS','ZERO_UV_AREA',
        'OUTSIDE_TEXTURE_UV','SLOT_UNBOUND','MISSING_PINNED_PNG')),
    pixel_support TEXT NOT NULL CHECK(pixel_support IN (
        'SOURCE_REGION_REMEASURED',
        'NO_SOURCE_INTERSECTION','SLOT_UNBOUND','SOURCE_PNG_MISSING')),
    PRIMARY KEY(model_key,provider_key,element_index,direction),
    FOREIGN KEY(provider_key,element_index,direction)
        REFERENCES provider_face(provider_key,element_index,direction)
) WITHOUT ROWID;
CREATE INDEX face_texture_idx ON model_face_link(texture_id,face_status);
CREATE INDEX face_model_idx ON model_face_link(model_key,face_status);

CREATE TABLE study_case(
    case_id TEXT PRIMARY KEY,
    cohort TEXT NOT NULL,
    minecraft_version TEXT NOT NULL,
    block TEXT NOT NULL,
    bbox TEXT NOT NULL,
    case_status TEXT NOT NULL DEFAULT 'FIXED_RESEARCH_SAMPLE'
);
CREATE TABLE case_application(
    case_id TEXT NOT NULL REFERENCES study_case(case_id),
    rule_index INTEGER NOT NULL,
    option_index INTEGER NOT NULL,
    model_source_asset_id INTEGER,
    model_key TEXT REFERENCES model(model_key),
    provider_source_asset_id INTEGER,
    provider_key TEXT REFERENCES model(model_key),
    x INTEGER NOT NULL, y INTEGER NOT NULL, uvlock INTEGER NOT NULL,
    source_link_status TEXT NOT NULL CHECK(source_link_status IN ('MODEL_LINKED','UNMATCHED_SCOPE')),
    PRIMARY KEY(case_id,rule_index,option_index)
) WITHOUT ROWID;
CREATE TABLE comparison_finding(
    finding_id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    classification TEXT NOT NULL,
    axis TEXT NOT NULL,
    measurement_json TEXT NOT NULL,
    observation TEXT NOT NULL,
    scope_limit TEXT NOT NULL,
    disposition TEXT NOT NULL CHECK(disposition IN (
        'CANDIDATE_REQUIRES_REVIEW','SCOPE_LIMIT_ONLY')),
    review_condition TEXT NOT NULL,
    audit_evidence_id TEXT NOT NULL REFERENCES evidence_manifest(evidence_id),
    CHECK((classification='UNVERIFIED_OR_COUNTEREXAMPLE' AND disposition='SCOPE_LIMIT_ONLY')
      OR (classification!='UNVERIFIED_OR_COUNTEREXAMPLE' AND disposition='CANDIDATE_REQUIRES_REVIEW'))
);
CREATE TABLE finding_case(
    finding_id TEXT NOT NULL REFERENCES comparison_finding(finding_id),
    case_id TEXT NOT NULL REFERENCES study_case(case_id),
    PRIMARY KEY(finding_id,case_id)
) WITHOUT ROWID;
CREATE TABLE runtime_condition(
    finding_id TEXT NOT NULL REFERENCES comparison_finding(finding_id),
    test_id TEXT NOT NULL,
    verification_status TEXT NOT NULL DEFAULT 'HISTORIC_ONLY_NOT_REEXECUTED',
    PRIMARY KEY(finding_id,test_id)
) WITHOUT ROWID;
CREATE TABLE evidence_exception(
    exception_family TEXT NOT NULL,
    resource_key TEXT NOT NULL,
    finding TEXT NOT NULL,
    impact_count INTEGER,
    source_table TEXT NOT NULL,
    PRIMARY KEY(exception_family,resource_key)
);

-- A conservative view: no data is training-approved by audit alone.
CREATE VIEW ai_training_eligible_model AS
 SELECT m.model_key,m.resource_id,m.source_id,m.source_path,m.static_grade
 FROM model m JOIN source_release s ON s.source_id=m.source_id
 WHERE s.license_review='CLEARED' AND s.training_approved=1
 AND m.effective_faces>0 AND m.terminal_status NOT IN ('PARENT_MISSING','PARENT_CYCLE')
 AND NOT EXISTS (
   SELECT 1 FROM model_face_link f
   WHERE f.model_key=m.model_key
     AND f.pixel_support IN ('NO_SOURCE_INTERSECTION','SLOT_UNBOUND','SOURCE_PNG_MISSING')
 );

CREATE VIEW candidate_finding AS
 SELECT finding_id,category,classification,axis,observation,scope_limit,review_condition
 FROM comparison_finding
 WHERE disposition='CANDIDATE_REQUIRES_REVIEW';
