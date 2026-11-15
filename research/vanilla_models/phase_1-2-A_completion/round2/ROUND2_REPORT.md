# Minecraft Java 1.21.11 — 1-2-A 고정계획 제2회차 실제 증거 통합

> 2026-11-15 KST | 시작 `main`: `6854f468926e23c7ead3b6f6ccd4a860960e929a` | 이전 연구 체크포인트 **v69 (그대로)**.
>
> 본 연구는 `1-2-A_FIXED_SCOPE_AND_EXIT_PLAN.md`의 **2/3회차**. 기존 모델군 기하·UV·PNG 연구를 새로 하지 않았다. **단계 1-2-A 자체는 G5 미실행으로 아직 미완료**.

## G2 — 역사 파일194·이후 체크포인트26의 source-level 근거 영역 분류 완료

v65 `00_HISTORY_194_FILE_AUDIT_LEDGER.csv`와 1회차 SHA/파일 크기 인덱스를 시작으로, 기존 v62~v65의 **원본 내용을 실제로 읽고 SHA 확인해 둔 증거 파일**들을 *새로 직접 열어* 원문 증거의 헤더, Markdown 선택 인용행, JSON 키, Python source lines, SQLite 정적 schema를 파일별로 연결했다.

- **194/194 역사 파일**: 원본 Git SHA와 증거 파일 원문 메타데이터가 연결됨. CSV 137, Markdown30, JSON19, Python4, SQLite4. 전부 `asset path+Git blob SHA`, 원래 형식, 기존 소스 검토 증거 경로, **실제 원본 헤더/원문 발췌에 근거한 기여 분야**로 기록.
- 처음 기여 분야가 불명확했던 **3개 원본**(`v6/06_v6_검증보류항목.csv`, `v6/README.md`, `v8/04_v8_17모델_유형요약.csv`)은 **실제 본문을 새로 직접 열고 SHA 대조**하여 unresolved issue register, 자료 묶음/검증한계 설명, 당시의 17모델 유형 요약으로 분류. 이 세 문서는 과거 연구 주장을 현재 모든 모델에서 재인증한 것이 아니다.
- 과거 증거 모델-파일 링크 **2,044쌍**은 원본 path+SHA 같은 행 일치로 기존 목록에서 통합; 이 안에는 **전체 모델을 식별하는 대량 인벤토리 3개**도 포함. **인벤토리 연결을 기하·PNG 의미론 증거로 승격하지 않는다**.
- 194개 파일에서 자료 유형·분야의 **등록/출처 확인은 완료**했지만, 과거 보고서에 적힌 **모든 기하·UV·픽셀·엔진 주장 자체의 전수 재실험은 하지 않았다**.
- v44~v69 **26/26 개별 `SUMMARY.json` 원본 내용 직접 재열람 및 Git SHA 확인**. 원본 `REPORT.md`의 존재·SHA는 Git tree에서 **26/26** 확인했지만, **본문 26개를 이번 회차에 모두 재열람한 것은 아니다**. 각 버전별 `SUMMARY`의 실제 키·스키마·focus로 범위를 태그했다. 이전 v62/v65 보고서 등 일부 원문 보고서는 기존 작업에서 별도 열람됨.

결과: `A_HISTORY_194_EVIDENCE_CROSSWALK.csv`, `A_CHECKPOINT_26_EVIDENCE_CROSSWALK.csv`, `G2_HISTORY_194_EVIDENCE_CLASSIFICATION_AUDIT.json`, `G2_CHECKPOINT_26_AUDIT.json`.

**G2 판정: PASS (파일별 source provenance·기여 영역 분류의 1-2-A 계약 범위).** 후속 개별 모델의 모든 역사 주장을 인증했다는 의미가 아니며 미인증 분야는 아래 후속 단계로 분기한다.

## G3 — P1 544개 출처·증거 등급·미검증 상태표

기존 v69 `07_P1_544_EVIDENCE_LEDGER.csv` **544행 × 393열**, `04_SOURCE_REVIEW_LEDGER_544.csv` **544행 × 70열**을 그대로 참조(원본 변경하지 않음). 1회차 원본 4,669 자산 원장/v34 P1·P2·P3 원장과 **모든 544개 정확한 source path+SHA**를 대조했고, v66 누적 `원본 JSON 직접 판독` 플래그 **544/544 true**를 기록. 이는 누적 과거 출처 이력, **이번 회차 직접 JSON 신규 판독0**.

P1 각 행에는 original-source 경로·SHA·P1 그룹·history provenance / bulk inventory 여부, direct-original-JSON, computed implicitUV candidate **엔진 미인증**, 원본 PNG 과거 근거 존재 여부, 비공식 2차 렌더러 증거와 원본 예외 상태, 미완료 이유, B~G 후속 owner를 구분했다.

- 모델 원본 경로 **544개**, 고유 Git blob SHA **539개**. 동일 SHA 재사용 **2그룹/7개 경로**를 합치거나 중복 모델로 삭제하지 않음.
- 이력의 **인벤토리 제외 비인벤토리 모델-파일 근거 연결 941쌍**은 고유 모델 개수나 새 기하 검증 수량이 아님.
- 누적 원장의 플래그만으로 후보가 존재하는 모델 **암시 UV 계산 후보189개**, 특수/기하 없음 근거에 따른 **E 단계 보수적 분기30개**, 과거 PNG 관련 근거가 기록된 모델232개. 이 수치들은 **이번 회차 새 분석 실적 0**, 서로 다른 증거 필드의 후속 검토 힌트이며 B~E 전체 인증 결과가 아니다.
- 원본 `JSON`에 elements가 없다는 사실은 월드에서 모델이 없다는 뜻이 아니다. `v68` 비공식 Java 소스의 렌더러 5사례는 **secondary**로 보존하고 공식 Mojang 런타임 인증으로 승격하지 않음.

결과 `A_P1_544_SOURCE_STATUS.csv`. **G3 PASS (544/544 source identification + evidence-grade status and unknowns).**

## G4 — P2/P3 1,846 + P1 544의 유한한 후속 분기

v34 원본 우선도 계층을 그대로 사용: **P1 544, P2 1,039, P3 807** = 전체 모델 **2,390/2,390**. 모델별 path/SHA와 이전 단계 분석 여부·다음 primary owner·후속 의존단계를 명시한 `A_TO_BCDEFG_HANDOFF_QUEUE_2390.csv` 작성.

- P1 **544/544**: 기존 원본 소스 기하·특수렌더러 예외 근거에 따라 우선 `1-2-B` 또는 `1-2-E` 배정. C(명시/암시 UV·PNG), D(blockstates), F(원형·스타일), G(독립 검수) 등이 뒤따른다는 **계획**이지 모두 검증했음을 뜻하지 않는다.
- P2/P3 **1,846/1,846**: 우선순위·그룹·원본 SHA·**P1 부모 의존성 검토 상태 미확인** 명기, `1-2-B` 소관으로 넘김. P2/P3 전체를 geometry/UV 검증 완료로 처리하거나 P1과 의존성이 없다고 단정하지 않는다.
- 미검증/후속 사항을 **2390개 모델별 owner**로 `A_UNRESOLVED.csv`에 등록, 이전 이력 오류/공식 렌더러 인증 등 공통 이슈3개도 별도 소관 표시. 모델 2,390 중 담당 단계가 비어 있는 항목 **0개**.
- 기존 v62의 `v44` 과거 증거 CSV SHA 끝 글자 누락 **6링크**는 이전 보고서 교정 근거를 인용만 함. 새 발견으로 중복계산 또는 구버전 CSV 덮어쓰기 금지.

결과 `A_TO_BCDEFG_HANDOFF_QUEUE_2390.csv`, `A_UNRESOLVED.csv`. **G4 PASS (범위·담당 단계 및 미확인 상태 기록).** 부모 의존성 1,846개 실제 구조 전수 비교가 통과했다는 뜻은 아니다.

## 현재 엄격 판정과 제3회차

| Gate | 판정 |
|---|---|
| G1 | **PASS (1회차 계승):** typed source 4,669/4,669 Git tree SHA |
| G2 | **PASS (source provenance/evidence-domain):** 역사194·현대26; 본문 전체 주장 진위 검증이 아님 |
| G3 | **PASS (P1 status):** 544/544 source identity + evidence grades, unknowns explicit |
| G4 | **PASS (scope/handoff):** P2/P3 1846, P1 544, 총2390 owner 지정 |
| **G5** | **PENDING — 3회차 독립 종료감사** |

**1-2-A는 아직 완료 아님. 3회차에서 G1~G4 원장별 경로·SHA·행·근거 참조·기존 v69 P1 393열 데이터 비변경, 1회차 자료 비변경, 대표 표본 원본과 맞춤 검사 후 완료 또는 `A_BLOCKED`를 판정**한다. 고정 계약에 따라 3회차가 마지막이며 자동 4회차 없음.

1-1 승인 150/150, 상위 5개 세부연구 중1개 완료 상태 그대로. Minecraft 가구 모델 제작과 Project Zomboid 변환 미착수.
