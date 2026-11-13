# TEX09-R001 — 토양·지면 9종 직접 미러 PNG + 정적 JSON/UV 교차 검증

검사일: 2026-11-13 (Asia/Seoul). 범위: **1-1-09 9개만**. 전역 기준 **v38 유지**, 애니메이션 전면 보류. 연구 유형: **정적 미러 자료 직접 바이너리/소스 검사**이며 **Mojang 공식 client.jar / 인게임 검증 아님**.

## A 출처·기존 증거 교차 확인
- `STATE.json`의 9개 `texture_id`, 경로, v4 SHA-256을 v4 `01_누적150종_픽셀측정.csv` 및 고정번호 원장과 대조했다: 9/9 정확히 일치.
- v4 행의 `evidence_type=mirror_png_pixel_measurement`, `official_client_jar_unverified`를 재확인. v4 9건은 **이전 분석**이며 이번 신규 표본 수에 더하지 않는다.
- `research/vanilla_models/v35..v38`의 문서 및 v35의 544개 모델 목록, v36 544개 히스토리 SHA 대조표를 검사. 1-1-09의 9개 `texture_id`를 다룬 동일 행은 없고, v37은 화로/훈연기/용광로, v38은 오크 선반 정적 검증을 다루므로 **타 분류 검증 수량을 계승하지 않음**. 이것은 저장소 모든 구버전의 전체 부재 증명이 아니다.

## B PNG 바이너리 / SHA / 청크 검사
- 소스: 공개 비공식 미러 `InventivetalentDev/minecraft-assets`, ref=`1.21.11`, `assets/minecraft/textures/block/*.png`. GitHub에서 각 PNG 바이너리를 base64로 수신해 Python `base64.b64decode` 처리, 바이트 전체 SHA-256 직접 계산. 또한 Git blob SHA-1 = SHA1(`blob ${bytes}\\0` + bytes) 검산.
- 9/9 바이트 SHA-256이 기록된 v4 값과 같음; 9/9 Git blob SHA1도 connector가 반환한 blob과 일치함.
- PNG signature, 청크별 CRC32, IEND 이후 잔여 byte 없음, Pillow `Image.verify`, RGBA 디코드 9/9 통과. 9/9 모두 16×16; 합계 **2304픽셀**, 2304/2304 완전 불투명(알파 255). 원본 PNG 바이트 합계 ${bytes.reduce((a,b)=>a+b,0)}.
- 이는 미러 바이트 검증. **공식 Minecraft client.jar와 바이트 대조하지 않음.**

## C RGBA·명도·색상·반복
- `PIXEL_METRICS.csv`는 별도로 재계산한 값. 평균 명도 `Y=0.2126R+0.7152G+0.0722B`, 모집단 표준편차 사용. `mean_h/v_adjacent_rgb_abs_channel`은 채널별 이웃 화소 절대차 평균. 이 값은 legacy v4 측정과 **동일하게** 재현되었음(9/9).
- 좌우/상하 seam은 **양 끝 열·행 사이 BT.709 명도 절대차 평균**이고, legacy v4의 RGB 계열 이음새 지표와 **정의가 다르므로 수치를 동일 개념으로 비교하면 안 됨**. FFT 고주파는 DC 제거 후 `(|fx|>=0.25 or |fy|>=0.25)` 위치의 에너지 비율. 16×16 작은 표본의 설명 지표일 뿐 실제 렌더 품질 인증이 아님.

| PNG | 밝기 평균 Y | Y 표준편차 | 좌우 이음새 Y | 상하 이음새 Y | 고주파 비율 |
|---|---:|---:|---:|---:|---:|
| `dirt` | 102.2505 | 22.8493 | 27.7213 | 26.1219 | 0.8853 |
| `coarse_dirt` | 90.9049 | 25.626 | 26.9611 | 34.5865 | 0.878 |
| `rooted_dirt` | 110.2279 | 26.1103 | 24.5719 | 32.6163 | 0.7614 |
| `mud` | 58.2706 | 6.999 | 4.8107 | 5.4805 | 0.6005 |
| `packed_mud` | 112.392 | 10.4999 | 9.3575 | 9.4731 | 0.8185 |
| `mud_bricks` | 109.0848 | 17.3264 | 10.5453 | 42.5794 | 0.4847 |
| `gravel` | 128.3427 | 17.0423 | 13.8381 | 15.474 | 0.7854 |
| `grass_block_top` | 147.4336 | 17.7023 | 21.25 | 19.6875 | 0.8818 |
| `podzol_top` | 66.473 | 12.634 | 10.8094 | 8.6572 | 0.6723 |

## D 재질 특화 결론
**D1**: `mud`는 Y=58.2706으로 이 집합에서 가장 어둡고 표준편차=6.999로 저대비. `grass_block_top`의 grayscale 원본 Y=147.4336이 가장 밝지만 틴트 전 값. `dirt` Y=102.2505, `coarse_dirt` 90.9049, `rooted_dirt` 110.2279은 흙 계열에서 명도 및 색상 종류가 다름. `gravel` Y=128.3427, `podzol_top` Y=66.473.

**D2**: `mud_bricks`는 상하 seam Y=42.5794, 좌우 10.5453으로 방향 비대칭이 큼. 이는 벽돌 줄눈의 고정 행 경계와 연결되며 좌우가 ‘완전 무봉합’이라는 뜻은 아님. `coarse_dirt` 상하=34.5865, `rooted_dirt` 상하=32.6163도 반복 접합 차이가 큼. 같은 PNG를 2×2로 배열한 이미지를 시각 확인했으나, 실제 게임의 블록 상태 회전 및 이웃 조명은 미검증.

**D3**: `grass_block_top.png`는 원본 `L` 모드로 디코드되며 RGB=(gray,gray,gray), 66종 grayscale. `models/block/grass_block.json`의 **up face `tintindex:0`** 및 측면 overlay의 tintindex=0을 직접 확인. 따라서 PNG의 밝기 147.4336을 ‘인게임 초록색’의 실제 RGB로 표기하면 오류. `podzol_top.png`는 갈색 원본이며, 정상 `podzol`의 `cube_bottom_top` inherited up face에 tintindex 지정 없음. `grass_block`/ `podzol`의 snowy variant는 별도 모델을 참조하고 포드졸 snowy=true에서도 `grass_block_snow`가 지정된 것을 미러 JSON에서 확인했다. **생물군계 tint 매핑의 실제 숫자·주변 블록 오버레이·눈 상태 화면은 인게임 미검증**.

## E 모델·블록 상태·UV 직접 JSON 검사
- 6종 `dirt`, `coarse_dirt`, `rooted_dirt`, `mud`, `packed_mud`, `gravel`: `cube_all → cube` 상속, 기본 full face UV 0..16, 여섯 면 동일 PNG. `dirt`는 별도로 잔디/포드졸 모델의 아래면에도 참조됨.
- `mud_bricks`: **blockstates/mud_bricks.json → mud_bricks_north_west_mirrored → cube_north_west_mirrored_all → cube_north_west_mirrored**. 북/서 faces가 `uv:[16,0,0,16]`으로 수평 반전. 나머지 면은 기본 full UV. `models/block/mud_bricks.json` 존재만으로 블록상태 연결을 단정하면 오류.
- `grass_block_top`: `grass_block`의 up face 명시 UV `[0,0,16,16]`, tintindex=0; snowy 상태 모델 연결도 구분.
- `podzol_top`: `podzol` 모델의 `top` 슬롯, `cube_bottom_top → cube`의 기본 16×16 상단 UV; 정상 snowy=false 변형에서 쓰임.
- `UV_FACE_EVIDENCE.csv` 54개 행은 **9개 주요 모델의 6면 텍스처 슬롯 및 소스 선언 UV**를 조사한 결과다. 목록 중 9개 이외의 측면/아래면 참조 텍스처는 사용 관계 표시용이지 타 단계의 PNG를 분석 완료한 것이 아님. 실제 PNG 표본 (0,0), (8,8), (15,0) RGB(A)도 별도 보존. UV 변환 출력 렌더 픽셀의 공식 일치 여부는 미확정.
- 소스 JSON/Git blob SHA는 `SOURCE_LEDGER.csv`에 9건 기록. 상속 템플릿 `cube`, `cube_all`, `cube_bottom_top`, `cube_north_west_mirrored`, `cube_north_west_mirrored_all`은 비공식 미러에서 직접 열람했다.

## F 공식 인증·인게임 정적 검수
- 이번 작업에서 공식 Mojang 1.21.11 `client.jar` 바이너리를 확보·해시 검증하지 못함: **0/9 공식 인증**.
- 실제 Minecraft 정적 인게임 장면/틴트 및 조명 대조 불가: **0/9 인게임 검증**.
- 애니메이션·프레임·키프레임 및 Project Zomboid 변환, 가구 3D 제작 수행 안 함.

## G 재현성과 다음 단계
- 이 릴리스 파일: `SOURCE_LEDGER.csv` 9건, `PIXEL_METRICS.csv` 9건, `UV_FACE_EVIDENCE.csv` 54건, `SUMMARY.json`, 이 보고서. 직접 검사 대상 **9개 고유 PNG** (v4 과거 9건과 별도 중복 집계 금지).
- 다음 목표 `TEX09-R002`: 공식 버전 매니페스트를 통한 인증 client.jar 입수 가능 시 9개 바이너리 대조, 인게임 정적 장면/틴트 확인, 모델 상속 및 UV 미러 샘플 세밀 검증. 다음 채팅은 항상 `STATE.json` 먼저 재읽기.
- 공식 전체 버전 `v38`와 다른 단계 파일은 변경하지 않음. 소스 미러는 Mojang의 공식 배포가 아님.

원본: https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft/ , 기초 기록: `research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv`.
