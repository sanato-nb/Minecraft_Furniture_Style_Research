# A-01 Another Furniture 기존 204 모델 직접 원장 교차감사

원본 선행 18개 CSV 파싱 결과: **v18 33, v21 38, v22 43, v23 51, v24 39 = 204행**. 고유 모델 204, 고유 원본 경로 204, 경로 중복 0, 다른 경로의 같은 Git blob SHA 그룹 0.

고정 원저자 `crispytwig/AnotherFurniture@57eb624cbb7f408d43398c7434b0d38d312cb55d` Git tree에서 **204/204 경로·SHA**, **204/204 model ID/경로**, **204/204 source pin** 일치를 검사했습니다. Tree만 확인하고 원저자 JSON 원문 bytes는 아직 직접 재해시하지 않았습니다. `A_direct_bytes_read=false`를 유지하며, 이를 기존 연구 204 신규발견으로 세지 않습니다.

선행 경로·SHA 범위 검사: **PASS**, A1 종료 게이트는 실제 원본 body 검증/다른 원장 관계/종료 감사까지 **PARTIAL**.


## 2026-11-18 원본 직접 재해시 보완

원저자 고정 커밋 모델 JSON 204/204를 다시 열고 Git blob SHA-1을 별도 구현으로 계산하여 SHA·parent·경로 일치 204/204, 고유 모델 204, 중복·누락 0을 확인. `A_A01_INDEPENDENT_RECHECK_01~12.json`에 파일별 원본 경로·SHA·부모를 저장하고, `A_A01_INDEPENDENT_204_AUDIT.json`에서 코호트별 별도 재집계 완료. **A1 출처/본문 게이트 PASS**. 기존 204개는 새로운 발견이 아니며 원장 단위 보존.
