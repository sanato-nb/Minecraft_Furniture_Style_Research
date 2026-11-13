# 1-1-01 목재·원목 전용 인수인계 — TEX01-R004

현재 TEX01-R004, 다음 TEX01-R005. 기존 글로벌 v38 변경 금지. R001/R002/R003 원본·CSV·커밋 불변. 18 목재 PNG 고정.

## 핵심 출처/검증

사용자 GitHub 1.21.11/은 사용자가 직접 Minecraft Java 1.21.11 JAR을 압축 해제한 사용자 제공 자료. R001에서 18 PNG SHA/CRC/RGBA, 43 정적 모델 JSON을 그 경로에서 직접 검증했다. 미러 v4 기록 SHA와 18개 일치하지만 독립 미러 바이너리 비교 0. Mojang 공식 JAR SHA1 인증 0/18, 실제 게임 렌더 0/18 — 서로 다른 검증 수준.

## 이번 R004 신규 분석

- 원본 18 PNG를 R001 SHA 기반으로 재확인하고 RGB 최초 등장 클래스 라벨을 16×16 전 픽셀에 적용한 **구조 차이 위치 분석**. 9종 판자 256/256 공통 패턴, mangrove 254/256(12,14 및 13,14 다름), acacia 252/256(9,8·1,12·11,12·11,13 다름), bamboo 20/256(236 다름). 공통 9종 정확 RGB 팔레트 대응표 **63건**. oak_log와 spruce_log도 256/256 동일한 구조 클래스를 가짐.
- 기존 R001 정적 로컬면 **150개 재사용**, 이 중 고정 18 PNG 연결 **132면**에 샘플 6개씩 **792 면별 RGB 결합**. 이는 신규 모델면 수나 새 고유 픽셀 수가 아님. 직접 본 원본 PNG의 6좌표 × 18 = **108 좌표색**에 근거. 고정 외부 단면 **18면 무샘플**.
- 모델 JSON 명시 UV rotation180 8면 중 2면(oak_log_top)은 범위 내라 180도 로컬 UV 좌표로 RGB 변환. 나머지 6면 범위 밖이라 RGB 생략. 축별 blockstate 회전값은 별도 저장. 엔진 최종 월드 UV/인게임 정적 렌더 확인 아님.

## R004 새 불변 산출물

- [REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R004/REPORT.md)
- [SOURCE_LEDGER.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R004/SOURCE_LEDGER.csv)
- [CANONICAL_PLANK_RGB_LUT.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R004/CANONICAL_PLANK_RGB_LUT.csv)
- [ANCHOR_SOURCE_RGB.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R004/ANCHOR_SOURCE_RGB.json)
- [MODEL_FACE_PIXEL_ANCHORS.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R004/MODEL_FACE_PIXEL_ANCHORS.csv)
- [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R004/SUMMARY.json)

## 다음 TEX01-R005

재진입 시 1-1-01 STATE.json 현재/다음 버전, SHA, main HEAD, 새 R005 폴더 존재 여부 확인. R001~R004 중복 완료량 적립 금지. A–G 절차 준수. Mojang 공식 전체 JAR SHA1/size 인증과 실제 인게임 정적 장면 검증은 각각 증거 확보 전 0 유지. 블록/월드 UV는 별도 소스 근거가 없으면 가정 금지. 사용자 JAR 추출본 최우선. R005 결과만 신규 폴더에 저장. 이 단계 HANDOFF.md, STATE.json만 갱신. 루트 HANDOFF.md/PROGRESS.md/handoff/STATE.json, v38, 다른 재질 1-1-nn 수정 금지. 애니메이션/PZ/실제 가구 3D 제작 보류.
