# 1-1-02 — 석재·벽돌 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX02-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-02 / 석재·벽돌 / 17개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-02 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-02_석재벽돌.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-02/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 17/17 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

v4 측정 데이터가 기본. 이전 v5~v38의 관련 모델 연구는 먼저 검색하고 기존 결론을 신규 실측으로 오인하지 말 것.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-02-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-02-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-02-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-02-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-02-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-02-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-02-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 자연석·자갈·연마석·벽돌 간 대비·에지 분포
- **D2:** 줄눈 간격 및 타일 패턴 반복성을 좌/우·상/하 접합으로 확인
- **D3:** 모델 면 회전과 UV 반복이 벽면 패턴에 미치는 영향

## 검토할 정확한 텍스처 17개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-02-001` | `stone` | `b5e10adc72442bfb257ce7ba0b9bbe36475a0c8cdfec89b80dc9517203ff3e9f` | `assets/minecraft/textures/block/stone.png` |
| `1-1-02-002` | `cobblestone` | `bcda95fdf5afa91747657aa198fc0b69ebf44141de30a718075f74045e9a5def` | `assets/minecraft/textures/block/cobblestone.png` |
| `1-1-02-003` | `stone_bricks` | `24415444c9e4815aad4a3a349ecbfc0e027b96be25ac5b7c273c06f16c4fdd2f` | `assets/minecraft/textures/block/stone_bricks.png` |
| `1-1-02-004` | `deepslate_bricks` | `d9533c750ce1910c821626f4fe9187f5d36e9e9cf5efa4fb8fd1b2574ff8f6b1` | `assets/minecraft/textures/block/deepslate_bricks.png` |
| `1-1-02-005` | `polished_andesite` | `1faaa8bacab00d23de46321801e7147a02e388febc43b6c7b31f0ae364e8137e` | `assets/minecraft/textures/block/polished_andesite.png` |
| `1-1-02-006` | `bricks` | `3242cb8e441c940156633b0d867e08c887ddaeaa32343b212d4b1e5ca3dae123` | `assets/minecraft/textures/block/bricks.png` |
| `1-1-02-007` | `tuff_bricks` | `4889db8fab0b3ef4b0cc3ef0d7df469ac3b89233dbeb09fdfecb4f2900b2eaf8` | `assets/minecraft/textures/block/tuff_bricks.png` |
| `1-1-02-008` | `granite` | `9bde1239e00c17b0d2842a941cda606c395039f59ec351ec8866a27e77ee7f8b` | `assets/minecraft/textures/block/granite.png` |
| `1-1-02-009` | `polished_granite` | `455445b2134e66ca93246b6b005f2adc3b75d90baa400f720e1643b66bd8336f` | `assets/minecraft/textures/block/polished_granite.png` |
| `1-1-02-010` | `diorite` | `5f44c6743cd72c00a074e6c43cc9c46b9cf54a82c0cf87c5eb675a7207cff648` | `assets/minecraft/textures/block/diorite.png` |
| `1-1-02-011` | `polished_diorite` | `dfe6b1ae9ecfc263f031d15f53b5775eb519217a2b0c6f2f887fbebf522558d5` | `assets/minecraft/textures/block/polished_diorite.png` |
| `1-1-02-012` | `andesite` | `7c7960dd3dd2084233907c1529dcbea0b8a2195fadaa608027f395b6f430fbd7` | `assets/minecraft/textures/block/andesite.png` |
| `1-1-02-013` | `deepslate` | `dc72c722bec23c929817fab7cc56e08e5e828ae3607fbfb7e7730e68b67d4cfc` | `assets/minecraft/textures/block/deepslate.png` |
| `1-1-02-014` | `deepslate_tiles` | `4e0ff4aa76d467697383c776f94d855d3fc2a49a40363d3fa846e441003ebc57` | `assets/minecraft/textures/block/deepslate_tiles.png` |
| `1-1-02-015` | `blackstone` | `8104d381f680eeb7d71a023aa056b593ef0855821538e435949c94b58033e7cb` | `assets/minecraft/textures/block/blackstone.png` |
| `1-1-02-016` | `polished_blackstone` | `4a36ac06b65d5330bc83e4711b4f62c3afe788b95526f2983730461a35b401ff` | `assets/minecraft/textures/block/polished_blackstone.png` |
| `1-1-02-017` | `chiseled_stone_bricks` | `fbd59c309a861f63cfbb1f0f2348316d16bafa3bdd1ef81550357e1b5778df8f` | `assets/minecraft/textures/block/chiseled_stone_bricks.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX02-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX02-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-02/TEX02-R001/`. 다음은 이 단계만 `TEX02-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-02/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
