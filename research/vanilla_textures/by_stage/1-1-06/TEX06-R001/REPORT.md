# 1-1-06 도기·유광도기 — TEX06-R001 신규 원본 검증

2026-11-13 · 연구 대상 **8종 고정**, 전체 공식 체크포인트 **v38 불변**. 본 신규 결과는 **Minecraft Java 1.21.11 비공식 자산 추출 미러**에 대한 원본 PNG 바이너리/정적 JSON 실검사이며 **Mojang 공식 인증이 아님**.

## A — 기존 기록·대조
`STATE.json`, v4 실측 CSV와 150개 번호 원장의 정확한 8개 item_id/path/SHA를 일치 대조. 기존 v4 기록 8/8은 **레거시 기록**이고, 아래 8/8 실측은 별도 신규 검증이다. v35–v38 대표 파일 5개에서 `terracotta` 문자열 일치 0건(선택한 파일만 해당); 타 분류 누적 실적을 전용 단계에 추가하지 않았다. 상세 `HISTORICAL_CROSSWALK.json`.

## B — 원본 PNG 8종, SHA 및 CRC
GitHub `InventivetalentDev/minecraft-assets`의 annotated tag `1.21.11`가 가리키는 **commit `7241a12cc2707abd7022f399c5d9033153e492e1`**에서 8 PNG를 base64로 가져와 **실제 바이너리 복원**. 로컬 SHA-256 재계산, Pillow `verify()`와 RGBA 디코딩, PNG 각 IHDR/PLTE(있는 경우)/IDAT/IEND의 **CRC32 개별 재검사**를 수행. 모든 파일이 **v4 SHA와 8/8 일치**, PNG 유효성·CRC 모두 통과. 16×16×8 = **2,048개 픽셀**, 전부 알파 255. 파일별 sha, Git blob SHA, 출처 `SOURCE_LEDGER.csv` 및 CRC `PNG_INTEGRITY.csv` 참조. Git blob SHA / PNG SHA256 / Mojang client.jar 인증은 다른 개념이다.

## C — RGBA·명도·반복 계측
모든 픽셀의 RGB 고유색/상위색/평균채널값·알파·명도를 계산. 명도=`0.2126R+0.7152G+0.0722B` (8-bit sRGB 코드값의 BT.709 가중치; 실제 선형 광학 값 아님). 인접 수평/수직 평균 절대차 및 좌우·상하 경계 RGB 채널 MAE를 직접 계산. `PIXEL_MEASUREMENTS.csv`의 새로운 계측 결과:

| ID | 고유 RGB | 평균 명도 | 명도 표준편차 | 좌우 이음 MAE | 상하 이음 MAE |
|---|---:|---:|---:|---:|---:|
| `terracotta` | 5 | 104.47 | 1.54 | 1.21 | 1.13 |
| `white_terracotta` | 52 | 183.55 | 2.25 | 1.56 | 1.52 |
| `orange_terracotta` | 68 | 97.06 | 2.13 | 1.88 | 1.56 |
| `blue_terracotta` | 45 | 65.06 | 1.45 | 1.10 | 1.02 |
| `green_terracotta` | 47 | 78.78 | 1.37 | 1.08 | 1.02 |
| `yellow_terracotta` | 70 | 137.38 | 2.24 | 1.71 | 1.56 |
| `black_glazed_terracotta` | 19 | 38.21 | 18.78 | 33.13 | 39.48 |
| `white_glazed_terracotta` | 13 | 206.70 | 52.82 | 56.08 | 55.98 |

## D1 — 테라코타/유광 비교
일반 6종의 명도 표준편차 범위 **1.37~2.25**, 유광 검정 **18.78**, 유광 흰색 **52.82**. 유광 둘은 일반보다 적은 고유색(검정 19, 흰색 13)을 쓰면서도 더 강한 밝기 대비를 그림에 표현한다. 이것은 **2D 색/패턴** 특성이고 PBR 광택 반사 검증이 아니다.

## D2 — 유광 회전·무늬 이어붙이기
미러 PNG 2종을 이미지 평면에서 시계방향 0/90/180/270° 회전, 각 2×2 조합 **4^4=256개 전수 비교**. 네 이음의 RGB 채널 MAE 평균 최소:
- 검정: 원본 4개 무회전 **36.302084**, 최적 **4.770833**, 시계방향 `[180,270,90,0]`(좌상·우상·좌하·우하).
- 흰색: 무회전 **56.03125**, 최적 **2.145833**, `[0,90,270,180]`.
두 경우 최적 해의 네 경계 오차가 각각 동일하고 단일 최적 회전 조합이었다. 이웃 색상 정합성은 **게임 안의 모티프 연결 의도, 블록 상태 방향, 실제 화면과 동등하다는 인증이 아니다**. 계산 방법/원본 수치 `GLAZED_2X2_ROTATION_ANALYSIS.json`.

## D3 / E — 실제 정적 모델 JSON / UV / 블록 상태
미러에서 8종 각각 리프 `assets/minecraft/models/block/<texture_id>.json`, 블록 상태 `assets/minecraft/blockstates/<texture_id>.json`을 직접 조회, Git SHA 기록. 추가 부모 `cube_all`, `cube`, `template_glazed_terracotta` 정적 JSON 검토. `STATIC_MODEL_LINKS.json` 및 `UV_FACE_ROTATIONS.csv`.
- 일반 6종: `cube_all`의 `all` 슬롯 → 각 해당 PNG, `cube` 6면으로 상속, 블록 상태 `variants[""]` 한 종류.
- 유광 2종: `template_glazed_terracotta`의 `pattern` 슬롯 → 해당 PNG; 모든 면 UV **[0,0,16,16]**, 면 UV 회전 **up/down=0, north=90, south=270, west=0, east=180°**.
- 두 유광의 상태 회전: **facing=south→y0, west→y90, north→y180, east→y270**(게임 렌더 세계 방향 재현과 구별).
- **블록 모델 Y축 회전**과 **개별 면 UV 회전**은 서로 다른 두 층의 변환이다. 원본 JSON의 정적 선언은 확인했으나 실제 게임의 UV 투영·상단 패턴 방향은 **미검증**.

## F — 공식 Mojang 인증 및 인게임 정적 검사 (미완료)
공식 Mojang Java 1.21.11 `client.jar` 확보·공식 체크섬 인증·8종 비교 **0/8**. 실제 게임 장면에서 유광 4방향·6면 UV/라이팅 관찰 **0/8**. PNG 미러 SHA 검증을 공식 인증으로 승격하지 않았다. 애니메이션·키프레임·동작 조사 중단을 유지한다.

## G — 결과·독립 이력 저장
이 릴리스는 **A–E의 소스 근거 8/8**, F **0/8**, 완전한 공식 및 인게임 종합 인증 **0/8**. 결과 파일 9개와 본 단계 `STATE.json`·`HANDOFF.md`만 갱신. 타 범주·루트 인수인계·과거 연구 v38 데이터는 보존.

**다음 고유 버전 `TEX06-R002`**: 공식 `client.jar` 파일의 인증과 그 내부 PNG/JSON 추출을 8개 비교하고, 실제 게임 정적 장면에서 Facing별 UV 방향을 검증한다. 신규 검증 없이는 버전을 올리지 않는다.
