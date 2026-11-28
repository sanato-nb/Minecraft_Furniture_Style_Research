# RQ-001 6-H/6-I 분류 재검증 기록

첫 실행 #46136672454는 아티팩트 해시·경로·근거 재검사를 통과했지만, 분류 결과는 REVALIDATE 3,138 / HISTORICAL 4 / REUSABLE_LIMITED 11 / DUPLICATE_CANDIDATE 14였다. 고정 원장 3,167경로에 작성된 정책을 별도로 적용한 계산은 REVALIDATE 2,268 / HISTORICAL 874 / REUSABLE_LIMITED 11 / DUPLICATE_CANDIDATE 14였다. 따라서 최초 실행의 분류 집계는 채택하지 않는다. 원인은 아직 확정하지 않는다.

H는 정규식 대신 경로 구성요소로 버전 폴더를 확인하고, I는 별도의 정규식 구현으로 전 경로의 기대 분류와 실제 분류를 일대일 대조한다. 고정 범위의 예상 집계와 불일치하면 검사 실패. 기존 자료 수정·삭제 없음. 조사 범위 변경 없음.
