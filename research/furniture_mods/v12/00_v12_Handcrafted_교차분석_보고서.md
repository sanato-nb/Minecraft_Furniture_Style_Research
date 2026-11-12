# v12 — Handcrafted 원형 모델 전체 실측 및 Another Furniture 5유형 교차비교

- **기준 날짜:** 2026-11-12 (Asia/Seoul)
- **연구 범위:** 상위 1단계, 세부 03 모드 가구 3D 분석 / 04 모드 텍스처·UV 사전 검사 / 05 사전 비교 데이터
- **대상 소스:** [Terrarium Earth Handcrafted](https://github.com/terrarium-earth/Handcrafted) · `1.21.x` 브랜치 · **커밋 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`**
- **비교 소스:** [Another Furniture](https://github.com/crispytwig/AnotherFurniture/tree/1.21.1) · 1.21.1 / 기존 v11 분석
- **유의:** 바닐라 연구의 기준 버전은 Minecraft **1.21.11**이고, 두 모드는 **1.21.1 계열의 소스**다. 게임 버전·렌더링 결과의 동일성을 가정하지 않는다.

## 1. 확보·분석 범위

Handcrafted Git tree의 경로를 구분해 읽었다.

| 범주 | Git tree 확인 수량 | 직접 본문 실측 수량 | 데이터 위치 |
|---|---:|---:|---|
| 직접 작성된 블록 모델 JSON (authored) | **120** | **120** | [전체 모델 기하 측정 CSV](handcrafted_authored_120_total.csv) |
| 자동 생성된 블록 모델 JSON | **11,989** | **16** | [생성형 모델 표본](handcrafted_generated_leaf_sample_16.csv) |
| 자동 생성된 블록 상태 JSON | **263** | **12** | [블록 상태 표본](handcrafted_blockstates_12.csv) |
| 직접 작성된 블록 상태 JSON | **4** | **0** | 추가 확인 대상 |
| 블록 PNG (원본 모드 리소스) | **921** | **12 PNG 헤더** | [PNG 헤더 표본](handcrafted_png_header_12.csv) |
| 아이템 PNG | **55** | **0** | 미검토 |

이 파일 개수는 동일 디자인의 목재/색상/연결 방향 변형을 모두 포함한다. **11,989 = 고유 가구 디자인의 수가 아니다.** Git tree는 `truncated=false` 상태였다.

## 2. 직접 작성한 모델 120종의 기하 구조 실측

| 계량 항목 | 결과 |
|---|---:|
| 원형 모델 JSON | **120개** |
| 직접 `elements`가 있는 모델 | **112개** |
| 직접 `elements`가 없는 모델 | **8개** |
| 직접 정의된 큐브/평면 요소 합계 | **810개** |
| 직접 정의된 `faces` 항목 합계 | **4,860개** |
| `faces[].uv` 명시된 면 항목 | **4,860개** |
| 0°가 아닌 요소 회전이 정의된 항목 | **283개** |
| 하나 이상의 비영(非零) 회전 요소가 있는 모델 | **75개** |
| 한 축 두께가 정확히 0인 요소 | **183개** |

- 모델 수(120), 요소 수(810), 면 수(4,860)는 **서로 다른 집계 단위**이며 합산 금지.
- 모델 파일의 `elements` 값은 해당 JSON에서 직접 기록한 값이다. 부모가 지닌 부품까지 합산하거나 월드 배치 시점 변환을 적용한 완성 외접 상자 크기는 아니다.
- `rotated_elements`는 `rotation.angle != 0`로 기록된 **요소 회전**이며, 블록 상태의 90° 회전은 별도이다.
- 0두께 요소도 실제 모델 데이터의 기하 요소로 세었다. **렌더링 가시성이나 충돌 판정은 별도 문제**다.
- 8개의 `elements=0` 파일에는 `base/*` 6개와 `oven/oven`, `oven/oven_on`가 포함된다. 이것만으로 오븐이 화면에 존재하지 않는다고 단정할 수 없다.

### 원형 모델 비교 예

| 원형 모델 | 요소 수 | 요소 회전 수 | 0두께 수 | 모델 내 표기된 텍스처 시트 |
|---|---:|---:|---:|---|
| `chair/chair` | 13 | 3 | 5 | 64×64 |
| `bench/single` | 13 | 4 | 4 | 128×128 |
| `bench/middle` | 5 | 2 | 2 | 128×128 |
| `couch/single` | 8 | 6 | 0 | 128×128 |
| `couch/middle` | 4 | 2 | 0 | 128×128 |
| `table/single` | 10 | 0 | 5 | 64×64 |
| `table/center` | 2 | 0 | 1 | 64×64 |
| `fancy_bed/bed_single` | 12 | 1 | 0 | 128×128 |

**관찰:** Handcrafted는 벤치 등받이, 소파 쿠션 등 일부 형태에 **소수점 좌표와 각도 회전**을 활용한다. 예를 들어 `bench/single` 안에는 7.5° X축 회전 요소가 있다. 모든 모델이 회전된 것은 아니며, 테이블 계열은 샘플에서 비영 회전 없이 주로 부품 조합으로 구조를 표현했다.

## 3. 생성형 완성 모델과 블록 상태 구조

- 추출한 생성형 모델 표본 **16/16개**는 직접 `elements`가 **0개**이고 부모 모델(`parent`)과 목재·쿠션 등의 텍스처 참조를 지정했다.
- 예시: `oak_chair_white` → `handcrafted:block/chair/chair`(13개 요소); `oak_bench_middle_white` → `handcrafted:block/bench/middle`(5개 요소).
- 블록 상태 표본 12개는 `variants` 형식을 사용하며, 총 **4,724개 상태 항목**을 포함한다. 이 숫자도 **독립 디자인 수가 아님**.
- `oak_bench`는 색상·방향·연결 모양·waterlogged 조합으로 **1,088 상태**와 **136개 고유 모델 참조**를 갖는다. `oak_couch`는 1,024 상태/128 모델 참조, `oak_table`은 544 상태/272 모델 참조다.
- 상태 수보다 모델 수가 적은 예는 방향 회전 및 `waterlogged` 유무가 **같은 정적 모델**을 공유하기 때문이다.

## 4. PNG 헤더 검증 (12종)

PNG 원본 바이트의 시그니처와 IHDR 크기·색상 유형을 직접 확인했다. 화소별 팔레트 통계·실제 불투명 픽셀 수는 측정하지 않았다.

| 대상 | PNG 원본 크기 |
|---|---|
| 참나무·벚나무 의자 표면 | 64×64 |
| 의자 흰 쿠션 | 64×64 |
| 참나무 벤치·흰 쿠션 | 128×128 |
| 참나무 소파·흰 쿠션 | 128×128 |
| 테이블·책상·협탁·카운터 | 64×64 |
| 침대 흰 쿠션 | 128×128 |

**주의:** PNG `color_type=6`은 RGBA 채널 **지원**을 의미하지만, 실제로 알파 0 픽셀을 가졌다는 증거는 아니다. 의자 흰 쿠션 표본은 팔레트형 PNG(`color_type=3`)였다. 원본 전체 픽셀을 디코딩해 비교하는 일은 04번의 후속 과제다.

## 5. Another Furniture와 5개 범주 사전 비교

[표본 5쌍 원본 측정표](another_vs_handcrafted_5_category_pairs.csv)

| 가구 | Another Furniture 요소/회전 | Handcrafted 요소/회전 |
|---|---|---|
| 의자 일반형 | 10 / 0 | 13 / 3 |
| 벤치 독립형 | 7 / 0 | 13 / 4 |
| 벤치 중앙형 | 3 / 0 | 5 / 2 |
| 소파 독립형 | 16 / 0 | 8 / 6 |
| 소파 중앙형 | 4 / 0 | 4 / 2 |

양쪽 모두 같은 명칭의 **유사 범주**를 선택했지만 **동일한 물체의 모델을 복제한 사례가 아니므로** 요소 수를 품질·정교함·바닐라 친화도의 순위로 오해하지 않는다.

**관찰 가능한 차이:** Another Furniture 표본의 비영 회전이 0인 반면 Handcrafted 표본은 2~6개의 비영 회전을 가진다. **잠정 해석:** Handcrafted는 가구의 기울기·곡면 인상을 직육면체 회전으로 풀어내는 사례가 있고, Another Furniture의 비교 템플릿은 상대적으로 정렬된 큐브와 텍스처로 디테일을 표현한다. 전 모드에 걸친 통계적 규칙으로 확정하지 않았다.

## 6. Macaw's Furniture 조사 상태와 사용권

- 공식 게시: https://modrinth.com/mod/macaws-furniture
- Mojang 1.21.11용 공식 모드 버전 **3.4.2/Fabric** 게시 기록 확인: https://modrinth.com/mod/macaws-furniture/version/xhmciaUD
- 공식 GitHub `sketchmacaw/macawsmods`는 모드 제안/버전 및 이슈 안내 중심이다. 이 조사에서는 **Macaw's Furniture 원본 모델 소스가 있는 공식 공개 저장소를 검증하지 못했다**.
- 검색 결과에 등장하는 `TagBlacksmith/macaws-furniture` 같은 제3자 저장소는 **원 제작자 출처와 해시 동일성을 검증하지 못했으므로** 모델링 실측 데이터로 채택하지 않았다.
- **이번 v12에 Macaw 모델 파일 실측 수치 0개.** 향후 제작자가 배포한 정식 JAR(또는 검증된 공식 소스)을 확보하면 내부 모델·텍스처를 검토하되 원본을 재배포하지 않는다.

## 7. 라이선스·재현성·남은 검증

- Handcrafted 공식 GitHub `LICENSE`는 문서/코드 외 게임 리소스 모델 JSON 및 PNG 등을 **All Rights Reserved**로 규정한다. 원본 게임 에셋을 사용자 GitHub에 복사하지 않았고, 추출 수치·원본 경로·Git blob SHA만 기록했다.
- v12 분석 숫자는 GitHub에 저장한 `handcrafted_authored_120_total.csv`, `handcrafted_generated_leaf_sample_16.csv`, `handcrafted_blockstates_12.csv`, `handcrafted_png_header_12.csv` 및 대응 소스 파일로 재현할 수 있다.
- 모델의 **최종 렌더 회전/부모 합성/UV 면 이미지 크롭**, PNG 실제 색상·알파 통계, 인게임 스타일 비교는 계속 미완료다.
- 공식 바닐라 1.21.11 `client.jar` 직접 해시 검사도 이전과 같이 **미완료**다.
- 이후 03에서는 Macaw 공식 모드 JAR 실측, Handcrafted 원형과 자동생성형 모델의 재질 연결 전수분석; 04에서는 PNG 실제 픽셀 디코딩; 05에서는 동일 버전 환경에서 비교를 진행한다.

**상태 판정:** 03번 진행 중 / 04번 PNG 헤더 사전분석 진행 / 05번 대표 5쌍의 **사전 비교만 작성**(최종 검증 미착수). 01과 02의 기존 미검증 상태 변경 없음. 전체 5개 세부 작업 중 확정 완료 **0개**.
