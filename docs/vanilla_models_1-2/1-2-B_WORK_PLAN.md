# Minecraft Furniture Style Research — 1-2-B 기하·부모 상속 작업계획

> 작성: 2026-11-15 KST · 대상 Minecraft Java 1.21.11 · 기존 연구 체크포인트 v69 유지.
> **상태: B 단계 실행 계획(기존 WORK_PLAN.md의 범위를 구체화). A의 수정이 아니며 사용자 확정 완료계약이라고 주장하지 않는다.**
> 1-2-A 완료 상태: `A_COMPLETE_SOURCE_SCOPE`, G1~G5 PASS. 재실행·4회차 생성 금지.

## 1. 기존 계획을 기준으로 한 정확한 범위

기준: `docs/vanilla_models_1-2/WORK_PLAN.md`의 1-2-B와 `research/vanilla_models/phase_1-2-A_completion/round3/A_HANDOFF.md`.

B는 **원본 block model JSON의 leaf/parent 상속 및 기하**를 연구한다:
- element `from/to` 좌표, 원본 요소 수와 선언 face 수, 모델 좌표 공간(원본에서 0~16 범위 밖도 실제 값으로 기록)
- element `rotation` origin/axis/angle, 0두께 요소, (회전 전) 원본 `bbox`, 축별 크기
- 면의 방향 및 `cullface` 존재 여부. *이는 UV 샘플링/면 렌더링 완료를 뜻하지 않는다.*
- parent chain 깊이·순환·원본 경로·Git blob SHA, leaf 자체 elements와 부모 상속 elements의 구분
- P1 상속 의존성과 P2/P3가 P1의 부모/공통 템플릿인지 여부를 출처로 대조

**B에서 하지 않는 일:** C의 explicit/implicit UV·texture slot·PNG 전체 RGBA, D의 모든 blockstate 조립, E의 runtime special renderer 공식 인증, F의 최종 미술 스타일 유형화, G의 최종 상위 연구 독립 감사, 가구 제작/PZ 변환.

## 2. 변경 금지 모집단과 선행 근거

| 모집단 | 대상 | B에서의 책임 |
|---|---:|---|
| P1 | 544 | A에서 first owner B **514**, first owner E **30**. E 예외 30은 삭제하지 않고 별도 명기 |
| P2 | 1,039 | B에서 원본 parent/geometry 및 P1 의존 여부 조사 |
| P3 | 807 | B에서 원본 parent/geometry 및 P1 의존 여부 조사 |
| **B 최초 담당 범위** | **2,360** | P1 514 + P2/P3 1,846. B 완료를 14개 대표 샘플과 혼동하지 않는다 |
| 기타 선행 | v44~v69 | 기존 geometry/parent 검증 결과를 원본 SHA/원장 경로 연결하여 재사용; 신규 성과로 재집계 금지 |

P1 기존 원장 `v69/07_P1_544_EVIDENCE_LEDGER.csv` 544×393, `04_SOURCE_REVIEW_LEDGER_544.csv` 544×70 및 v1~v69 자료를 수정하지 않는다. A 원장 키 `(asset_type, full_source_path, git_blob_sha)` 그대로 유지.

## 3. 유한한 완료 게이트(제안된 B단계 기준)

- **B1 — 범위·증거 등급 통합:** B-first 2,360/2,360과 E-first 30/30을 중복 없이 색인. 기존 과거 검증/원본 직접 재열람/추정/미확인을 분리한다.
- **B2 — 부모 계보:** B-first 2,360개의 parent 참조와 조상 모델 소스 SHA를 매칭하고 P2/P3 **1,846/1,846**의 P1 조상 의존성을 source 기반 `yes/no/unresolved`로 기록한다. unresolved는 사유·담당과 원본 경로 명시; 원본 파일을 읽지 않은 항목은 `verified` 금지.
- **B3 — 기하 상태 원장:** B-first 2,360개에 자체/상속 geometry 상태·기하 제공자·elements/from/to/rotation/0두께/cullface/경계상자 등 **각 항목의 증거 상태** 기록. 실제 상세 elements 검증은 대표 원형·반복 leaf를 구분하여 기존 WORK_PLAN의 원형 우선 방법을 따른다. 예외는 E로 인계하고 B 인증으로 승격하지 않는다.
- **B4 — 독립 종료 검수:** 경로·SHA·복합키·부모 순환/미해결·표본 원본 JSON·계산 재현·중복 실적·v69 전체 셀 보존·다음 C/D/E/F/G 인계를 감사. 소스 경로/해시 치명적 오류가 남으면 PASS 금지.

B1~B4가 모두 실제로 통과하기 전 **`B_COMPLETE_SOURCE_GEOMETRY_SCOPE`를 선언하지 않는다.** 시작 단계에서 분모를 임의 확장하거나 새 v70 연구를 성과 목표로 삼지 않는다. 무제한 반복에 대한 완료 판정의 대안은 정확한 남은 항목·차단 사유·다음 소관을 명시하고 작업을 중단하는 것이다. 본 계획의 회차 제한은 아직 사용자 확정 계약이 아니며 A의 최대 3회차 규칙을 임의 계승하지 않는다.

## 4. 산출물과 실행 방식

- `MODEL_GEOMETRY.csv`: 원본 모델 복합키, parent chain, leaf vs inherited source SHA, 원본 기하 수치와 검증 등급
- `ELEMENTS.csv`: leaf 적용 요소 인스턴스 vs 부모 원본 선언의 중복 분리; from/to/rotation/0두께/face/cullface
- `PARENT_TEMPLATE_SOURCE.csv`: 템플릿 단위 원본 증거와 재사용 구조
- `B_ENTRY*_AUDIT.json`, `B_ENTRY*_REPORT.md`, 이어서 위 B1~B4 충족 여부를 표시하는 상태원장
- GitHub 최신 HEAD lease 확인, 쓰기 후 원격 blob SHA·행수 readback, 원본 연구 파일 불변 검수

## 5. Entry1 시작 코호트

처음 직접 검사하는 B의 **검수 워크플로 표본은 14개 leaf (P1 3/P2 8/P3 3) + 상속 템플릿13개**로 제한. 이는 완료 분모 2,360의 선행 검증 샘플이지 1-2-B 완료 선언이 아니다. `research/vanilla_models/phase_1-2-B/entry1/`의 원장 참조.
