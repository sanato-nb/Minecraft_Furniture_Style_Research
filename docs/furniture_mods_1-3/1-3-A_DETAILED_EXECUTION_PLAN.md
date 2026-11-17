# 1-3-A — v11~v24 기존 가구 모드 3D 연구 증거 재정합·독립 감사 세부 실행계획

- **기준일:** 2026-11-17 (KST)
- **상태:** `A_PLAN_READY_NOT_EXECUTED` — **계획만 확정**, A 직접 감사·기검증 자료의 신규 SHA 재검산·A 종료 승인 **0건**.
- **작업 저장소:** `sanato-nb/Minecraft_Furniture_Style_Research` / `main`
- **상위 계약:** [1-3 전체 실행계획](1-3_DETAILED_EXECUTION_PLAN.md) 및 [1-3 검수 계약](1-3_PLAN_CONTRACT.json)
- **범위:** `research/furniture_mods/v11` ~ `v24`에 저장된 **기존 연구 성과만** 재확인하고 모순·중복·누락·증거 등급을 분리. 새 모드 전체 목록 확정·신규 3D 모델 전수 조사·신규 재질 평가 작업은 **1-3-B 이후**.

## 1. 목표와 완료의 정의

1-3-A의 목표는 “얼마나 많은 모델이 존재하는가”를 새로 추측하는 게 아니다. 이미 기록된 **Another Furniture 원본 leaf 204개**, **blockstate 22개**, **부모 템플릿 69개**, Handcrafted 부분 연구 및 Macaw 접근 차단 기록을 **모드/버전/원본 경로/원본 SHA/선행 CSV·JSON 레코드/증거 수준**으로 연결하는 **기존 근거 대조 원장**을 만드는 것이다.

**완료 조건:** 14개 버전 디렉터리의 실제 파일 목록 고정, 핵심 누적 수의 중복 없는 재집계, 원본 접근 여부와 과거 검증 여부 명시, 모순·단절 원장 분리, **독립 재집계 + GitHub 커밋 후 SHA·행수·내용 재조회 + 기존 파일 무변경**. 기존 자료를 단순 재열람했다고 신규 모델 발견 또는 새로운 인게임 인증으로 표시하지 않는다.

### 과거 연구의 출발 수치 — *이번 계획에서 새로 검증한 수치가 아님*

| 대상 | 기존 체크포인트의 숫자 | A에서 확인할 문제 |
|---|---|---|
| Another Furniture leaf 모델 | v18 **33** + v21 **38** + v22 **43** + v23 **51** + v24 **39** = **204** | 각 회차의 source path와 SHA가 서로 **중복 없이** 합해지는가? 모든 204가 같은 고정 원저자 커밋에 속하는가? |
| Another Furniture 부모 원형 JSON | v20 **69** (v18의 30 포함, 나머지 39) | leaf 204와 **다른 분모**이며 실제 템플릿 경로/SHA 집합에 중복이 없는가? |
| Another Furniture blockstate JSON | v21 **12** + v23 **10** = **22**, 기존 트리 **177** 후보·잔여 **155** | 22개 경로·SHA 고유성, 원본 variant/apply 근거, 177 분모는 아직 B 단계에서 재확인해야 하는 과거 모집단인가? |
| v24 의자 | 신규 leaf **39** / 템플릿 `chair`19·`chair_tucked`20, 기존 5개 참조 모델 제외 | v23 신규 10상태의 참조 44개 중 기존 5개를 뺀 39라는 관계·상속 기하를 실제 행으로 재계산 |
| 의자 상속 기하 | 템플릿 각 10요소·46면 → leaf 39개에 **요소390/face1,794** 인스턴스 | 인스턴스가 고유 face나 PNG 실화소 건수로 오인되지 않았는가? `tucked` 원시 z -9 반례 보존 |
| Handcrafted | v12 **authored 모델120** 기록, **generated leaf 표본16**, v16 원본16, v17 PNG **24**·RG​​BA면 **784** | authored120/leaf16/PNG24/면784는 각기 다른 분모·증거 수준. 일부 이전 계량값은 **선행 측정 재사용**이지 A 신규 직접 판독 아님 |
| Macaw's Furniture | 이전 체크포인트 당시 공식 JAR 원본 직접 확보 실패·모델 JSON **0** | `BLOCKED_PRIOR_SOURCE`로 기록하고 현 시점 원본 확보 여부는 **B에서 재검증** |
| 1-4 참고 누적 | 두 모드 PNG **175**, 면 RGBA **4,113** | 1-3-A 모델 수에 더하지 않으며 1-4의 기존 성과로만 연결 |

**원저자 고정 소스 식별:** Another `crispytwig/AnotherFurniture` 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d` / MC **1.21.1**; Handcrafted `terrarium-earth/Handcrafted` 과거 기준 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`. 바닐라 기준 MC **1.21.11**과 모드 버전을 혼동하지 않는다. 이 문서의 명시가 현재 모드 버전과 라이선스 검증을 대체하지 않는다.

## 2. 입력 데이터: 읽는 순서와 소관

먼저 다음 파일을 **직접 재개방**하고 본문·경로·Git blob SHA를 기록한다. 인수인계 수치나 보고서 한 문장만으로 원장 행을 만들지 않는다.

| 순서 | 기존 파일 | A에서 사용할 근거 |
|---|---|---|
| A0 | `docs/furniture_mods_1-3/1-3_DETAILED_EXECUTION_PLAN.md`, `1-3_PLAN_CONTRACT.json`, `handoff/STATE.json` | 상위 범위·계승 상태·불변 조건 |
| A1 | `v11/blockstate_samples_12.csv`, `v11/template_metrics_69_total.csv`, `v11/representative_models_33_resolved.csv` | 초기 후보/측정/모수, 원본 직접 검증과 선행 지표 구분 |
| A2 | `v18/another_leaf_direct_1_of_3.csv` ~ `3_of_3.csv`, `v18/v18_original_model_audit_summary.json` | 원본 33 leaf 모델 출처·SHA |
| A3 | `v20/another_69_templates_direct_original_geometry.csv`, `v20/v20_another_69_original_template_audit.json` | 원형 69개 원본 SHA, 상속·기하 기준 |
| A4 | `v21/another_38_new_leaf_originals_batch_1_of_4.csv` ~ `4_of_4.csv`, `v21/another_12_blockstates_pinned_source_audit.csv` | 신규 38 leaf 및 상태 12 원본 경로·SHA |
| A5 | `v22/shutter_43_leaf_orig_batch_1_of_4.csv` ~ `4_of_4.csv` | 신규 43 leaf, 셔터 가족·템플릿 연결 |
| A6 | `v23/new_51_leaf_originals_batch_1_of_6.csv` ~ `6_of_6.csv`, `v23/new_10_blockstates_author_original_audit.csv`, `v23/new_10_blockstates_applied_model_records.csv` | 신규 51 leaf, 신규 상태 10, 원문 모델 적용 관계 |
| A7 | `v24/chair_remaining_39_original_json_geometry_audit.csv`, `v24/v24_chair_39_audit_summary.json`, v24 보고서 | 신규 의자 39, 부모2, 2개 상태별 모델 참조 예외 |
| A8 | `v12/handcrafted_authored_120_total.csv`, `v12/handcrafted_generated_leaf_sample_16.csv`, `v16/handcrafted_16_leaf_original_verification.json`, `v17/v17_pixel_region_summary.json` | Handcrafted authored/generator/PNG/면 지표 분리 |
| A9 | 각 v11~v24의 나머지 `.md/.csv/.json` 및 `v13~v19`의 질감·UV 기록 | 파일 단위 전체 인벤토리와 각 주장에 연결된 보충 근거·후속 1-4 소관 |

※ 위 파일명은 과거 원장에서 **확인한 실제 입력 후보**다. 나머지 버전 디렉터리의 파일은 작업을 시작할 때 Git tree로 모두 열거하며, **실제 읽지 못한 파일이나 CSV 레코드를 완료라고 쓰지 않는다**.

## 3. 세부 작업 패키지 및 순차 종료 조건

### A-00 — 사전 고정·원본 보호

1. 작업 직전 저장소 `main` HEAD와 `v11~v24` 각 파일의 `path, size, blob SHA, type`을 Git tree에서 확보한다. 경로·대소문자 및 숨겨진 분할 원장까지 포함.
2. `v11~v24`, 기존 `1-1`, `1-2-A~G`에 **쓰기 금지**를 적용. 신규 산출물은 `research/furniture_mods/phase_1-3/A/`에만 쓴다.
3. 파일별 위치·원본 SHA·문서종류·분모 및 증거 수준을 인벤토리화하고, 입력 누락·중복 파일·디렉터리 미접근을 `A_INPUT_ISSUES.csv`에 기록한다.

**통과:** 기존 14개 디렉터리 열거 완료, 최소 필수 입력 실제 접근, baseline tree/commit 고정. **파일 목록 조회만으로 내용 직접검증 PASS 불가**.

### A-01 — Another leaf 204개 출처·중복 감사

1. 회차별 원장 33/38/43/51/39를 실제 CSV 파서로 읽어 서로 다른 컬럼명 `source_path`, `source_sha`, `original_author_model_git_sha`, `git_blob_sha` 등을 **하나의 공통 스키마**로 정규화한다.
2. `asset_key = (mod, source_pin, asset_type, normalized_source_path)`를 기본키로 사용. raw source path 및 SHA는 별도 유지. 동일 SHA가 다른 경로에 있어도 **별도 경로 기록 + 내용 중복**으로 구분.
3. cohort 내부/회차 간 중복, 원본 SHA 충돌, 모델 ref-파일 경로 불일치, 부모 ref 누락·다른 커밋 혼입을 탐지한다.
4. **실제 원저자 원본 재다운로드/재개방**이 가능하면 해당 commit의 Git blob SHA를 다시 계산하여 독립 확인. 불가능하면 기존 행은 `PRIOR_REPORTED_SOURCE_SHA`이고 `A_ORIGINAL_REHASH_PENDING`으로 기록한다. 기존 검증을 새 A bytes 검증으로 자동 승격하지 않는다.
5. 결과는 `Another_204_PRIOR_SOURCE_CROSSWALK.csv`의 정확한 204경로 고유성을 재검산한 뒤 승인. 204/204가 확인되지 않으면 **누락/중복/비일치**를 행 단위로 남기고 미통과.

**통과:** 코호트 수·전체 고유 경로/출처 SHA/중복 수 재계산, 원본 접근 수준이 경로별 구분됨.

### A-02 — 상태 22/177 및 모델 적용 관계 감사

1. v21 12개와 v23 10개의 blockstate JSON 경로/원본 SHA를 조인, 고유 22개와 범위 관계를 검산한다.
2. 원본 `variants`/`multipart`/조건/`apply`/회전값 등의 **선행 증거**를 해당 상태 원본과 연결하고 상태 문자열 개수·선택 모델 참조 수를 분리한다. 과거 177개는 **B 단계 재검토 예정의 기존 트리 분모**이며 A 단계에서 전체 내용 확인 177/177로 쓰지 않는다.
3. `model_ref`가 Another 소스 모델인지 `minecraft:block/air`처럼 외부 참조인지 구별한다.
4. 상태별 `source_sha`가 앞선 참조 모델 원장의 출처와 같은 immutable commit에 속하는지 대조하고, 모형 참조만 있다고 원본 모델 JSON 직접 읽은 것으로 세지 않는다.
5. v24의 `facing=south,tucked=false,variant=3` 관련 birch/spruce 의자 **2개 반례**를 독립 이슈 키로 유지한다. 제작자 원본을 정상화하거나 추정 모델로 교체하지 않는다.

**통과:** 22개 고유 상태 선행 범위의 교차대조·참조 분모 구분, 155개는 **미검사 후보**로 보존.

### A-03 — 부모69·의자39·기하 표기 감사

1. v20의 부모 원형 69개 출처와 v18에서 조회된 30개 집합을 연결하고 **30은 69의 부분집합**인지 검사한다.
2. v24 leaf 39는 기존 v23 참조 44에서 과거 실측 5를 제외한 신원 집합임을 직접 재계산. 39 leaf의 `parent_template`이 `chair` 19 / `chair_tucked` 20이며 **자체 요소 0**, 템플릿 **각 10요소/46면**, 39 leaf에 적용한 **390 요소·1,794 face 인스턴스**인지 검산한다.
3. `tucked`의 원본 **z -9** 이동, 템플릿 자체 bbox, 0두께·UV 회전과 같은 반례는 원본 좌표에서 명시하되 인게임 위치·collision으로 확정하지 않는다.
4. leaf/원형/face 선언/적용 인스턴스/PNG 실화소는 각각 다른 분모 필드로 저장한다. 의자39가 참조한 텍스처 경로 24개를 **PNG 신규 디코딩 24개**로 잘못 기록하지 않는다.

**통과:** 모델 계보·집합·원시 기하·예외 일관성 및 분모 분리 완료.

### A-04 — Handcrafted·Macaw 출처 상태 감사

1. v12 Handcrafted의 authored 120 CSV, generated leaf 16 CSV, v16의 **원저자 커밋에 연결된 원본16**, v15의 **기존 원장 파생 기하**를 구별한다.
2. Handcrafted 과거 24 PNG/면784·Another PNG·두 모드 175 PNG/면4,113은 **1-4 근거 참조**로만 연결. `모델 수`·`고유 원형 수`·`PNG 수`·`면별 RGBA 수`를 더하거나 상호 변환하지 않는다.
3. v12의 authored120가 **전체 현행 Handcrafted 모델 모집단**이라는 추론을 금지하고, 해당 소스 기준의 원장 기록으로만 보존한다.
4. Macaw 과거 공식 JAR·모델 원본 미확보는 `PRIOR_BLOCKED`로 기록. **현재 원본 접근 재시도와 실제 모델 전수 조사**는 B 단계 책임으로 남긴다.
5. Handcrafted 원본 SHA 공란·code-generated 모델·특수 렌더는 `A_UNRESOLVED.csv`로 분리한다.

**통과:** 모드별 기록의 버전·원본접근·검증등급·분모가 일관되고, 미검증을 확정하지 않음.

### A-05 — 오차·증거 등급 및 결측 검토

- 다음 상태를 최소한 분리: `ORIGINAL_REHASHED_IN_A`(A에서 실제 원본 bytes를 다시 읽음), `PRIOR_SOURCE_VERIFIED`(이전 보고서의 직접 검증 증거), `PRIOR_DERIVED`, `FILE_SHA_ONLY`, `SOURCE_MISSING`, `CONFLICT`, `BLOCKED`, `OUT_OF_SCOPE_1_4`.
- **증거 등급과 처리 상태를 별도 컬럼**으로 유지. 예: `prior_evidence_grade`, `A_direct_bytes_read`, `A_source_sha_match`, `audit_status`는 서로 다름.
- 미해결 항목에는 `issue_id, evidence_path, expected, actual, affected_rows, severity, owner, recheck_method, blocks_A_gate`를 명시.
- A에서 해결되지 않은 모드 라이선스·JAR 접근성·버전 갭·모드 전체 수량은 **B 담당 미결정 원장**에 인계.
- 실제 원본 접근이 불가능하면 **접근 방법, 예외/오류 텍스트, 해당 원본 수량**을 남기며 기존 SHA의 존재만으로 원본 재해시를 주장하지 않는다.

### A-06 — 독립 검산·원격 반영·B 인수인계

1. 산출 CSV들에서 **별도 스크립트/독립 경로**로 204·22·69·39·기존 Handcrafted 구분을 재집계. 핵심 경로/SHA/분모의 합과 집합차를 계산.
2. `main` 변경 전후 비교로 **v11~v24·1-1·1-2 자료 변경 0** 확인. A 신규 파일/인수인계 문서만 커밋.
3. 커밋 후 GitHub 원격에서 CSV **헤더·행수·본문 일부/전체·blob SHA** 재조회하여 독립 감사 결과와 대조.
4. A 종료 PASS 조건이 부족하면 `A_BLOCKED_...` 또는 `A_PARTIAL_...`로 유지하고 구체적으로 **B에 넘길 수 있는 범위와 넘기면 안 되는 범위**를 구분한다.
5. 통과 시에만 `A_PRIOR_EVIDENCE_RECONCILIATION_PASS` 기록. 이는 모드 원본 전체 census나 1-3 전체 게이트 M1~M6 중 임의 완료를 의미하지 않는다.

## 4. 파일 설계 (A에서 실제 작성할 것)

**새 작성 위치:** `research/furniture_mods/phase_1-3/A/`. 기존 `v11~v24` 자료 수정 금지.

| 파일 | 기본 필드 또는 내용 |
|---|---|
| `A_INPUT_MANIFEST.csv` | prior_version, repo_path, git_blob_sha, bytes, file_kind, reads_ok, evidence_scope |
| `A_ANOTHER_204_PRIOR_CROSSWALK.csv` | cohort, mod, pinned_commit, model_ref, normalized_source_path, prior_source_git_sha, A_actual_source_git_sha, parent_ref, prior_evidence, A_rehash_status, duplicate_group |
| `A_ANOTHER_22_BLOCKSTATES.csv` | cohort, state, source_path, source_sha, kind, variants_or_multipart_count, model_ref_count, direct_original_grade, prior_overlap |
| `A_ANOTHER_69_TEMPLATES.csv` | model_path, source_sha, template_ref, own_elements, own_faces, v18_selected, v20_direct_source |
| `A_CHAIR_39_RELATIONS.csv` | leaf, source_sha, parent_sha, inherited_elements, inherited_faces, variant_ref, discrepancy_id, coordinate_note |
| `A_HANDCRAFTED_PRIOR_SCOPE.csv` | record_type, source_pin, path, source_sha, 120_authored_or_16_generated, grade, 1_4_reference, unresolved |
| `A_PRIOR_COHORT_RECOUNT.json` | 각 회차·분모·합·원본 접근 등급·중복과 충돌 집계 |
| `A_UNRESOLVED.csv` | issue_id, source, expected, actual, reason, owner, blocking_gate |
| `A_INDEPENDENT_AUDIT.json` | A0~A6 PASS/BLOCKED, error_count, source_readback, prior_immutable |
| `A_REPORT.md` / `A_REMOTE_READBACK.json` / `A_NEXT.md` | 판정·제한·GitHub SHA·행수·B로 넘길 고정되지 않은 모집단 |

**스키마에서 강제할 분모 종류:** `LEAF_SOURCE_PATH`, `TEMPLATE_SOURCE_PATH`, `BLOCKSTATE_SOURCE_PATH`, `DECLARED_FACE`, `INHERITED_FACE_INSTANCE`, `TEXTURE_REFERENCE_PATH`, `PNG_PIXEL_SOURCE`, `RGBA_FACE_REGION`. **같은 파일 안에서도 단위가 다른 숫자는 합산 금지**.

## 5. A 종료 감사 게이트

| 게이트 | 증거·판정 기준 |
|---|---|
| **A0** 파일 인벤토리 | v11~v24 전 디렉터리 파일 목록과 blob SHA, 필수 입력 재개방, 이전 원본 불변 |
| **A1** Another leaf | 5개 코호트 원본 경로 **33+38+43+51+39=204**, 경로 고유성, SHA/parent 연결, 직접 재해시 여부 정확히 표시 |
| **A2** 블록 상태 | **12+10=22** 고유 state, 177 총량은 과거 트리 분모로 분리, 모델 참조·2개 예외 정확히 유지 |
| **A3** 원형·기하 | 부모69·의자39·상속390/1,794의 정확한 단위와 증거 재계산 |
| **A4** 기타 모드 | Handcrafted authored120/leaf16/PNG24/면784 등 **서로 다른 단위** 유지, Macaw 과거 접근 차단을 오판 없이 기록 |
| **A5** 오류·인계 | 원본 접근 실패/중복/출처 불일치·라이선스/버전 미확정 목록, B 책임 분리 |
| **A6** 독립 검산 | 원장 수치 재집계 오류0, GitHub 커밋·SHA/행수/내용 재조회, 기존 v11~v24/A~G 데이터 미수정 |

**A 완료:** A0~A6 모두 PASS, 명시된 필수 교차대조 완료, 선행 증거와 신규 재해시를 분리한 상태여야 한다. `A`는 **기존 자료 출처 재정합 작업**이므로 과거 원본이 일부 미접근이어도 기록의 정직성을 유지할 수 있지만, *필수 근거 자체를 확인할 수 없는 상태*는 PASS가 아니라 BLOCKED다. **1-3 전체 M1~M6 게이트는 A 통과만으로 6/6이 되지 않는다.**

## 6. 착수 순서·주의·다음 단계

- 즉시 실행할 첫 단위는 **A-00의 실제 Git tree v11~v24 전체 목록 재조회**와 **A-01의 기존 204 원장 5개 코호트 파일 정규화**다.
- 표본이나 출처가 막히면 `A_UNRESOLVED.csv`를 먼저 저장하고, 중단된 근거를 이어보기 전까지 A 완료 상태를 올리지 않는다.
- A의 목적은 선행 자료를 **재사용 가능하게 만드는 것**이고, 모드별 **전체 원본 모델 수와 고정 분모는 반드시 1-3-B 공식 소스 census 이후**에만 결정한다.
- 메타데이터와 파생 지표만 게시하며, 저작권 허락 범위를 확인하지 않고 원본 모드 JSON·PNG·JAR 파일을 저장소에 복제하지 않는다.
- 본 계획서 작성은 **A 실행·원본 204개 재다운로드·A PASS를 의미하지 않는다**.
