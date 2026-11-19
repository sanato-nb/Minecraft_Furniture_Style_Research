# H3 공통 연구 엔진

H2에서 등록한 연구 회차를 `mcfr.research_engine`으로 계획하고 실행한다. 실행이 끝나면 같은 SQLite DB의 `research_execution`에 구분 가능한 시도 ID, 상태, 실행기 버전, 입력 범위의 SHA-256, 관찰 결과를 저장한다. 재시도 결과는 새 행으로 기록된다. 시작 전에 확인해야 할 계획은 `plan`, 저장된 결과는 `show`로 확인한다.

| 모드 | 원본 검사 범위 |
|---|---|
| `NEW`, `REVALIDATE`, `FRESH` | 대상 릴리스에 등록된 전체 자산 |
| `INCREMENTAL` | 같은 대상의 등록 범위를 경로·종류·리소스 ID·해시·크기로 대조해 신규·변경 자산을 검사한다. 삭제 경로와 동일 자산 수는 실행 기록에 남긴다. |

카탈로그가 비어 있는 대상이나 기준 릴리스에는 먼저 자산을 등록한다. 증분 범위는 두 등록 목록에서 계산된다. 모델·텍스처 의존성의 연쇄 변경 계산은 후속 범위다.

## 실행

저장소 루트에서 Python 3.12로 실행한다. 기존 H2 SQLite에 `init`을 다시 실행하면 버전 2로 이관되며 기존 버전·자산·연구 회차가 보존된다.

```sh
export PYTHONPATH=src
research_db=/path/to/operational.sqlite

python -m mcfr.research_db --db "$research_db" init
python -m mcfr.research_db --db "$research_db" import-legacy
python -m mcfr.research_db --db "$research_db" run-create vanilla-fresh minecraft-java-1.21.11-git --mode FRESH
python -m mcfr.research_engine --db "$research_db" plan vanilla-fresh
python -m mcfr.research_engine --db "$research_db" execute vanilla-fresh --source "$PWD"
python -m mcfr.research_engine --db "$research_db" show vanilla-fresh --details
```

원본 경로는 카탈로그의 `source_path` 기준이다. 디렉터리는 개별 자산 해시와 등록된 크기를 검증한다. ZIP/JAR는 릴리스에 등록한 SHA-1 또는 SHA-256으로 전체 아카이브를 확인한 뒤 내부 자산을 검증한다. 원본 관찰 범위는 JSON 객체 구조와 PNG 헤더의 가로·세로 크기다. 형상 해석, 픽셀 디코딩, 인게임 판정이 필요한 분석은 해당 전용 도구의 범위를 따른다. 원본 검증이 실패하면 실패를 DB에 기록하고 프로세스 종료 코드 1을 반환한다.

## 기존 감사 연결

고정 릴리스에 생성한 `REVALIDATE` 회차는 `execute <run_id> --legacy`를 실행할 수 있다. 바닐라는 1-2-G 원본 감사, 모드는 고정된 3종을 다루는 1-3-F 인계 DB와 1-5-E 교차 비교 DB 감사를 재실행한다. 원래 도구가 사용하는 공개 판정과 결과를 대조하며, 저장소 커밋과 실제 실행한 감사 ID를 결과에 남긴다. 실행 기록의 카탈로그 집계는 해당 회차의 릴리스 범위이고, 감사 집계는 지정된 역사 분석기의 검증 범위다.

실제 실행에서 바닐라 원본 4,768개와 Macaw JAR 자산 3,999개의 검증이 통과했다. 레거시 경로에서는 바닐라 검사 56개 및 출력 3개와 모드 DB 감사 2건을 재현했다.
