# 1-2-D Entry3 부분 실행 1 — 48개 원본 JSON 실조사 보고서

**2026-11-16 KST · 사용자 제공 Minecraft Java 1.21.11 추출 원본 · GitHub 시작 HEAD `9e5892f20c55f16d358a732ce908b45bb26e722a`.**

## 정확한 범위와 완료·미완료

기존 Entry2의 원격 검산과 보고서를 확인했으며, Entry1 12 + Entry2 96 = **108/1,168**은 선행 완료 상태 그대로이다. 이번 작업은 **Entry3 고정 265개 중 처음 48개**(`black_wool.json`~`brown_wool.json`)의 원본 JSON 본문을 새로 읽고 Git blob SHA/파싱을 **48/48 직접 검사**했다. 다음 원본은 **`bubble_column.json`(ENTRY3 대기표 49행)**이다.

Entry3 실제 새 조사 **48/265 (18.11%)**, Entry3 미조사 **217**. 전체 D 누적 **156/1,168 (13.36%)**, 전체 D 미조사 **1,012**. **Entry3 완료, 전체 D 완료, Entry4 시작을 주장하지 않는다.** 배정표·분모·6회 종료 계약 그대로 유지한다.

## 원본 상태·방향·uvlock 조사

원본 전문을 8개씩 6개 SHA 고정 JSON에 보존했고, `D_ENTRY3_SUBBATCH1_48_SOURCE_STATUS.csv`의 행별 원본 경로/SHA와 연결했다.

- `D_ENTRY3_SUBBATCH1_48_RULES.csv`: **213개 선택 모델 옵션 행**의 `variants` 키 또는 `multipart.when`, `apply` 배열 대안 인덱스, 모델 참조, `x`·`y`·`uvlock`·`weight` 키의 **명시 여부와 실제 값** 보존.
- `D_ENTRY3_SUBBATCH1_48_STATES.jsonl`: 원본의 `variants`별 선언 상태 및 `multipart` 조건값의 문법상 후보 **319개**, 모델 선택 옵션 **997행**. multipart는 동시 부품, 한 규칙 배열은 대안으로 구분. boolean 조건에서 반대값이 소스에 없을 때 생성한 반대 후보는 **분석용 파생값**이며 원본 속성 레지스트리를 인증한 것이 아니다.
- 6개 snapshot을 **별도 재파싱**하고 별개 조건 판정기로 **319/319 후보의 규칙·모델 순서·x/y/uvlock/weight 명시 플래그와 원본 값을 재계산**했으며 불일치0. 상태별 모델 옵션 997개 재계산 확인. 독립 감사: `D_ENTRY3_SUBBATCH1_48_INDEPENDENT_RECHECK.json`.
- 정적 후보가 실제 게임에 존재하는 모든 상태라고 확정하지 않는다. 특히 `wall` 연결 높이의 조건에 없는 값이나 특수 엔진 동작은 원본 blockstate 단독으로 인증할 수 없다.

## 기존 B/C 모델·면·텍스처 교차검산

상태 모델 참조의 **고유 모델 80/80**을 기존 C 최종 원장 경로/Git blob SHA에 연결했다. C 직접 모델 **76개**, E 소관 특수 렌더 **4개**(`banner`, `bed`, `blue_shulker_box`, `brown_shulker_box`)는 일반 기하나 실제 렌더를 임의 확정하지 않고 `D_ENTRY3_SUBBATCH1_48_E_MODEL_REFERRALS.csv`로 분리했다.

기존 C의 **고유 직접 모델별 선행 786 face = PNG 연결786 + 템플릿 미바인딩0**, 기존 `TEXTURE_BINDINGS.csv` 슬롯 **313/313행** 경로·SHA 일치. C PNG 원장에 대응하는 고유 PNG **41경로**의 기존 Git SHA/RGBA SHA를 재사용했다. 이 모두는 **C 선행 작업의 재사용**, D 신규 face·PNG 픽셀 측정 **0**. `heavy_core` 정정6면 및 기존 C 23,090face·고유 PNG1,073의 전체 기준은 훼손하지 않는다.

`D_ENTRY3_SUBBATCH1_48_MODEL_BC_CROSSWALK.csv`, `D_ENTRY3_SUBBATCH1_48_TEXTURE_C_LINKS.csv`, `D_ENTRY3_SUBBATCH1_48_STATE_MODEL_BC_LINKS.csv`에 source 경로/SHA, 선행 B/C 증거 위치를 연결했다. 이 48개에서 모델 경로 미연결0, 슬롯 SHA 불일치0, C PNG 미연결0.

## 완료 게이트와 미검증

- **D1** 1,168경로와 6개 Entry 배정 PASS(기존 검사 재사용), 고정 계약 불변.
- **D2~D4** 이번 Entry3의 처음 48개만 원본 및 정적 조립·B/C 출처 연결 PASS. 나머지 Entry3 217개를 포함한 D 전체는 미완료.
- **D5** 마지막 Entry6의 독립 종합감사 PENDING. 개별 원격 readback은 별도 감사로 기록할 것.
- 공식 배포 JAR 인증, 실제 Minecraft 게임 내 렌더/UV 회전 실측, block property registry 확인, 특수 렌더 E 실제 해석, 모델 제작, TMX→마크 변환 **미실행**.
- 기존 A/B/C/v69 원본·원장, 승인150/150·상위단계1/5, E 원형 예외86은 보존.

**다음:** 같은 고정 Entry3의 49~265행 **217개 원본 JSON**을 조사한다. Entry3 작업이 끝나고 자체 게이트를 통과하기 전 ENTRY4로 넘어가지 않는다. ENTRY7 없음.
