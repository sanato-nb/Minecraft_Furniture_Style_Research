# 1-1-03 금속·금속부품 — 독립 채팅 인수인계

**현재 단계 릴리스: TEX03-R001. 다음 후보: TEX03-R002. 전체 공통 버전: v38 변경 없음.** 2026-11-13 기준.

## 정확한 대상/신규 실측
- 고정 16개 텍스처의 기존 v4 데이터/150개 번호 원장과 재대조 16/16.
- GitHub **비공식 Minecraft Java 1.21.11 추출 미러**에서 PNG 16개를 **각각 직접 재수집**, 바이트 SHA256 **16/16 v4 일치**, 모든 PNG 청크 CRC / Pillow verify / RGBA 16×16 직접 검사 **16/16 통과**.
- 총 4096픽셀: 완전 불투명 3775, 완전 투명 321, 중간 알파 0. 알파 구멍은 copper_grate 77, iron_trapdoor 36, heavy_core 64, iron_door_top 48, anvil_top 96.
- 14개 blockstate JSON·연결 모델·부모 템플릿 확인: 정적 iron_door 32조합, iron_trapdoor 16조합, anvil 방향 4조합. 16개 텍스처 UV 사용 근거를 파일별 기록.
- **Mojang 공식 client.jar 인증 0/16, 인게임 정적 관찰 0/16.** 비공식 추출본을 공식 인증 자료로 주장하지 않음.

## 고유 불변 릴리스
[REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R001/REPORT.md) · [SOURCE_LEDGER.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R001/SOURCE_LEDGER.csv) · [MODEL_UV_STATE_LEDGER.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R001/MODEL_UV_STATE_LEDGER.csv) · [ALPHA_MASKS.txt](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R001/ALPHA_MASKS.txt) · [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R001/SUMMARY.json)

## A–G / 남은 일
- A–C: 16/16 출처와 실제 미러 PNG 바이너리/CRC/SHA/RGBA 재검증.
- D1 팔레트 계층, D2 철문·철다락문·격자·모루 알파/부품면, D3 블록상태별 정적 모델/텍스처 경로 조사: 미러 소스 수준 수행.
- E: 16개 텍스처의 모델/부모 템플릿/UV 직접 소스 연계 확인.
- F: **보류** 공식 JAR·인게임 정적 검사. G: 결과 및 전용 상태 갱신.
- 다음은 기존 R001 폴더를 수정하지 않고 STATE를 다시 읽어 신규 증거가 있는 경우에만 **TEX03-R002**. 공식 1.21.11 client.jar의 16개 PNG 해시 비교, 이후 정적인 게임 화면/투명/광택 교차 검증이 최우선.
- **애니메이션/키프레임/움직임 연구 전면 보류**, 기존 동적 조사 기록 삭제 금지. Project Zomboid 변환·실제 가구 제작 금지.
- **쓰기 경계:** 이 단계 HANDOFF/STATE와 단계 자체 새 결과 폴더만. 루트 HANDOFF.md, PROGRESS.md, handoff/STATE.json, 다른 1-1-xx 단계 수정 금지.

버전 정책: [ISOLATED_CHAT_VERSIONING.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md). 매 번 GitHub 최신 SHA/HEAD 검사, 동시 작업 충돌 시 덮어쓰기 금지.
