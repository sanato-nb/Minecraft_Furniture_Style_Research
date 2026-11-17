# 1-2-G Entry3 — 원본 945개 직접 소스 감사

GitHub Actions 체크아웃의 Minecraft Java 1.21.11 사용자 추출 파일 bytes로 검증.
**Entry3 판정: 소스 감사 PASS (원격 readback·단계 승인 별도)**

## 원본 조사 수량
- 직접 파일 원본/해시: 945 / 945
- 모델 JSON: 495 / 495
- blockstate JSON: 265 / 265
- PNG 해시/디코드/RGBA: 185 / 185
- 모델 요소 971, face 4662 (원본 재계산)
- D 원문 선택: 1573, 서로 다른 참조 모델 479
- 선행 C PNG RGBA 일치 181 / C 외 G 신규 4
- mcmeta 13, 정적 애니메이션 메타 9
- 선행 F 시각 관찰 증거 연결 42 (이번 G의 신규 육안 관찰은 아님)
- 기록된 오류 0개

## 한계
- 공식 JAR 인증·게임 렌더·state registry·애니메이션 재생은 범위 외 미검증.
- E 특수 renderer, C 템플릿 미바인딩은 소관별로 계속 기록. PNG 내용 검증은 물체 정체/재질 확정이 아님.
- **전체 G 게이트 G1~G6는 계속 0/6이며 Entry4는 Entry3 원격 승인 이전 시작 금지.**
- A~F/v69 파일 변경 없음. 현 시점 글로벌 G 진행은 Entry1+Entry2 승인 1,122/4,669 + Entry3 실검증별도.

## 생성한 근거
G_ENTRY3_SOURCE_IDENTITY_945.csv, G_ENTRY3_MODEL_GEOMETRY_RECOUNT.csv, G_ENTRY3_D_ORIGINAL_OPTIONS.csv, G_ENTRY3_PNG_BINARY_AUDIT.csv, G_ENTRY3_ORIGINAL_FACES_*.csv, G_ENTRY3_INDEPENDENT_RECOUNT.json.
