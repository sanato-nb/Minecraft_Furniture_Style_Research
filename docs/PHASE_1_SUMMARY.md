# 1단계 연구 정리

**기준일 2026-11-19 KST · 상위 세부과제 5개 중 4개 종료 승인.** 1-5-F 독립 종료 감사를 통과했다. 1단계 전체 종료 판정은 1-2 상위 종료 심사 대기다.

## 단계별 상태

| 단계 | 현재 판정 | 검증 범위와 근거 |
|---|---|---|
| **1-1 바닐라 재질·텍스처** | 🟢 **100% · 고정 표본 종료** | PNG 150/150개와 재질 11/11분류. 석재·벽돌 및 잎·식생의 애니메이션 소스를 추가 확인했다. 승인 분모는 지정 표본 150개다. [정본](vanilla_texture_1-1/CURRENT_STATUS.md) |
| **1-2 바닐라 모델·상태** | 🟡 **G 감사 6/6 · 상위 심사 대기** | 모델 2,390개·블록상태 1,168개·PNG 1,111개, 합계 4,669개 원본과 sidecar 99개를 대조했다. 공식 1.21.11 클라이언트의 특수 렌더 대표 상태 84/84개도 후속으로 확인했다. 2개는 블록상태가 직접 선택하지 않는 표시 템플릿이다. [G 감사](../research/vanilla_models/phase_1-2-G/final/G_FINAL_EXIT_REPORT.md) · [특수 렌더 실측](../research/vanilla_models/phase_1-2-E/followup/REPORT.md) · [상위 심사 기준](vanilla_models_1-2/1-2_STAGE_EXIT_SEPARATE_REVIEW.md) |
| **1-3 가구 모드 모델·구조** | 🟢 **100% · 고정 원본 범위 종료** | Another Furniture·Handcrafted·Macaw’s Furniture의 모델 JSON 16,572개, 블록상태 JSON 1,158개. G 감사 6/6 통과. 후속으로 등록 상태 115,986개와 기본 문맥 충돌 상자 263,886개를 감사했다. 실제 월드 배치·상태 전이·동적 충돌은 대표 사례에서 관찰했다. [G 종료](../research/furniture_mods/phase_1-3/G/1-3_FINAL_REPORT.md) · [Actions 재현](../research/furniture_mods/phase_1-3/runtime_actions/README.md) |
| **1-4 가구 모드 텍스처·UV** | 🟢 **100% · 원본 텍스처·UV 범위 종료** | F 감사 6/6 통과. 592,312면 모두 판정했고 585,969면에서 원본 화소를 확인했다. 나머지 6,343면의 사유는 슬롯 미연결 6,202면·PNG 경로 누락 139면·UV 범위 외 2면이다. [F 종료](../research/furniture_mods/phase_1-4/F/REPORT.md) |
| **1-5 바닐라↔가구 모드 비교** | 🟢 **100% · 고정 비교 범위 종료** | 가구 9개 유형, 모드 상태 47개와 바닐라 대조군 15개, 판정 21건을 정리했다. 런타임 검사 10/10 및 R10 텍스처 77/77개를 확인했다. [런타임 최종 보고](../research/furniture_mods/phase_1-5/runtime_followup/REPORT.md) · [F 종료 보고](../research/furniture_mods/phase_1-5/F/REPORT.md) |

종료 승인 건수는 상위 세부과제별 판정으로 집계한다. 각 원장의 표본 수·면 수·런타임 검사 수는 해당 범위의 검증 지표다.

## 1-5 상세

| 항목 | 현재 상태 | 산출물 |
|---|---|---|
| **A 범위·출처** | 🟢 완료 | 47개 모드 상태·15개 바닐라 대조군, 원본 74경로 검증. [범위](../research/furniture_mods/phase_1-5/A/REPORT.md) |
| **B 공통 단위 측정** | 🟢 완료 | 모델 적용 74건·요소 390개·면 1,844개와 흰색 침대의 전용 렌더·UV 실측. [측정 원장](../research/furniture_mods/phase_1-5/B/REPORT.md) · [침대 실측](../research/furniture_mods/phase_1-5/runtime_followup/WHITE_BED_VERTICES.csv) |
| **C 유형별 비교** | 🟢 완료 | 9개 유형·21건 판정. 적용 범위가 제한된 7건을 다시 검증했다. [교차 비교](../research/furniture_mods/phase_1-5/C/REPORT.md) · [7건 후속 판정](../research/furniture_mods/phase_1-5/runtime_followup/LIMITED_FINDINGS.csv) |
| **D 반례·런타임** | 🟢 **100% · 10/10 완료** | R10 아이템 58개·블록 파괴 파티클 19개. [런타임 판정표](../research/furniture_mods/phase_1-5/runtime_followup/RUNTIME_VERIFICATION.csv) · [77개별 기록](../research/furniture_mods/phase_1-5/runtime_followup/R10_TEXTURE_DISPLAY.csv) |
| **E 비교 DB·인계** | 🟢 완료 | 정적 비교 SQLite와 2단계 인계 21건. 런타임 최신 판정은 D 판정표를 참조한다. [DB](../research/furniture_mods/phase_1-5/E/comparison.sqlite.xz) · [인계표](../research/furniture_mods/phase_1-5/E/PHASE2_HANDOFF.csv) |
| **F 독립 종료 감사** | 🟢 완료 | A~E 산출물 22개 재현, 런타임 재실행 11,029행, 원격 본문 83개 및 CSV·TSV 31개 재조회. [종료 감사](../research/furniture_mods/phase_1-5/F/REPORT.md) |

## 종료 심사 및 2단계 인계

1. **1-2 전체 종료 심사**에서 원본 A~G 종료 증거와 특수 렌더·프레임 소스 후속 근거를 함께 검토한다.
2. **1단계 전체 종료 판정**에서 1-2 심사 결과와 이미 승인된 1-4-F·1-5-F 근거를 함께 확인한다.
3. 종료 판정 후 인계표의 **규칙서 검토 후보 14건**과 **반례·적용 조건 7건**을 2단계에 넘긴다. 예를 들어 침대의 렌더 높이와 충돌 높이는 따로 기록한다.

2단계의 범위는 출처와 예외를 갖춘 모델링 규칙서다. 새 가구 모델 제작과 좀보이드 맵 변환은 이후 제작 과제다.

[현재 진행 기록](CURRENT_PROJECT_STATUS.md) · [기계 판독 상태](../handoff/STATE.json)
