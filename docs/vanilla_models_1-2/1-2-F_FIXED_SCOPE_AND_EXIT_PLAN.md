# 1-2-F — 가구 모델링 관점 유형화: 고정 범위·유한 실행계획·종료 계약

**2026-11-16 KST · 원본 Minecraft Java Edition 1.21.11 (사용자 제공 추출 자산) · 작성 기준 main `16ecd4e5a0c353ec077238909cc546ac158ed97f`.**

> 이 문서는 E4 `E_NEXT.md`의 요청에 따른 **착수 전 범위·작업계획**이다. 목록/SHA 교차대조와 6개 회차 배정만 수행했다. **개별 F 원형·스타일 판독은 0/2,390**. E의 소스 예외 완료를 실제 게임 renderer 검증으로 확대 해석하지 않는다.

## 1. 기존 계획과 목표
- 상위 [WORK_PLAN.md](WORK_PLAN.md)의 1-2-F 명세를 따른다: **'가구 모델링 관점 유형화 — 큐브 대 얇은 평면, 입체 디테일 vs 텍스처 디테일, 면 수/요소 수/비례 분포를 관찰값으로 비교'**. 의무 결과물은 `VANILLA_GEOMETRY_ARCHETYPES.md` 및 `STYLE_OBSERVATIONS.csv`.
- 실제 목표: 바닐라 블록 모델에서 **Minecraft 느낌을 유지하는 가구 제작에 재사용 가능한 구조적·시각적 표현 패턴**을 원본 근거와 함께 유형화하고, '어디까지 원본으로 확인했는지'를 증거 등급으로 명확히 구분한다.
- 선행 B(부모/기하), C(UV/텍스처/PNG), D(blockstate 조건·상태·부품), E(일반 기하 없는 예외·미인증 renderer)를 **서로 다른 증거 층**으로 연결한다. 유형화를 바탕으로 최종 제작 가이드를 제안하지만 **가구 3D 모델, 모드, 실제 게임 실행/변환 파일은 만들지 않는다**(그 일은 상위 후속 단계와 별도 구현 작업).

## 2. 고정 모집단·기준 문서 (중복 금지)
| 분류 | 고정 수량 | 출처·의미 |
|---|---:|---|
| C 전체 block 모델 원본 경로 | **2,390** | `C_SCOPE_2390_FINAL_STATUS.csv`; 고유 `(asset_type, full_source_path, git_blob_sha)` |
| P1 / P2 / P3 | **544 / 1,039 / 807** | 2,390개의 우선순위 **분할**, 신규 모델이 아니다 |
| 일반 기하 C 직접 모델 | **2,304** | 실제 C 원장 face/UV·B 모델 구조 기반 통계만 산출 |
| E 특수 표현 원본 예외 | **86** | **같은 2,390개 안에 포함**, 일반 기하 요소·face 분모에 억지 포함 금지 |
| D blockstate 선택에 직접 등장한 고유 모델 | **2,136** | D Entry1~6 연결원장 고유 경로·SHA 합집합 |
| D 모델 선택에 직접 등장하지 않은 경로 | **254** | **분모 포함**; 부모·인벤토리·템플릿 등 역할은 추후 F 소스 확인 전 미확정 |
| E 86 중 D 직접 선택 / 미선택 템플릿 | **84 / 2** | 미선택 `block.json`과 `thin_block.json`도 F 포함 |

- 단일 모집단 기준: [`F_FIXED_SCOPE_2390.csv`](../../research/vanilla_models/phase_1-2-F/F_FIXED_SCOPE_2390.csv); 원본 SHA·중복·소관/D 합집합 검사: [`F_SCOPE_PREP_AUDIT.json`](../../research/vanilla_models/phase_1-2-F/F_SCOPE_PREP_AUDIT.json). 이를 F의 고정 단일 기준으로 사용한다. 배정 전 모델 **신원**은 C·D·E 선행 원장과 2,390/2,390 대조했다. **F 새로운 원본 직접 판독은 아직 0**이다.
- C 범위 원장 blob `0950bae4293eaaf455f91073981c30bc7e563b05`; B 범위 `1c4a44bce97603215e8026a0bf5a2f61f2075756`; E 고정 86 `6e6c5c7e92de8a7006f125697573e9202b50a75e`. D 7개 분할 교차표 SHA는 사전 감사 JSON에 등록한다.
- **C 고정 선행 근거**: 일반 적용 face 23,090 = face-PNG 연결 21,590 + 템플릿 미바인딩 1,500, 고유 face-PNG 1,073개. E particle PNG 70개는 다른 모집단이며 C의 1,073개에 단순 가산하지 않는다. F에서 이들을 신규 face/PNG 실적으로 재계산 금지.
- 기존 v69 P1 544×393 / review544×70, 1-1 승인150/150, B/C/D/E 완료 상태, E renderer 미확인86, heavy_core 정정6면, 상위 1-1~1-5 완료1/5는 보존.

## 3. 정확한 6회차 Entry 배정 (F 자체의 작업 슬롯)
| 회차 | 대상 | 새 대상 수 | 누적 | 주된 작업 |
|---|---|---:|---:|---|
| **Entry1** | P1/P2/P3에서 원본 경로 정렬 기준 고르게 선정 각50개 | **150** | 150 | 분류 체계·비율 측정·기하/텍스처 표현 비교를 3개 우선순위에서 시험, 일치도 점검 |
| **Entry2** | Entry1 이후 P1 나머지 | **494** | 644 | P1의 복잡·가구와 가까운 구조, 원형/반복 변형/템플릿 분리 |
| **Entry3** | Entry1 이후 P2 중 정렬상 앞쪽 | **495** | 1,139 | 일반 재료·블록 구조의 기하·UV·연결 유형화 |
| **Entry4** | Entry1 이후 P2의 나머지 | **494** | 1,633 | P2 완료, 공통 템플릿/동형 모델의 근거 분리와 교차 비교 |
| **Entry5** | Entry1 이후 P3 앞쪽 | **379** | 2,012 | P3 일반화 모델/예외/스타일 대비 |
| **Entry6** | Entry1 이후 P3 나머지 | **378** | **2,390** | P3 종료 + 전체 2,390 독립 재분류·증거/원격 종료감사 |
| **합계** | 중복 없이 전수 배정 | **2,390** | | **Entry7 자동 생성 없음** |

- Entry1 표본은 각 우선순위의 경로 오름차순 정렬 배열 크기 `N`에서 `k=0..49`에 대해 `floor((k+0.5)*N/50)` 인덱스를 선택한다. **알파벳 분산을 위한 결정적 50개**이며 실제 기하 유형의 대표성을 미리 인증한 표본이 아니다. 이후 조사 때 추가 원형 비교는 배정 회차 내에서 수행하되 분모·Entry 이동 금지.
- Entry2~6 잔여 P1 494, P2 989(앞 495·뒤 494), P3 757(앞 379·뒤 378). 구간/경로는 `entry1`~`entry6/F_ENTRY{n}_QUEUE_{count}.csv`에 Git blob SHA와 함께 **정확히 고정**했다.
- 기존 E 예외의 분포: Entry1 **8**, Entry2 **47**, Entry3 **0**, Entry4 **0**, Entry5 **24**, Entry6 **7**; 전체 **86**. 이 배분은 E 렌더 확정 여부를 뜻하지 않는다.

## 4. 실제 F 처리 프로토콜 — 한 모델마다 (F1~F4)
1. **신원·근거 매칭:** 현재 원본 블록 모델 JSON 직접 재조회·SHA 확인, `(asset_type, path, sha)`로 B/C/D/E 자료 연결. 원본 JSON을 열지 않았으면 `source_f_checked=false`, 최종 원형 확정 불가. P1 선행 분석 자료는 **기존 증거로만** 기록한다.
2. **기하 원형:** 부모/leaf 기하 제공자, 적용 `elements` 개수, 원본 face/결합 후 참조 face, 요소별 `from/to`(0~16 밖·역방향 보존), 직교 큐브·얇은 평면(0 두께 vs 작은 두께)·다중 cuboid·회전 요소·프레임·혼합 요소 여부를 **복수 태그**로 측정. 전체 모델의 한 개 태그 독점 분류 강제 금지. 부재/미확정 모델의 기하 0과 유사하게 처리하지 않는다.
3. **시각·비례:** 바운딩박스 각 변·요소 두께 분포·3D 요소가 표현하는 요철 정도(관찰 근거)와 PNG 텍스처·페이스 표현(이미지/UV의 실제 출처)을 비교. '텍스처가 디테일을 담당한다'는 판단은 **원본 PNG 픽셀 또는 검증된 미리보기의 시각 관찰**이 있어야 하고, 단순 파일명·컬러·면 수만으로 결론 금지. 직접 PNG 관찰, C 기존 RGBA 자료 재참조, 가설을 독립 등급으로 분리.
4. **조립/활용:** D `variants/multipart`, (x/y/uvlock) **원본 값과 키 존재 여부**, 가중 대안 vs 다수 부품 동시 적용, 방향·상태별 조립 조건을 **참조되는 모델에 한해** 연결. D 비선택 254개는 `NOT_DIRECT_D_SELECTED`로 표시하고 템플릿/부모/인벤토리 모델 가능성을 **검사 전 단정 금지**. 가구용 시트·다리·프레임·판·문·선반 등 **재사용 패턴 후보**와 신뢰도를 원본 근거로 기록하되, 모델링 실물 설계를 완성으로 가장하지 않는다.
5. **예외 처리:** E 86개는 `E_SOURCE_EXCEPTION`이라는 **원본 역할**을 보존하고 일반 입체 유형 통계에서 분리; 실제 renderer의 기하·텍스처 표현은 `UNVERIFIED_RUNTIME_RENDERER` 그대로. 가구를 뜻하는 단어가 모델명에 있다고 실제 인게임 보이는 가구를 확정하지 않는다.

## 5. 개별 모델의 최소 산출 필드 (기계 판독)
`STYLE_OBSERVATIONS.csv`는 **2,390모델 당 정확히 1행**(+ 필요 시 요소·특성·패턴 상세 보조 원장)을 고정한다. 중요한 열은 다음과 같다.
- key: `asset_type, source_path, git_blob_sha, minecraft_version, priority, F_entry, original_f_source_checked`
- evidence: `B_geometry_evidence, C_UV_texture_evidence, D_blockstate_evidence, E_exception_evidence, source_reference_grade, visual_evidence_type, provenance_paths_sha, unresolved_reason`
- geometry: `provider_source_sha, leaf_vs_inherited, resolved_element_count, applied_face_count_prior, element_thickness_min, flat_zero_thickness_count, rotated_element_count, bbox_from_to, geometry_tags`
- visual: `texture_detail_observed, material_appearance_candidates, UV_explicit_implicit, texture_binding_path_sha, image_or_preview_reference, texture_vs_geometry_explanation`
- assembly/modeling: `D_directly_selected, state_assembly_modes, rotation_x_y_uvlock_source_keys, reusable_furniture_pattern_candidate, modeling_limits, confidence, status`

상세 타입·판정 조건은 [`1-2-F_TAXONOMY_SCHEMA.md`](1-2-F_TAXONOMY_SCHEMA.md), 자동검수 가능 게이트는 [`1-2-F_ACCEPTANCE_CONTRACT.json`](1-2-F_ACCEPTANCE_CONTRACT.json)에 고정한다. **무증거 확정명은 기입하지 않는다.**

## 6. 각 Entry 산출물·반복 방지
- `research/vanilla_models/phase_1-2-F/entryN/`: `F_ENTRYN_QUEUE_*.csv`(준비 완료), 실제 착수 후 `F_MODEL_SOURCE_STATUS.csv`, `STYLE_OBSERVATIONS.csv`, `F_GEOMETRY_FEATURES.csv`, `F_TEXTURE_VISUAL_EVIDENCE.csv`, `F_ASSEMBLY_LINKS.csv`, `F_ARCHETYPE_RULES.json`, `F_UNRESOLVED.csv`, `F_ENTRYN_REPORT.md`, `F_ENTRYN_INDEPENDENT_AUDIT.json`, `F_ENTRYN_REMOTE_READBACK.json`, `F_NEXT.md` 작성.
- 원형의 기하/UV 직접 관찰과 색상·목재·상태 leaf의 **반복 구조 재사용**은 구분한다. 중복 leaf는 본인의 source SHA와 부모/텍스처 override를 반드시 검증하고, 원형 측정 반복을 신규 성과로 세지 않는다.
- Entry1은 150개 파일의 실제 F 분류가 끝나야 완료이며, **queue 150행을 만들어 놓은 사실은 진척도 150/2,390으로 계산하지 않는다**. 각 Entry는 배정 수를 모두 처리한 뒤 독립 감사·원격 검사로 종료한다. 단일 대화에서 미완료면 정확한 행 경계·부분 실적·미확인만 기재한다.

## 7. 종료 게이트 F1~F5
| 게이트 | 완료 조건 | 실패/차단 |
|---|---|---|
| **F1 범위·선행** | 고정 2,390 단일 path/SHA와 P1/2/3(544/1,039/807), C 직접2,304/E86, D 직접2,136/미직접254 중복·누락0. A~E SHA와 직접조사 경계 보존 | path/SHA·우선순위 불일치 미해결 시 PASS 금지 |
| **F2 기하·비례** | 일반 기하 모델 2,304개 전체에 B 원본 기하·상속·요소/face·bbox/두께/회전의 출처 연결, 다중 태그·비교 분포·형태별 대표 근거; E86은 별도 소스 유형화 | 무근거 크기/기하/요소 추정은 원형 통계에서 제외·정확히 미해결 표시 |
| **F3 시각·텍스처** | C face-UV/texture/PNG provenance와 '3D 디테일 vs 텍스처 디테일' **시각 증거/미확인 상태**를 모든 모델에 기록; 대표 원형마다 실제 관찰 근거·출처·한계 | 원본 PNG 시각 확인 없이 '텍스처가 담당' 확정 금지 |
| **F4 조립·가구 활용** | D 직접 모델2,136과 그 밖254 구별, state/rotation/uvlock/다중부품 근거 연결, 설계 패턴 후보 및 **원본 근거와 미확인 범위**를 정확히 표시; E86 renderer 미확인 유지 | furniture object identity·인게임 기능·renderer 실제 구현을 추정으로 확정 금지 |
| **F5 전체 독립·원격** | Entry별 원본 모델/분류/분포 재계산, `STYLE_OBSERVATIONS.csv` 정확2,390행·유일키·근거 링크, `VANILLA_GEOMETRY_ARCHETYPES.md` 대표 증거, 모든 unresolved 분류/담당, 원본 A/B/C/D/E·v69 변경0, GitHub SHA·행수·본문 readback | 불명확한 원형/근거 누락·미수행 검사를 PASS로 위장 금지 |

- Entry6에서 F1~F5 **전부 PASS**일 때 `F_COMPLETE_SOURCE_STYLE_TAXONOMY_SCOPE`; 아니면 `F_BLOCKED_AT_ENTRY6`로 종료, 미해결 출처·사유 보존하고 **ENTRY7 자동 생성 금지**. 미확인 실제 renderer·실게임 UV는 E 책임으로 유지하며, 원본 정적 근거의 범위 내에서만 F 패스를 평가한다.
- **다음 1-2-G**는 F 완료 이후 **A~F 전체 소스 출처의 독립 정합성·인수인계** 책임; F 종료만으로 상위 1-2 전체 완료 아님.

## 8. 지금 준비 상태와 Entry1 착수점
- F 고정 경로/SHA/소관 대조 **2,390/2,390**, E 별도86/86, D 고유 직접 선택2,136/2,136. Entry1~6 작업 대기열과 감사 JSON 생성.
- 실제 F 모델 원형·시각 관찰/분류 **0/2,390**, 최초 모델 JSON 재열람 **0/2,390**, 스타일 확정 **0**. 이전 B/C/D/E 실적을 F 진행률로 전환하지 않는다.
- **다음 실행**: [`entry1/F_ENTRY1_PREP.md`](../../research/vanilla_models/phase_1-2-F/entry1/F_ENTRY1_PREP.md)에서 150개 SHA 고정 대상부터 원본 모델·B/C/D/E 결합을 실제 읽고, 타입/비례/시각 근거를 작성한다.
