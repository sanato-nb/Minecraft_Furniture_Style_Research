# 1-1-03 금속·금속부품 — 독립 채팅 인수인계

**최신 완료 단계: TEX03-R008 애니메이션 에셋 조사 완료 / 정적 소스 TEX03-R007 완료 보존 / 필수 다음 연구 없음 / 전역 v38 그대로.** 2026-11-13. 공식 JAR 인증 및 인게임 렌더 검증 제외 정책 반영(연구 릴리스 번호 유지).

## TEX03-R008 — 보류했던 애니메이션 연구 재개 후 에셋 차원 조사 완료 (2026-11-13)

[애니메이션 소스 연구 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R008/REPORT.md) · [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R008/SUMMARY.json) · [24개 모델 상태 양 끝](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R008/OPEN_CLOSE_STATIC_ENDPOINTS.csv)

**사용자 명시 지시로 애니메이션 연구 보류를 해제함.** 사용자 인게임 검증 제외·Mojang 공식 전체 JAR 인증 제외는 계속 적용. R007 정적 소스 완료 결과는 변경하지 않음.

- 대상 원본 PNG **16종 모두 16×16 단일 프레임**, 대응 `<texture>.png.mcmeta` **16/16 부재(직접 GitHub 원본 파일 조회)**. 별도 프레임 애니메이션 0종.
- 같은 사용자 추출 원본의 애니메이션 **양성 대조 3종**: `water_still` 16×512, `lava_still` 16×320, `fire_0` 16×512 PNG 및 각각 `.mcmeta.animation`을 직접 확인. 이 3종은 고정 금속 연구 샘플 16개에 **합산하지 않음**.
- 사용자 원본 관련 **39 models JSON + 14 blockstates JSON** 직접 재검사, 재생 시간·프레임·키프레임·타임라인 필드 **0건**. 모델 회전·GUI display 변화는 시간상의 프레임이 아닌 정적 설정.
- `iron_door` **16쌍**(위/아래 두 반쪽 포함, 완성 문은 8 facing×hinge 조합), `iron_trapdoor` **8쌍**의 `open=false↔true` 양 끝 모델을 직접 매칭하여 새 정적 대응 **24행** 기록. 24쌍 모델 참조·좌표 투영 경계 변화 확인; 중간 interpolation 프레임/시간 정보 **0건**. 이를 신규 고유 모델 24개로 중복 집계 금지.
- 구리 산화 단계는 **서로 다른 정적 PNG**, 모루 회전은 **정적 facing 모델**. 낙하·산화 속도 같은 런타임 동작은 이번 에셋이 인증할 수 없으므로 검증 성공으로 표기하지 않음.
- **애니메이션 관련 에셋 소스 조사는 완료.** 다음에 `계속해줘`를 받으면 고정 16종 연구가 끝났음을 알리고 멈춘다. 새로운 원본/범위, 구체적 오류, 사용자 지정 커스텀 animation 제작 요청 때만 R009 재개 후보 검토.

## 최종 상태 — TEX03-R007 (2026-11-13): 1-1-03 정적 소스 연구 완료

[최종 R007 연구 검수 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R007/REPORT.md) · [16종별 최종 감사 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R007/SOURCE_ONLY_ITEM_CLOSEOUT.csv) · [A~G 완료 판정 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R007/SOURCE_ONLY_COMPLETION_AUDIT.json) · [기존 R003 오류 정정 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R007/LEGACY_LEDGER_EXCEPTIONS.csv)

**검수 결과: A·B·C·D1·D2·D3·E·G 완료. F 인게임 사용자 제외, Mojang 전체 JAR 인증 제외, 애니메이션 보류.** 고정 대상 16종만의 정적 소스 연구를 완료 처리한다. 전체 프로젝트 완료가 아니다.

- 사용자 제공 `1.21.11/` **원본 PNG 16개**를 직접 다시 읽고 16×16/시그니처/CRC/Git SHA 검증 **16/16 일치**. 총 3,176바이트. SHA-256은 선행 R003 검증 계승. 4,096 고유 RGBA 픽셀 새 측정으로 중복 가산하지 않음.
- 사용자 원본 blockstates JSON **14/14**, models JSON **39/39** 직접 재취득·파싱해 해시/부모/상태 연결 검사. 정적 states **63개**, UV 부모 템플릿 **145면**(R002), 상태×모델 면 **406개**(R004)를 교차 대조. **406/406** 값 일치, 상태별 합계 **63/63** 일치, R006 투명 면 **70/70** 일치. 새 원본 경로 누락 0건.
- **과거 자료 메타데이터 오류 1건 정정 기록:** `TEX03-R003/USER_MODEL_JSON_CROSSCHECK.csv`에 `heavy_core` `explicit_geometry_faces=0`이라고 적혀 있지만 원본 JSON의 모델 요소는 **실제 6면**. R002·R004 실제 UV/모델 면 집계는 이미 6면으로 올바르므로 분석 누락·완료 방해는 아님. 과거 릴리스 내용은 변경하지 않았음.
- **다음에 `계속해줘`를 받으면**, 같은 16종 범위에 대해 새 버전을 인위적으로 만들지 말고 **연구 완료를 알리고 정지**. 사용자가 신규 원본·새 오류·확장 범위를 지정할 때만 `TEX03-R008` 후보를 평가한다. 스크린샷이나 게임 실행 요청 금지.

## 현행 검증 범위 결정 (2026-11-13, 사용자 지시)

**인게임 정적 렌더/스크린샷 검증을 필수·대기·추가자료 요청 범위에서 완전히 제외한다.** 사용자 제공 Java 1.21.11 추출본의 **원본 PNG·모델 JSON·블록 상태 JSON**으로 정적 텍스처 및 모델 연결/상태/UV 분석을 진행·판정한다. **Mojang 공식 전체 JAR 인증도 이전 사용자 지시대로 제외**한다.

- 인게임을 직접 관찰한 기록 **0/16**은 역사적 수치로만 보존한다. **0/16을 미완료 과제, 소스 연구 합격 방해 조건, 사용자에게 스크린샷을 요구하는 근거로 취급하지 않는다.**
- 출처 파일 무결성, RGBA/색상·알파·패턴, 부모 모델/텍스처 슬롯, 정적 blockstate variants·UV·회전 연결을 **현행 검증 기준**으로 사용한다. 실게임 조명·가려짐·GPU 렌더링을 검증했다고 주장하지 않는다.
- **F 항목은 `excluded_by_user`**이며 남은 A–E의 소스 연구 성과는 기존 근거에 따라 별도로 평가한다. 원본 과거 계획의 F 체크리스트 문구보다 **본 정책과 단계 `STATE.json`이 우선**한다.
- `TEX03-R006` 현재 버전, `TEX03-R007` 다음 후보, 전역 `v38` 그대로. 이번 정책만 변경하므로 신규 연구 릴리스/고유 픽셀·면 실적을 만들지 않았다.
- 앞으로 사용자가 **`계속해줘`**라고 하면 새 소스 근거가 있을 때만 정적 연구를 수행한다. 새로 확인할 비중복 정적 증거가 없으면 **중단하고 그 사실을 알리며, 인게임 자료 제출을 요청하지 않는다.**

## TEX03-R006 — 이전 최신 소스 기반 RGB·투명 마스크/정적 UV 미러 분석

[최신 R006 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R006/REPORT.md) · [R006 SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R006/SUMMARY.json)

- 사용자 `1.21.11/` 원본 PNG **3개** 직접 SHA-256/CRC 재검사 및 768 RGBA 재디코딩(이미 R001 누적 표본에 포함됨), 원본 blockstate **3개**·leaf model **8개**·중간/geometry model **9개** 재조회. **신규 원본 파일 수 0**; 기존 R005 70개 투명 포함 상태×면을 다른 속성으로 확장 연구.
- PNG 수평 반사 후 **alpha 불일치**: `iron_door_top` 0, `iron_trapdoor` 0, `copper_grate` 98픽셀. **불투명 RGB 차이**: 각각 114/56/116픽셀(원본 불투명↔불투명 대응만 비교).
- 정적 상태 **49개**(철문32/철다락문16/구리 격자1), 그중 투명 포함 상태 **33개**. 기존 alpha 포함 상태×면 **70개** 중 실제 수평 UV 반전은 **철문 상부의 16개 면만**, 이 16개의 구멍 위치는 모두 원본과 일치(대칭 alpha)하지만 금속 색상 무늬는 반전됨. **114×16=1,824**는 동일 텍셀의 중복 면 참조 횟수로 고유 픽셀 증가 아님.
- 원본 UV가 선언되지 않은 `cube_all → cube` 경로는 이전 R005 규칙에 따라 기본 면 좌표 해석. 70면의 38개에 cullface 선언. `STATE_MIRROR_RESEARCH.csv` 49행, `ALPHA_FACE_UV_MIRROR_CENSUS.csv` 70행, 원본 색/alpha 비교 3행, 마스크 좌표 행 48개를 새로 작성.
- 과거 **F 인게임 정적 렌더 확인 0/16** 기록은 사실로 보존하되, **현행 F 요구는 사용자 지시로 제외**. Mojang 공식 JAR SHA-1/메타데이터 확인도 사용자 요청으로 제외(성공 인증이 아님). 애니메이션·PZ·실제 3D 가구 제작 보류.

## TEX03-R005 — 선행 분석 (R001–R004 계승)

[최신 REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/REPORT.md) · [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/SUMMARY.json)

- **새로 읽은 사용자 원본:** PNG 6개(1,536 RGBA 재디코딩, SHA-256·PNG CRC 합격), blockstate 14 JSON 및 실제 면을 소유한 템플릿 모델 14 JSON. 기존 R003 69개 원본 목록에 이미 있는 파일이므로 신규 원본 34개라고 가산하지 않는다.
- **새로 기록한 원본 투명 좌표 321행:** 모루 윗면 96·Heavy Core 64는 모델 UV 밖, 철문 위 48·철다락문 36·구리 격자 77은 모델 UV에 포함. 사용 161 / 미사용 160. R001 이전 4,096 RGBA의 하위 집합 재측정임을 명시.
- **원본 기하 406개 상태별 면 대조:** `elements.faces` 406/406 존재, 명시적 UV 346행, 원본 `cube.json` 기본 생략 UV 60행. model-side cullface 272행, face UV rotation 84행, 선언된 UV 경계 역전 148행. 원본 blockstate 14종의 63상태 모델·회전 일치.
- **새 상태별 원본 PNG 알파 교차검증:** 6 PNG 관련 UV 면 **272/272 재검산 일치**, 나머지 134면은 R004·R002 유지. 기존 406면은 다시 신규 UV 실측으로 합산하지 않는다.
- **추가 산출:** [STATE_WORLD_FACE_PROJECTION.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/STATE_WORLD_FACE_PROJECTION.csv), [STATE_WORLD_ALPHA_SUMMARY.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/STATE_WORLD_ALPHA_SUMMARY.csv), [SOURCE_ALPHA0_COORDS.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/SOURCE_ALPHA0_COORDS.csv), [PNG_ALPHA_MASK_SUMMARY.csv](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R005/PNG_ALPHA_MASK_SUMMARY.csv).
- 철다락문 source `open=false`은 위/아래 투명 면, `open=true`는 수평 방향 투명 면. 철문은 upper에만 2개씩 투명 포함 면. **정적 소스 회전 방향이지 실제 게임 렌더 인증은 아니다.**
- 과거 인게임 정적 렌더 **0/16** 기록 보존(현행 검증 범위에서는 제외), 공식 Mojang JAR 전체 인증도 **사용자 지시로 제외**. 애니메이션·PZ 변환·3D 가구 제작 보류.

## 우선 출처·검증 기준

사용자가 직접 Java Edition 1.21.11 `client.jar`를 풀어 올린 [GitHub `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11) 폴더의 소스를 **우선 사용**. 이전 비공식 `InventivetalentDev/minecraft-assets@1.21.11`는 교차용. **공식 Mojang JAR 인증은 사용자의 요청에 따라 현재 단계에서 제외됨**. 사용자 제공 추출본과 미러 비교를 정적 소스 검증 기준으로 사용.

1. **사용자 제공 추출본 검증:** R003의 PNG16 + blockstates14 + model39 = 69개 직접 검사. **R004는 해당 사용자 blockstates14를 다시 읽고 63가지 정적 variants를 각 leaf/부모 UV면에 대응.**
2. **미러 교차:** R003 69/69 Git blob SHA-1, PNG 16/16 별도 SHA256 일치. 이전 측정의 파일 동일성이 확인된 상태.
3. **Minecraft 인게임 정적 렌더:** 사용자 지시로 **검증 요구에서 제외**. 과거 직접 인증 0건 기록만 보존하며 스크린샷 요청이나 미완료 상태로 사용하지 않는다.

**검증 범위 변경(2026-11-13):** Mojang 공식 `client.jar` SHA-1·메타데이터 인증 및 실제 인게임 정적 렌더/스크린샷은 **앞으로의 연구에서 제외**한다. 필수 조건·미완료 항목·다음 작업·사용자 자료 요청으로 계산하지 않는다. 기존 R001~R004 보고서의 역사적 언급은 당시 기록으로 보존한다.

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

GitHub `STATE.json`/`HANDOFF.md`/R004/HEAD 우선 확인 후 **새 증거가 있을 때만** R007 신규 저장. 새로운 비중복 정적 소스 검증 근거를 우선하며, 실제 게임 화면 증거를 요구하지 않는다. **공식 Mojang 원본 JAR 인증을 요구하거나 후속 과제로 지정하지 않는다.** 정적 JSON의 회전/UV는 실제 빛·면 가려짐·광택을 입증하지 못하지만 그런 실게임 검증은 현행 연구 완료 조건에서 제외됐다.

**애니메이션·키프레임·움직임 연구 보류**; Project Zomboid 변환 및 가구 3D 제작 금지. 다른 단계나 루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`, 전역 `v38` 수정 금지. **기존 R001~R008 릴리스 파일 영구 불변.** 현 단계 소스 정적/애니메이션 연구는 모두 완료. 신규 쓰기는 요구되지 않으며, 새 연구 재개 시 `TEX03-R009/` 후보와 해당 단계 `STATE.json`/`HANDOFF.md`만 수정 가능.
