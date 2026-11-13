# TEX04-R003 — R001 블랙 양털 모델 Git SHA 기입 오기, 원본 불변 보존

- **정정 대상 (과거 기록)**: `research/vanilla_textures/by_stage/1-1-04/TEX04-R001/SOURCE_LEDGER.csv`의 `black_wool` 1행 `model_git_blob_sha`; `TEX04-R001/UV_FACE_LEDGER.csv`의 `black_wool` 6개 면 `leaf_git_blob_sha`.
- **기존 표기 (잘못된 값)**: `7fea63ff530cad3b51435e662daa2c4d6324bd8` (**39자**, 유효한 40자리 Git SHA가 아님).
- **바른 40자리 Git blob SHA-1**: `7fea63ff530cad3b51435e662daa2c4d6324bd8a`.
- **확인 출처 A**: 사용자 제공 `1.21.11/assets/minecraft/models/block/black_wool.json`, Git blob `7fea63ff530cad3b51435e662daa2c4d6324bd8a`.
- **확인 출처 B**: `InventivetalentDev/minecraft-assets`의 브랜치 `1.21.11` 경로 `assets/minecraft/models/block/black_wool.json`, Git blob이 **정확히 같은 40자리 값**.
- 양쪽 JSON 콘텐츠도 직접 읽고 바이트가 일치함을 확인. `parent = minecraft:block/cube_all`, `textures.all = minecraft:block/black_wool`. 즉 **텍스처/모델 내용 불일치가 아니라 과거 CSV의 SHA 문자열 전사 오류**.
- R001 원본 CSV/MD/커밋 **모두 수정·삭제하지 않음**. R003 `USER_EXTRACT_9_PNG_JSON_CROSSCHECK.csv`에는 과거값과 정정값을 **둘 다** 남기고, `USER_EXTRACT_54_FACE_UV_SOURCE_CHECK.csv`의 블랙 양털 6행에는 올바른 `leaf_git_blob_sha`를 기록함.
- SHA-1은 Git **blob 객체 ID**이고 사용자 제공 `client.jar` 전체의 SHA-1 또는 PNG의 SHA-256이 아니다. 인증 등급은 원본 JAR 전체가 아닌 사용자 제공 추출본·미러 교차 검증.

새 단계: `TEX04-R003`, 연구 범위: `1-1-04`. 전역 `v38` 유지.
