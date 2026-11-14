# 1-2 연구 실행 계획 — 바닐라 모델/UV/blockstate

> **1-2-A 실제 실행 v44:** [원본 모델 인벤토리·544 P1 SHA 대조 결과](../../research/vanilla_models/v44/REPORT.md). (1) 파일 원본 2,390/2,390 SHA 일치 (2) 선택 증거 파일 17개/144참조 (3) 고유 P1 SHA 연결 110, 현재 미연결 434 (4) v38 중복 5·v36 SHA 타입 오탐2 정정. 이는 **A 단계의 첫 부분 결과**이며, 남은 전역 v5~v43 전체 문서/CSV 증거 검토·모델별 심층 검증은 진행 중.


> 현재 기준 v43 · **계획 및 검수 설계**. 실제 미수행 연구를 완료로 처리하지 않는다. 전역 목표는 [현재 단계 상태](CURRENT_STATUS.md) 확인.

## 연구 대상·범위

- 사용자가 제공한 **Minecraft Java 1.21.11 JAR 추출본**을 소스 원본으로 사용.
- `models/block` 2,390개 **파일 인벤토리**, `blockstates` 1,168개 **파일 인벤토리**, `textures/block` 1,111개 PNG. 전수 목록은 **파일 식별·SHA 근거**이며 모든 내용의 정밀 측정 완료 주장이 아님.
- 직접 가구 디자인에 유용한 **P1 544개**를 우선, P2 구조/연결과 P3 재료/식생은 P1의 표현법 비교에 필요한 범위를 출처와 함께 선정. 544개 모두 똑같이 면/픽셀 심층 실측할지 여부는 **대표 원형·반복 leaf·특수 예외** 기준으로 결정한 뒤 명문화.

## 7개 세부 작업

| 코드 | 작업 | 검사할 증거 | 예상 산출 |
|---|---|---|---|
| **1-2-A** | 모집단·과거 연구 통합 | 2,390 원본 파일/1,168 상태/1,111 PNG 경로·SHA, v5~v43 전체 이력, 자산 타입 혼동·중복 | `SOURCE_REVIEW_LEDGER.csv`, `HISTORICAL_EVIDENCE_CROSSWALK.csv` |
| **1-2-B** | 블록 모델 기하 분석 | 원본 leaf/parent, elements.from/to, rotation origin·axis·angle, cullface, 0두께 평면, bbox·블록 점유 | `MODEL_GEOMETRY.csv`, `ELEMENTS.csv` |
| **1-2-C** | UV·텍스처 연결 | 부모 상속·slot override·각 face.texture, 명시 UV/암시 UV 구분, 회전/반전, 필요시 PNG 원본 RGBA·알파 | `FACE_UV_EVIDENCE.csv`, `TEXTURE_BINDINGS.csv` |
| **1-2-D** | blockstate·방향/연결 | variants/multipart 조건, facing/half/open/powered/attached, x/y, `uvlock` **키 존재 여부**와 값, 정적 조합 수 | `BLOCKSTATE_RULES.csv`, `STATE_MODEL_APPLICATIONS.csv` |
| **1-2-E** | 특수 표현·렌더 예외 | 블록 모델 파일만으로 설명할 수 없는 후보(예: 블록엔티티·엔티티·색상 tint·particle) 구분, 실제 근거 없는 부분 표시 | `RENDER_EXCEPTIONS.md`, `UNRESOLVED.csv` |
| **1-2-F** | 가구 모델링 관점 유형화 | 큐브 대 얇은 평면, 입체 디테일 vs 텍스처 디테일, 면 수/요소 수/비례 분포를 **관찰값**으로 비교 | `VANILLA_GEOMETRY_ARCHETYPES.md`, `STYLE_OBSERVATIONS.csv` |
| **1-2-G** | 독립 정합성 검수·인수인계 | 원본 경로·Git blob SHA, face·상속 참조, 누적 중복, P1 근거 등급, 제외 항목, 모델 예외 검증 | `AUDIT.json`, `ISSUES.csv`, `HANDOFF.md` |

## 권장 작업 순서

1. **A부터 우선:** v36의 선택 18 CSV에선 모델 파일과 blockstate 파일의 *basename* 때문에 오탐 2건이 발생했다. **`(asset_type, full_source_path, blob_sha)`** 복합 키를 사용해 모든 v5~v43 이력을 재대조하고, 어디까지 실제 JSON을 열어봤는지 상태화한다.
2. **B/C를 원형 중심으로:** 동일한 geometry를 공유하는 다수 색상·목재 leaf는 원형의 요소·면을 검증하고, 반복 leaf에서는 parent/texture override/좌표 차이만 정확히 조사해 중복 실적을 줄인다.
3. **D를 타입별로:** orientation/state/UVlock을 JSON에 원래 기록된 값과 별도 계산된 조합 수로 분리하고, 누락 속성을 `false`나 `0` 원본 필드로 만들어 쓰지 않는다.
4. **E 예외:** JSON만으로 확인할 수 없는 chest, bed, sign, banner, shulker 등 *후보*를 별도 분류해 실제 모델/엔진/블록엔티티 경로 증거가 있는 경우에만 구조를 판정한다.
5. **F/G 완료 판정:** 타입별 대표 구조·한계·문제원장과 소스 SHA가 남아야 종료 판정. 단순 P1 파일 방문수나 PNG 개수만으로는 완료를 판정하지 않는다.

## 검증 상태/숫자 체계

- 상태 제안: `inventory_only` / `source_json_sha_checked` / `parent_geometry_resolved` / `face_uv_explicit_verified` / `uv_implicit_derived` / `blockstate_source_checked` / `special_renderer_unresolved` / `source_scope_complete`. 한 모델이 여러 증거 상태를 동시에 가질 수 있으므로 **다중 필드**로 기록한다.
- 카운트 분리: **JSON 파일 수, 직접 검사 leaf 수, 부모/원형 수, 고유 elements/원본 선언 faces, 파생 face×texture 인스턴스 수, 정적 source 상태 수, 상태별 파생 적용 수, 원본 PNG·픽셀 수**. 이 수치끼리 합산하지 않는다.
- 모든 관찰에 `asset_type`, `source_path`, `git_blob_sha`, `minecraft_version`, `analysis_revision`, `parent_chain`, `source_face_index`, `uv_evidence_type`, `validation_status`, `evidence_csv_path` 포함 권장.
- **검수 필수:** P1 544개 전체의 검증 등급·근거/미검증·중복 및 예외 상태를 완전하게 기록할 것. 정밀 분석이 필요한 유형별 대표 원형은 소스 연결까지 검사하되, 반복 leaf는 별도 근거로 중복 제거. P2/P3는 범위 정의·예외·재분류 결과를 기록하고, 사용자 승인 범위를 벗어나 전체 2,390 JSON을 모두 심층 분석했다고 선언하지 말 것.
- 제외: 공식 배포 압축 JAR 인증·인게임 실제 렌더/런타임 인증은 최신 사용자 지시에 따라 *필수 조건 제외* (성공 주장 금지). 실게임 움직임 및 Minecraft↔PZ 가구 변환은 본 단계의 완료 판정 밖. 애니메이션 소스 재개 여부는 최신 분야별 상태를 따를 것.
