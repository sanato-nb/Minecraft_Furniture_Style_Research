# v11 — Another Furniture 모델링 실측 분석 (1차)

**분석일:** 2026-11-12 (KST)  
**상위 학습 단계:** 1단계 내부 세부 작업 **03. 가구 모드 3D 모델 분석**, **04. 모드 텍스처·UV 분석 사전 표본**  
**게임/모드 기준:** Minecraft Java **1.21.1**용 공개 [Another Furniture 소스](https://github.com/crispytwig/AnotherFurniture/tree/1.21.1), `crispytwig/AnotherFurniture` 브랜치 `1.21.1`, 조사 시 HEAD `57eb624cbb7f408d43398c7434b0d38d312cb55d`.  
**중요한 버전 차이:** 앞선 바닐라 분석은 **Java 1.21.11**, 이번 가구 모드는 **1.21.1**이다. 1.21.11 모드 호환을 주장하지 않으며 비교 시 차이를 명시한다.

## 1. 확인 대상과 측정 범위

| 항목 | 탐색/실측 수 | 의미 |
|---|---:|---|
| 공개 리포지토리 전체 트리 | **4,074개 엔트리** | 디렉터리·파일을 포함한 Git tree (최신 버전 고정 아님) |
| `assets/another_furniture/models/block` | **1,451개 JSON** | 전체 블록 모델 경로 수. 모두 개별 형태인 것은 아님 |
| `assets/another_furniture/textures` | **1,223개 PNG** | 전체 PNG 경로 수, 그중 블록 텍스처 1,220개 |
| `assets/another_furniture/blockstates` | **177개 JSON** | 버전 브랜치의 상태 정의 파일 수 |
| 실제 읽고 측정한 공통 `template/*.json` | **69/69개** | 모델 69개, 모든 직접 요소·UV 면 수 검사 |
| 실제 읽고 상속 확인한 완성형 모델 | **33개** | 목재/색상/상태가 있는 대표 모델 표본 |
| 실제 읽고 상태 구조 집계한 블록 상태 | **12개** | 802개의 variants/multipart 항목(12개 파일의 항목 수 합계) |
| 실제 읽고 PNG 헤더를 확인한 모드 텍스처 | **12개** | PNG 헤더 기준, 픽셀 분포·시각적 품질까지 검수한 것은 아님 |

모든 수치는 **해당 Git 브랜치의 구조와 읽어들인 파일**에 국한된다. 모델이나 PNG 자체는 이 저장소에 복제하지 않는다.

## 2. 공통 템플릿 69종의 3D 기하 구조

- `elements` 합계 **299개**; 모델당 평균 **4.33개** (모든 템플릿의 요소를 단순 합계한 값, 독립 가구 수를 뜻하지 않음).
- 지정된 `faces` 합계 **1,362개**; 그중 **1,362개 면에 명시적 UV 좌표**가 존재했다.
- 정확히 어느 한 축의 `from/to` 값이 같은 **0두께 요소 34개**, 0두께 요소가 1개 이상 있는 템플릿 **20종**.
- `rotation.angle != 0`인 요소를 하나 이상 가진 템플릿 **10종**.
- 로컬 미회전 좌표 외접 범위가 `[0,16]`을 벗어난 모델 **3종**: `chair_tucked`, `coat_hook`, `grandfather_clock_full`. 이것이 실제 배치/렌더링의 블록 점유 범위와 같다는 뜻은 아니다.

| 템플릿 | 3D 요소 | UV 지정 면 | 특징 |
|---|---:|---:|---|
| `chair` | 10 | 46 | 좌판/등받이/다리로 구성되는 여러 요소 |
| `chair_tucked` | 10 | 46 | 의자 형태 유지, 좌표 범위 달라짐 (z −7~5) |
| `bench_single` | 7 | 34 | 독립형 벤치 |
| `bench_middle` | 3 | 10 | 벤치 중앙 연결 부품 |
| `sofa` | 16 | 65 | 기본 소파 |
| `sofa_middle` | 4 | 17 | 소파 중앙 연결 부품 |
| `table_top` | 1 | 6 | 상판 0~16×13~16×0~16, 두께 3 |
| `table_leg` | 3 | 9 | 테이블 다리용 별도 연결 요소 |
| `table_full` | 13 | 74 | 전체형 테이블 구성 |
| `stool` | 5 | 26 | 일반 스툴 |
| `shelf_full` | 5 | 24 | 모델 요소 일부에 실제 회전, 소수점 좌표 |
| `drawer` | 1 | 6 | 겉 형태는 단일 큐브로 표현 |

위 **치수·요소 수는 실제 JSON 템플릿의 값**이다. 바닐라 스타일에서의 최적 크기나 제작 권장치로 바로 확정하지 않는다.

## 3. 대표 완성형 33개와 부모 모델 상속

- **33/33개** 완성형 표본에 자체 `elements`는 없고 부모 모델을 사용했다. **33/33개 상속 템플릿까지 해석 성공**.
- 일반 참나무 의자 `chair/oak_1` → `template/chair` (10요소).
- 자작나무 의자 `chair/birch_1` → `template/chair` (10요소).
- 의자의 등받이 디자인 변형 `chair/oak_4`도 `template/chair`를 공유하며 텍스처 슬롯 `back`을 바꾼다.
- `drawer/oak_open` → `drawer/oak` → `template/drawer`. **완성형을 다시 상속하는 2단계 연결**도 확인했다.
- 다른 소파 연결 모델 `sofa/white_middle` → `template/sofa_middle` (4요소).

**완성형 파일 자체의 요소 수가 0이므로 0요소 가구라고 해석하면 틀린다.** 부모 템플릿의 기하 요소가 상속된다.

## 4. 블록 상태 정의 12개

- **`variants` 방식: 10개 파일**, **`multipart` 방식: 2개 파일**(`oak_table`, `oak_bench`).
- 12개에서 **802개 항목**을 집계. 이는 **조사한 상태 JSON의 entry 수 합계**이지 '고유한 게임 블록 상태 802종'이나 '모드 전체 상태'라는 뜻이 아니다.
- `oak_chair`: **88개 variants**, 서로 다른 **22개 모델 참조**. 의자 디자인 11종 × 좌석 뒤로 밀린 상태 2개 × 방향 4개로 구분.
- `white_sofa`: 32개 variants, 모델 참조 6종. `single/left/right/middle/inner/outer` 형태.
- `oak_bench`: 32개 multipart entry, 모델 8종을 상황별 조합. 연결형은 중앙 부품을 따로 생성.
- `oak_table`: 8개 multipart entry, 상판/다리 **2종 모델**을 조건부로 겹쳐 조립.
- `oak_shutter`: 528개 variants, 44개 모델 참조. 특정 가구 하나가 많은 상태를 갖는 이유와 모델 개수를 혼동하면 안 된다.
- `oak_drawer`: 8개 variants, 기본/열림 2개 모델 참조. `drawer/oak_open`은 `drawer/oak` 모델의 상속 기반으로 텍스처를 덮어쓴다.

## 5. 텍스처 조사 착수 (세부 작업 04의 사전 실측)

PNG **12개를 실제 다운로드하여 헤더(signature/IHDR, 컬러 타입, PLTE, tRNS)만 조사**했다.

- **11개가 16×16**, `bench/oak.png` **1개는 64×64**.
- 12개 중 11개는 PNG 컬러 타입 **6(RGBA)**, `drawer/oak_front.png`는 **2(RGB)**.
- RGBA 파일에 `tRNS` 청크가 없더라도 **알파 채널이 존재하므로 투명 픽셀이 전혀 없다고 결론낼 수 없다.**
- 실제 색상 수·알파 분포·UV 텍스처 매칭의 시각적 검증은 다음 작업. 단일 PNG의 헤더만으로 텍스처의 재질이나 색감을 단정하지 않는다.

## 6. 저작권과 출처

[모드의 `LICENSE`](https://github.com/crispytwig/AnotherFurniture/blob/1.21.1/LICENSE)에 따르면 **`common/src/main/resources/`, `fabric/src/main/resources/`, `forge/src/main/resources/`의 리소스 및 하위 파일은 All Rights Reserved**, 그 외 파일에는 MIT 라이선스가 적용된다.

따라서 **모델 원본 JSON·PNG 파일을 연구 저장소에 복사하거나 재배포하지 않는다.** 본 분석은 경로·Git SHA·수치·해석·출처 링크만 기록한다.

## 7. 다음 작업/미완료

- **03은 진행 중:** Macaw's Furniture와 Handcrafted의 실제 배포 에셋 접근성·버전·라이선스 확인 후 동일 모델 유형(의자/소파/테이블/수납)을 비교 분석.
- **04는 사전 분석 시작:** PNG 12개의 메타데이터만 검증했다. 다음에는 더 넓은 표본의 픽셀 내용(알파/팔레트/명암/UV 매핑)을 실측.
- **05는 미시작:** 바닐라 1.21.11과 모드 1.21.1의 버전 차이를 보존하면서 수치 비교 기준부터 마련해야 한다.
- **01/02 공식 검증은 보류:** Mojang 공식 `client.jar` 바이트 대조·인게임 관찰은 진행되지 않았다.
- 실측 기록: [템플릿 69개](template_metrics_69_total.csv), [완성형 33개](representative_models_33_resolved.csv), [블록 상태 12개](blockstate_samples_12.csv), [PNG 헤더 12개](texture_png_header_12.csv).

**결론은 모델링 규칙 확정이 아닌 파일 근거 수집과 비교기준 마련이다.**
