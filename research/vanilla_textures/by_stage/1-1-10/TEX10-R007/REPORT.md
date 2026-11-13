# TEX10-R007 — 원본 1.21.11 JVM 바이트코드로 바이옴 컬러맵 좌표·색상 우선순위·정적 CUTOUT 0.5 검증

> 2026-11-13 · Minecraft Java Edition 1.21.11 · 사용자 제공 `1.21.11/` 추출본을 직접 검사. 고정 블록 PNG 8종 유지; 인게임 정적 화면 **0/8**, 공식 Mojang 전체 client.jar SHA-1 검증은 사용자 지시로 **제외**(성공 인증 아님). 전역 `v38`, R001–R006, 다른 단계 무변경.

## 1. 단순 추정이 아닌 JVM 클래스 바이트코드 분석

새로운 실제 원본 소스 경로 **7개 클래스** `dvy.class`, `dxo.class`, `dwk.class`, `dwd.class`, `dwm.class`, `hpa.class`, `ggr.class`를 직접 바이너리로 조회해 Java class constant pool, `Code` 바이트코드, method descriptor를 검사했다. 각 파일 Git blob SHA, 명시적 bytecode hex 일부, 상수 해석은 `CLASS_BYTECODE_AUDIT.json`. **외부 Yarn 1.21.11 매핑은 클래스명/메서드명 대응 보조 근거**이며, 실제 명령어·숫자는 사용자 저장소의 바이트코드에서 읽었다.

- `dvy.a(DD[II)I` = Yarn `BiomeColors.getColor(double,double,int[],int)`. bytecode에 `dmul`, `dsub`, `ldc2_w 255.0`, `d2i`, `ishl 8`, `ior`, `iaload`가 확인됨. **0~1로 제한된 입력에 대해**:
  ```text
  t = clamp(float32(biome.temperature), 0, 1)
  d = clamp(float32(biome.downfall), 0, 1)
  x = int((1.0 - t) * 255.0)
  y = int((1.0 - t * d) * 255.0)
  index = (y << 8) | x
  color = colormap[index]  // absent/short array이면 별도 fallback
  ```
  `dxo.l(), dxo.k(), dxo.m()`은 두 climate 값을 독립적으로 `float clamp(0,1)`한 뒤 `double`로 변환해 각각 foliage, grass, dry-foliage 컬러맵 조회 함수에 넘김. **float32 변환을 먼저 해야 함**: `birch_forest`의 0.6은 float32로 저장되며 x=101, 십진수 0.6을 그대로 double 계산하면 x=102로 착오가 생길 수 있음.
- `dxo.d()` `Biome.getFoliageColor()`: `dxu.b()` Optional 명시 foliage color를 얻고 `Optional.orElseGet()`으로 없는 경우에만 `dxo.l()` default colormap getter 사용. `dxo.e()` dry foliage도 `dxu.c()` Optional → `dxo.m()` fallback. 따라서 R006 늪/맹그로브의 동일 (temperature, downfall)가 **같은 (x,y)**임에도 명시 foliage RGB가 서로 다름은 실제 바이옴 getter의 우선순위에서도 설명됨. 이 결과는 **바이옴 getter의 반환값 추적**이지 게임 화면 평균 색의 증명이 아님.
- `dwk.a(DD)I`, `dwd.a(DD)I`, `dwm.a(DD)I`는 모두 공동 `dvy.a(DD[II)I` 사용을 바이트코드로 확인. `dwk`의 기본 fallback `#FF48B518`, spruce 상수 `#FF619961`, birch `#FF80A755`, mangrove `#FF92C648`는 **R005 아이템 상수 RGB와 일치**하나, **각 블록이 실제 어느 컬러 프로바이더를 이용하는지**를 이 사실만으로 자동 확정하지 않는다. dry fallback `#FF5C3C32`; grass 미등록 map fallback `#FFFF00FF`.
- `ggr.class`는 `BlockColors`이며 여러 공급자/고정 상수와 biome resolver 호출 흔적이 있으나 **8개 블록 각각의 등록 경로·인게임 실제 결과는 검증 완료로 표기하지 않는다**.

## 2. 세 색상표의 실제 RGB 디코딩 및 65개 바이옴 좌표 계산

사용자 저장소의 `textures/colormap/foliage.png`, `grass.png`, `dry_foliage.png` 바이트를 직접 다시 읽고 PNG 모든 청크 CRC32, zlib Adler32, DEFLATE 압축 해제, PNG 필터/256×256×3 RGB 복원을 수행했다. `foliage` **8,837 고유 RGB**, `grass` **4,536 고유 RGB/백색 32,640픽셀**은 R004 실측과 정확히 일치. `dry_foliage`는 **이번 R007 최초로 65,536 RGB 픽셀 디코드**, **268 고유 RGB**. 이전 R006은 dry PNG의 청크 CRC만 검사한 상태였음. R004 계승 foliage+grass **131,072 고유 위치**와 이번 dry **65,536 신규 위치**를 구분하여 세 colormap 총 **196,608 고유 RGB 픽셀 위치**. 기존 대상 블록 8개 PNG 화소를 추가 계수하지 않음.

R006에서 직접 읽은 **65개 바이옴 JSON**(R007 신규 경로로 중복 집계하지 않음)에 위 **JVM 바이트코드와 float32** 해석을 적용하여 x/y/index를 계산하고, 3개 원본 색상표의 실제 해당 RGB를 조회했다. 각 행에 foliage/dry의 JSON 명시 색 우선 결과, grass pre-modifier 결과와 grass_color_modifier도 구분: `BIOME_COLORMAP_LOOKUP_65.csv` **65행×3 colormap = 195개 조회 셀**. 이미 R004에서 디코드한 foliage/grass 픽셀을 다시 사용하는 것은 고유 화소 수 증가가 아니며 이번에 새롭게 얻은 것은 **바이옴별 lookup 연결 및 dry 픽셀 해독**임.

검증용 대표 사례 (`#...`는 RGB만 표시):

| 바이옴 | (temp, downfall) | (x,y) | foliage colormap | 바이옴 getter 선택 RGB |
|---|---|---|---|---|
| `birch_forest` | (0.6, 0.6) | (101,163) | `#6BA940` | `#6BA940` |
| `cherry_grove` | (0.5, 0.8) | (127,152) | `#63A948` | `#B6DB61` |
| `desert` | (2, 0) | (0,255) | `#AEA42A` | `#AEA42A` |
| `forest` | (0.7, 0.8) | (76,112) | `#59AE30` | `#59AE30` |
| `mangrove_swamp` | (0.8, 0.9) | (50,71) | `#45B421` | `#8DB127` |
| `plains` | (0.8, 0.4) | (50,173) | `#77AB2F` | `#77AB2F` |
| `snowy_taiga` | (-0.5, 0.4) | (255,255) | `#60A17B` | `#60A17B` |
| `swamp` | (0.8, 0.9) | (50,71) | `#45B421` | `#6A7039` |

**중요 경계:** 이 표는 `Biome.getFoliageColor()`/상응 dry getter가 **사용자 원본 colormap이 로드되었을 때**의 계산 결과다. 게임의 블록 종류별 색상 공급자, 세부 조명, 주변 바이옴 3D 색상 보간, mipmap/필터링/동영상/실제 GPU 프레임 RGB은 입증하지 않는다. `grass_color_modifier`가 있는 바이옴의 grass 값은 해당 변형 전 값으로만 기록.

## 3. 잎의 mipmap 원본 sidecar와 alpha 컷아웃 파이프라인

대상 8개 PNG 옆의 `.png.mcmeta`를 개별 검사: `oak_leaves`, `spruce_leaves`, `birch_leaves`, `mangrove_leaves`, `azalea_leaves`, `flowering_azalea_leaves` **6개** 모두 `{"texture":{"mipmap_strategy":"dark_cutout"}}` 원문 동일, blob SHA `214e9838146f3f889c141f358a77c0dfa38bbea4`. `vine`/ `moss_block`은 **해당 sidecar가 사용자 추출본에 없음**. sidecar 부재는 1.21.11의 실제 기본 mipmap 전략 확인을 대체하지 않는다. 이 6개 sidecar가 **R007 새 고유 파일 경로 6개**.

`hpa.class`(Yarn `RenderPipelines`) 원본 클래스 정적 생성 루틴에서 `CUTOUT_BLOCK`/ `CUTOUT_TERRAIN` 각각 `RenderPipeline.Builder.withShaderDefine("ALPHA_CUTOUT", 0.5F)` 호출을 확인했다. `hpa` constant pool의 `ALPHA_CUTOUT`·IEEE754 float 비트 `0x3F000000`와 각 `putstatic`을 코드 위치로 연결한 결과. 이는 R006의 `terrain.fsh`/ `block.fsh` 조건부 `color.a < ALPHA_CUTOUT`과 대응하는 **컴파일 가능한 파이프라인 정의 0.5**를 정적 원본에서 확정한 것이다. 하지만 **잎/덩굴 각각이 실제 게임에서 특정 파이프라인에 할당됐는지**는 이번 단계에서 따로 검증하지 않았으므로 "8개 블록 임계값 0.5 확정"이라고 쓰면 안 된다. 새 측정 또한 실제 mipmap 레벨별 투명 픽셀 수 계측이 아니다.

## 4. 변경 범위·앞으로 필요한 사용자 근거

**R007 신규 고유 소스 경로 13 = JVM class 7 + PNG sidecar 6**. R003–R006 누적 121에서 **134**로 증가. 이번 결과물은 `CLASS_BYTECODE_AUDIT.json`, `BIOME_COLORMAP_LOOKUP_65.csv`, `COLORMAP_RECHECK.json`, `MIPMAP_STRATEGY_8.csv`, `SOURCE_LEDGER.csv`, `SUMMARY.json`, 이 보고서. **문서 원본이나 R001–R006 파일 수정 없음**, 단계 state/handoff만 최신 R007로 변경.

**다음 1-1-10 작업의 실질적인 미검증:** 직접 Minecraft 1.21.11에서 8개 블록의 기본 리소스팩·생물군계·조명·잎 그래픽 옵션·mipmap 설정에 따른 **인게임 정적 렌더 증거 (0/8)**, 대상별 실제 render pass/색상 공급자 경로 세부 추적, 좌표별 실제 주변 바이옴 보간. 앞의 원본 코드/PNG 정적 계산은 수행했으나 **게임 캡처는 사용자 도움이 필요**. 공식 client.jar 전체 SHA1 인증은 절차 제외, 애니메이션과 PZ→Minecraft 변환 및 가구 제작은 계속 제외.
