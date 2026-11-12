# MC 바닐라 모델링 학습 v5

- 기존 150종 텍스처 통계 CSV 유지; 새로 실제 모델 JSON 55개/블록 상태 JSON 16개 분석.
- 원본 Minecraft 3D 모델 JSON/PNG는 포함되지 않음. 파생 통계, 출처, 기록만 수록.
- 핵심 보고서: `00_v5_3D_구조분석_보고서.md`
- SQL DB: `MC_Furniture_Style_Stage1_Research_v5.sqlite` (integrity_check = ok)
- 검증된 파일 레코드: 71개, 요소 치수 레코드: 80개.
- `build_v5.py`는 추출한 요약 데이터를 재집계하기 위한 코드. 원본 JSON을 재수집하지 않으며 라이브 Github API 접근 기능은 없음.
