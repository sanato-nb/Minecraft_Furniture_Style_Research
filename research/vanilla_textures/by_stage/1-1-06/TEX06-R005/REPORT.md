# TEX06-R005 — 도기·유광도기: PNG 원본 픽셀 좌표와 UV 패널 대응

- 일자: **2026-11-13**. 이 채팅은 **1-1-06만** 연구한다. 마지막 확정 R004 이후 새 원본 위치별 RGB 증거를 작성. 공통 역사 체크포인트 **v38 불변**.
- 우선 1차 자료: 사용자가 GitHub에 제공한 `1.21.11/assets/minecraft/` (Java 1.21.11 JAR 압축 해제본).
- **기존 PNG 2개를 이번에 다시 직접 읽어 디코딩**: 검정 유광 `black_glazed_terracotta.png` 284 bytes, SHA-256 `214ce8ca46c60a42b8863655b3895aca839c7ef7cfa511a192dc1974a0ca2758`, Git blob `58832984e6700a295c890ab86b568929d36567d5`; 흰색 유광 `white_glazed_terracotta.png` 231 bytes, SHA-256 `cb1ebf9f3f3e93009ff4cab1b2b2b70d41fd87caa40c71942ae51996d12498b4`, Git blob `a500a876f14d6fab28d140023d32436f28f2512e`. 두 16×16 PNG 모두 IHDR/PLTE/IDAT/IEND CRC 검사 통과, 기존 R003 PNG SHA 값과 일치.
- **고유 텍스처 추가 0개**. R003의 기존 8/8 소스 검증 유지. 나머지 6개 PNG를 이번에 다시 검증했다고 주장하지 않는다.

## 신규 위치별 근거

이전 R002는 유광의 2×2 조합 512개 가설과 64개 이음쌍의 집계 자료를 제공했으며, R004는 원본 48면 매핑과 64개 facing 재색인을 제공했다. R005의 **새로운 자료는 그 가설을 실제 PNG의 개별 좌표로 역추적한 256행**이다. 각 행에는 두 경계의 회전된 화면 위치, 실제 원본 PNG 좌표(0..15), RGBA, 픽셀 RGB L1 차이를 적었다. 재검사로 만든 위치별 레코드이되, 앞선 원본 픽셀 측정을 새로운 고유 텍셀 256개로 중복 가산하지 않는다.

| 패널 | TL / TR / BL / BR facing | RGB L1 합계 | 3채널 RGB MAE | 같은 RGB 쌍 |
|---|---|---:|---:|---:|
| black_A_right_hand | north / west / east / south | 916 | 4.770833 | 28 / 64 |
| black_B_opposite_projection | north / east / west / south | 4474 | 23.302083 | 8 / 64 |
| white_A_right_hand | south / east / west / north | 412 | 2.145833 | 44 / 64 |
| white_B_opposite_projection | south / west / east / north | 17174 | 89.447917 | 14 / 64 |

이 수치는 이번에 원본 PNG 위치별 RGB에서 재계산했을 때 기존 R002 집계와 **정확하게 일치**했다. 검정 A의 불일치 36/64, 흰색 A의 불일치 20/64이므로 A가 무결점 타일링이라는 뜻은 아니다. 검정·흰색 각각 A/B 두 배치에서 참조한 원본 좌표는 **서로 다른 60개**이며 비교행 수 256과 구분한다.

## 모델·상태·UV와 픽셀 좌표 연결

사용자 `1.21.11/assets/minecraft/models/block/template_glazed_terracotta.json`의 `elements`는 0→16 큐브이고 6개 face 모두 원본 UV `[0,0,16,16]`. up/down은 face rotation 기본 0°, north 90°, south 270°, west 0°, east 180°. `#pattern` 슬롯은 두 유광 모델이 각각 자기 PNG로 지정한다. blockstates는 **south=0°, west=90°, north=180°, east=270°** 모델 y 회전. 두 item JSON은 `minecraft:block/<texture_id>` 모델을 참조하되 facing 상태를 직접 부여하지 않는다. 이 사실은 R004에서 이미 확인된 내용으로 계승만 한다.

이번 **40행** `SOURCE_UV_TOP_CORNERS.csv`에는 2개 PNG × (회전하지 않은 **아이템 모델 공간** 4코너 + 설치 모델의 **4 facing 조건부** 상단 코너 16개)의 원본 (x,y)와 RGBA를 기록했다. 이것은 아이템 인벤토리 화면이나 손에 든 모습의 게임 실제 투영을 관찰한 것이 아니다.

상단 기준이 북쪽(-Z) 위인 소스 투영 가정에서는 `image CW=(360-model_y)%360` (R004 조건부 가설). 회전 후 샘플 (x,y)의 원본 PNG 좌표는 0°=(x,y), 90°=(y,15-x), 180°=(15-x,15-y), 270°=(15-y,x). 수평 경계에서 왼쪽 블록 (15,i)와 오른쪽 블록 (0,i), 수직 경계에서 위 블록 (i,15)과 아래 블록 (i,0)을 16개씩 비교했다. **UV 원본 회전 0°와 모델의 상태 y 회전은 다른 개념**이다. A와 B 중 어느 것이 인게임 실제 정적 렌더 방향인지는 별도 스크린샷·실측이 필요하다.

## 추가 파일·계승 범위

- `TOP_SEAM_PIXEL_COORDS.csv`: 새 **256행** 위치별 RGB/원본 좌표 근거.
- `SOURCE_UV_TOP_CORNERS.csv`: 새 **40행** 아이템 모델 공간/배치 모델 조건부 상단 UV-화소 대응.
- `PANEL_PIXEL_METRICS.csv`: 위 네 패널의 재검산 요약.
- `SUMMARY.json`: 과거 계승 vs 이번 신규 분석 구분, SHA와 한계.
- `REPRODUCE_TOP_PIXEL_AUDIT.py`: 저장소 루트에서 사용자 PNG 두 파일을 직접 읽어 SHA/PNG CRC와 동일 패널 집계를 재현 (Pillow 필요).
- **계승(신규 가산 금지)**: R001 8 PNG / 2,048 픽셀, R002 512 회전 가설/64개 경계 집계, R003 8개 PNG·모델·상태 검증, R004 8 item JSON, 48면 법선 대응 및 64 facing LUT.

## 한계·완료 판정

**인게임 정적 렌더 0/8**. Minecraft 실행, 정적 스크린샷, 아이템 화면/측면의 인게임 UV 관찰 없음. 48면 원본 UV 매핑만으로 게임 렌더러의 실제 보이는 방향을 인증하지 않음. 광택을 PBR 실제 반사라고 판정하지 않음. 사용자 지시에 따라 **Mojang 공식 압축 client.jar 전체 SHA-1 검증은 필수 분모에서 제외**하되, 공식 인증 성공으로 간주하지 않는다. 애니메이션 보류; PZ 변환이나 가구 3D 모델 제작 진행하지 않음.
