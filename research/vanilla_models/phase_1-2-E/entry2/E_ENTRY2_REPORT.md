# 1-2-E Entry2 — B-first 일반 기하 부재 28개 원본 재검토

**2026-11-16 KST · 시작 main `449fde4d747fce95cecb3570b170ff24e2484a99` · Minecraft Java 1.21.11 추출 자산.**

고정 배정표의 Entry2 **28/28개** 모델 JSON 본문과 Git blob SHA를 직접 대조했다. E 누적 **58/86**, 미조사 **28개**(Entry3); Entry4는 86개 종합 감사다. 이번 28개 모두 `parent`와 `elements`가 없어 모델 JSON 일반 기하가 제공되지 않는다. D 원본 blockstate에서 선택 참조 **43건·37경로**를 다시 계산했다. `block.json`은 D 직접 참조가 없는 공통 표시 설정(`gui_light`, `display`) 템플릿이며 particle 선언이 없다. `air.json`은 `minecraft:missingno`를 선언하지만 추출 트리에 해당 PNG가 없다. 이 두 예외를 PNG 실측으로 세지 않았다.

| 근거 | Entry2 결과 |
|---|---:|
| 모델 원본 본문·SHA | 28개 |
| 부모/자체 요소 | 0/0 |
| particle만 있는 모델 / particle 없는 표시 템플릿 | 27 / 1 |
| 실제 존재하는 고유 particle PNG SHA·RGBA | 23개 (이 중 item 경로 8개) |
| C 기존 PNG RGBA 근거 재사용 | 14개 |
| D 직접 모델 선택 참조 | 43건·37경로 |
| 원본에 없는 `missingno` PNG / 실제 런타임 렌더 확인 | 1 / 0 |

원본 snapshot, 각 모델의 선언과 SHA, PNG 원장 및 D 연결은 `E_ENTRY2_*` 파일에 남겼다. 별도 검사기로 모델 **28개 본문/SHA**, 실제 PNG **23개 SHA/RGBA**, D 선택 **43건**을 원본에서 재계산했고 불일치 **0**이다. PNG는 particle 자산이며 실제 보이는 표면으로 단정하지 않는다. 일반 요소가 없다는 결과로 특정 renderer 구현이나 화면상의 형상을 인증하지 않는다. 모든 모델의 `renderer_path_grade`는 `UNVERIFIED_RUNTIME_RENDERER`다.

**게이트:** E1 고정 범위 PASS, E2 모델 원본 58/86 부분, E3 원본 자산과 미확인 렌더 경계 58/86 부분, E4 전체·원격 감사 대기. **E 전체 미완료**. A/B/C/D 및 v69, 승인 150/150, 상위 단계 1/5 유지.
