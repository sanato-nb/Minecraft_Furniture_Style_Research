# Minecraft Java 1.21.11 — 1-2-B Entry2 원본 부모상속·기하 진척 보고서

> 2026-11-15 KST · GitHub `main` 출발 SHA `f8c095d954ce29d4f361fd1736e54c9354dae1f7`. 기존 1-2-A `A_COMPLETE_SOURCE_SCOPE`, 연구 체크포인트 **v69** 유지.  
> **현재 1-2-B: 진행 중(미완료).** 기존 `docs/vanilla_models_1-2/1-2-B_WORK_PLAN.md`의 B1~B4 범위와 1-2-A 인수인계를 적용.

## 1. 직접 수행한 작업과 확인 가능한 증거

- 기존 Entry1 leaf 14개와 겹치지 않는 **120개 원본 모델 JSON**을 GitHub Git Blob SHA로 직접 조회·JSON 파싱: **P1 24 / P2 48 / P3 48**.
- 1-2-A의 그룹 ID에 따라 P1 네 그룹·P2 다섯 그룹·P3 네 그룹에서 균등 위치 표본을 선정(총 **13개 P×그룹 층**). 무작위/통계적 대표 표본이라는 주장은 하지 않는다. 선정 근거는 `B_ENTRY2_SAMPLE_SELECTION.json`.
- 각 leaf의 실제 `parent` 문자열을 복합키 `(asset_type, full_source_path, git_blob_sha)`에 연결, 부모 템플릿 JSON **43개 추가 직접 열람**, Entry1 기존 자료와 합쳐 **120/120 상속 계보 끝까지 추적**, SHA 누락/잘못된 경로 **0건**.
- Entry1에서 이미 열람한 부모(`cube`, `block` 등)는 재사용했으며 일부 Entry2 leaf는 과거 템플릿과 동일 소스(예: `cube_column`)이므로 중복 원본 파일을 새로운 고유 발견으로 집계하지 않는다.
- 원본 요소 자체 선언 **27개 leaf**, 부모로부터 elements를 상속 **90개 leaf**, 계보 전체에서 `elements` 선언 없는 모델 **3개 leaf**.
- `elements` 적용 인스턴스 **333개**, 그 인스턴스에 따른 원본 face 선언 **1,300회 참조**, 0두께 요소 인스턴스 **122개**, `rotation`이 원본 JSON에 있는 인스턴스 **92개**. 이것은 고유한 333개 원본 요소/1,300개 고유 면 선언이 아니라 **leaf별 적용·중복 포함 총수**.
- 고유 source geometry provider 경로 **71개**, 그 제공자의 요소 선언 단순합 **238개**, 면 선언 단순합 **872개**. 이는 방문 모델에 나타난 제공자만의 합계이며 모든 바닐라 모델 소스의 고유 요소 총계가 아니다.
- 원본 `from/to`의 최소·최대 좌표는 **회전 전 bbox**이며 월드 상태별 회전·blockstate 최종 조립은 D로 이관. UV/PNG는 C, 실제 렌더러는 E.

## 2. 구조 증거 사례

| leaf | 원본 parent/geometry 출처 | 관찰 |
| --- | --- | --- |
| `bamboo_shelf_unconnected.json` | `template_shelf_unconnected.json` | 원본 두께 0 요소 1개와 face 1개를 상속 |
| `powder_snow_cauldron_level1.json` | `template_cauldron_level1.json` | 원본 요소 14개·face 59개 선언 재사용 |
| `blue_candle_three_candles_lit.json` | `template_three_candles.json` | 요소 9개, 0두께 6개, 회전 명시 6개(동일 소스의 파생 적용) |
| `orange_candle_four_candles.json` | `template_four_candles.json` | 요소 12개, 원본 face 40개, 두께 0인 요소 8개 |
| `tripwire_nsew.json` | 자기 모델 원본 | 원본 elements 8개·face 16개; 8개 요소 모두 한 축 두께 0 |
| `four_sea_pickles.json` | 자기 모델 원본 | 원본 elements 16개·face 44개, 두께 0 요소 12개 |
| `carrots_stage2.json` | `crop.json` | 0두께 요소 4개·face 8개를 부모에서 상속 |

## 3. 특별히 미확정한 3개

`end_gateway.json`, `weathered_copper_golem_statue.json`, `light_08.json`: leaf부터 상위 parent 계보까지 일반 `elements` 배열이 없다. 이 사실은 직접 JSON으로 확인했지만 **엔진이 실제로 보이지 않는다거나 해당 모델이 렌더되지 않는다는 증명이 아니다.** 블록엔티티/특수 표현 여부는 E에 문의, B는 source-only 예외로 유지한다. `B_NO_ELEMENTS_3.csv`를 참조.

## 4. 1-2-B 전체 범위 상태 원장(2,390행)

A 확정 모집단 전체를 `B_SCOPE_2390_STATUS.csv`로 **비파괴 재색인**했다. 이는 전체 JSON 2,390개를 신규 직접 읽었다는 의미가 아니라 정확한 담당자·읽은 증거 등급을 분리한 것이다.

| 구분 | 출처로 실제 확인된 수 | 아직 B 직접 source 계보 미확인 |
| --- | ---: | ---: |
| B-first 전체 (2,360개) | **134** (Entry1 14 + Entry2 120) | **2,226** |
| B-first P1 (514개) | **27** | **487** |
| P2+P3 (1,846개) | **107** (Entry1 11 + Entry2 96) | **1,739** |
| P1 E-first 별도 예외 | **30개 전체 E에 보존** | B-first 분모 제외 |

P2/P3 검증된 107개의 계보에서 P1 모델 조상은 직접 검사 범위상 **0개**였고, 107개는 `no`, 나머지 1,739개는 **`unknown`** 그대로 두었다. 이 값은 표본 관찰일 뿐 전체 1,846개의 부모 의존성 해소가 아니다.

직접 증거가 있는 B-first 모델 134개 중 **131개는 원본 기하 제공자가 확인**, **3개는 elements 없음**(E 의심·추가 확인). 실제 렌더링·UV·blockstate 상태 인증 모델 수는 이 작업만으로 증가하지 않았다.

## 5. 완료 게이트

- **B1** 범위·원본 SHA·기존 증거 등급·B/E 담당 구분 2,390행 재색인: **PASS (source population/ownership index only)**.
- **B2** 부모 계보: 표본 누적 134 B-first, 이 중 P2/P3 107/1,846: **PARTIAL**.
- **B3** 원본 기하: 131/2,360 provider 확인·3 no-elements 명시, 나머지 미확인: **PARTIAL**.
- **B4** 전체 독립 최종 종료검수: **PENDING**.

**B 완료 선언 금지.** 1-1 승인150/150, 상위 연구 완료1/5, v69 원본 544×393·review544×70 원장은 그대로 유지. 향후 C/D/E/F/G의 검증을 B에서 수행했다고 가장하지 않으며 마크 가구 제작·좀보이드 변환은 시작하지 않는다.

## 6. 산출물 및 재현

`MODEL_GEOMETRY.csv`(120행), `ELEMENTS.csv`(333행), `PARENT_SOURCES.csv`(43행), `GEOMETRY_PROVIDER_REUSE.csv`(71행), `B_SCOPE_2390_STATUS.csv`(2,390행), `B_NO_ELEMENTS_3.csv`(3행), `B_ENTRY2_AUDIT.json`(20/20 PASS), `B_ENTRY2_SAMPLE_SELECTION.json`, `B_ENTRY2_SUMMARY.json`, `B_NEXT.md`를 참조. GitHub 원격 커밋·SHA readback은 별도 사후 검증에서 확인한다.
