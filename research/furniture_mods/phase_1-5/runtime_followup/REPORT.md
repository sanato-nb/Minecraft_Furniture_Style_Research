# 1-5-B·C·D 보류 항목 재검증

| 대상 | 결과 | 남은 확인 |
|---|---|---|
| 1-5-B 흰색 침대 형상·UV | 🟢 100% · 북향 실측 완료 | 보류 해제 |
| 1-5-C 제한 판정 | 🟢 100% · 7/7 재판정 | 표본별 반례와 적용 제한 기록 |
| 1-5-D 런타임 예외 | 🟡 10/10 착수 · 완료 9/10 (90%) · 부분 확인 1/10 | 각 확인의 남은 월드·조명·이벤트 조건은 검증표 참조 |

## 1-5-B · 흰색 침대

| 표본 | 가로 × 높이 × 깊이 (블록) | 모델 면 |
|---|---:|---:|
| 바닐라 흰색 침대 V11 | 1 × 0.5625 × 2 | 전용 렌더러 6 직육면체·36 quad |
| HC 북향 흰색 침대 S37/S38 | 1 × 1 × 2 | 일반 블록 모델 78 quad (발치 72·머리 6) |

**바닐라 V11.** 실제 1.21.11 클라이언트에서 흰색 침대의 머리와 발치 모델 레이어, 북향 렌더러 변환을 읽었다. 발치 원점에 맞춰 머리 정점을 북쪽 1블록에 배치했다. 전용 모델의 원본은 `assets/minecraft/textures/entity/bed/white.png` (64×64)이며 정점 UV 범위는 U 0–62, V 0–44px이다. UV 경계 좌표는 텍스처 평면의 범위이고, 전체 범위 안 모든 픽셀의 사용을 의미하지 않는다. 일반 블록 JSON의 요소 수 0은 해당 모델 경로의 집계다. GUI 항목은 `BedModelRenderer`를 선택했다. [정점과 UV](WHITE_BED_VERTICES.csv) · [월드와 손](evidence/V11_world_and_hand.jpg) · [인벤토리](evidence/V11_inventory.jpg)

**HC S37/S38.** 동일한 북향 기준으로 두 상태의 baked quad 좌표를 합산했다. 머리와 발치의 경사 메시가 위치가 같은 quad 6면에 서로 다른 스프라이트를 사용한다. 월드에서 북향 조립을 캡처했고 머리·발치 두 칸 모두 블록 바닥보다 9/16블록 높은 Y=25.5625에 떨어져 멈췄다. [북향 설치](evidence/S37_S38_north.jpg) · [충돌 좌표](evidence/S37_S38_collision.jpg)

## 1-5-C · 일곱 판정

[표본별 재판정](LIMITED_FINDINGS.csv). 계단과 의자, 투명 오버레이와 모델 연결, 서랍 손잡이, 벤치 등받이, 침대, 조명, 화분을 각각 재검증했다. 예를 들어 Macaw 대표 서랍의 렌더 폭은 1.00625블록이었고, 엔진의 좌우 충돌 폭은 0.875블록이었다. AF 램프는 세 단계에서 소등 0, 점등 5·10·15를 반환했고 점등 시 측면 4곳의 UV가 바뀌었다.

## 1-5-D · 엔진 확인과 월드 확인

[10개 검사 판정표](RUNTIME_VERIFICATION.csv)에는 원래 계획 조건별 실측과 남은 작업을 기록했다. 고정 모드 47상태와 바닐라 15상태에서 baked quad, 파티클 스프라이트, 블록 광량, 선택·충돌 상자, 이웃 면 가림 판단을 읽었다. 엔진의 블록 상자는 빈 블록 뷰의 기본 문맥이며, 별도의 월드 시험을 함께 기록했다. [월드 측정값](WORLD_READBACK.csv)

- AF 암실 램프는 광원에서 두 블록 떨어진 고정 위치에서 점등 레벨별 블록 광량 3·8·13을 반환했고 소등은 모두 0이었다. [레벨 1](evidence/lamp_level_1.jpg) · [레벨 2](evidence/lamp_level_2.jpg) · [레벨 3](evidence/lamp_level_3.jpg)
- 참나무 계단의 상단 디딤판은 북향에서 Z 방향 절반을 차지했고 동향에서는 X 방향 절반을 차지했다. 두 경우 모두 U는 월드 X, V는 월드 Z를 따라 증가했다. 계단·울타리·책장·소파의 북·동향 및 테이블의 연결별 패턴을 월드에서도 비교했다. 테이블 표본은 방향 속성 대신 연결 상태를 가졌다. [계단과 울타리](evidence/uv_controls.jpg) · [책장·소파·테이블](evidence/uv_tables_couches_bookshelves.jpg)
- HC 의자·사이드 테이블·선반 4상태는 같은 시점과 시야에서 돌 유무를 바꾸고, 돌을 유지한 상태로 낮과 밤을 비교했다. 캡처 위에서부터 낮·빈 이웃, 낮·돌 이웃, 밤·돌 이웃이다. [오버레이 및 이웃 비교](evidence/alpha_neighbor_light.jpg)
- 바닐라 통과 AF 서랍은 실제 우클릭으로 각 GUI를 열었다. 북향 Macaw 서랍의 손잡이는 모델 경계에서 돌출되며 선택·충돌 상자는 별도로 읽었다. [닫힘·상호작용 화면](evidence/storage_interactions.jpg)

- 가마솥과 싱크대는 물 상태에서 수면이 각각 1면씩 추가됐다. 가마솥은 15/16블록 높이·tint index 0, 싱크대는 14/16블록 높이·tint index -1이다. 두 스프라이트 모두 엔진에 준비된 32프레임을 읽었다. 카메라를 고정한 두 캡처의 선택 영역에서 만수 수면은 각각 1,192·1,308픽셀이 변했고 빈 대조 영역은 모두 0픽셀이 변했다. [같은 시야의 두 프레임](evidence/water_frames.png)
- 원본 누락 PNG ID 8개는 모두 `minecraft:missingno`를 반환했다. 별도 선언 77개의 블록 아틀라스 조회는 75개 일치, 2개 대체였다. 대체 2개는 Macaw 아이템 경로 `cabinet_door`, `cabinet_drawer`다. 두 경로는 블록 아틀라스 조회에서 대체됐다. 두 아이템 모두 실제 인벤토리에서 정상 표시됐다. 파티클은 HC 금속 벤치를 파괴하는 이벤트에서 확인했다. [파괴 전후](evidence/metal_bench_particles.jpg) [ID별 조회](ATLAS_READBACK.csv) · [두 아이템 캡처](evidence/macaw_item_layers.jpg)
- 부모 누락 모델 48개(AF 4·Macaw 44)의 파일은 배포 JAR에 모두 들어 있었고, 정확한 부모 경로와 소속 배포의 블록상태·아이템에서 연결되는 경로는 모두 없었다. [배포 JAR 대조](PARENT_DEPLOYMENT.csv)
- 미해결 상태 옵션 4개는 동일한 미등록 흰색 차양 블록의 네 방향이다. AF 자작나무·가문비나무 의자는 남향 `variant=3`과 `variant=1`의 baked quad가 각각 일치했다. [기존 의자 월드 캡처](../../phase_1-3/followup/evidence/chair_variants.jpg)

## 재현 자료

- Minecraft Java 1.21.1 · Another Furniture Fabric 4.0.2, Handcrafted Fabric 4.0.3
- Minecraft Java 1.21.11 · Macaw’s Furniture 3.4.2 및 vanilla 대조군
- Another Furniture 고정 소스 4.0.3과 런타임 배포 4.0.2는 모델 및 블록상태 JSON의 구조가 일치한다. 광량·동작 관측은 실제 실행한 배포 버전에 한정한다. [배포 대조](../../phase_1-3/followup/RELEASE_COMPARISON.csv)
- [1.21.1 엔진 기록](ENGINE_1.21.1.tsv.xz) · [1.21.11 엔진 기록](ENGINE_1.21.11.tsv.xz) · [정량 요약과 SHA-256](SUMMARY.json)
- `run_comparison_probe.py --version <버전> --work <캐시> --client-cache <공식 클라이언트 JAR> --output <TSV>`로 재실행할 수 있다. Java 21과 X 디스플레이가 필요하다. 두 원본 TSV를 제공된 이름으로 xz 압축한 뒤 `python audit_runtime.py <공식 1.21.11 클라이언트 JAR>`로 대상·중복·UV·주요 측정을 검산한다.
