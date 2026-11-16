# 1-2-C Entry5 · 원본 UV·텍스처·PNG 종료 보고서

Minecraft Java 1.21.11 · 2026-11-16 · 시작 원격 `main` `efedcdbee50d53ee9f4c7c5b7208d496fa07ed59`.

## 이번 고정 배정

Entry5 **732개(P1 154/P2 333/P3 245)**를 `C_FIXED_SCOPE_2390.csv`에서 선정해 원본 leaf/부모 SHA·기하 face·texture 슬롯·UV 키와 값을 조사했다. 적용 face **7,622개**는 명시 UV **6,251**, 원본 `uv` 키 부재 **1,371**개다. 텍스처 바인딩 2,803행, PNG **577경로·전체 RGBA 248,576픽셀**, `.mcmeta` 43경로를 기록했다. 템플릿의 미바인딩 **590면**은 실제 하위 모델로 확인했다. 기존 Entry1~4의 결과를 신규 Entry5 모델 실적으로 다시 세지 않았다.

## 전체 고정 범위와 종료 감사

| 항목 | 최종 원본 근거 |
|---|---:|
| 모델 신원 | **2,390** = C 직접 **2,304** + E 예외 **86** |
| 적용 face | **23,090** = 원본 명시 UV **18,808** + 원본 키 부재 **4,282** |
| texture 판정 | PNG 연결 **21,590면** + 실제 자식이 확인된 템플릿 미바인딩 **1,500면** = **23,090면** |
| PNG 고유 경로·전체 RGBA | **1,073개·413,440픽셀**, 경로/SHA 중복 제거 |
| `.mcmeta` 고유 경로 | **97개**, 존재/SHA 확인 |
| v69 P1 선행 값 연결 | **544개** 원본 경로/SHA 및 C 관련 원장 열 값 대조 |
| 설명되지 않은 참조/PNG 누락 | **0** |

`C_ENTRY5_INDEPENDENT_SOURCE_EXIT_AUDIT.json`은 고정 배정·원본 Git blob SHA·부모 체인·face마다 원본 속성과 슬롯 해석·PNG 전체 재복호·선행 값·보호 파일 SHA를 독립 대조했다. 과거 v69 값은 출처와 함께 보존하지만 과거 주장 전부를 새로 인증하거나 이번 단계의 최초 발견으로 계산하지 않았다. `C_SCOPE_2390_FINAL_STATUS.csv`가 각 모델의 최종 판정, `C_HISTORICAL_P1_544_PROVENANCE.csv`가 선행 값의 출처를 담는다.

### Entry4 `heavy_core` 6면 정정

Entry4 보고서의 bare `"all"` 6면 미해결 판정은 **최종 판정에서 정정**한다. 사용자 제공 1.21.11 클라이언트 추출 클래스 `hqp.class`의 정적 bytecode에서 슬롯 조회가 앞의 `#`를 선택적으로 제거해 키를 찾고, `iog.class`는 그 조회가 없을 때만 직접 경로로 돌아간다. 따라서 bare `all`은 이 모델의 슬롯 `all: block/heavy_core`를 가리킨다. 원본 모델·클래스·PNG blob SHA와 PNG RGBA 256픽셀을 별도 증거로 기록했다. 기존 Entry4 파일은 수정하지 않았으며 `HEAVY_CORE_FACE_ERRATUM.csv`의 6행을 최종 집계에 적용했다.

## 게이트와 한계

- **C1** 범위·선행 출처 PASS, **C2** face·UV·슬롯 PASS, **C3** 연결 PNG 전체 RGBA PASS: 원본 소스 범위.
- **C4** 독립 로컬 감사 PASS, GitHub 원격 파일 SHA·행수·내용 재조회는 **커밋 후 판정**한다.

이 결과는 사용자 제공 추출 클라이언트와 원본 자산의 **정적 소스 검증**이다. 공식 배포 JAR의 인증, 게임 런타임 렌더, 암시 UV 엔진 계산, blockstate 조립, 애니메이션 재생은 인증하지 않는다. E의 86개 예외, D/E/F/G 후속 소관도 그대로 유지한다. 고정 계약에 따라 Entry6을 생성하지 않는다.

## 재현 파일

`C_SELECTION.json`, `MODEL_SOURCE_EVIDENCE.csv`, `FACE_UV_EVIDENCE.csv`, `TEXTURE_BINDINGS.csv`, `PNG_RGBA_EVIDENCE.csv`, `PNG_MCMETA_SOURCE.csv`, `UNRESOLVED.csv`, `UNBOUND_TEMPLATE_EVIDENCE.csv`, `UNRESOLVED_NON_TEMPLATE.csv`, `SELECTED_P1_PRIOR_C_FIELDS.csv`, `C_ENTRY5_AUDIT.json`, `C_SCOPE_2390_FINAL_STATUS.csv`, `C_PNG_UNIQUE_ALL.csv`, `C_UNBOUND_TEMPLATE_ALL.csv`, `C_HISTORICAL_P1_544_PROVENANCE.csv`, `C_ENTRY5_COMPILED_SUMMARY.json`, `C_ENTRY5_INDEPENDENT_SOURCE_EXIT_AUDIT.json`, `HEAVY_CORE_CLIENT_BYTECODE_EVIDENCE.txt`, `HEAVY_CORE_PNG_RGBA_EVIDENCE.json`, `HEAVY_CORE_FACE_ERRATUM.csv`. 실행: `scripts/phase_1_2_c_entry1.py`, `phase_1_2_c_entry4_support.py`, `phase_1_2_c_heavy_core_erratum.py`, `phase_1_2_c_exit_compile.py`, `phase_1_2_c_exit_audit.py`.
