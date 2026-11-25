# INT-5-B10 — Another Furniture AF121 원본 등받이 8번 요소, 실게임 F2 독립 인과 검증

**검증일 2026-11-25 KST.** 원본 [INT-5-B9 Draft PR #121](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/121) 마지막 커밋 `576f3d76690a014421384ab001485976922a2979`에서 [INT-5-B10 Draft PR #122](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/122)로 분기. 기존 B1~B9 원본 감사·결과, `main`, 원본 제삼자 자산에 변경 없음.

## 1. 고정 원본과 독립 실험 범위

B3의 45요소 텍스처 원본 기록과 B6 원본 45행 원장/실험 큐 **4순위**: `AF121 / AF1393 / source element index 8`. 역할 `BACKREST_ASSEMBLY`는 **원본 소스 기반 가설**이며 기능 승인 아님.

- 원본 실제 형상 **from=[12,7,12], to=[14,16,14]**, 5개 면 정확히 `east`, `north`, `south`, `up`, `west`; B3 출처상 다섯 면 모두 원본 `back_1/acacia.png` 역할 이름 텍스처를 사용한다.
- 공식 Another Furniture **Fabric 4.0.2** JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`. 원본 공식 실행판 모델의 실제 Git blob: `acacia_1` 자식 `2261460299d13a15220f4fecfe059628ac28e813`, 비교 `acacia_3` 자식 `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`, 원본 `template/chair` 부모 `31c643617a7178ac5113702e785620f4d1150adf`. 연구본 4.0.3 JSON은 실행판 4.0.2와 바이트 동일하다고 가정하지 않는다.
- 실제 변경은 공식 JAR의 **`assets/another_furniture/models/block/chair/acacia_1.json` 한 ZIP 리소스 멤버**만. 공유 원본 부모의 **10요소·46면**에서 원래 index8 **5면**만 제외하고, 같은 자식에 남은 원본 **9요소·41면**을 명시 오버라이드. 원본 공유 `template/chair`, `acacia_3` 비교 자식 및 다른 모든 JAR 멤버는 uncompressed byte 동일, CRC·리소스 목록·개별 모델 Git SHA로 대조.
- 임시 수정 JAR SHA1 `9370a7f90b612a844d77d8e308e26d9be232e741`. 원본·변형 JAR/모델 JSON/제삼자 원본 텍스처는 Git에 커밋하지 않았으며 Actions 아티팩트에 포함하지 않았다.

## 2. 원본 Minecraft와 실게임 F2 재현 근거

[**B10 최종 GitHub Actions #45554490160 — 전체 SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45554490160), 검증 코드·회귀시험·CI 강화 커밋 **`f96eab9cf7c67964f5fb51344458fa4070bb8825`**.

- 별개 원본 클라이언트 게임 세션의 **H15 기존 실제 Minecraft 네이티브 F2 8장**, 전체 ZIP SHA256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462` 재검증 후 ZIP CRC, 원본 PNG 8개 SHA256·원본 client.log SHA 및 정확 서버 source state 전체 재개봉.
- B10은 Minecraft Java **1.21.1 Fabric** 공식 모드 JAR을 새 게임 세계에서 임시 자식 한 모델만 수정하여, **남쪽/북쪽 카메라 각각 4장, 신규 8장의 실제 네이티브 F2** 촬영. 단계 `variant1 A → untouched variant3 → A복원 → AIR`; 블록 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`, 좌표 `(-88,120,40)`, 두 카메라 기존 H15와 정확 일치. 원본/수정 합계 **실제 F2 16장**, 새로운 서버 상태 **8/8** 및 개별 PNG SHA 검증.
- 재현 RGB ROI `[350,275,675,620]`, 최대 채널 차이 임계값 **24**. 두 카메라의 source index8 제거 응답은 다음과 같다.

| 원본 H15 vs B10 요소8 제거 수정 화면 | 남쪽 | 북쪽 |
|---|---:|---:|
| **원본 variant1 → index8 제거 화면 변경** | **392px** | **362px** |
| **A복원 뒤 동일 변화 재현** | **392px** | **362px** |
| 미수정 변형3 variant3 원본↔수정 | **0px** | **0px** |
| AIR 원본↔수정 | **0px** | **0px** |
| 원본 variant1 A/A 시간 drift | **0px** | **0px** |
| 수정 variant1 A/A 시간 drift | **0px** | **0px** |
| 원본 의자 전경 밖 변경 픽셀 | **0px** | **0px** |
| 원본 의자 전경 vs AIR | 3,552px | 4,216px |

- 직접 두 아티팩트 원본 PNG를 다시 열어 이미지로 검수. **등받이 좌/우 세로 조립체 중 한쪽 세로부가 index8 제거 후 사라짐**; 남·북 관찰에서 독립적으로 확인된다. 응답 변화 픽셀에 숨겨졌던 원본 뒤쪽 재노출이나 셰이딩이 포함될 수 있으므로 원래 5개 source face가 해당 픽셀을 *독점적으로* 차지했었다는 결론이 아님.

## 3. 실제 잘못된 감사 키 발견·수정 및 실패-허위승인 차단

최초 실게임 [Actions #45554039558](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45554039558)에서도 원본 5면, index8 제거 및 남392/북362, 대조0으로 실제 화면 인과는 나타났으나, **출력 감사 JSON `original_source_part_key` 필드가 이전 B9의 `AF121/AF1393/7`**로 남은 메타데이터 오류를 독립 검수 과정에서 발견했다. 이 JSON을 영구 승인·커밋하지 않았다.

이를 **`SOURCE_KEY`와 `SOURCE_INDEX`에서 원본 키를 직접 조립하도록 변경**하고, 이탈을 방지하는 추가 회귀시험과 CI 필수 assert `source key==AF121/AF1393/8`, `removed index==8`, 정확한 원본 **10요소·46면**, 수정 **9요소·41면**, 삭제 원본 **5면**을 명시했다. 수정된 최종 별도 Actions **#45554490160 SUCCESS**에서 첫 화면 실측·음성대조 결과가 정확히 재현되고 메타데이터 문제도 사라진 것을 확인했다.

**최종 판정:** `PASS_AF121_ISOLATED_CHILD_ELEMENT8_REMOVAL_NATIVE_F2_RESPONSE`, 이는 **출처가 검증된 원본 모델 소스 element8 제거의 국소적 게임 화면 변화**에 한정된다. 개별 GPU 픽셀/face 소유권, 부품 구조 기능·재질·스타일, 실제 앉기 메커니즘, INT-6 학습/재배포 라이선스를 승인하지 않는다.

## 4. 영구 보존 증거

- [**실제 B10 수정 게임 F2 8장 + client.log + 출처 감사 아티팩트 #14995401421**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45554490160/artifacts/14995401421) (45일 후 만료). 원본 비교 F2 8장은 H15 이전 결과.
- `project/integration/INT5_B10_AF121_ELEMENT8_INDEPENDENT_CAUSAL_AUDIT_V1.json`에 실제 CI 실행 로그에서 확인된 원본·수정 PNG 16개 SHA, source 모델 SHA, 원본 ZIP SHA, 서버 8 marker, 원본/수정 좌표·픽셀 음성대조 영구 기록.
- GitHub 감사 JSON Git blob SHA-1 **`6fa2ccbb83043f41c52520417778c169fc054380`**는 성공한 Actions의 실제 감사 JSON Git blob과 **바이트 단위 일치**하는 것을 별도 다운로드/CRC 직접 검증했다.
- `src/mcfr/int5_b10_af121_backrest_element8_native_f2.py`, `src/mcfr/runtime.py`, `tests/knowledge/test_int5_b10_af121_backrest_element8_native_f2.py` (**11개 회귀시험**) 및 `.github/workflows/integration-int5-b10-af121-backrest-element8-native-f2.yml`은 이 결과를 재현하는 방법만 저장한다.

## 5. INT-5 누적 진행률 (B10 실제 재검증 성공 이후)

| 검증 작업 | 현재 확정된 진행 |
|---|---:|
| 원본 의자 부품 소스·UV 전체 | **45/45요소 · 229/229 원본 면** |
| 연구상 역할 가설 그룹 원본 연결 | **15/15** |
| **서로 다른 요소의 실제 Minecraft 단일 제거 → 한정 렌더 인과 확인** | **5/45 = 11.1%** |
| 개별 단독 렌더 시험 미수행 | **40/45 = 88.9%** |
| B6 큐의 초기 미실험 9건 중 실행 완료 | **4/9** (AF121 #4, HC11210 #12, AF121 #7, AF121 #8) |
| 요소별 원본 GPU face/pixel 배타적 귀속 승인 | **0/45** |
| 실제 부품 기능·재질·스타일 최종 승인 | **0/45** |
| INT-6 제삼자 모델/텍스처 학습·배포 권리 승인 | **0** |

원본 B5 AF123 좌판4(남751/북0), B7 AF121 좌판4(남1182/북2132), B8 HC11210 검은 쿠션12(남572/북1794), B9 AF121 등받이7(남776/북646), **B10 AF121 등받이8(남392/북362)** 총 **서로 다른 5개 원본 소스 요소**가 별개의 게임 개입 근거로 검증됐다. 결과를 게임 모델 일반 능력 또는 전체 45개 부품 기능 승인으로 전환하지 않는다.

기존 INT-4 엄격 **H03 HOLD**, **H05 CONDITIONAL**, **F70 무조건 승인 0/70** 유지. 다음으로 B6 큐의 **5순위 AF121/AF1393 원본 등받이 index9(5면)**는 아직 단독 시험하지 않았다. 기존 연구·지식 정확성을 우선하며 B10 PR #122는 계속 Draft·미병합, `main` 불변.
