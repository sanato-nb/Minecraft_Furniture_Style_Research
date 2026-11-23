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

## 후속 실제 게임 실패 원인 확정과 수정 이력

- 첫 검증 [Actions #45194656949](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45194656949): 새 `/` 직접 입력 경로가 두 버전 모두 실패. 실패 시 성공 처리하지 않았고 원래의 `t` 채팅 경로로 철회.
- 후속 검증에서 Xvfb에 창 관리자가 없으므로 `xdotool windowactivate --sync`가 실제 오류를 내는 것을 확인. 호출 제거, `windowfocus --sync`만 사용.
- 추가 실패 [Actions #45196094545](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45196094545): Minecraft 1.21.11 Job은 실제 F2 **SUCCESS**, 반면 1.21.1 Job은 관전자 명령 응답 확인 실패.
- 실패한 1.21.1 [원본 진단 아티팩트 #14827219188](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45196094545/artifacts/14827219188)에서 `client.log`와 `INT3_GUI_DIAGNOSTIC_SPECTATOR_ACK_FAILURE.png`를 직접 열었다. 게임 세계와 렌더는 정상 로딩됐으며 **`<RenderAudit> t/gamemode spectator`** 라는 채팅 메시지가 서버 로그에 존재했다. 따라서 채팅창이 이미 열린 순간 다시 입력한 `t`가 실제 명령 앞에 문자로 들어가는 구체적 오류 사례가 증명됐다. X11 포커스 또는 모델 오류라고 일반화하지 않는다.
- 해결: 기존 `t` 채팅 경로 뒤에 `Ctrl+A`로 남은 채팅 텍스트를 선택하고 전체 명령(`/...`)을 교체한다. 관전자 모드와 각 teleport는 **새 서버 로그 응답 필수**, 한 번의 제한적 재시도만 허용한다. 원본 블록/모델·UV/F2 의미 승인 범위는 변경하지 않았다.

## 최종 실제 GitHub Actions 결과 — 검증 완료

- 최종 소스·테스트 커밋: `39fa6fade8145392ea759fa18a683695c17179aa`
- [INT-3 실제 Fabric Actions #45196779470](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45196779470): **run 전체 SUCCESS**. 두 Job 모두 모든 단계 성공.
- Minecraft **1.21.1** Job `137769220321`: 모델 `AF121 / AF123 / HC11210`, 서버 원본 상태 **12/12**, 네이티브 1024×684 F2 **12장**.
- Minecraft **1.21.11** Job `137769220833`: Macaw `MACAW67`, 서버 원본 상태 **4/4**, 네이티브 F2 **4장**.
- 원본 아티팩트 `1.21.1` [#14829036761](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45196779470/artifacts/14829036761): ZIP SHA256 `da4d2c20dc83f4669364b510d1e6d64aeb709897d5eeec47fd7558b0c36a5c80`.
- 원본 아티팩트 `1.21.11` [#14829920096](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45196779470/artifacts/14829920096): ZIP SHA256 `fa69746d712dd2c6314a58ef9a5cd06fa502609d8d1a3aad4e087130bee2a358`.
- **두 아티팩트 직접 다운로드·ZIP CRC 통과**. 매니페스트가 보고한 원본 F2 **16개 SHA256과 실제 PNG 바이트 16/16 일치**, 서버 상태 확인 **16/16 true**, `human_verified_roles=0`, `copyright_or_ai_training_approved=0`. 정적 모델 의미/저작권/원본 텍셀별 GPU 인과 미승인을 유지한다.
- 별도 [Draft PR #91](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/91)은 다른 H12 병렬 브랜치이고, 본 PR은 #90에서 분기한 별도 H13이다.
- 본 H13의 작업으로 변경한 것은 카메라 GUI 명령 입력·검증, 해당 회귀시험과 CI 연결 및 연구 보고서뿐이다. 기존 H12의 808픽셀·UV 두 면 후보 및 원본 게임 증거를 덮어쓰지 않는다.

## 범위 한정 결론

**INT-3 의자 F2 촬영 카메라 타임아웃은 최종 실행에서 재현되지 않고 원본 촬영 16/16 통과했다.** 그렇지만 H03 **HOLD**, H05 **CONDITIONAL**, F70 **70/70 조건부·무조건 0/70**, H 전체 무조건 종료 0, INT5 의미 및 INT6 학습/재배포권 승인 0이라는 심사 경계는 기존 그대로다. 게임플레이 수면·파괴·아이템 조작 전체 시험을 모델링 최종 종료조건으로 추가하지 않는다.
