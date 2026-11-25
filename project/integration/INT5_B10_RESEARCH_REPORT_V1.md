# INT-5-B10 — AF121 기본 의자 등받이 요소8(원본 5면) 단일 소스 제거 실게임 F2 검증

기준일 **2026-11-25 KST**. [B9 Draft PR #121](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/121) 최종 HEAD `576f3d76690a014421384ab001485976922a2979`에서 B10 신규 브랜치 `work/int5-b10-af121-backrest-element8-native-f2-20261125`로 진행. 기존 B5~B9 원본 결론을 새 시험의 픽셀로 재분류하지 않는다. `main` 미병합.

## 1. 실제 원본 근거와 검증 목표

B3 45요소 원본 텍스처 역할 기록과 B6 고정 원장/9개 다음 실험 큐의 **4순위**는 `AF121 / AF1393 / source index8`, 원본 **5면**, `BACKREST_ASSEMBLY` **역할 가설**이며 원본 다섯 면 모두 역할 이름을 가진 원본 텍스처 `back_1/acacia.png`에 연결된다. 원본 텍스처 Git blob SHA `55f3bbf986c0c10b731cc0e67038402f30340972`(연구판 4.0.3 기준); 공식 게임 출시판 원본 JSON byte SHA와 동일하다고 추정하지 않는다.

원본 Another Furniture Fabric 4.0.2 JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785` 및 실행판 자식 `acacia_1` SHA1 Git blob `2261460299d13a15220f4fecfe059628ac28e813`, 미수정 negative control `acacia_3` SHA `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`, 공유 부모 `template/chair` blob `31c643617a7178ac5113702e785620f4d1150adf` 고정한다.

**실험 개입:** 부모 `template/chair` 원본 **10요소·46면**의 `source index8` **5면만** 제외하여 원본 자식 `assets/another_furniture/models/block/chair/acacia_1.json` 한 JAR 멤버에 원본 나머지 **9요소·41면**을 명시적 오버라이드. 원본 공유 부모·미수정 비교 `acacia_3`·모든 다른 JAR 리소스·원본 PNG 바이트 불변. 라이선스 자산은 Git/결과 아티팩트에 추가하거나 재배포하지 않는다.

## 2. 실제 Minecraft 검증 흐름

- 원본 H15 원본 Fabric Java 1.21.1 **8개의 실제 네이티브 F2**를 Actions artifact `14851461698`에서 가져와 전체 ZIP SHA-256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`, 원본 게임 로그·개별 PNG SHA 및 original server state 확인.
- 같은 소스 블록 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`과 좌표 `(-88,120,40)`에 별도 실제 Minecraft 1.21.1 Fabric 새 게임 클라이언트, 남·북 두 카메라 각각 **A variant1 → B variant3 원본미수정 → A복원 → AIR** 의 총 **8개 신규 F2**, 정확 서버 상태 8개와 PNG·게임 로그 SHA 확인.
- RGB `ROI=[350,275,675,620]`, 임계값24. 제거 전/후 A 화면 변화가 재현되는지 확인; **미수정 B variant3, AIR, 원본 A/A 반복, 수정 A/A 반복, 원본 의자 전경 밖 변화 모두 0** 이어야만 범위가 제한된 인과 PASS.
- **기능/스타일/재질, 원래 GPU face→pixel 배타적 귀속, INT6 AI 학습 및 제삼자 자산 재배포 권리 승인 0** 유지. 실제 실험 PASS 전까지 누적 4/45 인과, 남은 41/45 미실험으로 유지.

## 3. GitHub 실제 작업

- `src/mcfr/int5_b10_af121_backrest_element8_native_f2.py`: B9의 독립 검증 코드 기반으로 정확 원본8/5면·자식 한 개 수정 9/41 및 신·구 네이티브 F2 16개 대조
- `src/mcfr/runtime.py`: B10 전용 `int5-b10-af121-backrest8-native-f2` 명령과 기존 AF121 월드/카메라, 기존 B5~B9 동작 보존
- `tests/knowledge/test_int5_b10_af121_backrest_element8_native_f2.py`: 소스 원본·단일 수정·기존 대조·반증·권리 차단 **10개 회귀시험**
- `.github/workflows/integration-int5-b10-af121-backrest-element8-native-f2.yml`: 원본 H15 SHA 및 게임 실측 검증
- [B10 전용 실제 게임 Actions #45554039558](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45554039558) — **원본 F2 검수·실게임 촬영·엄격 독립 감사 진행** (결과 전 사전 성공 주장 금지).
- 최종 `project/integration/INT5_B10_AF121_ELEMENT8_INDEPENDENT_CAUSAL_AUDIT_V1.json`은 **실제 Minecraft Actions 성공 및 결과 로그 확인 후에만** 영구 기록.

## 4. 현재 INT-5 전체 진행과 엄격한 한계

| 연구 항목 | 현재 검증된 상태 |
|---|---:|
| 원본 소스 요소·UV 연결 | **45/45 요소 · 229/229면** |
| 원본 역할 가설 그룹 | **15/15** |
| 원본 단일 요소 제거 → **실제 게임 렌더 인과 성공** | **4/45 (8.9%)** |
| 아직 개별 인과 미실험 | **41/45 (91.1%)** |
| 원본 개별 요소의 배타적 GPU 픽셀 귀속 승인 | **0/45** |
| 부품 기능·재질·스타일 최종 승인 | **0/45** |
| INT6 제삼자 자산 학습·재배포 권리 승인 | **0** |

기존 B5 AF123 좌판4 / B7 AF121 좌판4 / B8 HC11210 검은 쿠션12 / B9 AF121 등받이7 인과 각각 독립 유지. **엄격 INT4 H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70** 변경 금지. B10은 **AF121 북향 변형1의 8번 요소 하나**에만 적용; 다른 방향·다른 모델·같은 등받이 다른 요소 7/9로 결과 전이 금지.
