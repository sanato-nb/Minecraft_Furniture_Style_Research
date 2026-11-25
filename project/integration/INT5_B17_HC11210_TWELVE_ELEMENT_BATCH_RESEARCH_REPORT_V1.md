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
