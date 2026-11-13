# 1-1-08 — 복합·기능면 전용 인수인계 (현재 TEX08-R001)

> 2026-11-13. 정확한 담당 범위 **21 PNG**. **현재 `TEX08-R001`**, 다음 `TEX08-R002`. 최초 `TEX08-R000`은 계획만 기록한 이력이다. 공식 전체 버전 **v38 유지**, 전체 1단계 완료 0/5 그대로.

## 현재 상태: 실데이터 분석 기록과 공식 검증의 분리

| 확인 | 상태 |
|---|---|
| A 21개 경로·v4 SHA·중복 대조 | 21/21, 신규 교차확인 |
| B 직접 PNG PNG-CRC/Adler/SHA/디코딩 | 21/21, 비공식 추출 미러 |
| C 독립 16×16 RGBA 정량 실측 | 21/21, 5,376픽셀 |
| D1 정면·측면·상부 기능적 재질 분리 | 정적 모델 JSON/시각 측정 수행 |
| D2 두 고정 텍스처 비교 | 고정 상태 차이 기록, 보조 PNG는 21에 미합산 |
| D3 및 E 실제 모델·UV 슬롯 | 21/21; 62면 근거(명시 UV 16·유도 UV 46) |
| F 공식 Mojang client.jar / 인게임 | **0/21 / 0/21, 미검증** |
| G 단계 파일·상태 저장 | TEX08-R001, 단계 전용 |

## 실제 결과 위치
- [보고서](../../../..//../../../research/vanilla_textures/by_stage/1-1-08/TEX08-R001/REPORT.md) (경로: `research/vanilla_textures/by_stage/1-1-08/TEX08-R001/REPORT.md`)
- `research/vanilla_textures/by_stage/1-1-08/TEX08-R001/SOURCE_LEDGER.csv` — 21 PNG 해시·CRC·RGBA·색·명암 근거
- `research/vanilla_textures/by_stage/1-1-08/TEX08-R001/MODEL_UV_EVIDENCE.csv` — 62 face×texture JSON 매핑
- `research/vanilla_textures/by_stage/1-1-08/TEX08-R001/CHISELED_SLOT_UV.csv` — 6 UV 템플릿·12 슬롯 리프 SHA
- `research/vanilla_textures/by_stage/1-1-08/TEX08-R001/STATIC_PAIR_DIFF.csv` — 정적 이미지 쌍 픽셀 차이 및 경계
- `research/vanilla_textures/by_stage/1-1-08/TEX08-R001/SUMMARY.json` — 정확한 수량·미검증 표기

## 재시작 및 충돌 보호
1. 본 단계 [STATE.json](STATE.json)을 GitHub에서 다시 읽고, **next_revision**과 현재 blob SHA를 점검.
2. 신뢰도는 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`를 별도로 판정.
3. 공식 JAR/실제 게임 정적 상태 접근이 가능하면 R001과 **별도 검증**, 불가능하면 F 보류. 기존 v35/v36/v37 및 v38 자료 임의 수정 금지.
4. 다음은 `TEX08-R002` 신규 **불변 폴더**만 사용. 기존 R001 불변. 다른 단계 또는 루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json` 수정 금지.
5. 애니메이션 프레임·동작·키프레임 조사는 사용자 해제 전면 보류, 기존 기록 삭제 금지. Project Zomboid 변환/실제 3D 가구 제작 금지.

## 표본 범위 (변경 금지)
- `1-1-08-001` `crafting_table_front`: `assets/minecraft/textures/block/crafting_table_front.png` — v4 SHA `1659c76a33039640e8bd5584af8db04bf626486432a389bcaf1567e1a45c6464`
- `1-1-08-002` `barrel_side`: `assets/minecraft/textures/block/barrel_side.png` — v4 SHA `30f31d8cecfbd44412af13983eee56220bcffbf7ce8dd5a948f1ab73c98d8dc8`
- `1-1-08-003` `bookshelf`: `assets/minecraft/textures/block/bookshelf.png` — v4 SHA `cf2b8c0da8e7164162ad4991916492b724c62c31de6c18b2abb7d60ec19ba418`
- `1-1-08-004` `crafting_table_side`: `assets/minecraft/textures/block/crafting_table_side.png` — v4 SHA `e9755fc6da763909b285342eae12c5f7d1cc8462fab695bb157504ea207cda8c`
- `1-1-08-005` `smithing_table_front`: `assets/minecraft/textures/block/smithing_table_front.png` — v4 SHA `f7a5479a3e1d3e3f604ec1b22634736ea952b676fef20e954a9607f15fb13ba0`
- `1-1-08-006` `barrel_top`: `assets/minecraft/textures/block/barrel_top.png` — v4 SHA `6b4cb64b1c34bd87225147479100bec9889ac69c7dcdb5694003248e3004fe1e`
- `1-1-08-007` `barrel_bottom`: `assets/minecraft/textures/block/barrel_bottom.png` — v4 SHA `1addc57c6221210107b7e64db8d2756983458a14828d8eb85b61f13bbf5a1028`
- `1-1-08-008` `loom_side`: `assets/minecraft/textures/block/loom_side.png` — v4 SHA `526372c59e91f10c1d690124d3f72a3938a154081cbc1a26a6151b924c8293f2`
- `1-1-08-009` `furnace_front`: `assets/minecraft/textures/block/furnace_front.png` — v4 SHA `aae808f71f1bddf4a25592f7dd3d7f6e9b3adaa739502170766424f4eb6bf9c5`
- `1-1-08-010` `smoker_front`: `assets/minecraft/textures/block/smoker_front.png` — v4 SHA `ce2bec2d026b954529024c4ead234a39932335cf5367ac0a71c380b055150795`
- `1-1-08-011` `blast_furnace_front`: `assets/minecraft/textures/block/blast_furnace_front.png` — v4 SHA `df580828cf9079059e167dc13b51713d8029cdcf0f0b20374367c71a805d7f62`
- `1-1-08-012` `smithing_table_side`: `assets/minecraft/textures/block/smithing_table_side.png` — v4 SHA `de6b8a0f0da0b27b275371a4fec5f2fbb2aa473ef104a1c5abcc41db4dda5f73`
- `1-1-08-013` `fletching_table_front`: `assets/minecraft/textures/block/fletching_table_front.png` — v4 SHA `1fef8372dbf5790428505f20ab0679faa77543e75fae2f181da50b19799bb258`
- `1-1-08-014` `jukebox_side`: `assets/minecraft/textures/block/jukebox_side.png` — v4 SHA `ce5e56da299713779c49b55fcdb705fbdc1381d4f449615b932877ba13c9fabb`
- `1-1-08-015` `note_block`: `assets/minecraft/textures/block/note_block.png` — v4 SHA `ce5e56da299713779c49b55fcdb705fbdc1381d4f449615b932877ba13c9fabb`
- `1-1-08-016` `enchanting_table_side`: `assets/minecraft/textures/block/enchanting_table_side.png` — v4 SHA `fed6f599ec71ce4307f6e9d08985dc40bedec60d50033e32c6a3c80496939a6a`
- `1-1-08-017` `beehive_front`: `assets/minecraft/textures/block/beehive_front.png` — v4 SHA `3d3fa761ee64d179fa1d29344e3eebbbcae609e2a8053421908dc854181b1dfa`
- `1-1-08-018` `chiseled_bookshelf_empty`: `assets/minecraft/textures/block/chiseled_bookshelf_empty.png` — v4 SHA `a756e5f993f698a566b73b24c0610b9832781d4a5f20358f38442b77d028841d`
- `1-1-08-019` `chiseled_bookshelf_occupied`: `assets/minecraft/textures/block/chiseled_bookshelf_occupied.png` — v4 SHA `a314c81a2dd8c3f14bec2428a0252322e6b37e95810d56316ac23c938540fb4e`
- `1-1-08-020` `pumpkin_side`: `assets/minecraft/textures/block/pumpkin_side.png` — v4 SHA `8f67ee060dd5c1ecc66913caed4294937e3cda8a11d0e0866ec8f558c157c30d`
- `1-1-08-021` `target_side`: `assets/minecraft/textures/block/target_side.png` — v4 SHA `58e9e93f74111c7fbfdb4ef0e8aa4cdf44dd2f4db59ac9347a98d14983ad98bb`

원 출처: [상세 A–G](../../1-1-08_복합기능면.md), [버전 운영](../../ISOLATED_CHAT_VERSIONING.md), [v4 150 실측](../../../../research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv). 상대경로 링크는 GitHub 페이지에서 검증하되 상기 절대 저장소 경로가 기준이다.
