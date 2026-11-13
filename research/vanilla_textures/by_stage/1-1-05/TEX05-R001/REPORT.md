# TEX05-R001 — Minecraft Java 1.21.11 / 유리 6종 정적 소스 연구 보고서

> 2026-11-13 / 담당 1-1-05. 직전 TEX05-R000은 계획 상태였으며 이 결과는 **실제로 신규 재검증한 자료**다. 전역 연구 버전 **v38 유지**, 전체 1단계 공식 완료 0/5 유지. 공식 Mojang client.jar 및 인게임 정적 렌더링은 미확인.

## 검증 분모와 증거 등급

- 고정 범위: `glass`, `red_stained_glass`, `black_stained_glass`, `blue_stained_glass`, `green_stained_glass`, `white_stained_glass` 정확히 6종. 추가 색상/유리 계열은 이 단계 실적으로 계수하지 않는다.
- 실제 GitHub 추출 미러 1.21.11 PNG **6개 바이너리** 읽기 → Pillow로 **1,536개의 RGBA 화소** 직접 디코딩, Python hashlib SHA-256 재계산, PNG 각 청크 IHDR/IDAT/IEND의 저장 CRC32와 zlib 재계산 CRC32 비교. 파일 크기·모드·픽셀 전체 기록 보존.
- 원본 추출 미러 `InventivetalentDev/minecraft-assets`의 `1.21.11` 파일과 이 저장소 `1.21.11/assets/...`의 같은 이름 파일의 **Git blob SHA가 6/6 같음**을 확인. PNG 실제 SHA-256은 v4 레거시 측정 원장의 값과 6/6 일치한다. **Git blob SHA, PNG SHA-256, PNG 청크 CRC32는 서로 다른 체크섬**이다.
- **현재 증거 수준**: `mirror_sha_pixel_checked` + `extracted_static_json_uv_checked`. 공식 JAR 인증 `0/6`, 인게임 정적 검증 `0/6`; 부재를 성공으로 기록하지 않는다.

## A — 과거 출처·중복 검사

- `docs/vanilla_texture_1-1/stages/1-1-05/STATE.json`, `docs/vanilla_texture_1-1/1-1-05_유리.md`, `research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv`, `research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv`의 항목 이름, ID, 경로, v4 SHA를 각각 교차했다. 6종 ID·경로·SHA 모두 고유하고 일치.
- v35~v38의 종/케이크/벌·화로 계열·오크 선반 등의 개별 성과를 이번 유리 항목 측정으로 계산하지 않는다. 기존 v4의 '측정 6개'와 이번 독립 실측 '6개'도 같은 표본이므로 전체 신규 텍스처 12개로 합산하지 않는다.

## B — PNG 바이너리/CRC/해상도

- 전부 **16×16 PNG**이며 Pillow로 읽기 성공. black/white stained PNG는 원본 채널이 **LA(그레이스케일+알파)**, 나머지는 RGBA. 정량 분석은 전부 RGBA로 변환했다.
- 6/6 모든 `IHDR`, `IDAT`, `IEND`의 CRC32를 검증했다. 다음 IDAT CRC는 파일 SHA와 별개.
- 6/6 PNG SHA-256 재계산은 `SOURCE_LEDGER.csv`의 `expected_v4_sha256`과 모두 정확히 일치.

| PNG | bytes | 원래 모드 | IDAT CRC32 | alpha=0 | 1..254 | 255 | 가시 RGB |
|---|---:|---|---|---:|---:|---:|---|
| `glass` | 147 | RGBA | `4a84b6dd` | 191 | 0 | 65 | #D0EAE9(31) · #A8D0D9(11) · #7BAEB7(4) · #8BC1CD(19) |
| `red_stained_glass` | 106 | RGBA | `c8a41131` | 0 | 256 | 0 | #993333 |
| `black_stained_glass` | 100 | LA | `5e5bf7d0` | 0 | 256 | 0 | #191919 |
| `blue_stained_glass` | 106 | RGBA | `b5d007d7` | 0 | 256 | 0 | #334CB2 |
| `green_stained_glass` | 105 | RGBA | `babd3a02` | 0 | 256 | 0 | #667F33 |
| `white_stained_glass` | 100 | LA | `08e37e23` | 0 | 256 | 0 | #FFFFFF |

## C — RGBA·명암·반복 정량 비교

- `glass`: 알파 0=191, 알파 255=65, 부분 알파 0, 평균 알파 **64.74609375**. 가시 RGB 4개, 합계 65개. alpha=0인 191개의 저장된 RGB는 #808080이지만 **보이는 팔레트로 세면 안 된다**. 보이는 픽셀의 표준 RGB 가중 휘도 평균은 약 **206.1934**.
- 착색 5종: 각 PNG의 단일 RGB는 red #993333, black #191919, blue #334CB2, green #667F33, white #FFFFFF. 전 화소의 alpha 분포가 각각 **102=191개, 155=5개, 163=60개**이고 alpha 0/255는 없음. 평균 alpha **117.33203125**. 가시 RGB 평균 휘도는 차례로 72.6852/25.0000/78.0494/116.1978/255.0000.
- 5종의 alpha 16×16 시퀀스가 **완전히 동일**함을 화소별 비교. 색상 대신 투명도의 명암 대비로 윤곽과 가운데 강조 5개를 공유한다.
- 정적 PNG 패턴 반복은 상하좌우 경계 및 단일 16×16 샘플에서 확인했을 뿐, 실게임 반복 텍스처 샘플러·조명 방식이 같다고 추론하지 않는다.

## D1 — 무색·착색 팔레트/알파

- 무색은 완전 투명 191과 불투명 65의 두 값만 사용. 착색은 완전 투명 0, 불투명 0, 세 종류의 부분 투명 값만 사용.
- 착색 유리의 중앙이 유리처럼 보이는 이유를 alpha=0인 '구멍'으로 해석하면 오류. **중앙은 alpha 102**다.

## D2 — 실제 윤곽·모서리·투명 구멍 좌표

- 좌표 원점은 PNG 좌상단 (0,0). `glass` 사방 테두리 60픽셀은 전부 alpha=255; 내부 14×14=196픽셀에서 다섯 강조점만 alpha=255, 나머지 **191픽셀 모두 alpha=0**.
- 다섯 점 좌표: **(4,2), (3,3), (2,4), (13,12), (12,13)**.
- 착색 5종에서는 동일 테두리 60픽셀 alpha=163, 동일 강조 5픽셀 alpha=155, 중앙 나머지 191픽셀 alpha=102. 무색 glass의 65개 불투명 좌표와 착색 유리의 '테두리+강조점' 좌표가 동일.
- **D2의 원본 화소 증거**: `ALPHA_MASKS.md` 16×16 표현 및 `PIXEL_RGBA.csv` 원본 채널 1,536행. 투명 픽셀의 RGB 값과 알파는 분리해 보관.

## E — 블록/아이템 모델 JSON·상속·상태·UV

- 6개의 blockstates `assets/minecraft/blockstates/<texture_id>.json`: 공통 `variants: { "": { "model": "minecraft:block/<texture_id>" } }`이고 분기/회전 없음.
- 6개 leaf block 모델 `assets/minecraft/models/block/<texture_id>.json`: `parent: "minecraft:block/cube_all"`, `textures.all: "minecraft:block/<texture_id>"`이다.
- `cube_all`(Git blob `fa2f9e776173224b2b523b8b537c695b921267f6`)은 `block/cube`를 상속하며 `down`, `up`, `north`, `east`, `south`, `west`, `particle`을 `#all`로 바인딩.
- `cube`(Git blob `1b9780b479aee527f79bde950656b82f1524128b`)는 요소 하나 `from=[0,0,0], to=[16,16,16]`; 원본 6면에 texture `#<face>`, 같은 이름의 `cullface`를 선언. 정적인 상속 해석으로 각 모델 **6면 전부 같은 PNG** 참조.
- 원본 face에 명시적 `uv`는 **0/36**이며 완전 정육면체의 기하에서 도출되는 기본 full-face UV 영역은 **[0,0,16,16]**. 소스 내 별도의 이미지 좌표·UV atlas rectangle은 없고 **인게임 UV 회전·투명 정렬·면 제거 동작은 미검증**이다.
- `assets/minecraft/items/<texture_id>.json` 6개가 각각 `minecraft:model` 형식으로 동일 `minecraft:block/<texture_id>` 모델을 참조함을 확인.
- 정적 면 바인딩은 6 PNG×6면 = **36건**, 면×텍스처 참조 개수 9,216 texel-uses(256×36)는 단순 참조 중복 계산으로 **원본 고유 픽셀 1,536개**와 혼동 금지. `UV_FACE_LEDGER.csv`에 전 36면 저장.

## D3/F — 공식 런타임 전용, 미검증

- 본 저장소의 `1.21.11/` 추출 PNG/JSON과 미러의 동일성은 확인했지만 Mojang 공식 `client.jar` 바이너리와 공식 버전 다운로드 SHA·검증 메타데이터에 연결해 인증하지 못했다. **official_client_jar_authenticated = 0/6**.
- 실제 실행한 게임의 정적 캡처/화면·모델 면 정렬/인접 컬링·render layer·조명 측정은 **0/6**. D3·F는 `pending`으로 유지. PNG의 알파만으로 게임 렌더 파이프라인을 확정하지 않는다.
- 애니메이션, 이동, 키프레임, 프레임 변경 연구는 사용자가 해제할 때까지 **전면 보류**. 기존 동적 조사 기록은 삭제하지 않음.

## G — 저장 및 인수인계

- `SOURCE_LEDGER.csv`: 여섯 원본의 경로/미러 URL/원본 SHA/미러와 프로젝트 Git blob SHA/크기/CRC/모델 및 blockstate·item descriptor Git blob SHA.
- `SUMMARY.json`: 분모를 분명히 한 범위와 검증 상태.
- `ALPHA_MASKS.md`: 좌표 포함 상세 16×16 마스크.
- `PIXEL_RGBA.csv`: 6×256행, R·G·B·A 원본 채널(투명 픽셀 포함).
- `UV_FACE_LEDGER.csv`: 6×6 정적 면별 바인딩·원본 명시 UV 부재·유도 UV.
- 이 파일 `REPORT.md`, 단계 전용 `STATE.json`, `HANDOFF.md`만 갱신한다. 공유 루트, 다른 단계, 기존 R000과 v38 변경 금지.

**다음 계획 버전: `TEX05-R002` (작업 개시 전에 GitHub `STATE.json` SHA와 다음 버전 경로 존재 확인).** 공식 client.jar 접근 시 원본 인증 후 F/D3를 별도 검증하고, 인게임 정적 관측의 캡처·설정·버전 증거가 없으면 그대로 미검증으로 유지한다.
