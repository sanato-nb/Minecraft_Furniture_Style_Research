# TEX05-R004 — 정적 리소스·셰이더의 증거 범위

> 자료 우선순위: 사용자 제공 `sanato-nb/Minecraft_Furniture_Style_Research/main/1.21.11/`. 4개 신규 소스 파일 모두 기존 InventivetalentDev `1.21.11` 미러와 Git blob SHA 및 읽은 원문 동일. **인게임 실행/블렌딩 증거로 간주하지 않음.**

## 1. 유리 텍스처의 .mcmeta와 아틀라스

- 사용자 추출본 `assets/minecraft/textures/block/glass.png.mcmeta` 파일을 직접 읽고 JSON `{"texture":{"mipmap_strategy":"mean"}}` 확인. Git blob: `5cb0fb739d59e745149bd602cc0d3cc2ee4f2d5b`.
- 동일한 경로 규칙으로 `red_stained_glass`, `black_stained_glass`, `blue_stained_glass`, `green_stained_glass`, `white_stained_glass`의 `*.png.mcmeta`를 각각 검색했으나 5/5 GitHub `404 Not Found`. **메타 파일 부재**를 '기본값은 어떻다'라고 해석하지 않음.
- `assets/minecraft/atlases/blocks.json`의 `sources` 중 `{"type":"minecraft:directory","prefix":"block/","source":"block"}` 확인. 이미 확인한 6 leaf 모델의 `minecraft:block/<id>` 정적 텍스처 ID가 `block/` 경로 규칙과 합치. **실제 아틀라스 배치 좌표, 패딩, 샘플링 방식은 이 JSON에 없음**.
- `mean`의 구체 연산 정의·실제 mipmap level/샘플링 결과는 **해당 .mcmeta만으로 증명할 수 없음**.

## 2. 일반 블록 셰이더 정적 코드

- `assets/minecraft/shaders/core/block.fsh`에서 `uniform sampler2D Sampler0`, `texture(Sampler0, texCoord0) * vertexColor * ColorModulator`, 조건부 `#ifdef ALPHA_CUTOUT` 하의 `color.a < ALPHA_CUTOUT` 및 `discard`, `apply_fog(...)`를 직접 확인.
- `assets/minecraft/shaders/core/block.vsh`에서 `in vec2 UV0`, `in ivec2 UV2`, `texCoord0 = UV0`, `vertexColor = Color * minecraft_sample_lightmap(Sampler2, UV2)`, `ProjMat * ModelViewMat`을 확인.
- **확정된 것:** 게임 자료에 이들 일반 블록 셰이더 코드가 존재하고 위 텍스트 조건이 선언됨.
- **확정되지 않은 것:** 여섯 유리의 실제 패스가 이 셰이더를 채택하는지, `ALPHA_CUTOUT`이 활성화되는지/값이 얼마인지, 블렌드 식/투명 순서/인접 면 제거/시각 조명 값. 이는 런타임·렌더 상태·호출 코드/실측 없이는 결론 내릴 수 없음.
- 그러므로 R001/R002 픽셀 알파 분포와 셰이더의 `discard`를 결합해 **실제 월드에 투명 픽셀이 폐기된다고 단언하면 오류**.

## 3. 기존 모델과 연결되는 범위

R003에서 검증한 `blockstate → leaf model → cube_all → cube → block`와 이번 아틀라스의 `block/` 디렉터리 규칙은 정적 참조에 관한 **추가 연결점**이다. R001의 36개 면/UV, R002의 경계·반복, R003의 27개 파일은 신규 텍스처·화소 연구량으로 중복 합산하지 않는다.

## 4. 4층 증거 분리

1. 사용자 제공 추출본: 신규 **4개** 정적 파일 직접 검사; R003의 27개와 합친 서로 다른 정적 경로 **31개**. 별도 메타 부재 질의 5건은 파일 수가 아님.
2. 비공식 미러: 4/4 신규 파일의 Git blob SHA+원문 일치. 누적 31/31 경로 내용 지문 교차 검증.
3. Mojang 공식 배포 JAR 전체 SHA-1/공식 메타데이터: **미완료**.
4. 인게임 정적 투명 레이어/정렬/면 컬링/조명: **미완료**.

애니메이션·Project Zomboid 변환·실제 가구 3D 모델링은 포함하지 않는다.
