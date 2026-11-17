# 1-3 가구 모드 3D 모델 구조 분석 — 세부 실행계획

**작성일:** 2026-11-17
**상태:** PLAN_READY_NOT_STARTED — 신규 1-3 감사·전체 모델 인벤토리·최종 승인 미착수.
**선행:** 1-1 바닐라 텍스처 승인 150/150, 1-2-G 사용자 추출 바닐라 원본 4669/4669·G1~G6 PASS. 1-2 전체 과제 종료는 별도 심사 대상.
**기준:** docs/01_1단계_학습계획_v1.md, docs/MASTER_PLAN_CURRENT_KO.md, research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md, handoff/STATE.json

## 1. 목표와 경계

**목표:** Minecraft 가구 모드의 원본 3D 모델이 바닐라의 구조를 어떻게 사용·확장하는지 실제 모델 소스/부모 상속/좌표/부품/치수/방향·상태/연결·다블록 관계로 설명할 수 있는 재현 가능한 증거 DB를 구축한다. 모델 출처→SHA→요소·면·상태→측정 방법→검수 판정이 이어져야 한다.

**1-3의 범위가 아닌 것:** 최종 PNG 픽셀·팔레트·텍스처·UV 실화소 계량은 1-4, 바닐라/복수 모드 공통 규칙의 최종 검수는 1-5, 모델링 권장치·스타일 규칙서는 2단계. 실물 가구 3D 제작·Minecraft 모드 구현·PZ 가구 정체 확정·TMX/월드 변환은 별도 제작 프로젝트. 공식 Minecraft 배포 JAR 및 인게임 렌더링을 검증하지 않았으면 PASS로 기록 금지.

## 2. 이전 분석 결과 — 보존·중복 실적 금지

| 출처 | 입증된 누적 범위 | 이 계획에서 주의할 사항 |
|---|---|---|
| Another Furniture | 원저자 crispytwig/AnotherFurniture, 소스 고정 커밋 57eb624cbb7f408d43398c7434b0d38d312cb55d, Minecraft 1.21.1, 선정 leaf 모델 원본 204개 직접 판독 | 204는 기존 선별 샘플로서 모드 전체 leaf 분모가 아님. 원본 SHA·경로를 재대조한 뒤 기검증으로 계승 |
| Another 블록 상태 | v24까지 제작자 트리 177개 중 원본 22개 조사, 155개 남음 | 고정 트리 재집계·SHA 검산 후 나머지 원본만 회차 배정 |
| Another 의자 39모델 | v24 신규 39개, 기존 chair/chair_tucked 템플릿 2개 재사용; 부모 상속 요소390·선언 면1794, 자체 요소0 | 1794면은 템플릿 인스턴스이며 실측 PNG RGBA 건수가 아님. tucked z축 원시 이동 -9, 상태별 모델 참조 예외 2건 보존 |
| Handcrafted | 과거 PNG 24개·face RGBA784개 검증 이력 | 3D 모델 전체 분모·모델 파일/버전/원본 SHA는 별도 조사 필요. PNG24를 모델24로 계산하지 않음 |
| Macaw's Furniture | 과거 공식 배포 후보 확인했으나 당시 원본 JAR 미확보, JSON 모델 실측0 | 공식 원본 바이트·SHA·라이선스 확인 전 조사 후보로만 표시 |
| 1-4 선행 자료 | 두 모드 PNG 실측 175종, 면 UV RGBA 4113건 | 다시 신규 모델/신규 PNG 실적으로 계상하지 말고 증거 참조 |

기존 v11~v24의 원본 연구 레코드·인수인계는 수정하지 않는다. Handcrafted 및 Macaw 정보는 오래된 시점의 근거이므로 **현재 지원 버전·제작자 배포 여부를 실제 소스 확보 단계에서 새로 검증**해야 한다.

## 3. 모드 우선순위와 최초 범위 설정

1. **Another Furniture (우선):** 고정된 제작자 소스가 이미 있으므로 이전 204 모델의 경로·SHA·부모 연결을 검산하고, 기존 22/177 blockstate와 155 미조사 파일을 독립 인덱싱한다. 동일 모델에 대한 재분석은 신규 모델 수 증가로 잡지 않는다.
2. **Handcrafted:** 원저자 원본/배포 아카이브와 적용 버전, 파일 형식(JSON, 생성코드 등), 법적 사용/재배포 조건을 확인하고 3D leaf·원형·상태의 **전체 모집단을 새로 고정**한다.
3. **Macaw's Furniture:** 저자 공식 원본 JAR 또는 재현 가능한 공식 소스의 SHA/파일 내용을 실제 확인할 때만 인증 범위에 포함한다. 확보 실패 시 출처 차단 기록과 유효한 대체 후보 선정을 별도 승인으로 처리한다.

원본 Minecraft 바닐라 연구 버전은 1.21.11이고 Another 원본은 1.21.1이므로 **비교 좌표계를 정규화하되 동일 게임버전·인게임 호환성을 인증한 것으로 간주하지 않는다.**

**상위 분류 9종:** 의자·스툴, 소형 테이블, 식탁·대형 테이블, 수납장·서랍장, 책장·선반, 소파·벤치, 침대, 주방 가구, 조명·장식물. source에서 증명 불가능한 정체는 미확인으로 남긴다.

## 4. 일관된 측정·판정 기준

| 항목 | 저장·검증 항목 |
|---|---|
| 원본 신원 | mod, 원저자, MC/모드 버전, 소스 URL/commit·배포 SHA, original_path, git blob SHA, asset_format, license, access_status |
| 모델 계보 | leaf_path, parent/template path+SHA, 재귀 상속 체인, 고유 원형, leaf own-elements, 상속 element/face, 순환·누락 |
| 모델 기하 | 각 요소의 from/to, pivot/rotation, 최소/최대 좌표, 원본/회전계산 bbox 별도, 너비·높이·두께·요소 간 간격, 0두께·역좌표·블록 밖 값 |
| 부품 구조 | 좌판·등받이·다리·팔걸이·프레임·문짝·쿠션·서랍·손잡이·장식 등: 기하/시각 근거 있을 때 확인, 이름만 보면 추론 상태 |
| 면 구조 | face 방향·texture slot·source UV·cullface/tint. 원본 UV 선언과 실제 PNG 픽셀 검증은 서로 다른 필드, 픽셀 감사 1-4로 이관 |
| 회전과 상태 | variants/multipart condition, alternate, x/y, uvlock, weight, 선택 model ref, facing, 조립 위치/연결 여부 |
| 다칸/특수 | 블록 점유·연결형/회전 소스·코드 증거; 원본 bbox와 실제 충돌박스·월드 점유·게임 렌더를 동일시하지 않음 |
| 불확실성 | evidence_type: SOURCE_DIRECT, STATIC_DERIVED, CODE_STATIC, SCREENSHOT, RUNTIME, INFERENCE, UNKNOWN. 미확인 원인·담당·재검증 기준 기록 |

일반 JSON 좌표는 원본 단위를 보존하고 검증된 경우에만 Minecraft 16좌표=1블록 정규화를 추가한다. 다른 형식의 모드에는 동일 좌표계를 추측 적용하지 않는다.

## 5. 실제 실행 소단계 1-3-A ~ 1-3-G

### A. 이전 v11~v24 기록 독립 감사
- Another 선별 leaf204·blockstate22/177·의자39, Handcrafted 과거 기하/텍스처 기록을 원본 경로/SHA·원형 ID별로 대조.
- 신규/기존/동일 SHA 다른 경로/공유 원형/렌더러 미확인 분류.
- 결과: PRIOR_CROSSWALK.csv, A_REPORT.md, A_INDEPENDENT_AUDIT.json.
- 통과: 재사용 원장·분모 분리·기존 원본 무변경. 신규 모델 실측 0으로 시작.

### B. 공식 원본 확보·모드 선정·고정 모집단
- 제작자 소스/배포 버전·저작권/라이선스·SHA/모델 형식 검증. 원본을 열 수 있는 모드만 SOURCE_VERIFIED 승인.
- 모드별 모든 leaf, parent/template, blockstate, 생성코드, custom renderer를 인벤토리하고 고유 path/SHA·유형 분포·직접 모델 참조를 고정.
- 기존 Another 상태177 / 미조사155 재계수. Handcrafted/Macaw 공식 원본 확보 실패 시 BLOCKED_SOURCE 표시, 임의로 완료처리 금지.
- 결과: SOURCE_REGISTRY.csv, FIXED_SCOPE.csv, ENTRY_QUEUE.csv, B_SCOPE_REPORT.md.
- **고정 분모와 유한 회차수는 B에서 실제 인벤토리 확보한 뒤에만 확정**. 204/177 수를 3모드 전체 분모로 추정하지 않음.

### C. 모델·부품·부모 상속·기하 전수 감사
- 고정 큐 대상 실제 JSON/코드 bytes·SHA 검산, 부모 chain/재사용 graph, own/inherited elements와 faces 분리.
- 원본 좌표·회전·요소 두께·bbox·일반/0두께·과도한 돌출을 개별 element별 기록.
- 가구 부품 대응은 계측+명시 근거로 확인; 단순 이름이나 AI 인상은 추론으로만 저장.
- 결과: mod_furniture_catalog.csv, mod_model_elements.csv, MODEL_PARENT_CHAINS.csv, PARTS.csv, C_AUDIT.json.
- 통과: 해당 고정 원본 직접 감사 100% 또는 명시적 출처 차단. 누락·부모 cycle은 예외 원장으로 보존.

### D. blockstate 방향·변형·연결형·다블록 조사
- variants/multipart, model option, x/y/uvlock/weight, 방향/연결/수납 변형을 원문별 대조.
- v24 의자 두 blockstate 원본의 특정 south 상태에서 variant=3임에도 모델1을 참조한 반례 2건을 그대로 보존.
- source JSON으로 확인 불가능한 멀티블록 실제 점유·충돌·anim·block entity는 code나 인게임 증거 없이 단정 금지.
- 결과: MODEL_STATE_ASSEMBLY.csv, CONNECTION_RULES.csv, D_AUDIT.json.
- 통과: 모델 ref 전수 조인, 규칙/선택 수 독립 재집계, 차단·예외 소관 명시.

### E. 공통 가구 유형의 구조적 패턴·반례 비교
- 9개 분류별 원형·폭/높이/두께·실루엣·부품 분해·모델 복잡도·연결/회전 패턴을 동일 단위로 측정.
- 가능한 범위 내 동일 유형을 **모드 2개 이상**으로 나란히 검토. 한 모드만 확인되면 single-mod evidence로 표기하고 보편 결론으로 승격하지 않음.
- 결과: furniture_category_comparisons.md, CATEGORY_EVIDENCE.csv, EXCEPTIONS.md.
- 통과: 원본 경로/SHA·요소 계산·반례 연결 완료, 과도한 일반화 없음. 보편 제작 권고는 1-5/2단계로 이관.

### F. DB 정규화 및 1-4·1-5 연계
- 모델/원형/부품/상태/texture slot의 ID와 근거 등급 연결. v24의 의자39가 참조하는 PNG24 경로 중 과거 151 PNG 실측과 겹치지 않는 파일을 1-4 후보로 등록.
- 과거 1-4 PNG175/face RGBA4113은 재검증·재사용 출처로만 표시. 새 PNG 픽셀 검사 수에 가산 금지.
- 결과: 1-3_TEXTURE_UV_HANDOFF.csv, MODEL_SOURCE_INDEX.csv, DB_VALIDATION.json.
- 통과: 모든 모델 ID 출처/버전/경로/SHA 연결, 1-4 미검증 목록과 1-5 비교 후보 목록 확정.

### G. 독립 종료 감사·원격 기록
- M1 원본·모드 버전·라이선스, M2 고정 분모·고유 asset, M3 부모·기하, M4 state·연결, M5 분류 근거·예외·1-4 인계, M6 독립 전수 재계산·GitHub SHA/행수/본문 검증·과거 파일 보호.
- 각 gate PASS/BLOCKED/NA+사유; 필수 원본·모드가 빠지면 범위 재승인 없이 PASS 금지.
- 결과: 1-3_INDEPENDENT_EXIT_AUDIT.json, 1-3_FINAL_REPORT.md, 1-3_REMOTE_READBACK.json, NEXT.md.
- **M1~M6 6/6 통과 및 검증된 고정 모드 원본 대상 전수 검사 완료 시에만 1-3_COMPLETE_SOURCE_GEOMETRY_SCOPE 선언**. 계획 시점 M1~M6=0/6.

## 6. 회차 분할과 오류 규칙

- A/B 이전에 1-3 전체 자산 수·종료율을 임의 산정하지 않는다. 실제 고정 모집단을 확정한 뒤 유한한 회차를 만든다.
- 권장 회차 크기는 모델 leaf 약 80~200 또는 상태 JSON 약 50~100, **작업 분할 단위일 뿐 확정 검증 대상 수 아님**. 긴 상태 규칙, 거대한 원형 family는 별도 분할.
- 회차마다 고정 큐 → 원본 파일/SHA → 부모·기하/상태 재계산 → 예외 원장 → 독립 감사 → GitHub 원격 SHA/행수/본문 재조회 → 인수인계 순서 준수.
- 실패 시 원본 경로·SHA·조건·소관을 기록하고 그 회차를 BLOCKED, 미검증을 PASS로 바꾸거나 새 Entry로 우회하지 않음.

## 7. 표준 산출물 위치

새 소스 분석 근거는 research/furniture_mods/phase_1-3 아래에 보관하고, 과거 v11~v24 산출물은 변경하지 않는다.

- SOURCE_REGISTRY.csv, PRIOR_CROSSWALK.csv, FIXED_SCOPE.csv, ENTRY_QUEUE.csv
- mod_furniture_catalog.csv, mod_model_elements.csv, MODEL_PARENT_CHAINS.csv, PARTS.csv
- MODEL_STATE_ASSEMBLY.csv, CONNECTION_RULES.csv, CATEGORY_EVIDENCE.csv
- furniture_category_comparisons.md, 1-3_TEXTURE_UV_HANDOFF.csv
- UNRESOLVED.csv, INDEPENDENT_EXIT_AUDIT.json, FINAL_REPORT.md, REMOTE_READBACK.json, NEXT.md

**모드 원본 JSON/PNG/JAR 저작권 자산은 허용 범위를 검토하지 않은 채 저장소에 재배포하지 않는다.** 기본 산출은 출처 URL·SHA·수치·감사 결과·허용 범위의 분석 메타데이터로 제한한다.

## 8. 가장 먼저 실제 착수할 항목

1-3-A에서 v11~v24 원장과 고정 제작자 SHA를 재대조해 Another 204 leaf·22/177 블록상태·의자39·Handcrafted 이전 근거에 대한 이전/신규·누락 목록을 만든다. 1-3-B에서 공식 소스를 얻은 모드들을 대상으로 정확한 분모와 유한한 Entry 수를 확정한다.

**본 문서 작성 자체는 1-3-A 실행이나 신규 모델 검증을 의미하지 않는다.** 전체 단계 1-2는 별도 종료 심사 대상이며, 1-3의 시작을 이유로 자동 승인하지 않는다.
