# v66 — 잔여 이슈 / 완료 범위 구분

- **V66-01 P1 직접 JSON 조회 544/544 vs 실질 모델링 검증:** 과거 기존516 + 이번 28의 원본 JSON SHA/구문/자체 elements/faces 확인으로 직접 조회 근거 전 경로 확보. 그러나 13/28 자체 elements0처럼 부모 상속·블록 엔티티 특수 렌더러가 별도이며 P1 544개 전부의 원본 기하·UV·PNG·state를 심층 인증한 건 아님.
- **V66-02 암시UV 148면:** v33/02 원본 JSON 12개와 기하 공식 재계산 모두 148/148 일치. 다만 원본 face UV 자체는 148면 모두 미기재. 엔진 원본 UV 생성 알고리즘/실제 렌더 인증 미실시. '계산한 후보' 등급을 유지.
- **V66-03 선반 38면 vs 월드 16면:** v38의 38 original explicit UV faces 중 inventory-only 18은 `oak_shelf.json` 월드 multipart 원본 규칙24개의 apply 모델에 포함되지 않음. 32 정적 조합마다 본체15+상태 덧붙임1 = source face instances16; 실제 렌더의 노출 면 수 확정 아님.
- **V66-04 v38 PNG 픽셀 원본 미재측정:** oak_shelf.png SHA/IHDR 32×32와 과거 파일의 UV 픽셀 경계/면적·alpha합 산술은 검증. 완전한 RGBA 픽셀 Pillow 신규 실측0, 과거 v38 실측 수치 역사 근거만 유지.
- **V66-05 leaf별 SHA 대조 엄격 적용:** 과거 v38 38행은 모두 oak_shelf leaf가 아니라 oak_shelf_inventory 및 서로 다른 overlay leaf 7종을 포함함. 정확한 `leaf_name`과 모델 원본 SHA로 조인해야 38/38이 일치. 단일 oak_shelf SHA로 38행을 연결하면 23건 가짜 불일치가 발생하므로 해당 방식은 배제. 올바른 증거파일 `00_V38_OAK_SHELF_38_FACE_24_STATE_32_COMBINATIONS_RECHECK.json`.
- **V66-06 공식 렌더/상속/텍스처 완전성:** 특수 렌더러 예외14, 부모 material/model inheritance, 전 모델 최종 UV/PNG/블록상태 인게임 판정 계속 미완료. `source SHA == exact`는 해당 원본의 정체 근거이지 유일한 물체 형상/UV까지 인증하지 않음.
- **V66-07 이전 자료 보존 및 1-2-A 완료 상태:** 역사194파일 모든 원본 내용 재조회는 완료(v65)지만 전체 의미론 재검증은 미완료. v65 P1 544×337, source_review544×37 모든 기존 셀 보존. 1-1 승인150/150, 상위1/5, 1-2-A 미완료, 완료율 null, 가구 모델 제작/맵 변환 미시작.
