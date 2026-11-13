# 1-1-01 목재·원목 전용 인수인계 — TEX01-R007

## TEX01-R007 — D1 옆면·단면 비교 4수종 4/4 완료 (2026-11-13; 사용자 범위 확장)

사용자 지시 **「확장해서해줘」**에 따라 이전의 고정 18개 PNG 옆면 원목 4종(`oak`, `spruce`, `birch`, `stripped_oak`) 중 누락된 **보조 단면 PNG 3개**(`spruce_log_top`, `birch_log_top`, `stripped_oak_log_top`)를 추가 분석했다. 원래 18 PNG 표본과 R001–R006 리비전은 그대로 보존한다. 보조 원본 3개만 신규 고유 PNG/768 RGBA 텍셀로 계산하며, 기존 표본 5개 재측정은 신규로 중복 가산하지 않는다.

- 8개 원본 PNG 전체 SHA256/CRC/16×16 RGBA/불투명 검사 완료(32 PNG 청크). 원목 4쌍의 평균 Y(Rec.709 RGB 코드값 가중합)·S·표준편차·H/V 1픽셀 대조·동좌표 RGB 차이 256×4쌍을 직접 계산. **단면−옆면 Y 차이:** 참나무 **+36.7351**, 가문비 **+43.3348**, 자작 **−35.8294**, 껍질 벗긴 참나무 **−14.6445**. 단면이 늘 밝지는 않음.
- 4종의 원본 블록상태, 세로/가로 원목 모델 JSON, 2개 공통 템플릿을 재확인. `#end` ↔ `*_log_top`, `#side` ↔ `*_log`, `axis=x/y/z` 모델 선택, 수평 모델 로컬 up UV 180° 연결도 검증. 모든 JSON은 이전 정적 연구와 중복이므로 신규 고유 JSON 개수 **0**.
- 단면 전체 180° 회전 불일치 픽셀은 oak 100, spruce 98, birch 108, stripped oak 92. 이는 소스 PNG 변환이며 최종 게임 모델 베이크/인게임 장면 인증이 아님.
- **D1 확장 상태: 원래 원목 옆면 4종의 단면 4/4 직접 비교 완료.** 원목 종류를 무한 확장해 조사한 것은 아님. 인게임·공식 JAR 인증은 사용자 정책상 제외; 애니메이션·PZ·실제 3D 가구 제작 보류.
- [보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R007/REPORT.md) · [4쌍 측정 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R007/D1_SIDES_ENDS_4PAIRS.csv) · [PNG SHA/CRC 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R007/D1_SOURCE_PNG_LEDGER.csv) · [원본 모델 연결 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R007/D1_MODEL_END_SIDE_LINKS.csv) · [재현 Python](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R007/REPRODUCE_D1_SIDE_END.py) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R007/SUMMARY.json)
- 현재 버전 `TEX01-R007`, 다음 `TEX01-R008`; **현재 D1 확대 범위에서는 실질 분석 완료**, 새 자료나 새 분류 확대 지시 없이 '계속해줘'만 반복하면 더 분석하지 말고 멈춰 알려줄 것. 루트/타 단계/v38 불변.



## 최신 우선 작업 기준 — 인게임 검증 제외 (2026-11-13)

사용자 직접 지시: **"인게임 검증은 제외해줘 어차피 모델링이랑 텍스텨있는데 필요없을거같아"**. 따라서 이 단계 **1-1-01**에서는 **실제 Minecraft 게임을 실행하거나 정적 스크린샷을 제공할 필요가 없으며**, 그 결과를 완료 조건·잔여 작업·다음 리비전 필수 조건에서 **완전히 제외**한다. 기존 R001–R006에 기재된 `ingame_static_render_verified=0/18`은 검증하지 않았다는 **역사적 사실**일 뿐 **미완료 작업이나 남은 분모를 뜻하지 않는다**. 옛 보고서·측정치·리비전은 불변 기록으로 유지하며, 아래의 오래된 "인게임 F 미완료" 지시보다 이 최신 규칙이 우선한다.

**현재 인정하는 연구 근거:** 사용자 제공 Minecraft Java 1.21.11 추출본 `1.21.11/` 원본 PNG 바이트 SHA/CRC/RGBA/색상·무늬 정량 측정, 정적 모델 JSON 부모상속·blockstates·로컬 UV 연결, 소스에 근거한 수학 투영. **원본 소스 분석 완료를 실제 엔진 렌더/베이크 UV 인증으로 표현하면 안 된다.** 기존에 사용자 요청으로 제외한 공식 Mojang JAR 인증 또한 계속 범위 밖. 애니메이션·PZ 변환·실제 가구 3D 제작 및 범위 밖 다른 원목 단면 PNG 수집은 이번 단계에 포함하지 않는다.

**단계 상태:** 18/18 원본 PNG의 출처·바이너리·픽셀 분석 및 정적 JSON/UV 근거는 R001–R006에서 기록되어 있다. D1의 일부 다른 수종 단면 PNG는 고정 18개 밖이므로 이번 단계의 완료 장애가 아님. 이 결정은 **검증 범위 변경일 뿐 새로운 실험이 아니므로 TEX01-R006 유지, 다음 TEX01-R007 유지**. R007을 무리하게 만들지 말 것. 향후 사용자가 "계속해줘"라고 하더라도 소스 기준 추가 실질 작업이 없거나 사용자 도움이 필요하면 멈추고 사유를 알릴 것. **인게임 화면을 요청하지 말 것.**



## TEX01-R006: 18 PNG D4 변환 126조건과 원목 단면 UV 180° 전체 256픽셀 직접 검증 (2026-11-13)

- 원본 사용자 JAR 추출 PNG **18개** 바이트 SHA256/CRC 재검사 통과(72 PNG chunks). 기존 R001 4,608개 고유 RGBA는 재사용, 신규 고유 소스 PNG/픽셀 **0**.
- 18 PNG×7개 정적 회전·반사 변환 = **126 신규 비교**, 좌표쌍 RGB 검사 **32,256회**. 모든 PNG는 180° 회전과 완전 동일하지 않음(차이 100–256픽셀). 9개 표준 팔레트 재색칠 판자는 모두 220/256 변경.
- 실제 소스 `cube_column_horizontal.json`의 로컬 `up.rotation=180` 및 `oak_log_horizontal.json`의 `#end=oak_log_top` 재확인. `oak_log_top` 전체 16×16 **100픽셀/256 차이**, R004 6점 앵커에서는 중심 2점만 차이. 정확 비트마스크 보존. 이 결과는 **소스 텍셀 변환**이지 게임 최종 UV/인게임 인증이 아님.
- [연구 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R006/REPORT.md) · [18 PNG 전체 D4 방향표](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R006/PNG_D4_ORIENTATION_18.csv) · [참나무 단면 전체 차이 마스크](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R006/OAK_LOG_TOP_ROT180_MASK.json) · [재현 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R006/REPRODUCE_D4.py) · [수량 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R006/SUMMARY.json)
- **현재 TEX01-R006 / 다음 TEX01-R007**. 기존 R001–R005 불변. 인게임 정적 검증 **0/18**. 공식 JAR 인증은 완료 범위에서 제외(인증 성공 아님). 애니메이션·PZ 변환·실제 3D 가구 제작 보류. 다른 1-1 단계/전체 v38 파일 수정 금지.


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

