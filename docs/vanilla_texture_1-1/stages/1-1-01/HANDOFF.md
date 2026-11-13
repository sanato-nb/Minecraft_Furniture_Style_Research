# 1-1-01 — 목재·원목 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX01-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-01 / 목재·원목 / 18개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-01 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-01_목재원목.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 18/18 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

v38: stripped_oak_log는 선반의 #particle로 등장하며 기하 선언면은 0. 본 작업의 목재 소재 원본 표본과 연결할 때 중복 계측하지 말 것.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-01-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-01-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-01-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-01-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-01-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-01-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-01-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 판자 vs 원목 단면·옆면 색·명암·채도 차이
- **D2:** 목재 무늬 방향·인접 타일 반복 이음새
- **D3:** 판자·원목의 UV 방향과 실제 모델 표면 연결

## 검토할 정확한 텍스처 18개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-01-001` | `oak_planks` | `65665943ef9c8bcf63fc67d2083ed0c50243f724106d0e4bb1abea5d921b16d3` | `assets/minecraft/textures/block/oak_planks.png` |
| `1-1-01-002` | `spruce_planks` | `a1e4cd5b1eb20bc03e8d1f3fdae59034363c3b2dde7f505694e4323222e00e21` | `assets/minecraft/textures/block/spruce_planks.png` |
| `1-1-01-003` | `birch_planks` | `e1559eaabbee0c1ea0fca983e3bcba1a188e0a29b6c25ea7d725651cc2569216` | `assets/minecraft/textures/block/birch_planks.png` |
| `1-1-01-004` | `dark_oak_planks` | `665f44b119f5a21711c4cb83749d871635134c001cb0c14761c4f02a40dd8645` | `assets/minecraft/textures/block/dark_oak_planks.png` |
| `1-1-01-005` | `cherry_planks` | `46f93c17e9baae47e9a6b07b049255a94d72b2d4d74323384f9f72649f7be581` | `assets/minecraft/textures/block/cherry_planks.png` |
| `1-1-01-006` | `mangrove_planks` | `8a23e913f39c14c050df721a775b2e2bd0dd7b9b0a74cab1056070e3d781119f` | `assets/minecraft/textures/block/mangrove_planks.png` |
| `1-1-01-007` | `acacia_planks` | `3f84918024e190f2767e03631d8c35b31fa5cd9235d7b114738224297dca6797` | `assets/minecraft/textures/block/acacia_planks.png` |
| `1-1-01-008` | `jungle_planks` | `eef0710428abe05aa915dd7f8d3f2ae2b85aba719a85c6f3e5daf7c5b2aae2d3` | `assets/minecraft/textures/block/jungle_planks.png` |
| `1-1-01-009` | `bamboo_planks` | `030e245c4bd4cd30e07b3195c2bd0593d8a123f4814b622a36ae060056b1c0cf` | `assets/minecraft/textures/block/bamboo_planks.png` |
| `1-1-01-010` | `pale_oak_planks` | `d478269d770f5bbefc0373a597155329d2f8d089ab76376c14c7eec8e79ea66f` | `assets/minecraft/textures/block/pale_oak_planks.png` |
| `1-1-01-011` | `crimson_planks` | `eba5d8f1fc24a284237178111e7f99a5c836ce89ab5c5013aff69b8298cb0f03` | `assets/minecraft/textures/block/crimson_planks.png` |
| `1-1-01-012` | `warped_planks` | `3a7da9c4a54eafaec07b50e474de8695a321401f5e5c1c3b435148056e94c2ea` | `assets/minecraft/textures/block/warped_planks.png` |
| `1-1-01-013` | `oak_log` | `61735859c9c9ea82601191a77c6f256d93619cbaf7cad998a3ed5762877a34e6` | `assets/minecraft/textures/block/oak_log.png` |
| `1-1-01-014` | `spruce_log` | `a87a55ec454cb682934666bdf864dbd7fab4a561415f76834f3c53bb75bf0ba9` | `assets/minecraft/textures/block/spruce_log.png` |
| `1-1-01-015` | `birch_log` | `81f2e40265758846858019a6b65b7617a205ac654dd2854b8b6cd31426e7c930` | `assets/minecraft/textures/block/birch_log.png` |
| `1-1-01-016` | `oak_log_top` | `a520800a833ea0c6214481245ab40397aa0c08b4ffc909046dac266386f9fc01` | `assets/minecraft/textures/block/oak_log_top.png` |
| `1-1-01-017` | `stripped_oak_log` | `a0beb15ad3d8223308d5b36a3ee9c3b9c2b5ed9b4fadc7c5bdbc69823dfb1bc2` | `assets/minecraft/textures/block/stripped_oak_log.png` |
| `1-1-01-018` | `bamboo_mosaic` | `fd1f84c51173cdbc46579e01cc67ff9df9bdbbcbac53e86662ec447865a44dfe` | `assets/minecraft/textures/block/bamboo_mosaic.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX01-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX01-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-01/TEX01-R001/`. 다음은 이 단계만 `TEX01-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
