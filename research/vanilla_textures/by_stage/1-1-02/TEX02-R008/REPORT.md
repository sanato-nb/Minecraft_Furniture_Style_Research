# TEX02-R008 — 사용자 제공 Java 1.21.11 렌더러 바이트코드의 기본 UV 규칙 직접 검증

**연구 범위:** `1-1-02` 석재·벽돌 고정 표본 17개, 기존 `TEX02-R007` 다음. **인게임 렌더 0/17**, 애니메이션 보류. 공식 Mojang JAR SHA-1/manifest 인증은 사용자의 범위 제외 지시를 준수하며 인증 성공으로 표시하지 않는다.

## 이번 턴 실제로 새로 검사한 원본

사용자 GitHub 업로드 `1.21.11/`의 **Java `.class` 바이너리 3개**를 새로운 증거 유형으로 직접 열람했다. GitHub blob SHA는 `CLIENT_CLASS_LEDGER.csv`에 보존한다.

- `hqi.class` (7,068B, blob `5b64584e8cc09a8db90f802e0021bc0533e81ab1`) — Mojang 네임스페이스에서는 `FaceBakery`, 이 파일의 `defaultFaceUV(from,to,Direction)` 메서드 302B와 `bakeQuad` 184B를 직접 파싱.
- `hqi$1.class` (657B, blob `237bb887fe196bc3d707a0f75ca5664c9baf8553`) — synthetic switch 표에서 `iz.a/b/c/d/e/f → switch 1/2/3/4/5/6` 대응.
- `iz.class` (16,348B, blob `e820016d321253132b9f33de2da4b1b07f358e91`) — enum `<clinit>`에 정의된 `DOWN→a, UP→b, NORTH→c, SOUTH→d, WEST→e, EAST→f` 직접 확인.
- 위 클래스의 난독화명/메서드명 해석은 독립적인 외부 매핑 문서로도 보조 교차 확인했으나, **UV 값 자체는 GitHub 사용자 제공 `.class` 바이트코드에서 추출**했다.

**재현 가능 결과:** `defaultFaceUV` 메서드의 `tableswitch` 6개 사례를 직접 실행 경로별로 스택 해석하여 각각 `BlockElementFace.UVs(u1,v1,u2,v2)` 생성자에 전달되는 4개 식을 추출. `bakeQuad`는 `face.uv`가 null인 경우 이 기본 UV 함수 호출을 수행함을 메서드 앞부분에서 확인.

## 6개 방향별 UV 공식 — 기존 추정에서 실제 클래스 소스 증거로 승격

| 방향 | 반환 `[u1,v1,u2,v2]` | 16×16 완전 큐브 |
|---|---|---|
| down | `[from.x, 16-to.z, to.x, 16-from.z]` | [0,0,16,16] |
| up | `[from.x, from.z, to.x, to.z]` | [0,0,16,16] |
| north | `[16-to.x,16-to.y,16-from.x,16-from.y]` | [0,0,16,16] |
| south | `[from.x,16-to.y,to.x,16-from.y]` | [0,0,16,16] |
| west | `[from.z,16-to.y,to.z,16-from.y]` | [0,0,16,16] |
| east | `[16-to.z,16-to.y,16-from.z,16-from.y]` | [0,0,16,16] |

- R007에서 가정했던 **기본 U/V 축 6/6 방향이 실제 `FaceBakery.defaultFaceUV`의 원본 코드와 일치**한다. 완전 큐브 `from=[0,0,0]`, `to=[16,16,16]`일 때 반환 사각 UV는 모든 방향 [0,0,16,16].
- R004/R007의 **186면은 이전 연결 실적 계승**, 이중 `138면`은 UV 생략으로 기본 UV 생성 대상이라는 과거 분류를 이번 원본 메서드로 보강한다. 남은 `48면`은 부모 `cube_mirrored`의 `uv=[16,0,0,16]`가 명시되어 `defaultFaceUV`의 직접 대상이 **아니다**. 이번 138·48은 기존 R004의 건수를 재사용하며 신규 면 증가가 아니다.
- 새 fixed PNG 0개, 새 RGB/픽셀 이음새 측정 0건, 새 모델 상태 항목 0건. **이번에 새로 입증한 것은 3개의 클라이언트 클래스 원본과 6개의 기본 UV 방향 공식 및 기본 UV 호출 조건**이다.

## 반드시 남기는 한계

원본 `defaultFaceUV`와의 일치는 **자동 생성 UV 기초 식의 검증**에 한정된다. R007의 X/Y 모델 회전 순서, `ModelState` 변환 행렬, 실제 baked quad 꼭짓점 배열/회전 부호, `uvlock`, 최종 GPU 상 텍스처/광원, 랜덤 variant 선택, 실제 이웃한 블록의 이미지 이음새는 **여전히 소스 추론 또는 미확정**. 특히 186면 월드 프레임과 R007 134개 가상 픽셀 접합을 `ingame verified`로 승격시키지 않는다.

원본 `bakeQuad`는 UV 없는 면에서 기본 UV 함수를 호출함을 확인했으나, 나중의 회전/UV 변환 메서드 전체와 동일하게 검증한 것은 아니다. 다음에는 **실제 클라이언트 모델 변환/UV 잠금 및 정적 baked quad** 코드 경로 검사를 수행할 수 있고, 실제 게임 시각 관찰이 필요한 단계에서는 사용자에게 스크린샷/실측 협조를 요청해야 한다.

- **인게임 정적 검증:** 0/17, 보류
- **A–G 전체 최종 완료:** 0/17 (기존 상태 유지)
- **Mojang 공식 전체 JAR 인증:** 완료 기준에서 제외, 인증 성공 아님
- **글로벌 `v38` / 다른 단계:** 변경 금지 및 불변
