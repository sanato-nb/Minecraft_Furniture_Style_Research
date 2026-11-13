# 1-1-08 — 복합·기능면 단계 전용 인수인계 (현재 TEX08-R005)

> **2026-11-13 · 라이브 다음 버전 `TEX08-R006` · 대상 21 PNG · 전체 v38 변경 없음**

## R005 신규 소스 비교
- 사용자 제공 `1.21.11/`의 원본 blockstate/model/부모를 다시 읽고, 기존 R004의 직접 소스 기하·상속 및 chiseled 책장 particle 수정 사항을 유지.
- **새 상태쌍 비교 62행:** 통 open 6, 화로류 lit 12, 벌통 honey 인접 단계 20, 조각된 책장 슬롯 변경 24. 일반 모델 로컬 면 변경 22쌍, 벌통 변화 없는 16쌍; lit 12쌍에서 모델 particle `#front` 참조도 바뀜.
- 새 정적 PNG 비교: `beehive_front`와 `beehive_front_honey`는 **24/256픽셀 RGBA 변경**, 알파 변경 **0**, bbox `(1,4)..(14,13)`. 사용자 추출본에서 `beehive_front_honey`, `beehive_side` 보조 PNG 직접 SHA/CRC/RGBA 확인. 두 보조 PNG는 **고정 21개 밖**이고 v35 선행 연구의 전역 신규 픽셀로 가산하지 않음.
- 상태쌍 기준 변경 UV 면적 **6,656 uses**는 기존 R004 32,512 uses 및 R001 5,376 원본 픽셀에 합산하지 말 것. `chiseled_bookshelf` 템플릿 `particle=#texture`는 자식에서 해결되지만 실제 multipart particle 렌더 선택은 **미확인**.
- 실게임 정적 렌더 **0/21**, 공식 전체 JAR 인증은 **사용자 범위 제외**(공식 인증 성공 아님). 애니메이션·다중 프레임/좀보이드 변환/가구 3D 제작 미수행.
- 불변 결과 경로: [TEX08-R005 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-08/TEX08-R005/REPORT.md), `STATIC_STATE_FACE_TRANSITIONS.csv`, `STATIC_PNG_BINARY.csv`, `BEEHIVE_RGBA_DIFFERENCE.csv`, `SOURCE_RECHECK_LEDGER.csv`, `SUMMARY.json`.
- 이후 새 근거가 있으면 **라이브 `next_revision`과 HEAD, STATE blob SHA 및 출력 폴더 부재를 다시 조회**하고 오직 1-1-08 전용 폴더·STATE·HANDOFF만 변경.

---

## 이전 R004 시점 인수인계 원문 (당시의 '다음 R005' 지시는 만료됨)


> 2026-11-13 · 다음 `TEX08-R005` · 고정 PNG 21개 · 전체 `v38` 불변 · R001–R004는 새 원본이 있어도 수정/삭제 금지.

## 2026-11-13 사용자 지시 — 공식 인증 항목 제거
**공식 Mojang 배포 JAR의 전체 SHA-1 및 manifest 인증을 이번 단계의 필수/선택 연구 작업표에서 제외한다.** 사용자 제공 추출본의 파일 분석 및 비공식 미러 교차 검증은 계속 수행한다. 본 변경은 연구 범위 정책만 변경하며 신규 PNG/모델 검증이나 `TEX08-R005` 연구 릴리스가 아니다. 과거 `R001`–`R004`는 수정하지 않는다.

## 원본 / 검증 분리
- 1차: **사용자가 직접 client.jar을 압축 해제했다고 명시한** [GitHub `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11) 내 `assets/minecraft/`.
- 2차: 이전 미러 `InventivetalentDev/minecraft-assets` 1.21.11, 파일 SHA 교차용.
- **공식 Mojang JAR 전체 SHA-1 / 버전 메타데이터 인증은 사용자 지시에 따라 연구 범위·완료 조건에서 제외(2026-11-13).** 향후 기본 작업에서 시도하거나 미완료 필수 항목으로 세지 않음. 과거 보고서의 '0/21'은 역사적 사실로 보존하되 인증 완료를 주장하지 않는다.
- 게임 내 **정적 렌더 관찰은 별개**이며 현재 0/21. 실제 인게임 자료가 없으면 미관찰로 보존.

## 누적, 중복 없는 단계 기록
- `TEX08-R001`: 21 PNG/5,376 원본 픽셀 분석, 고정 대상 62 모델 face 자료; 비공식 미러 근거.
- `TEX08-R002`: 16 blockstate/73 variants+52 multipart, 정적 통 open/closed 비교, 62 대상 face UV 면적 13,056 uses; 미러 기반.
- `TEX08-R003`: 사용자 추출본 77 고유 파일 Git blob SHA 확인, 기존 미러 SHA 71/71 동일; JSON 직접 파싱 blockstate16 + model10, PNG 헤더7.
- **`TEX08-R004` 새 실측:** R003에서 읽지 않았던 모델 29개의 추출본 JSON 직접 파싱 + 공통 부모 8개 파싱. 단계 모델 **39/39 실제 JSON 소스 확인**, 부모 포함 47 고유 JSON 경로. **143 model-face rows / 명시 UV29 / 암시 UV114 / UV 면적32,512 uses(픽셀 신규 측정치 아님)**.
- `chiseled_bookshelf`: 본체 정면 north 미선언(5면), 슬롯 6개 zero-depth 평면 x 좌우 반전 UV, 템플릿 particle=`#texture`가 child에서 상속 해결됨. **기존 R001/R002의 'overlay particle 없음' 표현을 모델 선언 차원에서 정정**. 실제 게임 최종 particle 렌더링 선택은 아직 미검증.
- `chiseled_bookshelf` blockstate yaw north0/east90/south180/west270; base `uvlock=true`, 12 slot 규칙/방향은 uvlock 생략. 52 규칙 신규 카운트 가산 금지.
- 정적 소스 해석용 결과: `research/vanilla_textures/by_stage/1-1-08/TEX08-R004/` 의 `REPORT.md`, `SOURCE_LEDGER.csv`, `MODEL_INHERITANCE.csv`, `MODEL_FACE_RESOLUTION.csv`, `CHISELED_SLOT_GEOMETRY.csv`, `CHISELED_FACING_UVLOCK.csv`, `SUMMARY.json`.

## 재개
1. GitHub 이 단계 `STATE.json`과 `HANDOFF.md`를 다시 읽고 `next_revision=TEX08-R005`, 파일 blob SHA 및 새 릴리스 미존재 확인.
2. 사용자 추출본에서만 정적 추가 근거 확인, 과거 픽셀 재실측/누적 부풀리기 방지.
3. **공식 JAR 인증은 필요 없음(범위 제외).** 인게임 정적 관찰은 실제 실행/캡처 근거가 있을 때만 기록하고, 근거 없으면 미관찰 상태 유지. 새 연구 근거 없이는 임의 완료/버전 증가 금지.
4. 이 단계 `HANDOFF.md`, `STATE.json` 및 새 `TEX08-R005` 외 파일 수정 금지. 다른 단계/루트/전체 v38은 건드리지 않음.
5. **애니메이션 프레임·움직임 연구 보류**, PZ 변환 및 실제 3D 가구 제작 금지.
