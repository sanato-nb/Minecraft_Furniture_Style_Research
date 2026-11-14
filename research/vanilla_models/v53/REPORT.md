# v53 — 1-2-A: P1 544개 모델 원본 경로·SHA 연결 범위 전수 확보

> 2026-11-14 KST · 연구 시작 당시 GitHub `main` HEAD `2fd4930a3432974d41bc0facd1ed8e0bd070fab5` · Minecraft Java Edition 1.21.11 사용자 제공 추출 자산. v1~v52 기존 파일 수정·삭제 없이 기존 증거를 이어받았다.

## 1. 이번 회차의 원본 직접 분석 결과

v52의 P1 전체 **544개** 원장에서 직접 경로·SHA 연결 **369개**와 미연결 **175개**를 정확히 분리했다. 미연결 175개 원본 `1.21.11/assets/minecraft/models/block/*.json`을 GitHub에서 하나씩 직접 읽고 각 파일의 `git_blob_sha`를 기존 원장과 교차 대조하여 **175개 전부 일치**. 동일 `(asset_type,full_source_path,git_blob_sha)` 중복은 **0건**. v53 누적 **544/544**, 미연결 **0건**.

| 직접 확인한 원본 P1 계열 | 신규 경로 |
|---|---:|
| 14색 × (촛불 1~4개, lit/unlit, 촛불 케이크 lit/unlit) | 140 |
| 색상별 셜커 상자 | 13 |
| 색상별 카펫 | 12 |
| 피스톤 헤드·템플릿 6, 피뢰침 3, skull 1 | 10 |
| **v53 신규 정확한 원본 JSON SHA 연결** | **175** |

이 수치는 **모델의 원본 경로+SHA 신원 근거를 P1 전체에 연결했다는 뜻**이지, 544개 모델의 기하·UV·PNG·블록상태·특수 렌더러 전체 연구 완료 또는 2,390개의 모든 block model 검수 완료가 아니다. 기존 v1~v52의 역사적 의미론적 자료를 완전히 재검수했다고도 주장하지 않는다. 본 회차의 신규 실적은 '이전 v52 원장에서 미연결 상태였던 원본 JSON 175개의 새 직접 검사'로 한정한다.

## 2. 실제 원본 선언과 상속 기하·UV를 분리

- **신규 175개 원본 JSON에 자신이 선언한 기하**: `template_piston_head.json` 및 `template_piston_head_short.json` 각각 **2요소·10면**, 총 **4개 원본 elements / 20개 원본 faces**, 명시 UV **20**, 암시 UV **0**. 나머지 173개는 해당 JSON 자체 요소 선언이 없다.
- **상속 포함 175모델별 적용 면 참조**: **3,413건**, 기존 원본 기하의 명시 UV 출처 **3,245건**, 원본 UV 키가 없는 암시 UV 출처 **168건**. 암시 UV 면에 임의의 실제 검증 UV 좌표를 추가하지 않았다.
- 회전 요소 적용 **616건**, 축 방향 0두께 요소 적용 **616건**. 이 수치는 **원본 고유 요소 수가 아니라 자식 모델에 반복 적용되는 요소 참조 수**다.
- 161모델에 부모 또는 자체 JSON 기하를 추적할 수 있었다. 남은 **14모델(셜커 상자 13, skull 1)**은 원본 JSON에서 parent/elements가 모두 없어 입체 기하가 JSON만으로 판정되지 않으므로 **특수 렌더러 미검증**으로 보류.
- 텍스처 슬롯 미해결 적용면 참조 **20건**은 두 피스톤 독립 템플릿의 플레이스홀더에서 발생했다. 실제 자식 leaf의 오류라고 확정하지 않는다.
- `template_candle`, `template_two_candles`, `template_three_candles`, `template_four_candles`, `template_cake_with_candle`, `carpet` 등 v50~v52에서 검사한 원본 부모 기하·UV를 재사용했다. **재사용한 원형을 신규 4요소/20면에 합산하지 않았다**. 이번에 새로 연 `template_lightning_rod` 원본 2요소·11면은 별도 P1 외 부모 교차 대조이며 P1 신규 원본 4요소/20면에 더하지 않는다.

## 3. 블록상태와 정적 조합의 단위

실제 GitHub 원본 blockstates **8파일**을 검사해 `variants` 키 **58건**, model apply 선택지 **58건**, 새 확인 `multipart` 규칙 **0건**을 별도로 기록했다. 대표적으로 brown_candle 8, brown_candle_cake 2, cyan_candle 8, green_candle_cake 2, exposed_lightning_rod 12, piston_head 24, brown_shulker_box 1, brown_carpet 1. 원본 `template_lightning_rod` 부모 모델 JSON 1개를 별도로 읽었다. `blockstates/skull.json`을 정확히 조회했을 때 404였지만 다른 유형의 블록상태 또는 특수 렌더러 처리 가능성을 배제하지 않는다. 58을 전체 blockstate 정적 조합의 완료량으로 오인하지 않는다.

## 4. 새 PNG 바이너리 직접 읽기, SHA 및 RGBA

GitHub Contents API의 Base64 응답에서 **실제 PNG 바이트**를 확보했고, 독립 실행 환경의 Python에서 **Git blob SHA-1을 원본 바이트로 재계산**해 일치 확인했다. Pillow로 각 원본 PNG를 RGBA 해독하여 총 **4개 파일 × 256 = 1,024 원본 픽셀**을 측정했다.

| PNG | 원본 SHA(앞 12자) | 불투명 | 완전 투명 | 부분 알파 |
|---|---|---:|---:|---:|
| `brown_candle.png` | `c1577328cafc` | 21 | 235 | 0 |
| `cyan_candle_lit.png` | `c1a9cc2b9d94` | 21 | 235 | 0 |
| `purple_wool.png` | `89964f6fc77c` | 256 | 0 | 0 |
| `lightning_rod.png` | `5c9a13d7145b` | 40 | 216 | 0 |

3,413건 상속 적용 면 가운데 **226건**은 이번에 실제 바이너리를 확인한 4개 PNG의 경로로 연결된다. 하지만 **226건 모두 각 면의 UV 좌표로 실제 텍셀을 측정했다는 뜻은 아니며 새 face UV texel 샘플링은 0건**이다.

## 5. 기존 자료 계승 / 보류 / 연구 경계

- 이전 v52까지 경로+SHA 연결 369개는 그대로 보존; 전체 544행에서 신규 175행에만 새 경로 연결 값을 추가했다. v52 원장은 변경하지 않았다.
- 과거 원본 기하 템플릿은 **상속 적용만 새로 계산**, 새로운 기하 원형으로 재집계하지 않는다.
- **P1 경로·SHA 544/544 확보**와 **1-2-A 역사적 의미론 근거 통합 및 1-2-B/C/D 기하·UV·PNG·blockstate·렌더러 완료**는 서로 다른 목표다.
- 이 회차 이후도 **1-2-A 및 1-2 전체 진행 중**, 실질적 전체 완료율 **미산정**. **1-1 승인된 150/150 완료**, 상위 5개 과제 중 **1/5 완료** 그대로 유지.
- 실제 마인크래프트 가구 모델 제작·Project Zomboid 가구 변환은 시작하지 않았다. Mojang 공식 압축 JAR 인증·인게임 렌더 검증은 수행한 것으로 주장하지 않는다.

## 6. 결과 원장

- [P1 544행 v53 원장](01_P1_544_EVIDENCE_LEDGER.csv), [신규 정확 신원 175 CSV](02_NEW_P1_175_TYPED_SOURCE_EVIDENCE.csv), [원본 JSON 175](03_ORIGINAL_MODEL_JSON_175.json), [모델별 원형/UV 175](04_PER_MODEL_175_GEOMETRY_UV_STATUS.csv)
- [상속 면 3413](05_EFFECTIVE_FACE_APPLICATIONS_3413.csv), [신규 원본 요소 4](06_ORIGINAL_SOURCE_ELEMENTS_4.csv), [신규 원본 면 20](07_ORIGINAL_SOURCE_FACES_20.csv), [블록상태·부모 10회 조회](08_ORIGINAL_BLOCKSTATES_AND_PARENT_10.json), [PNG RGBA 4종](10_ORIGINAL_PNG_RGBA_4.json)
- [보류사항](11_ISSUES.json), [원본/상속 수치 검증](12_MODEL_GEOMETRY_METRICS.json), [다음 채팅 인수인계](NEXT_CHAT_HANDOFF.md)
