# v67 → 다음 채팅 1-2-A 연구 인수인계

**최초 실행:** 실시간 GitHub `main` HEAD 조회. 최신이 v67인지 확인하고 v68+ 존재 시 최상위 최신 적용. `research/vanilla_models/v67/{REPORT.md,SUMMARY.json,07_P1_544_EVIDENCE_LEDGER.csv,VALIDATION_POST_RESEARCH_COMMIT.json}` 읽기.

## 이번 실측

v66에서 원본 직접 JSON 544/544 읽기 근거는 이미 있었으며 그 중 **own elements 0인 13개의 모델**(candle1~4, cartography_table, lightning_rod/on, torch, decorated_pot, ender_chest, oak_hanging_sign, shulker_box, white_shulker_box)의 **leaf 원본 13 + 부모 JSON 8 + blockstates 원본 9 + 실제 소스 PNG 9**를 원격 GitHub 경로+SHA로 다시 직접 읽음. 기존 v66 13 leaf original JSON 내용+SHA 동일, 새로운 unique direct read 신원0, 새로운 모델 identity0.

- 부모 상속으로 source geometry 확보한 leaf **8개**, 자체/부모 JSON 원본 요소 전부 없는 leaf **5개**. geometry0은 '인게임 보이지 않음' 또는 'shape 인증'이 아니다.
- 상속 적용 **요소 인스턴스36 / 면 참조134 = source explicit UV128 + 원본 UV-key missing6**. zero thickness 요소 인스턴스20, element rotation 인스턴스20. original source face에 `from/to`, 요소회전, cull/tint, 원본 UV, resolved texture path/SHA 모두 `01_ORIGINAL_INHERITED_FACE_134.csv` 기록.
- **cartography_table:** `minecraft:block/cube` 원본 [0,0,0]→[16,16,16] 1요소6면; **원본 UV 미지정6**, [0,0,16,16] full cube geometry derived UV 후보6, 공식 게임 엔진 인증 아님.
- candles4 leaf own0, 부모 template마다 **elements3/6/9/12, faces10/20/30/40** 재사용. 이 합계100은 신규 개별 원본 face 선언 100개가 아니라 leaf별 source 적용 참조.
- lightning_rod/on 동일 parent template 2요소11면을 둘 다 상속해 합22 face refs. powered true/false 각6방향 원본 blockstate 참조. torch template1요소6면.
- 원본 blockstates9 파일 **전체 variant 27중 선택 leaf13을 가리키는 refs23**, candle lit=true 4개는 선택 13 원형 대상 외; 관련 model source는 이번 미검수.
- 원본 PNG9(전부 16×16) Git blob SHA+PNG IHDR 재확인. face texture paths resolved134/134, **새 PNG RGBA 실제 픽셀 복호화0**, Minecraft renderer 직접 인증0. 과거 v56 49 PNG 경로 결과를 새 성과로 중복 계산 금지.
- **원장**: v66 P1 544행×351열 → v67 **544행×365열**, 이전 **190,944셀 값 전부 보존**. source review v66 544행×48열 → v67 544행×56열, 이전 **26,112셀 동일**. 증거 13 leaf+8 parent+9 blockstate 원본 스냅샷 `00_ORIGINAL_SOURCE_*`, source face 134 CSV, original blockstate refs23 CSV, source PNG9 SHA/IHDR JSON, style 관찰 JSON. 과거 v65 history 194files/ v66 prior28 direct JSON 및 UV148·shelf38 별도 실적 그대로.
- **다음 추천 실제 연구**: 이번 **5개 geometry0 모델의 특수 renderer 구현 근거**를 공식 소스/버전 맞는 리소스로 확인해 'unknown' 해결 시도. candle lit=true 모델4 원본/상속/source state/PNG 근거 조사; 암시 UV의 실제 1.21.11 버전 engine 공식 인증(가능할 경우). 또는 P1 다른 아직 상속/PNG 깊이 검증 안 된 모델을 고유 목록에서 우선 선정. 모든 경우 과거 49 PNG 전수 재연구 중복 금지.
- SHA key 항상 `(asset_type, full_source_path, git_blob_sha)`. source original explicitUV vs computed candidate vs runtime authentication 구분. 1-1 승인150/150, 상위 연구 1/5완료, 1-2-A/1-2 미완료·완료율 null. 마인크래프트 가구 실제 제작이나 PZ 변환 **시작하지 않음**.
- GitHub 수정 전 fresh main HEAD lease, 충돌시 병합/보류. 연구 저장 후 원격 파일/기존 데이터셀 check, 별도 validation commit과 최신 HEAD 읽기.
