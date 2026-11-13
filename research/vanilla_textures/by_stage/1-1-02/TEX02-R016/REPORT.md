# TEX02-R016 — 17개 실제 등록 블록의 렌더 시드 override 전수 소스 검증

**검증 날짜:** 2026-11-13  
**범위:** Minecraft Java 1.21.11, 고정 17개 석재·벽돌 텍스처 및 해당 blockstate 모델의 실제 vanilla 블록 등록 클래스  
**기준:** 사용자 원본 추출 `.class` 6개 및 R013의 불변 모델 선택 선언 CSV 1개. **실제 Minecraft 클라이언트 실행 또는 GPU 렌더 관측은 아님.** 공식 Mojang JAR SHA-1 인증은 완료 조건에서 제외되었으며 인증 완료를 주장하지 않는다.

## 1. R015의 미해결 문제를 정확히 해결

이전 R015에서는 `eog$a.class`의 `b(Lis;)J` (13바이트)가 실제 소유 블록의 `dzq.a(Leoh;Lis;)J` 가상 호출로 시드 계산을 위임하므로, Minecraft 17개 블록별로 기본 `eog` 위치 해시를 **override**하는 하위 클래스가 있을 수 있다는 한계를 남겼다.

R016은 원본 1.21.11 `dzs.class` (168264 bytes, Git blob `b58e7153fb0cfbb47313c3a59dd7c8516ee3642c`)의 클래스 파일 상수 풀, **`<clinit>` 40257바이트**, 문자열 `ldc_w`, 해당 호출의 실제 `invokestatic` 바이트코드, 등록 field에 대한 `putstatic`와 **`BootstrapMethods` LambdaMetafactory 인자**를 직접 검사했다. R013의 정확한 17개 모델 ID가 원본 레지스트리에 17/17 존재하며 각각 한 번씩 등록된다는 근거를 복원했다.

## 2. 17개 블록의 실제 생성 클래스 — 16개의 일반 `dzq`, 1개의 `egl`

원본 `dzs.class`에 블록을 등록하는 공통 보조 메서드 두 종류가 있다.

**일반 블록(16개):** `dzs.a(Ljava/lang/String;Leog$d;)Ldzq;` 메서드의 본문은 11바이트

```text
2a ba 05 c4 00 00 2b b8 05 19 b0
```

즉 이름을 담고 있는 `ldc_w`와 속성 `eog$d`를 넘겨, `invokedynamic #0x05C4`로 만든 Function을 `dzs.a(String,Function,Props)` 등록 helper에 전달한다. 원본 `BootstrapMethods` 12번은 실제로 **`kind8:dzq.<init>(Leog$d;)V`**를 참조한다. `stone`, `cobblestone`, `stone_bricks`, `deepslate_bricks`, `polished_andesite`, `bricks`, `tuff_bricks`, `granite`, `polished_granite`, `diorite`, `polished_diorite`, `andesite`, `deepslate_tiles`, `blackstone`, `polished_blackstone`, `chiseled_stone_bricks`까지 **16개 모두** `invokestatic #0x0991` → `dzs.a(String,eog$d)`의 일반 경로를 따른다.

**`deepslate`(1개):** `<clinit>` **PC 38800**의 `ldc_w` 이름 바로 다음에서 `invokedynamic #0x09FF`를 호출한다. 해당 원본 `BootstrapMethods` 20번은 **`kind8:egl.<init>(Leog$d;)V`**를 참조하고, 최종 등록 helper는 `dzs.a(String,Function,eog$d)` (#0x0519). 그러므로 `deepslate`만 `egl` 생성 경로로 확인된다.

**주의:** `deepslate_bricks`(PC39078)와 `deepslate_tiles`(PC39002)는 실제로는 `dzq` 생성 경로를 사용한다. 블록 이름의 `deepslate` 접두어만 보고 클래스 종류를 추측하는 방식은 잘못된 결과를 낼 수 있다.

개별 정확한 등록 `ldc_w` PC, CP string index, `putstatic dzs.*:Ldzq;` 필드, helper PC/메서드, 생성자 구현을 **`REGISTERED_BLOCK_TYPES_17.csv`의 17행**에 기록.

## 3. 실제 클래스 계층에서 해당 seed override가 0개임을 확인

다음은 원본 사용자 제공 클래스의 직접 검증 결과다.

| 원본 클래스 | Git blob SHA | 실제 상위 클래스 | 직접 선언 메서드 | `a(Leoh;Lis;)J` 선언 |
|---|---|---|---:|---|
| `egl.class` | `61424d1fe2efc6162c61c64e74a57f01c519d8f4` | `dzq` | 7 | **없음** |
| `dzq.class` | `fab6c386693f88d28cc680ba8112bf0a2243ee16` | `eog` | 84 | **없음** |
| `eog.class` | `bee52d0356520a1872a94b0a15b0c98ea5407154` | `java/lang/Object` | 66 | **있음 (기본 구현)** |

`eog.class`의 protected `a(Leoh;Lis;)J` 메서드 코드 길이는 **정확히 5바이트: `2c b8 02 07 ad`**, 즉 `BlockPos`를 `bgj.a(Vec3i)`에 넘겨 long을 반환한다. world seed 또는 world 객체를 인수로 받아 섞는 로직이 없다.

이는 원본 **실제 등록 경로 + LambdaMetafactory 생성자 + Java 상속 관계 + 메서드 목록**을 합쳐 확인한 결과다.

- 16개 일반 블록: `dzq → eog`.
- `deepslate` 1개: `egl → dzq → eog`.
- `dzq` 84개 및 `egl` 7개 선언 메서드 중 기본 렌더 시드 메서드 시그니처를 덮어쓰는 것은 **0개**.
- 이에 따라 `eog$a.b(BlockPos)` 가상 메서드 호출은 17종 모두 **최종적으로 `eog` 위치 해시**에 도달한다.

**결론:** 추가 모드/코드 수정 없는 고정 Minecraft 1.21.11 원본 **17/17 블록의 렌더 시드 규칙은 동일한 기본 좌표 해시**다. R015에서 남겨둔 17개 구체 클래스의 override 위험은 **소스 수준에서 해소**되었다.

원본 클래스의 바이트코드만 분석했기 때문에 게임 내 모델 atlas/렌더 부하/랜덤 출력 객체를 실제로 instrument하지 않았고, 다른 오버라이드 가능한 renderer 확장 지점까지 일반화하지 않는다.

## 4. R015 결과의 의미 변화 — 31개 모델 선택 선언에 상속 증명 연결

불변 `TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv`(Git blob `18f02c6f44fd18f2a522fca81b2f73ba7409f829`)에서 31개 `block + property + variant_index` 선언을 연결했다.

- **17개 블록**이 실제 레지스트리에 있음.
- `stone` **4개**, `deepslate axis=x/y/z` **12개**를 포함한 4개의 가중치 목록(각 weight=1). 그 밖의 15개 블록은 각각 1개 source 모델 선택 선언 → **총 31개**.
- `VERIFIED_POS_SEED_MODEL_SLOTS_31.csv`는 31개 슬롯 각각에 실제 블록 클래스(16 `dzq` 블록, 1 `egl` 블록)와 inherited 기본 시드 여부를 기록한다.
- 따라서 **R015 기본 위치 해시가 적용되려면 블록별 재정의가 없어야 한다**는 조건은 고정 17블록 모두 해소했다. 그러나 R015의 **49개 가상 좌표 / 196개 가상 선택 결과 / 10쌍 해시 충돌**은 여전히 실제 게임을 렌더하고 관찰한 결과가 아니라 **코드 기반 수학적 재현**이다. World seed 입력이 이 **기본 블록 시드 경로에 존재하지 않는다**는 사실과 실제 월드 출력 측정의 부재는 동시에 유지해야 한다.
- 기존 R011의 32개 월드방향 차이, R012의 40개 UV 코너 차이, R014의 744개 정점 인터너 값 보존과 R015의 RNG 흐름도 원본 근거로 보존. 이번에 이 수치를 새 실측으로 재집계하지 않았다.

## 5. 생성 파일과 재현성

- `REGISTERED_BLOCK_TYPES_17.csv`: 17 블록에 대한 실제 source `dzs.<clinit>` PC+CP+field+lambda 생성자+상속 경로.
- `SEED_OVERRIDE_CLASS_PROOF_7.csv`: 등록 helper, `deepslate` 람다, `egl`·`dzq` no override, `eog` 시드 본문, `eog$a` 가상 호출, `bgj` 해시 연결의 7개 증명 기록.
- `VERIFIED_POS_SEED_MODEL_SLOTS_31.csv`: 31개 기존 모델 선언과 확정된 source 기본 시드 상속을 연결.
- `SOURCE_SHA_LEDGER_7.csv`: 새로 직접 점검한 `.class` **3개**(`dzs,dzq,egl`), 이전 근거로 재사용 및 재열람한 클래스 **3개**(`eog,eog$a,bgj`), R013 기존 CSV **1개**의 원본 SHA.
- `VERIFY_R016_BLOCK_SEED_INHERITANCE.py`: Python 3 표준 라이브러리만 사용하는 로컬 재현 검사기. classfile 상수풀·BootstrapMethods·클래스 SHA·각 메서드 서명·17 문자열 PC+호출·31 모델 슬롯 검증. **GitHub connector 기반 JS 검증 작업은 실제 실행했고, 제공한 Python 파일은 원본 전체 클래스를 장착한 환경에서 종단 간 실행하지 않았다.** 사용자가 실험한 Java 런타임 로그는 없다.

## 6. 상태/완료 조건과 다음 단계

**현재 stage 1-1-02 source 검사 범위:** 원본 PNG 무결성/RGBA 17/17, 원본 model JSON/블록상태 17/17, 소스 기반 186 model faces, 744 normalized vertices, 블록 등록/시드 클래스 17/17. 연구 개정은 R001–R016.

**완료했다고 주장할 수 없는 범위:** 인게임 정적 렌더·최종 UV/조명/atlas/실제 옆 블록 seam 검증 **0/17**; A–G 전체 완료 0/17. 공식 Mojang JAR SHA-1 인증은 **필수 조건에서 제외**; 실행 인증은 하지 않았다. 애니메이션 연구 별도 보류.

**R017 가능한 신규 원본 연구:** `atlas`의 텍스처 sprite 연결·모델 atlas acceptance 조건을 원본 1.21.11 `.class`에서 추적하고 17 모델에 적용할 수 있는 추가 증거가 있으면 검증. 더 이상 새로운 독립 소스 증거가 없고 실제 게임 캡처가 필요해지면 새 revision 대신 사용자에게 필요한 화면을 구체적으로 요청해야 한다.

**독립 stage 경계:** 기존 `TEX02-R001`~`R015` 파일, 다른 작업 단계, 전역 `v38`을 수정하지 않았다.
