# Minecraft Furniture Style Research — 1-2-B Entry10 전체 잔여 636개 원본 연구

**Minecraft Java Edition 1.21.11 · 2026-11-16 KST** · 기준 main HEAD: `92d061766fcdc1e4c36ef4cad398968bc4943db3`.

## 실행 범위와 원본 직접 검증

기존 Entry9의 `B_SCOPE_2390_STATUS.csv`에서 `B_first_owner_scope=B_FIRST_2360` 및 `B_parent_chain_source_verified=false` 조건에 맞는 **636개 전부**(P1 169, P2 347, P3 120)를 선정. 기존 Entry1~9의 1,724개 leaf는 이번 신규 실적이 아님.

- **신규 leaf 636/636 원본 Git Blob SHA 지정 JSON 직접 조회 성공.** 고유 조상 부모 원본 **122개 Git Blob 직접 재열람**, 이전 캐시의 SHA/JSON과 일치.
- 모든 새 leaf의 parent chain **636/636** 해결. 누락·순환·지원되지 않는 부모 경로: **0**. 1-2-A 원본 자산 색인 4,669건과 모든 소스 경로/SHA를 대조.
- 이전 고유 소스 1,767 + 신규 고유 경로 593 = **2,360 고유 소스 JSON**. 새 leaf 중 **43개는 이전 부모 소스 재사용**이므로 새로운 고유 경로로 중복 계산하지 않음. 추가 신규 부모 소스는 0.
- 전체 B-first **2,360/2,360** 원본 계보·기하 상태 검수. E-first P1 30개는 B-first 분모에 산입하지 않고 기존 상태 그대로 보존.

## Entry10 소스 기하 실측

| 구분 | Entry10 신규 636 | B-first 전체 2,360 |
|---|---:|---:|
| 자체 `elements` 기하 | 85 | 327 |
| 부모로부터 상속 기하 | 538 | 1977 |
| 일반 `elements` 미존재 | 13 | 56 |
| 적용 element 인스턴스 | 1,602 | 5,689 |
| face 선언 참조 | 6,542 | 23,090 |
| cullface 참조 | 2,338 | 8,988 |
| 0두께 요소 | 502 | 1,965 |
| 회전 요소 | 402 | 1,548 |
| 원본 0~16 범위 밖 요소 | 75 | 413 |
| 원본 역방향 좌표 요소 | 2 | 18 |

숫자는 **leaf마다 실제로 적용되는 원본 선언 인스턴스 수**이다. 동일한 부모 템플릿이 여러 leaf에 사용되면 중복 적용된다. 회전 후 메쉬 또는 실제 게임 렌더 검증이 아니며 `from/to`를 뒤집어 수정하지 않았다. 모든 JSON 원본과 5,689개의 요소 행에 출처 SHA를 연결했다.

## B2 — 부모 의존성

P2/P3 **1,846/1,846** 모두 source 기반 P1 조상 여부 판단: **no 1,846, yes 0, unresolved 0**. 이전 원장의 `NO_P1_ANCESTOR_SOURCE_CHECKED` 표기 1,080건은 직접 확인된 `no`와 **동일 의미**임을 새 감사에 기록했으나, 그 **기존 셀을 수정하거나 신규 실적으로 재집계하지 않았다**. 이전 원장 원본 경로·SHA·기하 제공자 충돌 0.

## B3 — 기하·예외

기하 유형 분류 **2,360/2,360**. `elements`가 전체 JSON 계보에 없는 **56개**는 `B_NO_ELEMENTS_SOURCE_ALL.csv`에 원본 SHA/계보를 두고 **1-2-E**에 인계. 원본 좌표 역전 **18개 인스턴스**는 `INVERTED_COORDINATE_ELEMENTS_ALL.csv`에 원래의 from/to로 보존. 이러한 E 이관은 B 소스 기하 상태 미확인이 아니라 **특수 렌더/런타임 정체 인증 미수행**을 뜻한다.

## 종료 게이트와 검수 경계

- B1 범위·증거 통합: **source PASS**.
- B2 부모 계보 및 P1 의존성: **source PASS**.
- B3 원본 기하 상태: **source PASS**, E 예외 56 별도.
- B4 독립검사: **54/54 source PASS** + 첫 커밋 30/30 원격 파일 SHA·내용·행수 + 불변 원본 SHA 5/5 **PASS**. **`B_COMPLETE_SOURCE_GEOMETRY_SCOPE` 선언**.

**변경 금지 보존:** 1-2-A `A_COMPLETE_SOURCE_SCOPE`, v69 P1 544×393/검토 544×70, 1-1 승인 150/150, 상위 단계 완료 1/5, 원본 v1~v69 및 Entry1~9. 새 가구 모델/좀보이드 변환 없음. UV·PNG는 C, blockstate D, 특수 renderer E, 최종 스타일 규칙 F/G 소관이며 B의 추가 완료 조건이 아니다.

## 핵심 파일

- `B_ENTRY10_SELECTION.json`, `LEAF_DIRECT_SOURCE_PROOF_636.json`, `PARENT_DIRECT_SOURCE_PROOF_122.json`, `SOURCE_JSON_CACHE_2360.json`
- `MODEL_GEOMETRY_ALL_2360.csv` 및 신규 `MODEL_GEOMETRY.csv`; `ELEMENTS_P1_ALL.csv`, `ELEMENTS_P2_ALL.csv`, `ELEMENTS_P3_ALL.csv` 및 신규 `ELEMENTS.csv`
- `PARENT_TEMPLATE_SOURCE.csv`, `GEOMETRY_PROVIDER_REUSE.csv`, `B_NO_ELEMENTS_SOURCE_ALL.csv`, `INVERTED_COORDINATE_ELEMENTS_ALL.csv`, `B_UNRESOLVED_HANDOFF.csv`
- `B_SCOPE_2390_STATUS.csv`, `B_ENTRY10_B1B2_AUDIT.json`, `B_ENTRY10_B3_AUDIT.json`, `B_ENTRY10_AUDIT.json`, `B_ENTRY10_SUMMARY.json`, `B_NEXT.md`.


## 사후 GitHub 원격 검증 확정 (2026-11-16 KST)

첫 커밋 `e6e5baef84ed521f04c93cd6e29725b48290e055`의 **30개 파일**을 GitHub 원격 경로별로 다시 읽고 원본 Git Blob SHA·JSON/CSV 내용·행수 모두 일치 확인. v69 P1 원장 2개, A 원본 자산 색인, A 완료 인수인계, Entry9 보고서 **5개 보존 SHA 일치**. 최종 `B1~B4 PASS`와 B 소스 범위 완료 선언. UV/PNG 등 후속 단계는 별도.
