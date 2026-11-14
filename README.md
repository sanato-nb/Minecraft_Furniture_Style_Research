# Minecraft Furniture Style Research

> **최신 v54 (2026-11-14):** [원본 블록상태·UV 실측 보고서](research/vanilla_models/v54/REPORT.md) · [P1 전체544행 원장](research/vanilla_models/v54/01_P1_544_EVIDENCE_LEDGER.csv) · [v54 다음 채팅 인수인계](research/vanilla_models/v54/NEXT_CHAT_HANDOFF.md). **P1 모델 path+SHA 544/544 유지.** v53 신규175 모델 관련 원본 블록상태 기존8 + v54 신규49 + skull/head 신규14 = **71 원본 경로**(원본 variants/apply 각239), 블록상태에서 **173/175 모델 직접 참조**, 나머지 2개는 피스톤 헤드 부모 템플릿. 피스톤 자식 face 텍스처 경로40/40 해결. 실제 PNG 3종의 원본 명시 UV 16영역, 모델별 face 226개에서 **1,736회 반복 포함 원본 RGBA 픽셀 관측**(중복 없는 텍셀 좌표298, 모두 불투명). **실게임 렌더/전체 1-2-A 완료 의미 아님. 1-1 승인150/150·상위1/5 완료 유지, 1-2-A/1-2 미완료, 실질 완료율 미산정.** 아래 v53 이하는 역사 기록.


> **최신 v53 (2026-11-14):** [원본 모델 전수 path+SHA 연구](research/vanilla_models/v53/REPORT.md) · [P1 544행 확장 원장](research/vanilla_models/v53/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅용 인수인계](research/vanilla_models/v53/NEXT_CHAT_HANDOFF.md). **v52 369 → v53 544/544 P1 모델 원본 경로·SHA 연결**(175개 직접 원본 JSON 새 검사; 미연결0). 신규 자체 요소4/면20(명시UV20), 부모 적용3413면(명시UV3245·암시UV168), blockstate8파일·variants58, PNG4파일 실제RGBA1024픽셀. **544는 원본 신원 연결 범위이며 전체 1-2-A 의미론 통합·기하·UV·PNG·상태·렌더러 완료율이 아니다. 1-2-A/1-2 진행 중, 1-1 승인150/150·상위1/5 완료 유지.** 아래 v52 이하 내용은 역사적 기록.


> **최신 v52 (2026-11-14):** [v52 직접 원본 연구](research/vanilla_models/v52/REPORT.md) · [P1 전체 544행 원장](research/vanilla_models/v52/01_P1_544_EVIDENCE_LEDGER.csv) · [v52 다음 채팅 인수인계](research/vanilla_models/v52/NEXT_CHAT_HANDOFF.md). v51 **335 → v52 369개** 모델 경로+SHA 연결(신규34, 미연결175). 신규 자체23요소/60면(모두 원본 명시 UV), 상속 적용394면(원본 명시376·암시18), blockstates9/variants43/배열 선택지103, 원본 PNG 4종 실제 RGBA1024픽셀 Git blob SHA 검증. **1-2-A/1-2 미완료·완료율 미산정; 1-1 승인150/150·상위1/5 유지.** 아래 v51 이하 '현행' 표시는 역사적 기록.


> **현행 v51 (2026-11-14):** [1-2-A 신규 54모델 원본 조사 보고서](research/vanilla_models/v51/REPORT.md) · [P1 544모델 최신 원장](research/vanilla_models/v51/01_P1_544_EVIDENCE_LEDGER.csv) · [다음 채팅 인수인계](research/vanilla_models/v51/NEXT_CHAT_HANDOFF.md). **v50 281 → v51 335개 모델 path+SHA 근거 연결**, 조사된 근거에서 **209개 미연결**(미연구 확정 아님). 본 회차 신규 직접 원본 모델 54경로: 선반28·이끼카펫5+carpet 부모1·가마솥10·발광10. 원본 자체 44요소/185면(명시 UV8·암시 UV177), 모델에 적용된 상속면826건(명시 출처176·암시 출처650). 15개 원본 blockstate 변형21/multipart110, 선반 정적 파생128조합·256모델 적용. 11개의 템플릿 단독 텍스처 슬롯은 leaf 검증 전 보류. 원본 PNG 바이너리 직접 읽기 UTF-8 오류 → **새 RGBA 픽셀검사0, 런타임검사0**. **1-2-A·1-2 미완료, 1-2 완료율 미산정. 1-1 승인 텍스처150/150 및 상위 1/5과제 완료 유지.** 아래 이전 v50 '최신' 표시는 역사적 스냅샷.


> **현행 전역 v50 · 2026-11-14:** [1-2-A 원본 모델 51경로 직접 연구](research/vanilla_models/v50/REPORT.md) · [P1 544행 최신 근거 원장](research/vanilla_models/v50/01_P1_544_EVIDENCE_LEDGER.csv) · [v50 다음 채팅 인수인계](research/vanilla_models/v50/NEXT_CHAT_HANDOFF.md). v49 **230 → v50 281개 원본 모델 경로+SHA 연결**, 선택 연구 근거에서 **263개 미연결**(미연구 확정 아님). 촛불/케이크·표지판·구리 조명/상자 관련 P1 **51모델 원본 JSON 직접 검증**: particle-only22·부모 기하 상속27·자체 elements 2; 자체 5요소/22면(명시UV16, 암시UV6), 부모 적용면561건(명시519, 암시42). 원본 blockstate JSON35종, 원본 variant74건; world state 직접 모델 참조49종, 템플릿2종 별도. v48 기존 랜턴 부모 SHA2개 재검증·신규 원형 실적 제외. **원본 PNG RGBA 픽셀 검증 0, 인게임 렌더 미검증, 1-2-A/1-2 전체 미완료 및 완료율 미산정. 1-1 v42 승인 150/150 완료와 상위 과제 1/5 완료 유지.** 아래 v49 이하 '현행'은 당시 기록.


> **현행 전역 v49 · 2026-11-14:** [1-2-A 화분 37·선반 21·P1 부모 1 원본 분석 보고서](research/vanilla_models/v49/REPORT.md) · [P1 544행 최신 상태 원장](research/vanilla_models/v49/01_P1_544_EVIDENCE_LEDGER.csv) · [v49 다음 채팅 인계](research/vanilla_models/v49/NEXT_CHAT_HANDOFF.md). v48 **171 → v49 230개 모델 원본 경로+SHA 근거 연결**, 검사 근거에서 미연결 **314개**(미연구 확정 아님). 이번 SHA 연결 59개 중 기존 v47 실제 source 검증 6개 재연결(신규 실적 미집계), 새로운 source 직접 연구 53개. 화분 37 leaf의 적용면 978건(명시 UV 972/암시 6), 고유 원본 새 직접 조사 30요소·106면(명시 UV100/암시6), 선반 leaf 21의 기존 부모 상속 적용면 114건. 화분 blockstate 37개 단일 variant, 선반 3블록상태 원본 72 multipart/파생 정적 96조합. 새 PNG RGBA 픽셀 검증0·런타임 미검증. **1-2-A 및 1-2 전체 진행 중, 전체 완료율 미산정. 1-1 승인 150/150·상위 5개 중 1/5 완료 유지**. 아래 v48 이하 '현행'은 과거 체크포인트.


> **현행 전역 v48 · 2026-11-14:** [1-2-A P1 모델 36경로 원본 검증 보고서](research/vanilla_models/v48/REPORT.md) · [모델별 544행 증거 원장](research/vanilla_models/v48/01_P1_544_EVIDENCE_LEDGER.csv) · [v48 다음 채팅 인수인계](research/vanilla_models/v48/NEXT_CHAT_HANDOFF.md). v47 SHA 연결 **135 → v48 171개 원본 모델 경로**, 이번 조사 근거에서 미연결 **373개**(미연구 확정 아님). 신규 P1 모델 JSON 36경로(자작/벚 선반14, 조각책장10, 기타9, 신규 연결 부모3). 원본/부모 직접 선언 요소14·명시 UV면68 재검수, 그중 v38 기하 원형 3요소/18면 별도 제외. 원본 multipart 100규칙/파생정적 320조합·1920 모델 적용, 추가 blockstate 6파일/9 variants. PNG 화소 신규0·인게임 렌더 미검증. **1-2-A와 1-2 진행 중, 실제 완료율 미산정. 1-1 승인 150/150 및 상위 5과제 중 1/5 완료 유지.** 아래 v47 이전 현행 표시는 그 당시 기록.


> **현행 전역 v47 · 2026-11-14:** [1-2-A 신규 원본 모델 검증·역사 SQLite DB 조사 보고서](research/vanilla_models/v47/REPORT.md) · [P1 544 모델별 최신 SHA 근거원장](research/vanilla_models/v47/01_P1_544_EVIDENCE_LEDGER.csv) · [v47 다음 채팅 인계](research/vanilla_models/v47/NEXT_CHAT_HANDOFF.md). 이전 v46 연결 124에 신규 원본 직접 조사 11개 모델 경로를 추가해 **135/544 SHA 연결**, 현 조사 출처에서 미연결 **409개**(미연구 확정 아님). 기존 SQLite v5~v8 네 DB 직접 읽기/5·10·16·20테이블, 기존 연결 고유 P1 53개 확인 **신규 과거 연결 0개**, 빌드 스크립트 네 개 조사. 신규 flower-pot 3템플릿+beacon 원본 **26 elements/100 explicit UV faces**, bamboo_shelf 7 leaf는 v38/v45 부모 원형 재사용, 원본 multipart24/파생32조합. 원본 PNG 신규 실화소 분석 0. **1-2-A와 1-2 계속 진행 중**, 1-2 전체 완료율 미산정. **1-1 150/150 완료 및 상위 과제 1/5 완료 보존**. 아래 이전 버전의 '현행' 표현은 과거 스냅샷.


> **현행 전역 v46 · 2026-11-14:** [1-2-A 역사 Markdown·JSON 49개 및 최근 연구 CSV 30개 감사](research/vanilla_models/v46/REPORT.md) · [P1 544개 모델별 근거 원장](research/vanilla_models/v46/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [다음 채팅 인계](research/vanilla_models/v46/NEXT_CHAT_HANDOFF.md). 기존 v45 SHA 연결 119개 + 이번 새 원본 JSON 경로 연결 5개 = **124개**, 현 조사 근거에서 미연결 **420개**(미연구 확정 아님). P1 544 모델 경로 중 같은 내용 SHA의 경로 그룹 2건·7경로 식별, 모델 정체는 전체 경로로 구분. 9개의 particle-only model JSON 직접 확인(4 재검증/5 신규), 이름만 기록된 역사 참조 32건은 약한 근거. 1-2-A/1-2 **진행 중**, 전체 완료율 미산정. **1-1 150/150 완료, 상위 과제 1/5 유지**. 아래 v45·v44의 '현행'은 이전 시점 기록.


> **현행 전역 v45 · 2026-11-14:** [1-2-A 역사 SHA·아카시아 선반 7 leaf 직접 소스 검증](research/vanilla_models/v45/REPORT.md) · [P1 544행 최신 상태 원장](research/vanilla_models/v45/01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [v45 다음 채팅 인계](research/vanilla_models/v45/NEXT_CHAT_HANDOFF.md). 기존 v44 SHA 연결 110 + 과거 v30 증거 신규 회수 2 + 새 원본 아카시아 선반 leaf 7 = **119개 연결**, **425개는 검사 범위에서만 미연결**. 추가 역사 CSV **86종 SHA 필드 검사**; 7개 부모 템플릿은 v38 원형 재사용. 아카시아 blockstate 원본 24 multipart / 파생 32 조합. 1-2-A 및 1-2 전체 **진행 중**, 실제 종합 완료율 미산정. **1-1 150/150 완료 · 상위 1/5 유지**. 아래 v44 이하 '현행' 문구는 과거 스냅샷.


> **현재 전역 v44 · 2026-11-14:** [1-2-A P1 544개 역사적 SHA 증거 1차 대조](research/vanilla_models/v44/REPORT.md) · [544개 모델별 원장](research/vanilla_models/v44/01_P1_544_SHA_CROSSWALK.csv). **110개는 선택한 과거 증거에서 SHA가 연결된 고유 모델, 434개는 이번 자료에서 미연결**(미분석 확정 아님). v38 중복 5개 제거·오탐 2건 정정, v5~v43 전체 증거 통합은 **계속 진행 중**. 1-1 v42 소스 완료 150/150 및 전체 **1/5 완료 유지**. 아래 v43/v42 '최신' 문구는 당시 스냅샷.


> **1-2 최신 안내:** [모델·UV·블록상태 v43 실적](docs/vanilla_models_1-2/CURRENT_STATUS.md) · [세부 작업계획](docs/vanilla_models_1-2/WORK_PLAN.md) · [새 채팅 인수인계](docs/vanilla_models_1-2/NEW_CHAT_START.md). 1-1 v42 텍스처 연구 150/150 완료, 1-2 진행 중; 전역 세부과제 1/5 유지.

> **전역 최신 연구 v43 · 2026-11-14:** [1-2 crafter 원본 4 leaf / 48 source variants / 24 상속 face 연결, v36 SHA 유형 오탐 2건](research/vanilla_models/v43/REPORT.md). v35~v43 선택 회차 직접 leaf **28+4=32**, P1 544는 후보 분모이며 v5~v34 전체 역사 검수 완료는 아님. **1-1 v42의 150/150 완료 및 상위 세부과제 1/5 상태는 유지**. 아래 v42/v38의 '현재' 문구는 역사적 스냅샷. 공식 JAR/인게임 실증 미실시.


> **현재 GitHub 정본 · v42 (2026-11-14):** [전체 프로젝트 진행도](docs/CURRENT_PROJECT_STATUS.md) · [1-1 검수 완료](docs/vanilla_texture_1-1/CURRENT_STATUS.md) · [전체 상태 JSON](handoff/STATE.json). **11개 재질·150종 소스 분석 완료 / 상위 세부과제 1/5**, 다음 과제는 **1-2 바닐라 3D 모델·UV·상태 분석**. 아래 v38~v41의 '최신' 표현은 과거 스냅샷이며 현재 실행 지시가 아님.


> **현재 기준 v42(2026-11-14):** [1-1 지정 11분류·150종 소스 연구 완료](docs/vanilla_texture_1-1/CURRENT_STATUS.md) · [원본 Git tree·연구 근거 독립 재검수](research/vanilla_textures/audits/2026-11-14_v42_scope_verification/REPORT.md). 상위 세부과제 **1/5 완료**. 아래 v38~v41 문장/수치는 **당시 스냅샷**이며 현행 업무 지시가 아님.

> **전체 체크포인트 v42:** [1-1 고정 150종 원본 소스 연구 11/11단계 완료](research/vanilla_textures/integrations/v42_INT-1-1-11steps_150_SOURCE_COMPLETE/REPORT.md). 이전 v41의 목재 0/18은 기록상 완료 계수 미반영 오류였고 근거 감사 후 18/18 정정. 1단계 01 항목 완료, 전체 5개 세부과제 중 1/5; 과거 v39–v41 보고서 원본 보존.


> **[과거 v41] 당시 통합 스냅샷:** [11개 재질·150 원장 / 소스 연구 132개 완료](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/REPORT.md). 석재·벽돌 R017(17/17) 최신 반영, 목재·원목 18개 미종결, 상위 과제 0/5 유지. 과거 v39/v40 불변.



## [과거 v40] 당시 연구 기록: 바닐라 1-1 정적 근거 통합

- [v40 보고서](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/REPORT.md) · [11개 단계 원장](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/STAGE_INTEGRATION_LEDGER.csv) · [150개 ID 원장](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/TEXTURE_150_SCOPE_LEDGER.csv) · [매니페스트](research/vanilla_textures/integrations/v40_INT-1-1-11steps_150/MANIFEST.json).
- 통합 ID `INT-1-1-20261113-02`, **11단계·150/150 IDs, 제외 없음**. **1-1-02는 요청에 따라 `TEX02-R015` 고정**, 실제 LIVE `TEX02-R017`은 별도. v39 역사적 10단계·133종은 원본 그대로 보존.
- 이번 통합 새 PNG 실측 **0건**, 고정 참조 source-only 완료 115/150, LIVE 완료 132/150, 상위 연구 대과제 **0/5 유지**. 필수 조건에서 제외된 공식 JAR/인게임 실측을 완료했다고 주장하지 않음. 소스 애니메이션은 최신 상태 기준 9단계 재개·2단계 보류.


> **최신 전역 체크포인트 v39 (2026-11-13):** [1-1 연구 10개 분류·133개 PNG 부분 통합](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/REPORT.md). **1-1-02 석재·벽돌 17개 제외**, 원본 150개 표본 및 독립 TEX 버전 보존, 연구 전체 완료 0/5 유지. 사용자 최신 범위에서는 공식 JAR 인증·인게임 렌더 검증이 필수 완료 조건에서 제외되고, 애니메이션 재개 여부는 단계별 최신 기록에 따름.


> **새 채팅에서 재개하려면 먼저 [HANDOFF.md](HANDOFF.md)를 읽으세요.** [새 채팅 시작 문장](docs/NEW_CHAT_START.md) · [기계 판독 상태](handoff/STATE.json) · [현재 진행도](PROGRESS.md)

마인크래프트 바닐라 블록의 **재질·텍스처·3D 형상·UV·블록 상태·특수 렌더링** 연구 자료를 정리한 저장소입니다.

> **범위:** Minecraft Java Edition **1.21.11** 기준, 가구 모델링 학습의 **1단계 분석 자료**입니다. 실제 가구 제작이나 Project Zomboid 가구 변환은 포함하지 않습니다.

## 현재까지 축적된 연구

| 체크포인트 | 분석 내용 | 상태 |
|---|---|---|
| v1–v4 | 바닐라 텍스처 **150종**에 대한 재질별 픽셀 통계 및 비교 | 표본 분석 완료 / 공식 JAR 대조 및 인게임 검증 미완료 |
| v5 | 바닐라 모델 55개 및 상태 16개 근거, 3D 구성/치수 | 대표 사례 기록 |
| v6 | UV 면 **90건**, 3D 모델 및 블록 상태 추가 분석 | 대표 사례 기록 |
| v7 | 연결형 블록 **8종, 조립 상황 21개** | 선택한 사례의 조건부 모델 조립 분석 |
| v8 | 특수 렌더링 관련 블록 **17종**, 아틀라스 6개, 텍스처 메타데이터 19건 | 대표 사례 기록 |
| v9 | 특수 렌더링 실제 기하 모델 17종/55개 요소, 애니메이션 15개 클립 | 비공식 추출 모델 직접 분석 / 공식 JAR·인게임 검증 대기 |
| v10 | v8 SQLite에 v9 측정값 통합, 신규 DB 3개 테이블·SQL migration | 로컬 SQLite 무결성 검증 / 공식 JAR·인게임 검증 대기 |
| v11 | Another Furniture(1.21.1) 모델 템플릿 **69개**, 완성형 상속 **33개**, 블록 상태 **12개**, PNG 헤더 **12개** 실측 | 03 모드 3D 분석 착수, 04 모드 텍스처 사전 표본 시작 |
| v12 | Handcrafted 원형 120종(810 요소), 생성형 16종 상속, 12개 블록 상태, PNG 12개, 모드 간 5유형 비교 | 원본 파일 실측, 픽셀·인게임 검증과 Macaw 공식 JAR 실측 보류 |
| v13 | Another Furniture·Handcrafted PNG **각 12개 실제 화소 분석(24개)**, UV **13모델·571면 정렬 실측** | 고정 Git 원본 SHA 일치, 정확한 재질/face 연결·인게임 결과는 미검증 |
| v14 | Handcrafted 16개 생성형 leaf의 **51개 텍스처 슬롯 참조** 교차검사 | v13 PNG 근거 연결 19건·표본 밖 16건(고유 12 PNG)·Minecraft 의존 16건. 실제 face→PNG 픽셀 미검증 |
| v15 | 189개 모델(Another Furniture 69 + Handcrafted 120)의 **면 선언률·회전·평면·bbox 초과** 신규 통계 및 v13 PNG 24개 표본 중앙값 재집계 | 기존 실측 CSV의 2차 분석이며 원본 게임 파일·인게임 신규 검증은 하지 않음 |
| v16 | Handcrafted 고정 원본 **PNG 추가 12종 실화소·모델 JSON 30개 SHA 직접 검증**, 16 leaf 상속 face 786인스턴스 중 784모드 면의 실제 PNG/UV 정합성 | 바닐라 텍스처 의존 2면·면 내부 픽셀 샘플링·인게임 보류 |
| v17 | Handcrafted 원본 PNG **24종을 고정 커밋에서 재디코딩**, 16 leaf의 **784/784 모드 face UV 사각형 전체 RGBA 텍셀 실측** | 612 비영 UV/172 면적 0; 420 전부 불투명/145 혼합/47 전부 투명. 바닐라 2면·인게임 보류 |
| v18 | Another Furniture 제작자 고정 원본 **leaf 33/템플릿 30 SHA 직접 확인**, 상속 면 807개 재질 해결(804모드·3기본), **새 PNG 12종 실제 픽셀 검사** | Another PNG 참조 경로 53종 중 24종(45.28%) 실화소, 남은 29경로·면 UV 화소/인게임 미검증 |
| v19 | Another Furniture 미측정 **PNG 29종 새 원본 직접 디코딩**, 누적 선택 모델의 **53/53 PNG**, 모드 면 **804/804 UV 내부 실제 RGBA 실측** | 선정 표본에서만 100%. 바닐라 dirt 3면, Macaw 및 인게임 검증 미완료 |
| v20 | Another Furniture 기존 선정 원형 **69/69 제작자 원본 직접 재조회 및 SHA 대조**, **299 기하 요소·1,362 선언 면의 raw UV·회전·cullface 실측** | 39 원형은 이전 v18 선정 부모 30 바깥의 신규 상세검증 표본. Macaw 공식 JAR/인게임·바닐라 공식 검증 미완료 |
| v21 | Another 제작자 블록 상태 **12개 원본 SHA/802 모델 적용** 직접 재검증, **새 leaf 38개·14 PNG 직접 픽셀·1,192면 실제 UV RGBA**, 원본 가구 유형·상속 확대 | **Another 누적 71 leaf/67 PNG/1,996면 원본 UV 픽셀**, Handcrafted 합산 91 PNG/2,780모드 면. 바닐라·Macaw/인게임 미검증 |
| v22 | Another 셔터 신규 **43개 모델·PNG 42종·원본 UV 214면 직접 픽셀 검증**, 기존 12 블록 상태의 Another 고유 모델 경로 **113/113 원본 JSON 근거 확인** | 선정 Another **leaf 114/PNG 109/면 2,210**, Handcrafted 합계 **PNG 133/면 2,994**, 모드 전체/바닐라 공식/인게임/Macaw 미완료 |
| v23 | 이전 12개 밖 **블록 상태 10개 SHA·386 apply**, 원본 새 leaf **51개**와 새 PNG **42종**을 직접 조사해 **모드 면 1,119개 UV 실제 RGB/알파 실측** | Another **상태 22/177·leaf 165·PNG151·면3,329**, Handcrafted 포함 **PNG175종/면4,113**. 신규 상태의 의자 leaf39개·바닐라/Macaw/인게임 미완료 |
| v24 | Another 미조사 의자 leaf **39개 제작자 원본 JSON/SHA 직접 검사**, 부모 2종의 raw 좌표/UV 비교. **390 요소/1,794 선언 면 인스턴스** | Another leaf **204종**, 신규 10 상태의 Another 경로 91/91 JSON 직접 확인. 원본 PNG·RGBA 신규 검사 0, 누적 PNG175/실제 RGBA 4,113면 유지 |
| v25 | 바닐라 재개: 사용자 업로드 1.21.11 실제 JSON **40개** 및 PNG 헤더 **8개**, 애니메이션 메타 **2개** 직접 조사. 8 기하 모델 **44요소/204면**, 상태 8종 **79 variants+9 multipart** | 기존 v10 바닐라 연구 보완 / 공식 client.jar 및 인게임 검증 미완료 |
| v26 | 바닐라 PNG **8종 실제 8,704 RGBA 픽셀** 전체 해독, 모델 고유 UV면 **36개/애니 포함 70기록**, PNG 3프레임·과거 표본 3종 일치 | 새 화소·면 실측, 미러 SHA 8/8 일치 / 공식 Mojang JAR·인게임 미검증 | 
| v27 | 바닐라 32×32 선반 PNG/6원형 모델 **명시 UV20면/1,376 texel**, 24 multipart·32합성 상태; 퇴비통 암시 UV **26면/3,696 texel**. 새 PNG5종/2,048픽셀, UV 유도식 명시 참조23/23 | 원본 PNG/JSON 계량·일부 좌표 유도 / 공식 1.21.11 JAR·인게임 미검증 |
| v28 | 바닐라 문·다락문·울타리문·계단 **104 variant 상태 전체**의 UVlock/회전 감사, 참나무 문 부모8종 **40 UV면/5,248 텍셀** 원본 PNG 분석, 울타리문 4원형 32요소/160면 기하 | 사용자 업로드 원본 SHA/PNG/JSON 직접 읽기 · 공식 client.jar/인게임 미검증 |
| v29 | 참나무 울타리문 4원형 **160명시 UV면 전체 PNG RGBA 1,952 텍셀**, 열림 6요소 좌표 변화/담장 연결 8요소 y -3, `oak_planks` 독립 Pillow·SHA-256=v4 정확 일치 | 기존 PNG 재검증, 공식 Mojang JAR·인게임 UVlock은 미검증 |
| v30 | 독서대·숫돌·화분·마법부여대·모루 **5원본 모델/91면·93재질면**, PNG18개/4,608 RGBA 픽셀, face UV **6,012 texel-uses** 실제 측정. 그레이스케일 PNG `tRNS` 누락 발견·v26 수치 교정 | 바닐라 01/02 진행, 공식 Mojang JAR·실제 렌더링은 미검증 |
| v31 | 끌로 조각한 책장/양조기 `multipart` 원본59규칙을 256+8=**264조건**으로 실제 평가, 원본 **47면/53재질면** PNG UV **3,808 uses**(불투명3,052/투명756); 원본 PNG6경로/1,536픽셀; 모닥불 켜짐/꺼짐 소스 기하 조사 | 원본 source·RGBA 실화소/합성조건 계산, 공식 JAR·실제 게임 미검증 |
| v32 | **애니메이션 보류 유지**. 통 닫힘/열림·베틀·4작업대 총7 leaf가 공통 `cube` 선언6면을 상속하여 **42 face×material**, 25 PNG/6,400 화소 실측(전부 불투명), **10,752 암시 full-face UV uses**, 6 blockstate 20 variants, 통 윗면 132픽셀 차이 | 정적 상속/원본 PNG 검증, 공식 client.jar/게임 정적 UV 미확인 |
| v33 | 애니메이션 보류 유지. 가마솥·호퍼(아래·측면)·퇴비통(본체+내용물) **12소스모델/40요소/148원본면**, **12 PNG경로/3,072RGBA 픽셀**(불투명2,332/투명740), UV 명시없음→기하유도 추론 **9,280 uses** 전부 불투명, 15원본 정적 상태·퇴비통 9수준 선택 계산, 4PNG 독립 Pillow | 공식 Mojang JAR/실제 게임 UV방향 미검증 |
| v34 | Git tree 원본 모델 **2,390 JSON**, 상태 **1,168 JSON**, 블록 PNG **1,111 경로** 전체 SHA 인벤토리 확보(검토 완료 아님). 랜턴·촛불·막대 8 정적 원형/42요소·153 명시 UV면 중 **122면 실제 원본3PNG/888 texel-uses**, 랜턴 31면 PNG 보류, 정적 상태30. **애니메이션 연구 계속 보류** | 파일 경로 모집단 확보, 공식 Mojang JAR/인게임 UV 검증 미완료, 최종 0/5 |
| v35 | P1 후보544개 중 **이번 회차 원본 소스15 leaf SHA·JSON** 대조(나머지529는 이번에만 미검토). 종33명시 UV·케이크42암시 UV·벌 공유cube6면/24사용, **16PNG/4,096원본 RGBA**, **99 face×material/10,900 PNG texel uses**, 4 상태JSON/71원본 규칙, 꿀정면 차이24/25픽셀. **애니메이션 보류** | Python/Pillow 6PNG 독립 검사, 공식 Mojang JAR/종 본체·게임 정적 UV 미확인, 완료0/5 |

**학습 전체 5개 작업:** 01 바닐라 텍스처(표본 완료/검증 보류), 02 바닐라 3D(진행 중), 03 가구 모드 모델(v11~v12 실측 진행 중), 04 모드 텍스처·UV(PNG 24개 전체 실화소 및 13모델 571면 UV 표본 정렬 측정), 05 바닐라/모드 비교(5쌍 사전 비교, 최종 검증 미착수). 최종 확정 완료는 **0/5**입니다.

## [과거 지시] 애니메이션 보류 (2026-11-13)

**사용자 최신 작업 지시(2026-11-13): 애니메이션 분석은 일단 보류.** 새로운 애니메이션 프레임 해독, 키프레임·클립 분석, 움직임 재현 및 애니메이션 인게임 검증을 진행하지 않는다. 기존 v9/v26/v31 애니메이션 관련 기록은 삭제하지 않고 보존하되, 새로운 진행도에 포함하지 않는다. 우선순위는 **정적 바닐라 3D 모델·기하·텍스처·UV·블록 상태·정적 렌더링 검증·공식 원본 무결성**이다. 애니메이션 연구는 사용자가 명시적으로 재개를 요청할 때까지 유지 보류.


**전체 바닐라 모델 연구 예정 대상:** [블록 모델 JSON 2,390개를 13개 분야로 분류한 전체 목록](docs/VANILLA_STATIC_MODELS_FULL_STUDY_LIST_v34.md) · [2,390개 전체 우선순위 CSV](research/vanilla_models/v34/10_all_2390_future_review_queue_filename_categories.csv). P1 544/P2 1,039/P3 807. **기존 연구와의 완료 상태 대조 전인 파일명 기반 후보 분류**이며 실제 분석 완료 수가 아님. 블록 상태1,168/PNG1,111은 v34 원본 인벤토리 별도 링크. 애니메이션 보류 유지.

## 빠른 탐색

- [**v35 최신 P1 종·케이크·벌통·벌집 15 모델/71 상태/16 PNG 직접 분석**](research/vanilla_models/v35/00_v35_P1_종케이크벌통벌집_15모델_71상태_16PNG_분석보고서.md) · [P1 544파일 이번 회차 검수 원장](research/vanilla_models/v35/12_p1_544_static_source_review_ledger.csv) · [99 UV face×material 표본: 종/케이크75](research/vanilla_models/v35/08_bell_cake_75_faces_png_uv_sampling.csv) · [벌24](research/vanilla_models/v35/10_four_bee_leaf_24_parent_face_texel_records.csv) · [독립 Pillow6](research/vanilla_models/v35/14_six_png_independent_pillow_sha256_rgba.csv) · [v35 기계요약](research/vanilla_models/v35/v35_p1_bell_cake_bee_summary.json). **종 본체 특수 렌더러·공식 JAR 미검증, 애니메이션 보류, 최종0/5**.

- [**v34 최신: 정적 랜턴·촛불·막대 153명시 UV면, 2,390 모델 전체 목록**](research/vanilla_models/v34/00_v34_바닐라2390모델_정적랜턴촛불_153면UV_전체목록.md) · [블록 모델 전수 SHA 목록](research/vanilla_models/v34/01_inventory_2390_block_model_paths_git_shas.csv) · [blockstates 전수 SHA 목록](research/vanilla_models/v34/02_inventory_1168_blockstate_paths_git_shas.csv) · [블록 PNG 전체 목록](research/vanilla_models/v34/03_inventory_1111_block_texture_png_paths_git_shas.csv) · [원본 153면 조사](research/vanilla_models/v34/05_eight_source_models_153_explicit_uv_faces_static_alpha.csv) · [Pillow 원본3 PNG](research/vanilla_models/v34/06_three_static_png_pillow_sha256_alpha_masks.csv). **애니메이션 보류, 최종 0/5**.

- [**v33 최신 정적 가마솥·호퍼·퇴비통: 148 source face / PNG12 경로·3,072픽셀 / 15 원본 상태**](research/vanilla_models/v33/00_v33_가마솥호퍼퇴비통_148면_암시UV_PNG정적분석.md) · [40요소 원시 기하](research/vanilla_models/v33/01_twelve_model_40_elements_geometry.csv) · [148면 기하유도 UV](research/vanilla_models/v33/02_twelve_model_148_inferred_uv_faces.csv) · [12원본 PNG 7+5 파일](research/vanilla_models/v33/04_cauldron_hopper_7_png_rgba.csv) · [퇴비통 PNG5](research/vanilla_models/v33/06_composter_5_png_full_rgba.csv) · [기계 요약](research/vanilla_models/v33/v33_hollow_static_model_uv_png_summary.json). 사용자 애니메이션 보류 유지, 최종0/5.

- [**v32 최신 정적 모델: 통·베틀·4작업대 7 leaf /25 PNG/20상태·암시 UV 42면**](research/vanilla_models/v32/00_v32_정적통베틀작업대_25PNG_42면암시UV_20상태보고서.md) · [7 leaf 상속](research/vanilla_models/v32/01_seven_leaf_parent_chain.csv) · [42면의 최종 재질](research/vanilla_models/v32/02_42_inherited_cube_face_texture_bindings.csv) · [25 PNG 원본 RGBA](research/vanilla_models/v32/03_png_12_full_rgba_metrics.csv) · [PNG 추가 13종](research/vanilla_models/v32/04_png_13_full_rgba_metrics.csv) · [기계 summary](research/vanilla_models/v32/v32_static_cube_face_png_audit_summary.json). 사용자 애니메이션 보류 지시 유지, 최종 0/5.

- [**v31 최신 바닐라: 책장·양조기 264상태/47 source 면·6 PNG/모닥불 원본 형상**](research/vanilla_models/v31/00_v31_책장양조기_264상태_47면_PNG실화소_모닥불원본보고서.md) · [59 원본 multipart 규칙](research/vanilla_models/v31/01_bookshelf_brewing_59_original_multipart_rules.csv) · [264 조건 평가](research/vanilla_models/v31/02_bookshelf_256_and_brewing_8_combinations.csv) · [책장 17면×재질 UV 픽셀](research/vanilla_models/v31/04_bookshelf_17_source_face_material_rgba.csv) · [양조기 36면 UV 픽셀](research/vanilla_models/v31/06_brewing_36_face_original_png_rgba.csv) · [기계 summary](research/vanilla_models/v31/v31_bookshelf_brewing_campfire_summary.json). 확정 완료 0/5.

- [**v30 최신: 독서대·숫돌·화분·마법부여대·모루 91면·18 PNG/과거 v26 그레이스케일 투명도 정정**](research/vanilla_models/v30/00_v30_바닐라5모델_91면UV_18PNG_RGBA_투명도정정보고서.md) · [18 PNG 통계 (1)](research/vanilla_models/v30/01_lectern_grindstone_9_png_rgba.csv) · [18 PNG 통계 (2)](research/vanilla_models/v30/04_pot_enchant_anvil_9_png_rgba.csv) · [v30 요약 JSON](research/vanilla_models/v30/v30_five_models_face_png_summary.json). 바닐라 우선, 최종 완료 0/5.

- [**v29 최신 연구: 참나무 울타리 문 160면 실제 PNG·열림/담장 좌표 비교**](research/vanilla_models/v29/00_v29_울타리문160면_실제PNG_UV_열림담장좌표비교보고서.md) · [160면 원본 UV/화소 CSV](research/vanilla_models/v29/01_fence_gate_160_source_face_uv_rgba.csv) · [8요소 상태 델타](research/vanilla_models/v29/06_eight_element_open_wall_geometry_deltas.csv) · [요약 JSON](research/vanilla_models/v29/v29_fence_gate_full_uv_rgba_summary.json). 바닐라 우선, 완료 0/5.

- [**v28 최신 바닐라: 문·다락문·울타리문·계단 104상태 / 문 UV 40면 원본 픽셀**](research/vanilla_models/v28/00_v28_바닐라문다락문게이트계단104상태_40면UV_RGBA.md) · [104 variants 증거표](research/vanilla_models/v28/01_four_blockstates_104_exact_variants.csv) · [40면 UV PNG 통계](research/vanilla_models/v28/03_oak_door_eight_templates_40_faces_uv_rgba.csv) · [요약 JSON](research/vanilla_models/v28/v28_four_states_and_door_uv_summary.json). 바닐라 01/02 우선·최종 0/5.

- [**v27 최신 — 바닐라 선반·퇴비통 원본 PNG와 자동/명시 UV 실화소 검증**](research/vanilla_models/v27/00_v27_선반32x32_퇴비통자동UV_원본화소검증보고서.md) · [20면 선반 CSV](research/vanilla_models/v27/02_oak_shelf_20_face_actual_png_rgba.csv) · [26면 퇴비통 CSV](research/vanilla_models/v27/06_composter_26_implicit_uv_face_rgba.csv) · [v27 기계 요약](research/vanilla_models/v27/v27_shelf_composter_uv_pixel_summary.json). 완료 0/5 유지.

- [**v26 최신 보고서 — 바닐라 8 PNG 실제 RGBA와 UV 면 36개/70프레임**](research/vanilla_models/v26/00_v26_바닐라8PNG_전체RGBA_36면70프레임_실화소보고서.md) · [8 PNG 픽셀 계량](research/vanilla_models/v26/01_eight_png_full_rgba_pixels.csv) · [70행 면 실화소](research/vanilla_models/v26/02_selected_face_frame_original_rgba.csv) · [검증 요약](research/vanilla_models/v26/v26_vanilla_pixel_uv_audit_summary.json). 바닐라 우선 진행 및 최종 0/5 유지.

- [**v25 최신 보고서: 업로드된 1.21.11 바닐라 원본 JSON/상속·상태·PNG 메타 실측**](research/vanilla_models/v25/00_v25_바닐라원본_모델상속상태PNG_직접검증보고서.md) · [기계 판독 요약](research/vanilla_models/v25/v25_vanilla_research_audit_summary.json). 바닐라 공식 client.jar/인게임은 미검증이며 완료 0/5.

- [**v24 최신 보고서: 의자 39개 원본 SHA·상속·UV 구조 검증**](research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md) · [39모델 개별 SHA CSV](research/furniture_mods/v24/chair_remaining_39_original_json_geometry_audit.csv) · [감사 JSON](research/furniture_mods/v24/v24_chair_39_audit_summary.json).


- [1단계 학습 계획](docs/01_1단계_학습계획_v1.md)
- [현재 진행 상황](PROGRESS.md)
- [연구 근거 및 검증 한계](SOURCES_AND_LIMITS.md)
- [GitHub에 저장된 SQLite 기준본 (v8)](data/MC_Furniture_Style_Stage1_Research_v8.sqlite) — v10 전체 바이너리는 아직 미업로드, [SQL migration](data/migrations/v8_to_v10.sql)을 적용하여 복원
- [v4: 누적 150종 텍스처 분석](research/vanilla_textures/v4_150/11_누적150종_확장검증_보고서.md)
- [v7: 연결형 블록 조립](research/vanilla_models/v7/00_v7_연결형_조립분석_보고서.md)
- [v8: 특수 렌더링](research/vanilla_models/v8/00_v8_특수렌더_정적동적_비교보고서.md)
- [v9: 특수 렌더링 실제 3D 부품 구조](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md)
- [v9: 애니메이션 구성](research/vanilla_models/v9/03_v9_애니메이션_검토보고서.md)
- [v10: 누적 DB 통합 검증 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md)
- [v11: Another Furniture 실제 모델/텍스처 1차 실측 보고서](research/furniture_mods/v11/00_v11_AnotherFurniture_모델분석_보고서.md)
- [v11: 모델 템플릿 69개 측정 CSV](research/furniture_mods/v11/template_metrics_69_total.csv)
- [v12: Handcrafted 전수 원형 120종 분석 및 모드 간 사전 비교](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md)
- [v12 Handcrafted 120종 측정 CSV](research/furniture_mods/v12/handcrafted_authored_120_total.csv)
- [v12 모드 대표 5쌍 구조 비교](research/furniture_mods/v12/another_vs_handcrafted_5_category_pairs.csv)
- [v23: Another 블록 상태 10개·신규 leaf 51개·PNG 42종·1,119면 실제 UV RGBA](research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md) · [51 leaf 상속 면 CSV](research/furniture_mods/v23/new_51_leaf_source_face_texture_resolution.csv) · [실측 1,119면 CSV](research/furniture_mods/v23/new_51_leaf_all_1119_face_actual_rgba.csv)
- [v22: Another 셔터 신규 43 leaf·새 42 PNG·214면 UV 실제 RGBA](research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md) · [원본 PNG 43종 SHA/색상](research/furniture_mods/v22/shutter_43_png_original_source_manifest.csv) · [214면 UV 실제 RGBA](research/furniture_mods/v22/shutter_214_face_uv_original_rgba.csv)
- [v21: Another 신규 38 leaf·14 PNG·1,192면 UV 내부 실제 RGBA 분석](research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md) · [신규 38 leaf 재질 면](research/furniture_mods/v21/another_new_38_leaf_face_resolution.csv) · [실제 RGBA 1,192면 CSV](research/furniture_mods/v21/another_new_38_leaf_all_rgba_1192.csv)
- [v20: Another 원형 69개 전체 제작자 JSON/1,362 선언 면 기하·UV 분석](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md) · [69 모델 CSV](research/furniture_mods/v20/another_69_templates_direct_original_geometry.csv) · [원본 1,362면 CSV](research/furniture_mods/v20/another_69_templates_1362_original_faces.csv)
- [v19: Another 53 PNG 원본·804면 실제 UV 내부 픽셀 RGBA 분석](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md) · [804면 CSV](research/furniture_mods/v19/another_804_face_actual_rgba.csv) · [Handcrafted/Another 선정 표본 UV/알파 비교](research/furniture_mods/v19/00_v19_모드간실제면UV픽셀_선정표본비교.md)
- [v18: Another 원본 모델 63개·807면 재질 경로·새 PNG 12종 분석](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md) · [113개 면 재질 그룹](research/furniture_mods/v18/another_face_material_groups_113.csv) · [12개 새 PNG](research/furniture_mods/v18/another_new_png_12_pixel_metrics.csv)
- [v17: 784개 면의 실제 UV 사각형 픽셀·알파 검사](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md) · [전체 784면 CSV](research/furniture_mods/v17/face_pixel_samples_784.csv) · [오프라인 Pillow 재검산 코드](scripts/reproduce_v17_face_pixels.py)
- [v16: 고정 원본 PNG 12개/JSON 30개/면→PNG 정합성 검증](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md) · [신규 12 PNG 실화소 CSV](research/furniture_mods/v16/handcrafted_12_new_png_pixel_metrics.csv) · [로컬 원본 재검증 스크립트](scripts/reproduce_v16_handcrafted_originals.py)
- [v15: 모델 189개 표면·회전·평면·bbox 정량 비교](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) · [189개 모델별 CSV](research/furniture_mods/v15/model_geometry_derived_189.csv) · [재검산 스크립트](scripts/verify_v15_geometry_research.py)
- [v14: Handcrafted leaf 16개/51개 슬롯 연결 감사](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md) · [CSV](research/furniture_mods/v14/handcrafted_texture_bindings_51.csv)
- [v13: PNG 24개 직접 디코딩과 UV 13모델/571면 정량 검사](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md)
- [v13: 모델 PNG·픽셀 재계산 스크립트](scripts/reproduce_mod_png_v13.py)
- [v10 SQL 증분 패치](data/migrations/v8_to_v10.sql)
- [v10 SQLite 재구성 Python 스크립트](scripts/rebuild_v10_db.py)
- [공식 1.21.11 client.jar 대조 도구](scripts/verify_official_jar.py) / [사용법](docs/official_client_jar_검증방법.md) — 실제 JAR 검사 미완료

## 폴더 구조

```text
Minecraft_Furniture_Style_Research/
├── README.md
├── PROGRESS.md
├── SOURCES_AND_LIMITS.md
├── docs/                                  # 학습 계획
├── data/                                  # 최신 누적 SQLite 데이터베이스
├── research/
│   ├── vanilla_textures/v1_30...v4_150/  # 버전별 보고서·측정 CSV·재현 코드·분석 도표
│   ├── vanilla_models/v5...v10/           # 모델·블록상태·UV·특수 렌더링 연구 기록
│   └── furniture_mods/v11...v23/          # Another Furniture·Handcrafted 실측 통계 (원본 에셋 미수록)
└── FILE_MANIFEST_SHA256.csv              # 저장소 파일 해시 목록
```

## 분석 재현

텍스처 분석을 재검산하려면 본인이 적법하게 확보한 Minecraft `client.jar` 또는 추출된 게임 에셋을 **로컬에서만** 사용합니다. 스크립트 및 인수는 각 체크포인트의 `README.md`를 참고하세요.

```bash
pip install -r requirements.txt
```

일부 `build_v*.py` 스크립트는 제작 당시의 `/mnt/data` 경로와 **앞선 체크포인트 파일**을 전제로 작성되었습니다. 따라서 완전 자동 CI 재현 코드가 아니라 당시 분석 과정의 재현 참고 자료입니다. 실행 전 경로를 수정해야 합니다.

## 저작권과 검증 상태

- **v25에 사실 관계 변경:** 사용자가 `1.21.11/` 폴더에 `.class`·Minecraft 원본 PNG·모델 JSON을 업로드했으며 공개(public) 상태입니다. 이 저장소 전체에 원본이 없다는 과거 설명은 더 이상 유효하지 않습니다. 공개 재배포 관련 저작권/이용약관 위험을 검토하고 공개 원본 자산은 분리·비공개화할 것을 권장합니다. 연구 보고서 `research/`에는 CSV의 좌표·통계·파일 출처와 분석자가 작성한 설명만 새로 저장했습니다.
- 게임 관련 저작권은 각 권리자에게 있으며, 본 저장소는 Mojang/Microsoft의 공식 배포물이 아닙니다.
- 데이터 출처와 버전 고정, 검증하지 못한 부분은 [SOURCES_AND_LIMITS.md](SOURCES_AND_LIMITS.md)에 명시했습니다.
- **저장소 라이선스는 지정하지 않았습니다.** 추후 원본·파생 자료의 라이선스를 검토한 다음 결정하는 편이 안전합니다.


### 최신 DB 재구성 (v10)

```bash
python scripts/rebuild_v10_db.py
```

이 명령은 v8 SQLite를 읽고 SQL 패치를 적용한 새 v10 SQLite를 만듭니다. GitHub는 **v10 전체 바이너리가 아닌 v8 원본 + v10 증분**을 보관합니다.


### v11–v12 모드 소스의 라이선스 및 버전 주의

Another Furniture의 1.21.1 소스 모델을 조사했으며, **기존 바닐라 1.21.11과 버전이 다릅니다**. 제작사 에셋 리소스는 [원본 LICENSE](https://github.com/crispytwig/AnotherFurniture/blob/1.21.1/LICENSE)상 **All Rights Reserved**이므로 JSON·PNG 원본은 재배포하지 않고 분석 통계와 해시/경로만 저장합니다.
