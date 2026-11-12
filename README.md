# Minecraft Furniture Style Research

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

**학습 전체 5개 작업:** 01 바닐라 텍스처(표본 완료/검증 보류), 02 바닐라 3D(진행 중), 03 가구 모드 모델(미시작), 04 모드 텍스처·UV(미시작), 05 바닐라/모드 비교(미시작). 최종 확정 완료는 **0/5**입니다.

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
- [v10 SQL 증분 패치](data/migrations/v8_to_v10.sql)
- [v10 SQLite 재구성 Python 스크립트](scripts/rebuild_v10_db.py)

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
│   └── vanilla_models/v5...v10/           # 모델·블록상태·UV·특수 렌더링 연구 기록
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
