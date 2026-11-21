# INT-2 2차 — 1-2 바닐라 모델·UV 선언 및 블록 상태 원본 독립 검수

2026-11-21 · 기준 `main@176f7f34de2336eb7984c4734e97b6eb156c19f4`.

**결과: `PASS_SOURCE_GEOMETRY_UV_DECLARATIONS_AND_STATE_OPTIONS`.** 최초 성공한 실제 Actions [#44858710958](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44858710958)에서 사용자 추출 원본 JSON을 직접 읽고 역사 C/D 프로그램을 임포트하지 않는 별도 계산기로 대조했다.

## 검수 입력과 방법

- 원본 JSON 2,390 block models + 1,168 blockstates. 각각 기존 1-2-G의 Git blob SHA와 재검증.
- 모델별 정본: [1-2-C 최종 2,390원장](../../research/vanilla_models/phase_1-2-C/entry5/C_SCOPE_2390_FINAL_STATUS.csv).
- 참조 종료 조건: [1-2-B](../../research/vanilla_models/phase_1-2-B/entry10/B_FINAL_CLOSURE_REPORT.md), [1-2-C](../../research/vanilla_models/phase_1-2-C/entry5/C_ENTRY5_REPORT.md), [1-2-D](../../research/vanilla_models/phase_1-2-D/entry6/D_FINAL_CLOSURE.md).
- 새 계산: JSON 부모 체인 추적, 가장 가까운 `elements` 선언 형상 제공자 결정, 적용 요소와 face 개수, `uv` 명시 유무, 상속되는 texture 슬롯 병합·다단계 해석, 실제 원본 PNG 경로 존재 여부, variants/multipart의 모델 대안 열거, 참조된 고유 모델 키 집계.
- C 원장의 2,390 **개별 행**마다 적용 face, 명시/암시 UV, 실제 PNG 연결면, 미바인딩면, 텍스처 바인딩 수 6개 항목 비교. E 소관 86모델은 역사 C에 따라 별도 제외하고 E가 검증됐다고 표기하지 않음.

## 독립 재계산 결과

| 검수 항목 | 독립 재계산 | 기존 정본 | 불일치 |
|---|---:|---:|---:|
| 전체 block model JSON | 2,390 | 2,390 | 0 |
| 정적 C 대상 / E 별도 예외 | 2,304 / 86 | 2,304 / 86 | 0 |
| 상속 적용 요소 | 5,689 | 5,689 | 0 |
| 모델별 적용 면 | 23,090 | 23,090 | 0 |
| 명시 UV 면 | 18,808 | 18,808 | 0 |
| 원본 `uv` 키 없는 면 | 4,282 | 4,282 | 0 |
| 원본 PNG 결합 면 | 21,590 | 21,590 | 0 |
| 슬롯 미바인딩 템플릿 면 | 1,500 | 1,500 | 0 |
| 원본 blockstate JSON | 1,168 | 1,168 | 0 |
| 선언 모델 선택 대안 | 7,592 | 7,592 | 0 |
| 블록 상태에 고유하게 참조된 모델 | 2,136 | 2,136 | 0 |

블록 상태 유형은 variants 1,072개, multipart 96개로 파싱했다. 참조 모델 경로 미해결 0건. 별도 [기계 판독 집계](INT2_1_2_STRUCTURE_SUMMARY.json) 및 [모델별 2,390행 대조 결과](INT2_1_2_MODEL_CROSSCHECK.csv)를 새 파일로 보존했다. 비교 자료의 86개 E 렌더러는 원본 신원만 확인된 범위로 유지한다.

## 검수의 한계

이번 '기하' 재계산은 **요소 및 face 선언/상속 개수** 검증이다. 각 요소의 회전 후 실제 정점·AABB 수치를 독립 계측한 것은 아니다. 다음은 이번 PASS의 범위 밖으로 남긴다.

- 1-2-D의 **9,193개 정적 문법 상태 후보 및 19,440개 모델 적용 인스턴스** 전개 재계산 (원본 선택 대안 7,592만 독립 재계산).
- 요소 회전·면 좌표·렌더 베이크, 암시 UV 최종 수치·UV lock, 특수 렌더 86종 실제 표시, 충돌·GUI·조명·게임 화면.
- 1-2-B의 0두께·좌표 역전·회전 요소 개별 수치 독립 계측, Mojang 배포 JAR 본문 인증.
- AI가 가구를 생성할 수 있는지 및 모드 자산 학습·재배포 권한.

동일 계산 분모로 C를 재현한 것이지 텍스처 화소 시각상 의미나 재질 분류를 검증한 것은 아니다. 역사 원본/DB는 수정하지 않았고 새 원장에 재검수 증거만 기록했다.

## 재현 방법

```sh
python -m unittest discover -s tests/integration -p 'test_*.py' -v
python scripts/integration/audit_int2_structure.py --root . --out /tmp/int2-structure
```

통과 시 나온 CSV/JSON을 Git 저장본과 CI가 다시 **바이트 일치·필드 일치** 검증한다. 구체적 CI 상태는 해당 커밋의 Actions 결과로 판단한다.

**다음 범위:** 1-2-D의 정적 후보/적용 계산과 회전 기하 독립식 검사, 이후 1-3 모드 기하·1-4 텍스처 UV·1-5 비교 결과를 순차 검수.
