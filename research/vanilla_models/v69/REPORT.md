# v69 — 양조기 7개 원본 모델 × multipart 8상태 전수 조립·UV/텍스처 근거 분석

> 2026-11-15 · Minecraft Java 1.21.11 추출 원본. 연구 시작 `main` `475e1dd7715358aae76df91012a6bf8687cac0c9`. **1-2-A 진행 중/전체 모델 검증 완료 아님**.

## 1. 이전과 중복되지 않는 신규 검증 범위

원본 P1의 `brewing_stand`, `brewing_stand_bottle0~2`, `brewing_stand_empty0~2` **기존 모델 7개**와 `blockstates/brewing_stand.json` **실물 원본 JSON 8개를 GitHub에서 다시 조회**. 각 7모델 Git blob SHA를 P1 기존 누적 원장(544 경로)과 대조하고, v66의 기존 병/빈 모델 6개는 원본 JSON 내용과 SHA까지 다시 비교해 **6/6 동일**을 확인했다. v31의 양조기 본체 원본 연구 이력과 v66의 6개 leaf 직접 판독 이력은 기존 증거로 유지; 새 모델 신원0, P1 직접 source JSON unique 누적 모델 증가0.

원본 소스 snapshot: `00_ORIGINAL_BREWING_7_MODELS_1_BLOCKSTATE.json`.

## 2. 원본 7개 multipart 조건에서 8상태 모두 조립

원본 blockstate Git SHA `dfdffcd87ab8f8a3dd4086b6417e0b677dfca2b7`. 원본 multipart rules는 **7개**:
- 본체 `brewing_stand` 적용 1개(무조건)
- 병 상태 `has_bottle_0/1/2 = true`이면 대응 `brewing_stand_bottle0/1/2` 적용 3개
- 상태가 `false`이면 대응 `brewing_stand_empty0/1/2` 적용 3개

각 상태에 대한 source `when`을 **3개 boolean의 모든 (2^3=8) 조합에 실제 적용**. 매 상태 **무조건 본체1 + 각 자리에서 bottle/empty 중 하나씩3 = 모델4**가 정확히 선택되며, 서로 배제되는 같은 자리의 두 모델이 동시에 선택되거나 빠지는 경우는 없었다.

| 병 조합 (0,1,2) | 선택된 병 모델 | 선택된 빈 모델 | 원본 적용 elements | 원본 적용 face 참조 |
|---|---|---|---:|---:|
| 000 | 없음 | empty0,1,2 | 7 | 30 |
| 100 | bottle0 | empty1,2 | 7 | 30 |
| 010 | bottle1 | empty0,2 | 7 | 30 |
| 110 | bottle0,1 | empty2 | 7 | 30 |
| 001 | bottle2 | empty0,1 | 7 | 30 |
| 101 | bottle0,2 | empty1 | 7 | 30 |
| 011 | bottle1,2 | empty0 | 7 | 30 |
| 111 | bottle0,1,2 | 없음 | 7 | 30 |

**원본 소스 선언**: 7모델에 요소 10개, 원본 면 선언 **36개/모두 명시 UV36개**. **소스에서 계산된 각 조합의 참조**: 모델4/요소7/face30 × 조합8 = **조합별 적용 face 참조 총 240개**. 240은 모델 원본 면240개가 아니고 서로 배타적인 **8개 상태의 적용 참조를 합산한 수치**. 실제 게임의 cullface/렌더 출력 면 수가 아니다.

세부: `00_BREWING_7_MODELS_8_STATE_240FACE_PROOF.json`, `02_BREWING_8_EXHAUSTIVE_MULTIPART_STATES.csv`, `03_BREWING_240_STATE_APPLIED_FACE_REFERENCES.csv`.

## 3. 실제 소스 부품·회전·UV: 같은 평면 위의 다른 그림

본체 model에는 원본 **4개 요소/24면**(중앙 막대 + 하부 발 3개)이 선언. 병/빈 표식 leaf6개에는 각각 **0두께 평면1개·양면(북/남) face2개**, 전체 **6개 요소/12면**. 각각 같은 병 자리에서 bottle/empty 두 모델은 원본 `from/to`와 element `rotation`이 정확히 같지만 **uv좌표가 다르다**.

- slot0: y축 회전 없음. `north/south` 양면. source plane은 `[8,0,8] → [16,16,8]`.
- slot1: 원본 중심 `[8,8,8]`, y축 **−45°**. plane `[-0.41,0,8] → [7.59,16,8]`.
- slot2: 원본 중심 `[8,8,8]`, y축 **+45°**. plane은 slot1과 같은 원본 from/to.

각 조합에서 평면3개, 회전 적용2개. `brewing_stand_bottle{i}` 와 `brewing_stand_empty{i}`가 **원본 동일 기하 + 동일 `brewing_stand.png` + 서로 다른 명시 UV**를 통해 다른 부분을 선택한다는 구조는 직접 원본 JSON으로 확인했다. 이 사실은 가구 모드 제작 참고에 의미 있으나 **실제 texel이 어떤 그림인지/PZ 사물 대응은 PNG 픽셀 및 렌더 결과 없이 확정하지 않는다**.

모델별 원본 face `from/to, rotation, UV, texture slot, PNG path+SHA, cullface`의 36건 직접 표: `01_BREWING_SOURCE_36_DECLARED_FACES.csv`.

## 4. 원본 PNG 2개 Git SHA와 IHDR만 재검수

| 실제 텍스처 파일 | Git blob SHA | PNG IHDR |
|---|---|---|
| `brewing_stand.png` | `dc15b5805f8b06cc8fe69ab8782f8c187b7f3d4a` | 16×16, bit-depth8, color-type3 |
| `brewing_stand_base.png` | `9730634faf45ac0132932ba84435f8a76988ec9b` | 16×16, bit-depth8, color-type3 |

**중요:** color-type3은 팔레트 인덱스 형식이다. 바로 RGBA로 저장된 PNG라고 쓰면 잘못이다. 이번은 원본 Git SHA·PNG signature/IHDR 확인이며 **실제 팔레트/투명도/RGBA 픽셀 복호화 및 얼굴별 texel 재측정0**. 과거 v56 픽셀 전수근거와 중복 신규 실적을 주장하지 않는다.

## 5. 누적 증거 무결성 및 검증되지 않은 부분

- P1 증거 원장 **544행×379열 → 544행×393열**, v68의 `379×544=206,176`개 기존 데이터셀 원값 전부 동일.
- 보조 source review **544행×64열 → 544행×70열**, v68 `64×544=34,816` 데이터셀 전부 동일.
- 원본 544/544 직접 JSON 판독 이력은 기존 v66 검증 계승. 이번 원본 7모델 재조회는 544 고유 신원 증가 또는 모든 544개 실제 게임 기하·UV 완성 의미가 아님.
- 8조합은 **원본 multipart when 규칙의 결정론적 정적 평가**이며 Minecraft 1.21.11 클라이언트 렌더러 실행이 아니다. 공식 암시 UV/UVLOCK 또는 텍스처 픽셀 및 화면 최종 이미지 검증 실적은 이번에 없음.
- 1-1 승인150/150·상위1/5 완료 유지. **1-2-A·1-2 미완료**, 진척률 산정 불가, 마인크래프트 가구 제작 및 좀보이드 변환 미시작.

다음 단계는 `NEXT_CHAT_HANDOFF.md` 참조. 원격 SHA/기존셀 검증은 `VALIDATION_POST_RESEARCH_COMMIT.json`으로 별도 남긴다.
