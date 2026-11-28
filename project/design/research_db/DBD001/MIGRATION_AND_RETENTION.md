# DBD-001 7-F — 이관·호환성·근거 보존 설계 v1.0

기준 7-E 물리 스키마 제안 c5356aa. 이 문서는 **이관 절차 설계**이며 실제 운영 DB 또는 역사 DB를 이관하지 않는다. 7-G 임시 복제 시험 및 7-H 검수 전에는 운영 적용 승인 금지.

## 1. 운영 v4 호환성

- 기존 8개 테이블, PK/FK, 컬럼 순서, 기존 SQL/CLI 및 app_id/user_version 유지. release/asset의 SELECT * 튜플 비교, source_job/source_checkpoint, ai_review의 PASS source 실행 필터, upstream_observation 및 cross_research 의미 유지.
- 신규 DDL은 별도 schema_proposal.sql에만 존재. 기존 initialize의 세미콜론 분할 방식을 신규 복합 SQL에 적용하지 않는다. 임시 시험은 SQLite backup API로 일관된 사본을 만들고 독립 트랜잭션에서 신규 DDL 적용. 운영 도입 시 별도 승인된 migration runner, schema revision/호환 버전 및 회귀 시험 필요. 임시 사본은 user_version=4를 유지하지만 운영 파일로 사용 금지.
- SQL 신규 스키마 자체는 재실행 가능한 IF NOT EXISTS 방식이 아니다. 부분 적용 상태를 숨기지 않기 위해 두 번째 적용은 원자적으로 거부하거나, 최초 적용 전 기록한 스키마 지문 및 모든 객체 정의가 정확히 일치할 때만 runner에서 no-op. 일부만 있거나 정의 차이는 FAIL, DROP/REPLACE 금지.

## 2. 자료 분류와 이관 경계

| RQ001 분류 | 경로 수 | 이관 처리 |
|---|---:|---|
| REUSABLE_LIMITED | 11 | 입증된 출처·등록/DB 구조만 재사용 후보, 내용 자동 승인 금지 |
| REVALIDATE | 2,268 | 격리 또는 검수 대기, 원본과 새 기준의 재검증 승인 후에만 |
| HISTORICAL | 874 | 역사 기록으로 보존, 최신 지식으로 승격하지 않음 |
| DUPLICATE_CANDIDATE | 14 | 7그룹의 동일 바이트와 위치별 역할 보존, 삭제 금지 |

H 원장의 경로별 hash와 분류 근거를 legacy_disposition으로 연결할 수 있으나 실제 전체 행 import는 이번 제외. T14 합성 fixture로 분류·격리 규칙만 검증한다. F에서 검증한 25,387개 등록 자산만 기존 import_catalog를 임시 DB에서 다시 재현(재등록 0). 실제 외부 원본을 새로 다운로드하거나 역사 DB 전체 행을 옮기지 않는다.

두 CSV(TEX05-R004/SOURCE_LEDGER.csv, TEX05-R007/BLOCK_VS_TERRAIN_SHADER.csv)는 QUARANTINED; 열 밀림 있는 역사 파일을 그대로 보존. 이후 별도 승인된 정규화 파생본은 원본 Git SHA, 변환 코드·버전, 행/열 변화, 파생 SHA와 검수 승인 근거가 모두 있어야 이관 가능. 6,343 UV 면과 14 기법 후보/7 제한은 미확인 또는 후보로 유지.

## 3. dry-run 절차와 충돌/복구

1. 실제 파일 경로와 사용 대상, scope/plan 승인 확인. 운영 쓰기 중지 및 일관된 SQLite backup API로 사본 생성(단순 WAL 파일 복사 금지). 원본 및 사본의 스키마/app_id/user_version, table counts, integrity_check/foreign_key_check, logical digest와 snapshot hash 기록.
2. 임시 복제에 v4 보존 상태 확인 후 제안 DDL 한 트랜잭션 적용. DDL 오류 시 rollback. 기존 스키마 SQL/컬럼/인덱스·행 내용을 사전과 사후 대조. 운영 파일은 쓰지 않는다.
3. import 대상 명세는 release pin, source path, source digest, evidence hash, transform version, stable target key를 기록. 승인 없는 행 또는 누락/권리 제한 자료는 거부 또는 격리. 동일 ID/동일 payload 재시도는 no-op; 동일 ID/다른 payload는 FAIL 및 전체 배치 rollback; 새 원본 버전이나 분석기는 새 release/snapshot/revision.
4. 원본/계산/추론/검증 값은 별도 필드·객체에 기록. 역사 데이터의 UNKNOWN을 0/빈 확정값으로 변환하지 않는다. 기존 원장과 source rows 수·PK·FK·원본 출처를 대조. 대표 이관 fixture 및 음성 시험은 T14/T15에서 확인.
5. checkpoint/result manifest는 scope/input/config/code/result SHA256, 작업/시도 ID 및 다음 위치를 포함. 해당 배치 결과와 checkpoint를 같은 트랜잭션으로 커밋. 재개 시 실물 근거 해시, 연속 위치 및 fingerprint를 검사. 다르면 재사용 금지. 새로운 시도 ID로 기록하며 기존 성공 기록 덮어쓰기 금지.
6. 운영 전환은 이번 범위 밖. 향후 승인된 cutover는 사본 검수, 구버전 reader 거부 또는 명시된 호환, 쓰기 정지, 파일 원자 교체, 복구용 원본 백업 유지 필요. rollback은 검증된 사본 복원 또는 신규 DB 폐기; 원본 schema downgrade/DROP 금지. 새 쓰기가 발생한 뒤의 복구·변경분 보존 정책은 운영 도입계획에 별도 고정한다.

## 4. 장기 증거와 라이선스

- SQLite는 기준 지식·출처·판정·관계. JSON/MD는 파생 출력. 대형 바이너리 자체를 DB에 불필요하게 복제하지 않고 evidence_item의 SHA256·byte_count·locator·member_locator·storage_kind·권리·상태를 저장.
- Git: 적법한 소형 결과/스코프/계획/검수 보고서/코드/원장 및 고정 commit/path. 외부 원본·저작권 불명 원본을 커밋하지 않는다. Git 이력 역시 무기한 보장 아님.
- Actions artifact: 작업 전달/검수용 임시 보존 30일. run/job/artifact ID 및 파일 단위 hash 기록. 만료 전에 권리 확인한 파생 근거를 장기 보관 위치(운영자 관리 백업, 접근 제한 저장소 또는 적법한 Git 경로)로 옮기는 절차를 운영 도입 때 설정. 현재 RQ001 D/E/F/H 원장은 아직 아티팩트 보존에 의존하며 이 문서가 보존 이전 완료를 뜻하지 않는다.
- 외부 고정 원본: Git commit 또는 공식 배포 버전+archive digest와 member digest. locator만으로 원본 확보 인증 아님. 제한된 원본은 재배포 금지, 필요 시 권한 있는 환경에서 재취득/해시 확인. 접근 불가 시 HOLD. 단순 URL 변경은 원본 pin을 바꾸지 않는다.
- 백업: 일관된 SQLite snapshot + 외부 근거 파일 목록/크기/SHA256 + 코드/설정/범위/버전 manifest. 복원은 다른 임시 디렉터리에서 모든 파일 hash 및 SQLite FK/무결성 검증 후 사용. backup/checkpoint는 원본 보호와 권리 정책을 따른다.
- 만료/누락/제한 상태는 근거의 현재 접근 가능성이다. 과거 실행 판정을 소급 덮어쓰지 않는다. 신규 지식 검색·재검증·재사용 승인에서 실물 해시 확인 불가 시 HOLD 또는 역사 근거 표시. 보존 정책의 운영 자동화·다른 Job 간 실제 복원 성능은 미검증.

## 5. 검증 책임

T01/T02/T03/T14/T15/T16에서 기존 v4 schema/등록, 충돌·재등록, 두 결함 격리, 사본 DDL rollback, hash 및 복원을 시험한다. 합성 fixture와 카탈로그 재현의 성공은 생산 DB 이관 성공이나 의미 지식 재검증이 아니다. 7-G에서 실제 test suite 및 조회 계약을 추가하고, 7-H에서 독립 종료 심사한다.
