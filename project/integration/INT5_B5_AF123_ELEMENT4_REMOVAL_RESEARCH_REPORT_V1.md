# INT-5-B5 — AF123 의자 element 4 단일 제거·실제 F2 인과 대조

기준: 2026-11-25 (KST). 직계 INT-5-B4 [Draft PR #116](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/116), head `d055d1dcacab751330cfe49d8b33224759484d76`. `main` 직접 변경 없음.

## 1. 이번 단계가 해결하려는 문제

INT-5-B3에서 AF123 원본 소스의 **provider AF1394, element index 4, 역할 가설 SEAT_LAYER, 6면**이 확인되었고, B4는 실제 게임에서 상단 반블록이 의자 일부를 가리는 현상과 의자 전체의 노출 영역을 분리하였다. **하지만 개별 element 4의 화면 인과는 0건**이다.

B5는 원본 전체 가구 화면만으로 요소의 정체를 확정하지 않고, 실제 공식 Fabric Another Furniture 4.0.2 JAR의 모델 상속 체인을 따라가 해당 요소를 찾은 다음 **일회성 시험 JAR에서 오직 한 원본 모델 JSON 멤버의 element 4만 제거**한다. 나머지 9개 원본 요소, 블록상태, 지지용 슬랩, 실행 버전, 2대향 카메라, 게임 맵은 그대로 유지한다. 실제 원본 JAR SHA-1을 패치 전에 검증하고, 전체 ZIP 멤버와 CRC, 바뀐 JSON 멤버 1개의 근거를 남긴다.

개별 요소를 제거하면 다른 물체 뒤가 드러나거나 음영·AO가 달라질 수 있다. 따라서 제거 전후 변경된 모든 픽셀을 '원래 element 4 자체에 속한 픽셀'로 무조건 확정하지 않는다.

## 2. 실제 비교·부정대조

- **원본 무변조 기준:** B4 [Actions #45528207751](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751)의 실제 F2 원본 8장과 서버 상태 16개, 영구 JSON 동일 SHA. 원본 사진은 재촬영하지 않고 고정된 Actions 아티팩트에서 다운로드한다.
- **새 임시 수정 실험:** 동일 `AF123_north` 블록 `another_furniture:acacia_chair[facing=north,tucked=true,variant=10]`과 동일 지지용 top slab, 남/북 각 `A(의자+슬랩) → B(슬랩만) → A(의자 복원) → AIR` **8장**.
- **실제 게임 모델 확인:** 원본 출시 JAR → 자식 `acacia_10_tucked` → 실제 부모 상속 체인 → 10요소·46면 → index 4의 6면, 임시 수정 9요소·40면 확인.
- **대조:** 원본 A vs 임시 수정 A의 픽셀 변화, A 복원의 반복성, 원본 B(슬랩만) vs 수정 B 및 AIR vs AIR의 **음성대조**, 원래 의자 전경 바깥 변화 검사.
- **최종 판정:** 변경 화면이 한 방향 이상에서 실제 확인되고 양측의 무변경/재촬영 부정대조가 일치한 경우에 한해 '4번 소스 요소 제거가 실제 렌더 결과에 영향을 준다'는 **한정 인과 증거**로 승인한다. 그렇지 않으면 CONDITIONAL.

## 3. 정확한 결과물과 실행 상태

- `src/mcfr/int5_af_element4_removal_f2.py`: 공식 원본 SHA 검사, 단일 요소 임시 제거, 네이티브 F2 재사용 촬영, 두 원본의 독립 감사 및 화면 차이.
- `src/mcfr/runtime.py`: `int5-b5-af-element4-removal` 격리 명령 연결.
- `tests/knowledge/test_int5_af_element4_removal_f2.py`: 원본 요소 번호, 부모 모델, 부정대조·보류 보호 등 9개 회귀시험. 테스트 내 합성 이미지는 실제 게임 F2라고 주장하지 않는다.
- `.github/workflows/integration-int5-b5-af-element4-removal-native-f2.yml`: 원본 B4 다운로드/독립 감사 → 최신 원본 게임 준비 → 수정 실험 F2 → 독립 비교. 원본 PNG/수정 JAR는 일반 Git 커밋에 포함하지 않는다.
- 결과 감사: `INT5_B5_AF123_ELEMENT4_NATIVE_F2_CAUSAL_AUDIT_V1.json` (실제 게임 CI 산출물; 통과 후 소스에 메타데이터만 별도로 저장 가능).

**현재 CI 판정:** 전용 실제 GitHub Actions 실행 결과 확인 전, `PENDING_REAL_NATIVE_F2_COMPARISON`. 소스 작성과 브랜치 생성 자체를 게임 실험 성공으로 계산하지 않는다.

## 4. 승인 경계

B4의 지원 슬랩 `tucked=true` 필수 전제를 유지한다. 4.0.3 연구 Git 소스와 공식 Fabric 4.0.2 런타임 JSON이 동일하다고 가정하지 않는다. 화면 인과 증거가 통과하더라도 **착석 기능/부품 이름·재질·스타일 최종 의미 승인 0/45, 개별 원본 element 픽셀 소유 확정 0, INT-6 제삼자 AI 학습·재배포 권리 승인 0**을 유지한다. INT-4 기존 엄격 H03 HOLD, H05 CONDITIONAL 및 0/70 무조건 승인도 변경하지 않는다. 수정 JAR와 제삼자 원본 이미지/모드 자료를 GitHub 소스에 추가하지 않는다.

## 5. 다음 단계

실제 CI 로그와 원본 아티팩트를 확인한 뒤 결과가 명확하면 **화면 변화 영역을 그룹별 외형 후보와 교차 기록**한다. 조건 미충족 시 원인 및 해당 제약을 보고하고, 새로운 승인 수치를 임의로 올리지 않는다.
