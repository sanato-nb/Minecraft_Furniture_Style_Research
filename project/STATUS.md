# 현재 프로젝트 상태 / 하네스 도입

- 기존 1단계 고정 연구 범위 **5/5 종료 승인**: `docs/PHASE_1_SUMMARY.md`가 역사 연구의 기준이다.
- 기존 연구 원본·Git 고정 SHA·기존 `handoff/STATE.json`은 **이동/수정하지 않았다**.
- H0: 전체 Git 트리 32,148항목(파일 31,242개) 기록. 기준 커밋의 경로·모드·blob 보존을 새 CI 게이트에서 검사하고 1-3-F 인계 DB와 1-5-E 비교 DB의 기존 감사를 재실행한다.
- H1: 공통 정책, Vanilla/Mods 프로필, 공개 inbox 가이드, 읽기 전용 설정 검증·계획 출력, 1-3-D 고정 Mods 엔진 검사 진입점까지 도입했다.
- 최초 CI 기록은 `project/audits/H0_VERIFICATION.json`에 있다. 보강된 감사의 검증 방법 및 산출물은 [감사 자료 안내](audits/README.md)에 있다.
- Mods 런타임 재실행과 대표 배치 캡처는 [런타임 감사](audits/runtime/README.md)에 기록했다. 자동 AI 연구, 업데이트 추적, 원본 경로 이관은 후속 단계다.
- 기존 `main` 푸시 워크플로의 위험은 `project/audits/H0_MIGRATION_CLASSIFICATION.md` 참고; 이 PR에서 수정·실행하지 않았다.
- 이 작업은 PR #12에서 검토 중이며 `main` 병합은 사용자가 결정한다.
