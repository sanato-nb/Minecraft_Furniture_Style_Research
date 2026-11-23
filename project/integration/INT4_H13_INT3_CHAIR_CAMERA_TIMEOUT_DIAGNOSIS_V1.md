# INT-4-H13 — INT-3 원본 의자 F2 카메라 명령 확인 실패 복구

## 고정 원본과 병렬 PR 확인

- 기준: [H12 Draft PR #90](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/90), head `811d7c48d981cc2e88af71fabf859d8b957014d9`. 본 H13 브랜치는 해당 커밋에서 분기하며 H12를 base로 사용한다.
- 별도 [Draft PR #91](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/91)은 H11에서 분기한 **병렬 H12** 연구다. #90의 직계 후속 커밋이 아니므로 이곳에 무단 혼합하지 않는다.
- `main`은 변경하거나 병합하지 않는다. 기존 원본 F2·모드 JAR·PNG·게임 로그 파일 자체를 Git에 복제하지 않는다.

## 이전 실행의 직접 확인된 장애

- [INT-3 실패 Actions #45184559435](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45184559435), 커밋 `811d7c48...`.
- Minecraft Java 1.21.1 Job `137726676538` SUCCESS, Minecraft Java 1.21.11 Job `137726677289` FAILURE.
- 실패 작업: `Execute real Minecraft Fabric GUI and capture every server-verified source chair`, 오류 `Timed out waiting for original-source chair camera teleport`.
- 실패한 1.21.11의 [원본 아티팩트 #14822923115](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45184559435/artifacts/14822923115)를 다운로드해 `client.log`를 직접 확인했다. 통합 서버는 정상 시작했고 `RenderAudit joined the game`이 있었으나, 그 뒤 `[RenderAudit: Teleported RenderAudit to...` 카메라 완료 로그는 없었다. 따라서 **현재 증거로는 명령이 전달되지 않았는지, 전달됐지만 로그 확인이 누락됐는지 완전히 분리할 수 없다.**
- 별도 PR #91의 [INT-3 성공 실행 #45189062019](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45189062019)도 확인했으므로 지속적인 원본 의자 모델 오류로 승격하지 않는다. 동일 경로가 항상 성공한다는 결론 역시 내리지 않는다.

## 최소 코드 변경

1. 기본 키 `t`로 채팅을 열고 전체 문자열을 주입하던 방식을 기본 Minecraft의 `/` 직접 명령 입력으로 바꾼다. 기존 명령 자체·가구 블록상태·좌표·촬영 순서는 유지한다.
2. 매 카메라 명령 직전 **실제 Minecraft 창 포커스를 재확인**한다.
3. 서버 teleport 완료 문자열을 **해당 시도 이후 새 로그에서만** 확인한다. 25초 미확인 시 새 포커스에서 **단 한 번 재시도**(35초 제한)하며 그 후에도 확인되지 않으면 실패를 유지한다. 무한 timeout 증가 또는 무증거 성공 처리 없음.
4. 명령 열기, 구 로그 재사용 불가, 1회 재시도, 2회 실패, 프로세스 조기 종료를 별도 단위 회귀시험으로 검증한다.
5. CI에서 기존 정적/실게임/출처·F2 승인 분리를 유지하고 신규 단위시험을 실행한다.

## 연구 승인 및 증거 분리

- 이 변경은 **촬영 인프라의 재현성 회복 시도**다. 성공하더라도 GPU 개별 face/UV→픽셀 인과, 가구 의미, 제작자 의도, AI 학습 및 원본 자산 재배포 허가의 증거가 되지 않는다.
- 기존 INT-4 H 전체 8개 게이트: **범위 통과 6 / CONDITIONAL 1(H05) / HOLD 1(H03)**.
- F70 원본 사례 **70/70 조건부**, F70 무조건 최종 승인 **0/70**, INT-4 무조건 종료 **0**, INT5 의미 승인 **0**, INT6 권리 승인 **0** 유지.
- 수면·앉기·파괴 등 게임플레이 연속 행동은 모델링 필수 조건에 추가하지 않는다.

## 후속 실행 기록

본 파일 작성 시점에는 신규 브랜치의 실제 Minecraft Actions 재검증 결과가 **아직 확보되지 않았다**. 신규 실행이 완료되면 run ID·head SHA·각 버전 Job 상태·원본 아티팩트와 승인 범위를 별도로 갱신한다.
