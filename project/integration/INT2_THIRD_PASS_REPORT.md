# INT-2 3차 — 1-2-D 정적 상태 후보 전체 독립 전개·사례 대조

검수일: 2026-11-21 · 원본 기준: `main@176f7f34de2336eb7984c4734e97b6eb156c19f4`.

**최종 적용 범위 판정: `PASS_INDEPENDENT_SYNTAX_ENUMERATION_AND_PER_CASE_MATCH`.**
[실제 GitHub Actions 원본 재계산 #44859537942](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44859537942)에서 고정 1.21.11 blockstate JSON을 다시 읽고 원본 선언을 자체 전개했다. 구 1-2-D 계산 코드는 임포트/호출하지 않았다.

## 직접 확인한 결과

| 항목 | 이전 1-2-D | 이번 독립 전개 | 차이 |
|---|---:|---:|---:|
| blockstate 원본 개수 | 1,168 | 1,168 | 0 |
| variants / multipart | 1,072 / 96 | 1,072 / 96 | 0 |
| 선언된 모델 대안 | 7,592 | 7,592 | 0 |
| 정적 문법 상태 후보 | 9,193 | 9,193 | 0 |
| 상태별 모델 옵션 적용 | 19,440 | 19,440 | 0 |
| **개별 후보 대조** | 9,193 | **9,193 일치** | **0** |
| 원본별 집계 대조 | 1,168 | **1,168 일치** | **0** |

- 각 후보의 **적용 규칙 순서, 대안의 모델 경로, 인덱스, x/y 회전값, uvlock, weight**를 이전 Entry1~Entry6의 저장된 상태 원장과 대조.
- `multipart`의 `AND`/`OR`, `|` 대안값, 단독 true/false 속성에 대한 boolean 역값 도메인 생성 등 정적 소스 방식으로 독립 재계산.
- 블록상태 원본 raw Git blob SHA는 기존 D 고정 원장과 1-2-G 원장 모두와 일치한 것만 비교.

## 이력 저장 형식 차이: 41건 (오류로 부풀리거나 숨기지 않음)

첫 비교에서 총 후보 9,193·옵션 19,440은 일치했지만, 과거 Entry2는 일부 빈 variant 키를 `block|`로 저장했고 후속 Entry는 `block|<empty>`로 저장해 **41개 후보의 상태 ID 비교가 실패**했다. 원본 내용을 조회한 뒤 별도 검수기에서 두 표기를 같은 빈 키의 **표기 별칭(alias)**으로 정규화했다. 변경된 키는 역사 원장을 덮어쓰지 않았다.

재검수 후 개별 후보 내용 9,193/9,193, 각 원본별 집계 1,168/1,168 일치했고 **실제 규칙·옵션 불일치 0건**을 확인했다. 표기 별칭 41건은 [최종 JSON](INT2_D_SUMMARY.json)의 `historic_empty_id_format_aliases`에 영구 기록한다.

## 산출물

- [원본별 상세 1,168행](INT2_D_1168_SOURCE_CROSSCHECK.csv): 각 파일 SHA, variants/multipart, 규칙·상태·모델 옵션, 과거 카운트, 실제 비교 건수 및 불일치.
- [독립 집계·예외 JSON](INT2_D_SUMMARY.json): 후보/적용/개별 대조/상태 ID 별칭 포함.
- [독립 감사기](../../scripts/integration/audit_int2_states.py) 및 [회귀 테스트](../../tests/integration/test_int2_states.py).
- [GitHub Actions 감사 및 저장본 재실행 검증](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/workflows/integration-int2-states.yml).

## 감사 한계 및 다음 작업

이 집계는 **원본 JSON 문법으로 합성한 상태 후보**다. 실제 게임 레지스트리에 존재하는 모든 상태/합법 상태임을 인증한 것도, 대안 가중치에 따른 무작위 렌더를 실행한 것도 아니다. 회전한 모델의 baked quad 좌표·UV lock 결과와 최종 화면도 검증하지 않았다. 기존 D 원본 파일은 모두 변경 없이 보존했고, 어떤 AI 모델 훈련 승인 등급도 신규 부여하지 않았다.

**다음 INT-2 4차:** 1-2-B 요소의 회전 기하/ AABB를 별도 수학식으로 검산하고, 이후 1-3~1-5 가구 모드 연구의 독립 재검수로 확장한다.
