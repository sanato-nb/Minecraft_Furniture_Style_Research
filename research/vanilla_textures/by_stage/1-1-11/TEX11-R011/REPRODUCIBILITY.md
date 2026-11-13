# TEX11-R011 — 재현 절차 / 근거 계층

1. GitHub 사용자 제공 `1.21.11/` 에서 목재 7종의 `textures/block/<wood>_door_top.png` 및 `*_bottom.png` 총14개, `models/block/<wood>_door_<kind>.json` 56개, 공유 `door_<kind>.json` 8개, `blockstates/<wood>_door.json` 7개를 파싱한다. `kind`는 bottom/top × hinge left/right × open false/true의 8개. 모든 원본 모델/PNG blob SHA는 CSV에 남긴다.
2. PNG의 signature/IHDR 및 모든 chunk CRC32를 확인하고 indexed PLTE/tRNS, DEFLATE, scanline filter 0~4를 복원한다. 14×16×16=3,584개의 기존 원본 RGBA 텍셀. PNG가 신규 추가된 게 아니므로 총 범위 PNG31은 유지한다.
3. 각 leaf의 `textures.top`/`textures.bottom`를 확인하고 template `elements[].faces[].uv`의 `texture=#top/#bottom` 슬롯을 따라 PNG를 결정한다. 모델 UV `[u0,v0,u1,v1]`은 16×16 PNG에 직접 텍셀 대응. 각 uv사각형의 패치 크기는 `|u1-u0|×|v1-v0|`, x/y는 `floor(u0+(u1-u0)(i+0.5)/W)` 및 V 대응. 감소형 U/V는 역순 샘플링.
4. 모델당 기본 geometry `[0,0,0]→[3,16,16]`, face5개. `west/east` 2×256, `north/south` 2×48, `up/down` 1×48 = 656 텍셀 참조/모델. 56모델→280 patches/36,736 source texel references. 168 narrow face patches/8,064 refs는 이전 R008의 넓은 면 UV 연구와 구별되는 신규 source patch. 112 broad face 전체 16×16 RGBA 역시 R011에서 처음 면 전체로 실샘플하며 과거 edge 1행 근거를 중복 독립수로 가산하지 않는다.
5. 각 `blockstates` 32 variant/wood를 leaf와 결합. `rotation_y`는 0/90/180/270° 오른손 좌표 `(x,z)->(z,-x)`로 정적 정상 방향을 계산. `cullface` 부재는 빈 값으로 유지. 224 상태×5=1,120 state-face rows, 146,944 반복 UV 참조; GPU/월드카메라 검증 아님.
6. 동일 facing·hinge·open인 위·아래 모델 7×4×2×2=112쌍에서 vertical-face north/south/west/east 각각 `upper sample patch y=15` vs `lower sample patch y=0`를 비교, RGBA same·alpha 다름·양쪽 alpha>0의 RGB L1 계산. 112×4=448 rows, facing 회전만 제거하면 28 모델쌍×4=112 고유 face 패턴. narrow side는 112×2×3=672 원본 texel-pair 사용, 중복제거하면 28×2×3=168 model-column uses. Broad source seam metrics는 R008과 비교용만.
7. `UV_rotation` 90/270° 및 alpha count/color mean은 별도 기입. RGB 평균과 alpha픽셀 count는 texture-patch 시계 방향 회전에 무관하므로 집계 수치는 유효하지만 실제 GPU 화면의 면 내 무늬 방향은 검증하지 않음.
8. 실제 게임 렌더 F단계는 0/31. 공식 JAR SHA1 인증은 사용자 지정으로 필수 범위 밖. 원본 31개 full-face source 샘플 조사 이후, 실제 인게임 캡처가 필요하면 사용자의 `계속해줘`에 새로운 분석을 꾸미지 말고 중단 이유·자료 요구를 설명.
