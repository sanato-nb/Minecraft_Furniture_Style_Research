# v47 — 1-2-A 과거 SQLite·생성 스크립트 교차 검증 + 가구 관련 P1 원본 11개 직접 조사

> 2026-11-14 KST · GitHub 시작 HEAD `32e76160afabadcae6ba48e6a0371401f0d19671` · 사용자 제공 **Minecraft Java 1.21.11 추출본**. v1~v46 및 기존 DB 보존. 신규 기하 분석은 역사 자료 조사 결과와 분리.

## 1. 역사적 연구 4개 SQLite DB를 직접 읽은 결과
GitHub 바이너리 DB를 base64 원본으로 읽어 SQLite table B-tree/record를 직접 해석하고 스키마·행 수·모델 경로/원본 SHA를 검증했다. **파일명만 확인하거나 생성 스크립트 예상 행 수로 대체하지 않았다.**

| DB | 확인한 테이블 | 원본 SHA+모델 경로가 P1과 일치한 고유 모델 |
|---|---:|---:|
| v5 | 5 | 18 |
| v6 | 10 | 31 |
| v7 | 16 | 45 |
| v8 | 20 | 53 |

v5 기존 테이블 `sources 71`, `models 55`, `elements 80`, `blockstates 16`, `texture_stats_v4 150`. v6에는 `model_additions_v6 13`, `uv_faces_v6 90` 등이 추가되고, v7에는 `connected_sources_v7 61`, `connected_geometry_v7 39`, `assembly_cases_v7 21`, `assembly_parts_v7 53`, `assembly_primitives_v7 93` 등이 추가. v8에는 `special_block_evidence_v8 17`, `texture_atlases_v8 6`, `special_texture_metadata_v8 19`, `rendering_conclusions_v8 7`이 추가되어 기존 자료를 계승한다. 원본 파일 SHA/표/행 목록은 `02_LEGACY_SQLITE_4_SCHEMA_AND_SOURCE_LINKS.json`에 기록.

DB 네 개에서 P1 **고유 53개 모델 경로**의 정확한 SHA 연결을 찾았으나 **모두 v46 124개에 이미 연결**된 모델이다. 새 SHA 연결 수 0. 기존 SQLite가 스냅샷/백업을 통해 누적된 행을 각 차수별 독립 연구로 다시 세지 않았다.

추가로 v5/v6/v7/v8의 `build_v*.py` **4개 전체를 열람**, 소스 SHA 문자열과 모델 경로/이름 문맥을 대조했다. P1 40자리 SHA의 코드 출현은 각 **16/13/15/17건**이지만 전부 이미 연결되어 있다. 40자리 SHA 하나가 여러 서로 다른 모델 파일 경로를 가리키는 경우는 기계적으로 어느 모델을 증명했다고 하지 않았다. 정확한 SHA+타입+경로 기반의 교차가 우선이다.

## 2. 원본 JSON 직접 조사 — 신규 P1 11개
이전 v46에서 모두 `sha_linked=false`였던 다음 **11개 고유 원본 모델 경로+SHA**를 직접 읽어 일치 확인했다.

- **대나무 선반 7 leaf**: `bamboo_shelf` 본체/center/inventory/left/right/unconnected/unpowered. 본체에 자체 `elements` 선언이 없고 각 7 부모 템플릿을 참조. `textures.all = minecraft:block/bamboo_shelf`, `textures.particle = minecraft:block/stripped_bamboo_block`. 부모 SHA는 v38/v45의 참나무/아카시아 선반에서 이미 연구된 7개 원형과 일치하므로 **새 기하 원형 0개**, 기존 부모 선언면 38을 신규 실적에 더하지 않음.
- 원본 `blockstates/bamboo_shelf.json` SHA `c92ee3ed74adbe7bf2e3b4c278998ceb1b74e336`의 **multipart 원문 24규칙** 읽음. `facing 4 × powered 2 × side_chain 4`를 정적 조건으로 **32조합** 평가, 각 2 모델 적용 → **64건의 파생 적용**. `uvlock` 키는 원본 규칙에서 부재. 실제 게임 상태 생성/렌더 검증 아님.
- **화분 템플릿 3종**: `flower_pot_cross` (7 요소/26 선언면), `flower_pot_cross_emissive` (9/30), `tinted_flower_pot_cross` (7/26). 세 JSON 모두 자체 `elements`을 명시하며 `ambientocclusion:false`. 3종에서 **23 요소, 82 선언면, 6개의 0두께 회전 평면** 확인. 두 템플릿의 화분 위 식물면 회전은 원본 `axis:y, angle:45, rescale:true`로 선언되어 있다. `tinted` 템플릿에는 **4개 얼굴의 tintindex**가 실제로 명시되어 있다.
- **비콘 모델 1종**: 자체 `elements 3`, 선언면 **18**, 모두 명시 UV. 원본 유리 외피, 흑요석 내부, 비콘 코어를 서로 다른 텍스처 슬롯으로 구분. `blockstates/beacon.json`은 단일 variant로 비콘 모델을 참조. 빔·실시간 특수 렌더러 확인은 별개.
- 화분 세부 잎 텍스처는 템플릿에 `#plant`, `#cross_emissive`로 남아 있어, **템플릿 원본의 16 face 슬롯이 child override를 필요**로 한다. `potted_dandelion`, `potted_fern`, `potted_open_eyeblossom` 등 **6개 child JSON을 직접 읽어** override 관계를 표본 검증했다. 이 6개는 P1 신규 실적으로 계산하지 않음.

따라서 이번 4개 직접 기하 정의 파일에서 **실제 원본 요소 26개, 원본 선언면 100개, 모두 명시 UV 100개, 암시 UV 0개, 0두께 요소 8개, 회전 요소 8개**가 확인됐다. 이들은 **원본 JSON 선언 기록**이지 PNG 픽셀·RGBA 샘플 100회를 뜻하지 않는다.

## 3. 모델별 증거 연결 상태

| 구분 | v46 | v47 |
|---|---:|---:|
| P1 모집단 모델 경로 | 544 | 544 |
| 원본 모델 경로+SHA 근거 연결 | 124 | **135** |
| 조사 범위에서 미연결 | 420 | **409** |
| 신규 원본 모델 경로 직접 열람 | 9 | **11** |
| 역사 SQLite/스크립트에서 추가 회수한 새 고유 P1 모델 | — | **0** |
| 신규 원본 PNG 픽셀·RGBA 검증 | 0 | **0** |
| 1-2 전체 모델별 기하·UV·PNG·상태·특수 렌더 완료율 | 미산정 | **미산정** |

`124 + 11 = 135`은 **고유 모델 경로의 출처 연결 수**. 409는 근거를 찾지 못한 수이지 '아직 한번도 연구된 적 없는' 수가 아니다. v46의 동일 SHA/서로 다른 경로 2그룹 정정, v43의 model-vs-blockstate 오류 2건 정정은 그대로 계승했다.

## 4. 현재 한계와 다음 작업
기존 v5~v43 서술형 49종, 추가 CSV 133종(대량 원본 인벤토리 4개 별도), SQLite4, 생성 스크립트4의 검증은 각각 **수행한 검사 유형**을 명확히 구분해 유지. 근거 없는 이름 참조를 자동 완성하지 않는다. 여전히 기존 연구의 일부 간접 출처/가구 모형 연결 근거, 원본 PNG texel, 특수 렌더 출처를 충분히 확인하지 못했으므로 **1-2-A 종료 선언 불가**.

이 연구는 **디자인 규칙 도출 이전의 원본 분석**이다. 1-1 승인 텍스처 150/150 완료 및 상위 과제 **1/5 완료 유지**, 실제 가구 모델 제작·Project Zomboid 변환 미실시. 공식 Mojang 압축 client.jar 및 인게임 런타임 인증은 완료 요건에서 제외됐으며 수행하지 않았음.

## v47 증거 목록
- `01_P1_544_EVIDENCE_LEDGER.csv`: v46 544행을 그대로 이어받아 추가 출처·SQLite 근거·검증 등급을 모델별 기록
- `02_LEGACY_SQLITE_4_SCHEMA_AND_SOURCE_LINKS.json`: 실제 SQLite 테이블 및 원본 SHA 행 검증 기록
- `03_LEGACY_BUILD_SCRIPTS_SHA_SCAN.json`: 생성 스크립트 4개 실제 SHA 대조
- `04_NEW_DIRECT_P1_11_MODELS.csv`: 신규 모델 경로 11개
- `05_NEW_GEOMETRY_26_SOURCE_ELEMENTS.csv`: 기하 요소 26개 및 0두께·회전
- `06_NEW_GEOMETRY_100_SOURCE_FACES.csv`: 선언 UV·텍스처 슬롯·tintindex 100건
- `07_BAMBOO_24_RULES_32_DERIVED_STATES.json`: 원본 24규칙/파생 32정적 조합
- `08_LEGACY_SQLITE_53_P1_CROSSWALK.csv`: 53개 과거 연결 모델별 근거
- `09_POTTED_CHILD_LEAF_6.json`: child texture slot override 6개
- `10_NEW_11_SOURCE_LINKS.csv`: 이번 직접 SHA 연결 11개
- `11_ISSUES.csv`, `SUMMARY.json`, `NEXT_CHAT_HANDOFF.md`
