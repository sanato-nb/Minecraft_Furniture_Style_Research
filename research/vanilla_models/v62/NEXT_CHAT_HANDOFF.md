# v62 → 다음 채팅: 역사 통합 중심 1-2-A 인수인계

1. 실제 GitHub `main` HEAD를 먼저 읽고 `research/vanilla_models/v62/{REPORT.md,SUMMARY.json,07_P1_544_EVIDENCE_LEDGER.csv,VALIDATION_POST_RESEARCH_COMMIT.json}` 검증. v62보다 최신이면 최신 우선.
2. 이번 회차 **새 원본 모델 깊이 판독 0개**. 대신 v44에서 남겨둔 과거 **21개 원본 CSV 파일의 Git SHA 원격 재조회 + 원본 176행 모델 SHA/이름/경로 확인**. 원본 CSV 중 동일 행에 typed model path+SHA **78링크**, 이름+SHA만 **98링크**, 544 모델 중 서로 다른 **110모델**에 해당. 이는 전체 v5~v43 스캔 완료가 아님.
3. **v44 증거 CSV 파일 SHA 기록 오류** 발견: v27 `research/vanilla_models/v27/02_oak_shelf_20_face_actual_png_rgba.csv`의 SHA가 v44 역사 링크 6개에서 마지막 글자 `3` 빠짐. 실제 원본 Git blob SHA `8f5a14694934da3306e2aa3c3ba10e9a22862ed3`, v44 기록 `8f5a14694934da3306e2aa3c3ba10e9a22862ed`. 원본 v44 파일은 그대로 유지; v62 `03_V44_EVIDENCE_CSV_SHA_ERRATA_6.csv`에 모델 6개와 정정값 보존. **모델 Git SHA 충돌이 아님.**
4. v35~v61 원장에 **명시된 직접 모델 JSON 판독 플래그**를 18개 필드 집합으로 정확히 중복 제거하면 **514/544모델**. 나머지 30모델 중 **28**은 검증한 역사 CSV 21개에서 행 SHA가 있고, 나머지 **2**(`chipped_anvil.json`, `damaged_anvil.json`)는 선택 근거에서 직접 플래그도 역사 SHA도 없음. **모두 원본 식별 경로 SHA는 기존 544/544.** 이 2개가 진짜 연구 미수행이라고 단정 금지.
5. v61 기존 P1 ledger **544×297 → v62 544×310**, 이전 297개 열×544개 data row **161,568셀 모두 동일**, 신규 13개 근거 열만 추가. `04_SOURCE_REVIEW_LEDGER_544.csv`에는 모든 544 모델을 일괄 근거 등급/참고 링크와 상태로 기록. `01_HISTORICAL_EVIDENCE_CROSSWALK_176.csv`는 역사 연결 raw v44 vs actual SHA separate.
6. v5~v43 원본 모든 CSV/MD/JSON/SQLite 등 전수 검증은 여전히 미완료, 공식 엔진 암시UV/렌더 특수예외 14건 미인증. 이번 작업은 소스 파일 SHA·원래 CSV 행 근거 재검증(원본 모델 JSON 자체를 신규로 다시 읽은 것 아님).
7. 다음 권장 작업: 21파일 외 과거 전체 증거 파일별 검토 범위를 목록화, 특히 old SQLite/MD/JSON/CSV source SHA 및 타입 경로 정확 대조. `chipped_anvil`, `damaged_anvil` 관련 별도 과거 근거 확인. 모델 타입/Full path/ Git blob SHA 3중키 유지, 증거 원장과 정정 파일 절대 삭제/덮어쓰기 금지. 실질 완료율 주장 금지.
8. 1-1 승인150/150 완료, 상위 1/5 완료, 1-2-A/1-2 진행중, 가구 제작·좀보이드 변환 금지. 새 작업 후 HEAD optimistic lease commit, 원격 readback, validation follow-up commit.
