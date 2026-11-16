# 1-2-C Entry2 — 96모델 원본 UV·텍스처·PNG 분석

Minecraft Java 1.21.11 · 2026-11-16 KST · 시작 `main` `cee36c3d4062f1dd765d2d22edde95136216b731`.

## 선정과 기존 연구 연결

B-first 일반 기하 모델에서 Entry1 12개를 제외하고 P1 24, P2 36, P3 36을 선정했다. 우선순위별 정렬 원장에 균등한 간격으로 기준점을 놓고 동일 우선순위 내 기하 제공자 중복을 건너뛴 규칙은 `C_SELECTION.json`에 재현 가능하게 기록했다. 각 우선순위 내 제공자는 모두 다르며, 세 우선순위 사이에서 공유한 것을 빼면 **91개 고유 기하 제공자**다.

v69 P1 원장 **544행 전체의 경로·원본 SHA·C 관련 선행 열 위치**를 `HISTORICAL_C_CROSSWALK_P1_544.csv`로 색인하고, 이번 P1 24개의 해당 열 값은 `SELECTED_P1_PRIOR_C_FIELDS.csv`에 별도 보존했다. 이 색인은 과거 값의 존재 및 경로 연결 근거이며 과거 연구의 모든 face·PNG 의미론을 독립 인증한 결과는 아니다. 이번 재분석을 역사상 최초 모델 발견으로 세지 않는다. 기존 v69 원장 자체는 변경하지 않았다.

## 원본 직접 측정

| 항목 | Entry2 | Entry1~2 중복 제거 기준 |
|---|---:|---:|
| 이번 모델 | 96 (P1 24, P2 36, P3 36) | 누적 서로 다른 leaf 108 |
| 적용 face | 978 (명시 UV 878, 원본 UV 키 부재 100) | 모델별 적용 행, 원본 face 선언 고유 수와 구분 |
| 텍스처 슬롯 행 | 295 | leaf별 binding 기록 |
| 이번 PNG 경로 및 전체 RGBA | 127개 / 52,480픽셀 | Entry1 PNG와 중복 4개, 신규 경로 123개, 누적 고유 140개 |
| RGB(A) 원본 알파 픽셀 | 불투명 31,467 · 완전 투명 12,203 · 부분 투명 8,810 | 이번 PNG 127개 전체 픽셀 |

face UV 원본 좌표 순서가 한 축 이상 역방향인 적용 행은 **108개**이며 원래 값을 보존했다. `implicit_source_absent` 100면은 원본 `uv` 키가 없다는 뜻이다. 공식 게임 엔진 계산 UV를 검증한 결과로 바꾸지 않는다.

`UNRESOLVED.csv`의 **81개 face 참조**는 `template_lightning_rod`, `button_pressed`, `cube_mirrored`, `template_fence_gate_wall_open`, `flowerbed_4`, `stem_fruit`, `template_farmland` 7개 원본 템플릿에 texture slot 값이 없기 때문이다. 각 템플릿의 직접 자식 모델이 원본에 존재함을 `UNBOUND_TEMPLATE_EVIDENCE.csv`의 경로·SHA·자식 수로 확인했다. 이 81면을 누락 PNG로 계산하지 않았으며 자식 leaf의 override를 적용하기 전에는 최종 PNG가 정해지지 않는다. 이 외의 미해결 face/PNG는 이번 코호트에서 확인되지 않았다.

## 검산과 상태

별도 감사에서 Git tree의 leaf·부모 경로/SHA **96개 계보**, 원본 geometry/UV **978면**, PNG blob SHA 및 디코드 RGBA SHA **127개**, P1 v69 신원 **544개**, Entry1과 겹치는 leaf **0개**, 7개 템플릿의 unbound 참조 **81개**를 재대조하여 PASS. `C_ENTRY2_INDEPENDENT_AUDIT.json` 참조.

C 직접 대상 2,304개 중 이번 신규 96, Entry1부터 누적 **108개**, C 코호트에서 아직 다루지 않은 **2,196개**다. 이는 과거 v1~v69가 연구하지 않은 모델 수가 아니다. C1 역사 색인 PARTIAL(의미론 연결 남음), C2 108/2,304 PARTIAL, C3 소스 연결 부분 검증, C4 표본 감사 PASS/종료 감사 PENDING. A/B 완료 및 E 예외 86, 승인 150/150, 상위 연구 완료 1/5 유지. D blockstate·E 런타임, 가구 제작 및 PZ 변환은 수행하지 않았다.

## 산출물

`C_SELECTION.json`, `MODEL_SOURCE_EVIDENCE.csv`, `FACE_UV_EVIDENCE.csv`, `TEXTURE_BINDINGS.csv`, `PNG_RGBA_EVIDENCE.csv`, `UNRESOLVED.csv`, `UNBOUND_TEMPLATE_EVIDENCE.csv`, `HISTORICAL_C_CROSSWALK_P1_544.csv`, `SELECTED_P1_PRIOR_C_FIELDS.csv`, `C_ENTRY2_AUDIT.json`, `C_ENTRY2_INDEPENDENT_AUDIT.json`.
