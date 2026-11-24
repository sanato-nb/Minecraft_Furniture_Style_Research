# INT-4 H21 — AF 16개 역사 연구 사례의 4.0.3 Git / 4.0.2 Fabric 원본 비교

## 목적과 원본
H20 #102 모델링 계약 V2 41/70에서 AF 16건의 버전 차이 조건을 해소한다. 연구 원본 Git crispytwig/AnotherFurniture commit 57eb624cbb7f408d43398c7434b0d38d312cb55d (gradle mod_version=4.0.3), 공식 Modrinth Fabric 4.0.2 JAR SHA1 c2f992081bdc4795ed6d87771a3b5f7c71103785 / SHA256 3f0e6c276dde5cd6390e9c14bc4c283e4043f25d812c1f5ecc36b7b2f61642b5. 외부 바닐라 부모/텍스처는 Mojang 1.21.1 client SHA1 30c73b1c5da787909b2f73340419fdf13b9def88에서 직접 해결한다. Git 4.0.3 연구 소스는 공식 Fabric 4.0.3 배포 JAR라고 부르지 않는다.

## 직접 원본 검증
[Actions #45338341581 성공](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45338341581). 8/8 회귀시험 성공. Git 원본 ZIP / AF 공식 JAR / Mojang client 직접 열람 및 CRC 검사, 역사 application/face 원장 blob SHA 고정. variants 및 multipart 실제 선택자와 x/y, uvlock, weight를 비교; 각 적용의 전체 상속, geometry provider, face texture aliases, 명시/기본 UV와 회전, cullface 및 tintindex 비교. 각 역사 면의 원본 PNG SHA와 두 버전의 실제 PNG RGBA 및 mcmeta 비교.

| 항목 | 결과 |
|---|---:|
| 역사 AF 사례 | 16/16 |
| 적용 모델 | 21/21 |
| 원본 면별 UV / PNG 해시 연결 | 535/535 |
| 선택 상태·모델·부모 JSON 내용 일치 | 41/41 |
| JSON 원본 바이트 일치 | 1/41 (공용 바닐라 block.json) |
| AF JSON 바이트 차이지만 파싱 내용 일치 | 40/40 |
| PNG 원본 바이트 및 RGBA, 애니메이션 메타데이터 내용 일치 | 39/39 |
| 전체 자산 내용 일치 | 80/80 |
| 전체 자산 바이트 일치 | 40/80 |

39개 PNG에는 공용 vanilla dirt.png 1개가 포함된다. 41개 JSON에는 vanilla block/block.json 1개 포함. AF 전체 릴리스의 Java 코드, 모든 모델/상태, 아이템/게임플레이, GPU per-face attribution이 동일하다고 주장하지 않는다.

## 사례별 결과

| 사례 | 적용 | 면 | 판정 |
|---|---:|---:|---|
| S01 oak chair | 1 | 46 | PASS |
| S02 oak tucked chair | 1 | 46 | PASS |
| S03 birch chair south variant3 | 1 | 46 | PASS |
| S04 spruce chair south variant3 | 1 | 46 | PASS |
| S05 white stool | 1 | 26 | PASS |
| S14 oak table 4 legs | 5 | 42 | PASS |
| S15 oak table no legs | 1 | 6 | PASS |
| S20 oak drawer closed | 1 | 6 | PASS |
| S21 oak drawer open | 1 | 6 | PASS |
| S26 oak shelf | 1 | 24 | PASS |
| S30 oak bench back | 2 | 46 | PASS |
| S31 oak bench no back | 1 | 34 | PASS |
| S32 white sofa | 1 | 65 | PASS |
| S44 white lamp off | 1 | 37 | PASS |
| S45 white lamp on | 1 | 37 | PASS |
| S46 oak flower box | 1 | 22 | PASS |

F11F/H6/H97 원래 실제 게임 증거를 재사용한다. S14/S15는 기존 nonchair run 44986580186의 exact server state, F2 SHA, 원본 AF JAR pin 및 실제 선택 적용까지 대조했다. S20/S21 기존 남동 카메라 동일 PNG 예외는 지우지 않는다. H17 및 #97 북향 실제 F2 run 45251124211의 정확 상태 2건, 화면 1208픽셀 변화 증거를 재사용한다. S02는 실패했던 F4 F2가 아닌 F6 원래 정확 상태 복구 증거를 유지한다. 새 게임/F2 0회/0장. 신규 수동 육안 조사 없음.

## 모델링 계약 V3
- 역사 모델 50/62, 위험 질문 7/8.
- 합산 검토 단위 57/70 (81.4%), 조건부 13, 보류 0.
- V2에서 위 AF 16행의 모델링 상태/사유/증거/후속만 갱신. 54행 및 기존 승인 열 그대로 보존.
- 기존 엄격 F70 무조건0/70, H03 HOLD / H05 CONDITIONAL, INT5 의미 0, INT6 권리 0. 원본 F70 승인 기준 변경 없음.
- 잔여 12 역사 HC/Macaw 실행 원본 출처 정합성 및 R06 물 표면 시간 변화 1건.

## 산출
`INT4_H21_AF16_RELEASE_SOURCE_UV_RESULT_V1.json`, `INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V3.csv`, `INT4_F70_MODELING_CONTRACT_SUMMARY_V3.json`, 원본 재현/회귀시험/단일 cohort delta 검산 및 Actions. [파생 아티팩트 #14894607161](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45338341581/artifacts/14894607161). 원본 JAR·PNG·소스 원본 미복제.
