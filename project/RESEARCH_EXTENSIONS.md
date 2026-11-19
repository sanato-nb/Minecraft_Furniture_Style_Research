# H5 연구 확장 모듈

저장소에서 `PYTHONPATH=src`로 실행한다. 운영 DB는 `mcfr.research_db --db "$research_db" init`으로 버전 4까지 올린다.

| 기능 | 명령 | 결과 |
|---|---|---|
| 바닐라·모드 업데이트 확인 | `mcfr.extensions check-update` | 공식 배포 목록의 최신 안정 버전과 직전 관측값 |
| 감시 목록 일괄 업데이트 확인 | `mcfr.extensions check-updates` | 대상별 결과, 오류, 변경 감지 건수 |
| 연구 범위·검증률 측정 | `mcfr.extensions coverage` | 선정·검증 통과·실패·미검증 자산 수와 유형별 검증률 |
| 캡처 자동 비교 | `mcfr.extensions visual` | 전체 RGBA 픽셀 차이 수, 범위, 원본 SHA-256 |
| 고정 Mods 배치 자동 촬영 | `mcfr.runtime visual-capture` | 게임 내부 PNG, 서버 상태 검증 로그, 기준 이미지 비교 결과 |
| 모드 간 교차 연구 | `mcfr.extensions compare` | 검증된 두 대상의 관찰 지표별 교차표 |
| AI 사용량·재사용 | `mcfr.extensions usage`, `mcfr.workflow review-send --reuse-identical` | 모델별 사용 토큰과 재사용 건수 |

## 업데이트 추적과 범위

```sh
export PYTHONPATH=src
research_db=/path/to/operational.sqlite
python -m mcfr.research_db --db "$research_db" init
python -m mcfr.extensions --db "$research_db" check-update vanilla
python -m mcfr.extensions --db "$research_db" check-update dtWC90iB --game-version 1.21.11 --loader fabric
python -m mcfr.extensions --db "$research_db" check-updates
python -m mcfr.extensions --db "$research_db" coverage RUN_ID
```

첫 확인은 기준 관측 `BASELINE`으로 기록한다. 이후 같은 대상에서 바뀐 버전·메타데이터를 확인하면 `UPDATE_DETECTED`로 저장한다. 오래된 응답은 `OLDER_FEED`로 표시하고 최근 기준을 보존한다. 모드는 지정한 버전·로더에 해당하는 안정판을 선택한다. 바닐라는 최신 안정판의 버전 메타데이터 SHA-1을 기록하고, 모드는 파일별 SHA-512를 기록한다. 자산 다운로드·등록은 기존 연구 흐름에서 진행한다. [Mojang 배포 목록](https://piston-meta.mojang.com/mc/game/version_manifest_v2.json) · [Modrinth 버전 API](https://docs.modrinth.com/api/operations/getprojectversions/)

일괄 확인의 기본 대상은 [감시 목록](../registry/upstream-targets.json)에 있다. 다른 대상은 `check-updates --targets /path/to/targets.json`으로 지정한다. 한 대상의 응답에 오류가 있어도 나머지를 확인하고, 해당 대상의 이전 관측을 보존한다. 하나라도 오류가 있으면 종료 코드 1을 반환한다. 업데이트 감지는 JSON의 `updates_detected`와 대상별 상태로 확인한다. 주기 실행 시 작업 스케줄러에 이 명령과 운영 DB의 절대 경로를 지정해 같은 관측 이력을 이어간다.

[GitHub Actions 감시 워크플로](../.github/workflows/harness-upstream-watch.yml)는 워크플로 설정이 `main`에 반영될 때 실행하고, 이후 매일 오전 9시 17분(한국 시간)에 실행한다. 감시 전용 DB와 보고서를 30일 동안 아티팩트로 보관한다. 다음 실행은 기본 브랜치에서 생성한 가장 최근의 유효한 감시 DB를 복원한다. 복원할 자료가 없으면 새 기준 관측부터 시작한다. 일부 대상이 실패해도 이번에 성공한 관측은 저장한 뒤 실행을 실패로 표시한다. PR 미리보기는 별도의 임시 DB와 아티팩트를 사용한다.

`coverage`는 현재 연구 회차가 선택한 자산을 분모로 삼고, 같은 범위 해시의 최신 원본 검사 결과를 집계한다. 증분 연구에서는 추가·변경 자산이 분모이며, 동일 자산과 삭제 경로의 수는 `scope_counts`에 표시된다. 같은 범위의 결과가 없으면 선정 자산을 미검증으로 센다.

## 캡처와 교차 연구

고정 Mods 검증 월드의 배치부터 촬영·비교까지 실행하려면 [자동 촬영 명령](audits/runtime/README.md#자동-촬영과-비교)을 사용한다.

```sh
python -m mcfr.extensions visual baseline.png candidate.png --reference-sha256 PINNED_SHA256
python -m mcfr.extensions --db "$research_db" compare LEFT_EXECUTION_ID RIGHT_EXECUTION_ID
```

시각 비교는 Pillow가 필요하다. 같은 카메라·화면 크기·게임 설정에서 얻은 스크린샷을 입력한다. 게임 실행과 캡처 방법은 [런타임 감사](audits/runtime/README.md)를 따른다. 비교는 픽셀마다 색상과 알파를 확인한다. 크기가 다르면 `INCOMPARABLE`을, 같은 크기에서 차이가 있으면 `DIFFERENCE`와 달라진 범위를 반환한다. 종료 코드 0은 픽셀 일치다.

교차 연구는 서로 다른 대상의 통과한 원본 검사 실행 ID를 사용한다. JSON 최상위 키 조합과 PNG 크기 등 같은 관찰 지표의 개수를 절대 수로 집계한다. 좌우 연구 모드·관찰 범위·분모도 함께 출력한다. 결과는 정적 관찰로 분류된다. 형상, 렌더링, 인게임 동작은 해당 실험에서 확인한다.

## AI 응답 재사용과 사용량

H4와 같이 전송 내용을 검토한 뒤 승인 해시를 전달한다. 동일한 요청과 연구 범위·엔진 버전이 이미 완료됐다면 `--reuse-identical`로 이전 응답을 읽고 출처를 기록할 수 있다. 동일 요청이 진행 중이거나 응답 여부가 불확실하면 중복 전송을 차단한다. `FRESH`는 매번 새 검토를 수행한다. 완료 응답이 없고 활성·불확실 호출도 없다면 기존 승인 전송 흐름을 따른다.

```sh
python -m mcfr.workflow --db "$research_db" review-send REVIEW_ID --approve APPROVED_SHA256 --reuse-identical
python -m mcfr.extensions --db "$research_db" usage
```

사용량은 공급자가 응답에 담은 토큰을 집계한다. 재사용 결과는 토큰 합계에 두 번 넣지 않는다. 전송 여부가 불확실한 호출과 사용량 없는 응답은 건수로 기록한다.
