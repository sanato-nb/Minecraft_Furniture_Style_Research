# 7-G 6차 보완 — 재개/검색/이관/복원

T04: terminal attempt와 checkpoint 이력의 UPDATE/DELETE/REPLACE 방지, 순서·입력·결과 해시 검증, 새 시도에서 배치 재개 및 rollback. T13: 고정 scope 원본 연결, 실제 SHA256/SHA1/Git blob SHA1, 명시 release allowlist, 권리 미확정/제한 근거 차단 및 locator redaction. 실제 인증/권한 시스템은 아님. T14: 합성 CSV 원본 Git blob/파생본 해시/컬럼수/변환 버전/승인자/대상 경로 연결 검증, 원본 불변. 역사 CSV 실물 수정/이관 없음. T16: 임시 복제 및 근거 manifest 비교, 누락/변조/가상 만료 음성 사례. 실제 외부 보존 및 Job 간 복원 아님. 고정 16 시험/19 입력 유지. 전체 엔진 구현을 요구하는 항목은 7-H에서 별도 분류하고 미입증은 PARTIAL로 유지한다.
