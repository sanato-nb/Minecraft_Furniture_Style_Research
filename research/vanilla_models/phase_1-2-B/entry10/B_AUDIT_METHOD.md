# B Entry10 독립 소스 기하 감사 재현 방법

**원본 근거**: `SOURCE_JSON_CACHE_2360.json`, `B_SCOPE_2390_STATUS.csv`, A 원본 자산 색인 `A_ASSET_REGISTRY_4669.csv`, 기존 v69 두 P1 원장. 별도 원본 JSON 재열람 636 leaf / 122 고유 부모는 Git Blob SHA 지정 조회 근거 파일에 연결.

1. 복합 키는 `(asset_type, full_source_path, git_blob_sha)`. source index 4,669개와 모든 path/SHA 비교. SHA가 같아도 서로 다른 경로를 합치지 않는다.
2. B-first 모델 2,360개에서 parent를 참조하는 동안 `minecraft:block/<id>` → `1.21.11/assets/minecraft/models/block/<id>.json`으로 경로 변환, 순환·부모 누락·비정상 참조 확인. `P1` 조상 의존은 P1 자산의 원본 모델 경로 집합과 모든 조상 경로를 비교.
3. leaf 자신부터 첫 `elements` 선언이 있는 조상을 찾으면 기하 제공자, 없으면 `no_general_elements`. 요소 `from/to`, `rotation`, faces, cullface를 원본 JSON에 대한 정확한 선언값으로 읽는다. bbox는 각 from/to 값의 축별 min/max. 유효하지 않은 좌표는 오류로 기록하고 임의 수정 금지.
4. `ELEMENTS_P1_ALL.csv`·`P2`·`P3`의 각 원본 행은 제공자 SHA와 `elements[element_index]`를 직접 대조해 5,689 요소·face23,090·cullface8,988을 재계산. 입체 메시/후처리 렌더 결과의 중복 제거가 아니라 **leaf별 원본 선언 적용 인스턴스**다.
5. 원본 상태표 비교: Entry9 baseline 대비 Entry10 636개만 변경, 나머지 1,754행 **글자 단위 보존**. E-first P1 30개 및 이전 완료 1,724개는 신규 실적 금지.
6. 과거 `NO_P1_ANCESTOR_SOURCE_CHECKED` 1,080행은 실제 원본 검수에서 사용된 **P1 조상 없음(no)**과 동일 의미의 기존 enum이다. 판정 의미를 비교할 때만 정규화하고 이전 셀은 재작성하지 않는다.
7. `no_general_elements` 56개는 렌더러 작동 미확인/E 이관임을 보존한다. UV·PNG·blockstate·런타임 인증은 B 종료 판정에 넣지 않는다.
8. 생성물 독립 소스 감사: `B_ENTRY10_B1B2_AUDIT.json` 28/28, `B_ENTRY10_B3_AUDIT.json` 26/26. GitHub 커밋 후 실제 원격 Blob SHA와 CSV 행수, 전체 프로젝트 상태 파일 및 불변 원본 SHA를 다시 조회해야 최종 B4 PASS를 인정한다.
