# Entry4 원형 비교 — P2 후반

수치는 원본 모델 좌표의 축별 범위이며 회전 후 게임 화면의 외접 범위나 충돌 판정은 아니다. 시각 설명은 원본 PNG 첫 프레임을 `visual_contact/contact_01.png`~`contact_03.png`에서 관찰한 결과다. 부모·leaf 경로와 SHA는 같은 폴더의 원장에 있다.

| 원본 예시 | 기하 구조 | 원본 PNG 관찰 | 가구 표현 활용 후보와 한계 |
|---|---|---|---|
| `mangrove_fence_post.json` → `fence_post.json` | 하나의 4×16×4 수직 직육면체 | `mangrove_planks.png`는 붉은 갈색 수평 판재 줄무늬 | 가구 다리나 선반의 가는 지지대를 한 요소로 단순화하는 후보. 실제 목재 재질·강도는 이미지로 확정할 수 없다. |
| `scaffolding_stable.json` | 9요소, 0두께 없이 한 요소의 축 치수가 1 이하, bbox 16×16×16 | `scaffolding_top.png`는 갈색 격자와 투명 칸, `scaffolding_side.png`는 얇은 외곽과 넓은 투명 영역 | 열린 선반의 입체 프레임과 표면 격자를 각각 기하와 PNG에 나누는 후보. 원본의 기계적 지지 기능은 모델만으로 증명되지 않는다. |
| `spruce_trapdoor_bottom.json` → `template_orientable_trapdoor_bottom.json` | 단일 16×3×16의 얕은 판 | `spruce_trapdoor.png`는 갈색 세로 판·가로 띠·밝은 작은 구멍 | 문짝·상판 두께는 단일 요소로, 홈과 작은 장식은 이미지로 표현하는 후보. 투명 처리와 회전 상태는 blockstate 원문과 별도 검토한다. |
| `observer.json` | 정확한 단일 0..16 정육면체 | `observer_front.png`의 회색 사각 구획, `observer_back_on.png`의 붉은 점 | 단순 육면체에 방향별 면 이미지로 복잡한 전면·후면을 부여하는 후보. 이미지의 모양에서 기능을 추측하지 않는다. |
| `tripwire_hook.json` | 7요소, 4개 0두께, 6개 회전, bbox 4×8×8.1 | `tripwire_hook.png`는 회색 상단과 갈색 가는 줄이 투명 바탕에 보인다 | 작은 돌출 장식의 회전 평면과 입체 받침 조합 후보. 원본 좌표 bbox는 회전 뒤 형상을 뜻하지 않는다. |
| `stone_slab.json` | 단일 16×8×16 판 | `smooth_stone_slab.png`는 회색 가로 경계와 안쪽 명암 | 두꺼운 상판·받침을 입체로 두고 표면 경계를 PNG로 표현하는 후보. `spruce_trapdoor_bottom`의 3두께와 같다고 묶지 않는다. |

`EXACT_FULL_CUBE` 20개, `MULTI_ELEMENT` 194개, `THIN_ELEMENT` 63개, `ZERO_THICKNESS` 46개, `ROTATED_ELEMENT` 19개다. 태그는 겹치므로 합계가 494가 아니다. 0두께 평면이 모든 열린 틀에 필요한 것은 아니다. 예를 들어 `scaffolding_stable`은 9개 입체 요소의 열린 프레임을 사용하고, `observer`는 단일 큐브의 여러 면 PNG로 형태를 단순화한다. 이 구분이 향후 가구 모델링 후보를 선택할 때 유용하다.
