# INT-5-B9 — AF121 원본 등받이 element 7(2면) 단독 제거 → 실제 Fabric F2 인과 재검수

기준일 **2026-11-25 KST**, [B8 Draft PR #120](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/120) head `d97281f43a60a6fd29715dd160969ceb3ac6d635`에서 새 누적 브랜치를 분기했다. 본 실험은 새 소스 요소 인과 시험이며 H03/H05 및 INT-6 권리 승인과 분리된다.

## 원본 근거

B6 출처 고정 45행 원장과 실험 큐에서 **3순위 AF121/AF1393/source element index 7** 확인. 원본 provider `another_furniture:block/template/chair`, 원본 element index7 **2개 face**, 역할명 가설 `BACKREST_ASSEMBLY`, 실제 소스 `back_1/acacia.png`의 **역할명 텍스처 단서 2/2면**. 기능·재질·스타일과 특정 원본 F2 픽셀 귀속은 아직 검증되지 않았다.

기존 원본 B7에서 검증한 공식 Another Furniture Fabric **4.0.2** JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`와 출시판 자식 `acacia_1.json` 원본 Git blob `2261460299d13a15220f4fecfe059628ac28e813`, 비교 자식 `acacia_3.json` blob `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`, 공유 부모 `template/chair.json` blob `31c643617a7178ac5113702e785620f4d1150adf`를 다시 검증한다. **연구 Git 4.0.3과 실행 Fabric 4.0.2 소스는 바이트 동일하다고 가정하지 않는다.**

## 실험 목표 및 성공 조건

1. 공식 JAR을 임시 실행 폴더에서만 열어 **`acacia_1.json` 자식 파일 딱 하나**에 부모 원본 10요소·46면 중 **element index7(2면)만 제외한 9요소·44면**을 명시적으로 배치한다. 공유 부모·변형3 `acacia_3` 자식·원본 텍스처·모든 다른 JAR 멤버는 **압축 해제 후 바이트 불변**이어야 한다.
2. 기존 실제 원본 H15 Fabric 1.21.1 **남/북 양방향 네이티브 F2 8장** [artifact #14851461698](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/workflows/integration-int4-h15-af-opposing-real-f2.yml) ZIP SHA-256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`를 완전 검증하고 원본 PNG와 로그·원본 서버 상태를 다시 연다.
3. 별도 새 Minecraft Java **1.21.1 Fabric** 월드에서 자식 단일 요소7 제거 모델로 **새 F2 8장**을 찍는다. 원본과 동일한 블록 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`·좌표 `(-88,120,40)`, 남/북 각 `variant1 A → unmodified variant3 → A복원 → AIR` 4단계, 서버 상태 8/8 및 PNG SHA 전체 확인.
4. 원본 H15 F2와 제거 F2의 RGB `ROI=(350,275,675,620)`, 채널 변화 임계값 **24**를 비교한다. 원본/수정 각각 A→A복원 시간 변화 **0**, 미수정 variant3 **0**, AIR **0**, 원본 의자 전경 바깥 변화 **0**을 요구하며, 적어도 한 관찰 시점에서 동일 소스 요소 제거에 대한 재현 가능한 비영(非零) 응답이 나오면 **범위 한정 렌더 인과 PASS**로 인정한다. 그 외 실패/CONDITIONAL이며 기존 **3/45** 인과 수치를 증가시키지 않는다.

## 실행·실제 결과

- `src/mcfr/int5_b9_af121_backrest_element7_native_f2.py`: 원본 SHA·격리 단일 제거·실게임 F2·두 세션 대조
- `tests/knowledge/test_int5_b9_af121_backrest_element7_native_f2.py`: 10개 원본 10/46, 제거 9/44, 동일 서버 카메라/원본 F2·음성대조/false approvals 부정 회귀시험
- `src/mcfr/runtime.py`: B9에 정확한 기존 AF121 원본 world case 연결, HC/B8 분기 유지
- `.github/workflows/integration-int5-b9-af121-backrest-element7-native-f2.yml`: 실제 Minecraft F2 8장·원본 H15 8장 SHA/원본 모델 자산 검증·미수정 모델3/AIR 대조
- Actions: [B9 실게임 CI #45552711727](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45552711727)
- 영구 감사 JSON: **실게임 검증과 음성대조 성공을 재확인한 후에만 생성·커밋한다.** 현재 아직 새 성공 픽셀 수치를 부여하지 않는다.

## 원본·권리 보존

기존 B5 AF123 element4 남751/북0, B7 AF121 element4 남1182/북2132, B8 HC11210 element12 남572/북1794는 각 독립 출처/실험으로 보존한다. 신규 B9 실측 결과를 임의로 복제하지 않는다. 원본 요소 45/45, UV 229/229, 기존 렌더 개입 성공 **3/45**, 미개입 **42/45**. 원본 원소별 GPU 픽셀 독점, 실제 등받이 기능, 재질·스타일 최종 승인 **0/45**, INT-6 AI 학습·재배포 권리 승인 **0**, 기존 엄격 INT4 H03 HOLD/H05 CONDITIONAL/F70 무조건 0/70 유지.

원본 출시 JAR/모델/텍스처/임시 수정 JAR은 Git 또는 CI 아티팩트에 넣지 않고, **원본/새 실게임 F2 PNG 및 게임 로그·SHA**만 기간제 CI 아티팩트에 보존한다. PR Draft·미병합, `main` 불변.
