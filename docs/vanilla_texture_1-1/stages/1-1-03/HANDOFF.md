# 1-1-03 금속·금속부품 — 독립 채팅 인수인계

**현재 단계: TEX03-R005 / 다음 신규 후보: TEX03-R006 / 전역 공통: v38 그대로.** 2026-11-13. 공식 인증 제외 정책 반영(연구 릴리스 번호 유지).

## TEX03-R005 — 최신 신규 정적 연구 (R001–R004 계승)

[최신 REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/REPORT.md) · [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/SUMMARY.json)

- **새로 읽은 사용자 원본:** PNG 6개(1,536 RGBA 재디코딩, SHA-256·PNG CRC 합격), blockstate 14 JSON 및 실제 면을 소유한 템플릿 모델 14 JSON. 기존 R003 69개 원본 목록에 이미 있는 파일이므로 신규 원본 34개라고 가산하지 않는다.
- **새로 기록한 원본 투명 좌표 321행:** 모루 윗면 96·Heavy Core 64는 모델 UV 밖, 철문 위 48·철다락문 36·구리 격자 77은 모델 UV에 포함. 사용 161 / 미사용 160. R001 이전 4,096 RGBA의 하위 집합 재측정임을 명시.
- **원본 기하 406개 상태별 면 대조:** `elements.faces` 406/406 존재, 명시적 UV 346행, 원본 `cube.json` 기본 생략 UV 60행. model-side cullface 272행, face UV rotation 84행, 선언된 UV 경계 역전 148행. 원본 blockstate 14종의 63상태 모델·회전 일치.
- **새 상태별 원본 PNG 알파 교차검증:** 6 PNG 관련 UV 면 **272/272 재검산 일치**, 나머지 134면은 R004·R002 유지. 기존 406면은 다시 신규 UV 실측으로 합산하지 않는다.
- **추가 산출:** [STATE_WORLD_FACE_PROJECTION.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/STATE_WORLD_FACE_PROJECTION.csv), [STATE_WORLD_ALPHA_SUMMARY.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/STATE_WORLD_ALPHA_SUMMARY.csv), [SOURCE_ALPHA0_COORDS.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/SOURCE_ALPHA0_COORDS.csv), [PNG_ALPHA_MASK_SUMMARY.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/PNG_ALPHA_MASK_SUMMARY.csv).
- 철다락문 source `open=false`은 위/아래 투명 면, `open=true`는 수평 방향 투명 면. 철문은 upper에만 2개씩 투명 포함 면. **정적 소스 회전 방향이지 실제 게임 렌더 인증은 아니다.**
- 인게임 정적 렌더 **0/16** 그대로, 공식 Mojang JAR 전체 인증은 **사용자 지시로 제외**. 애니메이션·PZ 변환·3D 가구 제작 보류.

## 우선 출처·검증 기준

사용자가 직접 Java Edition 1.21.11 `client.jar`를 풀어 올린 [GitHub `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11) 폴더의 소스를 **우선 사용**. 이전 비공식 `InventivetalentDev/minecraft-assets@1.21.11`는 교차용. **공식 Mojang JAR 인증은 사용자의 요청에 따라 현재 단계에서 제외됨**. 사용자 제공 추출본과 미러 비교를 정적 소스 검증 기준으로 사용.

1. **사용자 제공 추출본 검증:** R003의 PNG16 + blockstates14 + model39 = 69개 직접 검사. **R004는 해당 사용자 blockstates14를 다시 읽고 63가지 정적 variants를 각 leaf/부모 UV면에 대응.**
2. **미러 교차:** R003 69/69 Git blob SHA-1, PNG 16/16 별도 SHA256 일치. 이전 측정의 파일 동일성이 확인된 상태.
3. **Minecraft 실제 인게임 정적 렌더:** 미완료/0. 인게임 자료가 있을 때만 확인.

**검증 범위 변경(2026-11-13):** Mojang 공식 `client.jar` SHA-1·공식 메타데이터 인증은 **앞으로의 연구에서 제외**한다. 필수 조건, 미완료 항목 또는 다음 작업으로 계산하지 않는다. 기존 R001~R004 보고서의 역사적 언급은 당시 기록으로 보존한다.

## 유지해야 하는 누적 성과

- `TEX03-R001`: 미러 PNG 16종 4,096픽셀의 알파0 321/완전불투명3,775 등 실측.
- `TEX03-R002`: 모델 템플릿 면 **145개**에 대한 실제 UV 알파 교차 실측. 이 중 alpha0 참조 면 **20개**. Heavy Core·모루 윗면의 PNG 투명 영역은 모델 UV에 사용되지 않음.
- `TEX03-R003`: 사용자 제공 추출본의 고유 **69개 파일**(16PNG+14blockstate+39model)이 미러와 동일하며 PNG SHA256도 16개 전부 일치. 기존 색상·UV 실측 추가 0건.
- **`TEX03-R004` 신규:** user source blockstate JSON 14개를 다시 직접 파싱해 **63개 정적 상태 → leaf 23모델 → 템플릿 면 406회**로 전수 확장. **70개 참조 면**에서 alpha0 포함. UV 전체 **53,392회**, alpha0 **3,150회**는 상태별 **중복 텍셀 참조 횟수**일 뿐 고유 픽셀/실제 게임 가시 면 개수 아님.
- 핵심: `iron_door` 32상태×5면=160면, upper 16상태에서만 32면 alpha0; `iron_trapdoor` 16상태×6면=96면, 32면 alpha0; `anvil` 4상태×21면=84면 alpha0 0; `copper_grate` 1상태×6면 모두 alpha0 포함.
- **기존 R002 145개 템플릿 면 UV 값과 R001 픽셀 원본은 재사용했으며, 이를 R004의 신규 템플릿/픽셀 실측으로 합산 금지.**

## 이전 TEX03-R004 불변 결과 위치

- [R004 연구 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R004/REPORT.md)
- [상태별 406개 면 해석 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R004/STATE_FACE_RESOLUTION.csv)
- [63개 정적 상태 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R004/STATE_VARIANT_SUMMARY.csv)
- [14개 블록/16개 텍스처 집계 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R004/STATE_FACE_AGGREGATES.json)
- [R003 원본 출처 검증 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R003/REPORT.md)
- [R002 UV 원본 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R002/UV_ALPHA_FACE_CENSUS.csv)

## 다음의 A–G 과제 / 범위 제약

GitHub `STATE.json`/`HANDOFF.md`/R004/HEAD 우선 확인 후 **새 증거가 있을 때만** R006 신규 저장. 새 정적 소스 검증 근거나 실제 게임 정적 화면 증거를 우선한다. **공식 Mojang 원본 JAR 인증을 요구하거나 후속 과제로 지정하지 않는다.** 정적 JSON의 회전/UV는 실제 빛·면 가려짐·광택을 입증하지 못한다.

**애니메이션·키프레임·움직임 연구 보류**; Project Zomboid 변환 및 가구 3D 제작 금지. 다른 단계나 루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`, 전역 `v38` 수정 금지. **기존 R001/R002/R003/R004/R005 릴리스 파일 영구 불변**, 이 단계 전용 새 `TEX03-R006/` 결과와 이 단계 `STATE.json`/`HANDOFF.md`만 이후 쓰기 허용.
