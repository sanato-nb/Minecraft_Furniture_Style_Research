# 1-2-A / 제1회차 실제 수행 기록 — G1 원본모집단 통과, G2 역사 기초색인 확보

2026-11-15 KST · 기준 GitHub `main` `52ef681327f7dce291312e59e647160a75005c53`.
범위 계약: `docs/vanilla_models_1-2/1-2-A_FIXED_SCOPE_AND_EXIT_PLAN.md` (기계판독 `1-2-A_ACCEPTANCE_CONTRACT.json`).
**정상적으로 1-2-A 1회차만 수행**했고, 단계 1-2-A 전체 완료 판정을 내리지 않는다. 기존 연구 체크포인트는 계속 **v69**.

## G1 PASS — GitHub 원본 Git Tree × v34 source catalog 4,669 전수 경로/SHA 비교

실제 원본 1.21.11 추출 데이터의 3개 부모 Git tree와 v34 원본 카탈로그:
- block models `1.21.11/assets/minecraft/models/block/` 2,390 JSON, parent tree `57eb7fbc4d0af0e931a04de94b4b6a766242d36e` → **2,390/2,390** path/mode/blob SHA 정확히 일치.
- blockstates `1.21.11/assets/minecraft/blockstates/` 1,168 JSON, tree `7a36f7d757e62aa61ee61aebcd8d5689bc462a8d` → **1,168/1,168** 일치.
- block texture `1.21.11/assets/minecraft/textures/block/` 1,111 PNG, tree `9a7172896d4a28b405b990733d51b77dcb50930c` → **1,111/1,111** PNG 일치.
- 텍스처 Git tree 총 1,210개 blob 중 **99개 `.mcmeta`는 PNG 분모 밖**의 별도 부속 파일로 명시적 기록. 1111개 PNG 누락으로 처리하지 않음.
- 모델 우선도 v34 원장 대조: **P1 544 + P2 1,039 + P3 807 = 2,390**, `source_path+git_blob_sha` 불일치0, typed path 중복0. 이름만으로 모델 정체 판정은 하지 않음.
- 고유 ID는 `(asset_type, full_source_path, git_blob_sha)`. 동일 SHA의 서로 다른 경로는 정상적인 상속/복제의 가능성을 보존하며 중복으로 지우지 않음.

G1 결과 `G1_SOURCE_TREE_AUDIT.json`, 실제 경로별 4,669행 `A_ASSET_REGISTRY_4669.csv`. **실제 파일별 기하/PNG 픽셀/렌더러 내용 전수 분석 아님**; 현재 Git tree와 기존 source 목록의 경로/해시 대응만 직접 검증했다.

## G2 기초색인 — 194개 역사 원본 경로와 26개 현대 체크포인트

v65 기존 역사 `00_HISTORY_194_FILE_AUDIT_LEDGER.csv`를 **직접 읽고**, v5~v43 사이 실제 존재하는 21개 연구 버전의 파일194개를 현 `research/vanilla_models` 전체 재귀 Git tree에 대조. 각 파일 경로·blob SHA·파일 크기가 **194/194 정확히 동일**.

이전 v65 검수 원장에는 이 194파일 모두에 대해 원본 contents 재열람 이력이 `true`로 기록되어 있다. 이번 1회차는 **그 이력을 검증 근거로 계승**하지만, 이번 대화에서 모든 194 파일 본문을 재열람·재해석한 것으로 주장하지 않는다. 각 파일의 의미론적 기여도·모델 단위 증거 연결은 G2/2회차 과제다.

v44~v69의 연속 26개 체크포인트 파일 트리를 다시 대조해 **26/26 버전 폴더 및 REPORT.md + SUMMARY.json Git blob SHA 존재** 확인. `v44/NEXT_CHAT_HANDOFF.md`는 해당 버전의 트리에서 없음(원래 없던 보조 파일로 기록). 반드시 이 파일이 있어야 한다는 요구는 없음; 누락을 임의 생성하지 않음.

G2 인덱스: `A_HISTORY_194_INDEX.csv`, `A_CHECKPOINT_26_INDEX.csv`, `G2_HISTORY_CHECKPOINT_AUDIT.json`. **G2 종합은 아직 PENDING_ROUND2**, 194개 파일의 전수 의미 통합 PASS는 아님.

## 단계별 완료 판정

| 필수 게이트 | 제1회차 상태 | 다음 검사 |
|---|---|---|
| G1 모집단·경로·Git SHA 4,669 | **PASS** | 새 SHA 변경 시 재기준화 검토 |
| G2 역사194·현대26 인덱스 | **인덱스 확보 / 의미근거 통합 미완료** | 2회차 역사 근거→P1 연결 |
| G3 P1 544 개별 증거상태 | **PENDING** | 2회차 |
| G4 P2/P3 1,846·P1 544 후속단계 지정 | **PENDING** | 2회차 |
| G5 독립 종료감사 | **PENDING** | 3회차 |

**오늘 수행한 원본 검증 중 경로·SHA 불일치 0건.** 최종 G1~G5가 모두 PASS가 아니므로 **A 미완료**. 다음은 계획대로 정확히 2회차를 실행하고, 3회차 감사 후 완료 또는 A_BLOCKED를 확정. 무의미한 신규 모델군 기하/UV/PNG 연구로 이탈하지 않는다.

## 2회차 시작 조건 및 데이터 경계

1. 최신 GitHub HEAD 확인; 완료된 G1 결과와 `G2_HISTORY_CHECKPOINT_AUDIT.json` 및 인덱스 읽기.
2. 194개 과거 파일의 기여 분야는 문서 원문/기존 증거로 확인된 것만 P1에 연결; 파일명에서 의미를 상상하지 않음. 과거 근거의 `direct`·`computed`·`secondary`·`unknown`를 분리.
3. P1 544행의 원본 SHA는 그대로 유지하고 증거 상태·부족한 범위·B~G 후속 단계 지정, P2/P3 1,846을 분류에 포함. 기존 연구를 신규 연구량으로 이중 계산하지 않음.
4. 추가 인벤토리 원본 차이나 치명적인 증거 부재 발견 시 정확한 수치로 기록. 3회차 중단 규칙 변경 금지.

이번 1회차에서 G1을 위해 읽은 Git object는 `git/trees` 기록이며, G2의 194파일 메타 검증은 recursive Git tree read이다. full original content 4,669개 파일을 새로 열었다고 주장하지 않는다.
