# INT-5-B11 — AF121 등받이 원본 요소9(5면) 단일 제거 실제 Minecraft F2 인과 연구

기준일 **2026-11-25 KST**. [B10 Draft PR #122](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/122)의 확정 최종 HEAD `e839ac43abcdf6dce6607f512bbd0d4e7c7adc3e`에서 새 독립 B11 브랜치로 분기했다. 기존 B1~B10 코드/원본 감사/증거 및 `main` 미변경.

## 1. 실제 원본 소스와 한정 실험

B3의 45개 원본 요소/역할명 텍스처 원장과 B6 원본 실험 큐 **5순위**의 `AF121/AF1393/original source element index 9`. 원본 **5면**, `BACKREST_ASSEMBLY`는 아직 역할 가설. 다섯 원본 면 전부 `back_1/acacia.png` 역할명 텍스처 단서가 기록되어 있다. 그 이름은 실제 등받이 기능, 재질·스타일, 원본 GPU 개별 픽셀을 입증하지 않는다.

엄격 원본 공식 **Another Furniture Fabric 4.0.2** JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`; 원본 실행판 자식 acacia1 Git blob `2261460299d13a15220f4fecfe059628ac28e813`, 미수정 acacia3 비교 자식 `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`, 공유 부모 template/chair `31c643617a7178ac5113702e785620f4d1150adf`를 독립 확인한다. 연구 Git 4.0.3과 출시 Fabric 4.0.2가 byte-identical이라고 가정하지 않는다.

실험 개입은 공식 임시 게임 JAR 내부 `assets/another_furniture/models/block/chair/acacia_1.json` **단 한 멤버만** 바꾸어 공유 부모의 원본 **10요소·46면** 중 index9의 **5면만 제거**, 보존 원본 배열의 **9요소·41면**을 명시적으로 오버라이드. 원본 공유 부모와 `acacia_3` 비교 모델, 전체 기타 모드 자산 및 텍스처의 압축 해제 바이트는 동일해야 한다. 원본/임시 JAR/제삼자 PNG/모델은 Git/아티팩트에 포함하지 않는다.

## 2. 실제 Minecraft 원본/수정 화면 엄격 대조

- Minecraft Java **1.21.1 Fabric**, Another Furniture Fabric 4.0.2.
- 기존 공식 H15 원본 게임 네이티브 F2 **8장** 원본 ZIP SHA-256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462` 및 8개 PNG·client.log SHA·원본 블록 상태 재검증.
- 별도 실제 Minecraft 새 게임 세계에서 **남·북 두 시점**, 동일 원본 블록 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`, 좌표 `(-88,120,40)`, 각 `variant1 A → untouched variant3 → A 복원 → AIR` 네 단계 신규 F2 **8장**, 정확 서버 상태 8/8과 PNG SHA.
- 픽셀 변화 RGB `ROI=[350,275,675,620]`, max-channel threshold 24. 미수정 variant3 / AIR / 원본·수정 A/A 시간 drift / 원본 의자 전경 밖 변화는 모두 **0**이어야 한다. 원본 vs index9 제거 수정 variant1 화면 변화는 시간 복원 뒤에도 동일해야 범위 한정 인과 PASS.
- 감사 JSON의 소스 ID는 **`SOURCE_KEY`와 실제 `SOURCE_INDEX=9`에서 계산**, 9번 요소·기존 7/8 오기 방지 회귀 포함.

## 3. 실제 GitHub 변경

- `src/mcfr/int5_b11_af121_backrest_element9_native_f2.py`: 4.0.2 원본 자식 SHA / 단일 요소9 제거 / 실제 새 게임 F2 / H15 원본 8장 재개봉과 대조
- `src/mcfr/runtime.py`: 기존 실험 모두 보존하면서 `int5-b11-af121-backrest9-native-f2` 정확 명령 추가
- `tests/knowledge/test_int5_b11_af121_backrest_element9_native_f2.py`: 11개 원본·단일 변경·음성대조·소스 키/권리 차단 시험
- `.github/workflows/integration-int5-b11-af121-backrest-element9-native-f2.yml`: 실제 1.21.1 Fabric Minecraft CI
- [B11 실제 게임 Actions #45555779012](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45555779012)에서 실험 결과 검증. 성공 후에만 영구 JSON과 픽셀 실측치를 결과로 인정한다.

## 4. 착수 시 전체 INT-5 경계

- 기존 원본 소스 요소/면 연결 **45/45요소, 229/229면**, 역할 가설 15/15.
- 원본 서로 다른 요소의 실제 게임 개입 인과 PASS **5/45 (11.1%)**, **40/45 미실험** (B5 AF123 index4, B7 AF121 index4, B8 HC11210 index12, B9 AF121 index7, B10 AF121 index8).
- 개별 GPU 픽셀/face 배타적 귀속, 부품 기능·재질·스타일 승인 **0/45**, INT-6 학습/재배포 권리 승인 **0**.
- 기존 엄격 H03 HOLD, H05 CONDITIONAL, F70 무조건 승인 0/70 유지. B11을 미리 6/45로 계산하지 않음.

## 5. 실제 측정 결과

실제 원본 F2/신규 F2 화면·로그·SHA 및 음성대조 재검수 **완료 시 최종 실험 수치·정확 원본 인과 판단으로 교체**. 본 초안은 성공 수치나 아직 존재하지 않는 아티팩트/영구 감사 JSON을 주장하지 않는다.
