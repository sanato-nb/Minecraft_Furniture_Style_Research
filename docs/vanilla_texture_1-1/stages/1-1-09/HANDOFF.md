# 1-1-09 — 토양·지면 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 현재 단계 버전 **`TEX09-R004` (잔디 측면 오버레이 알파·눈 측면 픽셀 정적 검사)** · 통합 체크포인트 **`v38` 유지** · **2026-11-13부터 1-1-09에서는 Mojang 공식 JAR 인증을 연구 요구사항에서 제외**.

## 연구 목표와 정확한 표본

- 담당: **1-1-09 / 토양·지면 / 9개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-09 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-09_토양지면.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-09/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 9/9 항목의 측정 기록 존재**; 이번 단계에서는 A–E의 미러 소스 정적 검사를 9종 모두 수행했고 G를 기록했다. 공식 F는 보류. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

모델링 응용 전 실제 사용 재질과 표본 성격을 분리; 생물군계의 색상 차이는 원본 PNG의 직접 관측이 아님.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-09-A | A 기존 출처·파일·중복 대조 | R001: 9종 v4·번호 원장 대조 확인 |
| 1-1-09-B | B PNG 실제 바이너리·SHA·CRC 검증 | R001: 9/9 미러 바이너리 확인 |
| 1-1-09-C | C RGBA·밝기·알파·반복 정량 검사 | R001: RGBA 9/9; R002: 회전 이음새 69건 |
| 1-1-09-D | D 재질 특화 세부 검사 | R002: 정적 D1–D3 보강; 실제 틴트/인게임 보류 |
| 1-1-09-E | E 정적 모델 JSON·UV·상태 연결 | R002: 면별 연결 70건·진흙 벽돌 실화소 36건 |
| 1-1-09-F | F 인게임 정적 렌더 검증 (공식 인증 제외) | 인게임 정적 렌더 미검증. Mojang JAR 인증은 사용자 지시로 대상 제외 |
| 1-1-09-G | G 근거 보고서·단계 인수인계 저장 | R001·R002 증거 원장 및 STATE 저장 |

**D 재질 특화 기준**

- **D1:** 흙·자갈·진흙 등의 명도 및 반복 무늬
- **D2:** 좌우/상하 이음새·고주파 패턴
- **D3:** grass/podzol PNG와 인게임 tint·주변 블록 효과 구분

## 검토할 정확한 텍스처 9개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-09-001` | `dirt` | `67197d5371efc3ca1638217c38349665dbd5a977b47bfb20075c858dff87d510` | `assets/minecraft/textures/block/dirt.png` |
| `1-1-09-002` | `coarse_dirt` | `6889a193decb2c38cd8559456693c15192917c7b917d6ef9c3c2e142f7819ad4` | `assets/minecraft/textures/block/coarse_dirt.png` |
| `1-1-09-003` | `rooted_dirt` | `3c59420f80c58794b49f822fb9b251779250b759f5c12111fa29f772a635f42b` | `assets/minecraft/textures/block/rooted_dirt.png` |
| `1-1-09-004` | `mud` | `3ddc6e47abc12db1e2e85938da5d0b0d49e0357d8c3424b069f521741ec42d23` | `assets/minecraft/textures/block/mud.png` |
| `1-1-09-005` | `packed_mud` | `143f1729042262d675f0eefe5a8b2704c5d5837f8526aa36b8930328dfb141bf` | `assets/minecraft/textures/block/packed_mud.png` |
| `1-1-09-006` | `mud_bricks` | `b9d94455caf0651b7ff777f2f85a92f4d67d04ae669cd4f65c308595ec9d38fa` | `assets/minecraft/textures/block/mud_bricks.png` |
| `1-1-09-007` | `gravel` | `bc1558fa64b238fabca4cc957e61c232337d410495784b106676bf73e52e16e0` | `assets/minecraft/textures/block/gravel.png` |
| `1-1-09-008` | `grass_block_top` | `52f44b64ce884a13dfe35e4b4da2e35898b790dd4d7a5ea536f1b0c0d56d29b4` | `assets/minecraft/textures/block/grass_block_top.png` |
| `1-1-09-009` | `podzol_top` | `598072d5a4db38ec4ea081a584a2de6b5960785bc2287e18e93427c7433c5d56` | `assets/minecraft/textures/block/podzol_top.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 최초 **`TEX09-R000`**는 계획, **R001**은 미러 PNG 실측, **R002**는 정적 UV/회전, **R003**은 사용자 제공 JAR 추출본의 9개 PNG·26개 JSON 교차 검증. 공식/인게임 0.
- 최신 추가 소스 검사: **`TEX09-R004`**; 경로 `research/vanilla_textures/by_stage/1-1-09/TEX09-R004/`. 다음 후보 `TEX09-R005` (시작 전 STATE 재검증).
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-09/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.


## TEX09-R001 신규 검증 및 다음 인수인계 (2026-11-13)

- [TEX09-R001 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/REPORT.md) · [원본 근거 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/SOURCE_LEDGER.csv) · [픽셀 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/PIXEL_METRICS.csv) · [면별 UV 증거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/UV_FACE_EVIDENCE.csv) · [요약 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R001/SUMMARY.json).
- **이번 새 바이너리 확인 9/9**: 미러 ref `1.21.11` 9개 PNG 바이트 SHA-256, CRC32/PNG 디코드, RGBA·명도·이음새 분석 9/9. v4 측정 9/9은 **과거 자료**로만 집계.
- **모델/UV 9/9 (미러 소스 단계)**: 전체 54면 연결 행. `mud_bricks` 북/서 미러 UV, `grass_block_top` 틴트 인덱스, `podzol_top` 무틴트 상단 모델 관계 확인.
- **미완료 F 공식 client.jar 인증 0/9, 실제 인게임 정적 렌더 0/9.** 색상·주변 블록 및 눈 상태는 실제 게임과 미대조. 가짜 공식 인증 금지.
- **현재 버전 TEX09-R001 / 다음 후보 TEX09-R002**. 매 수정 전에 실제 `STATE.json` SHA, HEAD, 새 릴리스 경로 재확인. 다른 채팅과 충돌 시 **덮어쓰지 않음**. `v38`는 전역 최신 그대로.
- 기존 A–G 초기 표는 초기 R000 체크포인트 이력으로 보존. **이번 이후 상태는 아래 신규 검증과 `STATE.json` 최신 `phases` 값이 우선**. 애니메이션 전면 보류.


## TEX09-R002 실제 신규 근거 및 미완료 인수인계 (2026-11-13)

- [R002 상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R002/REPORT.md), [70면 정적 출처 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R002/STATIC_FACE_RESOLUTION_70.csv), [회전 이음새 69쌍](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R002/ROTATION_SEAM_PAIRS.csv), [회전별 9종 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R002/ROTATION_SUMMARY.csv), [mud_bricks UV 화소 36건](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R002/MUD_BRICKS_UV_PIXEL_SAMPLES.csv), [SOURCE_LEDGER](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R002/SOURCE_LEDGER.csv), [SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R002/SUMMARY.json).
- **9개 고정 PNG 원본 다시 해시 일치** (기존 R001 측정 파일 재사용, 신규 텍스처 0). R002 새 검증량은 **70면 모델 요소/상태 연결, 69 인접 회전 시뮬레이션, 36 UV 화소 대응**. 이 수량을 독립 PNG나 공식 검증 완료 개수로 가산 금지.
- **D3** 일반 grass 상단 및 측면 overlay `tintindex=0`, snowy=true 별도 상속 모델 및 podzol snowy=true 모델 연결을 소스 JSON에서 확인. 해당 오버레이 PNG 및 게임 화면의 실제 컬러는 별도 미검증.
- **공식 JAR 예상 해시 참조만 확보:** 제3자 캐시 메타데이터의 SHA-1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`, 크기 31,152,600바이트. Mojang 서버의 실제 JAR 수신·해시 확인 및 9종 공식 PNG 대조는 **0/9**. 인게임 정적 렌더도 **0/9**.
- R001 보고서의 PNG 총 바이트 부분에는 잘못 출력된 문자열이 남아 있으나 불변 릴리스라 수정하지 않았고, R002에서 **2,198바이트**로 정정했다.
- **현재 R002 / 다음 예상 `TEX09-R003`**. 현재 SHA 및 HEAD를 다음 채팅이 먼저 읽고 버전 충돌 재검사. `v38` 유지, 애니메이션 전면 보류, 다른 단계/루트 수정 금지.


## TEX09-R003 — 사용자 제공 1.21.11/ 추출본 검증 및 다음 인수인계 (2026-11-13)

사용자가 `1.21.11/` 폴더를 직접 보유한 Minecraft Java 1.21.11 JAR 압축 해제본이라고 밝힘. 이제 이 자료를 분석 우선 출처로 삼되, **공식 Mojang JAR의 SHA-1 인증 또는 인게임 사실과 혼동하면 안 됨**.

- [R003 상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R003/REPORT.md), [40개 파일 경로·Git blob·해시 대조 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R003/SOURCE_LEDGER.csv), [9개 블록-상태-모델 연결](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R003/MODEL_BLOCKSTATE_LINKAGE.csv), [4계층 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R003/SUMMARY.json).
- 고정 범위 **1-1-09 PNG 9개**: 사용자 추출본에서 직접 다운로드/디코드한 PNG SHA-256=과거 v4=미러 **9/9**, PNG 청크 CRC 9/9. 기존 R001 픽셀 분석 값은 **바이트 동일성으로 재사용**하며 이번 새 표본 0개. 16×16×9=2,304픽셀.
- 사용자 제공 **블록상태 9개 + 선택 모델 9개 + 부모/상태/대체 모델 8개 = JSON 26개**를 직접 파싱; 동일 파일의 미러 blob과 26/26 일치. `mud_bricks` 북/서 UV `[16,0,0,16]`, `grass_block` 상단/측면 overlay `tintindex:0`, `podzol snowy=true`의 `grass_block_snow` 선택을 사용자 제공 JSON에서 확인.
- **보조 PNG 5개**: 잔디 측면/오버레이/눈, 포드졸 측면, `colormap/grass.png`의 출처 비교만 수행. 9개 공식 단계 표본에 추가하지 않음. 색맵 파일 존재가 곧 인게임 tint RGB 증명은 아님.
- **분리할 검증 4종:** (1) 사용자 추출본 9 PNG·26 JSON (검증), (2) 미러 교차 검사 (일치), (3) Mojang 공식 JAR SHA-1 및 메타데이터 인증 (미완료), (4) 실제 인게임 정적 렌더 (미완료).
- **현재 R003, 다음 R004 후보**. 추가 커밋 전 최신 `STATE.json`의 revision/SHA와 HEAD를 다시 확인할 것. R001/R002 불변; `v38`와 타 단계 파일 건드리지 말 것. 애니메이션 전면 보류.


## TEX09-R004 — 사용자 추출본 보조 PNG의 알파·눈 측면 분석 (2026-11-13)

- [R004 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R004/REPORT.md), [오버레이 16행 알파 마스크](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R004/GRASS_OVERLAY_MASK_ROWS.csv), [불투명 화소 45건](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R004/GRASS_OVERLAY_VISIBLE_TEXELS.csv), [눈 측면 순백 화소 16건](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R004/SNOW_WHITE_TEXELS.csv), [PNG 재질 측정](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R004/AUXILIARY_TEXTURE_METRICS.csv), [눈 상태 4조합 모델 연결](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R004/STATIC_VARIANT_FACE_CONNECTIONS.csv), [요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R004/SUMMARY.json).
- 기존 **정확한 9개 타깃** 유지. 이번 **2개 보조 PNG만 새로 실제 디코드**: 잔디 오버레이 16×16 중 불투명 45/투명 211, y=0..3에만 분포 (행별 16/15/11/3), 불투명 회색 16종; 눈 측면 256/256 불투명, 순백 16픽셀·고유 RGB 17종. 포드졸 상단은 이전에 계상된 원본을 재확인만 함.
- `grass_block`의 base cube 6면+overlay cube 4면, `tintindex:0`의 출처 및 grass/podzol snowy 상태의 `grass_block_snow` 연결을 사용자 JSON에서 확인. **알파/소스 연결만으로 실제 바이옴 RGB·조명·장면을 확정하지 않음**.
- **공식 JAR 인증 0/9, 인게임 정적 검증 0/9**, 애니메이션 보류. R001/R002/R003 불변, 전체 `v38` 및 다른 단계 파일 미수정.
- **현재 `TEX09-R004`, 다음 `TEX09-R005` 후보**. 다음 작업 전 `STATE.json`과 HEAD를 반드시 재읽어 충돌 방지.


## 2026-11-13 — 사용자 요청에 따른 연구 기준 변경 (버전 증가 없음)

사용자가 **“공식 인증 빼”**라고 지시했다. 이 날부터 **이 채팅 담당 단계 `1-1-09`에서는 Mojang 공식 `client.jar` SHA-1 인증, Mojang 공식 버전 매니페스트 확인 및 공식 원본 인증 완료율을 필수/후속 작업에서 제외한다.** 공식 인증을 건너뛰었다고 완료 처리하는 것도 금지한다.

진행할 연구는 (1) 사용자가 제공한 `1.21.11/` 추출본의 실제 PNG·JSON·모델·UV 및 정적 화소 검사, (2) 필요할 때 기존 비공식 미러와 바이트/내용 교차 검증, (3) 확보 가능한 경우 실제 게임의 **정적** 바이옴 틴트·눈·조명·인접 블록 렌더 검증이다. 인게임 증거가 없으면 해당 항목은 미검증으로 유지한다.

- 과거 `TEX09-R001`~`R004`의 기록/원장/인증 여부는 역사적 사실로 **불변 보존**. 과거 보고서 중 “공식 인증 필요/보류”라고 한 부분은 그 시점의 작업 규칙이며, **현재 적용되는 범위 규칙은 이 최신 항목이 우선**한다.
- **이번 변경은 연구 방식 지시의 갱신이지 새로운 바이너리·픽셀 검증이 아니므로 버전을 올리지 않는다.** 현재 `TEX09-R004`, 다음 신규 실측 버전 `TEX09-R005` 그대로 유지.
- 공통 `ISOLATED_CHAT_VERSIONING.md`는 다른 단계를 건드리지 않기 위해 수정하지 않았다. `1-1-09` 한정 사용자 지시가 해당 문서의 기존 F단계 공식 인증 기본값보다 우선한다. 다른 단계, 통합 `v38`, 애니메이션 보류 및 범위 제외 규칙 모두 그대로.

## TEX09-R005 — 사용자 grass colormap RGB 삼각영역 및 정적 grass/podzol/snow tint·UV 경로 (2026-11-13)

- [상세 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R005/REPORT.md), [256행 colormap 검사](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R005/COLORMAP_GRASS_ROW_AUDIT.csv), [RGB 실제 샘플](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R005/COLORMAP_GRASS_PIXEL_SAMPLES.csv), [정적 face 28행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R005/STATIC_COLOR_FACE_LINKS.csv), [소스 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R005/SOURCE_LEDGER.csv), [요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-09/TEX09-R005/SUMMARY.json).
- 사용자 제공 1.21.11/assets/minecraft/textures/colormap/grass.png **1개 보조 PNG의 65,536 RGBA 픽셀 신규 디코드**. PNG CRC 3/3·zlib Adler 및 SHA-256 대조. x>y인 32,640 픽셀 전부 흰색, x≤y인 32,896 픽셀 전부 비순백, 고유 RGB 4,536. 이 보조 PNG 파일 경로/Git blob은 R003에 이미 기록되어 있어 새로 발견한 파일로 중복 가산하지 않음.
- 원본 상태·모델 JSON **8개 재파싱(신규 JSON 0)**으로 grass/podzol snowy=false/true 총 4상태 및 28개 면별 texture·UV·tint·cullface 연결을 파생 정리. 일반 grass 10면 중 UV 명시 10면과 tintindex=0 5면(상단 1/측면 오버레이4), 나머지 18면의 UV 필드는 부모 cube에서 생략(implicit). 이 28면은 신규 소스 경로 표이며 28개의 새 모델이나 새 독립 face 이미지가 아니다.
- **기존 R004의 overlay 45 불투명/211 투명, snow 순백 16은 계승**. 4x45=180은 원본 alpha/모델 4면에 의한 이론상 투영이며 게임 렌더에서 관측된 픽셀 수가 아님.
- 고정 9개 PNG·기존 26 JSON 연결 유지, 신규 고정 PNG 0, 실제 인게임 정적 확인 0/9. 실제 바이옴 tint RGB 및 colormap 런타임 좌표·엔진 조명·주변 블록 렌더 확인 안 됨.
- Mojang 공식 client.jar 전체 SHA-1/메타데이터 인증은 사용자 정책으로 필수 제외, 공식 인증 성공 아님. 애니메이션 연구 전면 보류. 타 단계, 공용 HANDOFF/PROGRESS, 전역 v38 수정 금지.
- 현재 TEX09-R005 / 다음 후보 TEX09-R006. 반드시 새 작업 시 LIVE STATE/HEAD 및 마지막 릴리스 근거 재조회. 실제 인게임 정적 관측·검증 가능한 런타임 색상표 룩업이 없는 한 F를 완료하지 말 것.
