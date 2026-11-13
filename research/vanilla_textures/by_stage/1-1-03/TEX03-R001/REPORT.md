# TEX03-R001 · 1-1-03 금속·금속부품 증거 보고서

**기준:** Minecraft Java 1.21.11 / 2026-11-13 / 16개 고정 경로만. 전체 통합 버전 v38 변경 없음. 공식 JAR 또는 인게임 인증이 아닌 **비공식 추출 미러** `InventivetalentDev/minecraft-assets`의 `1.21.11` 스냅샷을 직접 읽은 결과.

## A — 원장·출처
- 단계 STATE의 16개 `item_id`, PNG 경로, SHA-256을 [v4 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv)과 1:1 비교: **16/16 동일**.
- v4에는 기존 측정 기록 16개가 존재하나 이 독립 채팅의 신규 실측으로 중복 계산하지 않았음. 관련 v35~v38 선행 자료가 본 단계 공식 검증을 의미하지 않으며 기존 파일은 변경하지 않음.

## B — 실제 PNG 바이너리
- 비공식 1.21.11 GitHub 추출 미러에서 **PNG 16/16 재수집**. 각 PNG의 Git blob SHA1, 파일 SHA-256을 별도 기록.
- 독립 SHA-256은 v4 기록과 **16/16 일치**. PNG 16/16 시그니처 및 전 청크 CRC 정상, Pillow `verify()` 및 RGBA 디코딩 성공.
- 전부 **16×16**, 총 **4,096픽셀**, 원본 파일 크기 합 **3,176바이트**. 개별 증거는 `SOURCE_LEDGER.csv`.
- 저작권 확인 전이라 PNG 바이너리 자체는 재배포하지 않고, 원본 URL·원본 해시만 인용.

## C — 16개 PNG RGBA 재계측
- alpha 255: **3,775픽셀**, alpha 0: **321픽셀**, 중간 alpha 1..254: **0픽셀**. RGB 팔레트 수와 밝기/평균 RGB도 개별 표에 기입함.
- 비불투명 PNG만 열거: `copper_grate` alpha0 **77**, `iron_trapdoor` **36**, `heavy_core` **64**, `iron_door_top` **48**, `anvil_top` **96**. 나머지 11개는 alpha0=0.
- 정확한 RGBA 이진 알파 마스크 5종: `ALPHA_MASKS.txt`. 투명 픽셀 = 인게임 렌더 투명도/물리 구멍/충돌 판정이 아님.

## D1 — 철·구리·녹청·단조 계열 비교
- 직접 재계측한 가시 픽셀 평균 RGB: `copper_block` (192.418,107.656,79.820) → `exposed_copper` (161.078,125.703,103.934) → `weathered_copper` (108.297,153.004,110.359) → `oxidized_copper` (82.426,162.668,132.867). 갈색 계열에서 녹청색 계열로 이동.
- 각 평균 밝기: **123.67 → 131.65 → 140.42 → 143.46**. 이 16개 PNG의 평균 밝기일 뿐 금속의 실제 물리적 반사광·런타임 셰이딩 검증은 아님.
- `cut_copper` 122.89 / `exposed_cut_copper` 127.27은 가공면 패턴 별도; `iron_block` 220.03, `raw_iron_block` 140.17, `anvil` 68.53, `anvil_top` 72.53, `gold_ore` 134.30. ‘금속’이라는 명칭만으로 한 팔레트/광택으로 묶으면 오류.

## D2 — 구멍·부품면 구별
- `copper_grate`: 구멍 alpha0 77/256 = 30.078125%; 단일 `cube_all` 정육면체 모델에 알파 마스크를 적용.
- `iron_trapdoor`: 구멍 36/256 = 14.0625%; closed bottom/top과 open의 3개 정적 판 모델 모두 같은 `iron_trapdoor` PNG 사용.
- `iron_door_bottom` 0/256 vs `iron_door_top` 48/256: 상단 창/구멍 표현이 다름.
- `anvil` 0/256 vs `anvil_top` 96/256: 본문과 상면 PNG 별도. `template_anvil`은 본체 4요소와 별도의 `#top` 면을 사용.
- `heavy_core`: 64/256 투명, PNG 오른쪽 아래 8×8 사분면. 이는 전체 블록 빈 영역이 아니라 부분 UV 아틀라스 데이터임.

## D3/E — 실제 정적 blockstate, 모델, 부모 템플릿, UV
- 이 16개 PNG의 사용자 범위 관련 **14개 고유 blockstate JSON**을 직접 읽음. 블록상태/리프 모델 Git SHA는 `MODEL_UV_STATE_LEDGER.csv`에 기록함.
- 일반 정육면체 **10개**는 `cube_all`→`cube`에 연결, cube 요소 `[0,0,0]→[16,16,16]`, 6면 전체 UV가 기본. `copper_grate`도 cube 전체면에 알파 구멍을 가진다.
- `heavy_core`: 단일 cuboid `[4,0,4]→[12,8,12]`. side UV `[0,8,8,16]`, up `[0,0,8,8]`, down `[8,0,16,8]`. 16×16 PNG 전체를 한 면에 늘려 쓰지 않음.
- `iron_trapdoor`: 정적 variant **16개**(facing 4 × half 2 × open 2), 리프 모델 **3개**(`iron_trapdoor_bottom`, `top`, `open`). 닫힌 밑판 `[0,0,0]→[16,3,16]`, 윗판 `[0,13,0]→[16,16,16]`, 열린 판 `[0,0,13]→[16,16,16]`. closed 위·아래 UV `[0,0,16,16]`, 옆 띠 `[0,16,16,13]`. `open`은 정지 상태 모델일 뿐 애니메이션 조사 아님.
- `iron_door`: 정적 variant **32개**(facing 4 × half 2 × hinge 2 × open 2), 리프 모델 **8개**. 대표 부모 `door_bottom_left`/ `door_top_left`: 요소 `[0,0,0]→[3,16,16]`; 넓은 면 UV `[0,0,16,16]`, 두께 띠 `[0,0,3,16]`. **half=lower ↔ upper일 때 사용 실제 상·하 PNG 전환**, facing/hinge/open에서 회전·모델 형태만 변경. 리프 텍스처 슬롯은 공통으로 `bottom`과 `top`을 선언하나 템플릿 면은 반쪽별 참조.
- `anvil`: `facing` **4개**가 동일 리프 `anvil`의 회전만 변경. `template_anvil`은 **4개 요소**, body `block/anvil`, top `block/anvil_top`으로 분리; 윗부분 상면 UV `[3,0,13,16]`, 본체 측면 UV 예 `[2,12,14,16]`. 텍스처 경로가 방향별로 바뀐다는 근거 없음.

## F — 공식 검증 보류
- Mojang **공식** 1.21.11 `client.jar` 확보/해시 인증 **0/16**. 게임을 실행해 동일 정적 블록·조명·알파·광택을 대조한 기록 **0/16**.
- 본 결과는 **mirror_sha_pixel_checked** 수준이다. `official_jar_authenticated` 또는 `ingame_static_verified`로 올리지 않는다.
- 애니메이션, 프레임, 키프레임, 움직임 검증은 **사용자 해제 지시까지 전면 보류**; 과거 관련 기록 삭제 없음.

## G — 결과 기록과 다음 작업
`SOURCE_LEDGER.csv`, `MODEL_UV_STATE_LEDGER.csv`, `ALPHA_MASKS.txt`, `SUMMARY.json`으로 파일·화소·UV·상태별 근거를 재검증할 수 있다. **다음 후보는 TEX03-R002**이고 공식 JAR 및 인게임 정적 증거가 새로 들어오기 전에는 임의 완료로 판단하지 않는다. 전역 `v38`과 다른 단계/루트 인수인계는 변경하지 않는다.

**원본 미러:** https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft/
