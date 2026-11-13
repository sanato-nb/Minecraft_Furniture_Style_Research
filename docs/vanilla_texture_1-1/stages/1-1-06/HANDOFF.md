# 1-1-06 — 도기·유광도기 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX06-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-06 / 도기·유광도기 / 8개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-06 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-06_도기유광도기.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-06/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 8/8 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

유광 효과에 대해 실제 PBR 반사와 혼동하지 말 것. 원본 그림의 색·패턴만 확정.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-06-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-06-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-06-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-06-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-06-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-06-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-06-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 일반 테라코타와 유광 도기의 팔레트·명도
- **D2:** 무늬 이어붙이기와 UV/회전 상태에 따른 패턴 방향
- **D3:** 특정 패턴을 만드는 블록 상태의 정적 회전·UV 연결

## 검토할 정확한 텍스처 8개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-06-001` | `terracotta` | `b2458267eac6b6f35d02990ee3244edf1f43fbe258bd6dfe15189cf2eaf42ae8` | `assets/minecraft/textures/block/terracotta.png` |
| `1-1-06-002` | `white_terracotta` | `9feeb13f19514ea58a5b6e942df7a8595330e61173f8d0a13c83b78acd1bd62e` | `assets/minecraft/textures/block/white_terracotta.png` |
| `1-1-06-003` | `orange_terracotta` | `3074d90b0a27d1c149df2f3eacc9c6895c4cc0548999f864146dc18f64bcab5a` | `assets/minecraft/textures/block/orange_terracotta.png` |
| `1-1-06-004` | `blue_terracotta` | `99b4ec0a8a02a9d609d4987cbb7ba594a59f93c76b5fd98e3a1f12c2df1f9a70` | `assets/minecraft/textures/block/blue_terracotta.png` |
| `1-1-06-005` | `green_terracotta` | `ffe10089bcef9873c74f18be35e605c5d035f472c06bf677746d39ff8a656c07` | `assets/minecraft/textures/block/green_terracotta.png` |
| `1-1-06-006` | `yellow_terracotta` | `7c00bf901f78ad628a06335d47310a6b18c1419243d4150e32cdf01d51bafca6` | `assets/minecraft/textures/block/yellow_terracotta.png` |
| `1-1-06-007` | `black_glazed_terracotta` | `214ce8ca46c60a42b8863655b3895aca839c7ef7cfa511a192dc1974a0ca2758` | `assets/minecraft/textures/block/black_glazed_terracotta.png` |
| `1-1-06-008` | `white_glazed_terracotta` | `cb1ebf9f3f3e93009ff4cab1b2b2b70d41fd87caa40c71942ae51996d12498b4` | `assets/minecraft/textures/block/white_glazed_terracotta.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX06-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX06-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-06/TEX06-R001/`. 다음은 이 단계만 `TEX06-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-06/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.

## TEX06-R001 — 2026-11-13 직접 검증 후 인수인계

- 현재 고유 버전 **TEX06-R001** · 다음 **TEX06-R002** · 공식 전체 프로젝트 **v38 유지**.
- [신규 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R001/REPORT.md), [파일별 출처](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R001/SOURCE_LEDGER.csv), [요약 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R001/SUMMARY.json).
- 대상 8/8 PNG를 비공식 미러 1.21.11 태그(커밋 `7241a12cc2707abd7022f399c5d9033153e492e1`)에서 실제 이진 복원하고 SHA-256, Pillow verify, 모든 PNG 청크 CRC32, RGBA **2,048픽셀** 독립 검증. SHA 8/8 기존 v4 일치. 본 단계 새 실측 8종이지, 기존 기록을 중복 누적한 값이 아니다.
- 리프 모델 8·blockstates 8·부모 3의 JSON/UV를 열람. 일반 6종 `cube_all` vs 유광 2종 `template_glazed_terracotta`; 유광은 면 UV 회전과 facing별 모델 y회전 각각 확인. D1 8종, D2 2종 2×2×256 조합, D3 2종 **정적 자료 수준** 확인.
- **공식 Mojang client.jar 인증 0/8, 인게임 정적 검증 0/8**, 정적 파일 검수만 완료. 이미지 평면의 시계방향 회전 최적 조합을 실제 인게임 방향으로 단정하지 않는다. F 및 모든 A–G 최종 인증 미완료.
- v35~v38 일부 역사 자료를 교차 검사해 이 8종 중복 집계 근거 없음. 전체 과거 자료 부재를 단정하지 않음.
- 다음 R002는 공식 `client.jar`에서 원본 8개 및 모델 JSON을 추출하고 SHA로 검증하거나 인게임 정적 Facing 장면을 확인할 때만 생성. 애니메이션/Project Zomboid/가구 모델링 연구는 계속 보류.

## TEX06-R002 — 2026-11-13 신규 정적 패턴·상태 연결 검증

- 현재 고유 버전 **TEX06-R002** / 다음 **TEX06-R003**. 전체 통합 **v38** 불변.
- R001 누적 미러 PNG 8/8 유지. R002는 **검정·흰색 유광 2종만 기존 PNG 직접 재열람·SHA 재확인**, 신규 고유 텍스처 **0개**.
- [R002 상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R002/REPORT.md) · [512개 경우의 수 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R002/TOP_FACING_2X2_512_COMBINATIONS.csv) · [픽셀쌍 이음 근거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R002/EDGE_SEAM_PAIRWISE.csv) · [독립 SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R002/SUMMARY.json).
- 2개 유광 각각 **2×2 회전 조합 256개** 실측 → 총 **512개**. 최적 무늬 경계 RGB 완전 일치 픽셀쌍은 검정 **28/64**, 흰색 **44/64**; 오차가 0이거나 패턴 완전 일치가 아님.
- 원본 정적 blockstates의 south0/west90/north180/east270 model Y 회전을 상단 PNG 이미지 회전과 **두 투영 관례로 구분**하여 조합별 방향 가설 생성. 추론을 실제 인게임 방향으로 확정하지 않음.
- Mojang 공식 1.21.11 client.jar 다운로드를 실제 시도했으나 실행 환경 접근 실패. **공식 인증 0/8, 인게임 정적 0/8** 유지. 다음 채팅의 PC용 검증 스크립트 `VERIFY_OFFICIAL_1_21_11.py`는 공식 클라이언트에서 실제 실행·검증 전이므로 결과 인증에 포함하지 않음.
- A–G 전체 인증 0/8; R002 새 근거는 D2/D3 정적 모델·화소 관계. 다른 단계 및 루트 파일·동적 기록 변경 금지. 애니메이션, PZ 변환, 가구 3D 제작 보류.

## TEX06-R003 — 2026-11-13 사용자 제공 1.21.11/ 원본 검증 반영

- 현재 **TEX06-R003**, 다음 **TEX06-R004**. 전체 공식 프로젝트 **v38 불변**.
- 새 우선 출처: 사용자가 직접 1.21.11 JAR을 압축 해제했다고 설명한 [GitHub `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/e06206f3cf2fad1d1f9ea3839e9d36a548fe9f4f/1.21.11). 직접 읽은 버전 JSON의 ID는 1.21.11. 이것만으로 Mojang 공식 JAR SHA-1 인증이 되지는 않음.
- **8/8 PNG**: 실제 사용자 바이너리의 SHA256 재계산·PNG 청크 CRC 검사 및 16×16 확인; v4/R001 비공식 미러와 **8/8 SHA256 및 Git blob 동일**.
- **8 리프 모델 JSON + 8 blockstates JSON + 4 공통 부모 모델 JSON** 직접 열람·구조 검사, 기존 미러와 SHA 동일. 유광 UV 면별 회전과 4방향 상태 모델 Y 회전 유지.
- 이전 **R001 2,048픽셀** 및 **R002 512개 2×2 회전 조합** 결과는 입력 파일 바이트가 같으므로 재사용만 했으며 **이번 신규 픽셀 측정 0**, 새 고유 텍스처 0.
- 검증 등급 1. 사용자 추출본 **8/8** / 2. 미러 바이트 일치 **8/8** / 3. Mojang 공식 JAR SHA-1 **0/8** / 4. 인게임 정적 화면 **0/8**.
- [R003 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R003/REPORT.md) · [PNG/모델/블록 상태 해시 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R003/SOURCE_LEDGER.csv) · [정적 JSON·UV 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R003/STATIC_SOURCE_AUDIT.json) · [4계층 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R003/FOUR_TIER_VERIFICATION.csv).
- 후속 **TEX06-R004**: 압축 원본 JAR 해시 공식 인증 혹은 인게임 정적 렌더 추가 증거 확보. 애니메이션/PZ 변환/가구 3D 제작 중지 유지.

## TEX06-R004 — 2026-11-13 신규 아이템 출처·유광 면 방향 정적 분석

- 현재 단계 버전 **TEX06-R004**, 다음 **TEX06-R005**, 통합 체크포인트 **v38 불변**. 이전 R001–R003 근거/버전 원본 그대로 보존.
- 신규 소스: 사용자 `1.21.11/assets/minecraft/items/`의 관련 **8개 아이템 JSON을 직접 확인**, 8개가 각자 `minecraft:block/<id>`를 참조하고 고정 비공식 미러에서 직접 대조한 Git blob도 **8/8 일치**.
- 신규 기하 계산: 유광 2종의 `4 facing × 6 source faces` 총 **48행** 원본 로컬 면→월드 면 법선 매핑 (3D Y축 표준 변환 적용). 원래 face UV 선언과 최종 월드 렌더상 2D 이미지 회전을 **구분**, Minecraft 실행으로 확인하지 않음.
- 기존 **R002 64개 원본 이음쌍 RGB 점수**를 조건부 top-view facing명으로 변환한 **64행 lookup** 저장. 기존 R002 최적 검정 MAE 4.770833/28동일쌍, 흰색 2.145833/44동일쌍 재확인. **새 PNG/RGBA 계측 0**, 신규 고유 텍스처 0.
- 아이템 JSON은 블록 모델을 그대로 참조하지만, 설치된 유광 블록은 facing별 모델 y회전이 추가됨. **구조상 차이**만 확인; 인게임 아이템 vs 설치 블록의 보이는 방향은 아직 검증되지 않음.
- 실게임 재현용 4패널/16블록 `STATIC_FACING_COMPARISON.mcfunction`을 준비했으나 **미실행**. 게임 캡처·공식 원본 JAR SHA-1 검사 **계속 0/8**.
- [R004 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R004/REPORT.md) · [아이템 SHA 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R004/ITEM_MODEL_LEDGER.csv) · [월드 방향 48행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R004/WORLD_FACE_UV_MAPPING.csv) · [기존 이음값 facing LUT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R004/FACING_EDGE_LOOKUP.csv) · [실게임 시험 배치 명령](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R004/STATIC_FACING_COMPARISON.mcfunction).
- **TEX06-R005**는 정식 압축 JAR SHA-1 확인 또는 게임 내 정적 실화면 검증 같은 신규 1차 증거가 있을 때만 생성. 다른 1-1-XX 단계, 애니메이션, PZ 변환, 가구 3D 제작, 공통 v38 변경 금지.
