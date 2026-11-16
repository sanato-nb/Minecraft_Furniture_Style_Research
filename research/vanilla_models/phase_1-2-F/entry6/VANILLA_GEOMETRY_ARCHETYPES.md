# 1-2-F Entry6 — 원본 JSON 기하 원형 비교 (PNG 직접 시각 검수 미완료)

> **증거 경계:** 다음은 사용자 추출 Minecraft Java 1.21.11의 *모델 JSON·부모 계보·요소 좌표를 직접 재검산*한 정적 유형화 결과다. C PNG 경로/SHA를 상속한 것과 **이번 회차에서 실제 PNG 픽셀을 눈으로 본 것**은 다르다. Entry6에서는 후자를 수행하지 못했으므로 PNG 색감·문양·물체 정체·엔진 블렌딩·렌더링 효과를 확정하지 않는다. F3 미통과.

## 회차별 복수 원형 태그
- `EXACT_FULL_CUBE`: **186모델**
- `THIN_ELEMENT`: **146모델**
- `ZERO_THICKNESS`: **145모델**
- `AXIS_ALIGNED_CUBOIDS`: **13모델**
- `MULTI_ELEMENT`: **155모델**
- `ROTATED_ELEMENT`: **94모델**
- `INVERTED_OR_OUTSIDE_16`: **65모델**
- `E_SOURCE_EXCEPTION`: **7모델**

총모델 378 = 적용 기하 371 + E 특수 7. 각 모델에 여러 태그가 동시에 적용될 수 있으므로 합은 378이 아니다. `THIN_ELEMENT`는 축 치수 ≤1 모델 좌표 단위, `ZERO_THICKNESS`는 정확한 0. bbox는 원본 `from/to` 범위이며 회전 후 게임 화면상 최종 경계가 아니다.

## 검증 가능한 대표 사례
| 모델 원본·SHA | 실제 기하 제공자·SHA | 요소 / 면 / bbox (원본좌표) | 가구 제작용 구조 표현 후보 | 반드시 남기는 한계 |
|---|---|---|---|---|
| `mud.json` (Git `5cfbb594db2f`) | `cube.json` (`1b9780b479ae`) | 1 / 6 / 16×16×16 | 단일 큐브형 몸체·표면 비례의 구조적 비교 기준 | 진흙 PNG 실제 색감/패턴 미관찰 |
| `mushroom_block_inside.json` (Git `8c7b371346b1`) | `template_single_face.json` (`d23e5f207cb8`) | 1 / 1 / 16×16×0 | 평면 문양/패널 표현을 구조적으로 비교할 후보 | 실제 투명/가림·렌더 방향 인증 안 됨 |
| `nether_sprouts.json` (Git `a13485762a60`) | `cross.json` (`37c8b09f251c`) | 2 / 4 / 약 14.4×16×14.4 | 교차 평면형 장식을 최소 요소로 배치하는 구조 후보 | 원본 PNG의 불투명 영역/실루엣 미관찰 |
| `template_two_candles.json` (Git `2abbb10c2906`) | `template_two_candles.json` (`2abbb10c2906`) | 6 / 20 / 6×7×3 | 작은 물체 여러 개의 높이·두께 차이를 cuboid로 구성하는 예 | 촛불 특수 효과·실제 게임 시각 상태는 미확인 |
| `template_three_candles.json` (Git `d9963dc7b600`) | `template_three_candles.json` (`d9963dc7b600`) | 9 / 30 / 5×7×5 | 여러 좁은 부품 군집을 적은 블록 공간에 압축하는 구조 비교 | 비례가 가구 부품으로 바로 적합하다는 보장은 없음 |
| `small_dripleaf_top.json` (Git `847edac30502`) | `small_dripleaf_top.json` (`847edac30502`) | 8 / 22 / 14×14×14 | 얇은 상판 및 다중 지지 입체를 조합하는 방식의 후보 | 실제 PNG·게임 내 관찰 각도 미검증 |
| `pink_petals_1.json` (Git `38dacd572f69`) | `flowerbed_1.json` (`5b7ba90dff0b`) | 7 / 14 / 9.65×2.99×10.6 | 바닥에 낮게 깔린 장식층을 얇게 구성하는 예 | 부분 투명 PNG 윤곽은 미확인 |

**반례:** `mud.json`은 완전한 16³ 단일 큐브, `mushroom_block_inside.json`는 0두께 단일 1면이며 모두 요소 1개로만 비교하면 동일시할 위험이 있다. `nether_sprouts.json`의 교차 평면은 형식상 두 요소를 가지지만, 두 개의 실제 단단한 가구판과 동일한 두께·렌더 효과라고 단정할 수 없다. `template_two_candles.json`과 `template_three_candles.json`은 작은 다중 cuboid를 갖지만 임의의 PZ 가구가 이 구조를 그대로 재사용할 수 있다는 증명은 아니다.

원본 전체 세부정보: [F_GEOMETRY_ELEMENTS.csv](F_GEOMETRY_ELEMENTS.csv) (요소 661행, `from/to`·회전), [F_GEOMETRY_FEATURES.csv](F_GEOMETRY_FEATURES.csv) (378모델), [F_TEXTURE_VISUAL_EVIDENCE.csv](F_TEXTURE_VISUAL_EVIDENCE.csv) (원본 PNG 경로/SHA만). 검증 중 미확정 사유: [F_UNRESOLVED.csv](F_UNRESOLVED.csv). 모델링 *후보*를 원본 사실이나 제작물 실적으로 전환하지 않는다.
