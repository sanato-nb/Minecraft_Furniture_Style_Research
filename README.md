# Minecraft Furniture Style Research

> **새 채팅에서 재개하려면 먼저 [HANDOFF.md](HANDOFF.md)를 읽으세요.** [새 채팅 시작 문장](docs/NEW_CHAT_START.md) · [기계 판독 상태](handoff/STATE.json) · [현재 진행도](PROGRESS.md)

마인크래프트 바닐라 블록의 **재질·텍스처·3D 형상·UV·블록 상태·특수 렌더링** 연구 자료를 정리한 저장소입니다.

> **범위:** Minecraft Java Edition **1.21.11** 기준, 가구 모델링 학습의 **1단계 분석 자료**입니다. 실제 가구 제작이나 Project Zomboid 가구 변환은 포함하지 않습니다.

## 현재까지 축적된 연구

| 체크포인트 | 분석 내용 | 상태 |
|---|---|---|
| v1–v4 | 바닐라 텍스처 **150종**에 대한 재질별 픽셀 통계 및 비교 | 표본 분석 완료 / 공식 JAR 대조 및 인게임 검증 미완료 |
| v5 | 바닐라 모델 55개 및 상태 16개 근거, 3D 구성/치수 | 대표 사례 기록 |
| v6 | UV 면 **90건**, 3D 모델 및 블록 상태 추가 분석 | 대표 사례 기록 |
| v7 | 연결형 블록 **8종, 조립 상황 21개** | 선택한 사례의 조건부 모델 조립 분석 |
| v8 | 특수 렌더링 관련 블록 **17종**, 아틀라스 6개, 텍스처 메타데이터 19건 | 대표 사례 기록 |
| v9 | 특수 렌더링 실제 기하 모델 17종/55개 요소, 애니메이션 15개 클립 | 비공식 추출 모델 직접 분석 / 공식 JAR·인게임 검증 대기 |
| v10 | v8 SQLite에 v9 측정값 통합, 신규 DB 3개 테이블·SQL migration | 로컬 SQLite 무결성 검증 / 공식 JAR·인게임 검증 대기 |
| v11 | Another Furniture(1.21.1) 모델 템플릿 **69개**, 완성형 상속 **33개**, 블록 상태 **12개**, PNG 헤더 **12개** 실측 | 03 모드 3D 분석 착수, 04 모드 텍스처 사전 표본 시작 |
| v12 | Handcrafted 원형 120종(810 요소), 생성형 16종 상속, 12개 블록 상태, PNG 12개, 모드 간 5유형 비교 | 원본 파일 실측, 픽셀·인게임 검증과 Macaw 공식 JAR 실측 보류 |
| v13 | Another Furniture·Handcrafted PNG **각 12개 실제 화소 분석(24개)**, UV **13모델·571면 정렬 실측** | 고정 Git 원본 SHA 일치, 정확한 재질/face 연결·인게임 결과는 미검증 |
| v14 | Handcrafted 16개 생성형 leaf의 **51개 텍스처 슬롯 참조** 교차검사 | v13 PNG 근거 연결 19건·표본 밖 16건(고유 12 PNG)·Minecraft 의존 16건. 실제 face→PNG 픽셀 미검증 |
| v15 | 189개 모델(Another Furniture 69 + Handcrafted 120)의 **면 선언률·회전·평면·bbox 초과** 신규 통계 및 v13 PNG 24개 표본 중앙값 재집계 | 기존 실측 CSV의 2차 분석이며 원본 게임 파일·인게임 신규 검증은 하지 않음 |
| v16 | Handcrafted 고정 원본 **PNG 추가 12종 실화소·모델 JSON 30개 SHA 직접 검증**, 16 leaf 상속 face 786인스턴스 중 784모드 면의 실제 PNG/UV 정합성 | 바닐라 텍스처 의존 2면·면 내부 픽셀 샘플링·인게임 보류 |
| v17 | Handcrafted 원본 PNG **24종을 고정 커밋에서 재디코딩**, 16 leaf의 **784/784 모드 face UV 사각형 전체 RGBA 텍셀 실측** | 612 비영 UV/172 면적 0; 420 전부 불투명/145 혼합/47 전부 투명. 바닐라 2면·인게임 보류 |
| v18 | Another Furniture 제작자 고정 원본 **leaf 33/템플릿 30 SHA 직접 확인**, 상속 면 807개 재질 해결(804모드·3기본), **새 PNG 12종 실제 픽셀 검사** | Another PNG 참조 경로 53종 중 24종(45.28%) 실화소, 남은 29경로·면 UV 화소/인게임 미검증 |
| v19 | Another Furniture 미측정 **PNG 29종 새 원본 직접 디코딩**, 누적 선택 모델의 **53/53 PNG**, 모드 면 **804/804 UV 내부 실제 RGBA 실측** | 선정 표본에서만 100%. 바닐라 dirt 3면, Macaw 및 인게임 검증 미완료 |

**학습 전체 5개 작업:** 01 바닐라 텍스처(표본 완료/검증 보류), 02 바닐라 3D(진행 중), 03 가구 모드 모델(v11~v12 실측 진행 중), 04 모드 텍스처·UV(PNG 24개 전체 실화소 및 13모델 571면 UV 표본 정렬 측정), 05 바닐라/모드 비교(5쌍 사전 비교, 최종 검증 미착수). 최종 확정 완료는 **0/5**입니다.

## 빠른 탐색

- [1단계 학습 계획](docs/01_1단계_학습계획_v1.md)
- [현재 진행 상황](PROGRESS.md)
- [연구 근거 및 검증 한계](SOURCES_AND_LIMITS.md)
- [GitHub에 저장된 SQLite 기준본 (v8)](data/MC_Furniture_Style_Stage1_Research_v8.sqlite) — v10 전체 바이너리는 아직 미업로드, [SQL migration](data/migrations/v8_to_v10.sql)을 적용하여 복원
- [v4: 누적 150종 텍스처 분석](research/vanilla_textures/v4_150/11_누적150종_확장검증_보고서.md)
- [v7: 연결형 블록 조립](research/vanilla_models/v7/00_v7_연결형_조립분석_보고서.md)
- [v8: 특수 렌더링](research/vanilla_models/v8/00_v8_특수렌더_정적동적_비교보고서.md)
- [v9: 특수 렌더링 실제 3D 부품 구조](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md)
- [v9: 애니메이션 구성](research/vanilla_models/v9/03_v9_애니메이션_검토보고서.md)
- [v10: 누적 DB 통합 검증 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md)
- [v11: Another Furniture 실제 모델/텍스처 1차 실측 보고서](research/furniture_mods/v11/00_v11_AnotherFurniture_모델분석_보고서.md)
- [v11: 모델 템플릿 69개 측정 CSV](research/furniture_mods/v11/template_metrics_69_total.csv)
- [v12: Handcrafted 전수 원형 120종 분석 및 모드 간 사전 비교](research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md)
- [v12 Handcrafted 120종 측정 CSV](research/furniture_mods/v12/handcrafted_authored_120_total.csv)
- [v12 모드 대표 5쌍 구조 비교](research/furniture_mods/v12/another_vs_handcrafted_5_category_pairs.csv)
- [v19: Another 53 PNG 원본·804면 실제 UV 내부 픽셀 RGBA 분석](research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md) · [804면 CSV](research/furniture_mods/v19/another_804_face_actual_rgba.csv) · [Handcrafted/Another 선정 표본 UV/알파 비교](research/furniture_mods/v19/00_v19_모드간실제면UV픽셀_선정표본비교.md)
- [v18: Another 원본 모델 63개·807면 재질 경로·새 PNG 12종 분석](research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md) · [113개 면 재질 그룹](research/furniture_mods/v18/another_face_material_groups_113.csv) · [12개 새 PNG](research/furniture_mods/v18/another_new_png_12_pixel_metrics.csv)
- [v17: 784개 면의 실제 UV 사각형 픽셀·알파 검사](research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md) · [전체 784면 CSV](research/furniture_mods/v17/face_pixel_samples_784.csv) · [오프라인 Pillow 재검산 코드](scripts/reproduce_v17_face_pixels.py)
- [v16: 고정 원본 PNG 12개/JSON 30개/면→PNG 정합성 검증](research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md) · [신규 12 PNG 실화소 CSV](research/furniture_mods/v16/handcrafted_12_new_png_pixel_metrics.csv) · [로컬 원본 재검증 스크립트](scripts/reproduce_v16_handcrafted_originals.py)
- [v15: 모델 189개 표면·회전·평면·bbox 정량 비교](research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md) · [189개 모델별 CSV](research/furniture_mods/v15/model_geometry_derived_189.csv) · [재검산 스크립트](scripts/verify_v15_geometry_research.py)
- [v14: Handcrafted leaf 16개/51개 슬롯 연결 감사](research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md) · [CSV](research/furniture_mods/v14/handcrafted_texture_bindings_51.csv)
- [v13: PNG 24개 직접 디코딩과 UV 13모델/571면 정량 검사](research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md)
- [v13: 모델 PNG·픽셀 재계산 스크립트](scripts/reproduce_mod_png_v13.py)
- [v10 SQL 증분 패치](data/migrations/v8_to_v10.sql)
- [v10 SQLite 재구성 Python 스크립트](scripts/rebuild_v10_db.py)
- [공식 1.21.11 client.jar 대조 도구](scripts/verify_official_jar.py) / [사용법](docs/official_client_jar_검증방법.md) — 실제 JAR 검사 미완료

## 폴더 구조

```text
Minecraft_Furniture_Style_Research/
├── README.md
├── PROGRESS.md
├── SOURCES_AND_LIMITS.md
├── docs/                                  # 학습 계획
├── data/                                  # 최신 누적 SQLite 데이터베이스
├── research/
│   ├── vanilla_textures/v1_30...v4_150/  # 버전별 보고서·측정 CSV·재현 코드·분석 도표
│   ├── vanilla_models/v5...v10/           # 모델·블록상태·UV·특수 렌더링 연구 기록
│   └── furniture_mods/v11...v19/          # Another Furniture·Handcrafted 실측 통계 (원본 에셋 미수록)
└── FILE_MANIFEST_SHA256.csv              # 저장소 파일 해시 목록
```

## 분석 재현

텍스처 분석을 재검산하려면 본인이 적법하게 확보한 Minecraft `client.jar` 또는 추출된 게임 에셋을 **로컬에서만** 사용합니다. 스크립트 및 인수는 각 체크포인트의 `README.md`를 참고하세요.

```bash
pip install -r requirements.txt
```

일부 `build_v*.py` 스크립트는 제작 당시의 `/mnt/data` 경로와 **앞선 체크포인트 파일**을 전제로 작성되었습니다. 따라서 완전 자동 CI 재현 코드가 아니라 당시 분석 과정의 재현 참고 자료입니다. 실행 전 경로를 수정해야 합니다.

## 저작권과 검증 상태

- 이 저장소에는 **Minecraft 원본 PNG, 원본 모델 JSON, client.jar를 포함하지 않습니다.** CSV의 좌표·통계·파일 출처와 분석자가 작성한 설명/도표를 보존합니다.
- 게임 관련 저작권은 각 권리자에게 있으며, 본 저장소는 Mojang/Microsoft의 공식 배포물이 아닙니다.
- 데이터 출처와 버전 고정, 검증하지 못한 부분은 [SOURCES_AND_LIMITS.md](SOURCES_AND_LIMITS.md)에 명시했습니다.
- **저장소 라이선스는 지정하지 않았습니다.** 추후 원본·파생 자료의 라이선스를 검토한 다음 결정하는 편이 안전합니다.


### 최신 DB 재구성 (v10)

```bash
python scripts/rebuild_v10_db.py
```

이 명령은 v8 SQLite를 읽고 SQL 패치를 적용한 새 v10 SQLite를 만듭니다. GitHub는 **v10 전체 바이너리가 아닌 v8 원본 + v10 증분**을 보관합니다.


### v11–v12 모드 소스의 라이선스 및 버전 주의

Another Furniture의 1.21.1 소스 모델을 조사했으며, **기존 바닐라 1.21.11과 버전이 다릅니다**. 제작사 에셋 리소스는 [원본 LICENSE](https://github.com/crispytwig/AnotherFurniture/blob/1.21.1/LICENSE)상 **All Rights Reserved**이므로 JSON·PNG 원본은 재배포하지 않고 분석 통계와 해시/경로만 저장합니다.
