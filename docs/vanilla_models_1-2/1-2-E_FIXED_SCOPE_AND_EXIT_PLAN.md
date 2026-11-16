# 1-2-E 특수 렌더·일반 기하 부재 모델: 고정 범위와 종료 계약

**2026-11-16 KST · 시작 `main` `5ef795f4d0b24ae5535d6c9411a5f092ba35e6ac`.** 사용자 제공 Minecraft Java 1.21.11 추출 자산을 기준으로 한다. [D 종료 인수인계](../../research/vanilla_models/phase_1-2-D/entry6/D_NEXT.md)의 다음 작업이다.

## 목적과 정확한 분모

C 고정 범위 2,390모델 중 `C_assignment=E_EXCEPTION`, `C_exception_owner=1-2-E`인 **86개 원본 경로**를 E 모집단으로 확정했다. B-first에서 일반 기하가 없다고 이관한 **56개**와 B-first 대신 E 우선으로 배정한 P1 **30개**다. 30개는 B가 실제 기하 부재를 검증했다는 뜻이 아니므로 E에서 직접 확인한다. D blockstate 원본이 직접 선택 모델로 참조한 E 경로는 **84개**다. 참조되지 않은 `block.json`과 `thin_block.json` 2개는 범위 밖이 아니라 원형 템플릿으로 **그대로 86개에 포함**한다.

기계판독 범위·각 행 SHA·D 참조는 [`E_FIXED_SCOPE_86.csv`](../../research/vanilla_models/phase_1-2-E/E_FIXED_SCOPE_86.csv), B/C/D 분모·원본 SHA 대조는 [`E_FIXED_SCOPE_AUDIT.json`](../../research/vanilla_models/phase_1-2-E/E_FIXED_SCOPE_AUDIT.json)에 보존한다. D의 84개를 E 완료율로 사용하지 않는다.

## 유한한 실행 회차

| 회차 | 고정 배정 | 주된 일 | 종료 상태 |
|---|---:|---|---|
| **Entry1** | E-first P1 **30개** | 원본 모델 JSON·부모/요소/텍스처, D blockstate 참조, PNG 원본 경로/SHA, 증거 등급 | 원본 직접 검사 및 독립 감사 |
| **Entry2** | B-first 이관 **앞 28개** | B 결과와 원본 부모 체인·일반 요소 부재를 재검토하고 E 예외 분류 | 원본 직접 검사 및 독립 감사 |
| **Entry3** | B-first 이관 **뒤 28개** | 나머지 예외 전수 원본 검사·D 사용 여부·템플릿과 특수 사례 구분 | 원본 직접 검사 및 독립 감사 |
| **Entry4** | 신규 모델 **0개**, 전체 86개 감사 | 렌더 근거 수준·미확인 항목·B/C/D 중복·원격 검증을 종합 판정 | 최종 PASS 또는 `E_BLOCKED_AT_ENTRY4` |
| **합계** | **86개** | 고정 4회차. 자동 Entry5 없음 | Entry3까지 86개 직접 조사, Entry4 최종 감사 대기 |

배정은 30개 E-first 경로 사전순, 56개 B-first 경로 사전순의 앞뒤 각 28개다. Entry4의 0개는 분석을 생략한다는 뜻이 아니라 **86개 전체의 renderer/예외 근거를 감사하는 회차**다.

## 완료 게이트

| 게이트 | 통과 조건 | 실패/보류 처리 |
|---|---|---|
| **E1 범위·선행** | 86/86 경로·Git SHA가 C의 E 담당 및 B 범위와 일치; D 참조 84·미참조 2 구별; 배정 중복·누락 0 | 불명확한 담당이나 누락은 통과 금지 |
| **E2 모델 원본** | 86개 원본 JSON 본문·SHA, 부모 체인·일반 elements 여부·텍스처 선언과 출처를 직접 기록 | B의 과거 판정을 E 새 검증으로 둔갑시키지 않음 |
| **E3 표현 근거** | 각 모델의 D blockstate 선택 참조, particle 등 모델 자산, 일반 기하 설명 가능 범위, 엔진 특수 표현에 대한 직접/보조/미확인 근거 등급·후속 소관 기록 | particle 텍스처만으로 실제 가구 형상이나 block entity renderer를 확정하지 않음. 미인증 실제 렌더는 **명시적 미확인**으로 닫음 |
| **E4 독립·원격** | 86개 행의 분모·원본·분류 독립 재계산, A/B/C/D·v69 보존, GitHub 원격 SHA·행수·본문 재조회 | 불일치나 소관 없는 예외가 남으면 `E_BLOCKED_AT_ENTRY4` |

E1~E4가 모두 통과하면 **`E_COMPLETE_SOURCE_EXCEPTION_SCOPE`**로 종료한다. 이 상태는 원본 자산과 특수 표현의 **증거 경계·예외 책임을 분류한 소스 범위 완료**이며, 게임 상태 레지스트리나 실제 엔진 렌더의 인증을 뜻하지 않는다. 실제 렌더러 클래스의 원본 연결을 확인하지 못한 모델은 `UNVERIFIED_RUNTIME_RENDERER`로 남긴다. 공식 배포 JAR 인증·인게임 화면이 수행되지 않았다면 성공한 것처럼 기재하지 않는다. A/B/C/D 및 v69 원장, C `heavy_core` 정정, 1-1 승인150/150, 상위 완료1/5는 유지한다.
