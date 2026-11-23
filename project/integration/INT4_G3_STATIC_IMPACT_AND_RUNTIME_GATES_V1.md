# INT-4-G3 정적 소스 선택 영향 검수

기존 A 예외 112 모델, C 예외 6343면 및 D 원본 예외 6건을 실제 78456 선택 옵션과 교차 검증.
AF 4.0.3 고정 Git 원본 AFBlocks.java 및 unused/white_awning.json 직접 재다운로드, Git blob SHA 검사.

A model review = {"CONDITIONAL_PARENT_MISSING_NOT_DIRECTLY_SELECTED_IN_D": 48, "HOLD_HANDCRAFTED_BASE_MODEL_USAGE_AND_JAVA_UNKNOWN": 6, "NOT_APPLICABLE_GENERATED_ITEM_STATIC_CUBOID": 58}
C face review = {"CONDITIONAL_C_EXCEPTION_NOT_DIRECTLY_SELECTED_IN_STATIC_D_OPTIONS": 6343}
D anomalies = {"PRIOR_CHAIR_VARIANT_3_POINTS_TO_1": 2, "UNRESOLVED_MODEL_REF": 4}

주의: 소스 내 정적 선택 부재가 동적 자바/아이템 렌더 사용의 부재를 의미하지 않는다.
AFBlocks.java에 awning 문자열 부재는 파일 한 곳의 사실이며 전체 등록 경로의 부재가 아니다.
INT-4-G/H 최종 승인 0. INT5 의미 및 INT6 원본 재배포/학습 권한 승인 0.

