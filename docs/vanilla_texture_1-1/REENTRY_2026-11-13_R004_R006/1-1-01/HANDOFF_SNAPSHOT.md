# 1-1-01 — 목재·원목 새 채팅 인수인계 스냅샷

> **조회 기준: 2026-11-13 · `TEX01-R004` / 다음 후보 `TEX01-R005` · 대상 PNG 18개.** 이 문서는 시점 고정 요약이며 저장되는 동안 다른 채팅이 진행했을 수 있다. **최우선은 [라이브 상태](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/STATE.json)**다. 기존 연구 버전 번호를 올리지 않는다.

## 신규 채팅에서 확인할 원본 문서

- **최신 실제 상태**: [`docs/vanilla_texture_1-1/stages/1-1-01/STATE.json`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/STATE.json) · 스냅샷 조회 당시 Git blob SHA: `eae9a52baa2a9375d2d15b3598f88825fedc298b`.
- **기존 연구 전체 인수인계**: [`docs/vanilla_texture_1-1/stages/1-1-01/HANDOFF.md`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/HANDOFF.md).
- **고정 표본 18개와 세부 과제 A–G**: [`docs/vanilla_texture_1-1/1-1-01_목재원목.md`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-01_목재원목.md).
- **기존 v4 150개 원장**: [v4 원본 측정 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) · [1-1 전체 파일별 작업 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- **기존 분석 결과의 마지막 폴더**: [`research/vanilla_textures/by_stage/1-1-01/TEX01-R004/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R004).

## 현재까지 확인된 연구 — 역사적 실적과 신규 완료 구분

- 담당 범위: **목재·원목 18개**. 기존 v4 원장에 **18개** 측정 기록. 이는 전체 단계를 끝냈다는 뜻이 아니다.
- 재진입 스냅샷 버전 **`TEX01-R004`**, 현 STATE의 다음 예정 **`TEX01-R005`**. 버전 간 누적값은 이 단계에만 속하고 전체 `v38`과 겹치지 않는다.
- 이미 확보한 검증 핵심: **기존 18 PNG/4,608 RGBA, 원본 정적 JSON 43개, 132면의 원본 RGB 색상 앵커와 목재 팔레트 대응표를 구분하여 계승.**
- 단계 STATE의 연구 요약 원문: `R004_research_completed_official_auth_removed_from_active_workflow_at_user_request_ingame_pending`.
- **PNG 원본/JSON·UV 정적 소스 측정**과 **인게임 실제 화면 증거**는 별도. 인게임 확인 **0/ 18**. 이 스냅샷의 소스 기준 추적값 `18`은 성과 근거일 뿐, 단계 완료 판정으로 단정하지 않는다.
- 최신 사용자 연구 기준: Mojang 공식 배포 JAR 전체 SHA-1/공식 인증을 필수 검증과 남은 과제 및 완료 기준에서 **제외**한다. 공식 인증을 완료했다고 쓰지 말고, 과거 미완료 수치는 역사적 기록으로 보존한다.

## A–G 상세 검증 현황 (GitHub STATE 당시의 문자열 그대로)

| 코드 | 연구 범위 | 기록 상태 |
|---|---|---|
| A | A 기존 출처·파일·중복 대조 | `completed_18_user_extracted_origin_reclassified_mirror_hash_legacy_distinguished` |
| B | B PNG 실제 바이너리·SHA·CRC 검증 | `R001_18_SHA_CRC_plus_R003_18_PNG_IHDR_and_git_blob_size_rechecked` |
| C | C RGBA·밝기·알파·반복 정량 검사 | `R001_4608_RGBA_source_measurement_plus_R004_canonical_color_class_topology_and_LUT` |
| D | D 재질 특화 세부 검사 | `D1_R001_6_partial_D2_R001_native_R002_synthetic72_D3_R004_132_face_local_UV_6anchor_RGB_source_mapping` |
| E | E 정적 모델 JSON·UV·상태 연결 | `R001_43_model_JSON_150_face_static_refs_augmented_R004_132_in_scope_face_RGB_values_nonruntime` |
| F | F 실제 인게임 정적 렌더 검증 | `pending_ingame_static_0_of18_official_JAR_certification_out_of_scope` |
| G | G 근거 보고서·단계 인수인계 저장 | `R004_source_palette_LUT_and_face_RGB6_result_saved` |

## 다음 채팅에서 이어갈 가장 중요한 정적 연구

**목재 결 무늬가 실제 모델에서 회전·상속·UV에 따라 어떻게 배치되는지 추가 검증. 132면 앵커 샘플은 게임 렌더링이 아닌 소스 텍셀 참조임을 유지.** 이것은 소스 기반 다음 조사 방향이며, 실행 전 최신 GitHub 원장과 실제 검증 가능한 자료를 확인해 우선순위를 수정할 수 있다.

## 필수 저장 및 버전 충돌 방지

1. GitHub에서 **최신 라이브** `STATE.json`의 `current_revision`, `next_revision`, 파일 SHA를 읽는다. 이 스냅샷 버전 숫자를 강제로 적용하지 않는다. 같은 단계 다른 채팅의 새 릴리스가 있으면 그것부터 읽는다.
2. 그 버전의 `REPORT.md`, `SUMMARY.json`, 증거 CSV를 읽고 **누락된 근거만** 조사한다. 사용자 제공 `1.21.11/` 직접 원본 우선, 비공식 미러는 교차 검증 보조.
3. 새 결과가 나올 때에만 `research/vanilla_textures/by_stage/1-1-01/<최신 next_revision>/` 신규 폴더에 근거·재현·결과 저장. 기존 R000~Rxxx 파일은 덮어쓰지 말 것.
4. **수정 허용 범위**는 오직 자기 단계의 `docs/vanilla_texture_1-1/stages/1-1-01/STATE.json`·`docs/vanilla_texture_1-1/stages/1-1-01/HANDOFF.md` 및 이 단계의 새 연구 릴리스 경로. 루트 프로젝트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`과 타 단계 문서 쓰기 금지. 본 새 채팅 스냅샷도 기록상 읽기 전용.
5. SHA/브랜치 HEAD를 쓰기 직전에 다시 확인해 경합이나 경로 충돌을 발견하면 덮어쓰지 않고 최신 기록을 다시 수집. 증거 없는 완료 처리 금지. 특히 실제 Minecraft 실행/스크린샷이 없으면 **인게임 검증 0** 유지.
6. 애니메이션·게임 움직임/키프레임, Project Zomboid 변환, 실제 3D 가구 제작은 계속 보류/제외. 공식 JAR 재업로드·SHA 인증은 요청하지 않는다.
