# 1-2 바닐라 3D 모델·UV·블록상태 — 최신 인수인계 (v48, 기존 v43~v47 기록 보존)

> **현행 v48 · 2026-11-14:** [원본 모델/상속·UV·상태 1-2-A 연구 보고서](../../research/vanilla_models/v48/REPORT.md) · [P1 544행 최신 검증 원장](../../research/vanilla_models/v48/01_P1_544_EVIDENCE_LEDGER.csv) · [신규 정확한 SHA 연결 36건](../../research/vanilla_models/v48/02_NEW_P1_36_TYPED_SOURCE_LINKS.csv) · [다음 채팅 인수인계](../../research/vanilla_models/v48/NEXT_CHAT_HANDOFF.md). v47 135 → v48 **171개 P1 모델 경로 SHA 연결**, 검사된 근거에서 **373개 미연결**(미연구 확정 아님). 새 원본 모델 경로 36개 직접 조회/parent 20개 재검수; 원본 own element14/explicit UV faces68(그중 v38 기존 원형 3요소/18면 별도 재검증). 3가지 블록상태 원문 multipart 100규칙·파생 static320조합·1920 모델 적용. 별도 6개 블록상태 9 variants. PNG 실화소 신규 0, 런타임 검증 미실시. **1-2-A와 전체 1-2 미완료, 완료율 미산정, 1-1 승인150/150과 상위 과제1/5 완료 유지.** 아래 v47·v46 '현재'는 이전 체크포인트의 기록임.


> **현행 v47 · 2026-11-14:** [실제 근거 조사 보고서](../../research/vanilla_models/v47/REPORT.md) · [P1 544개 모델별 최신 검증 원장](../../research/vanilla_models/v47/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인계](../../research/vanilla_models/v47/NEXT_CHAT_HANDOFF.md). v46 **124 → v47 135** 모델 source PATH+SHA 연결(신규 11 원본 모델 JSON 직접 조사), **409개는 검사 근거에서 미연결**이며 미연구 확정 아님. 역사 SQLite v5~v8 **4 DB 원본 테이블/행 실조사**(5/10/16/20테이블)·생성 스크립트 4개 확인, 이전 연결 53개 재검증·역사 중복 신규 0. 화분 템플릿 3모델+비콘의 원본 26요소/100명시 UV 선언면, bamboo_shelf 7 leaf 공통 v38 부모 원형 재사용, blockstates multipart 24개/파생 32조합. 실제 PNG 화소 재검증 신규 0. 1-2-A·1-2 미완료, 완료 퍼센트 미산정. v42 1-1 완료 및 상위 **1/5 완료 상태 유지**. 이전 문구의 v46/v45 '최신'은 과거 기록.


> **현행 v46 · 2026-11-14:** [1-2-A 실제 연구 보고서](../../research/vanilla_models/v46/REPORT.md) · [P1 544 모델별 근거원장](../../research/vanilla_models/v46/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [다음 채팅 전용 인계](../../research/vanilla_models/v46/NEXT_CHAT_HANDOFF.md). v45의 기존 119 SHA 연결 모델 **경로**에서 9개 원본 JSON 직접 검사(기존 4 재검증·새 5 경로 추가)하여 **124/544 SHA 연결**, 검토 근거에서 미연결 **420개**. 역사 MD/JSON 49개 전체 원문 열람 및 SHA/경로/모델명 참조 검수, 최근 v35~v43 CSV 30개 재대조, SHA 동일해도 서로 다른 모델 경로 2그룹/7경로 확인. 모든 파일명을 같은 기하 구조로 보지 말고 `(asset_type, full_source_path, git_blob_sha)`를 유지. 1-2-A 및 1-2 **진행 중, 완료율 미산정**, 1-1 v42 150/150 완료 및 상위 5과제 중 **1/5 완료 유지**. 아래 이전 버전의 '최신' 안내는 당시 스냅샷.


> **현행 v45 연구 갱신 · 2026-11-14:** [1-2-A 실제 검증 보고서](../../research/vanilla_models/v45/REPORT.md) · [544행 검증 상태 원장](../../research/vanilla_models/v45/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [9개 추가 SHA 연결 증거](../../research/vanilla_models/v45/02_NEW_EVIDENCE_LINKS_9.csv). v44 연결 110 + 과거 v30 중복 제거 후 증거 회수 2 + 새로운 acacia_shelf 7 leaf 원본 확인 = **119개 SHA 연결**, **425개는 조사한 근거에서만 미연결**. v44 제외 역사 CSV **86개 SHA 필드 조사**; v38 부모 7템플릿은 재사용, blockstate 원본 24개 multipart/파생 32조합. 1-2-A 전체 v5~v43 서술형/JSON 대조, PNG·특수 렌더 검증 **남아 있으며 전체 1-2 완료율 미산정**. v42 1-1 150/150 완료, 상위 **1/5 유지**. 아래 v44/v43 '최신' 표현은 역사적 스냅샷.


> **[최신 1-2-A v44 대조 결과](../../research/vanilla_models/v44/REPORT.md):** [544개 SHA 근거 원장](../../research/vanilla_models/v44/01_P1_544_SHA_CROSSWALK.csv), [176개 연결 기록](../../research/vanilla_models/v44/02_SOURCE_EVIDENCE_LINKS_176.csv), [오탐 정정](../../research/vanilla_models/v44/04_SHA_TYPE_ISSUES.csv). 선택 근거 110개 고유 모델 연결·434개 미연결, 전체 v5~v43 역사 증거 조사와 P1 심층 검사 **진행 중**. 아래 문서는 v43 시점 기초 상태를 보존한다.


> 작성일 2026-11-14 KST · GitHub HEAD `937224f328ae85060e7e5eb3140bbffc299cb151`의 기초 연구 자료를 읽어 **기존 자료를 정리한 문서**. 새 모델·PNG 실측, 새 리비전 발행 또는 전체 1-2 완료 판정을 수행한 문서가 아니다. **항상 [전역 최신 STATE](../../handoff/STATE.json)에서 현재 체크포인트를 다시 확인**한다.

## 목적과 현재 판정

Minecraft Java 1.21.11 **모델 JSON·상속 geometry·textures/UV·blockstates·정적 표현 및 엔진 특수 렌더 예외**를 분석해 바닐라 가구형 물체의 실루엣, 비례, 표면·디테일 표현 규칙의 근거를 확보한다.

- 상위 1단계 **1-1 바닐라 재질·텍스처의 고정 150/150 소스 범위는 v42에서 완료**. [1-1 현재 정본](../vanilla_texture_1-1/CURRENT_STATUS.md). 1-2는 **진행 중·종료 미판정**. 상위 세부과제 완료 **1/5** 그대로.
- **v34 원본 목록:** `1.21.11/assets/minecraft/models/block/` **2,390개 JSON**, `blockstates/` **1,168개 JSON**, `textures/block/` **1,111개 PNG**의 *경로/Git blob SHA 인벤토리*. 이건 **내용 정밀분석 완료율이 아니다**.
- **P1: 파일명 기반 가구 연관 우선후보 544개(169 수납·선반 / 32 제작·작업 / 227 조명·장식 막대 / 116 침대·표지판·실내 장식)**. 나머지 P2 **1,039**, P3 **807**. P1·P2·P3는 휴리스틱 초기 분류이며 연구 완료 여부가 아니다.
- **v35~v43 선택 회차에서 직접 source leaf 검사한 서로 다른 모델은 32개**(v35 15 + v36 6 + v38 7 + v43 4). 단, **v5~v34 역사 자료 전부와 중복/완료 상태 대조하지 않음**. 따라서 32/544나 83/544를 진짜 전체 진행률로 표현하면 안 된다.
- v36 선택 과거 증거 CSV 18종에서 **83개 SHA 일치 기록**을 찾았고, **446개 후보는 그 선택 증거 범위에서만 미매칭**. 미매칭 = 한 번도 연구하지 않았다는 증거가 아님.
- **v43 crafter 연구:** leaf 4개 원본 JSON·SHA, 고유 원형 큐브 1요소/6 선언면, 4 leaf 상속 **24 face×material**, 원본 `orientation 12 × crafting 2 × triggered 2`의 blockstate 규칙 **48개**, 파생 face 적용 288건. `crafting` leaf 2종의 *소스상* 최종 texture 바인딩이 같음(게임 화면 동일성 검증 아님). 과거 v36의 SHA basename 충돌 2건은 **blockstate vs model 경로 타입의 오탐**으로 정정.
- 공식 Mojang 배포 압축 JAR 인증과 인게임 렌더/런타임 검증은 사용자 결정으로 **필수 완료조건 제외**되지만 **실제로 검증 성공한 것은 아니다**. animation asset 연구는 단계별 최신 사용자 범위를 따르고 무분별한 동작 재현을 하지 않는다.

## P1 연구 대상 분류

| 우선분류 | 원본 모델 JSON 파일 수 | 대표 주제 |
|---|---:|---|
| 01 수납·선반·책장·용기 | 169 | shelf, chiseled_bookshelf, barrel, composter, shulker 등 |
| 02 제작·작업·가공 설비 | 32 | crafter, crafting_table 등 |
| 03 조명·촛불·장식 막대 | 227 | lantern, candle, lightning_rod 등 |
| 04 침대·표지판·실내 장식 | 116 | bed, hanging_sign, flower_pot 등 |
| **P1 계** | **544** | **우선 조사 큐 (완료 분모 아님)** |
| P2 건축·연결·기계·템플릿 | 1,039 | 구조 확장 및 예외 자료 |
| P3 자연·기본 재료·기타 | 807 | 비교 자료 및 재분류 대상 |
| **전체** | **2,390** | **파일명 1차 분류의 모든 block 모델 JSON** |

[전체 2,390종 목록과 초기 분류](../VANILLA_STATIC_MODELS_FULL_STUDY_LIST_v34.md) · [P1 544개 과거 근거 교차표](../../research/vanilla_models/v36/01_p1_544_historical_sha_evidence_crosswalk.csv)

## 기존 연구를 이어받는 방법

| 기존 연구 | 이미 입증된 내용과 단위 | 필요한 구분 |
|---|---|---|
| v25~v30 | 기본·도구·문·계단 등 요소/면·PNG 원본 연결 | 서로 다른 블록·모델·면 숫자 혼합 금지 |
| v31 | 조각된 책장 256정적 상태, 양조기 8정적 조건 · multipart | 모델 적용 횟수 ≠ 새로운 모델 수 |
| v32~v33 | 화분·호퍼·가마솥·퇴비통의 소스·암시 UV 분석 | 암시 UV 공식 추론 ≠ 엔진 인증 |
| v34 | 전체 인벤토리 2,390 / 1,168 / 1,111 및 랜턴·촛불·막대 | 파일 존재 ≠ 모델 깊이 분석 |
| v35 | 종·케이크·벌통/벌집 15 leaf 및 원본 블록상태 | 첫 선택 회차이며 전체 P1 종료 아님 |
| v36 | 화로·용광로·훈연기 6 leaf/24상태, 과거 18 CSV의 SHA 교차 | v43에서 SHA 경로타입 오탐 2건 교정 |
| v37 | 기존 원본 선택 이미지/UV 텍셀 추가 검증 | 신규 leaf 0건 |
| v38 | 참나무 선반 7 leaf·7 template, 32개 상태·38명시 UV면 | 이미 완료된 실적 재가산 금지 |
| **v43** | **crafter 4 leaf, 48상태, 24 face×material**, 충돌 오탐 2건 교정 | 최신 선택 누적 32 leaf, 전체 역사 대조 미완료 |

## 다음 작업과 완료 기준

[1-2 상세 단계별 조사 계획](WORK_PLAN.md) · [새 채팅 시작·인수인계](NEW_CHAT_START.md).

**우선 해야 할 일:** (1) v5~v43의 모든 역사 연구 파일을 **asset type + 전체 경로 + Git blob SHA** 기준으로 교차 대조 → (2) P1 544개를 기획·원본 확인·부모/UV/상태·특수 렌더 예외·재현 검증 등 **독립 근거 상태로 분류** → (3) 새 대상의 소스 분석을 수행 → (4) 검수 완료 조건과 연구 목적에 따른 P2/P3 검토 범위를 확정.

**현재 확정 불가능한 것:** 544개 중 전체 중복 제거된 실제 심층 분석 완료 수, 전체 1-2 완료율 %, 실제 게임 렌더 정밀 재현. 근거 없이 1-2 완료나 완료율을 선언하지 말 것.
