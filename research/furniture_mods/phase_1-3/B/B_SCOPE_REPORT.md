# 1-3-B 공식 소스 조사 — 2026-11-18 (진행 중)

**현 상태: Another·Handcrafted 공식 원본 Git 트리 모집단 고정 및 부분 원문 검증 완료. Macaw 공식 JAR 미확보로 1-3-B 전체 BLOCKED.** 이전 1-3-A 7/7 보존; 상위 1-3 M1~M6는 0/6.

## 공식 고정 Git 소스 모집단

| 구분 | Another Furniture | Handcrafted |
|---|---:|---:|
| 핀 commit | `57eb624cbb7f408d43398c7434b0d38d312cb55d` | `8d21d1665916850c3fa3bdaf1370c50ec2ca7035` |
| 고정 MC / 모드 버전 | 1.21.1 / 4.0.3 | 1.21.1 / 4.0.3 |
| 모델 JSON 전체 파일 경로 | 1,629 | 12,394 |
| 블록 모델 / 아이템 모델 | 1,451 / 178 | 12,109 / 285 |
| authored / generated 모델 | 1,629 / 0 | 121 / 12,273 |
| blockstate JSON | 177 | 267 |
| Java/Kotlin 소스 경로 | 89 | 86 |

모델 JSON 14,023경로·blockstate 444·코드 175를 Git tree의 **경로·Git SHA·크기**로 고정. `FIXED_SCOPE.csv`, `B_MODEL_INVENTORY_*.csv`, `B_BLOCKSTATE_INVENTORY.csv`와 109개 회차 `ENTRY_QUEUE.csv`로 추적. 모델 파일 수는 서로 다른 가구 원형·실제 게임 등록 수를 의미하지 않음.

## 실제 원본 JSON 바이트 확인

- Another blockstate: 기존 A 22 + 이번 B 신규 155 = **177/177 원본 SHA 근거**. 이번 B에서 155개 직접 JSON 파싱·Git SHA-1 독립 재계산; 규칙 및 적용 항목 8,137건, 모델 참조 1,153종. 1,151종 모드 내부 존재·1종 바닐라 `minecraft:block/air`·**1종 고정 원본 누락**.
- 참조 누락: `blockstates/unused/white_awning.json` → `another_furniture:block/awning/white_double`. `models/block/awning/white_double.json`은 핀 소스에 없음. `unused` 하위 경로라 런타임 등록·사용 여부는 아직 미확인. 정적 출처 예외로 기록하며 정상/결함 단정 금지.
- Another 모델 JSON 직접 원본 SHA: 기존 A 204 leaf + 69 template = **273/1,629**. 나머지 1,356개는 Git SHA만 확보·원본 body 검사는 C 단계.
- Handcrafted authored JSON: **121/121** 직접 재해시. 자체 element 810·면 4,860 (상속 면 제외). local 부모 파일 34개 모두 존재, 외부 Minecraft 부모 86개, 부모 없음 1개. 기존 A authored120 SHA 일치.
- Handcrafted generated: **16/12,273개** 기존 표본을 직접 JSON 열람·원본 SHA·parent 검사, 부모 원형 16개 모두 존재. 미열람 12,257개. 기존 A authored120 + generated16의 **136/136 원본 SHA 재대조** 완료; 이전 A 원문 2개와 재검증 건수 중복 구분.
- A+B 누적 서로 다른 원본 JSON 바이트 검증은 **587개**: Another 모델273 + Another states177 + Handcrafted 모델137. 이번 B에서 직접 다시 연 원본 292개 중 A에서 이미 본 2개를 제외한 신규 고유 경로는 **290개**.
- Handcrafted 데이터 생성 코드 `HandcraftedDataGenerator.java`, `ModBlockStateProvider.java`, `ModItemModelProvider.java`의 실제 소스 라인 확인. 등록 목록 반복·모델 builder.parent 구조 확인; 실행/실제 생성물 재현이 아님. `B_HC_DATAGEN_SOURCE_EVIDENCE.csv` 참조.

## 독립 증거와 작업 안전

- B 기본 인벤토리 17파일 원격 SHA 17/17 PASS, Another 상태 새 CSV 11파일 원격 SHA 11/11 PASS, Handcrafted authored CSV 8파일 원격 SHA 8/8 PASS. 세부 원본 SHA·본문 재계산 검증 결과는 `B_AF_155_INDEPENDENT_AUDIT.json`, `B_HC_AUTHORED_INDEPENDENT_AUDIT.json`, `B_HC_PRIOR136_REHASH_AUDIT.json` 참조.
- 기존 v11~v24·1-1·1-2 연구 원본 **수정 금지 유지**. A 7/7 변경 없음. 원저자 JSON·PNG·JAR을 연구 repo에 복제하지 않고 SHA·파생 계량·출처만 저장.
- Another `LICENSE`: 코드 MIT/리소스 All Rights Reserved. Handcrafted Terrarium License v1: 코드 MIT/비코드 All Rights Reserved. Macaw 공식 Modrinth 페이지도 ARR.

## B 전체가 여전히 미완료인 이유

1. Macaw's Furniture 공식 Modrinth 버전 `xhmciaUD` (3.4.2 / MC1.21.11 / Fabric)의 실제 JAR 바이트 확보가 실패. 내부 JSON/라이선스·파일 SHA·모집단 미검증, Macaw 0 원본.
2. Handcrafted generated 12,257 JSON, Handcrafted blockstate 267 JSON과 Another 나머지 모델 원본 body 검증 및 parent/renderer·실행규칙 분석은 미완료. 소스 트리 파일 분모 ≠ 고유 가구 형태 분모.
3. 실제 blockstate 등록·연결 동작·렌더·충돌은 이 원본 JSON 감사로 인증하지 않음. C/D 작업으로 계승.

**1-3-B 상태: PARTIAL_PASS_TWO_OFFICIAL_GIT_TREE_POPULATIONS / FULL_SCOPE_BLOCKED_MACAW. 1-3 상위 M 0/6.**
