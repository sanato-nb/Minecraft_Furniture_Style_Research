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
