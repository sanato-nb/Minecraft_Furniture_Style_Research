# Minecraft Furniture Style Research — 1-2-B Entry6 실제 원본 연구
> Minecraft Java Edition 1.21.11 · 기준 GitHub main `fdaffb052c03e8ad1989c13bbae1aa055e8392e4` · 2026-11-15 KST
>
> **B_IN_PROGRESS_ENTRY6.** 1-2-A의 `A_COMPLETE_SOURCE_SCOPE`는 종료 유지. 기존 1-1 승인 150/150, 상위 완료 1/5, v69 및 Entry1~5 연구 원본을 변경하지 않음.

## 실제 수행
Entry5가 이미 2026-11-15 GitHub commit `fdaffb052c03e8ad1989c13bbae1aa055e8392e4`에서 사후 검증된 상태임을 확인해 **Entry5를 재실행하지 않았다.**

Entry5 `B_SCOPE_2390_STATUS.csv`의 B-first 미검증 1,596개에서 결정적 우선순위×그룹별 층화 방식으로 **240개(P1 48 / P2 96 / P3 96)**를 선정하였다. 표본은 통계적으로 무작위 표본이 아니므로 전체 특성 일반화에 쓰지 않는다.

- 선정 모델 Git **원본 Blob SHA를 직접 240/240 읽고 JSON 파싱**. SHA와 G1 원본 4,669개 색인의 경로/타입 연결을 재확인.
- Entry1~5의 보존된 JSON 실제 읽기 근거를 재사용, 필요한 **새 부모 7개** Git Blob 직접 읽기. 계보 **240/240 해결**, SHA 불일치·존재하지 않는 부모·순환 0건.
- 14개 leaf 경로는 과거에 부모 원본으로 이미 읽힌 경로였음. 원본 **고유 파일 경로 855 → 1,088(순증 233)**; 신규 모델 식별 수와 혼동 금지.
- leaf 자체 요소를 선언 **30개**, 부모에서 기하 상속 **204개**, 일반 `elements`가 없는 소스 **6개**.

## 기하 선언 및 예외
| 항목 | 이번 Entry6 원본 소스 적용 개수 |
|---|---:|
| leaf별 적용 `elements` 인스턴스 | 552 |
| `faces` 선언 참조 | 2,239 |
| `cullface` 선언 참조 | 948 |
| 두께 0 요소 | 194 |
| 회전 선언 요소 | 154 |
| 원본 0~16 범위를 벗어난 요소 | 47 |
| 원본 좌표 `from>to` 역방향 요소 | 1 |
| 이번 기하 제공자 고유 경로 | 101 |

위 요소·면 수는 부모 템플릿을 사용하는 각 leaf별 **적용 횟수**다. 따라서 고유 JSON 선언 수가 아니다. 회전 전 좌표를 그대로 보존했고 실제 Minecraft 엔진의 보이는 결과를 이 단계에서 확정하지 않았다.

`vault_ominous.json` → `template_vault.json`에서 내부 면 템플릿의 **역방향 X 좌표**가 사용됨: `from=[15.998,3.002,0.002]`, `to=[0.002,15.998,15.998]`. 원본 값을 임의 수정하지 않고 `INVERTED_COORDINATE_ELEMENTS.csv`에 기록, C/E의 면·렌더 검증으로 인계.

일반 `elements` 미확인 6개: `copper_chest`, `warped_hanging_sign`, `end_portal`, `copper_golem_statue`, `barrier`, `light_05`. **안 보인다는 판정이 아니라 source JSON의 일반 요소 부재**이며, E 및 필요시 D로 인계.

## 원장 누적
| 영역 | Git 원본 JSON의 leaf·parent 계보 검증 | 남은 B-first |
|---|---:|---:|
| P1(B-first) | **201/514** | 313 |
| P2 | **404/1,039** | 635 |
| P3 | **399/807** | 408 |
| 전체 B-first | **1,004/2,360** | **1,356** |

P2/P3 P1 조상 의존성은 **803/1,846 소스 계보 확인**, 검증 범위 내 no 803, yes 0, 미확인 **1,043 unknown**. 미확인을 no로 바꾸지 않았음. 기하 소스 있는 B-first 980, 일반 요소 없는 B-first 24; E 최초 담당 P1 30개는 별도 보존.

### 완료 오인 금지
- 게이트 **B1 = 모집단·담당 근거색인 PASS**, **B2 = 부분, B3 = 부분, B4 = 대기**.
- `544/544` 원본 P1 조회를 544개 모두 기하·UV·PNG·엔진 렌더 완료로 계산하지 않는다.
- **UV/텍스처 = C**, **블록상태·조립 = D**, **특수 렌더러 = E**, **유형화 = F**, **최종 독립검수 = G**.
- B 완료 선언, 모델/가구 제작, 프로젝트 좀보이드 가구 변환 시작 금지.

## 증거 및 산출물
`B_ENTRY6_SELECTION.json`, `DIRECT_SOURCE_PROOF_240_7.json`, `MODEL_GEOMETRY.csv` (240행), `ELEMENTS.csv` (552행), `NEW_PARENT_SOURCES.csv` (7행), `GEOMETRY_PROVIDER_REUSE.csv` (101행), `B_NO_ELEMENTS_SOURCE.csv` (6행), `INVERTED_COORDINATE_ELEMENTS.csv` (1행), `B_SCOPE_2390_STATUS.csv` (2,390행), `B_ENTRY6_AUDIT.json` (**독립 검사 48/48 PASS**), `B_ENTRY6_SUMMARY.json`, `B_NEXT.md`.

GitHub 저장 완료 여부 및 원격 재조회 증거는 별도 `B_ENTRY6_POST_COMMIT_VALIDATION.json`으로 보관한다.
