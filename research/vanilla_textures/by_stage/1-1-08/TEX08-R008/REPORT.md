# TEX08-R008 — 기능 블록 원본 PNG 애니메이션 5프레임 직접 연구

**2026-11-13 · 1-1-08 · Minecraft Java 1.21.11 사용자 추출 소스 · 보류 애니메이션 사용자 명시 재개**

## 연구 범위와 출처
사용자 제공 저장소의 `1.21.11/assets/minecraft/textures/block/`를 1차 원본으로 사용. 과거 R004 모델 면 원장 143행에서 실제 연결된 텍스처 경로 52개를 중복 제거하고 각 `<texture>.png.mcmeta`를 GitHub 원본 파일 경로로 조회했다. 52개 중 2개가 존재(훈연기 켜짐, 용광로 켜짐), 50개는 해당 경로 미존재(404). 이는 현재 단계의 모델이 참조한 52개 텍스처의 메타데이터 감사이며 모든 엔티티/게임플레이 애니메이션에 관한 전역 조사와 다르다.

## 실제 원본 애니메이션 JSON 및 PNG
| 텍스처 | 원본 PNG | .mcmeta frametime | interpolate | 소스 프레임 | 순환 및 명목상 주기 |
|---|---|---|---|---|---|
| `smoker_front_on` | 16×48 / 380바이트 | 4틱 | false | 3개 × 16×16 | 0→1→2→0, 12틱(20 TPS 가정 0.6초) |
| `blast_furnace_front_on` | 16×32 / 283바이트 | 10틱 | true | 2개 × 16×16 | 0→1→0, 20틱(20 TPS 가정 1초) |

두 mcmeta에는 `frames` 목록이 없으며 원본 세로 스트립의 16×16 위치를 차례로 사용한다. 메타의 보간 true/false는 **소스 선언 근거**로만 기록했다. true인 용광로에서 엔진이 만드는 중간 프레임은 실제로 확인하거나 추정 픽셀로 위조하지 않았다. 20 TPS 시간 환산 역시 실제 게임 측정이 아닌 정상 틱 속도의 이론값.

원본 6개 PNG(`smoker_front_on`, `smoker_front`, `blast_furnace_front_on`, `blast_furnace_front`, `furnace_front_on`, `furnace_front`)를 GitHub 바이트/base64에서 직접 디코딩해 각 PNG signature, IHDR/PLTE/IDAT/IEND CRC32, Git blob SHA-1, SHA-256 및 Pillow RGBA 확인. 모두 완전 불투명, 알파 변경 0. 켜진 훈연기 Git blob `bc6ecfc46a8e49e7a8df9e22482a145efe49396f`, SHA-256 `9509bf23aecb04b857c1aecc3f71dbb79f182f0a8977bba1d9129b949a4bb0d5`. 켜진 용광로 Git blob `53ee5793bc50295a771e10818a5601a71fc285b0`, SHA-256 `5363eaaf29c6cfed922c05fd4df9eaa7ef52b2d78ca56affda9ebf45ba33215d`. 원본 메타 Git blob 각각 `09eaec921357aabdd2fef6603815130df7e764b0`, `4894b537c138a0cd21e4d64f93ce7ce5206d629a`.

## 프레임별 변화 분석
| PNG | 프레임 순환 전환 | RGBA 변경 원본 좌표 /256 |
|---|---|---:|
| 훈연기 | 0→1 | 21 |
| 훈연기 | 1→2 | 34 |
| 훈연기 | 2→0 | 36 |
| 용광로 | 0→1 | 6 |
| 용광로 | 1→0 | 6 |

훈연기는 **3개 모든 프레임에서 색상이 하나라도 달라지는 43/256 좌표**(16.796875%), bbox `(2,8)..(13,13)`이고 나머지 213좌표는 일정했다. 용광로는 **6/256 좌표**(2.34375%), bbox `(6,8)..(10,9)`, 나머지 250좌표는 일정했다. 모든 프레임마다 16×16 RGBA raw SHA-256을 계산해 중복 프레임이 없음을 검사했다. 정확한 동적 좌표는 `ANIMATION_DYNAMIC_ROWS.csv` 16행당 행 마스크에 보존한다. 5 프레임×256=1,280 프레임별 좌표 **샘플 사용량**이며 21종 고정 PNG의 5,376 원본 픽셀이나 프로젝트 전역 새 고유 화소에 더하지 않는다.

## lit 상태 변경과 프레임 애니메이션 구별
원본 `smoker_on`, `blast_furnace_on`, `furnace_on` 3 모델 JSON의 로컬 north front/parent texture 슬롯을 읽고, 각각의 원본 blockstates의 4방향 lit=true 규칙과 연결했다. 모델-상태 12개 가운데 8개는 2개의 다중 프레임 PNG, 4개는 `furnace_front_on` 단일 정적 PNG. 화로 꺼짐→켜짐 전면은 36/256 RGBA 차이지만 **두 정적 파일의 상태 변경**일 뿐 2프레임 애니메이션이 아니다.
꺼진 훈연기 원본과 켜진 0/1/2프레임의 RGBA 변경은 각각 105/106/105픽셀, 꺼진 용광로와 켜진 0/1프레임은 각각 12/12픽셀. 이 비교는 해당 프레임에서 달라지는 영역을 정량화한 것이며 동작 속도나 실제 게임 출력 효과의 측정은 아니다.

## 결과 파일과 재현
`SOURCE_PNG_BINARY_AUDIT.csv`(6 원본), `METADATA_52_SOURCE_AUDIT.csv`(52 조회), `ANIMATION_FRAME_AUDIT.csv`(5 프레임), `ANIMATION_FRAME_TRANSITIONS.csv`(5 순환 전환), `ANIMATION_DYNAMIC_ROWS.csv`(32 행), `LIT_STATE_VS_FRAME.csv`(6 꺼짐/켜짐 비교), `LIT_MODEL_SOURCE_LINKS.csv`(12 lit=true blockstate), `SUMMARY.json`, `VERIFY_ANIMATION_FRAMES.py`(기존 사용자 추출본을 읽는 재현 코드). 사용자가 제외한 인게임 화면, 런타임 보간, particle/uvlock, 공식 Mojang 전체 JAR 인증은 수행하지 않았다. 기존 R001–R007과 v38을 보존하고 다른 단계·PZ 변환·3D 모델 제작은 미수행.

**결론:** 1-1-08 모델 면에 연결된 52개 텍스처의 원본 `.png.mcmeta` 존재 조사와 발견된 2개의 다중 프레임 PNG, 총 5 원본 프레임의 소스 애니메이션 분석이 완료됐다. 더 넓은 엔티티/게임플레이 애니메이션 연구는 이 범위의 완료 의미에 포함되지 않는다. 새로운 범위나 자료가 없으면 후속 무의미한 버전을 생성하지 않는다.
