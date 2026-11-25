# INT-5-B11 — Another Furniture AF121 등받이 원본 9번 요소, 실제 Minecraft F2 독립 인과 감사

검증 기준일 **2026-11-25 KST**. 기존 [B10 Draft PR #122](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/122) 최종 HEAD `e839ac43abcdf6dce6607f512bbd0d4e7c7adc3e`에서 [B11 Draft PR #123](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/123)로 분기했다. 이전 B1~B10 원본/감사·연구 결론과 `main`을 변경하지 않았다.

## 1. 원본 소스 증거와 정확한 시험 경계

B3의 45요소 텍스처-역할 증거와 B6 원본 45행 원장·실험 큐 **5순위**를 직접 대조하여 `AF121 / AF1393 / original source element index9` 선정. `BACKREST_ASSEMBLY`는 **형상 및 역할명 텍스처 기반 가설**일 뿐 기능 승인이 아님. 원본 다섯 면이 `back_1/acacia.png` 역할명 원본 텍스처를 참조한다.

- 공식 **Another Furniture Fabric 4.0.2** 원본 JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`. 실행판 개별 JSON 원본 Git blob: `acacia_1` 자식 `2261460299d13a15220f4fecfe059628ac28e813`, 비교 `acacia_3` 자식 `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`, 공유 원본 `template/chair` 부모 `31c643617a7178ac5113702e785620f4d1150adf`. 연구 Git 4.0.3과 실제 배포판 Fabric 4.0.2 원본 JSON의 byte 동일성은 가정하지 않았다.
- 원본 선택 요소 index9의 형상: **`from=[2,7,12]`, `to=[4,16,14]`**, 원본 5면 `east`, `north`, `south`, `up`, `west`. 원본 부모 전체 **10요소·46면**.
- 공식 임시 게임 JAR의 **`assets/another_furniture/models/block/chair/acacia_1.json` 단 하나의 리소스 멤버만** 오버라이드하여 원본 요소9의 5면만 제거, 나머지 원본 **9요소·41면**을 보존. 공유 부모와 미수정 `acacia_3` 비교 자식, 모든 다른 원본 JAR 리소스 압축 해제 바이트 동일, ZIP CRC/리소스 이름 목록 검증.
- 임시 수정된 런타임 JAR SHA-1 `87efe037b27dc01551d9a0a9bf5577d47985617b`. 연구 Git이나 Actions 결과에는 원본 또는 임시 수정된 JAR·제삼자 텍스처·원본 개별 모델 JSON을 포함하지 않는다.

## 2. 실제 게임 원본↔수정 두 세션 F2 검증

[**B11 실제 Minecraft Java 1.21.1 Fabric Actions #45555779012 — SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45555779012). 검증 소스/회귀시험/Actions 코드 커밋 `d3e10ff4ab88c016e9b38f1d63a2f49f9457d2bd`.

- 원본 다른 Minecraft 세션의 H15 **네이티브 F2 8장**, 원본 ZIP SHA256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`를 **독립 다운로드하여 다시 검증**했다. ZIP 11개 항목 CRC 성공, 원본 8 PNG SHA·원본 client.log SHA 및 서버 블록상태 전체 재개봉.
- 새 Minecraft 1.21.1 Fabric 클라이언트에서 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]` 원본 북향 의자, 좌표 `(-88,120,40)`, 기존 H15와 같은 남쪽·북쪽 카메라 사용. 각 시점 `variant1 A → 원본 미변경 variant3 → A 복원 → AIR` 총 4단계, **신규 네이티브 F2 8장**과 정확 서버 블록 상태 **8/8**, PNG·client.log SHA 증거 기록.
- 원본 H15 8장 + 신규 B11 8장 = **정확한 두 실제 게임 세션의 16장**. 비교 RGB ROI `[350,275,675,620]`, 채널 최대 변화 임계값 24.

| 원본 공식 Minecraft F2 vs source9 제거 | 남쪽 | 북쪽 |
|---|---:|---:|
| **variant1 A 원본 → 단독 요소9 제거** | **366px** | **362px** |
| **variant1 A 복원 후 동일 변화** | **366px** | **362px** |
| 미수정 변형3 원본 vs 수정 비교 | **0px** | **0px** |
| AIR 원본 vs 수정 비교 | **0px** | **0px** |
| 원본 variant1 A/A 시간 변화 | **0px** | **0px** |
| 수정 variant1 A/A 시간 변화 | **0px** | **0px** |
| 원본 의자 전경 밖 변경 픽셀 | **0px** | **0px** |
| 원본 variant1 의자 전경 vs AIR | 3,552px | 4,216px |

**실제 원본 H15·수정 B11 F2 16장의 PNG를 직접 다시 열어 시각 비교**했다. 원본 의자 등받이 좌우 기둥 중 **index9에 해당하는 한쪽 세로 기둥이 단독 제거 후 사라지는 모습**이 남·북 두 방향 모두 확인됐다. 이는 소스 `[2,7,12]→[4,16,14]` 세로부에 부합한다. 픽셀 차이에는 뒤쪽 노출·가림·광원/셰이딩 영향이 섞일 수 있어 변경 픽셀 **366/362개 전체가 원래 index9의 고유 GPU 픽셀이라는 뜻은 아님**.

최종 판단 **`PASS_AF121_ISOLATED_CHILD_ELEMENT9_REMOVAL_NATIVE_F2_RESPONSE`**는 원본 `AF121/AF1393/9` 요소 제거가 **정해진 두 카메라의 실제 원본 게임 화면에 국소적 인과 효과**를 내는 것에만 제한된다. 부품 원래 구조 기능·실착석 기능·원본 UV/face별 정확 픽셀 소유권·재질·스타일·학습 및 제삼자 자산 재배포 권리를 승인하지 않는다.

## 3. 영구 증거와 재현 코드

- [**실제 신규 F2 8장·client.log·두 게임 세션 인과 감사 아티팩트 #14996007276**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45555779012/artifacts/14996007276) (45일 보존; 오래된 원본 H15 F2 8장은 별개 보존).
- `project/integration/INT5_B11_AF121_ELEMENT9_INDEPENDENT_CAUSAL_AUDIT_V1.json`: 공식 출시판 SHA, 기존 원본 H15 8 PNG SHA·신규 실제 F2 8 PNG SHA, 두 게임 로그 SHA, 8개 정확 원본 블록 마커, B11의 element9 5면 및 366/362 픽셀·음성대조 0 기록.
- 원본 성공 Actions 아티팩트 안의 실제 감사 JSON Git blob SHA-1 `4590d77384ce8aa6d85e0e327b0933a3d618204b`가 GitHub 영구 감사 JSON의 **Git blob SHA-1과 바이트 단위 일치**하는 것을 직접 검증했다.
- `src/mcfr/int5_b11_af121_backrest_element9_native_f2.py`: 실제 원본 SHA·단일 자식 요소 개입·8개 네이티브 F2·엄격 두 세션 독립 감사.
- `src/mcfr/runtime.py`: B11 원본 월드/정확 카메라 별도 명령 추가. B5~B10 기존 명령 보존.
- `tests/knowledge/test_int5_b11_af121_backrest_element9_native_f2.py`: 11개 원본 10/46→9/41, 정확 index9·원본 role 및 음성대조/권리 차단 회귀시험.
- `.github/workflows/integration-int5-b11-af121-backrest-element9-native-f2.yml`: 실제 Minecraft CI에서 원본 F2 SHA, 11개 단위시험, 공식 런타임 원본 JAR, 음성대조 zero, 원본 key `AF121/AF1393/9`, 요소9 5면 검증.

## 4. INT-5 누적 확정 상태

| 현재 확정 작업 | 누적 완료/전체 |
|---|---:|
| 원본 모델 요소 및 UV face 출처 검증 | **45/45요소 · 229/229면** |
| 소스 역할 가설 그룹 연결 | **15/15** |
| **서로 다른 원본 요소 단독 제거 → 실제 Minecraft 렌더 인과 검증** | **6/45 = 13.3%** |
| 아직 개별 실게임 제거/변경 실험하지 않은 요소 | **39/45 = 86.7%** |
| 원본 역할명 구별 텍스처를 가진 요소 9개 중 개별 렌더 인과 확인 | **6/9** |
| 원본 B6의 초기 9개 다음 실험 큐 중 실제 수행 | **5/9** |
| 원래 소스 요소의 배타적 GPU 픽셀/face 귀속 승인 | **0/45** |
| 부품 기능·재질·스타일 최종 의미 승인 | **0/45** |
| INT-6 원본 제삼자 모델·텍스처 학습/재배포 권리 승인 | **0** |

누적 성공은 **B5 AF123 좌판 #4(남751/북0), B7 AF121 좌판 #4(남1182/북2132), B8 HC11210 검은 쿠션 #12(남572/북1794), B9 AF121 등받이 #7(남776/북646), B10 AF121 등받이 #8(남392/북362), B11 AF121 등받이 #9(남366/북362)**로 각자의 원본 소스/런타임/화면 증거가 독립적으로 보존된다.

기존 엄격 기준 **H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70** 불변. 다음 후보는 B6 원본 큐의 **6순위 AF123/AF1394/source index7(원본 등받이 2면)**. 현재 AF123에 대해 원본 7번 요소 단독 실제 Fabric F2 제거 인과는 검증하지 않았다. Draft PR 미병합, `main` 불변.
