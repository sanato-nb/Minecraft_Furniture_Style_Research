PRAGMA foreign_keys=ON;
PRAGMA user_version=1;

CREATE TABLE source_artifact(
    path TEXT PRIMARY KEY, baseline_commit TEXT NOT NULL, git_blob_sha1 TEXT NOT NULL,
    sha256 TEXT NOT NULL, bytes INTEGER NOT NULL CHECK(bytes>0)
);
CREATE TABLE asset(
    asset_id INTEGER PRIMARY KEY, source_scope TEXT NOT NULL, minecraft TEXT NOT NULL,
    path TEXT NOT NULL, kind TEXT NOT NULL, UNIQUE(source_scope,minecraft,path)
);
CREATE TABLE asset_hash(
    asset_id INTEGER NOT NULL REFERENCES asset, algorithm TEXT NOT NULL, digest TEXT NOT NULL,
    PRIMARY KEY(asset_id,algorithm)
) WITHOUT ROWID;
CREATE TABLE category(category TEXT PRIMARY KEY);
CREATE TABLE study_case(
    case_id TEXT PRIMARY KEY, cohort TEXT NOT NULL, minecraft TEXT NOT NULL, mod_version TEXT,
    block TEXT NOT NULL, applications INTEGER NOT NULL, elements INTEGER NOT NULL, faces INTEGER NOT NULL,
    bbox TEXT NOT NULL, span_blocks TEXT NOT NULL, zero_thickness_elements INTEGER NOT NULL,
    min_positive_local_thickness_blocks TEXT NOT NULL, default_uv_faces INTEGER NOT NULL,
    explicit_uv_faces INTEGER NOT NULL, uvlock_declared_faces INTEGER NOT NULL, status_counts TEXT NOT NULL,
    faces_measured INTEGER NOT NULL, faces_with_first_frame_alpha_zero INTEGER NOT NULL,
    faces_with_first_frame_alpha_partial INTEGER NOT NULL, density_axis_median TEXT NOT NULL,
    faces_at_density_1x1 INTEGER NOT NULL
);
CREATE TABLE case_category(
    case_id TEXT NOT NULL REFERENCES study_case, category TEXT NOT NULL REFERENCES category,
    PRIMARY KEY(case_id,category)
) WITHOUT ROWID;
CREATE TABLE application(
    case_id TEXT NOT NULL REFERENCES study_case, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
    state TEXT NOT NULL, model TEXT NOT NULL, provider TEXT NOT NULL,
    x INTEGER NOT NULL,y INTEGER NOT NULL,uvlock INTEGER NOT NULL CHECK(uvlock IN(0,1)),
    weight INTEGER NOT NULL, geometry_status TEXT NOT NULL, elements INTEGER NOT NULL, faces INTEGER NOT NULL,
    zero_thickness_elements INTEGER NOT NULL, assembly_bbox TEXT NOT NULL, span_blocks TEXT NOT NULL,
    PRIMARY KEY(case_id,rule_index,option_index)
) WITHOUT ROWID;
CREATE TABLE application_source(
    case_id TEXT NOT NULL, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
    role TEXT NOT NULL CHECK(role IN('state','model','provider')), asset_id INTEGER NOT NULL REFERENCES asset,
    PRIMARY KEY(case_id,rule_index,option_index,role),
    FOREIGN KEY(case_id,rule_index,option_index) REFERENCES application
) WITHOUT ROWID;
CREATE TABLE element(
    case_id TEXT NOT NULL, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL, element_index INTEGER NOT NULL,
    local_size TEXT NOT NULL,zero_axes TEXT NOT NULL,assembly_bbox TEXT NOT NULL,faces INTEGER NOT NULL,
    PRIMARY KEY(case_id,rule_index,option_index,element_index),
    FOREIGN KEY(case_id,rule_index,option_index) REFERENCES application
) WITHOUT ROWID;
CREATE TABLE face(
    case_id TEXT NOT NULL, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
    element_index INTEGER NOT NULL, direction TEXT NOT NULL, slot TEXT NOT NULL, resource_id TEXT NOT NULL,
    png_asset_id INTEGER NOT NULL REFERENCES asset, sheet_width INTEGER NOT NULL,sheet_height INTEGER NOT NULL,
    frame_width INTEGER NOT NULL,frame_height INTEGER NOT NULL,png_frames INTEGER NOT NULL,
    uv TEXT NOT NULL,uv_method TEXT NOT NULL,uv_rotation INTEGER NOT NULL,cullface TEXT NOT NULL,tintindex INTEGER,
    density_u TEXT NOT NULL,density_v TEXT NOT NULL,status TEXT NOT NULL,pixel_box TEXT NOT NULL,
    pixels INTEGER,alpha_zero INTEGER,alpha_partial INTEGER,visible_rgb INTEGER,
    visible_luma_mean TEXT NOT NULL,visible_luma_stddev TEXT NOT NULL,visible_luma_span TEXT NOT NULL,
    top_rgb TEXT NOT NULL,rgba_sha256 TEXT NOT NULL,
    PRIMARY KEY(case_id,rule_index,option_index,element_index,direction),
    FOREIGN KEY(case_id,rule_index,option_index,element_index) REFERENCES element,
    CHECK(pixels IS NULL OR alpha_zero+alpha_partial<=pixels)
) WITHOUT ROWID;
CREATE TABLE face_frame(
    case_id TEXT NOT NULL, rule_index INTEGER NOT NULL, option_index INTEGER NOT NULL,
    element_index INTEGER NOT NULL, direction TEXT NOT NULL, frame INTEGER NOT NULL,
    pixel_box TEXT NOT NULL,pixels INTEGER NOT NULL,alpha_zero INTEGER NOT NULL,alpha_partial INTEGER NOT NULL,
    visible_rgb INTEGER NOT NULL,visible_luma_mean TEXT NOT NULL,visible_luma_stddev TEXT NOT NULL,
    visible_luma_span TEXT NOT NULL,top_rgb TEXT NOT NULL,rgba_sha256 TEXT NOT NULL,
    PRIMARY KEY(case_id,rule_index,option_index,element_index,direction,frame),
    FOREIGN KEY(case_id,rule_index,option_index,element_index,direction) REFERENCES face,
    CHECK(alpha_zero+alpha_partial<=pixels)
) WITHOUT ROWID;
CREATE TABLE control_asset(
    case_id TEXT NOT NULL REFERENCES study_case,asset_id INTEGER NOT NULL REFERENCES asset,
    PRIMARY KEY(case_id,asset_id)
) WITHOUT ROWID;
CREATE TABLE finding(
    finding_id TEXT PRIMARY KEY,category TEXT NOT NULL REFERENCES category,
    classification TEXT NOT NULL CHECK(classification IN
       ('VANILLA_SHARED','MULTI_MOD_SHARED','MOD_SPECIFIC','UNVERIFIED_OR_COUNTEREXAMPLE')),
    axis TEXT NOT NULL,measurement TEXT NOT NULL,observation TEXT NOT NULL,scope_limit TEXT NOT NULL
);
CREATE TABLE finding_case(
    finding_id TEXT NOT NULL REFERENCES finding,case_id TEXT NOT NULL REFERENCES study_case,
    PRIMARY KEY(finding_id,case_id)
) WITHOUT ROWID;
CREATE TABLE parent_exception(
    model_key TEXT PRIMARY KEY,mod TEXT NOT NULL,model_resource TEXT NOT NULL,model_path TEXT NOT NULL,
    model_sha TEXT NOT NULL,declared_parent TEXT NOT NULL,raw_parent TEXT NOT NULL,missing_exact_path TEXT NOT NULL,
    alternate_path_hint TEXT NOT NULL,direct_state_option INTEGER NOT NULL,state_lineage INTEGER NOT NULL,
    sample_lineage INTEGER NOT NULL
);
CREATE TABLE state_exception(
    state_id TEXT NOT NULL,rule_index INTEGER NOT NULL,option_index INTEGER NOT NULL,case_id TEXT REFERENCES study_case,
    state_path TEXT NOT NULL,state_sha TEXT NOT NULL,selector TEXT NOT NULL,
    model_ref TEXT NOT NULL,model_key TEXT NOT NULL,finding TEXT NOT NULL,
    PRIMARY KEY(state_id,rule_index,option_index)
) WITHOUT ROWID;
CREATE TABLE texture_exception(
    texture_id INTEGER PRIMARY KEY,resource_id TEXT NOT NULL,minecraft TEXT NOT NULL,finding TEXT NOT NULL,
    model_slots INTEGER NOT NULL,particle_slots INTEGER NOT NULL,face_instances INTEGER NOT NULL,
    blockstate_option_face_instances INTEGER NOT NULL,models_with_direct_state_option INTEGER NOT NULL,
    item_model_faces INTEGER NOT NULL,sampled_model_face INTEGER NOT NULL,other_version_sample_faces INTEGER NOT NULL,
    UNIQUE(resource_id,minecraft)
);
CREATE TABLE runtime_check(
    test_id TEXT PRIMARY KEY,axis TEXT NOT NULL,cases_or_scope TEXT NOT NULL,
    source_basis TEXT NOT NULL,setup TEXT NOT NULL,observation_required TEXT NOT NULL,status TEXT NOT NULL
);
CREATE TABLE runtime_case(
    test_id TEXT NOT NULL REFERENCES runtime_check,case_id TEXT NOT NULL REFERENCES study_case,
    PRIMARY KEY(test_id,case_id)
) WITHOUT ROWID;
CREATE TABLE phase2_handoff(
    finding_id TEXT PRIMARY KEY REFERENCES finding, disposition TEXT NOT NULL CHECK(disposition IN
       ('CANDIDATE_REQUIRES_REVIEW','SCOPE_LIMIT_ONLY')),
    review_condition TEXT NOT NULL
);
CREATE TABLE handoff_runtime(
    finding_id TEXT NOT NULL REFERENCES phase2_handoff,test_id TEXT NOT NULL REFERENCES runtime_check,
    PRIMARY KEY(finding_id,test_id)
) WITHOUT ROWID;
CREATE TABLE phase_gate(
    gate_id TEXT PRIMARY KEY,status TEXT NOT NULL,source_path TEXT NOT NULL,note TEXT NOT NULL
);
