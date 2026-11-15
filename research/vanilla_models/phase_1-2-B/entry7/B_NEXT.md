# 1-2-B Entry8 시작 인수인계

시작 시 GitHub 최신 main HEAD, 원본 계획 `docs/vanilla_models_1-2/1-2-B_WORK_PLAN.md`, `entry7/B_SCOPE_2390_STATUS.csv`, `entry7/B_ENTRY7_AUDIT.json` 먼저 확인. 이미 Entry8이 존재하면 반복 작업 금지.

- A = `A_COMPLETE_SOURCE_SCOPE` 확정. B = `B_IN_PROGRESS_ENTRY7`. B-first **1,244/2,360** leaf source 계보 확인, **1,116개 미확인**(P1 265, P2 539, P3 312). P1 E-first 30은 별도 E 담당 유지.
- 검증 누적: Entry1 14 + Entry2 120 + Entry3 180 + Entry4 210 + Entry5 240 + Entry6 240 + Entry7 240 = 1,244. 신규 실적으로 재계상 금지.
- P2/P3 P1 조상 source 검증 995, 미확인 unknown **851**. 검증 995의 no를 나머지 851에 일반화 금지.
- B-source 일반 요소 있음 1,215, 없음 29(E 검토). 원본 좌표 역전 `cube_bottom_top_inner_faces`, `trial_spawner_active`, `vault_active` 및 5개 no-elements 모델 소스는 그대로 보존.
- 원본 raw JSON 고유 경로 총 1,318. 과거 Entry3 399→396 중복 정정 문서 Entry4에 있음. Entry7 신규 모델 240, 신규 부모 5, 과거 부모 원본과 중복 15로 **고유 원본 경로 순증 230**.
- 다음 Entry8은 **`B_first_owner_scope=B_FIRST_2360`, `B_parent_chain_source_verified=false`**만 모델 최초 검증 후보로 고르고, 원본 Git Blob SHA·parent chain·element from/to·rotation·cullface를 실제 파싱한 결과만 계상.
- B1 범위 색인 PASS, B2/B3 PARTIAL, B4 PENDING. v69 원장 544×393/review544×70, 1-1 승인150/150 및 상위 1/5 보존. 모델 제작·PZ 변환·C/D/E/F/G 완료 오인 금지.
- 구조화 상태표 비파괴 수정, 독립 행수/SHA 감사, GitHub commit + remote blob readback 필수. B 종료 게이트 전 `B_COMPLETE_SOURCE_GEOMETRY_SCOPE` 금지.
