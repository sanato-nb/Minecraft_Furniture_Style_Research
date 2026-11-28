-- DBD-001 DESIGN PROPOSAL ONLY. Apply only to disposable v4 copy.
-- Existing eight tables and PRAGMA user_version remain unchanged.

-- 해시로 고정된 원본/파생 근거와 보존 위치
CREATE TABLE evidence_item (
    evidence_id TEXT PRIMARY KEY,
    content_sha256 TEXT NOT NULL CHECK(length(content_sha256)=64 AND content_sha256 NOT GLOB '*[^0-9a-f]*'),
    byte_count INTEGER NOT NULL CHECK(byte_count>=0),
    locator TEXT NOT NULL,
    member_locator TEXT NOT NULL DEFAULT '',
    storage_kind TEXT NOT NULL CHECK(storage_kind IN ('GIT','ARTIFACT','LOCAL_ARCHIVE','EXTERNAL_PIN')),
    git_commit TEXT,
    run_id_external TEXT,
    job_id_external TEXT,
    artifact_id TEXT,
    retention_state TEXT NOT NULL CHECK(retention_state IN ('VERIFIED_AVAILABLE','UNVERIFIED','EXPIRED','MISSING','RESTRICTED')),
    verified_at TEXT,
    rights_state TEXT NOT NULL CHECK(rights_state IN ('ALLOWED','RESTRICTED','UNKNOWN')),
    origin_kind TEXT NOT NULL CHECK(origin_kind IN ('SOURCE','DERIVED')),
    CHECK(retention_state<>'VERIFIED_AVAILABLE' OR verified_at IS NOT NULL),
    CHECK(storage_kind<>'GIT' OR git_commit IS NOT NULL),
    CHECK(storage_kind<>'ARTIFACT' OR (run_id_external IS NOT NULL AND artifact_id IS NOT NULL)),
    UNIQUE(content_sha256,locator,member_locator)
) STRICT;

-- 릴리스의 획득·라이선스 근거 이력
CREATE TABLE release_provenance (
    provenance_id TEXT PRIMARY KEY,
    release_key TEXT NOT NULL REFERENCES release,
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    origin_url TEXT NOT NULL,
    acquired_at TEXT NOT NULL,
    license_id TEXT,
    rights_state TEXT NOT NULL CHECK(rights_state IN ('ALLOWED','RESTRICTED','UNKNOWN')),
    notes TEXT NOT NULL
) STRICT;

-- 기존 등록 해시 외 알고리즘별 확인값
CREATE TABLE asset_hash (
    release_key TEXT NOT NULL,
    source_path TEXT NOT NULL,
    algorithm TEXT NOT NULL CHECK(algorithm IN ('GIT_BLOB_SHA1','SHA1','SHA256','SHA512')),
    digest TEXT NOT NULL CHECK(digest NOT GLOB '*[^0-9a-f]*' AND length(digest)=CASE algorithm WHEN 'SHA256' THEN 64 WHEN 'SHA512' THEN 128 ELSE 40 END),
    byte_count INTEGER NOT NULL CHECK(byte_count>=0),
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    PRIMARY KEY(release_key,source_path,algorithm),
    FOREIGN KEY(release_key,source_path) REFERENCES asset(release_key,source_path)
) STRICT;

-- 기존 asset 종류 밖 실제 원본만; 가짜 누락 파일 금지
CREATE TABLE unregistered_source (
    release_key TEXT NOT NULL REFERENCES release,
    source_path TEXT NOT NULL,
    format TEXT NOT NULL,
    content_sha256 TEXT NOT NULL CHECK(length(content_sha256)=64 AND content_sha256 NOT GLOB '*[^0-9a-f]*'),
    byte_count INTEGER NOT NULL CHECK(byte_count>=0),
    support_state TEXT NOT NULL CHECK(support_state IN ('UNSUPPORTED','UNREVIEWED','EXCLUDED')),
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    PRIMARY KEY(release_key,source_path)
) STRICT;

-- C1/C2/C3 범위와 계획의 개정 및 잠금
CREATE TABLE research_scope (
    scope_id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL REFERENCES research_run,
    revision INTEGER NOT NULL CHECK(revision>0),
    manifest_evidence_id TEXT NOT NULL REFERENCES evidence_item,
    plan_evidence_id TEXT NOT NULL REFERENCES evidence_item,
    manifest_sha256 TEXT NOT NULL CHECK(length(manifest_sha256)=64 AND manifest_sha256 NOT GLOB '*[^0-9a-f]*'),
    plan_sha256 TEXT NOT NULL CHECK(length(plan_sha256)=64 AND plan_sha256 NOT GLOB '*[^0-9a-f]*'),
    lifecycle TEXT NOT NULL CHECK(lifecycle IN ('DRAFT','LOCKED')),
    locked_at TEXT,
    approved_by TEXT,
    CHECK(lifecycle<>'LOCKED' OR (locked_at IS NOT NULL AND approved_by IS NOT NULL)),
    UNIQUE(run_id,revision)
) STRICT;

-- 잠긴 경로별 자산/미지원 원본의 합집합
CREATE TABLE scope_source (
    scope_id TEXT NOT NULL REFERENCES research_scope,
    source_ordinal INTEGER NOT NULL CHECK(source_ordinal>=0),
    asset_release TEXT,
    asset_path TEXT,
    unregistered_release TEXT,
    unregistered_path TEXT,
    included INTEGER NOT NULL CHECK(included IN (0,1)),
    reason TEXT NOT NULL,
    PRIMARY KEY(scope_id,source_ordinal),
    UNIQUE(scope_id,asset_release,asset_path),
    UNIQUE(scope_id,unregistered_release,unregistered_path),
    CHECK((asset_release IS NOT NULL AND asset_path IS NOT NULL AND unregistered_release IS NULL AND unregistered_path IS NULL) OR (asset_release IS NULL AND asset_path IS NULL AND unregistered_release IS NOT NULL AND unregistered_path IS NOT NULL)),
    FOREIGN KEY(asset_release,asset_path) REFERENCES asset(release_key,source_path),
    FOREIGN KEY(unregistered_release,unregistered_path) REFERENCES unregistered_source(release_key,source_path)
) STRICT;

-- 파일·모델·면·렌더 등 서로 다른 분모의 고정 키
CREATE TABLE scope_unit (
    scope_id TEXT NOT NULL REFERENCES research_scope,
    unit_id TEXT NOT NULL,
    unit_kind TEXT NOT NULL,
    unit_key TEXT NOT NULL,
    source_ordinal INTEGER,
    required INTEGER NOT NULL CHECK(required IN (0,1)),
    definition_json TEXT NOT NULL CHECK(json_valid(definition_json)),
    PRIMARY KEY(scope_id,unit_id),
    UNIQUE(scope_id,unit_kind,unit_key),
    FOREIGN KEY(scope_id,source_ordinal) REFERENCES scope_source(scope_id,source_ordinal)
) STRICT;

-- 범위 내 작업 단위/계획 버전
CREATE TABLE research_task (
    scope_id TEXT NOT NULL REFERENCES research_scope,
    task_id TEXT NOT NULL,
    task_kind TEXT NOT NULL,
    ordinal INTEGER NOT NULL CHECK(ordinal>=0),
    input_sha256 TEXT NOT NULL CHECK(length(input_sha256)=64 AND input_sha256 NOT GLOB '*[^0-9a-f]*'),
    tool_version TEXT NOT NULL,
    config_json TEXT NOT NULL CHECK(json_valid(config_json)),
    PRIMARY KEY(scope_id,task_id),
    UNIQUE(scope_id,ordinal)
) STRICT;

-- 재시도는 새 행; 기존 source execution 연결 가능
CREATE TABLE research_attempt (
    scope_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    attempt_no INTEGER NOT NULL CHECK(attempt_no>0),
    input_sha256 TEXT NOT NULL CHECK(length(input_sha256)=64 AND input_sha256 NOT GLOB '*[^0-9a-f]*'),
    lifecycle TEXT NOT NULL CHECK(lifecycle IN ('PENDING','RUNNING','FINISHED','INTERRUPTED')),
    started_at TEXT,
    ended_at TEXT,
    legacy_execution_id TEXT REFERENCES research_execution,
    environment_json TEXT NOT NULL CHECK(json_valid(environment_json)),
    PRIMARY KEY(scope_id,attempt_id),
    UNIQUE(scope_id,task_id,attempt_no),
    FOREIGN KEY(scope_id,task_id) REFERENCES research_task(scope_id,task_id),
    CHECK(lifecycle<>'FINISHED' OR (started_at IS NOT NULL AND ended_at IS NOT NULL))
) STRICT;

-- 입력/결과 해시와 재개 위치
CREATE TABLE task_checkpoint (
    scope_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    batch_no INTEGER NOT NULL CHECK(batch_no>=0),
    next_position INTEGER NOT NULL CHECK(next_position>=0),
    input_sha256 TEXT NOT NULL CHECK(length(input_sha256)=64 AND input_sha256 NOT GLOB '*[^0-9a-f]*'),
    result_evidence_id TEXT NOT NULL REFERENCES evidence_item,
    result_sha256 TEXT NOT NULL CHECK(length(result_sha256)=64 AND result_sha256 NOT GLOB '*[^0-9a-f]*'),
    committed_at TEXT NOT NULL,
    PRIMARY KEY(scope_id,attempt_id,batch_no),
    FOREIGN KEY(scope_id,attempt_id) REFERENCES research_attempt(scope_id,attempt_id)
) STRICT;

-- 고정 시도에서 생성된 분석 버전
CREATE TABLE analysis_snapshot (
    snapshot_id TEXT PRIMARY KEY,
    scope_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    input_sha256 TEXT NOT NULL CHECK(length(input_sha256)=64 AND input_sha256 NOT GLOB '*[^0-9a-f]*'),
    analyzer_version TEXT NOT NULL,
    config_sha256 TEXT NOT NULL CHECK(length(config_sha256)=64 AND config_sha256 NOT GLOB '*[^0-9a-f]*'),
    UNIQUE(snapshot_id,scope_id),
    FOREIGN KEY(scope_id,attempt_id) REFERENCES research_attempt(scope_id,attempt_id)
) STRICT;

-- 모든 상세 객체의 스냅샷·종류·원본 위치 식별자
CREATE TABLE research_object (
    snapshot_id TEXT NOT NULL REFERENCES analysis_snapshot,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL CHECK(object_kind IN ('MODEL','ELEMENT','FACE','TEXTURE','FRAME','STATE','APPLICATION','ASSEMBLY','INSTANCE','BINDING','PART','STYLE','ITEM','OTHER')),
    object_key TEXT NOT NULL,
    asset_release TEXT,
    asset_path TEXT,
    json_pointer TEXT,
    PRIMARY KEY(snapshot_id,object_id),
    UNIQUE(snapshot_id,object_id,object_kind),
    UNIQUE(snapshot_id,object_kind,object_key),
    CHECK((asset_release IS NULL)=(asset_path IS NULL)),
    FOREIGN KEY(asset_release,asset_path) REFERENCES asset(release_key,source_path)
) STRICT;

-- 객체와 근거 연결
CREATE TABLE object_evidence (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    evidence_class TEXT NOT NULL CHECK(evidence_class IN ('SOURCE','CALCULATED','OBSERVED','INFERRED','UNKNOWN','NOT_APPLICABLE')),
    locator_detail TEXT NOT NULL,
    PRIMARY KEY(snapshot_id,object_id,evidence_id,locator_detail),
    FOREIGN KEY(snapshot_id,object_id) REFERENCES research_object(snapshot_id,object_id)
) STRICT;

-- 모델 원문 부모/선언 및 해석 제공자
CREATE TABLE model_definition (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'MODEL' CHECK(object_kind='MODEL'),
    parent_raw TEXT,
    model_format TEXT NOT NULL,
    elements_declared INTEGER NOT NULL CHECK(elements_declared IN (0,1)),
    declared_element_count INTEGER CHECK(declared_element_count>=0),
    raw_properties_json TEXT NOT NULL CHECK(json_valid(raw_properties_json)),
    provider_id TEXT,
    resolution TEXT NOT NULL CHECK(resolution IN ('RESOLVED','MISSING','CYCLE','UNSUPPORTED','UNKNOWN')),
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,provider_id) REFERENCES model_definition(snapshot_id,object_id),
    CHECK((resolution='RESOLVED')=(provider_id IS NOT NULL)),
    CHECK(elements_declared=1 OR declared_element_count IS NULL)
) STRICT;

-- 원형 요소의 선언 좌표 및 회전
CREATE TABLE model_element (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'ELEMENT' CHECK(object_kind='ELEMENT'),
    model_id TEXT NOT NULL,
    ordinal INTEGER NOT NULL CHECK(ordinal>=0),
    from_x REAL NOT NULL, from_y REAL NOT NULL, from_z REAL NOT NULL,
    to_x REAL NOT NULL, to_y REAL NOT NULL, to_z REAL NOT NULL,
    rotation_json TEXT CHECK(json_valid(rotation_json)),
    raw_properties_json TEXT NOT NULL CHECK(json_valid(raw_properties_json)),
    coordinate_system TEXT NOT NULL,
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,model_id) REFERENCES model_definition(snapshot_id,object_id),
    UNIQUE(snapshot_id,model_id,ordinal),
    UNIQUE(snapshot_id,object_id,model_id)
) STRICT;

-- 원형 면·선언 UV·텍스처 alias
CREATE TABLE model_face (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'FACE' CHECK(object_kind='FACE'),
    element_id TEXT NOT NULL,
    direction TEXT NOT NULL CHECK(direction IN ('north','south','east','west','up','down')),
    texture_raw TEXT NOT NULL,
    declared_uv_json TEXT CHECK(json_valid(declared_uv_json)),
    uv_rotation INTEGER CHECK(uv_rotation IN (0,90,180,270)),
    cullface TEXT CHECK(cullface IN ('north','south','east','west','up','down')),
    tintindex INTEGER,
    raw_properties_json TEXT NOT NULL CHECK(json_valid(raw_properties_json)),
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,element_id) REFERENCES model_element(snapshot_id,object_id),
    UNIQUE(snapshot_id,element_id,direction),
    UNIQUE(snapshot_id,object_id,element_id)
) STRICT;

-- PNG 원본 크기·메타데이터
CREATE TABLE texture_definition (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'TEXTURE' CHECK(object_kind='TEXTURE'),
    width INTEGER NOT NULL CHECK(width>0),
    height INTEGER NOT NULL CHECK(height>0),
    color_mode TEXT NOT NULL,
    animation_json TEXT CHECK(json_valid(animation_json)),
    sidecar_release TEXT,
    sidecar_path TEXT,
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    CHECK((sidecar_release IS NULL)=(sidecar_path IS NULL)),
    FOREIGN KEY(sidecar_release,sidecar_path) REFERENCES asset(release_key,source_path)
) STRICT;

-- 텍스처实际 프레임 및 프레임 픽셀 지문
CREATE TABLE texture_frame (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'FRAME' CHECK(object_kind='FRAME'),
    texture_id TEXT NOT NULL,
    frame_ordinal INTEGER NOT NULL CHECK(frame_ordinal>=0),
    x INTEGER NOT NULL CHECK(x>=0), y INTEGER NOT NULL CHECK(y>=0),
    width INTEGER NOT NULL CHECK(width>0), height INTEGER NOT NULL CHECK(height>0),
    rgba_sha256 TEXT CHECK(length(rgba_sha256)=64 AND rgba_sha256 NOT GLOB '*[^0-9a-f]*'),
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,texture_id) REFERENCES texture_definition(snapshot_id,object_id),
    UNIQUE(snapshot_id,texture_id,frame_ordinal),
    UNIQUE(snapshot_id,object_id,texture_id)
) STRICT;

-- 모델별 선언 alias 및 최종 texture 해석
CREATE TABLE model_slot (
    snapshot_id TEXT NOT NULL,
    model_id TEXT NOT NULL,
    slot TEXT NOT NULL,
    declared_value TEXT NOT NULL,
    texture_id TEXT,
    resolution TEXT NOT NULL CHECK(resolution IN ('RESOLVED','MISSING','CYCLE','UNSUPPORTED','UNKNOWN')),
    PRIMARY KEY(snapshot_id,model_id,slot),
    FOREIGN KEY(snapshot_id,model_id) REFERENCES model_definition(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,texture_id) REFERENCES texture_definition(snapshot_id,object_id),
    CHECK((resolution='RESOLVED')=(texture_id IS NOT NULL))
) STRICT;

-- 블록상태 형식과 원문 속성
CREATE TABLE state_definition (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'STATE' CHECK(object_kind='STATE'),
    state_form TEXT NOT NULL CHECK(state_form IN ('VARIANTS','MULTIPART','MIXED','UNSUPPORTED')),
    raw_properties_json TEXT NOT NULL CHECK(json_valid(raw_properties_json)),
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind)
) STRICT;

-- variant selector/multipart 조건
CREATE TABLE state_rule (
    snapshot_id TEXT NOT NULL,
    state_id TEXT NOT NULL,
    rule_ordinal INTEGER NOT NULL CHECK(rule_ordinal>=0),
    rule_form TEXT NOT NULL CHECK(rule_form IN ('VARIANT','MULTIPART')),
    condition_json TEXT NOT NULL CHECK(json_valid(condition_json)),
    PRIMARY KEY(snapshot_id,state_id,rule_ordinal),
    FOREIGN KEY(snapshot_id,state_id) REFERENCES state_definition(snapshot_id,object_id)
) STRICT;

-- 원문 옵션과 적용 회전·가중치
CREATE TABLE state_option (
    snapshot_id TEXT NOT NULL,
    state_id TEXT NOT NULL,
    rule_ordinal INTEGER NOT NULL,
    option_ordinal INTEGER NOT NULL CHECK(option_ordinal>=0),
    model_raw TEXT NOT NULL,
    model_id TEXT,
    resolution TEXT NOT NULL CHECK(resolution IN ('RESOLVED','MISSING','CYCLE','UNSUPPORTED','UNKNOWN')),
    x_rotation INTEGER CHECK(x_rotation IN (0,90,180,270)),
    y_rotation INTEGER CHECK(y_rotation IN (0,90,180,270)),
    uvlock INTEGER CHECK(uvlock IN (0,1)),
    weight INTEGER CHECK(weight>0),
    PRIMARY KEY(snapshot_id,state_id,rule_ordinal,option_ordinal),
    FOREIGN KEY(snapshot_id,state_id,rule_ordinal) REFERENCES state_rule(snapshot_id,state_id,rule_ordinal),
    FOREIGN KEY(snapshot_id,model_id) REFERENCES model_definition(snapshot_id,object_id),
    CHECK((resolution='RESOLVED')=(model_id IS NOT NULL))
) STRICT;

-- 상태 할당의 선택된 옵션과 변환
CREATE TABLE state_application (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'APPLICATION' CHECK(object_kind='APPLICATION'),
    state_id TEXT NOT NULL,
    rule_ordinal INTEGER NOT NULL,
    option_ordinal INTEGER NOT NULL,
    assignment_json TEXT NOT NULL CHECK(json_valid(assignment_json)),
    selection_context TEXT NOT NULL,
    transform_json TEXT NOT NULL CHECK(json_valid(transform_json)),
    selection_status TEXT NOT NULL CHECK(selection_status IN ('SELECTED','UNRESOLVED','UNSUPPORTED')),
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,state_id,rule_ordinal,option_ordinal) REFERENCES state_option(snapshot_id,state_id,rule_ordinal,option_ordinal)
) STRICT;

-- 원형 요소와 실제 적용 변환/경계
CREATE TABLE geometry_instance (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'INSTANCE' CHECK(object_kind='INSTANCE'),
    assembly_id TEXT NOT NULL,
    assembly_kind TEXT NOT NULL CHECK(assembly_kind IN ('ASSEMBLY','APPLICATION')),
    element_id TEXT NOT NULL,
    instance_ordinal INTEGER NOT NULL CHECK(instance_ordinal>=0),
    transform_json TEXT NOT NULL CHECK(json_valid(transform_json)),
    bbox_json TEXT CHECK(json_valid(bbox_json)),
    coordinate_system TEXT NOT NULL,
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,assembly_id,assembly_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,element_id) REFERENCES model_element(snapshot_id,object_id),
    UNIQUE(snapshot_id,assembly_id,instance_ordinal),
    UNIQUE(snapshot_id,object_id,element_id)
) STRICT;

-- 실제 면의 기본·변환 UV와 texture/frame 연결
CREATE TABLE face_binding (
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    object_kind TEXT NOT NULL DEFAULT 'BINDING' CHECK(object_kind='BINDING'),
    instance_id TEXT NOT NULL,
    element_id TEXT NOT NULL,
    face_id TEXT NOT NULL,
    context_key TEXT NOT NULL,
    texture_id TEXT,
    frame_id TEXT,
    resolution TEXT NOT NULL CHECK(resolution IN ('RESOLVED','MISSING','CYCLE','UNSUPPORTED','UNKNOWN')),
    base_uv_json TEXT CHECK(json_valid(base_uv_json)),
    base_uv_method TEXT NOT NULL CHECK(base_uv_method IN ('DECLARED','DEFAULT','UNKNOWN','NOT_APPLICABLE')),
    transformed_uv_json TEXT CHECK(json_valid(transformed_uv_json)),
    transform_method TEXT,
    uv_status TEXT NOT NULL CHECK(uv_status IN ('PASS','PARTIAL','HOLD','FAIL')),
    PRIMARY KEY(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,object_id,object_kind) REFERENCES research_object(snapshot_id,object_id,object_kind),
    FOREIGN KEY(snapshot_id,instance_id,element_id) REFERENCES geometry_instance(snapshot_id,object_id,element_id),
    FOREIGN KEY(snapshot_id,face_id,element_id) REFERENCES model_face(snapshot_id,object_id,element_id),
    FOREIGN KEY(snapshot_id,texture_id) REFERENCES texture_definition(snapshot_id,object_id),
    FOREIGN KEY(snapshot_id,frame_id,texture_id) REFERENCES texture_frame(snapshot_id,object_id,texture_id),
    CHECK((resolution='RESOLVED')=(texture_id IS NOT NULL)),
    CHECK(frame_id IS NULL OR texture_id IS NOT NULL),
    CHECK(uv_status<>'PASS' OR (resolution='RESOLVED' AND transformed_uv_json IS NOT NULL AND transform_method IS NOT NULL)),
    UNIQUE(snapshot_id,instance_id,face_id,context_key)
) STRICT;

-- 명시적 원문 참조와 해결/누락/순환
CREATE TABLE reference_edge (
    snapshot_id TEXT NOT NULL,
    edge_id TEXT NOT NULL,
    from_object_id TEXT NOT NULL,
    edge_kind TEXT NOT NULL CHECK(edge_kind IN ('PARENT','TEXTURE_ALIAS','TEXTURE','STATE_MODEL','ITEM_MODEL','SIDECAR','OTHER')),
    declared_reference TEXT NOT NULL,
    declared_namespace TEXT,
    target_release TEXT,
    target_path TEXT,
    resolution TEXT NOT NULL CHECK(resolution IN ('RESOLVED','MISSING','CYCLE','UNSUPPORTED','UNKNOWN')),
    detail TEXT NOT NULL,
    PRIMARY KEY(snapshot_id,edge_id),
    FOREIGN KEY(snapshot_id,from_object_id) REFERENCES research_object(snapshot_id,object_id),
    FOREIGN KEY(target_release,target_path) REFERENCES asset(release_key,source_path),
    CHECK((target_release IS NULL)=(target_path IS NULL)),
    CHECK((resolution='RESOLVED')=(target_release IS NOT NULL))
) STRICT;

-- 증분 연구의 추가/변경/삭제/영향 경로
CREATE TABLE release_delta (
    scope_id TEXT NOT NULL REFERENCES research_scope,
    delta_id TEXT NOT NULL,
    old_release TEXT, old_path TEXT,
    new_release TEXT, new_path TEXT,
    change_kind TEXT NOT NULL CHECK(change_kind IN ('ADDED','CHANGED','DELETED','IMPACTED','UNCHANGED')),
    cause_json TEXT NOT NULL CHECK(json_valid(cause_json)),
    PRIMARY KEY(scope_id,delta_id),
    FOREIGN KEY(old_release,old_path) REFERENCES asset(release_key,source_path),
    FOREIGN KEY(new_release,new_path) REFERENCES asset(release_key,source_path),
    CHECK((old_release IS NULL)=(old_path IS NULL) AND (new_release IS NULL)=(new_path IS NULL)),
    CHECK((change_kind='ADDED' AND old_path IS NULL AND new_path IS NOT NULL) OR (change_kind='DELETED' AND old_path IS NOT NULL AND new_path IS NULL) OR (change_kind IN ('CHANGED','IMPACTED','UNCHANGED') AND old_path IS NOT NULL AND new_path IS NOT NULL))
) STRICT;

-- 측정 수치/구조 통계, 단위·방법·비교 기준
CREATE TABLE measurement (
    measurement_id TEXT PRIMARY KEY,
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    metric TEXT NOT NULL,
    method_version TEXT NOT NULL,
    input_sha256 TEXT NOT NULL CHECK(length(input_sha256)=64 AND input_sha256 NOT GLOB '*[^0-9a-f]*'),
    context_key TEXT NOT NULL,
    unit TEXT NOT NULL,
    coordinate_system TEXT NOT NULL,
    evidence_class TEXT NOT NULL CHECK(evidence_class IN ('SOURCE','CALCULATED','OBSERVED','UNKNOWN','NOT_APPLICABLE')),
    numeric_value REAL,
    value_json TEXT CHECK(json_valid(value_json)),
    numerator REAL,
    denominator REAL CHECK(denominator>0),
    status TEXT NOT NULL CHECK(status IN ('PASS','PARTIAL','HOLD','FAIL')),
    reason TEXT NOT NULL,
    FOREIGN KEY(snapshot_id,object_id) REFERENCES research_object(snapshot_id,object_id),
    CHECK((numeric_value IS NULL OR value_json IS NULL) AND ((numerator IS NULL)=(denominator IS NULL))),
    CHECK(evidence_class NOT IN ('UNKNOWN','NOT_APPLICABLE') OR (numeric_value IS NULL AND value_json IS NULL AND numerator IS NULL)),
    CHECK(status<>'PASS' OR (evidence_class NOT IN ('UNKNOWN','NOT_APPLICABLE') AND (numeric_value IS NOT NULL OR value_json IS NOT NULL))),
    UNIQUE(snapshot_id,object_id,metric,method_version,input_sha256,context_key)
) STRICT;

-- 측정 근거 연결
CREATE TABLE measurement_evidence (
    measurement_id TEXT NOT NULL REFERENCES measurement,
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    locator_detail TEXT NOT NULL,
    PRIMARY KEY(measurement_id,evidence_id,locator_detail)
) STRICT;

-- 범위에 고정된 렌더 대상 및 설정
CREATE TABLE render_case (
    scope_id TEXT NOT NULL,
    case_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    camera_json TEXT NOT NULL CHECK(json_valid(camera_json)),
    settings_json TEXT NOT NULL CHECK(json_valid(settings_json)),
    width INTEGER NOT NULL CHECK(width>0),
    height INTEGER NOT NULL CHECK(height>0),
    PRIMARY KEY(scope_id,case_id),
    FOREIGN KEY(scope_id,unit_id) REFERENCES scope_unit(scope_id,unit_id),
    FOREIGN KEY(snapshot_id,scope_id) REFERENCES analysis_snapshot(snapshot_id,scope_id),
    FOREIGN KEY(snapshot_id,object_id) REFERENCES research_object(snapshot_id,object_id)
) STRICT;

-- 생성 여부/이미지 및 로그 지문; 정확성 판정 별개
CREATE TABLE render_output (
    scope_id TEXT NOT NULL,
    output_id TEXT NOT NULL,
    case_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    generation_status TEXT NOT NULL CHECK(generation_status IN ('GENERATED','FAILED','NOT_GENERATED')),
    png_evidence_id TEXT REFERENCES evidence_item,
    log_evidence_id TEXT REFERENCES evidence_item,
    environment_json TEXT NOT NULL CHECK(json_valid(environment_json)),
    reason TEXT NOT NULL,
    PRIMARY KEY(scope_id,output_id),
    FOREIGN KEY(scope_id,case_id) REFERENCES render_case(scope_id,case_id),
    FOREIGN KEY(scope_id,attempt_id) REFERENCES research_attempt(scope_id,attempt_id),
    CHECK((generation_status='GENERATED')=(png_evidence_id IS NOT NULL))
) STRICT;

-- 가구/부품/스타일/기법 등의 통제 용어
CREATE TABLE semantic_term (
    term_id TEXT PRIMARY KEY,
    term_kind TEXT NOT NULL CHECK(term_kind IN ('FURNITURE','PART','STYLE','MATERIAL','TECHNIQUE','OTHER')),
    label TEXT NOT NULL,
    definition TEXT NOT NULL,
    UNIQUE(term_kind,label)
) STRICT;

-- 의미·디자인 주장, 확실성 및 검수 상태
CREATE TABLE claim (
    claim_id TEXT PRIMARY KEY,
    snapshot_id TEXT NOT NULL,
    object_id TEXT NOT NULL,
    term_id TEXT NOT NULL REFERENCES semantic_term,
    claim_key TEXT NOT NULL,
    revision INTEGER NOT NULL CHECK(revision>0),
    statement TEXT NOT NULL,
    evidence_class TEXT NOT NULL CHECK(evidence_class IN ('SOURCE','CALCULATED','OBSERVED','INFERRED','UNKNOWN','NOT_APPLICABLE')),
    certainty TEXT NOT NULL CHECK(certainty IN ('CONFIRMED','ESTIMATED','UNKNOWN')),
    review_status TEXT NOT NULL CHECK(review_status IN ('PASS','PARTIAL','HOLD','FAIL')),
    conditions_json TEXT NOT NULL CHECK(json_valid(conditions_json)),
    limitations TEXT NOT NULL,
    reviewer TEXT,
    reviewed_at TEXT,
    FOREIGN KEY(snapshot_id,object_id) REFERENCES research_object(snapshot_id,object_id),
    CHECK(certainty<>'CONFIRMED' OR (review_status='PASS' AND evidence_class NOT IN ('UNKNOWN','NOT_APPLICABLE') AND reviewer IS NOT NULL AND reviewed_at IS NOT NULL)),
    CHECK(evidence_class NOT IN ('UNKNOWN','NOT_APPLICABLE') OR certainty='UNKNOWN'),
    UNIQUE(snapshot_id,object_id,claim_key,revision)
) STRICT;

-- 주장 근거의 지지/반례/문맥
CREATE TABLE claim_evidence (
    claim_id TEXT NOT NULL REFERENCES claim,
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    role TEXT NOT NULL CHECK(role IN ('SUPPORT','COUNTEREXAMPLE','CONTEXT')),
    locator_detail TEXT NOT NULL,
    PRIMARY KEY(claim_id,evidence_id,role,locator_detail)
) STRICT;

-- 주장 상충/반례/개정 연결
CREATE TABLE claim_relation (
    claim_id TEXT NOT NULL REFERENCES claim,
    related_claim_id TEXT NOT NULL REFERENCES claim,
    relation TEXT NOT NULL CHECK(relation IN ('SUPPORTS','CONTRADICTS','COUNTEREXAMPLE','SUPERSEDES')),
    reason TEXT NOT NULL,
    CHECK(claim_id<>related_claim_id),
    PRIMARY KEY(claim_id,related_claim_id,relation)
) STRICT;

-- 제작 기법 후보와 승인 근거
CREATE TABLE technique (
    technique_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL UNIQUE REFERENCES claim,
    disposition TEXT NOT NULL CHECK(disposition IN ('CANDIDATE','APPROVED','REJECTED','RETIRED')),
    applicability_json TEXT NOT NULL CHECK(json_valid(applicability_json)),
    approval_evidence_id TEXT REFERENCES evidence_item,
    approved_by TEXT,
    approved_at TEXT,
    CHECK(disposition<>'APPROVED' OR (approval_evidence_id IS NOT NULL AND approved_by IS NOT NULL AND approved_at IS NOT NULL))
) STRICT;

-- 기법의 순서와 조건
CREATE TABLE technique_step (
    technique_id TEXT NOT NULL REFERENCES technique,
    step_ordinal INTEGER NOT NULL CHECK(step_ordinal>=0),
    instruction TEXT NOT NULL,
    conditions_json TEXT NOT NULL CHECK(json_valid(conditions_json)),
    evidence_id TEXT REFERENCES evidence_item,
    PRIMARY KEY(technique_id,step_ordinal)
) STRICT;

-- 사전 고정 검사 기준과 필수 여부
CREATE TABLE validation_requirement (
    scope_id TEXT NOT NULL,
    requirement_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    check_kind TEXT NOT NULL,
    mandatory INTEGER NOT NULL CHECK(mandatory IN (0,1)),
    expected_json TEXT NOT NULL CHECK(json_valid(expected_json)),
    reference_evidence_id TEXT REFERENCES evidence_item,
    PRIMARY KEY(scope_id,requirement_id),
    FOREIGN KEY(scope_id,unit_id) REFERENCES scope_unit(scope_id,unit_id),
    UNIQUE(scope_id,unit_id,check_kind)
) STRICT;

-- 검사 시도, 실제 값, 판정 및 독립 근거
CREATE TABLE validation_result (
    scope_id TEXT NOT NULL,
    result_id TEXT NOT NULL,
    requirement_id TEXT NOT NULL,
    attempt_id TEXT NOT NULL,
    render_output_id TEXT,
    status TEXT NOT NULL CHECK(status IN ('PASS','PARTIAL','HOLD','FAIL')),
    actual_json TEXT NOT NULL CHECK(json_valid(actual_json)),
    evidence_id TEXT REFERENCES evidence_item,
    independent_reference INTEGER NOT NULL CHECK(independent_reference IN (0,1)),
    reason TEXT NOT NULL,
    PRIMARY KEY(scope_id,result_id),
    UNIQUE(scope_id,requirement_id,attempt_id),
    UNIQUE(scope_id,result_id,requirement_id),
    FOREIGN KEY(scope_id,requirement_id) REFERENCES validation_requirement(scope_id,requirement_id),
    FOREIGN KEY(scope_id,attempt_id) REFERENCES research_attempt(scope_id,attempt_id),
    FOREIGN KEY(scope_id,render_output_id) REFERENCES render_output(scope_id,output_id),
    CHECK(status<>'PASS' OR evidence_id IS NOT NULL)
) STRICT;

-- 검사 분모별 종료 결과 및 재판정 이력
CREATE TABLE run_assessment (
    scope_id TEXT NOT NULL REFERENCES research_scope,
    assessment_id TEXT NOT NULL,
    revision INTEGER NOT NULL CHECK(revision>0),
    unit_kind TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('PASS','PARTIAL','HOLD','FAIL')),
    expected INTEGER NOT NULL CHECK(expected>=0),
    attempted INTEGER NOT NULL CHECK(attempted BETWEEN 0 AND expected),
    passed INTEGER NOT NULL CHECK(passed>=0),
    partial INTEGER NOT NULL CHECK(partial>=0),
    held INTEGER NOT NULL CHECK(held>=0),
    failed INTEGER NOT NULL CHECK(failed>=0),
    reason TEXT NOT NULL,
    assessed_at TEXT NOT NULL,
    PRIMARY KEY(scope_id,assessment_id),
    UNIQUE(scope_id,unit_kind,revision),
    CHECK(passed+partial+held+failed=attempted),
    CHECK(status<>'PASS' OR (expected>0 AND passed=expected)),
    CHECK(failed=0 OR status='FAIL')
) STRICT;

-- 종료시 선택된 검사 결과 하나/필수 기준
CREATE TABLE assessment_result (
    scope_id TEXT NOT NULL,
    assessment_id TEXT NOT NULL,
    requirement_id TEXT NOT NULL,
    result_id TEXT NOT NULL,
    PRIMARY KEY(scope_id,assessment_id,requirement_id),
    FOREIGN KEY(scope_id,assessment_id) REFERENCES run_assessment(scope_id,assessment_id),
    FOREIGN KEY(scope_id,result_id,requirement_id) REFERENCES validation_result(scope_id,result_id,requirement_id)
) STRICT;

-- 역사 경로별 분류 및 이관/격리 결정
CREATE TABLE legacy_disposition (
    history_commit TEXT NOT NULL,
    history_path TEXT NOT NULL,
    git_blob TEXT NOT NULL CHECK(length(git_blob)=40 AND git_blob NOT GLOB '*[^0-9a-f]*'),
    classification TEXT NOT NULL CHECK(classification IN ('REUSABLE_LIMITED','REVALIDATE','HISTORICAL','DUPLICATE_CANDIDATE')),
    import_state TEXT NOT NULL CHECK(import_state IN ('NOT_APPROVED','QUARANTINED','APPROVED','IMPORTED')),
    reason TEXT NOT NULL,
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    derived_evidence_id TEXT REFERENCES evidence_item,
    approval_evidence_id TEXT REFERENCES evidence_item,
    CHECK(import_state NOT IN ('APPROVED','IMPORTED') OR approval_evidence_id IS NOT NULL),
    PRIMARY KEY(history_commit,history_path)
) STRICT;

-- 범위 밖 질문을 후속 후보로 기록
CREATE TABLE research_followup (
    scope_id TEXT NOT NULL REFERENCES research_scope,
    followup_id TEXT NOT NULL,
    question TEXT NOT NULL,
    evidence_id TEXT NOT NULL REFERENCES evidence_item,
    state TEXT NOT NULL CHECK(state IN ('PROPOSED','APPROVED','REJECTED')),
    approved_scope_id TEXT REFERENCES research_scope,
    CHECK((state='APPROVED')=(approved_scope_id IS NOT NULL)),
    PRIMARY KEY(scope_id,followup_id)
) STRICT;

CREATE INDEX dbd_object_asset ON research_object(asset_release,asset_path);
CREATE INDEX dbd_ref_target ON reference_edge(target_release,target_path,resolution);
CREATE INDEX dbd_ref_from ON reference_edge(snapshot_id,from_object_id);
CREATE INDEX dbd_measure_metric ON measurement(metric,unit,numeric_value);
CREATE INDEX dbd_claim_term ON claim(term_id,certainty,review_status);
CREATE INDEX dbd_claim_evidence ON claim_evidence(evidence_id);
CREATE INDEX dbd_evidence_hash ON evidence_item(content_sha256);
CREATE INDEX dbd_validation_attempt ON validation_result(scope_id,attempt_id);
CREATE INDEX dbd_legacy_blob ON legacy_disposition(git_blob);
CREATE INDEX dbd_scope_source_asset ON scope_source(asset_release,asset_path);
CREATE INDEX dbd_scope_source_other ON scope_source(unregistered_release,unregistered_path);
CREATE VIEW source_inventory_view AS
 SELECT release_key,source_path,kind AS format,hash_algorithm AS algorithm,digest,byte_count,'REGISTERED' AS support_state FROM asset
 UNION ALL
 SELECT release_key,source_path,format,'SHA256',content_sha256,byte_count,support_state FROM unregistered_source;
-- Candidate rows, not automatic approval: checked export gate must verify evidence
-- bytes, revisions, counterexamples, scope and independent assessment.
CREATE VIEW knowledge_search_view AS
 SELECT c.claim_id,c.snapshot_id,c.object_id,c.claim_key,c.revision,c.statement,c.evidence_class,c.certainty,c.review_status,
 c.conditions_json,c.limitations,t.term_kind,t.label,o.asset_release,o.asset_path,s.scope_id,
 k.technique_id,k.disposition AS technique_disposition
 FROM claim c JOIN semantic_term t ON t.term_id=c.term_id
 JOIN research_object o ON o.snapshot_id=c.snapshot_id AND o.object_id=c.object_id
 JOIN analysis_snapshot s ON s.snapshot_id=c.snapshot_id
 LEFT JOIN technique k ON k.claim_id=c.claim_id;
