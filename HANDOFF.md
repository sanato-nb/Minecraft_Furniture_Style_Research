# 인수인계 · Minecraft Furniture Style Research

> **새 채팅 진입점 / 단일 인수인계 기준 문서**  
> 최종 확인일: **2026-11-12 (KST)** · 현재 체크포인트: **v15**  
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
| 03 | Another Furniture·Macaw's Furniture·Handcrafted 등 가구 모드의 실제 3D 모델 | **v11 Another Furniture 템플릿 69/완성형 33/상태 12, v12 Handcrafted 원형 120/생성형 16/상태 12. v15 기존 실측 원장 189개를 새로 교차 계량(면 선언·회전·평면·bbox)함. Macaw 공식 소스 실측 0개** |
| 04 | 가구 모드 텍스처·UV·팔레트 | **v13 PNG 24종 실화소·13모델 UV 571면 정렬 측정. v14 기존 Handcrafted 16개 leaf의 텍스처 참조 51건 교차 결합(모드 35건 중 기존 PNG SHA 일치 19건 / v13 표본 밖 16건, 바닐라 의존 16건). 실제 face→PNG 화소 및 인게임 검증 미완료** |
| 05 | 바닐라 ↔ 가구 모드 비교·공통 특성 검증 | **사전 비교: 의자·벤치·소파 5쌍 비교표만 작성, 바닐라·인게임 최종 검증 미시작** |

**확정 완료 0/5개.** 01의 100%는 **표본 수 목표**만 의미한다. 02는 미리 합의한 전체 분석 대상이 없어 퍼센트를 임의로 계산하면 안 된다.

## 2. 누적 연구 결과: v1–v15

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

**주의:** v11~v15 모드 가구 측정·파생 수치는 CSV/MD로 저장되어 있으며 **v10 SQLite에는 아직 통합하지 않았다**. 또한 55 정적 모델, 17 특수 모델, 19 레이어, 55 기하 요소는 서로 다른 집계 단위다. 합쳐서 '총 모델 수'로 쓰면 안 된다.

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

### v15 신규 기하학적 표현 전략 분석

- [상세 보고서](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) · [189개 모델별 지표](research/furniture_mods/v15/model_geometry_derived_189.csv) · [Handcrafted 계열 22종](research/furniture_mods/v15/handcrafted_family_metrics_22.csv) · [입력 blob SHA와 검증 수준](research/furniture_mods/v15/v15_geometry_summary.json) · [오프라인 재검산 코드](scripts/verify_v15_geometry_research.py).
- Another Furniture 템플릿 69개(299요소)의 가능한 face 1,794개 중 **1,362면 명시·432면 비명시(75.92%)**, 회전 요소 17, 0두께 34, 원시 bbox 0..16 밖 모델 3개. Handcrafted 원형 120개 중 **112개 모델이 요소를 직접 보유**하고(8개 0요소), 가능한 face **4,860개 전부 명시(100%)**, 회전 요소 283, 0두께 183, 원시 bbox 밖 모델 60개.
- `table/*` Handcrafted 16모델 80요소: 회전 0/0두께 48. `couch/*` 6모델 38요소: 회전 24/0두께 0. 같은 모드 안에서도 형태 구현 전략이 달라진다는 관찰 근거.
- **v15에서 원본 게임/모드 JSON·PNG 바이트를 새로 읽지 않음.** 이전 체크포인트의 해시 보존 실측 CSV를 직접 다시 계산하여 파생 지표를 만들었음. 새 모델 실측 0건, 공식/인게임 검증 완료 0건. 원시 bbox는 렌더 최종 경계·충돌 모양이 아니다.
- 가구 제작·좀보이드 변환은 여전히 프로젝트 제외. 5개 세부 단계 **최종 완료 0/5**, v10 SQLite에 v11~v15 내용 미통합.

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

> `https://github.com/sanato-nb/Minecraft_Furniture_Style_Research`의 `HANDOFF.md`를 먼저 전체 읽고, `PROGRESS.md`·최신 연구 DB/보고서를 확인해 Minecraft 가구 모델링 학습 프로젝트를 **v15 체크포인트부터 실제로 이어서 진행해 줘**. 기존 작업을 반복하지 말고 검증된 사실과 미검증 사항을 분리하고, 결과를 GitHub에 업로드한 뒤 HANDOFF/PROGRESS까지 갱신해 줘.

**바로 다음 작업:** v15의 모델별 189개 파생 지표를 기준으로, 실제 원본 모델 JSON/PNG에 접근 가능한 환경에서 v14의 **미측정 12 PNG**와 `face→#texture slot→실제 픽셀` 정합성을 확인한다. v15에서 발견한 로컬 bbox 0..16 밖 모델 63개(두 모드 합계)의 인게임 배치 결과도 별도로 검증한다. 공식 바닐라 JAR 및 Macaw 원본 실측/게임 렌더 검증 보류.

## 7. 인수인계 유지 방법

- **정본:** 저장소 루트의 `HANDOFF.md` (현재 v15).
- **진행도:** `PROGRESS.md`.
- **새 채팅 복사용:** `docs/NEW_CHAT_START.md`.
- **기계 판독 상태:** `handoff/STATE.json`.
- 다음 체크포인트에서는 해당 파일을 실제로 업데이트하고 **날짜/버전/새로운 실측값/원본 링크/미완료**를 빠짐없이 남긴다.

