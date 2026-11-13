# TEX05-R003 — 사용자 직접 추출한 Minecraft 1.21.11 파일 우선 검증 및 출처 원장 정정

> 담당 **1-1-05 / 유리 6종** · 2026-11-13 · 선행 **TEX05-R001/R002 불변** · 프로젝트 공통 체크포인트 **v38 불변**.
>
> **출처 우선순위 정정:** 사용자는 저장소 `1.21.11/`를 자신의 Minecraft Java 1.21.11 JAR을 직접 추출해 업로드한 폴더라고 확인했다. 앞으로 이 **사용자 제공 추출본**을 원본 분석 자료로 우선 사용한다. 이는 **Mojang 공식 배포 JAR 무결성 인증을 뜻하지 않는다**.

## A. 선행 결과 대조 및 신규 공백 선정

- GitHub 단계 `STATE.json`: 이번 작업 시작 전 최신 `TEX05-R002`, 다음 `TEX05-R003`, 고정 표본 6, 전역 `v38`.
- R001 6종 PNG 실측·원본 SHA/CRC/전 RGBA 1,536행, 정적 면 36개 및 R002 반복 가장자리 분석은 그대로 존중한다. **R003의 27건은 새 텍스처 27개가 아니라, 같은 6종을 구성하는 파일 27개 직접 출처 검증 건수**다.
- 사용자 추출본 속 PNG·JSON과 미러의 일치 관계가 직접 원장에 따로 정리되지 않았던 공백, `cube → block`의 최상위 부모 정의 누락, 기존 R001 원장 SHA 문자 길이 오류를 집중 검사했다.

## B. 사용자 제공 추출본 직접 바이너리·해시 검사

- 실제 GitHub 경로: [사용자 추출본 `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11) (`assets/minecraft/` 하위).
- `assets/minecraft/textures/block/{glass,red_stained_glass,black_stained_glass,blue_stained_glass,green_stained_glass,white_stained_glass}.png` **6개 모두 GitHub에서 base64 원본을 취득**했다. 디코딩 후 Python `hashlib.sha256`, Pillow로 **6/6 기존 R001/v4 SHA와 바이트 지문 일치**, 해상도 **16×16** 확인. black/white의 원본 PNG mode가 `LA`임도 재확인.
- GitHub 추출본과 InventivetalentDev `1.21.11` 추출 미러에서 **6개 PNG 모두 원시 base64/ Git blob SHA 일치**. PNG 내용은 이전 실측과 동일하므로 추가 1,536 픽셀을 새 원본 표본으로 세지 않음.
- 각 PNG의 실제 저장 바이트 길이, Git blob SHA, 계산한 raw SHA-256은 `SOURCE_LEDGER.csv`에 저장.

## C/D1/D2. 텍스처 기존 정량 검증의 출처 갱신

- R001의 무색 glass alpha0 191·alpha255 65, 착색 5종의 alpha102 191·155 5·163 60, R002의 테두리·경계 수치는 **이번 사용자 직접 추출본과 PNG SHA-256가 동일**하므로 동일 데이터에 적용된다.
- 기존 정량 값을 새로운 연구 완료량으로 중복 산정하지 않는다. 기존 R001 `PIXEL_RGBA.csv`와 R002 `EDGE_RGBA_AUDIT.csv`를 우선 참고한다.

## E. 사용자 추출 JSON 21개 / 블록·아이템·상태 상속 직접 검사

- 여섯 `assets/minecraft/models/block/<name>.json`: `parent=minecraft:block/cube_all` 및 `textures.all=minecraft:block/<name>` **6/6**.
- 여섯 `assets/minecraft/blockstates/<name>.json`: 기본 `variants[""].model=minecraft:block/<name>`, 분기 없음 **6/6**.
- 여섯 `assets/minecraft/items/<name>.json`: `model.type=minecraft:model`, `model.model=minecraft:block/<name>` **6/6**.
- 공통 JSON 3개를 사용자 추출본에서 직접 읽음: `cube_all.json` → `cube.json` → `block.json`. `cube_all`은 6면 `#all` 및 `particle=#all` 바인딩. `cube`는 `from=[0,0,0]`, `to=[16,16,16]` 요소 1개와 `down/up/north/south/east/west` 여섯 `cullface`를 선언.
- **이번 추가 상속 확인:** `cube.json`이 `parent="block/block"`을 선언하는 점을 실제 확인했고, `block.json`은 `gui_light="side"`, `display` 속성 7종 `gui/ground/fixed/on_shelf/thirdperson_righthand/firstperson_righthand/firstperson_lefthand`를 정의한다. JSON 정적 선언으로만 해석한다.
- 원본 6×6=**36면** 모두 명시적 면 UV 항목 없음. R001의 기하에서 유도한 기본 `[0,0,16,16]`과 연결됨. 실제 게임 샘플링·컬링·조명은 추정하지 않음.
- 21개 JSON 모두 구문과 경로 의미를 검사했고, 외부 미러 동일 Git blob SHA까지 검증됨. 세부 지문은 `SOURCE_LEDGER.csv`, 6종 해석은 `MODEL_CHAIN_AUDIT.csv`.

## 기존 미러 교차 검증 — 사용자 추출본과 분리 기록

- 비교 대상: `InventivetalentDev/minecraft-assets` Git ref `1.21.11`, `assets/minecraft/`.
- 대상 수: PNG 6 + leaf 블록 모델 6 + blockstates 6 + items 6 + 부모 모델 3 = **27 경로**.
- 사용자 추출본과 미러의 **Git blob SHA 동일 27/27**, 6 PNG는 실제 base64 원시 바이트를 별도로 비교, 부모 모델 3개는 원시 JSON 텍스트도 비교. Git blob SHA 일치는 동일 Git blob 내용의 지문이며 **Mojang 원본 인증이 아님**.
- R001 `SOURCE_LEDGER.csv`의 `green_stained_glass` `blockstate_git_blob_sha`가 **39자리로 기록된 오류** 발견: 옛값 `ca4fec4067cffd89000ee64251f878bf0d530a8`, 실제 양쪽 자료 `ca4fec4067cffd89000ee64251f878bf0d530a8a`. 기타 R001 SHA 자리수 이상은 없음. 자세한 기록은 `LEGACY_LEDGER_ERRATA.md`. **R001/R002 원본 파일은 수정하지 않음.**

## F/D3. 4종 검증 수준을 절대로 합산하지 않음

| 검증 수준 | 상태 | 근거 |
|---|---|---|
| 1. 사용자 제공 JAR 추출본 파일 직접 검증 | **27/27 파일 정적 검증** | 사용자 GitHub `1.21.11/` 실제 PNG SHA·JSON 구조/상속 |
| 2. 기존 비공식 미러 교차 검증 | **27/27 파일 지문 동일** | 동일 경로 Git blob SHA 대조 |
| 3. Mojang 공식 배포 원본 `client.jar` 무결성 인증 | **미검증** | 원본 JAR 전체 바이트 SHA-1 및 공식 메타데이터 직접 인증 증거 없음 |
| 4. Minecraft 1.21.11 게임에서 렌더링 확인 | **미검증** | 실제 캡처·설정·테스트 결과 없음 |

- 이 27개 파일은 사용자의 **추출본**임을 사실로 받아들인다. 출처 확인과 JAR **전체 SHA-1 증명**은 구별한다.
- 공식 배포 JAR 바이너리/공식 버전 JSON 원본·인게임 정적 render layer/정렬·인접 유리 면 제거·조명 검증은 F/D3 `pending` 유지. 6개 대상의 공식/인게임 검증 건수는 각각 0/6.
- 애니메이션 분석은 전면 보류; Project Zomboid 변환·가구 3D 모델링 제외.

## G. 저장 구성, 불변성 및 인수인계

- `REPORT.md`: 지금 읽는 A–G 결과.
- `SOURCE_LEDGER.csv`: 총 **27개 실제 사용자 추출본 파일**의 경로/종류/크기/Git blob SHA·미러 일치·6개 PNG 원시 SHA-256. 동일 파일 재검수이지 신규 27텍스처 아님.
- `MODEL_CHAIN_AUDIT.csv`: 유리 6종 blockstate→leaf 모델→`cube_all/cube/block` 상속, 면·cullface·UV·아이템 참조·display 정보.
- `LEGACY_LEDGER_ERRATA.md`: R001 원장 39자리 Git SHA 기록 정정만 명시한 **추가형 이력**.
- `SUMMARY.json`: 4층 증거 수준 분리, 기존 측정값 재사용 및 보류 상태.
- R001/R002 하위 폴더와 커밋을 삭제·수정하지 않고 **R003 새 폴더**만 추가. 이 단계의 `STATE.json`, `HANDOFF.md`만 갱신. 루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`, 다른 재질 단계 및 전역 `v38` 수정 금지.
- 다음 버전은 실증 자료 확보 시 **TEX05-R004**로 독립 생성하고, 쓰기 전에 동시 수정/HEAD/SHA/경로 존재를 반드시 재검사한다.
