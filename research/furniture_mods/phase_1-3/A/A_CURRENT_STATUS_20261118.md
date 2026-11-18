# 1-3 현재 상태 및 원장 재검산 — 2026-11-18

확인 기준 main: `f8956d960b2a9e6d5dcde6b2732ce643318bcfb0` (2026-11-18 12:55:17 KST).

## 현재 판정

요청문의 “A 미착수·0/7”은 과거 상태다. 현행 `handoff/STATE.json`, `A_REPORT.md`, `A_INDEPENDENT_AUDIT.json`은 **A 선행 증거 재정합 완료, 7/7 PASS**로 일치한다. 현재 실제 진행 단계는 **1-3-B**, 전체 B는 Macaw 공식 원본 미확보로 미완료다. **상위 1-3 M1~M6는 0/6**이다.

계획서 및 두 PLAN/ACCEPTANCE 계약의 미착수 상태 필드는 계획 수립 당시 스냅샷으로 남아 있다. 종료 실적의 정본은 실행 원장·감사·현행 STATE이며 계획 문서의 과거 상태를 현재 미착수로 해석하지 않는다. 이 확인에서는 기존 계획·원장·보고서를 수정하지 않았다.

## 이번에 실제 수행한 검사

- v11~v24 14개 버전의 **195파일, 5,321,808바이트**를 기존 manifest의 크기·Git blob SHA와 재대조했다. 불일치 0.
- Another 기존 leaf **33+38+43+51+39=204**의 경로 고유성, 선행 원장 SHA와 A 원장 SHA, 부모 선언 연결을 CSV 파서로 재검산했다. 중복·연결 불일치 0.
- A 상태22의 적용1,188건, 템플릿69 및 v18 부분집합30, 의자39의 부모19/20·상속390요소/1,794면 인스턴스를 별도 재집계했다.
- Handcrafted 선행 authored120/generated leaf16 및 PNG·RGBA·Macaw 이력 레코드를 분리했다.
- B 인벤토리 및 직접검증 증거를 재파싱해 두 모드 모델14,023경로, 상태444경로, 회차109개와 모델 경로 중복0을 확인했다.
- A 상태22와 B 상태155의 고유 합집합177, B Handcrafted authored121/generated16의 원장 간 SHA 일치를 확인했다.

이 검사는 **연구 저장소 파일 bytes와 저장된 출처·SHA 증거의 재집계**다. 이번 회차에 원저자 JSON 297개 또는 587개를 다시 다운로드·재해시하지 않았다. 원저자 신규 bytes 확인0, 신규 모델 발견0이다. 기존 원본 검증 수치는 이전 A/B의 직접검증 증거로 계승한다.

재현 코드: `recheck_current_snapshot.py`. 입력별 Git blob SHA·크기·CSV 행수와 결과: `A_CURRENT_SNAPSHOT_RECHECK_20261118.json`. 재검산 오류0, PASS.

## 최신 B 범위와 잔여

| 대상 | 고정 Git 파일 경로 수 | 기존 직접 원본 검증 증거 | 원문 미검사 잔여 |
|---|---:|---:|---:|
| Another 모델 JSON | 1,629 | 273 (leaf204+template69) | 1,356 |
| Another 상태 JSON | 177 | 177 (A22+B155) | 0 |
| Handcrafted authored 모델 JSON | 121 | 121 | 0 |
| Handcrafted generated 모델 JSON | 12,273 | 16 | 12,257 |
| Handcrafted 상태 JSON | 267 | 0 | 267 |
| Macaw 공식 JAR·내부 모델 | 미확정 | 0 | 원본 확보 차단 |

전체 모델14,023은 **두 모드의 block+item JSON 경로 수**다. 고유 가구 형태 수·3모드 전체 모집단·기하/상태 분석 완료 수가 아니다. A+B 고유 원본 JSON 직접검증 기존 증거587은 모델410+상태177이며, 코드3파일은 별도다.

Another 상태177 원본을 검사했어도 상태 동작·게임 렌더 승인을 뜻하지 않는다. `unused/white_awning.json`의 `another_furniture:block/awning/white_double` 참조 누락1건과 기존 birch/spruce 의자 상태 참조 예외2건을 보존한다. `unused`의 게임 사용 여부는 미확인이다.

## 다음 작업

현행 `../B/B_NEXT.md`를 따른다. Macaw 공식 JAR·라이선스·SHA 확보, Handcrafted generated12,257 및 상태267 원문 검사, Another 나머지 모델1,356의 원문·부모·기하 검사다. A를 재시작하거나 과거 A_NEXT의 상태155 잔여를 현재 미검사로 되돌리지 않는다. B 회차의 source SHA 확인은 C/D 기하·동작 승인과 구분한다.

이번 변경은 이 경로의 신규 확인서·검산 JSON·재현 코드로 제한한다. 기존 v11~v24·1-1·1-2·A/B 원장과 인수인계 상태는 보존한다. 실제 가구 제작·실게임 렌더·좀보이드 맵 변환 완료를 주장하지 않는다.
