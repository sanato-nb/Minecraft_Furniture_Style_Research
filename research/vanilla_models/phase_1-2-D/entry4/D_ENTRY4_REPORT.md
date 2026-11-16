# 1-2-D Entry4 원본 blockstate 조사

**2026-11-16 KST · 시작 main `cdcf42f26b68dd482e87529d8ebeee3e88db21ec` · 사용자 제공 Minecraft Java 1.21.11 추출 원본.**

고정 범위 `D_FIXED_SCOPE_1168.csv`의 Entry4 **265경로**(`dropper.json`~`oak_button.json`)를 직접 읽고 원본 JSON 본문·Git blob SHA를 대조했다. `D_ENTRY4_QUEUE_265.csv`는 고정 범위의 경로·SHA를 순서대로 옮긴 배정표이며, 원본 전문은 16개 단위 snapshot 17개에 보존했다. 독립 감사에서 고정 범위와 이 배정표의 265개 경로·SHA가 모두 일치했다. Entry1 12 + Entry2 96 + Entry3 265 + Entry4 265 = **D 누적 638/1,168 (54.62%)**, 미조사 **530**. Entry5·6은 아직 미실행이며 D 전체 완료는 아니다.

| Entry4 원본 검사 | 결과 |
|---|---:|
| variants / multipart 원본 | 241 / 24 |
| 선언된 모델 선택 옵션 | 1,496행 |
| 원본 variants 또는 multipart 조건 도메인의 정적 상태 후보 | 1,804건 |
| 상태·모델 대안 적용 | 3,976건 |
| 고유 모델 참조 | 498개 (C 직접 463, E 소관 35) |
| 기존 C 모델별 적용 face·텍스처 슬롯 참조 | 4,480면·1,821행 |
| 기존 C face에 연결된 PNG의 원본 SHA 확인 | 고유 249경로 |

variants의 선언 키, multipart의 AND/OR/`|`, 규칙별 배열 대안과 weight, x/y/uvlock의 **명시 여부 및 값**을 기록했다. multipart의 등장 조건값을 유한 직교 곱으로 전개했고, boolean 조건에 한쪽만 있으면 반대값을 파생 후보에 포함했다. 이는 **분석용 문법상 후보**이며 실제 게임에 등록된 상태의 완전 목록이 아니다. 서로 다른 multipart 규칙은 동시 부품, 한 규칙의 `apply` 배열은 대안 선택으로 분리했다.

모델 498개의 원본 SHA와 C 고정 범위표의 SHA를 일치시켰다. 직접 대상 463개는 기존 C의 모델·face·slot 원장으로 연결하고, 나머지 35개는 `E_EXCEPTION`/`1-2-E` 소관으로 기록했다. C face에 연결된 PNG 249경로의 원본 SHA와 기존 RGBA 증거의 SHA를 확인했다. **4,480면·1,821슬롯·249 PNG는 C 선행 증거의 재참조**이고 D 신규 face·PNG 픽셀 측정은 0이다.

별도 재판정은 원본 snapshot 265개를 다시 파싱하고 정적 후보 1,804건 및 모델 옵션 3,976건의 조건·모델·명시 플래그와 값을 재계산했다. 모델 498개의 원본/C 범위 SHA 및 E 소관을 별도로 대조했다. **불일치 0.** `scripts/phase_1_2_d_entry4.py`와 `scripts/phase_1_2_d_entry4_recheck.py`로 재현할 수 있다. 기계판독 원장은 `D_ENTRY4_265_*`, 파일별 SHA/행수는 `D_ENTRY4_265_MANIFEST.json`에 있다.

**게이트:** D1 고정 1,168·6회 배정 유지. D2~D4는 **실조사 638경로 한정 PASS**, 전체 분모에 대해서는 진행 중. D5 최종 독립·원격 감사 대기. 공식 배포 JAR 인증, 게임 내 상태 레지스트리·런타임 렌더/UV 회전, E 특수 렌더 해석은 수행하지 않았다. A/B/C·v69 원장, C `heavy_core` 6면 정정, E 86개, 1-1 승인 150/150, 상위 완료 1/5는 보존한다.
