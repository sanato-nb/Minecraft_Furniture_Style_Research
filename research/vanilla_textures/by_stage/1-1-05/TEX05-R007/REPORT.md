# TEX05-R007 — Minecraft 1.21.11 정적 terrain 셰이더 및 리소스 include 연결 검증

> 2026-11-13 · 1-1-05 유리 6개 고정 표본 · 사용자 추출 JAR 우선 · TEX05-R001~R006 / 전역 v38 불변

## A — 중복 없는 다음 근거 확인
- 최신 라이브 STATE에서 `TEX05-R006`/다음 `TEX05-R007`을 확인하고 R006 결과(20 RGBA 색 엔트리, 384개 가상 2×2 혼합)와 기존 R004 일반 block shader 원문을 읽었다.
- 새로운 픽셀 수, 고유 텍스처 수, 모델 UV 면 수를 늘리지 않았다. 이전 6개 PNG / 1,536 RGBA / 36면 정적 UV / 기존 정적 파일 31개는 모두 계승.
- **R004에서 아직 직접 감사하지 않았던 별도 `terrain.fsh`, `terrain.vsh`, 관련 GLSL include 4개**를 정적 자원 원문으로 직접 읽고 차이를 분석. 신규 서로 다른 실제 파일 경로 6개 → 본 단계 누적 정적 검증 경로 **37개**.

## B — 1차 자료 및 비공식 미러 독립 대조
- 사용자 저장소 `1.21.11/assets/minecraft/shaders/core/terrain.fsh`, `terrain.vsh`, `shaders/include/chunksection.glsl`, `globals.glsl`, `fog.glsl`, `projection.glsl` **6/6 원문 읽기**.
- 미러 `InventivetalentDev/minecraft-assets`의 ref `1.21.11` 대응 파일 6개를 각각 다시 조회: 사용자 Git blob SHA와 **6/6 정확히 동일**. 파일 경로·개별 SHA·텍스트 길이는 `SOURCE_LEDGER.csv`.
- `terrain.fsh`에 import 3개 (`fog`, `globals`, `chunksection`), `terrain.vsh`에 import 4개 (`fog`, `globals`, `chunksection`, `projection`)를 확인해 관련 정의를 사용자 추출본에서 **7/7 정적 참조 해소**. 새로 읽은 원문 import graph는 `TERRAIN_IMPORT_GRAPH.csv`.
- Git blob SHA 일치는 버전이 다른 파일의 우연한 이름 유사성이 아니라 파일 바이트 일치의 증거이지만 **Mojang 공식 JAR 전체 인증 또는 실제 렌더 실행 증거는 아님**.

## C/D — 유리 PNG·미프맵·텍스처 샘플링 근거 분리
- R006 이전 PNG의 RGBA/알파·팔레트 측정은 계승. 이번에 새 PNG를 읽거나 신규 픽셀을 계산한 것이 아니다.
- **`terrain.fsh` 원문에 존재하는 코드:**
  - `sampleNearest`는 texel center/offset을 보정하고 실제 샘플 함수로 `textureGrad`를 호출.
  - `sampleRGSS`는 `dFdx`, `dFdy`로 파생값을 계산하고 네 오프셋 `(0.125,0.375)`, `(-0.125,-0.375)`, `(0.375,-0.125)`, `(-0.375,0.125)`에서 각각 `textureLod`를 호출해 상·하위 mip level의 값을 혼합.
  - `mipLevelExact = max(0, log2(effectiveDerivative / minPixelSize))`와 `floor`, `fract`를 사용. `smoothstep(minPixelSize*1, minPixelSize*2, maxTexelSize)`로 nearest/RGSS 사이 혼합 계수를 계산.
  - `main`의 `UseRgss == 1` 여부로 RGSS와 nearest 함수를 분기. `TextureSize`는 `ChunkSection`, `UseRgss`는 `Globals`에서 정적 선언.
- **명확한 경계:** `textureLod`에서 읽을 mip level을 선택하는 소비/샘플링 코드가 확인되었다는 뜻이지, `glass.png.mcmeta`의 `mipmap_strategy="mean"`을 생성하는 알고리즘을 찾았다는 뜻은 아님. R005/R006의 가상 2×2 proxy는 실제 엔진과 일치한다고 입증되지 않았다.

## E — 지형 shader vs 일반 block shader, UV/월드 좌표/광원 소스 비교
- 기존 `block.fsh`: `texture(Sampler0, texCoord0)*vertexColor*ColorModulator`. 신규 `terrain.fsh`: RGSS 조건부 또는 nearest sampler의 결과 `*vertexColor`; `ChunkVisibility`를 사용한 FogColor 혼합이 추가로 명시됨.
- **둘 다** `#ifdef ALPHA_CUTOUT`에서 `color.a < ALPHA_CUTOUT`을 검사하는 조건부 `discard`를 포함하며 `apply_fog`를 호출. 실제 유리가 어느 셰이더를 호출하는지/이 매크로를 활성화하는지는 확인되지 않음.
- 기존 `block.vsh`: 위치 계산에 `Position + ModelOffset`. 신규 `terrain.vsh`: `Position + (ChunkPosition - CameraBlockPos) + CameraOffset`. `ChunkSection`과 `Globals` 원문으로 변수 출처 확인.
- 두 vertex shader 모두 `UV0 → texCoord0` 및 `Color * minecraft_sample_lightmap(Sampler2, UV2)`를 명시. 그러나 블록별 atlas UV rect, 실제 광량, 최종 프레임/컬링 결과는 정적 소스로 확정할 수 없음.
- 정적 차이 11건은 `BLOCK_VS_TERRAIN_SHADER.csv`에 비교 기록.

## F — 정적 소스에 의한 과잉 확정을 금지
- 실제 Minecraft 게임 실행, 스크린샷, GPU 측정 자료 **0건**. 여섯 원본에 대한 **인게임 정적 렌더 검증 0/6** 유지.
- 특정 glass 블록이 `terrain.fsh` 또는 `block.fsh`를 실제로 사용하는지, 알파 컷아웃 define/threshold, 블렌드/정렬, 인접한 유리 면 컬링, 텍스처 atlas 및 mipmap 생성 수식은 본 자료만으로 결론 내릴 수 없음.
- Mojang 공식 전체 client.jar SHA-1/배포 메타데이터 인증은 사용자 정책상 **out of scope**. 애니메이션·PZ 변환·가구 3D 제작 제외.

## G — 연구 결과와 재현
- `SOURCE_LEDGER.csv`: 신규 6개 원본 경로 및 미러 SHA.
- `TERRAIN_IMPORT_GRAPH.csv`: 사용자 자료로 실제 연결을 확인한 7개 import edge.
- `BLOCK_VS_TERRAIN_SHADER.csv`: 일반 블록 소스와 terrain 소스의 11개 정적 구현 대조.
- `REPRODUCE_SHADER_AUDIT.py`: 사용자 클론의 실제 원문을 읽어 SHA/선택 코드/참조를 독립 재검사.
- `SUMMARY.json`: 신규/계승 성과와 미완료 경계를 별도로 기록.

### 다음 검증 요구
이 시점까지 PNG·모델 JSON·blockstate·36개 정적 UV·아틀라스·셰이더의 자원 수준 확인을 수행했다. 실제 유리 월드 화면 및 GPU 바인딩의 검증은 아직 필요하다. **새로운 정적 근거를 못 찾으면 R008을 억지로 만들지 말고 사용자에게 Minecraft 1.21.11 실제 정적 스크린샷과 테스트 조건을 요청해 중단**한다.
