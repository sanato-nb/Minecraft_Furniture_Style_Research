# TEX11-R008 재현 규약 / 근거 계층

## 1. 입력 재현
1. 사용자 제공 추출본 `1.21.11/assets/minecraft/blockstates/<wood>_door.json`의 7재질×32 variants를 읽고, `facing`, `half`, `hinge`, `open`을 정확히 파싱한다.
2. 해당 재질의 `minecraft:block/<wood>_door_bottom_left[_open]` 등 8종의 parent 템플릿(`door_bottom_left`, `door_top_left`, `door_bottom_right`, `door_top_right` 및 open 변형)을 사용한다. R004는 56 리프를 이미 확인했으므로 이번에는 템플릿 8개·블록상태 7개를 직접 다시 열었다.
3. R007 `DOOR_SEAM_PIXEL_DETAIL.csv`에 남긴 7재질×16열의 `top_y15_RGBA`와 `bottom_y0_RGBA` 값을 읽는다. 이번 R008은 **동일 PNG 픽셀을 두 번째로 독립 실측했다고 주장하지 않고**, 새 원본 모델 UV/회전/cullface로 변환·투영한다.
4. 두께3 범위(원본 template 요소 from [0,0,0] to [3,16,16])의 폭 넓은 **west/east face**에 대해 `uv0/uv2` U 축 방향을 비교한다. 방향이 음수이면 역순 U 좌표로 실제 원본 픽셀 값을 샘플한다.
5. `y=90`일 때 북·동·남·서 변환은 수학적 오른손좌표계 `(x,z)→(z,-x)`을 사용. 이것은 **검사용 규약이지 엔진 화면 인증이 아니다**.
6. 112 (7wood×4facing×2hinge×2open) 하단·상단 상태 쌍×2 넓은 면=224 상태·면행; 4facing에 같은 원본 패턴이 투영되므로 7wood×2hinge×2open×2면×16열 = 896 고유 구성-열 결합 사례만 CSV 픽셀 행으로 따로 보존한다.
7. 각 16열에서 `alpha(top[15,x]) != alpha(bottom[0,x])`인지 검증한다. RGB L1은 두 texel 모두 alpha>0일 때만 측정. 4개 원본 차이열은 방향 투영 중 중복 등장하며 독립 결함 수로 합산하지 않는다.

## 2. 다락문 투명·비대칭 재현
1. `1.21.11/assets/minecraft/textures/block/*_trapdoor.png` 원본 12종(각16×16)의 PNG IHDR, 모든 chunk CRC, zlib/DEFLATE, PLTE/tRNS 및 필터별 scanline을 읽어 RGBA 배열을 만든다.
2. 각 (x,y)에서 `alpha(x,y)`와 `alpha(15-x,y)`, `alpha(x,15-y)`를 비교한다. RGB/RGBA는 **색상 전체 채널**로 따로 비교한다.
3. RGB L1 수치는 투명 픽셀의 RGB도 포함하는 원본 바이트 차이로, 화면상 관찰 가능한 색 차이가 아니다.
4. R007 `UV_ORIENTATION_CANDIDATES.csv`에서 다락문 별도 대칭 필드가 빠진 결함은 R008 새 CSV로 보완하며 R007 불변 파일은 덮어쓰지 않는다.

## 3. 완료로 보지 않는 것
- 게임에서의 yaw/hinge/half/open 상태 증거, GPU의 3D 면 정렬·실제 카메라 가림·알파 렌더 및 조명 등 **실제 인게임 확인은 0/31**.
- 공식 JAR SHA-1 인증은 사용자 결정에 따라 필수 범위 밖이며 인증 성공을 의미하지 않는다.
- v38 oak_shelf 역사적 기록, 다른 단계 문서/STATE/HANDOFF, 애니메이션 기록 수정 없음.
