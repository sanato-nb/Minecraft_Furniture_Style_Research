# 7-G 보완 2차 — 범위 잠금 및 판정/검색 안전성

최초 5 PASS / 11 PARTIAL 기록 보존. 고정 T01~T16 변경 없음. 설계용 DDL에 17개 잠금 트리거 추가(기존 8개 테이블 변경 없음). 연구 범위 잠금 뒤 정의 INSERT/UPDATE/DELETE 및 unlock 거부. 체크포인트 동일 위치·동일 근거 재시도 no-op, 충돌 거부 및 rollback 확인. 최신 결과는 요구 항목별 동일 task의 최대 attempt_no이며 다른 task 혼재 또는 미완료 최신 결과는 거부한다. 과거 assessment는 보존하지만 검색 승인에는 최신 결과와 필수 unit_kind 전체가 있어야 한다. COUNTEREXAMPLE 근거도 확정 검색 제외. 실제 cross-job 및 운영 권한 통합은 별도 범위. 이번 커밋은 재실행 전 승인하지 않는다.
