# 1-2-B Entry3 다음 작업

최신 GitHub `main` HEAD를 먼저 읽고 `docs/vanilla_models_1-2/1-2-B_WORK_PLAN.md` 및 이 디렉터리의 `B_ENTRY2_REPORT.md`, `B_SCOPE_2390_STATUS.csv`를 기준으로 진행한다.

**1-2-A 완료 유지** (G1~G5, 50/50). **1-2-B 현재 미완료**. 변경 금지 v69 연구 원장 544×393 및 review544×70, v1~v69/Entry1 및 Entry2 기존 결과, 1-1 승인150/150, 상위연구1/5. 새로운 모델 고유 정체 발견을 부풀리지 말 것.

1. `B_SCOPE_2390_STATUS.csv`에서 `B_parent_chain_source_verified=false`인 **B-first 2,226개**를 후속 대상으로 확인한다. 여기에는 P1 487, P2/P3 1,739 포함. E-first30은 별도.
2. Entry1 14 leaf + Entry2 120 leaf, 총 134개는 **다시 직접 읽은 항목을 신규 실적으로 중복 계상하지 않는다**. SHA 검증된 템플릿과 기존 v44~v69의 근거를 정확히 재사용한다.
3. 부모 계보에서 P2/P3 107개는 `no` 관찰, 나머지 **1,739는 `unknown`**; 전체 NO라고 단정하지 않는다. 기존 원본 parent JSON을 직접 열기 전 verified로 올리지 않는다.
4. `B_NO_ELEMENTS_3.csv` 3개는 원본 `elements` 부재를 보존하고 E단계 특수 렌더 후보로 이관하되, 렌더 의미는 확정하지 않는다.
5. B의 새 진행분은 original `asset_type/source_path/git_blob_sha`, parent chain SHA, from/to, rotation, flat, cullface, bbox 전/후 구분(회전 후 미계산)을 검증해 저장한다. C(UV/PNG), D(blockstate), E(특수 renderer), F(스타일), G(최종 검수)를 B 완료에 섞지 않는다.
6. GitHub 커밋 후 원격 readback; 독립 검증 결과 기록. B1 population index 재완료, B2~B4 미완료 유지.
