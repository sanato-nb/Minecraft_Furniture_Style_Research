# 1-2-G Entry2 — 원본 775개 실제 교차 감사 및 독립 검산 보고서

**2026-11-17 · Minecraft Java 1.21.11 사용자 추출 원본 · Entry1 승인 기준 HEAD `ae1448906d4cb6f2aff4bdc43fbdc808024fd6bb`.**

**게이트 검증: 775개 원본·SHA·상속·face·상태 조건·PNG 픽셀 증거 PASS.** 56개 원본 소스 배치와 주요 원장 원격 SHA/행수 사전 readback도 PASS. 최종 승인 표시는 HANDOFF/STATE 및 최종 readback 저장 후 확정하고, 그 전에는 Entry3 실작업을 수행하지 않는다.

## 새로 직접 수행한 원본 감사

| 대상 | 최초 고정 큐 | 직접 원본 본문 | 독립 검산 |
|---|---:|---:|---|
| 블록 model JSON | 494 | **494/494** | Git blob SHA-1/구문/상속 체인, 기하 및 C/F 재집계 PASS |
| blockstate JSON | 96 | **96/96** | Git SHA, variants/multipart 조건·apply 원문 809옵션 PASS |
| 블록 텍스처 PNG | 185 | **185/185** | Base64 원본 bytes, PNG 시그니처·chunk CRC32·zlib Adler32·전체 RGBA SHA256 PASS |
| **합계** | **775** | **775/775** | **원본 SHA 불일치 0 / 비교 오류 0** |

모델 494개에 필요한 **Entry2 큐 외부 조상 JSON 16개** 역시 별도 바이너리/원문 Git SHA로 직접 검증했다. 이는 상속 재계산의 보조 자료이며 G의 고정 775개 또는 전체 4,669개 분모에 **중복 산입하지 않았다**. 소스 775개의 원문과 Git SHA 및 구조 메타데이터는 `source_batches/` 56개 체크포인트와 `rollup/` 4개 독립 집계에 보존했다. 선행 자료만 엮은 `references/` 8개 분할 참조 원장은 G 직접 검증 실적으로 계산하지 않는다.

## 모델 상속·기하·face 검산

- 일반 모델 **447개**, E 소관 특수 렌더 예외 **47개**. E는 소스 JSON에 일반 geometry가 없어 실제 renderer 인증으로 승격시키지 않았다.
- 직접 확보한 모델/부모 본문을 잇는 부모 체인 및 기하 제공자를 전수 재계산했고 F·C의 모델별 경로/원본 SHA/element·face·UV/바인딩 계수 불일치 **0개**.
- 실제 적용 기하 **1,944 elements**, **7,131 faces**; UV 키 명시 **5,986** / 키 없음 **1,145**; 텍스처 소스 결합 **6,884 faces** / 템플릿 슬롯 미바인딩 **247 faces**.
- 개별 원본 face의 요소 번호·방향·`texture`/상속/별칭·UV 키 여부·`cullface`/`tintindex`를 보존한 `face_shards/` **7,131행** 저장. 분할은 2,187 + 1,518 + 2,024 + 1,402; 각 SHA·행수·실제 원격 본문 재조회 PASS.
- 미바인딩 247면에 임의 PNG 경로나 물질 의미를 붙이지 않는다.

## D blockstate 정적 조립 규칙 검산

- 원본 blockstate 96개에서 실제 선택 **809옵션** = variants **694** + multipart **115**; 참조 고유 모델 경로 **211개**.
- 원본 variants 키, multipart `when`의 중첩 조건 JSON, `apply` 전체 JSON, 선택 배열의 대안 수·인덱스, `x/y/uvlock/weight` 명시 여부 및 값을 선행 D 규칙 809행과 독립 비교 **0차이**.
- 참조 모델 211개는 D/C 원장에 source path/SHA가 존재하며, **이번 Entry2에 직접 열지 않은 대상 모델을 신규 G 모델 원본 직접 열람으로 계산하지 않았다**.
- 실제 게임의 등록 state space나 엔진 렌더 결과까지 인증하지 않는다.

## PNG·F 스타일 증거·애니메이션

- PNG **185개**, 원본 파일 크기 총 **39,276 bytes**. 직접 Git blob SHA와 파일 SHA256, PNG 압축/CRC 및 풀 RGBA 픽셀 SHA256 검증 PASS.
- 선행 C 1,073개 검증 집합과 겹치는 **171종은 원본 RGBA·치수·모드·알파 통계 모두 재대조 일치**, 나머지 **14종은 G 신규 직접 실증이지만 C 과거 수량에 소급 포함하지 않음**.
- 이번 PNG 중 과거 F에서 시각 관찰한 **45종**의 근거를 연결했다. 이는 G 신규 개별 외형·정체/재질 육안 인증이 아니라 F의 선행 근거다.
- `.mcmeta` 원본 **11/11** JSON·SHA 대조. 애니메이션 메타데이터 **6종**의 정적 프레임 및 시간 설정 확인. 실제 게임 재생, 동적 보간, 전 프레임 육안 검수는 하지 않았다.

## 미결정·예외를 삭제하지 않고 구분

`G_UNRESOLVED.csv` **98행**: E 특수 renderer **47모델**, C 선행 검증 집합 밖 PNG **14종**, 템플릿 미바인딩 face 관련 모델 **36개(총 247 faces)**, F 선행 시각 증거와 G 신규 이미지 픽셀 검증의 등급 차이 **1행**. 위 항목은 중복 소관과 범위 제한을 표시한 것으로 PNG 파손이나 Git SHA 불일치 98건을 의미하지 않는다. 운영 중 게임 특수 렌더 검증 및 물체 정체 확정은 범위 밖이다.

## 재현/검산·원격 증거

- 실행 코드: `G_ENTRY2_SOURCE_AUDITOR.js`, `G_ENTRY2_INDEPENDENT_AUDITOR.js`, `G_ENTRY2_FACE_LINK_AUDITOR.js`; PNG 바이너리 디코더는 **Entry1 검증기를 재사용**.
- 원장: `G_SOURCE_CROSSWALK.csv` **775행**, `G_ENTRY2_MODEL_GEOMETRY_RECOUNT.csv` **494행**, `G_ENTRY2_D_RULE_MODEL_LINKS.csv` **809행**, `G_ENTRY2_PNG_BINARY_AUDIT.csv` **185행**, `G_UNRESOLVED.csv` **98행**.
- 검증: `G_ENTRY2_INDEPENDENT_AUDIT.json`, `G_ENTRY2_D_CONDITION_INDEPENDENT_AUDIT.json`, `G_ENTRY2_PNG_MCMETA_AUDIT.json`, `G_ENTRY2_FACE_SHARD_MANIFEST.json`, `G_ENTRY2_PRE_CLOSEOUT_REMOTE_READBACK.json`.
- 모든 56 원본 배치의 Git SHA·행수·본문을 다시 열어 `remote_batch_readback/` 4개 파일로 독립 기록. 주요 13개 원격 대상의 SHA·본문/행수 및 원본 A~F/v69 보호 파일 diff 사전 검증 PASS. 최종 승인 readback 파일은 `G_ENTRY2_REMOTE_READBACK.json`에 별도 기록한다.

## 상태 경계

Entry1 **347/347** 원본 검증은 그대로 유지. Entry2 **775/775** 직접 원본 재검수로 G 누적 **1,122 / 4,669 (약 24.03%)**. 승인 Entry는 종료 확인 뒤 **2/6**; 다음 Entry3 고정 큐는 **945자산 = 모델495 + blockstate265 + PNG185**. 전역 G1~G6 종료 게이트는 계속 **0/6**, 전체 G 및 상위 1-2 완료 선언 금지, Entry7 없음. A~F·v69 원본, 기존 승인150/150 및 상위 완료1/5 보존. **공식 게임 배포 JAR, 런타임 state/renderer, 물리 재질·좀보이드 가구 정체·실제 맵 변환은 미인증**.
