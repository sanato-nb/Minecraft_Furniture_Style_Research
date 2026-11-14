# Minecraft Furniture Style Research — v53 1-2-A 다음 채팅 인수인계

1. 가장 먼저 GitHub `main` HEAD를 조회하고 `handoff/STATE.json`, `research/vanilla_models/v53/REPORT.md`, `SUMMARY.json`, `VALIDATION_POST_RESEARCH_COMMIT.json`, `01_P1_544_EVIDENCE_LEDGER.csv`를 읽는다. v54+가 있다면 최신 우선. 1MB 초과 원장은 Contents API가 빈 본문을 반환할 수 있어 **Git Blob API**를 사용할 것.
2. **P1 544 경로 전부 path+SHA 연결**: v52 **369**, v53 새 직접 원본 **175**, 합계 **544/544**, 현재 P1 미연결 **0**. 175 모두 원본 JSON 직접 읽기와 v52 원장 Git blob SHA가 일치. 과거의 모든 의미론적 연구 기록을 전수 검색했다고 주장하지 않음. 식별키 `(asset_type,full_source_path,git_blob_sha)` 필수.
3. 175개 분류: 촛불/케이크140, 셜커13, 카펫12, 피스톤6·피뢰침3·해골1. 실제 원본 175 JSON은 `03_ORIGINAL_MODEL_JSON_175.json`, 배치별 원본 파일은 `03_ORIGINAL_MODELS_BATCH_01..16.json`. 544 원장은 v52의 152열을 보존하고 v53 열을 추가.
4. 175개 **자체 선언** 4 elements/20 faces(명시 UV20, 암시0), 두 피스톤 원본 템플릿만 해당. **상속 적용** 3,413 face refs (원본 명시UV3,245/암시UV168). 회전 요소 적용616, 0두께 요소 적용616, 원본 고유요소 수로 중복 계산 금지. `04_PER_MODEL_175_GEOMETRY_UV_STATUS.csv` 및 `05_EFFECTIVE_FACE_APPLICATIONS_3413.csv` 참고.
5. 셜커 상자13와 skull1은 JSON에 parent/elements 없으므로 특수 renderer가 확인되기 전 입체형태 확정 불가. 두 피스톤 template 자체의 unresolved face texture slots 20은 leaf 오류로 자동 확정 금지. 원본 `blockstates/skull.json` 404는 다른 blockstate/renderer가 존재하지 않는다는 증거 아님.
6. 새로 읽은 blockstate 원본 **8파일·variants58·apply alternatives58·multipart0**, 비P1 부모 `template_lightning_rod` JSON1. 별도 source JSON 증거 `08_ORIGINAL_BLOCKSTATES_AND_PARENT_10.json`. 58을 전체 static state 조합 완료로 사용 금지.
7. PNG: `brown_candle.png`, `cyan_candle_lit.png`, `purple_wool.png`, `lightning_rod.png`, **4×16×16=1,024픽셀** 원본 바이트·Git SHA 및 Pillow RGBA 검증. 이번 확인한 PNG 파일로 해결되는 face texture path refs 226은 **면 UV 픽셀 실제 검증 226건이 아님**. Face UV 실제 픽셀검사 여전히 0. `10_ORIGINAL_PNG_RGBA_4.json`.
8. **우선 다음 일**: 전체 v1~v52 원본 의미론 근거 교차 통합 및 속성 중복 제거, 셜커/skull 특수 렌더러 source, piston template placeholder leaf 해결, 더 많은 원본 PNG·면별 UV 대응, 블록상태 원본 커버리지. 비P1 나머지 block models 1,846개도 모집단에서 제외됐을 뿐 완료가 아님.
9. 연구 버전 추가 전/직전 최신 main HEAD 조회, 동시작업 변경사항 보존, commit 후 실제 GitHub 544행/정확 SHA/파일 존재/상태/PNG 근거 역검증. **1-1 승인150/150 유지, 상위 1/5 완료 유지, 1-2-A 및 1-2 미완료·실질완료율 미산정**. 마인크래프트 가구 제작 및 PZ 변환 금지.
