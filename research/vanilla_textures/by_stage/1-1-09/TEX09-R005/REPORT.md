# TEX09-R005 — grass colormap RGB 전수 조사와 grass/podzol/snow 모델·UV 정적 경로

일자 2026-11-13. 대상 1-1-09 토양·지면 고정 PNG 9개. 사용자 제공 Minecraft Java 1.21.11 JAR 추출 폴더(저장소 1.21.11/)가 직접 출처다. 공식 JAR 인증을 의미하지 않는다.

## A. 기존/신규 분리
R001 대상 9 PNG 정적 픽셀, R002 정적 70면·69회전 이음새·mud_bricks UV36, R003 9 PNG·26 JSON, R004 잔디 오버레이 45 불투명/211 투명 및 눈 측면 순백 16을 계승한다. 이 수량은 신규에 더하지 않는다.
R005에서 새로 전체 RGB 디코드한 것은 보조 PNG colormap/grass.png 1개이다. 해당 파일의 존재·Git blob 대조는 이미 R003에서 기록됐고, 이 단계의 PNG 픽셀 전수 조사는 이번 R005 신규다. 고정 타깃 신규 0개, 신규 독립 JSON 0개.

## B. 바이너리 검증
사용자 추출본 1.21.11/assets/minecraft/textures/colormap/grass.png, 5930 bytes, blob f2e783063d40120245cd7141349681305e773831, SHA-256 6a7da1db5e76cdd74ba5c837afffc1f4ffa32442d7d087f3e1b414e590eb7486. SHA-256 계산 구현은 abc 표준 시험 벡터와 일치함을 확인.
PNG IHDR 256x256, 8-bit RGB(color type 2), IHDR/IDAT/IEND CRC 모두 통과(3/3). zlib Adler-32 통과. RGB 196608 bytes, 행별 filter 포함 196864 bytes를 디코드했다. RGBA 변환 시 alpha=255가 65536 픽셀 전부다.

## C. 새로운 실제 색상표 화소 측정
| 측정 | 결과 |
|---|---:|
| colormap 전체 texel | 65,536 |
| 순백 (255,255,255) | 32,640 |
| 비순백 | 32,896 |
| 고유 RGB | 4,536 |
| 비순백 영역 고유 RGB | 4,535 |
| 투명 | 0 |

256x256의 모든 좌표를 검사한 결과 x>y인 위치 32640개는 전부 순백, x≤y인 위치 32896개는 전부 비순백이며 양쪽 예외 0이다. y행의 흰색 수=255-y, 비순백 수=y+1. 이는 소스 이미지 경계일 뿐 게임 엔진의 기후 범위나 실제 화면 색상이라는 주장은 아니다.
실측 RGB 예시 (0,0)=(71,205,51), (64,64)=(103,196,81), (127,127)=(124,189,107), (255,0)=(255,255,255), (255,255)=(128,180,151). 256행 증거 및 13개 행의 51개 샘플 슬롯(좌표 중복 가능)을 별도 CSV에 보존한다.

## D. grass side overlay 및 colormap tint 경계
기존 R004의 grass_block_side_overlay.png에는 45 불투명과 211 투명 texel이 있다. 원본 grass_block.json은 같은 크기 cube 2개, 기본 6면과 별도 4개 측면 overlay를 선언한다. 위쪽 1면과 4개 overlay 면에 tintindex:0 및 명시적 UV [0,0,16,16]. 4x45=180은 정적 모델의 면별 비투명 오버레이 참조 위치 계산으로, 신규 180개의 서로 다른 픽셀이나 게임에 보이는 픽셀 수가 아니다.
독립 grass.png 색상표가 확인돼도 모델/상태 JSON만으로는 runtime의 biome index→(x,y) 조회, tint RGB, 감마, 조명, 가려짐 규칙을 확인할 수 없다. 색상표의 흰색 삼각형에 인게임 의미를 자의적으로 부여하지 않는다.

## E. JSON parent/elements/faces/UV/상태 직접 재검사
사용자 제공 blockstates 2개, models 6개 총 8개 기존 JSON을 다시 열어 파싱/상속/face-source를 해석했다. 모델 상태 4조합 28개 면 경로는 신규 파생 연결 표이며 기존 R002 면 수를 다시 누적하거나 신규 JSON 8개로 계산하지 않는다.
| 상태 | 선택 모델 / y 회전 | face | tintindex:0 | UV 출처 |
|---|---|---:|---:|---|
| grass_block snowy=false | grass_block / 0,90,180,270 | 10 | 5 | 10면 명시 [0,0,16,16] |
| grass_block snowy=true | grass_block_snow / 0 | 6 | 0 | UV 필드 없음 (implicit) |
| podzol snowy=false | podzol / 0,90,180,270 | 6 | 0 | UV 필드 없음 (implicit) |
| podzol snowy=true | grass_block_snow / 0 | 6 | 0 | UV 필드 없음 (implicit) |

grass_block_snow → cube_bottom_top → cube → block, podzol → cube_bottom_top → cube → block. cube.json은 [0,0,0]~[16,16,16] 요소를 갖지만 UV 수치 필드를 명시하지 않으므로 원장에서 implicit이라고 기록한다. snowy=true 두 경우 모두 top=grass_block_top, side=grass_block_snow, bottom=dirt. 일반 podzol은 top=podzol_top, side=podzol_side. 눈 모델과 podzol 모델에는 tintindex가 선언되어 있지 않다. 이것은 JSON 정적 결과이지 인게임 최종 외형 인증이 아니다.

## F. 남은 경계
인게임 정적 스크린샷·실측 검증 0/9. 실제 biome tint RGB, 색상표 샘플링 계산과 눈/이웃/조명 셰이딩은 미검증. Mojang 공식 client.jar 전체 SHA-1/메타데이터 인증은 사용자 지시로 필수 분모에서 제외했지만, 공식 인증 성공이 아니다.
애니메이션 분석 보류, Project Zomboid 변환·실제 가구 3D 제작 제외. 타 단계나 루트 상태, 전역 v38에 쓰지 않는다.

## G. 산출 및 다음 조사
SOURCE_LEDGER.csv (1개 보조 PNG의 신규 픽셀 디코드 vs 기존 8 JSON 재파싱), COLORMAP_GRASS_ROW_AUDIT.csv (256행), COLORMAP_GRASS_PIXEL_SAMPLES.csv (51 슬롯), STATIC_COLOR_FACE_LINKS.csv (28 파생 면), SUMMARY.json을 이 불변 릴리스에 보존한다.
다음 후보 TEX09-R006은 반드시 최신 LIVE STATE와 HEAD 재조회 후 결정한다. 실제 인게임 정적 관측 또는 출처가 검증되는 runtime biome colormap lookup 규칙이 확보될 때만 F나 tint 사실을 추가 검증한다.
