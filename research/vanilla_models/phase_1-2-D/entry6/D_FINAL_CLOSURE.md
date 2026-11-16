# 1-2-D 최종 종료 판정

**2026-11-16 KST · 사용자 제공 Minecraft Java 1.21.11 추출 원본 · 고정 6 Entry 종료.**

1-2-D의 고정 **1,168/1,168 blockstate JSON**을 실제 읽고 Git blob SHA로 검산했다. 배정 중복·누락 0. 원본 선언의 선택 모델 **7,592행**, 정적 상태 후보 **9,193건**, 상태·모델 대안 적용 **19,440건**을 여섯 회차의 원장과 대조했다. 상태에 등장한 고유 block 모델 2,136개는 C 고정 범위의 원본 SHA에 연결됐으며 그중 84개는 E 소관 예외다. C 기존 face·UV·slot·PNG는 D 신규 측정으로 집계하지 않았다.

| 종료 게이트 | 결과와 범위 |
|---|---|
| D1 | PASS — 1,168경로의 Git 원본·6회 배정, 중복·누락 0 |
| D2 | PASS — 원본 본문·SHA 전수, variants/multipart 규칙 및 모델 대안 기록 |
| D3 | PASS — 원본 문법에서 유한 전개한 정적 상태 조립. 실제 게임 등록 상태 인증은 범위 밖 |
| D4 | PASS — 모델 경로·SHA와 기존 B/C 증거, E 소관 예외 연결 |
| D5 | PASS — Entry별 독립 감사 7건과 Entry6 원격 변경 파일 **33개 SHA**, 원격 원본 상태표 **265행**·규칙 **1,836행** 재조회. A/B/C·v69·원본 자산 변경 0 |

Entry6 원격 연구 커밋 [`3df6ecac`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/commit/3df6ecacbabdd49697c79893d81ee4b81e5de31d)과 [원격 재조회 기록](D_ENTRY6_REMOTE_READBACK.json), [기계판독 종료 감사](D_FINAL_CLOSURE.json)를 근거로 **`D_COMPLETE_SOURCE_BLOCKSTATE_ASSEMBLY_SCOPE`**로 종료한다. Entry7은 없다.

이는 **원본 blockstate의 정적 조립 연구 완료**다. 공식 배포 JAR 인증, 게임 상태 레지스트리의 유효 상태 전체, 실제 런타임 렌더와 UV 회전, E 특수 렌더 해석은 검증하지 않았다. 상위 1-2 전체 완료나 가구 제작·좀보이드 맵 변환을 선언하지 않는다. 1-1 승인 150/150 및 상위 단계 완료 1/5를 유지한다.
