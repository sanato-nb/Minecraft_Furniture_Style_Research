# v48 — 1-2-A P1 미연결 모델 36경로 원본 근거 연결과 상속·UV·블록상태 검증

> 2026-11-14 KST · 시작 GitHub `main` HEAD `85acaba266f1887638d388a8b762e6eb6d32fe6f` · Minecraft Java **1.21.11 사용자 제공 추출본**. v1–v47 보존, 1-2-A 계속 진행 중.

## 수행한 직접 검증

### 새로 확인한 고유 P1 경로 36개
기존 v47의 P1 544행 `v47_sha_linked=false`를 기준으로, **서로 다른 모델 전체 경로 및 Git blob SHA**를 원본 `1.21.11/assets/minecraft/models/block/*.json`을 열어 대조했다. 총 **36개 새 연결**.

- **자작나무·벚나무 선반 leaf 14개**: 목재별 7개씩 원본 열람. 각 모델의 `parent`와 `textures.all`/`particle` override를 정확히 보존. 자체 `elements` 선언 없음. 7개 공통 선반 부모의 SHA는 과거 v38·v45·v47 연구 원형과 일치 → *부모 기하 7종을 신규 원형으로 재계산하지 않음*.
- **조각된 책장 관련 모델 10개**: 빈/채워진 슬롯 9개와 `chiseled_bookshelf_inventory` 1개. 슬롯 9개는 원본에서 각 `template_chiseled_bookshelf_slot_*`에 상속하고 `textures.texture`를 empty/occupied로 override. inventory는 자체 **1 element / 명시 UV 6면**을 선언. 기존 연구의 직접 근거와 분리.
- **그 외 모델 9개**: `conduit`, `copper_lantern`, `copper_lantern_hanging`, `copper_torch`, `item_frame`, `item_frame_map`, `glow_item_frame`, `glow_item_frame_map`, `jukebox`. 각각 부모 참조·텍스처 오버라이드·자체 elements 여부 확인. `conduit.json`은 원본에서 `textures.particle`만 있고 `elements`, `parent`가 없어 **정적 JSON으로 실물 구조를 추론할 수 없음**.
- 원래 위 33개 leaf의 부모 직접 확인 중 **P1이면서 v47의 선택 근거에서 SHA 미연결인 부모 3개**(`template_shelf_inventory`, `template_item_frame`, `template_item_frame_map`)도 원본 SHA를 직접 검증하여 별도의 3개 경로 근거로 연결했다. `template_shelf_inventory`의 3 elements / 18 explicit UV faces는 **v38에서 이미 조사한 원본**으로 명시했다.

따라서 33 leaf + 3 부모 = **36 P1 모델 경로**를 이번에 새로 연결함. 다른 부모 템플릿 17개는 별도 조사(이 중 기존 연결 P1 14, P1 모집단 밖의 공통 부모 3)로만 기록. 부모 경로가 기존 P1에 포함되지 않으면 P1 숫자로 계산하지 않는다.

### 원본 기하/UV 분리
이번에 직접 확인한 원본 `elements` 선언은 **14개**, `faces` 선언은 **68면(모두 명시 UV)**이며 `10_OWN_ELEMENT_DECLARATIONS_14.csv`와 `11_OWN_FACE_DECLARATIONS_68.csv`에 각 면의 from/to, UV, 텍스처 슬롯 등 정확한 source 위치를 기록했다.

이 중 `template_shelf_inventory` **3 elements / 18 faces**는 이미 v38 연구 원형을 재확인한 것. 나머지 `template_item_frame`, `template_item_frame_map`, `chiseled_bookshelf_inventory`의 **11 elements / 50 explicit UV faces**는 이번 회차에서 추가로 직접 검증한 모델 원본 선언으로 구분한다. 기존 과거 근거에 이름만 언급된 것을 또 신규 실적으로 올린 게 아니라, 원본 source path+SHA로 검증한 선언이다.

`template_item_frame`과 `template_item_frame_map`은 각 **5 elements / 22 explicit UV faces**. 아이템 액자/지도 액자 자식 leaf에는 직접 선언면이 없으며 해당 부모의 기하를 상속한다. `jukebox`는 `cube_top → cube → block` 상속을 원본별 SHA로 확인했고, 원본 텍스처 override와 부모 선언면/자체 선언면을 혼동하지 않는다.

### 블록상태 원본 및 정적 파생 평가
- `birch_shelf`: 원본 multipart **24규칙**, `facing 4 × powered 2 × side_chain 4 = 32`개 정적 조합, 조합당 2모델 → **64 적용**.
- `cherry_shelf`: 원본 multipart **24규칙**, 동일한 **32조합 / 64 적용**.
- `chiseled_bookshelf`: 원본 multipart **52규칙**, `facing 4 × 6슬롯 점유 bool(2^6)` = **256개 정적 조합**, 각 상태 본체 1 + 6슬롯 6 = **7모델 / 1,792 적용**. `uvlock` 키가 명시된 원본 규칙 4건, 그 외 규칙에는 이 키가 없다. 정적 평가에서 모든 52개 원본 규칙이 최소 한번 선택되었다.
- `copper_lantern`, `copper_torch`, `item_frame`, `glow_item_frame`, `jukebox`, `conduit`에 해당하는 **블록상태 원본 6개**의 variant 구성도 직접 읽었다(각 2/1/2/2/1/1 = 합계 원본 variant 9개).

3개 multipart JSON은 **원본 100규칙**, 모두 정적으로 열거한 **320개 상태 조합** 및 **1,920개 규칙-모델 적용 건수**로 서로 다른 단위를 유지한다. 실제 게임에서 모든 조합이 만들어지는지, 엔진 렌더가 일치하는지 실증한 수가 아님. inventory leaf는 world multipart의 별도 규칙 출처라고 주장하지 않는다.

## v47 → v48 누적 지표

| 항목 | v47 | v48 |
|---|---:|---:|
| P1 고유 모델 경로 | 544 | 544 |
| 선택/직접 근거로 경로+SHA 연결 | 135 | **171** |
| 조사 범위에서 SHA 미연결 | 409 | **373** |
| 신규 모델 원본 경로 직접 조사 | 11 | **36** |
| 본 회차 선언 요소/면 원문 열람 | 26/100 | **14/68** |
| 이 중 기존 원형 중복 재검수(요소/면) | — | **3/18** |
| 이번 신규 직접 검사 요소/면(기존 v38 부분 제외) | — | **11/50** |
| 신규 PNG RGBA/실화소 | 0 | **0** |
| 1-2 실제 전체 완성률 | 미산정 | **미산정** |

171은 모델 **원본 경로+Git blob SHA 연결** 수로, 171모델이 전체 geometry·UV·PNG·blockstate·renderer 분석을 끝냈다는 의미가 아니다. 373개는 이 조사 범위의 **미연결**로, 처음부터 한 번도 분석되지 않았다는 증거가 아니다.

## 주의/미해결
- 자산 비교 키는 `(asset_type, full_source_path, git_blob_sha)`. v43의 모델 vs blockstate 이름 혼동 오탐 2건, v46의 동일 blob 여러 모델 경로 문제를 계속 분리한다.
- 원본 100/68 explicit UV 숫자와 PNG 텍셀, 1,920 파생 적용 횟수는 서로 다른 분모이다.
- 실화소 샘플/알파, 조각된 책장 런타임 상태 유효성, 아이템 액자 실제 아이템 렌더, conduit 특수 렌더러는 미검증.
- **1-1 바닐라 승인된 150 텍스처 완료, 상위 5개 과제 1/5 완료 유지**. 1-2-A 및 1-2 전체 미완료. 사용자 지시에 따라 Mojang 공식 압축 client.jar와 실게임 렌더 인증은 필수에서 제외하며 이번에 수행하지 않았음. Minecraft 가구 제작·Project Zomboid 변환 시작하지 않음.

## v48 산출물
`01_P1_544_EVIDENCE_LEDGER.csv`, `02_NEW_P1_36_TYPED_SOURCE_LINKS.csv`, `03_BIRCH_CHERRY_SHELF_14_SOURCE.json`, `04_CHISELED_BOOKSHELF_10_SOURCE.json`, `05_OTHER_P1_9_SOURCE.json`, `06_PARENT_MODELS_12_SOURCE.json`, `07_PARENT_MODELS_8_SOURCE.json`, `08_THREE_MULTIPART_SOURCES.json`, `09_SINGLE_VARIANT_6_BLOCKSTATES.json`, `10_OWN_ELEMENT_DECLARATIONS_14.csv`, `11_OWN_FACE_DECLARATIONS_68.csv`, `12_ISSUES.csv`, `SUMMARY.json`, `NEXT_CHAT_HANDOFF.md`, `REPORT.md`.
