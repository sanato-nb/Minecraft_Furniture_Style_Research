# 1-2-B Entry9 — 원본 Git Blob 부모 계보·기하 실측

Minecraft Java Edition **1.21.11**, 2026-11-15 KST. 착수 시 main HEAD `e2ca1877bbdd6ca075ecd38d09d8a1f37fa2f95c` 재확인. Entry8의 2,390행 상태 원장에서 `B_FIRST_2360` AND `B_parent_chain_source_verified=false`만 선정.

## 직접 수행한 신규 검증
- 신규 leaf **240개 (P1 48, P2 96, P3 96)** Git Blob 원본 SHA 지정 JSON 직접 열람 240/240. Entry1~8 leaf 1,484개는 신규 계상하지 않음.
- 고유 부모 원본 **93개**를 Git Blob 직접 재열람하여 계보 **240/240** 해결. 종전 캐시에 없던 신규 부모 **2개**(`template_anvil`, `template_redstone_torch`). 부모 누락·순환 0.
- 이전 소스 캐시 1,544개에서 현재 **1,767개**로 순증 223(신규 leaf 221 + 신규 부모 2); 새 leaf 19개는 이미 이전에 부모 소스로 읽은 파일이어서 고유 소스 증가에 다시 넣지 않음.
- 자체 geometry **34**, 부모 geometry 상속 **199**, 전체 상속 경로에 일반 elements 없음 **7**. 해당 7개는 특수 렌더 인증이 아니고 E 소관의 미해결 증거.

## 정확한 원본 기하 적용 인스턴스 (leaf별 중복 포함)
| 지표 | 이번 Entry9 |
|---|---:|
| elements | 585 |
| face 선언 참조 | 2379 |
| cullface 참조 | 889 |
| 0두께 요소 | 215 |
| rotation 요소 | 163 |
| 0~16 범위 밖 좌표 요소 | 59 |
| from > to 역방향 요소 | 3 |

역방향 사례: `trial_spawner_ejecting_reward_ominous`, `vault_active_ominous`, `vault`. 원본 `from/to`를 수정하지 않았으며 `INVERTED_COORDINATE_ELEMENTS.csv`에 제공자 SHA와 함께 보존. faces/cullface는 선언 참조이며 렌더링 결과나 UV 공식 검증이 아님.

## B 최초 담당 누적
| 우선순위 | 검증 | 미검증 |
|---|---:|---:|
| P1 (B-first 514) | 345 | 169 |
| P2 (1,039) | 692 | 347 |
| P3 (807) | 687 | 120 |
| **총 2,360** | **1,724** | **636** |

P2/P3 P1 부모 조상 의존 확인 **1,379/1,846**: source 기반 no 1,379, yes 0, **unknown 467**. 읽지 않은 것은 절대 no로 치환하지 않음. 전체 B-first 일반 기하 소스 있음 **1,681**, 전체 경로에 일반 elements 없음 **43**. E-first P1 30개는 이 분모에 넣지 않음.

## 독립 검산·단계 판정
독립 소스·기하 재계산 **30/30 PASS** (별도 `B_ENTRY9_AUDIT.json`). **B1 PASS**, **B2 PARTIAL**, **B3 PARTIAL**, **B4 PENDING**. B 완료 판정 금지.

**불변 유지:** 1-2-A `A_COMPLETE_SOURCE_SCOPE`; v69 P1 원장 544×393 및 검토 544×70; 1-1 승인 150/150; 상위 1/5; 과거 v1~v69와 Entry1~8. C(UV/PNG), D(blockstate), E(special renderer), F/G 별개이며 가구 제작·PZ 변환을 시작하지 않음.

## 산출물
`B_ENTRY9_SELECTION.json`, `DIRECT_SOURCE_PROOF_240_93.json`, `SOURCE_JSON_CACHE_1767.json`, `MODEL_GEOMETRY.csv`, `ELEMENTS.csv`, `PARENT_TEMPLATE_SOURCE.csv`, `B_NO_ELEMENTS_SOURCE.csv`, `INVERTED_COORDINATE_ELEMENTS.csv`, `B_UNRESOLVED.csv`, `B_SCOPE_2390_STATUS.csv`, `B_ENTRY9_SUMMARY.json`, `B_ENTRY9_AUDIT.json`, `B_NEXT.md`. GitHub 원격 커밋 후 blob SHA/행수 검증은 별도 추가 보고.
