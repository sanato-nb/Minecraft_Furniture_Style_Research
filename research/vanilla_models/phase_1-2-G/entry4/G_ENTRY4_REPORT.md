> **2026-11-17 최종 승인: Entry4 PASS.** 고정 큐의 모델494+blockstate265+PNG185 = **944/944** 원본 bytes·Git SHA 직접 재검증, 기하·D·C·F 대조 오류0. [Actions 전체 감사](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44074106047) 성공, [독립 감사](G_ENTRY4_INDEPENDENT_RECOUNT.json) 및 [원격 SHA/행수/내용 readback](G_ENTRY4_REMOTE_READBACK.json) 통과. Entry5 진입 허용하되 아직 미착수. 전체 G 글로벌 G1~G6 종료 게이트는 **0/6**, 공식 JAR·게임 renderer 미인증.

# 1-2-G Entry4 — 원본 944개 직접 소스 감사

GitHub Actions 체크아웃의 Minecraft Java 1.21.11 사용자 추출 파일 bytes로 검증.
**Entry4 판정: PASS — 최종 원격 검산 및 단계별 원본 범위 승인**

## 원본 조사 수량
- 직접 파일 원본/해시: 944 / 944
- 모델 JSON: 494 / 494
- blockstate JSON: 265 / 265
- PNG 해시/디코드/RGBA: 185 / 185
- 모델 요소 1067, face 4811 (원본 재계산)
- D 원문 선택: 1496, 서로 다른 참조 모델 498
- 선행 C PNG RGBA 일치 180 / C 외 G 신규 5
- mcmeta 15, 정적 애니메이션 메타 3
- 선행 F 시각 관찰 증거 연결 37 (이번 G의 신규 육안 관찰은 아님)
- 기록된 오류 0개

## 한계
- 공식 JAR 인증·게임 렌더·state registry·애니메이션 재생은 범위 외 미검증.
- E 특수 renderer, C 템플릿 미바인딩은 소관별로 계속 기록. PNG 내용 검증은 물체 정체/재질 확정이 아님.
- **전체 G 게이트 G1~G6는 계속 0/6이며 Entry5는 Entry4 승인 후 별도 실행으로만 착수 허용.**
- A~F/v69 파일 변경 없음. Entry4까지 승인한 G 직접 원본 검증 **3,011/4,669 = 64.49%**, 잔여 1,658; 4/6 Entry 승인.

## 생성한 근거
G_ENTRY4_SOURCE_IDENTITY_944.csv, G_ENTRY4_MODEL_GEOMETRY_RECOUNT.csv, G_ENTRY4_D_ORIGINAL_OPTIONS.csv, G_ENTRY4_PNG_BINARY_AUDIT.csv, G_ENTRY4_ORIGINAL_FACES_*.csv, G_ENTRY4_INDEPENDENT_RECOUNT.json.

## 원본 독립 검산 및 범위 구분 상세
- **UV·PNG face:** 명시 UV **4,404**, 원문 UV 생략 **407**, face→PNG 바인딩 **4,355**, 템플릿 슬롯 미바인딩 **456**. 면 원장은 2,200+2,200+411행으로 실제 원격 보존. E 특수 renderer 소관 모델 0개(이 Entry에 배정 없음), 다른 Entry의 E 미인증 범위는 계속 유지.
- **D 265 blockstate:** 원본 선택 1,496개·고유 참조 모델 경로 498개. variants/multipart의 원본 적용 JSON, 조건, 대안, 명시 x/y/uvlock/weight를 이전 D 원장과 0차이로 정적 비교. 런타임 state registry는 미시험.
- **PNG 185개:** 원본 총 49,246 bytes. 원본 파일 SHA, PNG 시그니처·Pillow 전체 디코딩·RGBA SHA-256 증거 기록. C 과거 pixel 180개 모두 일치, C prior 범위 외 5개 G 신규 원본 근거로만 인정. mcmeta 15개 원문 메타데이터(애니메이션 3개 정적), F 이전 시각 관찰 37개는 재사용 증거이지 새로운 G 개별 이미지 의미 인증은 아님.
- **명시 미결정:** [G_ENTRY4_UNRESOLVED_SCOPE.csv](G_ENTRY4_UNRESOLVED_SCOPE.csv) **464행**, 이 중 미바인딩 face 456행과 과거 C 외 PNG5행, 선행 F 시각 범위1·런타임 인증1·애니메이션 재생1 범위 구분. **464행은 464개의 SHA 오류나 파손 파일을 의미하지 않음.**
- **최종 보호 검증:** GitHub 비교 검사에서 기존 A~F·v69 소스 변경 없음. 상태 기록의 신규 G Entry4만 갱신하며 이전 승인150/150·상위 완료1/5 불변. Entry7 없음. 공식 JAR·게임 renderer/애니메이션 동작·좀보이드 객체 정체·실제 마크 맵 변환은 미인증.
