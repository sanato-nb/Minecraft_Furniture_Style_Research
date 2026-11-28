# DBD-001 7-D 논리 데이터 모델 v1.0 (설계안)

잠긴 범위/실행계획 커밋 3684fef7d98c4f4087d1dca4405d0192ecb89706. 14개 영역의 논리 엔티티·키·검증 조건을 제안한다. 기존 운영 SQLite v4 8테이블은 유지하며, 본 문서는 운영 DB 적용 또는 기존 연구 지식 승인 아님.

## 1. 관계 구조

- 기존 release → asset (release_key,source_path) → research_run (run_id). release_provenance는 배포/라이선스/확보 이력, asset_hash는 여러 알고리즘과 측정 근거를 추가한다. 기존 release/asset의 단일 해시는 그대로 원본 등록 지문이다.
- 원본 사전 조사: 기존 asset이 표현하지 못하는 실제 파일 종류는 unregistered_source에만 기록. 두 저장소 간 동일 경로의 중복 등록은 금지(트랜잭션 검사). source_inventory_view는 두 범주의 합집합. 참조가 존재하지 않는 파일은 이 목록에 가짜 원본으로 넣지 않고 reference_edge에서 MISSING으로 기록.
- research_run → research_scope(개정별 immutable 범위, manifest/plan 해시, 승인·잠금) → scope_source 및 scope_unit(단위별 고정 분모) → research_task → research_attempt → task_checkpoint. 기존 source_job/checkpoint는 원본 검사용; 기존 research_execution은 원본/레거시 실행 증거로만 연결한다.
- 고정 scope → analysis_snapshot(분석기/설정/입력 fingerprint와 시도 연결) → research_object(객체 identity). typed 상세 테이블은 object_id와 scope/snapshot FK, 객체 종류 제약을 사용. 모델 원형, 적용 상태, 텍스처, 조립, 부품/스타일 분석 객체는 구분. 같은 모델이라도 다른 릴리스 또는 snapshot이면 다른 분석 객체. 물리 설계에서 typed child 종류와 snapshot 일치 보장; 미확정 객체/없는 원본을 가짜 모델로 만들지 않는다.
- model_definition → model_element → model_face; model_slot 및 reference_edge로 원문 alias/parent를 추적. geometry_instance는 assembly/state application에서 source element를 참조하며 변환과 결과 bbox를 분리. face_binding은 원형 face, 적용 문맥, texture/frame, 선언/기본/변환 UV와 검증 상태 연결. 상속된 요소를 원형에 중복 저장하지 않는다.
- state_definition → state_rule → state_option; state_application은 정확한 상태 할당 및 선택 옵션별 적용 객체. 옵션 weight는 원본값과 기본값 구분, 랜덤 선택/동시 multipart는 실제 조사 조건과 별도. state option과 geometry_instance는 모델 해석 및 상태 변환 연결.
- texture_definition → texture_frame; measurement는 단위·좌표계·측정 알고리즘 버전·분모·근거를 가진 객관 계산. 픽셀 샘플/통계는 프레임 및 face binding을 대상으로 함. 계산이 불가능하면 수치 NULL+이유, 0으로 대체 금지.
- render_case(고정 대상/카메라/설정) → render_output(생성 상태, PNG/로그 근거, 환경) → validation_result(독립 기준). 생성 성공은 형상·UV 정확성 PASS를 자동 생성하지 않는다.
- semantic_term → claim(객체, 역할/스타일/기법 주장, evidence class, semantic certainty, 조건, 한계, 검수 상태); claim_evidence 및 claim_relation(지지/반례/상충/대체). technique와 technique_step은 주장에 연결한 순서·조건·반례의 구조. 승인된 기법만 확정 지식 검색에 노출.
- evidence_item은 content SHA256/size, 위치 locator, Git commit/path, run/job/artifact, 보존 상태, 원본/파생 및 권리 구분. object_evidence, measurement_evidence, claim_evidence 등 실제 FK를 통해 근거 연결. 외부 URI/경로만으로 내용 검증 인정 금지.
- validation_requirement는 scope에서 대상 unit과 필수 여부/기대 기준을 고정; validation_result는 attempt의 실제 결과. run_assessment는 종료 당시 결과 집합과 집계, 판정, 미해결 사유. research_followup은 범위 밖 질문과 발견 근거를 보존하되 현재 분모 변경 금지. legacy_disposition은 역사 경로+blob+검수 분류, 이관 승인/격리 및 변환 출처. release_delta는 기존 INCREMENTAL과 연결해 추가/변경/삭제/참조 영향 구분.
- knowledge_search_view는 정규화 테이블에서 파생되는 읽기 전용 조회. 원본/측정/추론/검증 상태·제한을 동시에 반환. JSON export는 조회 결과의 버전과 필터·scope/출처를 명시한다.

## 2. 식별자와 데이터 경계

| 식별 단위 | 키 정책 |
|---|---|
| 원본 버전 | 기존 release_key + 고정 pin; 같은 버전 이름이라도 다른 digest면 별개 |
| 등록 자산 | 기존 (release_key,source_path), resource_id는 탐색용이며 전역 고유하지 않음 |
| 범위 | scope_id, run_id+revision unique; 잠긴 manifest/plan SHA256, 변경은 새 revision |
| 단위 | scope_id+unit_kind+unit_key, 실제 원장 및 대상/기대 기준 연결 |
| 분석 객체 | snapshot_id+object_kind+object_key unique, 실제 원본 위치와 context |
| 요소/면 | model object+element ordinal, element+direction; 재배열은 새 snapshot |
| 적용/측정 | 상태 할당/옵션/변환·알고리즘 버전·입력 fingerprint, 독립 계산 기록 |
| 근거/주장 | evidence_id 및 content hash/locator; claim id 및 revision/supersedes. 동일 해시 다른 위치 보존 |

원본 경로는 POSIX 상대 경로, 리소스 ID는 namespace 포함. 원본 버전이 바뀌면 원래 결과를 덮어쓰지 않는다. 기존 DB 전체 데이터가 정확하다는 의미가 아니다.

## 3. 값·근거·검증 3축

1. 근거 종류: SOURCE, CALCULATED, OBSERVED, INFERRED, UNKNOWN, NOT_APPLICABLE. 객관 좌표 및 계산값을 추론으로 덮어쓰지 않는다.
2. 의미적 확실성: CONFIRMED, ESTIMATED, UNKNOWN (의미 주장에만 적용). 추론을 SOURCE로 승격하지 않는다. CONFIRMED는 검수/지지 근거를 요구하며 반례/적용 범위 함께 보존. UNKNOWN은 구조 레코드 실패 사유가 아니다.
3. 검증 판정: PASS, PARTIAL, HOLD, FAIL; 실행 생명주기(PENDING/RUNNING/FINISHED 등) 및 형식/지원 상태와 별개. 필수 FAIL은 전체 FAIL, 필수 HOLD/미시도는 전체 PASS 금지; 확인된 부분만 종료 가능하면 PARTIAL, 판단 불가면 HOLD. 필수 모두 PASS이고 분모 충족·근거 유효하면 PASS. 불필요/제외는 사전 범위의 근거로만 처리. 같은 unit의 재시도는 새 attempt, 분모를 늘리지 않고 선택된 종료 기준 결과를 연결. 자동 집계의 이유/누락을 보존.

## 4. 14영역 논리 매핑

| 번호 | 영역 | 주요 엔티티 | 검증 |
|---:|---|---|---|
| 1 | 연구 대상·버전·출처 | release, release_provenance, upstream_observation | T01, T02, T03, T16 |
| 2 | 원본 파일 색인 | asset, asset_hash, unregistered_source, scope_source, source_inventory_view | T02, T03, T04, T14 |
| 3 | 모델 기본 구조 | research_object, model_definition, model_slot, reference_edge | T05, T07 |
| 4 | 3D 요소·형상 | model_element, model_face, geometry_instance, measurement | T05, T10 |
| 5 | 면별 UV | model_face, model_slot, face_binding, texture_frame, measurement | T05, T06, T07, T08 |
| 6 | 텍스처·픽셀 스타일 | texture_definition, texture_frame, measurement, claim | T06, T09, T10 |
| 7 | 블록상태 | state_definition, state_rule, state_option, state_application, geometry_instance | T07 |
| 8 | 참조 그래프 | reference_edge, release_delta | T03, T07 |
| 9 | 오프라인 렌더링 | render_case, render_output, validation_requirement, validation_result, evidence_item | T04, T08, T12, T16 |
| 10 | 가구 종류·부품 의미 | research_object, semantic_term, claim, claim_evidence, claim_relation | T09, T11, T13 |
| 11 | 형태·비율·스타일 | measurement, claim, claim_relation, semantic_term | T10, T13 |
| 12 | 재사용 가능한 제작 기법 | technique, technique_step, claim, claim_evidence, claim_relation | T11, T13 |
| 13 | 검증·예외·완료 | research_scope, scope_unit, research_task, research_attempt, task_checkpoint, validation_requirement, validation_result, run_assessment, legacy_disposition, evidence_item, research_followup | T04, T08, T12, T14, T15, T16 |
| 14 | AI용 지식 검색 색인 | knowledge_search_view, semantic_term, claim, measurement, technique, claim_evidence, run_assessment | T09, T10, T11, T13 |

세부 키와 계약은 area_map.json. 공통 analysis_snapshot/research_object/evidence_item 및 검사 구조는 모든 영역에 적용. 7-E에서 실제 SQL 제약·FK·인덱스·데이터 사전으로 정합화하며, 이 문서에 없는 새로운 연구 범위를 추가하지 않는다.

## 5. 설계상 경계 및 검증 의무

- 원형/변환 후 결과를 같은 값으로 취급 금지. 좌표계, 단위, 선언 여부, UV 계산법과 지원 상태를 기록한다.
- 같은 이름의 texture/model이 버전·source namespace가 다르면 분리; 미해결 edge를 실제 asset FK로 강제 연결하지 않는다.
- 운영 v4 기존 API의 SELECT * 비교 및 PASS/FAIL 의미를 보존. 새로운 상세 연구 판정은 별도 run_assessment를 사용하고 기존 원본 검사와 연결한다.
- SQL 제약으로 그래프 순환/전체 분모/근거 충분성/승인 상태 전이를 완전히 강제할 수 없는 경우 7-E/G에서 트랜잭션 검사 책임 및 음성 시험을 지정.
- RQ001의 역사 2개 CSV는 격리; 2,268 재검증/874 역사/14 중복/11 제한적 재사용은 원본 지식의 신뢰도 승인 아님.
- 7-D 산출물은 논리 설계 완료 후보이며 7-E~H의 물리·검증 결과가 남아 있음.
