# 1-2-E 보완 — 바닐라 클라이언트 특수 렌더 검증

2026-11-19 · Minecraft Java 1.21.11. 고정 예외 86개를 원장으로 사용하고, D 원본 블록 상태가 직접 선택하는 84개에 대해 모델별 대표 블록 상태 하나를 실제 테스트 월드에 배치했다. 버전 메타데이터의 SHA-1과 일치하는 원본 클라이언트를 사용했다. 리소스팩은 바닐라, 렌더링은 OpenGL 4.5 Mesa llvmpipe, 화면은 빈 손의 관전자 카메라 기준이다.

| 실제 검증 | 결과 |
|---|---:|
| 대표 블록 상태 설치 후 인게임 `execute if block` 확인 | **84/84** |
| 실제 화면에서 표면이나 효과 관찰 | **62개** |
| 정상 관전자 화면에서 보이는 표면 없음 | **19개** |
| 상단 상태는 있지만 별도 상단 표면 없음 | **3개** |
| 직접 선택되지 않는 공용 표시 템플릿 | **2개 적용 없음** |

표지판·현수막·침대·머리·셜커 상자·구리 상자·구리 골렘 조각상·항아리·도관·엔드 포털과 관문·물과 용암을 실제 화면에서 확인했다. `moving_piston`은 틱을 멈추고 전원을 넣어 한 틱씩 진행했다. 두 중간 화면에서 피스톤 머리가 이동했고, 두 시점 모두 인게임 블록 상태가 `moving_piston`으로 확인됐다.

관전자 화면에서 공기, 배리어, 구조물 공허, `light` 0–15는 독립적인 표면이 보이지 않았다. 이는 해당 화면 조건의 관찰이다. 창조 모드의 아이템별 안내 마커 표시와 광원 레벨의 밝기 비교는 별도다. 포충초 상단 0–2는 실제 상태를 확인하고 상단만 제거했다. 하단과 상단 영역을 포함하는 동일 카메라 영역 **305,100픽셀**에서 RGB 차이는 **0개**였다.

`block`과 `thin_block`은 D 원본 블록 상태에서 직접 선택하지 않는 표시 템플릿이다. 표에는 런타임 배치 대상에서 적용 없음으로 기록했다. 이번 실행은 모델별 대표 상태의 실제 화면과 배치를 확인한다. 모든 변형·아이템/GUI·리소스팩·내부 렌더러 클래스 호출 추적은 포함하지 않는다.

## 검증 자료

- [86개 결과 원장](E_RUNTIME_OUTCOMES_86.csv) · [배치 좌표와 상태](E_FIXTURE_PLAN_86.csv) · [상태 확인 로그](E_RUNTIME_LOG_EXCERPT.txt) · [집계](E_RUNTIME_SUMMARY.json)
- 실제 화면 [장면 00–02](evidence/scenes_00-02.jpg) · [03–05](evidence/scenes_03-05.jpg) · [06–08](evidence/scenes_06-08.jpg) · [09–11](evidence/scenes_09-11.jpg) · [12](evidence/scenes_12-12.jpg)
- 통제 실험 [피스톤 틱 변화](evidence/piston_ticks.jpg) · [포충초 상단 제거 비교](evidence/pitcher_crop_control.jpg)

## 재현

1. 1.21.11 바닐라 클라이언트에서 명령이 켜진 평지 싱글플레이 월드를 만든다.
2. 저장소 루트에서 `python research/vanilla_models/phase_1-2-E/followup/BUILD_FIXTURE.py --pack "/path/to/world/datapacks/render_audit" --plan /tmp/E_FIXTURE_PLAN_86.csv`를 실행한다.
3. 테스트 월드에서 `/reload`, `/function render_audit:platforms`를 실행한다. 청크가 로드된 뒤 `/function render_audit:place`, `/function render_audit:verify`를 실행한다.
4. 관전자 상태에서 각 장면의 Z값보다 7.5블록 앞의 `0.5 122.5` 위치로 이동한다. 회전은 yaw 0°, pitch 22°다. 화면 왼쪽부터 x 좌표 6, 4, 2, 0, −2, −4, −6이다.
5. 피스톤은 `6 121.5 116.5` 근처에서 북쪽을 향한 피스톤을 관찰한다. `/tick freeze` 후 `6 120 122`에 레드스톤 블록을 놓고 `/tick step 1`씩 진행하면서 `6 120 120` 위치의 상태를 확인한다. 실험이 끝나면 `/tick unfreeze`로 복귀한다.
