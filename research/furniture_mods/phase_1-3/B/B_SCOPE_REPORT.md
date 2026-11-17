# 1-3-B 공식 소스 인벤토리 — 2026-11-18

**상태: 공식 두 모드 Git tree 파일 분모 고정, Macaw 공식 원본 JAR 미확보로 전체 B 미완료.** 1-3-A 결과 7/7 그대로 보존, 1-3 상위 M1~M6 = 0/6.

| 항목 | Another Furniture | Handcrafted |
|---|---:|---:|
| 소스 고정 commit | `57eb624cbb7f` | `8d21d1665916` |
| MC / mod version | 1.21.1 / 4.0.3 | 1.21.1 / 4.0.3 |
| model JSON 경로 | 1,629 | 12,394 |
| block / item | 1,451 / 178 | 12,109 / 285 |
| authored / generated | 1,629 / 0 | 121 / 12,273 |
| 고유 model Git SHA | 1,629 | 9,439 |
| blockstate JSON | 177 | 267 |
| Java·Kotlin 소스 경로 | 89 | 86 |
| 이전 A 모델 원장 교차 | 273 | 136 |

검수 합계: 모델 JSON **14,023** 경로(2개 모드), 상태 JSON **444**개, Java/Kotlin **175**개. 파일 경로 별 Git SHA·크기를 보관하며 109개 유한 처리 회차를 할당함. **고유 Git SHA가 서로 같아도 서로 다른 resource ID의 파일은 독립 경로로 유지**.

## 원본·라이선스·차단

- Another [고정 소스](https://github.com/crispytwig/AnotherFurniture/tree/57eb624cbb7f408d43398c7434b0d38d312cb55d) / `LICENSE` blob SHA `a49cc44dcc57130151ed9e9032e066656b5e953b`: 코드 MIT, `/common/src/main/resources/` 등 리소스 All Rights Reserved.
- Handcrafted [고정 소스](https://github.com/terrarium-earth/Handcrafted/tree/8d21d1665916850c3fa3bdaf1370c50ec2ca7035) / `LICENSE` blob SHA `e91dc004b387336fb8ce0b052dfde5feeac0daed`: Terrarium License v1, 코드 MIT, 비코드 자산 All Rights Reserved.
- Macaw [원저자 Modrinth 배포 후보](https://modrinth.com/mod/macaws-furniture/version/xhmciaUD): 3.4.2 / MC 1.21.11 / Fabric 파일 후보를 찾았지만 **공식 JAR 바이트 접근·SHA 확인 실패**. 다른 소유자의 유사 GitHub 저장소를 공식 소스로 대체하지 않음.

## 정확한 실적 범위

이 회차는 Git 원본 트리의 **경로·SHA·크기 인벤토리 전수**이다. 14,023개 모델 JSON 전체 본문을 열어 parent/leaf 관계를 재귀 해석하거나, 상태 JSON의 모델 참조를 전부 파싱한 것은 아니다. `template` 및 `base`는 경로 단서로만 표시한다. A 기존 원본 재해시 204+69+22와 Handcrafted 표본2를 B의 신규 원본 읽기로 이중 계산하지 않는다.

- Another 이전 177 상태 중 미조사 **155개**는 해당 155개 파일의 경로/SHA를 확보한 상태이며 모델 연결 의미 분석은 1-3-D로 이관.
- Handcrafted 과거 120 authored+16 generated는 이번 전수 경로 모집단의 부분집합이고 16 generated를 전체로 오인하지 않음.
- 다음 필요한 작업: Macaw 공식 JAR 원본 바이트 확보→해시/내부 경로 추출, Another/Handcrafted 모델 본문·부모·renderer/생성 코드 해석, 1-3-B 독립 원격 감사.
- 저작권: 원저자 원본 JSON/PNG/JAR는 저장소에 복제하지 않고 분석 메타데이터만 게시.

산출물: `SOURCE_REGISTRY.csv`, `FIXED_SCOPE.csv`, `ENTRY_QUEUE.csv`, `B_MODEL_INVENTORY_*.csv`, `B_BLOCKSTATE_INVENTORY.csv`, `B_JAVA_KOTLIN_SOURCE_INDEX.csv`, `B_SCOPE_AUDIT.json`.

## 후속 원격 readback (2026-11-18)

커밋 `cb82ca46cf740e91d6aa022a687bee513bee4eea`에서 산출물 17개를 원격 재열람하고 Git blob SHA-1을 독립 계산한 결과 **17/17 PASS**, 총 파일 4,069,949 byte, 전체 인벤토리 행수 일치, 보호 연구 파일 변경 0. 근거: `B_REMOTE_READBACK.json` (다음 커밋 `c28f832430f3eb349d8d35213a0887a39e3d41e0`).
