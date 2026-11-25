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
