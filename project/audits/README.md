# H0 감사 자료 안내

- `H0_REPOSITORY_INVENTORY.json`: `main` 기준 커밋 `c87fa8...` 전체 Git 트리에서 **31,242개 파일의 경로/크기/객체 SHA**를 집계한 불변 기준선. Git 트리 API에 전체 경로 정보가 보존된다.
- `H0_CODE_PATH_SCAN.json`: 초기 일부 스크립트의 수동 분할 스캔. **전체 감사 완료본이 아니며**, 독립 스캔 증거로 사용할 때는 작업 범위 확인 필요.
- `scripts/migration/audit_repository.py`: 모든 추적 파일의 내용을 읽어 Git blob SHA-1을 대조하고 SHA-256 원장을 생성한다. `--baseline`으로 기준 커밋의 경로·Git 모드·blob과 비교하며 누락이나 변경 시 실패한다. 실행 코드 정적 스캔에는 Java, SQL, Minecraft 함수도 포함한다.
- GitHub Actions 아티팩트 `h0-h1-foundation-evidence`에는 파일별 원장 `H0_TRACKED_FILES.csv`, 경로 후보 `H0_CODE_PATH_SCAN_FULL.json`, 기준선 비교 `H0_AUDIT_SUMMARY.json`, 경로 재현 `H0_HISTORICAL_REPLAY.json`이 들어간다.
- [경로 재현 계약](H1_PATH_REPLAY.md)에는 바닐라 1-2-G와 모드 1-3-F·1-5-E의 검증 방식, 입력 경로, 출력 위치가 있다.
- 경로 후보는 문자열 정적 검사에 따른 결과다. 전체 동적 의존성과 게임 런타임 재현은 별도 범위다.
- SHA가 동일한 다중 경로는 중복 가능성만 표시한다. 삭제 대상이라고 자동 판정하지 않는다.

저장소 루트에서 다시 실행한다.

```sh
python scripts/migration/audit_repository.py \
  --baseline c87fa83846be513f797292bc9f31d2e01b4f3187 \
  --out /tmp/mcfr-h0
python scripts/migration/replay_evidence.py
```
