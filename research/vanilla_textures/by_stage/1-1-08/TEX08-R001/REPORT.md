# TEX08-R001 — 1-1-08 복합·기능면 원본 미러 재검증

날짜: 2026-11-13 · 대상: **21/21 고정 경로만** · 전체 v38 변경 없음.

## 증거 수준 및 검증 방법 (A–C)
- GitHub `InventivetalentDev/minecraft-assets`의 **1.21.11 브랜치**에서 직접 가져온 21개의 PNG Base64를 바이트로 복원. **독립 재계산한 SHA-256 = v4 원장 SHA-256 21/21**, Git blob SHA-1도 21/21 일치.
- PNG signature, IHDR, 모든 청크 CRC32, IDAT zlib 해제·Adler32, Pillow verify 및 RGBA 디코드 통과: **21/21, 16×16, 5,376픽셀, 4,818 원본 바이트**.
- RGBA 전수: 불투명 5,312, 완전투명 64, 반투명 0. 투명 64는 `enchanting_table_side`의 **위쪽 y=0..3 네 행**뿐. 나머지 20개는 전부 완전 불투명.
- `SOURCE_LEDGER.csv`는 개별 SHA·Git blob·PNG 바이트·RGBA·고유색·휘도 및 수평/수직 RGB 변화 측정을 분리 기록. 휘도는 sRGB 값에 Rec.709 계수 0.2126/0.7152/0.0722를 적용하고, 인접 변화는 채널 절댓값 평균으로 계산했다. v4 자료를 신규 실측으로 중복 합산하지 않음.
- 파일 **21개이지만 바이너리 고유 20개**: `jukebox_side`와 `note_block`의 원본 바이트/SHA/RGBA가 완전히 같음.

## D1 재질·기능면 분리 (실제 JSON + 시각/픽셀 대조)
- 작업대 `crafting_table`: front `north/west`, side `east/south`, up 별도 `crafting_table_top`, down `oak_planks`. front 대 side **38/256** RGB/RGBA 차이.
- 통 `barrel`의 `cube_bottom_top`: `#bottom=barrel_bottom`, `#side=barrel_side`, `#top=barrel_top`, particle은 **side**에 상속 연결. top 대 bottom **256/256** 변화; 닫힘/열림은 `barrel_open`의 **다른 상단 텍스처**이므로 이번 21개 본체 통계에는 미포함.
- 일반 책장 `bookshelf`는 `cube_column`의 측면 4개에 `bookshelf`를 사용, 상·하면은 `oak_planks`. `chiseled_bookshelf`의 base geometry는 별도 side/top과 6개 독립 frontal slot overlays.
- `furnace`, `smoker`, `blast_furnace`는 `orientable(_with_bottom)` 모델 상속: front `#front`, east/south/west `#side`, top `#top`; furnace 및 blast bottom은 top을 재사용하고 smoker는 `#bottom` 별도.
- `smithing_table` front north/south 및 side east/west; `loom`은 front `loom_front`, side `loom_side`, top/bottom 분리; `fletching_table` front north/south, side east/west 별도.
- `note_block`는 `cube_all/#all`; `jukebox`는 `cube_top/#side`와 상부 별도 이미지이므로 **동일 PNG를 사용해도 모델의 면 역할은 다름**.
- 벌통 `beehive_empty`: 정면 `#front`, 측면 `#side`, 상·하단 `beehive_end`; particle은 **beehive_side**. `pumpkin`과 `target`은 `cube_column/#side/#end`.

## D2 두 고정 상태만 교차 비교
- **조각된 책장** `chiseled_bookshelf_empty` ↔ `occupied`: **156/256 RGBA 변경**, alpha 차이 0. 6개 고정 슬롯 단위 변화는 25,29,24,29,25,24픽셀 (합 156).
- **화로** `furnace_front` ↔ 보조 `furnace_front_on`: **36/256**, bbox `[3,11,12,15]`, alpha 변화 0. 과거 v37 기록과 재계산 일치.
- **벌통** `beehive_front` ↔ 보조 `beehive_front_honey`: **24/256**, bbox `[1,4,14,13]`, alpha 변화 0. 과거 v35 기록과 재계산 일치.
- 보조 2 PNG는 D2 상태 비교용으로만 재디코딩했고, 21개 대상/5,376픽셀에 포함하지 않았다. `smoker_front_on`(16×48) 및 `blast_furnace_front_on`(16×32)은 다중 프레임이므로 **프레임·키프레임·동작·픽셀 분석을 수행하지 않음**. 과거 기록도 수정하지 않음.

## D3 / E 정적 모델·face UV·particle
- 고정 21 텍스처 모두 모델 JSON에 연결. `MODEL_UV_EVIDENCE.csv`에 **62 source face×texture 기록** 보존. 이중 상속 `cube` 면의 full-face `[0,0,16,16]`은 **직접 선언 UV가 아닌 추론 46건**이다. source explicit UV **16건** = enchanting side 4면 + 책장 slot overlays 12면.
- `enchanting_table`은 12높이 직육면체이며 측면 `#side` 4개 face UV가 **명시적 `[0,4,16,16]`**, 각 16×12=192 texel; 위쪽 4행의 투명 픽셀을 실제 측면 face에서 제외한다. particle은 `enchanting_table_bottom`으로 **side와 다름**.
- `chiseled_bookshelf` blockstate는 4방향 × 6개의 조건부 슬롯(occupied/empty) 모델 조합. 템플릿은 `north` face만 선언, 상단 UV `[0,0,6,8]`, `[6,0,11,8]`, `[11,0,16,8]`; 하단 UV는 같은 x범위 y=8..16. 각각 48/40/40 texels. `CHISELED_SLOT_UV.csv`에 12 자식 모델 SHA와 6 템플릿 SHA를 보존. base particle은 `#top`이며 **슬롯 오버레이 텍스처는 particle 아님**.
- Blender/Game 실제 적용 상태, face 회전·UV lock·렌더 샘플은 미검증. source `blockstates`/model 연결만 확인; 런타임과 동일하다고 단정하지 않음.

## F / G 검증 경계와 인수인계
- **공식 Mojang 1.21.11 client.jar와 비교한 SHA는 0/21, 실제 게임 정적 장면 관찰은 0/21**. 현재 근거 수준은 `mirror_sha_pixel_checked` + `model_json_uv_source_checked`이며 **공식 인증/인게임 완료가 아니다**.
- A–E는 21종 정적 미러 소스 기준 검사 수행. F **pending**. G 단계 보고서·원장·상태를 자기 단계 한정으로 저장.
- 동적 애니메이션 연구, Project Zomboid 변환, 3D 모델 제작 미수행. 다음 단계는 공식 JAR 별도 확보 시 이 릴리스 해시/모델 참조와 인증 대조, 인게임 정적 face UV 검수. 병렬 같은 단계 채팅의 동시 수정을 금지. **다음 릴리스 번호 TEX08-R002**.

원본 추출 미러: https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft
이전 근거: `research/vanilla_textures/v4_150/`, `research/vanilla_models/v35/`, `v36/`, `v37/` (모두 읽기 전용 재사용).
