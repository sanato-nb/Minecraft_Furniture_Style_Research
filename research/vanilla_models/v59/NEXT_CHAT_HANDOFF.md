# v59 → 다음 채팅 1-2-A 연구 인수인계 (Minecraft 1.21.11)

1. GitHub `main` HEAD를 새로 읽고 v59 이상 최신 우선. v59 `SUMMARY.json`, `REPORT.md`, `07_P1_544_EVIDENCE_LEDGER.csv`, `VALIDATION_POST_RESEARCH_COMMIT.json`부터 실제 읽기.
2. v59 원장 **544행×259열**; 이전 v58 242열×544셀 전부 동일. 신규17열은 이번35개 행만 데이터 기록. P1 **기존 544 경로·SHA**는 기하/UV/렌더러 완료 아님. 신규 신원 링크 **0**.
3. P1 v53 신규175, v57 신규 분석16, v58 신규 분석27과 겹치지 않는 **새 깊이 재검증35모델**: oak/spruce/birch/cherry shelf leaf 28 + template_shelf_* 7. 직접 원본 JSON+SHA `00A/00B/00C`; source own 11요소/38면 vs 상속 적용 55요소/190면. 원본 명시UV190, 암시후보0, 0두께 적용25, resolved PNG leaf152 face, standalone template #all 미해결38면.
4. 원본 블록상태 4종 원문은 `00C_`. 나무마다 multipart24규칙. `facing4×powered2×side_chain4=32` 유효 상태×4나무=**128상태/256 모델선택**, 전부 본체1+전면1 조건을 정적 평가 `03_`; Minecraft 런타임 인증 아님. `side_chain` 4가지 `unconnected,left,center,right`, `unpowered`는 `powered=false`에 대한 오버레이로 다섯번째 `side_chain` 값이 아님.
5. 실제 PNG 네 개 각각 **32×32**(총 **4,096 RGBA 픽셀**) Git SHA1/SHA256/Pillow 직접 확인. `uv` 0..16 좌표 **×2 실화소**. 전면 원본 명시 UV `5변형×4나무=20면` ×128 PNG픽셀 = **2,560원본 crop 텍셀**, 20개 crop SHA256 `04_`. **나머지 132 leaf faces는 texture path/UV 연결만 했지 Pillow crop하지 않았다.** full 152 face pixel complete 주장 금지. 실게임 UV/UVLOCK/회전 미검증.
6. 모델 별 소스가 보이는 190면 `02_`, 구조·상속 `01_`, 중복검사 `05_`, 스타일 관찰 `06_`; 재현용 스크립트 `REPRODUCE_V59_SHELF_PNG_AUDIT.py`는 저장했지만 full checkout에서 재실행하지 않았음. 개별 원본 4 PNG/20 crop은 직접 Python에서 검증.
7. 남은 코호트 **291 P1 모델**은 단순히 v53 new175/v57 16/v58 27/v59 35 범위 밖이라는 뜻; 이 모두가 과거 의미론 근거가 없는 완전 미분석 모델은 아님. v1~v58 역사 의미론 전체 통합 아직 미완료. v56 신규175 모델 PNG49·face3393·pixel51228, v57 PNG4·pixel1536, v58 PNG4·pixel1024는 이번 수치와 중복 합산 금지.
8. 셜커13+skull1 특수 렌더러 및 공식 1.21.11 엔진 암시UV/회전/uvlock 인증 여전히 미완료. **1-1 승인150/150**, 상위 **1/5 완료**, **1-2-A/1-2 진행 중·실질 완료율 미산정**. 가구 제작/좀보이드 변환 금지.
9. 후속 연구 후 새 원장/소스 SHA 셀 보존, precommit HEAD 임대·commit 후 GitHub 원격 직접 readback과 검증 파일 갱신 필수.
