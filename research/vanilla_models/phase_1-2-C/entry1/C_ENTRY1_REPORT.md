# 1-2-C Entry1 — 원본 UV·텍스처·PNG 첫 검증

2026-11-16 KST · Minecraft Java Edition 1.21.11 · 시작 `main` `73571a9e1ab791e6ded46b6a01a1aae04fc8ffaf`.

## 실제 연구 범위

P1 `cartography_table`, `flower_pot`, `oak_shelf_left`, `soul_lantern`; P2 `acacia_button`, `glass_pane_post`, `oak_door_bottom_left`, `stone_brick_stairs_inner`; P3 `acacia_leaves`, `stone`, `wheat_stage1`, `fire_floor1`의 **12개 B-first leaf**. 1-2-B의 SHA 원장과 JSON 캐시를 원본 파일에 대조하고 부모 경로를 따라 실제 기하 제공자와 텍스처 슬롯을 해석했다. 과거 v 보고서에 이름이 등장한 모델은 별도 표시했으며 역사 최초 신원 발견은 **0개**이다. 이름 등장만으로 과거의 C 분석 완료 여부를 단정하지 않는다.

| 관측 단위 | 이번 직접 검증 |
|---|---:|
| 모델 / 우선순위 | 12 = P1 4 + P2 4 + P3 4 |
| leaf 적용 face 행 | 96 |
| 원본 `uv` 키 존재 / 부재 | 84 / 12 |
| 텍스처 슬롯 행 | 40 |
| 고유 연결 PNG / 전체 RGBA 픽셀 | 17 / 13,568 |
| 해석 실패한 face·PNG | 0 |

`cartography_table` 6면과 `stone` 6면은 원본 face에 UV 키가 없어 **암시 UV 계산 후보**이다. 이 12면의 게임 엔진 UV 결과를 검증했다고 주장하지 않는다. `soul_lantern` 2면, `oak_door_bottom_left` 3면, `wheat_stage1` 4면은 명시 UV의 한 축 이상에서 원본 좌표 순서가 역방향이다. 좌표를 고치거나 면을 뒤집지 않고 `FACE_UV_EVIDENCE.csv`에 기록했다. PNG 전체 RGBA 해시와 알파 개수는 `PNG_RGBA_EVIDENCE.csv`에서 파일별로 확인할 수 있다.

## 감사와 한계

독립 검산은 Git `HEAD:path` SHA와 부모 계보 12개, 원본 face 선언 96행, 원본 PNG blob 및 복호 RGBA 17개를 별도 코드로 재대조하여 **PASS**. 이 결과는 선택된 12개 모델의 source 연결을 뜻한다. C 전체 직접 대상은 2,304개이고 이 체크포인트에서 **2,292개는 신규 C 실측 대상**으로 남는다. E 예외 86개는 별도 소관이다. v1~v69의 모델별 UV/PNG 의미론 교차표는 아직 작성되지 않았으므로 남은 2,292개를 역사상 미연구 모델이라고 부르지 않는다.

`C1` 역사 근거 교차표 PARTIAL, `C2` 12/2,304 PARTIAL, `C3` 이번 연결 17 PNG 검증·전체 범위 PARTIAL, `C4` Entry1 표본 독립검산 PASS·단계 종료감사 PENDING. 따라서 C 단계 진행 중이다. D blockstate, E renderer 및 실제 게임 UV 결과, 가구 제작과 PZ 변환은 이번 산출물이 아니다.

## 파일

- `MODEL_SOURCE_EVIDENCE.csv`: leaf·부모 소스 SHA와 역사 보고서 이름 등장 여부.
- `TEXTURE_BINDINGS.csv`: 부모 상속과 최종 slot·PNG 텍스처 참조.
- `FACE_UV_EVIDENCE.csv`: face별 원본 UV·회전·역방향 및 원본 기하·leaf SHA.
- `PNG_RGBA_EVIDENCE.csv`: 원본 PNG SHA·크기·RGBA 해시·알파 분포.
- `UNRESOLVED.csv`: 이번 검사의 미해결 0행(헤더 보존).
- `C_ENTRY1_AUDIT.json`, `C_ENTRY1_INDEPENDENT_AUDIT.json`: 집계 및 재계산 결과.
- `scripts/phase_1_2_c_entry1.py`: 같은 원본에서 산출물 재생성.
