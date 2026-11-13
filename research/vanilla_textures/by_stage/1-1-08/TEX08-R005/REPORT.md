# TEX08-R005 — 복합·기능면: 정적 상태 전환별 면·UV·particle 및 벌통 RGBA 대조

날짜: **2026-11-13** · 단계: **1-1-08** · 고정 표본: **21 PNG** · 전체 `v38` 변경 없음.

## 직접 수행한 원본 연구
사용자가 압축 해제해 GitHub에 업로드한 `1.21.11/assets/minecraft/`를 1차 자료로 사용했다. 이번 대화에서 실제 열고 파싱한 출처는 **blockstate JSON 16개, 모델 JSON 32개, 공통 부모 JSON 8개**, 고유 경로 합계 **56개**다. 이들은 이전 R003/R004에서 이미 확보된 파일들이므로 **신규 고유 JSON 0개**로 계상하고, 다른 단계의 계측을 복제 실적으로 더하지 않았다.

PNG `beehive_front`, `beehive_front_honey`, `beehive_side` 3개를 사용자 추출본 GitHub 바이너리에서 재확인하여 PNG chunk CRC32, SHA-256, Pillow 16×16 RGBA 디코드를 모두 검사했다. `beehive_front`는 기존 **21개** 대상이므로 재검증만 했고, 다른 두 파일은 **보조 PNG**이므로 21개와 이전 **5,376 원본 픽셀**에 추가하지 않았다. v35 선행 벌통 조사와의 프로젝트 전체 고유 중복 여부를 확정할 수 없어 전역 신규 픽셀 수를 선언하지 않는다.

## 새 상태쌍 비교의 정확한 분모
`STATIC_STATE_FACE_TRANSITIONS.csv`는 **62행**을 포함한다. 이는 blockstate의 73 variants 및 52 multipart 규칙 수나 기존 R004의 143 model-face rows가 아니라 **고정된 상태쌍을 비교한 새 결과**다.

| 대상 | 방향별 검사 상태쌍 | 소스 모델 로컬 면 변화 | 선언된 particle 참조 |
|---|---:|---|---|
| 통 barrel | 6 | `open=false→true`: `up`의 `barrel_top→barrel_top_open`만 변경 | `barrel_side` 그대로 |
| 화로 furnace | 4 | `lit=false→true`: `north`의 `furnace_front→furnace_front_on`만 변경 | 부모의 `#front` 상속으로 정면과 함께 변경 |
| 용광로 blast_furnace | 4 | `north`: `blast_furnace_front→blast_furnace_front_on` | `#front`에 따라 변경 |
| 훈연기 smoker | 4 | `north`: `smoker_front→smoker_front_on` | `#front`에 따라 변경 |
| 벌통 beehive | 20 (4방향×인접 honey 5단계) | 0→1→2→3→4는 변화 없음(16행); **4→5에서만 `north`의 `beehive_front→beehive_front_honey`** (4행) | 두 모델 모두 직접 선언 `beehive_side` 유지 |
| 조각된 책장 chiseled_bookshelf | 24 (4방향×6슬롯) | 단일 점유 슬롯의 `north` zero-depth overlay 1면에 `empty→occupied` | 슬롯 자식의 `#texture` 참조는 변경, 본체 `#top`은 유지 |

일반 variant 38상태쌍 가운데 **22쌍에서 모델 로컬 면 1개가 변경**, 벌통의 다른 16쌍에서 면과 particle 링크가 모두 동일했다. lit 12쌍에서 모델이 선언·상속한 particle 텍스처 참조가 변경됐다. 통 open 및 벌통 꿀 상태에서는 particle 참조가 변경되지 않았다. **실제 게임의 블록 단위 particle 우선 선택을 관찰했다는 뜻은 아니다.**

## 벌통 정적 이미지의 새 RGBA 비교
- `beehive_front.png`: 192바이트, SHA-256 `3d3fa761ee64d179fa1d29344e3eebbbcae609e2a8053421908dc854181b1dfa`, 8가지 RGBA 색.
- `beehive_front_honey.png`: 226바이트, SHA-256 `ff4ecedc9039b9579811d855a9188f22e00799708f940883fb4a2306950b15ec`, 13가지 RGBA 색.
- 두 이미지 **24/256픽셀(9.375%)의 RGBA 차이**, 알파값 변화 **0**, 차이의 픽셀 좌표 경계는 `(1,4)~(14,13)` (양 끝 포함). 변경 행 히스토그램 y0..y15: `0|0|0|0|14|1|0|0|0|0|4|2|2|1|0|0`.
- `beehive_side.png`: 187바이트, SHA-256 `db5aea136601a620f92acbe52c567d716bc7262f4142a3b43e6e09736927ca5c`, 8가지 RGBA 색.
- **모두 16×16, 알파 255 픽셀 256개, PNG IHDR/PLTE/IDAT/IEND 전 청크 CRC32 검증 통과.** 새 비교는 정적 PNG만 다뤘으며 애니메이션 프레임을 열지 않았다.

## UV와 모델 로컬 방향
일반 전환에서 변한 한 면의 UV는 모두 소스 상속 육면체에서 추론한 `[0,0,16,16]`. **22×256=5,632** 면적 사용이며 실측 고유 PNG 화소와 다르다. 조각된 책장 슬롯 24변경 중 한 방향의 6개 UV 면적 합은 **256**, 4방향 합은 **1,024**. 따라서 이번 상태 비교에서 바뀐 링크의 총 UV 사각형 면적은 **6,656 texel-reference-area uses**다. 이전 R004 32,512 uses 및 143 모델-면 행과 **합산하거나 중복 가산하면 안 된다**.

정면`north`/윗면`up`은 **모델의 로컬 방향**이다. 원본 blockstates의 `x/y` 회전은 CSV로 추적했으나, 화면에 실제 투영된 방향·uvlock·회전 결과는 인게임 근거가 없으므로 미확정이다. 책장 슬롯의 좌우 반전 UV, 본체의 north 면 미선언, 템플릿 particle=`#texture`의 자식 상속 해결은 R004 결과를 유지했다.

## 완료 근거의 경계
- 이번 단계의 대상은 계속 **21 PNG**, 이전 R001 **5,376 원본 픽셀**이며 R003/R004의 **39 모델+8 부모/143면**은 그대로 계승.
- `furnace_front_on`, `smoker_front_on`, `blast_furnace_front_on` 파일의 **프레임 내용·애니메이션·키프레임 픽셀 연구는 수행하지 않았다**. lit 판단은 모델 JSON의 정적 texture 경로만 다룸.
- 실제 Minecraft 인게임 정적 렌더와 실제 particle 선택의 인증 수 **0/21**.
- Mojang 공식 배포 client.jar 전체 SHA-1/manifest 인증은 **사용자 요청으로 완료 분모에서 제외**하며 공식 인증 성공을 주장하지 않음.
- 애니메이션, Project Zomboid 변환, 실제 3D 가구 제작, 다른 1-1 단계나 루트 상태파일의 수정 **모두 보류**.

## 연구 파일
- `STATIC_STATE_FACE_TRANSITIONS.csv` — 62 상태쌍, 모델 SHA·UV·local face·source particle 및 회전
- `STATIC_PNG_BINARY.csv` — 3개 PNG SHA·CRC·RGBA
- `BEEHIVE_RGBA_DIFFERENCE.csv` — 24/256 변화의 위치·행 분포
- `SOURCE_RECHECK_LEDGER.csv` — 이 조사에 직접 사용한 사용자 추출본 JSON/PNG의 출처·Git blob SHA
- `SUMMARY.json` — 이전 근거 계승 vs 신규 비교행·미검증 실적 구분

다음 정식 결과는 실시간 다음 버전이 여전히 `TEX08-R006`일 때 **새 근거가 있는 경우에만** 작성한다.
