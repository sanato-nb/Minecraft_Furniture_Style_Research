# 1-1-03 금속·금속부품 — 별도 새 채팅용 실행 프롬프트

이 메시지는 프로젝트 **Minecraft Furniture Style Research**의 `1-1-03` (**금속·금속부품 16개 PNG**) 단계 연구를 **새 채팅에서 실제로 이어서 수행**하도록 하는 지시다. 계획을 다시 만들거나 완료한 작업을 반복하는 것이 아니라, GitHub에 축적된 결과를 확인하고 검증이 덜 된 정적 소스 연구를 이어가라.

저장소: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research

**가장 먼저 아래 파일을 차례로 직접 읽고 상태를 확인하라.**

1. 읽기 전용 재진입 인수인계 스냅샷: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/REENTRY_2026-11-13_R004_R006/1-1-03/HANDOFF_SNAPSHOT.md
2. **반드시 실시간으로 다시 조회할** 본 단계 `STATE.json`: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-03/STATE.json
3. **반드시 실시간으로 다시 조회할** 본 단계 `HANDOFF.md`: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-03/HANDOFF.md
4. 본 단계 A–G 세부 작업표와 원본 대상: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-03_금속금속부품.md
5. 현재 `STATE.json`에 적힌 마지막 `TEXnn-Rxxx` 결과 `REPORT.md`, `SUMMARY.json`, CSV (경로는 GitHub에서 직접 재확인).

스냅샷을 만들 당시 상태는 **현재 `TEX03-R004` / 다음 `TEX03-R005`**였고, 이 단계의 고정 표본은 16개다. **이 버전은 예시가 아니라 조회 당시의 실제 상태이지만, 새 채팅 시점에는 반드시 GitHub STATE의 더 최신 값으로 대체**하라. `v38`은 전체 프로젝트 역사적 체크포인트이고 각 `TEXnn-Rxxx`와 다른 이름 공간이다. 단독 `v39`, `v40` 등을 이 채팅의 독립 릴리스 번호로 사용하지 말라.

**기존 연구 근거(중복 가산 금지):** 16 PNG/4,096 RGBA·정적 블록상태 63개·상태×모델 면 406건의 분석, 145 원본 면 UV 기록 유지. 이 근거를 읽고, 아직 소스 경로/UV/상태/정적 이미지의 확인이 부족한 항목을 찾아 실제 원본 PNG·JSON을 직접 분석하라.

**이 단계에서 우선할 다음 조사:** 금속문·철 다락문·모루/구리 계열의 각 상태에 따른 투명 픽셀 사용 위치·반전·표시 면을 소스 기준으로 추가 검증.

**업데이트된 검증 범위:** 사용자가 자신의 Minecraft Java 1.21.11 게임 JAR을 압축 해제한 `1.21.11/` 폴더를 GitHub에 제공했다. 이를 **사용자 제공 1차 자료**로 직접 읽고, 비공식 추출 미러는 필요할 때만 교차 검증에 사용하라. SHA/PNG CRC/RGBA, model JSON parent·elements·faces·UV, blockstates, 색상·패턴·정적 상태를 증거 기반으로 다루라. **Mojang 공식 client.jar 전체 SHA-1/공식 메타데이터 인증은 사용자 지시로 연구 필수 항목과 완료 분모에서 제외**한다. 이는 공식 인증 성공을 뜻하지 않는다. **인게임 정적 렌더링**은 실제 게임/스크린샷/실측의 증거가 있을 때만 완료로 표시하고, 소스 투영만으로 게임 화면을 인증하지 마라.

**애니메이션 분석 전면 보류**, 기존 애니메이션 기록은 삭제하지 않는다. Project Zomboid 변환이나 실제 가구 3D 모델 제작도 하지 않는다.

**서로 다른 채팅과 GitHub 충돌 방지:**
- 이 채팅은 **오직 `1-1-03` 단계**만 연구. 다른 1-1 단계의 STATE/HANDOFF, 루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`, 전체 `v38`을 수정하지 말라.
- 새로운 실측/검증 결과가 있을 때만 GitHub의 라이브 `next_revision`을 읽고 `research/vanilla_textures/by_stage/1-1-03/<next_revision>/`에 불변 결과물 작성. 기존 Rxxx 결과를 덮어쓰거나 다른 단계 버전을 공용으로 사용하지 마라.
- 쓰기 직전 `main` HEAD, 현재 `STATE.json` blob SHA, `next_revision` 폴더 미존재를 다시 확인. 경합이 있으면 재조회하고 충돌 없는 다음 릴리스에서 계속하라. 결과 파일(보고서·CSV·요약 JSON)과 **이 단계**의 라이브 `HANDOFF.md`, `STATE.json`만 갱신.
- 새로 확인한 파일 수·픽셀/UV 측정 수, 과거 자료에서 계승한 수, 아직 미검증인 인게임 시각 자료를 정확히 구분. **검증 근거가 없는 항목을 완료로 주장하거나 연구를 계획만 세우고 실제 조사한 것처럼 보고하지 마라.**

**지금 바로** GitHub 최신 STATE/HANDOFF와 최신 릴리스를 읽고, 새로운 정적 텍스처·기하·UV·상태 분석을 실행 가능한 범위에서 수행한 뒤 단계 전용 다음 버전에만 저장해라. 새 근거가 없는 경우 버전을 올리지 말고 확인한 한계와 후속 검증 과제를 구체적으로 보고해라.
