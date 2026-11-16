# 1-2-F Entry1 실제 실행 준비서 — 소스 150개 (F 분류 0)

**작성 2026-11-16 KST · 시작 1-2-E 인수인계, 기준 main `16ecd4e5a0c353ec077238909cc546ac158ed97f`**.

- [고정 전체 범위](../F_FIXED_SCOPE_2390.csv): 모델 JSON 2,390경로, P1 544/P2 1039/P3 807, 직접 C2,304/E86, D 직접 참조2,136/나머지254.
- [Entry1 정확한 대기표](F_ENTRY1_QUEUE_150.csv): P1/P2/P3 **각50개(총150)**를 경로 오름차순 균일 분산. 그중 C 직접142, E 예외8, D 직접 참조137, D 비직접13. 표본 분포는 형태의 대표성을 증명한 게 아니다.
- **F 신규 실제 모델 원본 JSON 열람0/150·분류0/150**, 전체 F 분류0/2,390. C/D/E 선행 SHA join 확인을 F의 개별 모델 구조·시각 검사 완료로 계산하지 말 것.

## 순서와 확인 리스트
1. 현재 GitHub HEAD/계약·queue·원본 A/B/C/D/E SHA 확인 및 이전 F 완료 실적 존재 여부 확인. 같은 SHA·원본을 다중 실적으로 계산하지 않는다.
2. Entry1 원본 정확150 JSON 본문 직접 열람·Git SHA 검증. B 기하 parent chain/elements와 C UV·slot·PNG 출처 원본 증거를 모델별로 재결합한다.
3. 유형 스키마를 따라 **입체(요소/면/회전/상속) vs 평면(0/≤1두께) vs 텍스처(원본 PNG 관찰)**를 구분하고 정확한 수치, 비례, 무관측 구역을 기록한다. 미리보기는 게임 엔진 재현 아님.
4. D 원본의 variants/multipart·방향·대안과 연관 있는 모델만 조립 관계를 기입. 선택되지 않은 13은 NONE이라고 단정하지 말고 `NOT_DIRECT_D_SELECTED`을 유지한다.
5. E 예외 8개는 실제 엔진 기하를 추측하지 않고 `UNVERIFIED_RUNTIME_RENDERER` 소관을 보존한다. 제작 활용 패턴 후보는 원본 관찰/추정 구분한다.
6. `STYLE_OBSERVATIONS.csv` 150행, `F_GEOMETRY_FEATURES.csv`, `F_TEXTURE_VISUAL_EVIDENCE.csv`, `F_ASSEMBLY_LINKS.csv`, `F_ARCHETYPE_RULES.json`, `F_UNRESOLVED.csv`, `F_ENTRY1_REPORT.md`, `F_ENTRY1_INDEPENDENT_AUDIT.json`, `F_ENTRY1_REMOTE_READBACK.json`, `F_NEXT.md` 작성.
7. 독립 파서/원장 재검산, source SHA/행수/자료 근거·원형 분포 확인, GitHub 원격 SHA/본문 재조회. 실제 성공분만 F 진행도로 더한다.

**Exit:** F Entry1의 150/150 원본·스타일 관찰 행 및 차단·근거 상태가 정확히 감사되어야 Entry2 시작. 미완료면 Partial과 다음 queue row 기록. 전체 F 완료는 Entry6의 F1~F5 전부 PASS만 허용. Entry7 없음.
