# 학습 진행도

**새 채팅 인수인계:** [HANDOFF.md](HANDOFF.md) · [복사용 시작 프롬프트](docs/NEW_CHAT_START.md) · [현재 상태 JSON](handoff/STATE.json)

업데이트: 2026-11-12 / 체크포인트 v21

| 1단계 세부 작업 | 상태 | 수치 |
|---|---|---|
| 01. 바닐라 재질·텍스처 분석 | 표본 목표 달성 / 최종 검증 보류 | **150/150종, 표본 100%** |
| 02. 바닐라 3D 모델·블록 구조 분석 | 진행 중 | 대표 모델·UV·연결형·특수 렌더링 v5–v10 |
| 03. 가구 모드 3D 모델 분석 | **v21 원본 Another 블록 상태 12 SHA 대조·802 적용 추적, 새 완성형 leaf 38개 원본 JSON 검사** | Another 원형 69개 SHA 직접 재검증(v20), v18 leaf 33 + **v21 새 leaf 38 = 선정 leaf 71개**. 새 leaf 부모 21종/텍스처 override 97개. Handcrafted 원형 120/leaf 16, Macaw 원본 JAR 모델 **0**.
| 04. 가구 모드 텍스처·UV 분석 | **신규 Another PNG 14종/1,192면 UV 내부 원본 RGBA** | Another 누적 PNG **67종**, 모드 면 **1,996면**; Handcrafted PNG **24종**, 모드 면 **784면**. 모드 PNG 2종 합계 **91종**, UV 실화소 면 **2,780개**(선정 표본). 바닐라 의존 **Another dirt 8면 + Handcrafted oak_planks 2면** 및 인게임 미검증.
| 05. 바닐라 ↔ 가구 모드 비교 검증 | 사전 비교만 작성 / 최종 검증 미시작 | 두 모드의 의자·벤치·소파 5유형 구조 비교표 작성. 바닐라와의 인게임 비교는 미완료 |

**전체 완료:** 0/5개. 일부 체크포인트의 100%는 *표본 수 달성*만을 뜻하며 공식 JAR/인게임 재현까지 마쳤음을 의미하지 않습니다. 02번도 모집단이 확정되지 않아 임의 완료율을 산출하지 않습니다.

## 누적 근거 데이터 (v8 SQLite + v9 CSV + v10 SQL migration + v11~v21 모드 CSV)

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

- **v16 원본 직접 검증 확장:** 제작자 Handcrafted 고정 커밋에서 원본 JSON **30개**(16 leaf/14 부모) 직접 읽고 이전 v12 Git blob SHA와 일치 검증. v14에서 남았던 PNG **12개 원본**을 새로 디코딩해 **66,816픽셀** 실측(가시 7,358·투명 59,458·반투명 0). 완전 투명 PNG `bench/cushion/none_cushion`·`shelf/overlay/none` 2개. 원본 leaf 51슬롯 확인, 부모 geometry 면 **786 인스턴스** 중 **784 모드 면 모두 원본 PNG 이름·SHA·해상도·정수 UV 픽셀 격자·범위 대조 성공**, Minecraft 기본 텍스처 의존 2면 제외. [v16 보고서](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md), [모드 면별 재질 그룹 36](research/furniture_mods/v16/handcrafted_16_leaf_face_material_groups.csv), [PNG 12 추가 픽셀 CSV](research/furniture_mods/v16/handcrafted_12_new_png_pixel_metrics.csv). **개별 면 사각형의 실제 픽셀/알파 샘플링 및 인게임 검증은 미완료**. [원본 파일 로컬 재현 코드](scripts/reproduce_v16_handcrafted_originals.py) 추가: 문법 검사는 통과했으나 실제 고정 원본 체크아웃 환경에서 전체 실행 테스트는 미완료.

- **v17 새로운 면별 직접 검증:** 고정 Handcrafted 원본 PNG **24종을 다시 직접 디코딩**, v16에서 연결된 **784/784 모드 면**의 UV 영역 실제 RGBA 픽셀 분포 측정. **612 비영 UV/172 0면적, 420 전부 불투명/145 불투명·완전투명 혼합/47 전부 투명**, 총 **41,290 텍셀 사용 횟수(불투명 31,665/완전투명 9,625/부분 반투명 0)**. [v17 보고서](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md) · [784면 CSV](research/furniture_mods/v17/face_pixel_samples_784.csv) · [모델별/텍스처별 집계](research/furniture_mods/v17/) · [로컬 Pillow 독립 검증 코드](scripts/reproduce_v17_face_pixels.py). **코드의 원본 체크아웃 대상 end-to-end 실행은 미수행.** 원본 픽셀 출처 검증은 인게임 렌더 검증이 아님.

- **v18 Another Furniture 원본 직접 분석:** 제작자 1.21.1 커밋의 **leaf 33 JSON/템플릿 30 JSON, 총 63개**를 직접 읽고 이전 blob SHA와 모두 일치 검증. **93개 텍스처 override 슬롯**, 원형 709면, leaf에 상속 적용된 **807면의 실제 재질 경로** 확인(모드 804, 기본 dirt 3; 미해결 0). 최종 모드 PNG 고유 53경로 중 이전 실측 12 + **이번 신규 PNG 12종 실제 픽셀** = 24개 실측(45.28%), **29경로 미측정**. 새 PNG 3,072 픽셀에서 불투명 2,156·완전 투명 916·부분 알파 0; 4비트 팔레트 PNG `sofa/wood_2` 지원까지 보완. [v18 보고서](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md) · [면 재질 113그룹](research/furniture_mods/v18/another_face_material_groups_113.csv) · [PNG 12 실측](research/furniture_mods/v18/another_new_png_12_pixel_metrics.csv). **Another 807면의 실제 UV→PNG 화소 영역 검증은 아직 미수행.**

- **v19 Another Furniture 원본 PNG 29종·UV 면별 직접 RGBA 분석:** v18에서 고른 **leaf 33개**의 참조 모드 PNG 미측정 **29종을 제작자 고정 원본에서 새로 직접 디코딩**, 누적 Another **53/53 PNG 원본 실화소**(52종 16×16 / 1종 64×64). 원본 전체 **17,408픽셀**(불투명 **11,536**, 완전투명 **5,872**, 부분알파 0). 템플릿 **30종 원본 JSON을 새로 읽고 SHA 재확인**, 총 **807면의 실제 선언 UV**를 추출한 뒤 **Another PNG에 연결된 804/804면(선정 표본 100%)의 실제 원본 사각형 RGBA** 샘플링 완료. 모두 정수 픽셀 정렬/PNG 경계 안, 4면은 UV 면적 0. 비영 800면 중 **712면 전체 불투명, 88면 혼합, 전체투명 0면**. 중복 면·텍스처 사용 포함 텍셀 사용 **32,531회** 중 불투명 **31,545·투명 986·부분 알파 0**; UV 반전 **221모드 면**. [v19 전체 보고서](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md) · [53 PNG/원본 SHA](research/furniture_mods/v19/another_texture_53_png_source_manifest.csv) · [804면 실화소 CSV](research/furniture_mods/v19/another_804_face_actual_rgba.csv) · [33 가구별 집계](research/furniture_mods/v19/another_33_leaf_actual_rgba_summary.csv) · [두 모드 선정 표본만 비교한 보고서](research/furniture_mods/v19/00_v19_모드간실제면UV픽셀_선정표본비교.md). **모드 전체 전수/바닐라 의존 3면·인게임 렌더·독립 로컬 PNG 재실행은 아직 미완료**.

- **v20 Another 원형 원본 JSON 69/69 직접 재조회:** 제작자 1.21.1 고정 커밋에서 **기존 v11 69 원형 모두** 파일을 다시 읽어 **Git blob SHA·요소 수·명시 면 수 전부 일치**. v18 선정 원형 30 이외 **39개를 새로 직접 자세히 조사**, 총 **299 요소, 1,362 원본 선언 면**의 UV·회전·0두께·raw bbox·cullface 원본 데이터를 저장. **UV 반전 422면 / UV 회전 134면 / cullface 443면 / 0면적 UV 4면 / 회전 요소 17개 / 0두께 요소 34개 / 0~16 외부 원시 bbox 요소 11개(3개 템플릿)**. [전체 상세 보고서](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md) · [69 원형 CSV](research/furniture_mods/v20/another_69_templates_direct_original_geometry.csv) · [1,362 원시 면 CSV](research/furniture_mods/v20/another_69_templates_1362_original_faces.csv) · [SHA 감사 JSON](research/furniture_mods/v20/v20_another_69_original_template_audit.json). Macaw's Furniture 공식 1.21.11 Fabric 3.4.2 배포는 확인했으나 **현재 실행 환경에서 JAR을 다운로드하지 못했으므로 모델 실측 0건**. 이 69 모델은 이미 v11에서 선정한 **원형 표본 전수**로 전체 모드 모델 전수 아님. PNG 실화소 누적 **Another 53 + Handcrafted 24 = 77개** 그대로, 새 39 원형의 재질별 PNG 실측 추가 0. 공식 1.21.11 바닐라/인게임/전체 모드 검증 미완료.

- **v21 Another 블록 상태 기반 신규 38 leaf 원본/PNG 실제 화소 확장:** 제작자 1.21.1 고정 커밋의 **12 블록 상태 JSON SHA 직접 재확인**, **802개 model apply / 고유 114 경로**(그중 Minecraft air 모델 2 apply). v18 선정 33 leaf에 없고 shutter variant 43경로를 제외한 **새 완성형 38개 원본 JSON**을 이번에 직접 읽고 자체 0 elements/원형 부모 21종/override 97슬롯 확인. 새 leaf 상속 face **1,197인스턴스(모드 1,192/바닐라 dirt 5)**, 모드 PNG 원본 **34종** 직접 디코딩(기존 v19 20종 재조회 SHA 일치, **신규 14종 픽셀**). **1,192/1,192면의 실제 원본 UV 사각형 내부 RGBA 전수 샘플**(불투명 1,086면, 혼합 106면, 0면적/전체투명 0). 누적 **Another 선택 leaf 71종, 원본 PNG 67종, 모드 면 RGBA 1,996개**. Handcrafted 합쳐 **고유 PNG 91종/UV 면 2,780인스턴스**. [v21 보고서](research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md) · [신규 38 leaf 재질 면](research/furniture_mods/v21/another_new_38_leaf_face_resolution.csv) · [신규 14 PNG 원본 화소](research/furniture_mods/v21/another_new_14_png_unique_source_metrics.csv) · [원본 1,192 면별 RGB·알파 CSV](research/furniture_mods/v21/another_new_38_leaf_all_rgba_1192.csv) · [감사 JSON](research/furniture_mods/v21/v21_blockstate_new_leaf_rgba_audit.json). **모드 전체 전수 아님**, 바닐라 dirt 미검증 총 **8면**, Handcrafted oak_planks **2면**, 공식 Macaw JAR 직접 실측 **0건** 및 인게임 미검증.

## 다음 과제

1. Minecraft Java 1.21.11 공식 `client.jar`와 비공식 미러 자료의 바이트/해시 비교. [로컬 검사 스크립트](scripts/verify_official_jar.py) 및 [사용법](docs/official_client_jar_검증방법.md) 준비 완료(실제 JAR 미실행).
2. 실제 게임에서 잔디·잎의 색 변형, 투명도, 모델 조립 결과 검증.
3. [v10 통합 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md) 및 [v9 특수 모델 자료](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md)의 공식 클라이언트·인게임 교차검증 후 02번 종료 여부 판정.
4. **03번 v12에서 Handcrafted 원형 120개 분석까지 완료:** 검증된 Macaw's Furniture 공식 1.21.11 배포 JAR(또는 공식 소스)을 확보하면 모델 구조를 직접 분석한다. 불확실한 제3자 복제본을 쓰지 않는다.
5. **v21 원본 블록 상태 12개를 통해 기존 leaf 33 이외 새로운 leaf 38과 추가 부모 19종/원본 PNG 14종을 직접 연결하고, 새 모드 면 1,192개의 RGBA 실측 완료**. 다음은 공식 Macaw JAR, Minecraft 1.21.11 client.jar의 dirt 8면/oak_planks 2면, shutter 43개 남은 경로와 모드 전체 표본 확대, 인게임 실제 렌더 확인이다.

**주의:** GitHub에 추적된 SQLite 바이너리는 **v8**입니다. **v11~v21 모드 실측·파생 수치는 CSV/MD로 저장되었고 아직 SQLite에는 통합하지 않았습니다.** v10 SQLite 전체 파일은 로컬에서 생성해 무결성을 검사했으며, GitHub에서는 [v10 SQL migration](data/migrations/v8_to_v10.sql)과 [재구성 스크립트](scripts/rebuild_v10_db.py)를 통해 복원합니다. GitHub에 v10 SQLite 바이너리가 업로드된 상태는 아닙니다.

다른 대화에서 이어갈 때는 v8 DB와 v10 migration, v9 연구 자료, 이 진행도 파일을 함께 기준으로 삼으세요.

## 새 채팅용 체크포인트

- **최신 v21:** [블록 상태 12 SHA/802 model apply, 신규 leaf 38 JSON, 14 새 PNG와 1,192모드 면 실화소 보고서](research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md). **Another 71 leaf/PNG 67/모드 면 1,996**, Handcrafted PNG 24/모드 면 784 누적. 바닐라 dirt 8면/oak_planks 2면 및 Macaw 원본 0건/인게임 미검증. **최종 완료 0/5**.


- 이전 v20: [제작자 Another 원형 69개 전체 JSON SHA 재검증/1,362면 직접 UV·기하 실측](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md). 이 69는 v11 원형 선정 표본(모드 전체 원본 모델 1,451개 파일과 다름). Macaw 공식 1.21.11 Fabric 릴리스 존재는 확인했으나 **JAR 원본 바이너리 확보 실패, 실제 모델 조사 0**. 상위 1단계 확정 완료 **0/5**.


- 이전 v19: [Another 선정 33 leaf가 참조한 고유 PNG 53/53종과 모드 면 UV 실제 RGBA 804/804면 전체 분석](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md). **선정된 표본만 100%**이고 바닐라·인게임·Macaw·전체 모드 전수는 미검증. 5개 작업 **최종 완료 0/5**.


- 이전 v18: [Another Furniture 원본 모델 63개·807면 텍스처 경로·신규 PNG 12종 직접 픽셀 분석](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md), 24/53 참조된 모드 PNG 경로 실화소(45.28%). 이 표본 검증률은 **전체 프로젝트 완료율이 아니다**. 전체 확정 완료 0/5.

- 이전 v17: [고정 원본 PNG 24종과 Handcrafted 면별 784/784 RGBA 분석](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md). **표본 목표 100%**이지만 공식 client.jar/인게임/타 모드 전수는 미완료. **전체 5개 단계 최종 완료 0/5**.

- 이전 v16: [원본 12 PNG/30 JSON/786 면 인스턴스 보고서](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md), 원본 PNG 누락 표본 해결. 남은 검증은 면 사각형 실제 화소 샘플링·바닐라 2면·게임 렌더. 5개 세부 작업 최종 완료 0/5.

- 이전 v15: [3D 모델 표현 방식 정량 비교](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md), 189모델·Handcrafted 22개 경로 그룹 신규 파생 통계. 면 선언 수는 최종 렌더 면이 아니며 bbox도 충돌체가 아님. 원본 자산 직접 검증 보류 상태 유지.

- 이전 v14: [텍스처 슬롯 바인딩 분석](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md) / [51건 CSV](research/furniture_mods/v14/handcrafted_texture_bindings_51.csv) / [기계판독 JSON](research/furniture_mods/v14/v14_binding_audit_summary.json). 이후 작업은 원본 face→PNG 검증.

- 최신: [v13 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md) · PNG 24/24 실화소·UV 13모델/571면 검사 완료(표본), 미완료는 재질의 실제 face 연결 및 인게임 검증.
- 이전: [v12 보고서](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md), [전체 120종 구조표](research/furniture_mods/v12/handcrafted_authored_120_total.csv), [5쌍 비교](research/furniture_mods/v12/another_vs_handcrafted_5_category_pairs.csv).
- 원본 모드 버전은 바닐라 1.21.11과 **상이**. 공식 클라이언트/인게임 검증을 완료 처리하지 않는다.
