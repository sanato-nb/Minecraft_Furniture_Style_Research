# TEX11-R013 — 1-1-11 애니메이션 연구 재개: PNG 프레임과 블록상태 모델 변화

- **일자:** 2026-11-13
- **사용자 요청:** 보류했던 애니메이션 연구를 재개.
- **조건:** 사용자 제공 Minecraft Java 1.21.11 원본 리소스/모델 JSON을 기준으로 직접 검사. 사용자 결정대로 인게임 검증과 공식 JAR SHA-1 인증을 필수 범위에 다시 포함하지 않음. 실제 3D 애니메이션 클립 제작은 별도 업무.

## 조사 1 — 실제 텍스처 프레임 데이터
기존 `1.21.11/assets/minecraft/textures/block/` Git tree SHA `9a7172896d4a28b405b990733d51b77dcb50930c`를 직접 조회했다.
- 대상 **31/31 PNG 실제 존재 및 원본 blob 검증**. 바이트 직접 해독으로 **PNG CRC 31/31 통과**, 16×16 PNG **26개** + 32×32 PNG **5개**.
- 대상 PNG에는 `<name>.png.mcmeta` 파일이 **0/31개**. PNG 내 다중프레임/APNG 관련 `acTL`, `fcTL`, `fdAT` **0/31개**.
- 같은 `textures/block/` 폴더에는 다른 자산의 `.png.mcmeta` 99개가 있지만, 대상 31개는 없다. 대비 예: `blast_furnace_front_on.png.mcmeta`는 `animation.frametime=10` 및 `interpolate=true`, `water_still.png.mcmeta`는 `animation.frametime=2`. 99개가 모두 시간 애니메이션인 것은 아님.
- `assets/minecraft/atlases/blocks.json`(SHA `541ce56ad0b09f258963dd2bf3e3cb6e786d2d79`)의 atlas source는 `minecraft:directory`→`block/` 경로를 포함하며, 대상 31개의 시간 프레임은 설정하지 않는다.

## 조사 2 — 원본 JSON 시간/프레임 키
블록상태24·모델리프122·모델템플릿20 = **JSON 166개**, 각 파일을 현재 원본 Git tree blob SHA에 대조해 **166/166 일치** 확인.
- blockstate tree SHA `7a36f7d757e62aa61ee61aebcd8d5689bc462a8d`.
- model tree SHA `57eb7fbc4d0af0e931a04de94b4b6a766242d36e`.
- `animation`, `animations`, `frames`, `frame`, `frametime`, `interpolate`, `interpolation`, `duration`, `duration_ticks`, `ticks`, `keyframes`, `loop` 같은 시간·프레임 관련 키: **0개**.
- `blockstate.x/y/z` 및 `model.face.rotation`은 파일에 적힌 **정적 변환/UV 회전**이다. 키프레임 보간 시간으로 해석하지 않는다.

## 조사 3 — 애니메이션을 위해 필요한 정적 시작·끝 상태의 실제 연결
- **문 7종:** 7×4 facing×2 hinge×2 half = **112개 `open=false→true` 끝점 비교**.
- **다락문 12종:** 12×4 facing×2 half = **96개 `open=false→true` 끝점 비교**.
- **선반 5종:** 5×4 facing×4 side_chain = **80개 `powered=false→true` 끝점 비교**.
- 위 3종의 **핵심 끝점은 288쌍**이다. 추가로 선반의 `side_chain` 4개 값에서 6개의 서로 다른 역할 쌍을 골라, 5wood×4facing×2powered×6 = **240개 논리적 연결 비교 후보**를 계산했다. 총 **528개 원본 속성 차이 후보** 중 모델 지정이 실제 달라지는 후보 408, **동일 모델 120개**. 동일 모델인 120개는 선반 `powered=false`에서 `side_chain`만 다른 경우.
- **주의:** 선반 좌↔우처럼 단일 속성만 달라지는 모든 조합이 게임에서 한 번의 물리 이벤트로 발생한다는 뜻은 아니다. 그래프는 JSON으로 표현 가능한 **상태 쌍**이다.
- 전체 상태공간은 문224 + 다락문192 + 선반160 = **576개의 소스 파생 상태**. 이는 이전 R006의 신규 집계 544 + 역사적 전역 `v38` oak_shelf 32로 이해해야 하며, 신규 576상태를 기존 수치에 추가 계산하지 않는다.

## 조사 4 — 모델 형상과 UV, 정적 회전 끝점
`ENDPOINT_MODEL_GEOMETRY.csv`에 핵심 **288쌍**의 시작·끝 leaf/parent template JSON, `elements.from/to` geometry, `faces.uv`, 정적 XYZ 회전을 모두 연결했다.

| 유형 | 끝점 쌍 | geometry bounds 변화 | 정적 회전 변화 | UV 레이아웃 변화 |
|---|---:|---:|---:|---:|
| door open | 112 | 0 | 112 | 112 |
| trapdoor open | 96 | 96 | 52 | 96 |
| shelf powered | 80 | 0 | 0 | 80 |

- **문:** 열림 전후 local geometry는 `[0,0,0]→[3,16,16]`으로 같지만, **정적 Y 회전값과 UV 면 구성**이 112쌍 모두 바뀐다. 실시간 문 경첩 회전 속도·중간 위치는 알 수 없다.
- **다락문:** 닫힘 bottom `[0,0,0]→[16,3,16]` 또는 top `[0,13,0]→[16,16,16]`에서 열린 상태 `[0,0,13]→[16,16,16]`로 **96쌍 geometry가 바뀜**. 정적 X 회전 변화 **40쌍**, Y 회전 변화 **52쌍**(일부 중복). 특히 방향형 재질의 열린 상단 `x=180`은 정적 모델 지정 값일 뿐 애니메이션의 시간 단계가 아니다.
- **선반:** `powered` 변경 80쌍은 본체/전면 면의 geometry bounds·정적 회전은 같고 전면 **UV 영역이 80/80 바뀐다**. 전원이 꺼진 선반의 연결 속성만 바꾸면 선택 모델은 변하지 않는다.
- 출발/도착 모델 이름, x/y/z, 텍스처 슬롯, 요소 bounds는 소스 증거로 저장했다. **중간 프레임 생성, easing, duration, 힌지 pivot, 물리 충돌, 실제 렌더링/소리**는 PNG/JSON에서 검증할 수 없어 값을 지어내지 않았다.

## 결론과 과거 범위
**고정 대상 31 PNG의 독립 텍스처 프레임 애니메이션 데이터는 발견되지 않았다.** 이 에셋에서 확인 가능한 동작 표현은 **정적 상태의 모델·UV 변경 관계**이다. 그래서 이번 재개한 애니메이션 **원본 에셋 조사 범위는 완료**했으나, **엔진이 실제로 어떤 부드러운 모션을 재생하는지**에 대한 실험을 완료했다는 뜻은 아니다. 부드러운 애니메이션을 별도 구현한다면 pivot, 재생시간과 보간 규칙을 새 설계로 정의해야 한다.

R012의 source-only **31/31** 완료 상태와 R009–R011의 full model face PNG 596패치/68,960회 UV 참조는 기존 근거로 유지한다. 사용자 결정대로 **인게임 검증 제외**, 역사적 인게임 검증 기록 **0/31**, 공식 Mojang JAR SHA-1 인증 제외 유지. root `v38`, 다른 단계, 과거 릴리스 폴더는 변경하지 않는다.

**외부 보조 자료(위 원본 파일 분석과 분리):** Mojang Java Edition 1.21.9 안내는 선반의 redstone-powered 상태에서 전면 텍스처가 달라진다고 설명한다. https://feedback.minecraft.net/hc/en-us/articles/39966147272589-Minecraft-Java-Edition-1-21-9-The-Copper-Age
