# 1-2-C Entry3 — 고정 배정 732개 원본 UV·텍스처·PNG 연구

Minecraft Java Edition 1.21.11 · 2026-11-16 KST · 기준 `main` `2992eb1378d30a4e83391ca7b7eff5cb967e979d`.

## 선택·중복 방지

고정 `C_FIXED_SCOPE_2390.csv`의 `ENTRY3` 정확히 **732개(P1 155, P2 332, P3 245)**를 선택했다. `C_SELECTION.json`의 각 원본 경로/SHA는 B Entry10의 Git blob/cache, 현행 Git tree와 일치하며 Entry1·2 모델과 중복 **0개**다. 기존 v69 P1 원장을 변경하지 않고 이번 P1 155개의 선행 UV·PNG 관련 열 값과 신원 SHA를 `SELECTED_P1_PRIOR_C_FIELDS.csv`에 연결했다. 과거 열의 존재는 그 값의 의미나 전체 연구 완료를 독립 인증하는 근거가 아니다.

## 실제 원본 측정

| 관측 | Entry3 | 계상 기준 |
|---|---:|---|
| leaf 모델 원본 체인·기하 SHA | **732** | 기존 B 기하 완료를 신규 발견으로 재집계하지 않음 |
| 적용 face | **7,317** | 명시 원본 UV **5,958**, `uv` 키 부재 **1,359** |
| 명시 UV 한 축 이상 역방향 | **687** | 원본 UV 좌표를 수정하지 않음 |
| leaf별 texture slot 행 | **2,802** | 상속·override·참조 체인 포함 |
| 원본 PNG 전체 RGBA 복호 | **574경로 · 224,768픽셀** | 불투명 152,631, 완전 투명 54,868, 부분 투명 17,269 |
| 기존 Entry1·2 PNG와 중복 | **89경로** | 이번 고유 신규 경로 485, Entry1~3 고유 누적 **625경로** |
| 관련 `.mcmeta` 소스 | **46경로** | 경로·blob SHA 기록, 애니메이션 타이밍/재생 미인증 |

face의 `uv` 키 부재 1,359면은 원본 관찰이다. 실제 Minecraft 엔진이 계산하는 UV나 게임 화면을 인증하지 않았다. PNG 수치는 각 연결 시트의 **전체 RGBA 픽셀**이며 face×상태의 렌더 결과나 새로운 텍스처 발명이 아니다.

`UNRESOLVED.csv`의 **427개 face**는 50개 원본 부모 템플릿에서 texture slot이 아직 바인딩되지 않은 참조다. 각 템플릿에 실제 하위 모델이 있는 것을 경로/SHA·직접 자식 수로 확인한 `UNBOUND_TEMPLATE_EVIDENCE.csv`를 생성했다. 이 427면은 누락 PNG로 세지 않는다. 이번 코호트에서 그 외 설명되지 않는 slot/PNG 참조는 0개다. 하위 leaf가 texture override를 적용할 때의 최종 상태는 해당 leaf의 행에서 별도로 확인한다.

## 별도 검산과 단계 판정

독립 스크립트에서 고정 배정/leaf SHA/부모 체인 **732**, 원본 face **7,317**, PNG blob SHA 및 재복호 RGBA SHA **574**, `.mcmeta` SHA **46**, template unbound **50모델·427면**, v69 P1 신원 **155**, 과거 두 Entry와 leaf 중복 **0**을 대조해 PASS. `C_ENTRY3_INDEPENDENT_AUDIT.json` 참조.

C 직접 대상 누적 **840/2,304**, 고정 Entry4·5 잔여 각 **732개**, 합계 **1,464개**다. C1 역사 근거의 의미론 대조 PARTIAL, C2 840/2,304 PARTIAL, C3 연결 PNG 부분 완료, C4 Entry3 독립 감사 PASS·전체 종료 감사 PENDING. 이 Entry에서 C 완료를 선언하지 않는다. 86개 E 예외, D blockstate, E 특수 렌더, F/G, 가구 제작과 PZ 변환은 수행하지 않았다.

## 파일

`C_SELECTION.json`, `MODEL_SOURCE_EVIDENCE.csv`, `FACE_UV_EVIDENCE.csv`, `TEXTURE_BINDINGS.csv`, `PNG_RGBA_EVIDENCE.csv`, `PNG_MCMETA_SOURCE.csv`, `UNRESOLVED.csv`, `UNBOUND_TEMPLATE_EVIDENCE.csv`, `SELECTED_P1_PRIOR_C_FIELDS.csv`, `C_ENTRY3_AUDIT.json`, `C_ENTRY3_INDEPENDENT_AUDIT.json`. 재생성 스크립트 `scripts/phase_1_2_c_entry1.py`의 `C_ENTRY=entry3` 실행과 별도 감사 `scripts/phase_1_2_c_entry3_audit.py`.
