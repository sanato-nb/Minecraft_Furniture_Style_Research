# Minecraft Java 1.21.11 · 1-2-D Entry2 원본 조사 및 독립 검증 결과

**2026-11-16 KST** · 시작 main `89e6d53e9dd67987f6e203db9cc7578aefaf68fe` · 원본 범위 계약과 1,168개 배정표 불변.

## 1. 이번 원본 조사와 정확한 분모

- `research/vanilla_models/phase_1-2-D/entry2/D_ENTRY2_QUEUE_96.csv`의 **정확한 96 JSON**(`acacia_button.json` ~ `black_wall_banner.json`) 전부 GitHub 원본 본문 직접 조회·파싱·배정 Git blob SHA 대조 **96/96 PASS**, 불일치/중복/원본 실패 **0**. 6개 × 16개 원본 전문 snapshot에 SHA와 raw body를 보존했다. `D_ENTRY2_SOURCE_STATUS.csv`가 파일별 직접 확인 근거다.
- **새 Entry2 실제 조사 96개**. 이전 Entry1 12개를 신규 연구로 재집계하지 않는다. D 누적 **108/1,168 = 9.25%**, 미조사 **1,060개**. 기존 v34 원본 목록 신원 확인 1,168/1,168은 **원본 JSON의 전수 조사 아님**.
- 구조: **variants 87 JSON, multipart 9 JSON**; 원본 **797 규칙 위치 / 809 모델 선택 옵션**. 배열을 통한 선택 대안이 있는 규칙 **4위치**; 명시 weight 0(원본 가중치가 없는 배열의 실제 난수 정책은 인증하지 않음). 명시 x 185선택옵션, y 518옵션, uvlock 247옵션, uvlock 키 미명시 562옵션. `AND` 조건 출현60, `OR`/파이프 복수값 출현0(이 **96개**에서만 관찰된 값).
- 소스 조건의 관찰 속성값과 단일 boolean의 상보값으로 구성한 **884개 정적 문법 후보 상태**를 원본 규칙으로 평가했다. **1,274개의 상태·모델 선택 옵션 적용**을 기록. 각각의 `multipart` 동시 부품 그룹과 **동일 그룹 내부 대안 선택**은 분리 보존. **전수 전개 884/884**, 미전개0, 규칙 매칭 누락0(정의한 문법상 도메인에 한정).
- 이 후보 상태 공간은 조건에 **등장하는 값들로만 만든 유한 도메인**이다. 예를 들어 벽 연결의 `none`처럼 본문 규칙에 드러나지 않은 속성값과 게임 레지스트리의 진짜 등록 상태까지 전수 인증했다는 주장이 아니다. 단일 boolean 상보값은 계산에서 **추론값**으로 별도 표시한다.

## 2. 기존 B/C 근거 연결, 특수 렌더 분리

- 원본 선택이 참조하는 **고유 모델 211개/211개**를 기존 C 최종 범위표의 **모델 경로+원본 blob SHA**에 결합, 미연결0. **200개는 C 직접 모델, 11개는 C가 이미 E_EXCEPTION으로 분류한 특수 렌더 모델**이다. E 참조를 발견했다고 그 모델의 기하·렌더를 D에서 새로 해명한 것은 아니다.
- 기존 C의 200개 모델에 해당하는 **선행 적용 face 1,833 = PNG 연결 face 1,833 + 템플릿 미바인딩0**, 명시 UV 1,631 / UV 키 부재202를 재참조했다. 이는 **C 선행 실적이고 D 신규 face 측정0**이다.
- C의 다섯 Entry `TEXTURE_BINDINGS.csv`로부터 이전 슬롯 **707행/707행**을 소스 경로·SHA로 재대조, 실패0. 그중 **698개 슬롯은 C face-PNG 원장에 있는 PNG**, 고유 원본 PNG **95개**를 재사용했다.
- 나머지 **9개는 파티클 전용 슬롯**으로, C가 face 기반으로 만든 PNG 원장에는 포함되지 않은 **원본 PNG 경로 3개**를 가리킨다: `bell_bottom.png`, `bamboo_fence_gate_particle.png`, `bamboo_fence_particle.png`. 원본 `textures/block` Git 트리 `9a7172896d4a28b405b990733d51b77dcb50930c`에서 **각 파일 존재와 blob SHA를 따로 확인**했다. **RGBA 재복호화·픽셀 검사 및 실제 입자 렌더 검증은 수행하지 않았다.** 이 3개를 C의 1,073개 face-PNG에 몰래 합산하지 않는다.
- `D_EXCEPTION_REGISTER.csv`: 기존 **E 소관 모델 11개**, **기존 C의 면 PNG 원장 밖 파티클 경로 3개**를 각각 출처·소관으로 구분, D 원본 조립 범위의 미설명 모델 연결0. 원본 모델의 일부가 특수 렌더를 요구한다는 점은 E 소관으로 남는다.
- 기존 `heavy_core` C Entry5 정정 6면, A/B/C 종료 상태, v69 P1 원장 544×393 및 review544×70, 1-1 승인150/150, 상위 5단계 완료 1/5를 건드리지 않았다.

## 3. 독립 원본 재계산·원장·감사

- `D_ENTRY2_INDEPENDENT_SOURCE_AUDIT.json`는 원본 6×16 snapshot을 별도 파싱·독립 조건 평가하여 **96 원본 SHA/JSON PASS**, **797 규칙위치 / 809 옵션**, **884/884 상태 규칙 적용 일치**, **1,274/1,274 선택 모델 항목 일치**, **211/211 C path/SHA 참조 일치**, **11 E 예외 정확 분리**를 확인했다. 상태 불일치0, 모델 SHA 불일치0.
- `D_ENTRY2_C_SLOT_PNG_AUDIT.json`는 C 다섯 슬롯 원본과 C PNG 범위를 따로 다시 읽어 **707/707 슬롯 근거 일치**와 파티클 원본 세 경로 SHA 확인, 비교 불일치0을 기록했다.
- 모든 source JSON 전문을 `D_ORIGINAL_SOURCE_BATCH1_16.json` ~ `BATCH6_16.json`에 기록, `D_SOURCE_RULES.csv`(809), `D_BLOCK_SUMMARY.csv`(96), `D_STATE_ASSEMBLY.jsonl`(884), `D_STATE_MODEL_BC_LINKS.csv`(1,274), `D_MODEL_BC_CROSSWALK.csv`(211), `D_TEXTURE_C_LINKS.csv`(707), `D_EXCEPTION_REGISTER.csv`(14)와 연결했다. 대형 884행 상태 원장은 6개 PART 파일·SHA manifest도 기록하여 전부 재결합 시 canonical blob SHA와 동일하도록 했다.
- 원격 main commit 후 GitHub SHA·행수·내용 검증은 별도 `D_ENTRY2_REMOTE_READBACK.json`에서 확인한다. **이 보고서 단독으로 아직 원격 readback PASS를 주장하지 않는다.**

## 4. 게이트/제한/다음 작업

- **D1** 범위·배정 **PASS**(고정 1,168경로, Entry2 96/96). **D2·D3·D4는 누적108경로 부분 충족**이며 1,168 완료 전 전체 PASS 불가. **D5는 6회 마지막 종합 종료감사 PENDING**.
- 원본 1.21.11은 **사용자 추출 자산**이며 공식 JAR 진본 인증·게임 등록 상태·엔진 회전/uvlock 실제 렌더·애니메이션·특수 E 기하·가구 제작·좀보이드 맵 변환은 수행하지 않았다. 소스에서 없는 값은 게임 기본 상태라고 추측하지 않는다.
- 다음 **Entry3 정확한 265경로**, `black_wool.json`부터 `dripstone_block.json`까지. `../entry3/D_ENTRY3_QUEUE_265.csv`는 배정용으로만 만들어졌고 원본 JSON 내용 **0/265 미조사**. Entry4~6 각265 남음, **Entry7 없음**.
- **현행 상태** `D_IN_PROGRESS_ENTRY2`, 총 **108/1,168 (9.25%)**. 최종 Entry6에서 **D1~D5 모두 PASS**일 때만 `D_COMPLETE_SOURCE_BLOCKSTATE_ASSEMBLY_SCOPE`, 아니면 `D_BLOCKED_AT_ENTRY6`.
