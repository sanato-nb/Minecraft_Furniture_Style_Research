# 1-1-01 — 목재·원목 전용 인수인계 (TEX01-R001)

> Minecraft Java 1.21.11 · **현재 TEX01-R001 / 다음 TEX01-R002** · 전체 통합 버전 **v38 변경 없음**. 이전 TEX01-R000은 계획 상태였으며 검증 완료판이 아니다.

## 이번 신규 직접 검증

- 고정 18개 원본 PNG: SHA-256/v4 비교 **18/18 일치**, 실제 PNG chunk CRC32·IDAT zlib·Pillow RGBA **18/18 통과**. 16×16 PNG 18개에서 **4,608 RGBA 픽셀 전부 불투명**. Git blob SHA-1과 PNG SHA-256을 `SOURCE_LEDGER.csv`에서 구분.
- **A 완료**, **B 완료**, **C 완료**. **D1 6개 조합 직접 비교(다른 종 단면 미검증)**, **D2 18 PNG 직접 검사**, **D3 18개 텍스처 정적 모델 연결**. **E 원본 정적 JSON 43개 확인, 로컬 모델면 150건**. **F 공식 client.jar 0/18, 인게임 정적 0/18**. **G TEX01-R001 결과 저장**.
- 원목 `axis=x/y/z` 모델을 검토했지만, 모델면 **150건 중 고정 범위 내 텍스처 참조 132건**만 연구 대상에 산입하고, 다른 종 단면 파일 참조 18건은 *외부 의존성*으로만 기록. `cube`의 UV는 implicit 16×16, 가로 원목 로컬 up 면 rotation=180°는 명시 근거.
- oak, spruce, birch 판자와 원목 옆면 밝기 차이 비교. `birch_log`는 다른 원목처럼 V/H<1이 아니므로 **결 방향 자동 추론의 예외**. 이음새 숫자는 실제 렌더 인증이 아님.
- v38의 `oak_shelf` → `stripped_oak_log` `#particle` **기하 면 0회** 기록을 보존. 이 단계에 선반 신규 분석량 추가 금지.

## 전용 결과 (불변 TEX01-R001)

- [REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/REPORT.md)
- [SOURCE_LEDGER.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/SOURCE_LEDGER.csv)
- [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/SUMMARY.json)
- [D1_COMPARISONS.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/D1_COMPARISONS.csv)
- [MODEL_UV_FACE_MAP.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/MODEL_UV_FACE_MAP.csv)
- [SOURCE_JSON_SHA_MANIFEST.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/SOURCE_JSON_SHA_MANIFEST.csv)

## 18개 고정 범위

- `1-1-01-001` `oak_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-002` `spruce_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-003` `birch_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-004` `dark_oak_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-005` `cherry_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-006` `mangrove_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-007` `acacia_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-008` `jungle_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-009` `bamboo_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-010` `pale_oak_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-011` `crimson_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-012` `warped_planks`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-013` `oak_log`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-014` `spruce_log`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-015` `birch_log`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-016` `oak_log_top`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-017` `stripped_oak_log`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기
- `1-1-01-018` `bamboo_mosaic`: 추출 PNG SHA/CRC/RGBA 및 정적 모델 연결 완료 / 공식 JAR·게임 렌더 대기

## 다음 채팅 우선순위

1. **먼저 [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/STATE.json) 재조회**해 `current_revision`, `next_revision`, 상태 SHA와 main HEAD를 검사하고 충돌 시 덮어쓰기 금지. 동일 단계 병렬 편집 피함.
2. [REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/REPORT.md)와 [18 PNG 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/SOURCE_LEDGER.csv) 및 [면별 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/MODEL_UV_FACE_MAP.csv)을 재사용. 정적 실측을 새 완료량으로 중복 계산하지 말 것.
3. 공식 Mojang 1.21.11 `client.jar` 인증과 인게임 정적 장면 검증 근거가 확보되는 경우에만 F 승인. 신규 근거가 없으면 정확히 **pending**.
4. 신규 분석이 있을 때만 `research/vanilla_textures/by_stage/1-1-01/TEX01-R002/`로 진행. `TEX01-R001` 불변. **루트 HANDOFF.md, PROGRESS.md, handoff/STATE.json 및 다른 단계 쓰기 금지.**
5. **애니메이션·프레임·움직임 보류**. 기존 동적 조사 삭제 금지. 실제 3D 가구 제작, Project Zomboid 변환은 범위 밖.

고정 목록 [1-1-01 A–G 원본 계획](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-01_%EB%AA%A9%EC%9E%AC%EC%9B%90%EB%AA%A9.md) · [버전 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
