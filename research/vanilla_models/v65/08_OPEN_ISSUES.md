# v65 — 남은 문제 및 과잉완료 판정 방지

1. **V65-E01 — 역사 원본 콘텐츠 194/194 재조회 ≠ 의미론 전수 확정.** v62~v65 선택 작업으로 v5~v43 과거 21폴더·194파일을 실제 열었으나 CSV 메타·SHA·행 구조, SQLite 정적 B-tree, MD/JSON/Python 원문을 검토한 범위에 한정. 예전 모든 정량 결론을 독립 재실측한 것은 아님.
2. **V65-E02 — SQLite PRAGMA 전수 무결성 확인 미실행.** 4개 원본 파일 Git SHA·전체 바이트 복원, 페이지 수·root page 순회와 정적 레코드 수 확인. 실제 sqlite3 `PRAGMA integrity_check`, 추가 SQL 질의, 모델 JSON 정합성 조인은 이번 라운드 미실행.
3. **V65-E03 — 동일 원본 Git SHA가 모델 경로 7개에 중복.** 2그룹 SHA: `00c837...`(bamboo_sign, bamboo_hanging_sign), `9406a849...`(banner, bed, chest, oak_sign, trapped_chest). blob SHA만으로 연결하면 오탐; 반드시 `asset_type+full_source_path+git_blob_sha`.
4. **V65-E04 — 원본 CSV 113개 중 80개에는 P1 원본 SHA 단독 완전 셀 미발견.** 역사 CSV에는 텍스처/UV 픽셀 등 유용한 자료가 있을 수 있으므로 '원본 미연구' 표시 금지. SHA-only 또는 같은 행 이름·path가 없는 링크는 모델 의미론 근거 승격 보류.
5. **V65-E05 — 과거 3개 전체 모델 인벤토리와 역사 중복.** v34 2390 모델 경로/SHA 및 v36 P1 544 crosswalk는 모두 기존 신원 근거이므로, 이번 v65 230개 비인벤토리 모델×파일 쌍에 집계하지 않음. `template_shelf_inventory`의 이전 선택 교차표 외 1개는 기존 P1 식별모델의 과거 경로 확인일 뿐 신원 신규0·기하 신규0.
6. **V65-E06 — 원본 모델 JSON 직접 검토/PNG 픽셀 검증 확대 없음.** 직접판독 표시516개 그대로, 나머지28 역사 SHA근거만. PNG 전체 RGBA 새 검증0, blockstate/공식 엔진 모델 동작 새 인증0, 14개 특수 렌더러/암시 UV UVLOCK 미해결.
7. **V65-E07 — v44 증거 CSV SHA 오기6링크 정정 역사 보존.** v62의 원본 v44 메타데이터 SHA 누락 한 글자 관련; 모델 Git SHA 충돌 이슈와 별개. 원본 과거 v1~v64 파일 덮어쓰기 금지.
8. **V65-E08 — 실제 1-2-A 완료율 불명.** 1-1 승인150/150, 상위1/5, 1-2-A·1-2 진행중. 모델 제작/좀보이드 맵 변환은 시작하지 않음.
