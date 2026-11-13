# 1-1-05 — 유리 별도 채팅 인수인계

> **현재 우선 적용 정책 (2026-11-13): 사용자가 "공식 인증 빼"라고 지시함.** `1-1-05` 유리 연구에서는 Mojang 공식 `client.jar` 전체 SHA-1·공식 버전 메타데이터 인증을 **연구 범위에서 제외**하고, 완료 조건·다음 할 일·진행률 분모에 넣지 않는다. **인증 완료를 뜻하지 않는다.** 이전 R001~R004 보고서의 `official pending` 등은 작성 당시 이력으로 보존한다. 현재 연구는 **사용자 제공 `1.21.11/` 파일 직접 분석 / 기존 미러 교차검증 / 실제 인게임 정적 렌더 검증**으로 계속한다. 정적 소스만으로 인게임 검증을 완료 판정하지 않는다. 애니메이션·PZ 변환·실제 가구 모델 제작은 계속 제외. **현재 `TEX05-R004`, 다음 검증 증거 버전 `TEX05-R005`, 전역 `v38` 유지.**

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX05-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

**현재 최신 실제 검사 버전: `TEX05-R004` (2026-11-13). 다음 후보 `TEX05-R005`.** 이 문서의 기존 R000 '미시작' 기술은 최초 계획 당시의 이력이며 현재 상태는 하단 R001 결과와 `STATE.json`을 우선한다.

> **현재 적용 출처 지시(2026-11-13 / TEX05-R003):** 저장소 `1.21.11/`는 사용자가 Minecraft Java 1.21.11 JAR을 직접 추출해 업로드했다고 밝힌 **사용자 제공 추출본**이며 본 단계의 **1순위 원본 분석 자료**다. 별도 `InventivetalentDev/minecraft-assets`는 교차 검증 대상일 뿐이다. 추출본 검증/미러 대조/공식 Mojang JAR SHA-1 인증/인게임 렌더 검증의 **네 증거 수준을 엄격히 분리**한다. 이전 R001·R002 기록은 당대 출처 기술을 포함한 불변 이력이며 현행 출처 우선순위는 R003을 따른다.\n\n## 연구 목표와 정확한 표본

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
- 불변 선행 검증 **`TEX05-R001`**, **`TEX05-R002`**, **`TEX05-R003`**를 모두 보존. 현재 최신 신규 분석 **`TEX05-R004`**; 새 실증 발생 시 다음 **`TEX05-R005`**(쓰기 전 STATE 재확인).
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

## TEX05-R003 — 사용자 제공 원본 추출본 우선 출처 정정·27파일 직접 검증 (2026-11-13)

- 사용자 제공 `sanato-nb/Minecraft_Furniture_Style_Research/main/1.21.11/`을 **1순위**로 실제 GitHub 파일 취득. 사용자 설명에 따라 **직접 JAR 압축 해제본**으로 기록하되 **Mojang 공식 배포 무결성 인증과 혼동하지 않음**.
- 정적 소스 **27개** 직접 검수: PNG 6·블록 leaf 모델 6·blockstate 6·item descriptor 6·공통 부모 모델 `cube_all/cube/block` 3. 기존 미러 `InventivetalentDev/minecraft-assets` Git ref `1.21.11`의 대응 파일과 Git blob SHA **27/27 일치**. PNG는 실제 base64 원본 디코딩·Python SHA-256 **6/6 기존 v4 일치**.
- 사용자 소스에서 실제 참조·상속 확인: `<glass-id> → cube_all → cube → block`. 공통 `block.json`은 `gui_light=side`와 7종 `display` 포즈를 정의. 6종의 기본 blockstate→leaf→texture 및 item 참조 6/6 정상, `cube`의 정육면체 6면·cullface 36개 정적 결합, 명시 UV 없음.
- **기록 오류 1건 확인**: R001 `SOURCE_LEDGER.csv`의 `green_stained_glass` `blockstate_git_blob_sha`가 39자리 `ca4fec4067cffd89000ee64251f878bf0d530a8`로 끝나지만, 사용자 추출본과 미러의 실제 동일 40자리 Git blob은 `ca4fec4067cffd89000ee64251f878bf0d530a8a`. **R001 자체는 수정하지 않고 R003 errata에 정정**. 다른 R001 SHA 컬럼의 자리수 오류 없음.
- **네 검증 기준**: (1) 사용자 추출본 정적 소스 **27/27**, (2) 비공식 미러 Git blob **27/27**, (3) Mojang 공식 전체 JAR SHA-1 인증 **0/6 pending**, (4) 인게임 정적 렌더링 **0/6 pending**. 첫 두 증거가 세 번째·네 번째의 대체가 될 수 없음.
- 이번 27개는 서로 다른 27종 텍스처를 뜻하지 않음. 고유 PNG 표본 **6개**, R001 측정 1,536 RGBA·R002 경계 값 재계산 완료량 **추가하지 않음**.
- 새 파일: [R003 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R003/REPORT.md) · [27개 출처 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R003/SOURCE_LEDGER.csv) · [6종 모델 체인 검수](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R003/MODEL_CHAIN_AUDIT.csv) · [R001 지문 오류 불변 정정](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R003/LEGACY_LEDGER_ERRATA.md) · [4층 검증 SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R003/SUMMARY.json).
- 현재 **TEX05-R003**, 다음 고유 증거 버전 **TEX05-R004**. 전체 공통 `v38` 그대로. 애니메이션·PZ 변환·실제 가구 모델링 제외.

## TEX05-R004 — 정적 .mcmeta·blocks atlas·일반 block shader 근거 추가 (2026-11-13)

- 유리 고유 PNG 6개와 1,536 RGBA, 36 정적 면, R003의 27개 추출 소스 검수는 **반복·증가 산정하지 않았다**.
- 사용자 제공 `1.21.11/assets/minecraft/`에서 신규 **4개** 실제 파일 직접 읽기: `textures/block/glass.png.mcmeta`, `atlases/blocks.json`, `shaders/core/block.fsh`, `shaders/core/block.vsh`. 대응하는 비공식 `InventivetalentDev/minecraft-assets@1.21.11`와 **4/4 동일 Git blob SHA 및 동일 원문**. 서로 다른 정적 출처 경로 **총 31개**(R003 27+R004 4).
- 새 재질 고유 정적 설정: `glass.png.mcmeta`는 `texture.mipmap_strategy="mean"`. 착색 5종은 대응 `*.png.mcmeta` 조회 결과 **5/5 없음**. 없다는 사실에서 기본 필터를 추론하지 않음.
- `atlases/blocks.json`: `type=minecraft:directory`, `source=block`, `prefix=block/` 규칙이 기존 6종 모델의 `minecraft:block/<id>`와 **정적 경로 상 합치**. 실제 압축 아틀라스 좌표/패딩은 문서에 없음.
- 일반 블록 `block.fsh`: `Sampler0`과 `#ifdef ALPHA_CUTOUT` 조건부 `discard` 및 `apply_fog`. `block.vsh`: `UV0→texCoord0`, `UV2/Sampler2` 광원맵 샘플을 `vertexColor`에 반영하는 코드 존재. **실제 게임 유리에서 해당 셰이더가 실행되었는지/컷아웃 매크로 활성화·투명 블렌드·정렬·컬링되는지는 전혀 검증되지 않음**.
- 4단계 증거: (1) 사용자 추출본 고유 소스 경로 31건, (2) 미러 동일 Git blob SHA 31건, (3) 공식 `client.jar` SHA-1 **0/6 pending**, (4) 인게임 유리 정적 검증 **0/6 pending**. 공식 완료 A–G 판정 계속 미충족. 기존 공통 `v38` 유지.
- 산출물: [R004 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R004/REPORT.md), [신규 4개 소스 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R004/SOURCE_LEDGER.csv), [유리 6종 메타데이터 매트릭스](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R004/SPRITE_METADATA_MATRIX.csv), [셰이더 증거 제한 문서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R004/STATIC_RESOURCE_CONSTRAINTS.md), [단계 SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R004/SUMMARY.json).
- 다음 고유 릴리스 **TEX05-R005**. 사용자 제공 JAR 추출본 우선, 애니메이션 분석 보류, Project Zomboid 변환 및 실제 가구 3D 모델 제작 제외. 저장 전 HEAD/STATE/새 경로 충돌 검사 필수.

## 작업 기준 변경 — 공식 JAR 인증 제외 (2026-11-13, 버전 번호 증분 없음)

- **유효 지시:** 사용자 요청에 따라 Mojang 원본 JAR SHA-1·공식 배포 메타데이터 인증 **범위 제외(out_of_scope)**. 완료 요구·다음 할 일·미진행률 계산의 필수 조건에서 제거. 이전 미완료 기록을 `verified`로 바꾸지 않음.
- 적용되는 세 증거 영역: **① 사용자 제공 `1.21.11/` 실제 PNG/JSON/모델/셰이더 검증 ② 기존 비공식 미러와 교차검증 ③ 인게임 정적 렌더 증거가 실제 존재할 때에만 검증**.
- 과거 **TEX05-R001~R004** 결과·원장·커밋을 보존하고, `TEX05-R005`는 새로운 *분석 증거*가 발생할 때 생성. 이번은 **정책·인수인계만 갱신했으므로 R004 유지**.
- F 단계는 **인게임 정적 검증만 남고 공식 JAR 인증 절차는 요구하지 않음**. 인게임 테스트 데이터가 없으므로 인게임 부분은 계속 pending.
- 다른 연구 단계, 루트 공통 문서, 전체 `v38`, 애니메이션 보류/제외 조건은 수정하지 않음.

## TEX05-R005 — 사용자 추출본 6 PNG 저장 형식·고알파 프레임 연결성 분석 (2026-11-13)

- **최신 연구 릴리스:** [TEX05-R005 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R005/REPORT.md) · [6종 근거 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R005/SOURCE_LEDGER.csv) · [6종 정량 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R005/PNG_ALPHA_TOPOLOGY.csv) · [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R005/SUMMARY.json) · [재현 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-05/TEX05-R005/REPRODUCE_STATIC_TOPOLOGY.py).
- 사용자 제공 `1.21.11/assets/minecraft/textures/block/`의 기존 6 PNG 바이트를 다시 직접 읽고 **실제 SHA-256/PNG CRC 6/6 일치**. 새로운 고유 PNG나 정적 경로는 **0**, 기존 31개 고유 정적 경로 **유지**. R001 1,536 RGBA·36면 UV는 계승, 신규 가산 금지.
- IHDR 16×16·8bit: 검정·흰색 착색 유리는 PNG grayscale+alpha(color type 4), 무색·빨강·파랑·초록은 RGBA(color type 6). 저장 포맷 차이는 실제 렌더 방식 증거가 아님.
- 높은 알파 판정(`glass A=255`; 착색 5종 `A>=155`)에서 6종 모두 동일한 65픽셀 마스크. **4-연결 성분 크기 [60,1,1,1,1,1]** = 바깥 프레임 60픽셀과 내부 단독 강조점 5개. 각 PNG마다 outer border 60/60. 기존 D2 픽셀 좌표와 동일하지만 연결 성분 수치는 신규 추가 실측.
- 비중첩 2×2 산술 알파 평균 proxy(가상 8×8): `glass` 최소 0/최대 191.25, 착색 5개 각각 최소 102/최대 147.75. **실제 게임의 밉맵 계산·LOD·셰이더·투명 정렬을 검증한 것이 아님**. R004 `glass.png.mcmeta`의 `mean`은 명시적 정적 설정일 뿐 동작 수식 단정 금지.
- 실제 인게임 정적 렌더 **0/6 pending** 유지. Mojang 공식 전체 JAR 인증은 사용자 정책상 **out of scope**이며 검증 성공이 아니다.
- 새 분석 증거 발생 시 라이브 STATE를 다시 확인하여 다음 단계 전용 `TEX05-R006`을 사용. 기존 R000–R005 변경 금지. 전체 `v38`과 타 단계, 애니메이션 보류·PZ 변환/가구 제작 제외 유지.
