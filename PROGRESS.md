# 학습 진행도

**새 채팅 인수인계:** [HANDOFF.md](HANDOFF.md) · [복사용 시작 프롬프트](docs/NEW_CHAT_START.md) · [현재 상태 JSON](handoff/STATE.json)

업데이트: 2026-11-13 / 체크포인트 v27

| 1단계 세부 작업 | 상태 | 수치 |
|---|---|---|
| 01. 바닐라 재질·텍스처 분석 | 기존 표본 달성 + **v27 새 5 PNG 전체 RGBA 조사** / 최종 검증 보류 | 150/150 기존 표본, v26 원본 PNG8/8,704픽셀 + v27 새 PNG5/2,048픽셀(이 중 `oak_shelf` v4 표본과 중복), 공식 JAR/인게임 보류 |
| 02. 바닐라 3D 모델·블록 구조 분석 | **v27 선반 상태+명시 UV/퇴비통 유도 UV 확대** | v26 명시 UV 36면/70프레임; v27 **선반 명시 UV20면 + 퇴비통 유도 UV26면**, 5,072 텍셀 사용, UV 좌표식 23/23 명시 참조일치. 공식 JAR/인게임 보류 |
| 03. 가구 모드 3D 모델 분석 | **v24 Another 의자 leaf 39개 원본 JSON/SHA 확인, 원형 구조 비교** | 선정 Another leaf **204**(165+39), 새 10 상태 Another 경로 **91/91**, 블록 상태 **22/177** 유지; Handcrafted 원형120/leaf16, Macaw 0. |
| 04. 가구 모드 텍스처·UV 분석 | **v23 화소 실측 누계 유지 (v24 신규 PNG/RGBA 0)** | Another PNG **151종/실제 UV RGBA 3,329면**, Handcrafted **24종/784면**. 합계 **175 PNG/4,113면**. v24 구조상 상속 1,794면은 PNG 실화소로 미검증. |
| 05. 바닐라 ↔ 가구 모드 비교 검증 | 사전 비교만 작성 / 최종 검증 미시작 | 두 모드의 의자·벤치·소파 5유형 구조 비교표 작성. 바닐라와의 인게임 비교는 미완료 |

**전체 완료:** 0/5개. 일부 체크포인트의 100%는 *표본 수 달성*만을 뜻하며 공식 JAR/인게임 재현까지 마쳤음을 의미하지 않습니다. 02번도 모집단이 확정되지 않아 임의 완료율을 산출하지 않습니다.

## v27 (2026-11-13) — 바닐라 32×32 선반/자동 UV 퇴비통 화소 및 상태 교차 검증

- [v27 원본 전체 보고서](research/vanilla_models/v27/00_v27_선반32x32_퇴비통자동UV_원본화소검증보고서.md) · 연구 CSV **8개**, 요약 JSON 1개를 별도 저장.
- PNG **5경로 새로 전체 RGB·알파 조사**, 2,048픽셀 **불투명1,824/투명224**. `oak_shelf` 32×32 한 종은 기존 v4 텍스처 150 표본과 중복. 기존 v26 `composter_top`은 신규 계수 제외.
- 선반 템플릿 **6개 원본**의 **명시 UV 20면** 실제 `oak_shelf.png` 영역 픽셀 **1,376회** 조사. `oak_shelf` 블록 상태 **24 multipart 원본 규칙**으로 32개 합성 상태의 본체+전면 **2경로/방향회전 일치 32/32** 계산.
- 퇴비통 본체 18면+내용물 8면 = **26 암시 UV**를 유도 좌표식에 따라 샘플한 **3,696회 실제 PNG 텍셀**. 계산식의 입력은 원본 요소 from/to, 직교 6방향이며 동일 버전 `stairs/slab/fence_post` 명시 UV **23/23 숫자·순서 일치**로 정합성 점검. **공식 엔진/인게임 UV 검증을 수행한 것은 아님**.
- 이번 v27의 **명시 20 + 유도 26 = 46면/5,072 텍셀 사용**은 전부 불투명한 소스 픽셀에 놓이지만, 전체 PNG에는 투명 픽셀이 존재하는 등 UV 선택 효과가 뚜렷함. 기존 v26 70프레임/36면과 중복 계수 유의.
- 미러 PNG SHA **5/5** 동일, v4 `oak_shelf` 파일·차원·픽셀/가시/색수 **1/1** 동일. 공식 JAR/인게임/CRC·독립 Pillow 미검증.
- **01·02 지속 진행, 03·04 v24 누적 유지, 05 미완료 / 최종 0/5**.

## v26 (2026-11-13) — 바닐라 원본 PNG 8종·면 36개/애니 프레임 70건 RGBA 직접 검증

- [v26 바닐라 PNG 실화소·UV 면 분석](research/vanilla_models/v26/00_v26_바닐라8PNG_전체RGBA_36면70프레임_실화소보고서.md) 및 파생 CSV **4개**와 기계 요약 JSON 저장. 기존 바닐라 v4/v10·모드 v24 연구 결과와 분리.
- v25에서 IHDR만 검사한 **같은 PNG 8종을 실제 zlib/PNG 압축 역해독**하여 **8,704 RGBA 픽셀 (불투명 4,422·완전 투명 4,282·부분 알파 0)** 측정. 본 단계 PNG 수가 기존 150 표본에 모두 추가되는 것은 아님: **3종은 v4에 이미 포함**.
- 명시 UV를 가진 모델 **6개/고유 면 36개**의 PNG 실제 사각형 조사, 애니메이션 3프레임 포함 **70개 기록**. UV 영역 픽셀 사용 **3,652회(불투명 3,424·완전 투명 228)**. 19건은 반전 UV. 이 사용 횟수는 고유 픽셀 수/인게임 화면 픽셀 수가 아님.
- 이전 v4 실측 3종은 **파일 바이트/크기/가시·전체 픽셀 수 3/3 일치**, 기존 공개 비공식 미러 PNG와 Git blob SHA **8/8 일치**. 자체 PNG chunk CRC/Adler32 및 Pillow 독립 전체 재검증은 미수행; **공식 Mojang JAR/인게임 검증은 미완료**.
- 최종 완료 **0/5**; 다음은 바닐라 01/02의 공식 검증, 암시적 UV·상태 회전, 추가 대표 모델. **모드 연구 지표 변경 없음.**

## v25 (2026-11-13) — 바닐라 원본 자료 직접 연구 재개

- [v25 원본 감사 보고서](research/vanilla_models/v25/00_v25_바닐라원본_모델상속상태PNG_직접검증보고서.md) 및 8개 파생 CSV와 기계 요약 JSON 게시.
- 사용자 제공 `1.21.11/assets/minecraft/`에서 **모델 JSON 32개, 상태 JSON 8개, PNG 8개, png.mcmeta 2개 = 50파일 직접 읽기**. 자체 기하 8모델 **44요소/204선언면**, 별도로 상태 8종 **79 variants/9 multipart/27 모델 참조 경로**; 퇴비통 8개 상태별 내용물 y상단 3~15, 8 leaf 상속 **11요소/57면 인스턴스**.
- PNG8종 원본 **IHDR 바이트 확인**, 16×48 톱날/랜턴 애니메이션 메타 확인. 새 PNG **전체 화소 분포/면 UV 내부 RGBA 0건**; 6개 업로드 에셋과 이전 1.21.11 비공식 미러의 Git blob SHA **6/6 일치**. **Mojang 공식 client.jar 인증·인게임 렌더 확인은 아니다.**
- `1.21.11` 원본 자료가 현재 public repo에 존재하므로 원본 재배포 정책/저작권 점검 필요. 이번 v25 결과에는 원본 게임 JSON·PNG·JAR를 별도 복제하지 않았음.
- 01의 기존 **150/150 표본** 유지, 02 **진행 중**, 03/04 모드 v24 누적 수치 변경 없음, 05 미완료. 최종 확정 완료 **0/5**. 다음은 **바닐라 01·02 우선**.

## 누적 근거 데이터 (v8 SQLite + v9 CSV + v10 SQL migration + v11~v24 모드 CSV + v25 바닐라 CSV)

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

- **v22 Another 셔터 원본 leaf 43개·새 PNG 42종·214면 실제 UV RGBA:** v21의 12 원본 블록 상태 802 적용/114 고유 모델 경로 중, 이미 읽은 셔터 `variant_1/oak_single`을 제외한 **셔터 leaf 43개 원본 JSON 직접 읽기·Git SHA 기록**. 4 부모 원형을 상속한 **214모드 면**, texture/UV 해석 **214/214**. 제작자 원본 PNG **43종 직접 디코딩**(기존 1종 SHA 재검사, **새 42종**), PNG 16×16 RGBA8 전체 **11,008픽셀 모두 불투명**, **214개 실제 UV 사각형도 전부 불투명**; UV 반전 75/회전 42, 0면적 0. [v22 상세 보고서](research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md) · [43 leaf 214면 재질 해석](research/furniture_mods/v22/shutter_43_leaf_resolved_source_face_uv.csv) · [43 PNG 전체 픽셀/해시](research/furniture_mods/v22/shutter_43_png_original_source_manifest.csv) · [214면 UV 픽셀](research/furniture_mods/v22/shutter_214_face_uv_original_rgba.csv) · [감사 JSON](research/furniture_mods/v22/v22_shutter_source_original_complete_audit.json). 누적 Another **leaf 114개/고유 PNG 109종/모드 면 2,210개**, Handcrafted 합계 **PNG 133종/모드 면 2,994개**. **이전 블록 상태 12개가 참조한 Another 모델 경로 113/113 원본 근거 완료**(111 leaf, 2 template; 별도 minecraft air 1 경로). 모드 전체 상태/모델 전수 아님. 바닐라 dirt 8면/oak_planks 2면, Macaw 공식 JAR/인게임 검증 미완료; 완료 판정 0/5.

- **v23 Another 블록 상태 10개·신규 leaf 51개·원본 PNG 42종/UV RGBA 1,119면 직접 검증:** 제작자 1.21.1 고정 원본에서 이전 12개 밖 **10개 새 blockstate JSON을 SHA/실제 variants·multipart 386 apply**로 확인(고유 경로 92, Another 91 + air 1). 벤치·소파·커튼·서랍·테이블·꽃상자·2종 의자 등 **51개 새 leaf JSON 직접 읽기(모두 자체 elements 0, 부모 원형 34종, 서랍 2단계 상속)**. 인스턴스 면 **1,127개** 중 Another PNG 면 **1,119/1,119 실제 UV RGBA**·바닐라 dirt **8면**(공식 PNG 미검증). 원본 PNG 51종 직접 디코딩(**새 42종/기존 9종 SHA 재검사**). 새 모드 면 전부 불투명 **1,063**, 혼합 **56**, 부분알파 0. 중복 포함 원본 PNG UV 텍셀 **41,666회** 중 불투명 39,304/투명 2,362. **누적 Another blockstate 22/177, leaf 165, PNG 151종, 모드 UV RGBA 3,329면**, Handcrafted 포함 **PNG 175종·모드 면 4,113개**. 자작/가문비 벤치 및 의자, 빨강/파랑 소파의 부모·UV 기하 동일/PNG 교체를 원본 면 쌍으로 검사. [v23 보고서](research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md) · [새 10 상태](research/furniture_mods/v23/new_10_blockstates_author_original_audit.csv) · [51 leaf 원본 face 상속](research/furniture_mods/v23/new_51_leaf_source_face_texture_resolution.csv) · [신규 42 PNG SHA](research/furniture_mods/v23/new_42_png_first_measured_in_v23.csv) · [원본 1,119면 직접 RGBA CSV](research/furniture_mods/v23/new_51_leaf_all_1119_face_actual_rgba.csv) · [감사 JSON](research/furniture_mods/v23/v23_new_blockstate_leaf_png_face_original_audit.json). 신규 10 상태에 남은 **39개 의자 leaf JSON**·그 외 블록 상태 **155개**·공식 바닐라/Macaw/인게임 미검증. 전체 0/5.

- **v24 신규 실측:** 제작자 원본 의자 **39개 leaf JSON/Git SHA** 직접 조사·부모 2 원형 재조회. 일반형 19/tucked 20, own elements 0, override 117, **390 요소·1,794 선언 면 인스턴스**. 두 부모 10요소의 raw z 좌표가 -9 이동하고 46면 UV 선언은 동일. 새 10 상태 Another 경로 91/91 원본 확인; 누적 Another leaf 204. **이번 PNG 실제 픽셀/UV 내부 RGBA 새 측정 0**, 기존 모드 누계 유지. [v24 보고서](research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md) · [39모델 SHA CSV](research/furniture_mods/v24/chair_remaining_39_original_json_geometry_audit.csv).

**v24 추가 교차검산:** 제작자 원본 `birch_chair`·`spruce_chair` 두 블록 상태 모두 `south + variant=3 + not tucked`에서 등받이 `*_3` 대신 `*_1` 모델 참조를 직접 확인. 전체 의자 apply 176 중 신규 39 leaf 적용 **155**(다른 기존 5 leaf 21). 기존 횟수 균일 가정 156에서 정정했으며 최종 원본 SHA·회전 분포 대조 완료. 게임 동작/의도 여부 미확정.

## 다음 과제

1. Minecraft Java 1.21.11 공식 `client.jar`와 비공식 미러 자료의 바이트/해시 비교. [로컬 검사 스크립트](scripts/verify_official_jar.py) 및 [사용법](docs/official_client_jar_검증방법.md) 준비 완료(실제 JAR 미실행).
2. 실제 게임에서 잔디·잎의 색 변형, 투명도, 모델 조립 결과 검증.
3. [v10 통합 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md) 및 [v9 특수 모델 자료](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md)의 공식 클라이언트·인게임 교차검증 후 02번 종료 여부 판정.
4. **03번 v12에서 Handcrafted 원형 120개 분석까지 완료:** 검증된 Macaw's Furniture 공식 1.21.11 배포 JAR(또는 공식 소스)을 확보하면 모델 구조를 직접 분석한다. 불확실한 제3자 복제본을 쓰지 않는다.
5. **v23 새 블록 상태 10개 원본·51개 leaf JSON·PNG 새 42종/모드 면 1,119개 실제 RGB·알파 검증 완료**, 누적 상태 22/177. 다음은 v24에서 확인한 39개 의자 leaf의 **PNG 실화소와 1,794면 UV** 및 조사 밖 **155개 블록 상태**, Macaw 공식 JAR, Mojang 공식 1.21.11 client.jar의 dirt 16면/oak_planks 2면, 독립/인게임 검증이다.

**주의:** GitHub에 추적된 SQLite 바이너리는 **v8**입니다. **v11~v23 모드 실측·파생 수치는 CSV/MD로 저장되었고 아직 SQLite에는 통합하지 않았습니다.** v10 SQLite 전체 파일은 로컬에서 생성해 무결성을 검사했으며, GitHub에서는 [v10 SQL migration](data/migrations/v8_to_v10.sql)과 [재구성 스크립트](scripts/rebuild_v10_db.py)를 통해 복원합니다. GitHub에 v10 SQLite 바이너리가 업로드된 상태는 아닙니다.

다른 대화에서 이어갈 때는 v8 DB와 v10 migration, v9 연구 자료, 이 진행도 파일을 함께 기준으로 삼으세요.

## 새 채팅용 체크포인트

- **최신 v24:** [의자 39개 신규 원본 JSON/SHA·2부모 상속 기하 보고서](research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md). Another leaf **204종**, 해당 신규 10상태의 Another 모델 JSON **91/91**. 블록 상태 22/177 유지. 이번 단계 신규 PNG 화소/UV RGBA 0건 → 전체 두 모드 PNG175/실제 모드 면4,113 변동 없음. 다음은 24 참조 PNG 경로와 과거 manifest 차집합·원본 화소 검사.


- **이전 v23:** [Another 새 10 상태/51 leaf 원본 JSON/PNG 신규 42종/1,119면 원본 UV RGBA 검증](research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md). 누적 Another **leaf165/PNG151/모드 면3,329**, Handcrafted 합산 **PNG175종/모드 면4,113**. 블록 상태 **22/177**, 신규 10 상태에 남은 원본 의자 leaf39개. 공식 Macaw/바닐라 JAR/인게임 미검증, 전체 최종 0/5.


- 이전 v22: [Another 셔터 leaf 43개 원본 JSON/새 PNG 42종/214면 UV 실제 RGBA 검증](research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md). 누적 Another leaf **114개/PNG 109종/면 2,210**, Handcrafted 포함 **PNG 133종/면 2,994**. 블록 상태 12개 내부 Another 모델 참조 113/113 원본 확보. **Macaw 공식 JAR/바닐라 공식 JAR/인게임 미검증, 전체 0/5**.


- 이전 v21: [블록 상태 12 SHA/802 model apply, 신규 leaf 38 JSON, 14 새 PNG와 1,192모드 면 실화소 보고서](research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md). **Another 71 leaf/PNG 67/모드 면 1,996**, Handcrafted PNG 24/모드 면 784 누적. 바닐라 dirt 8면/oak_planks 2면 및 Macaw 원본 0건/인게임 미검증. **최종 완료 0/5**.


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
