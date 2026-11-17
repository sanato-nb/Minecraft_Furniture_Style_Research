> **2026-11-17 · Entry6 최종 PASS:** 원본 829/829 실제 bytes·Git SHA, 모델378·blockstate265·PNG186, C/D/F 원장, 독립 감사 오류0, [GitHub Actions PASS](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44089873718). 전체 [G 4,669 원본·99 sidecar 독립 감사](../final/G_GLOBAL_INDEPENDENT_RECOUNT.json) G1~G5 PASS와 [원격 SHA·행수 검산](../final/G_GLOBAL_PRE_FINAL_REMOTE_READBACK.json)도 통과했어. **G 최종 6게이트 판정은 별도 G_FINAL_EXIT_AUDIT.json에 보존**하며 원본 게임 렌더·공식 JAR 인증으로 해석하지 않는다.

# 1-2-G Entry6 — 원본 829개 직접 소스 감사

GitHub Actions 체크아웃의 Minecraft Java 1.21.11 사용자 추출 파일 bytes로 검증.
**Entry6 판정: PASS — 원본·D/C/F·독립 감사·원격 재조회 통과**

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

## 범위 및 누락 출처 상세
- **G Entry6 모델378:** 일반371·E 특수7(원본 소스 신원만 인증). 부모/상속 기하 요소661, face2412. 명시 UV1352·생략1060, PNG 결합2178·템플릿 미바인딩234.
- **blockstate 265:** 원본 D 선택 1836, 참조 모델 고유522, 상태 조건·apply·회전/uvlock/weight 명시 필드 비교 오류0.
- **PNG186:** 원본44,847bytes, C 과거 RGBA182/182 일치·C 범위 밖4 신규 G 원본 검증. mcmeta12(애니7 정적), F3 선행 시각근거 교차135. F3 전체 첫 프레임 시각 자료 332종은 글로벌 증거이며 이번 Entry에서 모두 새로 육안확정한 것이 아님.
- **F 원장 출처 공백:** sculk_mirrored·stone_mirrored의 공유 부모 cube_mirrored 원본 SHA가 기존 F의 parent_chain 및 geometry_provider 총 4개 필드에 공란. 원본 파일 SHA 38f44bda128d10a5e09614e5ac155c956237681e를 G에서 직접 재검산했고 [누락 보완 JSON](G_ENTRY6_PROVENANCE_GAPS.json)에 별도 기록. F 원본을 소급 수정하지 않음. 최초 재실행의 오류 기록은 이력으로 보존.
- **미결정 원장:** [G_ENTRY6_UNRESOLVED_SCOPE.csv](G_ENTRY6_UNRESOLVED_SCOPE.csv) 252행 (미바인딩234, E renderer7, C 밖 PNG4, F 원장 누락SHA4필드, 시각·공식 JAR/런타임·애니메이션 제한3). 원본 해시 불일치 252건이 아니라 서로 다른 소관의 예외·제한.
- **글로벌 결과:** 6회 원본 검증 4669/4669, G1~G5 정적 감사 전제PASS, 최종 G6 원격 재확인/독립 종료 별도. 공식 JAR·런타임 렌더·애니메이션 실제 재생·좀보이드 가구 정체·맵 생성은 미인증.
