# TEX02-R012 — 실제 FaceBakery 정점/UV 정렬과 R007 코너 40개 재검증 및 북쪽 면 가상 이음새 64건 재측정

- 작성일: **2026-11-13**
- 범위: 고정 연구 단계 `1-1-02` — Minecraft Java 1.21.11 석재·벽돌 **17개 PNG**. 사용자 제공 `1.21.11/` 원본 코드·PNG 및 **변경 불가 R007/R010/R011 선행 자료**에서 직접 증거 검증
- 인증 정책: 전체 Mojang 공식 client.jar SHA-1 인증은 필수 요건에서 제외하며 인증 완료 주장을 하지 않음
- **인게임 정적 검증 0/17**; 다음 결과는 모두 원본 바이트코드·정적 PNG를 이용한 계산이며 실제 게임 renderer/GPU 실행이 아님

## 1. R011 이후 이번의 새로운 원본 코드 검증

R011에서는 회전 부호를 수정해 기존 R007 월드면 방향 **32/186건 불일치**를 찾았다. 그러나 월드면 방향이 맞더라도 면에 올라가는 텍스처 코너가 잘못될 수 있었다.

R012는 이미 존재하던 클래스들을 **새로운 내부 지점까지 재분석**했다. 이 클래스들을 '새로 처음 본 클래스'로 중복 집계하지 않는다.

1. `hoa$a.class`의 원본 클래스 초기화에 `MIN_X`, `MIN_Y`, `MIN_Z`, `MAX_X`, `MAX_Y`, `MAX_Z` 6개 selector가 존재함을 직접 확인.
2. `hoa.class`의 `<clinit>` 588바이트에서 **DOWN, UP, NORTH, SOUTH, WEST, EAST × 정점 4개 = 24개 canonical vertex selector**를 실제 `hoa$b` 구성자 인자로 검증. `HOA_FACE_CORNERS_24.csv`에 저장. 각 면의 배열은 인덱스 0=좌상단, 1=좌하단, 2=우하단, 3=우상단의 **원본 direction별 baked-vertex ordering**이다. 이는 임의의 screen-orientation 재정의가 아니다.
3. `hqi.class` (`FaceBakery`)의 `bakeQuad` 184바이트, `bakeVertex` 181바이트, `sortVertices` 295바이트, 정점/packed UV swap 두 메서드 각각 15바이트를 **호출·분기 단위로 재확인**. `bakeQuad`는 face별 `hoa`의 초기 4개 정점을 만들고, 방향 법선을 확인한 다음 **요소 자체 회전이 없으면 world-face `hoa` 코너 좌표에 맞도록 정점과 텍스처 UV 배열 모두를 swap**한다.
4. `hqc$b.class`의 `a(index)`/`b(index)` 코너 선택 규칙 계승: `[u1,v1],[u1,v2],[u2,v2],[u2,v1]`; UV transform은 R010에서 source-checked된 일반 `inm`의 항등 UV-lock 보정 경로. 모델의 소스 face rotation이 별도로 명시되지 않는 현재 full-cube 표본들에서 `g`의 offset 0 적용.
5. R011의 `f/h/g` 원본 회전 그룹 5개 행렬을 원본 정점 **(from,to)=(0,16)**의 0..1 정규화된 4개 꼭짓점에 중심 `0.5`을 기준으로 적용했다. **실제 quad builder 실행을 모방한 정적 코드 경로 계산**이지 게임 렌더러를 실제 실행해 관측한 baked quad 객체는 아니다.
6. R007의 기존 `implicit_auto_uv_assumed`는 R008에서 검증된 full-cube 기본 UV `[0,0,16,16]`를 사용하며, `explicit_U_reverse`는 사용자 원본 `cube_mirrored.json`의 `[16,0,0,16]`를 사용. 모델 parent/texture 연결과 PNG 이름은 R007의 원본-연결 자료를 계승한다.

이 계산은 **원본 정점 순서, 반사/회전, UV 코너 선택과 정렬**에서 R007보다 소스 근거가 강화되었으나, 모든 `inw$a` vertex-pipeline 변형, GPU interpolation/texture sampling, 실제 게임 화면을 인증하지는 않는다.

## 2. 기존 R007의 186개 face UV 코너 감사 및 40개 교정

R010의 **31개 기존 blockstate variant**, R011의 **회전행렬 5개**와 R007의 **186개 원본 face 행**을 같은 `(block, property, variant_index, local_face)`로 연결. 로컬 꼭짓점 4개를 world cube로 회전시킨 뒤, 월드면의 `hoa` canonical 4개 꼭짓점과 **모두 4/4 정확히 일치**하는 원본 인덱스를 찾았다. 행렬 5개 모두 0/1 큐브 중심 회전의 signed permutation이라 꼭짓점 격자 외 좌표가 없었다.

- **186면 전부 원본 정점 매칭 4/4 성공**.
- R007의 기존 top-left/top-right/bottom-right/bottom-left UV 코너값과 R012의 bytecode-derived 배열 비교: **146면 일치, 40면 불일치**.
- 40면은 전부 `deepslate`: `axis=x` **24개**, `axis=z` **16개**. `axis=y` 24면과 나머지 114면 UV 코너값은 이번 가정 범위에서는 일치.
- R011의 월드면 방향 오류 **32개가 40개의 UV mismatch와 겹치며**, 추가 **8면은 월드면 방향이 일치했지만 UV 코너가 불일치**한다.
- `REBAKED_UV_AUDIT_186.csv`: 모든 face의 R007/R012 월드 방향, 원본 정점→월드 정점 인덱스, UV 좌표 8+8개, 차이 여부.
- `R007_UV_CORNER_CORRECTIONS_40.csv`: 실제 차이가 있는 40면만 별도 기록. **R007은 변경하지 않음.**

**중요:** 코너 40개의 차이는 40개의 PNG 픽셀이 틀렸다는 뜻이 아니다. 모델 면별 **UV 코너 배치 해석**이 달라진 것. 실제 월드에서 렌더된 40개 이미지/UV를 측정했다는 뜻도 아니다.

## 3. R011의 이음새 재투영 대기 64건, 실제 16×16 소스 PNG로 새 계산

이번에는 단순히 “64건 재측정 필요”라고 남기지 않고, 사용자 제공 원본 PNG를 직접 base64 바이너리로 다시 가져와, PNG 디코드 후 **RGB 16×16×2 = 512 pixels**를 실제로 읽었다.

| 사용자 원본 이미지 | Git blob SHA | 용도 |
|---|---|---|
| `1.21.11/assets/minecraft/textures/block/deepslate.png` | `bb7dc9ced1943d1dc86ab0cded598e8541fd280a` | `axis=x` north face 로컬 `west`로 구성 |
| `1.21.11/assets/minecraft/textures/block/deepslate_top.png` | `a560ccfb90cae70a1df6d2fd89d0c6405c2c4347` | `axis=z` north face 로컬 `up/down`으로 구성 |

두 PNG 모두 원본 16×16 indexed palette 이미지로 읽고 Git blob SHA가 사용자 저장소와 일치함을 확인했다. **새 고유 텍스처 발견 0개** (R002–R003에서 이미 검증한 fixed `deepslate.png`와 supplemental `deepslate_top.png`를 재열람).

- `axis=x` 4 variant, `axis=z` 4 variant, 북쪽 면 UV **8개 정적 픽셀 투영**을 `NORTH_FACE_SOURCE_UV_8.csv`에 기록. 각 variant의 source local face 및 코너 좌표·원본 PNG SHA를 포함.
- 각 축에서 **4 left × 4 right × 2 이음새 방향** = 32, 두 축 합계 **64개** 기존 R007 가상 이음새를 새 source-UV 변환으로 **재구성 후 재측정**.
- **16 RGB 픽셀 쌍/행 × 64행 = 1,024 픽셀 쌍**, 각 3개 RGB 채널 비교(총 3,072 channel-pair differences)를 다시 계산.
- 재계산 결과 **RGB 차이 합계/평균/불일치 픽셀 수가 R007 기존 집계와 64/64건 전부 같음**; 집계 차이 0건.
- `R007_NORTH_SEAMS_RECALCULATED_64.csv`에 R007 기존 집계와 R012 새 집계, 원본 PNG, source local-face, 동일 여부를 함께 저장.

**왜 결과가 일치해도 40개 UV 교정이 필요한가?** R007의 UV 코너 해석 오류는 실제 이미지 배치의 방향과 특정 면의 식별에 영향을 준다. 그러나 이 **특정한 64개의 16픽셀 경계 RGB 합계·불일치 수 같은 집계값**은 교정 전후 우연히 동일할 수 있다. R007의 *픽셀별 차이 배열*은 없으므로 픽셀 순서까지 모두 동일한지 확인된 것으로 과장하지 않는다. 또한 **인게임 실제 블록 이음새**를 확인한 것은 아니다.

## 4. 고정 분모/실적 계수

- 표본 고정 17 PNG; 기존 RGBA 4,352 픽셀; 모델 JSON/기존 variant 31 및 face 186 모두 계승. R007 134개 가상 비교는 기존 번호를 유지. R011 32개 방향 교정도 계승.
- **이번 신규 연구 산출:** face canonical 24줄(기존 클래스의 새로운 세부 추출), face UV 감사 186개/신규 발견한 오류 40개, 8개 보정 북쪽 면 투영, 과거 R007에서 유래한 가상 seam 64행 **독립 재측정(새로운 고유 이음새 쌍이 아니라 보정 기준 재평가)**.
- 이전 R007 가상 이음새 64행의 “재투영 필요” 표시는 이제 **'집계 재투영 완료, R007 집계값 64개 모두 재현'**으로 해소. 원래 134개 전체/실제 인게임 화면 확인에는 적용하지 않는다.
- 이번 연구에서 새롭게 처음 열어본 `.class` **0개** (이미 R008~R011에 열람한 클래스의 메서드 및 실제 enum table을 깊게 확인함). 원본 클래스·PNG 재열람은 신규 asset/새 모델 수에 가산하지 않는다.

## 5. 남은 미검증과 다음 작업

**F 인게임 정적 검증 0/17, 전체 A–G 완료 0/17.** `MinecraftClient` 런타임의 concrete `inw$a` 변형 경로, GPU의 이미지 interpolation, lighting/filtering, 실제 blockstate random variant 선택 규칙 및 게임 내 이음새/방향 확인은 아직 미검증이다. 같은 표본을 더 큰 모델로 바꾼 적 없음. 공식 Mojang JAR SHA-1 인증 필수 요건 제외/인증 성공 주장 없음. `v38`, 다른 연구 단계, 이전 R001–R011 저장 파일은 변경하지 않음.

다음 단계 후보 `TEX02-R013`: 라이브 STATE/HEAD 재확인 후 **`inw$a`(vertex transformation), `hqm` 모델 bake 호출, variant 가중치·선택 경로를 원본 클라이언트에서 추적**하거나, PNG 정적 경계 134행 중 이번에 범위를 제한한 나머지 70행을 같은 코드 기반 방법으로 감사할 수 있음. 게임 렌더나 사용자 제공 자료만이 남는 시점에는 새 버전 번호 생성 대신 멈추고 자료를 요청할 것.
