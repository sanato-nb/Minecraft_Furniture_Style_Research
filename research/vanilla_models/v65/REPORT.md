# v65 — 과거 CSV 113개·SQLite 4개 실물 재조회로 v5~v43 연구 파일 194개 내용 접근 범위 확보

> 2026-11-15 KST · Minecraft Java 1.21.11 · 시작 GitHub `main` `1cb3c57f94509b4fd57f686869963bc202618ee9`.
> 실제 과거 연구 원본 내용을 읽어 Git SHA/출처 일치와 근거 분류를 실시. **최종 1-2-A 완료나 새 가구 제작이 아님.**

## 1. 남아 있던 원본 CSV 113개 직접 재조회

v64 `00_HISTORY_194_FILE_AUDIT_LEDGER.csv`의 `v64_selected_original_content_reopened_total=false` 117파일 중 CSV 113개를 GitHub 원본 경로에서 다시 열어 **각 실제 Git blob SHA를 이전 v63 파일목록의 SHA와 직접 비교**. 총 **10,946개 원본 CSV 데이터행**, **행의 열 수 불일치 0**. `00_BATCH_01…10_HISTORIC_CSV_SOURCE_AUDIT.json`에 **원본 헤더·행 수·파일 Git SHA·모델 SHA 동행 증거의 실제 CSV 행 번호**를 기록했다.

- **33개 CSV**에서 기존 P1 모델의 **40자리 원본 Git SHA와 일치하는 셀**을 발견. **80개 파일**에서는 그런 셀이 발견되지 않았으나 이들 파일이 무의미하거나 과거 연구를 하지 않았다는 뜻은 아님. 텍스처/블록상태 수치 등에는 모델 SHA가 없어도 의미 있는 원본 자료가 있다.
- `v34/01_inventory_2390...`, `v34/10_all_2390_future_review_queue...`, `v36/01_p1_544_historical_sha_evidence_crosswalk...` 세 가지 **기존 전체 모델 식별 인벤토리 파일은 모델 기하 연구 추가 성과로 집계하지 않음**.
- 나머지 원본 CSV에서 **같은 행에 모델 경로+정확한 원본 SHA 또는 모델 이름+정확한 SHA**가 있는 연결만 선별 → **230개 모델×역사 CSV 파일의 근거쌍**, **서로 다른 모델 경로 88개**. 55쌍은 full path+SHA, 175쌍은 이름+SHA. 한 파일의 같은 모델에 대한 100개 면이 나와도 100개 새 모델로 세지 않고 **모델-파일 쌍**으로 묶는다.
- SHA만 일치하고 모델 경로/이름이 없는 후보는 강한 근거로 승격하지 않고 배치의 `SHA_only_unresolved`에 남긴다.
- 이전 v63 선택 역사 179개 원본 연결은 변경하지 않음. 비인벤토리 88모델은 이미 과거 선택 연결 112모델 집합에 포함됨. 다만 v34의 전체 인벤토리에서 추가로 `template_shelf_inventory.json`의 역사 경로·SHA 근거가 확인됐으므로 **선택 근거 연결 집합 112→113**은 가능하다. 이것은 신규 모델 식별도, 신규 기하 검증도 아님.

## 2. 원본 SQLite 4개 독립 정적 B-tree 검증

`v5`, `v6`, `v7`, `v8`의 `MC_Furniture_Style_Stage1_Research_v*.sqlite` 파일 **4개를 GitHub에서 바이너리(base64)로 실제 수신**한 다음 SHA를 원본 파일 SHA와 대조. 전체 바이트 배열을 복원하여 SQLite header, 페이지 크기·총 페이지 수, `sqlite_master` 테이블 root page를 따라 B-tree page를 정적 순회하고 실제 leaf cell 수를 테이블별 계산. `00_SQLITE_4_ORIGINAL_STATIC_BTREE_AUDIT.json`에 출처·테이블 schema SQL·table row 수·일부 실제 record sample을 보존.

| 원본 DB | 물리 페이지 | 테이블 | 핵심 테이블 행수 예 |
|---|---:|---:|---|
| v5 | 36 | 5 | sources71 / models55 / elements80 / blockstates16 / texture_stats150 |
| v6 | 58 | 10 | 위 5개 + model_additions13 / state_additions7 / uv_faces90 / state_examples34 / issues9 |
| v7 | 89 | 16 | 추가 connected_sources61 / geometry39 / assembly_cases21 / parts53 / primitives93 / limits6 |
| v8 | 101 | 20 | 추가 special_block_evidence17 / atlases6 / special_texture_metadata19 / rendering_conclusions7 |

정적 SQLite 페이지 순회는 **`PRAGMA integrity_check` 실행이나 전체 SQL 질의, 모든 DB의 역사 연구 주장 재검증과 다름**. v47의 과거 SQLite 연구 실적을 새로 계산하지 않고 이번에는 별도 바이너리/테이블 출처 점검으로 기록.

## 3. v5~v43의 194개 파일: 실물 내용 재조회 범위

| 분류 | 파일 수 | 이번 통합(v62~v65) 원본 내용 재조회 |
|---|---:|---:|
| CSV | 137 | **137/137** (v62~v63 24 + v65 113) |
| Markdown | 30 | **30/30** (v64) |
| JSON | 19 | **19/19** (v64) |
| Python | 4 | **4/4** (v64, 소스만; 실행 안 함) |
| SQLite | 4 | **4/4** (v65 바이너리 헤더/스키마/B-tree 구조) |
| **합계** | **194** | **194/194 파일 원본 내용 재조회** |

**194/194는 선택한 과거 폴더의 파일 내용을 실제로 열 수 있었음을 의미하며, 194개 파일이 담은 모든 모델의 기하·UV·PNG·렌더러 의미를 전수 교차 인증한 수치가 아니다.** Python/SQLite 전체 코드 실행이나 공식 게임 client.jar/인게임 렌더도 수행하지 않았다. 관련 항목은 완료율로 산정하지 않는다.

## 4. 같은 내용의 원본 모델 JSON Git SHA 충돌 — 식별키의 중요성

현재 P1 **544개 서로 다른 경로에 Git blob SHA는 539개만 고유**. 동일 JSON 내용이므로 **서로 다른 모델 경로가 같은 blob SHA를 공유하는 사례 2그룹, 총7모델 경로**를 확인했다.

1. `bamboo_sign.json` / `bamboo_hanging_sign.json`: blob `00c837bfb2e49f00dff93ac37be1b3d17f9f9369`.
2. `banner.json` / `bed.json` / `chest.json` / `oak_sign.json` / `trapped_chest.json`: blob `9406a8491ed2532d4878b0a91b16a0e5f8d93d80`.

**동일 SHA를 동일 물체 또는 동일 렌더 기하로 해석하면 안 됨**. 원본 모델 경로의 실제 동작은 block entity/특수 렌더러 등과 관련될 수 있으나 이름만으로 런타임 형상 확정 불가. 반드시 `(asset_type, full_source_path, git_blob_sha)` 복합키로 원본 증거를 구분한다.

## 5. 누적 원장 보존과 아직 끝나지 않은 연구

- 역사 파일 내용검수 원장 `194행×17열 → 194행×26열`. 이전 **3,298개 데이터셀 전부 동일**. 신규 9열로 각 역사 CSV 재조회 행·파일 SHA와 SQLite 정적 검증 출처 기록.
- P1 누적 원장 `544행×330열 → 544행×337열`. 이전 **179,520개 데이터셀 전부 동일**. 새 7열은 모델별 역사 CSV 230파일쌍 연결·증거 등급·동일 원본 SHA 공유 여부·미완료 구분.
- 보조 source review 원장 `544행×33열 → 544행×37열`, 이전 **17,952개 데이터셀 동일**.
- 기존 `544/544`는 **원본 모델 식별 연결** 완료를 의미. 직접 모델 JSON 판독 플래그가 있는 **516개**와 오래된 역사 CSV SHA행만 있는 **28개**의 범위는 동일하게 유지. v65에서 새 원본 모델 JSON의 기하·UV·게임 출력 직접 읽기 실적은 0.
- 미확인 14개 특수 렌더러/암시 UV 공식/UVLOCK, 모델별 의미론 통합 및 전체 544개 깊이 검증은 계속 보류. **1-2-A 실질 완료율 미산정**, 공식 JAR/게임 런타임 인증했다고 주장 금지. 1-1 승인150/150·상위1/5완료, 가구 제작/좀보이드 변환 미시작.

정확한 다음 단계: `NEXT_CHAT_HANDOFF.md`. 추적/주의: `08_OPEN_ISSUES.md`.
