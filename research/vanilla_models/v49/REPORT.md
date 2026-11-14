# v49 — 1-2-A 화분 37종·선반 21종·부모 1종의 원본 출처/상속/UV/블록상태 교차 검증

> 연구일: 2026-11-14 (KST) · 작업 시작 GitHub main HEAD `3dbf1c4b1e5ce27225a0643c9d36687a50ae223a` · 사용자 제공 Minecraft Java **1.21.11** 추출 원본 기준. **기존 v1~v48 자료는 수정/삭제하지 않고 계승했다.**

## 1. 기존 v48과 중복을 제거한 신규 연구

v48 P1 544개 원장에서 `v48_source_path_SHA_linked=false`인 모델 중 가구 디자인과 직접 관계있는 59개 전체 경로를 실제 원본 모델 JSON에서 읽고, **자산 종류 + 전체 source 경로 + Git blob SHA**로 일치 확인했다.

- **화분 leaf 37경로**: 이 가운데 6개(`potted_closed_eyeblossom`, `potted_dandelion`, `potted_fern`, `potted_open_eyeblossom`, `potted_pale_oak_sapling`, `potted_torchflower`)는 **v47/09_POTTED_CHILD_LEAF_6.json에서 이미 직접 검사한 정확한 원본 SHA**를 재확인한 **이전 근거 회수**다. 원장에는 새로 연결하지만 *새로운 원본 분석 6건으로 계산하지 않는다*. 다른 화분 31경로는 이번에 새로 직접 열람했다.
- **선반 leaf 21경로**: `crimson_shelf`, `dark_oak_shelf`, `spruce_shelf` 각각 7경로. 모델별 독립 SHA, `parent`, `textures.all`, `textures.particle` 원본을 직접 확인했다. leaf 자체에는 `elements` 선언이 없다.
- **부모 템플릿 1경로**: `template_potted_azalea_bush`는 실제 P1 모집단에 들어 있고 이전 v48 SHA 미연결이었다. 정확한 원본 SHA로 확인하고 새 고유 P1 경로로 연결했다. 이미 조사된 부모 세 개(`flower_pot_cross`, `flower_pot_cross_emissive`, `tinted_flower_pot_cross`)는 v47 원본 SHA와 교차 검증만 하며 **신규 원형으로 부풀리지 않았다**.

결과: **P1 누적 171 → 230개 경로 SHA 연결**, 조사한 선택+직접 자료에서 미연결 **373 → 314개**. 이번에 연결한 59개 중 **53개는 이번 신규 직접 소스 조사, 6개는 v47 기존 직접 증거 재연결**이다. 230/544는 *정확한 source 연결 상태*이지 1-2 전체 완료율이 아니다.

## 2. 화분 37종 — 상속과 예외를 원본으로 검증

부모/소스별 원형을 구분했다.

| 유형 | leaf 수 | 원본 관찰 |
|---|---:|---|
| `flower_pot_cross` 상속 | 30 | parent 기하 재사용, `plant` 텍스처 override |
| `tinted_flower_pot_cross` 상속 | 1 | v47의 tinted 부모 원형 재사용 |
| `flower_pot_cross_emissive` 상속 | 1 | `plant` 및 `cross_emissive` override |
| `template_potted_azalea_bush` 상속 | 2 | 새로 경로 SHA 연결한 12 elements/36 명시 UV 얼굴 부모 |
| **자체 `elements` 선언** | **3** | `potted_bamboo` 7요소/29면, `potted_cactus` 2요소/11면, `potted_mangrove_propagule` 9요소/30면 |

3개 자체 요소 모델과 추가 부모 템플릿 1개의 **원본 직접 선언 총계는 30 elements, 106 faces (원본 명시 UV 100 / 원본 UV 키 없는 암시 UV 6)**. 암시 UV 6개는 전부 `potted_cactus.json`에서 확인했다. 30요소의 0두께 원본 요소 11개, 회전 선언 원본 요소 6개도 별개 기록했다.

각 leaf에 부모/자체 기하를 실제 연결해 **효과적으로 적용되는 면 참조 978건**을 만들었다(명시 UV 참조 972 / 암시 UV 참조 6). 출처 텍스처 슬롯은 **978/978** 소스 JSON 참조에서 해결됐지만 **원본 PNG 화소나 알파가 확인됐다는 뜻은 아니다**. 978은 parent faces를 leaf에 *반복 적용한 건수*이며 **978개의 독립 원본 선언면이 아니다**.

또한 화분 37종의 `blockstates/<leaf>.json` 원본을 **37개 직접 읽고**, 각 블록상태에 단일 `variants` 모델 참조가 해당 leaf를 정확히 가리킴을 확인했다. 인게임 런타임/렌더러는 확인하지 않았다.

## 3. 선반 21종 — 공통 기하 원형 재사용 확인

3목재 × 7 leaf가 각각 `template_shelf_body/center/inventory/left/right/unconnected/unpowered`를 상속하고, 부모 원본 7개 SHA는 v38/v48에 확인된 원형과 **7/7 일치**했다.

부모의 기존 원본 **11 elements/38 faces**를 신규 모델 21개에 곱해 신규 기하 원형으로 계산하지 않았다. 부모 면을 상속/텍스처 override로 해석해 **114개의 leaf-face 적용**을 기록했고, 모든 면의 텍스처 슬롯을 각 목재별 `textures.all` 소스에 연결했다. PNG 실화소 검증은 수행하지 않았다.

세 원본 블록상태(`crimson_shelf`, `dark_oak_shelf`, `spruce_shelf`)는 각각 **24개 multipart 규칙**. 각각 `facing 4 × powered 2 × side_chain 4`의 **32개 정적 조건**을 평가해 조합당 2개 모델 적용, 곧 **64건**의 파생 적용을 확인했다. 세 블록상태 합계는 **원본 72규칙, 파생 96조합, 모델 적용 192건**이다. 이는 가능한 정적 조건 평가이며 실제 게임의 모든 상태 도달 가능성이나 3D 런타임 검증이 아니다.

## 4. 근거 수준/한계와 중복 처리

`(asset_type, full_source_path, git_blob_sha)`로 서로 다른 모델 경로를 별개의 출처로 식별한다. v46의 동일 blob SHA를 공유하는 여러 모델 경로와 v43의 model/blockstate 자산 타입 오탐 해결도 보존한다.

모델별 544행 원장에는 **선택적 역사 SHA 연결 / 직접 새 소스 확인 / v47 과거 근거 재회수 / 부모 기하 재사용 / 명시·암시 UV / 원본 블록상태 / PNG·엔진 보류**를 각각 구분해 기록했다. 기존 v5~v8 SQLite/스크립트 및 v5~v43 과거 보고서·CSV·JSON 증거를 신규 연구로 재집계하지 않는다.

실제 PNG RGBA 픽셀 검수 0건, 엔진/인게임 렌더 실증 0건. 공식 압축 client.jar 인증도 사용자 지정 범위에서 필수 완료 조건이 아니므로 수행하지 않았다. **1-2-A 및 1-2 전체 미완료, 완료율 미산정**, 1-1의 승인 텍스처 150/150 완료와 상위 5개 과제 **1/5 완료 유지**. 실제 가구 모델 제작/Project Zomboid 변환은 시작하지 않는다.

## v49 결과 파일

`01_P1_544_EVIDENCE_LEDGER.csv`, `02_POTTED_37_SOURCE_AND_SLOTS.csv`, `03_POTTED_37_EFFECTIVE_FACE_BINDINGS.csv`, `04_POTTED_37_RAW_SOURCE_MODELS.json`, `05_POTTED_TEMPLATE_PARENTS_4_SOURCE.json`, `06_POTTED_NEW_GEOMETRY_106_SOURCE_FACES.csv`, `07_SHELF_21_SOURCE_AND_SLOTS.csv`, `08_SHELF_114_INHERITED_FACE_BINDINGS.csv`, `09_SHELF_3_BLOCKSTATES_MULTIPART.json`, `10_POTTED_37_SOURCE_BLOCKSTATES.csv`, `11_SHELF_PARENT_TEMPLATES_7_VERIFIED.json`, `12_POTTED_NEW_GEOMETRY_30_ELEMENTS.csv`, `13_NEW_P1_59_TYPED_LINKS.csv`, `14_ISSUES.csv`, `SUMMARY.json`, `NEXT_CHAT_HANDOFF.md`, `REPORT.md`.
