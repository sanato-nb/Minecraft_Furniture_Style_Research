# Minecraft Furniture Style Research

Project Zomboid의 가구를 Minecraft로 옮기는 작업에 필요한 모델링 근거를 모으는 연구 저장소입니다. Minecraft Java 바닐라와 가구 모드의 모델, 블록 상태, 텍스처와 UV를 조사하고, 하네스로 원본 검증과 인게임 재현을 반복합니다.

## 현재 상태

- **1단계 연구**는 정해진 범위 5개를 모두 종료 승인했습니다. 조사 결과와 항목별 한계는 [1단계 최종 정리](docs/PHASE_1_SUMMARY.md)에 있습니다.
- **연구 하네스**는 SQLite 카탈로그, 원본 검증, 중단 후 재개, 증분 비교, 인게임 자동 촬영을 지원합니다. [하네스 현황](project/STATUS.md) · [구현·검증 PR #12](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/12)
- **배포 감시**는 Minecraft Java 바닐라, Adorn, Macaw’s Furniture를 매일 오전 9시 17분(한국 시간)에 확인하도록 설정되어 있습니다. [첫 운영 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44566117861) · [전체 실행 기록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/workflows/harness-upstream-watch.yml)

가구 제작과 PZ 맵 변환은 후속 작업입니다. 현재 운영 기능은 OpenAI API 키 없이 실행하며, API 연동 검증은 보류 중입니다.

## 폴더 구조

최상위 폴더와 주요 하위 경로를 표시했습니다.

```text
📁 Minecraft_Furniture_Style_Research/
├── 📄 AGENTS.md
├── 📁 harness/                     연구 프로필과 실행 정책
│   ├── 📁 shared/
│   │   └── 📄 config.json
│   ├── 📁 vanilla/
│   └── 📁 mods/
├── 📁 src/
│   └── 📁 mcfr/                    하네스 실행 코드
│       ├── 📄 research_db.py       SQLite 카탈로그
│       ├── 📄 research_engine.py   원본 검증과 증분 범위 계산
│       ├── 📄 source_jobs.py       체크포인트 저장과 재개
│       ├── 📄 update_watch.py      배포 변경 감시
│       ├── 📄 runtime_capture.py   인게임 자동 촬영
│       └── 📄 visual_check.py      이미지 비교
├── 📁 registry/
│   ├── 📄 legacy-releases.json      연구 기준 배포 버전
│   └── 📄 upstream-targets.json     업데이트 감시 대상
├── 📁 research/                    연구 기록과 증거
│   ├── 📁 vanilla_textures/
│   ├── 📁 vanilla_models/
│   ├── 📁 furniture_mods/
│   ├── 📁 campaigns/
│   ├── 📁 comparisons/
│   └── 📁 historical/
├── 📁 project/                     하네스 사용법과 현황
│   ├── 📄 STATUS.md
│   ├── 📁 audits/
│   └── 📁 decisions/
├── 📁 docs/                        단계별 계획과 연구 정리
├── 📁 data/                        기존 SQLite DB와 이관 스크립트
├── 📁 1.21.11/                     Minecraft Java 1.21.11 원본 자료
├── 📁 handoff/                     이전 회차의 인수인계
├── 📁 inbox/                       새 연구 자료 제출
├── 📁 scripts/                     감사·재현 스크립트
├── 📁 tests/
│   └── 📁 harness/
└── 📁 .github/
    └── 📁 workflows/
        ├── 📄 harness-foundation-ci.yml
        └── 📄 harness-upstream-watch.yml
```

## 빠른 시작

저장소 루트에서 Python 3.12로 실행합니다. 아래 예제는 임시 SQLite DB에 기존 카탈로그를 불러오고, Minecraft Java 1.21.11의 바닐라 자산을 검증합니다.

```sh
export PYTHONPATH=src
research_dir=$(mktemp -d)
research_db="$research_dir/research.sqlite"

python -m mcfr.foundation validate
python -m mcfr.research_db --db "$research_db" init
python -m mcfr.research_db --db "$research_db" import-legacy
python -m mcfr.research_db --db "$research_db" run-create vanilla-verify minecraft-java-1.21.11-git --mode REVALIDATE
python -m mcfr.workflow --db "$research_db" scan vanilla-verify vanilla-job --source "$PWD"
```

이전에 중단한 검사를 재개하려면 같은 DB로 `python -m mcfr.workflow --db "$research_db" scan-resume`을 실행합니다. 기존 카탈로그 가져오기는 고정 배포 버전 4개와 자산 25,387개를 등록합니다. Adorn 두 버전의 실전 검증은 [별도 재현 절차](project/audits/h67/README.md)를 참고하세요.

| 연구 회차 | 용도 |
|---|---|
| `NEW` | 새로 등록한 대상의 원본 검사 |
| `REVALIDATE` | 등록된 버전의 원본과 기존 검증 결과 재확인 |
| `INCREMENTAL` | 같은 대상의 두 버전을 비교해 추가·변경 자산을 검사하고 삭제 경로를 기록 |
| `FRESH` | 등록된 범위를 처음부터 다시 검사 |

## 필요한 문서 찾기

| 찾는 내용 | 문서 |
|---|---|
| 공통 정책, 바닐라·가구 모드 연구 방법 | [공통 하네스](harness/shared/README.md) · [Vanilla](harness/vanilla/instructions.md) · [Mods](harness/mods/instructions.md) |
| DB 등록, 연구 회차, 실행과 재개 | [연구 DB](project/RESEARCH_DB.md) · [연구 엔진](project/RESEARCH_ENGINE.md) · [작업 재개](project/RESEARCH_WORKFLOW.md) |
| 배포 감시, 검증 범위, 비교 | [확장 모듈](project/RESEARCH_EXTENSIONS.md) |
| 실제 게임 촬영과 상태 로그 | [인게임 재현](project/audits/runtime/README.md) · [Adorn·BWG 호환 검증](project/audits/adorn_bwg/README.md) |
| 새 자료 제출 | [inbox 안내](inbox/README.md) |
| 과거 근거와 인수인계 | [기존 연구 기록 색인](project/HISTORY.md) · [이전 README 원문](README_2026-11-19.md) |

연구 결과에는 원본 확인, 정적 계산, 인게임 관찰, AI 추론을 구분해 기록합니다. 기존 증거는 해당 보고서에 기록된 경로와 Git 커밋으로 재현할 수 있습니다.
