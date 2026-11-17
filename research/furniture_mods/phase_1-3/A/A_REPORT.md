# Minecraft Furniture Style Research — 1-3-A 재정합 감사 (2026-11-18)

## 기준 및 실제 검증

- 작업 시작 main: `638d9e2889838ae75048104f02abc604de50f9d6`; A 작업 이전 baseline: `0542fb2b713fcaa5217ddb20a5273c02e1940b01`.
- A-00: v11~v24 14개 폴더, 195개 Git blob 경로·크기·SHA 목록 검증. `A_INPUT_MANIFEST.csv` 보존.
- A-01: 기존 Another leaf **204/204** 고정 원저자 JSON 직접 재열람 및 Git blob SHA-1 별도 계산, 원장·모델 ID·parent 204/204 일치. v18 33 + v21 38 + v22 43 + v23 51 + v24 39. 신규 발견 0, 중복 0, 원본 누락 0.
- A-02: 기존 선행 blockstate **22/22** 원본 SHA 직접 검산 증거 유지 (v21 12 + v23 10), 적용 1,188회. prior tree 177개와 미조사 155개 별도 관리; birch/spruce south 의자 예외 2건 유지.
- A-03: 부모 템플릿 **69/69** 원본 JSON 독립 SHA-1, parent·요소·face 대조 성공. 의자 39는 204의 부분집합. 일반19/tucked20, 상속 요소390·면1,794. 정상·tucked의 10요소/46면 및 로컬 Z 범위 직접 확인.
- A-04: Handcrafted authored120/generated16 경로·원장과 원저자 트리 대조 유지; 이전 실제 JSON 재해시 2, PNG24/면별 RGBA784는 별도 1-4 단위. Macaw 공식 JAR 과거 미확보·원본 모델 0은 현시점 새 검증으로 승격하지 않음.
- A-05: A1·A3의 차단 3건 해결. Handcrafted 잔여 134 원문·Macaw·버전·라이선스·미조사 state155·게임 렌더 등은 `A_UNRESOLVED.csv`에 미해결 및 B/1-4 책임 구분.
- A-06: 새 원본 SHA 증거 17조각과 통합 감사 2개, 총 **19파일 원격 본문·Git SHA1 재계산 일치**, 총 원본 JSON 273(204+69)개. A2 22 + Handcrafted 2 포함 A 범위 재해시 대상 합계 297(서로 다른 JSON 경로). Git compare에서 이전 연구 v11~v24 / vanilla / 1-1 / 1-2 변경 0. 최종 상태 파일 원격 재조회 전이므로 **A6 최종 승인 보류**.

## 게이트 판정 — 최종 메타데이터 readback 전

| 게이트 | 상태 |
|---|---|
| A0 | PASS |
| A1 | PASS |
| A2 | PASS |
| A3 | PASS |
| A4 | PASS_PRIOR_SCOPE |
| A5 | PASS |
| A6 | PENDING_FINAL_STATUS_READBACK |

**승인 6/7 — 1-3-A 전체 완료 선언 금지**. 최종 상태 파일 원격 SHA·행수·본문 및 보호 범위를 검증해야 A6 승인 가능. 상위 1-3 M1~M6 = 0/6, 1-3-B 고정 모집단 미결정, Minecraft 가구 실제 제작/실게임 모델 렌더/좀보이드 맵 생성 미완료.

## 사용 근거

`A_A01_INDEPENDENT_204_AUDIT.json`, `A_A03_INDEPENDENT_69_AUDIT.json`, `A_A06_REMOTE_PROOF_READBACK.json`, `A_INPUT_MANIFEST.csv`, `A_PRIOR_COHORT_RECOUNT.json`, `A_UNRESOLVED.csv`. 원저자 JSON·PNG·JAR 원문은 재배포하지 않음.
