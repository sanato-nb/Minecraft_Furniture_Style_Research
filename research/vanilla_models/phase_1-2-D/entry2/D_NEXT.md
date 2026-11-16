# 1-2-D Entry3 인수인계 · 2026-11-16 KST

## 진척도와 고정 배정
- Entry1 **12 JSON** 실제 조사 + Entry2 **96 JSON** 실제 조사 = **108/1,168 (9.25%)**. 미조사 **1,060 JSON**. Entry2는 87 variants/9 multipart, 규칙위치797/옵션809, 문법상 상태884/상태모델 적용1,274, 고유모델211(C 직접200 + E 예외11) 원본 SHA 연결, 독립 상태884/884 일치.
- **Entry3 정확히265개**: `research/vanilla_models/phase_1-2-D/entry3/D_ENTRY3_QUEUE_265.csv`, 첫 파일 `black_wool.json`, 마지막 파일 `dripstone_block.json`. 배정표 `research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv`는 불변. **Entry3 원본 JSON은 아직 0/265 미조사**이며 목록 존재는 조사 완료가 아님.

## 다음 회차 필수 절차
1. GitHub 최신 HEAD, 고정 1,168 배정표와 Entry1/Entry2 완료 목록을 읽어 Entry3와 교집합0 확인.
2. Entry3 배정265경로를 **실물 원본 JSON 내용 직접 읽고 각각 Git blob SHA 검사**. variants, multipart, OR/AND, pipe 복수조건, 배열 대안/weight, 명시 x/y/uvlock 및 키 부재 원문 보존.
3. 정적 후보 상태를 유한 전수 계산하거나 조건 분할에 대한 **명시적 상징 증명** 작성. JSON 조건에 보이지 않는 게임 등록 상태는 별도 검증하지 않았음을 명확히 기록.
4. 모델 path/SHA → 기존 B/C face·slot·PNG 출처 SHA 연결. C의 face/PNG를 D 신규 발견으로 계산 금지. E의 **86개 원형 예외**는 D JSON 모집단에서 빼지 말고 E 소관만 분리. 파티클 슬롯은 C의 face PNG 원장 범위 밖일 수 있어 자산 tree 출처로 별도 검사.
5. 독립 재계산·과거 원장 불변·GitHub 커밋 후 SHA/행수/원문 readback. Entry3 성공분만 누적에 더해 최대 **373/1,168**. 미해결/차단은 정확한 source path와 이유를 기록.

Entry2 증거: `research/vanilla_models/phase_1-2-D/entry2/D_ENTRY2_REPORT.md`, `D_ENTRY2_SOURCE_STATUS.csv`, `D_ENTRY2_INDEPENDENT_SOURCE_AUDIT.json`, `D_ENTRY2_C_SLOT_PNG_AUDIT.json`, `D_STATE_ASSEMBLY_SPLIT_MANIFEST.json`, `D_ENTRY2_REMOTE_READBACK.json`.

보존: **A/B/C 완료, v69 원장, 승인150/150, E86, heavy_core 정정6면, 상위완료1/5**. 공식 JAR/실게임 렌더 인증 없음. Entry4~6 각265, 최종 Entry6의 D1~D5 모두 PASS만 완료. **Entry7 자동 생성 금지**.
