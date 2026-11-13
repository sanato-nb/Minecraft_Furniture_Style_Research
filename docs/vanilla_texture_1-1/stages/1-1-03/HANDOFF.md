# 1-1-03 — 금속·금속부품 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX03-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-03 / 금속·금속부품 / 16개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-03 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-03_금속금속부품.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-03/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 16/16 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

v4 표본에 iron_door, iron_trapdoor, anvil_top 등 포함. 금속 반사/광택 표현은 원본 PNG 통계와 런타임 셰이더를 구분할 것.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-03-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-03-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-03-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-03-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-03-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-03-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-03-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 철·구리·녹청·단조 부품의 팔레트 단계
- **D2:** 철문·철다락문·모루/격자의 알파 마스크와 부품면 구분
- **D3:** 고정 블록 상태마다 정적 텍스처 경로 변화 조사

## 검토할 정확한 텍스처 16개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-03-001` | `iron_block` | `dafa9944ba49fe71958553eded50e87d7bea9c7410cfe568745989bede101c49` | `assets/minecraft/textures/block/iron_block.png` |
| `1-1-03-002` | `copper_block` | `1b0aaab59d19b4f909a9ac1208b02363bd2796637b10641a8b7cb0ed587c2aa7` | `assets/minecraft/textures/block/copper_block.png` |
| `1-1-03-003` | `exposed_copper` | `cfb6c192d230fa65f83c7691a4e8d5b686d904b1df329949e792ad85ae372fb7` | `assets/minecraft/textures/block/exposed_copper.png` |
| `1-1-03-004` | `oxidized_copper` | `c784fc83327169877d6a125f2eae00a5fbf784b9caaaa64e2fbc015d664d0bfb` | `assets/minecraft/textures/block/oxidized_copper.png` |
| `1-1-03-005` | `cut_copper` | `4bfc7253ccb07028fcefd90b4f7960873cd843521a1fdaaa6d4c450e7d032bba` | `assets/minecraft/textures/block/cut_copper.png` |
| `1-1-03-006` | `exposed_cut_copper` | `7d2bd18a2b2d92204face126960c1afdf9564d48be015dc9cce9c63435bdf43f` | `assets/minecraft/textures/block/exposed_cut_copper.png` |
| `1-1-03-007` | `weathered_copper` | `c41c28938fb64540576d5f607c87a2446a18bf8b78a388dbc5e147779925062a` | `assets/minecraft/textures/block/weathered_copper.png` |
| `1-1-03-008` | `copper_grate` | `c704177ce251df01260937e301723ceadc29fb6f586ea669782cc7174aa32b72` | `assets/minecraft/textures/block/copper_grate.png` |
| `1-1-03-009` | `iron_trapdoor` | `ca84a5c288bcfe8c9a53f066536175f50effa21e85cfb933094805527c5894ba` | `assets/minecraft/textures/block/iron_trapdoor.png` |
| `1-1-03-010` | `iron_door_bottom` | `e9d6c7dc182ca275a3d455ba28a8df325d1ad0c1539aace4ee11d0359f6fc83a` | `assets/minecraft/textures/block/iron_door_bottom.png` |
| `1-1-03-011` | `gold_ore` | `5253e5a8ea32739a5c8cb1d844f0e46c8c85641f77c3d07dcc03645e2914dd1f` | `assets/minecraft/textures/block/gold_ore.png` |
| `1-1-03-012` | `raw_iron_block` | `e2133b553079d3eb43c6b6dcecbe7f0b3feebc05766a9e28b789ca779a1159f3` | `assets/minecraft/textures/block/raw_iron_block.png` |
| `1-1-03-013` | `heavy_core` | `c74cc835fa46f5c24688cb163ee76122538a6920f806d36151260cc13e8242cc` | `assets/minecraft/textures/block/heavy_core.png` |
| `1-1-03-014` | `iron_door_top` | `54930bb1139268de1855ea03ce5b95097717e25307cbfa1ecce6e665e6da8d88` | `assets/minecraft/textures/block/iron_door_top.png` |
| `1-1-03-015` | `anvil` | `2266db251b99f5df98d8f049e3f7dd6cd85e8146b46011f6918995f392721e48` | `assets/minecraft/textures/block/anvil.png` |
| `1-1-03-016` | `anvil_top` | `757d6f79099583c159e3f95e9981efe0b16b524bed90739ae213142ad40fad26` | `assets/minecraft/textures/block/anvil_top.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX03-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX03-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-03/TEX03-R001/`. 다음은 이 단계만 `TEX03-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-03/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
