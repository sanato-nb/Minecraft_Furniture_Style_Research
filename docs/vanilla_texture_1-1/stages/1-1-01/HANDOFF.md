# 1-1-01 목재·원목 전용 인수인계 — TEX01-R005

## TEX01-R005 새 분석과 다음 단계 (2026-11-13)

원본 18 PNG SHA/PNG 청크 CRC 다시 확인. 기존 원본 픽셀 4,608개에 대해 **d=2/4/8 총 19,584 픽셀쌍의 새 RGB 공간대비** 분석 완료(새 고유 픽셀 수 0). 18개 사용자 제공 소스 JSON 재조회(기존 R001 43개 중 재검사). 원목 4종 × 3 blockstate 축 × 6면 = **72개 JSON 회전 행렬 기반 로컬→월드 면 투영** 신설. 수평 `up` 180° 로컬 UV 8면 중 범위 내 2면. 원래 R004 132면 RGB·792조회는 **계승만** 하며 새로 적립하지 않음.

- [신규 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R005/REPORT.md) · [18 PNG 2/4/8 거리측정 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R005/PNG_SPATIAL_LAG_METRICS.csv)
- [72 로컬→월드 면 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R005/MODEL_AXIS_WORLD_FACE_MAP.csv) · [직접 재조회 JSON 18개 SHA](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R005/SOURCE_JSON_AUDIT.csv) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R005/SUMMARY.json)

**F 미완료:** 실제 Minecraft 인게임 정적 검증 0/18. 수학적 면 투영·소스 텍셀 비교를 인게임 화면 검증으로 승격하지 말 것. 공식 Mojang JAR 전체 인증은 사용자 요청으로 범위 제외(인증 성공 아님). `TEX01-R006`은 신규 실측 근거를 확보한 경우에만 사용. 애니메이션·좀보이드·가구 3D 제작 제외. 이 단계 이외 STATE/HANDOFF 및 전역 v38 수정 금지.

현재 TEX01-R005, 다음 TEX01-R006. 아래 R004 지시는 역사 기록으로 보존. 기존 글로벌 v38 변경 금지. R001/R002/R003 원본·CSV·커밋 불변. 18 목재 PNG 고정.

## 핵심 출처/검증

사용자 GitHub 1.21.11/은 사용자가 직접 Minecraft Java 1.21.11 JAR을 압축 해제한 사용자 제공 자료. R001에서 18 PNG SHA/CRC/RGBA, 43 정적 모델 JSON을 그 경로에서 직접 검증했다. 미러 v4 기록 SHA와 18개 일치하지만 독립 미러 바이너리 비교 0. **공식 Mojang JAR 인증은 사용자 요청으로 연구 필수 항목에서 제외함.** 실제 게임 정적 렌더 검증은 0/18(미검증)으로 유지.

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

## R004 당시의 후속 지시 (역사 기록)

재진입 시 1-1-01 STATE.json 현재/다음 버전, SHA, main HEAD, 새 R005 폴더 존재 여부 확인. R001~R004 중복 완료량 적립 금지. A–G 절차의 F는 **인게임 정적 검증만** 해당하며, 공식 Mojang JAR SHA1/size 인증은 수행하거나 요구하지 않음. 실제 인게임 정적 장면 검증은 증거 확보 전 0 유지. 블록/월드 UV는 별도 소스 근거가 없으면 가정 금지. 사용자 JAR 추출본 최우선. R005 결과만 신규 폴더에 저장. 이 단계 HANDOFF.md, STATE.json만 갱신. 루트 HANDOFF.md/PROGRESS.md/handoff/STATE.json, v38, 다른 재질 1-1-nn 수정 금지. 애니메이션/PZ/실제 가구 3D 제작 보류.

## 연구 범위 변경 — 공식 인증 제외 (2026-11-13)

사용자 지시 **"공식 인증 빼"**에 따라 이 단계의 공식 Mojang client.jar 전체 SHA-1·다운로드 메타데이터 비교를 **검증 조건, 남은 작업, 완료 기준에서 제외**한다. 향후 보고서에서 공식 인증 진행률을 반복 표기하지 않는다. **과거 R001~R004 보고서의 역사적 숫자와 커밋은 그대로 보존**하고, 현재 상태는 새 연구 실측 없이 운용 규칙만 수정했으므로 버전 번호를 올리지 않는다.

현재 연구 검증 범위: (1) **사용자 제공 `1.21.11/` 추출본** PNG·JSON·색상·UV·blockstate 직접 검사, (2) 필요시 **기존 미러 기록과 해시 대조**(독립 미러 바이너리 검증과 구분), (3) **인게임 정적 렌더** 실제 장면이 있을 경우 확인. 애니메이션·좀보이드 변환·실제 가구 모델 제작은 계속 보류.

