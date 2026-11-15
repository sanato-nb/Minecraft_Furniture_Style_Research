# 1-2-B Entry5 시작·보존 지침
현재 **B_IN_PROGRESS_ENTRY4**이며 **A_COMPLETE_SOURCE_SCOPE**는 고정.

GitHub 최신 main HEAD 확인 뒤 `docs/vanilla_models_1-2/1-2-B_WORK_PLAN.md`와 `entry4/B_SCOPE_2390_STATUS.csv` 및 `entry4/B_ENTRY4_AUDIT.json`을 읽는다. **Entry1 14 + Entry2 120 + Entry3 180 + Entry4 210 = 524개** B-first leaf 직접 검증 완료이므로 중복 신규 실적 금지.

- B-first 미검증 **1,836개**: P1 409, P2 827, P3 600. P1 E-first 30은 별도 유지.
- P2/P3 부모 조상 의존성 확인 419, 미확인 **1,427**. 기존 419의 `no`를 나머지에 일반화 금지.
- 일반 원본 기하 출처 확인 **512**, source `elements` 없음 **12**. E에서 엔진 예외 의미 확인 예정; 가시성 단정 금지.
- 기하 원본 좌표가 뒤집힌 `trial_spawner`와 `vault_ejecting_reward_ominous` 요소를 소스 오류로 삭제 금지. 후속 C/E에서 면/UV/렌더 해석.
- 원본 고유 경로 615개(실제 Entry1~4 raw source SHA 검증 집합); 과거 Entry3 보고서의 399는 원본 재대조 **396으로 정정**, `entry4/PRIOR_UNIQUE_SOURCE_RECONCILIATION.json` 참조. 기존 역사 문서 수정 금지.
- 마크 Java1.21.11, 연구 체크포인트 v69, 원본 P1 544×393 및 review544×70, A 최종 기록, 1-1 승인150/150, 상위 완료1/5 절대 변경 금지.
- B1 원장 색인 PASS, B2·B3 PARTIAL, B4 종료감사 PENDING. B 종료 선포, C/D/E/F/G 완료 선포, 가구 제작/PZ 변환 금지.
- 다음 Entry5는 `B_SCOPE_2390_STATUS.csv`의 B-first `false`만 선정, 원본 leaf 및 parent Git SHA/JSON 직접 확인, 기존 source-proof를 단순 재사용할 수 있어도 반복 소스 읽기를 새 발견으로 계상 금지, 상태 원장 비파괴 업데이트, 저장 후 원격 SHA 검증.
