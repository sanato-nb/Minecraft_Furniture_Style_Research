# 1-3-B 현행 인수인계 — 2026-11-18

## 완료·검증

- 1-3-A 7/7 승인 원본 보존. 공식 소스 두 종 각 고정 Git commit, 모델 JSON 14,023개·blockstate 444개·Java/Kotlin 175개 **Git path/SHA/size 인벤토리** 고정. 109개 분석 회차 생성.
- Another 기존 미조사 state **155/155 직접 SHA** 검증 완료(A 22와 합쳐 **177/177**). 규칙/적용 항목 8,137개, ref 1,153종(내부 존재 1,151, 외부 air1, `unused/white_awning` missing `awning/white_double` 1). `B_AF_155_INDEPENDENT_AUDIT.json`와 예외 CSV를 계승.
- Handcrafted authored **121/121** 직접 SHA, 원형 parent 34 local 존재·86 Minecraft 외부·1 없음, 자체 810 elements/4,860 faces. A prior generated16도 직접 SHA·parent 확인; A prior136/136 정합. 현재 HC 모델 직접 검증 137/12,394, 생성 모델 잔여12,257개 원문 미열람.
- A+B 중복 제거 직접 원본 바이트 검증 **587 distinct JSON**. B에서 새로 본 290개(전체 이 B 원본 재열람292개 중 A 이전 직접 2개 제외). 3개 Handcrafted datagen Java의 정적 원본 소스 확인.
- 기존 B 인벤토리 17파일, AF 11파일, HC authored 8파일은 각 원격 SHA 전부 PASS; B 원본/기존 A 보호 파일 수정 없음.

## 다음 진행 순서

1. **Macaw 공식 JAR 원본 확보 및 SHA·내부 모델 인벤토리**: 공식 [Modrinth 버전 xhmciaUD](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD) (3.4.2/MC1.21.11/Fabric); 바이너리 접근 불가. GitHub issue 저장소를 모델 소스로 오인하거나 비공식 복제본 대체 금지. 현재 B 전체 BLOCKED.
2. **Handcrafted generated JSON 12,257개**의 직접 원문 SHA·parent 경로 검사 및 전체 source generator 모델 생성 구조 확인. 현재 생성 모델 수 12,273은 Git tree 파일 수이지 유니크 형태 아님. Handcrafted blockstate 267 원문 검사.
3. Another 모델 총 1,629 중 기존 A 273 원문 검증 외 **나머지 1,356개**의 직접 parent/geometry 검사. 177 상태 원문 SHA는 끝났지만 실제 분기·회전·연결 동작은 D와 코드 근거 필요. 특히 `unused/white_awning` 누락 1건 유지.
4. 109개 `ENTRY_QUEUE.csv` 회차를 기준으로 C/D 원형·상태 분석. source SHA verification completed로 변경된 5회차는 C/D 실측 승인(PASS)이 아님.
5. 원저자 리소스 All Rights Reserved. 원본 JSON/PNG/JAR 재배포 금지. 1-3 M1~M6 0/6 보존. 사용자 추가 승인 없이 Macaw 탈락·대체 모드 선정 금지.

## 참고 파일

`B_SCOPE_REPORT.md`, `B_SCOPE_AUDIT.json`, `B_ASSET_ORIGINAL_VERIFICATION_COVERAGE.csv`, `B_AF_155_INDEPENDENT_AUDIT.json`, `B_HC_AUTHORED_INDEPENDENT_AUDIT.json`, `B_HC_PRIOR136_REHASH_AUDIT.json`, `B_HC_DATAGEN_SOURCE_EVIDENCE.csv`, `B_REMOTE_READBACK.json`.
