# Minecraft 가구 스타일 연구 1-3-A 실제 감사 보고

**기준일:** 2026-11-17. **시작 main:** `0542fb2b713fcaa5217ddb20a5273c02e1940b01`. **작업 중간 HEAD:** `9b1db3b61dd421dba3d24713e5a4a276f149c33a`.

## 실제 재검증한 증거

- A-00: 기존 `v11~v24` **195 blob / 14 directories** 경로·크기·Git blob SHA 전수 기준 고정. 핵심 근거 본문 열람 및 파싱은 `A_INPUT_MANIFEST.csv`에 표시, 나머지는 트리 메타데이터 등급 유지.
- A-01: 원장 204 leaf (33+38+43+51+39), **204개 고유 경로·SHA/모델 ID**, 원저자 pinned Git 트리 **204/204** 일치, 중복 0. **모델 본문 직접 재해시 0/204**이므로 A1 최종 승인은 보류. 신규 발견 모델 0.
- A-02: 상태 22 JSON 원본 직접 재해시 **22/22**, 실제 상태 적용 1188건, 독립 오류 0, birch/spruce 의자 반례 2건 재현. 선행 원본 트리 177 중 미조사 후보 155를 분리.
- A-03: 템플릿 69/69 원저자 트리 SHA, 직접 원문 검산 2/69(두 의자 부모). 의자 39개, 부모 SHA 39/39, 정상 19/tucked 20, 상속 **390 요소, 1,794 면 인스턴스**. tucked의 음수 z 값은 일반형 대비 로컬 좌표 이동이며 실제 게임 렌더·collision 아님.
- A-04: Handcrafted authored 120, generated 16 고정 경로/SHA **136/136**, 원본문서 직접 재해시 2/136. 이전 PNG24·면RGBA784, 두 모드 합산 PNG175·면RGBA4113은 다른 분모(1-4). Macaw 과거 JAR 미확보·모델 직접 검증0을 새 검증으로 승격하지 않음.
- 원본 JSON 직접 재해시 합계 **undefined/431 (22 state + 2 template + 2 Handcrafted)**. 이는 동일 leaf와 부모/상태/모드를 합한 비중이 아니라 단지 서로 다른 고정 원본 JSON 파일 수.
- 이전 `v11~v24`, `1-1`, `1-2` 파일 Git 비교에서 **비A 변경 0건**(9b1db3b61dd421dba3d24713e5a4a276f149c33a 시점). 다음 A6에서 최종 다시 확인.

## 게이트 판정 (A6 최종 원격 검증 전)

- **A0** PASS_METADATA_AND_REQUIRED_FILES
- **A1** BLOCKED_A_DIRECT_LEAF_REHASH
- **A2** PASS
- **A3** BLOCKED_PARTIAL_TEMPLATE_BYTES
- **A4** PASS_PRIOR_SCOPE
- **A5** PASS_UNRESOLVED_CLASSIFIED
- **A6** PENDING_POST_COMMIT_READBACK

A 게이트는 아직 모두 PASS가 아닙니다. **1-3-A 완료 선언 금지**. 상위 1-3 M1~M6 = 0/6; 1-3-B 전체 고정 모집단 미결정. 세부 차단·B 인계는 `A_UNRESOLVED.csv`.

## 재배포·증거 등급

원저자 JSON·PNG·JAR 파일 원문은 저장소에 복제하지 않았습니다. `PRIOR_SOURCE_VERIFIED`, `FILE_SHA_ONLY`, `ORIGINAL_REHASHED_IN_A`, `BLOCKED`, `OUT_OF_SCOPE_1_4`의 의미를 분리합니다.
