# DBD-001 7-G 1차 시험 결과

검증 커밋 2176903c4f4b30fa28cd3f11b70c12b388b9cb6a, Actions 46155488364 / Job 141011092885 / artifact 15267865379. 임시 v4 복제 DB와 합성 fixture에서 고정 시험 16/16 실행, PASS 5, PARTIAL 11, HOLD 0, FAIL 0. CI success는 실행 성공이며 설계 승인 아님. 7-H 최종 승인은 보류.

| 시험 | 판정 | 실제 확인 | 남은 제한 |
|---|---|---|---|
| T01 | PASS | {"existing_tables":8,"unchanged_rows":{"ai_review":0,"asset":25387,"release":4,"research_execution":0,"research_run":0,"source_checkpoint":0,"source_job":0,"upstream_observation":0}} | - |
| T02 | PASS | {"initial":{"assets_added":25387,"assets_added_by_release":{"another-furniture-4.0.3-git":2994,"handcrafted-4.0.3-git":13626,"macaws-furniture-3.4.2-fabric":3999,"minecraft-java-1.21.11-git":4768}},"repeat":{"assets_added":0,"assets_added_by_release":{"another-furniture-4.0.3-git":0,"handcrafted-4.0.3-git":0,"macaws-furniture-3.4.2-fabric":0,"minecraft-java-1.21.11-git":0}}} | - |
| T03 | PASS | version distinct; conflicting existing key/digest and cross-catalog path blocked by guard | - |
| T04 | PARTIAL | scope drift and checkpoint hash mismatch rejected | guard detects mutation; immutable writer and real cross-job restart not implemented |
| T05 | PARTIAL | typed object FK, inherited provider and separate calculated value | no actual JSON parser or full original coordinate/pointer verification |
| T06 | PARTIAL | frame bounds, UV dimensionality and missing slot checked | no UV transform accuracy oracle or PNG frame extraction |
| T07 | PARTIAL | state/option FK, unresolved edge and cycle helper controls | no complete namespace resolver or multipart condition evaluator |
| T08 | PARTIAL | generation alone or nonindependent accuracy cannot pass | synthetic PNG and metadata only; full case/output/attempt cross-check not implemented |
| T09 | PASS | UNKNOWN independent of geometry; invalid confirmation rejected | - |
| T10 | PARTIAL | ratio, unit and finite value guards | no independent style or comparative measurement method validation |
| T11 | PARTIAL | candidate blocked; two distinct support bodies and steps required | distinct bodies not necessarily independent source cases; no full approval transition or claim relation cycle enforcement |
| T12 | PARTIAL | four verdicts and unit denominator controls | explicit selected result set; latest-result selection and all unit groups enforcement not complete |
| T13 | PARTIAL | revision/unit/source/approval/contradiction and actual evidence corruption controls | prototype search; no complete required-group or production permission gate |
| T14 | PARTIAL | two malformed CSV names quarantined; identical blob paths preserved | fixture guard only; no transformation approval/import runner |
| T15 | PASS | reapplication rejected atomically; partial DDL rolled back; source unchanged | - |
| T16 | PARTIAL | local backup restored, evidence hashes, checkpoint and FK verified | local temporary restore only; real artifact expiry and cross-job restore not exercised |

기존 등록 카탈로그 4릴리스 25,387개 재현 및 재등록 0, 기존 8테이블 구조 유지. 실제 원본을 다시 다운로드하지 않았으며 기존 DB에 저장하지 않았다. 신규 SQL은 설계용. 근거 손상·반례·미확정 기법을 제외하는 검색 fixture를 확인했다. 다만 현재 export는 모든 필수 단위 그룹의 존재 및 최신 결과 선택을 완전히 보장하지 않아 운영용 확정 지식 검색으로 사용할 수 없다.

## 고정 범위 후속 보완
- T04/T12/T13: 잠금/입력 fingerprint/선택된 결과 및 필수 unit group 검증을 강화. 특히 오래된 PASS 및 누락 group의 false-positive 방지.
- T05~T08/T10: 합성 원본과 구조·좌표·UV·상태·단위·렌더 증거 연결의 독립 기대값 검수. 실제 대규모 연구 파서/게임 정확성 검증으로 범위를 확대하지 않는다.
- T11/T14/T16: 근거 사례 식별/승인·반례·이관 격리·로컬 복구 계약의 음성 검증 강화. 실제 운영 이관·외부 저장소·TV001 렌더 정확성은 별도 범위.

16개 시험 분모 변경 없음. 이번 결과는 최초 실행으로 보존한다. 운영 DB/main 수정 없음.
