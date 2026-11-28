# DBD-001 7-G 4차 실제 보완 검증

검증 커밋 ae0fc8cbb4242c96eb0b4ecedbe890891b978216; Actions 46158304393 / Job 141019725955 / artifact 15268916082. 고정 16개 실행: PASS 7, PARTIAL 9, HOLD 0, FAIL 0. T06/T08/T10 부분 근거 강화; 판정 변경 없음. 최초~3차 증거 보존.

| 시험 | 판정 | 실제 확인 | 남은 제한 |
|---|---|---|---|
| T01 | PASS | {"existing_tables":8,"unchanged_rows":{"ai_review":0,"asset":25387,"release":4,"research_execution":0,"research_run":0,"source_checkpoint":0,"source_job":0,"upstream_observation":0}} | - |
| T02 | PASS | {"initial":{"assets_added":25387,"assets_added_by_release":{"another-furniture-4.0.3-git":2994,"handcrafted-4.0.3-git":13626,"macaws-furniture-3.4.2-fabric":3999,"minecraft-java-1.21.11-git":4768}},"repeat":{"assets_added":0,"assets_added_by_release":{"another-furniture-4.0.3-git":0,"handcrafted-4.0.3-git":0,"macaws-furniture-3.4.2-fabric":0,"minecraft-java-1.21.11-git":0}}} | - |
| T03 | PASS | version distinct; conflicting existing key/digest and cross-catalog path blocked by guard | - |
| T04 | PARTIAL | locked definition and REPLACE blocked; finished append rejected; retry and rollback verified | local transaction fixture; cross-job restart and full execution writer not implemented |
| T05 | PASS | actual synthetic source SHA, parent, pointer, elements/faces, coordinate mutation checked | - |
| T06 | PARTIAL | asymmetric PNG, exact ordered fixture UV corners, mirrored UV rejection and frame hash verified | asymmetric fixture UV ordering and sampling verified; Minecraft UV-lock and other transforms remain unverified |
| T07 | PARTIAL | actual multipart source condition, selected option, model target, transform and negative controls | simple multipart fixture verified; complete namespace and condition resolver not verified |
| T08 | PARTIAL | PNG decode and size, render unit/attempt and distinct reference/report/output body binding verified | render/result provenance fixture verified; report assertion is not independent visual accuracy |
| T09 | PASS | UNKNOWN independent of geometry; invalid confirmation rejected | - |
| T10 | PARTIAL | two independent synthetic model dimensions and comparable-unit difference; consistent but incorrect ratio rejected | source-derived dimensional comparison verified; broader style metrics not independently verified |
| T11 | PARTIAL | candidate blocked; two distinct support bodies and steps required | distinct bodies not necessarily independent source cases; no full approval transition or claim relation cycle enforcement |
| T12 | PASS | four verdicts, denominator, latest result selection and stale PASS rejection | - |
| T13 | PARTIAL | revision/unit/source/approval, missing group, unfinished attempt, counterexample and evidence corruption controls | design prototype; production permission and source case authorization not integrated |
| T14 | PARTIAL | two malformed CSV names quarantined; identical blob paths preserved | fixture guard only; no transformation approval/import runner |
| T15 | PASS | reapplication rejected atomically; partial DDL rolled back; source unchanged | - |
| T16 | PARTIAL | local backup restored, evidence hashes, checkpoint and FK verified | local temporary restore only; real artifact expiry and cross-job restore not exercised |

T06의 비대칭 16×16 RGBA 픽셀 및 고정 UV 순서 4코너 검증(반전 음성 사례 포함)은 Minecraft UV-lock 오라클이 아니다. T08은 단위·실행·렌더 결과·독립 기준 및 보고서의 해시 연결을 검증했으나 독립 시각 정확성을 판정한 것은 아니다. T10은 두 합성 모델의 원본 높이 8/16, 4/16 및 차이 0.25를 대조하고 원본과 다른 수학적으로 일관된 비율, 비교 방법 불일치를 거부했다. 전체 스타일 측정은 미검증.

19개 고정 입력/14영역/기존 8테이블/신규 43테이블/2뷰/11 인덱스/기존 카탈로그 25,387개 및 재등록 0 유지. 운영 DB/main 변경 없음. 후속 T07/T11/T04/T13/T14/T16의 고정 설계 검증 보완은 필요하며, 전체 엔진 구현으로 범위를 넓히지 않는다.
