# R010 재현 가능한 검증 방법

1. `1.21.11/assets/minecraft/textures/block/{oak,spruce,birch,cherry,bamboo}_shelf.png` 원본을 바이너리로 열어 PNG 전 chunk CRC, indexed PLTE/tRNS, zlib/DEFLATE, scanline filter를 읽는다. 5×32×32=5,120 source texels. 5종 원본 모두 alpha=255만 존재.
2. `models/block/template_shelf_body.json`는 3요소·15면, `template_shelf_{center,left,right,unconnected,unpowered}.json`는 각 1개 평면·북면. 5재질의 6개 model leaf JSON씩 총30개 원본 parent와 `textures.all` 슬롯을 검증한다.
3. Minecraft 모델 face `uv=[u0,v0,u1,v1]`은 16 단위 좌표로 표현되므로 PNG32×32에서는 원본 픽셀 좌표를 **2배** 해서 샘플링한다. 폭=abs(2u1−2u0), 높이=abs(2v1−2v0). UV가 감소하면 역방향 nearest-neighbor로 실제 픽셀을 샘플링한다. `UV_rotation` 및 `cullface` 키는 원본으로 저장. 투명/불투명 수는 UV 회전 순서에 영향 받지 않는다.
4. `blockstates/<wood>_shelf.json`의 `multipart` 24규칙/wood를 그대로 계산: facing 4 × powered 2 × side_chain 4 = 32 논리 상태/wood. `when.AND` 조건을 평가해 모델2개(본체1+전면1)씩 매칭한다. 5wood×32=160 소스 상태; 각 state 본체15면+front1면=16면; 2560 face projection uses. 미전원 side_chain 4개가 동일 전면 템플릿을 선택하므로 model-name/yaw signature는 20/wood, 전체100.
5. `SHELF_MODEL_FACE_RGBA.csv` 100건(본체75,전면25), `SHELF_STATIC_STATE_ASSEMBLIES.csv` 160건, `SHELF_STATE_FACE_PROJECTION.csv` 2560건은 동일 물리 PNG 원본을 중복 참조한다. R007 원본 35 sampled face patches는 **새 65개 면에 다시 가산하지 않는다**.
6. Geometry 기준: front overlay Z13 plane, X[0,16], Y[4,12]. shelf_body Z[13,16]는 북쪽 face 미기재, shelf_bottom Y[0,4], shelf_top Y[12,16]의 경계에 front plane이 딱 맞는다. 출처 JSON 25개 overlay에서 8 invariant 검사. Runtime z-fighting의 부재를 주장하지 않는다.
7. 패널 경계 후보: atlas UV 내 16×8 pixel samples의 왼쪽 패널 x15 및 오른쪽 패널 x0의 8행 RGB L1 비교. "second horizontal flip" 대안은 오른쪽 패널 x15를 대신 비교. `left→center`, `center→center`, `center→right`, `left→right`, `unconnected→unconnected`의 5 가상 인접 유형×5wood=25. 이 수치로 Minecraft에서 실제로 어느 쪽이 왼쪽인지 판정하지 않는다.
8. **실제 인게임 화면 미확보 0/31**. Mojang 공식 JAR SHA1은 사용자 지시로 필수 범위 제외. 애니메이션, 변환·3D 모델 제작, v38과 다른 stage 수정 금지.
