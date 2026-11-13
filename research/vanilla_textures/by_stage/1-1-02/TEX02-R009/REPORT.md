# TEX02-R009 — 원본 Java 클라이언트의 quad UV 처리 경로와 31개 uvlock 선언 확인

- 연구 날짜 2026-11-13, 범위 **1-1-02 석재·벽돌 고정 표본 17개**; 이전 R008 이후 R009.
- **사용자 제공 GitHub 1.21.11 추출 원본**의 난독화된 `.class`와 실제 blockstates JSON 직접 접근. Mojang 공식 전체 client.jar SHA-1 인증은 필수 기준에서 제외하며 인증 성공을 주장하지 않음.
- **이번에 신규로 직접 열람한 클래스 11개**: `hqc.class`, `hqc$b.class`, `g.class`, `ioc.class`, `i.class`, `e.class`, `ilp.class`, `hqd.class`, `hoa.class`, `hoa$a.class`, `hoa$b.class`. R008에서 이미 열람한 `hqi.class` 1개 재열람(신규로 재가산 금지). **총 12개 `.class` 경로의 Git blob SHA**를 `CLIENT_QUAD_CLASS_SHA.csv`에 기록.

## 직접 검증한 UV 처리 순서

`hqi.class` (추출 클라이언트의 FaceBakery 역할) 바이트코드 `bakeQuad` 184 byte 및 4-vertex helper 181 byte를 명령어·constant-pool 참조와 대조해 **신규 호출 증거 21행**을 `QUAD_PIPELINE_BYTECODE_CALLS.csv`에 기록했다.

1. `hqc.d()`로 face UV를 가져오고 null일 때에만 기존 R008 `defaultFaceUV(from,to,direction)`을 호출.
2. `ioc.b(direction)`로 해당 면의 UV용 `Matrix4fc` 조회(모델 상태가 공급하며, 기본 `ioc` 메서드는 공용 단위행렬을 반환). `ioc.a()`는 **별도의 위치 변환 `i`**를 반환.
3. 면의 코너 4개를 `hoa` 표로 열거하고, 각 꼭짓점에 **요소 회전(`hqd` 있을 때) → 모델 위치 변환** 적용.
4. UV는 `hqc.a/b`가 `g.b(index)`의 회전된 인덱스를 `hqc$b`의 U/V 코너 선택에 적용하고 **16으로 나누어 정규화**.
5. `e.a(uvMatrix)`의 matrix property bit 4 검사. 해당 검사에 **참이면** 정규화 UV 그대로 사용, **거짓이면** `(u,v)`에서 `0.5`를 빼고 `(u-0.5,v-0.5,0)`에 UV 행렬 `transformPosition`을 적용한 다음 `0.5`를 더함.
6. 텍스처 UV float을 `ilp.a/b`에 넣고 `hdr.a(float,float)`로 packed long 생성. quad 결과 4개 정점과 packed UV, 면의 법선/방향 등을 저장. 요소 회전이 없는 경우, 면 방향 확정 후 정점 배열과 UV 배열을 **함께 재배열**하는 분기도 존재.

**중요한 차이:** 위 'bit 4'는 실제 바이트코드가 검사하는 정수 플래그이며, 해당 메서드의 의미는 행렬 속성에 따른 UV 변환 건너뛰기다. 이 발견만으로 **모든 상태에서 `uvlock`이 활성/비활성**이라고 확정할 수 없다. `ioc` 기본 메서드가 단위행렬을 반환하는 사실과 실제 JSON 상태 로더가 어느 구현을 넘기는지는 별개의 검증 대상이다.

## 신규 UV 코너 인덱스 산출 32행

실제 사용자 추출 클래스에 있는 `g.b(I)` 계산은 `(인덱스 + 회전 오프셋) % 4`; `hqc$b.a(I)`는 i=0·1에 `u1`, 그 외 `u2`; `hqc$b.b(I)`는 i=0·3에 `v1`, 그 외 `v2`를 반환한다.

따라서 U/V 코너 선택은 정적 rectangle `[u1,v1,u2,v2]`에 대해 다음과 같다.

| 입력 i | U | V |
|---|---|---|
| 0 | u1 | v1 |
| 1 | u1 | v2 |
| 2 | u2 | v2 |
| 3 | u2 | v1 |

**신규 32가지 알고리즘 평가** = UV rectangle **2종**(`[0,0,16,16]` 기본 큐브, `[16,0,0,16]` 미러 큐브) × face rotation index **4종**(0..3) × vertex index **4개**(0..3). `UV_CORNER_FORMULA_EVALUATION.csv`에 각 `u,v`와 16분의 1 정규화 값을 저장. 이것은 **코드 공식 평가**, 17개 대상 blockstate에 실제 face UV 회전 0/1/2/3이 모두 선언되어 있다는 주장이 아니다.

## 17개 blockstate JSON 재열람과 새 확인

`stone,cobblestone,stone_bricks,deepslate_bricks,polished_andesite,bricks,tuff_bricks,granite,polished_granite,diorite,polished_diorite,andesite,deepslate,deepslate_tiles,blackstone,polished_blackstone,chiseled_stone_bricks` **17개 blockstate JSON을 다시 직접 열람했다**. **기존 31개 선언 중 `uvlock` 속성을 명시한 선언은 0개(31/31 없음)**. 각 파일의 SHA와 선언별 결과를 `BLOCKSTATE_UVLOCK_DECLARATIONS.csv`에 저장.

이는 **'원본 JSON에 uvlock 키가 없음'**이라는 직접 사실이지, 실행 시 각 상태의 실제 UV 행렬과 bit 4 조건의 결과·회전 확률이 모두 측정됐다는 결론이 아니다. `stone` 미러 + Y180 4분기 및 `deepslate` axis 세 종류 각 4분기는 과거 R004 발견을 재확인한 것이므로 신규 선언/신규 중복으로 계산하지 않는다.

## 기존 연구 범위 및 남은 필요 검증

- R008 기본 로컬 UV 6방향 `FaceBakery` 검증을 계승. R009은 그 **이후의 조건부 face UV matrix 처리**를 신뢰성 있게 추적한 신규 성과. R007 모델 world-UV 186행 및 134개 픽셀 비교는 다시 신규 실적으로 세지 않음.
- **고정 PNG 17개·RGBA 4352·블록상태 31·기존 면 186·기존 자동 UV 면 138/미러 면 48, 모두 분모 불변**.
- 새 PNG 바이너리 0개, 새 픽셀 이음새 측정 0건, 새 모델 면 0개.
- 미해결: blockstate/ModelState 로더가 실제로 `ioc`를 어떻게 구현하는지, 상태 회전으로 생기는 모든 UV 행렬과 `uvlock` 기본값, 실제 baked quad 숫자 출력, 인게임 시각/조명/이음새 관찰, 랜덤 선택 확률.
- **F 실제 게임 정적 0/17, A–G 전체 완료 0/17**. 인증 정책 불변. 전역 `v38`, 다른 단계·R008 이하 릴리스 불변. 애니메이션/Project Zomboid 변환/실제 3D 가구 제작 제외.
- 다음 진행 후보 `TEX02-R010`: GitHub STATE/HEAD 충돌 재검사 후에 사용자 추출 클라이언트의 `ioc` 구현과 blockstate loader/uvlock 데이터 처리를 추가 추적할 수 있다. 현재는 사용자 협조 없이 가능한 원본 코드 검사가 남아 있음.
