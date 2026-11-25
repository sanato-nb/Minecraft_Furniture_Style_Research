# INT-5-B9 — AF121 등받이 7번 원본 평면 요소, 독립 실제 Minecraft F2 인과 검증

검증일 **2026-11-25 KST**. 직계 [INT-5-B8 Draft PR #120](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/120) 기준 HEAD `d97281f43a60a6fd29715dd160969ceb3ac6d635`에서 새 [B9 Draft PR #121](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/121)로 분기. B1~B8 원본 소스·기존 감사 및 `main`은 변경·병합하지 않았다.

## 1. 정확히 어느 요소를 시험했는가

기존 B6 원본 45행 고정 원장, B3 텍스처-역할 단서, B6 실험 큐 **3순위**를 대조하여 `AF121 / AF1393 / source element index 7` 선정. `BACKREST_ASSEMBLY`는 오직 **소스 형상·텍스처 단서 기반 역할 가설**이며, 원본 2면 모두 `back_1/acacia.png`를 사용한다. 소스 parent 요소 index7 원본 기하:
- `from=[4,7,13]`, `to=[12,16,13]` — **z=13에서 두께가 0인 양면 판**, face는 `north`, `south` 딱 2개.
- 원래 모델 전체는 `another_furniture:block/template/chair` **10요소·46면**이며 `acacia_1`에 상속된다.
- 단일 요소를 제거한 자식 오버라이드 모델은 **9요소·44면**; 다른 9개 요소는 원본 배열의 해당 원소 JSON과 정확 일치.
- **'등받이의 실제 구조적 기능'·실착석 기능이나 원본 각 UV 페이스의 GPU 픽셀 범위**를 검증한 것이 아니다.

## 2. 고정 출처와 정확한 단일 수정 범위

공식 Another Furniture Fabric **4.0.2** 출시 JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785` 확인. 공식 **실행판** 자식 `acacia_1.json` Git blob SHA-1 `2261460299d13a15220f4fecfe059628ac28e813`, 독립 비교 자식 `acacia_3.json` `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`, 공유 부모 `template/chair.json` `31c643617a7178ac5113702e785620f4d1150adf` 확인. 연구판 Git **4.0.3**과 배포판 Fabric **4.0.2**의 원본 JSON byte 동등성을 추정하지 않음.

일회성 게임 실행용 공식 JAR 내부 **`assets/another_furniture/models/block/chair/acacia_1.json` 한 멤버만** 원본 10요소 중 index7을 제외하도록 수정했다. 원본 공유 `template/chair`·다른 `acacia_3` 자식·전체 텍스처·그 외 JAR 멤버는 압축 해제된 바이트가 원본과 같다. ZIP CRC, 동일 리소스 목록, 단일 변경 소스 해시를 확인했다. 임시 JAR SHA-1 `ea477da7b86e64c5490c41e9b849d557f2c95323`. **이 임시 모드 JAR/원본 모델 JSON/원본 텍스처는 연구 Git이나 배포 파일로 포함하지 않는다.**

## 3. 실제 게임 화면 두 세션 및 직접 시각 재검수

[**B9 실제 Minecraft Actions #45552711727 — SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45552711727) (검증 코드 커밋 `f2e8af328e194d759c399238b15b7414a3708e16`).

- **원본 Minecraft H15 실제 F2 8장** 기존 아티팩트 #14851461698 전체 ZIP SHA-256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462` 재확인, 개별 8개 PNG·client.log 및 원본 서버 정확 상태 마커 확인.
- **새 Minecraft Java 1.21.1 Fabric 4.0.2 임시 단일 변경 게임 세션 1회**, 실제 네이티브 F2 **8장**, 신규 서버 정확 source state **8/8건** 확인. 이전 H15와 같은 원본 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`, 좌표 `(-88,120,40)`; 두 대향 카메라 south/north 각각 `variant1 → 원본 미변경 variant3 → variant1 복원 → AIR`의 4단계.
- 두 게임 세션의 **16장 원본 PNG SHA**·2개 client.log SHA와 각 네이티브 F2 1024×684 포맷 재개봉. [**새 F2/로그/메타데이터 아티팩트 #14994563087**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45552711727/artifacts/14994563087) (45일 보존).
- **직접 PNG 시각 비교:** 남쪽 원본에서 보이던 의자 등받이 중앙부의 짧은 가로 띠 무늬가 index7 제거 후 사라짐. 북쪽도 원본 가로 띠 일부가 사라짐. 변경 위치는 소스의 z=13 평면과 양방향 렌더 시험에 정합적이다. 픽셀 자체의 독점 원본 페이스 소유 또는 재질·기능 검증은 아님.

## 4. 직접 감사된 실제 화면 픽셀과 음성대조

H15와 동일 RGB `ROI=[350,275,675,620]`, 채널 최대 차이 임계값 **24**를 적용했다.

| 실제 원본 H15 ↔ B9 단일 제거 F2 | 남쪽 시점 | 북쪽 시점 |
|---|---:|---:|
| **원본 variant1 vs element7 제거 variant1** | **776px** | **646px** |
| **variant1 반복 A 복원 후 같은 변화** | **776px** | **646px** |
| 원본·수정 *미변경* variant3 비교 | **0px** | **0px** |
| 원본·수정 AIR 비교 | **0px** | **0px** |
| 원본 variant1 A/A 반복의 시간 차 | **0px** | **0px** |
| 수정 variant1 A/A 반복의 시간 차 | **0px** | **0px** |
| 원래 variant1 의자 전경 *밖* 변경 픽셀 | **0px** | **0px** |
| 원래 variant1 의자 전경 vs AIR | 3,552px | 4,216px |

따라서 검증된 결정은 **`PASS_AF121_ISOLATED_CHILD_ELEMENT7_REMOVAL_NATIVE_F2_RESPONSE`**. 이는 **정확히 해당 원본 소스 element7을 제거하면 두 게임 화면에서 국소적인 렌더 변화가 재현된다**는 제한적 실험 결과다. 변경 픽셀에는 가림 뒤 드러난 픽셀·셰이딩 변화 등이 포함될 수 있으므로 원본 두 face가 변경 776/646개를 실제 소유했다고 주장해서는 안 된다.

## 5. 이전 단계와 구별한 누적 진행도

| 항목 | 검증 기준 | 누적 |
|---|---|---:|
| 원본 소스 부품·면 출처 연결 | B3/B6의 45요소, 229 face | **45/45 · 229/229** |
| 소스 역할 가설 그룹 | 15그룹 | **15/15** |
| **서로 다른 소스 요소 제거 → 실제 Minecraft 렌더 변화** | B5 AF123 element4, B7 AF121 element4, B8 HC11210 element12, **B9 AF121 element7** | **4/45** |
| 나머지 요소 실제 단독 개입 미실험 | 45−4 | **41/45** |
| 역할명 구별 텍스처가 있는 원본 요소 중 실제 단독 개입 | B3 9개 후보 | **4/9** |
| 개별 원본 요소의 배타적 GPU pixel/face 귀속 | 현재 근거 불충분 | **0/45 승인** |
| 부품 기능·재질·스타일의 최종 의미 승인 | 현재 근거 불충분 | **0/45 승인** |
| INT-6 AI 학습·제삼자 자산 재배포 권리 | 현재 근거 불충분 | **0 승인** |

별개 실험의 화면 반응:
- **B5 AF123** 접힌 variant10 좌판 index4: 남 751px / 북 0px.
- **B7 AF121** 기본 variant1 좌판 index4: 남 1,182px / 북 2,132px.
- **B8 HC11210** 기본 검은 쿠션 index12: 남 572px / 북 1,794px.
- **B9 AF121** 기본 variant1 등받이 판 index7: 남 **776px** / 북 **646px**.

각 실험은 소스 부품, 원본 블록 상태, 가림/카메라 조건이 달라 단순한 누적/모드 간 화면 픽셀 일반화가 불가하다.

기존 엄격 INT-4 **H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70** 불변. B9는 인과 확인된 **북향 variant1의 7번 요소 하나**에 국한된다. 다른 3방향 및 index8/9, 다른 의자 변형의 실제 단독 개입 시험은 아직 없다.

## 6. 실제 결과와 재현 파일

- `src/mcfr/int5_b9_af121_backrest_element7_native_f2.py`: 실제 공식 원본·자식 단일 수정·새 F2·H15 독립 감사
- `src/mcfr/runtime.py`: 기존 B7와 동일한 AF121 실제 원본 월드/카메라 명령 연결
- `tests/knowledge/test_int5_b9_af121_backrest_element7_native_f2.py`: **10개** 단일 요소·원본 SHA/역할/모델3·AIR·픽셀/허위 승인 회귀시험
- `.github/workflows/integration-int5-b9-af121-backrest-element7-native-f2.yml`: 실제 Actions #45552711727 성공
- `project/integration/INT5_B9_AF121_ELEMENT7_INDEPENDENT_CAUSAL_AUDIT_V1.json`: 기존/신규 원본 F2 16개·2개 로그 SHA와 실측 pixels
- **영구 GitHub 감사 JSON blob `5fcf5f34bb172c139fc1c7449074a0f3259b6e70` = 성공 Actions 아티팩트의 원본 감사 JSON Git blob 정확히 동일**.

**다음 실험 후보:** 동일 AF121 등의 index8(소스5면) 또는 index9(5면). 이번 B9에 포함되거나 승인되지 않았다. PR Draft 및 `main` 미병합 유지.
