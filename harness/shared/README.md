# Shared research harness

[현재 하네스 개발 현황](../../project/STATUS.md) · [기존 연구 기록 색인](../../project/HISTORY.md)

공통 하네스는 별도 AI 에이전트가 아니라 Vanilla/Mods 양쪽이 재사용하는 **정책·입출력 규격**이다.
- Python 분석기는 `src/mcfr/`에 둔다. 하네스 폴더에는 작업 선택·권한·연구 프로필을 둔다.
- 기본: 승인된 범위에서 실행, 결과는 브랜치와 PR로 제출. `main` 쓰기 금지.
- 단계적 혼합형은 고정된 원본의 해시·규칙·스키마를 먼저 프로그램으로 검사하고, 해석이 필요한 증거만 AI에 넘긴다. 검증된 산출물을 브랜치에 기록하고 PR로 검토한다.
- 입력 해시 및 분석기 버전이 같을 때만 검증 완료 결과를 재사용한다.

```sh
PYTHONPATH=src python -m mcfr.foundation validate
PYTHONPATH=src python -m mcfr.foundation plan --profile vanilla --mode FRESH --target-id minecraft --release 1.21.11
PYTHONPATH=src python -m mcfr.foundation runtime-plan --minecraft-version 1.21.11
```

고정 Mods 런타임은 `mcfr.runtime engine`으로 재실행하고 `mcfr.runtime visual-client`로 로컬 테스트 월드를 열 수 있다. [런타임 검증 결과와 촬영 절차](../../project/audits/runtime/README.md)에 지원 버전과 명령을 기록했다.

H2 연구 카탈로그에서 버전·자산·연구 회차를 등록하고 조회한다. [공통 연구 DB 사용법](../../project/RESEARCH_DB.md)

기존 연구를 이어받을 때는 `PYTHONPATH=src python -m mcfr.foundation replay-history --db /path/to/research.sqlite`를 실행한다. 운영 DB와 근거 경로를 확인하고 바닐라·모드 감사 3건을 재현한다. [검증 범위와 결과 확인 방법](../../project/audits/H1_PATH_REPLAY.md)

등록한 회차는 H3에서 원본을 검증하거나 기존 감사를 재실행한다. [공통 연구 엔진 사용법](../../project/RESEARCH_ENGINE.md)

[H4 연구 워크플로](../../project/RESEARCH_WORKFLOW.md)에서 중단된 원본 검사를 이어서 실행하고 승인한 AI 검토 요청을 전송한다.

[H5 연구 확장 모듈](../../project/RESEARCH_EXTENSIONS.md)에서 업데이트 확인, 연구 범위 측정, 캡처 자동 비교, 교차 연구와 AI 사용량 집계를 실행한다.

[Adorn 실전 검증](../../project/audits/h67/README.md)에서 신규 등록, 재개, 증분 연구, FRESH 재검사를 재현할 수 있다.

[검수 개선 2·3·4](../../project/HARNESS_AUDIT_234.md)에서는 기존 1-3-C 재사용 기반 회전·거리·부모 모델·UV 정적 분석, SQLite 상태 인계, 신규 등록 근거 및 수동 API 동의 정책의 실행법을 다룬다.
