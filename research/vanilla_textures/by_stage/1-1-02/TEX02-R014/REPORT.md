# TEX02-R014 — inw.c() 실제 기본 베이크 컨텍스트의 Vector3 정점 인터닝 확인·744개 정점 재대조

**작성일:** 2026-11-13  
**고정 대상:** Minecraft Java 1.21.11 사용자 추출물의 석재·벽돌 17개 고정 표본, 단계 `1-1-02`  
**근거 유형:** GitHub `1.21.11/`의 원본 `.class` 바이트코드 직접 열람 + 이전 불변 R011/R012/R013 소스 파생 CSV에 대한 정적 수학 검증. **게임 클라이언트 자체 실행, 런타임 baked-quad 수집, 실제 블록 렌더·이음새 검증 없음.** 전체 공식 Mojang JAR SHA-1 인증은 사용자 요구에 따라 완료 기준 제외이며, 인증 완료 주장 없음.

## 1. R013의 핵심 미해결 질문

R013은 `hqn.class`의 `inw.c():Linw$a;` 호출이 `hqi` `FaceBakery`에 정점 변환기를 공급한다는 사실은 확인했지만, **그 콜백이 정점의 실제 x/y/z 성분을 변경하는지**와 그 **실제 기본 베이크 컨텍스트 생성부**를 파악하지 못했다. 그래서 R012의 UV·월드면 수학이 모델 회전 이후 추가 변형을 간과했을 가능성을 미해결로 남겼다.

이번 R014에서는 사용자 원본에서 **핵심 관련 클래스 6개를 새로 직접 확인**했다. `inx.class`, `inx$d.class`, `inx$c.class`, `inx$b.class`, `inx$b$1.class`, `inx$a.class`. 이 중 `inx$a`는 베이크 결과 record의 관계만 확인하였고, 정점 콜백의 행위를 입증하는 핵심은 나머지 5개다. `inw`, `inw$a`, `hqn`, `hqi`, `inm`의 이전 조사 결과를 다시 연결했다. SHA·신규·재사용 정보는 `SOURCE_SHA_LEDGER_15.csv`에, 16개 주요 method/bytecode PC 사실은 `MODEL_VERTEX_TRANSFORM_CALLCHAIN_16.csv`에 보존한다.

## 2. 구체 구현체: 기본 모델 베이크 컨텍스트의 `inx$d`

원본 `inx.class` (Git blob `176e5b8176abac37c563bbdc40c7a113a57e9b3f`)의 `a(Liog;Ljava/util/concurrent/Executor;)Ljava/util/concurrent/CompletableFuture;` **121바이트 메서드**에서 정점 변환기를 생성·재사용하는 세 연결을 확인했다.

1. **PC 0–7:** `new inx$d()` 하나를 생성하고 지역 변수 3에 저장.
2. **PC 8–17:** 동일 객체를 `inx$b.a(iof, iog, inw$a)`에 넘김. 이는 누락 모델용 대체 베이크 준비 경로.
3. **PC 19–31:** 동일 객체를 `new inx$c(inx, iog, inw$a, inx$b)`에 넘김. **일반 등록 모델을 처리하는 베이크 컨텍스트 생성** 경로. 뒤이어 PC 33–69에서 모델 자료 map을 사용한 bake task/CompletableFuture 호출이 이어진다.

`inx$c.class` (Git blob `12e3d8e6f914e9d4c2a81d2b5dd04d11af302543`)는 **`inw`를 구현**하며,

- 생성자 **PC 35–39**: 전달받은 `inw$a`를 `inx$c.c` 필드에 보관.
- `c()Linw$a` **5바이트**: `aload_0; getfield inx$c.c; areturn`, 즉 별도 조합/변환을 넣지 않고 **원본 변환기 객체를 그대로 반환**한다.

대체 모델 컨텍스트 `inx$b$1.class` 또한 `inw`를 구현하고 같은 `inw$a` 필드를 저장하며, `c()`에서 단순 반환한다. 따라서 정상 모델 베이크 컨텍스트와 대체 모델 베이크 컨텍스트가 **동일한 구체 클래스의 정점 변환 로직**을 사용함을 원본 코드에서 확인.

## 3. `inx$d`는 좌표 수치 변환기가 아니라 strong interner

`inx$d.class` (Git blob `9f94b3f0d327db052de34f4351cdc94fd7a55622`, 863 bytes)는 **`inw$a`를 직접 구현**한다.

- `<init>()V` **12바이트**: `com/google/common/collect/Interners.newStrongInterner()`를 호출해 `Interner` 필드에 저장.
- `a(Lorg/joml/Vector3fc;)Lorg/joml/Vector3fc;` **14바이트 정확한 메서드 본문**:

  `2a b4 00 1b 2b b9 00 24 02 00 c0 00 26 b0`

  위 바이트코드는 `getfield Interner` → **전달받은 Vector3fc를 `Interner.intern(Object)`에 인자로 전달** → `checkcast Vector3fc` → `areturn`이다. **추가 Matrix, translate, rotate, scale, x/y/z 연산이 전혀 없다.**
- Guava 인터닝의 **동등 값 객체의 정규화(canonicalization)** 성질을 전제하면 출력 **좌표값은 보존**되고, 바뀔 수 있는 것은 사용되는 객체 인스턴스(동일한 값에 대한 참조 재사용)다. 이는 해당 메서드의 바이트코드에 숫자 변환이 없다는 직접 관찰과 인터닝 계약의 해석을 결합한 **source-derived conclusion**이다. 라이브 게임 메모리에서 실제 객체 동일성이나 정점 버퍼를 측정한 것은 아니다.

R013에서 직접 연 `hqn.class` **PC 302–337**은 `inw.c()`를 호출하여 `hqi.a(..., inw$a, ...)`로 전달한다. R008/R012의 `hqi` `FaceBakery`에는 이 콜백을 월드 방향 정점 조립 후 적용하는 경로가 있다. 따라서 현재 확인한 **일반 `inx` 베이크 경로**에서는 **기본 정점 콜백이 수치 좌표값을 수정하지 않는다**는 결론까지 소스 증거가 닫힌다. 다른 외부 리소스 팩/확장 제공자가 다른 `inw` 구현을 만들거나 게임 실행시 추가 GPU 변환이 생기지 않는다는 일반 보증으로 확장하지 않는다.

## 4. R012의 186개 면·744개 코너를 정적 행렬/정점표로 대조

이전의 불변 CSV 4개를 Git blob SHA별로 확인한 뒤 항목 키를 연결했다.

- `TEX02-R011/ROTATION_GROUP_MATRICES_5.csv`: 5개 실제 XYZ source-derived 회전 행렬.
- `TEX02-R012/HOA_FACE_CORNERS_24.csv`: 6 face × 4 normalized full-cube 원본 정점 selector.
- `TEX02-R012/REBAKED_UV_AUDIT_186.csv`: R012가 정정한 world face 및 UV·정점 permutation.
- `TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv`: 17 블록 / 19 선택 그룹 / 31 modelstate 변형 슬롯.

**정확히 186개의 face × 4 = 744개의 source-derived normalized full-cube 정점**을 꺼내 R011 회전 행렬로 변환하고, 그 좌표가 R012에서 기록한 **월드 방향별 `hoa` canonical vertex 슬롯과 4/4 대응**하는지 검사했다.

| 점검 | 결과 |
|---|---:|
| 기존 variant 키 일치 | 31/31 |
| 세계 방향의 canonical corner와 순열 대응 | **186/186면** |
| 재대조한 원본 정점 | **744개** |
| `inx$d` 호출로 좌표 숫자가 변경되는 경우 | **0/744개** |
| R007 대비 기존 월드 방향 불일치 | **32개 유지** |
| R007 대비 기존 UV 코너 불일치 | **40개 유지** |
| R012를 이번 코드 근거 때문에 다시 수정해야 할 projection | **0개** |

**주요 결과:** R013에서 미확인으로 남겼던 “기본 정점 콜백 때문에 R012의 186면/UV40이 달라질 수 있는가?”는 **정상 `inx` 모델 베이크 코드 경로의 좌표값 측면에서는 아니오**라고 판단할 수 있다. 원본 회전행렬·정점순서·UV값을 다시 계산했으며 실제 게임 밖에서 수행한 **수학 재검증**이므로 이전 R012의 186개와 40개 결과를 **새 인게임 실적으로 중복 계산하지 않는다**.

- `INX_D_VERTEX_VALUES_744.csv`: 소스 모델·로컬면·월드면·각 정점 인덱스, `inx$d` 인터닝 전후 **동일 좌표값**, 게임 실행 여부를 모두 기록.
- `R012_GEOMETRY_CONTEXT_RECHECK_186.csv`: 원래 R012의 UV/월드면 차이 플래그를 유지하면서 전체 면에 대해 context 정점순열 검증 여부를 부착.
- `VERIFY_R014_INX_TRANSFORMER.py`: 사용자 추출 원본 11개 `.class` 및 4개 기존 CSV의 SHA를 확인하고 **186/744·40/32 수치를 재생성**하는 표준 Python 스크립트. 이번 도구 세션에서 JS+GitHub로 원본을 판독해 744행과 186행의 정합성을 직접 검사했지만, 별도 사용자 원본 전체 폴더를 갖춘 Python 환경에서 **해당 Python 파일을 종단 간 직접 실행한 것은 아니다**. 해당 한계를 유지한다.

## 5. 단계 상태와 다음 후보

- 이번 새로 직접 열람한 연구 관련 클래스 6개, source callsite evidence 16개. 원본 17 PNG / 누적 RGBA 4,352 pixels / 선언 31개 / 모델 면 186 / R007 synthetic seam 134 / R011 방향 32개 / R012 UV 코너 40개 / R012 가상 seam 재계산 64개 / R013 선택 확률 19그룹·29고유 구조 모두 **계승 실적**이며 R014 신규 고유 PNG·실측·게임 런타임 기록은 **0개**.
- **정적 인게임 F 0/17, A–G 전체 완료 0/17**. 원본 클래스의 별도 RNG seed/월드 좌표 의존 방식, atlas 허용 여부, 실제 GPU UV filtering/lighting/실제 블록 인접 seams는 아직 미검증.
- 공식 Mojang JAR 전체 SHA-1 인증 불필요(사용자 요청), 인증 완료 주장 없음. 다른 단계 및 전역 `v38`, 불변 R001–R013 수정 금지.
- 다음 `TEX02-R015` 후보: **R013 weighted variant `bgr`가 월드 block 위치 및 RNG seed를 실제로 어떻게 받는지 원본 client dispatcher에서 추적**, 특히 동일한 block state가 같은 위치에서 어느 패턴으로 유지되는지 검토. 또는 17 텍스처 중 **실제 인게임 렌더 캡처**가 필요해지는 시점이 오면 중단하고 사용자에게 정확히 필요한 화면/파일을 요청. 더 이상의 유의미한 원본 검증이 없어지면 억지 revision을 생성하지 않는다.
