# 학습 진행도

> **현재 기준 v42(2026-11-14):** [1-1 지정 11분류·150종 소스 연구 완료](docs/vanilla_texture_1-1/CURRENT_STATUS.md) · [원본 Git tree·연구 근거 독립 재검수](research/vanilla_textures/audits/2026-11-14_v42_scope_verification/REPORT.md). 상위 세부과제 **1/5 완료**. 아래 v38~v41 문장/수치는 **당시 스냅샷**이며 현행 업무 지시가 아님.

## 최신 전역 v42 — 목재 완료 판정 오류 정정 · 1-1 소스 연구 150/150 완료

> **2026-11-14, 통합 `INT-1-1-20261114-02`**. 이 문단은 아래 v41/v40/v39의 역사적 누적 연구 기록보다 최신이며 현재 진행도에서는 이 값을 우선한다.

- **[v42 검수 보고서](research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/REPORT.md)** · [11개 단계 완료 원장](research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/STAGE_INTEGRATION_LEDGER.csv) · [150개 텍스처별 완료 원장](research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/TEXTURE_150_SCOPE_LEDGER.csv) · [Git SHA 증거](research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/MANIFEST.json) · [검증 JSON](research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/VALIDATION.json).
- **목재·원목 1-1-01 고정 18종은 v39부터 이미 원장에 포함**되어 있었다. 그 단계 `STATE.json`의 `stage_current_analysis_completed_count=0`은 이전 R001–R008 소스 연구 결과를 반영하지 않은 **완료 집계 누락**이었고, 근거 감사 및 사용자 정정 요청을 반영해 **18/18**로 갱신. 새 TEX 연구 버전/PNG 실측은 추가하지 않고 `TEX01-R008` 보존.
- **1-1 바닐라 재질·텍스처 지정 11개 분류 / 150개 texture_id = 사용자 승인 원본 소스 연구 범위 완료 100%**. 원장 등록 150/150과 단계별 승인 소스 검증 완료 150/150이 둘 다 충족됨. **모든 Minecraft 블록 PNG 1111종 완료라고 주장하는 것이 아님**.
- 범위에 맞춰 **상위 연구 5개 세부과제 중 첫 번째 '01 바닐라 재질·텍스처 분석'을 완료로 기록**, 다른 02–05는 계속 개별 검수 필요. **상위 1단계 1/5**이며 상위 2단계 디자인 가이드 완성을 의미하지 않는다.
- 공식 Mojang 압축 JAR SHA 검증 및 실제 인게임 정적 렌더 검증은 사용자 요청으로 완료 요건에서 제외(직접 성공했다는 뜻 아님). 애니메이션 소스 재개 9단계, 단계 02·10 별도 보류. 가구 모드 및 실제 가구 모델 제작·PZ 변환은 이번 소스 완료 판정 범위 밖.
- v39(133종 부분통합), v40(150종 최초 통합), v41(석재 R017 갱신) 연구 스냅샷은 **원본 그대로 보존**. 원래 v4·TEX 모든 리비전에도 신규 측정 실적을 중복 집계하지 않았다.


## [과거 v41] 석재·벽돌 R017 완료 반영, 11단계·150종 통합 유지

> **2026-11-14 KST · 통합 `INT-1-1-20261114-01`.** 이 문단의 v41 연구 상태/작업 범위가 아래의 v40/v39/v38 역사적 기록보다 우선한다. 기존 보고서와 독립 단계 파일은 삭제·수정하지 않았다.

- **[v41 통합 보고서](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/REPORT.md) · [11단계 원장](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/STAGE_INTEGRATION_LEDGER.csv) · [150종 텍스처 원장](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/TEXTURE_150_SCOPE_LEDGER.csv) · [SHA 매니페스트](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/MANIFEST.json) · [검증 결과](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/VALIDATION.json)**.
- 통합 범위: **11/11 단계, 150/150개 고정 `texture_id`**, 누락/중복 0개. **소스 연구 완료 10/11단계, 132/150 (88%)**. 서로 다른 지표이며 **마지막 미종결은 `1-1-01` 목재·원목 18개**.
- 석재·벽돌 **`1-1-02`의 전역 기준을 `TEX02-R015 → TEX02-R017`로 갱신**하고 독립 소스 검증 완료 **0/17 → 17/17**을 반영. 19개 모델·7개 부모·31개 블록상태 선택·186개 face→sprite 연결은 R017 근거이며 실제 Minecraft 게임 렌더 인증을 뜻하지 않는다.
- 원래 **v40은 11단계/150종이지만 석재 R015 고정(당시 소스 완료 115/150)**이었으며, v41은 **132/150**을 기준으로 새 통합 원장을 발행했다. v39(10단계 133종)와 v40 모두 **불변 보존**. 새로운 원본 PNG/JSON 분석 측정 0건.
- 상위 1단계의 5개 하위 연구 과제 최종 완료 **0/5 유지**, 실제 가구 모델 제작/좀보이드 맵 변환 포함되지 않음. `1-1-01`의 소스 완료가 확정되기 전까지 **1-1 소스 연구 100%라고 주장하지 말 것**.
- 사용자 추출 `1.21.11/` 게임 파일 최우선. **Mojang 공식 JAR SHA1 인증 및 실제 인게임 렌더 검증은 완료 필수조건에서 제외**(인증/실측한 사실은 없음). 애니메이션 소스 연구 **9개 단계 재개, 1-1-02·1-1-10 보류**. 과거의 전면 애니메이션 보류와 공식 인증 대기 문구는 작성 당시 역사적 기록으로 간주한다.
- 석재 이외 개별 TEX 단계의 버전·Git SHA는 v40과 동일. 이후 신규 TEX 증거가 생기면 전역 v41에 자동으로 편입되지 않으며 별도 v42 통합 필요.



## 과거 연구 기록 — v40 이하

### [과거 v40] 체크포인트 — 1-1 11단계·150개 ID 전역 통합 (2026-11-13)

> **이 섹션이 아래 v39/v38 및 과거 일괄 정책 문서보다 최신입니다.** 통합 ID: `INT-1-1-20261113-02`. **v39는 역사적 10단계·133개 부분 통합으로 보존**하며 파일을 덮어쓰지 않습니다.

- **[v40 상세 보고서](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/REPORT.md)** · [단계 11행](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/STAGE_INTEGRATION_LEDGER.csv) · [150개 텍스처 ID 원장](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/TEXTURE_150_SCOPE_LEDGER.csv) · [SHA 고정 매니페스트](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/MANIFEST.json) · [검증 기록](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/VALIDATION.json).
- **통합 범위 11/11단계, 고유 texture_id 150/150, 제외 0단계/0종, 새 PNG 실측 0개**. 기존 v4 150개 원장과 기초 픽셀 측정은 수정·재계산하지 않았습니다.
- **1-1-02 석재·벽돌 17종이 최초 포함**되었으며, 사용자가 선택한 **통합 참조는 `TEX02-R015`**입니다. 독립 최신 상태는 `TEX02-R017`이지만 R016·R017의 최신 연구 완료를 **R015의 고정 참조에 소급하지 않습니다**. 두 상태 SHA는 매니페스트에 각각 고정.
- **150/150은 통합 ID 커버리지 100%**, 연구 전체 완료율이 아닙니다. 고정 참조의 source-only 완료 **115/150**, LIVE 최신 독립 기준 완료 **132/150**, 목재·원목 18종의 독립 연구 완료 판정은 미종결. 상위 5개 연구 과제 완료 **0/5 유지**.
- 최신 단계 STATE 기준 애니메이션 **소스 연구 재개 9단계 / 보류 2단계 (`1-1-02`, `1-1-10`)**. 공식 Mojang 압축 client.jar SHA-1 인증과 인게임 렌더 검증은 **필수 연구 조건에서 제외**하되, 인증/관찰 성공 주장은 금지(실제 인게임 0). 실제 좀보이드 가구 3D 제작·맵 변환 결과는 여기의 완료율에 포함하지 않습니다.

### 단계별 진행도 (정적 소스 근거의 단계 완료 판정만)

| 지표 | 결과 |
|---|---:|
| **전역 통합 범위** | **11/11단계 · 150/150 ID · 100%** |
| 구 v39와 비교 | 10단계·133 ID → 11단계·150 ID |
| 통합 참조 고정 시점의 소스 완료 | 115/150 (R015 고정) |
| 각 최신 독립 LIVE STATE 소스 완료 | 132/150 (88%) |
| 독립 완료가 남은 목재·원목 | 18종 |
| 신규 PNG 픽셀 실측 | **0건** |
| 인게임 검증 | 제외 / 실제 관찰 0 |
| 공식 압축 JAR 인증 | 제외 / 미인증 |
| 애니메이션 소스 연구 | 9개 재개 · 2개 보류 |
| **상위 대과제** | **0/5 유지** |

### [과거 v39] 통합 — 1-1 바닐라 재질 10개 통합, 석재·벽돌(1-1-02) 제외

> **2026-11-13 KST**, 통합 ID `INT-1-1-20261113-01`. **본 문단은 아래의 v38·v35·R000 초기 작업 지시보다 최신이며 범위/우선순위에서 앞선다.** 기존 역사적 문서는 삭제하지 않음.

- **통합 결과:** [v39 10개 재질/133개 텍스처 통합 보고서](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/REPORT.md) · [포함 10개/제외 1개 단계 원장](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/STAGE_INTEGRATION_LEDGER.csv) · [133개 대상별 출처 원장](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/TEXTURE_133_SCOPE_LEDGER.csv) · [SHA 고정 매니페스트](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/MANIFEST.json).
- **10개 단계(1-1-01, 03–11) / 대상 133개 고정 `texture_id`를 전역 통합**. 제외한 **1-1-02 석재·벽돌 17개(`TEX02-R015` 기준)**는 삭제/폐기가 아니라 미통합. v4의 150개 역사적 표본 전체는 그대로. **133/150은 통합 범위이며 전체 완료율이 아님**, 통합 중 신규 PNG 실측 0.
- 독립 연구 최종 리비전은 각 채팅별 `TEXnn-Rxxx`로 계속 유지하며, 이 **전역 v39**는 고정 시점 연구 결과를 연결한 버전. **상위 1단계 최종 완료 0/5**, 1-1 전체 완성 선언 없음.
- 사용자 제공 `1.21.11/` JAR 추출본 우선, 비공식 미러는 교차용. **공식 압축 JAR SHA-1 인증과 인게임 시각/런타임 검증은 사용자 지시에 따라 필수 완료 조건에서 제외**(실제 인증/관찰 성공을 뜻하지 않음). 게임 원본의 공개 재배포 권리 확인 또한 별개.
- 애니메이션 **소스 연구는 1-1-01,03,04,05,06,07,08,09,11에서 사용자 지시로 재개**. **1-1-10 잎·식생은 최신 독립 STATE 기준 보류**. 아래 이전 문단의 '애니메이션 전면 보류'는 예전 지시 기록으로 읽고 최신 단계별 상태를 우선. 실행/런타임 효과는 별도 증거 없으면 완료 주장 금지.
- Project Zomboid 변환·실제 가구 3D 제작은 범위 밖. 과거 Another Furniture/Handcrafted, 바닐라 모델 연구, 원본 파일 및 v38 데이터는 보존.



**새 채팅 인수인계:** [HANDOFF.md](HANDOFF.md) · [복사용 시작 프롬프트](docs/NEW_CHAT_START.md) · [현재 상태 JSON](handoff/STATE.json)

업데이트: 2026-11-13 / 체크포인트 v39

**사용자 최신 작업 지시(2026-11-13): 애니메이션 분석은 일단 보류.** 새로운 애니메이션 프레임 해독, 키프레임·클립 분석, 움직임 재현 및 애니메이션 인게임 검증을 진행하지 않는다. 기존 v9/v26/v31 애니메이션 관련 기록은 삭제하지 않고 보존하되, 새로운 진행도에 포함하지 않는다. 우선순위는 **정적 바닐라 3D 모델·기하·텍스처·UV·블록 상태·정적 렌더링 검증·공식 원본 무결성**이다. 애니메이션 연구는 사용자가 명시적으로 재개를 요청할 때까지 유지 보류.

## 1-1 11개 개별 채팅 — 독립 시작 프롬프트·인수인계·버전 격리 (2026-11-13)

- **[새 채팅 시작 통합 런처](docs/vanilla_texture_1-1/NEW_CHAT_LAUNCHER.md)** · [TEXnn-Rxxx 고유 버전/동시 수정 방지 규칙](docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md) · [11개 파일별 1-1 상세 계획](docs/vanilla_texture_1-1/README.md).
- 각 `1-1-01`~`1-1-11`에는 GitHub `docs/vanilla_texture_1-1/stages/1-1-nn/` 아래 **START_PROMPT.md + HANDOFF.md + STATE.json** 생성. v4 150개 표본을 **18/17/16/9/6/8/7/21/9/8/31**로 독립 배분.
- **버전 충돌 없음:** `TEX01-R000`~`TEX11-R000` 11개 초기 계획 상태. 새 실제 근거 검증 때 각 단계에서만 `TEXnn-R001`, `R002`로 증가하며, 원래 전체 프로젝트 `v38` 및 다른 단계와 같은 릴리스명·경로를 공유하지 않는다.
- **별도 채팅 쓰기 규칙:** 그 채팅은 자기 단계의 `STATE.json`, `HANDOFF.md`와 `research/vanilla_textures/by_stage/1-1-nn/TEXnn-Rxxx/` 결과 폴더만 수정. 이 루트 인수인계·`PROGRESS.md`·`handoff/STATE.json`·다른 재질 단계를 직접 갱신하면 안 됨. 같은 단계 동시 쓰기는 금지/명시적 조정. 최종 통합 검수는 별도.
- 이번은 **인수인계 인프라 생성**으로 새 PNG/RGBA 원본 분석을 수행한 것이 아니다. 11개 초기 파일의 새 단계 검사완료 0, v4 레거시 실측 보존, 공식 Mojang `client.jar`/인게임 검증 미완료, 애니메이션 보류, 전체 프로젝트 현재 체크포인트 **v38 / 완료 0/5** 유지.

## 1-1 실행 작업번호 확정 — 재질 11분류·150 텍스처 추적표 (2026-11-13)

- [1-1 작업 통합 목록과 A–G 검증 절차](docs/vanilla_texture_1-1/README.md) · [11개 번호별 독립 실행 문서](docs/vanilla_texture_1-1/) · [v4 150개 텍스처 파일별 번호·원본 SHA256 추적 CSV](research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 고정 번호 `1-1-01` 목재·원목18 / `1-1-02` 석재·벽돌17 / `1-1-03` 금속·금속부품16 / `1-1-04` 직물·양털9 / `1-1-05` 유리6 / `1-1-06` 도기·유광도기8 / `1-1-07` 콘크리트·색면7 / `1-1-08` 복합·기능면21 / `1-1-09` 토양·지면9 / `1-1-10` 잎·식생8 / `1-1-11` 목재·구조부품31 = **11개 작업/150개 고유 PNG 경로**.
- 분류별 A 기존 증거, B 원본 무결성, C RGBA·명암 등 실제 화소, D 각 재질 특화 비교, E 정적 모델·UV 결합, F 공식 JAR·인게임 검증, G 완료 근거·파일 갱신. 사용자가 `1-1-04 시작해줘`처럼 번호 지정하면 해당 문서에서 이어갈 것.
- **계획만 수립했으며 신규 PNG·모델을 추가 분석 완료한 것은 아님.** v4의 150/150 표본 측정 및 v38 기존 증거는 유지하고, A–G 새 체크박스는 0부터 시작. 공식 Mojang client.jar/인게임 확인은 여전히 미완료. **체크포인트 v38과 상위 세부과제 최종 완료 0/5 불변**, 애니메이션 보류 및 기존 v24 모드 결과 보존.

## [과거 v38] 당시 최신 — 참나무 선반 7 leaf/7 template·32 정적 상태·38 UV 원본 실화소 (2026-11-13)

- [v38 오크 선반 상세 보고서](research/vanilla_models/v38/00_v38_오크선반7리프7부모_32상태_38UV실화소분석.md) · [리프/부모 7+7 SHA·기하](research/vanilla_models/v38/01_oak_shelf_7_leaf_7_template_source_sha_geometry.csv) · [원본 38 UV면](research/vanilla_models/v38/02_oak_shelf_38_original_declared_faces_explicit_uv.csv) · [24 multipart 규칙](research/vanilla_models/v38/03_oak_shelf_24_original_blockstate_multipart_rules.csv) · [32 상태 전수 평가](research/vanilla_models/v38/04_oak_shelf_32_static_blockstate_combinations_evaluated.csv) · [2 PNG 원본 검사](research/vanilla_models/v38/05_oak_shelf_2_original_png_pillow_rgba_crc_sha.csv) · [38면 전 화소 실측](research/vanilla_models/v38/06_oak_shelf_38_face_original_png_uv_rgba_regions.csv).
- v36 P1 544 후보 중 `oak_shelf` **7 leaf를 직접 원본 SHA 확인**(v36 일치 7/7), 템플릿 7 부모·공통 block 부모·블록 상태 1·item 에셋 1 확인. v35~v38 **선택 리프 신규 직접 검사 28개**(v35 15, v36 6, v38 7), 다만 v5~v34와 전체 중복 대조를 마친 완료율은 아님.
- 부모 원본 선언 **11 elements/38 faces**(7개 모델 합), **38/38 explicit UV**, UV X반전 8/Y반전 8, `cullface` 23, 0두께 앞면 패널 5. 한 월드 상태에서는 본체 3요소·15면 + 전면 1요소·1면 = **4요소·16면**, inventory 모델 별도 3요소·18면. 얕은 본체 깊이 z11–16 = 5/16블록.
- `multipart` 소스 **24 규칙** / 소스 속성 `facing` 4 × `powered` 2 × `side_chain` 4 = **32 조합 모두 정확히 본체+전면 패널 2모델** 선택됨. 실제 게임에서의 모든 상태 전이 가능성/정적 렌더 결과는 미검증.
- 원본 PNG 2개 `oak_shelf` 32×32 + `stripped_oak_log` 16×16을 **Pillow 전체 RGBA·PNG CRC로 독립 검사, 원본 1,280픽셀 전부 불투명**, v34 PNG SHA 2/2 일치. 38면 전부 `oak_shelf.png` 한 장 사용 (`stripped_oak_log`는 `#particle` 전용); 원본 UV 크롭 실제 **2,304 texel-uses 모두 불투명**, 고유 UV 사각형 19종(중복 포함 사용횟수와 원본 픽셀 수 구별).
- 공식 Mojang client.jar 무결성·실제 게임 UV/정적 연결 표시·컬링·조명 검증 **미완료**. 애니메이션 계속 보류, 기존 v24 가구 모드 누계·역사 자료 보존, 상위 1단계 5개 세부과제 완료 **0/5**, P1/프로젝트 완료율 미계산.

## v37 이전 체크포인트 — 정적 원본 PNG·기하 UV 근거 연결 (2026-11-13)

- [v37 실제 원본 화소·UV 검증 보고서](research/vanilla_models/v37/00_v37_화로용광로훈연기_정적11PNG_34면실화소_분석보고서.md) · [정적 원본 PNG11종 CRC·Adler·RGBA](research/vanilla_models/v37/01_eleven_static_png_original_rgba_crc_adler.csv) · [34면 실화소/2면 애니메이션 보류](research/vanilla_models/v37/02_six_leaf_36_face_material_static_png_rgba_vs_deferred.csv) · [요약 JSON](research/vanilla_models/v37/v37_static_furnaces_png_pixels_summary.json).
- v36 원본 화로·용광로·훈연기 6 leaf의 텍스처 참조 13종 중 **정적 11 PNG 파일 원본 바이너리 전체 RGBA 2,816픽셀을 직접 해독**(불투명2,816/투명0/반투명0). v34 원본 PNG SHA 11/11 일치, 모든 PNG 청크 CRC32 및 zlib Adler32 검증 성공.
- v36의 **36 face×material 적용 행 중 34면**에 원본 정적 PNG 실제 픽셀을 연결한 유도 UV 텍셀 사용 **8,704회 전부 불투명**. 이 34행은 공통 cube의 6고유 선언면과 다른 개념이며 원본의 미명시 UV를 추론한 영역이므로 엔진 방향·컬링 검증이 아님.
- 화로 고정 정면 PNG의 꺼짐/켜짐 비교: **RGBA 36/256 위치 차이, RGB 36/256, 알파 0/256**(정적 텍스처 비교, 애니메이션 아님). 다중 프레임 참조 `blast_furnace_front_on`, `smoker_front_on` **2 PNG/2면은 이미지 프레임 분석 보류 유지**.
- 이번 조사에는 **독립 Python/Pillow 재검산 및 공식 Mojang 1.21.11 client.jar/실제 인게임 UV·조명·컬링 검증 없음**. v24 모드와 과거 애니메이션 조사자료 보존, 전체 5 세부 과제 완료 **0/5**, P1/프로젝트 완료 퍼센트 미계산.

## v36 신규 P1 원본·역사 근거 대조

- [v36 보고서](research/vanilla_models/v36/00_v36_P1_544과거SHA대조_화로용광로훈연기6모델_24상태_정적분석.md): 기존 v35 P1 직접 15개 + 신규 v36 화로/용광로/훈연기 leaf 6개 직접 SHA 확인(6/6). 부모 3개, blockstate 3개, 24 variants, 공통 cube 6 source face / 36 face×material 적용.
- [P1 544 SHA 대조](research/vanilla_models/v36/01_p1_544_historical_sha_evidence_crosswalk.csv): 선택된 과거 증거 CSV 18종에 한하여 83개 모델의 직접 SHA 일치 기록 발견. 446개는 이 18개 기록에서만 미연결; 과거 전수 미검증 개수를 뜻하지 않음.
- v36 신규 PNG RGBA 0, 공식 client.jar·인게임 미검증, 애니메이션 보류, 완료 0/5. P1 전체 완료율 미계산.

| 1단계 세부 작업 | 상태 | 수치 |
|---|---|---|
| 01. 바닐라 재질·텍스처 분석 | v35 P1 종·케이크·벌통·벌집 **16 PNG/4,096 전 RGBA 픽셀**, 과거 v4 150선정표본 유지 | 원본 PNG 불투명3,496/투명600/부분0, UV 대상 99 face×material **10,900 texel-uses 전부 불투명**, 6 PNG 독립 Pillow·SHA256 검사; 종 particle-only 1 PNG 포함, face에 사용되지 않음 |
| 02. 바닐라 3D 모델·블록 구조 분석 | v35 P1 **544중 이번 source 검수15 leaf**(v34 SHA 15/15 일치), 전체 모델 경로 인벤토리2390 유지 | 종4원형33명시 UV면·케이크7원형42암시 UV면·벌4leaf 공유cube6소스면/24면×재질, 원본 선언면81/재질사용행99, blockstates4/71원본 상태. **15/544는 이번 회차 조사량이지 완료율 아님**, 공식 jar/인게임 검증 미완료 |
| 03. 가구 모드 3D 모델 분석 | **v24 Another 의자 leaf 39개 원본 JSON/SHA 확인, 원형 구조 비교** | 선정 Another leaf **204**(165+39), 새 10 상태 Another 경로 **91/91**, 블록 상태 **22/177** 유지; Handcrafted 원형120/leaf16, Macaw 0. |
| 04. 가구 모드 텍스처·UV 분석 | **v23 화소 실측 누계 유지 (v24 신규 PNG/RGBA 0)** | Another PNG **151종/실제 UV RGBA 3,329면**, Handcrafted **24종/784면**. 합계 **175 PNG/4,113면**. v24 구조상 상속 1,794면은 PNG 실화소로 미검증. |
| 05. 바닐라 ↔ 가구 모드 비교 검증 | 사전 비교만 작성 / 최종 검증 미시작 | 두 모드의 의자·벤치·소파 5유형 구조 비교표 작성. 바닐라와의 인게임 비교는 미완료 |

**전체 완료:** 0/5개. 일부 체크포인트의 100%는 *표본 수 달성*만을 뜻하며 공식 JAR/인게임 재현까지 마쳤음을 의미하지 않습니다. 02번도 모집단이 확정되지 않아 임의 완료율을 산출하지 않습니다.

## v35 (2026-11-13) — P1 첫 검수: 종·케이크·벌통/벌집 15원본모델/71상태·16PNG

- [v35 전체 보고서](research/vanilla_models/v35/00_v35_P1_종케이크벌통벌집_15모델_71상태_16PNG_분석보고서.md) · CSV **14개**+summary JSON1개, P1 모델 **544개 전체 이번 회차 검수 여부 원장**. 이번 직접 원본 검수는 leaf15개(종4·케이크7·벌4), P1 기존 Git SHA **15/15 일치**, 나머지529개는 **이번 회차 미검토**(과거 분석 상태는 전수 미대조). 기존 원본 파일 인벤토리 v34 및 모델 모집단 보존.
- 종 받침 4원형 **6 source요소/33 명시 UV 면**, 별도 종 본체/특수 렌더러는 원본 JSON만으로 검증되지 않음. 케이크7정적 원형 **7요소/42 암시 UV 면**, `from.x=1/3/5/7/9/11/13` 및 절단면 `cake_inner`. 벌4leaf(요소0)/공유 `orientable_with_bottom→cube` 1요소/6원본면, 24면×재질 적용.
- **16 PNG/4,096 원본 전체 RGBA**(불투명3,496/투명600/부분0), 면별 PNG 선택 픽셀 **10,900 texel-uses 전부 불투명**(종명시724+케이크유도4,032+벌유도6,144). **81고유 source 선언면**(종33+케이크42+공유cube6)/99 face×material 기록. `bell_bottom`은 particle-only로 선택면 표본에서 제외. 독립 Pillow verify/RGBA/SHA256 재검증 **6PNG 성공**, v4 선정150종과 16경로 중복0.
- source blockstate **4종·71 variants**(종16·케이크7·벌통24·벌집24), `uvlock` 키 원본 미기재 71. 꿀 수치5에 front texture 정적 교체, 원본 PNG 위치별 RGBA 차이 **벌통24/벌집25픽셀**. 기존 애니메이션 보류 지시 준수.
- 공식 Mojang 1.21.11 client.jar 및 종 특수 renderer/정적 UV 방향·실제 인게임 컬링/조명 미검증. v24 모드 보존, 상위 1단계 최종 완료 **0/5**.

## v34 (2026-11-13) — 바닐라 2,390 블록 모델 목록 확보, 정적 랜턴·촛불·막대 153명시 UV면

- [v34 전체 보고서](research/vanilla_models/v34/00_v34_바닐라2390모델_정적랜턴촛불_153면UV_전체목록.md) · 9 CSV + summary JSON. **Git tree를 실제 전수 열람**하여 `models/block` **2,390 JSON**, `blockstates` **1,168 JSON**, `textures/block` **1,111 PNG** 파일 경로·Git SHA 파일 인벤토리 보존. 고유 blob SHA 2,374/1,015/1,100. 별도 `models/item` 1,283 JSON 및 PNG `.mcmeta` 99파일은 이번 모델/PNG 분모 밖. **이건 파일 목록의 분모이지 검토 완료 모델 수/가구 검수 subset이 아니므로 현재 완료율 %로 사용하면 안 됨**.
- 정적 원형 `template_lantern/template_hanging_lantern`, `template_candle/2/3/4`, `end_rod`, `template_lightning_rod` **8원본 JSON/42요소/153 source face 전부 명시 UV**. **랜턴31면은 source JSON 구조·명시 UV만** 측정; 원본 랜턴 PNG 16×48은 사용자 애니메이션 보류 때문에 **PNG 픽셀/프레임 조사 안 함**.
- 촛불 4원형 **3/6/9/12요소·10/20/30/40면**, 각 2개는 0두께 평면에 `rotation ±45°`; 촛불 원본100면 / 520 texel-uses 전부 불투명. `end_rod` 11면/172, `template_lightning_rod`11면/196 각각 전부 불투명. 합 **122원본 UV면·888 texel-uses** 실제 원본 PNG 픽셀 검증.
- Python/Pillow로 사용자 GitHub 원본 3개 PNG를 **verify()·Git SHA/독립 SHA256·전체 RGBA·16비트 행 알파 마스크** 대조. 16×16×3=**768원본 PNG 픽셀 중 불투명119/완전투명649/부분0**. 가구 3 PNG 원본 전체 투명도가 높더라도 face UV에 선택된 888번 사용은 모두 불투명. 153 face 중 31 lantern은 픽셀 검증 미완료. **명시 UV 역방향18·UV 면적0 없음**.
- `blockstates` 5개 직접 읽어 **30 source variants**(일반·영혼 랜턴2+2/촛불8/엔드막대6/피뢰침12), x비0 15/y비0 9/`uvlock` 키 부재 30. lit/powered는 정적 source 선택 기록일 뿐 모션·불꽃·애니메이션 조사 아님.
- 공식 Mojang 1.21.11 client.jar 독립 출처 및 인게임 정적 렌더/UV·컬링 미검증. v24 모드 자료 유지, 상위 1단계 최종 완료 **0/5**. 다음은 새로 얻은 원본 파일 인벤토리에서 실제 가구 검수 대상으로 확정할 부분집합을 분리해 분석 분모를 만들고 공식 게임 엔진/정적 UV를 대조하는 것.

## v33 (2026-11-13) — 가마솥·호퍼·퇴비통 정적 148면·12PNG/3,072픽셀·15상태

- [v33 전체 원본·암시 UV 보고서](research/vanilla_models/v33/00_v33_가마솥호퍼퇴비통_148면_암시UV_PNG정적분석.md) · 파생 CSV **11개**/summary JSON 1개. 정적 모델 원본 **12 JSON/40요소/148선언면**: 가마솥13/58, 호퍼(아래)7/32·(측면)7/32, 퇴비통 본체5/18 + 내용물 상태8/8. **148면 모두 원본 JSON에 명시 UV 없음**.
- 요소 `from/to`·면방향에 기반한 **암시 UV 사각형 추론**으로 실제 원본 PNG 선택 영역을 측정: **9,280 texel-uses**, 불투명9,280/투명0. 정확한 게임 로더 UV 방향·회전/컬링은 미확인. 148면은 여러 정적 원형의 합이지 동시 렌더 148면 아님.
- **PNG12경로/3,072 원본 픽셀**, 불투명2,332/완전투명740/부분0. `cauldron_inner`와 `hopper_inside`는 원본 blob SHA가 완전히 같음(구별되는 파일 bytes 11). 기존 v4 선정150 경로와 겹침 0, 단 v26 `composter_top`과 중복 분석 일치. 새 4 PNG Python/Pillow **verify/RGBA/SHA256** 독립 교차검증 4/4.
- `hopper`와 `hopper_side`는 처음 6/7 요소 같고 **마지막 배출구 요소1만 다름**. `composter` `multipart` 원본9규칙의 level0–8 고정상태 조합 **9/9** 확인, 내용물 표면 y=3/5/7/9/11/13/15/15, 최종 두 level은 높이 같고 내용물 PNG만 변경. **15 원본 상태 규칙**(가마솥1·호퍼5·퇴비통9).
- 이전 v32와 모드 v24 자료 유지. **애니메이션 사용자 보류 계속 적용**, 공식 Mojang 1.21.11 client.jar/실제 게임 정적 UV·회전·조명 검증 미완료, 최종 완료 **0/5**.

## v32 (2026-11-13) — 정적 통/베틀/4작업대 7 leaf·25PNG 전 화소·20 states

- [v32 원본 직접 분석 보고서](research/vanilla_models/v32/00_v32_정적통베틀작업대_25PNG_42면암시UV_20상태보고서.md) · CSV **8개**, 비교 JSON1·summary JSON1. 공통 `cube` 부모 **한 요소/6 소스 면**을 상속하는 `barrel` 닫힘·열림, `loom`, `cartography_table`, `fletching_table`, `smithing_table`, `crafting_table` **7 leaf** 모두 자체 요소0. 각 leaf의 최종 6방향 재질 연결 **42 face×material 인스턴스**(신규 고유 원시 선언면 42가 아님).
- 직접 PNG 원본 **25경로×16×16=6,400픽셀** RGBA 해독: **6,400불투명/0완전투명/0부분알파**. v4 기존150종 표본과 **12경로 중복/13경로 밖**, 이전 v4 화소 기록 12/12 바이트·크기·총·가시 픽셀 일치. `cube`는 명시 UV 없이 완전한 16³ 정육면체이므로 **full-face 16×16 암시 UV 유도 추론** 기준으로 42면 **10,752 texel-uses** 모두 불투명; 실제 게임 UV방향/컬링 결과는 별도 검증.
- 원본 `blockstates` **6파일·20 variants**(통12, 베틀4, 4종 작업대 각1), source x비0 10/y비0 9/`uvlock` 키 부재20. `barrel_top` 대 `barrel_top_open` 두 원본을 **독립 Pillow+Git SHA 검증**, 256픽셀 중 **132픽셀 서로 다르고 124픽셀 일치**. 정적 상태 모델 선택이지 애니메이션 프레임 분석이 아니다.
- 사용자 애니메이션 보류 지시 계속 적용. 공식 Mojang 1.21.11 client.jar·실제 게임 정적 UV/조명/회전 미확인, 모드 v24 수치 보존, 최종 완료 **0/5**.

## v31 (2026-11-13) — 끌로 조각한 책장 256조건·양조기 8조건, 47면 UV/6PNG, 모닥불 on/off

- [v31 상세 실측 보고서](research/vanilla_models/v31/00_v31_책장양조기_264상태_47면_PNG실화소_모닥불원본보고서.md) · CSV **10개**, JSON 1개. 책장 52 `multipart` 원본규칙/4방향×64슬롯=**256상태 계산 평가**, 매 상태 본체1+장식6=7모델 선택. 양조기 7 source 규칙/3병×2상태=**8조건**, 매 조합 본체1+슬롯3=4모델 선택. 원본 규칙 **59건**, 평가 입력 **264개**, 조건별 모델 적용 횟수 1,792+32=**1,824번**(고유 모델 1,824개 아님).
- 책장 본체1요소/5면 + 장식6원형 평면 1요소/1면씩 = **11 source face**, occupied/empty 텍스처를 동일 UV에 연결한 **17면×재질** 실제 PNG 화소 **1,792 uses** 모두 불투명. 본체 `uvlock:true` 명시 4규칙, 장식48규칙 키 부재.
- 양조기 본체4요소/24면 + 6개 병/빈자리 원형 0두께 평면 각 1요소/2면 = **36 source face/2,016 uses(불투명1,260/투명756)**. 4 평면 요소 x값 -0.41로 모델 원시 영역 밖. 인게임 충돌/컬링 여부는 미검증.
- PNG6종 전체 **1,536픽셀/불투명1,410·완전투명126**, v4 기존 150종 표본 2경로 중복/4표본 밖. 이번 책장+양조기 **47고유 원본 면/53재질면·3,808 texel-uses 중 불투명3,052/투명756**.
- 모닥불 preliminary: `template_campfire` **7요소/32면**(평면2, 내부 회전2), `campfire_off` **5요소/28면**, blockstate 일반+영혼 8+8변형, 불꽃 두 `png.mcmeta`에서 `frametime=2`. 이번에는 불꽃 원본 PNG 화소/애니메이션 프레임 대조하지 않음.
- 기존 v30 투명도 정정과 모든 v24 모드 계량 보존. **독립 공식 Mojang client.jar/인게임 회전·UVlock·조명·애니메이션 미검증. 완료 0/5.**

## v30 (2026-11-13) — 5개 바닐라 가구형 모델 91면·18PNG 실화소 분석 및 v26 오류 정정

- [v30 전체 보고서](research/vanilla_models/v30/00_v30_바닐라5모델_91면UV_18PNG_RGBA_투명도정정보고서.md) · CSV **9개**/JSON 요약 게시. 소스 모델 **5개/18 요소/91원본 면**, 모루 top 텍스처 3종 치환으로 **93개 face×material 기록**, 원본 `uv`→PNG **6,012 texel-uses**, 모두 불투명. 화분 dirt 1면은 v26 표본과 중복, **90원본 face**를 새로 실제 픽셀까지 연결.
- 원본 **PNG 18경로×16×16 = 4,608픽셀** 실제 RGBA 해독(불투명3,582·완전투명1,026·부분알파0). v4 150표본 경로5 중복/13표본 밖. 기존 v4 파일 바이트·크기·전체/가시픽셀 **5/5 일치**. 18 모두 프로젝트의 신규 고유 텍스처는 아니며 기존 v26–29 `oak_planks/dirt`와 중복.
- 독서대 상판 **-22.5° 요소 회전**, 숫돌 `face×facing=12` 블록 상태, 모루 손상 3 leaf의 **공통 기하/서로 다른 top PNG**, 마법부여대/독서대의 **정적 모델 JSON과 책 엔티티 렌더러 연구 분리**(v8/v9 기존 근거)를 구분.
- **중요 수정(v26):** 색 형식 0 그레이스케일 PNG `tRNS` 샘플 0을 무시한 파서 오류로 `stonecutter_saw`의 투명도를 오기재했음. **독립 Pillow로 16×48 실제 불투명246/투명522** 검증 후 **v26 PNG8종 총합 불투명3,900·투명4,804** 및 **70행 UV·3,652uses 불투명3,328·투명324**로 CSV·JSON·보고서를 함께 교체. v30 새 PNG의 해당 형식도 정정.
- **공식 Mojang JAR·인게임 렌더·UVlock 검증 여전히 미완료**, 03/04 모드 v24 누적 고정, 최종 완료 **0/5**.

## v29 (2026-11-13) — 울타리문 160면 전부 직접 PNG 픽셀 및 열림·담장 좌표 변화

- [v29 실측 보고서](research/vanilla_models/v29/00_v29_울타리문160면_실제PNG_UV_열림담장좌표비교보고서.md) · 파생 CSV **6개**, JSON 1개 게시. **4원형×40=160 원본 명시 UV면**을 `oak_planks.png` 원본 픽셀에 연결하여 **1,952 텍셀 사용**(불투명1,952, 투명0, 부분 알파0) 계량. 이전 v28의 원형 선언 면 160과 동일 대상이므로 **중복 신규 face 합산 금지**.
- 각 원형 사용 횟수 일반512/열림464/담장512/담장+열림464. 원본 요소 8개 비교: **열림 시 2기둥 불변/나머지6 변화**, **담장 연결 시 8개 모두 y축 -3**, 열린 상태에도 같은 y -3 정확 일치. 16가지 source `facing/open/in_wall` 상태의 선택 원형·회전/uvlock 값을 직접 연계.
- **v29 새 원본 PNG 경로 0개**. 기존 `oak_planks.png` 195바이트를 사용자 GitHub에서 재취득, 독립 Python/Pillow PNG `verify`·RGBA 디코딩, Git blob SHA 재계산 및 **독립 SHA-256이 기존 v4 기록과 정확히 일치**.
- **원본 상태 JSON의 `uvlock:true` 확인은 실제 모델 로더 UVlock·회전/게임렌더 실행 검증이 아님**. 공식 Mojang 1.21.11 client.jar 교차인증도 미완료. 모드 v24 수치 보존, 완료 **0/5**.

## v28 (2026-11-13) — 바닐라 문 40면·울타리 문 4원형/104 상태 원본 직접 실측

- [v28 원본·화소 분석 보고서](research/vanilla_models/v28/00_v28_바닐라문다락문게이트계단104상태_40면UV_RGBA.md)와 CSV **7개**·JSON 요약 게시. 이전 바닐라 v25–27과 별도 보존.
- `oak_door`32 + `oak_trapdoor`16 + `oak_fence_gate`16 + `oak_stairs`40 = **104 원본 `variants`**의 상태키/모델/x·y/uvlock을 행 단위 전수 검토. **모델 경로18개**, `uvlock:true` 명시51/키 부재53, x비0 20, y비0 72. 이전에 읽은 블록상태를 '새 4종 발견'으로 중복 가산하지 않는다.
- 참나무 문 **leaf8 → 원형8(각1요소/5면)**, 동일 기하 원시 bbox `[0,0,0]–[3,16,16]` 및 면별 UV 대응 검사. 원본 `oak_door_bottom/top.png` **2종/512픽셀 재디코딩**, v4 기존 150종 표본 중복이므로 신규 PNG 고유 경로 수는 0. **40면/5,248 UV 픽셀 참조회수**(불투명4,864/완전 투명384) 직접 측정.
- 울타리 문 **leaf4/원형4** 직접 JSON, 각 원형 **8요소/40면 선언**, 원형 선언 합 **32요소/160면**. 열린 경우 깊이 z·담장 연결 시 y bbox가 원본에서 변경. `oak_planks`는 v26에 이미 재디코딩되어 이번 새 PNG로 계산하지 않음.
- 비공식 미러 PNG SHA2/2, v4 PNG2종 바이트/크기/전체·가시 픽셀2/2 일치. 공식 Mojang JAR·인게임 모델/UVlock 처리 검증 **미수행**, 완료 0/5, 모드 v24 지표 유지.

## v27 (2026-11-13) — 바닐라 32×32 선반/자동 UV 퇴비통 화소 및 상태 교차 검증

- [v27 원본 전체 보고서](research/vanilla_models/v27/00_v27_선반32x32_퇴비통자동UV_원본화소검증보고서.md) · 연구 CSV **8개**, 요약 JSON 1개를 별도 저장.
- PNG **5경로 새로 전체 RGB·알파 조사**, 2,048픽셀 **불투명1,824/투명224**. `oak_shelf` 32×32 한 종은 기존 v4 텍스처 150 표본과 중복. 기존 v26 `composter_top`은 신규 계수 제외.
- 선반 템플릿 **6개 원본**의 **명시 UV 20면** 실제 `oak_shelf.png` 영역 픽셀 **1,376회** 조사. `oak_shelf` 블록 상태 **24 multipart 원본 규칙**으로 32개 합성 상태의 본체+전면 **2경로/방향회전 일치 32/32** 계산.
- 퇴비통 본체 18면+내용물 8면 = **26 암시 UV**를 유도 좌표식에 따라 샘플한 **3,696회 실제 PNG 텍셀**. 계산식의 입력은 원본 요소 from/to, 직교 6방향이며 동일 버전 `stairs/slab/fence_post` 명시 UV **23/23 숫자·순서 일치**로 정합성 점검. **공식 엔진/인게임 UV 검증을 수행한 것은 아님**.
- 이번 v27의 **명시 20 + 유도 26 = 46면/5,072 텍셀 사용**은 전부 불투명한 소스 픽셀에 놓이지만, 전체 PNG에는 투명 픽셀이 존재하는 등 UV 선택 효과가 뚜렷함. 기존 v26 70프레임/36면과 중복 계수 유의.
- 미러 PNG SHA **5/5** 동일, v4 `oak_shelf` 파일·차원·픽셀/가시/색수 **1/1** 동일. 공식 JAR/인게임/CRC·독립 Pillow 미검증.
- **01·02 지속 진행, 03·04 v24 누적 유지, 05 미완료 / 최종 0/5**.

## v26 (2026-11-13) — 바닐라 원본 PNG 8종·면 36개/애니 프레임 70건 RGBA 직접 검증

- [v26 바닐라 PNG 실화소·UV 면 분석](research/vanilla_models/v26/00_v26_바닐라8PNG_전체RGBA_36면70프레임_실화소보고서.md) 및 파생 CSV **4개**와 기계 요약 JSON 저장. 기존 바닐라 v4/v10·모드 v24 연구 결과와 분리.
- v25에서 IHDR만 검사한 **같은 PNG 8종을 실제 zlib/PNG 압축 역해독**하여 **8,704 RGBA 픽셀 (불투명 3,900·완전 투명 4,804·부분 알파 0)** 측정. 본 단계 PNG 수가 기존 150 표본에 모두 추가되는 것은 아님: **3종은 v4에 이미 포함**.
- 명시 UV를 가진 모델 **6개/고유 면 36개**의 PNG 실제 사각형 조사, 애니메이션 3프레임 포함 **70개 기록**. UV 영역 픽셀 사용 **3,652회(불투명 3,328·완전 투명 324)**. 19건은 반전 UV. 이 사용 횟수는 고유 픽셀 수/인게임 화면 픽셀 수가 아님.
- 이전 v4 실측 3종은 **파일 바이트/크기/가시·전체 픽셀 수 3/3 일치**, 기존 공개 비공식 미러 PNG와 Git blob SHA **8/8 일치**. 자체 PNG chunk CRC/Adler32 및 Pillow 독립 전체 재검증은 미수행; **공식 Mojang JAR/인게임 검증은 미완료**.
- 최종 완료 **0/5**; 다음은 바닐라 01/02의 공식 검증, 암시적 UV·상태 회전, 추가 대표 모델. **모드 연구 지표 변경 없음.**

## v25 (2026-11-13) — 바닐라 원본 자료 직접 연구 재개

- [v25 원본 감사 보고서](research/vanilla_models/v25/00_v25_바닐라원본_모델상속상태PNG_직접검증보고서.md) 및 8개 파생 CSV와 기계 요약 JSON 게시.
- 사용자 제공 `1.21.11/assets/minecraft/`에서 **모델 JSON 32개, 상태 JSON 8개, PNG 8개, png.mcmeta 2개 = 50파일 직접 읽기**. 자체 기하 8모델 **44요소/204선언면**, 별도로 상태 8종 **79 variants/9 multipart/27 모델 참조 경로**; 퇴비통 8개 상태별 내용물 y상단 3~15, 8 leaf 상속 **11요소/57면 인스턴스**.
- PNG8종 원본 **IHDR 바이트 확인**, 16×48 톱날/랜턴 애니메이션 메타 확인. 새 PNG **전체 화소 분포/면 UV 내부 RGBA 0건**; 6개 업로드 에셋과 이전 1.21.11 비공식 미러의 Git blob SHA **6/6 일치**. **Mojang 공식 client.jar 인증·인게임 렌더 확인은 아니다.**
- `1.21.11` 원본 자료가 현재 public repo에 존재하므로 원본 재배포 정책/저작권 점검 필요. 이번 v25 결과에는 원본 게임 JSON·PNG·JAR를 별도 복제하지 않았음.
- 01의 기존 **150/150 표본** 유지, 02 **진행 중**, 03/04 모드 v24 누적 수치 변경 없음, 05 미완료. 최종 확정 완료 **0/5**. 다음은 **바닐라 01·02 우선**.

## 누적 근거 데이터 (v8 SQLite + v9 CSV + v10 SQL migration + v11~v24 모드 CSV + v25 바닐라 CSV)

- 텍스처 측정 레코드: 150건
- 최초 모델 근거: 55건
- 최초 블록 상태 근거: 16건
- v6 UV 면별 기록: 90건
- v7 조립 상황: 21건 (선택형 사례)
- v8 특수 렌더링 블록 근거: 17건
- v8 텍스처 아틀라스: 6건
- v9 특수 렌더링 모델: **17종**, **19개 레이어**, **55개 큐브/평면(평면형 15개)**, 추출 JSON 직접 검증
- v9 애니메이션: **6종 모델**, **15개 클립**, **304개 저장 키프레임**
- v10 통합: v9 데이터 **19개 모델 레이어·15개 애니메이션 클립**을 v8 SQLite에 추가하는 SQL migration 게시, 로컬 재구성 DB 무결성 검사 통과
- 공식 JAR 검증 도구: **스크립트 작성 및 합성 테스트 통과**, 실제 Minecraft 1.21.11 client.jar 비교는 미수행
- v11 Another Furniture (Minecraft 1.21.1): Git tree 모델 1,451개·블록 PNG 1,220개 확인. **템플릿 69개 직접 분석(299 요소/1,362 UV면/0두께 요소 34개)**, **완성형 33개 상속 해석**, **블록 상태 12개(802 entry 합산)**, **PNG 헤더 12개**.
- [v11 자세한 실측 보고서](research/furniture_mods/v11/00_v11_AnotherFurniture_모델분석_보고서.md).
- **v12 Handcrafted:** `1.21.x` 브랜치의 고정 커밋 `8d21d166...` 전체 원형 JSON **120/120 직접 측정(810 요소·4,860 UV 지정 면·283 비영 회전·183 0두께)**. 자동 생성 블록 모델 **11,989 경로** 확인(그중 16건 상속 실측), 상태 JSON 12개(4,724 상태 항목), PNG 헤더 12개. 소파·벤치·의자 **5쌍 사전 비교**. Macaw의 공식 1.21.11 배포 확인, 실제 모델 실측 0건(보류).
- [v12 자세한 실측 보고서](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md). 두 모드의 원본 JSON·PNG는 저작권 때문에 미재배포.
- **v13 실제 PNG 화소:** 양 모드 각각 12개씩 **24개 전체 PNG 바이트 직접 디코딩**, SHA 일치; 알파 0/255 화소 총 **117,504개**(반투명 0), RGB 색상 수·밝기·가시 범위 실측. **모델 13개 UV 571면 전부 텍스처 픽셀 경계 정렬**, UV 역방향 면 190개·면적 0 UV 64개(오류 단정 금지).
- [v13 실화소·UV 상세 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md) · [PNG 실측 12+12 CSV](research/furniture_mods/v13/) · [로컬 검증 스크립트](scripts/reproduce_mod_png_v13.py).

- **v14 신규 결과:** Handcrafted 생성형 leaf **16개**, 슬롯 참조 **51건** (모드 경로 35 / Minecraft 참조 16). 기존 v13 실측 PNG에 SHA·치수까지 일치 **19건**, v13 PNG 표본 밖 모드 참조 **16건(고유 12 PNG)**. 모드 슬롯 모두 연결 7개 leaf, 하나 이상 연결 13개, v13 UV 부모 표본 대응 9개. [v14 보고서](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md). **이번 원본 바이트 재디코딩 및 face→PNG 실화소 검증 0건**.

- **v15 신규 정량 비교:** v11/v12 기록 189개 모델에서 면 선언 가능한 슬롯과 실제 기재 수를 비교. Another Furniture 69개/299요소/가능면 1,794개 중 **1,362면 선언(75.92%)**/생략 432, 회전 17·평면 34·원시 bbox 0..16 밖 모델 3개. Handcrafted 120개 원형 모델 중 자체 요소 112개/810요소/가능면 4,860개 중 **4,860면 선언(100%)**, 회전 283·평면 183·원시 bbox 밖 모델 60개. [v15 보고서](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) · [모델별 189개 CSV](research/furniture_mods/v15/model_geometry_derived_189.csv) · [재계산 검증 코드](scripts/verify_v15_geometry_research.py). **기존 계측을 새 방식으로 집계한 2차 분석이며 v15 신규 원본 모델/PNG 직접 관찰은 0건.**

- **v16 원본 직접 검증 확장:** 제작자 Handcrafted 고정 커밋에서 원본 JSON **30개**(16 leaf/14 부모) 직접 읽고 이전 v12 Git blob SHA와 일치 검증. v14에서 남았던 PNG **12개 원본**을 새로 디코딩해 **66,816픽셀** 실측(가시 7,358·투명 59,458·반투명 0). 완전 투명 PNG `bench/cushion/none_cushion`·`shelf/overlay/none` 2개. 원본 leaf 51슬롯 확인, 부모 geometry 면 **786 인스턴스** 중 **784 모드 면 모두 원본 PNG 이름·SHA·해상도·정수 UV 픽셀 격자·범위 대조 성공**, Minecraft 기본 텍스처 의존 2면 제외. [v16 보고서](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md), [모드 면별 재질 그룹 36](research/furniture_mods/v16/handcrafted_16_leaf_face_material_groups.csv), [PNG 12 추가 픽셀 CSV](research/furniture_mods/v16/handcrafted_12_new_png_pixel_metrics.csv). **개별 면 사각형의 실제 픽셀/알파 샘플링 및 인게임 검증은 미완료**. [원본 파일 로컬 재현 코드](scripts/reproduce_v16_handcrafted_originals.py) 추가: 문법 검사는 통과했으나 실제 고정 원본 체크아웃 환경에서 전체 실행 테스트는 미완료.

- **v17 새로운 면별 직접 검증:** 고정 Handcrafted 원본 PNG **24종을 다시 직접 디코딩**, v16에서 연결된 **784/784 모드 면**의 UV 영역 실제 RGBA 픽셀 분포 측정. **612 비영 UV/172 0면적, 420 전부 불투명/145 불투명·완전투명 혼합/47 전부 투명**, 총 **41,290 텍셀 사용 횟수(불투명 31,665/완전투명 9,625/부분 반투명 0)**. [v17 보고서](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md) · [784면 CSV](research/furniture_mods/v17/face_pixel_samples_784.csv) · [모델별/텍스처별 집계](research/furniture_mods/v17/) · [로컬 Pillow 독립 검증 코드](scripts/reproduce_v17_face_pixels.py). **코드의 원본 체크아웃 대상 end-to-end 실행은 미수행.** 원본 픽셀 출처 검증은 인게임 렌더 검증이 아님.

- **v18 Another Furniture 원본 직접 분석:** 제작자 1.21.1 커밋의 **leaf 33 JSON/템플릿 30 JSON, 총 63개**를 직접 읽고 이전 blob SHA와 모두 일치 검증. **93개 텍스처 override 슬롯**, 원형 709면, leaf에 상속 적용된 **807면의 실제 재질 경로** 확인(모드 804, 기본 dirt 3; 미해결 0). 최종 모드 PNG 고유 53경로 중 이전 실측 12 + **이번 신규 PNG 12종 실제 픽셀** = 24개 실측(45.28%), **29경로 미측정**. 새 PNG 3,072 픽셀에서 불투명 2,156·완전 투명 916·부분 알파 0; 4비트 팔레트 PNG `sofa/wood_2` 지원까지 보완. [v18 보고서](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md) · [면 재질 113그룹](research/furniture_mods/v18/another_face_material_groups_113.csv) · [PNG 12 실측](research/furniture_mods/v18/another_new_png_12_pixel_metrics.csv). **Another 807면의 실제 UV→PNG 화소 영역 검증은 아직 미수행.**

- **v19 Another Furniture 원본 PNG 29종·UV 면별 직접 RGBA 분석:** v18에서 고른 **leaf 33개**의 참조 모드 PNG 미측정 **29종을 제작자 고정 원본에서 새로 직접 디코딩**, 누적 Another **53/53 PNG 원본 실화소**(52종 16×16 / 1종 64×64). 원본 전체 **17,408픽셀**(불투명 **11,536**, 완전투명 **5,872**, 부분알파 0). 템플릿 **30종 원본 JSON을 새로 읽고 SHA 재확인**, 총 **807면의 실제 선언 UV**를 추출한 뒤 **Another PNG에 연결된 804/804면(선정 표본 100%)의 실제 원본 사각형 RGBA** 샘플링 완료. 모두 정수 픽셀 정렬/PNG 경계 안, 4면은 UV 면적 0. 비영 800면 중 **712면 전체 불투명, 88면 혼합, 전체투명 0면**. 중복 면·텍스처 사용 포함 텍셀 사용 **32,531회** 중 불투명 **31,545·투명 986·부분 알파 0**; UV 반전 **221모드 면**. [v19 전체 보고서](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md) · [53 PNG/원본 SHA](research/furniture_mods/v19/another_texture_53_png_source_manifest.csv) · [804면 실화소 CSV](research/furniture_mods/v19/another_804_face_actual_rgba.csv) · [33 가구별 집계](research/furniture_mods/v19/another_33_leaf_actual_rgba_summary.csv) · [두 모드 선정 표본만 비교한 보고서](research/furniture_mods/v19/00_v19_모드간실제면UV픽셀_선정표본비교.md). **모드 전체 전수/바닐라 의존 3면·인게임 렌더·독립 로컬 PNG 재실행은 아직 미완료**.

- **v20 Another 원형 원본 JSON 69/69 직접 재조회:** 제작자 1.21.1 고정 커밋에서 **기존 v11 69 원형 모두** 파일을 다시 읽어 **Git blob SHA·요소 수·명시 면 수 전부 일치**. v18 선정 원형 30 이외 **39개를 새로 직접 자세히 조사**, 총 **299 요소, 1,362 원본 선언 면**의 UV·회전·0두께·raw bbox·cullface 원본 데이터를 저장. **UV 반전 422면 / UV 회전 134면 / cullface 443면 / 0면적 UV 4면 / 회전 요소 17개 / 0두께 요소 34개 / 0~16 외부 원시 bbox 요소 11개(3개 템플릿)**. [전체 상세 보고서](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md) · [69 원형 CSV](research/furniture_mods/v20/another_69_templates_direct_original_geometry.csv) · [1,362 원시 면 CSV](research/furniture_mods/v20/another_69_templates_1362_original_faces.csv) · [SHA 감사 JSON](research/furniture_mods/v20/v20_another_69_original_template_audit.json). Macaw's Furniture 공식 1.21.11 Fabric 3.4.2 배포는 확인했으나 **현재 실행 환경에서 JAR을 다운로드하지 못했으므로 모델 실측 0건**. 이 69 모델은 이미 v11에서 선정한 **원형 표본 전수**로 전체 모드 모델 전수 아님. PNG 실화소 누적 **Another 53 + Handcrafted 24 = 77개** 그대로, 새 39 원형의 재질별 PNG 실측 추가 0. 공식 1.21.11 바닐라/인게임/전체 모드 검증 미완료.

- **v21 Another 블록 상태 기반 신규 38 leaf 원본/PNG 실제 화소 확장:** 제작자 1.21.1 고정 커밋의 **12 블록 상태 JSON SHA 직접 재확인**, **802개 model apply / 고유 114 경로**(그중 Minecraft air 모델 2 apply). v18 선정 33 leaf에 없고 shutter variant 43경로를 제외한 **새 완성형 38개 원본 JSON**을 이번에 직접 읽고 자체 0 elements/원형 부모 21종/override 97슬롯 확인. 새 leaf 상속 face **1,197인스턴스(모드 1,192/바닐라 dirt 5)**, 모드 PNG 원본 **34종** 직접 디코딩(기존 v19 20종 재조회 SHA 일치, **신규 14종 픽셀**). **1,192/1,192면의 실제 원본 UV 사각형 내부 RGBA 전수 샘플**(불투명 1,086면, 혼합 106면, 0면적/전체투명 0). 누적 **Another 선택 leaf 71종, 원본 PNG 67종, 모드 면 RGBA 1,996개**. Handcrafted 합쳐 **고유 PNG 91종/UV 면 2,780인스턴스**. [v21 보고서](research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md) · [신규 38 leaf 재질 면](research/furniture_mods/v21/another_new_38_leaf_face_resolution.csv) · [신규 14 PNG 원본 화소](research/furniture_mods/v21/another_new_14_png_unique_source_metrics.csv) · [원본 1,192 면별 RGB·알파 CSV](research/furniture_mods/v21/another_new_38_leaf_all_rgba_1192.csv) · [감사 JSON](research/furniture_mods/v21/v21_blockstate_new_leaf_rgba_audit.json). **모드 전체 전수 아님**, 바닐라 dirt 미검증 총 **8면**, Handcrafted oak_planks **2면**, 공식 Macaw JAR 직접 실측 **0건** 및 인게임 미검증.

- **v22 Another 셔터 원본 leaf 43개·새 PNG 42종·214면 실제 UV RGBA:** v21의 12 원본 블록 상태 802 적용/114 고유 모델 경로 중, 이미 읽은 셔터 `variant_1/oak_single`을 제외한 **셔터 leaf 43개 원본 JSON 직접 읽기·Git SHA 기록**. 4 부모 원형을 상속한 **214모드 면**, texture/UV 해석 **214/214**. 제작자 원본 PNG **43종 직접 디코딩**(기존 1종 SHA 재검사, **새 42종**), PNG 16×16 RGBA8 전체 **11,008픽셀 모두 불투명**, **214개 실제 UV 사각형도 전부 불투명**; UV 반전 75/회전 42, 0면적 0. [v22 상세 보고서](research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md) · [43 leaf 214면 재질 해석](research/furniture_mods/v22/shutter_43_leaf_resolved_source_face_uv.csv) · [43 PNG 전체 픽셀/해시](research/furniture_mods/v22/shutter_43_png_original_source_manifest.csv) · [214면 UV 픽셀](research/furniture_mods/v22/shutter_214_face_uv_original_rgba.csv) · [감사 JSON](research/furniture_mods/v22/v22_shutter_source_original_complete_audit.json). 누적 Another **leaf 114개/고유 PNG 109종/모드 면 2,210개**, Handcrafted 합계 **PNG 133종/모드 면 2,994개**. **이전 블록 상태 12개가 참조한 Another 모델 경로 113/113 원본 근거 완료**(111 leaf, 2 template; 별도 minecraft air 1 경로). 모드 전체 상태/모델 전수 아님. 바닐라 dirt 8면/oak_planks 2면, Macaw 공식 JAR/인게임 검증 미완료; 완료 판정 0/5.

- **v23 Another 블록 상태 10개·신규 leaf 51개·원본 PNG 42종/UV RGBA 1,119면 직접 검증:** 제작자 1.21.1 고정 원본에서 이전 12개 밖 **10개 새 blockstate JSON을 SHA/실제 variants·multipart 386 apply**로 확인(고유 경로 92, Another 91 + air 1). 벤치·소파·커튼·서랍·테이블·꽃상자·2종 의자 등 **51개 새 leaf JSON 직접 읽기(모두 자체 elements 0, 부모 원형 34종, 서랍 2단계 상속)**. 인스턴스 면 **1,127개** 중 Another PNG 면 **1,119/1,119 실제 UV RGBA**·바닐라 dirt **8면**(공식 PNG 미검증). 원본 PNG 51종 직접 디코딩(**새 42종/기존 9종 SHA 재검사**). 새 모드 면 전부 불투명 **1,063**, 혼합 **56**, 부분알파 0. 중복 포함 원본 PNG UV 텍셀 **41,666회** 중 불투명 39,304/투명 2,362. **누적 Another blockstate 22/177, leaf 165, PNG 151종, 모드 UV RGBA 3,329면**, Handcrafted 포함 **PNG 175종·모드 면 4,113개**. 자작/가문비 벤치 및 의자, 빨강/파랑 소파의 부모·UV 기하 동일/PNG 교체를 원본 면 쌍으로 검사. [v23 보고서](research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md) · [새 10 상태](research/furniture_mods/v23/new_10_blockstates_author_original_audit.csv) · [51 leaf 원본 face 상속](research/furniture_mods/v23/new_51_leaf_source_face_texture_resolution.csv) · [신규 42 PNG SHA](research/furniture_mods/v23/new_42_png_first_measured_in_v23.csv) · [원본 1,119면 직접 RGBA CSV](research/furniture_mods/v23/new_51_leaf_all_1119_face_actual_rgba.csv) · [감사 JSON](research/furniture_mods/v23/v23_new_blockstate_leaf_png_face_original_audit.json). 신규 10 상태에 남은 **39개 의자 leaf JSON**·그 외 블록 상태 **155개**·공식 바닐라/Macaw/인게임 미검증. 전체 0/5.

- **v24 신규 실측:** 제작자 원본 의자 **39개 leaf JSON/Git SHA** 직접 조사·부모 2 원형 재조회. 일반형 19/tucked 20, own elements 0, override 117, **390 요소·1,794 선언 면 인스턴스**. 두 부모 10요소의 raw z 좌표가 -9 이동하고 46면 UV 선언은 동일. 새 10 상태 Another 경로 91/91 원본 확인; 누적 Another leaf 204. **이번 PNG 실제 픽셀/UV 내부 RGBA 새 측정 0**, 기존 모드 누계 유지. [v24 보고서](research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md) · [39모델 SHA CSV](research/furniture_mods/v24/chair_remaining_39_original_json_geometry_audit.csv).

**v24 추가 교차검산:** 제작자 원본 `birch_chair`·`spruce_chair` 두 블록 상태 모두 `south + variant=3 + not tucked`에서 등받이 `*_3` 대신 `*_1` 모델 참조를 직접 확인. 전체 의자 apply 176 중 신규 39 leaf 적용 **155**(다른 기존 5 leaf 21). 기존 횟수 균일 가정 156에서 정정했으며 최종 원본 SHA·회전 분포 대조 완료. 게임 동작/의도 여부 미확정.

## 다음 과제

1. Minecraft Java 1.21.11 공식 `client.jar`와 비공식 미러 자료의 바이트/해시 비교. [로컬 검사 스크립트](scripts/verify_official_jar.py) 및 [사용법](docs/official_client_jar_검증방법.md) 준비 완료(실제 JAR 미실행).
2. 실제 게임에서 잔디·잎의 색 변형, 투명도, 모델 조립 결과 검증.
3. [v10 통합 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md) 및 [v9 특수 모델 자료](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md)의 공식 클라이언트·인게임 교차검증 후 02번 종료 여부 판정.
4. **03번 v12에서 Handcrafted 원형 120개 분석까지 완료:** 검증된 Macaw's Furniture 공식 1.21.11 배포 JAR(또는 공식 소스)을 확보하면 모델 구조를 직접 분석한다. 불확실한 제3자 복제본을 쓰지 않는다.
5. **v23 새 블록 상태 10개 원본·51개 leaf JSON·PNG 새 42종/모드 면 1,119개 실제 RGB·알파 검증 완료**, 누적 상태 22/177. 다음은 v24에서 확인한 39개 의자 leaf의 **PNG 실화소와 1,794면 UV** 및 조사 밖 **155개 블록 상태**, Macaw 공식 JAR, Mojang 공식 1.21.11 client.jar의 dirt 16면/oak_planks 2면, 독립/인게임 검증이다.

**주의:** GitHub에 추적된 SQLite 바이너리는 **v8**입니다. **v11~v23 모드 실측·파생 수치는 CSV/MD로 저장되었고 아직 SQLite에는 통합하지 않았습니다.** v10 SQLite 전체 파일은 로컬에서 생성해 무결성을 검사했으며, GitHub에서는 [v10 SQL migration](data/migrations/v8_to_v10.sql)과 [재구성 스크립트](scripts/rebuild_v10_db.py)를 통해 복원합니다. GitHub에 v10 SQLite 바이너리가 업로드된 상태는 아닙니다.

다른 대화에서 이어갈 때는 v8 DB와 v10 migration, v9 연구 자료, 이 진행도 파일을 함께 기준으로 삼으세요.

## 새 채팅용 체크포인트

- **최신 v24:** [의자 39개 신규 원본 JSON/SHA·2부모 상속 기하 보고서](research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md). Another leaf **204종**, 해당 신규 10상태의 Another 모델 JSON **91/91**. 블록 상태 22/177 유지. 이번 단계 신규 PNG 화소/UV RGBA 0건 → 전체 두 모드 PNG175/실제 모드 면4,113 변동 없음. 다음은 24 참조 PNG 경로와 과거 manifest 차집합·원본 화소 검사.


- **이전 v23:** [Another 새 10 상태/51 leaf 원본 JSON/PNG 신규 42종/1,119면 원본 UV RGBA 검증](research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md). 누적 Another **leaf165/PNG151/모드 면3,329**, Handcrafted 합산 **PNG175종/모드 면4,113**. 블록 상태 **22/177**, 신규 10 상태에 남은 원본 의자 leaf39개. 공식 Macaw/바닐라 JAR/인게임 미검증, 전체 최종 0/5.


- 이전 v22: [Another 셔터 leaf 43개 원본 JSON/새 PNG 42종/214면 UV 실제 RGBA 검증](research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md). 누적 Another leaf **114개/PNG 109종/면 2,210**, Handcrafted 포함 **PNG 133종/면 2,994**. 블록 상태 12개 내부 Another 모델 참조 113/113 원본 확보. **Macaw 공식 JAR/바닐라 공식 JAR/인게임 미검증, 전체 0/5**.


- 이전 v21: [블록 상태 12 SHA/802 model apply, 신규 leaf 38 JSON, 14 새 PNG와 1,192모드 면 실화소 보고서](research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md). **Another 71 leaf/PNG 67/모드 면 1,996**, Handcrafted PNG 24/모드 면 784 누적. 바닐라 dirt 8면/oak_planks 2면 및 Macaw 원본 0건/인게임 미검증. **최종 완료 0/5**.


- 이전 v20: [제작자 Another 원형 69개 전체 JSON SHA 재검증/1,362면 직접 UV·기하 실측](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md). 이 69는 v11 원형 선정 표본(모드 전체 원본 모델 1,451개 파일과 다름). Macaw 공식 1.21.11 Fabric 릴리스 존재는 확인했으나 **JAR 원본 바이너리 확보 실패, 실제 모델 조사 0**. 상위 1단계 확정 완료 **0/5**.


- 이전 v19: [Another 선정 33 leaf가 참조한 고유 PNG 53/53종과 모드 면 UV 실제 RGBA 804/804면 전체 분석](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md). **선정된 표본만 100%**이고 바닐라·인게임·Macaw·전체 모드 전수는 미검증. 5개 작업 **최종 완료 0/5**.


- 이전 v18: [Another Furniture 원본 모델 63개·807면 텍스처 경로·신규 PNG 12종 직접 픽셀 분석](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md), 24/53 참조된 모드 PNG 경로 실화소(45.28%). 이 표본 검증률은 **전체 프로젝트 완료율이 아니다**. 전체 확정 완료 0/5.

- 이전 v17: [고정 원본 PNG 24종과 Handcrafted 면별 784/784 RGBA 분석](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md). **표본 목표 100%**이지만 공식 client.jar/인게임/타 모드 전수는 미완료. **전체 5개 단계 최종 완료 0/5**.

- 이전 v16: [원본 12 PNG/30 JSON/786 면 인스턴스 보고서](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md), 원본 PNG 누락 표본 해결. 남은 검증은 면 사각형 실제 화소 샘플링·바닐라 2면·게임 렌더. 5개 세부 작업 최종 완료 0/5.

- 이전 v15: [3D 모델 표현 방식 정량 비교](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md), 189모델·Handcrafted 22개 경로 그룹 신규 파생 통계. 면 선언 수는 최종 렌더 면이 아니며 bbox도 충돌체가 아님. 원본 자산 직접 검증 보류 상태 유지.

- 이전 v14: [텍스처 슬롯 바인딩 분석](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md) / [51건 CSV](research/furniture_mods/v14/handcrafted_texture_bindings_51.csv) / [기계판독 JSON](research/furniture_mods/v14/v14_binding_audit_summary.json). 이후 작업은 원본 face→PNG 검증.

- 최신: [v13 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md) · PNG 24/24 실화소·UV 13모델/571면 검사 완료(표본), 미완료는 재질의 실제 face 연결 및 인게임 검증.
- 이전: [v12 보고서](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md), [전체 120종 구조표](research/furniture_mods/v12/handcrafted_authored_120_total.csv), [5쌍 비교](research/furniture_mods/v12/another_vs_handcrafted_5_category_pairs.csv).
- 원본 모드 버전은 바닐라 1.21.11과 **상이**. 공식 클라이언트/인게임 검증을 완료 처리하지 않는다.
