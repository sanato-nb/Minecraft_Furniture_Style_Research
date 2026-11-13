# TEX09-R007 — 사용자 추출본 dirt 원본과 grass/podzol/snow 측면 정적 픽셀 정합성 검수

기록: 2026-11-13. 범위 **1-1-09의 고정 9종**. 직접 소스 `1.21.11/assets/minecraft/` (사용자 제공 Minecraft Java 1.21.11 JAR 추출본); 이 사실은 공식 Mojang 전체 JAR 인증을 의미하지 않는다.

## A. 기존 데이터와 신규 비교 근거를 분리
- R001/R003에서 정적 PNG 검증된 9개 중 `dirt.png`와 R004에서 전수 디코드한 `grass_block_snow.png`, R006에서 전수 디코드한 `grass_block_side.png`, `podzol_side.png`의 사용자 원본을 새로 다시 열었다. PNG 4개×256=1024 픽셀은 **이전에도 이미 개별 디코드된 픽셀**이며 신규 원본 PNG 0, 신규 고정 표본 0, 신규 색 픽셀 누적 0.
- 이번 독립 근거는 **기존 PNG 사이 동일 (x,y) 좌표 정합성 측정 3쌍×256=768 비교 및 256좌표별 네 텍스처 일치 유형 분류**다. 이전 R006의 side↔side 비교 768건과 중복 가산하지 않는다.

## B. 바이너리 직접 재대조
| 사용자 원본 PNG | bytes | SHA-256 | Git blob SHA-1 | PNG CRC |
|---|---:|---|---|---|
| `dirt.png` | 197 | `67197d5371efc3ca1638217c38349665dbd5a977b47bfb20075c858dff87d510` | `3f70996d2b9d5094afafc2cd2cdc090d9f38a486` | 4/4 |
| `grass_block_side.png` | 329 | `76a677640eb91d6a9aed844bc66e329b1894f89e241a0071333b6678c0854580` | `4e3ae001818611f0949a1294e804ac65a606a5a5` | 4/4 |
| `podzol_side.png` | 395 | `dacef78790b567396241e3d1453cdc5cd63eb79484f77fe8bd9311281805e283` | `914ff2c9464f8e517461fa8b61989e284cbe69dc` | 4/4 |
| `grass_block_snow.png` | 247 | `8802c885e4d689be9c85102ca3e4469ef2f6e382603a811bdc3b65fbcf76c0df` | `0c0cbcaa7bde54b6d6c8a794f030bf64b4b1a585` | 4/4 |

- 네 PNG는 모두 실제 16×16 RGBA로 디코드했고 전 픽셀 alpha 255, 각 PNG의 IHDR/PLTE/IDAT/IEND 4개 CRC 전부 정상, IEND 이후 잔여 바이트 없음. 계산 SHA-256은 기존 출처 R003/R006와 일치한다. 고정 9개 중 `dirt`만 이번 비교에 재사용됐다.

## C. dirt와 같은 좌표의 RGB 일치
| 대상 측면 | 흙 원본 일치/256 | 다름/256 | 모든 16픽셀 동일 행 | 윗부분에서 추가 일치 |
|---|---:|---:|---|---|
| `grass_block_side` | **195** | 61 | y=5..15, 176픽셀 | y2:1, y3:4, y4:14 |
| `podzol_side` | **188** | 68 | y=5..15, 176픽셀 | y3:4, y4:8 |
| `grass_block_snow` | **145** | 111 | y=7..15, 144픽셀 | y5:1 |

- 첫 번째/두 번째 측면은 y=5..15의 아래쪽 **176/176 좌표가 dirt의 동일 좌표 RGB와 완전히 일치**. 눈 측면은 y=7..15 아래쪽 **144/144 좌표가 동일**. R006에서 각 측면끼리 비슷하게 관측된 이유를 `dirt.png`라는 실제 별도 소스와 직접 대조해 재현했다.
- `DIRT_SIDE_COORDINATE_CLASSES_16_ROWS.csv`의 256문자 분류: `A`=dirt·grass·podzol·snow 4개 전부 동일(145); `B`=dirt·grass·podzol만 동일(39); `G`=dirt·grass만 동일(11); `P`=dirt·podzol만 동일(4); `.`=세 측면 중 dirt와 동일한 것이 없음(57). **145+39+11+4+57=256**. 세 측면 전부 흙과 같은 위치 145개 중 144개는 y=7..15, 나머지 1개는 (x11,y5).
- `DIRT_SIDE_CONTINUOUS_LOWER_BOUNDARY.csv`: x=0..15의 각 열에서 아래끝 y15까지 정확히 흙과 같은 RGB가 연속되는 가장 위쪽 y를 추출. 잔디 측면은 열별 시작 y2..5, 포드졸은 y3..5, 눈 측면은 전 열에서 y7.

## D3. 정적 모델과의 연결 및 증거 범위
- 사용자 JSON 모델 5개(`dirt`, `cube_all`, `grass_block`, `podzol`, `grass_block_snow`)와 상태 2개(`grass_block`, `podzol`)를 다시 파싱했으나 새 JSON 0개. `dirt` 모델은 `cube_all`의 여섯 면 모두 dirt를 참조하고, 잔디 base 밑면·포드졸 밑면·공유 snowy 모델의 밑면도 `dirt`를 직접 참조한다.
- 잔디 side와 포드졸 side는 각자 별도 PNG이며, **측면의 아래쪽 픽셀이 dirt와 일치한다는 것은 파일 내용 측정**이다. JSON이 side를 runtime에서 dirt와 합성하거나 자동 생성한다고 결론내리지 않는다. 이미 PNG 바이너리에 이 공유 패턴이 들어 있다.
- 잔디 base 위에 올리는 overlay는 이전 R004의 알파45 및 R006의 tintindex:0 근거를 그대로 계승한다. 이번에 overlay의 새 색 픽셀을 다시 누적하지 않았다. 색맵 좌표, 바이옴별 색, 광원/그림자/가려짐은 별도 런타임 증거 없이는 인증 불가.

## E/F. 검증 단계의 현재 경계
- 고정 9/9 PNG 소스 바이트·정적 모델/UV 비교 기록은 기존 R001~R006에 이미 보존돼 있으며 R007은 남은 `dirt ↔ side` 직접 소스 근거를 추가했다. 따라서 **현재 확보된 소스만 반복 열어서 리비전을 올리는 것은 중단**한다.
- **인게임 정적 검증 0/9**. 새 진척에 필요한 자료는 실제 Java 1.21.11 게임의 정적 비교 스크린샷/캡처(가능하면 F3 바이옴 정보, 시간/광원/그래픽 상태가 통제된 9종 및 grass/podzol 눈 유무 장면)다. 사용자의 직접 캡처가 없으면 런타임 틴트·눈/조명·인접 효과 단계는 `pending`, 임의로 완료하지 않는다.
- 공식 Mojang JAR SHA-1/manifest 인증은 사용자 지시로 필수 제외(성공했다고 표시하지 않음); 애니메이션 보류; Project Zomboid 변환과 가구 3D 제작은 여기 범위 외.

## G. 저장 및 재진입
- 신규 `DIRT_SIDE_COORDINATE_CLASSES_16_ROWS.csv` (16행), `DIRT_SIDE_CONTINUOUS_LOWER_BOUNDARY.csv` (16열), `DIRT_SIDE_MATCH_SUMMARY.csv` (3쌍), `DIRT_SIDE_RGB_SAMPLES.csv` (8좌표), `SOURCE_LEDGER.csv` (4 PNG+7 기존 JSON), `SUMMARY.json`, `REPORT.md`를 `TEX09-R007/`의 불변 산출물로 저장.
- 사용자 지시: 다음에 `계속해줘`라고 하더라도 새로운 근거가 없거나 사용자 직접 인게임 자료가 반드시 필요할 경우 **새 리비전을 만들지 않고 연구를 멈춘 후 필요한 도움을 알린다**. 다음 리비전 `TEX09-R008`은 후보일 뿐, 실제 새로운 증거가 있을 때만 시작한다.
- 다른 단계/루트 상태, 전역 v38, 이전 TEX09-R000~R006 보고서는 수정하지 않는다.
