# 1-2-D Entry2 실행 준비서 — 고정 96경로

**2026-11-16 KST · 작업 준비만 완료, 원본 JSON 상세 분석 아직 시작하지 않음.**

- 기준 범위: [`../D_FIXED_SCOPE_1168.csv`](../D_FIXED_SCOPE_1168.csv)의 `ENTRY2`; 총 **96 JSON**. `entry1`의 실제 조사 12/12는 보존. D 전체 12/1,168 실조사.
- 첫 대상: `1.21.11/assets/minecraft/blockstates/acacia_button.json`; 마지막: `1.21.11/assets/minecraft/blockstates/black_wall_banner.json`.
- [`D_ENTRY2_QUEUE_96.csv`](D_ENTRY2_QUEUE_96.csv)는 96개 고정 source 경로와 기대 Git blob SHA, **명시적 NOT_INSPECTED** 상태를 포함. 준비 시 원본 v34 목록과 배정표의 경로·SHA만 96/96 일치 대조했다. **JSON 내용 0/96 직접 읽음**.
- 기존 [`../entry1/D_NEXT.md`](../entry1/D_NEXT.md) 인수인계와 [`../../../../docs/vanilla_models_1-2/1-2-D_WORK_PLAN.md`](../../../../docs/vanilla_models_1-2/1-2-D_WORK_PLAN.md)를 확인하고 시작한다.

## Entry2 실제 착수 체크리스트

- [ ] GitHub 최신 `main` HEAD/파일 변경과 고정 배정표/기존 완료 대상을 확인한다.
- [ ] 정확히 96 원본 blockstate JSON 각각을 직접 읽고 원본 blob SHA를 96/96 검증한다. 접근 실패는 작업 실패 항목으로 남긴다.
- [ ] variants/multipart/AND/OR/pipe·모델 배열 대안/weight·x/y/uvlock 키의 존재/값을 원본 규칙별로 추출한다.
- [ ] 각 후보 상태를 전개하거나 재현 가능한 상징적 합성 증거와 unexpanded 범위를 남긴다. 조합이 큰 원본에서 무제한 완전 전개를 시도하지 않는다.
- [ ] 실제 선택 모델 path/SHA를 B/C 선행 face·UV·slot·PNG 증거에 연결하고, E나 범위 밖 모델은 별도 분류한다.
- [ ] 독립 조건 재평가, 파일 행수/중복, 모델 링크, 기존 A/B/C/v69·원본 불변 검사 후 새 파일만 GitHub 커밋한다.
- [ ] 원격 전체 SHA/행수/내용 readback을 검증한 뒤 Entry2 조사 누적을 최대 **108/1,168**로 갱신한다(실제 성공한 원본만 합산).

## 결과물 및 실패 분류

원본 JSON snapshot(파일 크기에 따라 분할), `D_SOURCE_RULES.csv`, `D_STATE_ASSEMBLY.csv` 및 필요 시 `D_SYMBOLIC_STATE_PROOFS.jsonl`, `D_STATE_MODEL_BC_LINKS.csv`, `D_MODEL_BC_CROSSWALK.csv`, `D_TEXTURE_C_LINKS.csv`, `D_UNRESOLVED.csv`, `D_ENTRY2_REPORT.md`, `D_ENTRY2_INDEPENDENT_AUDIT.json`, `D_ENTRY2_REMOTE_READBACK.json`, `D_NEXT.md`.

출처 미접근/불일치 = `BLOCKED_SOURCE`, 상태 조합 미증명 = `UNPROVEN`, 기존 C 연결 없음 = `BC_OUT_OF_SCOPE` 또는 `UNRESOLVED`, E 소관 = `E_REFERRED`; **원본 자체가 참조하지 않는 모델은 유령 미해결로 계산하지 않는다.**

**중요:** 준비 완료 ≠ Entry2 조사 완료. D 상태 `D_IN_PROGRESS_ENTRY1` 유지. ENTRY7 자동 생성 금지.
