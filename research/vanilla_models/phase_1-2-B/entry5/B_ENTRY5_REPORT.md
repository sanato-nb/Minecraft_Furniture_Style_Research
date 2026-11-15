# Minecraft Java 1.21.11 — 1-2-B Entry5 직접 원본 기하·부모 상속 조사

> 작업 기준 2026-11-15 KST · 시작 main `2706d206b01a03fa86ed7c7d6b133f4dd8ae8da5` · **B_IN_PROGRESS_ENTRY5** · **B 전체 미완료** · 기존 연구 체크포인트 **v69** 보존

## 실제 수행한 원본 소스 조사

이전 Entry1~4에서 직접 검증된 B-first leaf **524개는 신규 검증분에서 제외**했다. `entry4/B_SCOPE_2390_STATUS.csv`의 미검증 B-first **1,836개**에서 우선순위×그룹 13개 층의 남은 수에 비례해 균등 위치 선정했다. 선정된 **240개**는 **P1 48개, P2 96개, P3 96개**이고 무작위·통계적 대표 표본이 아니다. 경로와 Git Blob SHA는 `B_ENTRY5_SELECTION.json` 참조.

이번 Entry5에서 원본 Minecraft Java1.21.11 모델 **leaf 240개 Git Blob 직접 조회·JSON 파싱**, 추가로 필요한 **부모 12개 Git Blob 직접 조회·파싱**. Entry1~4에서 원본을 확인했던 parent JSON은 기존 원본 SHA 증거를 재사용했다. 전체 **240/240 부모 chain 끝까지 확인**, source SHA 충돌·부모 누락·부모 순환 **0건**. 완전한 원본 경로·SHA와 JSON을 `DIRECT_SOURCE_PROOF_240_12.json`에 기록.

Entry5 leaf 240개 중 **12개 원본 경로는 과거에 상속 부모의 원본으로 이미 읽은 자료**이므로 고유 소스 신규 실적에서 차감했다. 신규 부모12개는 과거 원본에 없는 경로였으므로 B 누적 고유 원본 JSON 경로는 **615 + (240 − 12 + 12) = 855개**다. 파일 정체 확정에 대한 신규 credit은 0.

## source JSON 기하 관찰

- **자체 `elements` 소스 33개**, 부모 상속 소스 **201개**, 일반 `elements` 소스 없음 **6개**.
- leaf별 적용 인스턴스 **요소 550개**, 원본 면 선언 참조 **2,306회**, 선언된 cullface 면 참조 **980회**, 두께 0 요소 **172개**, 원본 rotation 선언 요소 **145개**.
- 소스 기하 제공자 경로 **108개**. 해당 요소 중 **36개**는 원본 모델 좌표의 0~16 범위 밖 수치가 있으며, **4개**는 하나 이상의 축에서 `from > to`인 역방향 좌표를 포함한다. 원본값을 정규화·삭제하지 않는다.
- 역방향 요소가 적용된 leaf 예: `spawner` (부모 `cube_all_inner_faces`), `template_vault`, `trial_spawner_active_ominous` (부모 `cube_bottom_top_inner_faces`), `vault_ejecting_reward` (부모 `template_vault`). `INVERTED_COORDINATE_ELEMENTS.csv`에 원본 좌표와 제공자 SHA를 기록했다.
- 기하 및 bbox는 모두 **원본 JSON의 회전 전** 기준이다. 게임이 해당 면을 어떤 방향으로 표시하는지, blockstate를 통해 회전하는지, 픽셀이 어떻게 UV 맵핑되는지는 **C·D·E에서 별도로 확인**한다. 재사용된 원본 템플릿 요소·면을 leaf별로 적용한 **중복 포함 참조 수**이므로 원본 고유 요소 550개 발견이라는 뜻이 아니다.

## 특수 원본 예외 6개 (E 렌더 검토 후보)

`birch_hanging_sign`, `mangrove_hanging_sign`, `moving_piston`, `lava`, `light_06`, `light_14`. 부모 계보에서 일반 `elements`를 찾지 못했다. **게임에서 보이지 않는다거나 렌더링할 수 없다는 확정은 아니다.** `B_NO_ELEMENTS_SOURCE.csv`로 별도 저장하고 1-2-E에 인계한다.

## B-first 누적 소스 검증 상태

| 대상 | 직접 검증 | 남은 leaf |
|---|---:|---:|
| P1 / B-first | **153 / 514** | 361 |
| P2 | **308 / 1,039** | 731 |
| P3 | **303 / 807** | 504 |
| **B-first 전체** | **764 / 2,360** | **1,596** |

P1 E-first **30개는 제외·별도 보존**. B-first 중 일반 원본 기하 제공자가 확인된 모델은 **746개**, 일반 source elements가 없는 특수 원본 예외는 누적 **18개**. P2/P3의 부모 계보에서 P1 조상 여부를 직접 확인한 **611/1,846개는 'no'**, 미검증 **1,235개는 unknown**으로 보존한다. 아직 전체 모델을 검증하지 않았으므로 B 완료율·의미 해석 확정율로 바꾸지 않는다.

## 독립 교차검사 및 종료 조건

`B_ENTRY5_AUDIT.json`의 **41/41 PASS**: 원본 Git SHA·대상 선정, 2,390행 기존 범위 보존, 이전 524행 불변, 240개만 갱신, 기하 요소·면 원장 집계, 부모 JSON 12개, 특수 소스 예외6개, P2/P3 unknown 보존.

- **B1 PASS**: 원본 모집단 및 담당/증거 등급 인덱스만.
- **B2 PARTIAL**: B-first 원본 부모 검증 **764/2,360**; P2/P3 **611/1,846**.
- **B3 PARTIAL**: 기하 소스 746개 + source elements 없음18개로 분리; 미확인 B-first 1,596개.
- **B4 PENDING**: 전체 독립 종료검수는 아직 수행할 수 없음.

원본 v69 P1 544×393 및 review 544×70, A 종료 기록, 이전 Entry1~4 연구 파일, 1-1 승인150/150, 상위 연구 1/5는 유지한다. UV/PNG(C), blockstate(D), 엔진 렌더러(E), 시각 스타일(F), 최종 검수(G), 실제 마크 가구 모델·좀보이드 맵 제작은 이 작업에서 처리하지 않았다.

## 저장 산출물

`B_ENTRY5_SELECTION.json`, `DIRECT_SOURCE_PROOF_240_12.json`, `MODEL_GEOMETRY.csv` 240행, `ELEMENTS.csv` 550행, `NEW_PARENT_SOURCES.csv` 12행, `GEOMETRY_PROVIDER_REUSE.csv` 108행, `B_NO_ELEMENTS_SOURCE.csv` 6행, `INVERTED_COORDINATE_ELEMENTS.csv` 4행, `B_SCOPE_2390_STATUS.csv` 2,390행, `B_ENTRY5_AUDIT.json` 41/41, `B_ENTRY5_SUMMARY.json`, `B_NEXT.md`. 원격 SHA 검증 결과는 추후 `B_ENTRY5_POST_COMMIT_VALIDATION.json`에 별도로 기록.
