# TEX09-R006 — 사용자 원본 grass/podzol/snow 측면 PNG 16×16 화소 정렬 검증

날짜: 2026-11-13 · 연구 단계 **1-1-09 토양·지면** · 고정 표본 **9개 유지** · GitHub main의 **사용자 제공 Minecraft Java 1.21.11 JAR 압축 해제본**이 직접 소스. 공식 Mojang JAR 인증으로 간주하지 않는다.

## A. 이전 증거와 이번에 새로 측정한 자료
- R001~R003: 기존 9 PNG/26 JSON/면·UV, R004: 45 불투명 잔디 overlay 및 눈 측면 순백 16, R005: grass.png colormap 65,536 RGB 픽셀과 28 파생 면 경로. 모두 계승하며 이번 신규 파일·픽셀로 더하지 않는다.
- **이번에 비트맵을 처음 전수 RGBA 디코드한 보조 PNG 2개:** `grass_block_side.png`와 `podzol_side.png` (각 16×16, 총 독립 신측정 512 texel). R003에서 두 파일 경로/바이트 출처는 확인됐지만, 당시 두 PNG의 RGBA 공간 정렬 검사는 없었다.
- 이전부터 픽셀이 검증된 보조 PNG `grass_block_snow.png`, `grass_block_side_overlay.png`를 비교용으로 다시 읽었다(재검사 512 픽셀, **신규 누적 0**). 원본 9개 대상 및 신규 모델 JSON 0개.

## B. 원본 PNG SHA·CRC·RGBA 바이너리 검사
| PNG | 바이트 | SHA-256 | 16×16 고유 RGB | 불투명 / 투명 | 새 디코드? |
|---|---:|---|---:|---|---|
| `grass_block_side.png` | 329 | `76a677640eb91d6a9aed844bc66e329b1894f89e241a0071333b6678c0854580` | 40 | 256 / 0 | 예 |
| `podzol_side.png` | 395 | `dacef78790b567396241e3d1453cdc5cd63eb79484f77fe8bd9311281805e283` | 58 | 256 / 0 | 예 |
| `grass_block_snow.png` | 247 | `8802c885e4d689be9c85102ca3e4469ef2f6e382603a811bdc3b65fbcf76c0df` | 17 | 256 / 0 | 아니오(기존 재검사) |
| `grass_block_side_overlay.png` | 135 | `872056682c3b059c04aba88f8b4e706f2526b907e1acef12626a9f912f573a85` | 16 | 45 / 211 | 아니오(기존 재검사) |

- 4개 PNG에서 실제 바이너리를 열고 SHA-256, Git blob, IHDR·PLTE 또는 tRNS·IDAT·IEND **각 4개 PNG 청크 CRC 전부 통과**, 16×16 RGBA 픽셀 디코드 일치. RGB 고유값은 alpha=255의 유효 색을 기준으로 보고한다.
- 사용자 제공 원본 파일을 우선 사용했으며 비공식 미러로 신규 성과를 대체하지 않았다.

## C. 동일 좌표 RGB(모두 불투명인 3개 원본) 픽셀 비교 — 새 실측
| RGB/불투명 RGBA 비교 | 동일 | 다름 | 완전 동일 행 | 예외적 일부 일치 |
|---|---:|---:|---|---|
| grass side ↔ podzol side | **184** | 72 | **y=5..15 (176 픽셀)** | y=4에서 8 픽셀 |
| grass side ↔ snowy side | **145** | 111 | **y=7..15 (144 픽셀)** | y=5에서 1 픽셀 |
| podzol side ↔ snowy side | **145** | 111 | **y=7..15 (144 픽셀)** | y=5에서 1 픽셀 |

각 쌍은 16×16 동일 (x,y) 좌표 256개씩 비교했다. **3쌍 총 768 좌표별 비교**는 신규 산출 비교 연산 수이며 신규 PNG 표본이나 독립 texel 개수와 다르다. `SIDE_PAIR_EQUALITY_MASK_ROWS.csv`의 16행에서 `=`는 해당 좌표 RGB 동일, `.`는 다름을 뜻한다.
grass↔podzol의 y=0..3은 한 화소도 같은 RGB가 없고, y=4는 8/16 동일, y=5..15는 11행×16=176개 완전 동일. **따라서 PNG 안에서 아래쪽 공유 패턴이 구조적으로 확인**된다. snow 측면 역시 y=7..15의 9행×16=144픽셀을 두 기본 측면과 그대로 공유한다.

## D3. grass overlay 알파 및 모델에 관한 검증 경계
- R004에서 이미 검증된 `grass_block_side_overlay.png`: 16×16 중 **45 불투명/211 투명**, 불투명 좌표 y=0..3. 이 45 좌표에서 **overlay 원본 회색 RGB와 grass base side 원본 RGB가 같은 위치는 0/45**(R006 신규 대조). 211개의 투명 좌표는 모델/PNG 기반 설명에서 기본 측면 텍스처가 남는 위치로 해석할 수 있다.
- grass 모델에서 base cube(6면)와 overlay cube(측면 4면), 후자의 `tintindex:0`는 기존 R005 정적 JSON 근거를 새로 재판독했다. `podzol` 일반 모델은 별도 side PNG를 사용하고 **overlay cube가 없는 모델**이다. 두 모델의 공통 측면 픽셀은 **소스 비트맵의 공유 RGB이지, 두 블록의 동일한 인게임 tint/렌더를 입증하지 않는다**.
- 실제 overlay tint 배합 방식, colormap(바이옴 입력) 샘플링, 감마, 조명, culling/인접 블록 및 게임 표시는 **미검증**. 실제 바이옴별 RGB를 임의로 인증하지 않는다.

## E. JSON 상태·모델 정적 재대조
- 이번 JSON은 기존 자료 5개 재열람(신규 JSON 0): `grass_block.json` 모델의 `#side`/`#overlay`, `podzol.json`의 `#side`, `grass_block_snow.json`의 side 슬롯을 다시 확인했다.
- blockstates에서 grass/podzol `snowy=false`에는 각각 일반 모델의 Y 0·90·180·270 회전 후보, `snowy=true`에서는 둘 다 `grass_block_snow` 모델 하나가 선택됨. 소스 상태-모델 관계이며 실제 눈 상태 게임 장면 인증은 아니다.

## F. 미검증과 제외
- 사용자 제공 추출본의 바이너리/정적 모델 검증이지 Mojang 공식 JAR 인증이 아니다. 전체 JAR SHA-1/공식 메타데이터 인증은 사용자 지시로 필수 항목 및 완료 분모에서 제외하되 인증 완료로 표시하지 않는다.
- **실제 게임 정적 렌더 검증 0/9**. grass biome tint/눈/주변 블록/조명의 실제 화면 검증도 0. 애니메이션 연구 보류, 가구 3D 제작·Project Zomboid 변환 제외.

## G. 저장 근거 및 다음 진입
- `SIDE_PAIR_EQUALITY_MASK_ROWS.csv` 16행, `SIDE_PAIR_SUMMARY.csv` 3쌍, `SOURCE_PIXEL_STATS.csv` 4 PNG(2 신규/2 기존), `SOURCE_LEDGER.csv` 4 PNG+5 기존 JSON, `SUMMARY.json`, `REPORT.md`를 본 단계 릴리스에 저장.
- 기존 R001~R005 및 전역 v38, 타 단계 관리 문서 변경 금지. 다음 후보 `TEX09-R007`은 반드시 라이브 STATE와 Git HEAD를 다시 읽고 경합을 배제한 뒤 진행할 것. 확인 가능한 runtime tint 계산 규칙 또는 실제 인게임 **정적** 관찰이 확보되면 별도 증거로 F를 검증하고, 없으면 pending을 유지한다.
