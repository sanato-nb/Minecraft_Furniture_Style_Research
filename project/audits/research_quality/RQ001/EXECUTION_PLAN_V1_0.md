# RQ-001 상세 실행계획 v1.0 (6-C)

6-B scope_lock.json의 고정 목록만 사용. 실제 검사 실행 전에 이 문서와 범위 파일을 커밋한다. Python 3.12, SQLite, Pillow, PyYAML, GitHub Actions Ubuntu 24.04. 유료 AI API 및 Minecraft 실행 없음. 기존 src/mcfr 기능은 F에서 재사용. 작업 코드는 scripts/research_quality/, 결과는 RUNNER_TEMP/rq001, 소형 요약·검수 기록만 PR에 보존. 원본·역사 DB 변경 금지.

## 6-D — 파일 전수 검증
1. 고정 원장 7개 각각 Git blob/행수 확인; 경로 중복·절대경로·상위 이탈 금지. git ls-tree -r 고정 pin의 비원본 경로·blob·size와 전수 대조.
2. UTF-8 경로 바이트 순 정렬 후 200경로씩 16배치(15×200+167). 각 파일 실제 bytes 읽기, 크기·Git blob SHA1·SHA256 기록. symlink 등 일반 파일 외 유형은 HOLD, 해시 불일치 FAIL.
3. JSON 중복 키/NaN 금지 및 파싱, JSONL 비공백 행 파싱, CSV/TSV UTF-8-sig/strict 파싱·열수 확인(헤더 없음 등 역사 예외 명시), gzip/xz 전체 스트리밍 해제 후 해당 형식 검사, PNG/JPG Pillow verify+load, SVG XML 파싱, YAML safe_load_all, Python AST 구문 검사(실행 금지), 기타 문서/코드 UTF-8 디코딩(컴파일·의미 검증 아님), SQLite 헤더 및 해제 검사(깊은 검사는 E). 압축 해제 상한 512 MiB/파일, 초과 HOLD. 미지원 형식 HOLD.
4. 배치마다 원장/검사 코드 해시와 입력/결과 해시를 묶어 JSONL 및 체크포인트를 원자적으로 저장. 동일 입력/코드/결과 및 원본 실제 해시 재확인 시에만 재사용. 별도 Job 복구는 필수 아님. 누락/실패도 행으로 보존. 산출물 D_files.jsonl, D_summary.json, batches/.
5. 완료 기준 3,167/3,167 경로별 결과 및 별도 해시·형식 판정, 실제 검사 실행 수·PASS·HOLD·FAIL 집계 일치. 파일이 깨졌다고 자동 수정/삭제하지 않음.

## 6-E — SQLite 전수
scope_lock의 9경로를 순서대로 처리. 압축은 임시 해제(512 MiB 한도), 원본 해시 기록. sqlite URI mode=ro, query_only=ON, PRAGMA integrity_check/foreign_key_check, application_id/user_version, sqlite_schema DDL, table_xinfo/foreign_key_list/index_list, 테이블 행수와 선언 키 수집. 행 전체 내용을 복제하지 않는다. 원본 전후 SHA256 대조. 동일 blob 2경로 보존; 각 경로별 결과. FK 선언 없음은 NOT_APPLICABLE(논리 참조 무결성 아님). E_databases.json 및 E_summary.json. 9개 결과와 8고유 blob 대조.

## 6-F — 원본 원장 검증
기존 research_db.initialize/register_release, legacy_catalog.import_catalog, research_engine.asset_digest/verify_entry 재사용. 임시 SQLite v4에 4릴리스, 25,387개 등록 재현하고 릴리스별 4,768/2,994/13,626/3,999 및 경로 키·원장 경로 대조. 재등록 0건 기대. 등록 원장 자체의 직접 레코드 수 및 중복 키도 대조. 바닐라: 역사 pin b2960c...의 git ls-tree 및 현재 기준 main 원본 실제 bytes를 모두 대조. AF/HC: registry Git URL에서 고정 commit fetch, HEAD 확인 후 경로 bytes 검증. Macaw: registry의 Modrinth version xhmciaUD의 파일 메타데이터로 기대 SHA256과 일치하는 다운로드를 선택, 임시 JAR SHA256 전체 대조 후 ZIP 중복 경로 거부 및 파일별 해시 확인. 공식 원본 접근 실패 시 해당 릴리스 전 경로 HOLD 기록(다른 버전 대체 금지). 외부 다운로드/원본 재배포 금지. F_catalog.json, F_assets.jsonl, F_summary.json. 원장 검증과 실제 원본 검증 수 분리.

## 6-G — 14영역 대조
데이터 명세 v0.2 영역 번호/필수 항목을 그대로 사용. 역사 정본·원장 헤더/JSON 키/SQLite 테이블·컬럼에서 확인한 근거 경로와 실제 필드, 버전·원본 연결, SOURCE/CALCULATED/OBSERVED/INFERRED/UNKNOWN/NOT_APPLICABLE, 상태·제한을 기록. 자동 이름 기반 분류는 후보만; 필드/본문 확인 없는 지식은 재사용 확정 금지. 각 영역별 존재/부분/부재/보류 및 DB 설계 요구를 G_areas.json 14행으로 기록. 의미 정확성 전수 재연구는 제외.

## 6-H — 자료 분류
D 결과와 E/F/G 근거를 결합하여 고정 3,167경로 전수 H_classification.jsonl 작성. 기본 분류: REUSABLE_LIMITED(구체 검증 근거/재사용 한계 명시), REVALIDATE, HISTORICAL, DUPLICATE_CANDIDATE(별도 중복 플래그 및 위치별 역할; 삭제 금지). 근거가 없는 자동 분류는 REVALIDATE 또는 UNKNOWN 명시. 분류가 됐다는 사실과 정확성 검증은 별개. 각 경로 1행, 영역 복수 연결 허용.

## 6-I — 독립 종료
별도 검수 코드에서 7 원장·16 배치·3,167 경로·9 DB·4 릴리스/25,387 자산·14 영역과 결과 해시, 상태 합계, 판정 논리, 동일 blob 7그룹 및 main 원본 보존 확인. 실제 Action run/job/artifact·코드 SHA 기록. PASS/PARTIAL/HOLD/FAIL을 계약대로 구분. 누락과 불일치가 있으면 고정 범위의 구현만 수정 후 재실행. 후속 DB 상세 설계에는 검증된 필드·미검증 공백·이관 후보·참조 키·예외를 인계하고 DB 자체는 변경하지 않는다.

## 실행 순서와 비용
D→E→F→G→H→I; 선행 검사의 결과가 있어야 후행 검증. 각 단계 코드 작성 뒤 회귀/실행 결과 확인. D는 단일 Job 20분 상한, E/F는 별도 Job(각 20분/30분 상한), 외부 접근 실패로 다른 버전을 선택하지 않는다. 전체 결과 아티팩트 30일 보존, 영구 요약과 결과 해시를 Git에 기록. 실제 시간/메모리/재개 성공은 실행 전 보장하지 않음. 신규 범위 제안은 종료 시 따로 기록.
