# 1-1-04 — 직물·양털 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX04-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-04 / 직물·양털 / 9개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-04 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-04_직물양털.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-04/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 9/9 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

실제 실의 두께·표면 물성 추론은 PNG만으로 확정할 수 없음.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-04-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-04-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-04-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-04-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-04-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-04-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-04-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 9색 양털의 명도·채도 분포 및 팔레트 간 상대 차이
- **D2:** 작은 패턴의 반복·균일한 저대비 노이즈
- **D3:** 쿠션·패브릭 응용은 텍스처 소스 사실과 가이드 가설로 분리

## 검토할 정확한 텍스처 9개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-04-001` | `white_wool` | `70c9c9a9901d71ef9a5a89ea2cc4bc0d99ff5e65f733d1467da8b92f746107a5` | `assets/minecraft/textures/block/white_wool.png` |
| `1-1-04-002` | `red_wool` | `07b48cec9b4610e908025807fb85fa686dd50f17918fa677ce655d28b3ba3464` | `assets/minecraft/textures/block/red_wool.png` |
| `1-1-04-003` | `blue_wool` | `2ca85a3e25a3ea9b0d8209edab2ab93f64e458d8c6baf8215536912159a6e2db` | `assets/minecraft/textures/block/blue_wool.png` |
| `1-1-04-004` | `black_wool` | `8cefbc855a4ff04f6125ded6a69e8bd21144802fc466b179665c8c0203daffd9` | `assets/minecraft/textures/block/black_wool.png` |
| `1-1-04-005` | `green_wool` | `a2cd93d4bcead9b808d367fefa17081e12e5bd96ebff6993fc3d486422ecb9ad` | `assets/minecraft/textures/block/green_wool.png` |
| `1-1-04-006` | `yellow_wool` | `cc77805bdc4ccb24d210ec65e304f1c367ae9e9ee0fed404ec99143bf62a2ef2` | `assets/minecraft/textures/block/yellow_wool.png` |
| `1-1-04-007` | `purple_wool` | `f8f5d7eb9145633d27d80c4c06a9a71e21eaea522c277f81a4d6d9e8fd60f0d9` | `assets/minecraft/textures/block/purple_wool.png` |
| `1-1-04-008` | `cyan_wool` | `68706949a22ed0877a42ddca38e5ec428039d52ff23e6614f2900e33cb759303` | `assets/minecraft/textures/block/cyan_wool.png` |
| `1-1-04-009` | `orange_wool` | `de3ec43fe8ca99026bdda3c036a964990e7d9b08c8b67690e2f975ddbdc5ff68` | `assets/minecraft/textures/block/orange_wool.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX04-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX04-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-04/TEX04-R001/`. 다음은 이 단계만 `TEX04-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-04/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
