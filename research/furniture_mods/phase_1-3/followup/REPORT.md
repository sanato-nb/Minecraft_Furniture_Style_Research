# 1-3-C·D 후속 — 형상 예외 재검수와 실제 조립·충돌 검증

2026-11-19 KST. 기존 C/D 원장의 고정 모델 16,572개와 블록 상태 1,158개에서 이전에 미확인으로 남긴 항목을 재검토했다. 실제 인게임 시험은 각 모드가 지원하는 Minecraft Java 버전의 평지에서 진행했다.

## 1-3-C 부모·기하

| 항목 | 후속 검증 |
|---|---|
| 정적 요소 미산출 108개 | **생성형 아이템 58개**, **Handcrafted 요소 없는 기반 템플릿 6개**, **Macaw 부모 누락 44개** |
| 생성형 아이템 58개 | 소스의 텍스처 레이어를 실제 PNG에 대조했다. 아이템 58개를 `item_display`에 표시하고 저장된 아이템 ID와 실제 화면을 모두 확인했다. Another 1, Handcrafted 55, Macaw 2 |
| Handcrafted 기반 템플릿 6개 | 각각 일반 요소를 선언하지 않으며, 직접 블록 상태 선택은 0이다. 자식의 부모 참조는 여섯 경로 모두에서 확인했다 |
| Macaw 부모 누락 44개 | 공식 JAR에서 `block/parent/desk`, `block/parent/drawer_base`가 없다. 44개에 대한 직접 블록 상태 선택과 별도 아이템 정의 참조는 모두 0이다. 실제로 배치한 참나무 책상과 서랍은 다른 모델 경로를 사용했다 |
| Another 부모 누락 4개 | 선언은 `minecraft:lantern`이며, 실제 바닐라 모델 경로는 `minecraft:block/lantern`이다. 해당 4개에 자체 요소가 있어 108개 분모에 들어가지 않는다. 직접 블록 상태 선택은 0이다 |

부모 누락 48개는 C의 원본 결함으로 계속 기록한다. 생성형 아이템은 픽셀 레이어가 표시되는 실제 화면을 확인했다. 렌더러가 생성한 개별 메시 면 수와 모든 아이템 표시 모드의 외형은 별도다.

[C 예외 원장](C_EXCEPTION_RECHECK.csv) · [아이템 표시 로그](C_ITEM_DISPLAY_READBACK.csv) · [Another·Handcrafted 56개 화면](evidence/generated_56_items.jpg) · [Macaw 2개 화면](evidence/generated_macaw_items.jpg)

## 1-3-D 상태·방향·연결

- **Another Furniture**의 흰색 차양은 미사용 경로 하나에서 네 방향 모두 누락된 `white_double` 모델을 참조한다. 실제 Fabric 실행에서 `another_furniture:unused/white_awning`는 등록된 블록 ID가 아니었다. 자작나무·가문비나무 의자는 남향·밀어 넣지 않은 상태에서 변형 값 1, 2, 3을 확인했다. 동일 카메라 영역에서 변형 1↔3의 RGB 차이는 **0픽셀**, 1↔2는 **4,177픽셀**이다. 또한 인접 참나무 테이블의 다리 상태와 벤치·선반의 왼쪽/오른쪽 상태를 읽었다.
- **Handcrafted**에서는 참나무 침대 아이템을 한 번 사용하자 `foot,south`와 한 칸 남쪽의 `head,south`가 생성됐다. 같은 방향의 참나무 소파 두 개는 서로 `right`·`left` 상태로 이어졌다.
- **Macaw**에서는 참나무 테이블 두 개의 동쪽·서쪽 연결 속성, 위아래 옷장의 `bottom,hinge=left`·`top,hinge=left`를 확인했다. 책상과 서랍은 `facing=north`에서 Z축 인접, `facing=east`에서 X축 인접일 때 각각 `left`·`right`를 형성했다. 각 배치의 직교 방향 대조군은 두 블록이 모두 `single`이었다. 축 표기는 게임 상태 속성값 기준이다.
- **충돌**은 표본 가구 12곳과 공기·돌 대조군 6곳의 중심 위에서 아머 스탠드를 떨어뜨려 확인했다. 세 환경의 공기·돌은 각각 바닥 기준 0.000블록과 1.000블록에서 멈췄다. 가구는 모두 바닥보다 높은 위치에서 멈췄다. 예를 들어 의자는 Another **0.437**, Handcrafted **0.625**, Macaw **0.725**블록이었다. 측정은 좌표 로그에서 0.001블록 단위로 내림했다. 의자 변형 1↔3의 화면 비교와 별도로 Another 충돌 표본은 테스트 종료 시점의 변형 2다.

[기존 6개 예외 재검산](D_EXCEPTION_RECHECK.csv) · [상태 관측 원장](D_OBSERVED_STATES.csv) · [충돌 원장](D_COLLISION_PROBES.csv) · [조립 화면](evidence/assembly.jpg) · [의자 비교](evidence/chair_variants.jpg) · [원본 상태 로그 발췌](RUNTIME_LOG_EXCERPT.txt)

## 버전과 검증 범위

| 모드 | 실행 버전 | 고정 소스와의 대조 |
|---|---|---|
| Another Furniture | Minecraft 1.21.1, Fabric 4.0.2, SHA-256 `3f0e6c276dde5cd6390e9c14bc4c283e4043f25d812c1f5ecc36b7b2f61642b5` | 모델 1,629개·상태 177개 전부 JSON 내용 일치. 공식 NeoForge 4.0.3 JAR의 같은 JSON도 전부 일치. 런타임 결과는 Fabric 4.0.2에 해당 |
| Handcrafted | Minecraft 1.21.1, Fabric 4.0.3, SHA-256 `9609c27e2eeaed4c633ade2d68ad980cfbed0442a10239846a67e9c62bc1b230` | 모델 12,394개·상태 267개 전부 바이트 일치 |
| Macaw’s Furniture | Minecraft 1.21.11, Fabric 3.4.2, SHA-256 `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e` | 1-3의 고정 공식 JAR 그대로 사용 |

조립·충돌 검증은 시험한 재질·이웃·방향과 가구 중앙의 아머 스탠드에 해당한다. 모든 가구 변형의 전체 충돌 박스, 플레이어 통과·앉기, Another NeoForge 4.0.3의 실행은 미검증이다. 원본 모드/JAR 수정은 없었다.

[배포 리소스 대조](RELEASE_COMPARISON.csv) · [Another 4.0.2 Fabric](https://modrinth.com/mod/another-furniture/version/8xUs6Teu) · [Another 4.0.3 NeoForge](https://modrinth.com/mod/another-furniture/version/cugGiMKt) · [Handcrafted 4.0.3 Fabric](https://modrinth.com/mod/handcrafted/version/f0pKpUWd) · [Macaw 3.4.2 Fabric](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD)

## 재현

- [원본 예외 대조 스크립트](audit_exceptions.py)는 두 고정 Git 저장소, 실행 JAR 세 개, Another 4.0.3 비교 JAR와 바닐라 1.21.1 JAR을 받는다.
- [런타임 데이터팩 생성기](build_runtime_fixture.py)를 대상 게임 버전에 맞춰 실행하여 월드의 `datapacks/cd_audit`를 만든다. `/reload` 후 해당 지역으로 이동해 `/function cd_audit:place`와 `/function cd_audit:verify`를 실행한다. Minecraft 1.21.1 장면은 Z=40과 56, 1.21.11 장면은 Z=220이다. 침대는 4.5, 121.5, 56.5에서 아래를 보고 아이템을 사용한다. `drop` 실행 4초 뒤 `height`로 확인하고, `clear_probe`를 실행한다. 1.21.11의 Z=264 인근에서 `wide_matrix`를 실행하면 연결 방향을 대조한다.
- `items` 함수는 1.21.1의 Z=75·87과 1.21.11의 Z=240에 생성형 아이템을 전시한다. [실행 집계 스크립트](summarize_runtime.py)는 테스트 로그와 의자 동일 카메라 캡처를 읽는다.
