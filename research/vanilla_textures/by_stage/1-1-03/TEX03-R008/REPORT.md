# TEX03-R008 — 1-1-03 금속·금속부품 애니메이션 소스 연구 재개·완료

**일자:** 2026-11-13 · **대상:** 사용자 제공 Minecraft Java 1.21.11 `1.21.11/`의 고정 PNG 16종 + 관련 blockstate JSON 14개 + 모델 JSON 39개 · **이전:** TEX03-R007 정적 소스 연구 완료 보존 · **전체 전역 v38 불변**.

> 사용자의 명시 지시로 **기존에 보류하던 애니메이션 연구를 재개**했다. 현재 남아있는 **인게임 관찰/공식 전체 JAR 인증 제외 정책은 유지**한다. 이 R008은 (1) PNG 프레임 애니메이션이 들어 있는지, (2) 모델/블록상태에 재생 시간이나 keyframe이 있는지, (3) 열림·닫힘에 대해 어떤 **정적 양 끝 모델**이 지정되는지 검증한 에셋 차원의 연구다.

## 1. 애니메이션의 두 층을 분리

- **Texture frame animation:** 하나의 PNG에 여러 프레임이 결합되어 있고, 동일 경로에 `<name>.png.mcmeta`의 `animation` 객체로 `frametime` / `frames` / `interpolate` 등을 정의. 참고 규칙: [Minecraft Wiki, Resource pack – Texture animation](https://minecraft.wiki/w/Resource_packs#Texture_animation). 이 규칙은 외부 형식 설명이고 이 보고서의 **실제 파일 존재 검사는 사용자 제공 원본에서 직접 수행**했다.
- **Block state/model selection:** `blockstates/<block>.json`의 `variants`에 따라 서로 다른 `models/block/*.json` 정적 모델을 선택한다. `open=false`와 `open=true` 모델이 다르다는 사실 자체는 중간 프레임·재생 간격·보간 곡선이 있다는 뜻이 아니다.
- **런타임 이벤트/물리 효과:** 레드스톤 이벤트, 모루 낙하, 구리 산화 같은 동작의 실제 시간/프로세스는 텍스처·모델·blockstate 에셋만으로 **직접 인증할 수 없다**. 사용자 지시로 인게임 검증은 제외된다.

## 2. 실측 ① — 16 PNG의 프레임 메타데이터 전수 검사

**16/16개** 사용자 제공 `1.21.11/assets/minecraft/textures/block/*.png`가 **16×16 단일 프레임**임을 R007 원본 검증 자료와 대조. **각각의 동명 `.png.mcmeta`를 GitHub 원본 경로에서 직접 조회했고, 16/16개 모두 404/NOT_FOUND.** 따라서 고정된 이 16개 PNG에는 에셋 형태의 **프레임 재생 정의가 0개**다.

단순한 도구 실패가 아님을 확인하기 위한 **양성 대조 3건(고정 16종의 수에 포함하지 않음)**:

| 실제 사용자 추출본 대조 예제 | PNG 원본 해상도 | 원본 `.png.mcmeta` |
|---|---|---|
| `water_still` | 16×512 → 16×16 타일 32개 | `animation.frametime=2` |
| `lava_still` | 16×320 → 16×16 타일 20개 | `animation.frametime=2`, `frames` 38개 재생 참조 |
| `fire_0` | 16×512 → 16×16 타일 32개 | `animation.frames` 32개 재생 참조 |

세 예제는 **동일한 사용자 제공 `1.21.11/` 하위 폴더**에서 실제 PNG 바이트, PNG 원본 너비·높이, `.mcmeta` JSON 및 Git blob SHA를 직접 확인했다. 이것이 금속 PNG 16종의 메타데이터 부재 검사에 대한 **양성 대조**이다. 세 컨트롤을 새 대상 3종이나 애니메이션 금속 PNG라고 기록하지 않는다.

`TEXTURE_ANIMATION_META_AUDIT.csv` **16행**에 모든 파일의 PNG 해시·정적 프레임 수·동명 `.mcmeta` 결과를 별도 보존. `CONTROL_ANIMATED_TEXTURES.json`에 3개 양성 대조 저장.

## 3. 실측 ② — 39개 모델과 14개 blockstate에서 시간축 구조 검사

- 관련 사용자 원본 모델 JSON **39개**를 다시 **직접 열고 JSON 키들을 재귀 조사**. `animation` / `frames` / `frametime` / `keyframe` / `timeline` / `duration` / `interpolate` / `easing` / `tick` 계열 시간 재생 필드 발견 **0/39**. 공간 `display.rotation`과 기하 UV 회전 값은 **정적인 좌표/표시 설정**이며 시간상의 회전 키프레임이 아니다.
- 연결된 원본 blockstates JSON **14개**도 직접 다시 열어 동등한 시간 재생 필드 검사, **0/14**. 14 JSON의 63 variants는 각자 하나의 **정적 상태** 설명.
- 고유 원본 기하 39개 모델의 명시적 geometry face 정의를 재합산하면 **91면**(중복 부모 cube 공유 구분), 이 중 `heavy_core` 6면은 R007에서 이미 교정한 6면을 사용한다. R002의 텍스처별 **145 템플릿 면**과 동일 분모가 아니며 혼동하지 않는다.
- `MODEL_TIMELINE_AUDIT.csv` **39행**, `BLOCKSTATE_ANIMATION_CLASSIFICATION.csv` **14행**에 각 실제 소스 경로·기존 검증된 Git SHA·현재 재확인한 시간축 부재/해석을 보존.

## 4. 실측 ③ — 철문/철다락문 닫힘·열림 양 끝 모델 24쌍

사용자 제공 `iron_door.json`, `iron_trapdoor.json`의 실제 `variants`를 파싱한 후 동일한 `facing`·`half`·`hinge` (해당하는 속성만)끼리 `open=false` ↔ `open=true`를 정확히 매칭하고 R004/R005의 기존 원장과 교차 확인했다.

| 블록 | 정적 변형 수 | `open=false → true` 짝 | 기하/면 구성 |
|---|---:|---:|---|
| `iron_door` | 32 | **16쌍** | `facing` 4 × `hinge` 2 × `half` 2. 실제 하나의 철문 위·아래가 2블록이므로 완성 철문 기준 **8종 방향/경첩 조합**을 두 반쪽에서 각각 기록 |
| `iron_trapdoor` | 16 | **8쌍** | `facing` 4 × `half` 2. `open=false` 수평판 → `open=true` 수직판 정적 geometry 선택 |
| **합계** | **48 상태** | **24쌍** | 24개 모두 양쪽 leaf 모델 이름이 다르고 원본 투영 경계가 다름 |

24쌍 모두 R004에서 **닫힘·열림의 모델 면 수와 alpha0 면 수, alpha0 UV 참조 횟수가 동일**하다. 이는 투명 구멍 수와 구조가 유지된다는 소스 증거다. 실제 화면상 움직이는 물리 각도나 보간 궤적을 뜻하지 않는다. R005에서 얻은 회전 후 x/y/z model-bound도 양 끝 모두 저장했고, 24쌍 모두 bounds 변화 확인. 블록 상태 JSON의 선언 `y` 회전 차는 `0°` 2쌍, `90°` 10쌍, `180°` 2쌍, `270°` 10쌍이나, **이 값은 블록 모델의 선언 회전 차이지 실제 움직임 각도/속도가 아니다.**

- `iron_door` upper는 각 변형의 UV에 **투명 포함 2면(면당 alpha0 48)**, lower는 **0면**. 두 종료 상태에서 동일한 alpha0 참조 수를 유지한다.
- `iron_trapdoor`은 두 끝 상태 각각 **투명 포함 2면(면당 alpha0 36)**. 판의 방향과 형태만 바뀌며 PNG 텍스처가 새로운 프레임으로 바뀌는 것은 아니다.
- 유저 자료에는 **이들 양 끝 상태 사이에 찍힌 intermediate model, 키프레임, 시간/보간 값은 없다.** 24쌍의 모든 원본 및 UV/좌표 근거는 `OPEN_CLOSE_STATIC_ENDPOINTS.csv` **24행** 참조.
- **구분:** Minecraft Wiki [Iron Door](https://minecraft.wiki/w/Iron_Door) 및 [Iron Trapdoor](https://minecraft.wiki/w/Iron_trapdoor)는 게임 사용 설명에서 개폐 시 방향이 즉시 바뀐다고 설명한다. 이는 **제3자 게임 설명**이고, 본 단계에서 실제 게임 렌더나 client 코드로 개폐 시간을 계측한 것은 아니다.

## 5. 다른 시각 변화는 프레임 애니메이션이 아님

- 고정 범위의 구리 블록 텍스처는 `copper_block`, `exposed_copper`, `weathered_copper`, `oxidized_copper`가 **각각 별도 정적 PNG**다. 동일한 PNG의 `frames` 재생이 아니다. 실제 산화가 시간/랜덤 틱에 따라 발생한다는 것은 [Minecraft Wiki – Oxidation](https://minecraft.wiki/w/Oxidation)의 **외부 게임 동작 설명**이며, 해당 속도나 이벤트 코드는 이번에 제공받은 14개 blockstate/39개 모델 JSON에서 확인하지 않았다.
- 고정 범위에 포함된 `anvil`은 `facing` 4방향 모델 회전뿐이다. **모루가 떨어지는 런타임 물리, 사용에 따른 마모·파괴**를 `anvil.png` 프레임 애니메이션이나 `anvil` 모델 키프레임으로 기록하지 않는다.
- `heavy_core`의 `display` 회전은 인벤토리/GUI 등의 **정적 표시 변환**, 시간축 애니메이션이 아니다.
- 나머지 단순 금속 블록 등 정적 상태 11개는 원본 blockstate가 각 1 variant이므로 이 고정 소스 안에 개폐·시계열 애니메이션 키가 없다.

## 6. 판정 / 과거 결과 보호 / 다음 작업

- **R008 새 연구 결과:** 16개 동명 애니메이션 파일 **직접 부재 확인**, 3개 실제 애니메이션 원본을 통한 **양성 대조**, 39 모델·14 블록상태 **시간축 필드 검사**, **24개 신규 정적 종료 상태 쌍의 원본 기반 대응 및 bounds/UV 연결**. 이들 24쌍은 R004/R005의 기존 상태·면을 **새 관계로 연결한 것이며 원본 unique variants/face 수에 더하면 안 된다**.
- **금속 16종의 에셋 기반 프레임/시간축 애니메이션 조사 완료.** 텍스처 자체에 재생할 추가 프레임이 없으므로 **애니메이션을 새로 만들어야 한다는 요구도 없다**. 필요하면 철문/다락문은 source-grounded **정적 상태 전환** 두 모델로 표현할 수 있다. 별도 부드러운 tween/중간 프레임 제작은 바닐라 파일에서 재현한 근거가 없어 **사용자 요청에 따른 신규 설계 작업**일 뿐 본 분석 실적이 아니다.
- **인게임 검증과 Mojang 전체 JAR 인증은 사용자 제외, 실제 런타임 코드/물리/셰이더 인증을 했다는 뜻 아님.** 기존 TEX03-R007의 정적 소스 완료 상태는 그대로 유지.
- 과거 TEX03-R000~R007 불변. 다른 1-1 단계/루트 HANDOFF, PROGRESS/전역 v38 불변. 다음 릴리스 **TEX03-R009는 기본 계획에 없으며**, 새로운 확장 대상·명확한 문제·소스 증거가 있을 때만 열 것.
