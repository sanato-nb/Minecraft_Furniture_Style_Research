# INT-4 — Macaw 연결형 테이블의 실제 블록 주변 갱신 실험

## 목적과 출처

본 연구는 이전 [PR #43](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/43)의 Macaw 원본 선택 상태 S18(동·서·남·북 모두 false, single 모델, 6요소·31면)과 S19(네 방향 모두 true, center 모델, 1요소·6면)를 **블록상태 원본으로 사용**한다. PR #43은 임의 상태를 `/setblock`으로 강제한 후의 모델 외관을 확인한 반면, 이번에는 **이웃 블록의 설치/제거가 실제 런타임 블록상태를 바꾸는지**를 조사한다.

- 고정 게임: Minecraft 1.21.11 / Fabric, Macaw's Furniture 3.4.2 원본 JAR SHA-256 `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e`.
- 연구 원본: `research/furniture_mods/phase_1-5/B/APPLICATIONS.csv`, PR #41 원본 15사례 재검증 체크포인트, S18·S19 원본 모델 및 블록상태 SHA를 다시 검증한다.
- 사용자 Minecraft 월드나 모드 바이너리 수정 없이 공식 Mojang 서버에서 새 임시 평지 월드를 생성한다.

## 실제 서버 실험 시나리오

좌표 `centre=(0,120,40)`, `east=(1,120,40)`:

| 순서 | 게임 내 실행 | 관측/증거 |
|---|---|---|
| reset | 기존 영역을 비우고 중앙 `mcwfurnitures:oak_table` 하나를 일반 기본 상태로 설정 | 중앙 east/west/north/south, 동쪽 공기 여부 |
| join | 바로 동쪽에 `mcwfurnitures:oak_table`을 추가 | 양쪽 중앙 east, 동쪽 west 및 다른 방향 속성 |
| remove | 동쪽 테이블을 `minecraft:air`로 제거 | 중앙 east가 다시 변하는지와 동쪽 공기 여부 |

각 단계에 게임 서버 `/execute if block`을 사용해 실제 결과를 기록한다. True/False가 모두 나오거나 어느 쪽도 나오지 않으면 오류로 기록한다. 연결이 안 된 결과도 관측값으로 남기며 **연결됐다고 임의로 통과시키지 않는다**.

각 단계에 같은 카메라로 실제 Minecraft F2 PNG를 촬영하고 SHA-256·클라이언트 로그·화면을 Actions 아티팩트에 보관한다.

## 검증의 범위

- 이 실험의 `/setblock`은 원본 Minecraft 블록 배치 및 이웃 업데이트 코드를 실행한다. 하지만 **플레이어가 아이템을 들고 클릭하여 놓는 동작은 시험하지 않는다**.
- 결과가 `east=true`와 `west=true`로 변화해도 플레이어 수동 아이템 배치나 Minecraft 모드의 모든 테이블·책장·침대의 일반 규칙으로 확대할 수 없다.
- 동쪽 테이블이 원본에서 실제로 연결하지 않는다면 그 사실을 *관측 실패가 아닌 부정 결과*로 기록한다.
- 비의자 대표 15개 사례의 F2 확보 범위는 이전 9/15로 유지하며, 이번 단일 테이블 상태 변화 실험을 별도 표본으로 세지 않는다.
- INT-4 전체, INT-5 의미 45개 후보, INT-6 AI 학습·재배포 권리는 미승인.

## 재현

```bash
export PYTHONPATH=src
python -m mcfr.chair_runtime_fixture world \
  --version 1.21.11 --path /tmp/int4-neighbor-world --cache /tmp/int4-neighbor-cache
xvfb-run -a -s '-screen 0 1024x684x24' \
  python -m mcfr.runtime macaw-neighbor-capture \
    --version 1.21.11 --world /tmp/int4-neighbor-world \
    --work /tmp/int4-neighbor-client --output /tmp/int4-neighbor-evidence
python -m mcfr.int4_macaw_neighbor_capture --directory /tmp/int4-neighbor-evidence
```

**완료 판정은 원본 JAR SHA·실제 게임 서버 결과·F2 이미지가 모두 확보된 뒤 작성한다.**

## 실제 Fabric 1.21.11 · 이웃 갱신 실험 결과 (2026-11-22)

고정 Macaw 3.4.2 런타임 JAR SHA-256 `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e`, 연구 원본 S18/S19 모델과 부모 SHA를 확인했다.

| 실제 게임 서버 상황 | 중앙 테이블 east | 동쪽 테이블 west | 게임 결과 |
|---|---|---|---|
| 중앙만 배치 / 동쪽 air | false | 해당 없음 | 단독 외관 |
| 동쪽 테이블 추가 | **true** | **true** | 상판이 이어진 두 탁자 |
| 동쪽 테이블 제거 | **false** | 해당 없음 | 원래 단독 외관 복귀 |

실제 상태는 `/execute if block`의 각 방향 True/False 출력을 통합 서버 로그에서 **양쪽 모두 고유 1개씩** 확인한 결과다. 원본 상태명만으로 자동 연결을 추측하지 않았으며 이웃의 갱신 결과를 후속 Audit에서 **로그 원문으로 다시 파싱**했다.

첫 [실제 원본 게임 성공 CI #44974265995](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44974265995)의 F2 세 장은 탁자가 화면 아래 일부만 보이는 *프레이밍 문제*가 있었다. 이를 원본 모드·서버 상태 문제로 간주하지 않고 카메라 `x=0.5 y=122.8 z=45.5 yaw=180 pitch=28`로 변경 후 [재현 CI #44974527934](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44974527934)에서 **테이블 1개·연결된 2개·다시 1개가 충분히 보이는 실제 F2 세 장**을 촬영했다. 접촉시트를 실제로 열어 확인했다.

- [실제 원본 F2 및 클라이언트 로그 아티팩트 14734114817](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44974527934/artifacts/14734114817), ZIP SHA-256 `1ced6ddc80ae2a3607ef88306d61014c7d90d8d0d3b950cc85e27e1bbb0b47b3`.
- F2 SHA-256 `reset:419bd440d613d6d4b68e45148132bed092a915859b8db1b6bc4872987d0b7cda`, `join:8d1ea8e823e19d459cc7453fc190fdd1e01f25110b443a8dc322e521450a440e`, `remove:29363d98fc1658af8fb2305d62c82ecc6277d3f7160e7b84c02270ce882a2788`.
- 모든 원본 서버 속성, 전후 전환 판정, 직접 이미지 관찰, 처음 촬영의 프레이밍 문제와 실제 촬영 개선은 [INT4_MACAW_NEIGHBOR_SOURCE_RESULT.json](INT4_MACAW_NEIGHBOR_SOURCE_RESULT.json)에 SHA와 함께 고정한다.

### 완료 범위 / 미완료 범위

**통과:** 실제 게임 `/setblock` 기반 이웃 블록 추가 시 `centre.east=true` / `east.west=true`, 제거 시 `centre.east=false` 자동 복귀. 이웃 방향 변화가 고정 원본 모델 선택과 실제 화면 외형 변화에 연결되는 대표 사례다.

**미검증:** 플레이어의 아이템 손배치 클릭, 다른 자재/방향/교차 연결 전체, 연결형 책장의 상하 갱신, 자연스럽게 놓는 Handcrafted 침대의 머리/발 블록 생성과 사용성, 모델의 면별 GPU 텍스처·UV 일치, INT-5 부품 기능·스타일의 최종 의미 및 INT-6 AI 학습·배포 권한.

기존 비의자 대표 F2 사례 **9/15**를 그대로 유지한다. 새로운 3단계 테이블 연결 실험은 기존 S18의 블록상태 후속 검증이며 **별도의 대표 사례 3건으로 중복 계산하지 않는다**.
