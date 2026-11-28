# DBD-001 7-A 기존 DB 및 기능 사전 조사

기준 22e0033f39931aa8cf3699e5affd3139da700d8d; RQ001 종료(자료 품질 FAIL, 검사 종료), 데이터 명세 v0.2, 계약 v0.6 및 전체 합의 정리본을 확인했다.

## 재사용 대상 8개 테이블
| 기존 테이블 | 기능 | 설계 영향 |
|---|---|---|
| release | 대상/버전/로더/고정 지문 | PK 유지, 출처/권리 보강은 별도 연결 |
| asset | 릴리스+경로 복합 PK, 종류/해시/크기/근거 경로 | 그대로 사용, 여러 해시와 지원 상태/참조는 별도 연결 |
| research_run | 4가지 연구 방식 및 baseline | 회차 연결, 잠긴 scope/plan 추가 구조 |
| research_execution | 원본/역사 검사 결과, PASS/FAIL | 기존 의미 유지, 새 연구 판정 분리 |
| source_job | 원본 검사 진행, 64개 단위 처리 | 기존 검사 전용 재사용; 일반 연구 작업 별도 연결 |
| source_checkpoint | 위치별 JSON 결과 | 기존 원본 체크포인트 보존 |
| ai_review | 승인형 API 검토 | 필수 경로 아님, 추론 근거만 조건부 연결 |
| upstream_observation | 버전 관찰 이력 | 업데이트 추적 재사용 |

실제 코드 확인: register_release는 SELECT * 튜플을 기존 RELEASE_FIELDS/ASSET_FIELDS와 직접 대조하므로 기존 컬럼을 무심코 추가하면 재등록 회귀 가능. research_execution은 status CHECK PASS/FAIL, source_jobs/ai_review/cross_research는 그 의미에 의존. schema 적용기는 세미콜론 split 사용(복합 트리거/DDL 부적합 가능). 운영 초기화는 schema_version=4 및 APP_ID 고정. 따라서 신규 연구 설계는 기존 원본 검사의 상태를 재해석하지 않으며, 별도 연구 판정 구조를 검토한다. 현재 버전·운영 코드 변경 금지.

6단계 결과: 25,387 등록 원본 PASS, 역사 DB 9경로/8고유 blob 물리 PASS, 분류 11 제한 재사용/2,268 재검증/874 역사/14 중복. 두 CSV는 자동 이관 금지. 기존 TV001 PARTIAL 유지. 데이터 명세 14개 모두 설계에 포함하되 기존 지식 정확성의 재검증은 하지 않는다.
