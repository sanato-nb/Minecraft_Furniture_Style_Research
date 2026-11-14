# Minecraft Furniture Style Research — v47 인수인계 (1-2-A 계속)

## 먼저 확인
1. GitHub `main` **실시간 최신 HEAD** 조회, `handoff/STATE.json` 검사.
2. `research/vanilla_models/v47/REPORT.md`, `SUMMARY.json`, `01_P1_544_EVIDENCE_LEDGER.csv` 및 `11_ISSUES.csv` 원본 재열람.
3. 과거 버전의 '현재 v46/124 연결'은 이전 체크포인트이며 **v47: 135 연결 / 409 미연결**을 기본으로 하되 현재 SHA가 바뀌었으면 우선 반영.

## 중복금지 기준
- P1 544 모델 **경로** 중 **135 source path+SHA 연결**. 완전한 1-2 연구 완료 수가 아님. 409는 조사한 출처에서 미연결, 미연구 확정 아님.
- 지난 v46: v5~v43 Markdown30/JSON19, 최근 CSV30, 과거 CSV17+86 조사 계승. v47: **v5~v8 실제 SQLite4를 직접 디코딩**해 5/10/16/20개 테이블의 실제 행 조사. 전체 **53개 고유 P1 모델 출처 SHA 연결**, 모두 이미 v46에 포함 → 신규 모델 0. `build_v5..v8.py` 4개 직접 확인, 중복 SHA 출현이 새 연구 완료를 뜻하지 않음. 53 모델별 DB 근거는 `08_LEGACY_SQLITE_53_P1_CROSSWALK.csv`.
- 이번 직접 신규 P1 원본 **11개**: `bamboo_shelf*` 7 leaf는 v38/v45 7개 부모 원형과 동일 SHA이므로 새 기하 원형을 더하지 말 것. bamboo 상태 원본 **24 multipart**, 파생 **32조합/64 모델 적용**.
- `flower_pot_cross`, `flower_pot_cross_emissive`, `tinted_flower_pot_cross`, `beacon`: 직접 JSON 요소 **26개/원본 명시 UV faces 100개**, 0두께/회전 요소 8개씩. 템플릿 `#plant`과 `#cross_emissive` 면 참조는 leaf override 필요. potted child 원본 6개 확인했으나 **P1 11개 실적에 추가하지 않음**.
- **PNG RGBA 신규 0**, 실제 게임 renderer/beam/engine/공식 압축 JAR 검증 0. 다음에는 모델 leaf별 실사용 textures/blockstate/PNG 픽셀을 정밀하게 연결하되 P1 증거 연결과 심층 완료율을 섞지 말 것.
- `(asset_type,full_source_path,git_blob_sha)`를 키로 사용. v46 동일 SHA 다중 경로 그룹 2건(7경로), v43 model vs blockstate 오탐 2건은 분리 유지.
- **1-2-A 아직 미완료**, 1-2 전체 완료율 미산정, 1-1 v42 150/150 완료 및 전체 상위 5과제 중 1개 완료 유지. 실제 Minecraft 가구 제작/PZ 변환 시작 금지.
