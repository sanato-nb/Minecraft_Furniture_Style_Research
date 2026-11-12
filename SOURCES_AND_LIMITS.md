# 출처, 저작권 및 검증 한계

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

- 게임 원본 PNG/JSON/JAR는 저장소에 포함하지 않음.
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
