> **최신 v57 (2026-11-14):** [16개 P1 원본 모델 기하·UV·blockstates·PNG 검증](../../research/vanilla_models/v57/REPORT.md) · [P1 544행×225열 원장](../../research/vanilla_models/v57/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../../research/vanilla_models/v57/NEXT_CHAT_HANDOFF.md). v56 544×209열(과거 v55 198열 포함) 모두 보존. 기존 369 중 16개 모델 직접 소스 재검증(자체33요소/156면, 상속적용44요소/219면, 원본 명시UV95/계산 후보124), 원본 blockstates13(variants37/multipart68), PNG4경로 독립 Pillow 1,536소스 RGBA 픽셀, 석재 절단기 원본 명시UV 2면 소스196픽셀. 외부 Java 디컴파일의 셜커/해골 구조는 **보조 근거**로만 유지하며 런타임 검증 아님. v56 코호트 49경로 실적 재집계 금지. **1-1 승인150/150·상위1/5 완료 유지, 1-2-A·1-2 계속 진행·전체 완료율 미산정.** 아래 v56 이하 역사 기록.

# 1-2 새 채팅 인수인계·시작 프롬프트 (v43 이후)

> **최신 v56 (2026-11-14):** [원본 PNG·UV 실측 연구 보고서](../../research/vanilla_models/v56/REPORT.md) · [P1 전체 544행 209열 원장](../../research/vanilla_models/v56/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../../research/vanilla_models/v56/NEXT_CHAT_HANDOFF.md). v53 신규175 모델의 **남은 37개 텍스처 경로 원본 바이너리·Git SHA·PNG CRC·zlib Adler·RGBA 16×16 전픽셀 검사 완료**. 새 명시 UV face **2,926면**, 반복 포함 소스 픽셀 **21,416건**. v54~v56 누적 **해결된 PNG 49/49경로, 3,393면, 51,228회 반복 RGBA 관측**, 명시 UV3225·계산 후보168 구분. 이는 소스 PNG 측정이며 **P1 544개 전체 형상·UV·렌더러 완료가 아니다**. 1-1 150/150 완료, 상위1/5 완료, 1-2-A/1-2 진행 중·완료율 미산정. 아래 v55 이하는 기존 역사 기록.


> **최신 v55 (2026-11-14):** [원본 PNG·UV 검증 보고서](../../research/vanilla_models/v55/REPORT.md) · [P1 544행·198열 최신 증거 원장](../../research/vanilla_models/v55/07_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../../research/vanilla_models/v55/NEXT_CHAT_HANDOFF.md). P1 모델 원본 path+SHA **544/544 유지**. 원본 PNG 바이너리/실제 SHA/Pillow RGBA **9개 추가**(v53+v55 확인 합계13개), v55 신규 UV 대응 면 **241건**(원본 명시73 + 케이크 원본 미기재 UV의 **기하 계산 후보168**) · 원본 PNG/UV 영역21종 · 반복 소스 텍셀28,076회. v54부터 누적 **467면/29,812회**, v53 신규175 모델 참조 PNG **49개 경로 중 12경로만 면 소스 픽셀 대조**. 케이크 실제 PNG 3개 alpha 불투명 마스크가 계산 후보 사각형과 일치하나 **게임 엔진 UV 공식/렌더 출력 인증은 아님**. 1-2-A/1-2 미완료·실질 완료율 미산정, 1-1 150/150 완료·상위 1/5 유지. 아래 v54 및 그 이전은 과거 기록.


> **최신 v54 (2026-11-14):** [원본 블록상태·UV 실측 보고서](../../research/vanilla_models/v54/REPORT.md) · [P1 전체544행 원장](../../research/vanilla_models/v54/01_P1_544_EVIDENCE_LEDGER.csv) · [v54 다음 채팅 인수인계](../../research/vanilla_models/v54/NEXT_CHAT_HANDOFF.md). **P1 모델 path+SHA 544/544 유지.** v53 신규175 모델 관련 원본 블록상태 기존8 + v54 신규49 + skull/head 신규14 = **71 원본 경로**(원본 variants/apply 각239), 블록상태에서 **173/175 모델 직접 참조**, 나머지 2개는 피스톤 헤드 부모 템플릿. 피스톤 자식 face 텍스처 경로40/40 해결. 실제 PNG 3종의 원본 명시 UV 16영역, 모델별 face 226개에서 **1,736회 반복 포함 원본 RGBA 픽셀 관측**(중복 없는 텍셀 좌표298, 모두 불투명). **실게임 렌더/전체 1-2-A 완료 의미 아님. 1-1 승인150/150·상위1/5 완료 유지, 1-2-A/1-2 미완료, 실질 완료율 미산정.** 아래 v53 이하는 역사 기록.


> **최신 v53 (2026-11-14):** [원본 모델 전수 path+SHA 연구](../../research/vanilla_models/v53/REPORT.md) · [P1 544행 확장 원장](../../research/vanilla_models/v53/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅용 인수인계](../../research/vanilla_models/v53/NEXT_CHAT_HANDOFF.md). **v52 369 → v53 544/544 P1 모델 원본 경로·SHA 연결**(175개 직접 원본 JSON 새 검사; 미연결0). 신규 자체 요소4/면20(명시UV20), 부모 적용3413면(명시UV3245·암시UV168), blockstate8파일·variants58, PNG4파일 실제RGBA1024픽셀. **544는 원본 신원 연결 범위이며 전체 1-2-A 의미론 통합·기하·UV·PNG·상태·렌더러 완료율이 아니다. 1-2-A/1-2 진행 중, 1-1 승인150/150·상위1/5 완료 유지.** 아래 v52 이하 내용은 역사적 기록.


> **최신 v52 (2026-11-14):** [v52 직접 원본 연구](../../research/vanilla_models/v52/REPORT.md) · [P1 전체 544행 원장](../../research/vanilla_models/v52/01_P1_544_EVIDENCE_LEDGER.csv) · [v52 다음 채팅 인수인계](../../research/vanilla_models/v52/NEXT_CHAT_HANDOFF.md). v51 **335 → v52 369개** 모델 경로+SHA 연결(신규34, 미연결175). 신규 자체23요소/60면(모두 원본 명시 UV), 상속 적용394면(원본 명시376·암시18), blockstates9/variants43/배열 선택지103, 원본 PNG 4종 실제 RGBA1024픽셀 Git blob SHA 검증. **1-2-A/1-2 미완료·완료율 미산정; 1-1 승인150/150·상위1/5 유지.** 아래 v51 이하 '현행' 표시는 역사적 기록.


> **현행 v51 · 2026-11-14:** [1-2-A 원본 근거 보고서](../../research/vanilla_models/v51/REPORT.md) · [544개 P1 최신 검증 원장](../../research/vanilla_models/v51/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../../research/vanilla_models/v51/NEXT_CHAT_HANDOFF.md). v50 **281 → v51 335개 P1 모델 경로+SHA 직접 근거 연결**, 검사 근거에서 미연결 **209개**(미연구 확정 아님). 신규 원본 P1 JSON **54경로** (선반28, 이끼카펫5+carpet 부모1, 가마솥10, 조명10). 원본 고유 요소44/면185(명시UV8·암시UV177), 상속 적용면826(명시 출처176·암시 출처650). 원본 blockstates15 파일·variants21·multipart110 규칙, 선반 정적128조합/256모델 적용. 가마솥 템플릿 3종 177면은 원본 UV키 부재. PNG 바이너리 읽기에서 UTF-8 오류, 실제 RGBA 픽셀0·엔진 렌더0 검증. **1-2-A·1-2 미완료 및 완료율 미산정. 1-1 v42 승인150/150, 상위 5과제 1/5 완료 유지**. 아래 이전 v50 '현행'은 과거 기록.


> **현행 v50 · 2026-11-14:** [원본 P1 모델 51경로 연구 보고서](../../research/vanilla_models/v50/REPORT.md) · [P1 544행 최신 근거 원장](../../research/vanilla_models/v50/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](../../research/vanilla_models/v50/NEXT_CHAT_HANDOFF.md). v49 230 → v50 **281개 원본 모델 경로+SHA 연결**, 검사한 출처에서 **263개 미연결**(미연구 확정 아님). 새 51개 모델 원본 직접 검증 = particle-only 22 / inherited geometry 27 / own source 2. 원본 자체 5 요소/22면(명시UV16·암시UV6), 상속 적용면 561건(명시UV519/암시UV42). 원본 blockstate 35파일 및 variants74, 해당 51 모델 중 월드 상태 참조49·템플릿2. 기존 랜턴 템플릿2 SHA 재검증 실적 재사용. 새 PNG RGBA 검증0·실게임 렌더0. **1-2-A·1-2 전체 미완료, 완료율 미산정. 1-1 승인150/150 완료 및 상위 1/5 완료 상태 유지.** 아래 v49 이하 '최신/현행'은 당시 스냅샷.


> **현행 v49 · 2026-11-14:** [1-2-A 원본 검증 보고서](../../research/vanilla_models/v49/REPORT.md) · [P1 544 모델별 최신 원장](../../research/vanilla_models/v49/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인계](../../research/vanilla_models/v49/NEXT_CHAT_HANDOFF.md). v48 **171 → v49 230 SHA 연결 모델 경로**, 조사 출처에서 **314개 미연결**(미연구 확정 아님). 새 P1 source path 연결 **59** = 화분37 + 선반21 + 화분 parent1. 그중 **v47에 이미 직접 확인된 화분6개는 과거 근거 회수**, 새로운 직접 소스 연구 53개로 구분. 화분 원본 고유 30요소·106면(명시UV100/암시UV6), 상속 적용면978건; 선반 기존 7부모 원형 재사용/상속 적용면114건. 화분 original blockstate 37개 단일 variant, 선반 원본 multipart72/파생 static96조합. **새 PNG RGBA 측정 0, 인게임 검증 0, 1-2-A·1-2 전체 미완료 및 완료율 미산정**. 1-1 v42 승인150/150, 상위 5과제 중 **1/5 완료 유지**. 아래 과거 v48 이하 '현행'은 그때의 스냅샷.


> **현행 v48 · 2026-11-14:** [원본 모델/상속·UV·상태 1-2-A 연구 보고서](../../research/vanilla_models/v48/REPORT.md) · [P1 544행 최신 검증 원장](../../research/vanilla_models/v48/01_P1_544_EVIDENCE_LEDGER.csv) · [신규 정확한 SHA 연결 36건](../../research/vanilla_models/v48/02_NEW_P1_36_TYPED_SOURCE_LINKS.csv) · [다음 채팅 인수인계](../../research/vanilla_models/v48/NEXT_CHAT_HANDOFF.md). v47 135 → v48 **171개 P1 모델 경로 SHA 연결**, 검사된 근거에서 **373개 미연결**(미연구 확정 아님). 새 원본 모델 경로 36개 직접 조회/parent 20개 재검수; 원본 own element14/explicit UV faces68(그중 v38 기존 원형 3요소/18면 별도 재검증). 3가지 블록상태 원문 multipart 100규칙·파생 static320조합·1920 모델 적용. 별도 6개 블록상태 9 variants. PNG 실화소 신규 0, 런타임 검증 미실시. **1-2-A와 전체 1-2 미완료, 완료율 미산정, 1-1 승인150/150과 상위 과제1/5 완료 유지.** 아래 v47·v46 '현재'는 이전 체크포인트의 기록임.


> **현행 v47 · 2026-11-14:** [실제 근거 조사 보고서](../../research/vanilla_models/v47/REPORT.md) · [P1 544개 모델별 최신 검증 원장](../../research/vanilla_models/v47/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인계](../../research/vanilla_models/v47/NEXT_CHAT_HANDOFF.md). v46 **124 → v47 135** 모델 source PATH+SHA 연결(신규 11 원본 모델 JSON 직접 조사), **409개는 검사 근거에서 미연결**이며 미연구 확정 아님. 역사 SQLite v5~v8 **4 DB 원본 테이블/행 실조사**(5/10/16/20테이블)·생성 스크립트 4개 확인, 이전 연결 53개 재검증·역사 중복 신규 0. 화분 템플릿 3모델+비콘의 원본 26요소/100명시 UV 선언면, bamboo_shelf 7 leaf 공통 v38 부모 원형 재사용, blockstates multipart 24개/파생 32조합. 실제 PNG 화소 재검증 신규 0. 1-2-A·1-2 미완료, 완료 퍼센트 미산정. v42 1-1 완료 및 상위 **1/5 완료 상태 유지**. 이전 문구의 v46/v45 '최신'은 과거 기록.


> **현행 v46 · 2026-11-14:** [1-2-A 실제 연구 보고서](../../research/vanilla_models/v46/REPORT.md) · [P1 544 모델별 근거원장](../../research/vanilla_models/v46/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [다음 채팅 전용 인계](../../research/vanilla_models/v46/NEXT_CHAT_HANDOFF.md). v45의 기존 119 SHA 연결 모델 **경로**에서 9개 원본 JSON 직접 검사(기존 4 재검증·새 5 경로 추가)하여 **124/544 SHA 연결**, 검토 근거에서 미연결 **420개**. 역사 MD/JSON 49개 전체 원문 열람 및 SHA/경로/모델명 참조 검수, 최근 v35~v43 CSV 30개 재대조, SHA 동일해도 서로 다른 모델 경로 2그룹/7경로 확인. 모든 파일명을 같은 기하 구조로 보지 말고 `(asset_type, full_source_path, git_blob_sha)`를 유지. 1-2-A 및 1-2 **진행 중, 완료율 미산정**, 1-1 v42 150/150 완료 및 상위 5과제 중 **1/5 완료 유지**. 아래 이전 버전의 '최신' 안내는 당시 스냅샷.


> **새 채팅은 v45에서 재개 (2026-11-14):** [v45 직접 연구 보고서](../../research/vanilla_models/v45/REPORT.md) · [544행 상태 원장](../../research/vanilla_models/v45/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [실제 최신 인수인계](../../research/vanilla_models/v45/NEXT_CHAT_HANDOFF.md). 아래 v43/v44 시작문은 **과거 출발점**. 반드시 GitHub main HEAD 및 handoff/STATE.json을 재확인하고, **119 SHA 연결/425 선택 근거 미연결**, 지난 연구 CSV 86추가 검사·과거 2건 회수·신규 acacia_shelf 7 leaf 검증을 계승하라. 1-2-A·1-2 전체 계속 진행, 완료 퍼센트 미산정. 1-1 완료 및 상위 1/5 유지.


> **현행 v44 후속:** [v44 감사 보고서](../../research/vanilla_models/v44/REPORT.md)와 [P1 544개 모델별 상태](../../research/vanilla_models/v44/01_P1_544_SHA_CROSSWALK.csv)부터 읽고, **이미 대조한 17CSV/144근거·중복5/오탐2**를 신규 실적으로 반복하지 말 것. 434개는 현재 *선택한 증거에서만 미연결*, 첫 작업은 나머지 v5~v43 과거 CSV/보고서의 추가 확인. 아래 v43 시작 지시는 역사적 출발점이며 현행 v44 요약이 우선.


현재 v43의 1-2는 연구 진행 중이며 **마지막 독립 근거는 crafter 4 leaf/48 state, v36 오탐 2건 정정**이다. 자료는 [현재 상태](CURRENT_STATUS.md), [단계별 연구계획](WORK_PLAN.md)에 정리했다.

## 새 채팅에 복사할 시작 프롬프트

```text
Minecraft Furniture Style Research의 1단계 1-2(바닐라 3D 모델·기하·UV·blockstate 소스 연구)를 GitHub 최신 결과에서 실제로 이어라.
저장소: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research

가장 먼저 순서대로 실시간 확인:
1. handoff/STATE.json (current_checkpoint/02 연구상태/전체 진행도)
2. docs/vanilla_models_1-2/CURRENT_STATUS.md
3. docs/vanilla_models_1-2/WORK_PLAN.md
4. research/vanilla_models/v43/REPORT.md 및 05_v43_source_validation.json
5. docs/VANILLA_STATIC_MODELS_FULL_STUDY_LIST_v34.md, research/vanilla_models/v36/01_p1_544_historical_sha_evidence_crosswalk.csv
6. v5~최신 바닐라 모델 연구 보고서/원장 중 중복·과거검증에 필요한 직접 근거

연구 원칙:
- 1-1 재질·텍스처 150/150(전역 v42 소스 연구 완료)을 다시 신규 실적으로 올리지 마라.
- v34 모델 전체 경로 2,390개/상태1,168개/블록 PNG1,111개는 파일 목록이지 깊이 분석 완료가 아니다.
- P1 후보 544개 가운데 v35~v43 선택 회차 직접 모델 32개가 확인됐지만 v5~v34 전체 역사 대조 전이므로 이를 완료율로 쓰지 마라.
- 첫 과업은 1-2-A: v5~최신 모든 이력을 asset_type+전체 경로+SHA로 대조해 실제 직접 조사/반복/누락·오탐을 구분하는 것이다. v43에서 정정한 chiseled_bookshelf/oak_shelf 유형 오탐을 다시 만들지 마라.
- 다음엔 원형 JSON 요소/회전/상속, 명시 UV vs 암시 UV, 면 재질 슬롯, static blockstates의 원본 variant/multipart 조건과 회전·uvlock, 렌더 예외를 원본 1.21.11 파일로 직접 검사한다.
- 원본 Git SHA, 선언면 vs 파생 face 적용, static state vs 동작, 사용자 제공 추출본 vs 공식 배포 인증, 실제 관측 vs 추론을 혼동하지 마라.
- 공식 압축 JAR 인증과 실제 인게임 렌더는 사용자 승인 범위에서 필수 제외. 검증 성공이라고 표기하지 마라.
- 다른 과제인 1-3~1-5와 PZ 변환, 실제 가구 3D 제작을 섞지 않는다.
- 새 원본 증거가 실제 존재할 때에만 GitHub의 신규 연구 릴리스에 보고서+증거 CSV+SUMMARY를 저장하고, 동시 작업을 고려해 커밋 직전 HEAD를 재확인한다. v43 및 이전 연구 파일은 덮어쓰지 않는다.
- 분석이 수행되지 않은 계획 변경만으로 v44 등의 신규 연구 버전을 발행하지 마라.

지금 최신 GitHub 자료를 읽고 1-2-A 역사적 소스 중복·검증 교차부터 실제 진행해라.
```

최종 단계 완료 여부는 [WORK_PLAN.md](WORK_PLAN.md)의 1-2-G 기준으로 판단한다. 이전 1-2 연구 실적을 새로 수행한 것처럼 보고하지 말 것.
