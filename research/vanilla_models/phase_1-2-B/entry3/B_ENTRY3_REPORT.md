# Minecraft Furniture Style Research — 1-2-B Entry3 실측 연구

> 2026-11-15 KST · 원본 Minecraft Java 1.21.11 · 출발 main `19bf6292585622498a1795e868128b0f04addbe1` · v69 과거 근거 유지.
>
> **B 상태: `B_IN_PROGRESS_ENTRY3`. 1-2-A는 `A_COMPLETE_SOURCE_SCOPE`로 종료 상태 유지. B 전체는 미완료.**

## 직접 수행한 원본 연구
이전 Entry1 leaf14개·Entry2 leaf120개를 **이번 신규 성과로 다시 집계하지 않았다.** 이전 `entry2/B_SCOPE_2390_STATUS.csv`에서 B-first 미검증 2,226개 중 **180개(P1 36/P2 72/P3 72)**를 13개 우선순위×그룹 층화 안에서 남은 수에 비례해 균등 위치 선정했다. 무작위 대표표본이나 통계적 외삽 근거는 아니다. 정확한 경로·Git SHA는 `B_ENTRY3_SAMPLE_SELECTION.json` 참조.

- 각 모델 **원본 JSON 180개 직접 Git Blob 조회·파싱**. 초기 부족한 부모 템플릿 **33개를 추가 직접 조회·파싱**하고 Entry1·Entry2의 원본 부모 JSON 증거를 재사용하여 **부모 체인 180/180 끝까지 해결**, 경로/복합키/SHA 불일치 0.
- 조회 원본 파일 경로는 이번 leaf180 + 신규 부모33 = 213개. 그중 leaf **3개는 이전 B 연구에서 부모 소스로 이미 읽었던 파일**이므로 B 누적에서 **신규 고유 원본 경로 210개**만 계상. 기존 B 189개와 합쳐 **누적 399개 원본 JSON 경로**, 과거 v44~v69 모델 정체 신규 발견 **0개**.
- leaf가 자체 `elements` 선언 **24개**, 부모 `elements` 상속 **152개**, 전체 계보에 원본 `elements` 없음 **4개**.
- 상속 후 leaf별 적용 요소 인스턴스 **381개**, 면 선언 참조 **1,548회**, 두께 0 요소 인스턴스 **143개**, 원본 `rotation` 있는 요소 인스턴스 **105개**. **인스턴스는 부모 템플릿의 재사용을 포함하며 고유 원본 요소/면 수가 아니다.**
- 이번 범위에 실제 쓰인 고유 기하 제공자 경로 **79개**. `bbox`는 회전 전 원본 from/to의 최소·최대. 엔진의 월드 배치/렌더 완료 주장이 아니다.

## 미확인 사항을 보존한 예외
`crimson_hanging_sign.json`, `pitcher_crop_top_stage_0.json`, `light_03.json`, `light_15.json`은 leaf 및 모든 확인된 상위 부모 JSON에 일반 `elements` 배열이 없다. `B_NO_ELEMENTS_4.csv`로 격리하고 **1-2-E 특수 렌더·표현 근거 확인 대상으로 인계**한다. 게임에서 표시되지 않는다거나 기능이 없다는 결론은 내리지 않는다.

## 전체 B-first 2,360개로의 정확한 통합

| 대상 | Entry2 누적 | Entry3 신규 leaf | 현재 source 계보 검증 | 남은 직접 검증 |
| --- | ---: | ---: | ---: | ---: |
| P1 B-first | 27 | 36 | **63/514** | 451 |
| P2 | 56 | 72 | **128/1,039** | 911 |
| P3 | 51 | 72 | **123/807** | 684 |
| **B-first 전체** | **134** | **180** | **314/2,360** | **2,046** |

P1의 **E-first 30개는 그대로 별도**. P2/P3 부모·P1 조상 의존성 직접 검증은 **251/1,846**, 확인된 범위에서는 P1 조상 `no` 251개이고 **남은 1,595개는 `unknown`**으로 유지. 확인된 314개 중 source 제공자 발견 **307개**, source `elements` 없음 **7개**(이전 3 + 이번 4). **검증된 샘플을 전체 B 완료로 외삽하지 않는다.**

## B1~B4 게이트 및 보존
- B1 **PASS**: 2,390개 전체 자산 경로·SHA·원장 식별키 및 B-first/E-first/증거 등급 분리.
- B2 **PARTIAL**: B-first 314/2,360 체인 검증, P2/P3 251/1,846.
- B3 **PARTIAL**: 실제 기하 제공자 307, 일반 elements 부재7, 나머지 B-first 2,046 미검증.
- B4 **PENDING**: 전체 독립 종료검수 불가.

Entry3 별도 데이터 독립 교차검사 `B_ENTRY3_AUDIT.json` **36/36 통과**. 감사 시 Entry1·Entry2의 `no` 표기(107개)와 Entry3의 `NO_P1_ANCESTOR_SOURCE_CHECKED` 표기(144개)를 동의어로 처리하는 감사식만 정정했다. **원본 1,595개 unknown에는 영향을 주지 않았다.**

기존 `v69/07_P1_544_EVIDENCE_LEDGER.csv` **544×393**, `v69/04_SOURCE_REVIEW_LEDGER_544.csv` **544×70**, 1-2-A 자료 및 Entry1·Entry2 내용은 비파괴 보존한다. 1-1 승인150/150과 최상위 5개 중 완료1/5 유지. UV/PNG는 C, blockstate는 D, 특수 렌더러는 E, 유형화는 F, 최종 검수는 G. 실제 마인크래프트 가구 제작 및 PZ 가구 변환은 미착수.

## 산출물
`MODEL_GEOMETRY.csv` (180), `ELEMENTS.csv` (381), `PARENT_SOURCES_NEW_33.csv` (33), `GEOMETRY_PROVIDER_REUSE.csv` (79), `B_NO_ELEMENTS_4.csv` (4), `B_SCOPE_2390_STATUS.csv` (2,390), `B_ENTRY3_SAMPLE_SELECTION.json`, `DIRECT_SOURCE_PROOF_180_33.json`, `B_ENTRY3_SUMMARY.json`, `B_ENTRY3_AUDIT.json` 및 `B_NEXT.md`.

GitHub 원격 저장 후 파일을 재조회하여 SHA와 행수를 별도 검증한다. **본문은 그 작업이 완료되었다고 사전 주장하지 않는다.**
