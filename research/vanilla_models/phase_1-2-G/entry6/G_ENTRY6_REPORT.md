# 1-2-G Entry6 — 원본 829개 직접 소스 감사

GitHub Actions 체크아웃의 Minecraft Java 1.21.11 사용자 추출 파일 bytes로 검증.
**Entry6 판정: 소스 감사 PASS (원격 readback·단계 승인 별도)**

## 원본 조사 수량
- 직접 파일 원본/해시: 829 / 829
- 모델 JSON: 378 / 378
- blockstate JSON: 265 / 265
- PNG 해시/디코드/RGBA: 186 / 186
- 모델 요소 661, face 2412 (원본 재계산)
- D 원문 선택: 1836, 서로 다른 참조 모델 522
- 선행 C PNG RGBA 일치 182 / C 외 G 신규 4
- mcmeta 12, 정적 애니메이션 메타 7
- 선행 F 시각 관찰 증거 연결 135 (이번 G의 신규 육안 관찰은 아님)
- 기록된 오류 0개
- 선행 F 원장의 공유 부모 SHA 누락 보완 증거 4 필드 (원본 소급 수정 금지)

## 한계
- 공식 JAR 인증·게임 렌더·state registry·애니메이션 재생은 범위 외 미검증.
- E 특수 renderer, C 템플릿 미바인딩은 소관별로 계속 기록. PNG 내용 검증은 물체 정체/재질 확정이 아님.
- **전체 G 게이트 G1~G6는 계속 0/6이며 Entry6은 마지막 회차이며 G 글로벌 종료 게이트 G1~G6 별도 통과 전 G 전체 완료 선언 금지.**
- A~F/v69 파일 변경 없음. 현 시점 글로벌 G 진행은 Entry1~Entry5 승인 3,840/4,669 + Entry6 실검증별도.

## 생성한 근거
G_ENTRY6_SOURCE_IDENTITY_829.csv, G_ENTRY6_MODEL_GEOMETRY_RECOUNT.csv, G_ENTRY6_D_ORIGINAL_OPTIONS.csv, G_ENTRY6_PNG_BINARY_AUDIT.csv, G_ENTRY6_ORIGINAL_FACES_*.csv, G_ENTRY6_INDEPENDENT_RECOUNT.json.
