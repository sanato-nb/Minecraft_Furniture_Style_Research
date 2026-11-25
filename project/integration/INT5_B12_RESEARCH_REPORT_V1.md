# INT-5-B12 — AF123 정상 tucked 의자 등받이 source element7 원본 2면의 실제 Fabric F2 단일 제거 인과 검증

**검증일 2026-11-25 KST.** B11 [Draft PR #123](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/123) 최종 HEAD bd9e389617497193d9cc5d907a83f078e930c056에서 누적 [B12 Draft PR #124](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/124)로 분기했다. 기존 B1~B11 연구 데이터·코드·권리 결론과 main을 변경하지 않고 새로운 실험을 별도 보존했다.

## 1. 원본 소스 출처 및 실험대상 정확성

기존 B3 45요소 원본 texture-role cue 근거와 B6 45행 원장·9개 실험 큐 **6순위**를 직접 확인해 AF123 / AF1394 / **source index7**로 확정했다. 연구상 원래 2개 face는 **north / south**; 원본 좌표 **from=[4,7,4], to=[12,16,4]**의 두께 0인 가로 범위가 넓은 평면이다. 두 면의 출처는 원본 역할명 텍스처 back_10/acacia.png이며 BACKREST_ASSEMBLY는 아직 **소스 기반 역할 가설**이다.

- 실제 배포판 Another Furniture **Fabric 4.0.2** 공식 JAR SHA1 **c2f992081bdc4795ed6d87771a3b5f7c71103785**, Java 1.21.1 Fabric 원본 게임. 연구판 Git 4.0.3과 실행판 4.0.2 파일은 바이트가 같다고 추정하지 않았다.
- 원본 child: assets/another_furniture/models/block/chair/acacia_10_tucked.json, 공식 실행판 Git blob SHA1 **71fd514e28b36b47b45cc6a38594b4d11059e6ff**. 공유 원본 parent: assets/another_furniture/models/block/template/chair_tucked.json, Git blob SHA1 **bbfd54f73fd764015ce320082ba531bd314a6dfd** (기존 B5 독립 실증 고정).
- 원래 parent에 정의된 **10 elements / 46 faces** 가운데 원본 source index7의 **2면만 제외한 9 elements / 44 faces**를 오직 **acacia_10_tucked 자식 모델 1개**에 명시 오버라이드. 공유 template/chair_tucked 부모 및 모든 기타 JAR 멤버의 압축 해제 원본 바이트는 불변, 원본 목록/CRC 확인. 수정 한 리소스 외 변경0. 임시 런타임 JAR SHA1 **664cea196074e1a6b07447c30a900861a0dffe4d**.
- 원본·임시 수정 JAR, 원본 PNG/저작권 있는 모델 소스는 Git이나 CI 결과 아티팩트에 포함하지 않았다.

## 2. AF123은 AF121과 다른 원본 게임 상태

실제 검증 대상 북향 원본 blockstate: **another_furniture:acacia_chair[facing=north,tucked=true,variant=10]**. 이 상태는 앞쪽 인접 좌표에 **minecraft:oak_slab[type=top]**이 있어야 정상적으로 유지된다. 반드시 슬랩을 먼저 설치한 뒤 의자를 설치하는 기존 B4의 공식 원본 fixture와 의자+슬랩 서버 검증을 재사용했다. 실제 실험 중에 의자는 그대로 둔 채 정상 지지용 슬랩만 제거하는 불가능한 tucked=true 상태를 유효한 근거로 인정하지 않았다.

기존 B4 [실제 원본 Fabric Actions #45528207751](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751)의 **원본 F2 8장** 아티팩트 #14982648778 전체 ZIP SHA256 **4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35**를 다시 다운로드해 CRC·원본 8 PNG·client.log SHA·원본 의자/슬랩 서버 상태 16쌍을 검증했다. B4의 이미 커밋된 독립 감사 JSON과 Python 재감사 결과가 **내용 동일**임을 확인했다.

## 3. 실제 게임 새 8 F2와 음성대조

**[B12 수정 완료 실게임 Actions #45559681670 — 전체 SUCCESS](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45559681670)**. 검증 실행 코드·런타임·13회 회귀시험·Actions 변경 기준 커밋 **abdb0e32c5ff6f0f44030d0d0f3b90fc26d62951**.

별개 Minecraft Java **1.21.1 Fabric** 새 클라이언트 세션에서 원본 블록·원래 윗반블록 지지·원래 카메라를 유지한 채, 자식 모델의 **source7만 제거**하고 남쪽 및 북쪽 두 시점에서 각각 네 단계 **(1) chair+slab A, (2) slab only, (3) chair+slab A 복원, (4) AIR** 총 **신규 네이티브 F2 8장**을 생성했다. **실제 서버 의자·슬랩 상태 16개**, 8장 PNG SHA, 새 client.log SHA 확인. 기존 원본 8장과 신형 8장은 서로 다른 공식 게임 세션이다. 비교 RGB ROI **[350,275,675,620]**, 임계값 RGB 채널 최대 변화 **24**.

| 원본 B4 ↔ 수정 B12 실제 네이티브 F2 비교 | 남쪽 | 북쪽 |
|---|---:|---:|
| **원래 chair+slab A vs source7 제거 후 chair+slab A** | **714px** | **136px** |
| **chair+slab A 복원 후 동일 screen-response** | **714px** | **136px** |
| 원본↔수정 슬랩만 유지한 음성대조 | **0px** | **0px** |
| 원본↔수정 AIR 음성대조 | **0px** | **0px** |
| 수정 게임 세션 A↔A 시간 변화 | **0px** | **0px** |
| 기존 원본 의자 전경 밖의 변경 픽셀 | **0px** | **0px** |
| 기존 원본 의자 전경, chair+slab vs slab only | 2,656px | 386px |

원본 B4와 새로운 B12 **원본 네이티브 PNG 16장을 실제 다시 열어 직접 시각 비교**했다. 윗반블록 아래 등받이/가로 영역에서 요소7 제거에 따른 국소적인 띠 변화가 남쪽에 더 크게, 북쪽에 더 작게 관찰되며 소스 형상 평면 및 실측 차이와 일치한다. 단, 변동 픽셀에는 occlusion·뒤쪽 면 재노출 및 조명 변화가 포함될 수 있다. **원본 index7의 두 face가 변화한 714/136px을 독점적으로 차지했다는 것은 아니다.**

**실제 엄격 판단: PASS_BOUNDED_AF123_ELEMENT7_REMOVAL_RENDER_RESPONSE.** 원본 source index7을 독립 제거하면 정상 지원 슬랩이 있는 두 화면에서 확인 가능한 차이가 난다는 실험적 인과만 승인한다. 원본 착석·등받이 구조 기능, 물리적 재질·디자인 스타일, 원본 face→GPU 픽셀 배타적 소유, INT-6 원본 텍스처/모델 학습 또는 제삼자 자산 배포 권리는 모두 승인하지 않는다.

## 4. 독립 감사 증거 및 GitHub 재현성

- [신규 실제 게임 F2 8장+원본 게임 로그+임시 자식 모델 수정 출처+감사 JSON Actions 아티팩트 #14996579584](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45559681670/artifacts/14996579584) (45일 후 만료). 정품 원본 JAR/변형 JAR/원본 텍스처 없음.
- **project/integration/INT5_B12_AF123_ELEMENT7_NATIVE_F2_CAUSAL_AUDIT_V1.json**에 양 게임 원본 8 F2 SHA·새 8 F2 SHA, 공식 4.0.2 JAR 원본 SHA와 child/parent blobs, 서버 지지 상태 16건, source7 기하2면, 실제 화면 변화 및 음성대조 완전 기입.
- **Actions 원본 ZIP 내 감사 JSON Git blob SHA1 a25cd97ee0095533efdabe6a369ed322321b893f = GitHub 커밋의 영구 JSON Git blob SHA1** **바이트 그대로 일치**를 별도로 다운로드/검증했다.
- src/mcfr/int5_b12_af123_backrest_element7_native_f2.py: 원본 소스 고정/단일 child intervention/B4 원본 아티팩트 8 F2 독립 대조.
- src/mcfr/runtime.py: 원래 AF123 북향 tucked/윗반블록 source state로 새 스크린샷, 기존 B4~B11 명령 분리 보존.
- tests/knowledge/test_int5_b12_af123_backrest_element7_native_f2.py: **13개 테스트** (원본 요소7 두면, 모델 기하10/46→9/44, 잘못된 공유 parent/지원슬랩/음성대조/권리 승격 차단).
- .github/workflows/integration-int5-b12-af123-backrest-element7-native-f2.yml: 원본 B4 전체 ZIP SHA·원본 영구 감사 대조, 실제 1.21.1 Fabric 런타임, 정상 슬랩 server checks 16, 인과·반증 감사 PASS.

## 5. INT-5 누적 검증 현황 (B12 실게임 PASS 후)

| 원본 연구 범위 | 이번 단계 완료 이후 |
|---|---:|
| 원본 소스 모델 요소 및 UV face 출처 연결 | **45/45 요소 · 229/229면** |
| 원본 역할 가설 그룹 연결 | **15/15** |
| **서로 다른 원본 요소 독립 게임 개입→국소적 렌더 인과 실증** | **7/45 = 15.6%** |
| 아직 개별 독립 렌더 인과 미검증 | **38/45 = 84.4%** |
| 구별된 역할명 텍스처 cue를 가진 원본 9 요소 중 실제 단독 개입 | **7/9** |
| B6 원본 다음 연구 후보 큐 9개 중 검증 완료 | **6/9** |
| 원본 개별 source element→GPU pixel/face 배타적 소유 승인 | **0/45** |
| 부품의 실제 기능·재질·스타일 최종 의미 승인 | **0/45** |
| INT-6 제삼자 원본 자산 학습/배포 권리 승인 | **0** |

B5 AF123 좌판4 / B7 AF121 좌판4 / B8 HC11210 검은 쿠션12 / B9 AF121 등받이7 / B10 AF121 등받이8 / B11 AF121 등받이9 / **B12 AF123 등받이7**은 모두 소스 키/카메라/원본 PNG·게임 로그 구별된 독립 시험이다. 엄격 H03 HOLD, H05 CONDITIONAL, F70 무조건 0/70 불변.

**다음 후보:** B6 원본 큐 **7순위 AF123 / AF1394 / 등받이 source index8(원본5면)**. 같은 정상 윗반블록 지원 및 자식 단일 격리·두 게임 세션 실제 F2 원본 검증을 해야만 신규 인과 승인할 수 있다. 이번 B12로 다른 방향·index8/9·재질·기능까지 추론하지 않는다. PR Draft·미병합, main 불변.
