# Minecraft Furniture Style Research — 1-2-B Entry7 원본 JSON 기하·상속 검증

> 2026-11-15 KST · Minecraft Java Edition 1.21.11 · GitHub 기준 HEAD `f4ce528949c04df0bf968fa30f0a094fee59560e`
>
> **B_IN_PROGRESS_ENTRY7**, 1-2-A = **A_COMPLETE_SOURCE_SCOPE**. 기존 1-1 승인 150/150 및 전체 상위 1/5, 원본 v69 544×393/544×70과 Entry1~6 결과는 보존.

## 실제 수행한 연구

Entry6의 `B_SCOPE_2390_STATUS.csv`를 기준으로 B-first 미검증 1,356개 중 **신규 240개(P1 48, P2 96, P3 96)**를 우선순위×그룹 층화·파일명 결정적 균등 간격으로 선정했다. 확률 표본이 아니므로 전체에 일반화하지 않는다.

- **leaf 모델 240/240개 Git 원본 Blob SHA 직접 읽기·JSON 파싱.**
- 기존 Entry1~6에서 직접 읽은 원본 JSON 증거를 해시와 함께 재사용하고, 이번에 없던 부모 템플릿 **5개 원본**을 추가 직접 읽음.
- **부모 chain 240/240 해결**, 원본 경로/해시 불일치·부모 누락·상속 순환 **0건**.
- 이번 leaf 240개 중 과거 부모 원본으로 이미 열람된 경로 **15개**를 신규 고유 소스 파일 실적에서 제외함. 부모 신규 고유 경로 5개 포함, 원본 JSON 고유 경로 **1,088 → 1,318(순증 230)**.
- 자체 source `elements`가 유효 기하를 제공 **40개**, 부모 기하 상속 **195개**, 일반 source 요소 부재 **5개**.

## 원본 기하 관찰 (leaf별 적용 값)

| 구분 | Entry7 |
|---|---:|
| `elements` 인스턴스 | 615 |
| 선언 `faces` 참조 | 2,583 |
| 선언 `cullface` 참조 | 1,005 |
| 0두께 `from/to` 요소 | 203 |
| `rotation` 있는 요소 | 165 |
| 0~16 밖 원본 좌표 요소 | 43 |
| `from > to` 좌표 역전 요소 | 3 |
| 사용된 고유 geometry provider | 100 |

값은 부모 모델을 재사용하는 각 leaf에 적용한 **반복 포함 인스턴스 수**다. 고유 원본 기하 선언 수, UV나 렌더 통과 수가 아니다.

원본 좌표를 변경하지 않은 역전 사례:
- `cube_bottom_top_inner_faces` 자체 요소 1개
- `trial_spawner_active`가 `cube_bottom_top_inner_faces`를 상속해 적용한 요소 1개
- `vault_active`가 `template_vault`를 상속해 적용한 요소 1개

이는 실제 런타임 오류가 입증되었다는 주장이 아니다. `INVERTED_COORDINATE_ELEMENTS.csv`에 provider·좌표와 SHA를 기록했다. C/E에서 렌더 해석 인계.

일반 `elements` 부재 5개: `mangrove_sign`, `pale_oak_sign`, `pitcher_crop_top_stage_2`, `light_07`, `light_12`. 게임에서 보이지 않는다는 주장은 아니며, E의 특수 표현 및 D blockstate 검증 대상으로 넘긴다.

## 누적 B-first 상태

| 범위 | 원본 source 계보 검증 | 남은 미검증 |
|---|---:|---:|
| P1 (B 담당) | **249 / 514** | 265 |
| P2 | **500 / 1,039** | 539 |
| P3 | **495 / 807** | 312 |
| **전체 B-first** | **1,244 / 2,360** | **1,116** |

P2/P3의 P1 조상 의존성 **995/1,846 소스 계보 검증**, 해당 995개에서는 no 995, yes 0. 미확인 **851개는 unknown을 유지**. B-first 일반 기하 있음 1,215 / 일반 `elements` 없음 29. E-first P1 30개는 기존 소관 유지.

## 독립 감사 및 제한

`B_ENTRY7_AUDIT.json` 원본 SHA·모델 복합키·parent chain·기하 요소 참조·행수·수치 재계산·기존 행 비변경 **49/49 PASS**. **B1 범위 색인 PASS, B2/B3 부분, B4 독립 종료감사 PENDING**.

이 작업은 원본 JSON의 geometry만을 입증한다. **UV/실제 PNG = 1-2-C**, **blockstate 조합 = D**, **특수 렌더 엔진 = E**, **스타일화 = F**, **최종 감사 = G**이다. 아직 B 완료 또는 3D 제작/좀보이드 변환을 선언하지 않는다.

### 주요 파일
`B_ENTRY7_SELECTION.json`, `DIRECT_SOURCE_PROOF_240_5.json`, `MODEL_GEOMETRY.csv` (240), `ELEMENTS.csv` (615), `NEW_PARENT_SOURCES.csv` (5), `GEOMETRY_PROVIDER_REUSE.csv` (100), `B_NO_ELEMENTS_SOURCE.csv` (5), `INVERTED_COORDINATE_ELEMENTS.csv` (3), `B_SCOPE_2390_STATUS.csv` (2,390), `B_ENTRY7_AUDIT.json` (49/49), `B_ENTRY7_SUMMARY.json`, `B_NEXT.md`.

원격 커밋 SHA·파일 행수 재조회와 기성 역사 자료 보존은 `B_ENTRY7_POST_COMMIT_VALIDATION.json`에서 최종 검증.
