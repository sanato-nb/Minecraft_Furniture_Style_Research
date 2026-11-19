# 1-5-F 독립 종료 감사

**2026-11-19 KST · 통과 · 1-5 고정 바닐라↔가구 모드 비교 범위 종료 승인.**

감사 기준은 GitHub `main`의 [84842b0 커밋](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/commit/84842b0516af1aaa9a4dcc7b1fb73ee798b96f87)이다.

| 검사 | 결과 | 근거 |
|---|---|---|
| A 고정 범위·출처 | PASS | 모드 47상태·52모델 적용·1,610면. 바닐라 대조군 15개에 쓰인 공식 1.21.11 JAR 자산 74개를 다시 읽고 Git blob SHA-1·SHA-256을 대조했다. |
| B 비교 키·복합 상태 | PASS | 전체 62표본·74모델 적용·390요소·1,844면·109프레임. 중복 키, 상위 키 연결, 행 수와 복합 선택을 검산했다. 바닐라 울타리와 조각된 책장은 각각 모델 2개와 7개를 적용한다. |
| C 교차 비교·반례 | PASS | 9유형·21판정과 제한 판정 7개의 ID를 대조했다. 판정과 인계 내용은 일치했다. |
| D 예외·런타임 | PASS | 누락 부모 48개, 상태 예외 6건, 텍스처 예외 85개를 대조했다. 런타임 판정 10/10을 확인했다. 두 버전의 클라이언트를 새로 실행해 R10 77/77개 표시 경로를 재현했다. |
| E DB·인계 | PASS | SQLite 재생성본이 저장본과 같았고 무결성 및 외래키 검사도 통과했다. 규칙서 검토 후보 14건과 반례·적용 제한 7건을 확인했다. |
| F 저장본 검증 | PASS | A~E 재생성 22파일이 GitHub 저장본과 바이트 단위로 일치했다. 원격 기준의 본문 83개와 CSV·TSV 31개의 행 수를 확인했다. |

## 런타임 재실행

| 구분 | Minecraft | 행 | 저장본 대조 |
|---|---|---:|---|
| 비교 렌더 | 1.21.1 | 2,097 | 가구 망치와 흰 쿠션의 앞·뒷면 출력 순서 4행 차이. 각 아이템의 면, 정점, UV, 스프라이트는 모두 일치 |
| 비교 렌더 | 1.21.11 | 1,449 | 바이트 일치 |
| 아이템·파티클 전수 | 1.21.1 | 3,379 | 바이트 일치 |
| 아이템·파티클 전수 | 1.21.11 | 4,104 | 바이트 일치 |

클라이언트 관측은 고정 버전·표본과 R10의 기본 아이템 스택 및 블록 파괴 이벤트에 적용한다. 기존 월드·인벤토리 이미지 14개의 파일 무결성과 측정표의 링크를 확인했다. 월드 화면 근거는 기존 관측을 사용했다. E의 SQLite는 정적 비교 스냅샷이고 최신 런타임 결과는 D 후속 판정표에 있다. [D 후속 근거](../runtime_followup/REPORT.md) · [판정표](../runtime_followup/RUNTIME_VERIFICATION.csv)

## 1단계 전체 판정

**상위 과제 4/5 종료 승인. 1단계 총괄 종료는 1-2 전체 심사 대기.** 1-4-F 공식 판정은 통과다. 1-2-G의 소스 교차 감사는 6/6 통과했고, 1-2 전체 판정은 별도 심사 문서와 상태 원장에 대기로 기록돼 있다. 2단계 인계 근거는 E의 21건을 사용한다. [1-4-F 종료 근거](../../phase_1-4/F/REPORT.md) · [1-2 상위 심사](../../../../docs/vanilla_models_1-2/1-2_STAGE_EXIT_SEPARATE_REVIEW.md) · [1단계 현황](../../../../docs/PHASE_1_SUMMARY.md)

## 재현 자료

[감사 집계](EXIT_AUDIT.json) · [재조회한 입력 파일·행 수·SHA](REMOTE_INPUT_MANIFEST.csv)

저장소 루트에서 `bash research/furniture_mods/phase_1-5/F/replay_static.sh WORK AF_GIT HC_GIT MACAW_JAR MC_1.21.1_JAR MC_1.21.11_JAR`로 A~E를 재생성한다. A의 교차 대조에는 1-2-G의 `final`과 Entry 1~6 옵션 원장, 1-2-E Entry1 모델 원장이 필요하다. 런타임은 [D 재현 방법](../runtime_followup/REPORT.md)을 따라 버전별 `comparison-<버전>.tsv`와 `R10-<버전>.tsv`를 WORK에 기록한다. `python research/furniture_mods/phase_1-5/F/audit_exit.py --replay WORK --vanilla MC_1.21.11_JAR --remote-ref 84842b0516af1aaa9a4dcc7b1fb73ee798b96f87 --out OUTPUT`으로 고정 입력과 재생성본을 검산한다.
