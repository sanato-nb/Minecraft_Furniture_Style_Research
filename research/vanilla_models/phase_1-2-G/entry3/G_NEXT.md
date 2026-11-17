# 1-2-G Entry3 종료 PASS — Entry4 착수 허용, 아직 미착수

2026-11-17 기준. 사용자 추출 Minecraft Java 1.21.11 원본 **945개 = model JSON 495 + blockstate JSON 265 + PNG 185** 실제 bytes 확보·Git blob SHA 재계산 **945/945**. GitHub Actions [실행 기록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44071021479) **success**; [원본 독립 감사](G_ENTRY3_INDEPENDENT_RECOUNT.json) 오류 **0건**; [원격 검산](G_ENTRY3_REMOTE_READBACK.json)에서 주요 원장 Git blob SHA·행수·원문 재조회 PASS.

- 모델: 일반 기하 **495**, E 특수 예외 **0**. 상속 부모 원문과 F 부모 체인 SHA 비교 일치. 요소 **971**, face **4,662**, UV 명시 **4,348**, 비명시 **314**, PNG binding face **4,328**, 템플릿 미바인딩 **334**. 미바인딩에 임의 PNG를 할당하지 않음.
- blockstate 265: D 원본 선택 옵션 **1,573**, 서로 다른 참조 모델 경로 **479**. variants/multipart 원문, 적용 모델, 선택 인덱스, 조건·x/y/uvlock/weight 명시 여부 검산. **6건의 기본 multipart는 `when` 생략과 이전 D `{}` 조건을 동일한 무조건 규칙으로 정규화**하고 [정정 이력](G_ENTRY3_CONDITION_ERRATA.md)을 보존. 기존 D 원장 파일은 변경하지 않음.
- PNG 185: Git SHA·실제 PNG signature·Pillow full decode·RGBA SHA256, C 과거 RGBA 검증 **181/181 일치**, C 범위 밖 **4종은 새 G 검증으로만 인정**. 실제 원본 총 **62,873 bytes**. mcmeta 13종 원본 JSON 판독(애니메이션 9종 정적 메타); F 선행 시각자료 연결 42종(신규 육안 검수 아님).
- 원격 증거: G_ENTRY3_SOURCE_IDENTITY_945.csv(945행), G_ENTRY3_MODEL_GEOMETRY_RECOUNT.csv(495행), G_ENTRY3_D_ORIGINAL_OPTIONS.csv(1,573행), G_ENTRY3_PNG_BINARY_AUDIT.csv(185행), G_ENTRY3_ORIGINAL_FACES_00/01/02.csv(2,200+2,200+262행), G_ENTRY3_INDEPENDENT_RECOUNT.json 및 최종 보고.
- 누적 G 승인 Entry **3/6**, 원본 직접 내용 검증 **2,067/4,669 = 44.27%**, 잔여 2,602. 글로벌 최종 G1~G6 **0/6**, G 전체·상위 1-2 미완료. A~F/v69 기존 자료, 승인150/150 및 상위 1/5 보존. Entry7 없음.

**다음 작업:** 정해진 `research/vanilla_models/phase_1-2-G/entry4/G_ENTRY4_QUEUE_944.csv`의 **944개 = model JSON 494 + blockstate JSON 265 + PNG 185** 원본만 조사한다. 실제 bytes/Git SHA 직접 확인, F/C/D/E 출처 독립 대조, 전체 PNG pixel/metadata 검증, 미결정 소관 보존, 독립 재집계와 GitHub 원격 readback을 마친 다음에만 Entry4를 승인할 수 있다. Entry1~3의 기존 실적은 중복 계산 금지.

**범위 한계:** 공식 Minecraft 배포 JAR, 게임 내 등록 state/renderer, 애니메이션 재생, 좀보이드 가구의 실제 정체/물리 재질/마크 맵 제작을 검증했다고 주장하지 않는다.
