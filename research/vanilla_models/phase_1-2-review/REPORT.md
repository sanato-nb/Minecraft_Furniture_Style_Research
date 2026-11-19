# 1-2 전체 종료 심사

**2026-11-19 KST · PASS · Minecraft Java 1.21.11 바닐라 모델·상태의 고정 연구 범위 종료 승인.**

[별도 심사 기준](../../../docs/vanilla_models_1-2/1-2_STAGE_EXIT_SEPARATE_REVIEW.md)과 [1-2 연구계획](../../../docs/vanilla_models_1-2/WORK_PLAN.md#연구-대상범위)에 따라 A~G 종료 근거를 대조했다. 원격 기준은 GitHub `main`의 [b2960c6 커밋](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/commit/b2960c684f8e48ef3b413d408853cfd8a96d7746)이다. 판정은 지정된 소스와 모형 분석 산출물, 명시된 예외의 충족 여부에 적용한다.

| 구분 | 판정 | 확인 근거 |
|---|---|---|
| A 원본 범위와 이력 | PASS | 모델 2,390개·블록상태 1,168개·PNG 1,111개와 별도 `.mcmeta` 99개를 공식 JAR에서 다시 읽었다. 파일 크기와 Git blob SHA가 원장 및 원격 Git 트리와 모두 일치했다. 우선순위 P1 544개·P2 1,039개·P3 807개를 확인했다. [A 종료 보고](../phase_1-2-A_completion/round3/A_FINAL_REPORT.md) |
| B 원본 기하·계보 | PASS | B 우선 배정 모델 2,360개와 E 우선 30개를 확인했다. B·C·F의 2,390개 전체 모델 경로·SHA가 같은 원본 집합을 가리킨다. [B 종료 보고](../phase_1-2-B/entry10/B_FINAL_CLOSURE_REPORT.md) |
| C 면·UV·텍스처 | PASS | 적용면 23,090개, 명시 UV 18,808개·UV 키 생략 4,282개, PNG 결합 21,590면·템플릿 슬롯 미바인딩 1,500면을 G 재실행에서 같은 수로 재현했다. [C 종료 보고](../phase_1-2-C/entry5/C_ENTRY5_REPORT.md) |
| D 블록상태 조립 | PASS | 블록상태 1,168개에서 정적 상태 9,193개와 모델 옵션 적용 19,440건을 확인했다. [D 종료 보고](../phase_1-2-D/entry6/D_FINAL_CLOSURE.md) |
| E 특수 표현·예외 | PASS | 고정 분모 86개. 대표 배치 계획을 재생성했고 기존 클라이언트 로그에서 상태 84개를 확인했다. 나머지 2개는 블록상태가 직접 선택하지 않는 템플릿이다. 기존 화면 7개는 저장된 SHA-256 및 이미지 무결성을 검증했다. [E 종료 보고](../phase_1-2-E/entry4/E_FINAL_CLOSURE.md) · [E 후속 검증](../phase_1-2-E/followup/REPORT.md) |
| F 유형화·시각 증거 | PASS | 모델 2,390개 원장과 자식 표면·애니메이션 원본 프레임 후속 결과를 대조했다. PNG 16종의 원본 프레임 214개·재생 순서 232단계가 포함된 산출물 6개를 다시 생성했고 저장본과 바이트 단위로 일치했다. [F 종료 보고](../phase_1-2-F/entry6/F_FINAL_EXIT_REPORT.md) · [F 후속 검증](../phase_1-2-F/followup/REPORT.md) |
| G 교차 정합성 | PASS | 승인 게이트 6/6을 확인했다. 독립 집계 56개 검사와 원본·메타데이터 원장을 다시 실행해 산출물 3개가 바이트 단위로 일치했다. [G 종료 보고](../phase_1-2-G/final/G_FINAL_EXIT_REPORT.md) |

공식 배포 메타데이터에 기록된 1.21.11 클라이언트 SHA-1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`를 사용했다. E 런타임은 기존 로그와 캡처를 재검산한 대표 상태 범위다. F 재생 순서는 원본 파일과 메타데이터에서 재현했다. 전체 변형·리소스팩·애니메이션의 실제 재생과 보간 검증은 별도 범위다.

## 1단계 마감

1-2 전체 심사가 통과했다. 1-1 고정 재질 연구, 1-3 모드 구조 연구, 1-4 텍스처·UV, 1-5 비교 연구의 기존 종료 증거와 합쳐 **1단계 고정 연구 범위 5/5 종료 승인**으로 판정한다. 2단계 인계는 규칙서 후보 14건과 반례·적용 제한 7건을 사용한다. [1단계 최종 현황](../../../docs/PHASE_1_SUMMARY.md) · [1-5-F 증거](../../furniture_mods/phase_1-5/F/REPORT.md) · [2단계 인계표](../../furniture_mods/phase_1-5/E/PHASE2_HANDOFF.csv)

## 검산 자료

[기계 판독 집계](REVIEW_AUDIT.json) · [상위 심사 검산 스크립트](audit_review.py)

원격 기준의 문서와 원장을 새 작업 폴더에 복사하고, 고정 원본 경로 4,768개를 대조한 JAR에서 준비했다. `scripts/phase_1_2_g_global_exit_audit.py`의 재생성 산출물은 기존 G와 같은 상대 경로로, E 후속 배치 계획은 `E-replayed/E_FIXTURE_PLAN_86.csv`로, F 후속 재생성은 `F-replayed/`로 뒀다. 저장소에서 `python research/vanilla_models/phase_1-2-review/audit_review.py --jar CLIENT.jar --replay REPLAY_ROOT`로 비교 결과를 다시 계산한다.
