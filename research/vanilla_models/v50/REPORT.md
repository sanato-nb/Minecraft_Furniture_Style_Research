# v50 — 1-2-A 촛불·케이크·표지판·구리 조명/수납 계열 P1 원본 경로 검증

> 2026-11-14 KST · 시작 HEAD `30430db39c83251f2dff060f3fb7120222fee81e` · 사용자 제공 Minecraft Java Edition **1.21.11** `1.21.11/assets/minecraft` 추출본을 직접 조사. v1~v49의 연구 및 기존 SQLite/CSV/JSON을 덮어쓰지 않음.

## 실제 신규 원본 조사
v49 P1 544행 원장에서 원본 경로+SHA 근거가 미연결인 모델을 우선 선택. **50개 block model JSON 원문을 실제로 조회**, 각 파일의 정확한 `assets/minecraft/models/block` 경로와 Git blob SHA를 v49 모델별 원장에 대조하여 **50/50 정확히 일치**했다. 추가로 촛불/횃불 상속을 검증하다 확인한 P1 미연결 부모 `template_torch_wall.json`을 직접 읽어 **51번째 독립 모델 경로+SHA 연결**로 등록했다.

이 51개 직접 소스 경로에서 관찰한 기하 구조는 다음처럼 나뉜다.
- **22개**: `parent`·`elements` 선언 없이 `textures.particle`만 기술. 대표적으로 여러 목재 `sign/hanging_sign`, 산화 단계별 구리 `chest`. 이 JSON은 실제 3D 메시를 증명하지 않는다. 특수 렌더러의 구체적인 구현까지 확인했다고 주장하지 않음.
- **27개**: 자체 `elements` 선언 없이 부모 모델 JSON을 상속. 검은 촛불/케이크, 일반 촛불 lit leaf, campfire, copper lantern, wall torch, jack-o-lantern, sea lantern 포함.
- **2개**: 직접 요소 선언. `template_cake_with_candle` **4 elements/16 선언면(명시 UV 10·암시 UV 6)**, `template_torch_wall` **1 element/6 선언면(명시 UV 6)**. **총 5개 원본 자체 요소/22 원본 선언면**.

## 원본 부모·텍스처·UV 연결
상속/텍스처 슬롯 검증을 위해 사용된 부모 모델 JSON **11개를 직접 열람**하고, 연속 상속 `orientable_with_bottom`, `cube`, `block` 3개도 확인. 부모 source의 원본 SHA를 기록한 후 각 leaf의 source `textures` override를 상속 체인에 순서대로 적용했다.

그 결과, 51개 모델에서 실제로 대응시킨 **원본 기하 선언면의 leaf 적용 건수 561건**(소스 명시 UV **519**, 소스 UV 키 부재 **42**). 이것은 **561개의 고유 source face 선언이 아니다**. `template_cake_with_candle` 자체에서는 텍스처 슬롯 10면, `template_torch_wall` 자체에서는 6면이 아직 leaf 오버라이드되지 않은 `#slot` 참조로 남았다. 이 **16건은 템플릿 자체의 미결합 슬롯**이며, 자식 오버라이드 및 게임 런타임이 잘못되었다는 판정이 아니다. 원본 PNG RGBA 픽셀은 이번에도 0개 조사.

v48에서 이미 원본이 확인된 `template_lantern`과 `template_hanging_lantern`의 **기존 Git blob SHA 2개가 동일**함을 재확인하고, 동일 기하 원형을 새로 발견한 것처럼 재계산하지 않았다. v35에서 원본 `cake`와 `cake_slice1..6`을 확인한 이력은 `template_cake_with_candle`의 동일 source path+SHA를 확인한 이력이 아니므로 합치지 않았다.

## 35개 원본 블록상태 직접 검증
원본 `blockstates/*.json` **35개 파일을 직접 열람**해 Git blob SHA를 남겼다. 이들의 **원본 variants 규칙 합계는 74개**, multipart 규칙은 0개다. 선택 모델 51경로 중 템플릿 2개를 제외한 **49개**가 이 조사된 블록상태 원본의 `model` 참조에 직접 등장했다. 상태 파일에서 참조되는 고유 모델 ID는 총 **55개**로, 범위 밖 모델 ID도 포함된다.

원본 확인 사례:
- `black_candle`: `candles` 개수와 `lit`을 조합하는 원본 variants **8개**. `black_candle_cake`: 원본 **2개**.
- `candle`: variants **8개**, `candle_cake`: **2개**. `campfire`, `soul_campfire`: **각 8개** (off 모델도 참조됨).
- 산화 단계별 구리 상자 4개 블록상태: **각 1개**의 JSON variant와 particle-only 블록 모델을 연결.
- 산화 단계별 구리 랜턴 3개 블록상태: **각 2개**의 일반형/매달린 원본 모델 참조.
- 9개 목재 × 서 있는 표지판/매달린 표지판의 18개 블록상태: **각 단일 원본 variant**. 해당 block model JSON은 particle-only라 실제 표지판 메시 모양은 미검증.

74는 원본에 선언된 variant 항목 수이며 전부 실제 엔진에서 도달 가능한지 또는 실제 렌더러가 동일한지 검증한 건수가 아니다.

## v49 → v50 연결 범위

| 지표 | v49 | v50 |
|---|---:|---:|
| P1 모델 모집단 (경로) | 544 | **544** |
| 모델 출처 경로+SHA 연결 | 230 | **281** |
| 선택 증거에서 경로+SHA 미연결 | 314 | **263** |
| 이번 새로 원본 모델 JSON 직접 읽은 P1 경로 | 53 (6개 과거 재연결 별도) | **51** |
| 직접 확인한 자체 원본 요소/선언면 | 30/106 | **5/22** |
| 본 회차 소스 면의 leaf 적용 건수 | 978 화분 +114 선반 | **561** |
| 새 원본 PNG RGBA 픽셀 측정 | 0 | **0** |
| 전체 1-2 완전 연구 완료율 | 미산정 | **미산정** |

이번 **51개는 완전한 기하+UV+PNG+blockstate+특수 렌더 분석이 완료된 모델 수가 아니다**. 263개 또한 한 번도 연구되지 않은 모델이라는 확정 증거가 아니다. 정확한 비교 키는 계속 `(asset_type, full_source_path, git_blob_sha)`이며, v43 자산 타입 오탐과 v46 동일 SHA 다른 경로 오탐은 재발시키지 않았다.

## 미해결 및 금지 사항
- 표지판·상자 등 22 source particle-only 경로의 실제 메시/블록엔티티 렌더러는 **미검증**.
- 암시 UV 적용 42건은 원본 JSON의 UV 키 부재를 유지했다. PNG와 실제 texel/알파 대응은 **미검증**.
- v1–v49 역사 간접 근거 의미론적 전수 일치 검사는 완료 선언하지 않음. 원본 PNG 및 런타임 연구 완료 주장 금지.
- v42에서 완료된 **1-1 승인 텍스처 150/150** 완료 유지. 전체 상위 과제 **1/5 완료**, 1-2-A 진행 중 및 1-2 전체 완료율 **미산정**. 실제 Minecraft 가구 모델 제작과 Project Zomboid 변환은 이 범위 밖이며 수행하지 않음.
- 공식 압축 client.jar 인증 및 인게임 렌더 검증은 사용자 지정 필수 완료 조건에서 제외되었고 실제로 하지 않았다.

## 산출물
`01_P1_544_EVIDENCE_LEDGER.csv`, `02_NEW_51_P1_DIRECT_SOURCE_EVIDENCE.csv`, `03_SOURCE_FACE_APPLICATIONS_561.csv`, `04_PARENT_TEMPLATES_11_SOURCE.json`, `05_PARENT_CHAIN_3_SOURCE.json`, `06_ORIGINAL_BLOCKSTATES_35_SUMMARY.csv`, `07_ORIGINAL_BLOCKSTATE_VARIANTS_74.csv`, `08_ORIGINAL_BLOCKSTATES_35_RAW.json`, `09_MODEL_STATE_51_CROSSWALK.csv`, `10_HISTORICAL_REUSE_AUDIT.json`, `11_ISSUES.csv`, `12_BATCH1_SOURCE_MODELS_10.json` ~ `16_BATCH5_SOURCE_MODELS_10.json`, `SUMMARY.json`, `REPORT.md`, `NEXT_CHAT_HANDOFF.md`.
