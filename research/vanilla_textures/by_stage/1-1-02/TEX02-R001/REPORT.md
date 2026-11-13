# TEX02-R001 — 1-1-02 석재·벽돌 17종 정적 근거 재검증

- 연구일: 2026-11-13 (Asia/Seoul), Minecraft Java **1.21.11**; 범위 고정: `1-1-02-001` ~ `1-1-02-017` (17개).
- 근거 등급: **mirror_sha_pixel_checked**. **Mojang 공식 client.jar 인증 0/17, 인게임 정적 화면 0/17**. JAR/렌더를 확보하거나 실행했다고 주장하지 않는다.
- 원본: [InventivetalentDev/minecraft-assets tag 1.21.11](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11) (annotated tag `2c88d59b52a423044768ec7064697a38b91647b4`, target commit `7241a12cc2707abd7022f399c5d9033153e492e1`). 텍스처 경로는 `assets/minecraft/textures/block/<id>.png`; 모델 `assets/minecraft/models/block/<id>.json`; 상태 `assets/minecraft/blockstates/<id>.json`.
- 레거시 비교: [v4 150개 측정 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv), [고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv). v35 overlap 검사에 `stone` 이름이 등장하지만 그 행의 `in_v4_150_selected_sample=false`이므로 본 작업의 17번째 수행으로 중복 계산하지 않는다. v36 P1 SHA crosswalk에는 동일 텍스처 17건의 직접 대체 기록이 없다. v38은 oak shelf 자료이므로 이 범위의 공식 증명으로 오인하지 않는다.

## A — 식별·중복·원장

독립 STATE의 17개 ID·경로·SHA와 150개 고정 번호 원장의 17개, v4의 동일 17개가 **정확히 매칭**된다. 새로운 카테고리 확장 없음. v4의 17개 측정 기록은 기초 이력이며 아래 신규 검사와 별개다.

## B — 바이너리·해시·CRC

비공식 추출 미러 tag 1.21.11에서 **실제 PNG 17개 바이너리 취득**. 각각 독립 SHA-256 재계산 후 v4 SHA와 **17/17 일치**. PNG signature, IHDR/IDAT/IEND 청크 순회, 모든 청크별 저장 CRC32 대조, Pillow 이미지 디코드 **17/17 통과**. 모두 **16×16 px**. `SOURCE_LEDGER.csv`에는 PNG 바이트·SHA-256·파일 CRC32·Git blob SHA(서로 다른 값)를 독립 기록.

## C — 실제 RGBA·명암·반복 계측

- 모든 파일을 실제 RGBA로 변환하여 총 **17×256=4,352 픽셀** 검사; **불투명 4,352 / 완전 투명 0 / 부분투명 0**; 평균 알파 전부 255.
- 밝기 정의: `Y=0.2126R+0.7152G+0.0722B` (sRGB 8-bit 값에 대한 선형 가중합; 선형 광량 변환 아님). `mean`, `population std`와 인접 편차 및 이음새 재산출. v4 기록의 주요 luma/채널별 delta와 반올림 허용오차 약 0.0001 이내.
- 평균 Y 상·하단: `polished_diorite=193.1637`(밝음), `diorite=188.5477`; `blackstone=37.3047`, `polished_blackstone=50.1952`(어두움).
- `SOURCE_LEDGER.csv`에 파일별 Y/std, 수평·수직 에지 비율, 실제 좌/우·상/하 이미지 이음새 편차를 기록. RGB 재확인 기준 `stone` 인접 H/V 평균 6.3625 / 13.1208, 좌우/상하 이음새 10.5625 / 11.5625 (v4와 일치).

## D1 — 자연석/자갈/연마석/벽돌 대비·에지

에지는 `|Y(x+1,y)-Y(x,y)|>=24` (수평) / `|Y(x,y+1)-Y(x,y)|>=24` (수직), 각각 240개 인접 픽셀 쌍 분모:
- `cobblestone` 58.75% / 62.92%, `diorite` 60.42% / 68.33%: 고주파 대비가 강한 편.
- `stone` 2.50% / 17.08%; `stone_bricks` 9.17% / 11.25%; `deepslate_bricks` 7.50% / 9.58%: 선명한 접합부와 넓은 내부 면이 섞여 고주파 쌍 비율이 낮아질 수 있다.
- `polished_diorite` 32.92% / 32.92%로 원석 `diorite`보다 감소하지만 **경계 이음새는 더 커짐**. 따라서 '연마 = 모든 방향의 Seam 감소' 결론은 반례.

## D2 — 줄눈 주기·좌우/상하 접합

실제 16×16 PNG를 4×4로 **동일 반복**했을 때 이음새를 검사함. 수평 seam = 마지막 열 x=15 ↔ 첫 열 x=0을 y=0..15에서 비교(16쌍); 수직 seam = 마지막 행 y=15 ↔ 첫 행 y=0(16쌍). 수치 자체는 `SOURCE_LEDGER.csv`의 Y 차이. 비율은 이미지 내부 평균 인접 Y 차이에 대한 seam 배수.

- `stone_bricks`: 행 **7→8** Y 절대변화 51.819 (행 번호 0 기준). `deepslate_bricks`: 59.375, `tuff_bricks`: 47.697. 주 벽돌 수평 패턴 간격 후보 **8px**. 회전/배치까지 검증된 줄눈 물리 간격은 아님.
- `bricks`: 행 2→3, 6→7, 10→11, 14→15에서 큰 변화(40.241, 39.257, 36.62, 42.842), **4px 반복 간격 후보**. 상위 3개 인덱스는 `D2_ROW_PEAKS.csv`.
- `polished_andesite`: L/R seam=76.7346, 상하=73.8289, 내부대비 배수 **7.23× / 5.28×**; `polished_diorite`: 101.1889/106.1532 (**5.07× / 5.20×**). 연마 타일 테두리 때문에 반복 격자 경계가 더 강조될 수 있다.
- `granite`: seam 배수 0.69× / 0.73×, `diorite`: 0.76× / 0.79×. 반대로 거친 자연석 패턴은 반복 경계가 비교적 덜 튈 수 있다.
- 위 수치는 **인접 블록이 동일 UV 방향으로 반복**한다는 가정의 이미지 차이이며, 인게임 블록 인접 여부·조명·실제 렌더 접합을 인증하지 않는다.

## D3/E — 모델 면별 텍스처/UV 및 블록 상태 변형

미러에서 개별 17개 `models/block/*.json`과 `blockstates/*.json`을 직접 조회. 부모 JSON도 확인:
- **15/17** `cube_all` → `cube`: 면 `down/up/north/south/east/west` 모두 `#all`에 바인딩. `cube`의 0..16 전체 면 geometry, 명시적 UV 배열 없음(기본 상속). '면마다 임의 UV [0,0,16,16]'를 원본에 적혀 있다고 주장하지 않음.
- **2/17** `deepslate`, `blackstone`: `cube_column` → `cube`; 네 수직 면은 `#side`, 윗면·아랫면은 `#end`. 끝면은 각각 `deepslate_top.png`, `blackstone_top.png`로 **이 단계 17개 PNG에 포함되지 않음**. 해당 2개 끝면의 색/알파/UV 실제 PNG 픽셀 샘플링은 이번에 완료했다고 주장하지 않음.
- `stone`: 블록 상태에 normal, `stone_mirrored`, normal y=180, mirrored y=180의 **4개** 변형. `stone_mirrored` → `cube_mirrored_all` → `cube_mirrored`: 여섯 면 모두 **명시 `uv:[16,0,0,16]`** (U 뒤집기).
- `deepslate`: `axis=x/y/z`와 회전(`x:90`, `y:90/180`) 및 `deepslate_mirrored` 조합, JSON 변형 엔트리 **12개** (일부 중복 명시). 미러 부모 역시 `cube_column_mirrored` → `cube_mirrored`.
- 나머지 15종(단, 위 stone 제외 14종)의 단일 블록 상태 모델이 해당 텍스처를 가리킴. `MODEL_UV_LEDGER.csv`에 각 JSON Git blob SHA·부모·변형·끝면 예외 기록.
- 회전·미러 효과의 **2D 가상 인접 비교**: 원래 이미지/수평 뒤집기/180도 회전/그 조합 간 seam은 `stone` L/R **0–13**, `deepslate` L/R **0–33.6403** Y 단위로 변할 수 있음. 이는 변형 이미지의 가능 범위를 계산한 실험이며 실제 월드의 맞닿는 면/uvlock/엔진 동작을 재현한 판정이 아님.

## F — 공식 자료 / 인게임 정적 검증: PENDING

현재 실행 경로에서 Mojang의 공식 `client.jar` 인증 데이터를 확보·비교하지 못했으며 게임 정적 장면도 관측하지 못했다. 따라서 **공식 SHA 인증 0 / 인게임 정적 렌더 확인 0**. `official_client_jar_authenticated=false`, `ingame_static_render_verified=false`를 유지한다.

## G — 저장 및 다음 단계

- 이 폴더는 신규 불변 리비전 **`TEX02-R001`**. `SOURCE_LEDGER.csv`, `MODEL_UV_LEDGER.csv`, `D2_ROW_PEAKS.csv`, `SUMMARY.json`와 이 보고서 저장.
- 다음은 `TEX02-R002` (반드시 저장 직전 상태 재확인). 우선순위: (1) 정적 공식 JAR SHA·이미지 대조, (2) `deepslate_top`/`blackstone_top` 면 실제 이미지/UV 범위 구분(범위 밖 2개를 단계 완료 개수에 추가하지 않기), (3) 실제 게임의 **정적** 인접 벽면 회전/미러/조명 검증, (4) D2 접합 주기 관찰 반례 확보.
- 기존 v4~v38 기록 변경 없음. 공식 전체 `v38`, 상위 1단계 0/5 유지. 애니메이션(프레임/키프레임/움직임) 전면 보류, 기존 기록 보존. Project Zomboid 변환/가구 모델 제작 제외.

## 계측 재현 정의

파일별 `source SHA256=hashlib.sha256(binary)`; PNG 청크 CRC=`zlib.crc32(type+payload)`과 4바이트 저장 CRC 비교; 디코딩=`Pillow.Image.open(...).convert("RGBA")`; Y 계산 `0.2126R+0.7152G+0.0722B`; std=`np.std(Y)` (population); H/V 엣지=`np.abs(np.diff(Y,axis=1/0))` 240쌍; seam 좌우=`mean(abs(Y[:,15]-Y[:,0]))`, 상하=`mean(abs(Y[15,:]-Y[0,:]))`. 본 단위는 각 16×16 이미지의 **픽셀 공간**이고 광원/셰이더 결과가 아니다.
