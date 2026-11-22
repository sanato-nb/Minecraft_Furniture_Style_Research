# INT-4 실제 플레이어 입력 — Macaw 책장과 Handcrafted 침대

[PR #46](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/46)의 명령 기반 책장 갱신과 침대 설치·파괴에 이어 실제 아이템 배치와 수면을 확인했다. 공식 Minecraft 서버로 생성한 새 Creative 평지 월드 사본과 이전과 동일한 고정 모드 릴리스를 사용했다.

## Macaw 3.4.2 책장 · Minecraft 1.21.11

Creative 핫바에 오크 책장 아이템을 넣고 우클릭으로 하단을 놓았다. 웅크리기와 우클릭을 사용해 두 번째와 세 번째를 쌓은 뒤, 가운데를 좌클릭으로 부쉈다. 3층을 조준할 때 발판을 놓았으며 책장 위치의 배치·제거는 모두 실제 플레이어 입력으로 했다.

| 관찰 시점 | 아래 (0,120,40) | 가운데 (0,121,40) | 위 (0,122,40) |
|---|---|---|---|
| 배치 전 | 공기 | 공기 | 공기 |
| 1층 아이템 배치 | `base` | 공기 | 공기 |
| 2층 아이템 배치 | `bottom` | `top` | 공기 |
| 3층 아이템 배치 | `bottom` | `middle` | `top` |
| 가운데 파괴 | `base` | 공기 | `base` |

이번 플레이어 배치의 서버 방향은 모두 `east`였고, PR #46 명령 배치의 `north`와 수직 연결 순서가 같았다. 다섯 F2에서 빈 바닥, 적층, 제거 후 생긴 틈을 직접 확인했다. 다른 방향의 직접 배치, 다른 변형끼리의 결합, Survival 아이템 소비는 이 실험 범위 밖이다.

## Handcrafted 4.0.3 침대 · Minecraft 1.21.1

Creative 플레이어가 흰색 오크 침대를 놓은 뒤, 빈 손으로 우클릭해 잠들고 Escape로 수면을 종료했다. 야간과 수면을 유지하기 위해 `doDaylightCycle=false`, `playersSleepingPercentage=101`을 적용했다. 예약된 데이터팩 함수가 수면 중에 서버 상태와 플레이어 `SleepTimer`를 판독했다. 기상 판독은 관전자 모드로 바꾸기 전에 진행했다.

| 관찰 시점 | 발 (0,120,40) | 머리 (0,120,39) | 플레이어 증거 |
|---|---|---|---|
| 설치 전 | 공기 | 공기 | 빈 바닥 F2 |
| 설치 직후 | `occupied=false` | `occupied=false` | 설치된 침대 F2 |
| 수면 중 | `occupied=true` | `occupied=true` | `SleepTimer > 0`, 실제 F2에 `Leave Bed` 표시 |
| Escape로 기상 | `occupied=false` | `occupied=false` | `SleepTimer = 0`, 침대가 남아 있는 F2 |

핀 고정 원본 Git과 설치 JAR의 블록상태 및 네 선택 모델·기하 부모를 바이트 단위로 대조했다. S37 발의 원본 모델은 수면 시 **12요소·72면에서 14요소·84면**으로 바뀐다. S38 머리는 선택 모델 경로가 바뀌지만 같은 1요소·6면 부모와 같은 텍스처 선언을 사용한다. 수면 F2는 플레이어 화면이므로, 점유 모델 외형의 픽셀 대응은 따로 검증해야 한다. 밤 건너뛰기, 자연 기상, 다인 서버 동작은 실험 범위 밖이다.

## 증거와 범위

[결과 JSON](INT4_PLAYER_INTERACTION_RESULT.json)에 원본과 모드 버전, 서버 로그 SHA-256, 원본 F2 9장 SHA-256, 함수 SHA와 상태별 관찰을 기록했다. 기존 [Actions](../../.github/workflows/integration-int4-macaw-neighbor.yml)의 두 버전 작업에서 같은 월드 원본을 새로 복사해 재실행한 후 상태·출처를 결과 JSON과 대조한다. PNG는 실행별 SHA로 검증한다.

대표 비의자 F2 표본은 기존 15/15를 유지한다. 이번 결과는 해당 모드와 버전에서 관찰한 실제 플레이어 입력 동작이다. INT-4 면별 UV와 렌더 픽셀 대응, INT-5 의자 부품 45개 역할 검토 및 INT-6 이용 허가 심사는 후속 범위다.
