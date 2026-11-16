# 1-2-E Entry1 — E 우선 원본 모델 30개 직접 조사

**2026-11-16 KST · 시작 main `5ef795f4d0b24ae5535d6c9411a5f092ba35e6ac` · 사용자 제공 Minecraft Java 1.21.11 추출 원본.**

## 고정 범위와 이번 실적

C 고정 범위의 E 예외 **86개**(E-first 30 + B-first 일반 기하 부재 56)를 B Entry10의 경로·SHA 및 D 원본 1,168개 선택 참조와 대조했다. D가 직접 참조하는 E 고유 모델 **84개**, 참조하지 않는 모델 **`block.json`, `thin_block.json` 2개**도 E 범위에 남는다. 유한 **4 Entry**(모델 30/28/28/0·마지막 전체 감사) 배정을 [`E_FIXED_SCOPE_86.csv`](../E_FIXED_SCOPE_86.csv)에 고정했다. Entry5는 자동 생성하지 않는다.

이번 Entry1은 E-first P1 **30/30개 원본 모델 JSON 본문과 Git SHA**를 직접 확인했다. E 누적 직접 조사 **30/86**, 남은 **56**. 각각 원본에는 `parent`도 `elements`도 없고 `textures.particle`만 있다. 따라서 **모델 JSON의 일반 기하가 설명할 수 있는 형상은 0**이다. 이 사실만으로 block entity renderer의 실제 구현·움직임·표면 텍스처를 인증하지 않는다.

| 원본 근거 | 결과 |
|---|---:|
| 직접 판독한 E-first 모델 JSON·SHA | 30개 |
| 부모 키 / 자체 elements | 0 / 0 |
| `particle` 한 슬롯만 선언한 모델 | 30개 |
| 고유 particle PNG 원본 SHA·RGBA | 25개, 각 16×16, 총 6,400픽셀 |
| 기존 C RGBA 원장과 일치한 particle PNG | 8개 (기존 근거 재사용) |
| D 원본 blockstate의 모델 선택 참조 | 95건·95경로 |
| 실제 런타임 renderer 확인 | 0개 |

원본 snapshot, 모델별 SHA·particle 선언·D 연결, 고유 PNG SHA/RGBA는 `E_ENTRY1_ORIGINAL_30.json`과 `E_ENTRY1_*` 원장에 저장했다. D 참조는 고정 blockstate 원본을 다시 읽어 모델 참조를 재계산했다. 별도 검사기는 **모델 30개 본문/SHA, PNG 25개 SHA/RGBA, D 참조 95건**을 재계산해 불일치 0을 확인했다. 17개 PNG가 기존 C RGBA 원장에 없더라도 이 Entry의 새 조사는 **particle 자산의 기술적 검사**이며 렌더된 가구 표면·형상이나 C 신규 face 실적으로 세지 않는다.

과거 v57의 `09_SECONDARY_RENDERER_JAVA_EVIDENCE.json`에는 셜커/해골에 관한 **제3자 디컴파일 Java 자료**가 보조 근거로 등록돼 있다. 공식 클라이언트와 독립 인증되지 않았고 이번 Entry에서 그 구현을 재검증하지 않았다. 모든 30모델의 실제 renderer 경로는 `UNVERIFIED_RUNTIME_RENDERER`로 유지한다.

**게이트:** E1 분모·배정 PASS. E2 모델 원본은 첫 30개만 PASS, 나머지 56개 미조사. E3 증거 수준은 첫 30개에서 source-only 분류 완료·실제 렌더 미확인. E4 독립 최종·원격 종료 감사 PENDING. **E 전체 미완료.** A/B/C/D·v69 원본과 1-1 승인150/150, 상위 완료1/5를 보존한다.
