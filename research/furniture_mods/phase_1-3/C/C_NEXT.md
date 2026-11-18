# 다음 단계 1-3-D

세 모드 모델 원본 16,572개와 계보를 감사했다. `mod_furniture_catalog.csv.gz`에서 모드와 모델 ID로 조인한다. 정적 결과와 예외는 [C 보고서](C_REPORT.md)를 참고한다.

- B에서 고정한 상태 JSON은 Another 177, Handcrafted 267, Macaw 714경로다. 원문에서 variant/multipart 조건과 선택 모델, 각도·uvlock·weight를 확인한다.
- 방향·연결·조립 판정에 필요한 코드 근거를 추가한다. Another birch/spruce 의자 참조 예외 2건과 unused white_awning 누락을 보존한다.
- 부모가 빠진 Macaw 44개와 Another 4개는 C 예외를 연결하고 동작을 별도 판정한다. 실제 블록 상태가 선택하는지부터 확인한다.
