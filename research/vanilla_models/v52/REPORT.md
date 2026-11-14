# v52 — 1-2-A 원본 연구: 촛불·셜커 상자·카펫·횃불·거북알·해삼

> **2026-11-14 KST** · 대상 Minecraft Java 1.21.11 제공 추출본 · 시작 main HEAD `db84c29faf649b77dc21c5147449e2fd61d416d1`. v1~v51 연구 변경/삭제 없이 계승. 본 연구는 실제 GitHub 원본 JSON 및 일부 PNG 바이너리 직접 검증이다.

## 1. 정확한 출처와 누적 원장

P1 모집단 **544개**, v51 경로+SHA 연결 **335개**, v52 새 직접 원본 JSON·SHA 연결 **34개** = **369개**. 현재 검토된 증거에서 미연결 **175개**. 544개 원장과 기존 132개 열을 유지하고 v52 근거 열을 추가했다. 새 원본 34개 각각 `(block_model_json, 1.21.11/assets/minecraft/models/block/<name>.json, git_blob_sha)`를 v51 원장의 full source path/SHA와 교차검증했다. 과거 v1~v50의 모든 의미론적 기록을 전수 재검토했다는 뜻이 아니므로 '역사상 첫 연구'라 단정하지 않는다.

- **촛불·케이크**: blue candle lit/unlit, 개수 1~4 및 candle cake의 **10개 leaf**. 1~4개에 따라 `template_candle`, `template_two_candles`, `template_three_candles`, `template_four_candles`을 상속하며 케이크는 `template_cake_with_candle`에서 상속. 부모 자체의 face 선언은 leaf 신규 원형으로 세지 않는다.
- **셜커 상자**: 검정/파랑 2개 JSON에 `particle`만 있고 `parent/elements` 없음. 실제 렌더러의 기하/UV 미검증; 큐브로 추정 확정 금지.
- **카펫**: black/blue/red/white 4개가 v51에서 이미 검증한 `carpet` 부모 1요소·6면 재사용. 색별 `wool` 슬롯 override만 검증.
- **횃불**: 빨간돌 횃불 lit/unlit 벽/바닥 4개 및 `template_redstone_torch`, `template_redstone_torch_wall`, `template_torch_unlit`, `template_torch_wall_unlit` 신규 P1 원본 경로 4개. 일반 wall torch, soul torch, soul wall torch 포함. 벽 기울기 및 평면 요소를 JSON 키로 구별.
- **장식/가구 관련**: 거북알 3 leaf + `template_turtle_egg` 1, sea_pickle/dead_sea_pickle 2, note_block 1.

## 2. 기하·상속·UV의 서로 다른 단위

v52 **신규 P1 직접 원본 JSON 자체**: **23개 elements / 60개 face 선언**, 모든 60면 원본 명시 UV (암시 UV 0). 이전 연구의 `template_cake_with_candle` / `carpet` / `cube` 및 새로 교차 대조한 P1 외 부모 템플릿은 leaf 신규 원형으로 재집계하지 않았다.

**34개 대상 모델에 선언 원형을 상속 적용한 참조**: **394면 적용**, 원본 명시 UV 출처 **376건**, 암시 UV 출처 **18건**. 394는 원본 고유 face 선언 수가 아니다. 암시 UV는 원본 `uv` 키 부재를 기록하되 새 좌표를 계산해 확정하지 않았다. 적용 394건 중 42건은 독립 템플릿에서 자식 텍스처 override 없이 열어보았을 때의 unresolved slot이며 leaf 결함으로 간주하지 않는다. 실제 검증된 PNG 경로로 가는 적용면 참조 **158건**은 *텍스처 파일 출처 연결*이고, 개별 면별 UV RGBA 픽셀 샘플 검사 결과는 **0건**이다.

## 3. 원본 blockstates / PNG 직접 검사

원본 blockstates **9개 JSON**, `variants` 키 **43건**, 각 variant 값의 배열 요소까지 나눈 모델 적용 선택지 **103건**, 신규 검사된 `multipart` 규칙 **0건**. 103은 원본 규칙 수나 실제 게임 런타임 상태 수가 아니다. 예: blue candle은 candles(1~4)×lit(2) = 8 source variants; turtle_egg는 eggs(1~4)×hatch(3) = 12 source variants에 각 방향 모델 선택지, sea_pickle은 pickles(1~4)×waterlogged(2) = 8 source variants에 각 방향 선택지. 정적 원본 조건과 파생 계산/실제 렌더 상태를 혼동하지 않는다.

v51의 PNG 바이너리 UTF-8 읽기 실패 제한을 **GitHub Contents API Base64 원본 바이너리**로 해결했다. 각 원본 PNG의 Git blob SHA를 실제 바이트에서 재계산해 일치 확인했고, Pillow로 RGBA 변환해 총 **4×16×16 = 1,024개 원본 화소**를 측정했다:

| 원본 PNG | blob SHA | 불투명 | 완전 투명 | 부분 알파 |
|---|---|---:|---:|---:|
| blue_candle.png | `9fa29a8f34431e4c4ebbd08e63ba728174fa2555` | 21 | 235 | 0 |
| black_wool.png | `c38f621a89ed0e3038d1afd96201880ccca3b473` | 256 | 0 | 0 |
| redstone_torch.png | `56d3cf7013fb6459413c110ae768997713ab0f45` | 30 | 226 | 0 |
| sea_pickle.png | `c0585c3c1d32f12b0912f718ad53f718c05cf587` | 216 | 40 | 0 |

## 4. 보류 사항 및 과거 근거 계승

- **175개 미연결**: 추가 정확 경로/SHA 연결 필요. 역사적 CSV·MD·JSON·SQLite의 전체 교차 통합은 완료 주장 금지.
- **셜커 상자 2개**: particle-only 모델 JSON을 렌더러 기하와 동일시 금지.
- **템플릿 42개 적용면 참조**: leaf 텍스처 슬롯 지정 전의 unresolved 사례로 기록; 검증 실패 확정 아님.
- **PNG 실제 RGBA 1,024픽셀**은 성공했으나 면별 UV 텍셀 검사, 실제 게임 렌더 검사, 공식 Mojang 클라이언트 JAR SHA 인증은 이번에 하지 않았다.
- **1-2-A와 1-2 전체 미완료**, 전체 완료율 **미산정**. 1-1 기존 사용자 승인 **150/150 완료** 및 상위 5개 세부과제 **1/5 완료** 유지. Minecraft 실제 가구 제작·Project Zomboid 변환 시작하지 않음.

## 5. 결과 파일과 다음 작업

- [544 원장](01_P1_544_EVIDENCE_LEDGER.csv) · [새 P1 34개 SHA 근거](02_NEW_P1_34_TYPED_SOURCE_EVIDENCE.csv) · [34 원본 JSON](03_ORIGINAL_MODEL_JSON_34.json) · [34개 기하/UV 상태](04_PER_MODEL_34_GEOMETRY_UV_STATUS.csv)
- [394 면 참조](05_EFFECTIVE_FACE_APPLICATIONS_394.csv) · [원본 blockstates 9종](08_ORIGINAL_BLOCKSTATES_9.json) · [검사한 부모 7+5종](09_PARENT_SOURCE_REFERENCE_7.json) · [추가 부모5](09_ADDITIONAL_PARENT_SOURCE_5.json) · [PNG RGBA 4종](10_ORIGINAL_PNG_RGBA_4.json) · [이슈](11_ISSUES.csv) · [집계](12_METRICS_AUDIT.json)
- [다음 채팅 인수인계](NEXT_CHAT_HANDOFF.md)
