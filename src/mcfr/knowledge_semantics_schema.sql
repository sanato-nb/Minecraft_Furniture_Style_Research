-- INT-3 semantics v1 is deliberately evidence-conservative.
-- Original C geometric classes are facts about measured shape, not furniture
-- functions. The 45 chair-role labels are candidates, not visual approvals.
PRAGMA foreign_keys=ON;

CREATE TABLE semantic_geometry (
 provider_key TEXT NOT NULL,
 element_index INTEGER NOT NULL,
 source_geometry_type TEXT NOT NULL,
 source_size TEXT NOT NULL,
 source_center TEXT NOT NULL,
 source_texture_slots TEXT NOT NULL,
 primitive_zero_axes TEXT NOT NULL,
 primitive_reversed_axes TEXT NOT NULL,
 local_volume_model_units3 TEXT NOT NULL,
 original_role_candidate TEXT NOT NULL,
 original_role_evidence TEXT NOT NULL,
 evidence_source TEXT NOT NULL DEFAULT '1-3-C/PARTS.csv.gz',
 evidence_grade TEXT NOT NULL CHECK(evidence_grade IN ('MEASURED_GEOMETRY','ROLE_CANDIDATE_GEOMETRY_AND_SLOTS')),
 PRIMARY KEY(provider_key,element_index),
 FOREIGN KEY(provider_key,element_index) REFERENCES geometry_element(provider_key,element_index)
) WITHOUT ROWID;

CREATE TABLE part_role_candidate (
 provider_key TEXT NOT NULL,
 element_index INTEGER NOT NULL,
 role_label TEXT NOT NULL,
 role_basis TEXT NOT NULL,
 source_model_key TEXT NOT NULL REFERENCES model(model_key),
 source_model_sha TEXT NOT NULL,
 claim_status TEXT NOT NULL DEFAULT 'HYPOTHESIS_NEEDS_VISUAL_CONFIRMATION'
   CHECK(claim_status='HYPOTHESIS_NEEDS_VISUAL_CONFIRMATION'),
 source_artifact TEXT NOT NULL DEFAULT 'research/furniture_mods/phase_1-3/C/PARTS.csv.gz',
 PRIMARY KEY(provider_key,element_index),
 FOREIGN KEY(provider_key,element_index) REFERENCES semantic_geometry(provider_key,element_index),
 CHECK(role_label!='UNDETERMINED')
) WITHOUT ROWID;

CREATE TABLE historical_sample (
 sample_id TEXT PRIMARY KEY,
 scope TEXT NOT NULL,
 state_id INTEGER NOT NULL,
 assignment TEXT NOT NULL,
 bbox TEXT NOT NULL,
 original_source TEXT NOT NULL DEFAULT '1-3-E via 1-3-F.sample'
);
CREATE TABLE sample_part_candidate (
 sample_id TEXT NOT NULL REFERENCES historical_sample(sample_id),
 rule_index INTEGER NOT NULL,
 provider_key TEXT NOT NULL,
 element_index INTEGER NOT NULL,
 role_label TEXT NOT NULL,
 basis TEXT NOT NULL,
 claim_status TEXT NOT NULL DEFAULT 'SAMPLE_SPECIFIC_CANDIDATE_NOT_VISUALLY_CONFIRMED'
   CHECK(claim_status='SAMPLE_SPECIFIC_CANDIDATE_NOT_VISUALLY_CONFIRMED'),
 PRIMARY KEY(sample_id,rule_index,provider_key,element_index),
 FOREIGN KEY(provider_key,element_index) REFERENCES semantic_geometry(provider_key,element_index)
) WITHOUT ROWID;

CREATE TABLE semantic_review_queue (
 queue_id TEXT PRIMARY KEY,
 review_kind TEXT NOT NULL CHECK(review_kind IN ('ELEMENT_ROLE_VISUAL','FINDING_SCOPE_CONFIRMATION')),
 provider_key TEXT,
 element_index INTEGER,
 finding_id TEXT REFERENCES comparison_finding(finding_id),
 request TEXT NOT NULL,
 state TEXT NOT NULL DEFAULT 'PENDING' CHECK(state IN ('PENDING','IN_REVIEW','REVIEWED_WITH_EVIDENCE','REJECTED_WITH_EVIDENCE')),
 evidence_source TEXT NOT NULL,
 CHECK(
   (review_kind='ELEMENT_ROLE_VISUAL' AND provider_key IS NOT NULL AND element_index IS NOT NULL AND finding_id IS NULL)
   OR
   (review_kind='FINDING_SCOPE_CONFIRMATION' AND provider_key IS NULL AND element_index IS NULL AND finding_id IS NOT NULL)
 ),
 FOREIGN KEY(provider_key,element_index) REFERENCES semantic_geometry(provider_key,element_index)
);

-- Empty by default; MATERIAL / STYLE labels must be supported by explicitly
-- reviewed original renders or other directly inspected source evidence.
CREATE TABLE verified_material_style (
 assertion_id TEXT PRIMARY KEY,
 target_kind TEXT NOT NULL CHECK(target_kind IN ('MODEL','ELEMENT','TEXTURE','CASE')),
 target_key TEXT NOT NULL,
 predicate TEXT NOT NULL CHECK(predicate IN ('MATERIAL','STYLE','FUNCTION')),
 value TEXT NOT NULL,
 verification_status TEXT NOT NULL CHECK(verification_status IN ('VISUAL_VERIFIED','RUNTIME_VERIFIED')),
 evidence_reference TEXT NOT NULL CHECK(length(trim(evidence_reference))>0),
 verification_method TEXT NOT NULL,
 notes TEXT NOT NULL
);

CREATE VIEW ai_approved_semantic_part AS
 SELECT p.provider_key,p.element_index,p.role_label
 FROM part_role_candidate p
 JOIN semantic_review_queue q ON q.queue_id='ROLE:'||p.provider_key||':'||p.element_index
 WHERE q.state='REVIEWED_WITH_EVIDENCE'
 AND EXISTS (
     SELECT 1 FROM verified_material_style s
     WHERE s.target_kind='ELEMENT'
       AND s.target_key=p.provider_key||':'||p.element_index
       AND s.predicate='FUNCTION' AND s.value=p.role_label
 );

CREATE VIEW candidate_role_review AS
 SELECT m.source_id,m.resource_id,m.source_path,m.source_sha,
        p.provider_key,p.element_index,p.role_label,p.role_basis,
        g.source_geometry_type,g.source_size,g.primitive_zero_axes,
        q.state
 FROM part_role_candidate p
 JOIN model m ON m.model_key=p.source_model_key
 JOIN semantic_geometry g USING(provider_key,element_index)
 JOIN semantic_review_queue q ON q.queue_id='ROLE:'||p.provider_key||':'||p.element_index;
