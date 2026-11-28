# DBD-001 7-G 2차 실제 보완 검증

검증 커밋 2b3881d7ac80e18549c0d12964b68b23eea1ad6f; Actions 46157302810 / Job 141016682266 / artifact 15267968457. 고정 16개 실행: PASS 6, PARTIAL 10, HOLD 0, FAIL 0. T12 PARTIAL → PASS (설계 시험 범위), T04/T13 보완 후 부분 유지. 이전 실행 증거 보존.

| 시험 | 판정 | 실제 확인 | 남은 제한 |
|---|---|---|---|
| T01 | PASS | {"existing_tables":8,"unchanged_rows":{"ai_review":0,"asset":25387,"release":4,"research_execution":0,"research_run":0,"source_checkpoint":0,"source_job":0,"upstream_observation":0}} | - |
| T02 | PASS | {"initial":{"assets_added":25387,"assets_added_by_release":{"another-furniture-4.0.3-git":2994,"handcrafted-4.0.3-git":13626,"macaws-furniture-3.4.2-fabric":3999,"minecraft-java-1.21.11-git":4768}},"repeat":{"assets_added":0,"assets_added_by_release":{"another-furniture-4.0.3-git":0,"handcrafted-4.0.3-git":0,"macaws-furniture-3.4.2-fabric":0,"minecraft-java-1.21.11-git":0}}} | - |
| T03 | PASS | version distinct; conflicting existing key/digest and cross-catalog path blocked by guard | - |
| T04 | PARTIAL | locked definition rejects insert/update/delete/unlock; checkpoint retry and rollback verified | local transaction fixture; cross-job restart and full execution writer not implemented |
| T05 | PARTIAL | typed object FK, inherited provider and separate calculated value | no actual JSON parser or full original coordinate/pointer verification |
| T06 | PARTIAL | frame bounds, UV dimensionality and missing slot checked | no UV transform accuracy oracle or PNG frame extraction |
| T07 | PARTIAL | state/option FK, unresolved edge and cycle helper controls | no complete namespace resolver or multipart condition evaluator |
| T08 | PARTIAL | generation alone or nonindependent accuracy cannot pass | synthetic PNG and metadata only; full case/output/attempt cross-check not implemented |
| T09 | PASS | UNKNOWN independent of geometry; invalid confirmation rejected | - |
| T10 | PARTIAL | ratio, unit and finite value guards | no independent style or comparative measurement method validation |
| T11 | PARTIAL | candidate blocked; two distinct support bodies and steps required | distinct bodies not necessarily independent source cases; no full approval transition or claim relation cycle enforcement |
| T12 | PASS | four verdicts, denominator, latest result selection and stale PASS rejection | - |
| T13 | PARTIAL | revision/unit/source/approval, missing group, unfinished attempt, counterexample and evidence corruption controls | design prototype; production permission and source case authorization not integrated |
| T14 | PARTIAL | two malformed CSV names quarantined; identical blob paths preserved | fixture guard only; no transformation approval/import runner |
| T15 | PASS | reapplication rejected atomically; partial DDL rolled back; source unchanged | - |
| T16 | PARTIAL | local backup restored, evidence hashes, checkpoint and FK verified | local temporary restore only; real artifact expiry and cross-job restore not exercised |

잠금 트리거 17개 및 checkpoint 재시도/rollback, 최신 결과 및 전체 필수 그룹 검사, 미완료 최신 시도와 반례 차단 검증. 19개 고정 입력, 8 기존 테이블, 43 신규 테이블, 2 뷰, 11 인덱스, 카탈로그 25,387 및 재등록 0 유지. 1차 실행에서 나온 데이터 및 범위를 변경하지 않았다. 

추가 검토: SQLite REPLACE의 implicit delete/recursive_triggers 설정에 따른 scope 헤더 교체 가능성은 아직 시험하지 않았으며, 완료된 시도의 새로운 checkpoint append 제한도 필요하다. 최신 결과 선정은 동일 task의 기록된 attempt_no 기준이며, 실제 원본 파싱/렌더 정확성/운영 권한/교차 Job 재개 및 이관은 미입증. T04/T13은 이러한 한계로 PARTIAL 유지. 다음 보완에서 이 두 경계와 T05~T08/T10/T11/T14/T16의 고정 fixture 검사를 강화. 범위 외 실제 게임·운영 도입은 별도 승인 대상.
