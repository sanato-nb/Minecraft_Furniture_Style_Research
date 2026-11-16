# 1-2-F Entry1 첫 실제 조사 — 원본150 / 기하 원형·선행 C/D 교차분석

**2026-11-16 KST · 계획 기준 HEAD `fc12c20968073b0bfc1fc9dc983ea428e5e960fa` · F 고정6회/전체2,390개 불변.**

## 1. 직접 수행한 새 작업과 증거
1. `F_ENTRY1_QUEUE_150.csv`의 P1 50 + P2 50 + P3 50개 **모든 원본 모델 JSON 본문**을 GitHub에서 실제 읽고 원래 blob SHA 대조 **150/150 PASS**, JSON 파싱 오류0. 배치15×10의 원본 전문 snapshot, 본문 집계 `F_SOURCE_AGGREGATE_150.json`, B/C/E provenance 결합 `F_SOURCE_B_C_E_JOIN_150.json`, 150행의 `F_MODEL_SOURCE_STATUS.csv`와 경로/SHA 상호 참조.
2. B 원장 `MODEL_GEOMETRY_ALL_2360.csv` 및 P1/P2/P3 적용 요소 `ELEMENTS_P*_ALL.csv`를 실제 재조회해 142 일반 기하 모델의 **371 적용 요소/1,373 face**를 독립 재계산. C 최종 범위표의 적용 face **142개 모델 모두 일치**, SHA 불일치0. 나머지8개는 E 모델: **일반 요소 기하가 없는 원본 특수 표현**으로 구분하고 크기/face '0인 일반 큐브'라고 분류하지 않음.
3. `STYLE_OBSERVATIONS.csv` 150 모델 **소스 기반 기하 원형·다중 구조 태그** 생성. 배타적 주 원형: 전체 큐브33, 얇은/0두께 우선13, 회전36, 다중요소27, 기타 단순입체33, E8. 복수태그: 0두께52, 얇은57, 다중61, 회전36, 경계/역방향16(서로 중복 가능). 원본/계승 증거, min/max·bbox·UV키 유무, 활용 **후보**와 확정 여부를 분리했다.
4. C Entry1~5 슬롯 원장과 C PNG SHA/RGBA 사전 원장 재결합: 모델별 텍스처 **546 슬롯/546**, prior C 고유 face-PNG **188경로**, C 누락/슬롯 SHA 불일치0. 이 근거는 **이전 C 연구 재사용**. F에서 원본 PNG 이미지 새로 직접 보거나 복호화한 건수 **0**.
5. D Entry1~6의 7개 상태 모델 링크(총 기존 **19,440행**)를 경로/SHA로 재대조. F의 직접선택137모델 모두 원장에 존재했고 해당 상태·모델 선택 **1,180행**, 미직접13. 모델 SHA 누락0. D 후반 원장들에 x/y/uvlock explicit 필드가 없으므로 **115모델**은 이 원장에서만 진위 판정하지 않고 별도 원본 규칙 재확인 필요로 기록.
6. 출처 및 구조 독립 감사 `F_ENTRY1_INDEPENDENT_AUDIT.json`: 원본150/모델 SHA, B 적용 요소·0두께·회전·경계·C face 1,373대1,373, C 슬롯546, D 참조137/137, E8 책임 유지, 과장된 시각 판정 0검증. **기하·원본 교차분석 PASS**, 실제 PNG 스타일 확정은 PENDING.

## 2. F 전체와 Entry1 완료 여부 — 정확히 구분
- **F 원본 JSON 직접 검사 및 기하 원형 1차 분류 150/2,390 = 6.28%**. Entry1의 **고정150모델에 대한 소스·기하 원장 150/150 채움**. 선행 C/B/D/E 수치를 새로 측정했다고 다시 계산하지 않는다.
- **F 최종 스타일·시각·조립 게이트를 통과한 모델 0/2,390**. `F3`의 원본 PNG 시각 검증 150모델과 `F4`의 D x/y/uvlock 원문 명시 여부115모델 추가 검사가 **이 Entry1에 남아 있다**. E 예외8 runtime renderer 검증은 F 범위 밖 소관 유지.
- 미해결 원장 `F_UNRESOLVED.csv` 273행 = PNG 스타일 관찰150 + D 명시 플래그115 + E runtime 보류8(후자는 원본 F 종료의 차단이 아니라 E 소관).
- **Entry1 완료 아님**, Entry2로 넘어가지 않는다. G 전체 종료·가구 모델·좀보이드 맵 구현은 아직 시작하지 않는다.

## 3. 독립 감사·원본 보호와 다음 단계
- 원본 모델 JSON 150개 경로/SHA, B의 142 직접 기하, C 546 슬롯 및 188 고유 prior PNG, D의 모델137/137와 state link1,180, E 예외8를 각자 **서로 다른 분모**로 유지.
- 기존 A/B/C/D/E·v69 및 사용자 1-1 승인150/150, 상위 5단계 완료1/5를 변경하지 않는다.
- 공식 Minecraft 배포 JAR 진본 인증·실제 게임 렌더·게임 상태 레지스트리 검증, 특수 E 가시 형상 인증, 원본 PNG 직접 시각 관찰은 수행하지 않았다.
- 다음은 같은 Entry1의 `F3` 이미지 근거 검수, `F4` 115모델 D 원본 명시 여부, 필요 시 타입 반례/표본 대표성 점검. F 고정 2,390과 6회차, Entry7 금지 유지. 원격 커밋 이후 재조회 증거는 별도 `F_ENTRY1_REMOTE_READBACK.json`에 기록.

참조: `VANILLA_GEOMETRY_ARCHETYPES_DRAFT.md`, `F_ARCHETYPE_RULES.json`, `STYLE_OBSERVATIONS.csv`, `F_ENTRY1_INDEPENDENT_AUDIT.json`, `F_TEXTURE_PROVENANCE_AUDIT.json`, `F_D_STATE_RELINK_AUDIT.json`.
