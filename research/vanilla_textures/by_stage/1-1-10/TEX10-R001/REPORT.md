# TEX10-R001 — 1-1-10 잎·식생 독립 실측 및 정적 소스 연구
> Minecraft Java 1.21.11 · 2026-11-13 · **연구 표본 정확히 8개**. 공식 전체 연구 체크포인트는 **v38 유지**. `TEX10-R000` 계획 다음 첫 실측 릴리스.

## 출처와 검증 구분 (A)
1. 지정된 `HANDOFF.md`, `STATE.json`, `1-1-10_잎식생.md`, 독립 버전 규칙, v4 150표본 CSV 및 150개 번호 원장을 직접 조회해 대상 8개 경로/해시/순번 **8/8 교차 일치** 확인.
2. **이번 재검사:** 사용자 저장소 `1.21.11/assets/minecraft/textures/block/` 아래 8종 **바이너리를 GitHub에서 Base64로 읽고** Pillow RGBA 디코딩, SHA256·PNG 전 청크 CRC·가시 마스크 계측. **8/8 통과**. `InventivetalentDev/minecraft-assets` 의 `1.21.11` 브랜치 8종 파일과 **Git blob SHA 8/8 동일**. 기존 v4 기록 SHA-256 **8/8 동일**.
3. v35(종/케이크/벌통), v36~37(화로/용광로/훈연기), v38(오크 선반) 보고서에서 본 8개 ID의 동일 PNG에 대해 직접 완료로 기록된 항목 없음. 이 4개 버전의 다른 물체 검증은 이 단계 완료량에 추가하지 않음.
4. **중요:** 본 저장소의 `1.21.11/` 디렉터리는 추출본이다. 미러 동일성 및 `META-INF` 파일 존재만으로 **Mojang 공식 client.jar 인증을 주장하지 않는다**.

## B–C 실측 결과
- PNG **8/8 모두 16×16**, 총 **2,048 RGBA 픽셀**. 가시 **1,492**, 완전 투명 **556**, 부분 알파 **0**. 모든 청크 CRC 통과, SHA-256 v4와 일치. `moss_block` 256/256 불투명; 나머지 7개는 **알파 0/255 이진 컷아웃**.
- RGB/알파/연결요소/내부 구멍/테두리 세부 기록은 [PIXEL_AUDIT.json](PIXEL_AUDIT.json), 원본·해시·모델 주소는 [SOURCE_LEDGER.csv](SOURCE_LEDGER.csv).

| 이미지 | 바이트 | 가시 / 256 | 투명 | 고유 가시 RGB | 내부 구멍 (4-연결) | PNG 주색 |
|---|---:|---:|---:|---:|---:|---|
| `oak_leaves` | 202 | 172 (67.19%) | 84 | 4 | 16 | `#989998` |
| `spruce_leaves` | 175 | 160 (62.50%) | 96 | 6 | 26 | `#8A8A8A` |
| `birch_leaves` | 197 | 144 (56.25%) | 112 | 4 | 15 | `#706D70` |
| `mangrove_leaves` | 221 | 212 (82.81%) | 44 | 5 | 5 | `#6D6A6A` |
| `azalea_leaves` | 209 | 197 (76.95%) | 59 | 4 | 11 | `#50692C` |
| `moss_block` | 204 | 256 (100.00%) | 0 | 6 | 0 | `#647233` |
| `vine` | 167 | 146 (57.03%) | 110 | 4 | 2 | `#838383` |
| `flowering_azalea_leaves` | 220 | 205 (80.08%) | 51 | 7 | 12 | `#50692C` |

## D1 알파 마스크 / 외곽
- `oak_leaves`: 172/256 가시, 내부 4-연결 투명 구멍 16개. `spruce_leaves`: 160, 26개. `birch_leaves`: 144, 15개. `mangrove_leaves`: 212, 5개.
- `azalea_leaves`: 197, 11개. `flowering_azalea_leaves`: 205, 12개. `vine`: 146, 2개. `moss_block`: 256, 0개.
- 8종 **모두 알파 바운딩 박스가 전체 (0,0,16,16)**: 각 변 어딘가에 가시 픽셀이 존재한다. 따라서 모든 바깥 테두리가 투명하다는 뜻이 아니다. 경계의 일부 투명 픽셀은 `transparent_border_pixels`로 별도 계측.
- 내부 구멍은 **2D 4-연결 픽셀 마스크**의 수치로서 게임의 실제 3D 뚫린 면 수가 아니다.

## D2 PNG 자체의 녹색과 tintindex
- 참나무·가문비·자작·맹그로브 잎은 **대체로 회색/중립 계열 PNG**; `leaves.json` 부모의 6면에 **`tintindex:0`**. `vine.png`도 회색조이고 `vine.json` 양면에 **`tintindex:0`**.
- `azalea_leaves`, `flowering_azalea_leaves`의 주색은 `#50692C`(꽃 텍셀 추가), `moss_block`은 `#647233`. 이 셋의 모델 상속 계열 `cube_all`→`cube`에는 **`tintindex` 키가 미기재**다. **미기재와 `0`은 다르다.**
- JSON 플래그만으로 실제 biome tint 값, 종별 특례(가문비·자작나무), 인게임 RGB 또는 렌더 결과를 재현했다고 주장하지 않음. **생물군계별 게임 최종 색 미검증**.

## D3 / E 정적 모델·상속·UV
- 잎 `oak/spruce/birch/mangrove`: 모델 각각 `minecraft:block/leaves` 부모, 단일 **[0,0,0]~[16,16,16] 큐브**. 부모가 **6면 모두 `uv:[0,0,16,16]`, `#all`, `tintindex:0`, 방향별 cullface**를 명시. 총 **24 정적 면**.
- `azalea_leaves` / `flowering_azalea_leaves` / `moss_block`: `minecraft:block/cube_all` → `block/cube` → `block/block`; 16³ 단일 큐브, 6면에 동일 PNG. `cube`에서 UV 키는 **미기재**이며 전체 면 기본 `[0,0,16,16]`으로 해석되는 **파생 UV**로 기록. `tintindex` 미기재. 총 **18 정적 면**.
- `vine`: 자체 `model/vine.json`의 **0 두께 평면 [0,0,0.8]~[16,16,0.8]**에 **north/south 양면**. north UV **[16,0,0,16]** 좌우 반전, south UV **[0,0,16,16]** 정방향, `#vine`, 둘 다 tintindex 0. `blockstates/vine.json`은 **10개 multipart 조건**: 북/동/남/서/상단 및 모든 부착 방향이 거짓인 fallback 5개. 동/남/서 Y 회전 90/180/270, 상단 X 270; 해당 회전엔 uvlock true가 있다.
- 합계 **정적 모델 면 44행(큐브 42 + 덩굴 2)**. 각 면의 슬롯·UV·tint·텍셀 256개 중 가시 픽셀 수를 [MODEL_UV_AUDIT.csv](MODEL_UV_AUDIT.csv)에 저장. 이것은 **런타임 state별 복제 면 수나 게임 최종 메시가 아님**.
- 컷아웃 모양은 PNG의 **알파 마스크**, 공간상 큐브/얇은 덩굴 면과 방향은 **모델 및 blockstates JSON** 담당. 이를 수많은 복잡한 실제 3D 잎 다각형으로 잘못 해석하지 않음.

## F 공식 원본·게임 검증 미완료
- **공식 Mojang 1.21.11 client.jar 진본/매니페스트 교차 인증 0/8**. 보유한 것은 저장소 추출본/별도 추출 미러이며 JAR 바이트 진본 확인은 하지 못함.
- **실제 게임 정적 장면 확인 0/8**. biome 색, 컷아웃 렌더, 덩굴 상태별 배치, 텍셀 샘플의 인게임 검증을 보류.
- **애니메이션·흔들림·키프레임·움직임 분석 금지 유지**. 기존 동적 기록 보존.

## G 릴리스/연속성
- 독립 불변 경로 `research/vanilla_textures/by_stage/1-1-10/TEX10-R001/`: 본 보고서, `SOURCE_LEDGER.csv`, `PIXEL_AUDIT.json`, `MODEL_UV_AUDIT.csv`, `SUMMARY.json`. 단계 상태/인수인계 파일만 갱신. 다른 단계와 저장소 루트 파일은 변경하지 않음.
- A–E의 **추출본 정적 실측 8/8**와 F의 **공식·인게임 미인증 8/8**을 혼동하지 않는다. 전체 A–G 공식 완료율을 산출하지 않는다.
- 다음 번호: `TEX10-R002` — 다음 수정 전 GitHub STATE SHA·head·경로 재확인. 신규 증거 없이 버전 추가하지 않는다.
