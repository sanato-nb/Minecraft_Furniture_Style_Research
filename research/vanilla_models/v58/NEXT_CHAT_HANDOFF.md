# v58 다음 채팅 1-2-A 정확한 체크포인트

1. 시작 즉시 GitHub `main` 최신 HEAD를 조회하고 v58 이상 최신 인수인계를 우선 읽기. v58 `REPORT.md`, `SUMMARY.json`, `VALIDATION_POST_RESEARCH_COMMIT.json`, `07_P1_544_EVIDENCE_LEDGER.csv`부터 확인. 대형 원장은 Git Blob API 이용.
2. v58 원장 **544행×242열**. v57 225열 모든 값 보존. 기존 544/544 원본 경로·SHA 연결은 이전부터 완성된 신원 확인; 기하/UV/PNG/렌더러 완료율이 아님. **신규 원장 열17개**, 이번 정확히 27개 P1 모델 행만 채움.
3. v53 신규175 모델도 v57의 16모델도 아닌 **P1 다른27모델 원본 JSON 직접 SHA 재대조**. 조각 책장 12 leaf + 6 부모 평면 template + 8 composter contents + 1 bookshelf inventory. 자체 요소15/면20 vs leaf 적용 요소27/면32. 명시UV24 vs 계산 후보8. 제로 두께 적용18. 소스 원문 `00A_`·`00B_`; 상속 기하 `01_`, 면 `02_`.
4. `03_BLOCKSTATE_EXHAUSTIVE_256_PLUS_9.json`: 기존 소스 blockstates 2경로 재활용, bookshelf 원본 multipart52규칙 → 4방향×64=256 상태 전 조합에서 매번 7 모델 선택(총 반복1792회); composter multipart9규칙 → level0~8 전 9상태(총17 적용). `uvlock:true`는 책장 본체 apply에 명시되고 슬롯은 uvlock 키 생략; 인게임 회전/UV 테스트 아님.
5. `04_ORIGINAL_PNG_4_SOURCE_RGBA_UV.json`: 원본 PNG 4파일 Git blob SHA1/독립 SHA256/Pillow 전체RGBA **1,024 픽셀**. bookshelf 빈/점유 두 16×16 전부 불투명, compost/ready 각각 중앙 144 opaque/외부112 alpha0. 원본 명시 UV 실제 소스 13면·반복768픽셀, 기하 계산 후보 UV 8면·반복1152픽셀. 중복 제외 원본 좌표800. 엔진 UV 공식 인증하지 않았음.
6. `05_HISTORICAL_NON_DUPLICATION_27.json`: v57 27 원본 typed path SHA 그대로 계승, v44 교차원장에 실제 17모델/32기존 증거행 확인, 신규 model SHA 최초 식별0. 역사 전체 v1~v57 의미론 전수 감사 아직 미완료.
7. v56 신규175 코호트 49개 PNG/3,393면/51,228 소스 픽셀, v57 신규 분석16모델/4 PNG/1,536 source pixels과 혼합해 완료율 만들지 말 것. v56 케이크 암시 UV168, v57 계산 후보124, v58 이번8 모두 원본 명시 UV로 바꾸지 말 것.
8. 남은 과제: P1 남은 모델의 소스 PNG/면 검증, 공식 1.21.11 엔진 UV 구현/rotation/uvlock 확인, shulker13+skull1 렌더러 공식 JAR/실제 렌더 검증, v1~v57 과거 의미론 통합. 전체 1-2-A/1-2 미완료. **1-1 승인150/150·상위5개중1/5 완료 유지.** 가구 모델 제작 및 Project Zomboid 변환 시작 금지.
9. GitHub commit 직전 HEAD 재조회, 동시 HEAD 변경시 덮어쓰기 금지. commit 이후 544×242, 이전 225열 전 셀 보존, 원본 SHA, PNG/UV 합계, blockstate 256+9, 상태/다음채팅 인수인계, 최종 HEAD 실제 readback.
