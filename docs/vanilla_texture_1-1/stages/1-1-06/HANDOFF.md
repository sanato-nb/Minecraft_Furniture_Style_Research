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

## 연구 기준 변경 — 2026-11-13 (새 릴리스 아님)

**사용자 명시 지시: "공식 인증 빼". 이 지시가 본 단계 1-1-06의 최신 수행 기준이며, 위 R001~R004 역사적 기록보다 우선한다.**

- Minecraft Mojang **공식 원본 압축 JAR SHA-1 인증은 연구 범위 및 완료 조건에서 제외**한다. 향후 공식 JAR을 다운로드·검사하거나 이를 R005의 필수 선행 조건으로 삼지 않는다.
- 기존 보고서의 '공식 인증 미완료' 표기는 과거 시점 증거 기록이며 **삭제·수정하지 않는다**. 현재 연구의 공식 인증 상태는 `pending`이 아니라 **`excluded_by_user`** 이다. 이전 데이터의 0건 자체는 역사적 사실로만 남겨둔다.
- 이제 정적 연구 검증은 **① 사용자 제공 GitHub `1.21.11/`의 직접 PNG/JSON·모델 분석, ② 고정 미러와 파일/내용 교차 검증, ③ 실제 Minecraft 1.21.11 정적 인게임 화면 검증**을 서로 구분하여 관리한다. ①·② 관련 기존 8/8 검증 유지, ③ 현재 0/8 실측 미완료.
- 현재 버전 **`TEX06-R004` 유지**, 다음 고유 검증 버전 **`TEX06-R005` 유지**. 본 변경은 **방법·완료 기준만 수정**한 것으로 신규 분석 근거가 없으므로 새 릴리스 버전을 발행하거나 기존 데이터 수치를 중복 집계하지 않는다.
- R005의 우선순위는 `STATIC_FACING_COMPARISON.mcfunction`의 정적 게임 테스트(4개 2×2 패널/16블록, 방향별 상단·측면 및 아이템 렌더 캡처), 결과와 원본 UV/블록 상태 연결 확인. 공식 인증은 검사 목록에서 뺀다.
- 애니메이션 보류, PZ 변환·가구 3D 제작 금지, 다른 단계·공통 `v38`·기존 R001~R004 결과 보존.

## TEX06-R005 — 2026-11-13 사용자 PNG 원본 좌표 단위의 정적 UV·이음 검증

- 현재 **TEX06-R005**, 다음 **TEX06-R006**; 공통 역사적 **v38 불변**. R001–R004 원본 보존.
- 사용자 제공 `1.21.11/`의 **기존 유광 PNG 2개** 직접 재디코딩·SHA-256·PNG CRC 검사 통과. 신규 고유 PNG 0개, 이전 8/8 기록 계승.
- **256개** 위치별 PNG (x,y)–RGBA 경계 쌍, **40개** 아이템 모델공간/블록 조건부 상단 UV 코너 매핑 신규. 각 텍스처의 A+B에서 실제로 참조한 고유 원본 픽셀 좌표는 60개. 기존 R002 집계값(검정 A 916/28, B 4474/8, 흰색 A 412/44, B 17174/14)을 직접 재현했으나 기존 집계를 새 고유 측정으로 더하지 않음.
- [REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R005/REPORT.md) · [256행 픽셀 좌표 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R005/TOP_SEAM_PIXEL_COORDS.csv) · [40행 UV 좌표 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R005/SOURCE_UV_TOP_CORNERS.csv) · [집계 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R005/PANEL_PIXEL_METRICS.csv) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R005/SUMMARY.json) · [재현 Python](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R005/REPRODUCE_TOP_PIXEL_AUDIT.py).
- **인게임 정적 검증 0/8** 유지. 조건부 north-up 소스 회전 투영으로 실제 게임 화면 방향을 인증하지 않음. 공식 JAR SHA-1 인증은 사용자 지시로 필수 범위 제외(성공 인증 아님). 다음 R006은 추가 신규 근거가 있을 때만. 애니메이션 및 PZ 변환·가구 3D 제작 보류.

## TEX06-R006 — 2026-11-13 유광도기 4측면 source UV·RGB 패턴 조건부 검증

- **현재 `TEX06-R006`, 다음 `TEX06-R007`**. 역사적 `v38` 및 R001–R005 결과를 보존.
- 사용자 추출본 `1.21.11/`의 template 모델과 두 유광 blockstates를 직접 읽고 원본 면별 UV와 상태 y회전을 검사. 기존 유광 PNG **2개 Git blob 동일**, 원본 RGBA 값은 **R005의 원본 60개 경계 좌표/PNG**에서 계승(이번 PNG 바이너리 직접 재디코딩/신규 CRC 검사 0; 신규 고유 텍셀 0).
- **새 정적 분석:** 64개 측면 world/source/UV 부호 매핑, 512개 측면 경계 RGB 쌍 지표(16 픽셀쌍씩, 총 8,192개 *문맥별 비교*), 4,096개 측면 2×2 facing 조합 전수 조사, 16개 최적 결과. 기존 R002/R005 숫자를 독립 신규 RGB로 중복 가산하지 않음.
- 각 월드 측면과 두 UV 부호 가정에서 2×2 최적값은 검정 RGB L1 916 / MAE 4.770833 / 28/64 동일, 흰색 412 / 2.145833 / 44/64 동일. **측면/UV 부호에 따른 최적값 불변이므로 최적 이음 점수만으로 실제 게임 facing/부호를 판별할 수 없음**. 원본 모델/PNG의 조건부 2D 계산이며 실제 게임 시각 인증이 아님.
- [R006 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R006/REPORT.md) · [측면 소스 UV 매핑](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R006/SIDE_FACE_SOURCE_MAP.csv) · [측면 경계 512행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R006/SIDE_EDGE_PAIRWISE.csv) · [2×2 최적 16행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R006/SIDE_PANEL_OPTIMA.csv) · [재현 Python](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R006/REPRODUCE_SIDE_PIXEL_AUDIT.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R006/SUMMARY.json).
- **인게임 정적 렌더 0/8**. 사용자 지시로 공식 client.jar SHA-1 인증은 범위 제외(성공 인증 아님). 애니메이션, PZ 변환, 실제 가구 3D 모델 제작 모두 보류. 다음 R007은 신규 근거가 있을 때만.

## 연구 기준 변경 — 2026-11-13 (인게임 검증 제외 · 새 TEX06 릴리스 아님)

**사용자 최신 지시: "인게임 검증은 제외해줘 어차피 모델링이랑 텍스텨있는데 필요없을거같아".** 본 변경은 과거 보고서의 정적 인게임 검증 요청이나 보류 표기보다 우선한다.

- **실제 Minecraft 실행, 정적 인게임 스크린샷, 아이템/블록 화면 UV 및 facing 관찰·검증을 연구 요구사항과 완료 조건에서 제외**한다. 더는 사용자에게 이를 필수 작업·R007 선행 조건으로 요청하지 않는다.
- 계속 사용하는 근거는 사용자 제공 `1.21.11/`의 **PNG 바이너리·RGBA 픽셀, 부모/리프 모델 JSON, item JSON, blockstates JSON, face UV 및 상태별 수학적 변환**과 관련 고정 미러 교차 검사다. 이러한 근거로 보이는 외형·무늬 패턴의 정적 **소스 수준** 구조를 판단한다.
- 모델 JSON과 원본 텍스처만으로 해당 버전 자산의 선언된 모델/색상/기하/UV를 분석할 수 있으므로 실게임은 필수 아님. **단, 게임 엔진이 실제 렌더링한 시점·면의 방향이나 회전/조명 결과를 검증했다는 뜻이 아니다**. R005/R006의 UV 부호 후보를 확정 사실로 격상시키지 않는다. 실제 PBR 반사나 런타임 동작도 추정으로 인증하지 않는다.
- **사용자 압축 해제 1.21.11 PNG·관련 JSON 및 비공식 미러 교차 검증 8/8 유지**. 이는 8개 파일 경로에 대한 소스 기반 검증 성과이며, 모든 가능한 배치/렌더 결과에 대한 완전 인증은 아니다. 과거 `ingame_static_render_verified_count=0` 등은 **역사적 관찰 기록으로 유지**하되 추가해야 할 8개 검증을 의미하지 않는다.
- 기존 사용자 지시대로 Mojang 공식 압축 JAR SHA-1 인증도 제외 유지. 범위 제외는 인증 성공과 다르다.
- 변경은 **방법론/범위 설정만 수정**했으므로 `current_revision=TEX06-R006`, `next_revision=TEX06-R007` 그대로 유지. R001–R006 불변 릴리스 및 공통 `v38`는 손대지 않는다. **신규 소스 근거가 있을 때만 R007** 생성.
- 이후 사용자가 "계속해줘"라고 요청하면 재입장 후 **남아 있는 소스 기반 실증 분석만** 계속한다. 소스 관점에서 할 연구가 다 끝났거나 사용자 제공 원본이 부족해 실제 더 진행할 수 없다면 **버전/성과를 억지로 늘리지 말고 멈춰서 사유와 필요한 자료를 알려준다**. 단순히 인게임 캡처가 없다는 사유만으로 중단/도움 요청하지 않는다.
- 애니메이션 분석, Project Zomboid 변환, 실제 가구 3D 모델링 제작은 별도 지시까지 이 단계 범위 밖이다.

## TEX06-R007 — 2026-11-13 8개 원본 PNG의 색상별 명암 무늬 교차상관 신규 검증

- **현재 `TEX06-R007`, 다음 `TEX06-R008`**. 고정 `1-1-06` 8종, 공통 `v38` 불변. 기존 R001–R006의 불변 파일 보존. `STATE.revisions`에 누락됐던 기존 **R005 릴리스 색인 항목만 복원**했고 R005 파일은 수정하지 않았음.
- 사용자 제공 `1.21.11/` **8 PNG 모두를 바이너리 SHA256·PNG 청크 CRC 재검증하고 16×16 RGB 직접 재디코딩**. 이전 R001–R006의 같은 PNG 2,048 원본 화소를 별도 목적에 재사용; 신규 고유 PNG **0**, 신규 미관찰 고유 텍셀 **0**.
- **기존 R001~R006에서 없던 정적 비교:** RGB를 BT.709 가중 8비트 코드값 명도(선형 광학값 아님)로 변환, 같은 위치의 정규화된 256픽셀 Pearson r를 계산. **총 28쌍 × 1,024가지(4 회전×16×16 순환 이동)=28,672개의 정렬 점수**, 최적 배치와 두 번째 후보를 CSV로 기록. 이는 회전·순환 통계 비교수이며 신규 텍스처·화소 수치에 중복 가산하지 않음.
- **염색 일반 테라코타 5종끼리 10쌍:** 동일 위치 r **0.955880–0.992976**. **기본 terracotta ↔ 염색 5종 5쌍:** r **0.482668–0.490693**. 일반 계열 내부의 **15쌍 전부 회전0·이동0이 1,024개 중 최적**. 일반↔유광 12쌍은 같은 위치 r **-0.062656 ~ -0.009486**, 검정↔흰색 유광 1쌍은 r **0.123941**. 색상 다른 원본이 동일 원본을 도색했다는 제작 이력의 직접 증명은 아님.
- [R007 연구 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R007/REPORT.md) · [28쌍 전체 계산 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R007/PAIRWISE_LUMA_28.csv) · [재현 Python](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R007/REPRODUCE_LUMA_CORRELATION.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R007/SUMMARY.json).
- 사용자 최신 범위대로 **인게임 검증·Mojang 공식 압축 JAR 인증 제외** 유지. 기존 `0/8`은 역사적 계수이며 미완료 차단 요소가 아님. 애니메이션, PZ 변환, 실제 가구 3D 모델 제작 제외. 다음 진행 때 새로운 **실제 소스 기반** 질문/근거가 없으면 R008을 만들지 말고 중단 안내.

## TEX06-R008 — 2026-11-13 애니메이션 연구 보류 해제 및 8종 무(無) 애니메이션 실측

- 사용자 최신 요청 **"그럼이제 애니메이션하자"**로 **본 1-1-06 단계의 애니메이션 연구 보류를 해제**. 과거 R001–R007·START_PROMPT·전역 정책의 보류 문구는 역사적 기록이며, 이 단계의 최신 사용자 지시가 우선함. 인게임 검증과 공식 Mojang 압축 JAR 인증은 계속 범위 밖. PZ 변환·가구 3D 제작도 계속 제외.
- 사용자 추출 `1.21.11/assets/minecraft/textures/block/` 고정 **8 PNG 전부 바이너리 PNG signature·IHDR·청크·CRC32 재검사**. **8/8 가로16×세로16 = 단일 기본 텍스처**. APNG `acTL` 청크 **0/8**. 기존 PNG SHA256은 R007 기록 계승(이번 SHA256 독립 재계산 0).
- **8개의 대응 `.png.mcmeta` 파일을 전부 GitHub 직접 요청**해 8/8 **404 Not Found** 확인. 기본 Minecraft 1.21.11 사용자 추출 원본에 8종 **프레임 애니메이션 정의 0종**. 방향별 패턴 회전은 상태 변화·정적 UV이지 프레임 애니메이션이 아님. `애니메이션 부재`도 이번 새 검증 근거이므로 R008 발행.
- 동일 추출본에서 **단계 밖 양성 대조군 5개**(`water_still`, `lava_still`, `fire_0`, `sea_lantern`, `prismarine`)의 실제 PNG+mcmeta를 직접 검수: 원본 16×16 프레임 슬롯 각각 32/20/32/5/4, 명시/암묵 재생 순서 항목 각각 32/38/32/5/22, 프레임 시간 각각 2/2/1/5/300 ticks(마지막 보간 true). 이 5종은 **1-1-06의 8종에 더하지 않음**.
- [R008 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R008/REPORT.md) · [8개 정적 소스 검증 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R008/SOURCE_ANIMATION_AUDIT_8.csv) · [5개 동적 양성 대조 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R008/ANIMATED_POSITIVE_CONTROLS_5.csv) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R008/SUMMARY.json) · [재현 Python](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-06/TEX06-R008/REPRODUCE_ANIMATION_SOURCE_AUDIT.py).
- **현재 `TEX06-R008`, 다음 예약 `TEX06-R009`**. 1-1-06 8종의 정적·소스 애니메이션 존재 여부 검사 완료. 본 8종에는 애니메이션 프레임 연구할 대상이 없으므로 근거 없이 R009를 생성하지 말 것. 다른 움직이는 텍스처 연구는 각각 담당 단계에서 별도로 수행.
