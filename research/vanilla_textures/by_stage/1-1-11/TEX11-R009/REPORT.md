# TEX11-R009 — 12종 다락문 192 정적 상태의 모든 면 UV·RGBA 투영

**2026-11-13 / 단계 1-1-11 / 이전 TEX11-R008 / 다음 TEX11-R010**

## 출처와 검증 범위
사용자가 Minecraft Java 1.21.11 설치본 JAR에서 직접 추출했다고 제공한 GitHub `1.21.11/`의 실제 **12종 trapdoor blockstate JSON, 36종 leaf model JSON, 6종 공유 template model JSON, 12종 원본 PNG**를 직접 재조회·파싱하였다. PNG 12개는 실바이트 CRC, zlib/DEFLATE, palette/tRNS, scanline filter를 통해 16×16 RGBA를 다시 디코딩했다. **공식 Mojang client.jar SHA-1 인증은 사용자 결정에 따라 완료 요건에서 제외**되며 인증되었다고 주장하지 않는다.

**기존 불변 누적 자료:** scope PNG 31, leaf 127, blockstate 원본 규칙 512, 정적 상태 544, model instance 672, 방향 면 4,320, 문 기하 쌍 112, R007 다락문 UV 선택 면 36, R008 다락문 12종 대칭. 이번에 새 PNG 12개가 추가된 것은 **아니며 기존 PNG의 재검사**이다. 역사적 v38 참나무 선반 32상태는 중복 산입하지 않았다.

## A. 192 블록상태 × 실제 모델의 여섯 면 전수 조사
- **12재질×16 blockstate variant = 192 정적 상태**를 원본 state JSON에서 읽고 각 모델의 `north/south/west/east/up/down` **여섯 면**, 총 **1,152 상태·면 기록**을 생성했다. 블록상태 `x/y` 회전 후 면 법선과 cullface 방향을 계산했고, 192개 상태에서 각 6개 법선이 유일하게 남는지 검사해 **192/192 통과**하였다.
- 재질 12×모델 kind 3(`bottom/top/open`)×면 6=**216개의 모델별 UV 패치**를 실제 원본 PNG의 RGBA 픽셀로 샘플링했다. 각 모델의 16×16 넓은 면 2개와 16×3 또는 3×16 얇은 면 4개를 합하면 **704 UV texel 참조/모델**, 12×3 모델=**25,344 UV 참조 사용**. 192 상태로 반복 투영한 총 **135,168 참조 사용**은 새로운 독립 원본 텍셀 수가 아니다.
- R007은 다락문 각 material의 bottom-up/top-down/open-north **36개의 넓은 면 패치**만 실제 샘플링했다. 이번 R009의 **완전히 새로운 모델·면 패치 180개, 해당 UV 참조 16,128회**를 정확히 구분한다. `TRAPDOOR_MODEL_FACE_UV_RGBA.csv` 216행, `TRAPDOOR_STATE_192_FACE_PROJECTION.csv` 1,152행에 원본 Git blob SHA, 모델 JSON UV/UV-rotation, 투명·불투명 수, world normal/cullface, blockstate x/y를 기록했다.
- **얇은 모서리 패치 144개에는 완전 투명(alpha=0) 픽셀 0개**, 부분 투명(0<alpha<255) 0개. 216 패치 모두 부분 투명 픽셀 없음. **넓은 면 72개 중 48개**에 알파 0이 있는 면이 있었고, 4개 목재(spruce/birch/dark_oak/pale_oak)는 PNG 전체가 불투명. 이것은 **모델 UV로 지정된 원본 픽셀의 속성**이지 게임에서 모든 측면이 보인다는 의미가 아니다.

## B. 일반형 2종과 방향형 10종의 상단 열린 상태 회전 차이
- **일반 template_trapdoor 계열:** `oak`, `dark_oak`. `open=true`에서 `half=top`의 X회전은 4방향 모두 **0°**.
- **template_orientable_trapdoor 계열:** 나머지 **10종**. `open=true, half=top`의 X회전은 **각 방향 180°(총 40 state variants)**, `open=true,half=bottom`은 X0°. 상단 open의 Y각은 나머지 방향 보정에 맞춰 변경된다.
- 두 종류 모두 열린 상태 모델 `north`의 **수학적 world face normal**이 상단/하단에서 같은지 `12×4=48쌍` 검사했고 **48/48 일치**. 이는 모델 정상 방향의 정적 수학 투영이며 실제 게임 화면에서 전·후 텍스처가 보이는지 확인한 것은 아니다.

## C. PNG 이미지 180° 회전에 따른 투명 구멍 패턴
- 직접 디코딩한 PNG에서 `RGBA(x,y)`와 `RGBA(15−x,15−y)`를 비교. **3,072 source pixel·rotated pixel 대조**이며 이미지의 수학적 회전 감도 지표. 아래 값은 **상단 open 게임 화면을 확정 렌더링한 결과가 아니다**.
- **warped_trapdoor: alpha 불일치 38/256**, **jungle_trapdoor: 20/256**. 다른 10종은 alpha 불일치 **0/256**. 단, 12종 모두 180° 회전 전·후 RGBA가 완전히 동일한 것은 아니다(색상·나뭇결 차이).
- 방향형 10종의 상단 open X180° 회전은 세계좌표에서 면의 텍스처 방향 차이를 만들 수 있으므로, warped/jungle은 **실제 게임 화면 후보 검증 우선순위**를 높였다. 다른 요소, 카메라, UV-lock, culled-face, 색 변환을 검증하지 않았으므로 오류로 단정하지 않는다.

| 원본 trapdoor | 템플릿 종류 | 열린 상단 X180 /4 | 투명 픽셀 /256 | 180° alpha 차이 /256 | 180° RGBA 일치 |
|---|---|---:|---:|---:|---:|
| oak | 일반 | 0/4 | 36 | 0 | 132/256 |
| spruce | 방향형 | 4/4 | 0 | 0 | 92/256 |
| birch | 방향형 | 4/4 | 0 | 0 | 84/256 |
| dark_oak | 일반 | 0/4 | 0 | 0 | 88/256 |
| bamboo | 방향형 | 4/4 | 44 | 0 | 162/256 |
| acacia | 방향형 | 4/4 | 60 | 0 | 132/256 |
| cherry | 방향형 | 4/4 | 36 | 0 | 106/256 |
| mangrove | 방향형 | 4/4 | 32 | 0 | 170/256 |
| pale_oak | 방향형 | 4/4 | 0 | 0 | 82/256 |
| crimson | 방향형 | 4/4 | 40 | 0 | 136/256 |
| warped | 방향형 | 4/4 | 55 | 38 | 108/256 |
| jungle | 방향형 | 4/4 | 42 | 20 | 124/256 |

## 관측과 결론의 한계
- 31 PNG 중 **실제 Minecraft 게임에서 정적 렌더 이미지로 검증된 수 0/31**. 이 연구의 192 상태·1,152 면·25,344 원본 UV 참조는 GPU 렌더링, 색상 필터·실제 컬링, 알파 테스트·가림·광원 검증이 아니다.
- `TRAPDOOR_ROT180_ALPHA.csv`, `TRAPDOOR_ALPHA_MASK_180.svg`에는 warped/jungle의 마스크와 180° 변환 차이를 정적 증거로 남겼다. SVG는 게임 스크린샷이 아니다.
- R001–R008의 불변 릴리스는 수정하지 않고, 다른 단계 및 전역 v38은 건드리지 않는다. 애니메이션 전면 보류, PZ 변환 및 실제 가구 모델 제작 제외.

## 다음 TEX11-R010
스크린샷이 없더라도 별개로 남아 있는 **5종 32×32 shelf atlas의 모든 front/body/connection 조합별 정적 면 UV·모서리 텍셀·실화소 반복/접합 연구** 등은 원본만으로 계속 가능하다. 실제 인게임 판정이 필요한 순간에는 사용자에게 정확히 어떤 재질·상태·스크린샷이 필요한지 요청하고, 그 전에는 인게임 검증 0 유지.
