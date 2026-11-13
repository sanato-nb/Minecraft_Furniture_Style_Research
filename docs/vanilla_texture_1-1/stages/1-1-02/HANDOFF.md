# 1-1-02 — 석재·벽돌 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 현재 고유 버전 **`TEX02-R013` (블록상태 가중치·정점 콜백 호출 코드 검증)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

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

## TEX02-R007 — 17개 블록상태 × 186면의 정적 UV 좌표 투영과 신규 134개 픽셀 접합 (2026-11-13)

- [상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R007/REPORT.md) · [186면 UV 4꼭짓점 계산](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R007/FACE_UV_WORLD_CORNERS.csv) · [북쪽 면 정적 소스 투영의 134개 이음새 측정](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R007/SOURCE_PROJECTED_NORTH_FACE_SEAMS.csv) · [43 JSON Git blob SHA 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R007/SOURCE_JSON_SHA_LEDGER.csv) · [6 PNG 재확인](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R007/SOURCE_PNG_RECHECK.csv) · [재현 Python 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R007/REPRODUCE_STATIC_UV.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R007/SUMMARY.json).
- 이번에 직접 다시 확인한 JSON 경로: **17 blockstate + 17 기본 모델 + 2 대체 미러 모델 + 7 공유 부모 = 43개**. R004의 31개 원문 variant/186면은 계승; 이번에는 그 동일한 186면에 대한 **UV 방향 행렬과 네 꼭짓점 좌표 744쌍**을 신규 산출했다. 수학적 가정 하에서 서로 다른 UV 방향은 **8개**. 추가로 기존 PNG 6장을 재열람해 **134개의 투영 북쪽 면 가상 인접 픽셀 비교**, 경계 픽셀 쌍 2,144/채널 차이 6,432 계산. 새 고정 PNG **0개**, 고정 분모 **17개 불변**.
- 중요한 구별: 모델 JSON에서 `uv=[16,0,0,16]`과 회전각 X/Y가 선언된 것은 실제 원문이지만 **미기재 UV 자동 생성 축과 world 접평면 좌표 및 X→Y 회전 부호는 R007 연구의 명시적인 수학 가정**이다. R007의 면 배치/0 픽셀 접합을 실제 게임의 렌더 인증으로 오인 금지. 특히 deepslate axis=x 동일 선언 2개는 과거 R004 근거 계승이고 이번 발견 아님.
- 공식 client.jar SHA-1 인증은 완료 분모에서 제외(인증 성공 아님). **인게임 정적 실측 0/17, A–G 전체 완료 0/17**, 애니메이션 보류, 전역 v38과 타 단계 변경 없음.
- 다음 후보 **`TEX02-R008`**; 시작은 라이브 STATE + 현재 릴리스 재조회, 이후 게임 캡처·렌더러 증거 확보 시 UV 축 가정과 픽셀 접합 비교.

## TEX02-R008 — 사용자 제공 1.21.11 클라이언트 바이트코드의 기본 UV 생성 규칙 직접 검증 (2026-11-13)

- [보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R008/REPORT.md) · [3개 원본 클래스 blob 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R008/CLIENT_CLASS_LEDGER.csv) · [6방향 기본 UV 공식](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R008/DEFAULT_UV_BYTECODE_CASES.csv) · [R007 수학적 축 가정과 실제 바이트코드 교차검증](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R008/R007_AUTO_UV_BASIS_RECONCILIATION.csv) · [오프라인 바이트코드 재현검사](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R008/VERIFY_DEFAULT_UV_BYTECODE.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R008/SUMMARY.json).
- **이번에 새로 검증한 소스 3개:** 사용자 제공 `1.21.11/hqi.class` (렌더러 `FaceBakery`), `hqi$1.class` (6방향 enum switch), `iz.class` (방향 enum 초기화). `defaultFaceUV`의 6개 case별 실제 `[u1,v1,u2,v2]` 인자를 bytecode에서 추출, `bakeQuad`의 UV 필드 null 시 기본 UV 호출 조건 확인.
- **중요한 신규 결론:** R007의 '자동 생성 UV 기본 축은 수학적 가정' 중 **모델 로컬 6면의 U/V 기본 축 6/6은 클라이언트 원본 바이트코드가 확인해 줌**. 16×16 완전 큐브의 기본 UV는 6면 모두 [0,0,16,16]. 이전의 명시 UV 미러 48면은 이 자동 계산의 직접 대상이 아니며, 이전 기본 UV 138면 분류를 계승한다. R007 월드 좌표로 회전된 최종 UV 및 134개 접합은 여전히 **엔진 최종 투영/인게임 검증 전**.
- **신규 PNG/픽셀 재측정 0건, 기존 31 variant/186면/138 기본 UV/48 명시 반전 UV 등 모두 이전 실적 계승**. 게임 정적 렌더 0/17, A–G 전체 완료 0/17, 공식 Mojang client.jar SHA-1 인증은 연구 필수 기준에서 제외. 애니메이션 계속 보류.
- 다음 후보 **`TEX02-R009`**. 진행 가능하다면 사용자 추출 클라이언트의 `ModelState` 변환/UV 잠금과 실제 baked quad 코드를 추가 분석하고, 스크린샷 검증은 자료가 있을 때만 수행.

## TEX02-R009 — 사용자 제공 클라이언트의 bakeQuad UV 경로·코너 규칙·31 uvlock 선언 (2026-11-13)

- [R009 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R009/REPORT.md) · [클라이언트 클래스 12개 blob SHA 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R009/CLIENT_QUAD_CLASS_SHA.csv) · [바이트코드 21개 호출 지점](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R009/QUAD_PIPELINE_BYTECODE_CALLS.csv) · [UV 코너 공식을 실행한 32개 예시](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R009/UV_CORNER_FORMULA_EVALUATION.csv) · [31개 블록상태의 uvlock 키 검사](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R009/BLOCKSTATE_UVLOCK_DECLARATIONS.csv) · [오프라인 검사 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R009/VERIFY_QUAD_UV_PIPELINE.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R009/SUMMARY.json).
- R008에서 사용한 `hqi.class`는 계승/재검사. 이번에 **새로 직접 읽은 원본 자바 클래스 파일 11개**: `hqc, hqc$b, g, ioc, i, e, ilp, hqd, hoa, hoa$a, hoa$b`. 사용자 제공 `1.21.11/` 우선, Git blob SHA 저장.
- **신규 소스 확인:** `bakeQuad`의 UV 기본값 보충 → `ioc.b(direction)` UV 행렬 → `ioc.a()` 위치 변환 → 정점 네 개 반복 → UV 원점 보정(-0.5), UV행렬 `transformPosition`, 중심 복귀(+0.5) 조건부 경로 → sprite 텍스처 좌표 변환/quad 생성. `g.b(index)`는 rotation offset 합산 mod 4, `hqc$b`는 `(u1,v1),(u1,v2),(u2,v2),(u2,v1)`의 코너 선택 규칙. 그 공식을 기본/명시적 미러 UV 2종 × 회전 인덱스 4 × 꼭짓점 4로 **새 알고리즘 평가 32행** 생성.
- 17개 원본 blockstate JSON 전부 재열람. R004의 **기존 31개 변형 선언 중 `uvlock` 명시 0건**. 그러나 이는 선택되는 실제 ModelState 행렬/인게임 최종 UV까지 검증했다는 뜻은 아님. `ioc` 기본 구현은 공용 identity matrix 사용.
- **신규 픽셀/PNG 0건, 원본 고정 17, 이전 31 variant/186 face와 R007 134 픽셀 접합은 계승**, 다른 연구 실적 중복 가산 금지. 공식 jar SHA-1 인증 완료 기준 제외. **인게임 0/17, A-G 완료 0/17**, 애니메이션 제외.
- 다음 후보 `TEX02-R010`: 최신 STATE 재조회 후 `ioc` 구현체 선택과 ModelState 회전 파서의 실제 조건을 추가 확인할 수 있음. 당장은 사용자 협조 없이 소스 연구 가능.

## TEX02-R010 — 원본 Java 클라이언트의 uvlock 기본값 → ModelState → UV 행렬 경로 검증 (2026-11-13)

- [상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R010/REPORT.md) · [31개 상태별 effective uvlock/모델 상태/행렬 경로](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R010/EFFECTIVE_UVLOCK_31_VARIANTS.csv) · [클래스 바이트코드 15개 연결 근거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R010/UVLOCK_CLASS_BYTECODE_CHAIN.csv) · [6개 클래스 Git SHA 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R010/CLASS_SOURCE_SHA_LEDGER.csv) · [로컬 재현 Python 스크립트](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R010/REPRODUCE_UVLOCK_PATH.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R010/SUMMARY.json).
- 사용자 제공 `1.21.11/` 원본에서 **새 클라이언트 클래스 4개**(`hqq$a.class`, `hqq.class`, `inm.class`, `inm$a.class`)를 직접 읽고, 기존 `ioc.class`/ `hqi.class` 코드를 결합했다. **JSON 17개 원본 재열람 + 기존 31 선언에 코드 경로 연결 31행**, 새 JSON 선언이나 새 PNG 발견 0개.
- **R009의 미확정 해결:** `hqq$a` MapCodec은 `uvlock` 옵션 기본값을 `false`로 둔다. `false`는 일반 회전 ModelState `inm`, `true`만 `inm$a` UV 잠금 래퍼를 선택. `inm`는 방향별 UV 메서드를 재정의하지 않아 `ioc.b(Direction)`의 **공용 항등행렬**을 사용한다. 따라서 원본 31개 전부 **`uvlock=false` / 일반 `inm` / UV 잠금 보정용 항등행렬**이라는 *코드상 추론*이 가능하다. 그러나 정점 모델 회전은 그대로 수행하며 실제 월드 면 UV와 영상은 미검증.
- 31 상태의 `(x,y,z)` 튜플 5종: (0,0,0) 19개, (0,180,0) 4개, (90,90,0) 4개, (90,0,0) 2개, (90,180,0) 2개. 새 쿼드/실제 픽셀 측정/인게임 스크린샷 **0건**. 과거 31 상태·186면·R007 134 이음새 수량 누적 금지.
- **인게임 정적 검증 0/17, A–G 전체 완료 0/17**. 공식 JAR SHA-1 인증은 연구 기준 제외, 성공 주장 없음. 애니메이션 보류, 전역 v38과 타 단계 변경 없음.
- 다음 후보 **`TEX02-R011`**: 라이브 STATE/HEAD 재확인 후 사용자 추출 `f.class`의 실제 XYZ 90도 회전 및 `hqi` 정점 재배열까지 추적하여 모델 월드면의 UV 정확성 추가 검증. 현재 사용자 도움 없이 원본 소스 검사는 추가 가능.

## TEX02-R011 — f/h/g 원본 회전 그룹에 따른 R007 32면 방향 정정 (2026-11-13)

- [보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/REPORT.md) · [원본 회전 행렬 5종](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/ROTATION_GROUP_MATRICES_5.csv) · [R007 기존 186면 전수 감사](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/WORLD_FACE_AUDIT_186.csv) · [교정이 필요한 32면](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/R007_WORLD_FACE_CORRECTIONS_32.csv) · [이음새 재평가 대상 64행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/R007_NORTH_SEAM_REEVALUATION_64.csv) · [원본 Git SHA 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/SOURCE_LEDGER.csv) · [오프라인 재현 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/REPRODUCE_R011_ROTATION_AUDIT.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R011/SUMMARY.json).
- 사용자 추출 `1.21.11/`에서 **새 `.class` 2개** `f.class`(48개 signed-permutation 상수)·`h.class`(6개 축 순열)를 직접 조사. R009 `g.class`·R010 `inm.class` 재사용. `g`의 정수 90도는 소스의 `ROT_90_X_NEG` 같은 **음의 회전 부호 그룹**으로 매핑한다는 사실을 확인.
- R010에서 계승한 기존 31상태의 5개 XYZ 회전 조합을 소스 행렬로 유도. **이전 R007 186면 월드 방향 중 154건 일치, 32건 불일치**. 전부 `deepslate axis=x` 16면 + `axis=z` 16면이며, R011 교정 CSV로 별도 보존. **기존 R007 무수정**, 파생 연구의 오류만 새 버전에서 표시.
- R007의 가상 2D 이음새 134행 중 `deepslate axis=x` 32 + `axis=z` 32 = **64행은 수정 행렬로 다시 투영할 필요**. **64개 밝기 수치가 전부 틀렸다는 뜻은 아니며, 실측 인게임 자료는 전혀 아니다**. 나머지 70행도 소스 수치 유지만 할 뿐 게임 검증 완료가 아님.
- 신규 PNG/픽셀 측정 0건, 기존 원본 17 PNG/31 선언/186면/134 가상 seam 실적 계승. **실제 인게임 0/17, A–G 전체 완료 0/17**. 공식 JAR 전체 SHA-1 인증은 필수 연구 조건 제외. 애니메이션 및 3D 가구 제작/좀보이드 변환 제외.
- 다음 후보 `TEX02-R012`: 라이브 HEAD/STATE 확인 후 수정된 행렬과 `hoa/hqi` bake 정점·UV 처리로 **실제 코너 수치와 영향받는 64개 2D seam 가설 재계산**. 원본 코드로 연구 가능한 부분이 남아 있어 현재 사용자 협조 없이 이어갈 수 있음.

## TEX02-R012 — FaceBakery 정점+UV 재정렬·R007 40개 UV 교정·64개 합성 이음새 재측정 (2026-11-13)

- [R012 상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/REPORT.md) · [원본 HOA 6방향×4 꼭짓점](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/HOA_FACE_CORNERS_24.csv) · [전체 186면의 새로운 UV 감사표](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/REBAKED_UV_AUDIT_186.csv) · [R007 UV 코너 교정 40면](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/R007_UV_CORNER_CORRECTIONS_40.csv) · [소스 PNG 기반 north face 8형태](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/NORTH_FACE_SOURCE_UV_8.csv) · [R007 기존 가상 이음새 64건의 직접 재측정](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/R007_NORTH_SEAMS_RECALCULATED_64.csv) · [재현용 Python](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/REPRODUCE_R012_QUAD_UV_SEAMS.py) · [소스 Git SHA 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/SOURCE_LEDGER.csv) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R012/SUMMARY.json).
- **새 최초 발굴 클래스 0개**; 이전에 이미 열람한 `hoa`, `hoa$a`, `hqi`, `hqc$b` 등의 내용을 *더 깊게 재분석*. `hoa` 원본 클래스 `<clinit>`의 6면×4코너 표와 `FaceBakery`의 **정점·UV 배열 쌍방 swap**를 대조하고 R011 회전행렬에 적용. 고정 원본 모델 31상태/186면의 UV projection을 재작성: **146 UV 코너 패턴 일치, 40개 R007 코너 패턴 불일치(모두 deepslate axis=x 24 / axis=z 16)**. 세계 방향은 R011 때 32개 교정된 상태 그대로, 이 32개는 40개 UV mismatch 안에 포함. 세계 방향 일치 + UV mismatch 추가 8면.
- **실제 원본 PNG 두 파일**(`deepslate.png` Git blob `bb7dc9...`; `deepslate_top.png` `a560cc...`)을 다시 가져와 SHA 대조하고 16×16 palette RGB **2×256=512 pixels 직접 디코딩**. corrected north-facing `deepslate axis=x` 4 variant, `axis=z` 4 variant 합계 **8개 2D 가상 면 투영** 후 R011 재평가 대기 64건의 가상 경계 RGB 집계 다시 측정(**1,024 픽셀 쌍**). 놀랍게도 R007 집계값 RGB 합/평균/불일치 픽셀 수와 **64/64 동일**, 집계가 달라진 행 0건. 이는 게임 화면 검증도 아니고 이전 픽셀별 차이맵 동일성 증명도 아님. `deepslate axis=x/z` 가상 seam 집계 재계산 대기는 해소되지만 실제 게임 비교 필요.
- 기존 17 PNG, 31 variants, 186 face, R007 134 synthetic seam은 고정 분모·계승 실적. 이번에 새 고유 PNG / 새 독립적 이음새 쌍 **0개**, 재계산한 64건만 별도 성과. **인게임 F 0/17, A–G 전체 0/17**, 공식 JAR 인증 필수 조건 제외, 애니메이션·가구 모델링 보류, 전역 v38과 이전 R001–R011 불변.
- 다음 후보 `TEX02-R013`: 라이브 상태 재확인 후 `inw$a` 정점 변형/ `hqm` bake dispatch 또는 랜덤 variant 선택 코드를 클라이언트 소스에서 추가 검증할 수 있음. 독립 증거 없거나 실제 게임 캡처가 필요하면 숫자만 올리지 말고 중단하여 사용자의 도움을 요청할 것.

## TEX02-R013 — blockstates 가중치 선택 및 모델 베이크 정점 콜백 소스 연구 (2026-11-13)

- [상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/REPORT.md) · [31 모델 선택 슬롯](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv) · [19 상태별 선택 그룹](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/SELECTOR_GROUPS_19.csv) · [동일 모델 회전 조합 통합 29 결과](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/STRUCTURAL_OUTCOME_ODDS_29.csv) · [모델 선택/정점 호출 소스 근거 19행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/BYTECODE_DISPATCH_CHAIN_19.csv) · [22개 원본 클래스 SHA/중복 여부](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/CLASS_SOURCE_SHA_LEDGER.csv) · [표준 Python 재현 검증기](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/VERIFY_R013_SELECTION.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-02/TEX02-R013/SUMMARY.json).
- **처음 직접 분석한 관련 클래스 18개**: `hqh$b`의 **`weight` 기본값 1**, `ioj/ioj$a` 가중치 모델 위임, `cbn`의 `bgr.a(total_weight)` 정수 슬롯 draw, `cbn$c`의 가중치만큼 배열 반복 저장 등을 소스 opcode로 직접 확인. 17 JSON 원문 재열람: **weight 키 0/31**, state 선택 그룹 **19개**(4개씩 나열된 목록 4개 + 단일 객체 15개), 전체 슬롯 **31개**, 구조적으로 동일한 2개 중복을 통합한 **29개 고유 조합**. `deepslate axis=x`에서 normal indices 0+2, mirrored indices 1+3, 균등 bounded RNG 가정하 각 2/4=50%이며 실제 월드 빈도 검증이 아님.
- `hqn.class` 395바이트 bake 루프의 **PC 302–337**에서 `inw.c()`가 반환한 `inw$a` 정점 변환을 `hqi` FaceBakery에 전달하는 연결을 최초 직접 확인. `hqm`은 geometry bake 후 atlas 적합성을 검사하며 실패 시 fallback 사용. **정점 콜백의 실제 구현체/항등 여부, atlas 통과, world RNG/seed 및 게임 GPU 결과는 여전히 미확인.** 기존 R012 UV 186면을 런타임 검증으로 승격하지 말 것.
- 신규 PNG/픽셀 측정 0; 과거 17 PNG/31 variant/186면/134 가상 seam/R011 방향32/R012 UV40·seam64 수량은 그대로 계승. **F 인게임 정적 검증 0/17, 전체 A–G 완료 0/17**. 공식 JAR SHA1 인증 필수 조건 제외, 애니메이션 및 가구 3D 모델링·좀보이드 변환은 현재 연구 범위 제외. 전역 v38, 다른 단계, 기존 R001–R012 파일 변경 금지.
- 다음 `TEX02-R014` 후보: 라이브 HEAD/STATE 확인 후 `inw.c()`의 구체 변환 반환 경로를 원본 소스에서 찾아 R012의 정점/UV 가정을 검증. 원본 연구가 끝나거나 실제 게임 캡처/엔진 자료가 반드시 필요한 경우, 새 버전을 임의로 만들지 말고 멈춰서 사용자에게 필요한 자료를 구체적으로 요청.
