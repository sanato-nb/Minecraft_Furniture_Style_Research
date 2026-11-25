# INT-5-B17 — Handcrafted 원본 12개 요소 동시 실게임 인과 분석

기준일: 2026-11-25 KST · 직계 [Draft PR #128](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/128) HEAD `646c26c4e9d115556eb0c3db295eb69147ee683c`.

## 1. 반복 요청 없는 하나의 배치: Handcrafted HC11210의 미검증 12개

B16까지의 원본 45개 요소·229개 faces 중 실제 단일요소 제거→Minecraft F2 응답 **19/45**, 두 카메라 화면 반응 미검출 **2**, 아직 단일 요소 실험 전 **24**이다. 다음 24개를 한 개씩 따로 검수하지 않고 게임 버전/모드별 배치로 나눈다.

이번 **B17은 Handcrafted 검정 Warped 의자** `HC11210/HC13`에 속하는 정확 원본 요소 인덱스 **0~11(12개, 각 6 faces)**. 이전 B8에서 이미 실험한 원본 쿠션 element12(6 faces)는 **이번 배치 대상에 포함하지 않는다**. 원본 B3 역할 가설과 B16의 45행 원장을 각 요소 정확 ID로 검사한다.

| 원본 인덱스 | 원본 면 수 | 원본 기하/텍스처 역할 가설(기능 승인 아님) |
|---|---:|---|
| 0·1 | 각 6 | LEG_OR_LOWER_POST |
| 2 | 6 | BACKREST_ASSEMBLY |
| 3·4·5 | 각 6 | LOWER_FRAME |
| 6 | 6 | SEAT_LAYER |
| 7·8 | 각 6 | LEG_OR_LOWER_POST |
| 9·10·11 | 각 6 | BACKREST_ASSEMBLY |

## 2. 공식 원본·실제 2개 게임 세션·엄격 음성대조

- 원본: **Handcrafted Fabric 1.21.1-4.0.3** 공식 JAR SHA-1 `a9579fecd7ed429c282be21d5c921d220197acc6`, 원본 parent `handcrafted:block/chair/chair` Git blob `c5d9fbc054a897673f972fe2559376123751ba9b` 및 검정 자식/흰색 자식 각각 `2d989c0059a633a55ebe1386bf5c9547ccd86de7` / `6000caa39ce50c3b71632e59cfb49d0dfe2c9737`.
- 공식 원본 parent에는 **13요소/78 faces**. 각 독립 CI 작업은 검정 의자 자식 JSON 1개에만 원본 요소 중 **지정된 하나를 뺀 12요소/72 faces**를 오버라이드. 부모 JSON, 흰색 대조 자식, 원본 텍스처 및 나머지 모든 JAR 원본 ZIP 멤버의 압축 해제 바이트 동일성과 CRC를 검증한다.
- 고정 원본 상태: `handcrafted:warped_chair[facing=north,color=black,waterlogged=false]`. 음성대조: **미수정 흰색 의자** 및 AIR. 원본 Java **1.21.1 Fabric** 임시 세계를 각 요소마다 만들고, 원본 게임 1회 + 해당 단일요소가 제거된 새 게임 1회로 비교한다.
- 두 게임 각각 남/북 시점에서 `black_before → white → black_after → air` 네 단계의 **진짜 F2 8장**. 요소당 2세션·16 PNG·정확 블록 서버 마커 16개, **드롭 아이템 제거 후 /execute unless entity @e[type=minecraft:item] 서버 확인 16개**.
- B8에서 확인된 **게임 아이템 드롭에 의한 화면 혼란**이 재현되지 않게 매 프레임 아이템 제거+서버 증명을 유지. RGB `ROI=[350,275,675,620]` 임계 24, 원본/수정 검정 A/A 반복, WHITE/AIR 음성대조, 시간 변화 및 원본 검정 의자 전경 밖 변화가 모두 0일 때만 제한적 화면 원인 인과 PASS 가능하다.
- 0px이면 오류 없이 **NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS**로 남기되 인과 PASS로 승격하지 않음. 음성대조/시간 변화가 0이 아니면 작업 실패, 실제 게임 증거 보류.

## 3. 새로운 재현 코드 및 GitHub CI

- `src/mcfr/int5_b17_hc_twelve_element_batch_f2.py`: 원본 B8 공식 JAR·월드 복구·두 Fabric 실게임 세션·드롭아이템 제거 검증 기반 선택형 12개 요소 실행기.
- `src/mcfr/runtime.py`: 기존 AF 월드와 완전히 분리된 `int5-b17-hc-twelve-batch-f2 --index 0~11` Handcrafted 원본 월드/캡처 경로.
- `tests/knowledge/test_int5_b17_hc_twelve_element_batch_f2.py`: 원본 12개 source·기하 격리·텍스처/부정대조·반증·권리 경계 **13개 회귀시험**.
- `.github/workflows/integration-int5-b17-hc-twelve-batch-f2.yml`: **한 워크플로의 12개 독립 매트릭스 작업, max-parallel 4**, 작업별 원본+수정 Minecraft 2회. 원본/임시 JAR은 업로드하지 않고 **해당 요소 F2·게임 로그·manifest·audit JSON**만 GitHub Actions 보존.
- 전체가 성공하면 **12요소 × 16장 F2 = 신규 192장**, 서버 상태 192건, 무아이템 서버 증명 192건, 단일 소스 패치 12개. 단 **완료된 수치로 조기 표현하지 않음**. 성공/실패/미검출은 각 job 원본·아티팩트 확인 후 집계할 것.

## 4. 범위 경계

- B16까지 한정 렌더 인과 19/45. 이번에 검증되는 요소만 개별적으로 추가하고, 앞선 쿠션 index12 성공을 중복 계산하지 않는다.
- 원본의 `LEG_OR_LOWER_POST`/`LOWER_FRAME`/`BACKREST_ASSEMBLY`/`SEAT_LAYER`는 본래 연구 소스의 **역할 가설**이다. 단일 요소 제거 후 이미지 변화는 **요소 → 게임 렌더 반응의 한정 인과**이며 원래 해당 GPU 면/UV의 독점 픽셀 소유권·실제 착석 기능·재질·스타일 확정이 아니다.
- 기존 **엄격 H03 HOLD / H05 CONDITIONAL / F70 무조건 PASS 0/70**, INT-5 최종 부품 의미 승인 0/45 및 INT-6 제삼자 AI 학습/재배포 권리 0 유지.
- 그다음 배치는 다른 게임 환경의 **Macaw 12요소 Minecraft Java 1.21.11 Fabric**, 그리고 AF 모델 두 종의 공통 5번 원본 요소 화면 미검출 원인이다.

**실게임 CI가 완료되기 전에는 신규 인과 PASS 개수와 픽셀 수치를 주장하지 않는다.**

## 5. B17 실제 12요소 배치 GitHub Actions 및 독립 바이트 재감사 최종 결과

[실제 Minecraft Java 1.21.1 Fabric B17 Actions #45629478921 — **12/12 독립 job SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45629478921). 검증한 실행 코드 커밋 `093396da5f598c03f991221de910cddfe9a48b14`. 각 요소마다 원본 공식 JAR 1회 + 오직 검정 의자 자식의 해당 요소만 제거한 임시 JAR 1회, 남북 4상태의 F2 각 8장. **총 24 게임 세션 / 신규 실제 PNG 192장 / 정확 블록상태 서버 192건 / 아이템 엔티티 0개 서버 확인 192건**. 각 작업 원본 모델부모/미수정 WHITE/모든 리소스 SHA·원본 ZIP CRC 검증.

| HC11210 원본 요소 | 소스 원본 면 | 남쪽 제거 화면 차이(px) | 북쪽 차이(px) | 엄격 한정 인과 판정 |
|---|---:|---:|---:|---|
| 0 | 6 | 0 | 628 | **PASS** |
| 1 | 6 | 774 | 268 | **PASS** |
| 2 | 6 | 600 | 339 | **PASS** |
| 3 | 6 | 0 | 0 | **화면 변화 미검출** |
| 4 | 6 | 0 | 0 | **화면 변화 미검출** |
| 5 | 6 | 0 | 468 | **PASS** |
| 6 | 6 | 303 | 230 | **PASS** |
| 7 | 6 | 790 | 252 | **PASS** |
| 8 | 6 | 0 | 610 | **PASS** |
| 9 | 6 | 888 | 729 | **PASS** |
| 10 | 6 | 934 | 697 | **PASS** |
| 11 | 6 | 1456 | 1144 | **PASS** |

**직접 재감사:** 새 Actions 아티팩트 ZIP **12개 전체를 실제로 다운로드**하여 ZIP CRC·중복 여부·원본 및 수정 네이티브 F2 **192개 이미지 개별 SHA256/1024×684**·원본/수정 두 게임 로그 SHA와 정확 서버 명령, drop-item 0개 서버 증명, WHITE/AIR/원본·수정 A/A 시간 변화·원래 의자 전경 밖 변화·RGB ROI 임계24 픽셀을 독립 Python 경로로 재계산. **12개 아티팩트 감사 결과와 전부 일치**. CI 12/12 성공은 **신규 인과 PASS 10개**와 **두 시점 효과 미검출 2개(3·4번)**를 혼동해서는 안 된다.

## 6. 원본 기하와 실제 화면을 교차 비교한 별도 발견

- HC source 3은 `from=[14,6,4] to=[14,9,13]`, HC source 4는 `from=[2,6,4] to=[2,9,13]`. 원본 source faces는 각 6면으로 기록되었으나 **두 요소 모두 X축 폭=0인 평면형 부품**이다. 공식 Minecraft 두 게임의 남북 F2에서는 둘 다 원본↔단독 제거 시 **0/0픽셀**.
- 같은 원본 역할 가설 `LOWER_FRAME`에 속하는 source 5는 `from=[4,6,1] to=[12,9,1]`: **Z축 폭=0인 평면**인데 **북쪽 468/남쪽 0픽셀** 단일요소 제거 응답. 따라서 원본 요소 면이 형성되는 축과 촬영 방향이 실제 변경 검출에 영향을 줄 가능성이 있다. **이 해석은 향후 동·서 카메라 F2 검증 전까지 기하 가설이며, 요소3·4를 불필요/버그/없음으로 확정하지 않는다.**
- source 6의 원본 `SEAT_LAYER` 후보 제거는 남303/북230픽셀: 검은 쿠션 자체 외곽이 아니라 주변 청록색 좌면 테두리에서 가시 변화가 관찰됨. source 7 `LEG_OR_LOWER_POST` 후보 제거는 남790/북252픽셀의 하부 한쪽 지지대 관련 화면 변화. 이는 원본 역할 가설의 시각적 양립 가능성을 보조할 뿐 실제 착석/하중 지지·재질·face별 GPU 픽셀 소유권이 승인됐다는 뜻은 아니다.

## 7. B17 완료 후 고정 45 요소 원장 진행도

| 원본 모델 | 소스 원본 요소/면 | 실제 단일 요소 렌더 인과 PASS | 화면 반응 미검출 | 실험 전 |
|---|---:|---:|---:|---:|
| AF121 기본 의자 | 10/46 | 9 | 1 | 0 |
| AF123 tucked 의자 | 10/46 | 9 | 1 | 0 |
| HC11210 쿠션 의자 | 13/78 | **11** | **2** | **0** |
| MACAW67 의자 | 12/59 | 0 | 0 | 12 |
| **합계** | **45/229** | **29** | **4** | **12** |

**새 인과 10/12, 누적 29/45=64.44%**. 역할 가설·원본 UV 출처 45/45/229면과는 서로 다른 기준. 남은 새로운 요소 실험은 Macaw `MACAW67/MACAW1424` 12개(별도 Java 1.21.11 Fabric 공식 JAR/시점 필요). 그리고 추가 동서 카메라 검증으로 HC source3·4, AF121/AF123 source5 화면 미검출 원인을 재시험해야 한다.

이번 턴 GitHub 영구 산출: `project/integration/INT5_B17_TWELVE_NATIVE_F2_FOUR_MODEL_AUDIT_V1.json` (12개 개별 아티팩트 ID/ZIP·원본·수정 로그 SHA, 원본 기하/역할, 한정 판정) 및 `project/integration/INT5_B17_FOUR_MODEL_45_ELEMENT_BATCH_STATUS_V1.csv` (45개 정확 원본 키, 역할, 실험 상태, 12개 신규 픽셀/경로, 다음 후보). **공식/modded JAR, 게임 텍스처, 외부 모델 JSON은 Git 커밋에 포함하지 않음**.

기존 엄격 **H03 HOLD / H05 CONDITIONAL / F70 무조건 PASS 0/70**, INT5 원본 요소 독점 GPU 픽셀 귀속 0, 부품 물리 기능·재질·스타일 최종 의미 승인 0/45, INT6 AI 학습/재배포 권리 승인 0 **유지**.
