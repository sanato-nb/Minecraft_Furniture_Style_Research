# 1-3-B 공식 원본 확보·고정 모집단 검증

2026-11-18 KST. 시작 기준 main `8a94f9a3fe2b3720318a97f1b91221b55809d417`. 기존 원문 검증 587경로와 파일 목록 두 모드를 확인한 뒤, 미검사 원문과 Macaw 공식 JAR을 확인했다. 세 모드의 고정 소스 조사 범위는 완료됐다.

| 고정 출처 | 모델 JSON | blockstate JSON | 별도 항목 |
|---|---:|---:|---|
| Another Furniture, Git `57eb624cbb7f408d43398c7434b0d38d312cb55d` | 1,629 | 177 | Java/Kotlin 89경로 |
| Handcrafted, Git `8d21d1665916850c3fa3bdaf1370c50ec2ca7035` | 12,394 | 267 | Java/Kotlin 86경로 |
| Macaw's Furniture 3.4.2, Minecraft 1.21.11 Fabric | 2,549 | 714 | item definition 716경로, JAR 내 클래스 53경로 |
| 합계 | 16,572 | 1,158 | item definition 716경로 별도 |

- 모델·상태 원문 17,730경로를 읽어 해시와 JSON 파싱을 확인했다. 선행 587경로와 차집합인 17,143경로가 이번에 추가로 확인됐다. Macaw item definition 716개도 별도 집계했다.
- Another의 미검사 모델 1,356개, Handcrafted generated 모델 12,257개와 상태 267개가 모두 원문 검증됐다. 두 모드의 고정 Git 경로·크기·blob SHA와 원장 일치, 코드 175경로의 원본 SHA 확인. 클래스 내부 동작 분석은 후속 과제다.
- Macaw [공식 Modrinth 배포 버전](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD)의 파일 2,184,868바이트를 받았다. 공식 SHA-1·SHA-512, 로컬 SHA-256, ZIP CRC 및 Fabric 메타데이터를 확인했다. Macaw 모델 2,549개 중 block 2,547개와 item model 2개를 분리했다.
- Macaw 배포 페이지와 Fabric 메타데이터는 권리 유보를 표시한다. 내부 `LICENSE_modid` 파일의 헤더는 CC0 1.0이며 그 적용 범위는 확인되지 않았다. 원장에는 출처·해시·파생 통계만 저장했다.
- 정적 참조 예외는 45파일에서 48회 확인됐다. Another의 기존 `unused/white_awning` 누락 참조 1종이 선택 옵션 4회에 나타났다. Macaw는 부모 `mcwfurnitures:block/parent/desk`와 `mcwfurnitures:block/parent/drawer_base`에 각각 모델 22개가 연결되지만 JAR 해당 경로가 없다. 게임에서 모델이 로드되는 방식은 C/D에서 확인한다.
- 기존 회차 109개에 Macaw 회차 28개를 추가했다. A는 7/7, 전체 1-3 종료 게이트는 0/6이다. 다음 작업은 **1-3-C 부모 계보·형상 분석**이다. 회전·연결·상태 동작 검증은 D 담당이다.

[B_SOURCE_BODY_AUDIT.json](B_SOURCE_BODY_AUDIT.json) · [B_INDEPENDENT_SOURCE_RECOUNT.json](B_INDEPENDENT_SOURCE_RECOUNT.json) · [고정 범위 CSV](B_FIXED_THREE_SOURCE_SCOPE.csv) · [B_MACAW_ENTRY_QUEUE.csv](B_MACAW_ENTRY_QUEUE.csv)

`B_{AF,HC,MACAW}_SOURCE_BODIES.csv.gz`에는 파일별 SHA와 부모·요소·면·정적 참조 집계가 있다. `B_REFERENCE_EXCEPTIONS.csv.gz`에는 영향 경로와 참조별 예외를 기록했다. 일반 압축 도구로 해제하면 CSV로 읽을 수 있다.
