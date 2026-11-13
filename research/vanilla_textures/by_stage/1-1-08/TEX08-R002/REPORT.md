# TEX08-R002 — 정적 블록상태/UV 재감사 및 공식 JAR 검증 절차

- 날짜: 2026-11-13
- 대상: **오직 1-1-08 고정 21개**, 원본 R001을 수정·중복 증가하지 않음
- 신규 직접 확인: **16개 blockstates JSON**, 모델/UV 원장 62면의 실제 PNG 영역 재검사, 열림/닫힘 통 비교용 보조 PNG 1종
- 공식 전체 checkpoint: `v38` 그대로
- **중요: 공식 client.jar 실제 바이트를 이 실행 환경에서 확보하지 못했다. 공식 PNG 인증 0/21, 인게임 검증 0/21.**

## A 기존 증거 재사용과 신규 범위

R001: 21/21 PNG 바이트·SHA256·PNG CRC32·Adler32·Pillow RGBA, 모델 face 슬롯 62행. 이번 R002에서는 이 근거를 새 21개로 중복 계산하지 않고 **blockstate 연결 16종 및 62행의 UV 텍셀 사용 영역을 재검산**했다.

새 출처: `InventivetalentDev/minecraft-assets` `1.21.11` 브랜치의 `assets/minecraft/blockstates/{name}.json` (본문 `BLOCKSTATE_AUDIT.csv`에 각각 Git blob SHA1 저장), `assets/minecraft/textures/block/barrel_top_open.png` (Git blob `2f2b7c6928a02dd839c1b281174e7bc594cfb1c7`). 파일은 공식 Mojang JAR 인증본이 아니라 **비공식 추출 미러**다.

## B·C·D2 통 개폐의 새 고정 PNG 실측

- `barrel_top` (R001 대상) → `barrel_top_open` (R002 **보조**, 21개 분모 제외).
- 보조 open 원본: PNG 16×16, 181바이트; Git blob SHA1 `2f2b7c6928a02dd839c1b281174e7bc594cfb1c7`; SHA256 `ca852462e7131d5410ca8ae65932f4b5a5452f80a428e7c0570fdb8c020e7326`; PNG 모든 청크 CRC32 통과·Pillow RGBA 디코드.
- 전후 PNG 픽셀 **132/256 RGBA 변동**, alpha 0/256 변동. 차이 bbox `[2,2,13,13]`; 행별 변화 `0,0,8,10,12,12,12,12,12,12,12,12,10,8,0,0`. 정적 상태 사이의 픽셀 차이만 확인했고 애니메이션 동작/프레임은 연구하지 않았다.
- `barrel`의 12개 조합은 `6 facing × 2 open`; 닫힘 6개에서 `barrel_top`, 열림 6개에서 `barrel_top_open`; `barrel_side`·`barrel_bottom`은 양쪽 모델에 사용. blockstate의 `x/y` 값은 소스 JSON에 존재하지만, 게임에서의 최종 화면 회전은 미검증.

## D1·D3·E 블록 상태 조건과 텍스처 역할

- **16 blockstates** 직접 확인: 일반 `variants` **73행**, 조각된 책장 `multipart` **52행**. 두 분모를 동일한 하나의 '게임 상태 수'로 잘못 합하지 않는다.
- `furnace`, `smoker`, `blast_furnace`: 각각 **4 수평 방향 × lit false/true = 8개**. 고정 21개에 들어 있는 `*_front`는 lit=false 모델 정면(4개)에서 사용, lit=true의 대체 정면은 범위 밖. 특히 16×32 / 16×48 다중 프레임 PNG는 **프레임 분석 보류**.
- `beehive`: **4방향 × honey_level 0..5 = 24개**, `beehive_front`는 수준 0..4에 해당하는 20개 정적 블록상태 모델에서 사용, honey_level=5는 별도의 `beehive_front_honey` 정면.
- `chiseled_bookshelf`: 방향 4개 각각 `1 base + 6 slots × 2 condition` = 13개 규칙, 총 52 multipart 행. 한 시점의 논리적 구성은 **base 1 + slot overlays 6개**이며, 이론적으로 4방향 × 2^6 점유 조합 = **256개 선택 조합**(소스의 52규칙과 같은 분모가 아님). `empty`와 `occupied` 각각 24개 조건 규칙에 연결. UV는 R001의 **상·하단 6개 별도 영역**을 사용.
- `note_block`는 `cube_all`의 `#all`을 6면/particle에 사용; 같은 바이트를 쓰는 `jukebox_side`는 `cube_top`에서 측면·하단 5면과 particle에 사용. PNG 동일성으로 JSON 구조나 소리 동작을 동일하다고 판단하지 않음.
- 21개 항목의 블록상태 사용 조건은 `TEXTURE_STATE_COVERAGE.csv` 참조. 지역별 UV는 `UV_62_FACE_TEXEL_AUDIT.csv` 참조.

## 직접 원본 RGBA 영역에서의 UV 참조 재계산

- R001 62개 면×텍스처 기록을 불러와 원본 PNG **해당 UV 직사각형만 다시 Pillow로 샘플링**했다.
- 텍스처 내 원본 **고유 총 5,376픽셀**과 달리, 62개 모델 면에서 사용하는 **13,056 texel-uses** = **불투명 13,056 / 투명 0 / 반투명 0**. 이는 동일 픽셀을 여러 면이 참조하는 횟수를 포함.
- **명시 UV 16행**: `enchanting_table_side` 4면 × `[0,4,16,16]` = 768 texel-uses; 조각된 책장 12 overlay UV 합계 512 texel-uses. **암시/추론 UV 46행** = 11,776 texel-uses. 합계 **13,056**. 
- 마법부여대 이미지 상단 4행 64개 투명 픽셀은 모델 side UV가 y=4부터이므로 실제 4측면 참조 영역에는 들어가지 않는다. 렌더러의 실제 UV winding 및 게임 화면은 별도 검증 대기.
- `particle`은 렌더 face 자체와 구분하며, 상속 `#front`, `#side`, `#all`, 모델별 독립 슬롯 참조를 혼용하지 않았다.

## F 공식 인증 상태·실행 가능 검증기

공식 버전 정보 출처: https://piston-meta.mojang.com/mc/game/version_manifest_v2.json

검색 자료에 나타나는 1.21.11 client 객체 후보 SHA1: `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd` (https://piston-data.mojang.com/v1/objects/ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd/client.jar ). **후보/참조 주소만 확인했으며 공식 JAR을 다운로드해 SHA1을 대조하지 못했으므로 인증 수 0/21.** 컨테이너 HTTPS DNS 및 다운로드 시도 실패. 미러 PNG hash가 같다고 공식 인증을 대신할 수 없음.

재현 가능한 `VERIFY_OFFICIAL_CLIENT.py` 포함: 사용자가 확보한 `1.21.11.jar`와 R001 `SOURCE_LEDGER.csv`로, Mojang HTTPS manifest → 버전 metadata SHA1 → client JAR SHA1/size → ZIP 손상 → 21개 PNG SHA256을 연속 검증하는 코드. **이번 채팅에서는 JAR이 없어 실행하지 못했으며** 스크립트를 저장한 사실은 성공한 검증으로 세지 않는다.

## 경계 / 차기
- 보조 PNG는 21개 범위의 신규 완료 건수에 넣지 않음; F 공식 JAR **pending**, 인게임 정적 UV **pending**.
- 애니메이션 프레임/키프레임/움직임 0건; 과거 동적 조사 파일 보존.
- Project Zomboid 변환 및 실제 가구 3D 제작 진행하지 않음.
- 다음은 `TEX08-R003` (새 근거 확보 시에만), 루트 및 타 단계 파일 쓰기 금지.
