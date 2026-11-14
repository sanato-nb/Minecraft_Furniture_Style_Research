# v63 — 1-2-A 역사 연구 194파일 인벤토리 + 모루 3종의 v30 원본 증거·SHA 복원

> Minecraft Java 1.21.11 · 2026-11-15 KST · 연구 시작 HEAD `830111f5edda425cff04e961f382eaa9f4aa1776`. 1-2-A 실제 근거 연구 진행, 현재 1-2-A 완료 판정 아님.

## 1. v5~v43 과거 연구 파일 모집단 직접 Git tree 인벤토리

연결된 GitHub 저장소의 `research/vanilla_models` 하위 **실재하는 v5~v43 21개 폴더**(v5~v10, v25~v38, v43) 각각을 Git tree recursive로 읽어 **194개 파일**의 원본 경로·Git blob SHA·바이트 크기를 `00A_HISTORY_V5_V43_FILE_INVENTORY_194.csv`로 기록. 모두 API `truncated=false` 원본 디렉터리 목록에서 확인.

| 파일 확장자 | Git tree 출처 파일 |
|---|---:|
| CSV | 137 |
| Markdown | 30 |
| JSON | 19 |
| SQLite | 4 |
| Python | 4 |
| **전체** | **194** |

v62가 원본 내용과 SHA를 검사한 기존 CSV **21개**, v63에서 새로 직접 내용을 확인한 CSV **3개**(`v30/08_anvil_three_leaf_top_texture_overrides.csv`, `v30/04_pot_enchant_anvil_9_png_rgba.csv`, `v30/05_pot_enchant_anvil_51_material_face_uv_rgba.csv`)를 중복 제거하면 **선택 검수 원본 CSV 24개**. 다른 파일 **170개는 v62~v63 이번 통합 범위에서 파일/트리 SHA의 존재만 새로 기록**한 상태. 이전 역사 다른 채팅에서 이미 일부 내용을 연구했을 가능성을 부정하지 않음. 따라서 이번 회차를 **194개 과거 파일의 내용 전수 검수**라고 주장하지 않는다. 특히 SQLite 4개는 이번 회차 Git tree SHA 식별만, DB 로드·SQL 행별 의미론 전수 재검사는 하지 않았다.

원본 21개 폴더 목록과 각 SHA: `00A_HISTORY_V5_V43_FILE_INVENTORY_SUMMARY.json`. 트리 인벤토리 제작의 원본 API 자료는 `00A_HISTORY_TREE_PART1.json` 및 `00A_HISTORY_TREE_PART2.json`.

## 2. v62에서 선택 근거가 없던 두 모루 모델의 실제 역사 증거 발견

v62 `04_SOURCE_REVIEW_LEDGER_544.csv`에서 명시 직접 모델 JSON 재검증 플래그가 없고 선택 역사 SHA행 증거도 없는 P1 모델은 `chipped_anvil.json`, `damaged_anvil.json` 두 건이었다. 과거 **v30 `08_anvil_three_leaf_top_texture_overrides.csv` 원본을 이번 회차 실제 열어** `anvil`, `chipped_anvil`, `damaged_anvil` 각 leaf 이름 + 40자리 원본 SHA + `template_anvil` 부모 + 윗면 텍스처 이름 3개를 찾았다.

현재 동일한 1.21.11 추출본에서 leaf3 + 부모 `template_anvil.json` 1개, 총 **P1 4개 모델 JSON 원본 경로·Git SHA·JSON 내용**을 직접 다시 읽어 각각 v63/v30 구기록과 일치. 추가 공통 `block/block.json`도 원본 조회. 이번 4개 중 `anvil.json`, `template_anvil.json`은 이미 기존 직접 재검증 플래그가 있었으며, `chipped_anvil.json`, `damaged_anvil.json` **2개만 v35~v63 직접 재검증 범위의 새 고유 모델**에 해당. 신규 모델 **신원 식별 0** (기존 P1 544 모델 path/SHA는 v53에서 연결 완료).

v30 기존 `04_pot_enchant_anvil_9_png_rgba.csv`에 기록된 `anvil`, `anvil_top`, `chipped_anvil_top`, `damaged_anvil_top` PNG SHA와 현재 1.21.11 실제 PNG 바이너리의 Git SHA/16×16 IHDR가 **4개 모두 일치**했다. **v30 과거 RGBA 알파 수치의 Pillow 픽셀 실측은 v63에서 새로 실행하지 않았다.** `00C_ORIGINAL_ANVIL_PNG_4_IHDR_SHA.json` 참조.

## 3. 모루의 정확한 원본 기하·UV·방향

- leaf `anvil`, `chipped_anvil`, `damaged_anvil`은 모두 `parent:minecraft:block/template_anvil`, own elements **0**. 각각 `#top` 슬롯만 다른 상단 텍스처 경로로 대체하고 `#body`는 템플릿의 `block/anvil`을 상속한다.
- 공통 원형 `template_anvil.json`: 원본 **4개 elements, 21면**, 모든 면 원본 명시 UV **21/21**. 상속 적용 leaf **3×21=63면**, 실제 원본 UV 출처명시 **63/63**. 이 중 `#body` 면 **60**, `#top` 면 **3**. `02_ANVIL_ORIGINAL_INHERITED_FACE_63.json`는 각 element.from/to, face, 실제 원본 UV, rotation, cullface, 원본 PNG 경로+SHA까지 보존.
- `blockstates/{anvil,chipped_anvil,damaged_anvil}.json` 3개 파일 원본 SHA 직접 재확인. 각각 `facing=east/north/south/west` **4 variant**, 합계 **12**. JSON 원본에 누락된 south의 `y`를 임의로 `0`으로 원본 필드처럼 기록하지 않음. `uvlock`도 원본 명시 키 없음 (이것은 엔진 UVLOCK 동작을 검증한 결과가 아님).
- **실제 게임 엔진에서의 회전 UVLOCK·광원/방향 출력 검증 미실행**. 이번 결과는 원본 JSON/PNG 원본 경로 대조 및 원본 face UV 근거다.

## 4. 과거 증거 통합: 176 → 179 역사 링크

v62의 21개 선택 CSV **176링크/110고유 P1 모델**을 행 내용·SHA 그대로 보존하고, v30/08의 **3개 원본 모델 이름+SHA 행 증거**를 새로 추가했다. v63 역사 CSV 선택 교차표 **179링크/112개 서로 다른 P1 모델**. 신규 3링크 중 anvil은 이미 원본 v62 역사 연결 보유, chipped·damaged **2개 고유 모델 연결**. 구 v44의 원본 증거 CSV SHA 문자열 오류6링크는 수정/삭제 없이 별도 v62 정정 기록을 유지.

기존 v35~v61 직접 JSON 판독 플래그의 서로 다른 모델 **514**, 이번 신규 고유 모델 **2**를 더해 선택 원장의 **v35~v63 직접 JSON 판독 모델 516개**. 나머지 **28개**는 선택 원본 역사 CSV에서 이름/경로 + 모델 SHA 행이 있으나 v35~v63 명시 직접판독 플래그가 없음. 이들은 원본 모델이 미연구라고 확정할 수 없음. **516/544는 단순 직접 원본 JSON 판독 근거의 집합 크기, 1-2-A 실제 완료율 아님**.

## 5. 원장 무결성·미완료 범위

- P1 누적 증거 원장 **544행×310열 → 544행×325열**, 이전 **310개 열 × 544행 = 168,640 데이터셀 전부 동일**; 신규15열로 v63 모루별 SHA·부모·UV·블록상태·근거 등급 추가.
- 보조 모델별 증거 원장 **544행×24열 → 544행×30열**, 이전 13,056 데이터셀 그대로 보존.
- 본 단계는 실제 바닐라 가구 스타일의 근거를 구축하기 위한 **1-2-A 과거 연구 모집단/증거 통합**. 194파일 중 170은 v62/v63 새 내용 검수 미수행, 셜커13/skull1 특수 렌더 예외, 공식 암시UV 런타임 검증 및 v5~v43 전체 의미론적 결론 통합은 남음.
- 공식 JAR 인증/인게임 런타임 인증은 현재 사용자가 정한 필수 완료조건에 포함되지 않음. 검증 성공을 주장해서도 안 됨.
- **1-1 승인 범위150/150 완료, 상위1/5 완료, 1-2-A/1-2 아직 진행, 실질 완료율 미산정, 실제 마크 가구 제작/좀보이드 변환 미시작.**

다음 채팅 작업 및 저장소 체크포인트: `NEXT_CHAT_HANDOFF.md`, `SUMMARY.json`, `VALIDATION_POST_RESEARCH_COMMIT.json`.
