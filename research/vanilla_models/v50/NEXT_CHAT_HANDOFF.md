# v50 인수인계 — Minecraft Furniture Style Research 1-2-A 계속 진행

GitHub `main` 최신 HEAD 먼저 읽고 `handoff/STATE.json`, `research/vanilla_models/v50/REPORT.md`, `SUMMARY.json`, `01_P1_544_EVIDENCE_LEDGER.csv`, `11_ISSUES.csv` 조회. 이전 v49의 230/314는 역사적 체크포인트일 뿐.

## 현행 근거 범위
- P1 모델 경로 **544개**, path+SHA 출처 연결 **281개**, 이번 조사 근거에서 미연결 **263개**. 전체 1-2 완료율 산정하지 않음. `(asset_type, full_source_path, git_blob_sha)` 필수.
- v50 새 직접 source 확인 P1 **51경로** = v49 미연결이던 모델 50경로 + 추가 발견한 P1 미연결 부모 `template_torch_wall.json` 1경로. `source-model JSON만 직접 확인`과 `geometry+UV+PNG+blockstate+renderer 완료`는 다르다.
- 51경로 중 22 particle-only (특수 렌더 실제 구현 미확인), 27 부모 상속, 2 own geometry. 자체 원본 5 elements / 22 faces (명시 UV16 / 암시 UV6). 부모 11개 및 상속 고리 조상 3개 직접 원본 읽기, 561 effective face applications (source explicit519/implicit42). template 자체 16개 미결합 슬롯은 자식 texture override 여부와 별개.
- 블록상태 원본 **35파일**, 소스 variants **74건**, 해당 51개 P1 경로 중 49개는 source world state 모델 참조 확인, 나머지 2개는 template라 직접 world state 참조 없음. 74개를 정적 상태 조합이나 런타임 성공 수로 변환하지 말 것.
- v48 `template_lantern`과 `template_hanging_lantern` 부모 원형 2개 SHA 일치; 재검증만, 신규 원형 성과 아님. v35 `cake`/slice와 v50 `template_cake_with_candle` 구분.
- 기존 v47 SQLite 4개 + scripts 4개, v49 화분/선반, v46 동일 blob 다른 경로, v43 asset_type 다른 파일명 오탐 정정 유지.

## 다음 작업
1. 나머지 P1 263 중 캔들 컬러 변형, 카펫/셜커 상자/조명 및 특수렌더 source를 근거 중심으로 대조하되 같은 부모 기하 재연구를 신규로 계산하지 않는다.
2. 실제 원본 PNG bytes/RGBA 및 face pixel mapping에 접근하면 v47~v50 명시/암시 UV를 source PNG SHA·UV range·alpha 실측으로 연결. JPEG 이미지 검색으로 원본 PNG 검증을 대체하지 않기.
3. v50 source particle-only 22경로의 렌더러 예외는 독립 코드/모드 source 근거로만 추가 검증.
4. 1-2-A 계속 진행, 1-1 v42 150/150 완료·상위 과제 1/5 유지. 사용자 제외 Mojang 압축 client.jar 인증 및 실제 인게임 렌더에 성공했다고 주장하지 않는다. 실제 가구 모델 제작/PZ 변환 시작 금지.
