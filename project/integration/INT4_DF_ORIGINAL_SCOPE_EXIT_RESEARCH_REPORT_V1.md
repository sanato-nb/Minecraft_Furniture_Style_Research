# INT-4 D/F 기존 고정 계약 재판정 — 정적 완료와 엄격한 렌더 승인 분리

작성 기준: 2026-11-24. 상위 분기 H27 Draft PR #109 head 50ca85307cdd372d28652ce3b3341266ca85279e. 신규 모드 H28을 추가하지 않고 **원래 INT4 A~H 공식 계약의 D와 F만** 검수한다. 원본 역사 원장을 덮어쓰지 않았다.

## 1. 완료 판정

| 구분 | 실제 확인 | 해당 범위 판정 |
|---|---|---|
| D 고정 모드 blockstates | **1,158/1,158 원본 소스 상태** | **정적 원본 범위 한정 종료 가능** |
| D 원본 선택 규칙·모델 참조 | **78,456/78,456**, 예외 원본 6행 독립 재대조 | 구조 원장 완결. 런타임/릴리스 동등성 별도 |
| D 엄격 모든 등록·동적 런타임 | G5 원래 조건부 1,157 · HOLD 1 | 무조건 승인 아님 |
| F 정확 사례별 F2 출처 연결 | **70/70 사례**, 원본 네이티브 이미지 실행·SHA·로그 및 역사적 사람 관찰 연결 | **근거 연결과 범위 한정 분류 종료 가능** |
| F 원래 엄격 전체 렌더 계약 | **조건부 70/70, 무조건 0/70** | **최종 승인 미완료** |
| H 독립 종료 | H03 HOLD, H05 CONDITIONAL | 최종 종료 보류 |

위 D 정적 원장과 F 시각 근거 연결의 '완료'는 기존 역사 데이터의 계약 요건에 한정한다. H23의 별도 **모델링 전용 70/70 PASS**는 F 엄격 승인 70/70을 대신하지 않는다.

## 2. D 소스 예외 여섯 행의 실제 upstream 재검증

고정 저장소: https://github.com/crispytwig/AnotherFurniture/tree/57eb624cbb7f408d43398c7434b0d38d312cb55d
고정 commit 57eb624cbb7f408d43398c7434b0d38d312cb55d, Another Furniture Git 연구 4.0.3 / Minecraft 1.21.1.

정확한 원본 파일 SHA1:
- birch_chair.json: fb91fe6fca469381b200fd080a671b5a09e77399
- spruce_chair.json: c8a57ceb9f34c255cd6b098deca6628c595be0df
- unused/white_awning.json: f1330a172a20d47a24d40288317293bc47c59511
- AFBlocks.java: 380e721488f3f0cd0a717291a185a5a938ed237d

실제 원본 Git 트리와 4개 파일의 Git blob SHA를 독립 재계산하고, D 1,158행과 G3의 여섯 예외 원장을 대조했다.

- **birch_chair** 남향·tucked=false·variant=3은 원본에서 birch_1, y=180을 선택한다.
- **spruce_chair** 동일한 상태는 원본에서 spruce_1, y=180을 선택한다.
- **unused/white_awning** 네 방향의 type=double은 white_double 모델을 선택하지만, 고정 Git 트리에 그 모델 파일이 없다. 원본 경로는 실제 unused 하위이다. AFBlocks.java에는 awning 명칭이 나타나지 않는다.

위 사실은 **원본 선택자를 그대로 읽었다는 검증**이지, 의도적으로 제작된 모델/버그인지, 전체 Java 등록 경로에 존재하는지, 실제 Fabric 4.0.2 릴리스와 동일한지에 대한 증명이 아니다. 기존 G5 상태 **1,157 CONDITIONAl / 1 HOLD**를 멋대로 승격하지 않는다.

D 고정 출처 1,158개 = AF 177, Handcrafted 267, Macaw 714. 총 선택 78,456건 = 로컬 78,420 + 바닐라 32 + 미해결 4. 6건의 출처·영향·후속 단계 기록은 완결됐다. **D 원본 정적 계약은 범위 한정 완료**로 인계하되 모든 실제 등록 상태/배포 버전 등가성은 미승인이다.

## 3. F 원본 70개 실제 렌더 증거 원장

과거 정확 F2 증거 미매핑 추가 대상은 **0개**이다. 새 독립 코드에서는 기존 원본 감사의 **20 ZIP·91 네이티브 F2 PNG·21 client.log** SHA·캡처 JSON 연결 및 70건의 원본 상태와 실제 화면 관찰 텍스트를 원본 범위별로 다시 대조했다. 그러나 **이번 새 CI에서 과거 이미지 바이너리를 다시 다운로드하거나 전체 70장을 사람이 재판정한 것은 아니다.**

| 원본 사례별 근거 품질 | 개수 | 다음 필수 검증 |
|---|---:|---|
| 원본 전체 로그 SHA는 맞지만 해당 사례별 정확 서버 상태 메타 부족 | **6** | 대상 상태·프레임 매칭 재확인 또는 해당 범위 최소 재현 |
| 구조화된 상태·이미지 SHA는 있지만 정확 사례 ID 로그 줄 없음 | **38** | 원본 캡처 메타와 실제 프레임/서버 상태 직접 대조 |
| 정확 사례 ID 로그 줄이 있으나 전체 프레임 인과 수용 근거 미승인 | **26** | 원본 화면·상태·시각 관찰을 종합 독립 판정 |

이 6/38/26은 서로 배타적인 **70개 근거 등급**이다. 70건 모두 새로 게임을 실행해야 한다는 뜻은 아니다. 새 원장 INT4_DF_F70_CASE_ORIGINAL_EXIT_BLOCKERS_V1.csv가 ID별 필요한 확인 범위를 기록한다. 원래 엄격 F 계약에서 아직 0/70 무조건 승인인 상태를 그대로 유지한다.

## 4. 실제 GitHub 검증 및 산출

- 독립 코드: src/mcfr/int4_original_df_gate_reaudit.py
- 영구 70건 원본 F2와 6건 D 예외 JSON: project/integration/INT4_DF_ORIGINAL_EXIT_CONTRACT_REAUDIT_V1.json
- F 70개 사례별 엄격 승인 차단 CSV: project/integration/INT4_DF_F70_CASE_ORIGINAL_EXIT_BLOCKERS_V1.csv
- 8개 위·변조 및 잘못된 PASS 승격 방지 회귀시험: tests/knowledge/test_int4_original_df_gate_reaudit.py
- 공식 실행 워크플로: .github/workflows/integration-int4-original-df-closure.yml
- [최종 독립 GitHub Actions #45389551921 — SUCCESS](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45389551921): 8/8 회귀시험 통과, 새 영구 JSON 및 70행 CSV와 실제 고정 upstream·역사 데이터 재계산 정확히 일치.
- upstream 원본 Java/JAR/PNG/F2 파일을 Git에 재배포하지 않고 파생 숫자와 출처만 저장했다.

## 5. 원래 종료 의도에 대한 최종 판정

**D:** 원본 블록상태의 전수 정적 조사·모델 선택·예외 disposition 요구를 충족하므로 **범위 한정 종료 가능**. 미검증 실제 런타임 상태·다른 릴리스가 있음을 기록한다.

**F:** 원본 70사례의 정확한 화면/로그 출처 매핑·기존 질적 관찰·조건부 분류 요구를 충족하므로 **자료 인계 범위는 종료 가능**. 그러나 원래 엄격한 전체 F 최종 무조건 종료는 **0/70, 미완료**. H03/H05의 요구를 충족했다고 거짓으로 선언하지 않는다.

**인계:** 모델링 목적으로는 이미 종료된 H23 70/70을 사용할 수 있지만, F 엄격 라이브 렌더 계약을 승인하려면 6/38/26 사례별로 실제 원본 프레임/상태와 시각 장면의 인과 관계를 추가 검증해야 한다. INT5 의미·INT6 학습/재배포 권리는 모두 미승인, main 미병합, 기존 역사 원장 불변.
