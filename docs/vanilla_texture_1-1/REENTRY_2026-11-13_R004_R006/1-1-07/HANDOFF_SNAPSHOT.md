# 1-1-07 — 콘크리트·색면 새 채팅 인수인계 스냅샷

> **조회 기준: 2026-11-13 · `TEX07-R005` / 다음 후보 `TEX07-R006` · 대상 PNG 7개.** 이 문서는 시점 고정 요약이며 저장되는 동안 다른 채팅이 진행했을 수 있다. **최우선은 [라이브 상태](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/STATE.json)**다. 기존 연구 버전 번호를 올리지 않는다.

## 신규 채팅에서 확인할 원본 문서

- **최신 실제 상태**: [`docs/vanilla_texture_1-1/stages/1-1-07/STATE.json`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/STATE.json) · 스냅샷 조회 당시 Git blob SHA: `475d696072341762a402b723ecf2729175f208cc`.
- **기존 연구 전체 인수인계**: [`docs/vanilla_texture_1-1/stages/1-1-07/HANDOFF.md`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/HANDOFF.md).
- **고정 표본 7개와 세부 과제 A–G**: [`docs/vanilla_texture_1-1/1-1-07_콘크리트색면.md`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-07_콘크리트색면.md).
- **기존 v4 150개 원장**: [v4 원본 측정 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) · [1-1 전체 파일별 작업 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- **기존 분석 결과의 마지막 폴더**: [`research/vanilla_textures/by_stage/1-1-07/TEX07-R005/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-07/TEX07-R005).

## 현재까지 확인된 연구 — 역사적 실적과 신규 완료 구분

- 담당 범위: **콘크리트·색면 7개**. 기존 v4 원장에 **7개** 측정 기록. 이는 전체 단계를 끝냈다는 뜻이 아니다.
- 재진입 스냅샷 버전 **`TEX07-R005`**, 현 STATE의 다음 예정 **`TEX07-R006`**. 버전 간 누적값은 이 단계에만 속하고 전체 `v38`과 겹치지 않는다.
- 이미 확보한 검증 핵심: **7 PNG/31 사용자 제공 추출본 파일 교차·42면 선언 및 공유 display 컨텍스트 7개 조사. R005는 공식 인증 제외 정책 변경만 기록.**
- 단계 STATE의 연구 요약 원문: `R005_policy_official_auth_excluded_ingame_static_still_pending`.
- **PNG 원본/JSON·UV 정적 소스 측정**과 **인게임 실제 화면 증거**는 별도. 인게임 확인 **0/ 7**. 이 스냅샷의 소스 기준 추적값 `단계별 필드 상이`은 성과 근거일 뿐, 단계 완료 판정으로 단정하지 않는다.
- 최신 사용자 연구 기준: Mojang 공식 배포 JAR 전체 SHA-1/공식 인증을 필수 검증과 남은 과제 및 완료 기준에서 **제외**한다. 공식 인증을 완료했다고 쓰지 말고, 과거 미완료 수치는 역사적 기록으로 보존한다.

## A–G 상세 검증 현황 (GitHub STATE 당시의 문자열 그대로)

| 코드 | 연구 범위 | 기록 상태 |
|---|---|---|
| A | A 기존 출처·파일·중복 대조 | `R003_user_extracted_31_files_and_mirror_crosscheck_completed` |
| B | B PNG 실제 바이너리·SHA·CRC 검증 | `R003_user_extracted_7_png_sha256_png_crc_and_mirror_byte_equal` |
| C | C RGBA·밝기·알파·반복 정량 검사 | `R001_RGBA_measurements_transfer_by_R003_byte_identity_not_newly_counted` |
| D | D 재질 특화 세부 검사 | `R001_R002_color_stats_apply_to_identical_R003_bytes_no_new_measurement` |
| E | E 정적 모델 JSON·UV·상태 연결 | `R004_user_source_model_face_flags_42_inherited_and_parent_display_contexts_7_checked` |
| F | F 인게임 정적 렌더 검증 (Mojang 공식 JAR 인증 범위 제외) | `pending_ingame_static_only_official_auth_excluded_by_user` |
| G | G 근거 보고서·단계 인수인계 저장 | `R004_results_and_offline_verifier_saved` |

## 다음 채팅에서 이어갈 가장 중요한 정적 연구

**콘크리트 저대비 노이즈/명도/반복에서 실제 화면과 별개로 추가 가능한 PNG·UV 기반 오류 후보를 조사하고, 새 소스 데이터 없이 형식적 버전 증가 금지.** 이것은 소스 기반 다음 조사 방향이며, 실행 전 최신 GitHub 원장과 실제 검증 가능한 자료를 확인해 우선순위를 수정할 수 있다.

## 필수 저장 및 버전 충돌 방지

1. GitHub에서 **최신 라이브** `STATE.json`의 `current_revision`, `next_revision`, 파일 SHA를 읽는다. 이 스냅샷 버전 숫자를 강제로 적용하지 않는다. 같은 단계 다른 채팅의 새 릴리스가 있으면 그것부터 읽는다.
2. 그 버전의 `REPORT.md`, `SUMMARY.json`, 증거 CSV를 읽고 **누락된 근거만** 조사한다. 사용자 제공 `1.21.11/` 직접 원본 우선, 비공식 미러는 교차 검증 보조.
3. 새 결과가 나올 때에만 `research/vanilla_textures/by_stage/1-1-07/<최신 next_revision>/` 신규 폴더에 근거·재현·결과 저장. 기존 R000~Rxxx 파일은 덮어쓰지 말 것.
4. **수정 허용 범위**는 오직 자기 단계의 `docs/vanilla_texture_1-1/stages/1-1-07/STATE.json`·`docs/vanilla_texture_1-1/stages/1-1-07/HANDOFF.md` 및 이 단계의 새 연구 릴리스 경로. 루트 프로젝트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`과 타 단계 문서 쓰기 금지. 본 새 채팅 스냅샷도 기록상 읽기 전용.
5. SHA/브랜치 HEAD를 쓰기 직전에 다시 확인해 경합이나 경로 충돌을 발견하면 덮어쓰지 않고 최신 기록을 다시 수집. 증거 없는 완료 처리 금지. 특히 실제 Minecraft 실행/스크린샷이 없으면 **인게임 검증 0** 유지.
6. 애니메이션·게임 움직임/키프레임, Project Zomboid 변환, 실제 3D 가구 제작은 계속 보류/제외. 공식 JAR 재업로드·SHA 인증은 요청하지 않는다.
