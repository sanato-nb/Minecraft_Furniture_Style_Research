# 1-2-C — UV·텍스처·PNG 원본 연구 계획

작성 2026-11-16 KST · Minecraft Java 1.21.11 · 시작 기준 `main` `73571a9e1ab791e6ded46b6a01a1aae04fc8ffaf`.

## 범위와 분모

- A에서 확인한 블록 모델 2,390개의 신원은 고정한다. B-first 2,360개 중 일반 `elements`가 있는 **2,304개**가 face UV·텍스처 연결의 직접 대상이다. B-first 일반 기하 없는 56개와 E-first P1 30개, 합계 **86개**는 별도 예외로 관리한다. E 소관 렌더러를 C 완료 조건으로 바꾸지 않는다.
- 부모 텍스처 슬롯의 상속·leaf 재정의·`#slot` 연쇄, face.texture의 최종 참조, 원본 명시 `uv` 또는 키 부재, 원본 face `rotation` 및 UV 좌표의 역방향을 출처별로 기록한다. UV 키가 없는 면은 `implicit_source_absent`로 적고, 계산이 필요한 경우 공식 구현과 대조되기 전에는 계산 후보로만 둔다.
- 각 face가 실제로 가리키는 PNG 경로·Git blob SHA와 필요시 전체 PNG RGBA·알파를 검사한다. PNG 1,111개는 자산 목록의 분모이며 모두 반드시 픽셀 복호화한다는 뜻이 아니다. 중복된 PNG는 경로+SHA 단위로 한 번만 검사한다. `.mcmeta` 애니메이션·블록상태 회전·실게임 렌더러 해석은 별도 후속 근거가 필요한 경우 미해결로 둔다.
- v1~v69 UV/PNG 연구는 이미 존재하는 증거로 연결하되, 이번에 다시 확인한 모델·face·PNG를 역사상 최초 발견으로 세지 않는다. P1 기존 두 원장, A 및 B 결과는 수정하지 않는다.

## 완료 게이트

| 게이트 | 완료 조건 |
|---|---|
| C1 범위·이력 | 2,390개가 직접 대상 2,304 또는 E 예외 86으로 중복 없이 분류되고, 선행 v1~v69 근거의 재사용 여부를 표시 |
| C2 face와 slot | 직접 대상 2,304개에 face 원본 SHA, 상속 기하 SHA, texture 슬롯 해석, 명시/부재 UV 및 회전·역방향을 기록. unresolved는 근거와 함께 별도 행으로 남김 |
| C3 PNG | C2에서 해결한 PNG를 경로·blob SHA로 연결하고, 필요한 픽셀·알파 관측은 실제 복호 결과와 범위를 표시. 미해결 참조와 애니메이션은 별도 표시 |
| C4 독립 감사 | source/cache/원장 SHA, 행수·중복·샘플 재계산, 역사 실적 중복, 이전 원장 불변 및 원격 커밋 readback 검사 |

모든 게이트 통과 전 `C_COMPLETE` 선언 금지. 오류나 접근 차단 시 남은 항목과 이유를 기록하고 유한한 체크포인트로 끝낸다. 원형을 먼저 분석하고 반복 leaf는 slot override를 대조한다. D의 blockstates, E의 특수 렌더, F/G의 양식·최종 감사, 가구 제작과 PZ 변환은 C의 연구 실적에서 제외한다.

## Entry1 실제 시작

P1/P2/P3 각 4개, 합계 12개 원형·상속 leaf를 선정한다. B 종료 원장과 원본 Git blob을 대조하고 `FACE_UV_EVIDENCE.csv`, `TEXTURE_BINDINGS.csv`, `MODEL_SOURCE_EVIDENCE.csv`, `PNG_RGBA_EVIDENCE.csv`, `UNRESOLVED.csv`, 감사 결과를 `research/vanilla_models/phase_1-2-C/entry1/`에 둔다. 이 12개는 C 단계 전수 완료 주장이 아니다.
