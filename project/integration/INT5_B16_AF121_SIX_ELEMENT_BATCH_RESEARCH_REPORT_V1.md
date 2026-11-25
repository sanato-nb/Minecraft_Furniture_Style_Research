# INT-5-B16 — AF121 원본 미검증 6요소를 한 번에 실제 Minecraft F2 비교 연구

작성일: 2026-11-25 KST. 직계: [INT-5-B15 Draft PR #127](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/127) HEAD `886dceab0a9b56f066605df3d413ff9cdb246d04`. 원본 main과 과거 Draft 증거를 병합하지 않고 이 HEAD에서 분기.

## 1. 실제 배치 연구 목적

이전 B15는 AF123 tucked 의자의 미검증 6개 소스 요소를 한 PR/여섯 CI 병렬 실험으로 실제 분석해 **5개 bounded PASS, index5 한 개 두 시점 화면 변화 미검출**을 기록했다. B16에서는 다른 독립 원본 모델인 AF121 기본 의자에서 아직 개별 실게임 개입하지 않은 **6개**(0·1·2·3·5·6)를 **한 개의 PR·Actions 병렬 6 job**으로 연구한다.

| 원본 모델/요소 | 원본 면 수 | B3 기하·텍스처 기반 역할 가설 | B15 기준 상태 |
|---|---:|---|---|
| AF121 / AF1393 / 0 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 1 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 2 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 3 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 5 | 4 | LOWER_FRAME | 미시험 |
| AF121 / AF1393 / 6 | 4 | LOWER_FRAME | 미시험 |

기존 B7/B9/B10/B11에서 검증한 AF121 4·7·8·9는 **다시 성공 사례로 더하지 않는다**. 고정 원본 B3 45부품 역할/face 증거 Git blob SHA1 `d314941b950b70fa637536f86182eb4866b7aed1`, 그리고 B15 전체 45행 상태 CSV를 정확 ID로 연결한다. 위 '다리/하부 프레임' 명칭은 **기능·재질 승인 전의 기하 역할 가설**이다.

## 2. 실제 소스와 영구 검증 계약

- Minecraft Java **1.21.1 Fabric**, 공식 Another Furniture **Fabric 4.0.2** JAR 원본 SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`, parent `template/chair` 원본 Git blob `31c643617a7178ac5113702e785620f4d1150adf`, target child `acacia_1` 원본 blob `2261460299d13a15220f4fecfe059628ac28e813`, 음성대조 sibling child `acacia_3` blob `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`.
- 원본 부모 10 요소·46 faces. 각 CI job은 원본 자식 `acacia_1.json` 단일 리소스만 임시 재정의하고 **해당 인덱스 한 요소만 제거**하여 9 요소·41 또는 42 faces. 나머지 원본 부모·`acacia_3` 비교 자식·텍스처·모든 다른 원본 JAR 멤버는 압축 전 바이트 동일, ZIP CRC 및 Git blob 검증.
- 정상 원본 상태 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`, 비교 컨트롤 `variant=3`, 고정 시점 south/north. 기존 원본 H15 원본 실제 F2 **8장**, artifact `14851461698`, ZIP SHA256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`를 각 job의 기준으로 엄격 재개봉.
- 모든 작업은 별도 창/일회성 세계에서 네 단계 `model1 A → model3 음성대조 → model1 A 복원 → AIR`를 두 대향 시점에서 검사. **job당 새 F2 8장, 원본 서버 상태 마커 8개**, ZIP·PNG·로그 SHA/원본 ROI 픽셀·음성대조·반복 A/A 검사. 화면이 같으면 미검출/조건부로 보존하며 임의로 PASS 처리하지 않는다.
- 시각 변화가 나와도 원본 특정 요소의 화면 변화 **인과 응답**만 한정해 승인한다. 실제 face별 GPU 픽셀 배타적 소유권이나 기능·좌판 착석·재질·스타일·제삼자 AI 학습/재배포 권리를 의미하지 않는다.

## 3. 배치 실행 코드 및 CI

- `src/mcfr/int5_b16_af121_six_element_batch_f2.py`: B11의 실제 원본 H15/Fabric 재검증 경로를 공통화하고 동적 원본 요소 정확 ID/face 수·원본/음성대조 인과를 배치화.
- `src/mcfr/runtime.py`: `int5-b16-af121-batch-f2 --index {0,1,2,3,5,6}` 명령, 동일 공식 AF121 source fixture.
- `tests/knowledge/test_int5_b16_af121_six_element_batch_f2.py`: 13개 원본/음성대조/미승인 회귀시험.
- `.github/workflows/integration-int5-b16-af121-six-element-batch-f2.yml`: **6개 매트릭스 작업, fail-fast false, 병렬 3개**, 각 작업 개별 네이티브 F2/서버/출처 독립 감사.
- 성공 또는 불일치 발생 시 각 job 아티팩트는 자신이 캡처한 실제 PNG/client.log/JSON·메타데이터만 업로드한다. **임시 JAR·타사 텍스처/모델을 배포하지 않는다**.

## 4. 정확한 완료 범위와 다음 단계

- 배치 시작 시 기정 검증 인과 PASS **14/45**, 화면 미검출 **1**, 미시험 **30**.
- B16 여섯 요소 모두 독립 bounded PASS일 때만 **최대 20/45**. 화면 효과 0·실험 실패·양성대조 혼선이 나오면 해당 요소 단위 보류, 이전 검증 결과로 대체하지 않는다.
- B16 이후 아직 HC11210 **12개**, Macaw MACAW67 **12개**(별도 Minecraft 1.21.11/원본 JAR), 기존 AF123 index5 미검출의 원인까지 남는다.
- 기존 엄격 **H03 HOLD, H05 CONDITIONAL, F70 무조건 승인 0/70**, INT-5 최종 부품 의미 승인 0/45, INT6 타사 학습·재배포 허가 0은 불변.

**실제 Actions가 끝나고 PNG·로그·서버 상태·ZIP SHA를 검증하기 전에는 신규 인과 성공 숫자를 기록하지 않는다.**

## 5. 실제 B16 6개 요소 통합 게임 검증 결과 — GitHub Actions 성공

[실제 B16 GitHub Actions #45604664928 — **여섯 매트릭스 Job 모두 SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45604664928), 검증 소스 SHA `12e6143356462282da2b9a577a73f626d5d0bd0c`. 정적·부정 회귀시험 13개, 각 공식 JAR의 개별 single-child 원본 요소 개입, Minecraft 1.21.1 원본 F2 양면 **신규 48장**, 서버 블록 상태 **48건** 검증. 원본 H15 ZIP `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`에서 원래 8장 F2 SHA/CRC 재확인.

| AF121 source index | 원본 면 | 남쪽 제거 응답(px) | 북쪽 제거 응답(px) | 엄격한 한정 인과 판정 |
|---|---:|---:|---:|---|
| 0 | 5 | 0 | 159 | **PASS** |
| 1 | 5 | 179 | 0 | **PASS** |
| 2 | 5 | 0 | 159 | **PASS** |
| 3 | 5 | 155 | 0 | **PASS** |
| **5** | 4 | **0** | **0** | **두 시점 모두 미검출: 인과 PASS 아님** |
| 6 | 4 | 304 | 304 | **PASS** |

**기계 및 독립 재검증:** 신규 여섯 아티팩트 ZIP을 직접 모두 내려받아 CRC·원본/수정 F2 PNG 48개의 SHA/1024×684 픽셀·모델3/AIR/시간 대조와 변경 영역을 독립 계산. 모든 음성대조와 원본 전경 밖 변화는 0픽셀, A/A 반복 픽셀 수는 동일. 실제 원본 JAR/부모/변형3 비교 자식 바이트 동일성·서버 마커는 각 CI job에서 확인. 최종 CI SUCCESS는 **5개 렌더 인과 PASS, 1개 화면 응답 미검출**을 의미하며 6개 모두 인과 승격하지 않는다.

### 처음 실패한 워크플로와 복구

첫 [Actions #45604081587](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45604081587)은 **각 새로운 F2 8장 촬영·서버 마커 8개를 이미 남겼으나** `src/mcfr/runtime.py`의 허용된 캡처 완료 상태 문자열에 신규 B16 `ACTUAL_SOURCE_ELEMENT_SELECTED_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT`가 누락되어 각 job 종료 코드 1. 실제 PNG를 직접 재개봉해 가구 요소 0/1/2/3/5/6의 초기 반응을 확인한 뒤, 정상 캡처는 성공으로 종료하고 **후속 독립 감사 단계가 최종 승인하도록 분리**하는 최소 수정 후 새 Actions #45604664928에서 6개 모두 실제 검증 SUCCESS. 실패를 최종 성공이라고 과장하지 않고 기록.

## 6. AF121↔AF123 원본 요소5/6 교차 연구 (서로 다른 두 모델 검증)

| 고정 original 모델 | index5 from→to | index6 from→to | index5 제거 두 시점 | index6 제거 두 시점 |
|---|---|---|---|---|
| AF121 기본 | [13,2,3]→[3,4,13] | [3,2,3]→[13,4,13] | 0/0 px | 남304/북304 px |
| AF123 tucked | [13,2,-6]→[3,4,4] | [3,2,-6]→[13,4,4] | 0/0 px | 남238/북0 px |

각 모델에서 index5와 index6은 좌표 정규화 시 **같은 기하 범위**이나 **index5의 X좌표 from→to 순서가 역전**이다. 실제 두 서로 다른 소스/블록상태·게임 실험 모두에서 index5 제거가 현재 두 시점 F2에 변화를 주지 않고 index6 제거는 변화를 보였다. 이는 모드 간, 같은 2개 모델 variant 간 **재현된 이상 징후**로 관찰된다. 면 winding/역좌표 렌더 해석/가림/텍스처/UV 중 원인이 무엇인지는 아직 미증명. **index5가 필요 없는 요소라거나 공식 모드 버그라고 결론 내리지 않는다.**

## 7. 4개 원본 모델 전체 다음 배치 및 범위

| 고정 모델 | 원본 요소·면 | 누적 제한 인과 PASS | 화면 반응 미검출 | 미실험 |
|---|---:|---:|---:|---:|
| AF121 | 10/46 | **9** | **1** | **0** |
| AF123 | 10/46 | **9** | **1** | **0** |
| HC11210 | 13/78 | 1 | 0 | 12 |
| MACAW67 | 12/59 | 0 | 0 | 12 |
| **합계** | **45/229** | **19** | **2** | **24** |

따라서 **실제 단일 원본 요소 제거→게임 렌더 응답 인과 19/45=42.22%**; 화면 미검출 2개, 단독 개입 실험 아직 24개다. 두 의자 모델의 검증이 곧 해당 모드 전체/모든 게임 상태의 검증은 아니다. 남은 독립 모델은 **Handcrafted 12개(1.21.1), Macaw 12개(1.21.11)**로 별도 원본 버전/상태·음성대조의 대규모 배치로 설계할 수 있다. HC는 드롭 아이템과 검정/흰색 컨트롤, Macaw는 별도 원본 F2/실행 JAR이 필요하다.

영구 JSON `project/integration/INT5_B16_SIX_REAL_F2_FOUR_MODEL_AUDIT_V1.json`에는 각 job 정확 원본 키·실제 F2·아티팩트 ZIP SHA·로그 SHA·B15 모델 교차 단서를 저장하고, CSV `project/integration/INT5_B16_FOUR_MODEL_45_ELEMENT_BATCH_STATUS_V1.csv`에는 **45행 정확 원본 키별** PASS·미검출·미실험을 중복 없이 저장한다. 과거 H03 HOLD / H05 CONDITIONAL / 엄격 F70 무조건 PASS 0/70, GPU face↔pixel 소유권 승인 0, INT5 기능·재질·스타일 승인 0/45, INT6 제삼자 모델/텍스처 AI 학습·재배포 허가 0은 변하지 않는다.
