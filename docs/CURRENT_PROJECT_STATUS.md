# 프로젝트 현재 진행도

**2026-11-19 KST · 1단계 고정 연구 범위 5/5 종료 승인.** 1-2 전체 심사 통과로 1단계를 마감했다. 2단계 모델링 규칙서에 넘길 근거는 1단계 정리에 연결했다.

[1단계 최신 정리와 근거](PHASE_1_SUMMARY.md)

## 이전 기록

아래는 작성 당시의 계획과 진행 기록이다.

## 2026-11-19 — 1-5-B·C·D 보류 항목 재검증

| 단계 | 진행 상태 | 확인 근거 |
|---|---|---|
| 1-5-B 공통 단위 측정 | 🟢 100% | 흰색 침대 보류 해제. 전용 모델 36면·64×64 UV와 HC 침대 78면 비교 및 월드·아이템 화면 확인 |
| 1-5-C 유형별 교차 비교 | 🟢 100% | 기존 제한 판정 7/7 재검증. 표본별 반례와 적용 범위 기록 |
| 1-5-D 반례·런타임 예외 | 🟢 100% | 런타임 검사 10/10 완료. R10 텍스처 77/77 검증 · 아이템 58개 및 블록 파괴 파티클 19개 |

[판정표·클라이언트 기록·월드 캡처](../research/furniture_mods/phase_1-5/runtime_followup/REPORT.md)

## 2026-11-19 — 1-4-F 독립 종료 감사 통과

**1-4-A~F 6/6 통과. 1-4 원본 텍스처·UV 연구 범위 종료 승인.** A~E 산출물 49개와 런타임 아틀라스 관측 217행을 동일하게 재현했다. 면 592,312개의 판정을 검산했으며, 원본 화소 근거가 있는 면은 585,969개(98.93%)다. 원격 기준 본문 75개와 CSV·TSV 41개의 행 수 및 연구 SQLite 무결성을 확인했다. [종료 감사 보고서와 1-5 인계](../research/furniture_mods/phase_1-4/F/REPORT.md)

## 2026-11-19 — 1-4-E 실제 텍스처 경로 검증

**경로 예외 8/8과 후보 16/16 판정 완료.** Another Furniture Fabric 클라이언트의 아틀라스에서 누락 ID 8개는 모두 `missingno`로 해석됐다. 후보 중 참나무 의자 13개는 실제 모델 면에 사용됐고, 나머지 3개는 고정 모델에서 미참조였다. 의자 등록 상태 176개를 고정 선택 조건 88개와 대조했다. 연구 SQLite에 근거를 추가하고, 기존 영면적 선행 측정 176행을 C의 점·선 화소 기록에 연결했다. [실측과 연구 DB](../research/furniture_mods/phase_1-4/E_followup/REPORT.md)

## 2026-11-19 — 1-4-C UV 예외 추가 화소 검증

**면 판정 592,312/592,312.** 기존 사각형 화소 실측 511,709면에 점·선·경계 접점·범위 내 일부의 화소 실측 74,260면을 보완해, 원본 화소 근거 **585,969면(98.93%)**을 확보했다. 자체 화소 근거가 없는 6,343면은 슬롯 미연결 6,202면, 원본 PNG 누락 139면, 범위와 겹치지 않는 UV 2면이다. 슬롯 미연결 중 6,196면의 자식 모델 바인딩을 확인했다. 실제 아틀라스 경계 렌더는 미검증이다. [화소·슬롯 검증 보고서](../research/furniture_mods/phase_1-4/C_followup/REPORT.md)

## 2026-11-19 — 1-3-D GitHub Actions 등록 상태 감사

| 실행 환경 | 등록 블록 | 엔진 등록 상태 | 기본 문맥 충돌 상자 |
|---|---:|---:|---:|
| Minecraft 1.21.1 · Another Furniture / Handcrafted | 441 | 107,424 | 244,266 |
| Minecraft 1.21.11 · Macaw’s Furniture | 714 | 8,562 | 19,620 |
| **합계** | **1,155** | **115,986** | **263,886** |

등록 상태를 1-3-D 원본 규칙에 대입한 결과 variants 누락·중복과 multipart 미선택은 모두 0건이다. 빈 이웃과 기본 주체 문맥에서 충돌 형상 조회 오류는 0건이었다. 원본 블록 상태 리소스 1,158개 중 등록되지 않은 3개는 Another Furniture의 `unused/oak_grandfather_clock`, `unused/oak_small_shelf`, `unused/white_awning`이다. 실제 월드의 배치 가능성, 주변 블록 변경에 따른 상태 전이, 엔티티별 동적 충돌은 대표 시험 범위까지 검증됐다.

[Actions 1.21.1 작업](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44355559182/job/134982603085) · [Actions 1.21.11 작업](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44355559182/job/134982604030) · [워크플로 설명](../research/furniture_mods/phase_1-3/runtime_actions/README.md)

## 2026-11-19 — 1-3-C·D 후속 검증

| 단계 | 현재 확인한 범위 | 남은 검증 범위 |
|---|---|---|
| 1-3-C 부모·기하·부품 | 정적 요소 미산출 108개의 원인을 재확인했다. 생성형 아이템 58개는 실제 게임에서 표시됐고, 6개는 요소 없는 기반 템플릿, 44개는 Macaw 부모 누락이다. Another의 부모 경로 누락 4개는 자체 요소가 있다. | 원본 누락 경로 총 48개는 결함 기록으로 유지. [C·D 후속 실측](../research/furniture_mods/phase_1-3/followup/REPORT.md) |
| 1-3-D 상태·방향·연결 | 미사용 차양의 누락 참조 4건은 원본에서 재확인했다. 실행에서는 차양 블록 미등록과 남향 의자 두 종류의 변형 중복을 확인했다. 세 모드의 대표 조립과 가구 12곳의 중앙 충돌을 실측했다. | 전체 변형과 충돌 박스 전수 검증은 미수행. [상태 원장](../research/furniture_mods/phase_1-3/followup/D_OBSERVED_STATES.csv) · [충돌 원장](../research/furniture_mods/phase_1-3/followup/D_COLLISION_PROBES.csv) |

## 2026-11-19 — 1-2-E·F 후속 검증

| 단계 | 현재 확인한 범위 | 남은 검증 범위 |
|---|---|---|
| 1-2-E 특수 렌더·예외 | 소스 86/86. 공식 1.21.11에서 대표 상태 84/84를 실측했다. 표면·효과가 보이는 사례 62, 관찰 범위에서 표면 없는 사례 22, 블록 상태가 직접 선택하지 않는 표시 템플릿 2 | 모델별 전체 변형과 아이템·리소스팩별 화면은 미검증. [E 실측 보고서](../research/vanilla_models/phase_1-2-E/followup/REPORT.md) |
| 1-2-F 가구형 원형·스타일 | 소스 분류 2,390/2,390. 기존 미결정 38개 중 36개는 자식 모델의 표면을 연결했고, 2개는 E 예외로 판정했다. 애니메이션 16종 원본 214프레임과 재생 순서를 모두 확인했다 | 게임 화면에서 16종의 보간 및 재생은 미검증. [F 소스 검수 보고서](../research/vanilla_models/phase_1-2-F/followup/REPORT.md) |

> **2026-11-15 최신 1-2-B Entry8:** 이전 Entry1~7의 B-first 1,244개 원본 소스 계보를 보존하고 신규 leaf **240개(P1 48, P2 96, P3 96)** Git Blob 원본 JSON 직접 검증 및 새로운 부모 3개 추가 검증. **누적 1,484/2,360, 미검증 876** (P1 297/514, P2 596/1,039, P3 591/807). P2/P3 P1 조상 직접 확인 1,187, 미확인 659. 기하 source 있음 1,448, 일반 elements 없음 36. 이번 leaf별 요소 561/면 참조 2,242, 좌표 역전 2개 원본 보존. 원본 JSON 경로 고유 1,544 (순증 226, 이전 부모로 본 leaf 17개 제외). 독립 감사 **39/39 PASS**. B1 범위 색인 PASS, B2/B3 PARTIAL, B4 PENDING; **A = A_COMPLETE_SOURCE_SCOPE 유지**. v69 544×393 및 review 544×70, 승인 150/150, 상위 1/5 보존. UV/PNG/블록상태/런타임 또는 가구 제작·PZ 변환 완료가 아님. [Entry8 보고서](../research/vanilla_models/phase_1-2-B/entry8/B_ENTRY8_REPORT.md) · [Entry9 인수인계](../research/vanilla_models/phase_1-2-B/entry8/B_NEXT.md). 이전 기록은 아래 보존.

> **최신 2026-11-15 / Minecraft Java 1.21.11 / 1-2-B Entry7 원본 분석:** 기존 Entry1~6 leaf1,004개 검증 결과는 재계상하지 않고, B-first 미검증에서 신규 **240개(P1 48/P2 96/P3 96)** 원본 Git Blob JSON 직접 열람·신규 부모 **5개** 추가 원본 확인. 부모 계보 **240/240**. B-first 누적 **1,244/2,360**, 미검증 **1,116**(P1 249/514, P2 500/1,039, P3 495/807); P2/P3 조상 확인995, unknown851. 일반 기하 소스 있음1,215, 요소 소스 없음29(E 검토). Entry7 요소 적용615, face 선언2,583, 좌표 역전 적용3건 원본 보존. 원본 고유 JSON 경로1,318(순증230; 기존 부모로 읽힌 leaf15개 중복 제거). 독립 교차감사 **49/49 PASS**. B1 범위 색인 PASS, B2/B3 PARTIAL, B4 PENDING; A = `A_COMPLETE_SOURCE_SCOPE`. 기존 v69 P1 544×393/review544×70, 1-1승인150/150 및 상위 완료1/5 보존. **B 완료나 UV/PNG·blockstate·runtime 인증 또는 가구 제작·PZ 변환 아님.** [Entry7 보고서](../research/vanilla_models/phase_1-2-B/entry7/B_ENTRY7_REPORT.md) · [Entry8 인수인계](../research/vanilla_models/phase_1-2-B/entry7/B_NEXT.md). 이전 기록은 아래 보존.

> **최신 2026-11-15 · Minecraft Java 1.21.11 · 1-2-B Entry6 원본 연구:** 이전 Entry1~5의 764개 leaf 검증 결과를 보존하고, B-first 미확인 중 **240개(P1 48/P2 96/P3 96)** Git Blob JSON 직접 열람 및 신규 부모 **7개** 직접 검증; 부모계보 **240/240**. 누적 B-first **1,004/2,360 직접 검증, 미검증 1,356** (P1 201/514, P2 404/1,039, P3 399/807); P2/P3 의존성 검증 803, unknown 1,043. 원본 기하 있음 980, 일반 `elements` 없음 24(E 담당). 이번 소스 요소 적용 552, 면 참조 2,239, 좌표 역전 1개 원본 보존. 고유 원본 JSON 경로 1,088(순증 233, 이전 부모 소스로 읽은 leaf 14개 중복 제거). 독립 원장 감사 **48/48 PASS**. **B1 범위 색인 PASS, B2/B3 부분, B4 보류**; 1-2-A `A_COMPLETE_SOURCE_SCOPE`, v69 원장, 승인 150/150, 상위 완료 1/5 보존. UV·PNG·블록상태·런타임 검증 및 가구 제작/좀보이드 변환 완료 아님. [Entry6 보고서](../research/vanilla_models/phase_1-2-B/entry6/B_ENTRY6_REPORT.md) · [Entry7 인수인계](../research/vanilla_models/phase_1-2-B/entry6/B_NEXT.md). 이전 기록은 아래 보존.

> **최신 2026-11-15 / Minecraft Java1.21.11 / 1-2-B Entry5 직접 연구:** 기존 Entry1~4 leaf524개 제외, B-first 미검증에서 **신규 leaf240(P1 48/P2 96/P3 96)** 원본 Git Blob JSON 직접 검증·부모 템플릿12개 추가 직접 조회, 부모 계보 **240/240** 해결. B-first source 계보 누적 **764/2,360**, 미확인 **1,596**. P1 **153/514**, P2 **308/1,039**, P3 **303/807**; P2/P3 조상 source 검증611, unknown **1,235**. 일반 기하 source746, 일반 elements 없음18(E 별도). 이번 원본 기하 요소 인스턴스550·face2306·flat172·rotation145·역방향좌표4, 교차감사 **41/41 PASS**. raw source SHA 기반 고유 경로 누적855. 1-2-A `A_COMPLETE_SOURCE_SCOPE`, v69 P1 544×393/review 544×70, 1-1승인150/150, 상위완료1/5 유지. **B1 원장범위 PASS, B2/B3 PARTIAL, B4 PENDING**; B 완료·UV/PNG·렌더링·가구 제작·좀보이드 변환 아님. [Entry5 보고서](../research/vanilla_models/phase_1-2-B/entry5/B_ENTRY5_REPORT.md) · [다음 인수인계](../research/vanilla_models/phase_1-2-B/entry5/B_NEXT.md). 아래는 이전 기록.

> **최신 2026-11-15 / Minecraft Java1.21.11 / B Entry4:** 기존 Entry1~3 직접 계보314개를 제외한 **신규 leaf210(P1 42/P2 84/P3 84)**, 신규 부모19개 Git Blob JSON 원본 직접 확인. **B-first 검증524/2,360, 미확인1,836**; P1 105/514, P2 212/1,039, P3 207/807. P2/P3 부모조상 확인419/1,846(`no` 419), `unknown` 1,427. 원본 기하 제공자512, 일반 `elements` 없음12(E 검토). 역방향 from/to 2사례 보존, 기하/원장 독립검사50/50 PASS. **B1 범위 원장만 PASS, B2·B3 부분검증, B4 PENDING.** raw source 경로 누적615이며 Entry3 보고서의 399는 기존 raw 경로 증거 전수 대조 결과396으로 정정(기존 파일 수정 없음). A는 `A_COMPLETE_SOURCE_SCOPE`, 기존 v69 P1 544×393와 review544×70 및 1-1승인150/150·상위 완료1/5 보존. **B 완료/UV·PNG/엔진렌더 인증/가구 제작·좀보이드 변환 아님**. [Entry4 보고서](../research/vanilla_models/phase_1-2-B/entry4/B_ENTRY4_REPORT.md) · [Entry5 인수인계](../research/vanilla_models/phase_1-2-B/entry4/B_NEXT.md). 아래는 이전 기록.

> **최신 확인: 2026-11-15 · Minecraft Java 1.21.11 · 1-2-B Entry3 진행 완료:** 이전 Entry1 leaf14·Entry2 leaf120 반복 없이 추가 leaf **180개(P1 36, P2 72, P3 72)** 및 추가 부모 템플릿33개 직접 원본 Git Blob SHA/JSON 판독. B-first 직접 계보 **314/2,360**, 남음 **2,046**, P1 **63/514**, P2 **128/1,039**, P3 **123/807**. P2/P3 조상 의존성 `no` 직접 증거 **251개**, `unknown` **1,595개**. 기하 출처 있음307·원본 elements 없음7(E 이관); 독립 원장검수 **36/36 PASS**, 아직 **B2/B3 PARTIAL·B4 PENDING**. B 진입 후 고유 원본 경로399, 이번 순증210(기존 부모 원본3중복 제외); 신규 모델 정체 발견 0. **1-2-A A_COMPLETE_SOURCE_SCOPE** 고정, **1-1 승인150/150**, 상위연구 완료1/5, 기존 v69 544×393/544×70 보존. **B 전체 완료·UV/PNG·실게임 렌더링 완료 또는 가구 제작/좀보이드 변환이 아님**. [Entry3 보고서](../research/vanilla_models/phase_1-2-B/entry3/B_ENTRY3_REPORT.md) · [다음 인수인계](../research/vanilla_models/phase_1-2-B/entry3/B_NEXT.md). 아래는 이전 기록임.

> **최신 연구 갱신 — 2026-11-15 / 1-2-B Entry2 수행:** 기존 1-2-A는 `A_COMPLETE_SOURCE_SCOPE` 보존. B 원본 leaf 120개(P1 24/P2 48/P3 48), 새 parent JSON43개 직접 Git SHA 판독, 부모 체인120/120. 이번 조사에서 원본 적용 요소333·face 선언 참조1300(동일 소스 반복 포함), 0두께122, 3개 source JSON 계보에 elements 없음. 전체 B-first **2,360개** 중 Entry1+Entry2 직접 계보 검수 **134개**, 나머지 **2,226개** 미확인. P2/P3는 **107/1,846개** 계보 확인, **1,739개 unknown** 유지. 전 2,390건 분모·담당·증거등급 색인 B1 source index PASS, B2/B3 부분·B4 종료 검수 대기 → **B_IN_PROGRESS_ENTRY2**. 기존 v69 544×393·review544×70 보존, 1-1 승인150/150, 상위 연구1/5 유지. [Entry2 보고서](../research/vanilla_models/phase_1-2-B/entry2/B_ENTRY2_REPORT.md) · [B 전체 상태원장](../research/vanilla_models/phase_1-2-B/entry2/B_SCOPE_2390_STATUS.csv). 아래는 이전 이력.

> **최신 1-2-B 실행 (2026-11-15, Java 1.21.11):** 1-2-A는 `A_COMPLETE_SOURCE_SCOPE` (G1~G5 50/50 종료)로 보존. 기존 B 범위에서 **leaf 원본 JSON 14개(P1 3/P2 8/P3 3) + parent 템플릿13개** Git SHA 직접 판독, leaf 부모계보 **14/14**, 상속 후 source element 인스턴스17·face 선언 참조84·0두께 요소3, 검수 **15/15 PASS**. **B 전체 아직 미완료**: B-first **2,360**(P1 514 + P2/P3 1,846), E-first P1 30 별도. 이 실적은 신규 고유모델 발견0·기존 연구 중복집계0이며 UV/PNG/렌더 인증 아님. [B 계획](../docs/vanilla_models_1-2/1-2-B_WORK_PLAN.md) · [B 첫 실측 보고서](../research/vanilla_models/phase_1-2-B/entry1/B_ENTRY1_REPORT.md). 기존 v69 원장 544×393, 승인150/150·상위 연구1/5 보존. 아래는 이전 연구 기록.

> **최신 확정 상태 — 2026-11-15 / Minecraft Java 1.21.11 / 1-2-A 종료:** 고정 계약 G1~G5 **5/5 PASS**, 독립감사 **50/50 PASS**, 실행 **3/3회차 완료** → **`A_COMPLETE_SOURCE_SCOPE`**. 원본 자산4,669, 역사 파일194·체크포인트26, P1 544, P2/P3 1,846의 source/SHA/근거수준·후속 소관 통합 완료. **1-2-A는 즉시 종료하며 4회차·v70-A 자동 신규 연구 금지**. 다음 연구는 **1-2-B 기하·부모 상속**(A의 미검증은 B~G에 명시 이관). v69 기존 544×393 및 review 544×70, 과거 v1~v69 자료 보존. **1-1 승인150/150, 상위 연구 완료1/5 유지**, 1-2 전체 심층검증 미완료, 가구 모델 제작·PZ 변환 미착수. [3회차 종료보고](../research/vanilla_models/phase_1-2-A_completion/round3/A_FINAL_REPORT.md) · [1-2-B 인수인계](../research/vanilla_models/phase_1-2-A_completion/round3/A_HANDOFF.md). 아래는 이전 단계의 연구 이력으로 유지됨.

> **1-2-A 고정계획 2회차 실제 수행 (2026-11-15 · 모델 연구 v69 유지)**: [2회차 연구 보고서](../research/vanilla_models/phase_1-2-A_completion/round2/ROUND2_REPORT.md) · [2회차 증거 요약](../research/vanilla_models/phase_1-2-A_completion/round2/ROUND2_SUMMARY.json) · [3회차 최종 감사 시작](../research/vanilla_models/phase_1-2-A_completion/round2/ROUND3_START.md). **G1 PASS(1회차 계승)** 자산4669 원본 경로·Git SHA, **G2 PASS(source provenance 범위)** 역사파일194개 기여 근거 분류·현대체크포인트26개 summary 내용/SHA 직접 열람(전부 개별 모델 기하 재실험 아님), **G3 PASS** P1 544개 출처·direct/derived/secondary/unknown 증거 등급 기록, **G4 PASS** P1 544 + P2 1039 + P3 807 전체2390개 B~G 소관 지정(의존성·렌더러 문제 미확인으로 명시 이관). **G5 PENDING: 3회차 독립 종료감사 전에는 A 완료로 표기 금지**. 과거 P1 원장 544×393과 review544×70 및 v1~v69 연구 파일 불변. 이미 검증된 결과를 신규 모델로 중복 계산하지 않음. A 최종 유한한 3회차 종료 또는 차단 기준 유지, 가구 제작·PZ 변환 미착수. 이하 역사 및 고정 완료계약 문서 보존.

> **최신 v69 (2026-11-15):** [1-2-A 양조기 원본7모델·multipart7규칙의 8가지 상태 전수 소스 검증](../research/vanilla_models/v69/REPORT.md) · [P1 누적 증거 544행×393열](../research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v69/NEXT_CHAT_HANDOFF.md). 1.21.11 실제 `brewing_stand` 본체1/병3/빈3 JSON과 원본 blockstate 조회·Git SHA 대조, v66 병/빈6 JSON 내용/SHA 재검증. 원본 geometry 선언 요소10/면36 모두 explicit UV, multipart7조건의 가능한 병 위치 3비트 **8조합 모두 정적 평가**: 매 상태 본체1+위치별3 모델=4모델·7요소·30면, 8상태 적용면 참조합 **240(새 원본 선언 240개 아님)**. 병/빈3쌍은 0두께 양면 평면 기하 동일하고 **원본 UV만 다름**, 위치1/2의 y회전 ±45°. 원본 PNG2 개 **16×16 bit8 indexed color-type3** Git SHA/IHDR, 새 RGBA 픽셀실측0·공식 클라이언트 렌더 인증0. v68 P1 기존 **206,176셀 값 보존**하여 544×393열, review **34,816셀 값 보존**해 544×70열. 신규 P1 신원0; 1-1 승인150/150·상위1/5완료, **1-2-A/1-2 계속 진행·실질완료율 미산정**, 가구 제작·좀보이드 변환 미시작. 이하 v68 이전 기록 보존.

> **최신 v68 (2026-11-15):** [1-2-A 원본 점등 촛불4·원본상태8·비공식 1.21.11 Java 특수 renderer5 경로 연구](../research/vanilla_models/v68/REPORT.md) · [P1 544행×379열 누적 증거](../research/vanilla_models/v68/07_P1_544_EVIDENCE_LEDGER.csv) · [인수인계](../research/vanilla_models/v68/NEXT_CHAT_HANDOFF.md). 원본 lit candle leaf4 + parent template4 직접 재조회 및 원본 blockstate8 variants 대조: leaf 자체 elements0, 상속 적용30요소·100면 원본 명시UV100, 같은 수의 unlit 모델과 동일 부모 template, lit PNG별도. candle_lit/candle 16×16 원본 PNG2 SHA/IHDR 확인(새 RGBA 픽셀0). geometry0 원본 모델5의 world BE 렌더러 등록4 및 special model mapping 확인은 **비공식 서드파티 Java 디컴파일 코드7파일 SHA·줄번호 근거**이며 공식 client.jar 런타임 인증이 아님. 누적 P1 v67 365열×544의 **198,560셀 보존**해 379열로 확장, review 544×64 이전 56열×544 **30,464셀 보존**. 기존 P1 원본 JSON 직접 판독 이력 544/544 유지(신규 고유모델0). 1-1 승인150/150·상위 연구 1/5완료, **1-2-A 및1-2 계속 진행/실질 완료율 미산정**. 마크 가구 제작·좀보이드 변환 미시작. 이하 v67 이전 기록 보존.

> **최신 v67 (2026-11-15):** [1-2-A 13개 own-elements=0 모델의 실제 원본 부모 상속·UV·blockstate 검사](../research/vanilla_models/v67/REPORT.md) · [P1 544행×365열 누적 원장](../research/vanilla_models/v67/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v67/NEXT_CHAT_HANDOFF.md). v66의 직접 원본 JSON read 544/544에서 **새 모델 신원·신규 고유 JSON 직접 판독 수 0**. 해당 기존 13 leaf 원본+부모 8 JSON+blockstates 9 직접 경로/SHA 재조회; **8개 leaf가 부모 요소 36개·원본 적용면134개를 상속(명시UV128/원본 UV키 없는 계산후보6)**, 나머지 원본5 모델은 자체/부모 요소가 없으나 blockstate target 참조 있음(게임 실렌더 기하 인증 아님). 원본 blockstate 참조 23, PNG9종 Git SHA/IHDR 확인, 새 RGBA 픽셀 실측0·엔진 인증0. v66 P1 기존 **190,944 데이터셀 전부 보존**해 365열로 확장, review 56열(과거26,112셀 보존). 1-1 승인150/150·상위5중1완료, 1-2-A와1-2 **계속 진행 중/완료율 미산정**, 가구 제작·좀보이드 변환 미시작. 이하 v66 이전 기록 그대로 유지.

> **최신 v66 (2026-11-15):** [1-2-A 원본 JSON 직접조회 누적544/544 + 기하·UV 과거 주장의 독립 검증](../research/vanilla_models/v66/REPORT.md) · [P1 544행×351열 증거 원장](../research/vanilla_models/v66/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v66/NEXT_CHAT_HANDOFF.md). 기존 v35~v65 직접모델 JSON 판독516모델에, 이전에는 선택 역사 원본 SHA만 근거로 있던 **28개 원본 모델 JSON을 경로+SHA까지 직접 읽고 파싱**해 누적 직접 JSON 조회 범위 **544/544** 확보(기하·UV·블록상태·PNG·공식 렌더러 전모델 완료 의미 아님). 이28파일 자체 own37요소·164면·원본명시UV164면(own elements0 모델13 포함). 기존 26모델도 추가 재조회, 이 라운드 합계54경로. 과거 v33 **12모델 암시UV 후보148면**을 원본 UV 키 없음·원본 SHA·기하 좌표·방향별 계산식 등 10항목 148/148 독립 일치(공식 렌더러 인증 아님). v38 선반 7 leaf+7 parent 원본 **명시UV 38면×17항목**, 블록상태24규칙 전부 일치, 32개 정적 조건에서 각 **본체15면+overlay1면** 원본 참조(컬링 전). 과거38면 중 인벤토리 전용18면은 월드 blockstate 동시 적용 아님. PNG oak_shelf 32×32 Git SHA/IHDR만 재확인, 새 RGBA 전체복호0. v65 P1 337열×544 **183,328셀** 전부 보존해 351열로 확장, 모델별 리뷰37→48열(기존20,128셀 보존). 1-1 승인150/150·상위1/5 완료, **1-2-A와1-2 진행 중**·실질 완료율 미산정, 가구 모델/좀보이드 변환 미시작. 이하 v65 이전 기록 보존.

> **최신 v65 (2026-11-15):** [1-2-A 과거 원본 CSV113·SQLite4 실제 Git SHA·내용 재조회](../research/vanilla_models/v65/REPORT.md) · [기존 연구파일 194개 내용 재조회/미완료 구분 원장](../research/vanilla_models/v65/00_HISTORY_194_FILE_AUDIT_LEDGER.csv) · [P1 544행×337열 최신 누적 증거](../research/vanilla_models/v65/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v65/NEXT_CHAT_HANDOFF.md). v62~v65 역사 파일194/194의 **원본 파일 내용 재조회 범위** 확보(CSV137·MD30·JSON19·Python4 소스·SQLite4 바이너리/스키마). 이것은 **각 파일의 모델별 의미론·3D·UV·PNG 픽셀·게임 렌더 전수 인증 완료가 아니다**. v65 새 CSV113개 **10,946행/행폭불일치0**, 과거 전체 인벤토리 파일 3개 제외 후 모델+CSV 근거쌍230/고유모델88(원본 SHA/이름 또는 전체경로 동일행). SQLite4는 Git SHA·헤더·B-tree 테이블행수 정적 확인만, `PRAGMA integrity_check` 실행 아님. P1 원본모델544경로/서로 다른 blob SHA539, 동일 SHA 공유2그룹/7경로 확인; SHA만으로 정체/형상 연결금지. v64 P1 544×330 이전 **179,520개 데이터셀 전부 보존**한 337열, source review 544×37, history194×26. 원본 JSON 직접판독 표시516·역사 SHA만28·실질 모델완성률 미산정; 승인 1-1 150/150, 상위1/5 완료, 1-2-A·1-2 계속 진행, 마크 가구 제작·좀보이드 변환 미착수. 이하 v64 이전 기록 보존.

> **최신 v64 (2026-11-15):** [1-2-A 역사 Markdown30·JSON19·Python4 원본 내용·Git SHA 재검증](../research/vanilla_models/v64/REPORT.md) · [194개 역사 파일별 내용 검수 원장](../research/vanilla_models/v64/00_HISTORY_194_FILE_AUDIT_LEDGER.csv) · [최신 P1 544행×330열 누적 증거](../research/vanilla_models/v64/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인계](../research/vanilla_models/v64/NEXT_CHAT_HANDOFF.md). v63 과거 v5~v43 원본파일194 인벤토리 중 기존 v62~v63 CSV24개의 선택 실물 내용 검증에 더해 **v64 MD30/JSON19/Python4=53개 소스 원문 SHA·내용 추가 검사**, 선택 누적 **77/194**, 이번 선별 검토 범위 미조회 **117(CSV113/SQLite4)**. 이전 v47 SQLite 선행 DB 확인 실적이 있으므로 미조회=역사상 미연구 아님. v30 원본 보고서9행이 `anvil/chipped_anvil/damaged_anvil` 3 leaf JSON을 이미 읽었다고 기록하여 v63의 '새 근거 복원'은 **역사상 최초 연구가 아님**을 확인. 새 모델 JSON/PNG 디코드0, 직접 JSON 재검증 모델 고유516·역사 SHA만28 유지. v63 P1 325열×544행 전 **176,800 데이터셀 보존**, v64 330열. 이전 역사 내용 전체 의미론 대조 완료 아님. 1-1 승인150/150·상위1/5 완료, 1-2-A/1-2 미완료·실질 완료율 미산정, 가구 제작/좀보이드 변환 미시작. 이하 이전 v63 기록 보존.

> **최신 v63 (2026-11-15):** [1-2-A 역사 연구 폴더21개·원본파일194개 SHA 인벤토리](../research/vanilla_models/v63/REPORT.md) · [P1 544모델 최신 원장325열](../research/vanilla_models/v63/07_P1_544_EVIDENCE_LEDGER.csv) · [v63 다음채팅 인계](../research/vanilla_models/v63/NEXT_CHAT_HANDOFF.md). v62의 선택 역사 CSV21개에 v63 신규3개 원본 내용 검수를 더해 **24개** 내용 확인(나머지170개 이번 선별 검수에선 파일 트리 SHA·경로만 확인, 전체 역사 전수 콘텐츠 검증 아님). 기존 선택 자료에서 근거가 없던 `chipped_anvil`, `damaged_anvil`의 **과거 v30 원본 CSV 모델SHA행 + 실제 1.21.11 원본 JSON SHA**를 복원. 모루 leaf3·템플릿1 총4 모델 원본 JSON 판독, 공통 4요소21원본 명시 UV면을 leaf3에 적용한 63면, 3 blockstates×4방향=12상태, PNG4개 SHA/IHDR(이번 PNG 실픽셀 재측정0). v35~v63 명시 직접 JSON 검토 이력 모델 **516**, 나머지28은 선택 역사 원본 CSV 행 SHA 증거; **깊이 검증 완료율 아님**. 선택 역사 교차표176→179링크·110→112고유 P1모델. v62 P1 원장 544×310 이전 **168,640 데이터셀 전부 보존**, v63 544×325 확장. 1-1 승인150/150·상위5중1완료, 1-2-A/1-2 진행 중·완료율 미산정, 가구 제작/좀보이드 변환 미시작. 이하 v62 기록 보존.

> **최신 v62 (2026-11-15):** [1-2-A 역사 증거 21개 원본 CSV·176링크 재검증](../research/vanilla_models/v62/REPORT.md) · [P1 544개 증거 등급표](../research/vanilla_models/v62/04_SOURCE_REVIEW_LEDGER_544.csv) · [P1 544행×310열 누적 증거 원장](../research/vanilla_models/v62/07_P1_544_EVIDENCE_LEDGER.csv) · [v44 증거 CSV SHA 오기 6링크 정정 근거](../research/vanilla_models/v62/03_V44_EVIDENCE_CSV_SHA_ERRATA_6.csv) · [다음 채팅 인계](../research/vanilla_models/v62/NEXT_CHAT_HANDOFF.md). 21개 원본 CSV 파일 SHA+해당 모델 SHA 행 근거 176링크/110모델 확인(typed path+SHA78, name+SHA98). v44의 v27 공유 증거파일 SHA 마지막 글자 누락으로 영향6링크, **원본 모델 SHA 오류는 아님**. v35~v61 명시 직접 JSON 검토 표시514개, 표시 없으나 선택 역사 SHA행28, 선택 범위 신원만 확인2 (미연구 판정 아님). v61 297열×544행 이전 **161,568 데이터셀 전부 보존**하고 v62 310열 확장. v5~v43 모든 역사 자료 전수 대조·실제 렌더/암시 UV 검증 아님. 1-1 승인150/150, 상위1/5완료, 1-2-A/1-2 미완료·실질 완료율 미산정. 아래 v61 이전 기록 보존.

> **최신 v61 (2026-11-14):** [1-2-A 가마솥 11개 P1 원본 분석](../research/vanilla_models/v61/REPORT.md) · [P1 증거원장 544행×297열](../research/vanilla_models/v61/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v61/NEXT_CHAT_HANDOFF.md). 11개 기존 P1 경로+원본SHA 심층 재검증(신규 신원 링크0), own55요소235면 / 부모 상속 적용153요소648면. **원본 명시UV 0면 / UV누락648면, 공식 엔진 암시UV 미검증**. 원본 blockstates4파일·8variant와 내용물 높이Y=9/12/15; 원본 PNG7경로+Git SHA/IHDR, **정지 PNG5개** 실제 Pillow RGBA1,280픽셀(불투명1008/투명272); 애니메이션 water/lava2개 프레임 PNG 전체 픽셀 검증은 하지 않음. 이전 v60 원장279열 전체 셀 값 보존, 실질 완료율 미산정. 1-1 승인150/150·상위1/5 완료, 1-2-A/1-2 진행 중, 마크 가구 제작/좀보이드 변환 미시작. 이하 v60 이전 기록 보존.

> **최신 v60 (2026-11-14):** [랜턴 P1 14모델 원본 기하·UV·6종 애니메이션 PNG 검사](../research/vanilla_models/v60/REPORT.md) · [P1 544행×279열 증거 원장](../research/vanilla_models/v60/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v60/NEXT_CHAT_HANDOFF.md). v59 이전 259열×544개 모든 셀 보존. 12개 leaf+추상 부모2개의 실제 JSON/SHA 재검증(원본 자체 8요소31면 vs 상속 적용56요소217면, 명시UV217/암시후보0, 0두께·회전 각28). blockstate6파일/variant12개 및 PNG.mcmeta6파일 frametime8 직접 확인. 새로운 PNG6종 16×48 픽셀(전체 RGBA 4,608개)을 Pillow로 직접 복원해 186 리프면×3프레임=558개 face-frame 샘플, 반복 포함 12,168 실 PNG 소스 RGBA 관측(고유 원본 좌표2,088)을 수행. 14개의 경로·SHA 신원은 기존 계승이며 새로운 식별0건, 독립 템플릿31면은 leaf override 없이는 texture 미해결. 실게임 엔진 UV방향·애니메이션 렌더링 미인증. **1-1 승인150/150, 상위5개 중1/5 완료 유지, 1-2-A/1-2 미완료·완료율 미산정**, 모델/좀보이드 변환 아직 시작 금지. 아래 v59까지는 역사 기록.

> **최신 v59 (2026-11-14):** [1-2-A P1 선반 35모델 실제 소스·기하·PNG 연구](../research/vanilla_models/v59/REPORT.md) · [P1 544행×259열 증거 원장](../research/vanilla_models/v59/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v59/NEXT_CHAT_HANDOFF.md). 이전 v58 242열×544행 전 셀 보존. 기존 P1 신원 링크를 보존하며 oak/spruce/birch/cherry 선반 리프28+공통 템플릿7(원본11요소38면, 상속 적용55요소190면, 원본 명시UV190/암시후보0)을 직접 원본 SHA와 대조. 블록상태4파일의 multipart96규칙, 유효128상태 정적검사, 원본32×32 PNG4종 Pillow 4,096 RGBA 픽셀 및 전면 명시UV 20면의 2,560 source 픽셀 직접 crop. 132개 나머지 리프면 색상 crop·실게임 렌더러는 미검증, 1-1 승인150/150·상위1/5 완료 유지, 1-2-A/1-2 진행 중·완료율 미산정. 아래 v58 이하는 역사 기록.

> **최신 v58 (2026-11-14):** [1-2-A 27 P1 모델 기하·상태·실제 PNG 연구](../research/vanilla_models/v58/REPORT.md) · [P1 544행×242열 원장](../research/vanilla_models/v58/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v58/NEXT_CHAT_HANDOFF.md). 기존 v57 225열 전체 보존. P1 다른27모델 원본 경로+SHA 재검증(원본 15요소20면, 상속 적용27요소32면, 명시UV24/계산UV후보8); 조각책장 256개 상태·퇴비통9개 상태 원본 JSON 정적 전조합 검사. 기존 PNG 경로와 겹치지 않는 4파일 Pillow RGBA 1,024소스 픽셀, 원본 명시UV 13면/768회 대조·계산 후보8면/1,152회 대조, 엔진 검증 아님. v44 선행 근거 17모델/32행 계승·신규 모델 식별0. **1-1 승인150/150·상위1/5 유지, 1-2-A·1-2 진행 중·실질 완료율 미산정.** 아래 v57 이하는 역사 기록.

> **최신 v57 (2026-11-14):** [16개 P1 원본 모델 기하·UV·blockstates·PNG 검증](../research/vanilla_models/v57/REPORT.md) · [P1 544행×225열 원장](../research/vanilla_models/v57/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v57/NEXT_CHAT_HANDOFF.md). v56 544×209열(과거 v55 198열 포함) 모두 보존. 기존 369 중 16개 모델 직접 소스 재검증(자체33요소/156면, 상속적용44요소/219면, 원본 명시UV95/계산 후보124), 원본 blockstates13(variants37/multipart68), PNG4경로 독립 Pillow 1,536소스 RGBA 픽셀, 석재 절단기 원본 명시UV 2면 소스196픽셀. 외부 Java 디컴파일의 셜커/해골 구조는 **보조 근거**로만 유지하며 런타임 검증 아님. v56 코호트 49경로 실적 재집계 금지. **1-1 승인150/150·상위1/5 완료 유지, 1-2-A·1-2 계속 진행·전체 완료율 미산정.** 아래 v56 이하 역사 기록.

# Minecraft Furniture Style Research — 현재 프로젝트 진행도

> **최신 v56 (2026-11-14):** [원본 PNG·UV 실측 연구 보고서](../research/vanilla_models/v56/REPORT.md) · [P1 전체 544행 209열 원장](../research/vanilla_models/v56/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v56/NEXT_CHAT_HANDOFF.md). v53 신규175 모델의 **남은 37개 텍스처 경로 원본 바이너리·Git SHA·PNG CRC·zlib Adler·RGBA 16×16 전픽셀 검사 완료**. 새 명시 UV face **2,926면**, 반복 포함 소스 픽셀 **21,416건**. v54~v56 누적 **해결된 PNG 49/49경로, 3,393면, 51,228회 반복 RGBA 관측**, 명시 UV3225·계산 후보168 구분. 이는 소스 PNG 측정이며 **P1 544개 전체 형상·UV·렌더러 완료가 아니다**. 1-1 150/150 완료, 상위1/5 완료, 1-2-A/1-2 진행 중·완료율 미산정. 아래 v55 이하는 기존 역사 기록.


> **최신 v55 (2026-11-14):** [원본 PNG·UV 검증 보고서](../research/vanilla_models/v55/REPORT.md) · [P1 544행·198열 최신 증거 원장](../research/vanilla_models/v55/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v55/NEXT_CHAT_HANDOFF.md). P1 모델 원본 path+SHA **544/544 유지**. 원본 PNG 바이너리/실제 SHA/Pillow RGBA **9개 추가**(v53+v55 확인 합계13개), v55 신규 UV 대응 면 **241건**(원본 명시73 + 케이크 원본 미기재 UV의 **기하 계산 후보168**) · 원본 PNG/UV 영역21종 · 반복 소스 텍셀28,076회. v54부터 누적 **467면/29,812회**, v53 신규175 모델 참조 PNG **49개 경로 중 12경로만 면 소스 픽셀 대조**. 케이크 실제 PNG 3개 alpha 불투명 마스크가 계산 후보 사각형과 일치하나 **게임 엔진 UV 공식/렌더 출력 인증은 아님**. 1-2-A/1-2 미완료·실질 완료율 미산정, 1-1 150/150 완료·상위 1/5 유지. 아래 v54 및 그 이전은 과거 기록.


> **최신 v54 (2026-11-14):** [원본 블록상태·UV 실측 보고서](../research/vanilla_models/v54/REPORT.md) · [P1 전체544행 원장](../research/vanilla_models/v54/01_P1_544_EVIDENCE_LEDGER.csv) · [v54 다음 채팅 인수인계](../research/vanilla_models/v54/NEXT_CHAT_HANDOFF.md). **P1 모델 path+SHA 544/544 유지.** v53 신규175 모델 관련 원본 블록상태 기존8 + v54 신규49 + skull/head 신규14 = **71 원본 경로**(원본 variants/apply 각239), 블록상태에서 **173/175 모델 직접 참조**, 나머지 2개는 피스톤 헤드 부모 템플릿. 피스톤 자식 face 텍스처 경로40/40 해결. 실제 PNG 3종의 원본 명시 UV 16영역, 모델별 face 226개에서 **1,736회 반복 포함 원본 RGBA 픽셀 관측**(중복 없는 텍셀 좌표298, 모두 불투명). **실게임 렌더/전체 1-2-A 완료 의미 아님. 1-1 승인150/150·상위1/5 완료 유지, 1-2-A/1-2 미완료, 실질 완료율 미산정.** 아래 v53 이하는 역사 기록.


> **최신 v53 (2026-11-14):** [원본 모델 전수 path+SHA 연구](../research/vanilla_models/v53/REPORT.md) · [P1 544행 확장 원장](../research/vanilla_models/v53/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅용 인수인계](../research/vanilla_models/v53/NEXT_CHAT_HANDOFF.md). **v52 369 → v53 544/544 P1 모델 원본 경로·SHA 연결**(175개 직접 원본 JSON 새 검사; 미연결0). 신규 자체 요소4/면20(명시UV20), 부모 적용3413면(명시UV3245·암시UV168), blockstate8파일·variants58, PNG4파일 실제RGBA1024픽셀. **544는 원본 신원 연결 범위이며 전체 1-2-A 의미론 통합·기하·UV·PNG·상태·렌더러 완료율이 아니다. 1-2-A/1-2 진행 중, 1-1 승인150/150·상위1/5 완료 유지.** 아래 v52 이하 내용은 역사적 기록.


> **최신 v52 (2026-11-14):** [v52 직접 원본 연구](../research/vanilla_models/v52/REPORT.md) · [P1 전체 544행 원장](../research/vanilla_models/v52/01_P1_544_EVIDENCE_LEDGER.csv) · [v52 다음 채팅 인수인계](../research/vanilla_models/v52/NEXT_CHAT_HANDOFF.md). v51 **335 → v52 369개** 모델 경로+SHA 연결(신규34, 미연결175). 신규 자체23요소/60면(모두 원본 명시 UV), 상속 적용394면(원본 명시376·암시18), blockstates9/variants43/배열 선택지103, 원본 PNG 4종 실제 RGBA1024픽셀 Git blob SHA 검증. **1-2-A/1-2 미완료·완료율 미산정; 1-1 승인150/150·상위1/5 유지.** 아래 v51 이하 '현행' 표시는 역사적 기록.


> **현행 v51 · 2026-11-14:** [1-2-A 원본 근거 보고서](../research/vanilla_models/v51/REPORT.md) · [544개 P1 최신 검증 원장](../research/vanilla_models/v51/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v51/NEXT_CHAT_HANDOFF.md). v50 **281 → v51 335개 P1 모델 경로+SHA 직접 근거 연결**, 검사 근거에서 미연결 **209개**(미연구 확정 아님). 신규 원본 P1 JSON **54경로** (선반28, 이끼카펫5+carpet 부모1, 가마솥10, 조명10). 원본 고유 요소44/면185(명시UV8·암시UV177), 상속 적용면826(명시 출처176·암시 출처650). 원본 blockstates15 파일·variants21·multipart110 규칙, 선반 정적128조합/256모델 적용. 가마솥 템플릿 3종 177면은 원본 UV키 부재. PNG 바이너리 읽기에서 UTF-8 오류, 실제 RGBA 픽셀0·엔진 렌더0 검증. **1-2-A·1-2 미완료 및 완료율 미산정. 1-1 v42 승인150/150, 상위 5과제 1/5 완료 유지**. 아래 이전 v50 '현행'은 과거 기록.


> **현행 v50 · 2026-11-14:** [원본 P1 모델 51경로 연구 보고서](../research/vanilla_models/v50/REPORT.md) · [P1 544행 최신 근거 원장](../research/vanilla_models/v50/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../research/vanilla_models/v50/NEXT_CHAT_HANDOFF.md). v49 230 → v50 **281개 원본 모델 경로+SHA 연결**, 검사한 출처에서 **263개 미연결**(미연구 확정 아님). 새 51개 모델 원본 직접 검증 = particle-only 22 / inherited geometry 27 / own source 2. 원본 자체 5 요소/22면(명시UV16·암시UV6), 상속 적용면 561건(명시UV519/암시UV42). 원본 blockstate 35파일 및 variants74, 해당 51 모델 중 월드 상태 참조49·템플릿2. 기존 랜턴 템플릿2 SHA 재검증 실적 재사용. 새 PNG RGBA 검증0·실게임 렌더0. **1-2-A·1-2 전체 미완료, 완료율 미산정. 1-1 승인150/150 완료 및 상위 1/5 완료 상태 유지.** 아래 v49 이하 '최신/현행'은 당시 스냅샷.


> **현행 v49 · 2026-11-14:** [1-2-A 원본 검증 보고서](../research/vanilla_models/v49/REPORT.md) · [P1 544 모델별 최신 원장](../research/vanilla_models/v49/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인계](../research/vanilla_models/v49/NEXT_CHAT_HANDOFF.md). v48 **171 → v49 230 SHA 연결 모델 경로**, 조사 출처에서 **314개 미연결**(미연구 확정 아님). 새 P1 source path 연결 **59** = 화분37 + 선반21 + 화분 parent1. 그중 **v47에 이미 직접 확인된 화분6개는 과거 근거 회수**, 새로운 직접 소스 연구 53개로 구분. 화분 원본 고유 30요소·106면(명시UV100/암시UV6), 상속 적용면978건; 선반 기존 7부모 원형 재사용/상속 적용면114건. 화분 original blockstate 37개 단일 variant, 선반 원본 multipart72/파생 static96조합. **새 PNG RGBA 측정 0, 인게임 검증 0, 1-2-A·1-2 전체 미완료 및 완료율 미산정**. 1-1 v42 승인150/150, 상위 5과제 중 **1/5 완료 유지**. 아래 과거 v48 이하 '현행'은 그때의 스냅샷.


> **현행 v48 · 2026-11-14:** [원본 모델/상속·UV·상태 1-2-A 연구 보고서](../research/vanilla_models/v48/REPORT.md) · [P1 544행 최신 검증 원장](../research/vanilla_models/v48/01_P1_544_EVIDENCE_LEDGER.csv) · [신규 정확한 SHA 연결 36건](../research/vanilla_models/v48/02_NEW_P1_36_TYPED_SOURCE_LINKS.csv) · [다음 채팅 인수인계](../research/vanilla_models/v48/NEXT_CHAT_HANDOFF.md). v47 135 → v48 **171개 P1 모델 경로 SHA 연결**, 검사된 근거에서 **373개 미연결**(미연구 확정 아님). 새 원본 모델 경로 36개 직접 조회/parent 20개 재검수; 원본 own element14/explicit UV faces68(그중 v38 기존 원형 3요소/18면 별도 재검증). 3가지 블록상태 원문 multipart 100규칙·파생 static320조합·1920 모델 적용. 별도 6개 블록상태 9 variants. PNG 실화소 신규 0, 런타임 검증 미실시. **1-2-A와 전체 1-2 미완료, 완료율 미산정, 1-1 승인150/150과 상위 과제1/5 완료 유지.** 아래 v47·v46 '현재'는 이전 체크포인트의 기록임.


> **현행 v47 · 2026-11-14:** [실제 근거 조사 보고서](../research/vanilla_models/v47/REPORT.md) · [P1 544개 모델별 최신 검증 원장](../research/vanilla_models/v47/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인계](../research/vanilla_models/v47/NEXT_CHAT_HANDOFF.md). v46 **124 → v47 135** 모델 source PATH+SHA 연결(신규 11 원본 모델 JSON 직접 조사), **409개는 검사 근거에서 미연결**이며 미연구 확정 아님. 역사 SQLite v5~v8 **4 DB 원본 테이블/행 실조사**(5/10/16/20테이블)·생성 스크립트 4개 확인, 이전 연결 53개 재검증·역사 중복 신규 0. 화분 템플릿 3모델+비콘의 원본 26요소/100명시 UV 선언면, bamboo_shelf 7 leaf 공통 v38 부모 원형 재사용, blockstates multipart 24개/파생 32조합. 실제 PNG 화소 재검증 신규 0. 1-2-A·1-2 미완료, 완료 퍼센트 미산정. v42 1-1 완료 및 상위 **1/5 완료 상태 유지**. 이전 문구의 v46/v45 '최신'은 과거 기록.


> **현행 v46 · 2026-11-14:** [1-2-A 실제 연구 보고서](../research/vanilla_models/v46/REPORT.md) · [P1 544 모델별 근거원장](../research/vanilla_models/v46/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [다음 채팅 전용 인계](../research/vanilla_models/v46/NEXT_CHAT_HANDOFF.md). v45의 기존 119 SHA 연결 모델 **경로**에서 9개 원본 JSON 직접 검사(기존 4 재검증·새 5 경로 추가)하여 **124/544 SHA 연결**, 검토 근거에서 미연결 **420개**. 역사 MD/JSON 49개 전체 원문 열람 및 SHA/경로/모델명 참조 검수, 최근 v35~v43 CSV 30개 재대조, SHA 동일해도 서로 다른 모델 경로 2그룹/7경로 확인. 모든 파일명을 같은 기하 구조로 보지 말고 `(asset_type, full_source_path, git_blob_sha)`를 유지. 1-2-A 및 1-2 **진행 중, 완료율 미산정**, 1-1 v42 150/150 완료 및 상위 5과제 중 **1/5 완료 유지**. 아래 이전 버전의 '최신' 안내는 당시 스냅샷.


> **현행 v45 연구 갱신 · 2026-11-14:** [1-2-A 실제 검증 보고서](../research/vanilla_models/v45/REPORT.md) · [544행 검증 상태 원장](../research/vanilla_models/v45/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [9개 추가 SHA 연결 증거](../research/vanilla_models/v45/02_NEW_EVIDENCE_LINKS_9.csv). v44 연결 110 + 과거 v30 중복 제거 후 증거 회수 2 + 새로운 acacia_shelf 7 leaf 원본 확인 = **119개 SHA 연결**, **425개는 조사한 근거에서만 미연결**. v44 제외 역사 CSV **86개 SHA 필드 조사**; v38 부모 7템플릿은 재사용, blockstate 원본 24개 multipart/파생 32조합. 1-2-A 전체 v5~v43 서술형/JSON 대조, PNG·특수 렌더 검증 **남아 있으며 전체 1-2 완료율 미산정**. v42 1-1 150/150 완료, 상위 **1/5 유지**. 아래 v44/v43 '최신' 표현은 역사적 스냅샷.


> **최신 전역 v44 · 2026-11-14:** [1-2-A 원본 근거 1차 재대조](../research/vanilla_models/v44/REPORT.md): P1 544 후보 중 110개 SHA 증거 연결, 미연결 434개(미조사 확정 아님), 176 증거 링크·중복5·SHA 타입 오탐2 해결. **1-2-A 진행 중**, 완료 과제 **1/5 유지**. 아래 v43 이전 문구는 역사 기록.


> **1-2 세부 정리 (현재 v43):** [현재 성과·모집단](vanilla_models_1-2/CURRENT_STATUS.md) · [7개 단계별 실행 계획](vanilla_models_1-2/WORK_PLAN.md) · [새 채팅 인수인계](vanilla_models_1-2/NEW_CHAT_START.md). 1-2는 진행 중, P1 544는 우선후보, v35~v43 선택 직접 leaf 32건은 전체 완료 분모가 아님. 전역 완료 **1/5**는 변경하지 않는다.


> **[과거 v43 기록] 당시 정본: v43 · 2026-11-14 (Asia/Seoul) · 상위 1단계 세부과제 1/5 완료.** 이 문서 및 [기계 판독 상태](../handoff/STATE.json)가 연구의 현재 진행 기준이며, v38~v41의 '최신/현재/0/5' 표현은 당시의 역사적 기록이다.

## v43 신규 1-2 증거

[자동 제작기 네 모델의 원본 JSON SHA·UV·48 상태 및 v36 경로 유형 오탐 정정](../research/vanilla_models/v43/REPORT.md). v31 책장 256상태와 v38 선반 32상태는 신규 실적으로 중복 계상하지 않는다. 1-1 v42의 완료 판정과 전역 완료 세부과제 1/5 유지. 공식 JAR/인게임 검증은 제외·미수행.

## 진행 상태

| 상위 1단계 세부과제 | 검수 판정 | 현재 입증된 범위 |
|---|---|---|
| **1-1 바닐라 재질·텍스처 분석** | **완료 (승인된 소스 연구 범위)** | 고정 표본 **150/150** 텍스처, **11/11** 재질 분류, v42 통합 검수 |
| **1-2 바닐라 3D 모델·기하·UV·블록상태** | 진행 중 / 최종 미승인 | [v43 crafter 신규 근거](../research/vanilla_models/v43/REPORT.md): P1 544후보, 선택 회차 직접 leaf 기존 28+신규 4=32, 원본 48 상태, v36 SHA 출처 유형 오탐 2건; 전체 완료율 미산정 |
| **1-3 가구 모드 3D 모델 구조 분석** | 진행 중 / 최종 미승인 | v24까지 Another Furniture 204개 leaf 원본 분석 등 과거 실적 유지 |
| **1-4 가구 모드 텍스처·UV 분석** | 진행 중 / 최종 미승인 | v23까지 원본 PNG 175종 및 면별 RGBA 4,113건 등 과거 근거 유지 |
| **1-5 바닐라↔가구 모드 비교** | 예비 단계 | 비교 5쌍, 전체 비교 연구 종료 판정 없음 |

**1/5 = 세부과제 완료 건수이며, 전체 프로젝트의 작업량 기반 진척률 20%가 아니다.** 별도 상위 2단계인 실용 가구 모델링 스타일 가이드는 최종 완성 전이다.

## 1-1 최종 근거 (현재 완료된 과제)

- [v42 11단계 / 150개 통합 보고서](../research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/REPORT.md)
- [v42 개별 텍스처 원장 150개](../research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/TEXTURE_150_SCOPE_LEDGER.csv)
- [v42 11개 재질별 근거 요약](vanilla_texture_1-1/CURRENT_STATUS.md)
- [2026-11-14 근거 정합성 독립 재감사](../research/vanilla_textures/audits/2026-11-14_v42_scope_verification/REPORT.md)

**재감사 핵심:** 원본 블록 PNG Git 경로 150/150 확인, 단계별 증거 Git blob SHA 150/150 대응, 각 단계 최신 STATE/REPORT/SUMMARY SHA 33/33 일치, 통합 원장 ID·경로·기존 SHA256 불일치 0. 다만 이번 독립 감사가 PNG 원본 150개를 전량 재디코딩하거나 SHA256/CRC/픽셀 측정을 새로 수행한 것은 아니다.

**완료 판정의 범위:** 사용자가 선택한 바닐라 **150개 텍스처의 소스 연구 완료**다. 게임의 블록 PNG **1,111개 전체 연구**나 가구 모드 분석, 실제 게임 내 렌더링, 모델링 가이드 완성을 뜻하지 않는다. **공식 압축 client.jar 인증과 인게임 렌더/런타임 검증은 사용자 지시로 필수 조건에서 제외**되었으며, 이 두 검증을 실제로 성공했다고 주장하지 않는다. 1-1-C에서 보류했던 석재·벽돌 17개와 잎·식생 8개의 애니메이션 소스 검사를 2026-11-19에 완료했다. 고정 표본 25종의 PNG 프레임 애니메이션은 0/25이며 해당 연구 보류는 해제됐다. [1-1 현황](vanilla_texture_1-1/CURRENT_STATUS.md)

## 다음 실제 연구

**1-2 바닐라 가구형 모델 JSON·UV·블록상태 분석을 계속한다.** 현재까지 수행된 v34~v38의 P1 544후보와 선택 leaf 28개의 근거를 먼저 확인하고, 남은 검증 항목을 구분할 것. 이미 수행한 1-1 연구 결과를 새 실적으로 중복 계산하거나, 완료된 150개 소스 항목을 다시 미완료로 표시하지 말 것.

- [새 채팅 시작 지시서](NEW_CHAT_START.md)
- [기존 상세 진행 기록](../PROGRESS.md) 및 [전역 인수인계](../HANDOFF.md)
- [전체 상태 JSON](../handoff/STATE.json)

## 기록 관리 원칙

- 현재 체크포인트: **v43**(1-2 신규 연구), 1-1 마지막 독립 검수: **2026-11-14**. v43은 1-2의 별도 신규 원본 증거를 반영했으며 1-1 완료수와 전역 완료 세부과제 수를 변경하지 않는다.
- v39(10/11 통합), v40(11/11 최초 통합), v41(석재 R017 갱신), v42(목재 집계 정정 및 150종 종료)는 **서로 다른 역사적 스냅샷**으로 보존한다.
- 연구 문서에 남은 v38~v41 당시의 '최신', 초기 미완료 체크박스, 0/5·132/150 같은 숫자를 현재 진행률로 취급하지 않는다. 충돌이 생기면 최신 [STATE.json](../handoff/STATE.json)과 본 문서를 먼저 확인한다.
