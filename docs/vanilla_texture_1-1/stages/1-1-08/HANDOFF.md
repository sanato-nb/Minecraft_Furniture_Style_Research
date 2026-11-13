# 1-1-08 — 복합·기능면 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX08-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-08 / 복합·기능면 / 21개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-08 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-08_복합기능면.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-08/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 21/21 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

v36/v37에서 furnace, blast_furnace, smoker 정적 모델·PNG 검증 기록 존재: v37 비애니메이션 정적 PNG 11종/2,816픽셀, 그중 다중 프레임 PNG 2종은 분석 보류. v35에서 beehive 관련 기록 존재. 모두 기존 출처로 회수해 중복 방지.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-08-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-08-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-08-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-08-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-08-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-08-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-08-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 작업대·화로·훈연기·책장·통의 정면·측면·상단 기능적 재질 분할
- **D2:** 꺼짐·켜짐 등 두 고정 텍스처 차이만 비교, 다중 프레임 해독 금지
- **D3:** 기능면의 #all·#front·#side 슬롯 및 실제 face UV/particle 분리

## 검토할 정확한 텍스처 21개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-08-001` | `crafting_table_front` | `1659c76a33039640e8bd5584af8db04bf626486432a389bcaf1567e1a45c6464` | `assets/minecraft/textures/block/crafting_table_front.png` |
| `1-1-08-002` | `barrel_side` | `30f31d8cecfbd44412af13983eee56220bcffbf7ce8dd5a948f1ab73c98d8dc8` | `assets/minecraft/textures/block/barrel_side.png` |
| `1-1-08-003` | `bookshelf` | `cf2b8c0da8e7164162ad4991916492b724c62c31de6c18b2abb7d60ec19ba418` | `assets/minecraft/textures/block/bookshelf.png` |
| `1-1-08-004` | `crafting_table_side` | `e9755fc6da763909b285342eae12c5f7d1cc8462fab695bb157504ea207cda8c` | `assets/minecraft/textures/block/crafting_table_side.png` |
| `1-1-08-005` | `smithing_table_front` | `f7a5479a3e1d3e3f604ec1b22634736ea952b676fef20e954a9607f15fb13ba0` | `assets/minecraft/textures/block/smithing_table_front.png` |
| `1-1-08-006` | `barrel_top` | `6b4cb64b1c34bd87225147479100bec9889ac69c7dcdb5694003248e3004fe1e` | `assets/minecraft/textures/block/barrel_top.png` |
| `1-1-08-007` | `barrel_bottom` | `1addc57c6221210107b7e64db8d2756983458a14828d8eb85b61f13bbf5a1028` | `assets/minecraft/textures/block/barrel_bottom.png` |
| `1-1-08-008` | `loom_side` | `526372c59e91f10c1d690124d3f72a3938a154081cbc1a26a6151b924c8293f2` | `assets/minecraft/textures/block/loom_side.png` |
| `1-1-08-009` | `furnace_front` | `aae808f71f1bddf4a25592f7dd3d7f6e9b3adaa739502170766424f4eb6bf9c5` | `assets/minecraft/textures/block/furnace_front.png` |
| `1-1-08-010` | `smoker_front` | `ce2bec2d026b954529024c4ead234a39932335cf5367ac0a71c380b055150795` | `assets/minecraft/textures/block/smoker_front.png` |
| `1-1-08-011` | `blast_furnace_front` | `df580828cf9079059e167dc13b51713d8029cdcf0f0b20374367c71a805d7f62` | `assets/minecraft/textures/block/blast_furnace_front.png` |
| `1-1-08-012` | `smithing_table_side` | `de6b8a0f0da0b27b275371a4fec5f2fbb2aa473ef104a1c5abcc41db4dda5f73` | `assets/minecraft/textures/block/smithing_table_side.png` |
| `1-1-08-013` | `fletching_table_front` | `1fef8372dbf5790428505f20ab0679faa77543e75fae2f181da50b19799bb258` | `assets/minecraft/textures/block/fletching_table_front.png` |
| `1-1-08-014` | `jukebox_side` | `ce5e56da299713779c49b55fcdb705fbdc1381d4f449615b932877ba13c9fabb` | `assets/minecraft/textures/block/jukebox_side.png` |
| `1-1-08-015` | `note_block` | `ce5e56da299713779c49b55fcdb705fbdc1381d4f449615b932877ba13c9fabb` | `assets/minecraft/textures/block/note_block.png` |
| `1-1-08-016` | `enchanting_table_side` | `fed6f599ec71ce4307f6e9d08985dc40bedec60d50033e32c6a3c80496939a6a` | `assets/minecraft/textures/block/enchanting_table_side.png` |
| `1-1-08-017` | `beehive_front` | `3d3fa761ee64d179fa1d29344e3eebbbcae609e2a8053421908dc854181b1dfa` | `assets/minecraft/textures/block/beehive_front.png` |
| `1-1-08-018` | `chiseled_bookshelf_empty` | `a756e5f993f698a566b73b24c0610b9832781d4a5f20358f38442b77d028841d` | `assets/minecraft/textures/block/chiseled_bookshelf_empty.png` |
| `1-1-08-019` | `chiseled_bookshelf_occupied` | `a314c81a2dd8c3f14bec2428a0252322e6b37e95810d56316ac23c938540fb4e` | `assets/minecraft/textures/block/chiseled_bookshelf_occupied.png` |
| `1-1-08-020` | `pumpkin_side` | `8f67ee060dd5c1ecc66913caed4294937e3cda8a11d0e0866ec8f558c157c30d` | `assets/minecraft/textures/block/pumpkin_side.png` |
| `1-1-08-021` | `target_side` | `58e9e93f74111c7fbfdb4ef0e8aa4cdf44dd2f4db59ac9347a98d14983ad98bb` | `assets/minecraft/textures/block/target_side.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX08-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX08-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-08/TEX08-R001/`. 다음은 이 단계만 `TEX08-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-08/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
