# v68 — 촛불 점등 4종 원본 상속 모델·상태 8개 + 특수 렌더러 5종 2차 소스 근거

- 원본: Minecraft Java 1.21.11 추출 JSON/PNG; 이전 main HEAD `ddc1382920f494b2ff7f7f5c3c36314285f60e83`. **1-2-A는 계속 진행 중**.
- v67 자체 JSON elements=0 표본 중 촛불 소등4 → **v68 점등4 leaf JSON 직접 판독**. 각 P1 모델 경로+Git SHA를 이전 원장과 대조. 부모 template4개 원본 JSON의 SHA/내용도 v67 동일. 새 모델 신원0·544/544 직접 조회 이력 중 새로운 고유 직접 조회 플래그0.
- **상속 적용 30 요소 / 100 face 참조 / 원본 명시 UV100 / 암시 UV0**. 모델별 점등 순서1~4의 원본 상속 요소3/6/9/12, 원본 적용면10/20/30/40. 100은 고유 원본 template 선언100개가 아니라 leaf별 재사용 적용 참조.
- 원본 `blockstates/candle.json`(SHA `9e867034...`) **8 variants** = candle 수1~4 × lit false/true, 각 서로 다른 원본 leaf target 1개와 일치. 같은 개수 점등/소등 leaf는 같은 template 부모 SHA를 사용하고 `textures.all` 참조만 `minecraft:block/candle_lit` 대 `minecraft:block/candle`로 달라진다. 이 정적 구조만으로 실제 불꽃·게임 조도·particle·동작 인증은 안 됨.
- `candle_lit.png` 원본 Git SHA `413f962a2cb460a7c037101b29807c7b057696ac`, `candle.png` SHA `01c91a001d84cdb32c26f1800f88fadc537d7432`. 두 PNG 16×16, 8bit RGBA color-type6, Git SHA/IHDR만 직접 확인. 이번 신규 전체 RGBA 복호화0, PNG 픽셀/조도 테스트0.
- 파일: `00_CANDLE_4_LIT_LEAF_4_TEMPLATE_1_BLOCKSTATE_SOURCE.json`(4 leaf/4 template/1 state 원본 SHA+JSON), `00_CANDLE_LIT_4_PARENT_100_FACE_AND_8_STATE_PROOF.json`, `01_ORIGINAL_CANDLE_EIGHT_STATES.csv`, `02_ORIGINAL_LIT_CANDLE_SOURCE_FACE_100.csv`, `03_ORIGINAL_CANDLE_PNG_TWO_SHA_IHDR.json`.

## 5개 모델 JSON geometry=0의 다른 렌더 경로 — 2차 Java 근거

원본 `decorated_pot`, `ender_chest`, `oak_hanging_sign`, `shulker_box`, `white_shulker_box`에는 자체·부모 JSON의 elements0이지만 각 `blockstates/*.json`가 모델을 직접 참조한다(이 사실은 v67 검증). 이번에는 공개 **비공식 1.21.11 디컴파일 Java** 저장소 `H1lkaaaGD/Minecraft_1.21.11_Source` (`main` HEAD `fb136698ca0ae1f6e6e5a1b0c964740fb2f6dd18`)에서 7개 코드 파일의 Git SHA·해당 행을 직접 다시 열어 검증했다.

| 원본 resource model | 2차 소스의 world block entity 타입 → 렌더러 | 확인한 소스 동작 단서 |
|---|---|---|
| decorated_pot | DECORATED_POT → DecoratedPotRenderer | neck·top·bottom·side plane 모델 레이어와 부품 |
| ender_chest | ENDER_CHEST → ChestRenderer | ChestModel의 bottom·lid·lock 구성과 lid 회전 |
| oak_hanging_sign | HANGING_SIGN → HangingSignRenderer | board·plank·chains의 모델 기하 |
| shulker_box | SHULKER_BOX → ShulkerBoxRenderer | 모델 레이어 및 뚜껑 진행도 기반 위치·회전 |
| white_shulker_box | 위와 같은 SHULKER_BOX renderer | 색별 leaf JSON은 다르나 world 렌더러 클래스 공유 |

`SpecialModelRenderers.java`에서도 해당 다섯 블록의 정적 special-item mapping을 별도 확인. 원본 모델5경로에 독립 world type4개. 근거: `00_SECONDARY_RENDERER_5_CODE_EVIDENCE.json` (7 Java 소스 경로+Git blob SHA+원문과 일치하는 정확한 행 번호). **비공식 디컴파일 소스는 Mojang 공식 client.jar 바이너리 해시나 실제 world render 테스트가 아님**. 따라서 런타임 인증/모델별 UV·텍스처·애니메이션 최종 검증0.

## 원장 보존과 단계 상태

P1 544행 **365→379열**, v67 앞 **198,560셀 정확히 보존**; source-review 544행 **56→64열**, 기존 **30,464셀 보존**. 모델 544/544 직접 원본 JSON 조회 범위 유지, 그러나 모든 모델의 기하·PNG·렌더러 검증은 미완료. 1-1 승인150/150, 상위5단계 중1개 완료, 1-2-A/1-2 진행 중·실질 완료율 미산정. 가구 모델 제작 및 좀보이드 맵 변환 미착수.

자세한 후속 작업: `NEXT_CHAT_HANDOFF.md`. 연구 저장 후 검증 결과는 별도 `VALIDATION_POST_RESEARCH_COMMIT.json` 기록.
