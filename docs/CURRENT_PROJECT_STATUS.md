# Minecraft Furniture Style Research — 현재 프로젝트 진행도

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

**완료 판정의 범위:** 사용자가 선택한 바닐라 **150개 텍스처의 소스 연구 완료**다. 게임의 블록 PNG **1,111개 전체 연구**나 가구 모드 분석, 실제 게임 내 렌더링, 모델링 가이드 완성을 뜻하지 않는다. **공식 압축 client.jar 인증과 인게임 렌더/런타임 검증은 사용자 지시로 필수 조건에서 제외**되었으며, 이 두 검증을 실제로 성공했다고 주장하지 않는다. 애니메이션 소스 연구는 9개 재질에서 재개, 2개(1-1-02/1-1-10)에서 보류다.

## 다음 실제 연구

**1-2 바닐라 가구형 모델 JSON·UV·블록상태 분석을 계속한다.** 현재까지 수행된 v34~v38의 P1 544후보와 선택 leaf 28개의 근거를 먼저 확인하고, 남은 검증 항목을 구분할 것. 이미 수행한 1-1 연구 결과를 새 실적으로 중복 계산하거나, 완료된 150개 소스 항목을 다시 미완료로 표시하지 말 것.

- [새 채팅 시작 지시서](NEW_CHAT_START.md)
- [기존 상세 진행 기록](../PROGRESS.md) 및 [전역 인수인계](../HANDOFF.md)
- [전체 상태 JSON](../handoff/STATE.json)

## 기록 관리 원칙

- 현재 체크포인트: **v43**(1-2 신규 연구), 1-1 마지막 독립 검수: **2026-11-14**. v43은 1-2의 별도 신규 원본 증거를 반영했으며 1-1 완료수와 전역 완료 세부과제 수를 변경하지 않는다.
- v39(10/11 통합), v40(11/11 최초 통합), v41(석재 R017 갱신), v42(목재 집계 정정 및 150종 종료)는 **서로 다른 역사적 스냅샷**으로 보존한다.
- 연구 문서에 남은 v38~v41 당시의 '최신', 초기 미완료 체크박스, 0/5·132/150 같은 숫자를 현재 진행률로 취급하지 않는다. 충돌이 생기면 최신 [STATE.json](../handoff/STATE.json)과 본 문서를 먼저 확인한다.
