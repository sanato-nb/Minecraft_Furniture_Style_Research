# INT-5-B18 — Macaw 가구 원본 12요소 전체 다중 실게임 실험

기준: 2026-11-25 KST. 직계 [B17 Draft PR #129](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/129) HEAD `e10e59f23443ace1d9ab2448a61067d81cb1de44`. 기존 원본 Git `main`은 병합하지 않음.

## 1. 실제 작업 범위

B17까지 원본 45개 요소/229 faces 중 **실게임 단일 요소 제거→렌더 응답 인과 PASS 29/45**, 실제 화면 변화 미검출 4개, 미실험 12개. 이번 B18은 남아 있는 **Macaw MACAW67/MACAW1424의 0~11번 12개 요소** 전부를 **한 PR/하나의 CI 매트릭스**에서 처리한다.

| 원본 인덱스 | faces | B3 역할 가설(실물 기능 승인 아님) |
|---|---:|---|
| 0 | 5 | SEAT_LAYER |
| 1 | 4 | BACKREST_ASSEMBLY |
| 2·3·4·5 | 각 5 | LEG_OR_LOWER_POST |
| 6·7·8 | 각 5 | BACKREST_ASSEMBLY |
| 9 | 4 | BACKREST_ASSEMBLY |
| 10 | 5 | BACKREST_ASSEMBLY |
| 11 | 6 | SEAT_LAYER |

각 original source ID는 B3 고정 45요소 CSV 및 B17 45요소 상태 CSV의 `NOT_YET_TESTED`와 연결하고, 기존 B5~B17의 다른 모델을 중복 성공으로 집계하지 않는다.

## 2. 공식 원본 및 실제 개입 절차

- **Minecraft Java 1.21.11 Fabric**, 공식 Macaw's Furniture **3.4.2** 출시 JAR `mcw-furniture-3.4.2-mc1.21.11fabric.jar`, SHA-256 `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e`.
- 대상 원본 블록상태 `mcwfurnitures:acacia_chair[facing=north]`, 원본 `facing=north` 모델 선택 `mcwfurnitures:block/chair/acacia_chair` / y=90 고정. 블록상태 SHA-256 `e6405186a33100104cb6dcbddd2cad774f157298cafe8e750dc228cd9ba24b95`.
- 원본 child `assets/mcwfurnitures/models/block/chair/acacia_chair.json` SHA-256 `f0aeb2ad025179dfd68c63b3c2ea5a25ab8d4a7e3e161dc43f270772672bda3b`, parent `assets/mcwfurnitures/models/block/parent/chair.json` SHA-256 `26f389f8cc286dcdd97a608adf685294bcc2f60323e7b1ea40755b2110ff1650`. **공식 출시판에서 동일 바이트 SHA가 확인될 때만 실제 변형**.
- original parent **12요소/59 faces**. 한 CI job은 **정확 한 요소만 제외한 11요소·(59−해당 faces)**를 선택 child JSON 하나에 임시 오버라이드한다. parent·blockstates·제삼자 텍스처·다른 모든 JAR 멤버는 ZIP CRC 및 압축 해제 바이트 비교.
- 원본 Minecraft 클라이언트 1회, 같은 pristine world로 복귀한 수정 클라이언트 1회, 공식 blockstate를 실제 서버에 설치·읽기 검증.
- 남/북 카메라 `chair_before → minecraft:oak_stairs[facing=north] (원본 미수정 vanilla 음성대조) → chair_after → AIR` 각각 F2 **8장 × 두 독립 게임**, 총 **요소마다 진짜 F2 16장**. 원본 변형 A/A 반복, vanilla 계단/AIR, 시간 drift, 원래 의자 전경 밖 변화가 모두 0일 때만 bounded PASS.
- 화면 0픽셀 변화는 **NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_CONTROLS**로 보존; 음성대조 오류/불일치는 조건부 및 CI 실패. 현재 테스트하지 않은 원본 요소를 PASS로 승격 금지.

## 3. 구현 및 검수

- `src/mcfr/int5_b18_macaw_twelve_element_batch_f2.py`: 공식 Macaw 3.4.2 모델 12요소 단독 제거, pristine 원본/변형 2클라이언트, 정확 서버 상태와 실제 PNG SHA/픽셀 독립 감사.
- `src/mcfr/runtime.py`: 전용 `int5-b18-macaw-twelve-batch-f2 --index 0~11` 명령, Minecraft 1.21.11 전용 단일 `MACAW67_north` 월드 구성.
- `tests/knowledge/test_int5_b18_macaw_twelve_element_batch_f2.py`: 12개 정적·변형·음성대조·부정 회귀시험.
- `.github/workflows/integration-int5-b18-macaw-twelve-batch-f2.yml`: 12개 job, 병렬 max 4, 각 job 공식/변형 Minecraft 실제 세션 2회. 전원 PASS 시 신규 F2 **최대 192장**, 정확 서버 상태 **최대 192건**; 목표이지 자동 완료 수치가 아님.
- 임시 변경 JAR/원본 PNG 리소스/모델 JSON은 Git 커밋·CI 아티팩트에 포함하지 않고, 실제 자체 F2와 SHA/스크린 감사만 아티팩트로 보존한다.

## 4. 승인 경계와 후속 작업

B17 인과 PASS **29/45**, 미검출 **4**, 새 Macaw 미실험 **12**. 새 실게임 결과가 확정되기 전에는 29/45에서 올리지 않는다. 화면 변화 픽셀은 원본 source 제거로 생긴 한정 응답이지 정확 GPU face-UV 픽셀 독점 귀속이나 실물 착석 기능·재질·스타일 증명이 아니다. 기존 엄격 **H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70**, INT5 최종 의미 승인 0/45 및 INT6 학습·재배포 권리 승인 0 유지.

이전 두 AF 의자 index5, HC index3/4 등 기존 **4개 미검출**은 향후 원본 가구 전체 동/서 카메라의 독립 재검증 대상으로 보존한다.

## 5. B18 실제 원본 12요소/59면 게임 두 클라이언트 검증 — 최종 결과

[**실제 Macaw B18 GitHub Actions #45638195899**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45638195899) 매트릭스 **12/12 job SUCCESS**, 실험 코드 SHA `ebba1a84b35d8162c40ddc648260652e02f51074`. 공식 Macaw 3.4.2 + Minecraft Java **1.21.11 Fabric**에서 original JAR/원본 부모·자식·블록상태 SHA(연구 original과 바이트 동일) 확인 후 **오직 선택 source 요소 1개**만 제거한 검증용 child 오버라이드를 12번 **서로 독립된 임시 JAR**으로 실행하였다. 각 job 공식 원본 게임+변형 게임 **2세션**, 합계 **24개 독립 클라이언트/신규 실제 F2 192장/정확 서버 상태 192건**.

| Macaw 원본 요소 | 원본 faces | 남쪽 화면 변화(px) | 북쪽 변화(px) | 판정 |
|---|---:|---:|---:|---|
| 0 | 5 | 664 | 890 | **범위 한정 PASS** |
| 1 | 4 | 440 | 266 | **범위 한정 PASS** |
| 2 | 5 | 284 | 10 | **범위 한정 PASS** |
| 3 | 5 | 12 | 194 | **범위 한정 PASS** |
| 4 | 5 | 284 | 10 | **범위 한정 PASS** |
| 5 | 5 | 12 | 193 | **범위 한정 PASS** |
| 6 | 5 | 179 | 117 | **범위 한정 PASS** |
| 7 | 5 | 415 | 263 | **범위 한정 PASS** |
| 8 | 5 | 378 | 254 | **범위 한정 PASS** |
| 9 | 4 | 440 | 288 | **범위 한정 PASS** |
| 10 | 5 | 128 | 109 | **범위 한정 PASS** |
| 11 | 6 | 570 | 522 | **범위 한정 PASS** |

실험의 **12개 ZIP 전부 다운로드·독립 Python 경로로 재검증**: 각각 ZIP CRC, 정확 F2 16장 SHA-256/1024×684 해상도, 원본/수정 두 게임 client.log SHA 및 실제 `[RenderAudit]` 서버 마커, `ROI=(350,275,675,620)` 채널차 24픽셀, 모델 전경 밖 변화, 변형 전후 원본 의자 A/A, 미수정 vanilla oak stairs 및 AIR 대조군을 다시 계산하였다. **192개 원본 PNG 해시와 각 12개 pixel delta/음성대조 모두 저장된 감사 JSON 및 Actions 원본과 일치**, 대조/전경 밖/시간변화는 전부 0. **새로운 B18 12개 모두 한정 인과 PASS, 화면 미검출 Macaw 0개**.

### 원본 학습 증거를 보강한 두 가지 추가 관찰

1. 공식 Macaw 3.4.2의 `assets/mcwfurnitures/models/block/parent/chair.json` SHA256 `26f389f8cc286dcdd97a608adf685294bcc2f60323e7b1ea40755b2110ff1650`와 child SHA `f0aeb2ad025179dfd68c63b3c2ea5a25ab8d4a7e3e161dc43f270772672bda3b`의 **연구 원본↔실제 실행 공식 release byte 동일**을 B18 전체 job에서 직접 확인했다. 이전 B2 원장의 `model_parent_json_byte_identity_in_runtime=NOT_VERIFIED`를 임의 수정하지 않고 **후속 검증 증거로 층별 기록**한다.
2. Source index2와 index4는 남284/북10px로 **변화량이 우연히 동일하지만 변경 픽셀 위치 교집합 0px**. index3와 index5 역시 남12/12px·북194/193px이나 **두 시점 모두 서로 다른 위치(교집합 0px)**. 대칭 기하의 별도 개입을 구별했으며, 화면 변경 전부를 해당 원본 face가 독점한다는 주장은 하지 않는다. Macaw source index0 제거는 사진에서 주황색 좌면 판이 사라지는 국소 변화를 눈으로도 확인했다. 이는 기하/원본 텍스처 역할 가설과 양립하지만 실제 착석·재질 역할 승인은 아니다.

### 첫 실패/재실행 기록

[최초 CI #45637854461](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45637854461)는 새 음성 회귀시험 두 건이 `override_child` 인자를 잘못 호출하는 단위시험 오류로 실게임 이전 실패. 2개 테스트 호출 인자만 정확히 수정해 [최종 #45638195899](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45638195899)에서 **12/12 실제 Minecraft 검사 SUCCESS**. 실패가 실게임 검증 성공으로 집계된 적은 없다.

## 6. 45원본 부품 분모 유지: 인과 검증 완료 범위 / 미승인 구분

| 원본 모델 | 원본 요소·면 | 실게임 단일요소 렌더 인과 PASS | 두 시점 효과 미검출 | 미실험 |
|---|---:|---:|---:|---:|
| AF121 기본 의자 | 10 / 46 | 9 | 1 | 0 |
| AF123 tucked 의자 | 10 / 46 | 9 | 1 | 0 |
| HC11210 검정 쿠션 의자 | 13 / 78 | 11 | 2 | 0 |
| MACAW67 의자 | 12 / 59 | **12** | 0 | **0** |
| **합계** | **45 / 229** | **41** | **4** | **0** |

**전체 요소를 단일 개입 방식으로 각각 한 번 이상 연구한 범위 45/45(100%), 그중 실제 두 시점 한정 인과 PASS 41/45(91.11%), 미검출 4/45.** 모델 종류·상태·카메라·JAR 버전에 종속된 결과로서 **INT5 부품 기능·재질·스타일 최종 의미 승인 0/45, 배타적 원본 GPU face/UV 픽셀 대응 승인 0/45, INT6 제삼자 모델/텍스처 AI 학습·재배포 권리 승인 0**이다. 기존 엄격 H03 HOLD/H05 CONDITIONAL/F70 무조건 승인 0/70을 그대로 유지한다.

다음 별도 배치: 미검출 4개 `AF121/AF1393/5`, `AF123/AF1394/5`, `HC11210/HC13/3`, `HC11210/HC13/4`에 대해 공식 원본의 **동·서 카메라 추가 및 source face 방향·가림을 확인**할 것. 기존 남북 0픽셀을 '불필요 요소'나 '버그 확정'으로 해석하지 않는다.

**영구 산출:** `project/integration/INT5_B18_MACAW12_REAL_F2_FOUR_MODEL_AUDIT_V1.json`(각 12 source/원본 좌표·192장 실제 F2 결과·ZIP/로그 SHA와 artifact ID·정확 범위), `project/integration/INT5_B18_FOUR_MODEL_45_ELEMENT_BATCH_STATUS_V1.csv`(원본 45행 개별 상태/실험 범위). 원본 제삼자 JAR/텍스처·수정 모델 JSON은 Git 아티팩트에 포함하지 않았다.
