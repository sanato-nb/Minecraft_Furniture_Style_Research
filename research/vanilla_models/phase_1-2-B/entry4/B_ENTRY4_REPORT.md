# Minecraft Java 1.21.11 — 1-2-B Entry4 원본 기하·부모상속 연구
> 2026-11-15 KST · GitHub baseline `576ea4569c70d4ce889be41e7a637fbbe7cb35ad` · 기존 v69 보존 · **B_IN_PROGRESS_ENTRY4 / B 전체 미완료**
>
> 근거: `docs/vanilla_models_1-2/1-2-B_WORK_PLAN.md`, `entry3/B_SCOPE_2390_STATUS.csv`, `entry3/B_NEXT.md`. **1-2-A는 종료 `A_COMPLETE_SOURCE_SCOPE` 유지.**

## 1. 이번에 실행한 원본 작업

기존 Entry1~3 leaf **314개는 신규 직접 검증 대상으로 다시 세지 않았다.** B-first 미검증 2,046개에서 13개 P×그룹 층별 잔여분 비례 quota와 파일명 순 균등 위치 선정을 적용하여 **210개(P1 42/P2 84/P3 84)** 선정했다. 통계적 무작위 표본·전체 일반화는 아니다.

- 선정 leaf **210개 원본 Git Blob SHA 직접 읽기+JSON 파싱**, 부족한 부모 **19개 추가 직접 읽기**, 과거 Entry1~3의 Git Blob 원본 JSON 증거 재사용.
- leaf 210개의 완전한 parent chain **210/210 해결**. 원본 복합키/부모 SHA/계보 순환/없는 부모 관련 치명적 오류 **0건**.
- 210개 중 leaf 자체 `elements`의 원본 기하 **24개**, 부모 상속 **181개**, 계보에 일반 원본 `elements` 기하 없음 **5개**.
- 상속 후 요소 인스턴스 **493개**, 면 선언 참조 **1,867회**, 두께 0 요소 인스턴스 **201개**, `rotation` 선언 요소 **149개**, `cullface` 선언 면 참조 **735회**. 부모 요소/면이 여러 leaf에 반복 적용되므로 **고유 소스 선언 수가 아니다.**
- 이용된 소스 기하 제공자 경로 **90개**. bbox는 회전 전 원본 from/to의 실제 최소/최대 좌표를 기록하며, UV와 blockstate 적용 회전·월드 렌더는 인증하지 않았다.

## 2. 특별한 원본 기하 발견(원본 좌표 보존)

`trial_spawner.json` → `cube_bottom_top_inner_faces.json` 및 `vault_ejecting_reward_ominous.json` → `template_vault.json`에서 `from.x > to.x`인 **2개 leaf 적용 요소**를 확인했다. 예시 원본 내부 표면 좌표는 전자의 `[15.998,0.002,0.002]` → `[0.002,15.998,15.998]`, 후자의 `[15.998,3.002,0.002]` → `[0.002,15.998,15.998]`이다. **이들은 단순 데이터 오류로 삭제하거나 정렬하지 않는다.** `INVERTED_COORDINATE_ELEMENTS.csv`에 그대로 남겼다. 원본에서 좌표가 0~16 밖에 있는 요소 인스턴스 **57개** 역시 변형 없이 보존했다. 텍스처 방향/면 실제 렌더는 C/E 이후 확인한다.

원본 `elements` 없는 5개: `birch_sign`, `cherry_hanging_sign`, `exposed_copper_golem_statue`, `light_04`, `light_13`. 이는 모델 JSON의 일반 요소 부재만 검증한 결과다. **게임에 표시되지 않는다는 뜻이 아니며**, 후속 E 렌더러/특수 표현 확인 담당으로 남겼다.

## 3. B-first 누적 상태

| 우선순위 | 누적 소스 계보 검증 | 미검증 |
|---|---:|---:|
| P1 / B-first | **105 / 514** | 409 |
| P2 | **212 / 1,039** | 827 |
| P3 | **207 / 807** | 600 |
| **B-first 합계** | **524 / 2,360** | **1,836** |

B-first에서 일반 원본 기하 제공자 확인 **512개**, `elements` 미확인 렌더링 보류 **12개**. P2/P3의 P1 조상 의존성 **419/1,846** 직접 확인: 확인된 419개는 원본상 `no`; 나머지 **1,427개는 unknown** (근거 없이 `no`로 바꾸지 않음). P1 E-first **30개**는 기존 담당 유지.

## 4. 이전 원장 고유 경로 수 중복 제거 정정

기존 Entry3 보고서에는 원본 JSON 누적 고유 경로 **399개**로 적혀 있으나, **보존된 Entry1 원본27건 + Entry2 원본163건 + Entry3 원본213건 전체를 경로·SHA 단위 재대조**하면 유일한 원본 경로는 **396개**다. 이전 보고서에서 언급한 부모 소스 중복 3개 외에 **추가 3개**(`template_four_candles`, `cube_column_uv_locked_x`, `template_fire_side`)가 겹친 것이 원인이다. 자세한 경로는 `PRIOR_UNIQUE_SOURCE_RECONCILIATION.json`.

이번 leaf 210 중 10개 경로는 과거 부모 원본으로 이미 읽힌 바 있고, 신규 부모 19개는 과거 원본 경로와 겹치지 않는다. 따라서 **이번 신규 직접 열람 원본 고유 경로 순증 219개**, 누적 **615개**다. 이것은 신규 모델 의미 정체를 219개 발견했다는 말이 아니다. **이전 파일 원본을 수정하지 않고** 정정 근거를 새로운 보고서에 첨부했다.

## 5. 검증과 후속 인계

Entry4 기하 및 2,390행 상태 원장 독립 교차감사 **50/50 PASS** (`B_ENTRY4_AUDIT.json`). 게이트 **B1 PASS(모집단 근거색인만), B2 PARTIAL, B3 PARTIAL, B4 PENDING**. **B 전체 완료 선언 불가**. 원본 v69 P1 544×393 원장·544×70 review, 이전 Entry1~3, A 확정 보고서 불변 보존. 1-1 승인 **150/150**, 상위 5개 중 완료 **1/5**. UV/PNG C, blockstate D, 특수렌더 E, 스타일 유형화 F, 최종 독립 검수 G는 별도이며 실제 가구 모델 제작/좀보이드 변환 미착수.

### 생성한 산출물
- `B_ENTRY4_SELECTION.json`: 원본 SHA가 있는 신규 B-first 210개 선정 근거
- `DIRECT_SOURCE_PROOF_210_19.json`: leaf 원본 JSON210 및 신규 부모 원본 JSON19의 직접 재현 증거
- `MODEL_GEOMETRY.csv` (210), `ELEMENTS.csv` (493), `NEW_PARENT_SOURCES.csv` (19), `GEOMETRY_PROVIDER_REUSE.csv` (90)
- `B_NO_ELEMENTS_SOURCE.csv` (5), `INVERTED_COORDINATE_ELEMENTS.csv` (2), `B_SCOPE_2390_STATUS.csv` (2,390), `PRIOR_UNIQUE_SOURCE_RECONCILIATION.json`
- `B_ENTRY4_AUDIT.json` (50/50), `B_ENTRY4_SUMMARY.json`, `B_NEXT.md`

GitHub 원격 저장·파일 SHA readback은 아래 별도 사후 검증에서 입증한다.
