# v62 모델별 증거 등급 및 역사 원본 교차검사 규칙

기준: Minecraft Java 1.21.11, 자산 식별키 `(asset_type, full_source_path, git_blob_sha)`; `source_model` basename 단독 조인 금지.

## 원본 실증과 계승 기록 분리

- `identity_linked`: 기존 v61 P1 544개 원본 모델 경로와 SHA가 원장에 연결됨. 544/544 **모델의 기하/UV/PNG/블록상태가 완료되었다는 의미 아님**.
- `explicit_direct_JSON_review_flags_any(v35…v61)`: v61 원장의 명시 `v35_direct_sha_checked`, `v45_direct_leaf_read`, `v53_new_direct_source_JSON_read`, `v61_source_JSON_SHA_rechecked` 등의 라운드별 직접 판독 플래그가 있는 514개. 18개 명시 플래그만 계산하며 `v54_P1_model_source_path_SHA_linked`처럼 *전체 경로 식별* 플래그는 직접 읽기로 승격하지 않음.
- `selected_history_source_SHA_witness`: v44의 176개 링크로 제한한 원본 역사 CSV **21개 파일**을 이 회차에 원격 재조회하고 각 소스 파일 Git SHA 및 행 내 **모델 원본 SHA와 이름/경로**를 대조. **78개 링크**는 동일 행에 모델 경로와 SHA가 직접 존재, **98개 링크**는 이름과 SHA가 직접 존재하지만 완전한 경로 필드는 없다. 독립 모델 JSON을 이번 회차에서 176개 다시 열었다는 주장이 아니다.
- `selected_CSV_v44_file_sha_erratum`: v44 `02_SOURCE_EVIDENCE_LINKS_176.csv` 중 6개 모델 템플릿 링크가 같은 v27 원본 CSV의 SHA를 `8f5a14694934da3306e2aa3c3ba10e9a22862ed`로 적어 **끝의 `3`이 누락**. GitHub의 해당 CSV 실제 blob SHA는 `8f5a14694934da3306e2aa3c3ba10e9a22862ed3`. v44 파일 자체 수정/과거 증거 폐기 없이 `03_`에 기록. **모델 SHA 6개는 자체 원장과 일치**.
- `evidence_tier_selected_scope`: (1) 위 라운드 명시 모델 JSON read 기록 514; (2) 라운드 직접읽기 표시가 없으나 선택한 역사 21 CSV에서 원본 모델 SHA 행이 존재하는 28; (3) 두 증거 없음 2(`chipped_anvil.json`, `damaged_anvil.json`). 세 그룹은 **선택한 검증 범위에서의 증거 등급**이며, 2개를 과거 미연구 모델로 확정하지 않는다.
- 544개 모든 모델에 `all_v5_to_v43_historical_files_exhaustively_audited=false`, `whole_geometry_UV_PNG_state_renderer_completed=false`, `stage_1_2_A_completed=false`. 전체 역사 종합/모델 의미론/게임 런타임 인증을 증거 없이 성공 처리하지 않음.

## 산출물

- `00A_`, `00B_`: 21 원본 CSV의 원격 Git SHA+행 대조 경로·구조화 증거, 94+82개 역사 링크
- `01_HISTORICAL_EVIDENCE_CROSSWALK_176.csv`: 176개 원본 링크, 현재 P1 model path/SHA, 역사 CSV의 v44 기록값 vs 실제 소스 파일 Git SHA, 직접 행 증거 수준
- `02_HISTORICAL_RECHECK_SCOPE_AND_COUNTERS.json`: 21/176/110, SHA 불일치6 요약
- `03_V44_EVIDENCE_CSV_SHA_ERRATA_6.csv`: v44의 역사 증거 파일 SHA 기록 오류로 영향을 받는 6개 모델
- `04_SOURCE_REVIEW_LEDGER_544.csv`: 544개 모델 각각 24개 증거 상태, 선별된 역사 CSV 증거와 직접 원본 읽기 플래그 구분
- `07_P1_544_EVIDENCE_LEDGER.csv`: v61 544×297을 544×310으로 확장, **기존 161,568 셀 동일**
- `08_OPEN_ISSUES.md`: 미완료·오류·후속 검증
- `REPRODUCE_V62_HISTORY_AUDIT.py`: repo 전체 체크아웃용 정합성 재현 코드. GitHub에 코드를 저장했으나 **전체 체크아웃에서 실행했다는 인증은 아직 없음**.

## 완료기준

A는 **모집단/과거 연구 통합**이므로 P1 544개 모델의 증거별 일치·누락·예외를 모두 명시해야 한다. **21개의 선택 CSV 재검증으로 v5~v43 전체 역사 연구 파일 전수 검수 완료를 주장하지 않는다.** 1-2-A는 계속 진행중. 공식 JAR/실게임 렌더는 현재 사용자 범위에서 필수 완료조건 제외되어도 성공 검증했다고 기록하지 않는다.
