# INT-4 연구 결과 간 교차 검증 — 대표 비의자 F2와 책장·침대 배치

기준은 [PR #45](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/45)의 `655a29154a5ae097a02cb9f059f3e293a5ce341c`다. 기존 [15사례 원본 교차검증](INT4_NONCHAIR_SOURCE_CROSSCHECK_REPORT.md), [Macaw 주방](INT4_MACAW_KITCHEN_REAL_F2_REPORT.md), [Macaw 테이블·책장](INT4_MACAW_TABLE_SHELF_REAL_F2_REPORT.md), [Handcrafted 침대](INT4_HANDCRAFTED_BED_F2_REPORT.md)의 대표 9사례에 이번 회차에서 실제 F2와 상태를 확인한 6사례를 추가했다. 대표 표본은 **15/15**다.

## 남은 대표 6사례의 서버·시각 검증

Minecraft 1.21.1, Fabric Loader 0.18.4, Another Furniture 4.0.2, Handcrafted 4.0.3 환경에서 `execute if block`으로 중앙 좌표 `0 120 40`의 원본 전체 상태를 판독했다. 같은 카메라에서 실제 클라이언트 F2로 찍었으며 여섯 사진 모두 대상이 화면에 들어왔다.

| 사례 | 역사 원본 적용·기하 | 런타임 관찰 |
|---|---|---|
| S14 | Another Furniture 상판과 4방향 다리, 5적용·42면 | 단독 테이블, 네 다리 속성 모두 `true` |
| S15 | Another Furniture 상판, 1적용·6면 | 같은 방향 3×3 테이블을 배치해 중앙의 네 다리 속성이 모두 `false`가 됨 |
| S16 | Handcrafted 단독 테이블, 1적용·60면 | 단독 테이블, `shape=single` |
| S17 | Handcrafted 중앙 테이블, 1적용·12면 | 3×3 배치로 중앙에 `shape=center`가 형성됨 |
| S39·S40 | Handcrafted 방해석 카운터, 각각 1적용·12면 | `type=1`, `type=2` 각각 확인. 상판과 하부 모양은 유사하며 같은 카메라 RGB 차이는 총 31픽셀 |

첫 실행에서 단독 블록에 강제 지정한 S15와 S17은 서버에서 요청한 상태를 유지하지 않았다. 처음 시도는 카메라도 바닥으로 내려가 증거 사진에서 제외했다. 재현 때는 위 두 사례를 이웃과 함께 배치했고 관전자 카메라로 위치를 고정했다. S15/S17 사진은 연결된 전체 상판을 보여 주며, 중앙 블록의 선택 상태는 서버 로그로 구별한다.

Another Furniture S14/S15의 연구 원본은 4.0.3 Git 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`이고 실행 JAR는 Fabric 4.0.2다. 블록상태·선택 모델·기하 부모 5개에서 원본 Git blob SHA와 실제 JAR SHA를 각각 확인했다. 바이트는 모두 달랐으며 파싱한 JSON은 5/5 동일했다. Handcrafted의 네 대표 사례에 참조된 블록상태·선택 모델·기하 부모는 역사 Git blob과 JAR 바이트가 일치했다. S39/S40은 같은 부모 기하와 상판 텍스처를 사용하며 목재 텍스처 경로가 다르다. 이번 RGB 차이 집계는 촬영 시점 한 곳의 화면 측정이다.

## Macaw 책장 수직 연결

Minecraft 1.21.11과 Macaw 3.4.2에서 `/setblock`으로 북향 책장을 아래부터 추가하고 가운데를 제거했다. 명령은 `connection`에 값을 주지 않았으며, 서버가 계산한 결과를 네 번 판독했다.

| 순서 | 아래 y=120 | 가운데 y=121 | 위 y=122 |
|---|---|---|---|
| 1단 | `base` | 공기 | 공기 |
| 2단 | `bottom` | `top` | 공기 |
| 3단 | `bottom` | `middle` | `top` |
| 가운데 제거 | `base` | 공기 | `base` |

실제 F2 네 장에서 한 칸, 연결된 두 칸, 연결된 세 칸, 가운데가 빈 두 책장이 보였다. 직접 회귀 검증한 범위는 블록 명령에 따른 수직 이웃 갱신이다. 원본 JAR의 방향별 선택 모델, 회전과 기하 부모 SHA, 요소·면 수를 결과에 보존했다.

## Handcrafted 실제 침대 설치와 파괴

Minecraft 1.21.1과 Handcrafted 4.0.3에서 Creative 플레이어에게 오크 침대 아이템 하나를 주고, 북향으로 우클릭해 설치했다. `0 120 40`에 발, `0 120 39`에 머리가 생겼다. 두 블록 모두 `color=white,facing=north,occupied=false,shape=single`로 S37/S38의 원본 상태와 일치했다. 발을 좌클릭으로 파괴하자 두 위치 모두 공기가 됐다. 같은 카메라에서 설치 전, 설치 뒤, 파괴 뒤 F2로 바닥과 침대 모습을 직접 확인했다. 수면 상호작용 및 `occupied=true` 전환은 후속 검증 범위다.

## 증거와 재현

[결과 JSON](INT4_NONCHAIR_RUNTIME_RESULT.json)은 설치 JAR SHA, 역사 원장 SHA, 원본 모델과 부모 SHA, 서버 로그 SHA-256, F2 13장의 SHA-256과 사진별 관찰을 함께 고정한다. 첫 실행에서 제외한 F2와 상태 결과의 해시도 보존했다.

기존 [Macaw 이웃 갱신 Actions](../../.github/workflows/integration-int4-macaw-neighbor.yml)가 두 버전의 실제 클라이언트 재현과 로그·PNG 무결성 감사를 실행한다. 재현된 출처와 상태는 결과 JSON과 비교한다. 하드웨어와 촬영 시간에 따라 달라질 수 있는 PNG 해시는 실행별로 검증하고 새 아티팩트에 기록한다.

INT-4 전체에는 고정된 전체 분모가 없다. 책장 아이템 직접 배치, 침대 수면·점유, 면별 UV와 렌더 픽셀의 인과 검증을 보류한다. INT-5 의자 부품 역할 후보 45개는 의미 승인 0건, INT-6 학습·재배포 권한 승인 0건이다.
