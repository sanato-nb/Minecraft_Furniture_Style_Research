# INT-5-B12 — AF123 접힌 의자 등받이 원본 요소7(2면) 단독 제거·실게임 F2 인과 검증

**2026-11-25 KST**. 직계 [INT-5-B11 Draft PR #123](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/123) 최종 HEAD `bd9e389617497193d9cc5d907a83f078e930c056`에서 별도 브랜치를 분기해 실제 작업했다. **main과 B5~B11 이력은 변경·병합하지 않는다.**

## 1. 원본 출처 및 실험 기하

- B6 원본 45요소 원장 및 초기 실험 큐 **6순위**: `AF123 / AF1394 / original source element index7`, 소스 `BACKREST_ASSEMBLY` 역할 **가설**, 원본 **2면**, 두 면 모두 원본 역할명 `back_10/acacia.png` 참조(B3).
- 공식 Another Furniture Fabric **4.0.2** JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`, B5에서 독립 검증된 실제 출시판 원본 공유 부모 `assets/another_furniture/models/block/template/chair_tucked.json` Git blob `bbfd54f73fd764015ce320082ba531bd314a6dfd`를 고정.
- 원래 `another_furniture:block/chair/acacia_10_tucked` 자식이 공유 `template/chair_tucked`에서 **10요소·46면**을 상속한다. 이번 개입은 **공유 부모를 수정하지 않고** `assets/another_furniture/models/block/chair/acacia_10_tucked.json` **자식 JSON 1개**에 index7 제외한 원본 **9요소·44면**을 오버라이드. 실제 JAR 해시·개별 출처·ZIP CRC·수정된 원본 외 **모든 압축 해제된 JAR 멤버의 byte 불변**을 검증한다.
- 이 실험은 게임 자산 원본・임시 JAR・모드 PNG・원본 모델 JSON을 Git/증거 아티팩트에 올리지 않는다.

## 2. AF123의 필수 게임 상태 — B4/B5 독립 대조 재사용

AF123 원본은 **`another_furniture:acacia_chair[facing=north,tucked=true,variant=10]`**이다. 윗반블록 없이 tucked=true가 자연 유지되는 상태가 아니므로, `minecraft:oak_slab[type=top]`을 의자 앞쪽에 배치·보존하는 **정상 지원 상태**에서만 실험한다. 원본 AF123 의자와 슬랩 각각을 **게임 서버가 16/16건** 증명해야 하며, 슬랩 제거 시 의자 상태가 바뀔 가능성을 무시하지 않는다.

- 실제 원본 B4 공식 게임 [Actions #45528207751](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751)의 기존 8 F2 원본 ZIP artifact `14982648778`을 다시 불러와 전체 SHA256 **`4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35`**, ZIP CRC, 원본 PNG 8장 개별 SHA, 원본 서버 16개 pair 및 영구 B4 원본 감사 JSON과 완전 동일함을 검증한다.
- 다른 Minecraft Java **1.21.1 Fabric** 실세션에서 `AF123_north` 원본 블록/윗반블록을 보존한 뒤 원본 index7만 자식 모델에서 제외한 **새 네이티브 F2 8장**을 남·북에서 재촬영. 각 카메라는 `의자+윗반블록(A) → 윗반블록만(B) → A복원 → AIR` 네 단계이며, 서버 의자+슬랩 상태 16개 및 새 PNG/로그 SHA로 증명한다.
- H15 AF121 baseline 사용 금지: **AF123 지원 슬랩과 tucked=true/variant10 원본만** 비교한다. RGB ROI `[350,275,675,620]`, threshold24. 두 세션 윗반블록만/AIR 음성대조 0, 수정 세션 A/A temporal 0, 원본 의자 전경 바깥 화면 변화0을 만족하면서 원래 의자+슬랩 vs 제거 의자+슬랩 변화가 나타날 때에만 **범위 제한 인과 PASS**.

## 3. 실제 GitHub 구현

- `src/mcfr/int5_b12_af123_backrest_element7_native_f2.py`: 원본·이력 SHA, 단일 자식 모델 격리 개입, 원본 B4 앵커 대조, 실제 게임 픽셀 독립 감사
- `tests/knowledge/test_int5_b12_af123_backrest_element7_native_f2.py`: **13개** 소스/2면·정확 10/46→9/44·원본 슬랩 정상 상태·변형 독립·반증/권리 차단 회귀시험
- `src/mcfr/runtime.py`: 다른 AF121 프로그램/모델과 분리된 **AF123 원본 월드 및 윗반블록 지원** 전용 명령 `int5-b12-af123-backrest7-native-f2`
- `.github/workflows/integration-int5-b12-af123-backrest-element7-native-f2.yml`: 실제 공식 Minecraft F2 + SHA 및 원본 상태 재검증, 결과 보고서/증거 분리
- **영구 JSON과 실측 픽셀 승인 기록은 실게임·음성대조 결과 확인 후에만 기록**한다.

## 4. 착수 기준 및 승인 경계

원본 요소 45/45, 원본 면/UV 229/229, 소스 역할 가설 15/15. 서로 다른 요소의 실제 개별 수정 인과 **6/45 (13.3%)**, 미실험 **39/45 (86.7%)**. 현재 B12는 아직 완료 수치에 포함하지 않는다. 원본 개별 페이스의 GPU 픽셀 배타적 귀속 및 실제 부품 기능·재질·스타일 최종 승인 0/45; INT-6 학습/제삼자 자산 재배포 권리 승인 0; H03 HOLD / H05 CONDITIONAL / F70 무조건 0/70 유지. **AF123 인접 슬랩이 가릴 수 있으므로 실제 F2 응답이 0일 가능성도 허위 PASS로 바꾸지 않는다.**
