# 1-1-02 — 석재·벽돌 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 현재 고유 버전 **`TEX02-R005` (공식 인증 제외·정책 변경)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-02 / 석재·벽돌 / 17개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-02 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-02_석재벽돌.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-02/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 17/17 항목의 측정 기록 존재**; TEX02-R001에서 비공식 미러 A–E 소스 검수와 G 저장을 수행했다. F 공식/인게임 검증은 대기 상태이다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

v4 측정 데이터가 기본. 이전 v5~v38의 관련 모델 연구는 먼저 검색하고 기존 결론을 신규 실측으로 오인하지 말 것.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-02-A | A 기존 출처·파일·중복 대조 | TEX02-R001 미러 PNG/모델 직접 검수 / 공식 검증 대기 |
| 1-1-02-B | B PNG 실제 바이너리·SHA·CRC 검증 | TEX02-R001 미러 PNG/모델 직접 검수 / 공식 검증 대기 |
| 1-1-02-C | C RGBA·밝기·알파·반복 정량 검사 | TEX02-R001 미러 PNG/모델 직접 검수 / 공식 검증 대기 |
| 1-1-02-D | D 재질 특화 세부 검사 | TEX02-R001 미러 PNG/모델 직접 검수 / 공식 검증 대기 |
| 1-1-02-E | E 정적 모델 JSON·UV·상태 연결 | TEX02-R001 미러 PNG/모델 직접 검수 / 공식 검증 대기 |
| 1-1-02-F | F 인게임 정적 렌더·UV·이음새 검증 | **공식 JAR 인증은 범위·완료 조건에서 제외**, 인게임 검증 0/17 대기 |
| 1-1-02-G | G 근거 보고서·단계 인수인계 저장 | TEX02-R001 미러 PNG/모델 직접 검수 / 공식 검증 대기 |

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

- 현재 **`TEX02-R005`**: R001~R004 실측 기록 보전, **공식 Mojang client.jar SHA-1 및 버전 매니페스트 인증은 연구 범위와 완료 조건에서 제외**. 인게임 정적 검증은 여전히 0/17.
- 최신 단계 개정: **`TEX02-R005`** (정책 변경만); 저장 경로 `research/vanilla_textures/by_stage/1-1-02/TEX02-R005/`. 다음은 이 단계만 **`TEX02-R006`**.
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

## 최신 실측 결과 — TEX02-R001 (2026-11-13)

- 결과: [정적 검증 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R001/REPORT.md) · [17종 파일별 SOURCE_LEDGER](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R001/SOURCE_LEDGER.csv) · [MODEL_UV_LEDGER](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R001/MODEL_UV_LEDGER.csv) · [D2 행별 에지 피크](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R001/D2_ROW_PEAKS.csv) · [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R001/SUMMARY.json).
- 미러 PNG SHA-256/청크 CRC/디코드 **17/17**, RGBA 불투명 **4,352/4,352 픽셀**; v4 SHA와 17/17 일치. 모델 및 blockstates JSON 17/17 확인; 15 cube_all / 2 cube_column. 실제 인게임 동작은 인증하지 않음.
- **F 공식 Mojang client.jar 인증 0/17, 인게임 정적 장면 0/17**. 전체 A–G 완료 0/17 유지. 비공식 미러 증거 수준을 공식으로 올리지 말 것.
- 후속: **TEX02-R002** (STATE와 HEAD/SHA 다시 읽기 필수). 공식 JAR 확보 → 끝면 텍스처 연결 예외 검토(17개 분모 유지) → 정적 장면 UV/접합 검증. 애니메이션 계속 보류.

## TEX02-R002 후속 — 2026-11-13

- [상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R002/REPORT.md) · [보조 끝면 PNG 측정](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R002/END_FACE_SUPPLEMENT.csv) · [정적 102면 텍스처 슬롯](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R002/FACE_SOURCE_LEDGER.csv) · [31개 blockstate 변형](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R002/BLOCKSTATE_VARIANTS.csv) · [기계 판독 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R002/SUMMARY.json) · [공식 JAR 오프라인 검사기](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R002/VERIFY_OFFICIAL_JAR.py).
- **이번 신규 바이너리 검증은 2개 보조 끝면 PNG**: `deepslate_top`, `blackstone_top`. 둘 다 PNG CRC·16×16·불투명 256픽셀 확인, 측면과 37/256 픽셀만 RGBA 일치. 고정 대상은 **계속 17개**. 이전 R001의 17 PNG 측정을 신규 17개로 중복 기록하지 말 것.
- **공식 `client.jar` 취득 실패**: 공식 JAR SHA 인증 0/17, 인게임 정적 렌더 0/17. 새 검사기 자체는 인증 증거가 아님. `TEX02-R003`에서는 실제 Mojang 공식 파일 수급·JAR 해시 검증 및 정적 인게임 장면 검사를 우선 수행할 것. 전역 `v38` 변경 없음, 애니메이션 계속 보류.

## TEX02-R003 원본 출처 정정 및 검증 (2026-11-13)

- **1차 분석 원본:** [사용자 제공 직접 JAR 압축 해제 `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/2a43897b8f605b4e0c96a272bca476ee6b70058e/1.21.11), pinned commit `2a43897b8f605b4e0c96a272bca476ee6b70058e`. **2차 증거:** 기존 GitHub 비공식 미러. 사용자 설명에 따른 추출 출처이므로 Mojang 원본 JAR 인증을 뜻하지 않음.
- [R003 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R003/REPORT.md) · [17종 SHA/CRC CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R003/SOURCE_LEDGER.csv) · [42 JSON 교차검증 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R003/MODEL_JSON_CROSSCHECK.csv) · [끝면 2 PNG](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R003/SUPPLEMENTAL_END_FACE_LEDGER.csv) · [4수준 검증 SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R003/SUMMARY.json).
- 사용자 추출본 PNG SHA256/CRC **17/17**, 모델 JSON **17/17**, blockstate **17/17**, 공유/미러 JSON **8/8**, 보조 끝면 PNG **2/2** 모두 기존 미러와 정확히 일치. R001 4,352 RGBA 픽셀·R002 102 모델 면과 31 blockstate 변형 기록은 **새 계측이 아닌 바이트 일치로 계승**, 중복 성과 계산 금지.
- 4수준 독립 검증: 사용자 추출본 인증 **예**, 비공식 미러 교차 검증 **예**, Mojang 공식 압축 JAR SHA-1 인증 **아니오 (0/17)**, 인게임 정적 장면 **아니오 (0/17)**.
- 다음 단계 고유 번호 **TEX02-R004**. 작성 직전 GitHub STATE 및 HEAD를 재검증할 것. `v38` 및 다른 단계·R001/R002 불변, 애니메이션 연구 보류.

## TEX02-R004 정적 UV·회전 변형 추가 분석 (2026-11-13)

- [보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R004/REPORT.md) · [186면 매핑](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R004/EXPANDED_VARIANT_FACES.csv) · [31 변형·중복 체크](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R004/VARIANT_DUPLICATES.csv) · [수치/4수준 검증 SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R004/SUMMARY.json).
- R003 사용자 제공 `1.21.11/`를 우선 소스로 R002 면별 JSON 연결을 재검토. **31상태×6면=186**, 구조상 고유 29/31, deepslate axis=x의 index 0=2·1=3 동일 중복 2개. `#all` 108면, `#side` 52면, `#end` 26면, explicit mirror UV 48면, 기본 UV 138면. R001 4,352 RGBA 픽셀 및 R002 102 기본면 재계측 없음.
- 월드 면 방향 표는 수학적 추론이지 엔진/인게임 확인 아님. 공식 Mojang JAR+메타데이터 SHA-1 및 인게임 정적 인증 **각 0/17**. 다음 **TEX02-R005**, 애니메이션 보류. 전역 v38 및 다른 재질 단계·기존 릴리스 무변경.

## TEX02-R005 공식 인증 제외 정책 (2026-11-13)

- [정책 변경 전문](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R005/POLICY_CHANGE.md) · [기계 판독 설정](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R005/SUMMARY.json).
- **Mojang 원본 `client.jar` SHA-1/공식 버전 JSON 인증을 연구 및 완료 조건에서 제외**. 다음 버전에서 해당 인증을 요구하거나 공식 인증 0건 때문에 완료를 차단하지 않는다. 공식 인증의 기존 0건 기록은 **과거 사실**로만 보존한다.
- 계속 유지: 사용자 업로드 `1.21.11/` 직접 PNG·JSON 분석, 필요한 미러 교차 검증, 정적 모델·UV·블록 상태·색상·줄눈 분석, 실제 인게임 정적 검증(0/17 보류), G 보고서. 애니메이션은 보류.
- 이 버전은 **정책 개정만**, 새 측정·연구 진도 0건. R001–R004 및 다른 단계·전체 v38 불변. **다음 TEX02-R006**.

## TEX02-R006 사용자 추출 PNG·정적 UV 경계 픽셀 분석 (2026-11-13)

- [R006 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R006/REPORT.md) · [192행 가상 2D 경계 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R006/HYPOTHETICAL_UV_SEAMS.csv) · [6 PNG SHA/CRC](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R006/SOURCE_PNG_CHECKS.csv) · [18 JSON 파일](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R006/JSON_SOURCE_LEDGER.csv) · [재현 스크립트](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R006/REPRODUCE_SEAMS.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R006/SUMMARY.json).
- **신규 계산:** 사용자 추출 `1.21.11/`의 기존 고정 PNG 5개 + 기존 보조 끝면 1개를 재열람하여 SHA-256/청크 CRC/16×16/불투명 RGBA 총 1,536픽셀 확인. 5개 blockstate + 13개 모델/부모 JSON 직접 확인. 6 × (4 화면상 변환 × 4 변환 × 2 인접 방향) = **192개 픽셀 경계 비교**, 3,072개의 경계 픽셀 쌍(9,216 RGB 채널 차이) 계산. *서로 다른 고유 PNG 신규 추가 0개.* 이전 R001~R004 실적 17 PNG/4,352 RGBA/31 상태/186면/중복 2건은 계승만.
- **핵심 판정:** `bricks`/`stone_bricks`/`deepslate_bricks`는 blockstate에 회전 선언이 없음. `deepslate`의 축 회전과 `cube_mirrored`의 U 반전 UV `[16,0,0,16]`은 소스 사실이나, R006의 2D 화면 회전 숫자는 실제 모델/엔진 방향으로 옮겨 인증할 수 없음. 좌우 반전 상대 타일과의 경계 0은 동일 열을 붙인 계산상 항등성이고 **게임에서 접합이 완벽하다는 증거가 아님**.
- **인게임 정적 0/17 및 A–G 전체 완료 0/17** 유지. 공식 Mojang JAR 전체 SHA-1/버전 메타데이터 인증은 연구/완료 조건에서 제외, 성공 주장 아님. 애니메이션 보류; 다른 단계·전역 v38 변경 없음.
- 이 단계의 다음 후보는 **`TEX02-R007`**. 먼저 최신 LIVE STATE를 다시 읽고, 실제 정적 게임 화면/실측이 없는 한 화면 공간 UV·조명·줄눈을 검증 완료라고 하지 말 것.
