# v43 — 바닐라 1-2 자동 제작기 원본 3D 모델/UV/blockstate 검증

> 2026-11-14 KST · 사용자 제공 Minecraft Java 1.21.11 추출본 Git 소스 기준 · **공식 압축 JAR SHA 및 인게임 렌더/런타임 검증은 수행하지 않았으며 필수 범위에서도 제외**.

## 기존 증거 계승과 중복 제외
- v42의 **1-1 지정 11재질·150 PNG 소스 완료**는 변경 없음. v39~v42 및 TEXnn-Rxxx 원본 보존, 신규 PNG/RGBA 분석 0.
- v34 전체 block model JSON 2,390 인벤토리, **P1 544 후보**는 정밀 분석 완료 수가 아님. v35 직접 15 + v36 직접 6 + v38 직접 7 = 기존 선택 leaf 28개; v37은 정적 PNG 실화소 11개·34 face 검사이며 새 leaf 없음.
- **v31 조각된 책장 7 요소 및 blockstate 256 조합은 이미 완료된 자료**. 이번에 원본을 재조회했지만 신규 상태나 UV 실적으로 재계상하지 않는다. v38 오크 선반 7 leaf/32상태도 중복 계상하지 않음.
- v36 P1 역사적 교차표는 v5~v34의 선택 18 CSV와 대조한 1차 표. 446 미매칭을 전부 미조사라고 간주하지 않는다.

## 신규 직접 연구: crafter 4 leaf
사용자 GitHub `1.21.11/assets/minecraft/models/block/`의 `crafter`, `crafter_triggered`, `crafter_crafting`, `crafter_crafting_triggered` **네 원본 JSON을 실제로 직접 읽음**. 각각 Git blob SHA를 v34/v35 P1 목록과 대조해 **4/4 일치**. v36 선택 역사 증거에서 4개 모두 이전에 `v34_queue_only_no_direct_evidence_in_selected_sources`로 남은 것을 확인했음. (다른 v5~v34 미선택 문서까지 최초 여부를 확정한 건 아님.)

| 원본 leaf | 자체 elements | 부모 | 소스 텍스처 슬롯 변경 |
|---|---:|---|---|
| `crafter` | 1 | `block/block` | bottom/top/north/south/west/east, particle=#north |
| `crafter_triggered` | 0 | `block/crafter` | top/south/west/east 4 |
| `crafter_crafting` | 0 | `block/crafter_triggered` | top/north/east/west 4 |
| `crafter_crafting_triggered` | 0 | `block/crafter_crafting` | 없음 |

- **기하 원형 1개** [0,0,0]→[16,16,16] 큐브, **원본 선언 faces 6개**, `uv:[0,0,16,16]` 여섯 면에 모두 명시, `up`에만 `rotation:180`, 여섯 면에 `cullface` 원본 명시. 총 4 leaf × 6 상속 face = **24 face×material 원본 연결 기록**. 원본 선언 24면 또는 픽셀 실측 24건 아님.
- `crafter_triggered`가 상단/남/서/동만 재정의하므로 북/바닥은 기본 텍스처 그대로임.
- `crafter_crafting`이 상단/북/동/서를 재정의하고 **남쪽은 `crafter_south_triggered`, 아래는 `crafter_bottom`을 상속**.
- `crafter_crafting_triggered`는 새 texture/elements가 없는 별도 leaf. 따라서 **4 leaf 파일이지만 상속을 모두 해석한 면별 텍스처 조합은 3종**. 두 crafting leaf의 기하·면별 texture 경로 동일(소스상 판정); 실게임 렌더 동일성 증명 아님.

## 48개 원본 blockstate 정적 규칙 검수
- `blockstates/crafter.json` SHA `2de2b178a8988ffcb25aa40fc5866aed908519cf`를 직접 읽음. `orientation` **12** × `crafting` **2** × `triggered` **2** = **48개 source variant** 전수 파싱, 적용된 모델 참조 48/48 원본 4 leaf에 해소.
- 12 방향: down_east, down_north, down_south, down_west, east_up, north_up, south_up, up_east, up_north, up_south, up_west, west_up.
- 모든 원본 규칙의 `uvlock` **키 부재 48/48**; `x`, `y`도 상황에 따라 키 부재. 미기재를 원본에 명시된 false 또는 0으로 바꾸지 않았다. 원본 x/y 값은 CSV 개별 기록.
- `crafting=false`일 때 triggered에 따라 기본/triggered 소스 모델 분기, `crafting=true`일 때 다른 leaf 2종을 택하지만 최종 텍스처 바인딩은 같다. 조건별 GPU 회전/컬링/동작은 미검증.
- **6면×48 상태=288 face instance**는 선언면을 반복 적용한 정적 구조 파생 계산이며 새로운 독립 원본 UV 선언 288개 또는 텍셀 검증 288회가 아니다.

## v36 SHA 충돌 기록 2건의 출처 유형 오탐 발견
v36이 같은 모델명에 서로 다른 SHA라고 적은 `chiseled_bookshelf`, `oak_shelf`는 **v7의 blockstates 경로와 v34 모델 경로를 basename만으로 비교한 오탐**.
- 책장 v7 `0c9b22...`은 **blockstates/chiseled_bookshelf.json**; 비교 모델 `a9bda72...`은 **models/block/chiseled_bookshelf.json**. v7 원장에는 후자의 모델 SHA도 같은 값으로 존재.
- 선반 v7 `404c901...`은 **blockstates/oak_shelf.json**; 비교 모델 `4b0f3db...`은 **models/block/oak_shelf.json**. 다른 종류의 원본 파일.
- 기존 v36 원장 원본 수정 없이 v43 경로 포함 별도 정정 증거로 기록. **다른 SHA 상충 전체가 해결됐다는 주장 아님**.

## 범위 및 검증 결론
이번 **직접 검사 새 leaf 4개**, 블록상태 48행, 상속 기하/UV/face texture 24행, 역사적 SHA 이름충돌 오탐 2건. 기존 v35~v38의 28개 + 이번 4개 = **선택한 실행 회차 기준 서로 다른 직접 leaf 32개**로 대조했지만, v5~v34 전체 역사 증거 완전 재조정은 미완료. P1 544의 완료 퍼센트 **미계산**.
원본 PNG 실제 RGBA/아틀라스 texel·공식 JAR/인게임 애니메이션·실 렌더 검증 **이번 0건**. 최신 단계 STATE에 따라 애니메이션 소스는 9재질 재개, 1-1-02/1-1-10 보류. v38의 과거 전면 보류는 현행 지시 아님.
다음 연구: P1 전체 역사 문서에서 경로+SHA별 정합 교차, 미조사 family의 원본 JSON/상태, 선택 UV에 원본 픽셀 추가 연결. 실제 가구 모델 제작과 Project Zomboid 변환은 범위 밖.

## 증거 목록
[4 leaf SHA/부모](01_crafter_four_leaf_sha_parent.csv) · [48 source states](02_crafter_48_original_variant_rules.csv) · [24 face texture/UV](03_crafter_24_inherited_face_texture_bindings.csv) · [v36 오탐 수정](04_v36_sha_conflict_path_type_audit.csv) · [검증 JSON](05_v43_source_validation.json).
