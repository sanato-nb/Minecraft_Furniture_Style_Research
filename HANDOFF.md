# 인수인계 · Minecraft Furniture Style Research

> **새 채팅 진입점 / 단일 인수인계 기준 문서**  
> 최종 확인일: **2026-11-12 (KST)** · 현재 체크포인트: **v10**  
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
| 03 | Another Furniture·Macaw's Furniture·Handcrafted 등 가구 모드의 실제 3D 모델 | **미시작** |
| 04 | 위 가구 모드의 텍스처·UV·팔레트 | **미시작** |
| 05 | 바닐라 ↔ 가구 모드 비교·공통 특성 검증 | **미시작** |

**확정 완료 0/5개.** 01의 100%는 **표본 수 목표**만 의미한다. 02는 미리 합의한 전체 분석 대상이 없어 퍼센트를 임의로 계산하면 안 된다.

## 2. 누적 연구 결과: v1–v10

| 체크포인트 | 내용 | 확인할 자료 |
|---|---|---|
| v1–v4 | 바닐라 텍스처 30→83→100→150종, 색상·밝기·투명도·재질 비교 | [v4 보고서](research/vanilla_textures/v4_150/11_누적150종_확장검증_보고서.md) |
| v5 | 바닐라 정적 모델과 상속·요소 크기 조사 | [v5 연구 폴더](research/vanilla_models/v5/) |
| v6 | 면별 UV·부모 템플릿·블록 상태 예제 확대 | [v6 연구 폴더](research/vanilla_models/v6/) |
| v7 | 울타리·담장·철창·유리판·선반 등 연결형 모델 21조합의 조건부 조립 | [v7 보고서](research/vanilla_models/v7/00_v7_연결형_조립분석_보고서.md) |
| v8 | 침대·상자·표지판 등 특수 렌더링 블록과 엔티티 텍스처·아틀라스 구분 | [v8 보고서](research/vanilla_models/v8/00_v8_특수렌더_정적동적_비교보고서.md) |
| v9 | 비공식 1.21.11 엔티티 모델 추출 JSON으로 **17모델/19레이어/55 기하 요소(0두께 15)** 및 애니메이션 **6모델/15클립/304 저장 키프레임** 계측 | [v9 기하 보고서](research/vanilla_models/v9/00_v9_실제부품구조_분석보고서.md), [v9 애니메이션 보고서](research/vanilla_models/v9/03_v9_애니메이션_검토보고서.md) |
| v10 | v8 SQLite에 v9 측정 내용을 증분 SQL로 통합; 검증 상태를 테이블로 분리; 공식 JAR 로컬 검사기 작성 | [v10 보고서](research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md) |

### 실제 SQLite에서 확인된 행 수

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

**주의:** 55 정적 모델, 17 특수 모델, 19 레이어, 55 기하 요소는 서로 다른 집계 단위다. 합쳐서 '총 모델 수'로 쓰면 안 된다.

## 3. 데이터 위치와 버전 복원

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

- **기본 Minecraft 버전:** Java Edition **1.21.11**로 고정. 다른 버전의 텍스처와 모델을 무심코 섞지 말 것.
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
4. 02번의 목표 범위·완료 조건을 명시하고 바닐라 연구의 빈틈을 채운다. 필요하면 공식 검증 보류 상태를 유지한 채 03번 가구 모드의 공개 모델 분석을 **별도 진행 상태**로 착수할 수 있으나, **02 완료**라고 오기하지 않는다.
5. 가구 모드의 실제 `.json`, `.bbmodel`, 텍스처 PNG, 가능하면 `.jar` 내부 리소스를 분석해 정량 비교한다. 스크린샷만 보고 모델의 부품 수를 단정하지 않는다.
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

> `https://github.com/sanato-nb/Minecraft_Furniture_Style_Research`의 `HANDOFF.md`를 먼저 전체 읽고, `PROGRESS.md`·최신 연구 DB/보고서를 확인해 Minecraft 가구 모델링 학습 프로젝트를 **마지막 체크포인트부터 실제로 이어서 진행해 줘**. 기존 작업을 반복하지 말고 검증된 사실과 미검증 사항을 분리하고, 결과를 GitHub에 업로드한 뒤 HANDOFF/PROGRESS까지 갱신해 줘.

## 7. 인수인계 유지 방법

- **정본:** 저장소 루트의 `HANDOFF.md`.
- **진행도:** `PROGRESS.md`.
- **새 채팅 복사용:** `docs/NEW_CHAT_START.md`.
- **기계 판독 상태:** `handoff/STATE.json`.
- 다음 체크포인트에서는 해당 파일을 실제로 업데이트하고 **날짜/버전/새로운 실측값/원본 링크/미완료**를 빠짐없이 남긴다.

