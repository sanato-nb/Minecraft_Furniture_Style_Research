# 1-2-D Entry5 원본 blockstate 조사

**2026-11-16 KST · 시작 main `5febebb97207ecee724725c272eefe2ea9c83481` · 사용자 제공 Minecraft Java 1.21.11 추출 원본.**

고정 범위 `D_FIXED_SCOPE_1168.csv`의 Entry5 **265경로**(`oak_fence.json`~`short_dry_grass.json`)를 직접 읽고 JSON 본문·Git blob SHA를 대조했다. `D_ENTRY5_QUEUE_265.csv`의 순서와 SHA는 고정 범위 Entry5 265행과 일치한다. 원본 전문은 16개 단위 snapshot 17개에 보존했다. Entry1 12 + Entry2 96 + Entry3 265 + Entry4 265 + Entry5 265 = **D 누적 903/1,168 (77.31%)**, 미조사 **265**. Entry6 및 D 종료 감사는 아직 미실행이다.

| Entry5 원본 검사 | 결과 |
|---|---:|
| variants / multipart 원본 | 242 / 23 |
| 선언된 모델 선택 옵션 | 1,711행 |
| 원본 variants 또는 multipart 조건 도메인의 정적 상태 후보 | 2,303건 |
| 상태·모델 대안 적용 | 5,027건 |
| 고유 모델 참조 | 513개 (C 직접 497, E 소관 16) |
| 기존 C 모델별 적용 face·텍스처 슬롯 참조 | 5,394면·2,023행 |
| 기존 C face에 연결된 PNG 원본 SHA 확인 | 고유 270경로 |

variants의 선언 키, multipart AND/OR/`|` 조건, `apply` 배열 선택 대안과 weight, x/y/uvlock의 **명시 여부·원본 값**을 기록했다. multipart의 등장 조건값을 유한 직교 곱으로 전개했고, boolean 조건에 한쪽만 있으면 반대값을 파생 후보로 추가했다. 이는 **정적 분석용 문법상 상태 후보**이며 실제 게임 등록 상태 전부의 인증은 아니다. 서로 다른 multipart 규칙의 적용은 동시 부품, 한 규칙의 배열은 대안으로 분리했다.

모델 513개의 원본 SHA와 C 고정 범위의 SHA를 대조했다. C 직접 대상 497개는 기존 모델·face·slot 증거와 연결했고, 16개는 범위표 `E_EXCEPTION`/`1-2-E` 소관으로 분리했다. C face에 연결된 PNG 고유 270경로의 원본 SHA와 기존 RGBA 근거의 SHA를 대조했다. **5,394면·2,023슬롯·270 PNG는 기존 C 증거 재참조**이며 D 신규 face·PNG 픽셀 측정은 0이다.

별도 재판정은 원본 전문 265개를 다시 파싱하고 후보 상태 2,303건의 조건 결과, 모델 옵션 5,027건의 선택·회전·명시값을 계산했다. 모델 513개의 원본/C 범위 SHA와 E 담당 여부도 재확인했다. **불일치 0.** 재현 스크립트는 `scripts/phase_1_2_d_entry5.py`와 `scripts/phase_1_2_d_entry5_recheck.py`, 원장과 SHA/행수 manifest는 `D_ENTRY5_265_*`다.

**게이트:** D1 고정 1,168경로·6회 배정 유지. D2~D4는 실조사 **903경로에 한해 PASS**, 전체 분모는 진행 중. D5 최종 종합·원격 감사 대기. 공식 배포 JAR 인증, 게임 상태 레지스트리·런타임 렌더/UV 회전, E 특수 렌더 해석은 수행하지 않았다. A/B/C·v69 원장, C `heavy_core` 6면 정정, E 86개, 1-1 승인 150/150, 상위 완료 1/5를 보존한다.
