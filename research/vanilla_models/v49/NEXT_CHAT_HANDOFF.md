# Minecraft Furniture Style Research v49 — 다음 채팅 시작용 인수인계

## 필수 최신 조회
GitHub `main` 실제 HEAD → `handoff/STATE.json` → `research/vanilla_models/v49/REPORT.md` / `SUMMARY.json` / `01_P1_544_EVIDENCE_LEDGER.csv` 순서로 열고 최신 연구 여부 확인. 이전 v48 `171/544` 숫자를 현재 수치로 사용하지 말 것.

## 이어받을 정확한 수량
- P1 모집단 **544 모델 경로**, v49에서 모델 **원본 경로+SHA 연결 230개**, 검토한 출처에서 **미연결 314개**. 이 숫자는 완전한 geometry+UV+PNG+blockstate+renderer 검증 비율이 아니다.
- v48 기존 171 + 이번 새 증거 연결 **59**. v49에 직접 다시 읽은 JSON 59경로 중 **6개 화분 leaf는 v47/09의 직접 검사 근거 회수** (신규 원본 연구 실적 아님), **53개만 이전 직접 연구에서 새롭게 검사**.
- v49 P1 신규 연결 구성: 화분 leaf 37, crimson/dark_oak/spruce 선반 leaf 21, `template_potted_azalea_bush` 부모 P1 경로 1.
- 화분 37: parent 상속 leaf34 / 자체 요소 모델3(`potted_bamboo`,`potted_cactus`,`potted_mangrove_propagule`). 새로 직접 조사한 원본 소스 자체 선언은 이 세 모델과 `template_potted_azalea_bush`까지 **30요소/106면(명시UV100, 암시UV6)**. 6개 암시 UV는 `potted_cactus`의 UV 키 부재. **효과적으로 leaf에 적용한 면 참조 978건**은 독립 원본 면 수가 아님.
- 화분 4 parent 중 `flower_pot_cross`,`flower_pot_cross_emissive`,`tinted_flower_pot_cross`는 v47 기존 연구 재사용; `template_potted_azalea_bush`만 이번 새 P1 경로 연결. 원본 화분 blockstate **37개 단일 variant → 정확한 해당 leaf 37**.
- 선반 21: 세 목재×7 leaf. 부모 원형7은 v38/v48 기존 SHA 동일, 신규 원형 0. **상속 면 참조114** (원본 선언면38×3목재 패턴) / 원본 blockstate **24×3=72 multipart** / 정적 파생 **32×3=96 상태** / **64×3=192 적용**. 원본 PNG RGBA 새 검증 0.
- 기존 v43 asset type 충돌 2건, v46 동일 SHA 다른 경로 7개 모델, v47 SQLite/스크립트 누계, v48 모델36/원본 기하 및 상태 검사 보존. 복합키 `(asset_type,full_source_path,git_blob_sha)` 사용.

## 다음 직접 작업
1. 남은 P1 미연결 314개에서 실제 디자인 가치 높은 `candle/cake`, `sign/hanging_sign`, 구리 조명·수납 계열 원본 JSON 및 기존 연구 SHA 근거 조사.
2. v49의 화분 **명시UV/암시UV와 source texture override**를 PNG 원본의 실제 RGBA 픽셀에 연결하되 pixel/source UV/상속 적용/렌더 예외를 별도 단위로 기록.
3. 정확한 원본 SHA와 이전 연구 버전/근거를 유지, 현재 연결된 230이 1-2 전체 완료율이란 주장은 금지.
4. v49 연구 파일/상위 상태 문서를 읽은 후 새 revision 생성, 커밋 전 HEAD 재확인 및 저장 후 재검증. 1-1 완료·상위 1/5 유지, 1-2-A 미완료, 모델 제작·PZ 변환 금지.
