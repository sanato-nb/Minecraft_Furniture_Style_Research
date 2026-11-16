# 1-2-C Entry4 — 고정 배정 732개 원본 UV·텍스처·PNG 연구

Minecraft Java Edition 1.21.11 · 2026-11-16 KST · 기준 `main` `5355a53a078b906c8a934ca126c5367ecdf865f4`.

## 고정 범위와 기존 근거

`C_FIXED_SCOPE_2390.csv`에서 `C_assignment=ENTRY4`의 **732개(P1 154, P2 333, P3 245)**만 선정했다. `C_SELECTION.json`에 원본 경로/SHA를 남기고 B Entry10 원장/JSON 캐시·Git tree의 leaf/부모 SHA를 대조했다. Entry1~3과 leaf 중복 **0**. v69 P1 원장의 기존 UV·PNG 관련 열 값 154행을 출처·SHA와 연결했으며, 해당 열의 존재를 최초 발견이나 과거 의미론 완료로 세지 않았다.

## 직접 측정

| 측정 | Entry4 결과 | 집계 경계 |
|---|---:|---|
| leaf/부모 원본 체인 | **732개** | 기존 B 계보 신원 신규 실적으로 계상하지 않음 |
| 적용 face | **7,077개** | 명시 원본 UV **5,637**, 원본 `uv` 키 부재 **1,440** |
| 명시 UV 한 축 이상 역방향 | **606개** | 원본 값 보존 |
| leaf별 텍스처 슬롯 행 | **2,903개** | 부모 상속·override 포함 |
| PNG 경로/전체 RGBA | **589개·239,360픽셀** | 불투명 156,793·투명 64,893·부분 투명 17,674 |
| PNG 경로 중 Entry1~3과 중복/신규 | **342 / 247** | 누적 고유 PNG **872경로** |
| `.mcmeta` 소스 경로/SHA | **48개** | 애니메이션 시트의 재생 인증 아님 |

원본 UV 키가 없는 1,440면은 `implicit_source_absent`이며 공식 엔진에서 산출될 좌표를 인증하지 않았다. PNG 픽셀은 각 시트 전체의 복호 결과이고 게임 화면의 합성 픽셀이 아니다.

## 구분해야 하는 두 종류의 미해결 참조

- **템플릿 53개·face 402개:** 원본 texture slot이 아직 바인딩되지 않았지만 해당 부모의 실제 자식 모델과 소스 SHA가 있다. `UNBOUND_TEMPLATE_EVIDENCE.csv`의 자식 수와 경로로 확인했으며 누락 PNG로 세지 않는다.
- **`heavy_core` 6면:** 원본 각 face의 참조는 접두사 없는 `"all"`이다. 이 값을 직접 리소스 경로 `minecraft:all`로 해석하면 `textures/all.png`는 없다. 그러나 같은 원본 JSON에는 슬롯 `all: block/heavy_core`가 있고 실제 `textures/block/heavy_core.png`도 Git blob SHA로 존재한다. 이 슬롯을 bare 참조에 적용하는 것이 정식 해석인지 이번 원본 자산만으로 인증하지 못했다. `UNRESOLVED_NON_TEMPLATE.csv`에 **원본 face 값·모델 SHA·후보 PNG SHA**를 남기고 미해결로 유지한다. 게임에서 누락 텍스처로 보인다고 단정하지 않는다.

이 6면을 PNG 경로 해결이나 성공 픽셀 검증으로 계산하지 않았다. C3의 무설명/누락 0 종료 기준에 대해 **Entry5에서 판정할 차단 후보**다. 원본 좌표와 텍스처 값을 임의로 고치지 않았다.

## 감사·진행 상태

별도 감사에서 배정/원본 SHA/부모 체인 **732**, face 원본 **7,077**, PNG blob/재복호 RGBA **589**, `.mcmeta` SHA **48**, 템플릿 **53·402면**, `heavy_core` 후보 경로/PNG SHA **6면**, P1 v69 신원 **154**, 이전 Entry leaf 중복 **0**을 대조해 **PASS_WITH_SOURCE_EXCEPTION**. 설명되지 않은 6면을 해소했다는 뜻이 아니다.

C 직접 대상 누적 **1,572/2,304**, Entry5 잔여 **732개**. C1 과거 근거 의미론 PARTIAL, C2 모델 조사 PARTIAL, C3 원본 예외 6면 및 미검사 범위, C4 표본 감사 PASS/최종 종료 감사 PENDING. 이 Entry에서 C 완료를 선언하지 않는다. E 예외86 및 D/E/F/G 후속 소관, v69 두 원장, 승인150/150, 상위1/5를 보존했다.

## 파일

`C_SELECTION.json`, `MODEL_SOURCE_EVIDENCE.csv`, `FACE_UV_EVIDENCE.csv`, `TEXTURE_BINDINGS.csv`, `PNG_RGBA_EVIDENCE.csv`, `PNG_MCMETA_SOURCE.csv`, `UNRESOLVED.csv`, `UNBOUND_TEMPLATE_EVIDENCE.csv`, `UNRESOLVED_NON_TEMPLATE.csv`, `SELECTED_P1_PRIOR_C_FIELDS.csv`, `C_ENTRY4_AUDIT.json`, `C_ENTRY4_INDEPENDENT_AUDIT.json`. 재생성/검산: `scripts/phase_1_2_c_entry1.py` (`C_ENTRY=entry4`), `scripts/phase_1_2_c_entry4_support.py`, `scripts/phase_1_2_c_entry4_audit.py`.
