# 1-1-10 — 잎·식생 별도 채팅 인수인계

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX10-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-10 / 잎·식생 / 8개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-10 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-10_잎식생.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-10/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 8/8 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

애니메이션/흔들림 연구는 보류; 정적 이미지와 인게임 정적 검증만 허용.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-10-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-10-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-10-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-10-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-10-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-10-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-10-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 잎·덩굴 알파 마스크·가시 영역·투명 외곽
- **D2:** PNG의 녹색과 생물군계 tintindex의 차이
- **D3:** 컷아웃 영역과 3D 요소의 담당 역할 구분

## 검토할 정확한 텍스처 8개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-10-001` | `oak_leaves` | `69c9c7048695e014aee6b8a2c4cb080607bd7a2a5291c06218b8134cbfcdc04f` | `assets/minecraft/textures/block/oak_leaves.png` |
| `1-1-10-002` | `spruce_leaves` | `538a4d679a8677d710cde7a99c44f9dd95d1e117aa42844d1dad1e24ed47fb16` | `assets/minecraft/textures/block/spruce_leaves.png` |
| `1-1-10-003` | `birch_leaves` | `03ea357f700a55a3e830e9bd0264c8b0a6c2901e3d1d328808adc1c7c97cc330` | `assets/minecraft/textures/block/birch_leaves.png` |
| `1-1-10-004` | `mangrove_leaves` | `1044dd96b9d2225d56bcdf9549e7890283c29f434fd80740c0ad0d8c571915c5` | `assets/minecraft/textures/block/mangrove_leaves.png` |
| `1-1-10-005` | `azalea_leaves` | `fdfa370f1bc7460a0f51d70fd57c691a86ee9269bbaba5b7e46693bb2de09a2a` | `assets/minecraft/textures/block/azalea_leaves.png` |
| `1-1-10-006` | `moss_block` | `863aae6a09178ccd3700c7ee6e3e9f2448e99f51cbbd8c157dd0126f8c749c80` | `assets/minecraft/textures/block/moss_block.png` |
| `1-1-10-007` | `vine` | `5ca6b688ee8cce05df9d90a8d0f7bb669361ce27dba4a761dcb209819e0d232e` | `assets/minecraft/textures/block/vine.png` |
| `1-1-10-008` | `flowering_azalea_leaves` | `b6e494ed60f5e4fa2704645777d56d585ac0aa4b2c7493879f286a954ce9a9d6` | `assets/minecraft/textures/block/flowering_azalea_leaves.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX10-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX10-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-10/TEX10-R001/`. 다음은 이 단계만 `TEX10-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-10/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.

---

## TEX10-R001 — 2026-11-13 실제 신규 근거 저장

- 사용자 저장소의 Minecraft 1.21.11 추출 PNG 8종 직접 바이트 수신/PNG CRC·SHA/전 **2,048 RGBA** 픽셀 검사; v4 기록·외부 추출 미러 Git blob 모두 **8/8 일치**. 이미지 8/8, RGB/알파 8/8.
- 정적 모델/상태 JSON 8쌍, 상속 부모 4종, 정적 UV 면 **44행**, vine 10 multipart 조건 확인. **D1** 7종 이진 컷아웃 + moss 1종 완전 불투명, **D2** 모델 tintindex 0인 5종 vs 미기재 3종, **D3** 큐브/덩굴 양면 평면+알파 외곽 역할 구분.
- [독립 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R001/REPORT.md), [SHA·출처 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R001/SOURCE_LEDGER.csv), [PNG 픽셀 증거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R001/PIXEL_AUDIT.json), [면별 UV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R001/MODEL_UV_AUDIT.csv), [상태 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R001/SUMMARY.json).
- **F 미완료:** Mojang 공식 JAR 진본 인증 0/8, 인게임 정적 렌더 0/8. 추출 미러 동일성=공식 인증 아님. 애니메이션 보류 계속, 전역 v38 유지. **현재 `TEX10-R001`, 다음 `TEX10-R002`**. 저장 직전 상태/SHA 충돌 재확인 필수.

---

## TEX10-R002 — 추가 정적 실측 / 2026-11-13

- 대상은 기존 **8개로 동일**, 각각 원본 SHA·blob SHA 재확인. 실제 RGB/알파 이미지 2,048픽셀에 대해 **128행 이진 마스크**, 경계 60픽셀/장, 4-인접 전환 및 반복 경계 좌우/상하 차이 추가 기록. R001의 8/8을 누적 16개로 계산 금지.
- 철쭉/개화 철쭉 같은 좌표 256픽셀 RGBA 직접 대조: **동일 217, 변경 39**(공통 불투명 RGB 변경 21, 한쪽만 가시 18).
- 덩굴 10 multipart 원본 규칙을 5 부울값의 **32개 논리 조합**에 적용. 전체 85 인스턴스·170 선언 면, 모두 false fallback 5개가 선택됨; 실제 인게임 32상태 접근성은 미확인. 북/남 UV 좌우 반전 실화소 16개 샘플 기록.
- [R002 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R002/REPORT.md), [알파 마스크](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R002/PIXEL_MASK_AUDIT.json), [덩굴 32 상태](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R002/VINE_32_STATIC_STATES.csv), [철쭉 차분](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R002/AZALEA_PAIR_DIFF.json).
- **Mojang 공식 client.jar 인증·인게임 정적 검증 0/8 유지**: 공식 API 발견, 실제 서버 다운로드 불가. 애니메이션 보류, 전역 v38 유지. 이번 단계 버전 `TEX10-R002`; 다음 `TEX10-R003`은 신규 증거가 있을 때만 진행.

---

## TEX10-R003 — 2026-11-13 · 사용자 제공 JAR 추출본 출처 우선화 및 4중 검증 상태 분리

- **원본 출처 정정:** [`1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)은 사용자 진술에 따르면 **Minecraft Java 1.21.11 JAR을 사용자가 직접 압축 해제해 GitHub에 업로드한 파일**이다. 앞으로 이 저장소 추출본을 1차 분석 자료로 사용한다. **사용자 진술에 따른 추출 출처와 Mojang 공식 JAR의 SHA-1 인증은 별개**이며, 공식 인증 완료를 주장하지 않는다.
- **중복 없는 실제 재검사:** 사용자 저장소의 PNG **8개 바이너리**, 개별 모델 JSON **8개**, blockstates JSON **8개**, 공통 상속 부모 JSON **4개** 등 **서로 다른 경로 28개**를 실제 조회. 현재 Git blob SHA 8×3이 이전 원장과 **24/24 일치**, 4개 부모도 해시 기록. blockstates→model→부모→PNG 참조 **8개 모두 연결 검증**. 7개 기본 `variants:{"":...}` / 덩굴 10 multipart. 이전 R001/R002의 픽셀·알파·UV 측정은 **재집계 없음**; 새 표본 텍스처 수 **0개**.
- **네 검증 축:** (1) 사용자 제공 추출본 직접 파일·정적 참조 검증 **8/8**; (2) 기존 비공식 미러와 Git blob 일치 **8/8 — R001 계승, R003 재다운로드 0**; (3) Mojang 공식 JAR 전체 SHA-1 + 공식 메타데이터 인증 **0/8 미완료**; (4) 게임 실제 정적 렌더 확인 **0/8 미완료**. 첫 두 축의 완료가 나머지 둘을 완료시키지 않는다.
- [R003 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R003/REPORT.md) / [출처·모델 경로 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R003/SOURCE_PROVENANCE_LEDGER.csv) / [모델 리소스 참조 폐쇄](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R003/RESOURCE_REFERENCE_CLOSURE.json) / [독립 검증 4축](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R003/FOUR_AXIS_VERIFICATION.json).
- **현재 단계 `TEX10-R003`, 다음 `TEX10-R004`**. `TEX10-R001`, `TEX10-R002`, 옛 v4와 전체 `v38` 보존. 애니메이션 보류. Project Zomboid 변환·실제 가구 3D 제작 금지. 다른 단계·루트 상태 수정 금지.

---

## TEX10-R004 — 2026-11-13 · 원본 색상표 PNG 2종 + 아틀라스·내부 버전 확인

- 사용자 제공 `1.21.11/` 추출본에서 **새 고유 경로 4개** 직접 확인: `assets/minecraft/textures/colormap/foliage.png`, `grass.png`, `assets/minecraft/atlases/blocks.json`, `version.json`. 기존 R003의 고유 28경로에 보조 4경로를 추가해 R003–R004 **32개 경로**. 연구 표본 PNG 8개는 그대로이며, 2개 colormap을 8+2=10개 완료로 계산 금지.
- 2개 색상표 모두 **256×256 8-bit RGB**, PNG CRC32와 zlib Adler-32 통과, **각 65,536픽셀** 직접 압축 해제·계측. foliage **8,837개** 고유 RGB, grass **4,536개** 고유 RGB; grass의 `#FFFFFF` **32,640픽셀**. 샘플 24좌표. **정적 색상표 실측**과 **실게임 biome tint**는 별개.
- `atlases/blocks.json`에서 `minecraft:directory` + `source:block` + `prefix:block/` 실제 존재 확인. 대상 8개 경로 `textures/block/...`에 해당하는 규칙이나 `colormap/`은 별도이며 이 아틀라스 정의에는 명시적으로 없음. `version.json`의 1.21.11, Java 21, world version 4671, protocol 774, resource major 75는 사용자 추출본 **내부 버전 자료**, 공식 JAR SHA-1 인증은 아님.
- [R004 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R004/REPORT.md), [colormap 감사 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R004/COLORMAP_AUDIT.json), [24개 색상 샘플 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R004/COLORMAP_SAMPLE_PIXELS.csv), [아틀라스·내부 버전](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R004/ATLAS_AND_VERSION.json).
- 4축: 사용자 추출본 기존 대상 8/8 + 보조 색상표 2개, R001 비공식 미러 기존 8/8(신규 0), Mojang 공식 JAR SHA-1 인증 **0/8**, 인게임 정적 확인 **0/8**. 기존 R001/R002/R003 불변, 공통 `v38` 불변, 애니메이션 보류. 현재 `TEX10-R004`, 다음 신규 증거 시 `TEX10-R005`.

---

## 운영 범위 변경 — 2026-11-13 · 공식 인증 제외 (릴리스 버전 증가 없음)

- 사용자 직접 지시에 따라 **Mojang 공식 `client.jar` 전체 SHA-1 및 공식 버전 매니페스트 대조는 현재 연구의 검증 절차·완료조건·미완료 집계에서 제외**. 더 이상 공식 인증을 시도하거나 필수 과제로 요구하지 않음.
- 현재 **적용되는 3가지 검증 축**: ① 사용자 제공 `1.21.11/` 추출본 실제 내용 검증, ② 기존 비공식 미러 교차 검증, ③ **실제 Minecraft 인게임 정적 렌더 확인**. ③은 아직 0/8로 남아 있음.
- 과거 `TEX10-R001`~`TEX10-R004` 보고서의 4축 상태표·`official 0/8` 표시는 **그 시점의 역사적 기록**이므로 고치거나 삭제하지 않음. 현재 연구의 공식 인증 상태는 **미완료(pending)가 아니라 정책상 제외(excluded / not applicable)**이며 완료율 분모에 포함하지 않음.
- **현재 버전 `TEX10-R004` 유지, 다음 신규 근거를 저장할 때 `TEX10-R005`**. 이는 연구 실측이 아니라 검증 범위 정책 변경이므로 별도 R005 결과물을 만들지 않음. 전체 `v38` 및 다른 단계 무변경. 애니메이션 분석/가구 3D 제작/Project Zomboid 변환은 기존대로 보류·제외.

---

## TEX10-R005 — 2026-11-13 · 아이템 틴트·덩굴 아이템 기하·지형 셰이더

- 사용자 추출본 `1.21.11/`에서 **신규 고유 경로 16개** 직접 조회: 아이템 JSON 8, item 모델 2, terrain 셰이더 2, import include 4. 이전 R003–R004 고유 32 + R005 16 = 누적 **48경로**. 8개 원래 PNG는 새 텍스처로 중복 가산하지 않음.
- 기존 **8 PNG 바이트 재조회**: 8/8 PNG 전체 청크 CRC32 성공, Git blob SHA 기존 기록 일치. 7개 `tRNS` 투명 청크, `moss_block`은 없음; PNG palette 6종, grayscale 2종. raw SHA-256 R001 값과 R002 마스크·R004 colormap 131,072 픽셀 계승; **R005 raw SHA-256 새 산출 0, RGBA 새 픽셀 계수 0**.
- `items` 8종의 `minecraft:constant` **5종**: oak `#48B518`, spruce `#619961`, birch `#80A755`, mangrove `#92C648`, vine `#48B518`; azalea / flowering azalea / moss는 `tints` 미선언. 블록 tintindex와 아이템 constant 구별. item→model **8/8**.
- vine 아이템은 `item/vine → item/generated → builtin/generated`(layer0 `block/vine`), 블록은 두께 0 양면 평면+multipart; R001 44 UV 행, R002 32 논리 상태는 계승.
- `terrain.vsh` UV0 및 Color×라이트맵, `terrain.fsh` 텍스처×vertexColor 및 `#ifdef ALPHA_CUTOUT` 조건부 `discard` 소스 확인. 런타임 매크로 임계값, biome→colormap XY 및 인게임 최종 색은 **미확인**.
- [R005 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R005/REPORT.md), [요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R005/SUMMARY.json), [PNG 청크 기록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R005/PNG_CONTAINER_RECHECK.csv), [아이템 틴트 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R005/ITEM_TINT_LEDGER.csv).
- **인게임 정적 0/8**, Mojang 공식 JAR 인증은 사용자 지시로 필수 범위 제외(성공 인증 아님). 애니메이션·PZ 변환·가구 제작 보류. 전체 `v38` 및 다른 단계·R001–R004 불변. 현재 `TEX10-R005`, 다음 신규 증거 발견 시 `TEX10-R006`.

---

## TEX10-R006 — 2026-11-13 · 바이옴 65개 잎색 명시 오버라이드 + 컷아웃 셰이더 비교

- 사용자 제공 `1.21.11/data/minecraft/worldgen/biome/` **65/65 JSON 직접 읽음**. 정적 필드 확인: foliage_color **7**, grass_color **5**, dry_foliage_color **4**, grass_color_modifier **3**, temperature_modifier **2**. 필드 중복 바이옴 혼합 없이 구분.
- `swamp`/ `mangrove_swamp`은 temperature 0.8, downfall 0.9로 같으나 `foliage_color`는 각각 `#6a7039` / `#8db127`. 바이옴 JSON 명시 오버라이드와 colormap 좌표/아이템 상수 틴트를 분리할 것. 실제 룩업 좌표/우선순위와 인게임 색 미확정.
- 신규 GLSL 7개(`block.{vsh,fsh}`, `entity.{vsh,fsh}`, `particle.fsh`, `light.glsl`, `dynamictransforms.glsl`) 직접 읽음. block/entity 조건부 `ALPHA_CUTOUT`, particle **0.1**은 particle 전용 숫자. 실제 8개 블록 컷아웃 값/패스는 여전히 미확인.
- `colormap/dry_foliage.png` 보조 **1개** 원본 컨테이너 확인: 8,979 bytes, 256×256 RGB, 전 PNG 청크 CRC 통과. **픽셀 디코딩 0**, 보조 1개를 8개 표본에 합산 금지.
- **R006 새 고유 소스 경로 73 = 바이옴 65 + shader 7 + 지원 colormap 1**; R003–R005 계승 고유 48 포함 누적 **121경로**. R001 RGBA 2,048, R001 UV 44, R004 colormap 131,072 RGB 픽셀 계승; 이번 신규 대상 텍스처/화소/UV 실측 0.
- [R006 연구 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R006/REPORT.md), [65개 바이옴 감사](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R006/BIOME_SOURCE_AUDIT.csv), [명시적 색상 사례](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R006/BIOME_OVERRIDE_CASES.csv), [셰이더 근거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R006/SHADER_STATIC_AUDIT.json), [R006 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R006/SUMMARY.json).
- 인게임 정적 **0/8**, Mojang 공식 전체 JAR SHA-1 필수 절차 제외/인증 성공 아님, 애니메이션·PZ 변환·실제 가구 3D 작업 보류. 이번 리비전 이후 다음 후보 `TEX10-R007`이며 새로운 근거가 있을 때에만 작성. v38 및 다른 단계/이전 Rxxx 변경 금지.

---

## TEX10-R007 — 2026-11-13 · JVM 원본 코드로 컬러맵 XY 계산/우선순위 확인, dry_foliage 전체 RGB, dark_cutout sidecar

- **원본 Java .class 7파일 직접 분석**: `dvy` `BiomeColors` (x=int((1-t)*255), y=int((1-t*downfall)*255), index=y*256+x), `dxo` `Biome` float32 clamp·foliage/dry Optional 명시값 우선, `dwk`/ `dwd`/ `dwm` 3색상표 getter, `hpa` RenderPipelines, `ggr` BlockColors. Yarn 1.21.11는 난독화 클래스명 대조 보조 자료이며 **바이트코드는 사용자 저장소 원본**.
- `hpa.class` `CUTOUT_BLOCK` 및 `CUTOUT_TERRAIN`에 `ALPHA_CUTOUT 0.5F` 정적 등록 확인; 8개 블록의 실제 render pass 개별 배정 **미확정**.
- 잎 PNG 6개의 원본 `.png.mcmeta` sidecar에 `mipmap_strategy: dark_cutout` 직접 확인. `vine`, `moss_block` sidecar 없음(기본 전략 검증 아님).
- 컬러맵 RGB 완전 디코드: `foliage` 및 `grass` 기존 R004의 **131,072화소 재조회·대조**, `dry_foliage` 신규 **65,536화소/268고유 RGB** + 3파일 청크 CRC32/zlib Adler32 통과. 사용자 제공 바이옴 JSON 65개를 float32 정밀도로 변환해 **195개 색상표 조회 셀**, foliage/dry 명시 JSON override 우선 적용 표 작성. 화면 RGB 실측 아님.
- 이번 신규 경로 **13 = class 7 + sidecar 6**; R003 이후 누적 **134**. [R007 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R007/REPORT.md), [65 바이옴 좌표·RGB](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R007/BIOME_COLORMAP_LOOKUP_65.csv), [바이트코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R007/CLASS_BYTECODE_AUDIT.json), [mipmap 8](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R007/MIPMAP_STRATEGY_8.csv), [색상표 검증](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R007/COLORMAP_RECHECK.json).
- **인게임 정적 확인 0/8** 유지. 게임의 실제 촬영·블록별 실제 파이프라인 배정과 블렌딩에는 추가 증거 필요. 사용자가 요청한 규칙에 따라 사용자 도움이 필요한 인게임 검증 단계에서는 멈추고 안내할 것. 공식 JAR 전체 SHA1 필수 절차 제외(인증 성공 아님). 기존 `v38`, 타 단계·R001–R006 불변. 현재 `TEX10-R007`, 다음 `TEX10-R008`은 실제 새 근거로만.

---

## 연구 범위 정책 변경 — 2026-11-13 · 인게임 검증도 필수 조건에서 제외 (연구 릴리스 증가 없음)

**사용자 지시:** “인게임 검증은 제외해줘 어차피 모델링이랑 텍스텨있는데 필요없을거같아.”

- **1-1-10 잎·식생 연구에 한정**하여 Minecraft 실제 실행, 스크린샷 수집, 8개 블록 인게임 정적 렌더 판정은 연구의 **필수 검증·완료 조건·진행률 분모에서 제외**한다. 더 이상 이 작업을 위해 사용자에게 게임 캡처를 요구하거나 `계속해줘` 요청에서 **0/8을 이유로 연구를 중단하지 말 것**.
- 검증 기준은 **사용자 제공 Minecraft 1.21.11 원본 PNG 바이트와 RGBA 계측, 정적 모델 JSON/부모·블록상태/UV 연결, tintindex·바이옴 데이터·컬러맵·관련 셰이더 및 클래스 바이트코드** 등의 독립 확인 가능한 근거다. 출처·해시·추론/실측 구분을 계속 유지한다.
- **인게임 검증 0/8은 과거 조사 기록으로 남긴다.** 현재 정책상 `excluded/not required`이며 연구 미완료 항목으로 세지 않는다. 원본 정적 자료만으로 확인하지 못한 **실제 GPU 화면 색상, 실시간 주변 바이옴 보간, 광원·렌더 패스 배정** 등을 검증 성공으로 주장하지 않는다. 필요시 **정적 소스에서 해석할 수 있는 부분까지만** 규명하고 한계를 문서화한다.
- 앞서 사용자 지시로 제외한 **Mojang 공식 전체 client.jar SHA-1 인증** 역시 필수 절차에서 제외한 상태를 유지한다(인증 성공 아님).
- **현재 연구 버전 `TEX10-R007` 그대로**, 다음 신규 정적 분석·근거를 실제로 추가할 때만 `TEX10-R008` 생성. **정책 변경만으로 새 연구 R008 릴리스를 만들지 않는다.** 이전 R001–R007 연구 보고서는 작성 당시 기록으로 불변. 전체 `v38`, 다른 단계의 요구사항과 파일도 변경하지 않는다. 애니메이션 연구·실제 가구 3D 작업·PZ→Minecraft 변환 보류 유지.
- 사용자가 `계속해줘`라고 하면 이 업데이트를 우선 적용하여 **정적 검증에서 아직 남아 있는 독립 검증 사항을 조사**할 것. 정적 범위 연구가 완전히 끝났거나, 필수 원본을 추가로 제공해야 해서 더 이상 진행할 수 없을 때에만 사용자에게 멈춘 이유와 정확한 필요 자료를 알릴 것.

---

## TEX10-R008 — 2026-11-13 · 8종 BlockColors 공급자·모델 틴트 원본 연결 + 덩굴 32 상태 정적 기하

- 사용자 추출본 **신규 `.class` 2경로** `dzs.class`(Blocks 레지스트리)와 `hns.class`(바이옴 색상 리졸버) 원본 바이트코드·bootstrap 분석. R007 기존 `ggr.class`(BlockColors)와 `dxo.class`(Biome)를 원본 SHA 재확인 후 심화 분석하여 **8개 블록의 이름→registry field→색상 공급자→모델 tintindex** 연결 확정.
- 블록 8종 중 **바이옴 foliage 3종** oak / mangrove / vine, **고정색 2종** spruce `#619961` / birch `#80A755`, **틴트 없는 3종** azalea / flowering azalea / moss. `ggr.i→hns.b→dxo.d()` foliage 경로, `ggr.k/j`의 고정값, 색상 공급자 미등록 블록의 `tintindex` 부재를 구분. **아이템 고정 틴트와 배치 블록 바이옴 틴트는 별도 계층**(oak/mangrove/vine 차이).
- 모델/블록상태 기존 원본 **21경로 재확인**(대상 8모델+8blockstates+부모3+ggr/dxo 2). **44 모델 face 수량**(틴트 큐브 24 + 무틴트 큐브 18 + 덩굴 양면 2) 확인. 덩굴 multipart **10규칙/32논리상태/합계 85 평면 적용·170 양면**, 모두 false 상태는 5평면 대체 배치. 실제 게임 상태 빈도나 한 화면 폴리곤 합산이 아님.
- R006 원본 바이옴 65종·R007 계산 색상표를 계승하여 **65×8=520단일 바이옴 참조 틴트 행** 생성. 바이옴 근처 보간/조명/화면 색상 실측 아님. 신규 JPEG/PNG 실측·신규 RGBA 픽셀 0. **이번 새 고유 원본 경로 2개**, R003 이후 누적 **136개**.
- [R008 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R008/REPORT.md), [8종 블록 색상 공급자](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R008/BLOCK_COLOR_PROVIDER_8.csv), [등록 코드 증거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R008/CLASS_REGISTRATION_AUDIT.json), [65×8 틴트 참조](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R008/BIOME_TINT_REFERENCE_65x8.csv), [덩굴 32상태](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R008/VINE_MULTIPART_32.csv).
- **인게임 검증은 사용자 지시에 따라 제외**(0/8 역사적 기록만 유지), 공식 Mojang 원본 전체 JAR SHA1 인증도 제외. 필요시 남은 **정적 소스** 렌더 패스·mipmap·세계 바이옴 색상 샘플링을 연구하되 인게임 캡처를 요구하거나 완료 분모에 넣지 말 것. 현 버전 `TEX10-R008`, 다음 새 근거 시 `TEX10-R009`. 전역 `v38`, 타 단계, 과거 R001–R007 불변. 애니메이션/PZ변환/가구 제작 보류.

---

## TEX10-R009 — 2026-11-13 · 잎 그래픽 분기/덩굴 CUTOUT/이끼 SOLID 정적 렌더 경로

- **새 원본 .class 고유 경로 6개**: `hoe` BlockRenderLayers, `hth` BlockRenderLayer, `eei` LeavesBlock, `eir` TintedParticleLeavesBlock, `eje` UntintedParticleLeavesBlock, `ees` MangroveLeavesBlock. 모두 사용자 1.21.11 추출본의 JVM .class 내용 직접 읽고 blob SHA 확인. R008 기존 `dzs`, R007 기존 `hpa`/`ggr`는 계승.
- 원본 `hoe.a(Leoh;)Lhth;`에서 **LeavesBlock이면 그래픽 cutoutLeaves=true는 CUTOUT, false는 SOLID** 분기 검증. `hoe.b(HashMap)` CUTOUT 맵에 대상 잎 6종+덩굴 1종 **7개 등록**, 이끼는 해당 map에서 미등록→기본 SOLID. 잎은 등록 맵보다 LeavesBlock 분기를 우선하므로 컷아웃 옵션 false면 SOLID.
- `hth.b CUTOUT` → `hpa.f CUTOUT_TERRAIN` 및 R007의 `ALPHA_CUTOUT=0.5F` 정적 관계 확인. `hth.a SOLID` → `hpa.c SOLID_TERRAIN`. 실제 선택된 사용자 그래픽 설정이나 화면 캡처 검증 주장이 아님.
- 기존 `dzs.class`의 `BootstrapMethods`/생성자와 신규 leaf classes 슈퍼클래스 대조: oak/spruce/birch `eir→eei`, mangrove `ees→eir→eei`, azalea/flowering azalea `eje→eei`. **철쭉도 LeavesBlock 분기 대상**임을 정적 원본으로 확정. 덩굴은 CUTOUT, 이끼는 SOLID.
- **이번 신규 경로 6**, R003–R008 누적 136→R009 누적 **142**. 신규 픽셀·UV·대상 PNG 수 **0**, 과거 44면/3컬러맵 196,608 RGB 픽셀 계승. [R009 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R009/REPORT.md), [8종 render-layer 표](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R009/RENDER_LAYER_8.csv), [상속·블록 생성자](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R009/LEAF_FACTORY_INHERITANCE_6.csv), [바이트코드 근거](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R009/CLASS_RENDER_LAYER_AUDIT.json), [요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R009/SUMMARY.json).
- 사용자 정책: **인게임 검증 의무 제외**, 공식 원본 JAR SHA-1 필수 제외, 애니메이션·가구 제작·PZ 변환 보류. **현재 `TEX10-R009`, 다음 `TEX10-R010`은 미확인 정적 알고리즘에 대해 새로운 1차 자료 검증이 있을 때만**. R001–R008/전역 v38/다른 단계 무변경.

---

## TEX10-R010 — 2026-11-13 · 원본 MipmapHelper로 잎·덩굴·이끼 8개 기본 전략 확인

- 신규 원본 Java 클래스 3개: ild (MipmapHelper), ile (MipmapStrategy), inj (TextureResourceMetadata). 파일 SHA와 메서드 경로는 R010 SOURCE_LEDGER/CLASS_AUDIT에 보존.
- inj metadata default: mipmap_strategy AUTO, alpha_cutoff_bias 0.0F. ild AUTO 해석: alpha=0 픽셀이 하나라도 존재하면 CUTOUT, 없으면 MEAN.
- 잎 6종은 기존 mcmeta에 dark_cutout 명시. 덩굴은 mcmeta 부재 및 기존 R002 투명 110/256→CUTOUT. 이끼는 부재/0/256→MEAN.
- DARK_CUTOUT은 특수 알파 기반 2×2 보간, CUTOUT/STRICT_CUTOUT/DARK_CUTOUT은 mip alpha coverage 조정 분기로 확인. helper 내부 기본 0.5F/strict 0.3F는 shader cutout 정의와 별개.
- 신규 파일 경로 3개, 누적 고유 경로 142→145. 이전 R002 마스크 8종 및 R007 mcmeta 6종은 계승. 신규 RGBA 픽셀 0, 실제 mip 이미지 생성/검증 0, 인게임 0/8은 사용자 정책상 제외.
- 상세 근거: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R010/REPORT.md
- 전략 CSV: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R010/MIPMAP_EFFECTIVE_STRATEGY_8.csv
- 현재 TEX10-R010, 다음 TEX10-R011. 향후 mip 수준별 바이트 일치 정적 재생성 가능하지만 미완료. 전체 v38, 다른 단계, 과거 릴리스 무변경. 애니메이션 및 가구/PZ 작업 보류.

---

## TEX10-R011 — 2026-11-13 · 실제 PNG 재해시 + 정적 재현 680개 밉맵 alpha 값

- 신규 원본 고유 경로 **`1.21.11/bel.class` 한 개**, JVM constant pool 및 알파/gamma LUT 관련 메서드 분석. R010 `ild.class` 재해석. R002 잎·덩굴·이끼 8종 PNG 원본 다시 받아 Python PIL 16×16 RGBA **2,048화소 재디코드**하고 raw SHA256 **8/8 이전 원본과 일치**. 같은 원본 위치이므로 고유 신원본 화소 추가 0.
- 전 8종 원본 16×16에서 8×8/4×4/2×2/1×1 **각 85개×8=680개 alpha 값 실험 재계산**. Python numpy.float32+Pillow 구현 vs JavaScript Math.fround 구현이 **32/32 레벨 CRC32 일치**, 전체 680바이트 CRC `2171e3da`. 595개 부분 알파/85개 불투명/0개 완전 투명 값(재현 실험 산출, 게임 결과 아님).
- [보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R011/REPORT.md), [alpha 680개 행별 hex](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R011/ALPHA_LEVELS_HEX_8.json), [32개 레벨 계측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R011/MIP_ALPHA_METRICS_32.csv), [원본 PNG 8 SHA256](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R011/ORIGINAL_PNG_REHASH_8.csv), [원본 코드/한계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-10/TEX10-R011/BYTECODE_ALPHA_MATH_AUDIT.json).
- **두 재구현의 일치 ≠ 실제 Java NativeImage/JVM 실행 byte-exact 검증**. full RGB/PNG atlas GPU 화면 검증 0, 인게임 검증 의무 제외. 새 source 1개, 누적 고유 경로 **145→146**. 기존 R001–R010 및 전역 v38·타 단계 불변. 후속은 `TEX10-R012`, 새 정적 실제 근거가 있을 때만. 애니메이션/PZ변환/실제 가구 제작 보류.
