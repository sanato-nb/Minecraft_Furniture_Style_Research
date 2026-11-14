# v56 다음 채팅 연구 인수인계 (Minecraft Furniture Style 1-2-A)

1. GitHub `main` 최신 HEAD를 실제로 확인하고 `handoff/STATE.json`, `research/vanilla_models/v56/REPORT.md`, `SUMMARY.json`, `VALIDATION_POST_RESEARCH_COMMIT.json`, `07_P1_544_EVIDENCE_LEDGER.csv`부터 읽을 것. 새 v57+가 있으면 최신을 우선. 1MB 넘는 CSV 원장은 Git Blob API 또는 Contents 메타데이터의 blob SHA로 읽을 것.
2. 원본 모델 P1 544/544 typed SHA 신원 연결 유지; v56 544행·**209열** = v55의 198열 모든 이전 값 보존 + 신규 11열. 기존 v55 실적을 v56 신규 실적으로 중복 계산 금지.
3. v55의 신규 175모델과 연결된 원본 PNG **49개 경로** 중 이전 v54/v55에서 직접 UV 픽셀 대조한 **12개 보존**, 이번 v56에서 나머지 **37개 원본 바이너리를 직접 GitHub에서 읽고 독립 Git SHA1, PNG CRC32, DEFLATE/zlib Adler32, RGBA 전픽셀 검사**. v56 새 파일은 색상별 촛불26 + 양털11, 각각 16×16, 원본 실제 RGBA 9472픽셀. 검사 오류0.
4. v56 이번 직접 원본 **명시 UV 204개의 서로 다른 PNG 사각형**, **2,926개 모델 face 참조**, **21,416건 반복 포함 소스 RGBA 관측**, **중복 제거한 PNG+픽셀좌표 3,362개**, 측정된 face 범위 내 alpha255 21,416건. JS 재현 코드 `REPRODUCE_ORIGINAL_PNG_SOURCE_RGBA_AUDIT.js`는 원본 PNG bytes/Base64로 검사; v56 신규 37개를 Pillow로 별도 교차 검증하지 않았으며 게임 렌더 측정은 아님.
5. v54~v56 누적 해당 175모델: resolved texture path **49/49** 실제 UV 사각형 소스 PNG 픽셀 검사. **3,393개 resolved face refs 전부** 소스 픽셀 대조, 반복 포함 관측 **51,228**, 중복 제외 PNG 텍셀 좌표 **4,860**. 원본 명시 UV **3,225 face** / 케이크 원본에 UV 키가 없고 기하로 계산한 후보 **168 face**를 반드시 구분. 엔진 암시 UV 생성 공식 인증 미완료.
6. 신규 175모델 중 **159개**는 모든 해결된 면의 source PNG 픽셀 근거 있음. **2개는 추상 피스톤 부모 템플릿의 placeholder 20면**, **14개는 shulker13 + skull1의 renderer JSON geometry 미확인**. P1 544개 전체 3D/UV/PNG 연구 완료가 아님. v1~v55 역사적 의미론 근거 전수 통합도 아직 미완료.
7. 새로운 연구는 이전 결과 중복 계산 없이 P1의 다른 모델 369개 또는 P2/P3, renderer 구현 근거, 암시 UV 엔진 검증, 가구 스타일 형상 비례 규칙을 심화하는 방향으로 할 것.
8. **1-1 승인 150/150, 상위 1/5 완료 유지. 1-2-A·1-2 미완료, 전체 실질 완료율 미산정.** MC 가구 실물 모델 제작·PZ 변환 시작 금지. 커밋 직전에 최신 main HEAD 확인, 동시 변경이 있으면 덮어쓰지 말고 병합; 커밋 후 파일/544원장/SHA/메트릭 역검증.
