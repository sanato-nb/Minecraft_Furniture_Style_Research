# DBD-001 7-G 검색 및 검증 계약 v1.0

설계 전용 구현 `design_contract.py`와 합성 fixture `design_tests.py`는 운영 API가 아니다. 고정 T01~T16에 대응하는 시험의 제한을 각 결과에 기록한다. 실제 데이터베이스 이관, Minecraft 모델의 진실성, 렌더링 정확성, 대량 성능을 여기서 입증하지 않는다.

검색: parameter binding으로 용어(label, term_kind), 릴리스, 측정 metric/unit/min_value를 제한한다. claim의 같은 snapshot/object/key 최신 revision을 선택한다. confirmed_only 기본 true. 최신 범위별 assessment의 실제 선택 결과와 근거 실물 SHA를 재검사하며, CONFIRMED/PASS·유효 SUPPORT 및 링크 근거·기법 승인·충돌 여부를 확인한다. 불완전/후보는 confirmed_only=false에서 명시적으로 usable=false. 수치 필터는 동일 단위만 비교; 임의 단위 환산 없음. JSON 반환은 버전, 필터, 주장/조건/한계/원본 경로, 근거 메타데이터, 측정, 판정 및 반례를 함께 포함. 원본 바이너리 노출 없음. 단일 fixture의 서로 다른 두 근거 body는 기법 승인 최소 조건을 시험하기 위한 예이며 실제 독립 모델 사례 증명은 연구 검수자의 책임이다.

시험은 SQL 제약과 별도 계약 함수의 양성/음성 경로를 확인한다. 조회 결과는 데이터베이스 권한 있는 환경에서 읽는 설계용 결과이며, 외부 공개 시 locator/권리 상태에 대한 추가 정책이 필요하다. 현재 입력 식별자 검증, 원본 파서/의미적 정확성, 전체 운영 트랜잭션 통합, 대규모 검색 성능, 실제 외부 보존 위치 복구는 구현·검증되지 않았다. 이 범위가 필요한 시험은 PARTIAL로 남기며 전체 PASS로 승격하지 않는다.
