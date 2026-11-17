# A-02 기존 blockstate 22개 직접 원문 검증

원저자 고정 커밋의 **JSON 22/22 본문 재읽기 + Git blob SHA1 재계산 22/22 일치**. v21 12개 적용 802, v23 10개 적용 386, 총 1188개, 행·모델참조 집합 대조 오류 0개. variants 원문 상태 키·모델·회전·uvlock 복합키 동치 17/17.

미조사 후보 `177 - 22 = 155`개는 **이번 새 검증 177/177로 승격하지 않음**. 22개 상태가 참조한 원본 모델(고유) 205, 외부 `minecraft:block/air` 등 다른 분모 유지.

v24 예외 2건 원문 재현 2/2: birch_chair facing=south,tucked=false,variant=3 → another_furniture:block/chair/birch_1; spruce_chair facing=south,tucked=false,variant=3 → another_furniture:block/chair/spruce_1. 임의로 모델을 정정하지 않음.

A2 판정: **PASS** (원본 JSON SHA와 상태 규칙을 감사한 22개 범위에 한정). 원본 멀티파트 조건의 문자열/객체 동형 여부까지 전체 의미 동치 인증하지는 않음.
