# 1-2-D 원본 blockstate 1,168경로 고정 범위 · 유한 6 Entry 종료 계약

Minecraft Java Edition 1.21.11 **사용자 제공 추출 원본**, 2026-11-16 시작 GitHub `main` `96dbd5b6859e91efd5c8693469ae759927abd65c`.

## 범위·정확한 분모
원본 `research/vanilla_models/v34/02_inventory_1168_blockstate_paths_git_shas.csv`(Git blob `48f385ea06f5e100331cc41bbc24da082adbfb2e`)의 blockstate JSON **1,168경로**를 모집단으로 한다. 원본 blockstates 트리 `7a36f7d757e62aa61ee61aebcd8d5689bc462a8d`의 Git blob SHA와 **1,168/1,168 경로·SHA 대조 일치**, 중복 0을 확인했다. **이 검사만으로 1,168 JSON 내용을 조사했다고 주장하지 않는다.**

실제 D 조사는 원본 `variants`/ `multipart` 각 조건, `AND`·`OR`·복수값, 선택 모델(배열 대안·weight 포함), `x`/`y` 회전, `uvlock`의 **명시 여부 및 원본 값**을 별도 기록한다. 조건을 정적 평가한 상태·모델 조립은 원본 조건의 문법상 후보이다. 게임 레지스트리에서 유효한 상태라는 보장이나 실제 렌더 방향·uvlock 엔진 결과를 인증하지 않는다.

B-first **일반 elements 부재 56개**와 E-first P1 **30개**의 특수 기하/렌더는 1-2-E 소관이며, 그 모델을 참조하는 blockstate JSON도 **D의 1,168 분모에서는 빼지 않는다**. A/B/C의 완료 상태를 유지하며 C의 2,304모델·23,090 face·21,590 PNG 연결 face·1,500 템플릿 미바인딩 face·1,073 PNG RGBA 실적은 D 신규로 다시 세지 않는다. `heavy_core` Entry4의 6면은 C Entry5 정정 근거로 취급한다. 공식 배포 JAR 인증·실게임 런타임/렌더·동적 블록 변화·애니메이션 재생·F/G·가구 제작·PZ 맵 생성은 제외한다.

## 6회 고정 배정

| Entry | 배정 경로 | 상태 |
|---|---:|---|
| ENTRY1 | 12 | 첫 원본 분석 대상 |
| ENTRY2 | 96 | 미검증 배정 |
| ENTRY3 | 265 | 미검증 배정 |
| ENTRY4 | 265 | 미검증 배정 |
| ENTRY5 | 265 | 미검증 배정 |
| ENTRY6 | 265 | 미검증 배정 및 최종 게이트 |
| **전체** | **1,168** | **배정 ≠ 조사 완료** |

Entry1은 brewing_stand, lantern, oak_shelf, oak_door, oak_fence_gate, campfire, chiseled_bookshelf, cauldron, heavy_core, furnace, piston, stonecutter. 남은 1,156개는 원본 경로 사전순으로 ENTRY2부터 96/265/265/265/265를 정확히 배정. 기계판독 경로별 표는 `research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv`. 과거 v34 원본 신원은 **전부 선행·중복으로 표기**하며 조사하지 않은 역사적 심층근거는 `not_yet_reconciled`로 둔다.

## 완료 게이트와 종료 계약
- **D1**: 원본 목록 및 Git 트리 1,168 SHA 일치, 배정 중복/누락 0.
- **D2**: 1,168 실제 JSON 원본 직접 읽기, 모든 variants/multipart 조건/모델 선택 및 명시 x/y/uvlock·배열·weight 전수 기록.
- **D3**: 정적 조건에 따른 상태별 모델 조립 전수 또는 분모/미전개 영역을 명시한 유한 상징적 증명. 게임 상태 유효성·엔진 렌더 추측 금지.
- **D4**: 모델 원본 경로/SHA와 B/C face·텍스처·PNG 근거 경로/SHA 연결, 미해결/E 별도 표시, 역사 재집계 금지.
- **D5**: 독립 원장 재계산, 기존 A/B/C/v69 원본 자료·원장 보존, 원격 커밋 후 SHA·행수·내용 재조회.

6회까지 **D1~D5 모두 PASS**인 경우에만 `D_COMPLETE_SOURCE_BLOCKSTATE_ASSEMBLY_SCOPE`로 종료한다. 아니면 `D_BLOCKED_AT_ENTRY6`로 종료. 자동 ENTRY7 금지. A=`A_COMPLETE_SOURCE_SCOPE`, B=`B_COMPLETE_SOURCE_GEOMETRY_SCOPE`, C=`C_COMPLETE_SOURCE_UV_TEXTURE_PNG_SCOPE`, v69 544×393/review544×70, 1-1 승인150/150, 상위 단계 완료1/5 그대로 유지.

**계약 고정은 D 전체 완료가 아님.**
