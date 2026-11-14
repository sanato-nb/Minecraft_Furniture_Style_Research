# v48 다음 채팅 인수인계 — 1-2-A 계속

- 먼저 GitHub `main`의 **실제 HEAD**, `handoff/STATE.json`, `research/vanilla_models/v48/REPORT.md` / `SUMMARY.json` / `01_P1_544_EVIDENCE_LEDGER.csv` 재열람. 과거 v47의 135/409 수치를 현재 상태로 쓰지 말 것.
- **현재 P1 544 모델 경로 / SHA 연결 171 / 이번 조사 출처에서 미연결 373**. SHA 연결 = 기하/UV/PNG/런타임 전체 완료가 아님. 미연결 373 = 미연구 확정 아님.
- v48에서 새로 원본 모델 JSON 직접 읽은 P1 **36경로**: birch/cherry shelf 14, chiseled_bookshelf leaf/inventory 10, 기타 copper_lantern/torch·item_frame/glow·jukebox·conduit 9, 별도로 P1 미연결이었던 부모 template_shelf_inventory + template_item_frame + template_item_frame_map 3. 위 부모의 이전 기하 연구는 중복금지.
- 직접 확인한 부모 소스 **20개** 중 이전에 P1 SHA 연결 14, 이번 신규 P1 연결 3, P1 모집단 외 공통 부모 3. 현회차 원본 요소 14 / 원본 명시 UV 선언면 68; v38 기존 template_shelf_inventory 원형 3요소/18면 재검수 분리. 나머지 11요소/50면은 이번 직접 소스 실측. leaf의 상속면을 새 원본 선언으로 계산하지 말 것.
- 원본 multipart: birch_shelf 24규칙/파생32 상태/64 적용, cherry_shelf 24/32/64, chiseled_bookshelf 52/256/1792. 세 모델 합계 원본규칙 100, 파생상태 320, 모델 적용 1920. 조각된 책장 원본 uvlock 키는 4규칙. 그 외 6개 blockstate 원본 variant 합계 9규칙 확인. **게임 런타임 상태/렌더를 실제 확인하지 않음**.
- `conduit.json` particle-only; 렌더러 직접 검증 필요. 아이템 액자 관련 parent template source는 기하 선언이 있으나 실제 아이템/지도 엔진 렌더는 미확인.
- v47까지 계승: v5-v8 SQLite 4개+scripts4, 역사 CSV133, Markdown30+JSON19, SHA 공유 그룹 2개/모델 7경로, v43의 자산 타입 충돌 2건 정정. 과거 실적 신규로 다시 계산하지 말 것.
- 후속 우선: 남은 P1 미연결 373경로에서 실제 설계 가치가 높은 가구와 조명 family 원본 JSON을 확인. 기존 source geometry/UV 선언과 실제 PNG 화소를 별개 원장으로 연결. 완전한 과거 간접 근거 및 특수 렌더 예외 조사 계속.
- `(asset_type,full_source_path,git_blob_sha)` 복합키. 전체 1-2 완료율 미산정, 1-2-A 미완료, 상위 과제 1/5 완료·1-1 v42 150/150 승인 소스 완료 보존. Minecraft 가구 실제 제작/PZ 전환 보류.
