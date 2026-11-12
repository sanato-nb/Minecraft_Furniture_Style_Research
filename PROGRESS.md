# 학습 진행도

**새 채팅 인수인계:** [HANDOFF.md](HANDOFF.md) · [복사용 시작 프롬프트](docs/NEW_CHAT_START.md) · [현재 상태 JSON](handoff/STATE.json)

업데이트: 2026-11-12 / 체크포인트 v15

| 1단계 세부 작업 | 상태 | 수치 |
|---|---|---|
| 01. 바닐라 재질·텍스처 분석 | 표본 목표 달성 / 최종 검증 보류 | **150/150종, 표본 100%** |
| 02. 바닐라 3D 모델·블록 구조 분석 | 진행 중 | 대표 모델·UV·연결형·특수 렌더링 v5–v10 |
| 03. 가구 모드 3D 모델 분석 | **v15 정량 교차비교까지 진행 중** | v11 Another Furniture 템플릿 69개 + v12 Handcrafted 원형 120개 실측 보존. v15 **189개 모델 face 선언/회전/평면/bbox 신규 파생 집계**. 공식 게임/맥코/인게임 검증 보류 |
| 04. 가구 모드 텍스처·UV 분석 | **v14 교차 참조 근거 감사 진행 중** | v13 PNG 24종 실화소·13모델 UV 571면 정렬 표본. v14 Handcrafted 16 leaf의 슬롯 51건: 모드 35(기존 PNG SHA 일치 19, 표본 밖 16), Minecraft 의존 16. 실제 face/픽셀 미검증 |
| 05. 바닐라 ↔ 가구 모드 비교 검증 | 사전 비교만 작성 / 최종 검증 미시작 | 두 모드의 의자·벤치·소파 5유형 구조 비교표 작성. 바닐라와의 인게임 비교는 미완료 |

**전체 완료:** 0/5개. 일부 체크포인트의 100%는 *표본 수 달성*만을 뜻하며 공식 JAR/인게임 재현까지 마쳤음을 의미하지 않습니다. 02번도 모집단이 확정되지 않아 임의 완료율을 산출하지 않습니다.

## 누적 근거 데이터 (v8 SQLite + v9 CSV + v10 SQL migration + v11~v15 모드 CSV)

- 텍스처 측정 레코드: 150건
- 최초 모델 근거: 55건
- 최초 블록 상태 근거: 16건
- v6 UV 면별 기록: 90건
- v7 조립 상황: 21건 (선택형 사례)
- v8 특수 렌더링 블록 근거: 17건
- v8 텍스처 아틀라스: 6건
- v9 특수 렌더링 모델: **17종**, **19개 레이어**, **55개 큐브/평면(평면형 15개)**, 추출 JSON 직접 검증
- v9 애니메이션: **6종 모델**, **15개 클립**, **304개 저장 키프레임**
- v10 통합: v9 데이터 **19개 모델 레이어·15개 애니메이션 클립**을 v8 SQLite에 추가하는 SQL migration 게시, 로컬 재구성 DB 무결성 검사 통과
- 공식 JAR 검증 도구: **스크립트 작성 및 합성 테스트 통과**, 실제 Minecraft 1.21.11 client.jar 비교는 미수행
- v11 Another Furniture (Minecraft 1.21.1): Git tree 모델 1,451개·블록 PNG 1,220개 확인. **템플릿 69개 직접 분석(299 요소/1,362 UV면/0두께 요소 34개)**, **완성형 33개 상속 해석**, **블록 상태 12개(802 entry 합산)**, **PNG 헤더 12개**.
- [v11 자세한 실측 보고서](research/furniture_mods/v11/00_v11_AnotherFurniture_모델분석_보고서.md).
- **v12 Handcrafted:** `1.21.x` 브랜치의 고정 커밋 `8d21d166...` 전체 원형 JSON **120/120 직접 측정(810 요소·4,860 UV 지정 면·283 비영 회전·183 0두께)**. 자동 생성 블록 모델 **11,989 경로** 확인(그중 16건 상속 실측), 상태 JSON 12개(4,724 상태 항목), PNG 헤더 12개. 소파·벤치·의자 **5쌍 사전 비교**. Macaw의 공식 1.21.11 배포 확인, 실제 모델 실측 0건(보류).
- [v12 자세한 실측 보고서](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md). 두 모드의 원본 JSON·PNG는 저작권 때문에 미재배포.
- **v13 실제 PNG 화소:** 양 모드 각각 12개씩 **24개 전체 PNG 바이트 직접 디코딩**, SHA 일치; 알파 0/255 화소 총 **117,504개**(반투명 0), RGB 색상 수·밝기·가시 범위 실측. **모델 13개 UV 571면 전부 텍스처 픽셀 경계 정렬**, UV 역방향 면 190개·면적 0 UV 64개(오류 단정 금지).
- [v13 실화소·UV 상세 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md) · [PNG 실측 12+12 CSV](research/furniture_mods/v13/) · [로컬 검증 스크립트](scripts/reproduce_mod_png_v13.py).

- **v14 신규 결과:** Handcrafted 생성형 leaf **16개**, 슬롯 참조 **51건** (모드 경로 35 / Minecraft 참조 16). 기존 v13 실측 PNG에 SHA·치수까지 일치 **19건**, v13 PNG 표본 밖 모드 참조 **16건(고유 12 PNG)**. 모드 슬롯 모두 연결 7개 leaf, 하나 이상 연결 13개, v13 UV 부모 표본 대응 9개. [v14 보고서](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md). **이번 원본 바이트 재디코딩 및 face→PNG 실화소 검증 0건**.

- **v15 신규 정량 비교:** v11/v12 기록 189개 모델에서 면 선언 가능한 슬롯과 실제 기재 수를 비교. Another Furniture 69개/299요소/가능면 1,794개 중 **1,362면 선언(75.92%)**/생략 432, 회전 17·평면 34·원시 bbox 0..16 밖 모델 3개. Handcrafted 120개 원형 모델 중 자체 요소 112개/810요소/가능면 4,860개 중 **4,860면 선언(100%)**, 회전 283·평면 183·원시 bbox 밖 모델 60개. [v15 보고서](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) · [모델별 189개 CSV](research/furniture_mods/v15/model_geometry_derived_189.csv) · [재계산 검증 코드](scripts/verify_v15_geometry_research.py). **기존 계측을 새 방식으로 집계한 2차 분석이며 v15 신규 원본 모델/PNG 직접 관찰은 0건.**

## 다음 과제

1. Minecraft Java 1.21.11 공식 `client.jar`와 비공식 미러 자료의 바이트/해시 비교. [로컬 검사 스크립트](scripts/verify_official_jar.py) 및 [사용법](docs/official_client_jar_검증방법.md) 준비 완료(실제 JAR 미실행).
2. 실제 게임에서 잔디·잎의 색 변형, 투명도, 모델 조립 결과 검증.
3. [v10 통합 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md) 및 [v9 특수 모델 자료](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md)의 공식 클라이언트·인게임 교차검증 후 02번 종료 여부 판정.
4. **03번 v12에서 Handcrafted 원형 120개 분석까지 완료:** 검증된 Macaw's Furniture 공식 1.21.11 배포 JAR(또는 공식 소스)을 확보하면 모델 구조를 직접 분석한다. 불확실한 제3자 복제본을 쓰지 않는다.
5. **v15는 기존 189개 모델의 기하 지표를 확장했으나 원본의 면별 실제 텍스처/렌더는 미검증이다.** v14에서 남은 미측정 PNG 12종, `face→#slot→PNG` 정확한 화소 대응, v15의 bbox 초과 사례를 공식·고정 원본으로 추가 검증한다.

**주의:** GitHub에 추적된 SQLite 바이너리는 **v8**입니다. **v11~v15 모드 실측·파생 수치는 CSV/MD로 저장되었고 아직 SQLite에는 통합하지 않았습니다.** v10 SQLite 전체 파일은 로컬에서 생성해 무결성을 검사했으며, GitHub에서는 [v10 SQL migration](data/migrations/v8_to_v10.sql)과 [재구성 스크립트](scripts/rebuild_v10_db.py)를 통해 복원합니다. GitHub에 v10 SQLite 바이너리가 업로드된 상태는 아닙니다.

다른 대화에서 이어갈 때는 v8 DB와 v10 migration, v9 연구 자료, 이 진행도 파일을 함께 기준으로 삼으세요.

## 새 채팅용 체크포인트

- **최신 v15:** [3D 모델 표현 방식 정량 비교](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md), 189모델·Handcrafted 22개 경로 그룹 신규 파생 통계. 면 선언 수는 최종 렌더 면이 아니며 bbox도 충돌체가 아님. 원본 자산 직접 검증 보류 상태 유지.

- 이전 v14: [텍스처 슬롯 바인딩 분석](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md) / [51건 CSV](research/furniture_mods/v14/handcrafted_texture_bindings_51.csv) / [기계판독 JSON](research/furniture_mods/v14/v14_binding_audit_summary.json). 이후 작업은 원본 face→PNG 검증.

- 최신: [v13 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md) · PNG 24/24 실화소·UV 13모델/571면 검사 완료(표본), 미완료는 재질의 실제 face 연결 및 인게임 검증.
- 이전: [v12 보고서](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md), [전체 120종 구조표](research/furniture_mods/v12/handcrafted_authored_120_total.csv), [5쌍 비교](research/furniture_mods/v12/another_vs_handcrafted_5_category_pairs.csv).
- 원본 모드 버전은 바닐라 1.21.11과 **상이**. 공식 클라이언트/인게임 검증을 완료 처리하지 않는다.
