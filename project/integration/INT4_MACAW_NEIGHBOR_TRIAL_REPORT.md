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
