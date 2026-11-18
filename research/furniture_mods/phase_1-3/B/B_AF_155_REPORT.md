# Another Furniture 이전 미조사 155 blockstate 원본 검증 완료

- 고정 원저자 commit: `57eb624cbb7f408d43398c7434b0d38d312cb55d`.
- 신규 직접 열람한 원본 `blockstates/*.json` **155/155**, 독립 Git blob SHA·원본 바이트 크기·기존 트리 SHA **전부 일치**. 저장소의 11개 증거 CSV도 원격 독립 SHA **11/11 PASS**.
- 기존 A 22개 직접 검증에 연결하되 중복 신규 실적으로 계산하지 않음: **177/177 원본 blockstate 소스의 SHA 검증 근거 확보**.
- 155개에서 variants 138 / multipart 17, 상태 규칙 **8,137**, 모델 적용 항목 **8,137**, 서로 다른 모델 참조 **1,153**.
- 모드 내부 모델 ref **1,151**는 고정 모델 파일 트리에 존재. 외부 참조 `minecraft:block/air`는 14개 curtain 상태에 존재(별도 바닐라 모드 해석). **원본 누락 ref 1개**: `unused/white_awning.json`이 `another_furniture:block/awning/white_double`을 참조하지만 해당 모델 JSON 파일이 없음. 원본 `white_awning.json` 정상 경로도 원본에 없음. 해당 `unused` 경로의 런타임 사용 여부 미확인.
- 이 결과는 소스의 **정적 모델 참조와 JSON 규칙**에 대한 것이며, 실제 등록·게임 내 렌더·충돌·연결 판정과 동일하지 않음.
- 후속: `B_AF_155_INDEPENDENT_AUDIT.json`, `B_AF_155_MODEL_REF_INDEX.csv`, `B_AF_155_REF_EXCEPTIONS.csv`를 사용해 1-3-D에서 상태 조건·회전 및 실제 코드/등록 교차 검증. Macaw JAR 미확보 때문에 1-3-B 전체·상위 M 게이트를 완료 처리하지 않음.
