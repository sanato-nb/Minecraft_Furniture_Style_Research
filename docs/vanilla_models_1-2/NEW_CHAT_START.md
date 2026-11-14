# 1-2 새 채팅 인수인계·시작 프롬프트 (v43 이후)

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
