# 1-2-A 제3회차 (마지막) 시작 체크포인트 — 새 연구 없이 독립 종료감사

GitHub live `main` HEAD 먼저 조회. 원래 연구 체크포인트 v69, 1회차 G1, 2회차 G2~G4 상태를 확인. v70+ 연구가 있으면 충돌/변경 여부부터 확인. 계약 `docs/vanilla_models_1-2/1-2-A_FIXED_SCOPE_AND_EXIT_PLAN.md` 및 `1-2-A_ACCEPTANCE_CONTRACT.json` **변경 금지**.

제1회차: 4,669 자산 path+type+SHA 원본 Git tree 대조 PASS, P1 544/P2 1039/P3 807. `phase_1-2-A_completion/round1/` 보고서와 원장.
제2회차: `phase_1-2-A_completion/round2/`.
- 역사 v5-v43 194개 원본의 헤더·선택 문서 lines·JSON keys·SQLite schema 증거로 기여 영역194/194, 원본 컨텐츠 prior SHA/원본 tree 대조. 원본 3개 추가 직접 열람해 분야 명시. v44-v69 26개 SUMMARY 직접 재열람+SHA, REPORT는 tree SHA/존재 확인(26개 REPORT 본문 전체 읽었다고 주장 금지). **역사 전체 의미론적 재실험은 수행하지 않음**.
- P1 `A_P1_544_SOURCE_STATUS.csv` 544/544, 원본 Git SHA와 v66 누적 direct JSON flag, 과거 direct/derived/secondary/unknown 명확하게 구분. v69 원본 544×393 CSV를 건드리지 않음.
- 후속 전체 `A_TO_BCDEFG_HANDOFF_QUEUE_2390.csv`, 우선도 P1 544, P2 1039, P3 807. `A_UNRESOLVED.csv` 2390 모델별 owner + 3 공통 이슈. P2/P3 부모 의존성 1846은 미확인/1-2-B로 이관.
- 선별 역사 모델-파일 근거 링크 2044 중 벌크 인벤토리 출처는 의미론 근거로 세지 않음; 비인벤토리 941쌍은 고유 모델 개수 아님. P1 544 경로에 Git SHA 539고유/공유2그룹7모델 보존.

**3회차 G5 독립 필수 검사**: (1) original v34 registry typed 4669 vs latest source tree, (2) Round1 4669/194/26 original SHA preservation, (3) Round2 194 sources and 26 checkpoint source proof paths/SHAs valid, (4) P1 544 path/SHA crossjoin v69 원장/round1 original source, (5) P2/P3 1846 priorities and all2390 owner, (6) ambiguous evidence grade flags not falsely promoted, (7) v69 original 544×393 and review544×70 and prior v1~v69 original research file history remain untouched, (8) issues all assigned, (9) reference CSV/JSON row and SHA integrity, (10) GitHub commit then remote readback and separate validation SHA.

**결론:** G1~G5 모두 PASS면 `A_COMPLETE_SOURCE_SCOPE` 판정, A 종료 후 후속 1-2-B로 인계. G5 실패 및 마지막 회차 오류 수정 1회에도 오류가 남으면 `A_BLOCKED` 판정, 자동 4회차 금지. 단계 A 종료가 전체 1-2/B~G/실제 모델 완성 의미 아님.
