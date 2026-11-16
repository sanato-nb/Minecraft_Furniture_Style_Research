# 1-2-D — blockstate 방향·상태별 모델 조립 전체 실행 계획

**작성 2026-11-16 KST · Minecraft Java Edition 1.21.11 · 계획 준비 기준 main `cea2877f725247235cfc6ba893e07483e9ab30cb`.**

> **우선순위:** [`1-2-D_FIXED_SCOPE_AND_EXIT_CONTRACT.md`](1-2-D_FIXED_SCOPE_AND_EXIT_CONTRACT.md)와 [`1-2-D_ACCEPTANCE_CONTRACT.json`](1-2-D_ACCEPTANCE_CONTRACT.json)의 범위·분모·종료 계약은 이미 고정되어 있다. 이 문서는 구체 실행 절차를 보강할 뿐 **계약 재설정이 아니다**. 계획 작성은 원본 1,168개 심층 분석이나 Entry2 조사가 아니다.

## 1. 목표와 고정 입력

- 목표: 블록 하나가 어떤 **원본 blockstate 조건**에서 어떤 **원본 모델(및 multipart 부품·선택 대안)**을 적용하고, 그 모델의 `x`/`y`/`uvlock` 메타데이터가 무엇인지 출처 단위로 재구성한다. B/C가 확인한 3D 기하·UV·PNG의 출처/SHA를 연결하여 나중에 가구 방향·부분조립 규칙으로 활용한다.
- 원본 버전: **사용자가 추출해 제공한 Minecraft Java 1.21.11 자산**. 공식 배포 JAR의 신뢰성, 게임 내 렌더링·상태 등록 확인은 이 계획에 포함하지 않는다.
- 원본 경로 모집단: `research/vanilla_models/v34/02_inventory_1168_blockstate_paths_git_shas.csv` (blob SHA `48f385ea06f5e100331cc41bbc24da082adbfb2e`). blockstates Git tree SHA `7a36f7d757e62aa61ee61aebcd8d5689bc462a8d` (선행 신원검사).
- 작업 배정의 단일 진실원: `research/vanilla_models/phase_1-2-D/D_FIXED_SCOPE_1168.csv` (blob SHA `a9e25893465810bf1386dddf4cf7a4f755b28fa1`, **1,168 데이터 행**). 해당 CSV는 배정 당시 스냅샷이므로 ENTRY1의 옛 `ASSIGNED_NOT_SOURCE_CHECKED` 표기를 완료 여부로 읽지 않는다. 이후 실적은 각 Entry 감사로 판정한다.
- 이번 준비 과정에서 목록 1,168/1,168 경로·Git SHA·배정 유일성을 원본 v34 목록과 다시 대조했으며 일치했다. **원본 JSON 내용의 전수 재독해가 아니며** 실제 D 조사 누적은 ENTRY1의 **12개(1.03%)**, 미조사 **1,156개**이다.

## 2. 유한 6 Entry 할당과 실행 순서

| Entry | 이번 배정 | 배정 누계 | 원본 파일명 범위(경계 예시) | 실제 실적 |
|---:|---:|---:|---|---|
| 1 | 12 | 12 | `brewing_stand.json` ~ `stonecutter.json` | 조사 완료 |
| 2 | 96 | 108 | `acacia_button.json` ~ `black_wall_banner.json` | 미조사 배정 |
| 3 | 265 | 373 | `black_wool.json` ~ `dripstone_block.json` | 미조사 배정 |
| 4 | 265 | 638 | `dropper.json` ~ `oak_button.json` | 미조사 배정 |
| 5 | 265 | 903 | `oak_fence.json` ~ `short_dry_grass.json` | 미조사 배정 |
| 6 | 265 | 1168 | `short_grass.json` ~ `zombie_wall_head.json` | 미조사 배정 |

- ENTRY1 **이미 완료**: `brewing_stand`, `lantern`, `oak_shelf`, `oak_door`, `oak_fence_gate`, `campfire`, `chiseled_bookshelf`, `cauldron`, `heavy_core`, `furnace`, `piston`, `stonecutter`. 원본 12 JSON·167 선택 규칙/옵션·380 문법상 상태·1,972 모델 옵션 적용·49개 B/C 모델 연결·독립 380/380 일치. 과거 성과를 새로 세지 않는다.
- ENTRY2 **다음 차례**: 범위표의 `ENTRY2` **정확히 96경로**, `acacia_button.json`부터 `black_wall_banner.json`까지. [`entry2/D_ENTRY2_QUEUE_96.csv`](../../research/vanilla_models/phase_1-2-D/entry2/D_ENTRY2_QUEUE_96.csv)는 원본 경로/SHA만 준비했으며 실제 JSON 조사는 아직 0/96이다.
- ENTRY3~ENTRY5: 각 **265경로**를 순서대로 실행. 기존 완료 경로 재조사로 실적 중복 금지. 차단·예외 및 뒤늦은 선행 자료 발견은 정확한 행 ID를 기록한다.
- ENTRY6: 마지막 **265경로** 직접 조사 후 전체 1,168 경로에 대한 D1~D5 독립 종합감사. 최종 **PASS 5개 전부**면 `D_COMPLETE_SOURCE_BLOCKSTATE_ASSEMBLY_SCOPE`, 아니면 `D_BLOCKED_AT_ENTRY6`로 고정 종료. **ENTRY7 자동 생성 금지.**
- 대상 배정은 고정 상태로 유지하고, 회차별 소규모 처리 배치는 편의상 나눌 수 있지만 추가 Entry로 표시하지 않는다.

## 3. 원본 JSON별 작업 절차 (D2)

1. GitHub 현재 HEAD와 이전 Entry 감사/인수인계를 확인한다. 범위표에서 현재 회차 경로 집합을 추출하고 완료 집합과 교집합이 없음을 검산한다.
2. 각 **원본 블록상태 JSON 본문을 직접 읽어** blob SHA를 배정표와 비교한다. 경로만 조회하거나 이전 CSV에 이름이 존재하는 것은 내용 조사로 인정하지 않는다. 읽기 차단·SHA 변화·파싱 실패는 `BLOCKED_SOURCE`로 남긴다.
3. 최상위 `variants`와 `multipart`의 구조, 빈 `variants` 키, `multipart` 조건 누락(항상 적용), 규칙 순서, 속성 이름·값, `|` 복수값, `OR`/`AND`의 중첩을 **원본 순서와 JSON 원문을 보존**해 정규화한다. 실제 원본에 없는 조건이나 속성은 추정 생성하지 않는다.
4. `apply`가 단일 모델인지 배열인지, 배열 각 요소가 대안인지와 `weight`의 키 존재·숫자 값을 구분한다. **여러 multipart 규칙의 동시 조립**과 **한 규칙 내부의 가중 대안 중 하나 선택**을 구분한다. 무작위 선택 결과를 실제 런타임 결과인 것처럼 확정하지 않는다.
5. 모델 namespace·파일 경로, `x`·`y`·`uvlock`·`weight` 각각의 **키 명시 유무**와 원본 값(명시 0/false vs 생략)을 기록한다. 회전 좌표·UV 재투영의 엔진 결과는 생성하지 않는다.
6. 원본 미해결/오류를 숨기지 말고 `D_UNRESOLVED.csv`에 정확한 경로, rule/state 참조, 사유·소관·차단 여부를 남긴다.

## 4. 상태 공간 및 조립 평가 (D3)

- **출처의 문법상 후보**: 원본 조건에서 실제 언급된 속성/문자열 값만 추출해 조합을 만들며, 게임 엔진이 등록한 블록의 유효 상태 목록이라고 부르지 않는다. 조건에 아예 언급되지 않은 상태 차원은 파악 불가로 보존한다.
- 후보 Cartesian product가 **4,096개 이하**이고 예상 모델 옵션 적용 기록이 현실적인 크기이면 전수 열거해 각 상태별 매칭 규칙·multipart 동시 부품·대안 모델/weight·회전/uvlock을 기록한다. 이 수치는 **실행 관리용 제안 임계치**이며 고정 계약의 분모·완료조건을 변경하지 않는다.
- 4,096개 초과이거나 원장 크기가 과도하면, 속성별 유한 도메인·분할 조건(OR/AND·파이프 값)·매칭 규칙 묶음·정확한 조합 수를 **상징적 규칙/유한 증명**으로 남긴다. 무작위 표본만으로 전수 인증하지 않고, 분할의 상호 배타성·합집합 커버리지와 각 분할의 모델 대안 적용을 독립 검사한다. 증명 불가 영역은 정확한 범위와 함께 `UNEXPANDED/UNPROVEN`으로 표시하여 D3 PASS를 막는다.
- `variants`의 겹침·불일치·미지원 구조 또는 모델 배열 semantics가 모호할 때는 원본 사실과 계산 가정을 분리하고 `D_UNRESOLVED.csv`에 기록한다.

## 5. 기존 B/C 근거 연결 (D4) 및 E 분리

- 상태/규칙에서 실제 참조한 **고유 모델 경로 + Git blob SHA**를 찾고, C 최종 범위 [`C_SCOPE_2390_FINAL_STATUS.csv`](../../research/vanilla_models/phase_1-2-C/entry5/C_SCOPE_2390_FINAL_STATUS.csv), B 종료 범위 [`B_SCOPE_2390_STATUS.csv`](../../research/vanilla_models/phase_1-2-B/entry10/B_SCOPE_2390_STATUS.csv)의 정확한 행과 연결한다.
- B/C의 원본 face·UV·slot 상속·연결 PNG 경로/SHA는 **기존 증거를 참조**만 한다. C 기존 **2,304 모델 / 23,090 face / 1,073 고유 PNG**를 D 신규 측정으로 재계산하지 않는다. 선행 v69 중복 경로와 `brewing_stand`도 `PRIOR_SOURCE_REUSED`로 적는다.
- 모델이 기존 B/C 표에 없으면 자동으로 `없다` 혹은 `E 완료`로 결정하지 말고 원본 존재 여부를 별도 확인하고 `BC_OUT_OF_SCOPE/UNRESOLVED`로 표시한다. 기존 B/C 대상이 아닌 모델을 임의로 C 조사 완료로 승격하지 않는다.
- E 소관 모델은 **B-first 기하 없음 56개 + E-first 30개 = 86개**. 이들을 참조하는 blockstate JSON은 **D 모집단에서 제외하지 않으며**, 조립 근거까지만 D에 기록하고 실제 특수 기하/렌더는 E로 이관한다.
- `heavy_core` 기존 6면 증거는 C Entry5 정정본을 사용한다. 선행 보고서에 남은 이전 미해결 표기를 최종 사실로 재사용하지 않는다.

## 6. 매 Entry 산출물 및 채점 기준

| 산출물(각 entryN 폴더, Entry1은 기출력 보존) | 필수 내용 |
|---|---|
| `D_ORIGINAL_SOURCE_*.json/jsonl` | 각 원본 경로·Git blob SHA·JSON 실제 내용 또는 분할 snapshot 및 검수 상태 |
| `D_SOURCE_RULES.csv` | 원본 variants/multipart 규칙·선택 대안, 조건 AST/문자열, x/y/uvlock/weight의 존재와 값 |
| `D_STATE_ASSEMBLY.csv` · `D_SYMBOLIC_STATE_PROOFS.jsonl` | 전수 후보 상태별 규칙 적용 또는 재현 가능한 유한 상징 증명, 불전개 영역 |
| `D_STATE_MODEL_BC_LINKS.csv` · `D_MODEL_BC_CROSSWALK.csv` | 상태별 모델 옵션 및 B/C 고유 모델 path/SHA·기하/UV 근거 |
| `D_TEXTURE_C_LINKS.csv` · `D_UNRESOLVED.csv` | C PNG·slot의 경로/SHA 참조와 원인별 E/미해결 |
| `D_ENTRYN_REPORT.md` · `D_ENTRYN_INDEPENDENT_AUDIT.json` | 유일 경로·검증 개수·예외·독립 조건 재평가·게이트 상태·다음 회차 |
| `D_ENTRYN_REMOTE_READBACK.json` · `D_NEXT.md` | 원격 커밋 뒤 SHA/행수/내용 재조회, 다음 정확한 배정/차단 사항 |

- 파일 용량이 크면 정렬·행수·부분 SHA 명세를 넣어 **조각 파일로 나누고**, 전 조각을 재결합하여 원본 Git blob SHA/길이·행수 일치를 확인한다. 전수 원장 일부만 읽은 뒤 전체 readback PASS라고 주장하지 않는다.
- 각 회차마다 `source_json_inspected`, `candidate_states_exhaustively_evaluated`, `symbolically_proven`, `model_option_rows`, `model_paths_sha_linked`, `E_referred`, `unresolved`, `prior_evidence_reused`, `new_D_measurements`의 분자를 분리 기록한다. 예외와 증거 미비는 0으로 숨기지 않는다.

## 7. 독립 감사 및 최종 종료 게이트 (D1~D5)

| 게이트 | 독립 합격 기준 |
|---|---|
| **D1 — 고정 범위** | 원본 v34 목록 1,168경로와 배정표·Git SHA 1:1, 중복·누락 0, 각 Entry 배정 수 정확 |
| **D2 — 원본 규칙** | 모든 1,168 JSON 직접 조회·SHA/파싱 확인 및 모든 규칙·옵션·명시 키 기록; 미해결 원본 구조가 가려지지 않음 |
| **D3 — 상태 조립** | 전수 상태/유한 상징증명으로 전체 D2 규칙의 적용을 포괄; 게임 등록 상태 및 렌더 결과는 이 범위의 합격 판정이 아님 |
| **D4 — 출처 연결** | 모든 실제 참조 모델에 path/SHA 및 B/C 증거 또는 정확한 E/범위 밖·차단 사유 표시; 설명 불가 연결을 PASS로 위장 금지 |
| **D5 — 독립·원격 감사** | 스냅샷과 별도 평가기/사람 검수로 규칙·상태·모델 합산 재계산, 누적 1,168개 중복 0, A/B/C/v69 원장·소스 변경 0, 원격 GitHub SHA/내용 재조회 |

- Entry1 현재: **D1 PASS**; D2/D3/D4는 원본12개만 완료; D5 단계 최종감사 **PENDING**. 이번 계획 작성으로 추가 PASS를 선언하지 않는다.
- **ENTRY6 종료 조건**: D1·D2·D3·D4·D5가 전부 PASS인 경우에만 `D_COMPLETE_SOURCE_BLOCKSTATE_ASSEMBLY_SCOPE`; 하나라도 미통과면 `D_BLOCKED_AT_ENTRY6`와 실패 근거. 후속 수정은 별도 승인 범위에서 다루고 ENTRY7은 자동 생성하지 않는다.

## 8. 작업 경계·불변성·다음 시작점

- 제외: 공식 마인크래프트 JAR 진본 인증, 실제 게임 렌더/UV 회전 검증, 상태 레지스트리 확인, 동적 변화·랜덤 런타임, 특수 렌더 E의 실제 구현, 스타일 유형화 F, 최종 통합 G, 마인크래프트 가구 제작 및 프로젝트 좀보이드 TMX→마크 월드 변환.
- **원본 보호:** `1.21.11/assets/...` 원본, A/B/C 조사 파일과 원장, v69 검증 자료, 1-1 승인 150/150을 수정하지 않는다. 모든 추가 자료는 `docs/vanilla_models_1-2/` 및 `research/vanilla_models/phase_1-2-D/` 하위의 새 파일/기존 인계 문서 갱신으로 제한한다.
- **즉시 착수점:** 최신 GitHub HEAD 확인 → [`entry1/D_NEXT.md`](../../research/vanilla_models/phase_1-2-D/entry1/D_NEXT.md) 읽기 → [`entry2/D_ENTRY2_QUEUE_96.csv`](../../research/vanilla_models/phase_1-2-D/entry2/D_ENTRY2_QUEUE_96.csv)의 **96개 원본 JSON** 직접 조회·각 SHA 확인 → D2/D3/D4 조사 및 D5 해당 Entry 감사 → 커밋·원격 검증.

**준비 상태:** `D_WORK_PLAN_READY_ENTRY2`; **실제 조사 상태:** `D_IN_PROGRESS_ENTRY1` (12/1,168).
