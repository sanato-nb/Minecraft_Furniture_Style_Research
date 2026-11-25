# INT-5-B8 — Handcrafted 의자 쿠션 요소12 원본·실게임 F2 단일 개입 인과 재감사

검증일 **2026-11-25 KST**. 직계 [INT-5-B7 Draft PR #119](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/119) head `26784200843b9ad50b7cc105a0df2bff0ec14608`에서 [INT-5-B8 Draft PR #120](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/120)으로 분기했다. 기존 B1~B7 증거/검수 데이터, `main` 및 원본 공개 모드는 수정하거나 병합하지 않았다.

## 1. 연구 목표와 공식 출시판 원본

B6의 45개 부품 원장에서 미실험 대상으로 선택한 **Handcrafted HC11210 / 원본 제공자 HC13 / source element 12 / 원본 6면 / `SEAT_LAYER` 역할 가설**의 실제 렌더 인과를 신규 Minecraft F2 실험으로 확인했다.

[원본 사전 검사 Actions #45542452464 SUCCESS](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45542452464): 실제 공식 Modrinth **Handcrafted Fabric 1.21.1-4.0.3** JAR SHA-1 `a9579fecd7ed429c282be21d5c921d220197acc6` 검증. 원본 black child 모델 `handcrafted:block/warped_chair_black`는 `handcrafted:block/chair/chair`를 상속한다. 실제 부모의 **13요소·78면** 중 원본 **index 12**가 6면이고 모든 면 텍스처 슬롯이 `handcrafted:block/chair/cushion/black_cushion`으로 실제 해석됨을 ZIP 원본에서 확인했다.

원본 좌표 `from=[3,9,2]`, `to=[13,11,14]`; 부모 모델의 공식 실행판 Git blob SHA-1 **`c5d9fbc054a897673f972fe2559376123751ba9b`**, 연구 원본과 정확 일치한다. 검은 자식 Git blob `2d989c0059a633a55ebe1386bf5c9547ccd86de7`, 원본 미수정 흰색 의자 자식 Git blob `6000caa39ce50c3b71632e59cfb49d0dfe2c9737`.

이번 연구는 텍스처 이름과 원본 형상으로 **원래 사물의 렌더 요소**를 추적하지만, 부품의 실제 착석 기능 또는 재질·스타일을 이를 통해 확정하지 않는다.

## 2. 원본 손상 없는 정확한 소스 개입

- 실제 원본 게임 선택 상태는 `handcrafted:warped_chair[facing=north,color=black,waterlogged=false]`; 비교 음성대조는 `handcrafted:warped_chair[facing=north,color=white,waterlogged=false]`. 두 모델은 같은 원본 부모를 상속하지만 **서로 다른 자식 JSON**이다.
- 공식 JAR 원본 SHA 고정 후 **검은 자식 `assets/handcrafted/models/block/warped_chair_black.json` 단일 멤버**에만 부모 원본 element 0~11 전체를 복사하고 index12를 제외한 **12요소·72면**을 직접 오버라이드. 공통 `chair/chair.json` 부모와 흰색 자식의 원본 **압축 전 바이트 및 모든 다른 ZIP 리소스 불변**, CRC 및 실제 ZIP 재개봉 검증.
- 실험에만 사용된 임시 수정 JAR SHA-1 `04a5b86a8f4f4005dd69ac24ba8d59e9bcabb28e`. 제삼자 원본·수정 JAR, 모델 JSON 원본, 텍스처 및 클라이언트 게임 파일은 Git에 커밋하거나 사용자에게 재배포하지 않았다.
- 같은 원본 Minecraft Java **1.21.1 Fabric** 일회성 월드의 새 클라이언트 **2개 독립 세션**: ① 원본 공식 JAR ② 첫 세션 종료 후 월드를 초기 원본으로 되돌리고 임시 단일 모델 개입 JAR.
- 각 세션에서 두 대향 카메라 **south / north**의 `black_before → white → black_after → air` 네 단계 **네이티브 F2 8장씩, 합계 16장**, 서버 블록상태 응답 **16/16개**, PNG 1024×684/원본 개별 SHA-256와 실제 client.log SHA 검사.
- 원본 좌표 `(40,120,40)`; 고정 카메라 `south:40.5,122.3,45.5 yaw180 pitch20`, `north:40.5,122.3,35.5 yaw0 pitch20`. RGB `ROI=(350,275,675,620)`, 각 채널 `>=24` 원본↔수정 픽셀 변화.
- 처음 두 번 촬영에서 **Handcrafted 색상 교체 시 생기는 움직이는 드롭 아이템 엔티티**가 원본/수정 AIR 및 흰색 비교 화면을 변화시키는 교란을 실제 F2로 발견. 이를 승인하지 않고 각 16장 F2 **촬영 직전 아이템 제거 + `/execute unless entity @e[type=minecraft:item]` 서버 확인 16/16건**을 추가하여, 교란이 해소된 새 실게임 원본 16장으로 엄격 재검증.

## 3. 실제 최종 Actions 및 원본 F2 직접 검수

[**최종 GitHub Actions #45544073413 SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45544073413). 검증된 시험 코드 커밋 `dfe6e470918a9e1dc05cd72974e9608da6eb5b79`: 원본 검사 및 새 회귀시험, 실제 Fabric 2회 실행, 16개 server state, 16개 드롭아이템 부재 서버 마커, 16장 실제 F2 PNG 직접 재개봉, 양방향 ROI/음성대조 전체 통과.

[성공한 새 16장 F2+로그 SHA 아티팩트 #14991555743](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45544073413/artifacts/14991555743) (45일 만료). ZIP CRC 검증, 파일 22개(원본/수정 각 F2 8, client.log·세션 manifest, 상위 manifest·audit JSON). 원본 아티팩트의 감사 JSON Git blob **`1e27c5dd13ea99dae2c34684dcdf0c99e2a82de3`**와 Git에 영구 커밋된 JSON Git blob이 **바이트까지 일치**함을 재확인했다.

원본/수정 PNG를 직접 열어본 시각 관찰: **북쪽 카메라는 원본 검은 쿠션 좌면이 보이고, index12를 없애면 해당 자리에 안쪽 청록색 프레임이 드러난다.** 반대쪽 남쪽 카메라에서는 등받이에 일부 가려져 변화 영역이 더 작다. 이 관찰은 원래 쿠션 요소의 **제거가 만든 가시적 결과**를 보조한다. 특정 변경 픽셀 모두를 원본 요소 12가 배타적으로 소유했다는 뜻은 아니다.

## 4. 실제 RGB 픽셀 및 모든 음성대조

| 원본 네이티브 F2 ↔ 요소12 제거 네이티브 F2 | 남쪽 시점 | 북쪽 시점 |
|---|---:|---:|
| **검정 black_before 원본→임시 제거** | **572px** | **1,794px** |
| **검정 black_after 반복 비교** | **572px** | **1,794px** |
| 미수정 흰색 white 원본↔수정 비교 | **0px** | **0px** |
| AIR 원본↔수정 비교 | **0px** | **0px** |
| 원본 세션 black_before↔black_after 시간 변화 | **0px** | **0px** |
| 수정 세션 black_before↔black_after 시간 변화 | **0px** | **0px** |
| 원본 검정 의자 전경 밖 변경 픽셀 | **0px** | **0px** |
| 원본 검정 의자 자체 전경 vs AIR | 7,038px | 7,698px |
| 각 촬영 직전 드롭 아이템 엔티티 서버 확인 | **0개 검증** | **0개 검증** |

음성대조, 정확 서버 블록상태, JAR 원본·수정 범위, F2 개별 해시 모두 통과. 엄격하게 제한한 결과는 **`PASS_HC11210_BLACK_CHILD_ELEMENT12_REMOVAL_REAL_NATIVE_F2_RESPONSE`**다. **소스 index12 제거 → 검정 쿠션 의자 화면 응답**을 독립 검증한 것이며 GPU 원본 face/UV 픽셀 소유권·착석 기능·재질·스타일·학습/재배포 라이선스 승인과 구분한다.

## 5. 이전 두 실패와 반증 사실 보존

| Action | 경과 | 의미 |
|---|---|---|
| [#45542711431](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45542711431) | **실패**, B8 명령이 AF121 런처 분기에 잘못 포함되어 Handcrafted 대신 AF 의자 월드가 배치됨 | 실제 서버 블록상태 ACK 실패. 오류 수정 및 재발 방지 회귀시험 추가 |
| [#45543182600](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45543182600) / [#45543197621](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45543197621) | 원본·수정 F2 **16장 촬영됐으나 Actions 실패**, 런처 새 상태 종료 코드 누락. 촬영 PNG 직접 재개봉 시 **색상 변경으로 발생한 움직이는 아이템 엔티티**가 AIR/white/시간 대조를 오염 | 기존 화면 일부 픽셀 차이를 인과 PASS로 승격하지 않고, 드롭 엔티티 제거·원본 서버 16회 부재 검증을 추가 |
| [#45544073413](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45544073413) | **SUCCESS**. 서버 16회 무아이템 증명 + 원본/수정 F2 전부 정상; white, AIR, 시간, 원래 의자 전경 밖 변화 **모두 0** | **범위 한정 source intervention→render response 독립 통과** |

## 6. INT-5 누적 결과와 보류 범위

| 구분 | 누적 상태 |
|---|---:|
| B3 고정 의자 원본 source element 및 UV | **45/45부품 / 229/229면** |
| 역할 가설 그룹 원본 연결 | **15/15** |
| **실제 원본 소스 요소 제거→렌더 변화 검증** | **3/45** (AF123 index4, AF121 index4, HC11210 index12) |
| 개별 개입 인과 미실험 원본 요소 | **42/45** |
| 텍스처 이름에 역할 단서가 있는 원본 요소 중 실제 개입 실험 | **3/9** |
| 배타적 원본 요소→GPU 픽셀 소유권 승인 | **0/45** |
| 실제 부품 기능·재질·스타일 최종 의미 승인 | **0/45** |
| INT-6 제삼자 AI 학습·재배포 권리 승인 | **0** |

B5의 AF123은 접힌 의자+슬랩 상태에서 **남751/북0px**, B7의 AF121은 기본 의자에서 **남1,182/북2,132px**, B8의 HC11210은 검정 쿠션에서 **남572/북1,794px**이다. 각 개입은 서로 다른 요소/모델/상태이므로 개입 응답을 다른 요소의 자동 판정으로 복제하지 않는다. H03 **HOLD**, H05 **CONDITIONAL**, F70 엄격 무조건 승인 **0/70** 유지.

## 7. 영구 저장 및 다음 검증

- `src/mcfr/int5_b8_hc_cushion_source_preflight.py`: 공식 출시판 원본 JAR/136 states/부모·자식/원본 cushion 6면.
- `src/mcfr/int5_b8_hc_cushion_element12_native_f2.py`: 원본/임시 수정 실제 F2 16장, 무아이템/화이트/AIR 음성대조, 실게임 독립 감사.
- `src/mcfr/runtime.py`: HC 런처 전용 소스 월드 및 신규 capture 결과 정상 종료 코드.
- `tests/knowledge/test_int5_b8_hc_cushion_element12_native_f2.py`: 독립 **13개** 시험 (초기 11, HC world 선택 회귀, 드롭 아이템 차단).
- `.github/workflows/integration-int5-b8-hc-source-preflight.yml`, `.github/workflows/integration-int5-b8-hc-cushion12-real-native-f2.yml`: 원본 preflight와 실제 두 게임 검증.
- `project/integration/INT5_B8_HC11210_CUSHION12_REAL_F2_CAUSAL_AUDIT_V1.json`: 16개 PNG/두 client.log SHA, 인과 수치, 공식 원본 JAR·모델 출처, 엄격 한계.

**다음 후보:** B6 연구 큐의 AF121 `BACKREST_ASSEMBLY` elements 7/8/9 또는 Macaw 좌면 대비. 실제 소스 index 개입은 아직 수행하지 않았으며 역할/기능 승인도 하지 않았다. Draft PR만 사용하고 `main`은 미병합.
