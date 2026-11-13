# 1-1-08 복합·기능면 독립 인수인계 — 현재 TEX08-R002

> 2026-11-13. 대상 21개 고정. 기존 v38 그대로. 다음 독립 버전 **TEX08-R003**. `TEX08-R000`은 계획, `R001`은 PNG/모델 소스 분석, `R002`는 정적 blockstate/UV 재감사.

## 현재 검증 구분

| 작업 | 확인 수 | 증거 수준 |
|---|---:|---|
| A–C R001 PNG 해시·CRC·RGBA | 21/21 | 비공식 1.21.11 추출 미러, R001에서 검증 후 계승 |
| D1/E 정면·측면·상부 슬롯/face | 21/21 | 모델 JSON 소스 연결 |
| R002 정적 blockstate 소스 감사 | 16종 | 73 variants + 52 multipart rules |
| R002 고정 상태 비교 | 추가 보조 PNG 1개 | `barrel_top_open`; 132/256 차이, 21개 분모 외 |
| R002 face UV 실제 RGBA 참조 | 62면, 13,056 texel-uses | 명시 16면, 유도 46면; 소스상 모두 불투명 |
| F 공식 1.21.11 client.jar 인증 | **0/21** | 공식 바이너리 접근 실패, 절대 완료 처리 금지 |
| F 인게임 정적 모델/UV | **0/21** | 실제 게임 환경 없음 |
| G 단계별 저장 | R001·R002 | 단계 전용 불변 폴더 |

## 결과물
- 이전 불변 결과: [TEX08-R001/REPORT.md](../../../../research/vanilla_textures/by_stage/1-1-08/TEX08-R001/REPORT.md)
- 이번 불변 결과: [TEX08-R002/REPORT.md](../../../../research/vanilla_textures/by_stage/1-1-08/TEX08-R002/REPORT.md)
- R002: `BLOCKSTATE_AUDIT.csv`, `TEXTURE_STATE_COVERAGE.csv`, `UV_62_FACE_TEXEL_AUDIT.csv`, `BARREL_STATIC_TOP_DIFF.csv`, `SUMMARY.json`, `VERIFY_OFFICIAL_CLIENT.py`.

## 다음 채팅의 실제 잔여 작업
1. GitHub 이 `STATE.json`의 `current_revision`, `next_revision`, blob SHA 및 R003 폴더 존재 유무를 먼저 재확인.
2. 확보한 Mojang **1.21.11 정식 client.jar**의 다운로드 metadata SHA1+size를 확인하고, JAR의 21 PNG SHA256을 R001 원장과 비교한다. 결과가 일치하지 않으면 pending/difference를 보존.
3. 인게임 정적 장면 검증은 별도 수행: 실제 blockstate 방향, 음영/particle, source/implicit UV, 창고/책장 기능면 상태를 관찰할 때에만 `ingame_static_verified` 증가.
4. 애니메이션 재생·키프레임·움직임 연구는 **사용자 해제 전까지 금지**. `smoker_front_on`과 `blast_furnace_front_on` 다중 프레임 원본은 보류, 기존 기록 삭제하지 않는다.
5. 새 근거 발생 시 **TEX08-R003** 불변 결과 폴더만 만들고 단계 `HANDOFF.md`, `STATE.json`만 수정. 타 단계/루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json` 수정 금지.

이 단계의 21개 `texture_id` 및 원본 SHA·경로는 [STATE.json](STATE.json)의 `items` 배열을 기준으로 변경하지 않는다. 상위 상세 규칙: `docs/vanilla_texture_1-1/1-1-08_복합기능면.md`, `docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md`. 전체 프로젝트 `v38` 변경 없음.
