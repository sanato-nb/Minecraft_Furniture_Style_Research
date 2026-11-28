# DBD-001 7-G 5차 실제 보완 검증

검증 커밋 25a93bb670bf31f3c87dca5419622e7a66ab1478; Actions 46159077686 / Job 141022106930 / artifact 15269166833. 고정 16개 실행: PASS 7, PARTIAL 9, HOLD 0, FAIL 0. T07/T11의 부분 근거 강화; 판정 변경 없음. 이전 증거 보존.

| 시험 | 판정 | 실제 확인 | 남은 제한 |
|---|---|---|---|
| T01 | PASS | {"existing_tables":8,"unchanged_rows":{"ai_review":0,"asset":25387,"release":4,"research_execution":0,"research_run":0,"source_checkpoint":0,"source_job":0,"upstream_observation":0}} | - |
| T02 | PASS | {"initial":{"assets_added":25387,"assets_added_by_release":{"another-furniture-4.0.3-git":2994,"handcrafted-4.0.3-git":13626,"macaws-furniture-3.4.2-fabric":3999,"minecraft-java-1.21.11-git":4768}},"repeat":{"assets_added":0,"assets_added_by_release":{"another-furniture-4.0.3-git":0,"handcrafted-4.0.3-git":0,"macaws-furniture-3.4.2-fabric":0,"minecraft-java-1.21.11-git":0}}} | - |
| T03 | PASS | version distinct; conflicting existing key/digest and cross-catalog path blocked by guard | - |
| T04 | PARTIAL | locked definition and REPLACE blocked; finished append rejected; retry and rollback verified | local transaction fixture; cross-job restart and full execution writer not implemented |
| T05 | PASS | actual synthetic source SHA, parent, pointer, elements/faces, coordinate mutation checked | - |
| T06 | PARTIAL | asymmetric PNG, exact ordered fixture UV corners, mirrored UV rejection and frame hash verified | asymmetric fixture UV ordering and sampling verified; Minecraft UV-lock and other transforms remain unverified |
| T07 | PARTIAL | scoped namespace, alias cycle/missing, nested OR, weighted options, missing model and application coverage verified | bounded multipart and variant predicate fixtures; full variant selection and complete game resolver not verified |
| T08 | PARTIAL | PNG decode and size, render unit/attempt and distinct reference/report/output body binding verified | render/result provenance fixture verified; report assertion is not independent visual accuracy |
| T09 | PASS | UNKNOWN independent of geometry; invalid confirmation rejected | - |
| T10 | PARTIAL | two independent synthetic model dimensions and comparable-unit difference; consistent but incorrect ratio rejected | source-derived dimensional comparison verified; broader style metrics not independently verified |
| T11 | PARTIAL | two distinct scoped source model bodies, approval manifest, unrelated support, counterexample, cycle and changed step controls | two distinct scoped source fixtures and approval manifest verified; actual independent research evidence and production approval transitions not validated |
| T12 | PASS | four verdicts, denominator, latest result selection and stale PASS rejection | - |
| T13 | PARTIAL | revision/unit/source/approval, missing group, unfinished attempt, counterexample and evidence corruption controls | design prototype; production permission and source case authorization not integrated |
| T14 | PARTIAL | two malformed CSV names quarantined; identical blob paths preserved | fixture guard only; no transformation approval/import runner |
| T15 | PASS | reapplication rejected atomically; partial DDL rolled back; source unchanged | - |
| T16 | PARTIAL | local backup restored, evidence hashes, checkpoint and FK verified | local temporary restore only; real artifact expiry and cross-job restore not exercised |

T07: 합성 블록상태 2규칙/3옵션, 고정 assignment 3개에서 3개 적용 기록을 대조(2개 resolved, 1개 unresolved). namespace 불일치, 누락 모델, alias 순환, 원본 parent 경로 오연결, 적용 누락, variant predicate 중복을 검사. 실제 variant 선택과 가중 무작위 선택 및 전체 게임 해석은 미검증.
T11: 고정 scope 내 서로 다른 합성 모델 2개(base.json, second.json)의 release/path/pin/SHA256/byte_count 및 SOURCE 연결 검증. unrelated body, 근거 누락, 반례, 양방향 상충 관계, 개정 순환, 승인 후 단계 변경을 거부. 승인 manifest의 실제 독립 연구 일반화와 운영 승인자 인증·권한 및 상태 전이는 미검증. SHA256 이외 기존 등록 해시 방식의 적용은 별도 구현 필요.
19개 고정 입력, 14영역, 기존 8테이블, 신규 43테이블, 2뷰, 11인덱스, 기존 25,387 등록 재현/재등록 0 유지. 실제 운영 DB/main 변경 없음.
후속은 T04/T13/T14/T16의 설계 범위 내 검증 및 7-H 독립 종료 심사 준비. 고정 16개 시험의 미충족 근거를 삭제하거나 기준을 낮춰 PASS로 승격하지 않는다.
