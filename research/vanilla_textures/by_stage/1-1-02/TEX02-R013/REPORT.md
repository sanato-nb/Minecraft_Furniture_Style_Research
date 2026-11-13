# TEX02-R013 — Minecraft 1.21.11 모델 선택 가중치와 Quad Bake 정점 콜백 호출 경로

- 연구 일자: 2026-11-13
- 고정 단계: `1-1-02` — 기본 석재·벽돌 **17개 원본 PNG**; 전역 `v38`, 다른 단계, 과거 R001–R012 원본 자료 변경 금지
- 입력: **사용자 업로드 GitHub의 `1.21.11/` 원본 .class 및 blockstate JSON 17개**. 공식 Mojang JAR 전체 SHA-1 인증은 이 단계의 필요 완료 기준에서 제외되어 있으며, 인증 완료 주장을 하지 않음
- 분류: **원본 클래스 바이너리 직접 조사 + 코드 경로 재현 + JSON 기반 이론적 선택률 산출**. 실제 게임 실행/렌더러 추적/월드 RNG 관측 0건. 인게임 정적 검증 0/17

## 1. 새 원본 클래스 직접 열람 및 근거

기존 R008–R012보다 모델 **변형 선택/가중치/베이크 컨텍스트** 영역으로 소스 조사 범위를 넓혔다. 핵심 원본 바이너리 클래스 **18개를 새로 직접 열람**하고, 기존 `hqq`, `hqi`, `hqc`, `ioc` 4개를 참조했다. 모든 파일의 SHA·선행/신규 구분은 `CLASS_SOURCE_SHA_LEDGER.csv`(총 22개 클래스)에 보존했고, 검증된 코드 분기/호출은 `BYTECODE_DISPATCH_CHAIN_19.csv`(19개 경로)에 따로 기록했다.

### A. blockstates의 JSON 단일 variant와 variant 목록

- `hqf.class`는 blockstate JSON의 `variants`·`multipart`를 별도로 읽는 로더 계열이다. `hqf$b.class`는 해당 `variants` 값을 `hqh$b` 타입의 codec으로 파싱하는 경로를 갖는다.
- `hqh$b.class`는 variant **단일 객체**(`hqo$a`)와 **목록**(`ioj$a`)을 구분하며, `RecordCodecBuilder`의 `weight` 기본값은 `1`: 직접 확인한 opcode 구간 `b2 00 fc 12 fe 04 b8 01 04`에서는 weight Codec, `weight` 문자열, `iconst_1` 기본값이 연결됨.
- `hqo$a.class`의 `a(inw)`는 한 모델을 베이크하고 `hqo` 단일 모델 래퍼를 생성하며, `ioj$a.class`는 `cbn` 가중치 리스트의 각 항목을 `inw` 컨텍스트에서 베이크한 뒤 `ioj`를 생성한다.
- `ioj.class`의 `a(bgr, List)` 19바이트: `cbn.b(bgr)`로 **선택한 모델 하나**에 `hqh.a(bgr,List)`를 위임한다.

### B. 가중치 리스트의 실제 정수 슬롯 선택

- `cbm.class`는 각 선택지의 value/정수 weight를 보유하며 음의 가중치를 거절한다.
- `cbn.class`의 생성자(87바이트)는 `cbo.a(List,ToIntFunction)`로 총 가중치를 계산한다. 합계가 0이면 선택기가 없고, **양의 합계가 64 미만이면 `cbn$c`, 64 이상이면 `cbn$b`** 선택기 구현을 사용한다.
- `cbn$c.class` 생성자(77바이트)는 `Object[total_weight]` 배열을 만들고, 각 가중치 항목의 값을 `Arrays.fill(array,start,start+weight,value)`로 해당 무게만큼 반복 저장한다.
- `cbn.b(bgr)` 39바이트: 난수 소스 `bgr.a(total_weight)`로 **0..total_weight−1 중 정수 인덱스 하나**를 얻어 `cbn$d.a(index)`로 값 하나를 고른다. 17표본의 모든 목록이 4×weight1, 총 weight4이므로 **모두 `cbn$c` 최적화 경로**에 해당한다.
- 이것으로 **유효한 variant가 등록되고 bounded RNG가 균등 분포를 제공한다는 조건 아래**, 동일 weight1 슬롯 4개는 각각 1/4, 같은 구조의 중복 두 개의 합은 2/4라는 **조건부 이론적 비율**을 계산할 수 있다. 난수의 실제 시드나 월드 좌표별 호출 독립성, 재렌더/환경 변화 시퀀스 또는 현실 관측 빈도를 검증한 것은 아니다.

## 2. 고정 17 blockstate JSON을 이번에 직접 다시 확인

17개 `1.21.11/assets/minecraft/blockstates/{block}.json`을 이번에도 원문 파싱했다. 결과 원문 31개 선언 각각의 블록/속성/variant 인덱스/모델/XYZ 회전/UVLock/weight 원문 존재여부/기본값 및 source Git blob을 기록했다.

| 표본 범주 | JSON 선택 그룹 | 선언 슬롯 | 중복 제거한 모델+회전+UVLock |
|---|---:|---:|---:|
| stone | 1 (4-entry array) | 4 | 4 |
| deepslate (axis=x/y/z) | 3 (4-entry array each) | 12 | 10 |
| 다른 15개 고정 블록 | 15 (single object each) | 15 | 15 |
| **전체** | **19** | **31** | **29** |

**원본 JSON의 `weight` 명시: 0/31**. `hqh$b` 소스에서 확인된 기본값 1을 대입했을 때 모든 variant 슬롯 가중치 = 1, 4개 목록의 총합 = 4, 단일 객체의 값은 구조상 유일한 선택 결과다.

- `BLOCKSTATE_CHOICE_SLOTS_31.csv`: 원본 선언 31개 전부와 명시/기본 가중치 및 각 조건부 확률.
- `SELECTOR_GROUPS_19.csv`: stone 1 + deepslate axis=x/y/z 3 + 나머지 15 = **19개 선택 그룹**, 그중 list 4개/단일 15개.
- `STRUCTURAL_OUTCOME_ODDS_29.csv`: 동일 `(model,x,y,z,uvlock)`별 선택 확률을 합산해 **구조가 다른 결과 29개**. 이는 29개 새 텍스처나 독립 모델 파일을 발굴했다는 뜻이 아니다.
- **deepslate axis=x 특이 사항:** `variant 0`과 `variant 2`는 `minecraft:block/deepslate, x90,y90,z0`로 동일; `variant 1`과 `variant 3`은 `minecraft:block/deepslate_mirrored, x90,y90,z0`로 동일. 원문 슬롯 4개를 각각 1/4로 뽑으면 **정규·미러 구조는 각각 합산 2/4=50%**다. 같은 구조 = 이미지를 1:1 실제 게임에서 본 것은 아니며, 단순히 JSON/행렬 모델 속성 기준의 구조 동일성이다.
- stone 네 옵션은 소스 구조적으로 4개가 다르며 각 1/4; deepslate axis=y/z도 각각 4개 구조가 달라 각 1/4. 나머지 15블록은 각 하나의 JSON 모델 선택(100%).

## 3. 모델 bake와 실제 정점 변환기는 어디에서 연결되는가?

이번에 새로 직접 연 `hqn.class`의 395바이트 source 메서드에서 다음 **per-element/per-face 호출 위치**를 확인했다.

- PC 48–60: `hqb`의 `from`·`to` 정점을 읽고 X/Y/Z 축별 두 끝점이 다른지 검사. 3축 모두 퇴화(degenerate)면 요소 bake를 생략.
- PC 149–210: 요소의 face map을 순회, 면 방향 및 face 속성 취득.
- **PC 281–300**: `inw.b()`에서 얻은 sprite resolver(`iog`)를 사용해 `hqc.c()` texture 레퍼런스를 sprite로 해석.
- **PC 302–337**: `inw.c():Linw$a;`로 **정점 변환 함수를 얻어** `hqi.a(FaceBakery, ...)`에 전달한다. R009/R012에서 열람한 `hqi`의 vertex 처리 PC 146–159가 이 `inw$a.a(Vector3fc)`를 호출하여 변환된 좌표를 vertex output에 저장한다.
- **PC 339–382**: face의 `cullface`가 없으면 unculled list, 있으면 `ioc.a()` 위치행렬로 면 방향을 변환한 culled list에 quad 저장.
- `inw$a.class`의 `a(Vector3fc)`는 **추상 인터페이스 메서드**이고 `a(float,float,float)` 기본 메서드는 `new Vector3f`를 통해 동일 메서드로 위임한다. **어떤 구체 객체가 runtime에서 `inw.c()`를 반환하는지는 아직 확인되지 않았으므로, 모든 경우 항등 정점 변환이라고 단정할 수 없다.**
- `hqm.class`의 178바이트 모델 bake 경로는 `inw.a(model)` → `iof` geometry → sprite/quad 검수 → `hqm` 생성. 모델에서 허용된 atlas 바깥 sprite가 발견되면 경고 후 fallback `inw.a()`를 사용한다. 사용자 제공 17소스 PNG가 실제 런타임 atlas에 모두 성공적으로 들어왔는지는 이번 bytecode만으로 보증하지 않는다.

**R012의 186-face UV 투영은 변환기 경로를 완전히 실측한 결과가 아니다.** 이번 R013에서 그 이유(추상 콜백의 실제 구현체 확인 누락)를 더 구체적으로 기록했다. 원본 JSON의 full cube 6면씩이라는 R004/R012의 구조적 가정에서 `hqn`이 그러한 quad를 bake할 위치가 확인되었으나, 실제 렌더러에서 186개 quad 객체를 생성/관찰했다고 주장하지 않는다.

## 4. 신규 실적과 남은 문제

**신규 작업:** 기존 고정 blockstate JSON 17개 원문 재열람 및 가중치 연결 분석, 원본 관련 신규 `.class` 18개 직접 열람, bytecode-dispatch/조건 19행, JSON 가중치 슬롯 31행, 그룹별 합계 19행, 중복 구조 조건부 확률 29행. **새 고유 PNG/새 픽셀 측정/새 실제 인게임 데이터 모두 0**. 앞선 17 PNG, 4,352 RGBA 픽셀, 31 변형, 186면, 134 기존 합성 seam, R011 교정 32방향, R012 교정 40 UV 코너 및 재측정 64 seam은 모두 계승하며 새 작업으로 재가산하지 않는다.

`VERIFY_R013_SELECTION.py`는 표준 Python만으로 **Git blob SHA가 고정된 18개 핵심 클래스**와 17개 blockstate JSON 원문을 검사하여 31/19/29 수량 및 각 가중치를 재생성하도록 작성했다. **사용자 추출 전체 원본 폴더로 스크립트 종단 간 실행 검증은 이번 도구 환경에서 하지 않았다**(직접 소스를 통한 JavaScript 집계와 GitHub CSV 검증은 수행함).

**완료하지 않은 검증:** 실제 `inw.c()` 구현체/주어진 모델에 적용되는 정점 변환, atlas 검증 통과 여부, 실제 월드 seed 및 RNG 선택 빈도, 렌더러 GPU·조명·필터링·인접 블록 이음새, 17종 인게임 정적 캡처. 인게임 F **0/17**, A–G 전부 완료 **0/17** 유지.

다음 후보 **TEX02-R014**: 라이브 GitHub `STATE`/HEAD 재확인 후 `inw.c()`의 실제 구현과 모델 베이킹 context 공급자를 찾고, R012의 186면 정점 변환에 추가 변형이 있었는지 검증. 혹은 `cbn`의 월드 RNG 호출/seed 전달 경로를 추가 추적. 원본 정보만으로 더 이상 실질적으로 전진할 수 없고 게임 화면만 필요한 시점에는 연구 버전만 생성하지 말고 사용자에게 구체적 캡처/데이터를 요청할 것.
