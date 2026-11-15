# 1-2-A 제2회차 시작 체크포인트

먼저 Github `main` 최신 HEAD 재확인 및 최신 단계 계획 확인. 최신 연구 버전은 **v69(변경 없음)**, 새 `round1` 결과만 저장됐다.

**이미 수행됨/G1 PASS:** 원본 2,390 block model JSON + 1,168 blockstate JSON + 1,111 block texture PNG = **4669/4669 Git tree path/mode/SHA match**. 모델 우선도 P1 544/P2 1039/P3 807 우선그룹 완전. 추가 99 mcmeta는 PNG 범위 밖; 미확인 모델의 기하 완료 아님.

**G2 기초색인:** v5-v43 총 194 파일 Git tree SHA+size 대조 일치, 기존 v65 원본 파일 내용 열람 이력 194/194 계승. 실제 이번 회차에 194 원문 본문 일괄 재열람 안 함. v44-v69 체크포인트 26개 REPORT+SUMMARY Git SHA 확인, v44 NEXT_CHAT_HANDOFF 부재는 선택적 파일로 기록. **역사 파일별 의미 근거·P1 연결은 아직 완료하지 않음.**

제2회차 **반드시 수행할 것**: (a) G2 역사 194 파일/체크포인트26 각각에 증거 성격과 대응 P1 관계를 원문 기반으로 연결(확실하지 않으면 `unclassified`), (b) G3 544개 모델 각각 SHA + direct/computed/secondary/unknown evidence grade와 이전 증거 출처/미해결 사유, (c) G4 P2/P3 총1846개 분류 및 P1 544개 B~G handoff owner 지정, 열린 이슈의 소관 기록. 우선 과거 v65·v66·v69 기존 원장만 재사용, 신규 모델군 JSON/PNG 심층 분석을 별도 성과로 추가하지 말 것.

결과는 `research/vanilla_models/phase_1-2-A_completion/round2/`에 저장. 원본 연구 v1~v69 및 Round1 CSV 수정 금지. GitHub live HEAD lease 후 커밋, remote SHA/행수/원장 셀 보존 감사. 다음 3회차에서 독립 G1~G5 종료감사, **최대3회차**. 성공 시 `A_COMPLETE_SOURCE_SCOPE`, 불통과 시 `A_BLOCKED` 중단하고 무한 반복 금지.

원래 1-2-A 문서 `docs/vanilla_models_1-2/1-2-A_FIXED_SCOPE_AND_EXIT_PLAN.md`, 기계 계약 `1-2-A_ACCEPTANCE_CONTRACT.json` 변경 불가.
