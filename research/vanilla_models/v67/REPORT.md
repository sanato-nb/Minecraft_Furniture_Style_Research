# v67 — 자체 요소 0 모델 13종의 원본 부모 상속·UV·blockstate 실제 검증

> Minecraft Java Edition 1.21.11 추출 원본 · 2026-11-15 KST · 시작 `main` 9c3ee2bf70ad7f2874f4facd9b85aa194a83803a. 1-2-A **진행 중**.

## 1. 범위와 기존 연구 중복 제거

v66에서 P1 원본 모델 544/544의 **JSON 직접 조회 이력**이 확보되었지만, 원본 자체의 elements=0인 개별 모델에 대한 실제 부모 기하·UV·블록상태는 별도 검증이 필요했다. v66의 이전 history-only 28개 중 **자체 원본 elements 0인 모델 13개**만 선별하여, 이번 회차에서 원본 모델 leaf 13개 + 실제 부모 JSON 8개 + 실제 blockstate JSON 9개를 GitHub 원본 경로에서 다시 직접 열고 Git blob SHA·원본 JSON 내용으로 대조했다.

**새 P1 모델 신원0 / 새로운 직접 JSON 조회 고유 모델0.** 이번 추가 성과는 **부모 상속 적용 내용과 UV·원본 블록상태 근거**이며, 기존 544/544 판독 이력을 신규 실적으로 중복 계상하지 않았다.

## 2. 검증된 원본 상속 기하

| 원본 leaf | leaf 자체 요소 | 검증된 상속 원본 요소 | 원본 적용 면 참조 | 원본 명시 UV | UV 누락 원본면 |
|---|---:|---:|---:|---:|---:|
| candle_one_candle | 0 | 3 | 10 | 10 | 0 |
| candle_two_candles | 0 | 6 | 20 | 20 | 0 |
| candle_three_candles | 0 | 9 | 30 | 30 | 0 |
| candle_four_candles | 0 | 12 | 40 | 40 | 0 |
| cartography_table | 0 | 1 | 6 | 0 | 6 |
| lightning_rod | 0 | 2 | 11 | 11 | 0 |
| lightning_rod_on | 0 | 2 | 11 | 11 | 0 |
| torch | 0 | 1 | 6 | 6 | 0 |
| decorated_pot | 0 | 0 | 0 | 0 | 0 |
| ender_chest | 0 | 0 | 0 | 0 | 0 |
| oak_hanging_sign | 0 | 0 | 0 | 0 | 0 |
| shulker_box | 0 | 0 | 0 | 0 | 0 |
| white_shulker_box | 0 | 0 | 0 | 0 | 0 |
| **모델 13개 적용 합계** | **0** | **36** | **134** | **128** | **6** |

상속을 포함한 실제 **소스 적용 면 참조 134개**는 8개 leaf 원형에 템플릿 면을 재사용한 수치이며, 새로 발견한 원본 고유 면 선언 134개가 아니다. 8개 모델의 합산에서는 **0두께 요소 적용 20건, 요소 회전 적용 20건**이 확인된다. 각 면의 원본 `from/to`, `rotation`, `cullface`, `tintindex`, `uv` 및 leaf 텍스처 슬롯 override를 `01_ORIGINAL_INHERITED_FACE_134.csv`에 보존했다.

부모 요소가 없는 모델 5개도 원본 blockstate에서 각각 모델 대상 참조를 확인했다. 따라서 **JSON elements=0이라고 게임에 물체가 보이지 않는다는 뜻이 아니다.** 별도 block-entity/특수 렌더러의 **실제 형상은 이번 분석에서 확인하지 못했다.**

## 3. 반드시 구분해야 할 UV 출처

원본 `cartography_table.json`은 `minecraft:block/cube`를 상속하고 큐브 부모는 `from:[0,0,0]`, `to:[16,16,16]` 하나의 요소와 여섯 면을 갖는다. **원본 여섯 면 모두 UV 필드가 없음**을 직접 확인했다. 전체 16단위 큐브라는 기하를 바탕으로 `[0,0,16,16]`을 **암시 UV 계산 후보**로 기록했다. 이것은 원본 명시 UV 여섯 면이 아니며 **Minecraft 1.21.11 렌더러의 암시 UV 공식이 인증됐다는 뜻도 아니다.**

그 외 128면은 실제 부모 모델에 명시된 `uv`를 leaf 모델에 적용한 참조. 기존 v33 계산 후보148면을 새 원본 명시 UV로 바꾸지 않았고, 이번 신규 후보 6면은 별도 모델에 속한다.

## 4. 원본 blockstate 및 texture PNG 근거

실제 원본 blockstate 9파일을 읽어 선택 leaf13개를 참조하는 **variant 항목 23건**을 찾아 원본 상태 키와 apply 모델/rotation을 `02_ORIGINAL_BLOCKSTATE_REFS_23.csv`에 기록. candles는 lit=false 4형태(원본 blockstate 전체8 variant 중 lit=true 4개는 이번 선택 leaf집합 외의 모델), lightning_rod는 facing×powered 12, torch/cartography_table 및 geometry0 5개는 각각 1건. 23개는 **선택 leaf 대상 blockstate 참조**, Minecraft 렌더 후 화면에 표시되는 면 수가 아니다.

면의 `#slot` 참조를 원본 leaf texture override로 해결하여 **134/134 원본 PNG 경로**를 확인했다. 중복 제거된 **9개 원본 PNG**에 대해 Git blob SHA와 원본 PNG 16×16 IHDR을 확인한 결과 대응이 모두 일치. `00_PNG_9_ORIGINAL_SOURCE_SHA_IHDR.json` 참조. **이번 신규 실제 RGBA 픽셀 전체 복호화0**, Pillow 교차검증0, 공식 엔진/게임 렌더 인증0. 예전 candle PNG 연구를 새 관측 픽셀 실적으로 다시 계산하지 않는다.

## 5. 실제 마인크래프트 가구 스타일에 대한 한정된 관찰

- **반복되는 부품 기하 사용:** 원본 candle 1~4개 모델은 각 템플릿이 elements 3→6→9→12, face refs 10→20→30→40으로 늘어난다. 모델 leaf는 자체 요소가 없는 텍스처 선택·부모 계승 형태다. 적어도 이 소스 모델군에서 반복·재사용이 관찰된다.
- **기하와 텍스처의 분담:** 지도 제작대는 단일 16단위 큐브 기하를 상속하고, 실제 면별 텍스처 경로를 leaf 슬롯으로 선택한다. 여섯 UV는 원본 명시가 아닌 후보 계산에 속한다.
- **동일 기하·다른 시각 상태:** lightning_rod/on은 같은 template 2요소11면을 상속하되 각 leaf가 서로 다른 원본 PNG 슬롯을 가리키고, powered 상태별 blockstate에 연결된다.
- **JSON 원본으로 형상을 확정할 수 없는 예외:** decorated_pot, ender_chest, oak_hanging_sign, shulker_box, white_shulker_box는 모델 JSON에서 기하 없음 및 blockstate target 확인까지만 관찰. 실제 형상을 이 정보로 추정 확정하지 않는다.

이것은 검증된 **표본 모델군의 관찰**일 뿐 모든 마인크래프트 가구에 적용되는 최종 스타일 규칙은 아니다.

## 6. 누적 원장 무결성 및 남은 연구

- P1 누적 증거 원장 **544행×351열 → 544행×365열**. v66 이전 **544×351=190,944 데이터 셀 변경 없음**.
- source review 원장 **544행×48열 → 544행×56열**. 이전 **544×48=26,112 데이터 셀 변경 없음**.
- 직접 원본 모델 JSON 판독 범위 **544/544 유지**, 원본 신원 연결 **544/544 유지**. 1-2-A 실질 완료율 산정 불가.
- v65의 194개 역사파일 내용 열람, v66의 148계산 후보 UV·선반38명시 UV 면 등 기존 기록을 모두 보존하고 이번 성과로 재계상하지 않았다.
- 실제 전 모델 상속/블록상태/PNG/특수 렌더러/암시 UV 엔진검증은 보류. 1-1 승인150/150, 상위 연구 1/5 완료, 1-2-A·1-2 미완료. 가구 모델 제작/좀보이드 맵 변환 미시작.

다음 실제 연구 체크포인트는 `NEXT_CHAT_HANDOFF.md` 참조. 사후 GitHub remote readback은 `VALIDATION_POST_RESEARCH_COMMIT.json` 기록.
