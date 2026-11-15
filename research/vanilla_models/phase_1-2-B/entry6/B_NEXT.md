# 1-2-B Entry7 인수인계 · 중복 분석 및 무한 반복 금지
마인크래프트 Java 1.21.11. 시작하자마자 GitHub **최신 main HEAD 조회**. 최신 상태가 이 파일보다 앞서 있으면 재실행 대신 최신 파일 사용.

- **A = A_COMPLETE_SOURCE_SCOPE 완료, 재실행 금지. B = B_IN_PROGRESS_ENTRY6.**
- 기존 B-first 직접 leaf/parent 계보 원본 검증은 **1,004/2,360**. Entry1 14 + Entry2 120 + Entry3 180 + Entry4 210 + Entry5 240 + Entry6 240. 남은 **1,356**: P1 313, P2 635, P3 408. E-first P1 30개 별도.
- `research/vanilla_models/phase_1-2-B/entry6/B_SCOPE_2390_STATUS.csv`의 `B_first_owner_scope=B_FIRST_2360` AND `B_parent_chain_source_verified=false`만 다음 최초 검증 대상으로 사용.
- P2/P3 계보 의존성 **803/1,846** source 검증(현재까지 P1 조상 yes0/no803), **1,043 unknown** 강제 분류 금지. source 기하 있음 **980**, 일반 `elements` 없음 **24**. 렌더 E 담당 예외 유지.
- Entry6 신규 leaf 240, 신규 부모 원본 7, 이전 부모 원본과 중복 14 → 원본 raw 소스 누적 고유 경로 **1,088**. 기존 1-2-A 및 이전 Entry1~5 파일 수정 금지; 과거 Entry3 399→396 정정 내용 Entry4 참조.
- `vault_ominous`의 역방향 `from/to` 좌표, 일반 요소 없는 `copper_chest`, `warped_hanging_sign`, `end_portal`, `copper_golem_statue`, `barrier`, `light_05`는 원본 보존·C/D/E에 인계. 눈에 안 보인다고 단정 금지.
- B1 scope-only PASS; B2/B3 PARTIAL; B4 PENDING. 단계 완료 임의 선언 금지. C/D/E/F/G 별도. v69 P1 544×393 및 review544×70, 1-1 승인150/150, 상위 1/5 유지.
- Entry7에서 신규 미확인 leaf/parent Git Blob 원본 확인 후 `B_SCOPE_2390_STATUS.csv` 비파괴 갱신, 독립 감사, commit 및 **원격 readback** 필수. 신규 모델 의미 정체 중복 계상 및 가구 제작·PZ 변환 금지.
