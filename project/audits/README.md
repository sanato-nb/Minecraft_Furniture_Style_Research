# H0 감사 자료 안내

- `H0_REPOSITORY_INVENTORY.json`: `main` 기준 커밋 `c87fa8...` 전체 Git 트리에서 **31,242개 파일의 경로/크기/객체 SHA**를 집계한 불변 기준선. Git 트리 API에 전체 경로 정보가 보존된다.
- `H0_CODE_PATH_SCAN.json`: 초기 일부 스크립트의 수동 분할 스캔. **전체 감사 완료본이 아니며**, 독립 스캔 증거로 사용할 때는 작업 범위 확인 필요.
- `scripts/migration/audit_repository.py`: 체크아웃된 **모든 추적 파일**을 다시 읽고 Git blob SHA·SHA256을 확인하며 모든 실행 스크립트의 정적 경로 참조를 조사한다.
- 새 PR의 GitHub Actions 아티팩트 `h0-h1-foundation-evidence`: `H0_TRACKED_FILES.csv`, `H0_CODE_PATH_SCAN_FULL.json`, `H0_AUDIT_SUMMARY.json`. 자동 검사 결과는 CI가 실제 성공한 뒤에만 확정할 수 있다.
- 이 감사는 정적 파일 목록/문자열 검사다. 모든 Python 스크립트·게임 런타임 기능의 **실행 재현 성공**을 의미하지 않는다.
- SHA가 동일한 다중 경로는 중복 가능성만 표시한다. 삭제 대상이라고 자동 판정하지 않는다.
