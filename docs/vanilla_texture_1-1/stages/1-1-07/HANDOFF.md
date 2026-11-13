# 1-1-07 콘크리트·색면 — 최신 인수인계

## TEX07-R005 (2026-11-13) — 공식 인증 요구 제외

- 사용자의 **“공식 인증 빼”** 지시에 따라 **Mojang 공식 client.jar 전체 SHA-1/메타데이터 인증은 1-1-07의 필수 검증·완료 기준·후속 작업에서 제외**한다. 공식 인증을 완료했다고 간주하는 뜻이 아니다.
- 앞으로는 사용자 GitHub [`1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11) PNG·JSON 직접 검사 → 필요할 때 비공식 미러 교차 검증 → 정적 모델/색상/UV/블록 상태 분석을 계속한다.
- **인게임 정적 검증은 별도 유지:** 실제 게임 렌더 관찰 0/7. 캡처/게임 실행 증거가 있으면 진행한다. 애니메이션 분석은 계속 보류한다.
- R001~R004 기존 보고서·CSV·JSON·커밋·R004 보조 인증 스크립트는 **역사 기록으로 그대로 보존**, 더 이상 인증 스크립트 실행을 다음 단계의 요구사항으로 잡지 않는다. R005는 **정책 변경만**이며 신규 텍스처/픽셀/모델 분석 건수 0.
- [R005 변경 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R005/REPORT.md), [R005 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R005/SUMMARY.json). 글로벌 `v38` 및 다른 재질 단계는 불변.
- **다음 TEX07-R006.** 작업 전 최신 STATE SHA 및 R006 출력 폴더 충돌 확인. 연구 범위 1-1-07 유지, PZ 변환 및 실제 가구 제작 금지.

---

## 아래는 R004 이하 과거 인수인계로, 당시의 공식 인증 언급은 **현재 의무사항이 아닌 역사 기록**이다.

# 1-1-07 콘크리트·색면 — 최신 인수인계

## TEX07-R004 (2026-11-13) — 사용자 추출본 정적 모델 선언 필드·버전 내부 정보

- **이번 새 근거:** [R004 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R004/REPORT.md)와 사용자 `1.21.11/version.json` 직접 확인: id 1.21.11, protocol 774, world 4671, 리소스팩 75.0, Java 21. 내부 버전 일관성의 근거일 뿐 공식 JAR 인증 아님.
- R003에서 확인된 7색+31개 파일·42개 모델 면을 중복 계상하지 않고, **새로운 필드 감사**: 6면 모두 방향 일치 `cullface`, 면별 UV/rotation/tintindex/shade 명시 0, 7개 색 모델의 개별 display override 0. 공통 부모의 `gui_light=side`, 공유 아이템 표시 변환 7종을 CSV로 별도 기록.
- [42면 선언 감사](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R004/42_STATIC_FACE_FLAGS.csv) / [표시 변환 7건](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R004/7_DISPLAY_CONTEXTS.csv) / [R004 상태 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R004/SUMMARY.json).
- Mojang 공식 manifest/파일 서버 DNS 접속 실패. **공식 JAR SHA-1 인증 0/7**, **인게임 정적 검증 0/7**. 다음에 사용자가 실제 JAR을 확보하면 [검증용 스크립트](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R004/VERIFY_CLIENT_JAR.py)를 이용해 공식 SHA1과 31개 엔트리 해시를 *별도로* 확인할 수 있음. 이 스크립트는 실제 client.jar 인증에 사용된 것이 아니므로 현재 상태를 높이지 말 것.
- 다음 단계는 **TEX07-R005**. 작업 시작 전 단계 STATE SHA·current_revision, R005 출력 폴더 충돌 확인. 이전 R001~R003 불변, 다른 단계/전체 **v38** 수정 금지. 애니메이션 연구, 좀보이드 변환, 실제 가구 제작 금지.

---

## 이전 단계의 인수인계 원문 보존 (R003 이하)

# 1-1-07 콘크리트·색면 — 최신 인수인계

## TEX07-R003 / 사용자 제공 1.21.11 자료 검증 (2026-11-13)

- 사용자 직접 JAR 추출이라고 알려준 [`1.21.11/` 폴더](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)의 7 콘크리트 PNG, 7 blockstate, 7 block model, 7 item, 공통 모델 3 = **31개 파일 원본 직접 조회**.
- 비공식 InventivetalentDev 미러 1.21.11과 실제 PNG 바이트/JSON 내용 및 Git blob SHA가 **31/31 일치**. 사용자 추출본 PNG **7/7 SHA256·CRC 정합**, 42개 모델 면 참조/UV 수치 명시 0·유도 42도 확인. 조사 당시 source commit `2a43897b8f605b4e0c96a272bca476ee6b70058e`.
- 새 [R003 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R003/REPORT.md) 및 [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R003/SUMMARY.json)와 31/7/7행의 교차검증 CSV 참조.
- 증거 수준 4축 구분: **사용자 제공 추출본 7/7**, **미러 교차 7/7**, **Mojang 공식 JAR SHA-1 인증 0/7**, **인게임 정적 검증 0/7**. 추출본과 미러가 같아도 Mojang 공식 인증이 아님.
- R001/R002 픽셀 결과 중복 집계 금지. 기존 기록 보존. 다른 1-1 단계 및 글로벌 `v38` 수정 금지. 애니메이션 보류, PZ 변환과 가구 실제 3D 제작 금지.
- 다음 **TEX07-R004**: 최신 STATE SHA·버전·R004 출력 충돌 확인 후 공식 전체 JAR 및 실제 인게임 정적 증거가 확보될 때만 해당 검증을 진척시킬 것.

---

## 이전 R002/R001/R000 인수인계 기록 (아래는 역사적 상태)

# 1-1-07 콘크리트·색면 — 최신 인수인계

## 최신: TEX07-R002 (2026-11-13)

- 범위는 그대로 7색 콘크리트만. R001의 비공식 미러 PNG 7개를 **R002에서 같은 바이트로 다시 SHA256/CRC/Pillow 디코딩 재검사 7/7**. R001과 R002를 합쳐 14개 고유 경로로 세지 말 것.
- R002 신규 계측: **38개 RGB 팔레트 빈도 기록, 7개 반복 경계·중앙/외곽 기록, 21개 CIEDE2000 색차쌍**. [R002 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R002/REPORT.md) / [기계 판독 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R002/SUMMARY.json).
- 공식 Mojang 1.21.11 `client.jar` 전체 인증 및 내부 7 PNG 대조 **0/7**, 실제 인게임 정적 장면 **0/7**. 공식 엔드포인트는 알지만 다운로드 차단. 제3자 목록의 클라이언트 JAR SHA1은 실제 공식 JAR 대조 결과로 인정 금지.
- R001에서 검증한 42개 정적 면의 UV 영역은 **JSON 숫자 명시가 아니라 풀 큐브에서 파생**. R002 새로운 면 모델 수 0. 상위 체크포인트 **v38 불변**. 애니메이션 전면 보류.
- **다음 TEX07-R003**, 작업 전 GitHub 단계 `STATE.json` SHA와 버전을 재조회하고 신규 R003 디렉터리 부재를 검사. 다른 단계 문서/루트 문서 쓰지 말 것.

---

## 과거 인수인계 보존 (이하는 R001/R000 시점 기록)

# 1-1-07 콘크리트·색면 — 최신 인수인계

## TEX07-R001 (2026-11-13)

- 이번 독립 분석: 비공식 미러 1.21.11 실제 PNG 바이너리·CRC·SHA·RGBA **7/7**, 정적 상태/모델/아이템 JSON 7+7+7 및 공통 부모 3개, 면 42개 색면 UV 참조. 자세한 [REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R001/REPORT.md), [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R001/SUMMARY.json).
- A/B/C/D/E/G는 미러 소스 범위 분석 기록 완료, F 공식 Mojang client.jar 인증 **0/7**, 인게임 정적 렌더 **0/7**. 전체 A–G 완료라고 주장 금지.
- UV 수치 42면은 **명시 UV 0 / 16×16 풀큐브로부터 파생된 영역 42**; 독립 PNG 위치 1,792개와 42면 참조 합 10,752 texel-uses는 구별한다.
- 다음 단계 고유 버전 **TEX07-R002**. 새 작업 전에 STATE SHA/버전 및 출력 경로 충돌 검사. 전체 v38 불변, 다른 단계 수정 불가. 애니메이션 전면 보류, 좀보이드 변환 및 가구 실모델 제작 범위 제외.

---

## R000 당시 계획 인수인계 (아래 과거 현황 문구는 초기 상태의 역사적 기록)


> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX07-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-07 / 콘크리트·색면 / 7개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-07 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-07_콘크리트색면.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 7/7 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

기존 7색 원본 표본 범위만 비교; 나머지 전체 콘크리트 색 포함으로 부풀리지 말 것.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-07-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-07-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-07-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-07-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-07-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-07-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-07-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 7색 콘크리트의 평균 RGB·명도·채도
- **D2:** 미세 픽셀 분산과 단색 평면 경계 검사
- **D3:** 가구 평면의 색상 사용 가설을 원본 관찰과 분리

## 검토할 정확한 텍스처 7개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-07-001` | `white_concrete` | `cf3300b0ebbdf5859a7ce14ca004d4529a3cd2e0de1c830acf00fb3dec8baea4` | `assets/minecraft/textures/block/white_concrete.png` |
| `1-1-07-002` | `black_concrete` | `0d2f1cf4f6b7f1abada383bb2dbeb4bf274628a65793b2d388805dd8a5c1b0cb` | `assets/minecraft/textures/block/black_concrete.png` |
| `1-1-07-003` | `red_concrete` | `4069c61ef07e5c113c2e0850b009d8c814c21881525535a01dffea7d52fd1896` | `assets/minecraft/textures/block/red_concrete.png` |
| `1-1-07-004` | `blue_concrete` | `54eea9be4c801ed6206fdb79fab7711185e5dcda5ccf5251871013ce14d1da33` | `assets/minecraft/textures/block/blue_concrete.png` |
| `1-1-07-005` | `green_concrete` | `42bf8de7fd911c4f649f03eb428e35bd303a571f012046b929bea9070ab37f34` | `assets/minecraft/textures/block/green_concrete.png` |
| `1-1-07-006` | `yellow_concrete` | `c66ed9653baf4abb311cd41a2acc444fe7139355259e12aed79a511723c69367` | `assets/minecraft/textures/block/yellow_concrete.png` |
| `1-1-07-007` | `gray_concrete` | `a760d9bc6255fc2c1bcbe481b57a8a242687eda6c64459812398d7c40c9769bc` | `assets/minecraft/textures/block/gray_concrete.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX07-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX07-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-07/TEX07-R001/`. 다음은 이 단계만 `TEX07-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
