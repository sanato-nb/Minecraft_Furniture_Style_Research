# H2 공통 연구 DB

하네스는 SQLite 운영 DB 한 개에서 바닐라와 가구 모드의 고정 버전, 자산, 연구 회차를 관리한다. 운영 DB는 명령으로 생성한다. 기존 연구 원장과 DB는 공개본에서 읽고, 각 자산에 근거 원장의 경로를 기록한다.

| 테이블 | 식별자와 역할 |
|---|---|
| `release` | `release_key`로 대상, 게임·모드 버전, 로더, 고정 출처와 해시 방식·값을 식별한다. 같은 버전 이름에 서로 다른 소스 해시가 있으면 별도 릴리스로 기록할 수 있다. |
| `asset` | 릴리스 내부 원본 경로를 키로 사용한다. 리소스 ID, 자산 종류, 해시, 확인된 크기, 근거 경로를 저장한다. |
| `research_run` | `run_id`로 계획된 연구 회차를 식별한다. 대상 릴리스와 모드, 기준 릴리스, UTC 생성 시각을 기록한다. |

`INCREMENTAL`은 같은 대상의 서로 다른 기준 릴리스를 지정한다. `NEW`, `REVALIDATE`, `FRESH`는 대상 릴리스만 지정한다. 같은 값으로 등록을 재시도하면 기존 기록을 돌려주거나 추가 건수가 0이다. 같은 키의 메타데이터가 충돌하면 해당 등록 전체를 되돌린다. 실제 작업 실행과 재개는 이후 엔진에서 연결한다.

## 명령

저장소 루트에서 Python 3.12와 SQLite 표준 모듈을 사용한다.

```sh
export PYTHONPATH=src
research_dir=$(mktemp -d)
research_db="$research_dir/research.sqlite"

python -m mcfr.research_db --db "$research_db" init
python -m mcfr.research_db --db "$research_db" import-legacy
python -m mcfr.research_db --db "$research_db" summary
python -m mcfr.research_db --db "$research_db" assets minecraft-java-1.21.11-git --limit 5
python -m mcfr.research_db --db "$research_db" run-create vanilla-fresh-01 minecraft-java-1.21.11-git --mode FRESH
python -m mcfr.research_db legacy-info mod-handoff
```

새 릴리스와 자산은 JSON으로 준비해 `python -m mcfr.research_db --db "$research_db" register manifest.json`으로 등록한다. 최상위 `release`는 [고정 버전 등록 예시](../registry/legacy-releases.json)의 단일 객체와 같은 형식이며, `assets`는 배열이다. 각 자산에는 `source_path`, `kind`, `resource_id`, `hash_algorithm`, `digest`를 지정하고, 확인한 경우 `byte_count`, `evidence_path`를 추가한다. 자산 경로는 릴리스 안의 상대 경로, 근거 경로는 저장소의 상대 경로다. 종류는 `model`, `blockstate`, `texture`, `texture_sidecar`, `item_definition`을 지원한다.

## 연결한 역사 자료 범위

| 고정 대상 | 등록 자산 |
|---|---:|
| Minecraft Java 1.21.11 | 4,768 |
| Another Furniture 4.0.3 | 2,994 |
| Handcrafted 4.0.3 | 13,626 |
| Macaw’s Furniture 3.4.2 Fabric | 3,999 |
| **합계** | **25,387** |

1-2-G 바닐라 원본·sidecar 원장, 1-3-B 세 모드의 JSON 원장, 1-3-F의 고정 모드 PNG 행 2,173개를 사용한다. Another Furniture와 Handcrafted는 공통 소스 트리의 Git 커밋으로 구분한다. 모드가 참조하는 바닐라 PNG 행 75개와 누락 참조 8개는 1-3-F 원장에서 확인할 수 있다. 등록된 자산 수는 기존 연구 범위이며 릴리스 전체의 자산 수는 각 원본 배포 범위에서 결정된다.

`legacy-info`는 `stage1-v8`, `mod-handoff`, `comparison`의 SQLite 버전·테이블 목록·무결성 검사 결과를 반환한다. 일반 파일은 SQLite 읽기 전용 모드로 열고, XZ 파일은 임시 메모리에서 해제해 읽기 전용으로 조회한다.
