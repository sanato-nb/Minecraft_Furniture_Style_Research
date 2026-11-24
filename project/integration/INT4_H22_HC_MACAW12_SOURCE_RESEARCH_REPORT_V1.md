# INT-4 H22 — Handcrafted·Macaw 역사 12개 모델 원본 및 기존 F2 출처 정합

## 목표와 원본
부모 H21 Draft #103 head 08472c8a149edee0cfbee6fe9cdff7f1b4e33e63. F70 별도 모델링 V3의 조건부 역사 모델 12개를 해소한다.
- HC 5건: 연구 Git 8d21d1665916850c3fa3bdaf1370c50ec2ca7035, 공식 Fabric 4.0.3 JAR SHA1 a9579fecd7ed429c282be21d5c921d220197acc6.
- Macaw 7건: 역사 연구 및 실제 실행본 동일 공식 Fabric 3.4.2 JAR SHA1 28f0929b6005bc28b1bde475579c13020420ae9f / SHA256 e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e. 별도 두 버전 비교라고 주장하지 않는다.
- 공식 Minecraft 1.21.1 / 1.21.11 client JAR SHA1 각각 30c73b1c5da787909b2f73340419fdf13b9def88 / ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd.

## 실제 검증
[Actions #45339071003](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45339071003)에서 원본 ZIP/JAR CRC·SHA와 기존 Git 원장 blob을 고정하고, 선택 rule/option, 회전·uvlock·weight, 전체 상속, geometry provider, 면별 UV/texture/cullface/tintindex 및 원본 PNG 해시를 대조했다. 6/6 회귀시험. HC 선택 JSON 13개/PNG 6개, Macaw JSON 18개/PNG 6개 검증 (cohort별 공용 자산 포함). 기존 F2 및 서버 상태 원본 검증 기록을 재사용하며 신규 게임/F2/육안 관찰 0.

| 사례 | 모델 요소 | 면 | 기존 정확 상태 F2 run |
|---|---:|---:|---:|
| S16 HC single table | 10 | 60 | 44986580186 |
| S17 HC center table | 2 | 12 | 44986580186 |
| S18 Macaw single table | 6 | 31 | 44923726837 |
| S19 Macaw center table | 1 | 6 | 44923726837 |
| S28 Macaw bookshelf base | 10 | 31 | 44923726837 |
| S29 Macaw bookshelf middle | 8 | 19 | 44923726837 |
| S38 HC head cushion | 1 | 6 | 44929863978 |
| S39 HC counter type1 | 2 | 12 | 44986580186 |
| S40 HC counter type2 | 2 | 12 | 44986580186 |
| S41 Macaw counter | 2 | 11 | 44920889453 |
| S42 Macaw dry sink | 16 | 55 | 44920889453 |
| S43 Macaw filled sink | 17 | 56 | 44920889453 |
| 총합 | 77 | 311 | 12 사례 |

311면: STATIC_RECT 286 / ZERO_UV_AREA 24 / ANIMATED_FRAME_RECTS 1. S16/S17의 0면적 UV는 역사 원본 선언대로 보존. S38은 독립 head cushion이며 같은 카메라 air 대비 465 픽셀 차이 기존 증거로 한정. 실제 전체 침대 자연 설치를 새로 승인하지 않는다.

## R06 다음 작업의 직접 원본 근거
S43 원본 element 1의 up 면은 UV [1,2,13,11], rotation 0. texture assets/mcwfurnitures/textures/block/water_still.png 16x512, 기존 프레임 32행, mcmeta animation frametime 2. PNG SHA256 d5d63ddd36311d6b064123750715fe551fbeccb5cb1f677ef93027e9305791de, mcmeta SHA256 e9b8025fde1b09b0a4d2a38427b04f98f28a593045be6d177eb2b29164c872b0. 원본 애니메이션 선언을 확인했지만 기존 R06 시간별 F2 변화가 정확히 이 애니메이션 때문인지 계측하지 않았다. R06은 조건부 유지한다.

## V4 모델링 승인 범위
역사 모델 62/62 PASS; 위험 질문 7/8 PASS, R06만 조건부. 합산 서로 다른 검토 단위 69/70 (98.6%), 보류 0. V3의 12개 HC/Macaw 행에서 모델링 상태/사유/증거/후속만 변경; 나머지 58행 및 기존 엄격 승인 유지. H03 HOLD / H05 CONDITIONAL / F70 무조건 0/70 / INT5·INT6 0. 새 GPU·프레임 인과나 전체 기능/권리 승인 없음.

산출: INT4_H22_HC_MACAW12_SOURCE_RESULT_V1.json, INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V4.csv, INT4_F70_MODELING_CONTRACT_SUMMARY_V4.json, 감사기·회귀시험·V4 delta 검산·Actions. [파생 아티팩트 #14894688210](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45339071003/artifacts/14894688210). 원본 자산은 커밋하지 않음. main 미병합.
