# DBD-001 7-G 3차 실제 보완 검증

검증 커밋 08d1afd3e489047fc4773af7b48f08d9b3e9068e; Actions 46157953724 / Job 141018656190 / artifact 15267929786. 고정 16개 실행: PASS 7, PARTIAL 9, HOLD 0, FAIL 0. T05 PARTIAL → PASS (제한된 합성 모델 설계 시험). T04/T06/T07/T08 개선 후 부분 유지. 기존 실행 증거 보존.

| 시험 | 판정 | 실제 확인 | 남은 제한 |
|---|---|---|---|
| T01 | PASS | {"existing_tables":8,"unchanged_rows":{"ai_review":0,"asset":25387,"release":4,"research_execution":0,"research_run":0,"source_checkpoint":0,"source_job":0,"upstream_observation":0}} | - |
| T02 | PASS | {"initial":{"assets_added":25387,"assets_added_by_release":{"another-furniture-4.0.3-git":2994,"handcrafted-4.0.3-git":13626,"macaws-furniture-3.4.2-fabric":3999,"minecraft-java-1.21.11-git":4768}},"repeat":{"assets_added":0,"assets_added_by_release":{"another-furniture-4.0.3-git":0,"handcrafted-4.0.3-git":0,"macaws-furniture-3.4.2-fabric":0,"minecraft-java-1.21.11-git":0}}} | - |
| T03 | PASS | version distinct; conflicting existing key/digest and cross-catalog path blocked by guard | - |
| T04 | PARTIAL | locked definition and REPLACE blocked; finished append rejected; retry and rollback verified | local transaction fixture; cross-job restart and full execution writer not implemented |
| T05 | PASS | actual synthetic source SHA, parent, pointer, elements/faces, coordinate mutation checked | - |
| T06 | PARTIAL | actual synthetic RGBA PNG bytes, frame pixel SHA, bounds, UV dimensionality and missing slot checked | fixture RGBA frame extraction verified; full UV transform accuracy not verified |
| T07 | PARTIAL | actual multipart source condition, selected option, model target, transform and negative controls | simple multipart fixture verified; complete namespace and condition resolver not verified |
| T08 | PARTIAL | actual PNG decode, render dimensions, independent-reference metadata and attempt links checked | synthetic PNG checked; full case/output/result consistency and independent visual accuracy not verified |
| T09 | PASS | UNKNOWN independent of geometry; invalid confirmation rejected | - |
| T10 | PARTIAL | ratio, unit and finite value guards | no independent style or comparative measurement method validation |
| T11 | PARTIAL | candidate blocked; two distinct support bodies and steps required | distinct bodies not necessarily independent source cases; no full approval transition or claim relation cycle enforcement |
| T12 | PASS | four verdicts, denominator, latest result selection and stale PASS rejection | - |
| T13 | PARTIAL | revision/unit/source/approval, missing group, unfinished attempt, counterexample and evidence corruption controls | design prototype; production permission and source case authorization not integrated |
| T14 | PARTIAL | two malformed CSV names quarantined; identical blob paths preserved | fixture guard only; no transformation approval/import runner |
| T15 | PASS | reapplication rejected atomically; partial DDL rolled back; source unchanged | - |
| T16 | PARTIAL | local backup restored, evidence hashes, checkpoint and FK verified | local temporary restore only; real artifact expiry and cross-job restore not exercised |

실제 생성된 합성 JSON/PNG 바이트와 등록 해시/구조·프레임 픽셀 SHA 비교, 좌표·pointer·조건·회전·픽셀 해시 오류 차단 확인. 범위 REPLACE 우회 및 종료 시도 신규 checkpoint append 차단. 기존 19개 고정 입력, 8 기존 테이블, 43 신규 테이블, 2뷰, 11인덱스, 25,387 카탈로그 및 재등록 0 유지. 원본과 운영 DB/main 변경 없음.

## 남은 제한 및 후속 보완
- T04: 실제 다른 Job 재개 및 운영 실행기 미통합. 완료된 시도 상태를 다시 RUNNING으로 직접 바꾸는 우회 가능성 및 checkpoint 수정/삭제 방지 정책은 별도 검토 필요.
- T06~T08: 단순 합성 원본의 픽셀/조건/출력은 검증했지만 전체 UV 변환, namespace 및 multipart 해석, render output과 validation result의 교차 연결 검증 및 독립 시각 정확성 미입증. 합성 fixture의 단색 RGBA는 UV 방향의 정확성을 입증하지 않는다.
- T10/T11/T13/T14/T16: 측정 비교, 독립 사례와 승인, 검색 권한, 격리/이관, 장기 보존의 남은 조건 유지. 후속 시험은 이미 고정된 설계 경계 내에서만 수행하고 실제 게임 파서/렌더러 전면 구현 및 운영 마이그레이션은 확대하지 않는다.
- T05 PASS는 고정 합성 JSON 사례의 설계 검증이며 모든 Minecraft 모델 형식의 파싱/상속/형상 검증을 보증하지 않는다.
