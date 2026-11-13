# 1-1-05 — 유리 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX05-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

**현재 최신 실제 검사 버전: `TEX05-R002` (2026-11-13). 다음 후보 `TEX05-R003`.** 이 문서의 기존 R000 '미시작' 기술은 최초 계획 당시의 이력이며 현재 상태는 하단 R001 결과와 `STATE.json`을 우선한다.

## 연구 목표와 정확한 표본

- 담당: **1-1-05 / 유리 / 6개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-05 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-05_유리.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-05/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 6/6 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

6개가 원본 파일 표본이다. PNG의 알파가 실제 월드의 투명 렌더러 동작을 직접 증명하지는 않음.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-05-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-05-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-05-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-05-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-05-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-05-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-05-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 무색/착색 유리 팔레트와 알파 0·255·부분투명 분포
- **D2:** 윤곽·모서리와 투명 구멍의 실제 픽셀 위치
- **D3:** 인게임 정적 render layer/정렬은 공식 런타임에서만 검증

## 검토할 정확한 텍스처 6개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-05-001` | `glass` | `cb89c706dce86eac3123cef087d359b5f23098b658a468fb91662b4a9922bcd0` | `assets/minecraft/textures/block/glass.png` |
| `1-1-05-002` | `red_stained_glass` | `4520f85fee79972191217d623c8b38522cacf74cb7c71113c0a6240d3b1f2ad2` | `assets/minecraft/textures/block/red_stained_glass.png` |
| `1-1-05-003` | `black_stained_glass` | `62c705812949f0372dcc2fa82a5d89f7028ba1d9b3bd38765613e344f34f5b1c` | `assets/minecraft/textures/block/black_stained_glass.png` |
| `1-1-05-004` | `blue_stained_glass` | `7d6cfe98ddc5d975b3bcf5f9cffc008f90db94d5d981ef440f7b68e8267ae247` | `assets/minecraft/textures/block/blue_stained_glass.png` |
| `1-1-05-005` | `green_stained_glass` | `dc82be445bd9c7cf158bd57651d51bfef400310f2ad4937fe1e5b1c60b4f5916` | `assets/minecraft/textures/block/green_stained_glass.png` |
| `1-1-05-006` | `white_stained_glass` | `2d4504957fa123a6e9f35d93e05f94fb053ec213541f01fcecbc0097eaa5df75` | `assets/minecraft/textures/block/white_stained_glass.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 최초 **`TEX05-R000`**: 단계 분리/작업 안내만 저장한 계획 상태(역사적 이력).
- 이전 불변 검증 결과: **`TEX05-R001`**; 보존 위치 `research/vanilla_textures/by_stage/1-1-05/TEX05-R001/`. 최신 신규 분석 **`TEX05-R002`**; 새 증거 발생 시 다음 **`TEX05-R003`**(쓰기 전 STATE 재확인).
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-05/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.

## TEX05-R001 — 2026-11-13 독립 실측 완료 부분과 다음 작업

- **A**: v4 150 측정 원장 + 150 번호 원장 + 본 분류 STATE의 동일 6개 경로·SHA 재대조. 새 샘플을 더하지 않음.
- **B**: GitHub 1.21.11 미러에서 6개 PNG 원본 바이트를 실제 취득하고 SHA-256을 재계산해 v4 기록 6/6 일치. IHDR/IDAT/IEND CRC 6/6 확인. 저장소 자체의 `1.21.11/`와 Git blob SHA 동일.
- **C/D1**: 6×256=1,536 실제 RGBA 기록. 무색 glass 알파0 191·불투명65, 착색 5종은 각각 알파102 191·155 5·163 60(완전투명 없음). 모든 착색 유리의 알파 배열 일치.
- **D2**: 16×16 마스크와 좌표 증거 확보. 내부 강조 5픽셀 (4,2), (3,3), (2,4), (13,12), (12,13). 자세한 전체 픽셀은 새 원장 참조.
- **E**: leaf 모델 6, blockstate 6, item descriptors 6, 부모 `cube_all → cube` 소스 검사. 36 정적 면의 유도 전체 UV [0,0,16,16]. 원본에 명시 face UV 0/36.
- **D3/F — pending**: Mojang 공식 client.jar 인증·인게임 정적 render layer/정렬 확인 모두 0/6. 미러 SHA가 공식 인증을 대체하지 않는다. **애니메이션은 계속 전면 보류**.
- **G**: [보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R001/REPORT.md) · [소스 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R001/SOURCE_LEDGER.csv) · [요약 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R001/SUMMARY.json) · [좌표 마스크](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R001/ALPHA_MASKS.md) · [원본 픽셀 1536행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R001/PIXEL_RGBA.csv) · [정적 UV 36행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R001/UV_FACE_LEDGER.csv).

최신 단계 상태: **정적 소스 재검증 6/6**, **공식 JAR/인게임 0/6**, **A–G 공식 완료 0/6**; 전체 전역 v38과 전체 완료 0/5는 불변. 다음 버전 **TEX05-R002**는 STATE, SHA, 다음 릴리스 경로 재검사 후 새 실증이 있을 때만 개시한다.

## TEX05-R002 — 2026-11-13 이어서 수행한 신규 실측과 공식 검증 경계

- 기존 6종 PNG를 **별도 Pillow 분석**으로 다시 재해시·RGBA 전수 판독. 동일 1,536픽셀 재검산이므로 신규 고유 파일/픽셀을 6개/1,536개 추가 계산하지 않음.
- 새 경계 시험: glass 좌우 RGBA 일치 **2/16**, 상하 **1/16**, 좌우 RGB 절댓값 평균 **40.9583**, 상하 **38.4583**(v4 레거시 경계 기록과 일치). 착색 5종은 좌우/상하 각 RGBA **16/16** 일치, RGB MAE 0. 여섯 원본 모두 가장자리 알파는 양방향 16/16 일치, 가로/세로 내부 인접 알파 변화 각각 38/240.
- PrismLauncher `meta-upstream` 제3자 메타데이터 미러에서 1.21.11 매니페스트와 1.21.11 JSON을 직접 읽음. **매니페스트가 지정한 버전 JSON SHA-1 `812ee7fd...`와 복제 JSON 실제 SHA-1 `eecf9227...` 불일치**. 단순 미러는 공식 인증이 아님. 사본이 기록한 클라이언트 후보: SHA1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`, 길이 **31,152,600 bytes**.
- 공식 Mojang HTTPS 메타데이터와 클라이언트 JAR 직접 접근 실패. 따라서 F 공식 `client.jar` 인증 **0/6**, D3 인게임 정적 render layer/정렬 **0/6** 그대로 **pending**. 무색/착색 원본 PNG 측정과 실제 렌더 실험을 절대로 혼동하지 않음.
- 공식 자료가 제공될 때 사용 가능한 [독립 JAR 검증 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R002/VERIFY_OFFICIAL_CLIENT.py)는 공식 Mojang 메타데이터를 실제 조회하고 로컬 `client.jar`의 SHA1·길이·내부 6 PNG SHA를 검사하도록 준비. **이번에 공식 JAR로 검사했다는 뜻 아님**.
- 새 결과: [R002 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R002/REPORT.md) · [6종 경계 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R002/EDGE_RGBA_AUDIT.csv) · [요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R002/SUMMARY.json) · [메타데이터 출처·불일치 증거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R002/METADATA_PROVENANCE.json) · [원본 PNG 재실측 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R002/REPRODUCE_EDGE_AUDIT.py).
- 상위 전역 **v38**과 공통 완료 0/5는 변경하지 않았으며, 애니메이션·동작·실제 가구 제작은 여전히 제외. 다음 단계 고유번호는 `TEX05-R003`을 시작 전에 GitHub에서 확인해야 한다.
