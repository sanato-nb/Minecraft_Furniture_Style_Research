# 1-1-07 — 콘크리트·색면 전용 새 채팅 시작 프롬프트

너는 프로젝트 **Minecraft Furniture Style Research**의 상위 1단계 1-1 텍스처 연구 중 **오직 1-1-07 (콘크리트·색면)** 담당이다. 사용자가 이 프롬프트를 새 채팅에 붙여넣었다. **과거 채팅 내용을 알고 있다고 가정하지 말고 아래 GitHub 실파일을 직접 읽어서 작업을 이어가라.** 이것은 단순 계획서 작성 요청이 아니라, 가능한 범위에서 실제 원본을 읽고 증거 기반 분석·결과 저장을 해야 하는 작업이다.

**저장소:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research

**새 채팅에서 첫 번째로 반드시 읽을 파일(순서 유지):**

1. **본 단계 인수인계:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/HANDOFF.md
2. **본 단계 독립 상태 JSON:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/STATE.json
3. **본 단계 상세 A–G 및 정확한 텍스처 목록:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-07_콘크리트색면.md
4. **버전·병렬 충돌 금지 규칙:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md
5. **v4 실측 원본 150개 표본 CSV:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv
6. **전체 150개 번호 원장:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv

**고정 작업 범위:** 콘크리트·색면 **7개**(본 단계 STATE의 `items`에 각 `texture_id`, 원본 SHA-256, 경로가 보존되어 있다). A–G 작업 중 이미 v4/v35~v38 원본 근거가 검증된 범위를 먼저 재사용·교차 검사하고, 누락/검증 부족을 찾아 이번 채팅에서 직접 소스 JSON·PNG/픽셀/UV를 확인한다. '1-1-07' 밖의 단계로 자의적으로 확대하거나 원본 150개 중 다른 분류를 이 단계 완료량에 더하지 말라.

**이 단계 특화 D 검사:** D1 7색 콘크리트의 평균 RGB·명도·채도 / D2 미세 픽셀 분산과 단색 평면 경계 검사 / D3 가구 평면의 색상 사용 가설을 원본 관찰과 분리.

**정확한 독립 버전:** `TEX07-R000`은 초기 **작업 계획 상태**다. 실제 신규 근거와 결과물을 처음 커밋할 때 `TEX07-R001`, 이후 `TEX07-R002`, `TEX07-R003`으로 자기 단계에서만 증가한다. 이 작업에 **`v32`·`v39`처럼 과거 프로젝트와 겹치는 단독 vNN을 절대 붙이지 않는다.** 다음 번호는 매번 GitHub `STATE.json`을 다시 읽고 검증하라. 결과물은 `research/vanilla_textures/by_stage/1-1-07/TEX07-R001/` 형태의 단계 전용 불변 폴더에 저장하라.

**쓰기 경계:** 이 단계의 `docs/vanilla_texture_1-1/stages/1-1-07/HANDOFF.md`, `docs/vanilla_texture_1-1/stages/1-1-07/STATE.json`, 단계 자체의 새 결과 폴더만 갱신한다. 저장소 루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json` 및 다른 단계 `1-1-xx` 폴더를 수정하지 말라. 공식 전체 버전은 현재 `v38` 그대로 유지. 같은 단계를 동시에 진행하는 다른 채팅이 있다면 편집 전 SHA와 버전 충돌을 먼저 검사하고 덮어쓰지 말라.

**검증 경계:** 레거시 v4에서 선정 표본 측정 기록 7/7이 이미 있어도 새 A–G 실측/공식 검증이 전부 끝났다는 뜻은 아니다. 직접 관찰한 원본 데이터와 과거 기록을 구분하고, 비공식 추출 미러 SHA/PNG와 Mojang 공식 `client.jar`의 인증을 절대 혼동하지 말라. 공식 JAR이나 인게임 정적 장면에 접근할 수 없으면 솔직히 미검증으로 남겨라. 애니메이션 프레임·키프레임·움직임 연구는 **사용자의 해제 지시 전까지 전면 보류**한다. 기존 동적 조사 기록은 삭제하지 않는다. Project Zomboid 변환 및 실제 가구 3D 모델 제작도 이 연구 범위가 아니다.

**즉시 수행할 일:** 인수인계·상태·번호별 상세 작업표를 읽고, 기록상 미완료/증거가 취약한 파일부터 A→G 순서로 최대한 **실제 분석**하여 이 단계의 고유 버전으로 GitHub에 출처/파일별 결과·보고서·새 인수인계 상태를 저장한다. 마무리 답변은 이번 검증한 파일 수, 실제 PNG·RGBA·UV 근거, 미검증 범위, 작성 커밋과 다음 `TEX07-Rxxx` 번호를 정확히 구분하여 보고한다.
