# v51 — 1-2-A 추가 원본 검증: 선반 4목재·이끼 카펫·가마솥·발광 블록

> 2026-11-14 KST · GitHub 시작 HEAD `5c8db16ef9ca1cb24e9f4cf75557ef4ab8f6d77c` · 사용자 제공 Minecraft Java Edition **1.21.11** 추출본. v1~v50 연구 파일을 수정·삭제하지 않고 새 버전으로 보존.

## 1. 이번에 실제 수행한 원본 모델 조사

v50 P1 원장 `544`행 중 선택된 근거에서 미연결로 표시된 원본 모델 경로를 실제 `1.21.11/assets/minecraft/models/block/*.json`에서 직접 읽었다. 각 항목의 `(asset_type, full_source_path, git_blob_sha)`가 기존 v50 원본 모집단과 일치해야만 새 연결로 인정했다.

| 원본 계열 | 이번 신규 정확한 P1 source 연결 |
|---|---:|
| `jungle/mangrove/pale_oak/warped_shelf` (목재당 7) | 28 |
| `moss_carpet`, `mossy_carpet_side`, `pale_moss_carpet`, `pale_moss_carpet_side_small/tall` | 5 |
| 원본 부모 `carpet.json` | 1 |
| `template_cauldron_full/level1/level2` 및 lava/water/powder_snow 자식 | 10 |
| `redstone_lamp` 상태 2 + glowstone/shroomlight 2 + froglight 3색×2 방향 | 10 |
| **이번 신규 원본 경로+SHA 연결** | **54** |

P1 전체 SHA 연결이 **281 → 335/544**로 증가, 이번에 확인한 선택 근거에서 **209개 미연결**. 이 숫자는 소스 정체 증거의 범위이며 기하·UV·PNG·엔진 전체 연구 완료율이 아니다. v50 필드에서 이번 선택 54경로의 과거 직접 SHA 연결 표시는 없었지만, 모든 이전 기록을 완전한 의미론적 검색으로 부정한 것은 아니므로 '역사상 처음 연구'라고 주장하지 않는다.

## 2. 고유 기하 선언과 상속 적용을 별도로 계산

이번 54개 원본 JSON 자체에 쓰인 **44개 elements / 185개 face 선언**, 그중 원본 `uv` 키 명시 **8면**, 키 부재 **177면**을 직접 구분해 `06_ORIGINAL_SOURCE_ELEMENTS_44.csv`, `07_ORIGINAL_SOURCE_FACES_185.csv`로 저장했다.

- **가마솥 템플릿 3개**: `template_cauldron_full`, `level1`, `level2` 각각 **14요소/59면**, 합계 **42요소/177면**. 원본 177면에서 모두 UV 키가 없었다. 이는 암시 UV의 **원본 선언 수준** 사실이지 PNG 픽셀에서 이미 유도/검증했다는 뜻이 아니다. 자식 7개는 세 템플릿의 기하를 상속하며 새로운 요소 7세트를 선언하지 않는다.
- **이끼 카펫**: `mossy_carpet_side`의 원본 **1개 0두께 평면 요소/명시 UV 2면**, `carpet` 부모 원본 **1개 요소/명시 UV 6면**. `moss_carpet`과 `pale_moss_carpet`은 `carpet`을, side_small/tall은 `mossy_carpet_side`를 상속한다.
- **선반 28개**: `template_shelf_body/center/inventory/left/right/unconnected/unpowered` 부모 7종의 Git SHA를 v49 원본 증거와 교차 대조. **기존 부모 원형 11요소/38면을 신규 기하 원형으로 재계산하지 않는다.**
- **발광 10개**: `cube_all → cube`, `cube_column → cube`, `cube_column_horizontal → block` 계보로 기하를 확인하고 텍스처 슬롯을 개별 원본의 `all` 또는 `side/end` override로 연결했다.

54개 leaf/템플릿에 실제로 적용되는 면 출처는 **826개 적용 건**이다: 선반 **152**, 카펫 **24**, 가마솥 **590**, 발광 블록 **60**. 이 중 원본 UV 명시 출처가 적용된 면 **176건**, 원본 UV 암시 출처가 적용된 면 **650건**. **826은 826개 고유 원본 면이 아니라 부모 선언을 자식에게 적용한 횟수**다.

독립 템플릿으로 열람했을 때 **11개의 텍스처 슬롯 미해결 면 참조**를 별도 보류했다: `carpet` 6, `mossy_carpet_side` 2, 가마솥 템플릿 3개 각각 1. 자식에서 텍스처 override를 지정하기 전의 템플릿 용도 슬롯이므로 **실제 leaf의 오류로 자동 확정하지 않았다**.

## 3. 실제 blockstates JSON 조사

15개 원본 블록상태 JSON을 직접 읽었다. **원본 variants 21건, multipart 110규칙**을 확인했다. 선반 4목재 블록상태는 각 **24개** multipart 조건으로, `facing 4 × powered 2 × side_chain 4 = 32` 정적 조합/목재, 총 **원본 96규칙·파생 128조합·모델 적용 256건**이다.

`pale_moss_carpet` 블록상태는 **14개 multipart 규칙**과 측면 소형/대형 모델 참조가 있어, 단순 바닥 카펫과 다르게 보존했다. `water_cauldron` 및 `powder_snow_cauldron`의 원본 variants는 각각 3개, `lava_cauldron`은 1개였다. `redstone_lamp`은 꺼짐/켜짐 2개 소스 모델이 참조되고 `froglight` 3색은 각각 원본 방향 variants 3개로 vertical/horizontal 텍스처 슬롯과 모델이 분리된다.

이번 54 P1 경로 중 조사한 원본 blockstates의 월드 모델 참조가 직접 확인된 것은 **45개**다. 나머지 **9개**는 선반 inventory 4, 템플릿/부모 5 (`carpet`, `mossy_carpet_side`, 가마솥 템플릿3)로, 직접 world 모델 참조와 구분한다. 정적 조합은 게임 런타임의 실제 도달 상태나 렌더 검사로 세지 않는다.

## 4. PNG 실측 차단과 미해결 연구

이번에 `1.21.11/assets/minecraft/textures/block/redstone_lamp.png`를 직접 읽어 실화소 검증을 시도했으나, 현재 GitHub 파일 읽기 기능이 PNG 바이너리를 UTF-8 텍스트로 해석하여 `UnicodeDecodeError`를 반환했다. **원본 PNG RGBA 픽셀 측정 0건**. JSON 텍스처 슬롯 연결이 PNG 실화소 검증이라고 주장하지 않는다.

아직 209개 P1 경로가 이번까지의 선택/정확한 소스 증거에서 미연결이다. 특히 색상별 초·초 케이크·셜커 상자·일부 원본 광원/특수 렌더는 계속 조사해야 한다. 모델 정체를 이름만으로 구조 확정하지 않고 원본·부모·렌더 예외를 유지한다.

기존 v1~v50 보고서, 선택 모델의 1.21.11 SHA, v43 자산 타입 충돌 2건 해결, v46 동일 blob 다른 경로 문제, v47 SQLite 원본 증거 대조를 보존했다. **1-2-A와 전체 1-2는 미완료**, 완료율 미산정. **1-1 승인 텍스처 150/150 완료**, 상위 과제 **1/5 완료** 그대로 유지. 사용자 지시에 따라 공식 압축 client.jar 인증과 실제 인게임 런타임 검증은 필수 조건에서 제외되며 이번에 수행하지 않았고, 실제 가구 제작 및 PZ 변환도 시작하지 않았다.

## 증거 파일

- `01_P1_544_EVIDENCE_LEDGER.csv` — 확장 544행 원장 (기존 열 보존)
- `02_NEW_P1_54_TYPED_SOURCE_EVIDENCE.csv` — 신규 출처 경로 54행
- `03_ORIGINAL_MODEL_JSON_54.json` — 54개 소스 JSON 및 SHA
- `04_PER_MODEL_54_GEOMETRY_UV_STATUS.csv` — 모델별 부모 출처와 검증 등급
- `05_EFFECTIVE_FACE_APPLICATIONS_826.csv` — 826개 적용면, 각각 원본 기하 SHA/UV/텍스처 슬롯
- `06_ORIGINAL_SOURCE_ELEMENTS_44.csv`, `07_ORIGINAL_SOURCE_FACES_185.csv` — 독립 원본 선언 증거
- `08_ORIGINAL_BLOCKSTATES_15.json` — 15개 블록상태 원본/정적 계산
- `09_PARENT_CHAIN_5_RECHECKED.json`, `10_ANCESTOR_CHAIN_3_RECHECKED.json` — 모델 계보
- `11_ISSUES.csv`, `SUMMARY.json`, `NEXT_CHAT_HANDOFF.md`, `REPORT.md`
