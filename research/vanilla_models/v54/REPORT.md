# v54 — 1-2-A 원본 블록상태 역참조·PNG 소스 UV 픽셀 조사

> 2026-11-14 KST. 시작 main HEAD 300b3ddc89130121379061ca7c4081d738a5998c. Minecraft Java 1.21.11 추출 원본을 기준으로 했으며 v1~v53 연구 증거를 보존한다.

## 1. 직접 수행한 블록상태 원본 조사

v53 신규 P1 모델 175개의 정확한 모델명과 해당 블록상태 이름을 연결하여 관련 원본 blockstates JSON 경로 **57개**를 선정했다. v53에서 이미 직접 검사한 **8개는 이전 조사**로 남겨 두고, 나머지 **49개를 v54에서 GitHub 원본 파일로 직접 읽고 SHA를 검증**했다. 이 57개에는 **원본 variants 키 225건, model apply 기록 225건, multipart 규칙 0건**이 있다. model apply 기록을 독립 월드 상태나 완성 모델 수로 환산하지 않는다.

추가로 **명명된 skull/head 블록상태 원본 14개**의 서로 다른 경로를 직접 조사했다. skeleton_skull, skeleton_wall_skull, wither_skeleton_skull, wither_skeleton_wall_skull, zombie_head, zombie_wall_head, creeper_head, creeper_wall_head, player_head, player_wall_head, dragon_head, dragon_wall_head, piglin_head, piglin_wall_head. 14개 원본 JSON은 모두 기본 variant에서 minecraft:block/skull 모델을 참조한다. 경로는 14개이지만 **Git blob SHA는 전부 동일한 3951e3eea59612d4049577042a176de31d1ed88c**이다. 기존 skull이라는 이름의 독립 블록상태 경로가 없다는 사실은 skull 모델이 미사용이라는 근거가 아니었다.

| 원본 상태 출처 | 파일 경로 | 원본 variants | model apply |
|---|---:|---:|---:|
| v53 직접 확인 보존 | 8 | 58 | 58 |
| v54 새 가족 상태 원본 | 49 | 167 | 167 |
| v54 skull/head 이름별 새 원본 | 14 | 14 | 14 |
| **합계** | **71** | **239** | **239** |

가족 상태 57개의 모델 참조는 v53 신규 모델 **172/175개**를 직접 가리킨다. skull/head 상태 14개가 참조하는 skull.json 1개를 추가하여 **173/175개 직접 블록상태 모델 참조**를 확인했다. 직접 참조되지 않는 2개는 피스톤 헤드의 **기하 부모 템플릿**인 template_piston_head.json, template_piston_head_short.json이다. 원본 상태에서 별도로 참조되는 lightning_rod_on.json의 실제 모델 파일 SHA **1796303bb2d31f17a491f1e9fe1f4b43b653befb**도 검사했으나 이미 P1 원장에 있는 원본 모델이라 신규 모집단으로 세지 않는다.

## 2. 피스톤 텍스처 슬롯 재검증

v53 원본/상속 면 기록에서 피스톤 모델별 face **60건**을 다시 분리했다. 두 부모 템플릿은 자식이 채울 슬롯을 남기기 때문에 부모 단독일 때 **20건 미해결**이다. 피스톤 헤드 leaf 4종에는 상속된 **각 10면 × 4 = 40면의 텍스처 경로가 전부 해석**, 미해결 0건이다. **부모 템플릿의 플레이스홀더를 leaf 오류라고 판정할 수 없다.** 실제 texture PNG나 게임 렌더 결과의 완전 무결성 검사는 별도로 남아 있다.

## 3. 실제 원본 PNG 바이트와 face UV 영역의 RGBA 픽셀 샘플링

기존 v53에서 실제 Git SHA와 Pillow RGBA로 검증한 원본 PNG 중 brown_candle.png, cyan_candle_lit.png, purple_wool.png **3개**의 실제 텍스처를 이번에는 모델별 면의 **원본 명시 UV 좌표**와 연결했다. 다른 UV 영역은 **16개**, 해당 원본 영역을 참조한 상속 적용 모델별 면은 **226개**였다.

| 원본 PNG | 모델별 face 참조 | 고유 UV 사각형 | 반복 포함 픽셀 관측 | 중복 제거 원본 텍셀 좌표 |
|---|---:|---:|---:|---:|
| brown_candle.png | 110 | 7 | 580 | 21 |
| cyan_candle_lit.png | 110 | 7 | 580 | 21 |
| purple_wool.png | 6 | 2 | 576 | 256 |
| **합계** | **226** | **16** | **1,736** | **298** |

1,736건의 반복 적용 원본 UV 영역 내 픽셀 모두 alpha=255로 확인했다. 이는 **원본 PNG의 선언된 UV 범위 내부에 있는 소스 픽셀을 실제로 읽었다**는 증거다. U가 뒤집힌 [1,5,0,6] 같은 UV는 사각형의 최소·최대 범위를 정렬해 픽셀을 관측했다. 따라서 UV 방향·게임 렌더러의 보간·회전·조명·mipmap·화면 픽셀까지 검증했다는 뜻은 아니다. 별도 lightning_rod.png는 v53에서 바이너리 SHA/RGBA를 검증했으나 이번 신규 모델 적용 면에서 그 파일 경로를 가리킨 참조는 0건이다.

재현 프로그램 [REPRODUCE_SOURCE_PNG_UV_RECTANGLES.py](REPRODUCE_SOURCE_PNG_UV_RECTANGLES.py)은 실제 추출 원본 자산이 있는 로컬 저장소에서 Git blob SHA를 독립 재계산하고 Pillow RGBA로 각 명시 UV 사각형 픽셀을 측정한다.

## 4. 근거를 보존하는 연구 경계

- P1 모집단은 **544개 원본 모델 경로**, 이들의 typed path+SHA 연결은 **544/544**로 유지된다. 원본/인수인계 기록은 이전 v53 파일을 고치지 않고 v54 별도 폴더와 **544행/185열 원장**에 기록했다. 이전 v53의 169개 필드와 값은 보존하고 16개 열을 추가했다.
- 셜커 상자 13개와 skull 모델 1개의 **실제 렌더러/기하 미확인 14개**는 그대로 남는다. skull 원본 상태의 **모델 참조** 검증이 실 렌더 기하의 존재를 입증하지는 않는다.
- 이번 **71개 블록상태 경로**는 v53 신규175 모델 관련 범위이다. 전체 P1 544개 모델/전체 2,390개 모델의 기하·UV·PNG·블록상태 전수 완성을 의미하지 않는다. v1~v53의 모든 의미론적 역사 기록을 전수 재검토하지도 않았다.
- **1-1 승인 150/150 완료, 상위 5개 단계 중 1/5 완료 유지**. 1-2-A와 1-2 심층 연구는 **미완료**, 실질 전체 완료율 **미산정**. 마크 가구 제작 및 좀보이드 가구 변환은 시작하지 않는다.

## 5. 검증 자료

[P1 544행 최신 원장](01_P1_544_EVIDENCE_LEDGER.csv) · [신규 49개 원본 blockstates](02_ORIGINAL_BLOCKSTATES_NEW_49.json) · [57개 원본 경로 SHA](03_BLOCKSTATE_SOURCE_57_INDEX.csv) · [variants 225](04_BLOCKSTATE_VARIANT_APPLY_225.csv) · [175개 모델 블록상태 역참조](05_P1_175_BLOCKSTATE_REVERSE_LINKS.csv) · [skull/head 14 및 피뢰침 모델 원본](06_SPECIAL_SKULL_14_AND_POWERED_ROD_MODEL.json) · [피스톤 face 슬롯 60](07_PISTON_TEMPLATE_AND_CHILD_FACE_SLOTS_60.csv) · [PNG UV 고유 16개 원본 샘플](08_ORIGINAL_PNG_UV_RECTANGLE_RGBA_16.json) · [원본 face 픽셀 226건](09_SOURCE_PNG_FACE_UV_PIXELS_226.csv) · [Python 재현 코드](REPRODUCE_SOURCE_PNG_UV_RECTANGLES.py) · [인수인계](NEXT_CHAT_HANDOFF.md).
