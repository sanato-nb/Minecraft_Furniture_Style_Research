# RQ-001 6-F 최종 원본 원장 검사

검증 커밋 97f649bc24d0706585e7a95f8dff52767a017068, Actions 46131279132 / Job 140936745863 / artifact 15257597734. 기존 카탈로그 v4를 임시 DB에 재현, 직접 원장 25,387행과 정확히 일치, 재등록 추가 0개, 중복 키 0개. 기존 고정 릴리스의 실제 원본 25,387/25,387 해시 및 기본 형식 PASS.

| 릴리스 | 검사 수 | 원본 확인 방식 |
|---|---:|---|
| vanilla | 4768 | historical_and_main_git_tree_and_body |
| AF | 2994 | pinned_git_commit_and_body |
| HC | 13626 | pinned_git_commit_and_body |
| MACAW | 3999 | pinned_whole_jar_sha256_and_member |

등록 범위 외 원본 전수 분석, PNG 전체 화소/형상·UV·모델 의미 정확성은 미검증. 기존 DB 변경 없음. 외부 원본 미재배포. 전체 원장 F_assets.jsonl은 Actions artifact, 영구 요약 및 SHA256은 F_FINAL_EVIDENCE.json에 보존. 6-D CSV 결함 2건 유지. 6-G 진행.
