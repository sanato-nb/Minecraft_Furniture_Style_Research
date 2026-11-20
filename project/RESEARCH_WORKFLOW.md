# H4 연구 작업 재개와 AI 검토

## 원본 검사 체크포인트

`mcfr.workflow scan`은 H3의 원본 검사를 재사용한다. 완료한 묶음과 다음 자산 위치를 SQLite에 같은 트랜잭션으로 저장한다. 묶음은 최대 64개다. 중단 후 같은 작업 ID, 연구 회차, 원본 경로로 실행하면 마지막 완료 묶음부터 이어진다. 실행 중 카탈로그 범위, 원본 경로·종류, 엔진 버전이 달라지면 새 작업 ID가 필요하다.

```sh
export PYTHONPATH=src
research_db=/path/to/operational.sqlite
python -m mcfr.research_db --db "$research_db" init
python -m mcfr.research_db --db "$research_db" import-legacy
python -m mcfr.research_db --db "$research_db" run-create vanilla-fresh minecraft-java-1.21.11-git --mode FRESH

python -m mcfr.workflow --db "$research_db" scan vanilla-fresh job-1 --source "$PWD" --max-assets 128
python -m mcfr.workflow --db "$research_db" scan-status job-1
python -m mcfr.workflow --db "$research_db" scan vanilla-fresh job-1 --source "$PWD"
```

`--max-assets`를 지정하면 그 호출에서 처리할 자산 수를 제한한다. 원본 검사 완료 시 H3와 같은 결과 원장에 실행 한 건을 남긴다. 같은 완료 작업을 다시 실행하면 저장된 실행 ID를 반환한다. 이 기능은 원본 디렉터리와 PIN이 지정된 ZIP/JAR 검사에 적용한다. 기존 감사 재실행은 H3의 실행 방법을 사용한다.

로컬 작업 스케줄러나 수동 실행에서 아래 명령을 호출하면 DB에서 미완료 검사를 찾아 저장된 원본 경로와 체크포인트로 재개한다. 실행 환경에서 DB와 저장된 원본 경로에 접근할 수 있어야 한다.

```sh
python -m mcfr.workflow --db "$research_db" scan-resume
```

원본이 사라졌거나 검사 범위가 달라진 작업은 오류를 반환하고 체크포인트를 유지한다. 나머지 대기 작업은 계속 처리한다. 개별 작업에 오류나 검증 실패가 있으면 종료 코드 1을 반환한다. 완료한 검사는 다음 실행부터 목록에서 빠진다.

## AI 검토 한 건 준비 및 전송

검토 준비에는 원본 검증이 통과한 실행 ID를 쓴다. 요청은 검증 집계와 사용자가 `--asset`으로 골라 지정한 관찰만 포함한다. 이 옵션은 최대 12개까지 반복할 수 있다. 준비 단계에서 전송될 JSON 전체와 승인용 SHA-256이 출력된다.

```sh
python -m mcfr.workflow --db "$research_db" review-prepare review-1 EXECUTION_ID \
  --model MODEL_NAME --max-output-tokens 256 \
  --asset 1.21.11/assets/minecraft/models/block/acacia_shelf_unconnected.json
python -m mcfr.workflow --db "$research_db" review-status review-1
```

요청 내용을 확인한 뒤 `OPENAI_API_KEY`를 환경에서 제공하고 아래 명령으로 승인한 해시를 제출한다. 요청은 [OpenAI Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create)로 전송된다. API 호출에 비용이 발생할 수 있다.

```sh
python -m mcfr.workflow --db "$research_db" review-send review-1 --approve APPROVED_SHA256
```

현재 ai_api_enabled=false 정책 때문에 일반 review-send는 유료 전송을 차단한다. 의도한 단 한 건의 호출만 승인하려면 위 명령에 --enable-api를 덧붙인다. OPENAI_API_KEY와 정확한 승인 해시는 여전히 필수이며, GitHub Actions가 자동 호출하는 기능은 아니다. [정책 검증 안내](HARNESS_AUDIT_234.md#4-설정-정책의-실제-실행-적용)

요청은 8,192바이트 이하이며 출력 토큰 한도는 16~2,048이다. 응답에서 제공한 사용 토큰 수를 기록한다. `COMPLETE`는 응답을 받았다는 뜻이고, 모델의 처리 상태는 `provider_status`로 확인한다. API 응답을 확인하지 못하면 `UNCONFIRMED`가 기록된다. 호출 중 프로세스가 종료되면 `DISPATCHING`으로 남을 수 있다. 두 경우 모두 같은 검토 ID의 자동 재전송을 차단한다. 답변은 `AI_INFERENCE`로 별도 저장하며 원본 검증 판정은 검증 실행 원장에서 확인한다.
