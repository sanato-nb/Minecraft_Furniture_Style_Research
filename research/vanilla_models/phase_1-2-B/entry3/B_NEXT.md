# 1-2-B Entry4 인수인계 (Entry3 중복 재연구 금지)

2026-11-15 · **B_IN_PROGRESS_ENTRY3**, 1-2-A **A_COMPLETE_SOURCE_SCOPE**. GitHub 최신 HEAD 우선 확인.

## 반드시 재사용
- `docs/vanilla_models_1-2/1-2-B_WORK_PLAN.md`에서 B1~B4 완료 조건을 그대로 유지.
- `entry2/B_SCOPE_2390_STATUS.csv` 대신 **`entry3/B_SCOPE_2390_STATUS.csv`**를 최신 B 증거상태 기준으로 사용.
- Entry1 14 + Entry2 120 + Entry3 180 = **314개 직접 검증 leaf**. 같은 314개를 신규 성과로 반복 계상하지 않는다.
- P1 B-first 63/514, P2 128/1,039, P3 123/807, E-first P1 30 별도. **B-first 2,046개 미검증**.
- P2/P3 부모/P1 의존성 직접 확인 **251/1,846**, `no` 251개, `unknown` **1,595개**. 전체 의존성이 없다고 추론 금지.
- source geometry 있음 307개, 원본 elements 없음7개. E에 인계한 7개를 렌더 누락으로 단정하지 않는다.
- 신규 부모33개, 신규 leaf180개를 직접 읽었으나 leaf 중 이전 부모 증거 경로 3개가 겹쳐 신규 고유 원본 경로는 **210개**, B 직접 열람 원본 경로 누적 **399개**.

## 다음 실행
1. Entry3 B-first 미검증 2,046개 안에서 우선순위/그룹/실제 geometry provider 재사용을 고려해 신규 대상을 선정, original source leaf/parent JSON·Git blob SHA 직접 검증.
2. 이전 `DIRECT_SOURCE_PROOF_180_33.json`과 Entry1/Entry2 원본 부모 템플릿은 재사용. 동일 Git SHA라도 다른 원본 경로는 합치지 않는다.
3. 원본 `from/to`, `rotation`, zero thickness, cullface, bbox(회전 전)·부모 순환/없음 여부를 기록하고 source 의미와 runtime 검증을 분리.
4. `crimson_hanging_sign`, `pitcher_crop_top_stage_0`, `light_03`, `light_15`을 E 소관으로 기록, 기존 no-elements3개와 중복 제거.
5. B2·B3·B4를 검증되지 않은 채 PASS 하지 않는다. 1-1 150/150, top1/5, v69 원장 544×393·70열, A 완료 상태 유지.
6. GitHub 최신 main HEAD lease 확인 후 새 결과만 커밋, 원격 파일 SHA·행수·원본 보존 post-commit 검증.

**아직 B 완료 아님.** 무한 신규 모델군 분석을 목표로 하지 않고, B의 2,360개 확정 분모 및 종료 판정 조건을 유지한다.
