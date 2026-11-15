# 1-2-B 첫 진입 코호트 — 실제 원본 모델·부모 상속 기하 판독

> 2026-11-15 KST · GitHub `main` 기준 `7f2e72ff2f9d3681242959536d475dc8a93062b0` · Minecraft Java 1.21.11.
> 기존 `WORK_PLAN.md`의 B 범위를 실행. **B 전체 미완료**; A는 완료 상태 유지.

## 실제 작업

- A에서 확정한 2,390개 block model 모집단 중 최초 담당 B는 **2,360(P1 514/P2 1,039/P3 807)**, 특수 예외 E-first P1 30개.
- 원본 leaf JSON **14개를 Git Blob SHA로 직접 조회/파싱**: P1 **3**, P2 **8**, P3 **3**.
- 직접 연결된 원본 부모 템플릿 **13개**를 Git Blob SHA로 조회/파싱. 각 14개 leaf에서 부모 chain을 끝까지 따라가 총 **14/14 연결 완료**, 누락·순환·SHA 오류 0.
- 상속받는 leaf **13개**, 자체 `elements`를 선언한 leaf **1개**(`stonecutter`). 원본 JSON만으로 확인한 파생 적용 요소 인스턴스 **17개**, 적용되는 원본 face 선언 참조 **84개**, 0두께 요소 인스턴스 **3개**(`stonecutter` 1, `iron_bars_post` 2). **이 수치는 새로운 고유 소스 요소·면 17/84개를 발견했다는 의미가 아니다.** 여러 leaf가 동일한 부모 템플릿 요소를 반복 참조하므로 중복을 포함한다.
- P2/P3에서 직접 추적한 **11개** parent chain의 P1 조상 여부만 소스 기반으로 기록했다. P2/P3 전체 1,846개 완료 아님.
- 실제 회전된 세계 공간/PNG UV/엔진 렌더링은 아직 검사하지 않았다. `bbox`는 원본 좌표의 **회전 전** min/max.

## 관찰된 구조의 예시

- `bookshelf` → `cube_column` → `cube` → `block`: leaf 자체 element 없음, 부모 `cube`의 정육면체 1개·6면 상속.
- `crafting_table` → `cube` → `block`: 부모 큐브 1개·6면.
- `oak_stairs` → `stairs` → `block`: 원본 부모 elements 2개·11면 선언을 상속.
- `acacia_button` → `button`: 폭 6, 높이 2, 깊이 4 원본 좌표, 부모 elements 1개·6면.
- `acacia_button_pressed` → `button_pressed`: 부모 요소 높이 **1.02** (원본 수치이며 임의로 1로 반올림하지 않음).
- `iron_bars_post` → `template_bars_post`: 축 하나가 두께 0인 두 요소·양면 총 4면.
- `stonecutter`: 자체 elements 2개·8면 중 하나는 한 축 길이 0인 날 형상.
- `oak_door_bottom_left` → `door_bottom_left`: 한쪽이 얇은 판 형태의 원본 기하를 부모에서 상속.

이 중 일부 구조는 v44~v69 과거 연구에도 해당 계열의 선행 근거가 있다. 이번 14개는 **B 진입 이후 소스 직접 재검증**이고, 신규 모델 정체 발견수는 0이다.

## 근거·산출물 및 검수

- `MODEL_GEOMETRY.csv`: 14개 leaf parent chain(모든 소스 원본 SHA 포함), 원본/상속 구분, 요소·면·zero thickness·cullface, 회전 전 bbox, P1 조상 포함 여부.
- `ELEMENTS.csv`: leaf별 17 요소 인스턴스의 source from/to, 요소 제공자 SHA, 회전/cullface/face 방향.
- `PARENT_TEMPLATE_SOURCE.csv`: 실제 조회된 부모 원본 13개.
- `B_ENTRY1_AUDIT.json`: 자동 무결성 확인 및 B-stage 진행 상태.

B의 완료율을 14/2,360으로 계산하지 않는다. 별도 B1~B4 종료 게이트 전부 미달이며, 전체 프로젝트 상위 완료 **1/5**·1-1 **150/150** 유지. 가구 제작/PZ 변환 미착수.
