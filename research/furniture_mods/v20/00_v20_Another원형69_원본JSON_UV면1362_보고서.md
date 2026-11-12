# v20 — Another Furniture 원형 모델 69종의 원본 JSON·UV·기하 직접 검증

> 2026-11-12 KST, 이전 v19에서 계속한 실제 학습 연구. **이번 v20에서는 Macaw 공식 1.21.11 JAR 내부를 확보하지 못해 Macaw 모델을 분석했다는 주장을 하지 않는다.** 대신 원 제작자 Another Furniture **기존 분석 집합 69개 원형 JSON을 고정 커밋에서 전부 재조회**하고, v11 당시 정량값을 넘는 실제 면/회전/가림 속성 분석을 수행했다.

## 1. 원본·증거 출처

- 제작자 저장소: `crispytwig/AnotherFurniture`, 1.21.1 소스, 고정 commit `57eb624cbb7f408d43398c7434b0d38d312cb55d`.
- 기존 v11 문서에서 확보한 템플릿 JSON **69개 기록**, v18에서 완성형 33개에 직접 연결한 **부모 원형 30개**, v18의 선정 모델에서 사용하지 않았던 **나머지 원형 39개**를 분리하여 **원본 39개를 새로 상세 측정**했다.
- 추가로 30개도 같은 제작자 커밋에서 **다시 직접 열어 Git blob SHA를 확인**했고, 그 결과 **69/69 원본 JSON 해시·원본 요소 개수·명시 face 개수가 과거 v11 측정과 일치**했다.
- v20의 **새로운 독립 원본 모델 39개**라는 말은 'v11에서 존재를 처음 발견'한 의미가 아니다. **v11의 69개 기록 중 v18~v19가 직접 다시 검증한 30개 외 39개를 이번에 원본에서 새로 직접 확인한 것**이다.
- 제작자 저장소의 전체 모델 경로 개수(v11 조사 시 1,451개)는 별도로 존재한다. **69/69 (100%)는 v11에서 골라 놓은 원형 템플릿 표본의 SHA/면 원본 검증률**이지 전체 모드 모델 전수 검증률이 아니다.

## 2. 실제 원본 모델 JSON에서 계산한 기하·면 속성

| 항목 | 원본 69개 |
|---|---:|
| 제작자 JSON 원본을 직접 다시 읽고 기존 Git SHA 대조 | **69/69개** |
| 기존 선택 부모 30개 밖의 원형 JSON 이번 원본 직접 상세 검사 | **39개** |
| JSON `elements` 정의 수 | **299개** |
| 원본 `elements[*].faces`의 면 선언 수 | **1,362면** |
| 면 `uv` 키가 없는 경우 | **0면** |
| `uv` 한 축 이상이 거꾸로 선언된 면 | **422면** |
| UV 면적이 0인 면 | **4면** |
| face의 `rotation` 값이 0이 아닌 면 | **134면** |
| `cullface`가 명시된 면 | **443면** |
| face에 `tintindex`가 명시된 면 | **0면** |
| 회전값이 0이 아닌 `elements[*].rotation` | **17개 요소** |
| `from/to` 한 축 크기가 0인 평면형 요소 | **34개 요소** |
| 원시 `from/to` 중 0~16을 넘어가는 요소 | **11개 요소** |
| 이 원시 범위 초과 요소를 가진 템플릿 | **3개** (`chair_tucked`, `coat_hook`, `grandfather_clock_full`) |
| 원형 면이 참조하는 서로 다른 원문 슬롯 표기 | **28종** |

여기서 *요소*와 *면*은 다른 단위다. `UV 뒤집힘`은 소스 선언 방향, `cullface`는 소스의 가림 후보 선언일 뿐, 실제 인게임에 보이는 면의 최종 수·렌더 성능을 의미하지 않는다. 11개의 원시 bbox 밖 요소도 게임 충돌 박스나 실제 블록 차지 범위와 같다고 주장하지 않는다.

### 원본에서 직접 관찰한 사례

- **`table_full`** — 모델 요소 13개, 면 선언 **74개**, 그중 **8개가 평면형 요소**, UV 반전 58면, face UV 회전 61면. 단순히 16×16의 정육면체 한 개가 아닌, 다수 부품의 면과 방향을 조합하는 원형임을 검증.
- **`sofa_outer`** — 요소 4개, 면 21개 중 `cullface` 선언 **12면**, 재질 슬롯이 `seat_front`, `seat_side`, `seat_top`, `bottom`, `back`, `wood_1` 등으로 분리됨. 연결 위치나 실제 인게임 가림은 블록 상태 확인이 필요함.
- **`small_shelf_double`** — 요소 10개, 명시 면 **48개**, 요소 회전 4개, `cullface` 15면. 크기가 달라지는 선반 형태를 기존 작은 선반과 다른 원형으로 표현하는 사례.
- **`chair_tucked`** — 요소 10개, 면 46개, 원시 좌표 0~16을 넘어간 요소 5개. 좌표 초과가 바로 월드의 물리 충돌을 뜻하지는 않는다.
- **`curtain_left_bottom`** — 원형 1요소·2면, 그 요소의 두께가 0. **`curtain_left_top`** — 2요소·8면 중 1개 요소는 평면형. 유리·천·시트처럼 얇은 면을 `from/to` 동일 좌표로 표현하는 패턴의 실제 사례.
- **`flower_box_attached_middle`** — 3요소·16면 중 `cullface` 13면. 인접 블록과 이어지는 형태에서 가림 후보 선언을 사용하는 예.
- **`coat_hook`** — 2요소·12면, 원시 경계 초과 요소 1개, 회전 요소 1개.
- **`grandfather_clock_full`** — 요소 7개·면 23개, 평면형 요소 3개, 원시 경계 밖 요소 5개. 블록 하나의 0~16 좌표를 넘는 조형 패턴의 실제 사례.

이 사례들은 소스 JSON의 필드와 숫자에 근거하며, 사용자에게 화면 속 시각적 형태를 직접 렌더링해 검증했다고 주장하지 않는다.

## 3. 지난 단계와 결합해 배운 가구 모델링의 근거

1. **원형 모델과 마감 텍스처를 분리해 재사용** — v18 Another 완성형 33개 leaf는 자체 요소 0개이고 부모 템플릿을 참조하며, 93개의 texture override 슬롯을 가진다. 형태는 부모·색은 leaf에 유지하는 패턴.
2. **모델을 면·평면으로 세밀하게 분할** — 이번 원형 69개의 299 요소/1,362면 가운데 34개가 0두께 요소. 커튼·테이블·가구의 장식 표면에 응용 가능한 패턴이지만, 물리 충돌 규칙과 같지는 않음.
3. **UV 방향과 재질 슬롯을 별도 설계** — 원형 면 중 422면의 UV 방향 반전과 134면의 UV 회전이 실제 소스에서 존재. 면 종류·재질이 바뀌면 명시 UV와 텍스처 경로의 결합이 달라짐.
4. **연결 부품과 가림 후보** — 69개 원형 중 `bench_left/right`, `bench_back_left/right`, `sofa_outer`, `flower_box_attached_* `, `curtain_left/right` 등 별도 원형이 있고, `cullface`가 443면에 명시됨. 다만 **`cullface`가 곧 두 개의 가구를 자동 연결하는 규칙이라는 뜻은 아니다**. 실제 블록 상태 정의/게임 렌더가 필요.
5. **실제 텍스처 UV 영역을 면마다 확인** — v19에서 Another 완성형 33개가 참조하는 모드 PNG 53/53종 실화소, 모드 면 804/804의 원본 UV 내부 픽셀을 확인했고, v17 Handcrafted 784/784도 완료. 이 v20의 추가 39개 템플릿은 **아직 leaf/PNG와 직접 UV 픽셀 샘플링까지 이어 붙이지 않았으므로** 804/784면과 합산하지 않는다.

## 4. Macaw's Furniture 공식 배포 확인과 실제 모델 분석의 구분

- 제작자 배포: [Modrinth Macaw's Furniture Fabric 3.4.2 / Minecraft 1.21.11](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD), 공식 버전 ID `xhmciaUD`, Modrinth 프로젝트 `dtWC90iB`.
- 공식 배포 파일 이름: `mcw-furniture-3.4.2-mc1.21.11fabric.jar` (공식 Modrinth CDN 링크 `https://cdn.modrinth.com/data/dtWC90iB/versions/xhmciaUD/mcw-furniture-3.4.2-mc1.21.11fabric.jar`).
- **현재 실행 환경의 외부 DNS/직접 바이너리 다운로드 제약**으로 공식 JAR 바이트를 로컬에 확보하지 못함. 프로젝트의 GitHub 공식 개발자 소스에서 이 릴리스의 3D 자산 JSON을 확인하지도 못함. **Macaw 원본 모델 실측 0개, PNG 실제 픽셀 0개, UV/렌더 검증 0개**를 유지.
- `sketchmacaw/macawsmods` GitHub 저장소는 공개 건의/버전 안내용이며 위 JAR의 실제 3D 파일 대체 근거가 될 수 없다. 출처 미확인 제3자 JAR·비공식 복제 모델을 공식 모델의 근거로 사용하지 않는다.
- 사용자가 이미 공식 JAR를 갖고 있다면 다음 체크포인트에 해당 JAR를 제공받아 **SHA-512 검증, ZIP 내부의 `assets/mcwfurnitures/models`, `textures`, `blockstates` 실제 확인**을 해야 한다. 이 단계 전에는 Macaw를 완료로 판정하지 않는다.

## 5. 산출 파일

- [원본 69개 원형 모델의 직접 SHA·geometry·UV 통합 레코드](another_69_templates_direct_original_geometry.csv)
- [69개 템플릿, 원본의 **1,362면** face별 실측 레코드](another_69_templates_1362_original_faces.csv)
- [이름 접두어별 구조 분포 참고 CSV](another_69_template_prefix_grouping.csv) — 참고로 접두어는 **게임 내 공식 가구 카테고리가 아님**.
- [69 원본 JSON의 SHA·UV·요소 수 감사 결과](v20_another_69_original_template_audit.json)
- 이번에 원본 추가 검증한 39개는 `another_remaining_template_39_source_audit_batch_1/2/3_of_3.csv`과 `another_remaining_template_face_source_batch_1/2/3_of_3.csv`.
- 기존 v18 선정 템플릿 30개도 이번 단계에서 다시 읽어 전체 69에 맞춘 통합 기준으로 `another_selected_template_30_source_audit_batch_1/2/3_of_3.csv`와 면별 기록으로 남김.
- **원본 저작권 리소스 JSON/PNG/JAR 자체는 GitHub 연구 저장소에 재배포하지 않고 경로·SHA·기하 속성·계량만 기록**.

## 6. 다음 검사와 전체 진행도

| 상위 1단계의 세부 작업 | v20 현재 근거 | 최종 판정 |
|---|---|---|
| 01. 바닐라 텍스처/재질 | 선정 150/150종, 공식 1.21.11 JAR/인게임 미완료 | 진행 중 |
| 02. 바닐라 기하/특수 렌더 | v5~v10 기존 분석, 공식 JAR/인게임 미완료 | 진행 중 |
| 03. 가구 모드 구조 | **Another 원형 69/69 원본 JSON 재조회·SHA 확인 및 1,362면 실제 요소/UV 속성 분석**, Handcrafted 원형 120 기존 직접 측정, **Macaw 원본 0** | 진행 중 |
| 04. 가구 모드 PNG/UV | 선정 Another PNG 53종/804모드 면 원본 UV RGBA, Handcrafted PNG 24종/784모드 면 원본 UV RGBA 완료. 이번 추가 원형 39개 PNG 연결·게임 검증 미완료 | 진행 중 |
| 05. 비교/규칙 검증 | v19의 두 모드 선정 표본 비교, 최종 바닐라 대조/인게임 미완료 | 진행 중 |

**최종 5개 세부 작업 중 완료 판정: 0/5.** v20의 69/69(100%)는 **선정된 Another 원형 템플릿 집합의 재검증률**이고, 모드/바닐라/프로젝트 전체의 완료 퍼센트가 아니다.

**우선 후속 v21:** (1) 공식 Macaw JAR 실제 바이너리 확보와 원본 모델·PNG·UV, (2) Minecraft 1.21.11 `client.jar`에서 Another dirt 3면과 Handcrafted oak_planks 2면 공식 PNG 검증, (3) 이번 v20 추가 39개 원형에 연결되는 실제 생성형 leaf와 텍스처 경로 신규 확인, (4) 게임 내 렌더·컬링·UV 방향 확인, (5) 검증된 패턴을 모델링 규칙서로 정리. **이미 완료한 v19 선정 804모드 면 RGBA와 v17 Handcrafted 784모드 면 RGBA를 처음부터 반복하지 않음**.
