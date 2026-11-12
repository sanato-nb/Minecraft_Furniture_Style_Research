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
