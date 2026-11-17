# 1-2-G Entry1 PNG 후속 실검증 종료 단계 — 최종 원격 재조회 대기

2026-11-17 신규 원본 PNG 185/185 Base64 바이너리, Git blob SHA/PNG CRC/zlib/RGBA가 전부 PASS. C 원장 177/177 독립 해시 및 치수 비교 PASS, C 밖 8은 새로운 G 실증, mcmeta 17/17 SHA 확인(애니메이션 7), F 기존 38 시각 근거 유지. G 소스 감사 대상 347/347 직접 본문 확인. 기존 E8 특수 renderer/135 템플릿 미바인딩/게임 상태 검증 제외 보존. **Entry1 정식 승인 선언은 신규 보고서·상태 파일 원격 SHA/행수 재검사를 통과한 다음에만 진행**. 그 전에는 Entry2 미착수.

다음 단계는 1) 새 보고서·독립감사·상태/원장 원격 readback; 2) 이상 없을 때 Entry1 APPROVED, Entry2 허용하지만 아직 실행하지 않음; 3) 그 후 기존 고정 큐 `entry2/G_ENTRY2_QUEUE_775.csv`에 배정된 775개만 진행. 6 Entry와 원본 A~F/v69은 불변.

---

## 이전 인수인계 (당시 바이너리 차단, 현재 해소된 이력)

# 1-2-G Entry1 후속 인수인계 — 185 PNG 원본 바이너리 직접 확인 차단

**현재 상태:** `G_ENTRY1_PARTIAL_JSON_COMPLETE_PNG_BINARY_PENDING`. **Entry2 시작 금지**(Entry1 미종료). 기준 `main` `88d9da945953e80597faa6e91a7c79078a5da819`; 실행 재개 시 최신 HEAD를 다시 확인하라.

완료한 사실: Entry1 347개 경로/Git SHA 실제 검수 완료; 모델 150·blockstate 12 소스 JSON 원문 직접 열람, 부모 계보214 고유 JSON path, 일반142/E8, geometry 371 elements / face 1,373, 원본 UV 명시1,142, 원본 texture slot 전개로 C 결합1,238/미바인딩135, D 모델 옵션167/대상49 모델 대조 모두 0차이. 모델/F/B/C/G 교차 참조를 다시 처음부터 만들지 말고 소스 스냅샷·CSV·독립 검산을 재사용할 것.

**차단 원인:** GitHub 연결의 텍스트 전용 인터페이스가 원본 PNG 바이너리 185개를 UTF-8 디코드할 수 없다. 최신 Git 트리의 blob SHA 185/185 및 C의 이전 RGBA 177개 SHA, F의 기존 38 PNG 시각 증거는 연결했으나 이번 G에서 픽셀을 직접 봤다고 하지 않는다.

**다음 실행:** 동일 185 PNG 원본을 바이너리 접근 가능한 수단으로 열어 bytes·PNG 시그니처·디코딩 및 필요 범위 RGBA와 C 기존 SHA/크기/애니메이션 `.mcmeta`를 독립 비교. 대조 뒤에도 C 범위 밖 8 PNG를 임의로 C 검증 완료로 변경하지 말고 신규 G 실증/미확정을 분리. 완료 시 `G_INDEPENDENT_AUDIT.json` 새 독립 검산과 `G_ENTRY1_REPORT.md` 신규 ERRATA/후속 판정 파일로 수정 근거 작성하고 원격 SHA/행수/본문 재조회. 다른 기존 A~F·v69 소스에 손대지 말 것.

검증 자료: `G_SOURCE_CROSSWALK.csv` 347행, `G_ENTRY1_FACE_PNG_CROSS_LINKS.csv` 1,373행, `G_ENTRY1_D_RULE_MODEL_LINKS.csv` 167행, `G_UNRESOLVED.csv` 203행, `G_ENTRY1_SOURCE_INDEX.json` 및 `source_snapshots/`. 이 상태에서 종료 게이트 G1~G6 **0/6**, G 전체 완료 **금지**. 모든 Entry는 당초 계획의 6회만 허용.
