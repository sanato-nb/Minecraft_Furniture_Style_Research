# 1-2-A 종료 → 1-2-B 시작 인수인계

**현재 상태: `A_COMPLETE_SOURCE_SCOPE`.** 2026-11-15 KST, 3/3 마지막 회차 완료, G1~G5 5/5 및 독립 검사 50/50 PASS. **1-2-A를 더 반복하지 않는다.**

## 확정 고정 소스
- 연구 기준: Minecraft Java **1.21.11**, 연구 체크포인트 **v69**. `1-1` 승인 **150/150**, 상위 연구 완료 **1/5**.
- G1 자산: `../round1/A_ASSET_REGISTRY_4669.csv` (모델2390, blockstates1168, PNG1111), `.mcmeta`99 제외.
- G2: `../round2/A_HISTORY_194_EVIDENCE_CROSSWALK.csv`, `../round2/A_CHECKPOINT_26_EVIDENCE_INDEX.csv`.
- G3: `../round2/A_P1_544_SOURCE_STATUS.csv`; 원본 `../../v69/07_P1_544_EVIDENCE_LEDGER.csv` **544×393**, `../../v69/04_SOURCE_REVIEW_LEDGER_544.csv` **544×70** 절대 변경 금지.
- G4: `../round2/A_P2_P3_1846_SCOPE.csv`, `../round2/A_TO_BCDEFG_HANDOFF_QUEUE.csv`, `../round2/A_UNRESOLVED.csv`.
- G5: `A_AUDIT.json`, `A_FINAL_REPORT.md`, `G1_INDEPENDENT_AUDIT.json`~`G5_INDEPENDENT_AUDIT.json`.

## 즉시 다음 작업: 1-2-B
1. GitHub 최신 HEAD 재확인 후 **A 종료 상태와 인계 원장을 읽는다**. A의 G1~G5를 매번 전체 재실행하지 않는다.
2. `A_TO_BCDEFG_HANDOFF_QUEUE.csv`에서 **1-2-B** 담당 모델과 P1/P2/P3 부모 의존성 미확인 기록을 선택한다.
3. 기존 v44~v69 기하·부모 상속 선행 연구를 재사용하고 **새로 직접 검사한 항목만 신규 실적**으로 계산한다.
4. 원본 `(asset_type, full_source_path, git_blob_sha)`를 유지하고 SHA가 같더라도 서로 다른 모델 경로를 합치지 않는다.
5. UV/PNG는 **C**, 블록상태는 **D**, 특수 렌더러는 **E**, 유형화는 **F**, 최종 독립 검수는 **G**에 명시적으로 분리한다.
6. 각 파일·검증상태·미확인 사항·후속 담당을 보존하여 GitHub에 새 B 단계 결과를 작성한다. 기존 A/v1~v69 및 1-1 파일 수정 금지.

## 특히 금지
**A 4회차 없음, v70을 A 연구 버전으로 억지 생성하지 않음, 544개 원본 JSON 확인=544개 기하·UV·렌더 인증 아님, 마크 가구 제작·좀보이드 변환 시작하지 않음.**

A의 원본 자산/역사 근거 통합 완료와 상위 1-2 전체 완료는 전혀 다르다.
