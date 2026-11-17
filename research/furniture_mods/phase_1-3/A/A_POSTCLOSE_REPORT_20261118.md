# 1-3-A 종료 후 독립 재감사 — 2026-11-18

- 대상: GitHub `main` 커밋 `702a2a62d4399438e64c6e90e7bd24f3d6809300`의 1-3-A 결과. **새 게이트를 만들거나 1-3-B를 수행하지 않음.**
- 기준: `A_INPUT_MANIFEST.csv`, Another 204·22·69·의자39·Handcrafted 원장, `A_UNRESOLVED.csv`, 현재 Git tree와 보호 파일 diff.

## 실제 재확인

| 항목 | 결과 |
|---|---:|
| v11~v24 Git blob 경로·SHA·크기 일치 | 195/195 (총 5,321,808 bytes) |
| Another 기존 모델 경로·ID·원장 SHA | 204/204, 중복 0 |
| blockstate v21/v23 | 12 + 10 = 22, 적용 1,188 |
| 과거 blockstate 전체 후보 / 잔여 | 177 / 155 |
| 부모 템플릿 및 v18 부분집합 | 69 / 30 |
| 의자 부모 상속 | 39 leaf, 390 elements, 1,794 faces |
| Handcrafted 선행 기록 | authored 120 / generated 16 |
| 미해결/해결 이슈 | 7 / 3 |
| v11~v24·1-1·1-2 등 보호자료 변경 | 0 |
| 이번 재집계 차이 | 0 |

## 범위와 결론

기존 `A_PRIOR_EVIDENCE_RECONCILIATION_PASS` 및 **A0~A6 7/7 상태 유지**. 본 재감사는 이미 저장된 원장·Git 메타데이터를 **다시 파싱하고 교차검산**한 것이며, 원저자 JSON의 바이트를 이번 회차에 297개 전부 재수집하거나 재해시한 성과는 아닙니다. 기존 A의 SHA·원문 직접검증 증거와 이번 메타데이터 재검증은 서로 다른 증거 등급입니다.

A 이후 다음 정규 단계는 **1-3-B 원본 모집단 고정**으로, Another 미조사 state 155, Handcrafted 현행 전체 모델, Macaw 공식 원본 및 라이선스·버전을 확인해야 합니다. 상위 1-3 M 게이트는 0/6, 마크 가구 제작·실제 렌더/맵 제작은 범위 밖입니다.

상세 독립 검산값과 입력 Git blob SHA는 `A_POSTCLOSE_INDEPENDENT_REAUDIT_20261118.json`에 보존했습니다.
