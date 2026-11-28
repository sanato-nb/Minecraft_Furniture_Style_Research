# DBD-001 7-H 독립 종료 심사

심사 기준 d44600fe5f0cba090c8c0477b953a0a63bbade8b. 실제 Actions #46162260118 / Job 141031959754 / artifact 15270217722. **심사 실행 완료, 설계 품질 PARTIAL, 설계 승인 보류.** 고정 계획의 16/16 PASS 기준을 변경하지 않는다. H 기계 판독 CLOSED_PARTIAL은 이번 심사 실행 종료를 나타내며 전체 설계 통과/8단계 실행 승인 아님.

## 1. 독립 확인
- DBD001 시작 직전 commit 22e0033f39931aa8cf3699e5affd3139da700d8d의 31,386개 blob 경로 모두 동일. 검증 commit에서 신규 35개, 기존 변경/삭제 0. main 병합 없음.
- 고정 입력 19/19 실제 Git blob 검증, 영역 14/14 물리 객체 연결, 고정 검사 16/16 유지. 기존 8테이블 및 user_version=4 유지, 신규 43테이블/11인덱스/2뷰/34트리거. 운영 적용 없음.
- 과거 6회 실제 job 로그의 96개 T 결과와 summary를 보존 JSON과 직접 대조: 모두 동일.
- 7-H에서 실제 역사 SQLite 9개 경로(8개 고유 blob) 직접 읽기·압축 해제·DDL/컬럼/인덱스/FK·무결성 및 테이블별 행수 대조. 총 134개 경로 기준 테이블/366,868개 경로 기준 행(중복 포함). RQ001 E의 지문/행수 모두 일치. 전체 DDL은 아티팩트 H_historical_ddl.json (SHA256 b33e357fedaf6b06d07693b94ce2a5a0e8bedac7ba8ebe1e949e3e67ee664802); 장기 보존 이전 및 의미 검증·이관 아님.
- 기존 카탈로그 25,387개 재등록 0, 원본/운영 DB 불변. 7-H 교정 후 고정 시험 16개 실행, PASS 7/PARTIAL 9/HOLD 0/FAIL 0. 최신 결과 수정·삭제·REPLACE 방지, 전체 행 논리 해시 복원, 필수 원본 검사 단위 및 제한 근거 필터 음성 검사 확인.

## 2. 14개 영역 대조
| 영역 | 설계 연결 | 연결 시험의 fixture 상태 |
|---|---|---|
| 1 연구 대상·버전·출처 | PASS (3 객체) | PARTIAL (T01, T02, T03, T16) |
| 2 원본 파일 색인 | PASS (5 객체) | PARTIAL (T02, T03, T04, T14) |
| 3 모델 기본 구조 | PASS (4 객체) | PARTIAL (T05, T07) |
| 4 3D 요소·형상 | PASS (4 객체) | PARTIAL (T05, T10) |
| 5 면별 UV | PASS (5 객체) | PARTIAL (T05, T06, T07, T08) |
| 6 텍스처·픽셀 스타일 | PASS (4 객체) | PARTIAL (T06, T09, T10) |
| 7 블록상태 | PASS (5 객체) | PARTIAL (T07) |
| 8 참조 그래프 | PASS (2 객체) | PARTIAL (T03, T07) |
| 9 오프라인 렌더링 | PASS (5 객체) | PARTIAL (T04, T08, T12, T16) |
| 10 가구 종류·부품 의미 | PASS (5 객체) | PARTIAL (T09, T11, T13) |
| 11 형태·비율·스타일 | PASS (4 객체) | PARTIAL (T10, T13) |
| 12 재사용 가능한 제작 기법 | PASS (5 객체) | PARTIAL (T11, T13) |
| 13 검증·예외·완료 | PASS (11 객체) | PARTIAL (T04, T08, T12, T14, T15, T16) |
| 14 AI용 지식 검색 색인 | PASS (7 객체) | PARTIAL (T09, T10, T11, T13) |
영역 연결 PASS는 데이터 모델의 연결 존재만 의미하며 연구 정확성·운영 구현이 아니다.

## 3. 고정 시험 최종 재실행
| 시험 | 실제 fixture 판정 | 실제 확인 | 남은 제한 |
|---|---|---|---|
| T01 | PASS | {"existing_tables":8,"unchanged_rows":{"ai_review":0,"asset":25387,"release":4,"research_execution":0,"research_run":0,"source_checkpoint":0,"source_job":0,"upstream_observation":0}} | - |
| T02 | PASS | {"initial":{"assets_added":25387,"assets_added_by_release":{"another-furniture-4.0.3-git":2994,"handcrafted-4.0.3-git":13626,"macaws-furniture-3.4.2-fabric":3999,"minecraft-java-1.21.11-git":4768}},"repeat":{"assets_added":0,"assets_added_by_release":{"another-furniture-4.0.3-git":0,"handcrafted-4.0.3-git":0,"macaws-furniture-3.4.2-fabric":0,"minecraft-java-1.21.11-git":0}}} | - |
| T03 | PASS | version distinct; conflicting existing key/digest and cross-catalog path blocked by guard | - |
| T04 | PARTIAL | locked scope and terminal attempts immutable; checkpoint update/delete/replace, sequence, new attempt retry and rollback checked | local transaction fixture; cross-job restart and full execution writer not implemented |
| T05 | PASS | actual synthetic source SHA, parent, pointer, elements/faces, coordinate mutation checked | - |
| T06 | PARTIAL | asymmetric PNG, exact ordered fixture UV corners, mirrored UV rejection and frame hash verified | asymmetric fixture UV ordering and sampling verified; Minecraft UV-lock and other transforms remain unverified |
| T07 | PARTIAL | scoped namespace, alias cycle/missing, nested OR, weighted options, missing model and application coverage verified | bounded multipart and variant predicate fixtures; full variant selection and complete game resolver not verified |
| T08 | PARTIAL | PNG decode and size, render unit/attempt and distinct reference/report/output body binding verified | render/result provenance fixture verified; report assertion is not independent visual accuracy |
| T09 | PASS | UNKNOWN independent of geometry; invalid confirmation rejected | - |
| T10 | PARTIAL | two independent synthetic model dimensions and comparable-unit difference; consistent but incorrect ratio rejected | source-derived dimensional comparison verified; broader style metrics not independently verified |
| T11 | PARTIAL | two distinct scoped source model bodies, approval manifest, unrelated support, counterexample, cycle and changed step controls | two distinct scoped source fixtures and approval manifest verified; actual independent research evidence and production approval transitions not validated |
| T12 | PASS | four verdicts, denominator, latest result selection and stale PASS rejection | - |
| T13 | PARTIAL | revision/unit/source/approval, missing group, unfinished attempt, counterexample and evidence corruption controls | fixture allowlist, scoped source hash and rights filtering verified; production identity/permission enforcement not integrated |
| T14 | PARTIAL | two synthetic malformed CSV fixtures quarantined; exact source blob and corrected derivative/approval binding checked; duplicate paths preserved | synthetic transformation approval verified; actual historical CSV correction and production import runner not performed |
| T15 | PASS | reapplication rejected atomically; partial DDL rolled back; source unchanged | - |
| T16 | PARTIAL | local restore manifest including all table row digests, FK, checkpoint, modified row and missing/tampered/expired evidence rejection verified | local manifest and simulated expiry verified; real external archive retention and cross-job restore not exercised |

## 4. 독립 심사 잔여 결함 및 범위 분리
- **H-B01 DESIGN_OPEN (T04, T08)**: render_case의 고정 scope 계획 행에 실행 후 생성되는 snapshot/object의 NOT NULL FK가 있고 잠금 후 INSERT/UPDATE가 금지된다. 실제 실행 전 C3 계획 고정과 실행 후 물리화의 분리가 설계에 필요하다. 현재 fixture는 분석 객체를 잠금 전에 구성하여 이 운영 순서를 검증하지 않는다.
- **H-B02 DESIGN_OPEN (T12, T13)**: latest_results는 요구 항목에 기록된 결과의 최대 attempt_no만 선택한다. 새 시도에 결과가 아직 전혀 없는 경우 기존 PASS의 최신성 판단에 필요한 요구 항목↔계획 task 관계가 부족하다. 기존 T12 PASS는 실행된 음성 fixture에 한정하며 이 경계는 독립 심사에서 승인하지 않는다.
- **H-B03 DESIGN_OPEN (T11, T13)**: 기법 원본 사례 guard는 SHA256 등록 자산만 지원한다. 검색은 원본/claim/measurement 권리 일부를 검사하지만 관련 판정/기법/상충 관계 전체의 권리 및 실제 호출자 인증은 미입증.
- **H-B04 FUTURE_IMPLEMENTATION (T04, T06, T07, T08, T10, T11, T13, T14, T16)**: 실제 cross-job 재개·외부 보존 복원, 게임 UV/상태 해석/렌더 시각 정확성, 전체 스타일 측정, 실제 연구 일반화, 운영 인증/이관은 별도 승인된 운영/연구 단계의 검증으로 구분. 현재 미입증 기록은 유지.

특히 H-B01/H-B02/H-B03은 실제 엔진 구축을 기다리기만 하면 되는 항목이 아니라, 운영 도입 전에 명확히 해결할 설계 경계이다. 기존 T12 fixture PASS를 소급 변경하지 않고 독립 심사에서 미검증 경계를 기록한다. 전체 16개 검사의 통과율을 실제 전체 설계 진척률로 간주하지 않는다. 

## 5. 판정 및 인계
- 7-A~F 설계 산출물 작성/기본 검증 완료. 7-G 시험 실행 완료, 품질 PARTIAL. 7-H 독립 심사 실행 완료, 승인 보류.
- DBD001 v1.0 설계 후보와 현재 증거는 보존. 후속 교정은 H-B01~03부터 시작하여 고정 범위 내 회귀 시험 후 재심사. 8단계 신규 연구 실행 및 운영 DB schema 변경·main 병합은 승인하지 않는다.
- H-B04는 별도 승인된 구현/연구 계획에 이관할 후보이며, 고정 합성 설계 검증을 실제 운영 성능/정확성으로 바꾸거나 임의로 PASS 승격하지 않는다.
