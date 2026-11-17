# 1-3-B 중간 인수인계 (2026-11-18)

**상태: 두 공식 소스 고정 트리의 자산 경로 전수 PASS, 1-3-B 전체는 BLOCKED/IN_PROGRESS.** 이전 1-3-A 7/7 유지. 상위 1-3 M1~M6 0/6.

## 현재 실제 수행 완료

- Another Furniture 고정 `57eb624cbb7f408d43398c7434b0d38d312cb55d`: 모델 JSON 1,629(블록 1,451, 아이템 178), 상태177, 소스 Java/Kotlin 89.
- Handcrafted 고정 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`: 모델 JSON 12,394(블록 12,109, 아이템 285; authored 121, generated 12,273), 상태267, Java/Kotlin 86.
- 총 모델 JSON 경로14,023, 상태444, 코드175. Git tree SHA·size 경로별 표기. 유한 109회차. 연구 GitHub 결과 파일 17개 원격 Git blob SHA 재계산 17/17 PASS 및 보호 파일 diff0.
- 두 모드 모두 고정 `gradle.properties`: MC1.21.1 / mod4.0.3. 리소스 저작권 제한 확인. 파일 SHA 중복을 고유 모델 형상 수로 오인 금지.

## 미완료 / 다음 실제 행동

1. **Macaw 공식 JAR**: 원저자 Modrinth의 `xhmciaUD` (Macaw Furniture 3.4.2, MC1.21.11 Fabric) 다운로드 URL은 확인했으나 이 실행 환경에서 바이너리 접근에 실패. 공식 배포 바이트, 다운로드 SHA, JAR 메타데이터와 내부 모델/상태 전수 검증 이전에는 B PASS 불가. 제삼자 포크를 공식 소스로 인정하지 않음. 버전 간 호환성도 추정하지 않음.
2. Another A 미조사 **155 blockstate**는 경로·Git tree SHA 인덱스만 신규 등록. 원문 직접 SHA 및 model refs 전체 읽기 미수행. 대량 동시 원문 호출은 커넥터 호출 한도에 막혔으므로 적은 묶음으로 재시도하며 결과를 B 증거 CSV로 저장해야 함.
3. Handcrafted generated 12,273를 포함한 모델 원문 부모/leaf, 참조 체인·생성 코드 실체를 본문으로 판별. 현재 `template`/ `base`는 파일명에 근거한 후보일 뿐이며 parent 직접 확인이 아님.
4. 소스 전체 3모드 승인과 고정 분모 이후 1-3-C/D에 109개 Entry를 계승. 원본 JSON/PNG/JAR 저작권 파일은 GitHub에 게시하지 말 것. 1-3 A 기존 증거 수정·중복 실적 금지.

## 주요 파일

`B_SCOPE_REPORT.md`, `B_SCOPE_AUDIT.json`, `SOURCE_REGISTRY.csv`, `FIXED_SCOPE.csv`, `ENTRY_QUEUE.csv`, `B_BLOCKSTATE_INVENTORY.csv`, `B_JAVA_KOTLIN_SOURCE_INDEX.csv`, `B_MODEL_INVENTORY_*.csv`, `B_REMOTE_READBACK.json`.
