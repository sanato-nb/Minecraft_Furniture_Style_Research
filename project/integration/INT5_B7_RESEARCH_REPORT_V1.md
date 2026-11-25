# INT-5-B7 — AF121 기본 의자 element 4, 독립 실제 Minecraft F2 인과 검증

검증일 **2026-11-25 KST**. 직계 [INT-5-B6 Draft PR #118](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/118) head `83d48db20b5da3626944adabcd77d62aa912b403`에서 새 누적 [INT-5-B7 Draft PR #119](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/119)로 분기. `main`과 B3~B6 기존 감사 DB는 변경·병합하지 않았다.

## 1. 연구 질문과 실제 종료 기준

B6 45개 원본 요소 원장에서 **AF121 기본 의자·연구 원본 제공자 AF1393·element index 4·소스 6면·`SEAT_LAYER` 역할 가설**은 최우선 미실험 후보였다. 기존 B5의 `AF123` 접힌 의자 사례와 별도로 **원본 `AF121_north` 기본 의자에서 정확한 소스 요소 4를 삭제했을 때** 네이티브 Minecraft 화면이 어떻게 변하는지 비교했다.

이번 연구는 원본 모델의 **출처가 고정된 단일 소스 요소 제거 → 실게임 렌더 결과 변화**만을 승인한다. 원래 4번 요소가 화면의 모든 변경 화소를 배타적으로 차지했다는 의미나 실제 앉기 기능·재질·스타일·학습/재배포 권리를 승인하지 않는다.

## 2. 실제 공식 출시판과 격리된 단일 수정

- 실제 게임: **Minecraft Java 1.21.1 Fabric**, Another Furniture Fabric **4.0.2**. 공식 JAR 원본 SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`.
- 원본 선택 블록상태: `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`, 원본 선택 자식 `another_furniture:block/chair/acacia_1`. 검증 비교 변형: `facing=north,tucked=false,variant=3` → `acacia_3`.
- 실제 모델/템플릿: `acacia_1.json` → `template/chair.json`의 **10요소·46면** 상속. `element 4` 원본 6면만 제외한 **9요소·40면**을 임시 **자식 `acacia_1.json` 단일 파일에만** 명시적으로 오버라이드했다.
- **공통 `template/chair.json`과 비교용 `acacia_3.json` 및 기타 모든 JAR 멤버의 압축 전 원본 바이트 유지**, ZIP CRC 및 정확한 단일 변경 모델 검증. 실제 임시 JAR SHA-1 `11a47ca897e658bd0a879a8bc3f3a9a7e15e8bf9`.
- 고정 출시판 Git blob SHA-1: 원본 자식 `acacia_1.json` = `2261460299d13a15220f4fecfe059628ac28e813`, 비교 자식 `acacia_3.json` = `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`, 원본 부모 `template/chair.json` = `31c643617a7178ac5113702e785620f4d1150adf`.
- **중요한 출처 차이:** 연구본 Git **4.0.3**과 실행판 Fabric **4.0.2**는 JSON 의미가 같아도 Git blob byte SHA가 달랐다. 첫 [Actions #45541214422](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45541214422)는 이를 혼동하여 **보수적으로 실패**했다. H12의 원본 실행판 핀과 실제 리소스 SHA를 재확인하도록 고친 후 **새 게임 시험이 성공**했다. 서로 다른 버전의 바이트 동일성을 허위로 주장하지 않는다.

## 3. 실제 네이티브 F2와 원본의 엄격한 비교

[**INT-5-B7 실제 Actions #45541413294: 전체 SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45541413294)

- **원본 촬영 8장:** 기존 H15의 공식 Fabric 4.0.2 실게임 원본 [ZIP 아티팩트 #14851461698](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/workflows/integration-int4-h15-af-opposing-real-f2.yml) SHA-256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462` 전체 재검증; 원본 게임 server acknowledgement, 고정 카메라 및 개별 F2 PNG SHA 확인.
- **신규 촬영 8장:** 별도 신생 일회성 세계의 실제 Minecraft 1.21.1 Fabric에서 **남쪽 4장·북쪽 4장**. 순서 `A(AF121 variant1) → B(미수정 variant3) → A복원 → AIR`. **새 게임 내 원본 정확 블록상태 8/8개** 확인, 8/8 PNG 원본 1024×684 F2 SHA 확인.
- **합계 2개 실제 게임 세션·원본/수정 F2 16장 비교.** 신규 게임 실행은 **1회, 신규 F2 8장**. 임시 수정 JAR/모드 JSON/원본 텍스처 바이트는 Git에 저장하지 않음.
- 새 실제 F2와 로그/원본 SHA 감사 아티팩트 [**#14989138256**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45541413294/artifacts/14989138256) (45일 유효), 영구 텍스트 감사 `project/integration/INT5_B7_AF121_ELEMENT4_INDEPENDENT_CAUSAL_AUDIT_V1.json`.

## 4. 실제 픽셀 차이와 반증용 음성대조

동일 H15 카메라·동일 블록상태에서 original-vs-patched 프레임을 ROI `[350,275,675,620]`, RGB 채널 차이 임계값 **24**로 재검사했다.

| 실제 원본 ↔ 임시 요소 제거 | 남쪽 관찰 카메라 | 북쪽 관찰 카메라 |
|---|---:|---:|
| **AF121 A(변형1) element4 제거 전후** | **1,182px** | **2,132px** |
| **A 복원 비교(동일 변화 재현)** | **1,182px** | **2,132px** |
| **미수정 변형3 B 비교의 변화** | **0px** | **0px** |
| **AIR 비교의 변화** | **0px** | **0px** |
| **원본 게임 A↔A 복원 시간 변화** | **0px** | **0px** |
| **수정 게임 A↔A 복원 시간 변화** | **0px** | **0px** |
| **원래 AF121 의자 전경 바깥의 변화** | **0px** | **0px** |
| 원래 AF121 의자 전경 vs AIR 크기 | 3,552px | 4,216px |

**실측 결론:** 정확한 AF121 원본 index4 요소를 **해당 자식 모델만** 임시 제거하면, 다른 변형 의자와 AIR가 바이트 원본 모델 그대로인 상태에서 남쪽 **1,182px**, 북쪽 **2,132px**의 재현 가능한 화면 차이가 생긴다. `PASS_AF121_ISOLATED_CHILD_ELEMENT4_REMOVAL_NATIVE_F2_RESPONSE` **한정 실험 결과**를 통과했다.

이 수치 자체를 '원본 요소4가 화면에서 직접 차지한 픽셀'로 해석해서는 안 된다. 제거 후 뒤의 다른 요소·광원·그림자·차폐가 바뀔 수 있기 때문이다. 소스 `seat/acacia.png` 경로와 형상은 **좌판 역할 가설에 대한 단서**이지 실제 가구 기능 입증이 아니다. AF121에 대해 시험된 블록은 오직 **북향 원본 상태 하나**이며 다른 방향·모드·원본 43개 부품에는 결과를 일반화하지 않는다.

## 5. INT-5 누적 상태 — 정확한 서로 다른 분모

| 연구 항목 | 누적 현황 |
|---|---:|
| B3 고정 원본 의자 요소 | **45/45 소스 근거 연결** |
| 원본 face UV | **229/229** |
| 원본 역할 그룹 | **15/15** |
| **서로 다른 소스 요소 제거→실게임 렌더 인과** | **2/45** (AF123 4번 + AF121 4번) |
| 요소별 렌더 개입 시험 미실행 | **43/45** |
| 역할 지시 원본 텍스처 단서 9개 중 개입 시험 확인 | **2/9**, 나머지 7개 미실험 |
| 원본 요소별 배타적 GPU 픽셀 귀속 확정 | **0/45** |
| 부품 기능·재질·스타일의 최종 의미 승인 | **0/45** |
| INT-6 AI 학습·재배포 권리 승인 | **0** |

기존 B5 AF123은 top slab 유지·`tucked=true` 조건하에서 **남 751px/북 0px**이라는 독립적인 별개 실험이다. 이번 AF121은 `tucked=false` 기본 의자이며 슬랩이 필요 없다. 다른 모델의 원본 4번 요소라 해도 두 픽셀 수치/가림 특성을 서로 전가하거나 일반 법칙으로 승인하지 않는다. B6의 역사적 1/45 결론은 B6 당시의 참인 수치로 보존하며, 이번 B7에서만 **독립 실험 2/45로 누적**한다.

## 6. 다음 연구 및 보류

- 다음 우선 후보는 Handcrafted `HC11210`의 원본 element12 쿠션 텍스처 역할 단서이다. **아직 실제 단일 요소 제거 F2 시험 미실행**.
- INT-5-C 재질·스타일·쉐이딩 의미 확정과 INT-5-D 전체 독립 감사도 미완.
- 원래 엄격 INT-4 **H03 HOLD, H05 CONDITIONAL, F70 무조건 승인 0/70** 그대로, INT-4 별도 모델링 범위 한정 성과도 변경하지 않는다.
- 새 PR은 Draft 상태; `main` 병합 없음. **원본 모드·PNG·게임/실험 스크린샷 Git 커밋 없음**.

## 7. 검증 파일
- `src/mcfr/int5_b7_af121_child_element4_f2.py`: 실제 Fabric 출시본 출처 고정·자식만 변경·원본 H15과 F2 인과 독립 감사.
- `tests/knowledge/test_int5_b7_af121_child_element4_f2.py`: **10개** 부모/자식/게임 상태/음성대조/허위 승인 차단 회귀시험 성공.
- `.github/workflows/integration-int5-b7-af121-child-element4-native-f2.yml`: 실제 F2 8장·서버 상태 8·원본 모델3 AIR 대조 Actions.
- `project/integration/INT5_B7_AF121_ELEMENT4_INDEPENDENT_CAUSAL_AUDIT_V1.json`: 네이티브 F2 개별 SHA·소스 부모/자식 Git blob·2카메라·실측 픽셀/영구 승인 제한.
