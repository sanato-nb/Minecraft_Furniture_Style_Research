# TEX10-R005 — 잎·식생 8개: 아이템 tint 상수, 실제 PNG 투명 청크, 지형 셰이더 색상·컷아웃 경로 교차 검증

> 2026-11-13 · Minecraft Java 1.21.11 · GitHub 사용자 제공 JAR 추출 디렉터리 `1.21.11/` 직접 조회. **대상 8 PNG 유지, 인게임 정적 0/8**. 사용자 요청으로 Mojang 공식 전체 JAR SHA-1 인증은 필수 검증에서 제외(공식 인증 성공이 아님). 기존 R001–R004 및 전역 v38 불변.

## 새 조사 범위와 기존 결과 계승 구분

신규 **고유 16경로**를 직접 읽었다: `assets/minecraft/items/{id}.json` 8개, `models/item/vine.json`·`item/generated.json` 2개, `shaders/core/terrain.vsh`·`terrain.fsh` 2개, 셰이더 import `fog.glsl`, `globals.glsl`, `chunksection.glsl`, `projection.glsl` 4개. R003–R004 32개 기존 고유 경로와 합쳐 **48개**이며 기존 원본 PNG 재조회는 새 경로로 합산하지 않았다.

R005에서 기존 대상 **PNG 8개를 다시 GitHub Base64 바이트로 수신**, IHDR / PNG 청크를 파싱하여 **8개 전 파일의 모든 청크 CRC32 통과**, 저장소 Git blob SHA와 이전 원장 **8/8 일치** 확인. 각 파일 **16×16**. 6개는 palette indexed(색상 타입 3), 2개(spruce, vine)는 grayscale(0). **7개에는 `tRNS` 투명도 선언**, moss에는 없음. 이는 이미지 컨테이너의 저장 방식이며, 실제 RGBA를 재디코드해 픽셀을 새로 합산했다는 뜻은 아니다. **R005 신규 RGBA 픽셀 계측 0**; R001의 2,048 RGBA 화소/PNG SHA-256, R002의 알파 마스크, R004의 보조 colormap 131,072 RGB 화소, R001 44개 면별 UV 기록은 **계승 수치**다. 이번 R005에서 raw PNG SHA-256 값을 새로 재계산하지 않았으므로 `sha256_prior_R001`로 별도 표시했고, Git blob SHA와 CRC 검사만 이번에 새로 시행했다.

## 아이템 모델의 constant tint: 블록 tintindex 와 구별

8개 `items/{id}.json`에서 **5개 `minecraft:constant`**, 3개 `tints` 미기재 확인. 부호 있는 32-bit 정수를 ARGB로 변환한 결과는 다음과 같다.

| 텍스처 | 아이템 상수 ARGB | RGB | 블록 모델 tintindex |
|---|---|---|---|
| oak_leaves | FF48B518 | #48B518 | 0 |
| spruce_leaves | FF619961 | #619961 | 0 |
| birch_leaves | FF80A755 | #80A755 | 0 |
| mangrove_leaves | FF92C648 | #92C648 | 0 |
| vine | FF48B518 | #48B518 | 0 |
| azalea_leaves | 미선언 | 미선언 | 없음 |
| moss_block | 미선언 | 미선언 | 없음 |
| flowering_azalea_leaves | 미선언 | 미선언 | 없음 |

**5/8개** 아이템의 명시적 상수는 **고유 RGB 4개**다. 8개의 아이템 JSON은 모두 실제 모델 경로로 연결되는 것이 확인되었다. 블록의 `tintindex:0`(R001/R003 면별 근거)과 아이템의 `minecraft:constant`는 다른 데이터 경로이며, 이 상수는 최종 바이옴 렌더 RGB 실측이 아니다. 아이템 상수 중 oak와 vine은 같은 #48B518. `ITEM_TINT_LEDGER.csv`에 파일 SHA 및 모델 참조 보존.

## 덩굴: 같은 텍스처와 다른 기하 경로

- 블록 `models/block/vine.json`: 0두께 양면 평면 `from:[0,0,0.8]`, `to:[16,16,0.8]`; 북 `uv:[16,0,0,16]`, 남 `uv:[0,0,16,16]`, 각 면 `tintindex:0`(R001에서 검증, 이번 새 UV 면 0).
- `items/vine.json`의 `model:minecraft:item/vine` → `models/item/vine.json`의 `parent:minecraft:item/generated` → `models/item/generated.json`의 `parent:builtin/generated`; `layer0:minecraft:block/vine` 직접 연결.
- 따라서 **블록의 평면/회전 multipart 모델**과 **아이템의 generated sprite 모델**은 동일 PNG를 사용해도 동일 기하가 아니다. item JSON은 명시적인 face UV 배열을 정의하지 않는다. 이전 R002의 vine 32 논리 상태·회전 실측은 새로 수치 누적하지 않았다.

## 셰이더: PNG 컷아웃과 틴트의 실제 정적 소스 경계

사용자 추출본의 `terrain.vsh`, `terrain.fsh` 및 실제 import include 네 파일을 읽었다.

1. 정점 단계: `texCoord0 = UV0`; `vertexColor = Color * minecraft_sample_lightmap(Sampler2, UV2)`.
2. 프래그먼트 단계: `UseRgss == 1`에 따라 `sampleRGSS(Sampler0, ...)` 또는 `sampleNearest(Sampler0, ...)`; 그 텍스처 샘플을 `vertexColor`와 곱한다.
3. **`#ifdef ALPHA_CUTOUT`** 안에서 `color.a < ALPHA_CUTOUT`이면 `discard`한다. *이 소스만으로* 매크로가 실제 어느 블록 렌더 패스에서 정의되는지 또는 임계값이 얼마인지는 알 수 없다.
4. 읽은 두 지형 셰이더에는 `foliage.png`, `grass.png`, 온도/강수량 좌표계 변환을 직접 나타내는 코드가 없다. 이는 **이 파일에서 직접 확인할 수 없음**이지 바이옴 색 계산이 존재하지 않음을 증명하지 않는다. 이 경우 텍스처 색이 셰이더에 도달하기 전에 정점 `Color`로 주입될 가능성은 있으나 실제 CPU 측 구현까지 확인되지 않았다.

**새 실측으로 확정할 수 없는 것:** R004의 256×256 colormap 좌표(x,y)가 온도·습도에 어떻게 대응되는지, biome interpolation, 잎 종류별 예외, 최종 게임 화면 RGB, 컷아웃 임계값 및 RGSS/mipmap 경계 색. 실제 Minecraft 게임 실행/스크린샷이 없으므로 **F 인게임 정적 0/8**을 유지한다.

## 기록 구성과 보류

`SOURCE_LEDGER.csv`: 새 16경로/기존 PNG 8경로 구분. `PNG_CONTAINER_RECHECK.csv`: 직접 CRC·청크·SHA 출처. `ITEM_TINT_LEDGER.csv`: 8개 아이템의 상수·모델·블록 틴트 관계. `SHADER_STATIC_AUDIT.json`: 색상·UV·조건부 컷아웃 증거. `SUMMARY.json`: 신규 및 계승 수치의 별도 집계.

다음 정적 검증은 (1) 실제 온도·강수량→colormap 좌표 룩업의 소스코드, (2) `ALPHA_CUTOUT`의 컴파일 경로 및 실제 적용 여부, (3) 인게임 실제 정적 화면(별도 증거 필요). 애니메이션, Project Zomboid 변환 및 3D 가구 제작은 보류/제외.
