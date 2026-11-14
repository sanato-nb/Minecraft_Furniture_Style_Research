# v64 → 다음 채팅: 1-2-A 역사 자료 원본 출처 통합

- 시작: 연결 GitHub `main` 최신 HEAD를 읽고 `research/vanilla_models/v64/{SUMMARY.json,REPORT.md,07_P1_544_EVIDENCE_LEDGER.csv,VALIDATION_POST_RESEARCH_COMMIT.json}` 원격 검증. 최신 버전 있으면 그것 우선.
- v63 기존 v5~v43 21폴더·194파일 중 v62~v63 선택 원본 CSV **24개** 내용 재조회. 이번 v64에서 추가로 **Markdown30/30 + JSON19/19 + Python script4/4 = 53개** 실제 원본 SHA·내용 검증. 선택 통합 누적 **77/194 내용 재조회**, 나머지 **117 = CSV113 + SQLite4**. 이는 **이번 선택 검사** 기준이며 과거 연구 전부 미실행 뜻 아님.
- `00_HISTORY_194_FILE_AUDIT_LEDGER.csv`: 194행×17열. 이전 v63 인벤토리11열·194행 **2,134 데이터셀 모두 동일**, v64 직접 내용/JSON 파싱 등 6개 열 추가. `00_BATCH_1…6_ORIGINAL_MD_JSON_SOURCE_EVIDENCE.json`에 49개 원본 SHA/JSON keys/선택 line 증거. `00_PYTHON_4_ORIGINAL_SOURCE_EVIDENCE.json`에 기존 v5~v8 Python4 소스 원문 SHA·원본 DB 코드행. **스크립트 실행, SQLite B-tree 재판독, 전체 의미론 스캔은 하지 않음.**
- 중요한 정정: `v30/00_v30_바닐라5모델_91면UV_18PNG_RGBA_투명도정정보고서.md` SHA `1c843f013ba7dd2575356a77c3dd6e6315ca7b66`의 **9행**에서 과거 v30이 이미 `anvil`, `chipped_anvil`, `damaged_anvil` 3 leaf 원본 JSON을 읽었다고 기록. v63 두 모델은 **새로 복원된 선택 원장 증거 및 실제 재확인**이지 최초 연구가 아님. v30 보고서 65행은 공통 #top UV와 leaf top PNG; v64 전체 PNG 원본 Pillow 신규 검증 0. 새 모델 원본 JSON 읽기0.
- P1 원장 **544행×330열**, v63 325열/544행 **176,800 기존 데이터셀 동일**. `04_SOURCE_REVIEW_LEDGER_544.csv`는 544×33열 (v63 30열 기존 **16,320 데이터셀 동일**). v30 MD 근거 4개 기존 모델행만 보강. v35~v63 명시 direct JSON read 516, 역사 SHA만28, 전부 P1 path SHA 식별544/544. **실제 기하·UV·PNG·렌더러 연구 완료율 아님**.
- 다음 우선: 나머지113 원본 CSV가 최신 P1 544개 path SHA에 제공할 실제 행별 증거 파악. SQLite4는 v47에 DB 선행 B-tree 검수 기록 있으니 동일 검증 중복이 아니라 새 오탐/결론 확인 위주. `asset_type+full_source_path+git_blob_sha` 복합키, 문서 내용이 원본 모델 SHA 인증은 아니라는 경계 유지.
- 1-1 승인150/150·상위1/5완료, **1-2-A·1-2 진행 중·정확한 완료율 미산정**. 변환/가구 제작 시작하지 않기. 연구 커밋 이후 GitHub remote SHA/CSV preservation 검증, 별도 validation commit 수행.
