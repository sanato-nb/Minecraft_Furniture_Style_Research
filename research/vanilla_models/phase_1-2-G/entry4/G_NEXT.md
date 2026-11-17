# 1-2-G Entry4 최종 PASS — Entry5 허용, **아직 미착수**

**2026-11-17, Minecraft Java 1.21.11 사용자 추출 원본 조사.** Entry4 고정 원본 **944 = model JSON494 + blockstate JSON265 + PNG185** 실제 파일 bytes·Git blob SHA 재계산 **944/944 PASS**, 오류 0. [GitHub Actions 검증](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44074106047) success, [독립 감사](G_ENTRY4_INDEPENDENT_RECOUNT.json)·[원격 SHA/행수/본문 재검산](G_ENTRY4_REMOTE_READBACK.json) PASS.

- **모델 원본:** 494개 전체 부모 JSON 상속과 F 기하/C face 원본 교차. 일반 모델494, E 예외0(이번 Entry 배정 한정), 적용 요소1,067·face4,811, 명시 UV4,404/생략407, PNG 참조 연결4,355/템플릿 미바인딩456. 가상의 concrete PNG 경로를 만들지 않는다.
- **D state:** 265개 원본, variants/multipart 선택 **1,496개**, 참조 고유 모델 **498개**, 원문 조건·apply·명시 회전/UV lock/weight 및 기존 D 룰 재교차 오류0. 실제 state registry/런타임 renderer는 미검증.
- **PNG:** 원본185 bytes 합계49,246, Git SHA/PNG 디코딩/RGBA SHA256 검사 PASS. 기존 C 검증180/180 완전 일치. C 밖 5개는 G 신규 검증만 기록하며 소급 승격 금지. mcmeta 원문15(애니메이션 설정3, 재생은 미검증). F 선행 첫 프레임 시각 근거37은 G 새 육안 분류 실적으로 계산하지 않음.
- **범위 제한:** [G_ENTRY4_UNRESOLVED_SCOPE.csv](G_ENTRY4_UNRESOLVED_SCOPE.csv) 464행 = 미바인딩 face456 + C 밖 PNG5 + 시각/런타임/애니메이션 소관3. 이것은 원본 손상/해시 오류 464건이라는 뜻이 아님. 기존 A~F/v69 원본·승인150/150·상위 완료1/5 유지.
- **증거:** [보고서](G_ENTRY4_REPORT.md), [원본 신원 944행](G_ENTRY4_SOURCE_IDENTITY_944.csv), [모델 494행](G_ENTRY4_MODEL_GEOMETRY_RECOUNT.csv), [D 1,496행](G_ENTRY4_D_ORIGINAL_OPTIONS.csv), [PNG185행](G_ENTRY4_PNG_BINARY_AUDIT.csv), face 샤드3개(2,200+2,200+411행), [독립감사](G_ENTRY4_INDEPENDENT_RECOUNT.json), [원격 readback](G_ENTRY4_REMOTE_READBACK.json).

**G 전체:** Entry1~Entry4 승인 **4/6**, 누적 실제 원본 내용 **3,011/4,669 = 64.49%**, 잔여 **1,658**. **글로벌 G1~G6 최종 게이트 0/6**, G 전체·상위 1-2 미완료, Entry7 없음.

**다음 실행:** 사전 확정된 `research/vanilla_models/phase_1-2-G/entry5/G_ENTRY5_QUEUE_829.csv` **829개 = 모델 JSON379 + blockstate JSON265 + PNG185**만 별도 착수한다. Entry4의 944개를 반복 실적으로 계산하지 않는다. 원본 내용·Git SHA 전체 재검증, C/F/D/E 각 소관 대조, PNG 픽셀/애니메이션 정적 검사, 미결정 유지, 독립 검산 및 GitHub 원격 SHA·원장 행수·본문 재검증 PASS 전 Entry5 완료 선언 금지.

**인증 한계:** 공식 Minecraft JAR, 실제 게임 렌더/애니메이션, 물리 재질·PZ 가구의 정확한 정체·3D 모드 가구 구현·TMX→마크 맵 출력까지 검증했다는 뜻 아님.
