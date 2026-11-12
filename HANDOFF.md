# 인수인계 · Minecraft Furniture Style Research

> **새 채팅 진입점 / 단일 인수인계 기준 문서**  
> 최종 확인일: **2026-11-12 (KST)** · 현재 체크포인트: **v20**  
> 저장소: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research  
> **새 채팅에서 먼저 이 문서, [PROGRESS.md](PROGRESS.md), [SOURCES_AND_LIMITS.md](SOURCES_AND_LIMITS.md)를 읽고 기존 작업을 이어간다.**

## 1. 프로젝트 목표와 변경 불가 범위

- 상위 목표는 **마인크래프트와 잘 어울리는 가구 모델링 방식을 근거 기반으로 학습**하는 것.
- 사용자는 이 연구 프로젝트를 **상위 1단계(실제 바닐라/가구 모드 모델과 텍스처의 깊은 분석)** + **상위 2단계(검증된 관찰을 토대로 실용적 모델링 규칙서 작성)** 까지 하기로 결정했다.
- **Project Zomboid 가구를 Minecraft 모델로 변환하거나 실제 가구 3D 모델을 만드는 작업은 이 프로젝트 범위에서 제외한다.**
- 이 문서의 `01~05`는 **상위 1단계 내부의 세부 작업 번호**이다. 상위 2단계와 혼동하지 말 것.
- 실제 파일·정량 분석으로 근거를 모으고, 이미지를 보고 추측한 정보는 사실로 승격시키지 않는다. 완성될 때까지 진행 기록을 GitHub에 남긴다.

### 상위 1단계의 다섯 세부 작업

| 번호 | 범위 | 2026-11-12 상태 |
|---|---|---|
| 01 | 바닐라 재질·텍스처 | **150/150종 표본 확보·분석 완료**, 공식 게임 파일 대조 및 인게임 검증 **미완료** |
| 02 | 바닐라 3D 형태·모델 JSON·UV·상태·특수 렌더링 | **v10까지 연구 진행 중**, 전체 완료 판정 전 |
| 03 | Another Furniture·Macaw's Furniture·Handcrafted 등 가구 모드의 실제 3D 모델 | **Another 원형 69/69 제작자 고정 원본 JSON v20 직접 재조회·SHA 대조, 299 요소·1,362 원시 면 기하/UV 속성 실측**; v18 leaf 33개, Handcrafted 원형 120/leaf 16 기존 자료 유지. **Macaw 실제 JAR 모델 0개**. |
| 04 | 가구 모드 텍스처·UV·팔레트 | **기존 v19 Another PNG 53종/선정 804면 실제 RGBA**, v17 Handcrafted PNG 24종/선정 784면 실제 RGBA 유지. **v20 Another 69 원형의 raw UV/회전/cullface 1,362면 직접 검사**, 새 39원형의 leaf/PNG 실화소 상속 연결·Macaw/인게임 미완료. |
| 05 | 바닐라 ↔ 가구 모드 비교·공통 특성 검증 | **사전 비교: 의자·벤치·소파 5쌍 비교표만 작성, 바닐라·인게임 최종 검증 미시작** |

**확정 완료 0/5개.** 01의 100%는 **표본 수 목표**만 의미한다. 02는 미리 합의한 전체 분석 대상이 없어 퍼센트를 임의로 계산하면 안 된다.

## 2. 누적 연구 결과: v1–v20

| 체크포인트 | 내용 | 확인할 자료 |
|---|---|---|
| v1–v4 | 바닐라 텍스처 30→83→100→150종, 색상·밝기·투명도·재질 비교 | [v4 보고서](research/vanilla_textures/v4_150/11_누적150종_확장검증_보고서.md) |
| v5 | 바닐라 정적 모델과 상속·요소 크기 조사 | [v5 연구 폴더](research/vanilla_models/v5/) |
| v6 | 면별 UV·부모 템플릿·블록 상태 예제 확대 | [v6 연구 폴더](research/vanilla_models/v6/) |
| v7 | 울타리·담장·철창·유리판·선반 등 연결형 모델 21조합의 조건부 조립 | [v7 보고서](research/vanilla_models/v7/00_v7_연결형_조립분석_보고서.md) |
| v8 | 침대·상자·표지판 등 특수 렌더링 블록과 엔티티 텍스처·아틀라스 구분 | [v8 보고서](research/vanilla_models/v8/00_v8_특수렌더_정적동적_비교보고서.md) |
| v9 | 비공식 1.21.11 엔티티 모델 추출 JSON으로 **17모델/19레이어/55 기하 요소(0두께 15)** 및 애니메이션 **6모델/15클립/304 저장 키프레임** 계측 | [v9 기하 보고서](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md), [v9 애니메이션 보고서](research/vanilla_models/v9/03_v9_애니메이션_검토보고서.md) |
| v10 | v8 SQLite에 v9 측정 내용을 증분 SQL로 통합; 검증 상태를 테이블로 분리; 공식 JAR 로컬 검사기 작성 | [v10 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md) |
| v11 | Another Furniture 원형 템플릿 69종·완성형 상속 33종·블록 상태 12개·PNG 12종 | [v11 보고서](research/furniture_mods/v11/00_v11_AnotherFurniture_모델분석_보고서.md) |
| v12 | Handcrafted 원형 모델 **120종(810요소/4,860면/283회전/183평면)**, 생성형 16종, 블록 상태 12종, PNG 12종, 모드 간 5쌍 비교 | [v12 보고서](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md) |

| v13 | 기존 24 PNG 실화소·13모델 571면 UV 픽셀 격자 정렬 | [v13 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md) |
| v14 | 기존 16 leaf의 텍스처 슬롯 51건과 PNG 실측 근거를 새로 결합 | [v14 보고서](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md) |
| v15 | 기존 189개 모델 전체의 명시적 face 선언 밀도·회전·0두께·기본 블록 범위 초과를 **신규 파생 계량**, v13 PNG 24개 팔레트 중앙값 재집계 | [v15 보고서](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) |
| v16 | 고정 공식 제작자 커밋의 **미측정 PNG 12개 실제 화소 디코딩**과 원본 모델 JSON **30개 직접 SHA 대조**, **16 leaf의 786 면 인스턴스** 중 **784면→PNG/픽셀 좌표 결합** | [v16 보고서](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md) |
| v17 | Handcrafted **고정 원본 PNG 24개 재디코딩** 후 **784/784 모드 면 UV 사각형의 실제 RGBA 텍셀 검사** (0면적 172, 불투명 420, 투명/불투명 혼합 145, 완전 투명 47) | [v17 보고서](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md) |
| v18 | Another Furniture 제작자 원본 JSON 63개(33 leaf/30 template) SHA 직접 재검증, 807면 재질 경로 추적(모드 804/바닐라 3), 새 PNG 12종 실제 화소 분석·4비트 팔레트 지원 | [v18 보고서](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md) |
| v19 | Another Furniture 선정 33 leaf의 미측정 원본 PNG **29종 신규 완전 디코딩**, 원본 템플릿 UV로 **804/804 모드 면 실제 PNG 내부 픽셀·알파 조사**, 바닐라 dirt 3면 별도 보류 | [v19 보고서](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md) |
| v20 | 기존 원형 템플릿 **69/69 JSON** 제작자 고정 커밋 원본을 직접 재조회·SHA 검증, **1,362 선언 면·299 요소의 UV/회전/cullface** 속성 전수 표본 분석. Macaw 공식 JAR 확보는 환경 제약으로 미완료 | [v20 보고서](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md) |

### 실제 SQLite에서 확인된 행 수 (v10까지의 바닐라 DB)

v10 로컬 SQLite 스냅샷을 직접 열어 조회하고 `PRAGMA integrity_check = ok`, `PRAGMA foreign_key_check` 문제 0건을 확인함.

| 테이블 | 행 수 | 의미 |
|---|---:|---|
| `texture_stats_v4` | 150 | 표본 텍스처 수치 |
| `models` | 55 | v5 정적 모델·부모 템플릿 근거 |
| `blockstates` | 16 | v5 블록 상태 근거 |
| `elements` | 80 | 정적 3D 요소 |
| `uv_faces_v6` | 90 | UV 면별 기록 |
| `assembly_cases_v7` | 21 | 블록 상태별 조립 사례 |
| `assembly_parts_v7` | 53 | 사례에 채택된 모델 부품 |
| `assembly_primitives_v7` | 93 | 조립된 요소 인스턴스 |
| `special_block_evidence_v8` | 17 | 특수 렌더링 블록 |
| `texture_atlases_v8` | 6 | 아틀라스 근거 |
| `special_model_layers_v9` | 19 | 서로 다른 특수 모델 17종의 레이어 |
| `special_animation_clips_v9` | 15 | 특수 모델 애니메이션 클립 |
| `validation_audit_v10` | 6 | 직접 검증/부분 검증/미검증 분리 |

**주의:** v11~v20 모드 가구 측정·파생 수치는 CSV/MD로 저장되어 있으며 **v10 SQLite에는 아직 통합하지 않았다**. 또한 55 정적 모델, 17 특수 모델, 19 레이어, 55 기하 요소는 서로 다른 집계 단위다. 합쳐서 '총 모델 수'로 쓰면 안 된다.

### v11–v12 모드 실측 자료의 범위

- [Another Furniture v11 템플릿 69종](research/furniture_mods/v11/template_metrics_69_total.csv): 299개 요소, 1,362개 UV면, 0두께 요소 34개. 모드 소스는 Minecraft 1.21.1; 브랜치 SHA `57eb624cbb7f408d43398c7434b0d38d312cb55d`.
- [Handcrafted v12 작성 모델 120종 전체](research/furniture_mods/v12/handcrafted_authored_120_total.csv): 직접 정의된 810 요소, 4,860 UV 지정 면, 비영(0° 아님) 요소 회전 283건, 0두께 요소 183건. [생성형 16종 표본](research/furniture_mods/v12/handcrafted_generated_leaf_sample_16.csv), [블록 상태 12종](research/furniture_mods/v12/handcrafted_blockstates_12.csv), [PNG 헤더 12종](research/furniture_mods/v12/handcrafted_png_header_12.csv).
- Handcrafted 출처: `terrarium-earth/Handcrafted` `1.21.x` 커밋 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035` 고정. **120종은 authored 블록 모델 전체**, 11,989개 자동 생성 모델은 **경로만 전수**, 내용은 16종 표본을 확인한 것.
- [두 모드의 의자·벤치·소파 대표 5쌍 사전 비교](research/furniture_mods/v12/another_vs_handcrafted_5_category_pairs.csv): 형태 기준 선택 쌍이며 디자인 품질 우열의 검증이 아니다.
- **Macaw's Furniture** 1.21.11 Fabric 3.4.2 정식 게시 확인: https://modrinth.com/mod/macaws-furniture/version/xhmciaUD. 공식 공개 모델 원본 또는 배포 JAR의 직접 내용을 아직 확인하지 못함. **모델 실측 0건**이며 제3자 비검증 저장소를 원 제작자 소스로 쓰지 말 것.
- 두 모드 원본 리소스(모델/PNG)는 **All Rights Reserved**, GitHub에는 추출 측정값과 경로/해시만 보관. 1.21.1 모드 데이터와 바닐라 1.21.11의 버전이 다름.

### v13 실제 텍스처·UV 직접 검증

- [v13 상세 보고서](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md)
- [Another Furniture 12 PNG 픽셀 통계](research/furniture_mods/v13/another_png_12_pixel_metrics.csv) · [Handcrafted 12 PNG 픽셀 통계](research/furniture_mods/v13/handcrafted_png_12_pixel_metrics.csv) · [13 모델 571면 UV 정렬](research/furniture_mods/v13/uv_to_pixel_alignment_13_models.csv)
- **24/24 PNG SHA·해상도 교차 검증 및 전체 픽셀 디코딩 완료.** Another 6,912픽셀 중 가시 3,352, Handcrafted 110,592픽셀 중 가시 22,730. 두 표본 모두 반투명 알파(1~254) **0**; 이 수치가 실제 렌더 면적/디자인 우열을 뜻하지는 않음.
- **13개 모델, 571개 UV 면:** 모두 PNG 픽셀 경계에 정확히 정렬; 역방향 UV 면 190개, 0 면적 UV 면 64개(의도적 미러링/특수 기하 가능). **원본 모델의 정확한 face→PNG 픽셀 연결 및 인게임 관찰은 아직 하지 않음.**
- 직접 측정이 아닌 구두 설명으로 표본 수를 늘리지 말고 실제 원본 PNG·모델 JSON을 읽어야 한다. 로컬 재검증 소스: [scripts/reproduce_mod_png_v13.py](scripts/reproduce_mod_png_v13.py).
- 기존 1.21.11 바닐라 공식 JAR, Macaw 공식 JAR/모델 실측 0건, 게임 렌더 미검증 상태는 **그대로 유지**.

### v14 신규 교차 연결 감사 결과

- [상세 보고서](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md), [슬롯별 51건](research/furniture_mods/v14/handcrafted_texture_bindings_51.csv), [모델별 16건](research/furniture_mods/v14/handcrafted_leaf_coverage_16.csv), [미측정 PNG 12종](research/furniture_mods/v14/unsampled_mod_png_priority_12.csv), [입력 SHA·검증 등급 JSON](research/furniture_mods/v14/v14_binding_audit_summary.json).
- 기존 v12 leaf 16개가 가진 **51개 슬롯**을 파싱함. 모드 참조 35건 중 **19건은 v13 실측 PNG의 Git SHA·해상도 기록과 일치**, **16건은 표본 밖(고유 12 PNG)**. 별도 **16건**은 Minecraft 바닐라 텍스처 의존(미검증). 모든 모드 슬롯 연결 7 leaf, 일부 연결 13 leaf; v13 UV 표본 부모 해당 9 leaf.
- **이번에는 외부 원본 파일 바이트를 새로 읽지 않았다.** 따라서 19건은 기존 기록의 참조/근거 연결이고, face의 화소를 직접 재검증한 결과가 아니다. Another Furniture 33개 leaf CSV는 개수만 있고 텍스처 경로 데이터가 없어 실제 슬롯/PNG 연결을 만들지 않았다.
- 상위 1단계 세부 작업 완료 판정 **0/5**. v10 SQLite에 v11~v14 신규 가구 분석 결과를 통합한 것은 아니다.

### v20 Another Furniture 원형 69개 원본 SHA 및 1,362면 구조·UV 검증 (현재 최신)

- [v20 전체 보고서](research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md) · [원형 JSON 69개 SHA·geometry](research/furniture_mods/v20/another_69_templates_direct_original_geometry.csv) · [원본 1,362면 UV/회전/cullface](research/furniture_mods/v20/another_69_templates_1362_original_faces.csv) · [Git SHA 감사](research/furniture_mods/v20/v20_another_69_original_template_audit.json).
- 제작자 `crispytwig/AnotherFurniture` 고정 `57eb624c...`에서 **v11 선정 원형 JSON 69/69개 전체를 이번에 직접 재조회해 기존 Git SHA·요소/면 수와 일치 검증**, 그중 v18~v19 30개 외 **39개를 새로 직접 상세 조사**. 이것은 **원형 표본 69개**의 검증이며 모드 전체 1,451 모델 파일의 전수가 아님.
- **299 geometry elements / 1,362 선언 face**, raw UV 뒤집힘 **422면**, face UV 회전 **134면**, `cullface` 지정 **443면**, 0면적 UV **4면**, UV 키 누락 **0**. 회전 geometry element **17개**, 0두께 element **34개**, 0~16 바깥 raw bbox element **11개**(`chair_tucked`, `coat_hook`, `grandfather_clock_full`). 물리 충돌/렌더/화질 우열로 오인 금지.
- `table_full` 요소13·면74 중 평면8/UV회전61, `sofa_outer` 면21 중 cullface12, `small_shelf_double` 면48/회전 요소4, 커튼의 0두께 평면형 및 `grandfather_clock_full`의 raw bbox 확대 등 새 구체 관찰. v19 선정 leaf 33개 **804모드 면 실제 PNG UV RGBA**와 v17 Handcrafted **784모드 면** 결과를 유지하며, 이번 39개 원형의 새 face는 아직 leaf/PNG 픽셀까지 연결되지 않음.
- 공식 Macaw's Furniture [Minecraft 1.21.11 Fabric 3.4.2 Modrinth](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD) 존재 확인. 다만 실행 환경에서 **공식 1.21.11 JAR 다운로드/DNS 실패**, 실제 JAR 내부 모델 **0건 분석**; 공식 배포 존재 확인과 원본 실측은 다름. 바닐라 1.21.11 `client.jar`·인게임 또한 미검증. **5개 작업 확정 완료 0/5**.

### v19 Another Furniture 원본 PNG 53종/804면 UV 사각형 실화소 검증 (이전 체크포인트)

- [v19 상세 보고서](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md) · [Another 원본 PNG **53종** SHA/픽셀 통합](research/furniture_mods/v19/another_texture_53_png_source_manifest.csv) · [804면 실제 원본 UV 사각형 RGBA](research/furniture_mods/v19/another_804_face_actual_rgba.csv) · [807면 원본 UV 선언/경계 좌표](research/furniture_mods/v19/another_33_leaf_807_face_uv_rects.csv) · [53 PNG별 면 분포](research/furniture_mods/v19/another_53_png_face_actual_rgba_summary.csv) · [원본 감사 JSON](research/furniture_mods/v19/v19_original_png_face_rgba_audit.json).
- v18에서 고른 **33 leaf가 참조하는 모드 PNG 53종** 중 미측정 **29종을 이번에 제작자 고정 원본 `57eb624c...`에서 직접 가져와 PNG 전체 화소까지 분석**하여 **53/53종**. 53종 원본 PNG 전체 **17,408픽셀(불투명 11,536·투명 5,872·부분 알파 0)**, PNG 크기 **16×16 52개 / 64×64 1개**. **모드 전체 PNG가 아니라 선정된 leaf 표본 내 참조 경로 기준 100%**.
- 이번에 실제 원본 템플릿 **30 JSON을 고정 커밋에서 다시 읽고 SHA 교차 검증**, v18의 33 leaf 텍스처 상속 경로에 적용해 **807면 원본 UV**를 파싱. 그중 **804 모드 면 모두 PNG 원본 SHA/크기·정수 픽셀 경계·이미지 내 UV 사각형/실제 RGBA 샘플링** 완료. 바닐라 `minecraft:block/dirt` 의존 **3면**은 공식 원본 PNG 미확보.
- Another 804 모드 면: **712면 사각형 전체 불투명 / 88면 혼합 / 0면 전체 투명 / 4면 UV 면적 0**. 면별 중복 사용 포함 텍셀 샘플 **32,531회** 중 불투명 **31,545**, 투명 **986**, 부분 알파 **0**. 모드 면 중 역방향 UV **221면**.
- **누적 모드 원본 PNG 실화소 77종** = Another **53종** + Handcrafted **24종**. **Handcrafted 784/784 표본 모드 면(v17)**과 **Another 804/804 표본 모드 면(v19)** 모두 UV 안의 원본 픽셀 검사까지 끝남. [두 모드 표본만 비교한 자료](research/furniture_mods/v19/00_v19_모드간실제면UV픽셀_선정표본비교.md). 다른 가구 모델/JAR/바닐라 공식 PNG·인게임 렌더는 미완료, **5개 작업 최종 완료 0/5**.

### v18 Another Furniture 원본 JSON/PNG 및 807면 재질 경로 검증 (이전 체크포인트)

- [v18 상세 보고서](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md) · [완성형 33개 직접 SHA 확인](research/furniture_mods/v18/another_leaf_texture_resolved_33.csv) · [새로 확인한 실제 텍스처 슬롯 93건](research/furniture_mods/v18/another_leaf_slots_93.csv) · [템플릿 30개 직접 SHA 확인](research/furniture_mods/v18/another_template_direct_30.csv) · [113 면×재질 그룹](research/furniture_mods/v18/another_face_material_groups_113.csv) · [신규 PNG 12종 직접 픽셀 분석](research/furniture_mods/v18/another_new_png_12_pixel_metrics.csv).
- 원 제작자 `crispytwig/AnotherFurniture` Minecraft **1.21.1** 고정 원본 `57eb624c...`의 모델 JSON **63개를 직접 다시 읽고** 기존 v11 Git SHA와 63/63 일치. **33 leaf는 own elements 0**, 부모 원형 30종의 명시적 면 709개를 재료/면 인스턴스로 적용하여 **807개 면 인스턴스**의 원본 텍스처 슬롯을 추적함: **804모드 면 + 3 Minecraft dirt 면**, 참조 미해결 0건.
- 원본 leaf override 슬롯 **93건**, 최종 모드 PNG 경로 고유 **53종**, 기본 dirt 경로 1종. **588면**은 leaf override를 사용하고 **219면**은 원형 기본 재질을 사용. `block/dirt` 생략 표기 하나를 `minecraft:block/dirt`로 정규화하면서 원문 유지. 제작자 리소스 저작권 때문에 원본 JSON/PNG 재배포 없음.
- 과거 v13 Another PNG 12개 외에 **새로운 원본 PNG 12개를 실제 해독**해 3,072픽셀(불투명 2,156·완전 투명 916·부분 알파 0)을 검사. `sofa/wood_2`의 **4비트 팔레트 PNG**도 보완한 해독기로 확인. 이 33 leaf의 실제 모드 재질 53경로 중 PNG 실화소 검증 **24/53 (45.28%)**, 남은 29경로 미측정. 전체 모드 PNG 직접 실측은 **Another 24+Handcrafted 24 = 48종**.
- **엄격한 한계:** Another **807면의 face→원본 최종 경로 확인은 완료**, PNG 29종 및 **각 face의 정확한 UV 화소 사각형 내부 실측은 미완료**. Handcrafted v17의 784면 UV 실측과 구분. 게임 렌더/Macaw·바닐라 공식 JAR 미검증. 상위 1단계 세부 작업 완료 **0/5**.

### v17 원본 PNG 면별 실제 픽셀/알파 검증 (이전 체크포인트)

- [v17 상세 보고서](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md) · [784 면별 RGBA 통계](research/furniture_mods/v17/face_pixel_samples_784.csv) · [24종 텍스처별 집계](research/furniture_mods/v17/texture_face_pixel_usage_24.csv) · [16개 leaf별 집계](research/furniture_mods/v17/leaf_face_pixel_usage_16.csv) · [통합 감사 JSON](research/furniture_mods/v17/v17_pixel_region_summary.json).
- **원본 직접 실행 근거:** 고정 `terrarium-earth/Handcrafted` 커밋 `8d21d166...`에서 **원본 PNG 24개를 이번 턴에 다시 직접 읽어** Git blob SHA 대조 및 IDAT/zlib/PNG 필터/알파까지 해독. v16의 모델 면·slot/PNG 참조에 따른 **784/784 Handcrafted UV 사각형** 각각의 원본 RGBA 샘플링 완료(선정 표본 기준 100%, **새 독립 모델/PNG 발견이 아니라 기존 24종 재검사**).
- **실측 지표:** 784면 중 **612면 비영 사각형 / 172면 0면적**. 비영 사각형 중 **420면 완전 불투명 / 145면 불투명+완전투명 혼합 / 47면 완전 투명**. 사각형 전체 텍셀 사용 누계 **41,290회(불투명 31,665/완전투명 9,625/부분 알파 0)**. 251면 역방향 UV. 표면별 원본 PNG 픽셀의 재료 분포 통계이며 실제 게임에 보이는 면 개수/픽셀 수가 아님.
- **핵심 새로운 관찰:** `chair/cushion/black_cushion`은 PNG 전체 가시 372/4096(9.08%)지만 실제 쿠션 UV **6면의 328 텍셀 사용 모두 불투명**. `none_cushion` PNG에 연결된 **6면의 248 텍셀 사용은 모두 투명**. PNG 전체 팔레트 통계와 면이 실제 참조한 부분을 분리해 해석해야 함.
- **검증 상태:** 고정 원본 PNG·JSON 직접 근거 확보. `minecraft:block/oak_planks` 의존 **2면**/공식 Minecraft `client.jar`·Macaw 원본 모델 및 인게임 렌더 보류. [Pillow 독립 검증 스크립트](scripts/reproduce_v17_face_pixels.py)는 작성했으나 공식 원본 로컬 체크아웃으로 end-to-end 실행하지 않았음. **상위 1단계 0/5 최종 완료**, 전체 프로젝트의 의미 있는 완료 퍼센트를 임의 산출하지 말 것.

### v16 고정 원본 모델 JSON과 실제 PNG 화소·face 슬롯 연결

- [v16 상세 보고서](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md) · [신규 12 PNG 실화소 측정](research/furniture_mods/v16/handcrafted_12_new_png_pixel_metrics.csv) · [16 leaf 원본 51슬롯 확인](research/furniture_mods/v16/handcrafted_16_leaf_original_slots_confirmed.csv) · [16 leaf/36 재질·면 그룹](research/furniture_mods/v16/handcrafted_16_leaf_face_material_groups.csv) · [face 검증 감사 JSON](research/furniture_mods/v16/v16_original_face_mapping_audit.json) · [원본 로컬 재검증 스크립트](scripts/reproduce_v16_handcrafted_originals.py) (표준 라이브러리, 문법 테스트만 수행; 원본 로컬 end-to-end 미실행).
- **직접 새로 검증:** Handcrafted 원 제작자 커밋 `8d21d166...`에서 PNG 원본 **12종 추가 픽셀 완전 디코딩**(66,816픽셀; 가시 7,358/투명 59,458/부분 알파 0), 원본 JSON **30개**(생성형 16/원형 부모 14) Git blob SHA 재확인, leaf 텍스처 슬롯 **51개** 재확인.
- **face 인스턴스 786개** 중 Handcrafted 모드 PNG 24종에 연결된 **784면 모두** 정확한 파일 경로와 SHA·크기를 확보, UV의 PNG 픽셀 정수 격자 정렬·범위 내 위치 확인. 나머지 **2면은 `minecraft:block/oak_planks`**(공식 PNG 미검증). `bench/cushion/none_cushion` 및 `shelf/overlay/none`은 가시 픽셀 0인 완전 투명 PNG.
- **핵심 구분:** 786은 부모 기하가 복수 leaf에 재적용된 *면 인스턴스*, 고유 면 786개가 아니다. face 사각형 **내부**의 실제 픽셀 분포/알파 샘플링과 인게임 렌더 상태 확인은 여전히 미완료. 이전 v13 원본 PNG 12개와 v16 신규 12개로 Handcrafted 고유 24개 PNG의 실화소 근거 확보.
- **전체 확정 완료 0/5**, v10 SQLite에 모드 v11~v17 내용 미통합. 원본 PNG/JSON 저작권 에셋 미재배포.

### v15 신규 기하학적 표현 전략 분석

- [상세 보고서](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) · [189개 모델별 지표](research/furniture_mods/v15/model_geometry_derived_189.csv) · [Handcrafted 계열 22종](research/furniture_mods/v15/handcrafted_family_metrics_22.csv) · [입력 blob SHA와 검증 수준](research/furniture_mods/v15/v15_geometry_summary.json) · [오프라인 재검산 코드](scripts/verify_v15_geometry_research.py).
- Another Furniture 템플릿 69개(299요소)의 가능한 face 1,794개 중 **1,362면 명시·432면 비명시(75.92%)**, 회전 요소 17, 0두께 34, 원시 bbox 0..16 밖 모델 3개. Handcrafted 원형 120개 중 **112개 모델이 요소를 직접 보유**하고(8개 0요소), 가능한 face **4,860개 전부 명시(100%)**, 회전 요소 283, 0두께 183, 원시 bbox 밖 모델 60개.
- `table/*` Handcrafted 16모델 80요소: 회전 0/0두께 48. `couch/*` 6모델 38요소: 회전 24/0두께 0. 같은 모드 안에서도 형태 구현 전략이 달라진다는 관찰 근거.
- **v15에서 원본 게임/모드 JSON·PNG 바이트를 새로 읽지 않음.** 이전 체크포인트의 해시 보존 실측 CSV를 직접 다시 계산하여 파생 지표를 만들었음. 새 모델 실측 0건, 공식/인게임 검증 완료 0건. 원시 bbox는 렌더 최종 경계·충돌 모양이 아니다.
- 가구 제작·좀보이드 변환은 여전히 프로젝트 제외. 5개 세부 단계 **최종 완료 0/5**, v10 SQLite에 v11~v16 내용 미통합.

## 3. 데이터 위치와 버전 복원

- **v11 모드 실측 보고서/CSV:** [v11 분석 폴더](research/furniture_mods/v11/), [템플릿 69개](research/furniture_mods/v11/template_metrics_69_total.csv), [완성형 33개](research/furniture_mods/v11/representative_models_33_resolved.csv), [블록 상태 12개](research/furniture_mods/v11/blockstate_samples_12.csv), [PNG 헤더 12개](research/furniture_mods/v11/texture_png_header_12.csv). **v10 SQLite와 별도**로 저장.
- GitHub에 직접 저장된 바이너리 DB: [v8 SQLite](data/MC_Furniture_Style_Stage1_Research_v8.sqlite)
- v9 기하 CSV: [01_특수모델_부품요약.csv](research/vanilla_models/v9/01_특수모델_부품요약.csv)
- v9 애니메이션 CSV: [02_애니메이션_클립_실측.csv](research/vanilla_models/v9/02_애니메이션_클립_실측.csv)
- **v10 DB는 GitHub의 v8 SQLite + [v10 SQL migration](data/migrations/v8_to_v10.sql)으로 재구성:** [Python 스크립트](scripts/rebuild_v10_db.py)
- GitHub에는 **완성된 v10 SQLite 바이너리가 아직 업로드되지 않았다.** 이전 대화에서 별도의 파일로 제공된 v10 SQLite가 있더라도, 새 채팅에서 로컬 파일 접근을 보장하지 말고 GitHub 저장 파일로 복원하면 된다.

```bash
python scripts/rebuild_v10_db.py
# 새 파일: data/MC_Furniture_Style_Stage1_Research_v10.sqlite
# 확인: PRAGMA integrity_check == 'ok'
```

GitHub 접근 도구가 SQLite 바이너리 내용을 텍스트로 읽을 수 없는 경우에는 **바이너리 내용을 UTF-8로 해석하지 말고** 저장소 파일을 다운로드하거나 SQL·CSV 기록을 이용한다.

## 4. 사용 출처와 검증 수준

- **바닐라 Minecraft 버전:** Java Edition **1.21.11**로 고정. Another Furniture 모드 기준은 **1.21.1**, Handcrafted의 소스는 **1.21.x 브랜치**다. 서로 다른 버전의 수치/텍스처를 한 버전으로 묶지 말 것.
- **모드 고정 소스:** https://github.com/crispytwig/AnotherFurniture/tree/1.21.1 (조사 당시 branch HEAD `57eb624cbb7f408d43398c7434b0d38d312cb55d`). 해당 `resources/` 에셋은 원본 `LICENSE`에 의해 **All Rights Reserved**, 수치와 출처/해시만 보관.
- 바닐라 비공식 추출 원본: https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11
- 엔티티/블록엔티티 모델 추출 원본: https://github.com/InventivetalentDev/minecraft-entity-models/tree/1.21.11
- 모델마다 직접 읽은 추출본의 좌표·큐브 수·키프레임은 **그 추출본에 대한 사실**이지만 Mojang 공식 게임 파일과의 동일성은 별도 검증이 필요하다.
- 바닐라 스타일에 관한 일반화는 **관찰·측정·해석을 구분**, 사례의 대표성과 예외를 함께 기록.
- **미완료:** 공식 1.21.11 `client.jar`와 비공식 에셋 미러의 직접 해시/바이트 교차검증, 인게임의 바이옴 틴트·조명·투명도·배치/회전·애니메이션 재현.
- 공식 JAR 검증 보조: [로컬 검사 스크립트](scripts/verify_official_jar.py), [사용법](docs/official_client_jar_검증방법.md). 실제 1.21.11 JAR 입력은 아직 검증하지 않았으므로 **검증 완료로 처리하지 않는다.**
- 원본 Minecraft PNG/JSON/JAR 또는 제3자 모드의 비허가 에셋을 GitHub에 배포하지 말 것. 분석 결과와 출처/해시는 허용 범위를 검토해서 보관.

## 5. 새 채팅이 곧바로 이어갈 실제 작업

**작업 계획서를 반복 작성하지 말고 실제 데이터 분석을 진행한다.**

1. 이 파일을 읽고 [PROGRESS.md](PROGRESS.md), [v10 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md), [SOURCES_AND_LIMITS.md](SOURCES_AND_LIMITS.md)를 읽는다.
2. GitHub에서 **최신 파일/커밋 기준**으로 현재 상태를 확인한다. 새 채팅의 과거 기억과 충돌하면 GitHub 근거가 우선이며, 충돌 자체를 기록한다.
3. 가능한 경우 공식 JAR 비교를 수행한다. JAR이 없으면 검증을 **보류**하고, 검증 가능한 모델 회전/렌더 좌표 및 대표 사례를 추가 분석한다. 사용자에게 게임 파일을 공개 업로드하라고 요구하지 말 것.
4. 02번의 목표 범위·완료 조건을 정리하고 바닐라 연구 빈틈을 추적한다. **03번은 v11 Another Furniture와 v12 Handcrafted에서 실측을 수행했다.** 공식 게임 검증 보류 상태를 유지한 채 Macaw 공식 JAR 검증 또는 모드 UV·PNG 분석을 이어간다.
5. Handcrafted 원형 120개/Another 템플릿 69개는 기존 실측했고, **v15에서 189개 모델의 면 선언 밀도·회전·평면·기본 0..16 경계 초과를 새로 집계**했다. 기존 측정 복제 금지. 다음은 고정 원본에서 실제 face→슬롯→PNG 영역 확인, 공식 Macaw JAR, 또는 확장 좌표 모델의 실제 게임 회전·배치 검사다.
6. 작업이 끝날 때마다 새로운 보고서·CSV/SQLite·출처·검증 기록을 GitHub에 업로드한다. **[PROGRESS.md](PROGRESS.md), [README.md](README.md), 본 HANDOFF.md**도 새 체크포인트에 맞춰 함께 갱신한다.
7. 사용자에게 실제 수행·검증 완료 수치와 남은 작업을 분리한 진행도를 제공한다.

### 반드시 유지할 작업 원칙

- 할 수 있는 실제 분석은 현재 대화에서 수행하고 **시간만 약속하거나 재확인을 반복하지 않는다.**
- 측정 근거가 없는 **완료율 %**, 모델 수, 성공 판정, 업로드 완료를 지어내지 않는다.
- GitHub 업로드는 **쓰기 결과 + 원격 재조회**로 확인한다.
- 원본 파일을 그대로 재배포하지 않으며 라이선스/버전/파일 출처를 기록한다.
- **상위 2단계 규칙서 도출은 상위 1단계 관찰에 기반**해야 한다. 좀보이드 가구 변환이나 새로운 3D 가구 제작은 하지 않는다.

## 6. 새 채팅 시작 프롬프트

[새 채팅용 프롬프트 파일](docs/NEW_CHAT_START.md)을 열어 내용을 붙여넣거나 아래 한 문장을 사용한다.

> `https://github.com/sanato-nb/Minecraft_Furniture_Style_Research`의 `HANDOFF.md`를 먼저 전체 읽고, `PROGRESS.md`·최신 연구 DB/보고서를 확인해 Minecraft 가구 모델링 학습 프로젝트를 **v20 체크포인트부터 실제로 이어서 진행해 줘**. 기존 작업을 반복하지 말고 검증된 사실과 미검증 사항을 분리하고, 결과를 GitHub에 업로드한 뒤 HANDOFF/PROGRESS까지 갱신해 줘.

**바로 다음 작업:** v20에서 **Another 원형 69/69 JSON 직접 SHA·원시 face 1,362개 기하 분석**을 마쳤음. Macaw 공식 1.21.11 Fabric JAR URL은 확인했으나 다운로드 제약으로 **실측 0건**. 다음에는 **공식 Macaw JAR 바이너리 확보**, 공식 바닐라 1.21.11 `client.jar`, 이번 추가 **39개 원형의 leaf/PNG 실제 UV 연결**, 인게임 렌더 검증부터 수행. **확정 완료 0/5**.

## 7. 인수인계 유지 방법

- **정본:** 저장소 루트의 `HANDOFF.md` (현재 v20).
- **진행도:** `PROGRESS.md`.
- **새 채팅 복사용:** `docs/NEW_CHAT_START.md`.
- **기계 판독 상태:** `handoff/STATE.json`.
- 다음 체크포인트에서는 해당 파일을 실제로 업데이트하고 **날짜/버전/새로운 실측값/원본 링크/미완료**를 빠짐없이 남긴다.

