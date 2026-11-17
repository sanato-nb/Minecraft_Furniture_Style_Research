# 1-2-G Entry1 후속 인수인계 — 185 PNG 원본 바이너리 직접 확인 차단

**현재 상태:** `G_ENTRY1_PARTIAL_JSON_COMPLETE_PNG_BINARY_PENDING`. **Entry2 시작 금지**(Entry1 미종료). 기준 `main` `88d9da945953e80597faa6e91a7c79078a5da819`; 실행 재개 시 최신 HEAD를 다시 확인하라.

완료한 사실: Entry1 347개 경로/Git SHA 실제 검수 완료; 모델 150·blockstate 12 소스 JSON 원문 직접 열람, 부모 계보214 고유 JSON path, 일반142/E8, geometry 371 elements / face 1,373, 원본 UV 명시1,142, 원본 texture slot 전개로 C 결합1,238/미바인딩135, D 모델 옵션167/대상49 모델 대조 모두 0차이. 모델/F/B/C/G 교차 참조를 다시 처음부터 만들지 말고 소스 스냅샷·CSV·독립 검산을 재사용할 것.

**차단 원인:** GitHub 연결의 텍스트 전용 인터페이스가 원본 PNG 바이너리 185개를 UTF-8 디코드할 수 없다. 최신 Git 트리의 blob SHA 185/185 및 C의 이전 RGBA 177개 SHA, F의 기존 38 PNG 시각 증거는 연결했으나 이번 G에서 픽셀을 직접 봤다고 하지 않는다.

**다음 실행:** 동일 185 PNG 원본을 바이너리 접근 가능한 수단으로 열어 bytes·PNG 시그니처·디코딩 및 필요 범위 RGBA와 C 기존 SHA/크기/애니메이션 `.mcmeta`를 독립 비교. 대조 뒤에도 C 범위 밖 8 PNG를 임의로 C 검증 완료로 변경하지 말고 신규 G 실증/미확정을 분리. 완료 시 `G_INDEPENDENT_AUDIT.json` 새 독립 검산과 `G_ENTRY1_REPORT.md` 신규 ERRATA/후속 판정 파일로 수정 근거 작성하고 원격 SHA/행수/본문 재조회. 다른 기존 A~F·v69 소스에 손대지 말 것.

검증 자료: `G_SOURCE_CROSSWALK.csv` 347행, `G_ENTRY1_FACE_PNG_CROSS_LINKS.csv` 1,373행, `G_ENTRY1_D_RULE_MODEL_LINKS.csv` 167행, `G_UNRESOLVED.csv` 203행, `G_ENTRY1_SOURCE_INDEX.json` 및 `source_snapshots/`. 이 상태에서 종료 게이트 G1~G6 **0/6**, G 전체 완료 **금지**. 모든 Entry는 당초 계획의 6회만 허용.
