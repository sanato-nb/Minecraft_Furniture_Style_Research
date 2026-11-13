# TEX11-R009 — 재현 규약

- **원본:** `1.21.11/assets/minecraft/blockstates/*_trapdoor.json` 12개, `models/block/*_trapdoor_{bottom,top,open}.json` 36개, 6종 `template_(orientable_)trapdoor_*.json`, `textures/block/*_trapdoor.png` 12개. 모든 외부 입력의 Git blob SHA는 CSV에 보존.
- **PNG:** CRC32(모든 PNG chunk), PNG 타입(대체로 indexed)과 palette/tRNS, DEFLATE, filter 0~4를 재구성. **원본 16×16 실제 RGBA 12×256=3,072개**. 새 texture 12종 추가가 아니라 기존 12종 재조회.
- **각 모델·면:** 원본 element.faces UV `[u0,v0,u1,v1]`의 U/V 두 끝을 직접 읽고 샘플 영역 폭 `abs(u1-u0)`, 높이 `abs(v1-v0)`; 각 픽셀 중심 `floor(u0+(u1-u0)(i+0.5)/width)` 등으로 원본 텍셀 인덱스 조회. UV의 90° 필드 회전은 `UV_rotation`에 따로 기록(불투명·투명 개수는 순서 회전에 불변). 상하/좌우 반전 역시 실픽셀 배열에서 샘플링. `[0,0,16,16]`과 `[0,16,16,0]` 같은 경로를 문자열이 아닌 실제 sample sequence로 취급.
- **면 합계:** 각 bottom/top/open template의 16×16 면 2개(512참조)와 얇은 면 4개(4×48=192) = 704참조/모델. 12×3×6=216 모델·면 패치, 12×3×704=25,344 모델·면 참조. R007의 bottom-up/top-down/open-north 36개×256=9,216참조를 제외하면 180새 면 패치 /16,128참조. 고유 물리 원본 픽셀은 늘어나지 않는다.
- **state:** blockstate variants 12×16=192, 6개 면 각=1,152 상태·면. 상태 x축 회전 후 y축 회전 순서를 수학적 좌표 변환 규약으로 사용했다. 오른손 모델 normal `north=(0,0,-1)`, `east=(1,0,0)`, `up=(0,1,0)`; x=180은 `(x,y,z)->(x,-y,-z)`, y=90은 `(x,y,z)->(z,y,-x)`. normal/cullface는 이 기준의 **source-derived projection**이며 Minecraft 게임 화면 확인 아님.
- **회전 대칭:** source RGBA 배열에서 `(x,y)`와 `(15-x,15-y)`의 RGBA 및 alpha를 비교. 모든 256픽셀×12 PNG=3,072 비교 사용. 180도 이미지 회전은 `open=true,half=top`의 x=180 source state와 관련해 **후보를 조사하는 검사용 가설**이며 실제 OpenGL 텍셀 방향을 인증하지 않는다.
- **보류:** 렌더링 없는 마스크 및 UV 검사로는 게임 가림·컬링·텍스처 회전의 최종 시각 판정이나 인게임 completion을 올릴 수 없다. 공식 JAR SHA1은 사용자 지정으로 필수 범위가 아님.
