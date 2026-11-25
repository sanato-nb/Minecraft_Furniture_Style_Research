# INT-5-B13 — AF123 등받이 원본 8번 요소(5면) 실제 Minecraft 1.21.1 Fabric 단일 제거 인과 검증

**실제 검증일 2026-11-25 KST.** [B12 Draft PR #124](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/124) 최종 HEAD `7165a3d6934276947ec0154b886477466e9b6f94`에서 [B13 Draft PR #125](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/125)로 신규 분기. 기존 B1~B12 연구 자료·실험 승인 경계와 `main`을 변경하지 않고 누적 별도 검증했다.

## 1. 실제 소스 정확성 및 실험한 단일 원본 모델 요소

기존 B3 45요소 role-named PNG 원장과 B6 원본 9개 후속 실험 큐의 **7순위** `AF123 / AF1394 / original source element index8`을 재대조했다. 원래 element8의 공식 실제 게임 기하는 **from=[12,7,3], to=[14,16,5]**, face **east/north/south/up/west 5면**이다. 원본 역할명 `back_10/acacia.png` 출처 텍스처와 연결한 **BACKREST_ASSEMBLY 역할 가설**은 소스 추정이지 부품 실제 기능·재질·스타일 승인 아니다.

- 공식 Another Furniture **Fabric 4.0.2 JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`**. 원본 공식 런타임 child `assets/another_furniture/models/block/chair/acacia_10_tucked.json` Git blob `71fd514e28b36b47b45cc6a38594b4d11059e6ff`, 공유 원본 provider `assets/another_furniture/models/block/template/chair_tucked.json` Git blob `bbfd54f73fd764015ce320082ba531bd314a6dfd`를 그대로 확인했다. 연구판 4.0.3 소스와 게임 배포판 4.0.2의 JSON을 바이트 동일하다고 가정하지 않았다.
- 원본 공유 template에 정의된 **10요소·46면** 중 source8의 **5면만** 제외하고 남은 원본 요소 **9개·41면**을 **`acacia_10_tucked.json` 자식 단일 JSON**에 명시 오버라이드. 공유 부모·기타 자식 모델·모든 원본 텍스처 및 다른 모든 JAR 압축 해제 리소스 바이트 불변, JAR 멤버 목록·ZIP CRC 검수. 변경된 리소스는 정확히 **1개**.
- 실험용 수정 JAR SHA1 `6a4fd6266590888864be49d2b8d0959f07021b16`. 원본·변형 JAR/모델 소스/제삼자 원본 텍스처를 Git 또는 F2 증거 ZIP에 넣거나 배포하지 않았다.

## 2. AF123의 유효한 원본 tucked=true 지지 슬랩 상태

북향 원본 의자 state **`another_furniture:acacia_chair[facing=north,tucked=true,variant=10]`**. 이 상태를 실제 게임에서 유효하게 유지하려면 앞쪽 **`minecraft:oak_slab[type=top]`**을 먼저 설치하고 보존해야 한다. B4 정상 지지 슬랩 world fixture와 서버의 **의자/슬랩 상태 검증**을 재사용해, 슬랩 없는 tucked=true 의자를 허구의 원본 기준으로 삼지 않았다.

기존 공식 B4 [Minecraft 원본 실게임 Actions #45528207751](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751) **네이티브 F2 8장** 실제 ZIP artifact #14982648778을 별도로 다시 내려받았다. 원본 ZIP 전체 SHA256 `4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35`, 모든 11개 엔트리 ZIP CRC, 8개 원본 PNG SHA·client.log SHA 및 정확 의자+슬랩 서버 상태 16쌍을 재검증했다. 원본 B4 재감사 JSON은 Git에 고정된 B4 영구 감사 JSON과 정확히 일치한다.

## 3. 실제 새 Minecraft F2 촬영 및 픽셀 차이

[**B13 실제 Minecraft Java 1.21.1 Fabric Actions #45561411530 — 전체 SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45561411530). 검증 소스·런처·13개 회귀시험·Actions 코드는 **`ba87d72bf9b49aae4f273082e634027cbf83ac86`**에서 실제로 시험됐다.

별개 실제 게임 새 클라이언트에서 정상 지원 슬랩을 보존한 AF123 의자에 **원본 source index8만 제거한 자식 모델**을 적용했다. 동일 남쪽·북쪽 카메라에서 각각 **의자+슬랩(A) → 슬랩만(B) → 의자+슬랩(A) 복원 → AIR** 4단계, **실제 신규 네이티브 F2 PNG 8장**을 촬영했다. 정확 server 의자/슬랩 상태 **16쌍**, 신규 PNG/게임 로그 SHA 검증. 기존 원본 B4 8장과 신규 B13 8장 = **서로 다른 공식 게임 세션의 실제 F2 총16장**. 실측 RGB ROI **[350,275,675,620]**, RGB 최대 채널 차이 threshold **24**.

| 원본 B4 F2 ↔ element8 제거 B13 공식 게임 F2 | 남쪽 | 북쪽 |
|---|---:|---:|
| **원본 chair+slab vs index8 단독 제거 chair+slab** | **276 px** | **80 px** |
| **chair+slab A 복원 뒤 동일한 변화** | **276 px** | **80 px** |
| 원본↔수정 slab-only 음성대조 | **0 px** | **0 px** |
| 원본↔수정 AIR 음성대조 | **0 px** | **0 px** |
| 수정 게임 chair+slab A/A 시간 drift | **0 px** | **0 px** |
| 기존 원본 의자 전경 밖 변화 | **0 px** | **0 px** |
| 기존 원본 의자 전경, 원본 chair+slab vs slab-only | 2,656 px | 386 px |

**실제 원본 ZIP와 수정 ZIP의 16개 원본 F2 PNG를 독립적으로 다시 열었다.** 각 카메라에서 실험 이미지의 PNG 해상도 1024×684와 ZIP CRC를 다시 확인하고, 실제 raw RGB ROI를 임계값24로 새로 계산하자 **남쪽 before/after 276/276, 북쪽 before/after 80/80, 양방향 slab-only/AIR 0/0**으로 독립 감사 숫자가 재현됐다. 시각적으로 **AF123 등받이 한쪽의 얇은 세로 지지 영역이 제거된 변화**가 보이며 실험 기하와 부합한다.

단, 한 요소 제거에 따른 화면 차이의 원인이라는 제한적 결론이지, 차이가 난 **276/80픽셀이 원래 해당 다섯 개 face의 배타적 GPU 픽셀 소유권**임을 뜻하지 않는다. 겹친 후면 노출, 가림이나 조명·셰이딩 변화가 있을 수 있다. 실제 앉기 기능·재질·스타일 또는 학습/재배포 라이선스 승인도 아니다.

**최종 판정: `PASS_BOUNDED_AF123_ELEMENT8_REMOVAL_RENDER_RESPONSE`** — 정확 원본 자식 모델의 source index8 단독 제거가 정상 윗반블록 지지 상태의 두 게임 화면에서 국소 변화를 유발함을 인과적으로 확인.

## 4. 영구 결과 및 재현 방법

- [**B13 신규 실게임 F2 8장·client.log·단일 자식 개입 출처 감사 아티팩트 #14997937670**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45561411530/artifacts/14997937670) (45일 보존; 원본 B4 8장은 별도).
- `project/integration/INT5_B13_AF123_ELEMENT8_NATIVE_F2_CAUSAL_AUDIT_V1.json`: B4 원본 F2 8개 SHA, 신규 B13 F2 8개 SHA, 두 클라이언트 로그 SHA, 공식 4.0.2 SHA/공유 부모 SHA, source8 5면·한 자식 변경, 실제 서버 16쌍·화면 및 부정대조 수치 영구 보존.
- **원본 성공 Actions 아티팩트 JSON Git blob SHA1 `4b04bc83c6efa30c8f1d2ab29c0f9a6f49666974`와 GitHub 영구 감사 JSON blob SHA1이 바이트 단위 완전히 일치함**을 별도로 검증.
- `src/mcfr/int5_b13_af123_backrest_element8_native_f2.py` + `src/mcfr/runtime.py`: 공식 원본 소스 JAR·자식 단독 요소8 개입·정상 지지 슬랩 세계 선택·실제 F2/원본 B4 독립 검사.
- `tests/knowledge/test_int5_b13_af123_backrest_element8_native_f2.py`: 원본 소스 5면·10/46→9/41·정상 tucked/slab·부정대조 및 권리 차단 등 **13개 회귀시험**.
- `.github/workflows/integration-int5-b13-af123-backrest-element8-native-f2.yml`: 원본 ZIP SHA/CRC·원본 B4 영구 JSON, 실게임 서버 16쌍, 새 F2 8 PNG SHA·권리 금지 및 엄격 PASS 결정 검사.

## 5. INT-5 누적 검증 현황

| 연구 항목 | B13 실제 성공 이후 검증된 누적 |
|---|---:|
| 원본 소스 모델 요소 및 face/UV 출처 연결 | **45/45 요소 · 229/229면** |
| 원본 역할 가설 그룹 출처 연결 | **15/15** |
| **서로 다른 원본 소스 요소의 실게임 단독 개입→화면 인과 증거** | **8/45 = 17.8%** |
| 개별 제거 실험을 아직 수행하지 않은 요소 | **37/45 = 82.2%** |
| 역할명 텍스처 큐 원본 9 요소 중 별도 실제 제거 실험 | **8/9** |
| 원본 B6 후속 연구 큐 9건 중 실제 수행 | **7/9** |
| 원래 요소별 배타적 GPU face/pixel 귀속 승인 | **0/45** |
| 부품의 실제 기능·재질·스타일 최종 의미 승인 | **0/45** |
| INT-6 제삼자 원본 모델/텍스처 학습·재배포 권리 승인 | **0** |

기존 B5 AF123 좌판4 / B7 AF121 좌판4 / B8 HC11210 검은 쿠션12 / B9 AF121 등받이7 / B10 AF121 등받이8 / B11 AF121 등받이9 / B12 AF123 등받이7 / **B13 AF123 등받이8**의 각 source 키·원본·개입 게임 세션은 서로 독립적인 검증 근거다. **H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70**도 불변.

**다음 후보:** B6 큐 **8순위 `AF123/AF1394/등받이 원본 index9(5면)`**는 아직 독립적인 실제 Minecraft 제거 및 음성대조를 수행하지 않았다. 같은 AF123 원본 tucked 지원 슬랩과 부모 불변 자식 단독 개입·원본/수정 별개 세션이 필요하다. PR Draft·미병합, `main` 불변.
