# Entry3 원형 비교 — P2 전반

수치는 원본 `from/to` 좌표의 축 정렬 범위다. 회전 후 게임 화면의 외접 범위, 충돌, 실제 renderer는 뜻하지 않는다. 이미지 관찰은 `visual_contact/contact_01.png`~`contact_03.png`의 원본 PNG 첫 프레임에 한정된다.

| 원본 예시 | 구조 관찰 | PNG 직접 관찰 | 가구 표현에 이전할 후보와 한계 |
|---|---|---|---|
| `bamboo_fence_gate.json` → `template_custom_fence_gate.json` | 8개 입체 요소, 좌표 bbox 16×11×2 | `bamboo_fence_gate.png`: 연노란 가로대와 기둥 사이 투명한 두 칸 | 열린 틀을 한 장의 평면 대신 여러 막대의 간격으로 표현할 수 있다. 이 모델의 게임 속 열림 동작은 이 정적 모델만으로 증명되지 않는다. |
| `copper_trapdoor_bottom.json` → `template_trapdoor_bottom.json` | 단일 16×3×16 판 | `copper_trapdoor.png`: 주황색 틀·십자 무늬와 일부 투명 공간 | 판 두께를 3 좌표 단위로 두고 표면의 작은 패턴을 이미지에 맡기는 후보. 실제 재질·투명 처리 결과는 미확인. |
| `glass_pane_post.json` → `template_glass_pane_post.json` | 단일 2×16×2 기둥 | `glass.png`: 옅은 경계, 대각 반사선, 넓은 투명 영역 | 가는 세로 지지대를 별도 요소로 표현하는 후보. 유리 광학 효과를 PNG만으로 단정하지 않는다. |
| `iron_bars_post.json` → `template_bars_post.json` | 2개 0두께 요소, bbox 2×16×2 | `iron_bars.png`: 수직 살과 가로 연결부 사이 투명 영역 | 철창형 파티션의 얇은 면과 이미지 실루엣 결합 후보. 0두께는 원본 좌표값이며 실제 두께가 0이라는 뜻이 아니다. |
| `ladder.json` | 1개 0두께 요소, bbox 16×16×0 | `ladder.png`: 양쪽 세로대와 반복 가로대, 사이 투명 영역 | 벽에 붙는 격자나 선반 전면을 평면+알파로 압축하는 후보. 원본에 개별 입체 발판은 없다. |
| `calibrated_sculk_sensor.json` | 7요소, 6개 회전·0두께 요소, 원본 좌표 bbox 18×20×16 | `calibrated_sculk_sensor` 관련 첫 프레임에 보라색 중심과 짙은 청록색 배경 | 작은 장식을 회전 평면으로 외곽에 배치하는 후보. 좌표가 0~16 밖이며 회전 후 형상과 실제 시각 효과는 별도 검증 필요. |
| `acacia_button_inventory.json` → `button_inventory.json` | 단일 6×4×4 직육면체 | `acacia_planks.png`: 갈색 수평 판재 무늬 | 매우 작은 돌출 부품을 간결한 입체로 두고 면 무늬를 PNG로 부여하는 후보. 실제 버튼 기능이나 가구 손잡이 적용은 가설이다. |

각 모델의 원본 경로·SHA, 부모 체인, 요소 좌표 및 선택 상태는 같은 폴더의 `F_MODEL_SOURCE_STATUS.csv`, `F_GEOMETRY_ELEMENTS.csv`, `F_D_ORIGINAL_RULE_CHOICES.csv`에 있다. 반례로 `copper_trapdoor_bottom`은 얇지만 0두께가 아니며, `ladder`는 0두께지만 개별 입체 사다리 발판은 없다. 하나의 태그만으로 대상의 기능을 결정하지 않는다.
