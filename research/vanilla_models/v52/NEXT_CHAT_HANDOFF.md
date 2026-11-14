# v52 — 다음 채팅 시작 / 정확한 1-2-A 인수인계

1. **GitHub `main`의 실제 최신 SHA부터 조회**; 현재 문서보다 v53 이상이 있다면 그 버전을 우선한다. `handoff/STATE.json`, `research/vanilla_models/v52/SUMMARY.json`, `REPORT.md`, `VALIDATION_POST_RESEARCH_COMMIT.json`을 읽는다.
2. P1 block model JSON **544개**, v51 **335개 SHA 연결**, v52 새 **34개** 원본 JSON·SHA 정확 연결 → **369개**, 현재 근거에서 미연결 **175개**. Git Blob API로 `01_P1_544_EVIDENCE_LEDGER.csv` 원문 **544행**을 읽는다(Contents API는 1MB 초과 시 빈 내용 반환 가능). 기존 v51의 132개 열은 보존했다.
3. v52 신규 34개 원본 JSON은 `03_ORIGINAL_MODEL_JSON_34.json`, provenance와 SHA는 `02_NEW_P1_34_TYPED_SOURCE_EVIDENCE.csv`. blue candle 10, shulker 2, carpets 4, torches/templates, eggs/sea pickles 및 note block. 기존 부모 geometry 재활용은 신규 source 원형 실적에 중복 포함하지 않는다.
4. **고유 원본 자체 선언** = 23 elements / 60 faces (원본 UV 명시60, 암시0). **상속 포함 모델별 면 적용** = 394 (명시 UV 출처376, 암시 UV 출처18), 42 standalone template unresolved texture slot refs. 원본/상속/계산/검증 단위는 별도로 유지. 부모는 `09_PARENT_SOURCE_REFERENCE_7.json`, `09_ADDITIONAL_PARENT_SOURCE_5.json`.
5. 원본 **9 blockstate JSON / 43 variant 키 / 103 variant array alternative apply records / 0 multipart**. 103을 103개의 독립 static game states로 단정 금지.
6. **새 PNG 바이트 확보 성공**: Contents API `fetch_file(encoding=base64)` 사용, Git blob SHA1 직접 재계산, Pillow RGBA 원본 4개·총 1,024픽셀 실측. `10_ORIGINAL_PNG_RGBA_4.json`에 원본 파일별 alpha 집계. 이 중 158 face refs가 검증된 PNG *경로*를 가리키지만 실제 UV face texel 검사 0. 다른 PNG도 같은 방식으로 점진 확대.
7. particle-only `black_shulker_box`, `blue_shulker_box`의 실제 renderer 기하는 미확인. 템플릿 단독 42개의 미해결 슬롯은 leaf 오류라는 증거가 아니다. 기타 보류는 `11_ISSUES.csv`와 REPORT 참조.
8. 미연결 **175개** 중 색상 촛불 leaf / 셜커·카펫·특수 장식 나머지 우선. v1~v51의 exact tuple `(asset_type,full_source_path,git_blob_sha)`를 찾아 역사적 근거는 별도로 회수; 새 원본 직접 조사로 중복 계산 금지.
9. 다음 회차는 변경 전/커밋 직전 main HEAD 확인, 새 버전 별도 폴더 추가, GitHub 저장 후 blob SHA/544행/카운트/유형별 참조 검증, top-level 인수인계 갱신. **1-1 승인150/150 완료·상위1/5 유지, 1-2 미완료/실질완료율 미산정**, 실제 마크 가구 제작/PZ 변환 시작 금지.
