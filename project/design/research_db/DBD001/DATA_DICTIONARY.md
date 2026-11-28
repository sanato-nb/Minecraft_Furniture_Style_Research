# DBD-001 7-E 물리 SQLite 스키마 제안 v1.0

기준: 논리 설계 76a36e1, 사전 고정 DBD001. schema_proposal.sql은 기존 v4 위에 적용하는 **설계용 SQL**이며 src/mcfr 운영 스키마에 추가하지 않는다. 기존 8개 테이블/컬럼/인덱스/user_version=4 유지. 신규 43개 테이블과 2개 조회 뷰, 명시적 조회 인덱스 11개 제안. 실제 배치 성능과 테이블 수 최종 적절성은 시험 후 검토한다.

## 테이블 데이터 사전
각 컬럼의 자료형/NULL/PK/FK/CHECK/UNIQUE는 SQL 파일을 단일 물리 명세로 사용한다. 아래는 역할 및 계층. 1=원본 색인, 2=원본 구조, 3=계산, 4=지식, 5=검증, 6=운영.

| 테이블 | 계층 | 저장 목적 |
|---|---:|---|
| evidence_item | 1 | 해시로 고정된 원본/파생 근거와 보존 위치 |
| release_provenance | 1 | 릴리스의 획득·라이선스 근거 이력 |
| asset_hash | 1 | 기존 등록 해시 외 알고리즘별 확인값 |
| unregistered_source | 1 | 기존 asset 종류 밖 실제 원본만; 가짜 누락 파일 금지 |
| research_scope | 6 | C1/C2/C3 범위와 계획의 개정 및 잠금 |
| scope_source | 6 | 잠긴 경로별 자산/미지원 원본의 합집합 |
| scope_unit | 6 | 파일·모델·면·렌더 등 서로 다른 분모의 고정 키 |
| research_task | 6 | 범위 내 작업 단위/계획 버전 |
| research_attempt | 6 | 재시도는 새 행; 기존 source execution 연결 가능 |
| task_checkpoint | 6 | 입력/결과 해시와 재개 위치 |
| analysis_snapshot | 6 | 고정 시도에서 생성된 분석 버전 |
| research_object | 2 | 모든 상세 객체의 스냅샷·종류·원본 위치 식별자 |
| object_evidence | 2 | 객체와 근거 연결 |
| model_definition | 2 | 모델 원문 부모/선언 및 해석 제공자 |
| model_element | 2 | 원형 요소의 선언 좌표 및 회전 |
| model_face | 2 | 원형 면·선언 UV·텍스처 alias |
| texture_definition | 2 | PNG 원본 크기·메타데이터 |
| texture_frame | 2 | 텍스처实际 프레임 및 프레임 픽셀 지문 |
| model_slot | 2 | 모델별 선언 alias 및 최종 texture 해석 |
| state_definition | 2 | 블록상태 형식과 원문 속성 |
| state_rule | 2 | variant selector/multipart 조건 |
| state_option | 2 | 원문 옵션과 적용 회전·가중치 |
| state_application | 3 | 상태 할당의 선택된 옵션과 변환 |
| geometry_instance | 3 | 원형 요소와 실제 적용 변환/경계 |
| face_binding | 3 | 실제 면의 기본·변환 UV와 texture/frame 연결 |
| reference_edge | 2 | 명시적 원문 참조와 해결/누락/순환 |
| release_delta | 6 | 증분 연구의 추가/변경/삭제/영향 경로 |
| measurement | 3 | 측정 수치/구조 통계, 단위·방법·비교 기준 |
| measurement_evidence | 3 | 측정 근거 연결 |
| render_case | 5 | 범위에 고정된 렌더 대상 및 설정 |
| render_output | 5 | 생성 여부/이미지 및 로그 지문; 정확성 판정 별개 |
| semantic_term | 4 | 가구/부품/스타일/기법 등의 통제 용어 |
| claim | 4 | 의미·디자인 주장, 확실성 및 검수 상태 |
| claim_evidence | 4 | 주장 근거의 지지/반례/문맥 |
| claim_relation | 4 | 주장 상충/반례/개정 연결 |
| technique | 4 | 제작 기법 후보와 승인 근거 |
| technique_step | 4 | 기법의 순서와 조건 |
| validation_requirement | 5 | 사전 고정 검사 기준과 필수 여부 |
| validation_result | 5 | 검사 시도, 실제 값, 판정 및 독립 근거 |
| run_assessment | 5 | 검사 분모별 종료 결과 및 재판정 이력 |
| assessment_result | 5 | 종료시 선택된 검사 결과 하나/필수 기준 |
| legacy_disposition | 6 | 역사 경로별 분류 및 이관/격리 결정 |
| research_followup | 6 | 범위 밖 질문을 후속 후보로 기록 |

## 공통 컬럼
- TEXT ID: 비어 있지 않은 정규화 식별자(애플리케이션 검증); 기존 release_key 및 asset 복합 키 유지. INTEGER 0/1은 boolean, ordinal은 0부터; revision/attempt_no는 1부터. REAL 좌표·수치: 유한 수만 허용, NULL은 미확인, 0으로 대체 금지.
- *_json: 원문 또는 계산 객체·배열. json_valid는 기본 형식만 보장하므로 타입/벡터 길이/키 중복/유한값/정규화와 알고리즘별 의미는 애플리케이션에서 검사. *_sha256: 소문자 64 hex. timestamp: UTC ISO 8601.
- snapshot_id/object_id 복합 FK는 교차 분석 스냅샷 오결합 방지. typed 상세 행은 object_kind까지 검증. model_face/geometry_instance/face_binding은 동일 요소와 동일 프레임의 texture 연결을 강제. 원형 및 적용 결과 분리.
- 생성 상태와 검증 상태 분리. validation_result는 요구 항목별 시도 결과; run_assessment의 집계 단위는 scope_unit.unit_kind, 여러 검사는 한 unit에 속하며 선택된 결과를 assessment_result에 저장한다. 단위 판정은 필수 검사 우선순위로 계산. 모든 필수 검사 PASS/근거 유효/고정 분모 충족 전 PASS 금지.
- knowledge_search_view는 **후보 조회**이며 확정 지식 승인 뷰가 아님. export gate에서 해당 claim의 최신 유효 revision, 검수·지지/반례, 근거 실물 해시, 선택된 범위 판정 및 기법 승인 여부를 검사. 미검증/반례는 별도 표시. 기존 운영 검색과 혼용 금지.

## SQL 밖 필수 트랜잭션 검사 (7-G 시험 대상)
| 검사 | 책임 |
|---|---|
| 원본 등록/미지원 경로 교차 중복 및 기존 해시 충돌 | asset 등록 트랜잭션 내 검증; 기존 등록 API는 변경하지 않고 설계용 wrapper 검증 |
| scope lock | 잠금 전 source/unit/requirement/task/case 명세 일치 및 증거 SHA 대조; 잠금 후 변경 거부, 개정 생성 |
| 시도/체크포인트 | scope/plan/input/도구 fingerprint 일치, batch/position 단조 증가 및 결과 bytes 검증, 기존 execution의 run 일치 |
| 객체 상세 | 실제 원본의 종류/경로/JSON pointer와 snapshot 소속, typed row 완전성, 원형 좌표와 UV 의미 검증 |
| 참조 | 선언 namespace·버전 해결, parent/alias 순환 검출 및 누락 보존; raw 값 불변 |
| 프레임/UV | 프레임 경계 within PNG, 면 방향·UV 배열 차원·기본/변환 좌표 및 회전 검증 |
| 측정 | 단위/좌표계/분모/비율 일치, 알고리즘 버전 및 근거 존재; 유한 수, 측정 대상 정확성 |
| 주장/기법 | 지지 근거 존재·실물 가용, CONFIRMED 검수, 상충/대체 이력 순환 금지; 복수 독립 사례, 단계/조건/반례 및 별도 승인 |
| 렌더/검증 | 고정 case/attempt 일치, 실제 PNG SHA와 크기, 독립 reference와 observed result 구분, output 생성만으로 PASS 금지 |
| 종료 | 고정 unit 분모와 필수 requirement별 최신 선택 결과, 필수 FAIL/HOLD/PARTIAL/미시도, 상태별 합계 일치, 근거 해시 검증 |
| 역사/증거 | 두 CSV 자동 이관 차단, 승인 없는 이관 거부, duplicate 위치 보존; 원본 및 파생/권리/만료 상태 분리 |

SQL만 실행해서 전체 연구 시스템이 검증됐다고 판단할 수 없다. 이 책임들은 7-G의 설계 시험/음성 사례에서 확인한다. 향후 운영 도입은 별도 migration runner와 버전 정책 필요; 기존 세미콜론 분할 적용기를 복합 SQL에 사용하지 않는다.
## 7-H 후속 교정 H-B01/02
고정 render_case는 실행 전 analysis_task_id, planned_object_kind/key 및 카메라·설정을 잠근다. 실행 후 render_output이 실제 snapshot/object에 연결되며 같은 scope와 계획된 분석 task 및 객체 식별자를 검사한다. 생성 실패는 물리 객체 미생성을 기록할 수 있다. 출력 행은 변경·삭제·REPLACE 금지. validation_requirement는 고정 task_id를 FK로 보유하며 다른 task의 시도 결과를 거부한다. 최신성은 결과 행이 아니라 해당 task의 최대 시도 번호로 판단하고 최신 결과 누락 시 이전 PASS로 대체하지 않는다. 기존 43개 신규 테이블/11 인덱스/2 뷰 유지. 실제 운영 적용 아님.
