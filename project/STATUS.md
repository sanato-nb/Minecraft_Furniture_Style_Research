# 현재 프로젝트 상태 / 하네스 도입

- 기존 1단계 고정 연구 범위 **5/5 종료 승인**: `docs/PHASE_1_SUMMARY.md`가 역사 연구의 기준이다.
- 기존 연구 원본·Git 고정 SHA·기존 `handoff/STATE.json`은 **이동/수정하지 않았다**.
- H0: 전체 Git 트리 32,148항목(파일 31,242개) 기록; PR CI의 **31,267개 파일 무결성 검사 PASS**, 실행 코드 186개 정적 스캔.
- H1: 공통 정책·Vanilla/Mods 프로필, 공개 inbox 가이드, 읽기 전용 설정 검증 CLI, 기존 재구성 분류 보고서를 추가한 **초기 토대 구축**.
- GitHub Actions: `44506172295` (7개 테스트 PASS; 전체 파일 SHA PASS). 검증 근거 `project/audits/H0_VERIFICATION.json`.
- 새 코드에는 AI 자동 연구, 업데이트 자동 추적, 원본 물리적 이동, 런타임 시각 캡처 자동화가 **아직 없다**.
- 기존 `main` 푸시 워크플로의 위험은 `project/audits/H0_MIGRATION_CLASSIFICATION.md` 참고; 이 PR에서 수정·실행하지 않았다.
- 이 작업은 PR #12에서 검토 중이며 `main` 병합은 사용자가 결정한다.
