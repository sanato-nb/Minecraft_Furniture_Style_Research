# 출처, 저작권 및 검증 한계
## 전역 최신 체크포인트 v41 — 석재·벽돌 R017 완료 반영, 11단계·150종 통합 유지

> **2026-11-14 KST · 통합 `INT-1-1-20261114-01`.** 이 문단의 v41 연구 상태/작업 범위가 아래의 v40/v39/v38 역사적 기록보다 우선한다. 기존 보고서와 독립 단계 파일은 삭제·수정하지 않았다.

- **[v41 통합 보고서](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/REPORT.md) · [11단계 원장](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/STAGE_INTEGRATION_LEDGER.csv) · [150종 텍스처 원장](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/TEXTURE_150_SCOPE_LEDGER.csv) · [SHA 매니페스트](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/MANIFEST.json) · [검증 결과](research/vanilla_textures/integrations/v41_INT-1-1-11steps_150_R017_REFRESH/VALIDATION.json)**.
- 통합 범위: **11/11 단계, 150/150개 고정 `texture_id`**, 누락/중복 0개. **소스 연구 완료 10/11단계, 132/150 (88%)**. 서로 다른 지표이며 **마지막 미종결은 `1-1-01` 목재·원목 18개**.
- 석재·벽돌 **`1-1-02`의 전역 기준을 `TEX02-R015 → TEX02-R017`로 갱신**하고 독립 소스 검증 완료 **0/17 → 17/17**을 반영. 19개 모델·7개 부모·31개 블록상태 선택·186개 face→sprite 연결은 R017 근거이며 실제 Minecraft 게임 렌더 인증을 뜻하지 않는다.
- 원래 **v40은 11단계/150종이지만 석재 R015 고정(당시 소스 완료 115/150)**이었으며, v41은 **132/150**을 기준으로 새 통합 원장을 발행했다. v39(10단계 133종)와 v40 모두 **불변 보존**. 새로운 원본 PNG/JSON 분석 측정 0건.
- 상위 1단계의 5개 하위 연구 과제 최종 완료 **0/5 유지**, 실제 가구 모델 제작/좀보이드 맵 변환 포함되지 않음. `1-1-01`의 소스 완료가 확정되기 전까지 **1-1 소스 연구 100%라고 주장하지 말 것**.
- 사용자 추출 `1.21.11/` 게임 파일 최우선. **Mojang 공식 JAR SHA1 인증 및 실제 인게임 렌더 검증은 완료 필수조건에서 제외**(인증/실측한 사실은 없음). 애니메이션 소스 연구 **9개 단계 재개, 1-1-02·1-1-10 보류**. 과거의 전면 애니메이션 보류와 공식 인증 대기 문구는 작성 당시 역사적 기록으로 간주한다.
- 석재 이외 개별 TEX 단계의 버전·Git SHA는 v40과 동일. 이후 신규 TEX 증거가 생기면 전역 v41에 자동으로 편입되지 않으며 별도 v42 통합 필요.


## 최신 전역 v39 — 1-1 바닐라 재질 10개 통합, 석재·벽돌(1-1-02) 제외

> **2026-11-13 KST**, 통합 ID `INT-1-1-20261113-01`. **본 문단은 아래의 v38·v35·R000 초기 작업 지시보다 최신이며 범위/우선순위에서 앞선다.** 기존 역사적 문서는 삭제하지 않음.

- **통합 결과:** [v39 10개 재질/133개 텍스처 통합 보고서](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/REPORT.md) · [포함 10개/제외 1개 단계 원장](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/STAGE_INTEGRATION_LEDGER.csv) · [133개 대상별 출처 원장](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/TEXTURE_133_SCOPE_LEDGER.csv) · [SHA 고정 매니페스트](research/vanilla_textures/integrations/v39_INT-1-1-10steps_133/MANIFEST.json).
- **10개 단계(1-1-01, 03–11) / 대상 133개 고정 `texture_id`를 전역 통합**. 제외한 **1-1-02 석재·벽돌 17개(`TEX02-R015` 기준)**는 삭제/폐기가 아니라 미통합. v4의 150개 역사적 표본 전체는 그대로. **133/150은 통합 범위이며 전체 완료율이 아님**, 통합 중 신규 PNG 실측 0.
- 독립 연구 최종 리비전은 각 채팅별 `TEXnn-Rxxx`로 계속 유지하며, 이 **전역 v39**는 고정 시점 연구 결과를 연결한 버전. **상위 1단계 최종 완료 0/5**, 1-1 전체 완성 선언 없음.
- 사용자 제공 `1.21.11/` JAR 추출본 우선, 비공식 미러는 교차용. **공식 압축 JAR SHA-1 인증과 인게임 시각/런타임 검증은 사용자 지시에 따라 필수 완료 조건에서 제외**(실제 인증/관찰 성공을 뜻하지 않음). 게임 원본의 공개 재배포 권리 확인 또한 별개.
- 애니메이션 **소스 연구는 1-1-01,03,04,05,06,07,08,09,11에서 사용자 지시로 재개**. **1-1-10 잎·식생은 최신 독립 STATE 기준 보류**. 아래 이전 문단의 '애니메이션 전면 보류'는 예전 지시 기록으로 읽고 최신 단계별 상태를 우선. 실행/런타임 효과는 별도 증거 없으면 완료 주장 금지.
- Project Zomboid 변환·실제 가구 3D 제작은 범위 밖. 과거 Another Furniture/Handcrafted, 바닐라 모델 연구, 원본 파일 및 v38 데이터는 보존.



## 사용자 최신 범위 지시 — 애니메이션 일시 보류 (2026-11-13)

**사용자 최신 작업 지시(2026-11-13): 애니메이션 분석은 일단 보류.** 새로운 애니메이션 프레임 해독, 키프레임·클립 분석, 움직임 재현 및 애니메이션 인게임 검증을 진행하지 않는다. 기존 v9/v26/v31 애니메이션 관련 기록은 삭제하지 않고 보존하되, 새로운 진행도에 포함하지 않는다. 우선순위는 **정적 바닐라 3D 모델·기하·텍스처·UV·블록 상태·정적 렌더링 검증·공식 원본 무결성**이다. 애니메이션 연구는 사용자가 명시적으로 재개를 요청할 때까지 유지 보류.

기존 v9/v26/v31에 포함된 애니메이션 관련 소스·표본 데이터는 **과거 조사 증거**로 유지한다. 이 지시는 과거의 측정 사실을 취소하지 않으며, 새 분석부터 동적 프레임 검사·연출·키프레임 연구를 제외한다.


## v38 최신 — 참나무 선반 7 leaf/7 template·32 정적 상태·38 UV 원본 실화소 (2026-11-13)

- [v38 오크 선반 상세 보고서](research/vanilla_models/v38/00_v38_오크선반7리프7부모_32상태_38UV실화소분석.md) · [리프/부모 7+7 SHA·기하](research/vanilla_models/v38/01_oak_shelf_7_leaf_7_template_source_sha_geometry.csv) · [원본 38 UV면](research/vanilla_models/v38/02_oak_shelf_38_original_declared_faces_explicit_uv.csv) · [24 multipart 규칙](research/vanilla_models/v38/03_oak_shelf_24_original_blockstate_multipart_rules.csv) · [32 상태 전수 평가](research/vanilla_models/v38/04_oak_shelf_32_static_blockstate_combinations_evaluated.csv) · [2 PNG 원본 검사](research/vanilla_models/v38/05_oak_shelf_2_original_png_pillow_rgba_crc_sha.csv) · [38면 전 화소 실측](research/vanilla_models/v38/06_oak_shelf_38_face_original_png_uv_rgba_regions.csv).
- v36 P1 544 후보 중 `oak_shelf` **7 leaf를 직접 원본 SHA 확인**(v36 일치 7/7), 템플릿 7 부모·공통 block 부모·블록 상태 1·item 에셋 1 확인. v35~v38 **선택 리프 신규 직접 검사 28개**(v35 15, v36 6, v38 7), 다만 v5~v34와 전체 중복 대조를 마친 완료율은 아님.
- 부모 원본 선언 **11 elements/38 faces**(7개 모델 합), **38/38 explicit UV**, UV X반전 8/Y반전 8, `cullface` 23, 0두께 앞면 패널 5. 한 월드 상태에서는 본체 3요소·15면 + 전면 1요소·1면 = **4요소·16면**, inventory 모델 별도 3요소·18면. 얕은 본체 깊이 z11–16 = 5/16블록.
- `multipart` 소스 **24 규칙** / 소스 속성 `facing` 4 × `powered` 2 × `side_chain` 4 = **32 조합 모두 정확히 본체+전면 패널 2모델** 선택됨. 실제 게임에서의 모든 상태 전이 가능성/정적 렌더 결과는 미검증.
- 원본 PNG 2개 `oak_shelf` 32×32 + `stripped_oak_log` 16×16을 **Pillow 전체 RGBA·PNG CRC로 독립 검사, 원본 1,280픽셀 전부 불투명**, v34 PNG SHA 2/2 일치. 38면 전부 `oak_shelf.png` 한 장 사용 (`stripped_oak_log`는 `#particle` 전용); 원본 UV 크롭 실제 **2,304 texel-uses 모두 불투명**, 고유 UV 사각형 19종(중복 포함 사용횟수와 원본 픽셀 수 구별).
- 공식 Mojang client.jar 무결성·실제 게임 UV/정적 연결 표시·컬링·조명 검증 **미완료**. 애니메이션 계속 보류, 기존 v24 가구 모드 누계·역사 자료 보존, 상위 1단계 5개 세부과제 완료 **0/5**, P1/프로젝트 완료율 미계산.

## v37 이전 체크포인트 — 정적 원본 PNG·기하 UV 근거 연결 (2026-11-13)

- [v37 실제 원본 화소·UV 검증 보고서](research/vanilla_models/v37/00_v37_화로용광로훈연기_정적11PNG_34면실화소_분석보고서.md) · [정적 원본 PNG11종 CRC·Adler·RGBA](research/vanilla_models/v37/01_eleven_static_png_original_rgba_crc_adler.csv) · [34면 실화소/2면 애니메이션 보류](research/vanilla_models/v37/02_six_leaf_36_face_material_static_png_rgba_vs_deferred.csv) · [요약 JSON](research/vanilla_models/v37/v37_static_furnaces_png_pixels_summary.json).
- v36 원본 화로·용광로·훈연기 6 leaf의 텍스처 참조 13종 중 **정적 11 PNG 파일 원본 바이너리 전체 RGBA 2,816픽셀을 직접 해독**(불투명2,816/투명0/반투명0). v34 원본 PNG SHA 11/11 일치, 모든 PNG 청크 CRC32 및 zlib Adler32 검증 성공.
- v36의 **36 face×material 적용 행 중 34면**에 원본 정적 PNG 실제 픽셀을 연결한 유도 UV 텍셀 사용 **8,704회 전부 불투명**. 이 34행은 공통 cube의 6고유 선언면과 다른 개념이며 원본의 미명시 UV를 추론한 영역이므로 엔진 방향·컬링 검증이 아님.
- 화로 고정 정면 PNG의 꺼짐/켜짐 비교: **RGBA 36/256 위치 차이, RGB 36/256, 알파 0/256**(정적 텍스처 비교, 애니메이션 아님). 다중 프레임 참조 `blast_furnace_front_on`, `smoker_front_on` **2 PNG/2면은 이미지 프레임 분석 보류 유지**.
- 이번 조사에는 **독립 Python/Pillow 재검산 및 공식 Mojang 1.21.11 client.jar/실제 인게임 UV·조명·컬링 검증 없음**. v24 모드와 과거 애니메이션 조사자료 보존, 전체 5 세부 과제 완료 **0/5**, P1/프로젝트 완료 퍼센트 미계산.

## v36 출처와 근거 경계

- [v36 상세 보고서](research/vanilla_models/v36/00_v36_P1_544과거SHA대조_화로용광로훈연기6모델_24상태_정적분석.md), [P1 SHA 대조표](research/vanilla_models/v36/01_p1_544_historical_sha_evidence_crosswalk.csv).
- 과거 CSV 18개와 P1 544 경로의 SHA를 대조해 v35 직접 15개, 과거 SHA 일치 83개, 해당 선정 CSV 근거 미연결 446개로 기록했다. 이것은 모든 과거 CSV/보고서/DB의 전수 검증이 아니다.
- 기존 v7에는 chiseled_bookshelf 및 oak_shelf 이름의 SHA 이견이 존재하므로 이전 증거 충돌로 남겼다. 원본 바이너리 오류라고 단정하지 않는다.
- v36 신규 source: 화로·용광로·훈연기 6 leaf JSON SHA 6/6 일치, 부모 3 JSON, blockstates 3 JSON / 24 source variants. 공통 cube source 6 face, 36 face×material 사용기록. 자동 UV는 추론.
- 이 모델들이 참조하는 13 PNG 경로를 확인했으나 PNG 바이트/실제 RGBA는 이번 회차 미검사. 공식 Mojang 1.21.11 client.jar·인게임 정적 UV/컬링·조명 미검증. 애니메이션 보류 지속, 0/5 최종 완료.

## 주요 근거

1. Minecraft Java **1.21.11** 버전 고정 비공식 에셋 미러: https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft
2. Minecraft Java 1.21.11 Yarn 문서에서 일부 특수 렌더링 클래스의 존재 확인: https://maven.fabricmc.net/docs/yarn-1.21.11+build.1/
3. 1.21.11 특수 렌더링 모델·애니메이션의 비공식 추출 연구 데이터: https://github.com/InventivetalentDev/minecraft-entity-models/tree/1.21.11
4. [Another Furniture 1.21.1 소스](https://github.com/crispytwig/AnotherFurniture/tree/1.21.1), 조사 당시 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`. [LICENSE](https://github.com/crispytwig/AnotherFurniture/blob/1.21.1/LICENSE) 상 `resources/` 폴더는 All Rights Reserved. **모델 및 PNG 원본 비재배포**.
5. 각 연구 체크포인트 CSV/DB에 개별 텍스처 경로, 모델 경로, Git blob SHA-1 또는 PNG SHA-256 기록.

## 검증된 범위

- 저장소로 옮긴 분석 파일들의 바이트 해시를 계산하고 전수 보존할 수 있음.
- v8 SQLite `PRAGMA integrity_check` 통과.
- v9 CSV Git blob SHA-1 두 개가 로컬 분석본과 일치.
- v10 로컬 SQLite (v8 복사 + v9 데이터 추가) 무결성 검사 통과, 외래키 검사 문제 0건.
- GitHub에 v10 데이터 복원을 위한 SQL migration과 재구성 스크립트 보관; 완성된 v10 바이너리 SQLite는 GitHub 미업로드.
- v1–v8 ZIP 각각 CRC 검사 통과.
- v11 Another Furniture 69개 템플릿·33개 대표 모델·12개 블록 상태 JSON 직접 해석, 12개 PNG 헤더 읽음. 수치는 **해당 1.21.1 버전의 소스**에서 관찰된 것이며 1.21.11에서 인게임 재현은 미확인.
- 각 체크포인트의 작성자는 비공식 미러에서 JSON/PNG를 조사한 결과를 기록하고 있음.

## 남은 검증

- Mojang의 정식 `client.jar`와의 **직접 SHA-256/바이트 비교 미완료**.
- 실제 게임 화면의 픽셀 및 모형/조명/애니메이션 **인게임 비교 검증 미완료**.
- 특수 렌더링의 모든 3D 모델 부품 좌표·애니메이션에 대한 완전 검증은 수행하지 않음.
- 각 파이썬 스크립트는 기존 환경 경로·입력 자료에 의존할 수 있음. 업로드 사실만으로 전체 코드 재현성이 입증되지는 않음.
- 이 연구는 Minecraft 전체 블록 100% 분석이 아니라 **표본 기반 학습 자료**임.
- **과거 v11 시점** 모드 PNG 12개는 헤더만 읽었으나, **v13에서 양 모드 합계 24개에 대해 실제 픽셀·알파/색상 해석 완료**. 정확한 재질 face 대응·인게임 관찰은 여전히 미완료.

## 배포 정책

- **v25 이후 현재 사실 변경:** 연구 산출물에는 원본 게임 PNG/JSON/JAR를 재포함하지 않지만, **사용자가 별도로 업로드한 저장소 루트 `1.21.11/`에는 실제 Minecraft 원본 게임 `.class`·JSON·PNG가 공개 상태로 존재한다.** 공개 배포 권한/라이선스 확인과 비공개화 또는 분리가 필요하다.
- 분석 보고서, 추출 통계, 생성된 그래프, 재현용 연구 스크립트만 보관.
- 별도의 라이선스는 붙이지 않았고, 게임 에셋 재배포 권한을 주장하지 않음.


## v11–v12 가구 모드 출처 및 제한

- [Another Furniture 1.21.1](https://github.com/crispytwig/AnotherFurniture/tree/1.21.1), 원본 모델·텍스처 All Rights Reserved. v11 연구의 원본 경로·Git SHA를 별도 보관.
- [Terrarium Earth Handcrafted](https://github.com/terrarium-earth/Handcrafted/tree/1.21.x), 커밋 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`; 공식 [Terrarium License](https://github.com/terrarium-earth/Handcrafted/blob/1.21.x/LICENSE)는 일반 리소스 PNG/모델 JSON을 All Rights Reserved로 정의. v12에서 **원형 모델 120개 전부 직접 읽어 구조 계측**, 자동 생성 모델 11,989 경로 중 16개 샘플 실측.
- [Macaw's Furniture 공식 Modrinth](https://modrinth.com/mod/macaws-furniture), 1.21.11 Fabric 3.4.2 버전 [공식 게시 기록](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD); 공식 원본 모델 파일 직접 계측 0개. 제3자 미검증 소스를 공식 근거로 취급하지 않음.
- **과거 v12 시점** Handcrafted PNG 12개는 IHDR만 검사했으나 **v13에서 실제 화소 분석으로 확장**. 13 모델 UV의 픽셀 경계 정렬도 조사했지만 face→PNG 실제 대응/렌더는 아직 미검증.
- v12 사전 5유형 비교는 서로 비슷한 용도의 대표 가구를 비교한 것이며 똑같은 디자인이 아니므로 품질 평가에 사용할 수 없음.
- 모드(1.21.1)와 바닐라 기준(1.21.11)의 버전 차이를 유지하고 실제 인게임 검증 전에는 완성 판정을 하지 않음.

## v13 실화소·UV 검증 출처

- [실화소·UV 분석 상세 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md): 고정 원본 Git SHA를 대조한 PNG 24개 완전 디코딩, 모델 13개에서 UV 571면 픽셀 격자 검사.
- [원본 PNG 로컬 재측정 스크립트](scripts/reproduce_mod_png_v13.py): 사용자 측 원본 repo 디렉터리를 대상으로 SHA 및 픽셀 통계를 재현하도록 작성; 본 실행 환경의 외부 네트워크가 불가해 이 Python 스크립트의 직접 재실행 테스트는 아직 미완료. 이번 수치는 연결된 GitHub 원본을 JavaScript로 직접 디코딩하여 계산함.
- 반투명 픽셀 0건은 **24개 표본**에 한정한다. 571면 정렬 역시 **13개 모델 표본**에 한정한다. 공식 JAR, 인게임 픽셀 렌더 및 Macaw 모드 실측 0건 상태 유지.

## v14 기존 텍스처 참조·PNG 실측 근거 결합 검증

- [v14 상세 보고서](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md) · [51 슬롯 CSV](research/furniture_mods/v14/handcrafted_texture_bindings_51.csv) · [분석 입력 저장소 blob SHA](research/furniture_mods/v14/v14_binding_audit_summary.json).
- 직접 수행한 일: v12 Handcrafted 생성형 leaf 16개 CSV의 `textures` JSON을 재파싱하고, v12 PNG 헤더 manifest와 v13 픽셀 통계의 **Git blob SHA 및 치수**를 일치 검증, 기존 v13 원형 모델 UV 조사 대상의 부모 참조를 비교.
- 통계: 총 슬롯 51건 중 모드 경로 35(기존 실측 PNG에 상응 19 / v13 표본 밖 16) 및 바닐라 Minecraft 경로 16. 표본 밖의 **고유 모드 PNG 12종**은 원본 소스 부재로 이번 화소 재검증 미실시. v11 Another Furniture 완성형 CSV에는 실제 텍스처 override 경로가 없어 33종 face/PNG 연결 미확정.
- **검증 수준:** `cross_record_reference_join`. 모델별 슬롯이 이미 분석된 어느 PNG 경로/해시에 연결되는지는 확인했으나, 원본 face JSON의 `texture` 지정 및 PNG 내 각 면의 실제 픽셀 영역/알파는 직접 확인하지 않았다. 이번 v14에서 새 원본 PNG/JSON 파일 **0개** 직접 디코딩. 이전 v13의 직접 관찰 수치와 구분하여 누적.
- Handcrafted 리소스는 All Rights Reserved이며 원본 이미지·모델 JSON을 재배포하지 않는다. Minecraft 1.21.11 공식 JAR·게임 렌더 및 Macaw 원본 실측 0건 상태 변경 없음.

## v15 신규 파생 기하 분석의 근거와 비교 한계

- [v15 연구 보고서](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) · [189 모델별 지표](research/furniture_mods/v15/model_geometry_derived_189.csv) · [계열별 22그룹](research/furniture_mods/v15/handcrafted_family_metrics_22.csv) · [원본 입력 blob SHA](research/furniture_mods/v15/v15_geometry_summary.json) · [오프라인 재검산 도구](scripts/verify_v15_geometry_research.py).
- 연구자는 연결된 사용자 GitHub 저장소의 v11 Another Furniture 실측 CSV 69행, v12 Handcrafted 원형 실측 CSV 120행, v13 PNG 화소 CSV 24행을 **직접 재집계해 새 지표를 계산**했다. 새로 원 제작자 PNG/JSON 원본 파일을 직접 다운로드/디코딩/읽은 건수는 **0**. 직접 분석했다는 표현은 기존 GitHub 실측 CSV 및 해당 수치의 재집계에 한정한다.
- 새 확인 수치: Another 299요소 가능한 방향 면 1,794개 중 JSON 명시 1,362개, 비명시 432개; Handcrafted 810요소 가능한 방향 면 4,860개 중 명시 4,860개. 초과 원시 bbox 모델: Another 3/69, Handcrafted 60/112(0요소 8개 제외). 이는 6면을 가질 수 있는 cuboid 요소라는 집계 관례에 따른 수치로, 실제 렌더링 면 수나 컬링 성능·충돌상자 규격이 아니다.
- 두 모드는 **템플릿 69개 vs 작성 모델 120개**라는 다른 모집단을 측정했다. 이들의 회전·0두께·bbox 지표 차이를 모드 전체 우열이나 Minecraft 바닐라 '공식 규칙'으로 승격하지 않는다. 회전·0두께 요소는 겹칠 수 있다. 원시 bbox는 로컬 좌표이고 부모·블록 상태 변환 및 실제 렌더/충돌을 반영하지 않는다.
- v13 PNG 기존 표본 12개씩의 가시 RGBA 색상수 중앙값은 두 모드 모두 7색(이전 픽셀 표본의 재통계), 반투명 픽셀 포함 PNG 0/12 각각. 전체 모드 텍스처에 일반화하지 않는다.
- 본 v15의 Python 오프라인 검증 스크립트는 GitHub에 새로 게시했으나 **이 대화의 로컬 런타임에서 직접 실행하지 않았다**. 현재 측정은 GitHub 연결 데이터를 JavaScript로 처리하고 불변식을 검사한 것. 공식 Minecraft client.jar 및 인게임 그래픽 검증 상태 미완료; 저작권 원본 에셋 재배포 없음.

## v16 원본 Handcrafted PNG·JSON 직접 재접근 및 UV 연결

- [v16 상세 보고서](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md) · [12종 PNG 실화소 CSV](research/furniture_mods/v16/handcrafted_12_new_png_pixel_metrics.csv) · [16 leaf 면/재질 그룹](research/furniture_mods/v16/handcrafted_16_leaf_face_material_groups.csv) · [원본 SHA·검증 JSON](research/furniture_mods/v16/v16_original_face_mapping_audit.json).
- **원본 데이터 직접 접근에 성공:** 제작자 저장소 `terrarium-earth/Handcrafted` 고정 커밋 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`의 생성형 leaf **16 JSON**, 작성 부모 **14 JSON**, 신규 **12 PNG**를 GitHub Contents 읽기로 확보, 기존 v12 30 JSON의 Git blob SHA 일치 확인. v14에 기재되었던 미측정 PNG 12종의 원본 해시·IHDR·IDAT를 직접 디코딩했으며 66,816픽셀(가시 7,358, 알파 0 59,458, 알파 1~254 0)의 관찰이 가능해짐.
- 원본 PNG 12개 중 **완전 투명** 2개 `bench/cushion/none_cushion` 및 `shelf/overlay/none`. 세부 통계/그림 픽셀은 재게시하지 않고 색상 수·픽셀 개수·해시만 저장.
- 원본 16 leaf와 14 parent의 텍스처 슬롯 체인을 직접 해석하여 **786개의 재사용된 면 인스턴스**를 검사. **784개**는 원본 PNG 24종(v13 샘플 12 + v16 샘플 12)의 경로·SHA·크기까지 연결되었고, 선언된 UV를 픽셀 좌표로 환산했을 때 전부 정수 격자에 정렬되고 PNG 범위 내에 있음. 나머지 **2면**은 바닐라 `minecraft:block/oak_planks` 참조이며 공식 PNG를 새로 읽지 않았음.
- **보류**: 784개 면의 UV 사각형 **내부 화소를 face별로 실제 샘플링**하지 않았으며, 뒤집힌 UV/0면적/부모 회전/알파 테스트/인게임 컬링·조명 최종 모습도 검증하지 않았다. 면 인스턴스 786은 고유 모델 면 수가 아니라 여러 leaf에 부모 원형을 반복 적용한 값이다.
- **검증 등급:** upstream JSON/PNG bytes and pixel decoding + direct texture path resolution + numeric UV-to-pixel bounds. **저작권 원본 JSON/PNG/JAR 바이너리를 재배포하지 않음**. 공식 Minecraft 1.21.11 `client.jar`와 Macaw 배포 원본 JAR, 인게임 시각 검증은 계속 미완료. 전체 세부 단계 최종 완료 **0/5**.

- [v16 재현 Python 스크립트](scripts/reproduce_v16_handcrafted_originals.py)는 Python 표준 라이브러리 `hashlib`, `zlib`, `csv`, `json` 등을 이용해 고정 원본 SHA 및 12 PNG/16 leaf/14 parent의 기록을 재측정하도록 작성했다. **로컬 PyCompile 문법 검사 통과, 원본 고정 커밋으로의 end-to-end 재실행은 미수행**. 이전 GitHub Contents 환경에서의 직접 바이트 계측과 구분한다.

## v17: 고정 원본 24 PNG의 실제 UV 면 사각형 픽셀 검증

- [v17 상세 보고서](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md), [784 면별 원본 텍셀 통계](research/furniture_mods/v17/face_pixel_samples_784.csv), [24종 PNG별 사용 통계](research/furniture_mods/v17/texture_face_pixel_usage_24.csv), [입력 Git SHA와 전체 집계](research/furniture_mods/v17/v17_pixel_region_summary.json).
- 직접 작업: 제작자 `terrarium-earth/Handcrafted` 고정 커밋 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`에서 PNG **기존 24종을 다시 직접 읽고** Git blob SHA·PNG IDAT/DEFLATE/필터·RGB/RGBA/팔레트 `tRNS`를 검사. v16에서 계산한 **16 leaf × 14 원형 부모의 Handcrafted 소유 PNG 면 인스턴스 784/784**에 대해 UV 사각형 내부 원본 픽셀을 직접 집계. **v17 신규 고유 PNG/모델 원본 증가는 0**이며 v13/v16 자료의 원본 재검증·정량 심화다.
- 산출 수치: 784면 중 172면은 0면적 UV(사각형 내부 픽셀 없음), 612면이 비영 사각형; 비영 중 420면은 전부 불투명, 145면은 불투명·완전투명 혼합, 47면은 전부 투명. **41,290번의 UV 텍셀 읽기**(불투명 31,665, 투명 9,625, 부분 알파 0)이며 재사용 부모/모델 또는 서로 다른 면이 동일 텍셀을 반복 참조한 **중복 포함 누적 사용 횟수**이다.
- 주의: `UV 사각형의 원본 픽셀이 불투명`은 **실제 인게임에 해당 면이 보인다**는 의미가 아니다. 조명·컬링·회전·알파 테스트·블록 상태·UV 보간·렌더링 관찰이 없으며 바닐라 기본 `oak_planks` PNG 2면은 미측정. 0면적 UV를 결함이나 미표시로 단정하지 않는다.
- [실제로 사용한 JS PNG 픽셀 해독/샘플링 도구](scripts/v17_png_rgba_js_helper.js) 및 [독립 재검사용 Python/Pillow 스크립트](scripts/reproduce_v17_face_pixels.py)를 게시. **Python 스크립트의 실제 고정 원본 로컬 체크아웃에서 end-to-end 재실행 시험은 아직 하지 않았다.** 원본 All Rights Reserved 이미지/JSON 자체 재배포 없음.
- 완료율 혼동 방지: **784/784 = 이번에 범위를 정한 Handcrafted 면 샘플 100%**. 공식 바닐라 JAR·Macaw JAR·인게임 최종 검증이 완료된 상위 1단계 작업은 **0/5**, 전체 연구 작업량의 유효한 총 백분율은 아직 없다.

## v18 제작자 Another Furniture 원본 직접 재검증 및 PNG 12종 추가

- [v18 상세 보고서](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md) · [leaf 33개 원본 재료 참조](research/furniture_mods/v18/another_leaf_texture_resolved_33.csv) · [원형 템플릿 30 SHA](research/furniture_mods/v18/another_template_direct_30.csv) · [최종 face→텍스처 113그룹](research/furniture_mods/v18/another_face_material_groups_113.csv) · [새 12 PNG 실화소](research/furniture_mods/v18/another_new_png_12_pixel_metrics.csv) · [원본 SHA 감사 JSON](research/furniture_mods/v18/v18_original_model_audit_summary.json).
- 원 제작자 `crispytwig/AnotherFurniture`의 Minecraft **1.21.1** 고정 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`에서 모델 JSON leaf **33개**, 부모 원형 **30개**를 직접 GitHub Contents로 읽고 구 v11 실측 Git blob SHA와 각각 일치 검증하였다. **기존 v11에서 한번 본 모델들에 대한 새 원본 직접 재확인**이며, 새 독립 모델 63종을 발견했다는 뜻이 아니다.
- 33 leaf의 실제 텍스처 override **93건**과 각 템플릿의 명시적 face→슬롯을 결합하여 **807개 상속 면 인스턴스**의 최종 재질 경로를 검증. **모드 텍스처 804면, Minecraft 기본 `dirt` 3면**. 한 번 생략된 `block/dirt`는 원문 보존과 함께 `minecraft:block/dirt`로 정규화. 원본 네임스페이스 생략 관련 공식 게임 파일/실제 렌더까지 검증한 것은 아님.
- v13에 없었던 **새 Another PNG 12개 원본 바이트를 직접 읽고 전체 픽셀 디코딩**(16×16×12 = 3,072픽셀, 불투명 2,156/알파0 916/부분 알파 0). **4비트 인덱스 팔레트 PNG** `sofa/wood_2`를 새 [v18 디코더](scripts/v18_png_rgba_4bit_helper.js)로 해독. 기존 Another 12 + 이번 12 = **24 고유 PNG** 실화소 표본, 이 33 leaf의 모드 텍스처 **53종 경로 중 24종(45.28%)**에 해당. 남은 29 경로는 원본 이미지 화소 미측정. Handcrafted의 고유 실화소 24개와 합한 전체 현재 모드 PNG 표본은 **48종**.
- **검증 수준:** pinned original model source inspection + SHA + inherited face texture path resolution; sampled 12 exact original PNG byte/pixel decode. **807 face의 UV 좌표/실제 PNG 영역 픽셀과 인게임 화면은 아직 검증 안 함.** 이전 v17 Handcrafted 784면 UV RGBA 실측과 검증 수준이 다름. 공식 바닐라 1.21.11 `client.jar`, Macaw 공식 배포물 원본 모델, 인게임 렌더 미검증. 5개 세부 작업 확정 완료 **0/5**.
- **저작권:** 원본 Another Furniture 리소스 All Rights Reserved. 원본 모델 JSON·PNG/JAR 파일은 연구 GitHub에 업로드하지 않고, Git 해시·상대 경로·집계 수치만 업로드. v18 분석 중 중간 CSV 2·3묶음 직렬화 오류 발견·수정 후 전체 33/93/30/104 기록 재검산.

## v19 — Another Furniture 선정 모델 참조 PNG 전체 원본·804면 실제 UV 화소 직접 검증

- [v19 상세 보고서](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md) · [Another 53개 원본 PNG 경로·SHA·가시 픽셀](research/furniture_mods/v19/another_texture_53_png_source_manifest.csv) · [33 leaf에 적용한 807개 원본 면 UV](research/furniture_mods/v19/another_33_leaf_807_face_uv_rects.csv) · [804모드 면별 실제 PNG UV 픽셀 RGBA](research/furniture_mods/v19/another_804_face_actual_rgba.csv) · [검증 JSON](research/furniture_mods/v19/v19_original_png_face_rgba_audit.json).
- 원본은 제작자 `crispytwig/AnotherFurniture` 고정 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`. v18에 선정한 **33 leaf**에서 사용된 **53개 고유 모드 PNG 참조 경로** 중 종전 미측정 **29종 원본을 이번에 새로 직접 읽고 전체 PNG 픽셀 디코딩**했다. v13·v18 기존 24종과 합쳐 **53/53(해당 선택 범위 100%)**이고, 면의 실제 RGBA 샘플링 과정에서 PNG **53종 모두 제작자 원본 바이트를 다시 직접 읽고 Git SHA·치수·전역 픽셀 수치 일치** 확인. **원본 PNG 전체 픽셀 17,408(불투명 11,536·투명 5,872·부분 알파 0)**.
- 원본 템플릿 **30 JSON을 제작자 고정 커밋에서 다시 읽고 SHA 일치** 확인, v18 원본 leaf 경로를 재사용하여 **807면 인스턴스 선언 UV** 추출. 모드 PNG 참조 **804면 모두** 원본 PNG 정수 픽셀 경계 및 이미지 범위 내, 실제 사각형 RGBA 검증 완료: **712면 전체 불투명, 88면 혼합, 0면 전체 투명, 4면 0면적**, 소스 UV 뒤집힘 **221 모드 면**. 텍셀 사용 총 32,531회(불투명 31,545/완전투명 986/부분 알파 0), 동일 모드/원형/UV 영역의 **중복 참조 포함**.
- 꽃상자의 `minecraft:block/dirt` **3면은 UV 좌표 선언만 추출**했고 **공식 Minecraft 1.21.11 바닐라 PNG와 픽셀은 조사하지 않아** 모드 픽셀 수치 804면에 넣지 않았다. Handcrafted v17의 바닐라 oak_planks 2면도 동일. 모드 원본 PNG 전체 알파와 렌더링의 실제 면적/표시 색상은 구분해야 한다.
- **모드 PNG 원본 실화소 누적 표본:** Another **53종**, Handcrafted **24종**, 합계 **77종**. **두 모드의 선정 생성형 모델 표본**에서 PNG 직사각형 픽셀 실제 검사 완료: Another **804/804**, Handcrafted **784/784**. [차이 비교](research/furniture_mods/v19/00_v19_모드간실제면UV픽셀_선정표본비교.md)는 표본 구성이 다르므로 모드 전체 스타일 일반화 불가.
- 53/53은 v18에서 선정된 **33 leaf의 모드 텍스처 참조 경로**에 한정. v11 파일 트리에는 더 많은 모델/블록 PNG 경로가 존재한다. 이 결과를 모드 전체 전수·공식 바닐라 1.21.11 client.jar/인게임 렌더·Macaw 공식 모델 검증으로 과대해석하면 안 된다.
- 원본 저작권 리소스 JSON·PNG·JAR를 연구 GitHub에 올리지 않았고 모델/픽셀의 통계·원본 blob SHA만 게재. GitHub Contents에서 제작자 원본을 직접 열어 계산한 JS 결과의 **입력 SHA·면 유일키·모든 면 픽셀 합 검산 통과**, **독립 원본 체크아웃에서 Pillow 방식의 end-to-end 재실행은 아직 하지 않음**. 상위 1단계 최종 완료 **0/5**.

## v20: Another Furniture 원형 69개 제작자 원본 재검증 및 Macaw 릴리스/바이너리 구별

- [v20 상세 보고서](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md) · [제작자 JSON 69개 직접 SHA·기하](research/furniture_mods/v20/another_69_templates_direct_original_geometry.csv) · [1,362 원본 면 속성](research/furniture_mods/v20/another_69_templates_1362_original_faces.csv) · [감사 JSON](research/furniture_mods/v20/v20_another_69_original_template_audit.json).
- 제작자 `crispytwig/AnotherFurniture` Minecraft 1.21.1 소스 고정 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`의 **v11 원형 선정 69개 JSON 전부를 이번에 직접 재조회**하고 Git blob SHA·요소·원본 face count를 과거 v11 기록과 비교했다. **69/69 일치**. v18~v19에 실제 읽었던 30개뿐 아니라 기존 선정 범위 밖 **39개 원형을 이번에 직접 상세 분석**했다. **신규 원본 모델 경로 발굴 0건**, 기존 표본의 원본 증거 강화임.
- **69 원형, 299 요소, 1,362 명시 면**의 `from/to`, 요소 회전, `faces[*].uv`, UV 회전, `cullface`, 재질 raw 슬롯을 원본에서 조사. **422 역방향 UV 면, 134 UV 회전 face, 443 cullface face, 4 0면적 UV, 17 회전 element, 34 평면형 element, 11 원시 bbox 0~16 초과 element**. raw bbox는 물리 collision 또는 게임 내 차지 범위가 아니다. 39개 새로운 직접 상세 표본은 **653개 원시 face**이며 생성형 leaf/실제 PNG RGBA에 새로 연결한 수치는 0.
- **전체 모드 전수 아님:** 기존 v11 원본 Git tree의 Another 모델 경로 **1,451개** 중 원형으로 기록한 69개에 한정. 다른 모델 원본의 배제/존재 여부에 관한 완료 주장 금지. v19 선정 완성형 33개의 PNG 53종/804모드 면 RGBA와 v17 Handcrafted 24 PNG/784모드 면 RGBA 성과 유지하며 재검사한 척 새 데이터로 합산하지 않는다.
- 공식 Macaw's Furniture [Modrinth 3.4.2 Minecraft 1.21.11 Fabric](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD) 릴리스 게시 확인, 공식 CDN `https://cdn.modrinth.com/data/dtWC90iB/versions/xhmciaUD/mcw-furniture-3.4.2-mc1.21.11fabric.jar`. 다만 컨테이너 DNS/외부 네트워크 차단으로 JAR 파일 실제 바이트 확보 실패. 제작자 `sketchmacaw/macawsmods` GitHub는 1.21.11 가구 원본 리소스가 확인된 저장소가 아니라 이슈·안내용. **공식 릴리스 존재와 JAR 내부 원본 모델 검증은 별개**. Macaw **실제 모델 0 / PNG RGBA 0 / UV 0**.
- 독립 로컬 원본 체크아웃 재실행 및 1.21.11 공식 Minecraft `client.jar`와 인게임 UV·culling·빛/알파 검증 미완료. 원본 저작권 있는 모드 JSON/PNG/JAR을 연구 GitHub에 복사하지 않음. 5개 세부 작업 최종 완료 **0/5**.

## v21 — Another Furniture 블록 상태와 새 38 완성형 원본 상속·실화소

- [v21 상세 보고서](research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md) · [원본 상태 12개 SHA 기록](research/furniture_mods/v21/another_12_blockstates_pinned_source_audit.csv) · [802 상태 적용·114 모델 경로](research/furniture_mods/v21/another_12_blockstates_applied_models.csv) · [새 38 leaf/1,197 상속 face 구조](research/furniture_mods/v21/another_new_38_leaf_face_resolution.csv) · [새 14 PNG 실화소](research/furniture_mods/v21/another_new_14_png_unique_source_metrics.csv) · [모드 면 UV 사각형 내부 실제 RGBA 1,192행](research/furniture_mods/v21/another_new_38_leaf_all_rgba_1192.csv) · [입력 SHA/원시 면/PNG 픽셀 1:1 감사](research/furniture_mods/v21/v21_blockstate_new_leaf_rgba_audit.json).
- 제작자 `crispytwig/AnotherFurniture`, Minecraft 1.21.1 브랜치, 고정 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`의 **12 블록 상태 JSON 원본 다시 SHA 확인**. 원본 `variants`/`multipart` **802개 적용 레코드**에서 서로 다른 모델 참조 **114경로**를 추적했고 **`minecraft:block/air` 적용 2건**이 포함되어 있으므로 이 모두가 가구 모델이 아니다.
- v18 기존 33 leaf에 없는, shutter 계열 새 43경로를 제외한 **새 leaf 38개 원본 JSON을 실제 읽고 SHA 기록**. 자기 elements 0개, 원형 부모 21종(그중 기존 33 leaf가 사용하지 않았던 19종), 텍스처 override 97건. 새 leaf 부모 상속 **1,197면**의 참조 경로를 연결했으며 모드 PNG **1,192면**, 바닐라 dirt **5면**.
- **모드 PNG 원본 34종을 실제 다시 다운로드해 PNG 전체 픽셀 디코딩**, v19 출처 20종은 원본 SHA/치수/원본 PNG 전체 alpha 수치 다시 확인, **고유 14종은 신규 원본 화소 표본**으로 추가. 새 leaf의 모드 UV 영역 **1,192/1,192면 직접 픽셀·RGBA 샘플링**: 1,086면 전부 불투명/106면 혼합/0면 전체투명/0 UV 면적0, 부분 알파 픽셀 0. 중복 텍셀 사용 **32,784회**(불투명 30,480/완전 투명 2,304), 실제 렌더 출력 아님. 원본 PNG SHA·정수 픽셀 좌표/PNG 경계/전체 면 픽셀 합계 검증 통과.
- 누적 선정 표본: **Another 71 leaf, 고유 PNG 67종/모드 면 RGBA 1,996개**. Handcrafted 24 PNG/784면과 합해 **원본 PNG 91종 / 면 UV 실제 RGBA 2,780인스턴스**. 바닐라 `dirt` Another 8면 및 `oak_planks` Handcrafted 2면은 게임 공식 PNG 미검증. **Macaw 공식 배포 페이지 존재 확인·JAR 원본 다운로드 DNS 실패·모델 실측 0건**. 인게임 UV/컬링/상태/조명 검증 미완료.
- 이 38 leaf는 해당 원본 블록 상태 12개에서 새로 선정한 파일일 뿐 모드 전체 생성형 모델 전수가 아니다. `shutter/variant_*` 잔여 43모델을 비롯해 1,451 모델 경로/177 상태/1,220 블록 PNG 전체 분석은 아직 끝나지 않았다. 파일 한정 **선정 표본 100%**와 전체 프로젝트 완료율을 혼동하지 말 것. **저작권 원본 JSON·PNG·JAR은 재배포하지 않고 SHA·경로·면·색상·알파 계량만 보관**. 상위 1단계 5개 세부 작업 최종 완료는 **0/5**.

## v22 — Another Furniture 셔터 원본 43 leaf·PNG 42 신규·214면 UV 실제 RGBA

- [v22 전체 보고서](research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md) · [43 leaf/214 face 원본 상속·slot·UV](research/furniture_mods/v22/shutter_43_leaf_resolved_source_face_uv.csv) · [원본 PNG 43종 SHA·픽셀 전체](research/furniture_mods/v22/shutter_43_png_original_source_manifest.csv) · [214면 PNG 사각형 실제 RGBA](research/furniture_mods/v22/shutter_214_face_uv_original_rgba.csv) · [입력 Git blob SHA 및 면 픽셀 키 감사](research/furniture_mods/v22/v22_shutter_source_original_complete_audit.json).
- 저작자 `crispytwig/AnotherFurniture` Minecraft 1.21.1 고정 `57eb624cbb7f408d43398c7434b0d38d312cb55d` 소스에 대해 v21의 블록 상태 12개 참조 셔터 원본 **44종 경로 중 v18에서 이미 검사한 1개 제외하고 새 43 leaf JSON 실제 읽어 Git SHA 기록**. 4 부모 원형 직접 사용, 자체 요소 없음. 상속 재질/UV **214면**을 원본 PNG 경로에 해결했고, unresolved 0.
- 43 모드 PNG 원본 바이너리 실제 디코딩(**기존 1 원본 SHA·픽셀 재검사 + 처음 읽은 PNG 42**). 전부 PNG 16×16 8bit RGBA이며 파일 전체 11,008 픽셀 모두 불투명. 새 214면 전부 픽셀 정수 UV 사각형이 PNG 범위 내·원본 픽셀 영역 전부 알파 255. **UV 반전 75면, face UV 회전 42면**, 반복 사용 텍셀 합 **28,160회 전부 알파 255**. 실제 보이는 렌더 면, 조명/컬링, 물리 collision 값은 아니다.
- **v22 누적 선정 표본:** Another leaf 114(33+38+43), 서로 다른 원본 PNG **109종**(53+14+42), 모드 PNG 면 실제 UV RGBA **2,210인스턴스**(804+1,192+214). Handcrafted 24 PNG/784면을 합해 **133 고유 PNG/2,994모드 면**. 바닐라 dirt Another 8면, oak_planks Handcrafted 2면은 공식 Mojang `client.jar` PNG 원본 미검증.
- 기존 **12개 블록 상태 표본**에 대한 고유 모델 참조 114경로 = Another **111 leaf 원본 + 2 template 원본**(모두 직접 제작자 JSON 근거), 별도 `minecraft:block/air` 하나. 따라서 **이 12 상태 표본의 Another 참조 경로 113/113 원본 근거 확보**. 원본 약 177 상태 파일/1,451 모델 경로/1,220블록 PNG의 전수는 아니다.
- 공식 Macaw's Furniture [1.21.11 Fabric 3.4.2](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD) 원본 JAR을 재시도했으나 **컨테이너의 cdn.modrinth.com DNS 해결 실패**. Macaw 원본 JSON/PNG/UV **0건** 유지. 게임 공식 `client.jar` 및 인게임 렌더는 미검증. 소스 원본 JSON/PNG/JAR 저작권 리소스는 연구 GitHub에 재업로드하지 않음. 전체 세부 작업 최종 완료 **0/5**.

## v23 — 신규 블록 상태 원본 10종·완성형 51 JSON·새 PNG 42종·실제 UV RGBA 1,119면

- [v23 전체 보고서](research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md) · [신규 원본 블록 상태 10 Git SHA](research/furniture_mods/v23/new_10_blockstates_author_original_audit.csv) · [386개 상태 model apply](research/furniture_mods/v23/new_10_blockstates_applied_model_records.csv) · [새 51 leaf/부모 템플릿의 1,127면 재질·UV](research/furniture_mods/v23/new_51_leaf_source_face_texture_resolution.csv) · [51 PNG 원본 SHA/전체 RGBA](research/furniture_mods/v23/new_51_leaf_51_png_original_source_manifest.csv) · [1,119면 원본 PNG 직사각형 RGBA](research/furniture_mods/v23/new_51_leaf_all_1119_face_actual_rgba.csv) · [검산 JSON](research/furniture_mods/v23/v23_new_blockstate_leaf_png_face_original_audit.json).
- 제작자 `crispytwig/AnotherFurniture` Minecraft 1.21.1 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`에서 **이전 12개 밖의 10개 블록 상태 원본 JSON을 직접 읽고 SHA 기록**(`birch_chair/spruce_chair/birch_bench/spruce_bench/red_sofa/blue_sofa/red_curtain/birch_drawer/spruce_table/birch_flower_box`). 386개 variants/multipart apply, 서로 다른 92 모델 경로(Another 91/바닐라 air 1).
- 선정된 **신규 51개 생성형 leaf JSON을 직접 조회하고 원본 SHA 기록**, 원형 부모 34종 사용, 전원 자체 `elements=0`. `drawer/birch_open`은 intermediate leaf를 거쳐 원형으로 연결되는 2단계 상속. **1,127면 소스 선언 UV/재질** 해결(모드 PNG 1,119/바닐라 dirt 8), 미해결 0.
- 실제 모드 PNG 고유 경로 **51종 제작자 원본 PNG 직접 읽고 전역 RGBA 검사**(v22까지 원본 측정된 9종 SHA·화소 재검산/**신규 42종 원본 실제 픽셀 디코딩**). 49종 16×16, 2종 64×64. **실제 UV 원본 PNG 내부 사각형 면 1,119/1,119 전수 RGBA 직접 표본**: 1,063 전체 불투명/56 혼합/전체 투명 0/면적0 0. 원본 UV 반전 347면·회전 73면. 픽셀 사용 횟수 **41,666회(불투명 39,304/투명 2,362/부분 알파 0)**, **반복 텍스처/면 상속 사용 포함**, 게임 화면 픽셀 아님.
- **비교 근거:** [원본 면별 3쌍 재질 비교 CSV](research/furniture_mods/v23/new_51_material_variants_pairwise_source_comparison.csv). 빨강/파랑 소파 대응 229면 동일 부모+UV/알파, 그중 159면 PNG 동일/70면 PNG 서로 다름. 자작/가문비 벤치 116면과 의자 92면도 동일 부모/UV+알파, 재질 PNG 경로 모두 다름. 인게임 실제 보이는 색·광원/가림과 구별.
- **누적 선정 표본** Another 블록 상태 원본 **22/177**, leaf **165**, 원본 PNG 실화소 **151종**, 모드 면 원본 UV 실제 RGBA **3,329인스턴스**. Handcrafted 24 PNG/784면 합산 두 모드 원본 PNG **175종/모드 면 4,113**. 바닐라 dirt Another 16면·oak_planks Handcrafted 2면은 공식 Minecraft 1.21.11 client.jar 원본 PNG 미검증.
- 이번 10 상태의 Another 원본 모델 참조 91경로 중 51개는 이번 새 leaf JSON 직접 확인, 1개(`chair/birch_1`)는 기존 v18 직접 확인, **다른 39개 의자 모델 JSON은 아직 직접 열지 않음**. 전체 블록 상태 177개 중 직접 검사한 22개만 해당하고 전체 파일 수/전체 PNG/전체 게임 렌더 완료율이 아니다.
- 원본 저작권 JSON/PNG/JAR을 연구 GitHub에 복제하지 않고 파생 경로·SHA·치수·UV 사각형·색/알파 통계만 저장. 외부 DNS 문제로 Macaw 공식 1.21.11 Fabric JAR 원본 미확보(모델 0), Mojang 공식 1.21.11 `client.jar`/인게임 렌더 미검증. 전체 상위 1단계 내부 5개 작업 최종 완료 **0/5**.

## v24 Another 의자 39 leaf 원본·상속 기하 검증의 출처와 한계

- [원본 JSON SHA·기하 감사 보고서](research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md) · [39모델 개별 SHA/경로 CSV](research/furniture_mods/v24/chair_remaining_39_original_json_geometry_audit.csv) · [파생 수치 감사 JSON](research/furniture_mods/v24/v24_chair_39_audit_summary.json). 제작자 `crispytwig/AnotherFurniture`의 **Minecraft 1.21.1** 고정 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`에 있는 남은 의자 leaf **39 JSON**을 직접 읽고 Git blob SHA·상속 원형·3개 슬롯 경로 확인. 기존 원형 2 JSON도 직접 재조회했다.
- 두 원형 모두 자체 10요소/46선언 면이며 `chair_tucked`의 10요소 좌표는 `chair`보다 raw z -9, 면별 UV/재질 슬롯 선언 동일. 39개 leaf에 반복 상속한 **390 요소/1,794 선언 face 인스턴스**(bottom1,131/seat195/back468), 새 override 117건을 계량했다. 모델이 반복한 **원본 선언 인스턴스**이므로 새로운 고유 기하 390개나 실제 화면 1,794면을 뜻하지 않는다.
- **v24 신규 원본 PNG 다운로드/픽셀 디코딩 0개, UV 내부 원본 RGBA 샘플링 0면**. 해당 39개 leaf의 24개 PNG *참조 경로*가 과거 실측한 151종과 얼마나 중복되는지 원본 manifest 대조는 아직 수행하지 않음. 기존 Another PNG 실화소 151종/실제 UV면 3,329, Handcrafted PNG 24종/784면, 합산 PNG175종/실제 RGBA면4,113 유지. UV 선언만으로 원본 PNG 픽셀 불투명 여부를 판단하지 않음.
- 새 10개 원본 상태의 Another 모델 경로 91/91 직접 JSON 근거가 마련됐지만 원본 블록 상태 파일은 전체 177 중 **22개만** 직접 검사했고 155개 미검증. **Minecraft 공식 1.21.11 client.jar**, **공식 Macaw JAR 내부**, 인게임 렌더·컬링·충돌은 이 단계에서 검사하지 않았다.
- 제3자 리소스가 All Rights Reserved이므로 **원본 모델 JSON, PNG, JAR 자체를 저장소에 업로드하지 않고** 출처·SHA 및 파생 수치만 남긴다.


## v25 — 사용자가 업로드한 1.21.11 원본 아카이브 직접 감사와 검증 경계 (2026-11-13)

- [v25 바닐라 보고서](research/vanilla_models/v25/00_v25_바닐라원본_모델상속상태PNG_직접검증보고서.md)와 파생 CSV 8개 및 JSON 요약을 실제 `1.21.11/assets/minecraft/` 경로에서 수집·작성.
- 모델 원본 JSON **32**, 블록 상태 JSON **8**, PNG **8**, PNG 애니메이션 메타 **2** = **메인 저장소 직접 자료 50개**(보고서 파생 계량 표본 고유 집합). 8개 자체 기하 모델 **44 요소/204 선언 face**, 상태 8파일 **79 variants/9 multipart**, 퇴비통 내용물 8개/상속 leaf 8개와 부모 템플릿 8개 계량.
- PNG 8개를 base64 바이트로 조회 후 **서명과 IHDR만 확인**했으며, **전체 RGBA 픽셀 디코딩 0개**, 새 face→PNG 원본 영역 실제 픽셀 **0면**. `stonecutter_saw` / `lantern`은 **16×48** 및 각 `.png.mcmeta` 확인, `frametime` 1/8. 실제 인게임 프레임/컬링 검증 미실시.
- 사용자가 올린 파일 6개와 기존 [1.21.11 비공식 에셋 미러](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11)의 **Git blob SHA 6/6 일치**. **이것은 독립 Mojang 공식 `client.jar` 무결성 판정이 아니다**. 오직 해당 6개 경로의 정확한 바이너리 일치만 근거로 삼는다.
- 구버전 문서의 '**저장소에는 원본 Minecraft 리소스가 없다**'는 진술은 새 `1.21.11/` 업로드 이후 거짓이므로 정정함. **GitHub 공개(public) 저장소 내 원본 게임 Java `.class`, JSON, PNG의 공개 재배포 권한을 확인하지 못했다.** 저작권과 Minecraft 이용약관 관점에서 별도 비공개 보관/삭제/분리 검토가 필요하다. 이번 연구 커밋에서는 원본 리소스를 새로 복제하거나 업로드하지 않음.
- v10 SQLite 등 기존 바닐라 DB, v24 모드 누적 자료 변경 없음. 01 **150/150 표본**은 최종 검증 아님, 02 바닐라 3D 진행 중, 03/04 v24 보존, 05 최종 비교 미완료. **완료 0/5**, 전체 완료 % 산출 불가.

## v26 — 바닐라 PNG 전체 픽셀·모델 UV 70행 실제 검사 (2026-11-13)

- [v26 원본 분석 보고서](research/vanilla_models/v26/00_v26_바닐라8PNG_전체RGBA_36면70프레임_실화소보고서.md)와 PNG 8종 전 화소 CSV, 6개 JSON 모델의 고유 face36개/애니메이션 프레임 포함70행 RGBA CSV, 미러 SHA 8종/기존 v4 3종 교차검사 CSV, 기계 요약 JSON 게시.
- 저장소 `1.21.11/assets/minecraft/textures/`의 PNG **8개 원본 전체 Base64 바이너리 취득·DEFLATE/PNG filter/PLTE/tRNS 실제 해독**, **총 8,704픽셀(완전불투명3,900/완전투명4,804/부분알파0)**. 기존 v4 150선정 텍스처 중 **3경로 중복**, 다른 5경로는 v4 CSV 표본 밖. v25 8개의 PNG 헤더만 읽은 계수와 서로 합산 금지.
- 선정 모델 6종의 **명시적 UV 면 36개**, 프레임 시점에 따라 **70개 face×frame 픽셀 조회 기록**(4가지 PNG 소스), 총 **원본 UV 텍셀 사용 3,652회(불투명3,328/투명324)**. 다락문 원형의 `#texture`는 v25 leaf JSON 상속을 통해 `oak_trapdoor`로 연결; 랜턴과 톱날은 16×48 PNG의 16×16 3프레임 모든 영역 조회. 자동 UV인 퇴비통 본체 등은 이번 70건 범위 밖.
- 사용자 업로드 PNG 8/8는 기존 1.21.11 비공식 추출본과 **Git blob SHA 동일**. v4에서 이미 측정된 `oak_planks`·`dirt`·`oak_trapdoor`는 **파일 바이트/전체 픽셀/가시 픽셀/크기 3/3 일치**. v4의 SHA-256을 이번 v26에서 직접 재산출하지 않았음.
- **방법상 제한:** JPEG/GIF가 아닌 PNG의 signature, IHDR, IDAT zlib, 팔레트/알파 및 scanline filter로 화소를 재구성하고 크기·합계를 검산. 각 PNG 청크 **CRC32/zlib Adler32 미검사**, Pillow를 통한 **독립 로컬 재실행 미수행**, 독립 공식 Mojang `client.jar` 검증 및 실제 인게임 렌더 미수행. 바닐라 01/02 최종 완료 아님.
- `1.21.11/`의 Minecraft 게임 원본 파일이 공개 저장소에 그대로 있는 문제는 **변경하지 않았으며**, 연구 기록에는 원본 게임 이미지/JSON/JAR 재복제를 하지 않았다. 권리/배포 정책 점검 필요. 전체 단계 최종 완료 **0/5**.

## v27 — 바닐라 원본 선반 32×32 아틀라스·퇴비통 자동 UV 구조/실화소 대조 (2026-11-13)

- [v27 원본 감사·정량 보고서](research/vanilla_models/v27/00_v27_선반32x32_퇴비통자동UV_원본화소검증보고서.md), [20면 선반 명시 UV PNG 대조](research/vanilla_models/v27/02_oak_shelf_20_face_actual_png_rgba.csv), [선반 32개 합성 조건](research/vanilla_models/v27/03_oak_shelf_32_combination_rule_evaluation.csv), [퇴비통 26암시 UV면](research/vanilla_models/v27/06_composter_26_implicit_uv_face_rgba.csv), [자동 UV 계산식↔원본 명시 UV 23면](research/vanilla_models/v27/04_uv_projection_23_explicit_face_source_crosschecks.csv).
- 사용자 공개 저장소 `1.21.11/assets/minecraft`에서 **새로 원본 5 PNG 완전 RGBA 해독 (2,048픽셀, 불투명 1,824·완전 투명 224, 부분알파0)**. 기존 v4 표본에 포함된 `oak_shelf` 1경로와 v26에 이미 해독한 `composter_top`를 중복 합산하지 않음. 5 PNG는 1.21.11 비공식 미러 Git blob SHA와 5/5 일치함.
- 선반 `template_shelf_body`/전면 선택 template 5개는 **원본 JSON에 직접 UV가 기재됨**. leaf `oak_shelf` texture override를 상속해 32×32 원본 PNG 20면의 픽셀 영역을 검사해 **1,376 texel-uses**; source 24 multipart를 32 합성 조건으로 평가해 정확히 2모델/조건 조회했으나 **인게임의 모든 유효 상태 검증 아님**.
- 퇴비통 본체 18+내용물8의 **uv 누락 26면**은 요소 from/to에서 6방향 사영식으로 복원한 **유도 좌표**다. 소스 `stairs` 11면, `slab` 6면, `fence_post` 6면의 원본 explicit UV와 **23/23 순서·값 일치**로 공식을 근거화. 원본 PNG 5종(신규4 + v26 기존 top1) 픽셀 값을 조회해 3,696회 모두 알파255 확인. 그러나 이 식이 **Mojang 1.21.11 클라이언트가 실제 사용한 자동 UV 계산 로직과 바이트 수준 동일하다고 판정할 수 없음**. UV 회전·컬링·조명·게임 렌더 역시 미검증. [일반 모델 스펙(외부 2차 설명)](https://minecraft.wiki/w/Model)은 UV 미기재 시 자동 생성만 명시하고 구체적 내부 함수 검증은 대신하지 않음.
- v27 face→PNG 샘플은 **명시 UV 20 + 유도 UV 26 = 46면 / 총 5,072 texel-uses(전부 불투명)**. 이전 v26의 **36면/70 face-frame**과 별도로 기록하되 texel-uses는 고유 픽셀/렌더 픽셀 수가 아님. 향후 인게임 상태 변화와 방향, 독립 Pillow 및 CRC/Adler 검증이 필요하다.
- v27/이전 누적은 바닐라 공식 client.jar 인증 **0**, 인게임 검증 **0**, 모드 v24 연구 수치 유지, 상위 1단계 최종 완료 **0/5**. 공개 저장소 `1.21.11`의 비허가 저작권 원본 재배포 문제는 계속 점검 필요; v27 커밋에 원본 게임 이미지/모델 JSON/JAR을 재업로드하지 않음.

## v28 — 104 variant 블록상태 원본, 문 40면 UV 실화소, 울타리 문 4원형 검증 범위 (2026-11-13)

- [v28 원본 분석 보고서](research/vanilla_models/v28/00_v28_바닐라문다락문게이트계단104상태_40면UV_RGBA.md) · [104 원본 variants](research/vanilla_models/v28/01_four_blockstates_104_exact_variants.csv) · [문 PNG 2경로 전체 RGBA](research/vanilla_models/v28/02_oak_door_two_png_full_rgba.csv) · [문 8부모 40면 UV 원본 RGBA](research/vanilla_models/v28/03_oak_door_eight_templates_40_faces_uv_rgba.csv) · [울타리 문 leaf/원형 구조 8소스](research/vanilla_models/v28/05_oak_fence_gate_4_templates_4_leaf_geometry.csv).
- 사용자 공개 GitHub `1.21.11/assets/minecraft/blockstates/`에서 **문32·다락문16·울타리문16·계단40 = 104 original JSON variants**의 방향/모델 참조/회전/x·y/`uvlock` 키를 정확히 추출. **명시 `uvlock:true` 51행, 키 부재 53행**(명시적인 false가 아니다). source `x/y`는 실제 런타임 회전 결과·UVlock 보정 검증과 다르다.
- `oak_door` leaf 8종, 원본 부모 template 8종(각 1요소·5 face)을 직접 읽고 PNG `oak_door_bottom/top` **2파일 전 바이트 해독 후 40명시 UV 원본 face→PNG 영역 샘플 5,248 texel-uses**(불투명4,864, 투명384) 계량. 2 PNG는 기존 v4 150 선정 표본 경로에 포함되며 **새 고유 PNG +0**. 새 파일 바이트 크기·픽셀/가시 면적이 v4 기존 기록과 2/2 일치. v4에 기록된 SHA-256을 이번에 독립 재계산하지 않음.
- `oak_fence_gate` leaf4/원형4 직접 JSON, **각 원형8요소·40선언면**, 원형 4건 합 32요소/160선언면. 이 160면에 `oak_planks` 원본 PNG를 이용한 실제 UV 텍셀 샘플링은 **아직 수행하지 않음**. 실제 충돌체/렌더 결과 아님.
- `InventivetalentDev/minecraft-assets` 추출본 동일 1.21.11 PNG 2종과 Git blob SHA **2/2 일치**. 이것은 독립 Mojang 공식 게임 JAR 배포 해시 인증이나 게임 실행 확인을 대체하지 않는다. 원본 바이트에 대한 Pillow 독립 복호/PNG chunk CRC·Adler 검증 및 실시간 게임 시각 검증도 v28에서 수행하지 않았다.
- 바닐라 01 표본 150/150 달성/최종검증 미완료, 02 대표 연구 진행, 03·04 v24 모드 누적값 변경 없음, 05 최종 비교 미시작. **상위 1단계 확정 완료 0/5**. 공개 원본 게임 `.class`/PNG/JSON의 재배포 권리는 추가 검토가 필요하며 이번 GitHub 커밋에 원본 리소스 자체를 복제하지 않음.

## v29 — 참나무 울타리문 원형 160면 직접 PNG RGBA 픽셀 검증(2026-11-13)

- [v29 원본 연구보고서](research/vanilla_models/v29/00_v29_울타리문160면_실제PNG_UV_열림담장좌표비교보고서.md) · [160면 실제 UV·RGB·alpha 파생 표](research/vanilla_models/v29/01_fence_gate_160_source_face_uv_rgba.csv) · [32원본 요소 좌표](research/vanilla_models/v29/02_fence_gate_32_source_elements.csv) · [16 source 상태↔선택 원형](research/vanilla_models/v29/03_fence_gate_16_state_source_profile.csv) · [8개 부품 열림·담장 위치 델타](research/vanilla_models/v29/06_eight_element_open_wall_geometry_deltas.csv) · [Pillow 원본 해시 재검사](research/vanilla_models/v29/05_oak_planks_independent_sha256_pillow_v4_crosscheck.csv).
- v28에 `160 source face declaration`만 확인하고 실제 PNG 픽셀 검증하지 못했던 4개 울타리문 템플릿의 **160/160 `faces.*.uv` 전부 원본 이미지의 RGBA 텍셀 값에 대응**. 각 원형 8요소/40면, 4원형 **512+464+512+464 = 1,952 texel-uses**, 소스 픽셀의 알파 **모두 255**. 이 `160`면은 v28 문서의 동일 선언면이므로 새 고유 face로 다시 세지 않음.
- GitHub `1.21.11/assets/minecraft/textures/block/oak_planks.png` 195바이트 직접 fetch → **독립 Python/Pillow `verify()`, RGBA 재해독** 및 파일 전체 Git blob SHA-1, SHA-256 재계산. Git blob SHA `e5a15780171bdff340a8bab625c31d0891e8ba5e`, SHA-256 `65665943ef9c8bcf63fc67d2083ed0c50243f724106d0e4bb1abea5d921b16d3`은 사용자 GitHub/기존 v4 선정 150텍스처 CSV 기록과 각각 **일치**했다. PNG **1종에 대한 독립 검증**이므로 다른 PNG 전체/공식 클라이언트 검증 완료로 확대해선 안 됨. v29 신규 PNG 종류 **0**.
- 원본 요소 비교: 일반→열림 시 **두 기둥 2/8 원시 좌표 동일, 나머지 6/8 이동·형상 조정**, y는 모두 불변; `in_wall`이면 원시 from/to.y **8/8 전부 정확히 -3**, 열림에서도 8/8 동일하게 -3. 정적 모델 인스턴스 차이이며 인게임 실시간 보간·collision이나 renderer 확인이 아님.
- 상태 16개는 4원형을 각각 4방향으로 선택하며 `uvlock:true`가 16/16 소스에 **명시**된다. **UVlock 실제 효과와 회전된 face 방향·인게임 화면은 미검증**. 독립 Mojang 공식 1.21.11 client.jar 확인도 미완료.
- 기존 v25–v28 바닐라 연구 및 v24 모드 연구 결과·지표는 그대로 둔다. **상위 1단계 최종 완료 0/5**, 01 바닐라 텍스처 선정 표본 150/150(전체 게임 아님), 02 바닐라 모델/상태/UV 진행 중. 게임 원본 `.class`/JSON/PNG는 사용자의 **공개 repo**에서 재배포되고 있으므로 별도 배포 권한·저작권 검토 필요. v29 커밋에는 원본 리소스를 복제하지 않고 파생 데이터와 해시만 올림.

## v30 — 복합 가구형 바닐라 5모델 91면 원본 텍스처 분석 / v26 수정 (2026-11-13)

- [v30 직접 분석·오류 정정보고서](research/vanilla_models/v30/00_v30_바닐라5모델_91면UV_18PNG_RGBA_투명도정정보고서.md), 원본 모델·PNG·blockstate·v4 비교 CSV 9개 및 JSON 1개를 GitHub에 저장. 소스는 사용자 저장소 `1.21.11/assets/minecraft/`의 실제 원본 PNG·모델 JSON·blockstate JSON이며 모든 산출물에 경로·Git blob SHA·표본 조건을 기재함.
- `lectern/grindstone/flower_pot/enchanting_table/template_anvil` **5모델 18요소·91고유 source face**, 원본 `faces.uv`의 PNG 범위 실제 RGBA 검사. 모루의 정상/금감/파손 leaf top 재질 3종으로 face×재질 **93개 레코드/6,012 texel-uses**, 전부 불투명. 이 중 `flower_pot` dirt 상단 1면은 기존 v26 표본 중복, **실제 화소 검증 신규 90고유 면**.
- 원본 **PNG 18개/4,608픽셀** 전체 해독: 불투명 **3,582**, 완전 투명 **1,026**, 부분 알파 0. v4 선정150종 표본에 포함되는 경로 **5개**, 그 밖 **13개**. v4 파일 길이/크기/가시·총 픽셀 **5/5 일치**. 기존 v26·v29에 판독한 `oak_planks/dirt`는 중복이며 프로젝트 신규 18종이라는 뜻은 아님. 전 PNG의 SHA-256을 v30에서 독립 재해시하지 않았음.
- 원본 blockstate 7 JSON의 **30 variants**(`lectern4/grindstone12/flower_pot1/enchanting_table1/anvil4/chipped_anvil4/damaged_anvil4`)를 별도 CSV로 기록. 이 30개에서 명시적 `uvlock:true` 0 (키 부재와 명시 false는 구분). `lectern`의 내부 element 회전 -22.5도, 숫돌 설치면별 x/y 회전, 모루 top 재질만 상태에 따라 바뀌는 parent 상속 사례를 확인했다. source 회전 속성이지 인게임 실제 회전/UVlock 검증은 아니다.
- **중요 v26 정정:** 자체 JS 디코더가 회색조 PNG `color_type=0`의 `tRNS` 투명색 키 0을 적용하지 않았다. 독립 Pillow에서 `stonecutter_saw`, `grindstone_round`, `grindstone_side`, `anvil_top` 4 PNG의 전체 화소를 재검사했으며 모두 새 표에 반영. **v26의 `stonecutter_saw` 16×48 불투명246/투명522**가 정답이다. v26 PNG8종 전체 픽셀 합 **불투명3,900/투명4,804**, v26 선택 모델 face-frame 70행 texel-uses **불투명3,328/투명324**로 바로잡고 [v26 보고서](research/vanilla_models/v26/00_v26_바닐라8PNG_전체RGBA_36면70프레임_실화소보고서.md), PNG CSV, UV CSV, JSON 요약도 수정했다.
- v8·v9의 `LecternBlockEntityRenderer`·`EnchantingTableBlockEntityRenderer`·book 모델 정보는 간접 출처/이전 연구이고, v30에서는 공식 런타임/책 애니메이션/인게임을 새로 검증하지 않음. **독립 Mojang 1.21.11 client.jar 인증 및 게임 조명/UV/회전 검증은 미완료.** 모드 v24 수치 그대로, 확정 완료 **0/5**. 공개 저장소 게임 원본 바이너리/JSON/PNG 재배포 권리 점검 필요.

## v31 — 책장/양조기 원본 multipart·합성조건 및 모닥불 켜짐/꺼짐 원시 모델 (2026-11-13)

- [v31 원본 source/실화소 연구 보고서](research/vanilla_models/v31/00_v31_책장양조기_264상태_47면_PNG실화소_모닥불원본보고서.md) · [59 source multipart 원본규칙](research/vanilla_models/v31/01_bookshelf_brewing_59_original_multipart_rules.csv) · [264 합성상태 조건 평가](research/vanilla_models/v31/02_bookshelf_256_and_brewing_8_combinations.csv) · [6 PNG 전체 RGBA](research/vanilla_models/v31/03_six_png_full_rgba_audit.csv) · [책장 17면×재질 픽셀](research/vanilla_models/v31/04_bookshelf_17_source_face_material_rgba.csv) · [양조기 36면 픽셀](research/vanilla_models/v31/06_brewing_36_face_original_png_rgba.csv) · [모닥불 원본 12요소/16 source variants](research/vanilla_models/v31/08_campfire_12_source_geometry_elements.csv).
- 사용자 `1.21.11` 원본 `chiseled_bookshelf` 블록 상태의 **52 multipart** 및 `brewing_stand`의 **7 multipart** 조건을 직접 파싱하여, 각각 **4×2^6=256**, **2^3=8** 총 **264개 입력**에서 원본 `when` 조건을 평가했다. 각 입력에 책장7모델/양조기4모델 적용 **256/256, 8/8**; 합성 적용 횟수 **1,824**는 원본 모델 고유 수가 아님. 원본 스펙을 JS 평가한 것으로 **Mojang 게임 모델 로더 직접 실행 검증 아님**.
- 책장 기본 source 모델 1요소·5면, 슬롯 템플릿 6개(0두께 1요소·1면)·공통 geometry에 occupied/empty leaf 12개가 각각 다른 PNG 텍스처 바인딩. **11 source face/17 face×material 재질표본**의 실제 원본 PNG 사각형을 전부 읽음, **1,792 texel-uses/불투명 전부**. 원본 기본 4규칙만 `uvlock:true`가 명시되어 있고 슬롯48규칙은 속성 키 부재. 게임의 실제 UVlock 수학·회전·컬링까지 입증한 것이 아님.
- 양조기는 원본 7 모델(기본4요소/24면 + 슬롯6개 각 1요소/2면), 36 source face / 실제 **2,016 texel-uses 중 불투명 1,260/완전 투명 756**. 슬롯의 0두께 양면 면형상과 `x=-0.41` 범위 밖 원시 좌표를 원본 JSON에서 확인. **실제 충돌 범위/렌더 가시성까지 검증하지 않음**.
- 원본 PNG6파일 **1,536 RGBA픽셀 (불투명1,410/완전 투명126/부분알파0)** 직접 전체 해독. 인덱스 팔레트 PNG의 `tRNS`도 적용. 기존 v4 선정 150표본의 `chiseled_bookshelf_occupied/empty` **2경로 중복**, 다른 4경로는 표본 밖. 기존 v4 2/2 파일 바이트·크기·가시/총픽셀 일치. 공식 1.21.11 game JAR에서 직접 획득했다는 독립 SHA 인증은 여전히 보류.
- 총 **47원본 source face + 53 face×material UV pixel records**에서 **3,808 texel-uses(불투명3,052/투명756)**를 얻었다. 이전 v7/v8에는 연결형/책장 구성의 일부 원본 구조·52조건 존재를 조사했으므로 모든 원본 JSON을 프로젝트 최초 발견 대상으로 합산 금지.
- 모닥불 source-only 선택 연구: `template_campfire` 7요소/32면(0두께2·회전2), `campfire_off` 5요소/28면(0두께0), 두 종류 blockstate 8+8variants, 두 불꽃 `.png.mcmeta`에 **`frametime=2`**. **실제 불꽃 PNG 원본 화소/프레임별 면 UV 대응은 v31에서 미수행**; 책장·양조기 47면에 포함하면 안 된다.
- **공식 Mojang Minecraft Java 1.21.11 client.jar 독립 획득/무결성 대조, 인게임 북쉘프/양조기/모닥불의 렌더·블록상태 회전/UVlock·애니메이션은 미확인**. 이전 v24 모드 계량과 최종 05 비교 진도는 그대로. 상위 1단계 내부 다섯 세부 작업 **최종 확정 0/5**. 저장소 `1.21.11/`에 공개된 원본 Mojang 에셋의 라이선스/재배포 권리 별도 점검 필요; v31 파생 CSV·보고서만 새로 추가.

## v32 — 사용자 애니메이션 보류 중, 정적 통/베틀/4작업대 7leaf 상속·25원본 PNG 전 화소 (2026-11-13)

- [v32 원본·실화소 보고서](research/vanilla_models/v32/00_v32_정적통베틀작업대_25PNG_42면암시UV_20상태보고서.md), [7 leaf/parent 구조](research/vanilla_models/v32/01_seven_leaf_parent_chain.csv), [42면 최종 재질 바인딩](research/vanilla_models/v32/02_42_inherited_cube_face_texture_bindings.csv), [PNG12 원본 RGBA](research/vanilla_models/v32/03_png_12_full_rgba_metrics.csv), [PNG13 원본 RGBA](research/vanilla_models/v32/04_png_13_full_rgba_metrics.csv), [42면별 계산된 암시 UV 픽셀](research/vanilla_models/v32/05_42_inherited_faces_png_full_rgba_evidence.csv), [20 blockstate](research/vanilla_models/v32/07_six_blocks_20_static_state_variants.csv), [통 원본 두 PNG 독립 SHA 검증](research/vanilla_models/v32/08_barrel_two_top_png_pillow_sha256.csv).
- 사용자 업로드 GitHub `1.21.11/assets/minecraft/`의 leaf 모델 7개와 최종 공유 템플릿 `cube`(기하 한 요소/6면), 중간 템플릿 `cube_bottom_top`, `orientable_with_bottom`을 원본 SHA 단위 조회. **7 leaf마다 자체 elements0, 상속 6면, 총42 leaf-specific 면-재질 인스턴스**이지 새 source geometry faces42가 아님. 이 부모 구조는 v25 기존 연구와 부분 중복. 표본 전체에서 **유일한 공통 source cube 면 선언은 6개**.
- leaf가 참조하는 원본 PNG **25경로 전 바이트를 Base64로 취득**해 4/8비트 인덱스 및 RGB PNG를 전 이미지 복호. **25×16²=6,400 RGBA 화소, 완전 불투명6,400, 알파0 및 부분 알파 0**. 기존 v4 선정150종과 **12경로 중복, 13경로 표본 밖**, 기존 v4 동일 경로의 파일 크기/치수/가시·전체 화소 **12/12 일치**. 이것은 원본 이미지 SHA-256 25개를 독립 재계산했다는 뜻 아님.
- `cube.json` source 면에는 **명시 UV가 없음**. source `cube`의 16×16×16 기하에서 full-face `[0,0,16,16]`을 **암시 UV로 추론**해 42 face×material의 256픽셀 각각, **10,752 texel-uses 모두 불투명**으로 계산. **게임 로더의 면별 UV 기호/방향·반전/UVlock/정적 렌더가 실측된 것은 아님**. 명시 UV 42면이 아닐 뿐 아니라 새로운 source 선언면 42개라고 기록해서도 안 됨.
- 원본 blockstate **6파일·20 variants**(통 12=6방향×열림닫힘 2, 베틀4, 4작업대 각1), source `x` 비0 10/`y` 비0 9, `uvlock` 키 **전부 미명시**. 통 `barrel_top`과 `barrel_top_open`은 static leaf 상속 기하 같지만 top 텍스처가 다르다. 원본 2PNG를 독립 Pillow `verify`/SHA-256/Git SHA1 검사하여 **256 RGBA 위치 중 132개 다름, 124개 동일**. 정적인 상태를 비교한 것일 뿐 **애니메이션 프레임 분석 안 함**.
- `client.jar` 공식 배포 출처·해시 독립 검증 및 실제 게임에서의 정적 UV 면 방향/회전·컬링·조명은 미완료. 과거 애니메이션 자료는 보존하되 신규 조사 **보류**. 모드 v24 연구 및 05 최종 비교 미완료 상태 유지, **상위 1단계 완료 확정 0/5**. 게임 원본 `.class`/JSON/PNG 공개 재배포 권한 검토 필요, v32 커밋엔 파생 보고서/표만 포함.

## v33 — 가마솥·호퍼·퇴비통: 12원본 모델/148 source face·12PNG 화소·15 정적 블록상태 (2026-11-13)

- [v33 실제 소스 분석 보고서](research/vanilla_models/v33/00_v33_가마솥호퍼퇴비통_148면_암시UV_PNG정적분석.md), [12 JSON/40요소](research/vanilla_models/v33/01_twelve_model_40_elements_geometry.csv), [148선언면 유도 UV](research/vanilla_models/v33/02_twelve_model_148_inferred_uv_faces.csv), [가마솥/호퍼 PNG7](research/vanilla_models/v33/04_cauldron_hopper_7_png_rgba.csv), [퇴비통 PNG5](research/vanilla_models/v33/06_composter_5_png_full_rgba.csv), [15 원본 정적 선택 규칙](research/vanilla_models/v33/08_three_blocks_15_source_static_state_rules.csv), [Pillow 4PNG 독립 검증](research/vanilla_models/v33/11_four_png_independent_pillow_sha256_crosschecks.csv) 및 JSON 요약 저장.
- 사용자 GitHub `1.21.11/assets/minecraft` 원본 12개 모델 JSON(`cauldron`1, `hopper/hopper_side`2, `composter`1 + `composter_contents1–7/ready`8)에서 **40 요소/148 원본 face 선언** 직접 확인. 모델별 수치 13/58, 7/32, 7/32, 5/18, 8/8. 기존 v25 모델 JSON 표본과 일부 선언 겹침 주의. **정적 상태별 모델 원형을 합산한 숫자**이므로 실제 한 화면 동시 렌더 면 수가 아님.
- `faces.*.uv`는 **148/148 전부 키 없음**. 계산된 `[u1,v1,u2,v2]`는 `from/to`와 면 방향을 사용한 **기하 파생 추론**이며, Fabric/Minecraft Wiki 공개 모델 사양의 암시 UV 규칙 설명을 참고했다. **실제 Mojang 1.21.11 모델 로더의 각 방향별 UV 계산 및 회전·컬링 구현을 검증하지 않았음**. 이 후보 사각형을 실제 원본 PNG 픽셀에 적용하여 중복 포함 **9,280 texel-uses/불투명9,280/완전투명0** 산출. 실제 GPU/화면 픽셀 수가 아님. 상세 유도식은 v33 보고서.
- **12 PNG 경로/3,072 원본 RGBA 픽셀**, 불투명2,332·완전투명740·부분0. `cauldron_inner`=`hopper_inside`는 Git SHA 동일 → **11개 고유 blob bytes**. v4 기존 150선정 PNG와 **경로 중복 0**, 단 `composter_top`은 v26 실측과 중복(112/144 결과 일치). `cauldron_bottom/hopper_top/composter_bottom/composter_ready` **4파일 독립 Pillow verify+RGBA+SHA-256 검증**, JS 전체 원본 디코더 통계와 4/4 일치.
- 상태: `cauldron` source variants1, `hopper`5, `composter` multipart9 = **15원본 규칙**. 퇴비통 **level 0..8, 9정적 상태**의 source 조건을 평가해 level0=본체 단독/level1..8=본체+내용물 모델1. 내용물 x/z=[2,14] 동일, 표면 y=3/5/7/9/11/13/15/15; level7/8은 동일 높이·다른 PNG. `hopper` 아래/측면 원형 7요소 중 **앞 여섯 요소 불변, 마지막 배출구 요소만 변경** 확인. 정적 비교이며 애니메이션이 아님.
- 여전히 Mojang 공식 1.21.11 `client.jar` 인증·실제 게임 렌더/자동 UV 면 방향/빛·회전 검증 미완료. **사용자 애니메이션 연구 일시 보류 계속 준수**, 과거 v9/v26/v31 동적 자료는 삭제 없이 보존. 가구 모드 v24 증거 및 Stage 1 03/04 계량 변경 없음, 최종 완료 **0/5**. 게임 원본 PNG/JSON/`.class` 공개 재배포 권한은 따로 확인해야 하며 v33에는 파생 데이터만 추가.

## v34 — 바닐라 전체 블록 모델 목록/정적 랜턴·촛불·막대 구조와 UV·PNG 픽셀 (2026-11-13)

- [v34 출처·측정 범위 상세 보고서](research/vanilla_models/v34/00_v34_바닐라2390모델_정적랜턴촛불_153면UV_전체목록.md) 및 소스 파생 CSV9개, JSON1개. 사용자 GitHub `1.21.11/assets/minecraft`의 **Git tree SHA를 지정하여 실제 원본 파일 경로 전체를 읽음**. `models/block` JSON **2,390경로/고유blob2,374**, `blockstates` JSON **1,168경로/고유blob1,015**, `textures/block` PNG **1,111경로/고유blob1,100**. 각 원본 SHA를 [모델 2,390](research/vanilla_models/v34/01_inventory_2390_block_model_paths_git_shas.csv), [상태1,168](research/vanilla_models/v34/02_inventory_1168_blockstate_paths_git_shas.csv), [PNG1,111](research/vanilla_models/v34/03_inventory_1111_block_texture_png_paths_git_shas.csv) CSV에 기록. 별도 `models/item` 1,283 JSON은 위 모델 범주에 넣지 않았고 블록 PNG `.mcmeta` 파일명 99경로는 내용/프레임 **읽지 않았음**.
- **위 총 4,669 파일 경로는 사용자 저장소의 카테고리 파일 목록**이며 바닐라 정적 가구형 모델 총수/고유 3D 형상수/모델의 PNG 실화소 검증 완료수를 나타내지 않는다. 본 project's 가구 모델링 목표 집합은 아직 선정·검증되지 않았으므로 **전체 진행도 퍼센트로 치환 금지**.
- 직접 읽은 원본 `template_lantern/template_hanging_lantern/template_candle/template_two_candles/template_three_candles/template_four_candles/end_rod/template_lightning_rod` **8형상 JSON/42요소/153고유 원본 선언면**, 전부 source 명시 `uv` 있음. `rotation` 선언 요소24/0두께 요소24, 방향 역순 UV 선언18면. 4랜턴 leaf/4촛불 unlit leaf/2피뢰침 leaf의 부모·재질 바인딩과 원본 5blockstates/30variants 별도 조회했다.
- **랜턴 2 템플릿 4+4요소/15+16명시 UV면**은 JSON 원본 형상·UV 범위까지만 확인. `lantern`/`soul_lantern` PNG 16×48의 픽셀/프레임/모션은 **사용자 애니메이션 분석 보류 요청을 존중하여 조사하지 않음**. 이 31 source 면의 선택 PNG alpha/색상은 v34에 실측 자료가 없다. 랜턴 4 leaf(일반/영혼·매달림여부)는 부모 기하를 공유하고 재질을 변경. 설치형과 매달기형의 본체 y차 1, 상단 지지 구조 길이/마디 차이는 실제 원본 기하 좌표에서 확인.
- 기본 `candle.png` unlit, `end_rod.png`, `lightning_rod.png` 원본 **3 PNG(각16×16)/768화소**는 원본 Git SHA/바이트를 Python Pillow `verify()`/독립 SHA256으로 검사하고 RGBA 전체 복호, **불투명119·완전투명649/부분알파0**. Pillow에서 만든 **16행 픽셀 알파 마스크**를 [원본 SHA/전체 RGBA 알파/마스크 CSV](research/vanilla_models/v34/06_three_static_png_pillow_sha256_alpha_masks.csv)에 저장. 4종 촛불 **100면/520 uses**, 엔드막대 **11면/172 uses**, 피뢰침 **11면/196 uses** → **122개 명시 UV source face의 원본 정적 PNG 888 repeated texel-uses 모두 불투명**. 이 데이터는 3개 PNG 고유 화소수 768 또는 게임 렌더 픽셀수와 다름. [153면 source JSON/122면 알파 실측](research/vanilla_models/v34/05_eight_source_models_153_explicit_uv_faces_static_alpha.csv).
- Blockstate 5 JSON `lantern`2+`soul_lantern`2+`candle`8+`end_rod`6+`lightning_rod`12 = **30원본 variants**, x비0 15/y비0 9/`uvlock` 키 부재30. `candle.lit` 및 `lightning_rod.powered`는 source JSON 상의 **고정된 상태 선택 참조만 조사**. 실제 시간적 점화 과정/애니메이션 프레임·키프레임 연구 아님.
- **공식 Minecraft Java 1.21.11 client.jar의 Mojang 출처·해시 독립 대조는 아직 없음**. 게임 실제 렌더/컬링·면별 UV/winding/uvlock/조명 재현도 미실시. 원본 PNG/JSON 공개 재배포 권한 검토 필요, v34 커밋에는 게임 원본 자산이 아닌 파생 소스 목록·해시·통계만 추가. 사용자 애니메이션 분석 보류 계속 적용. 이전 v24 모드/05단계 검토 현황 변경하지 않으며 완료0/5.

## v35 — P1 정적 종·케이크·벌통/벌집 source JSON/PNG·71 variants, 과거 전수 대조는 미완료 (2026-11-13)

- [v35 직접 소스/실화소 분석 보고서](research/vanilla_models/v35/00_v35_P1_종케이크벌통벌집_15모델_71상태_16PNG_분석보고서.md) · [P1 544개 후보별 v35 이번 회차 검수 원장](research/vanilla_models/v35/12_p1_544_static_source_review_ledger.csv) · [4개 원본 blockstates의 71 source variants](research/vanilla_models/v35/04_four_static_blockstates_71_variants.csv) · [종 케이크 75 source declared faces+RGBA](research/vanilla_models/v35/08_bell_cake_75_faces_png_uv_sampling.csv) · [벌 24 inherited face×material PNG](research/vanilla_models/v35/10_four_bee_leaf_24_parent_face_texel_records.csv) · [6 source PNG 별도 Pillow 교차검증](research/vanilla_models/v35/14_six_png_independent_pillow_sha256_rgba.csv).
- 사용자 GitHub `1.21.11/assets/minecraft/`에서 bell 설치4 leaf + cake 7 leaf + bee/nest 4 leaf **15 JSON** 및 공유 부모 `orientable_with_bottom,cube` **2 JSON**, blockstate JSON4, PNG16경로를 직접 읽음. 해당 15 leaf JSON의 SHA는 v34 P1 전체 파일 인벤토리 SHA와 **15/15 일치**. 기존 v5–v34 파일별 과거 수행 증거와 P1 544의 교집합은 **전수 대조하지 않음**, v35 조사15/P1 544는 **이번 회차 소스 감사 건수일 뿐 최종 완료율이 아님**.
- 원본 source face **bell 33 직접 선언(전부 명시 UV) + cake42 직접 선언(전부 암시 UV) + 공통 cube6 직접 선언(전부 암시 UV)** = **81 source declared faces**. 벌 네 leaf 원본 자체 요소0이나 동일 cube6면을 부모 상속해서 **24 face×material 사용 기록**. 따라서 이번 원본 PNG 면별 적용 기록 **99행**(33+42+24), source face가 99개라는 의미 아님. JSON 직접 요소: bell6+cake7+cube1. 모드 v24 결과와 숫자 혼합 금지.
- PNG **16경로×256 = 4,096 original RGBA 픽셀** 직접 Base64·PNG 압축/필터·인덱스 PLTE/tRNS/그레이스케일/알파 포함 복호, **3,496 불투명/600 완전투명/0부분 알파**. `bell_bottom`은 모델 `particle` 텍스처로 원본 통계에는 포함되지만 요소의 face 슬롯에 사용되지 않아 UV 면별 샘플에서 제외. 텍셀 참조는 bell33 source explicit 724 + cake42 derived implicit 4,032 + bee4leaf 상속 full-cube implicit 6,144 = **10,900 uses 모두 불투명**. `cake` 및 `bee`의 UV 사각형은 원본 JSON의 기하/부모 완전 정육면체에서 유도한 **추론**이며 Mojang 게임에서 텍스처 방향/winding/회전을 재현해 확인하지 않았음.
- `beehive_front`↔`beehive_front_honey` PNG 동일 좌표 비교 **24/256 픽셀 RGBA 다름**, `bee_nest_front`↔`bee_nest_front_honey` **25/256** 다름, 둘 다 알파값 변경0. Source honey_level 0..4 empty / 5 honey. 케이크 bites0..6의 `from.x`는 **1,3,5,7,9,11,13**, 나머지 구조 고정이며 `cake_inner` 절단면 재질. 종 model JSON 네 종류는 **지지대/부착 구조**만 확인: 종 본체 block-entity 특수 renderer·본체 실제 3D 기하는 **독립 클라이언트 미확인**.
- **별도 Python/Pillow `verify()`+전체 RGBA·SHA256**으로 PNG **6경로**만 검증(케이크 top/side, bee/nest 각 front empty/honey), 커스텀 JS 디코더와 alpha 집계 및 honey RGB 비교 일치. 나머지10경로를 독립 Pillow 검증한 것으로 기록하면 안 됨. 과거 v4 선정150 PNG와 v35의 16경로 직접 중복0이나 모든 과거 보고서/CSV 전역 중복 여부는 미확인.
- v35 **정적 source variants 71개**(bell16/cake7/beehive24/bee_nest24)의 `uvlock` 키는 원본에 전부 미명시. 오직 source 규칙 확인이며 실제 게임 배치/모델로더 `uvlock`, 컬링, 조명 검증 아님. 공식 Mojang Java Edition 1.21.11 `client.jar` 독립 출처·무결성 검증 없음. **사용자 지시: 애니메이션 프레임/움직임/동적 시각 분석 계속 보류**. Stage1 최종 완료 0/5, v24 모드 연구 지표 및 과거 동적 자료 그대로 보존.
