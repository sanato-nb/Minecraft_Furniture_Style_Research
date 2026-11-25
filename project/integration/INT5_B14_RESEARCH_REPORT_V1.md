# INT-5-B14 — AF123 정상 tucked 의자 원본 등받이 source index9(5면) 실제 Minecraft F2 독립 인과 감사

**실제 검증일 2026-11-25 KST.** 기존 [B13 Draft PR #125](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/125)의 최종 검수 HEAD `aa2f71fc82b08d051c00ce35e6b7aecedef722c9`에서 별도 [B14 Draft PR #126](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/126) 분기. 원본 B1~B13 자료 및 원본 `main`을 수정하지 않았고 PR은 미병합이다.

## 1. 원본 요소9의 직접 검수 증거

B3 원본 45요소 원장과 B6 초기 실험 큐 **8순위**가 `AF123/AF1394/original_source_element_index9`임을 원문 CSV에서 직접 대조. 원본 소스 요소9의 5개 face `east,north,south,up,west`, 기하 `from=[2,7,3]`, `to=[4,16,5]`가 공식 실제 게임 배포판의 원래 공유 부모 모델에 정의되어 있음을 확인했다. B3의 5면은 원본 `back_10/acacia.png` 텍스처 역할명 단서에 연결된다. **BACKREST_ASSEMBLY는 역할명/형상에 근거한 가설이지 등받이의 실제 기능이나 재질·스타일 또는 원본 각 face가 독점한 GPU 픽셀의 승인 근거가 아니다.**

- 공식 Minecraft Java **1.21.1 Fabric**, Another Furniture **Fabric 4.0.2** 원본 JAR SHA-1 **`c2f992081bdc4795ed6d87771a3b5f7c71103785`**.
- 실제 출시판 원본 child `assets/another_furniture/models/block/chair/acacia_10_tucked.json` Git blob SHA-1 **`71fd514e28b36b47b45cc6a38594b4d11059e6ff`** 및 원본 공유 parent `assets/another_furniture/models/block/template/chair_tucked.json` Git blob SHA-1 **`bbfd54f73fd764015ce320082ba531bd314a6dfd`**.
- 원본 parent **10요소·46면**에서 원본 **index9의 5면 하나만 제외**한 9요소·41면을 원본 `acacia_10_tucked.json` **자식 JSON 한 멤버에만 오버라이드**. 공유 parent·다른 모든 모드 원본 리소스/텍스처는 압축 해제 바이트 불변, 원본 ZIP CRC 및 멤버 목록 동일.
- 실험용 임시 JAR SHA-1 **`764df594bdc5460058c1fed032d9e325bb91ff70`**, 공식 원본 대비 실제 변경된 uncompressed member 정확히 **1개**. 연구 소스 Git 4.0.3과 공식 실행판 4.0.2가 byte-identical이라는 추정은 하지 않았다. 제삼자 원본·임시 JAR/모델 JSON/텍스처 PNG를 Git이나 Actions 아티팩트에 재배포하지 않았다.

## 2. AF123 원본 정상 의자 + 지지물 게임 상태

북향 원본 블록은 `another_furniture:acacia_chair[facing=north,tucked=true,variant=10]`이다. 원본 게임에서 이 상태의 유효성은 앞쪽 `minecraft:oak_slab[type=top]` 지지에 달려 있으므로 슬랩을 먼저 배치하고 유지했다. 앞쪽 슬랩 없이 tucked=true를 주장하는 게임 상태를 정상 근거로 사용하지 않았다.

이전 [B4 원본 실게임 Actions #45528207751](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751)의 원본 정상 의자 F2 **8장** artifact **14982648778** 전체 ZIP SHA-256 **`4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35`**을 독립 다운로드·재검증했다. ZIP **11개 파일 CRC 전부 OK**, 원본 PNG 8개의 SHA와 실제 원본 client.log SHA, 원본 의자/슬랩 정확 서버 상태 16쌍, 이미 저장된 B4 원본 감사 JSON과의 재감사 동일성까지 확인했다.

## 3. 실제 Minecraft 신규 F2 8장·정확 서버 상태·부정대조

[**B14 실게임 Java 1.21.1 Fabric Actions #45562828175 — 전체 SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45562828175). 테스트된 소스·워크플로·런타임 기준 커밋 `68ffcd891beaa7952cb9c8d0b08bb1e30ae23cc7`.

원본 B4와 구별되는 **새 실게임 세션**에서 정상 지원 슬랩을 유지한 원래 AF123 의자에 index9만 제거한 모델을 적용. 원본 B4와 같은 남/북 두 시점 각각 `chair+slab A → slab only → chair+slab A 복원 → AIR` 4단계로 **새 Minecraft 네이티브 F2 8장**과 신규 PNG/client.log SHA, 실제 서버 의자+슬랩 **16쌍**을 기록·검증했다. 두 게임 세션 총 **16장**, RGB ROI `[350,275,675,620]`, 최대 채널 차이 임계값 **24**.

| 실제 원본 B4 ↔ 수정 B14 네이티브 F2 | 남쪽 | 북쪽 |
|---|---:|---:|
| **source index9 단독 제거 전/후 화면 차이** | **296 px** | **80 px** |
| **의자 A 복원 뒤 변화 재현** | **296 px** | **80 px** |
| 원본↔수정 slab-only 부정대조 | **0 px** | **0 px** |
| 원본↔수정 AIR 부정대조 | **0 px** | **0 px** |
| 수정 실게임 A/A 시간 드리프트 | **0 px** | **0 px** |
| 원본 의자 전경 범위 밖 개입 변화 | **0 px** | **0 px** |
| 원본 의자 전경 chair+slab vs slab-only | 2,656 px | 386 px |

독립적으로 내려받은 원본 **B4 8 PNG** 및 수정 **B14 8 PNG**를 **Pillow로 실제 재개봉**, 모든 ZIP CRC·PNG 형식/1024×684 크기 검사 및 새 manifest PNG SHA 일치를 확인했다. 별도의 픽셀차 계산으로 **남 296 px / 북 80 px**를 재현했다. 확대 대조에서 원본 의자 등받이의 **한쪽 좁은 세로 지지 영역이 사라지는 국소 변화**가 확인되어 원본 index9의 `[2,7,3]→[4,16,5]` 기하와 부합한다. 다만 뒤쪽 원래 가려진 부위의 노출이나 조명 변화가 섞일 수 있어 **변경 픽셀 296/80개가 해당 원본 5면의 GPU 배타적 픽셀이라는 뜻은 아니다.**

실제 독립 판정: **`PASS_BOUNDED_AF123_ELEMENT9_REMOVAL_RENDER_RESPONSE`**. 이 PASS는 정상 슬랩 지지 환경에서 **AF123 source element9만 단독 제거하면 두 원본 게임 카메라의 화면에 인과적 국소 변화가 생긴다**는 제한된 사실에만 적용한다. 실제 등받이 기능·착석 기능·재질·스타일·독점 GPU face/pixel/UV 매핑·제삼자 자산 학습/재배포 권리는 승인하지 않는다.

## 4. 재현 코드·영구 감사·바이트 일치 검증

- [**B14 수정 실게임 F2 8장, 서버 확인·client.log·단일 자식 개입 증거/감사 ZIP artifact #14997769661**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45562828175/artifacts/14997769661) (45일 보존; 원본 B4 F2 8장은 별개).
- **`project/integration/INT5_B14_AF123_ELEMENT9_NATIVE_F2_CAUSAL_AUDIT_V1.json`**: 원본 B4 8장/새 B14 8장 각 SHA, 원본/수정 게임 로그, 공식 4.0.2 배포판·shared parent/child SHA, 요소9 원본5면 기하, 원래 블록 상태, 16 서버쌍·화면 차이/대조 수치 및 엄격 승인 범위 저장.
- Actions **실제 원본 아티팩트 감사 JSON Git blob SHA1 `47c76cfa7c0bd960d02c54efe3a40318c7d2b01a`와 GitHub 영구 JSON blob SHA1이 바이트 단위 정확 일치**함을 직접 검증했다.
- `src/mcfr/int5_b14_af123_backrest_element9_native_f2.py`: 원본 SHA 및 index9 단일 child override, B4 원본 실제 F2 독립 대조·부정대조 인과 감사를 재현.
- `src/mcfr/runtime.py`: B5~B13 프로그램 보존, B14만 별도의 정상 AF123 tucked+슬랩 원본 fixture 사용.
- `tests/knowledge/test_int5_b14_af123_backrest_element9_native_f2.py`: **14개** 원본 B6 큐 8순위/정확 source9·5면·10/46→9/41·서버 슬랩 정상/부정대조·무권리 승격 회귀시험.
- `.github/workflows/integration-int5-b14-af123-backrest-element9-native-f2.yml`: 공식 원본 Minecraft 1.21.1 Fabric 실게임 8 F2, B4 원본 ZIP SHA/CRC/원본 JSON, 서버16쌍, 권리 차단/엄격 성공 검사.

## 5. INT-5 누적 현황 (B14 실게임 PASS 이후)

| 검증 항목 | 확정 수량 |
|---|---:|
| 원본 요소 출처 및 원본 face·UV 출처 검증 | **45/45요소 · 229/229면** |
| 원본 역할 가설 그룹 출처 연결 | **15/15** |
| **서로 다른 원본 요소 단독 개입의 실제 게임 국소 렌더 인과 검증** | **9/45 = 20.0%** |
| 아직 개별 소스 요소 단독 실게임 개입하지 않은 요소 | **36/45 = 80.0%** |
| B6 초기 9개 우선 큐의 독립 실험 완료 | **8/9** |
| 원본 개별 GPU face→pixel 독점 귀속 승인 | **0/45** |
| 물리적 부품 기능·재질·스타일 최종 의미 승인 | **0/45** |
| INT-6 제삼자 원본 자산 학습/재배포 권리 승인 | **0** |

개별 인과 확인 요소는 B5 AF123 index4 / B7 AF121 index4 / B8 HC11210 index12 / B9 AF121 index7 / B10 AF121 index8 / B11 AF121 index9 / B12 AF123 index7 / B13 AF123 index8 / **B14 AF123 index9**. 기존 엄격 **H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70** 유지. PR Draft 미병합, main 불변.

**다음 원본 실험 후보**는 B6 초기 큐 마지막 **9순위 MACAW67 / MACAW1424 / original source index0**, source 역할 가설 `SEAT_LAYER`, 원본 역할명 텍스처가 아니라 `UNIQUE_SOURCE_TEXTURE_CONTRAST_NO_ROLE_NAME` 단서이다. Macaw 원본 별도 Minecraft **1.21.11 Fabric**, 실제 원본 JAR/옵션·좌표·방향·원본 F2를 새로 확인한 뒤 진행해야 하며 Another Furniture 1.21.1/B4 슬랩 증거를 대체 사용해서는 안 된다.
