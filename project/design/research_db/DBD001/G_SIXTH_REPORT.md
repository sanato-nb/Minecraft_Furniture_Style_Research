# DBD-001 7-G 6차 실제 보완 검증 및 7-H 인계

검증 커밋 04c7111e1f6b8a4834b06af38402b686d000dc3b; Actions 46159601524 / Job 141023718555 / artifact 15268968317. 고정 16개 실행: PASS 7, PARTIAL 9, HOLD 0, FAIL 0. T04/T13/T14/T16의 부분 근거 강화; 판정 변경 없음. 이전 실행 증거 보존.

| 시험 | 판정 | 실제 확인 | 남은 제한 |
|---|---|---|---|
| T01 | PASS | {"existing_tables":8,"unchanged_rows":{"ai_review":0,"asset":25387,"release":4,"research_execution":0,"research_run":0,"source_checkpoint":0,"source_job":0,"upstream_observation":0}} | - |
| T02 | PASS | {"initial":{"assets_added":25387,"assets_added_by_release":{"another-furniture-4.0.3-git":2994,"handcrafted-4.0.3-git":13626,"macaws-furniture-3.4.2-fabric":3999,"minecraft-java-1.21.11-git":4768}},"repeat":{"assets_added":0,"assets_added_by_release":{"another-furniture-4.0.3-git":0,"handcrafted-4.0.3-git":0,"macaws-furniture-3.4.2-fabric":0,"minecraft-java-1.21.11-git":0}}} | - |
| T03 | PASS | version distinct; conflicting existing key/digest and cross-catalog path blocked by guard | - |
| T04 | PARTIAL | locked scope and terminal attempts immutable; checkpoint update/delete/replace, sequence, new attempt retry and rollback checked | local transaction fixture; cross-job restart and full execution writer not implemented |
| T05 | PASS | actual synthetic source SHA, parent, pointer, elements/faces, coordinate mutation checked | - |
| T06 | PARTIAL | asymmetric PNG, exact ordered fixture UV corners, mirrored UV rejection and frame hash verified | asymmetric fixture UV ordering and sampling verified; Minecraft UV-lock and other transforms remain unverified |
| T07 | PARTIAL | scoped namespace, alias cycle/missing, nested OR, weighted options, missing model and application coverage verified | bounded multipart and variant predicate fixtures; full variant selection and complete game resolver not verified |
| T08 | PARTIAL | PNG decode and size, render unit/attempt and distinct reference/report/output body binding verified | render/result provenance fixture verified; report assertion is not independent visual accuracy |
| T09 | PASS | UNKNOWN independent of geometry; invalid confirmation rejected | - |
| T10 | PARTIAL | two independent synthetic model dimensions and comparable-unit difference; consistent but incorrect ratio rejected | source-derived dimensional comparison verified; broader style metrics not independently verified |
| T11 | PARTIAL | two distinct scoped source model bodies, approval manifest, unrelated support, counterexample, cycle and changed step controls | two distinct scoped source fixtures and approval manifest verified; actual independent research evidence and production approval transitions not validated |
| T12 | PASS | four verdicts, denominator, latest result selection and stale PASS rejection | - |
| T13 | PARTIAL | revision/unit/source/approval, missing group, unfinished attempt, counterexample and evidence corruption controls | fixture allowlist, scoped source hash and rights filtering verified; production identity/permission enforcement not integrated |
| T14 | PARTIAL | two synthetic malformed CSV fixtures quarantined; exact source blob and corrected derivative/approval binding checked; duplicate paths preserved | synthetic transformation approval verified; actual historical CSV correction and production import runner not performed |
| T15 | PASS | reapplication rejected atomically; partial DDL rolled back; source unchanged | - |
| T16 | PARTIAL | local restore manifest, FK, checkpoint, missing/tampered/expired evidence rejection verified | local manifest and simulated expiry verified; real external archive retention and cross-job restore not exercised |

T04: terminal attempt 수정/삭제/REPLACE와 체크포인트 수정/삭제/중복/순서/해시 오류 차단. 로컬 새 시도/rollback만 검증, 실제 타 Job 재개 아님.
T13: 원본 scope 포함 및 body digest 확인, 호출자 전달 release allowlist, 제한/미확정 근거의 확정 재사용 제외. 생산 인증/권한 검증 아님. candidate metadata의 전체 비공개성은 보장하지 않음.
T14: 두 역사 CSV 이름을 이용한 합성 결함/수정 사례의 Git blob·파생 SHA·경로·승인 manifest 검증. 실제 역사 CSV 수정·자동 이관 없음.
T16: 로컬 SQLite backup 및 evidence manifest 복원, 파일 누락/변조/가상 만료 거부. 실제 외부 저장소/Job 간 복원 미검증. manifest는 현재 스키마와 근거 목록 비교이며 DB 전체 행 지문을 포함하지 않음.

19개 고정 입력, 14영역, 기존 8테이블, 신규 43테이블, 2뷰, 11인덱스, 원본 25,387 재현/재등록 0 유지. 실제 운영 DB/main 변경 없음.

## 7-H 인계
7-G 6차 실행 종료, 품질 PARTIAL. 다음 독립 심사에서는 고정 계획과 실제 시험 범위 일치, 14영역/16개 조건/원본 불변, 증거 해시 및 과거 결과 보존을 재대조한다. 남은 9개 PARTIAL을 설계 내부에서 수정할 결함과 별도 운영/연구 엔진 검증으로 분류한다. 실제 연구 엔진이나 생산 DB를 구현하는 식으로 범위를 임의 확대하지 않는다. 전체 PASS 및 다음 단계 실행 승인은 아직 없음. 특히 7-H에서 최신 결과의 삭제/변조 가능성, 필수 대상 scope 연결의 충분성, backup의 DB 행 지문, export의 권리 필터 경계를 재검토한다.
