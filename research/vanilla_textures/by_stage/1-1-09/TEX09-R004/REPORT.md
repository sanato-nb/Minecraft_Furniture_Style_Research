# TEX09-R004 — 사용자 제공 잔디 오버레이의 불투명 영역·눈 상태 측면 정적 픽셀 분석

일자 **2026-11-13**. 담당 **1-1-09 토양·지면**, 고정 표본 **9개** 변경 없음. 게임 버전 Java 1.21.11. 전역 체크포인트 `v38` 변경 없음. R001/R002/R003 불변.

## A — 기존 결과 대비 이번에만 새로 실측한 범위
이전 R001은 9개 타깃 PNG의 원본 화소·RGB, R002는 정적 UV/회전, R003은 **사용자 제공 `1.21.11/` 폴더**의 9개 표본과 5개 보조 PNG·26개 모델 JSON의 바이트/출처 동일성을 확인했다.

이번에는 원본 사용자 추출본에서 **보조 텍스처의 내부 화소 구조**가 누락된 부분을 진행했다.
- 기존 검토만 했던 보조 PNG 2개 `grass_block_side_overlay.png`, `grass_block_snow.png`를 **실제 Pillow RGBA로 디코드해 알파/색상 분포 새로 실측**.
- 고정 표본 `podzol_top.png`은 기존 데이터와 일관성 점검을 위해 재확인했으나 **신규 PNG 표본으로 계상하지 않음**.
- 기존 9개 PNG와 70개 모델면/69개 회전쌍/36개 mud_bricks UV 기록은 **재집계하지 않음**.

## B — 사용자 제공 보조 PNG 바이너리 직접 검증
GitHub `sanato-nb/Minecraft_Furniture_Style_Research` `1.21.11/assets/minecraft/textures/block/`의 **실제 PNG 바이너리**를 `fetch_file(encoding=base64)`로 읽고 raw bytes Git blob SHA-1=SHA1(`blob {length}\0{bytes}`) 검증 후 Pillow `Image.verify()`, RGBA 디코드 수행.
- `grass_block_side_overlay.png`: 원본 135바이트, SHA-256 `872056682c3b059c04aba88f8b4e706f2526b907e1acef12626a9f912f573a85`, Git blob `0e60ccc34e458bf30ea19a2dff4e013e5cb8b314` 일치.
- `grass_block_snow.png`: 원본 247바이트, SHA-256 `8802c885e4d689be9c85102ca3e4469ef2f6e382603a811bdc3b65fbcf76c0df`, Git blob `0c0cbcaa7bde54b6d6c8a794f030bf64b4b1a585` 일치.
- `podzol_top.png`: 이전부터 검증된 대상 원본 196바이트, SHA-256 `598072d5a4db38ec4ea081a584a2de6b5960785bc2287e18e93427c7433c5d56`, Git blob `1ce952a8bec048de1bcaf3cf248f06aec5d20ed6`. 이 항목은 **동일 타깃 재검사**일 뿐 R004 신규 대상 추가 아님.

## C — 실제 RGBA 정량 결과 (새 측정)
| PNG | PNG 원본 mode | 불투명 화소 | 투명 화소 | 불투명 영역 고유 RGB | 특징 |
|---|---|---:|---:|---:|---|
| grass_block_side_overlay | `L` + `tRNS` (값 0) | **45/256** | **211/256** | **회색 16종** | 알파 값은 0 또는 255만 존재 |
| grass_block_snow | `P` (불투명) | **256/256** | 0 | **17종** | 순백 `(255,255,255)` 16픽셀 |
| podzol_top | `P` (불투명) | 256/256 | 0 | **6종** | R001/R003에서 검증한 타깃 반복 표본 |

오버레이 불투명 45픽셀은 16×16 원본의 `y=0..3`에만 분포한다. 행별 개수는 **16, 15, 11, 3, 0×12**. 빈 곳은 `alpha=0`이며, 보이는 부분은 `alpha=255`. `alpha=255` 영역의 RGB 값은 균일한 흰색이 아니라 `119..178` 범위 16종의 동일 R=G=B 회색이다.

원본 소스의 실제 16행 알파 마스크(`#=불투명, .=투명`):

```text
################
#####.##########
#.###.#.####.##.
....#...#.#.....
................
................
................
................
................
................
................
................
................
................
................
................
```

`GRASS_OVERLAY_MASK_ROWS.csv`에 각 행별 16픽셀 마스크를, `GRASS_OVERLAY_VISIBLE_TEXELS.csv`에는 **45개 모든 불투명 좌표의 실제 RGBA**를 기록했다. `SNOW_WHITE_TEXELS.csv`는 snowy 측면에서 확인된 순백 16개 실제 좌표만 기록했다. 256px 전체 RGBA의 계산 결과는 요약 원장에 담되 R004 데이터를 기존 9 타깃 실측으로 추가하지 않음.

## D3 — 잔디 tint 및 눈 상태의 정적 의미
사용자 제공 `models/block/grass_block.json`은 같은 `[0,0,0]~[16,16,16]` 위치에 두 큐브 요소를 선언한다. 첫 요소는 하단/상단/측면 6면, 두 번째는 **측면 4면**으로 텍스처 슬롯 `#overlay`를 사용하며 `tintindex:0`를 선언. 상단도 `tintindex:0`이다.

이번 PNG 분석으로 **측면 overlay가 전체 얼굴을 덮는 불투명 레이어가 아니라 상단 4행 일부만 비투명으로 갖는 패턴**이라는 점을 사용자 원본으로 직접 확인했다. 이 회색 명도와 임의 예시 초록색을 조합한 이미지는 색상 메커니즘 이해용 **설명용 마스크 합성**이지 게임이 표시한 실제 색상 재현이 아니다.

`grass_block_snow.png`는 불투명 RGB 픽셀 전체를 포함하므로 **눈 상태 측면의 픽셀 자체가 눈/흙 혼합 색채를 담음**을 확인했다. 순백 RGB 16개는 y=0..4 범위에 분포; 나머지 영역에는 순백 외의 밝은 눈 색상 및 흙색이 함께 존재한다. JSON상 `grass_block_snow` 모델은 `cube_bottom_top` 상속으로 추가 측면 overlay/tintindex 선언 없음.

`podzol snowy=true`도 사용자 제공 `blockstates/podzol.json`이 `grass_block_snow` 모델을 선택한다. 따라서 **정적 소스 모델 기준**으로 눈이 쌓인 경우 포드졸 특유의 측면 슬롯 대신 해당 눈-잔디 모델 측면 슬롯을 참조한다. 게임 엔진의 틴트/주변 조명/기상 표현은 검증하지 않음.

## E — 모델/블록상태 관계 확인
`STATIC_VARIANT_FACE_CONNECTIONS.csv`에 4가지 variant 조합(잔디 일반/눈, 포드졸 일반/눈)에서 위/측면/오버레이 소스, JSON `tintindex` 선언 여부, element count를 별도 저장했다. 선택 연결은 R003의 원본 사용자 JSON을 다시 열어 확인했으며 **새 모델 4종을 추가 발견했다고 계상하지 않음**.

## F — 검증 범위 4계층을 엄격히 구분
1. **사용자 제공 JAR 추출본:** 보조 PNG 2개 **신규 픽셀 디코드**, 기존 target 9개/JSON 26개 검증 이력 유지.
2. **비공식 미러 대조:** R003에서 같은 보조 PNG 5개 Git blob 일치. 이번 R004는 사용자 제공 실제 PNG 화소 기준.
3. **Mojang 공식 원본 인증:** 원본 JAR 전체 SHA-1/공식 메타데이터 대조 **미완료**. 공식 인증 0/9.
4. **인게임:** 실제 게임 장면의 tint·눈·이웃/광원 **미완료**, 정적 인게임 0/9.

## G — 산출·향후 인수인계
- `GRASS_OVERLAY_MASK_ROWS.csv`: 16행의 정확한 불투명 마스크
- `GRASS_OVERLAY_VISIBLE_TEXELS.csv`: 45개 불투명 픽셀의 좌표/RGBA
- `SNOW_WHITE_TEXELS.csv`: 눈 상태 측면의 순백 16개 픽셀
- `AUXILIARY_TEXTURE_METRICS.csv`: 3개 파일의 크기/해시/알파/색 집계(2개 보조 신규 화소 검사, 1개 타깃 재확인)
- `STATIC_VARIANT_FACE_CONNECTIONS.csv`: 4개 상태-모델 조합 및 tint/오버레이 연결
- `SUMMARY.json`, `REPORT.md`.
- 다음 단계 **`TEX09-R005`**, 먼저 최신 `STATE.json`/HEAD/충돌을 재확인.
- **애니메이션 분석 보류**, Project Zomboid 변환·가구 3D 모델링 금지, 다른 단계 및 전역 v38 변경 금지.

출처: `https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11/assets/minecraft/` (사용자 제공 추출본, 공식 인증 미완료), R003 SHA 원장 및 R002 모델 상속 근거.
