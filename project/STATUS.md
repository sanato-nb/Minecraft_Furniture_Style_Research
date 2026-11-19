# 현재 프로젝트 상태 / 하네스 도입

- 기존 1단계 고정 연구 범위 **5/5 종료 승인**: `docs/PHASE_1_SUMMARY.md`를 현재 역사 연구의 정본으로 사용한다.
- 기존 연구 원본·Git 고정 SHA·기존 `handoff/STATE.json`은 **아직 이동/변경하지 않았다**.
- H0: 원본 Git 트리 인벤토리 기준선 저장. 코드 경로 스캔 및 마이그레이션 검토 진행.
- H1: 공통 정책·Vanilla/Mods 하네스 설정, 공개 inbox 가이드, 최소 설정 검증 CLI의 **비파괴적 토대** 추가.
- 현재 구현은 AI 자동 연구, 전체 파일 이동, 런타임 시각 캡처 자동화를 포함하지 않는다.
- 공식 적용은 검증 완료 후 이 브랜치의 PR을 병합해야 이뤄진다.
- 감사 근거: `project/audits/H0_REPOSITORY_INVENTORY.json`, `project/audits/H0_CODE_PATH_SCAN.json`.
