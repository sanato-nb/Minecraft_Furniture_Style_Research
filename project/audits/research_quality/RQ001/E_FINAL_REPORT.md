# RQ-001 6-E 종료 — 역사 SQLite 읽기 전용 조사

검증 커밋 5a1739b695736b5b9b8df2a5d532c1f8c21d4250. Actions 46129939313, job 140932670111, artifact 15256619098. PASS 9/9, 원본 전후 SHA256 일치 9/9, integrity_check ok 및 선언 FK 검사 통과 9/9, 자체 테스트 4/4. 고유 blob 8개.

| 경로 | 테이블 | 행 합계(중복 포함) | 판정 |
|---|---:|---:|---|
| data/MC_Furniture_Style_Stage1_Research_v8.sqlite | 20 | 924 | PASS |
| research/furniture_mods/phase_1-3/F/furniture_research.sqlite.xz | 16 | 337713 | PASS |
| research/furniture_mods/phase_1-4/E_followup/research_texture_uv_runtime.sqlite.xz | 16 | 11188 | PASS |
| research/furniture_mods/phase_1-4/entry04/research_texture_uv.sqlite.xz | 9 | 10498 | PASS |
| research/furniture_mods/phase_1-5/E/comparison.sqlite.xz | 22 | 3829 | PASS |
| research/vanilla_models/v5/MC_Furniture_Style_Stage1_Research_v5.sqlite | 5 | 372 | PASS |
| research/vanilla_models/v6/MC_Furniture_Style_Stage1_Research_v6.sqlite | 10 | 545 | PASS |
| research/vanilla_models/v7/MC_Furniture_Style_Stage1_Research_v7.sqlite | 16 | 875 | PASS |
| research/vanilla_models/v8/MC_Furniture_Style_Stage1_Research_v8.sqlite | 20 | 924 | PASS |
| 합계 | 134 | 366868 | PASS |

행 합계는 역사 버전 및 동일 v8 복제본을 포함하며 고유 지식 수가 아니다. 모든 테이블의 의미적 참조나 연구 주장 자체의 정확성은 증명하지 않는다. 전체 DDL/컬럼/인덱스/외래키/행수는 E_databases.json Actions 아티팩트, 영구 로그 요약과 결과 SHA256은 E_FINAL_EVIDENCE.json에 보존. 기존 DB 변경·통합 없음. D의 CSV 결함 2건은 그대로 유지. 다음 6-F.
