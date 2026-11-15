# 1-2-B Entry8 실제 원본 계보 및 기하 연구

Minecraft Java Edition 1.21.11, 2026-11-15 KST. 작업 시작 GitHub main HEAD: ecffe0adf4aaf907c3b241bf74ca5cbed2768ba0.

## 변경하지 않은 범위
- A = A_COMPLETE_SOURCE_SCOPE, 재연구 금지.
- 기존 v69 P1 원장 544행×393열, 검토원장 544행×70열, 승인 150/150, 상위 단계 1/5 유지.
- 기존 Entry1~7, 원본 1.21.11 소스는 덮어쓰거나 신규 성과로 계산하지 않음.

## 실제 원본 분석
- Entry7의 B-first 미검증 1,116개 중 **240개(P1 48, P2 96, P3 96)**를 우선순위와 그룹 단위 결정적 층화 선택(무작위 표본 아님).
- 원본 Git Blob SHA 직접 조회·JSON 파싱 leaf **240/240**. 이전 원본 소스 캐시를 재사용하고 신규 부모 **3개**(template_piston_head, flowerbed_4, stem_growth6)를 직접 조회. parent chain **240/240 해결**, 경로/SHA 불일치, 누락, 순환은 0.
- 17개 신규 leaf 경로는 이미 과거에 부모 소스로 읽었던 경로. 고유 원본 JSON 수 1,318 → 1,544(순증 226; 별도 신규 부모 3개 포함).
- 자체 기하 선언 29개, 부모 기하 상속 204개, 일반 elements 없는 소스 7개. 기하 제공자 고유 100개.

## Entry8 소스 기하 선언 재현
| 지표 | leaf별 적용 인스턴스 |
|---|---:|
| elements | 561 |
| faces 참조 | 2,242 |
| cullface 참조 | 904 |
| 0두께 요소 | 210 |
| rotation 요소 | 173 |
| 좌표 0~16 바깥 요소 | 40 |
| from > to 역방향 요소 | 2 |

부모 템플릿이 여러 leaf에 적용되면 반복 집계된다. 이것은 고유 큐보이드 수나 실제 화면 렌더 인증이 아니다.

원본 좌표를 수정하지 않은 역방향 요소: trial_spawner_inactive_ominous, vault_unlocking_ominous. 정확한 원본 SHA·from/to·제공자 경로는 INVERTED_COORDINATE_ELEMENTS.csv에서 조회 가능.

일반 elements 미확인 7개: oxidized_copper_chest, cherry_sign, warped_sign, block, thin_block, light_02, structure_void. block/thin_block 등의 추상 템플릿 가능성과 특수 렌더 여부는 실제 다른 근거로 판정해야 한다. 보이지 않는다는 의미 아님.

## Entry1~8 누적 B-first
| 분류 | 검증 완료 | B-first 미검증 |
|---|---:|---:|
| P1 | 297/514 | 217 |
| P2 | 596/1,039 | 443 |
| P3 | 591/807 | 216 |
| 전체 | **1,484/2,360** | **876** |

P2/P3의 P1 부모 계보는 1,187/1,846 소스 기반 확인. 확인된 1,187개는 P1 조상 no, 남은 659개 unknown. 전체 no로 강제 변경하지 않음. 일반 elements 있는 B-first 1,448, 없는 소스 36. E-first P1 30개 별도 보존.

## 검증
독립 소스/상태 교차검증: **39/39 PASS**, 원본 1,244개 행 보존. B1 범위 근거 PASS, B2/B3 PARTIAL, B4 PENDING. B_COMPLETE_SOURCE_GEOMETRY_SCOPE 상태로 변경하지 않음.
소스의 parent/elements/from/to/rotation/cullface만 이 단계에서 주장. UV·PNG는 C, 블록상태는 D, 특수 렌더는 E, 스타일 유형화는 F, 최종 검수는 G.

## 파일
B_ENTRY8_SELECTION.json; DIRECT_SOURCE_PROOF_240_3.json; SOURCE_JSON_CACHE_1544.json; MODEL_GEOMETRY.csv; ELEMENTS.csv; NEW_PARENT_SOURCES.csv; GEOMETRY_PROVIDER_REUSE.csv; B_NO_ELEMENTS_SOURCE.csv; INVERTED_COORDINATE_ELEMENTS.csv; B_SCOPE_2390_STATUS.csv; B_ENTRY8_AUDIT.json; B_ENTRY8_SUMMARY.json; B_NEXT.md. 원격 커밋 후 추가 사후검증 기록을 별도 파일로 저장한다.
