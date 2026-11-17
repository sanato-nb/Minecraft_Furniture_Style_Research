# A-03 부모 원형69·의자39 원본 관계 재검산

기존 v11/v18/v20 CSV를 직접 열어 69 원형의 원저자 고정 Git 트리 SHA **69/69** 및 v18 부분집합 30/30 교차 대조. 원본 JSON bytes 독립 재해시 2/69(의자 부모 2개 직접 재판독), 나머지 67개는 `TREE_ONLY` 등급 유지.

v24 의자 leaf 39/39 경로·SHA 일치, 부모 SHA 39/39 대응, 원본 모델 JSON은 별도 직접 재해시 미수행. v23 birch/spruce 의자 참조 44개 중 기검증 5개 제외 39개. 의자 일반 19, tucked 20. **상속 요소 390, 상속면 1794**(bottom 1131, seat 195, back 468)이며 이는 **PNG 픽셀/실제 렌더가 아닌 선언된 상속 인스턴스**.

원본 부모 원형 실측: chair.json: 10 elements / 46 faces, z_min 2, z_max 14, z=-9 false; chair_tucked.json: 10 elements / 46 faces, z_min -7, z_max 5, z=-9 false. 음수 z는 로컬 좌표이며 충돌·시각 렌더 모델 인증이 아님.

A3 선행 관계/분모 검산 일치, 독립 재해시 범위 2/69. 1-3-A 전체 완료는 별개.


## 2026-11-18 원형 69개·의자39 독립 재해시

69개 템플릿 JSON 직접 재개방 후 SHA-1·원본 `parent`·요소 수·면 수를 대조하여 69/69 일치. 의자 leaf 39/39는 A1의 204개에 포함되어 이중 집계 없음. 정상 19 / tucked 20, 상속 요소 390 / 면 1,794(29 bottom·5 seat·12 back×39) 확인. 원본 chair Z=2~14, tucked Z=-7~5는 모델 로컬 좌표. **A3 출처/기하 게이트 PASS**. PNG·실게임 renderer 검증으로 승격하지 않음. 근거: `A_A03_INDEPENDENT_TEMPLATE_REHASH_01~05.json`, `A_A03_INDEPENDENT_69_AUDIT.json`.
