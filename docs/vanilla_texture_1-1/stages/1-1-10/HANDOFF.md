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
