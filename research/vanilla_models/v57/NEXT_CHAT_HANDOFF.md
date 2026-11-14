# v57 다음 채팅 연구 인수인계 — Minecraft Furniture Style 1-2-A

1. GitHub `main` 최신 HEAD부터 실제 조회. v58 이상 있으면 최신 우선. `research/vanilla_models/v57/REPORT.md`, `SUMMARY.json`, `VALIDATION_POST_RESEARCH_COMMIT.json`, `07_P1_544_EVIDENCE_LEDGER.csv`를 읽어 시작.
2. v57 원장 **544행×225열**. v56의 209열, 이전 v55의 198열 모든 기존 데이터 동일. 새 16열은 이번 16개 모델의 직접 재검증만 표시, 528개는 빈칸. 원본 경로·SHA 544/544는 소스 식별 수치.
3. P1 v53 신규175 코호트를 피해서 기존 나머지369 모델 중 16개를 실제 JSON 재검증. 원본 자체 33요소/156면과 상속 적용 44요소/219면 구분; 명시UV95/기하 계산 UV 후보124 분리. 모델·부모 원문+SHA는 `00A_`, `00B_`, 종합 원장은 `01_`, 면별은 `02_`.
4. 별도 `03_BLOCKSTATES_13.json`: 원본 JSON+Git SHA 13개, variants37, multipart68, apply105. 엔진 상태 선택/회전 공식 인증 아님.
5. 별도 P1 소스 텍스처 4 PNG를 Python Pillow로 독립 Git SHA1/SHA256/RGBA 전픽셀 **1,536픽셀** 대조. `stonecutter_saw.png` 원본 16×48, 상단 frame 명시 UV 2면 반복 196 소스 픽셀(164 opaque, 32 투명), distinct98. 이것은 게임 엔진의 UV 방향·애니메이션 프레임 출력 검증이 아님.
6. 셜커 lid/base와 일반 skull 기본 기하 단서는 제3자 1.21.11 디컴파일 코드에서 확인. `09_SECONDARY_RENDERER_JAVA_EVIDENCE.json`에 외부 경로/SHA. 공식 original client jar/런타임 검증이 없으므로 14 렌더러 미해결 유지.
7. v54~v56 이전 175 코호트 PNG 49경로/face3393/관측51228는 재검사하거나 신규 수치로 합산하지 말 것. 기존 케이크 UV 계산 후보168도 원본 명시로 바꾸지 말 것. 다음 목표는 369모델의 미측정 텍스처 실사, 암시 UV 엔진 구현, 머리종류별 렌더러, 역사 의미론 통합.
8. 1-1 150/150 완료와 전체 상위 1/5 완료 유지. 1-2-A/1-2 미완료·완료율 미산정, 마인크래프트 가구 제작·PZ 변환 금지. commit 전 HEAD 재검사, commit 후 GitHub readback 검증 필수.
