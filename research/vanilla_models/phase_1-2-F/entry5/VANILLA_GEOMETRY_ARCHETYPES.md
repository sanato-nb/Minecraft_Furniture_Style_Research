# Entry5 원형 비교 — P3 전반

`from/to` 좌표 범위와 PNG 첫 프레임을 비교했다. 이미지는 `visual_contact/contact_01.png`~`contact_08.png`에서 직접 확인했다. 다음은 **가구 제작에 옮겨 쓸 표현 후보**이며 실제 물체의 기능, 충돌 형상 또는 런타임 렌더 판정이 아니다. 각 leaf와 기하 제공자·PNG의 경로/SHA는 같은 폴더의 원장에 기록한다.

| 원본 예시 | 원본 구조 | 원본 PNG 관찰 | 가구 표현 후보와 한계 |
|---|---|---|---|
| `acacia_leaves.json` → `leaves.json` | 정확한 단일 16×16×16 정육면체 | `acacia_leaves.png`에서 회백색 잎 픽셀이 분절된 빈 영역과 함께 보임 | 단순 기하와 복잡한 표면 실루엣을 결합하는 후보. 빈 픽셀의 실제 블렌딩·가시성은 엔진 미검증. |
| `copper_grate.json` → `cube.json` | 정확한 단일 16×16×16 정육면체 | `copper_grate.png`의 주황색 격자와 규칙적인 투명 칸 | 격자 표면을 입체 막대 없이 이미지에 맡기는 후보. 원본의 물리적 열린 프레임이라고 해석하지 않는다. |
| `mangrove_roots.json` | 8요소, 0두께 요소 2개를 포함한 다중 구조 | `mangrove_roots_side.png`의 굵은 갈색 세로 줄과 투명한 사이 공간 | 수납장 틀이나 불규칙 지지대를 여러 요소와 이미지 실루엣으로 조합하는 후보. 실제 수납 기능은 가설이다. |
| `amethyst_cluster.json` → `cross.json` | 회전한 0두께 평면 2개, 원본 bbox 약 14.4×16×14.4 | `amethyst_cluster.png`의 보라색 뾰족한 투명 배경 실루엣 | 작은 장식의 부피감을 교차 평면과 이미지로 암시하는 후보. 회전 후 경계·관찰 각도의 실제 외형은 미검증. |
| `cobweb.json` → `cross.json` | 회전한 0두께 평면 2개 | `cobweb.png`의 가는 흰 대각선과 넓은 투명 영역 | 가는 장식·망을 최소 요소로 암시하는 후보. 실물 두께와 충돌은 원본 요소만으로 판정하지 않는다. |
| `fire_floor0.json` → `template_fire_floor.json` | 회전·0두께 평면 4개, 원본 bbox 16×22.4×16 | `fire_0.png` 첫 프레임에서 노랑·주황 실루엣 | 반복 평면으로 비정형 장식 실루엣을 세우는 후보. 애니메이션 전 과정과 실제 광원은 인증되지 않았다. |
| `end_portal_frame.json` | 단일 16×13×16 직육면체 | 관련 측면 PNG에 짙은 청록 테두리와 밝은 황록색 가로 장식 | 두꺼운 받침의 돌출은 기하로, 면의 작은 장식은 이미지로 나누는 후보. 기능과 실제 재질을 이미지로 확정하지 않는다. |

`EXACT_FULL_CUBE` 202, `MULTI_ELEMENT` 127, `THIN_ELEMENT` 129, `ZERO_THICKNESS` 122, `ROTATED_ELEMENT` 89로 태그는 겹친다. `copper_grate`의 격자 **이미지**와 `mangrove_roots`의 다중 **입체**는 외형이 유사해 보여도 제작 방법이 다르다. E 소관 24개는 일반 요소 통계에서 제외했고 particle 이미지를 실제 renderer 표면으로 해석하지 않았다.
