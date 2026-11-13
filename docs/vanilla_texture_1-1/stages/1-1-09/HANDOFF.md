# 1-1-09 — 토양·지면 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 현재 단계 버전 **`TEX09-R001` (미러 PNG·정적 모델 소스 검증)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-09 / 토양·지면 / 9개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-09 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-09_토양지면.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-09/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 9/9 항목의 측정 기록 존재**; 이번 단계에서는 A–E의 미러 소스 정적 검사를 9종 모두 수행했고 G를 기록했다. 공식 F는 보류. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

모델링 응용 전 실제 사용 재질과 표본 성격을 분리; 생물군계의 색상 차이는 원본 PNG의 직접 관측이 아님.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-09-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-09-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-09-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-09-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-09-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-09-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-09-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 흙·자갈·진흙 등의 명도 및 반복 무늬
- **D2:** 좌우/상하 이음새·고주파 패턴
- **D3:** grass/podzol PNG와 인게임 tint·주변 블록 효과 구분

## 검토할 정확한 텍스처 9개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-09-001` | `dirt` | `67197d5371efc3ca1638217c38349665dbd5a977b47bfb20075c858dff87d510` | `assets/minecraft/textures/block/dirt.png` |
| `1-1-09-002` | `coarse_dirt` | `6889a193decb2c38cd8559456693c15192917c7b917d6ef9c3c2e142f7819ad4` | `assets/minecraft/textures/block/coarse_dirt.png` |
| `1-1-09-003` | `rooted_dirt` | `3c59420f80c58794b49f822fb9b251779250b759f5c12111fa29f772a635f42b` | `assets/minecraft/textures/block/rooted_dirt.png` |
| `1-1-09-004` | `mud` | `3ddc6e47abc12db1e2e85938da5d0b0d49e0357d8c3424b069f521741ec42d23` | `assets/minecraft/textures/block/mud.png` |
| `1-1-09-005` | `packed_mud` | `143f1729042262d675f0eefe5a8b2704c5d5837f8526aa36b8930328dfb141bf` | `assets/minecraft/textures/block/packed_mud.png` |
| `1-1-09-006` | `mud_bricks` | `b9d94455caf0651b7ff777f2f85a92f4d67d04ae669cd4f65c308595ec9d38fa` | `assets/minecraft/textures/block/mud_bricks.png` |
| `1-1-09-007` | `gravel` | `bc1558fa64b238fabca4cc957e61c232337d410495784b106676bf73e52e16e0` | `assets/minecraft/textures/block/gravel.png` |
| `1-1-09-008` | `grass_block_top` | `52f44b64ce884a13dfe35e4b4da2e35898b790dd4d7a5ea536f1b0c0d56d29b4` | `assets/minecraft/textures/block/grass_block_top.png` |
| `1-1-09-009` | `podzol_top` | `598072d5a4db38ec4ea081a584a2de6b5960785bc2287e18e93427c7433c5d56` | `assets/minecraft/textures/block/podzol_top.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 최초 **`TEX09-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0. 현재 **`TEX09-R001`**: 9개 미러 PNG 재해시·CRC·RGBA·모델 JSON/UV 확인, 공식/인게임 0.
- 다음 검증 보고서: **`TEX09-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-09/TEX09-R001/`. 다음은 이 단계만 `TEX09-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-09/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.


## TEX09-R001 신규 검증 및 다음 인수인계 (2026-11-13)

- [TEX09-R001 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/REPORT.md) · [원본 근거 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/SOURCE_LEDGER.csv) · [픽셀 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/PIXEL_METRICS.csv) · [면별 UV 증거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/UV_FACE_EVIDENCE.csv) · [요약 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/SUMMARY.json).
- **이번 새 바이너리 확인 9/9**: 미러 ref `1.21.11` 9개 PNG 바이트 SHA-256, CRC32/PNG 디코드, RGBA·명도·이음새 분석 9/9. v4 측정 9/9은 **과거 자료**로만 집계.
- **모델/UV 9/9 (미러 소스 단계)**: 전체 54면 연결 행. `mud_bricks` 북/서 미러 UV, `grass_block_top` 틴트 인덱스, `podzol_top` 무틴트 상단 모델 관계 확인.
- **미완료 F 공식 client.jar 인증 0/9, 실제 인게임 정적 렌더 0/9.** 색상·주변 블록 및 눈 상태는 실제 게임과 미대조. 가짜 공식 인증 금지.
- **현재 버전 TEX09-R001 / 다음 후보 TEX09-R002**. 매 수정 전에 실제 `STATE.json` SHA, HEAD, 새 릴리스 경로 재확인. 다른 채팅과 충돌 시 **덮어쓰지 않음**. `v38`는 전역 최신 그대로.
- 기존 A–G 초기 표는 초기 R000 체크포인트 이력으로 보존. **이번 이후 상태는 아래 신규 검증과 `STATE.json` 최신 `phases` 값이 우선**. 애니메이션 전면 보류.
