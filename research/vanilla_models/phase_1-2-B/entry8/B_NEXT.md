# 1-2-B Entry9 시작 체크포인트

1. GitHub main 최신 HEAD를 먼저 다시 조회한다. 이미 Entry9 이상의 파일이 있다면 이번 작업을 중복 실행하지 않는다.
2. 기준 상태: A = A_COMPLETE_SOURCE_SCOPE, B = B_IN_PROGRESS_ENTRY8. B 소스 범위 **1,484/2,360 검증, 876 미검증** (P1 217, P2 443, P3 216).
3. 다음 직접 조회 대상은 research/vanilla_models/phase_1-2-B/entry8/B_SCOPE_2390_STATUS.csv에서 B_first_owner_scope=B_FIRST_2360 AND B_parent_chain_source_verified=false인 행만. E-first P1 30개는 B-first 완료 분모에 합치지 않는다.
4. 연구 자체의 원본 재사용을 쉽게 하도록 entry8/SOURCE_JSON_CACHE_1544.json을 추가했다. 이 1,544개는 경로/원본 SHA를 보존한 기존 증거 캐시이며, 그중 이전 1,318개는 신규 실적으로 집계하지 않는다.
5. P2/P3 부모 계보 1,187/1,846 확인, no 1,187, yes 0, unknown 659. 아직 보지 않은 경로를 no로 처리 금지.
6. B-first 일반 elements 있는 source 1,448, 없는 source 36. 원본 좌표 반전 2개와 일반 요소 없는 7개 source는 그대로 보존하며, 특수 렌더 완료와 구분.
7. B1 범위 통합 PASS, B2/B3 PARTIAL, B4 PENDING. v69 544×393 및 review544×70, 승인150/150, 전체 1/5 보존. UV(C), blockstate(D), 특수 renderer(E), 유형화(F), 최종감사(G)는 각각 별도.
8. 남은 876개라는 유한 분모에서 단계 종료 게이트 통과를 목표로 수행. v70 같은 불필요한 연구 버전 생성, 새 모델군 무한 추가, 가구 제작·PZ 변환 금지.
9. Git 원본 Blob 직접 검증 및 독립 감사를 수행하고 저장 후 GitHub 원격 파일과 SHA/행수 재확인할 것.
