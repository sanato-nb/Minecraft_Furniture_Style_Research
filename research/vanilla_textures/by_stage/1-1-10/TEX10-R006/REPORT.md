# TEX10-R006 — 잎·식생: 65개 원본 바이옴 색상 오버라이드 전수 정적 대조 및 7개 셰이더 소스 보강

> Minecraft Java 1.21.11 · 2026-11-13 · 사용자 제공 JAR 추출본 `1.21.11/`을 1차 자료로 확인. **표본 블록 PNG 8개는 그대로**, 이번에 신규 대상 PNG/신규 RGBA 픽셀 계산 **0**. 독립 연구 버전은 `TEX10-R006`; 역사적 전체 `v38` 및 R001–R005 변경 없음. 애니메이션·3D 가구·PZ 변환 보류.

## 신규 경로 및 재검사 구분

- `data/minecraft/worldgen/biome/` 아래 JSON 파일 **65/65개**: 이번에 각각 직접 읽고 `temperature`, `downfall`, `has_precipitation`, `temperature_modifier`, `effects.foliage_color`, `effects.grass_color`, `effects.dry_foliage_color`, `effects.grass_color_modifier`를 조사. `BIOME_SOURCE_AUDIT.csv`에는 **65개 전부** 파일 Git blob SHA와 필드 원문 값, `BIOME_OVERRIDE_CASES.csv`에는 명시적 효과 색상/조정자 사례 **8개**를 기록. 원본 파일 경로/스키마를 바꾸지 않았다.
- 신규 shader GLSL **7개 경로**: `block.{vsh,fsh}`, `entity.{vsh,fsh}`, `particle.fsh`, `include/light.glsl`, `include/dynamictransforms.glsl`. 새 파일 본문을 직접 조회하고 정적 표현식을 확인. `SHADER_PATH_AUDIT.csv`·`SHADER_STATIC_AUDIT.json`에 원본 Git SHA와 검증 범위.
- 보조 colormap PNG **1개 새 경로**: `assets/minecraft/textures/colormap/dry_foliage.png` Git blob `b5750169dd2c6588a32674565b2f668624ece00d`. 실제 파일 **8,979바이트**, **256×256 8-bit RGB truecolor (color type 2)**, PNG `IHDR`·`IDAT`·`IEND` **3개 모든 CRC32 통과**. **65,536개 좌표가 있는 이미지만 확인했으며 RGB 디코딩·픽셀별 색상 통계는 새로 하지 않음(0)**. 따라서 누적 RGB 계측 수에 더하지 않음.
- 신규 **73개 고유 정적 경로 = 바이옴65 + GLSL7 + 보조 PNG1**. 기존 R003–R005 고유 48개와 합해 R003–R006 **121개 경로**. 경로는 중복 없이 계산했으며 서로 동일한 Git blob 내용이 있는 바이옴 JSON의 경우에도 서로 다른 파일 경로로 표시한다.
- 기존 대상 8 PNG, R001 **2,048 RGBA 픽셀**, R002 마스크 8개, R001 UV face 44행 및 R004 보조 `foliage.png`·`grass.png`의 **131,072 RGB 픽셀은 모두 계승**. 이번에 다시 실측한 값으로 보고하지 않는다.

## D2 신규 결론 — temperature/downfall만으로 foliage RGB가 단일값으로 결정된다고 주장할 수 없음

65개 JSON의 **정적 필드 존재 수**:

| JSON 필드 | 명시된 바이옴 수 |
|---|---:|
| `effects.foliage_color` | **7** |
| `effects.grass_color` | **5** |
| `effects.dry_foliage_color` | **4** |
| `effects.grass_color_modifier` | **3** |
| `temperature_modifier` | **2** |

명시적인 effects 색상/grass modifier 중 하나라도 존재하는 바이옴은 **8종**; `temperature_modifier`만 추가한 경우까지 포함하면 **10종**. 각 필드는 같은 경로라도 독립 항목이므로 수를 더해 총 바이옴 수로 착각하지 않는다.

**엄격한 직접 비교**: `swamp.json`, `mangrove_swamp.json` 모두 `temperature=0.8`, `downfall=0.9`, `grass_color_modifier="swamp"`, `dry_foliage_color="#7b5334"`이지만 `foliage_color`은 각각 **`#6a7039`**와 **`#8db127`**로 다르다. 이는 정적 원본 정의가 climate 숫자 외의 명시적인 foliage 구분을 보존한다는 **확정된 반례**다. 정확한 게임 렌더링 우선순위까지 확인한 것은 아니다.

그 밖의 명시적 잎색: `badlands`, `eroded_badlands`, `wooded_badlands` **`#9e814d`**, `cherry_grove` **`#b6db61`**, `pale_garden` **`#878d76`**. `dark_forest`에는 `grass_color_modifier: dark_forest`와 `dry_foliage_color`은 있지만 `foliage_color` 명시값은 없다. `frozen_ocean`, `deep_frozen_ocean`은 `temperature_modifier: frozen`만 확인. 필드가 없다는 것이 **실제 게임에서 tint가 없음**을 뜻하지 않는다.

기존 R005에서 확인한 oak/spruce/birch/mangrove/vine **아이템 constant 색상 5개**와 **블록 모델의 tintindex**, 이번 **바이옴의 foliage_color**는 서로 다른 계층: 하나의 최종 인게임 색/샘플 위치로 합치지 않는다. 자바 런타임 온도·강수량→colormap(x,y) 룩업, 기온 공간 보정, 바이옴 색상 오버라이드의 실제 적용, 보간은 **미검증**.

## D1/D3/E — 컷아웃 정적 GLSL 증거를 확장하되 블록 임계값은 미확정

- R005 `terrain.fsh`의 `#ifdef ALPHA_CUTOUT`에 더해 원본 `block.fsh`와 `entity.fsh`에서도 각각 **매크로가 정의됐을 때** `color.a < ALPHA_CUTOUT`이면 `discard`함을 직접 확인. `block.fsh`는 `Sampler0` 샘플×`vertexColor`×`ColorModulator`; `entity.fsh`는 샘플 알파 검사 이후 분기별 조명/색상 결합.
- `particle.fsh`에는 별도 고정 숫자 **`0.1`** 알파 컷오프가 실제로 있지만, **파티클 셰이더만의 수치**다. 이를 8개 블록 또는 `terrain.fsh`의 `ALPHA_CUTOUT` 실제 값으로 전용하면 잘못된 인증이다.
- `block.vsh`, `entity.vsh`에서 UV0 전달 및 Color/조명 입력, `include/light.glsl`의 면 방향 기반 RGB 조명, `include/dynamictransforms.glsl`의 `ColorModulator` 정의를 확인했다. 정적 셰이더와 모델 UV 계층의 연결 정황이지만, **어떤 렌더 패스가 실제 8개 블록에 선택되는지**는 이 파일만으로 확정할 수 없다.

## 검증 중단선

1. 바이옴 JSON 수치 또는 `foliage_color` 명시 필드 ≠ **온도·강수량에서 컬러맵 (x,y)를 얻는 Java 런타임 규칙/우선순위 인증**. 원본 클래스 바이트코드의 정확한 해석 또는 별도의 인게임 증거 필요.
2. GLSL 소스의 조건부 `ALPHA_CUTOUT` ≠ **바닐라 1.21.11에서 특정 잎·덩굴 블록이 임계값 얼마로 렌더링됐는지 확인**. 그 빌드의 컴파일 정의와 실제 셰이더·렌더 패스 근거 필요.
3. **인게임 정적 검증 0/8**, 공식 JAR 전체 SHA-1은 사용자 지시로 연구 필수 항목 및 완료 분모에서 **제외**(공식 인증 성공이 아님).
4. 새 JPEG/게임 스크린샷/시뮬레이션 인게임 증거 없음. 텍스처 PNG 8개 고정, R001–R005 결과 불변. 애니메이션·PZ 변환·3D 가구 제작 보류.

## 결과 파일

`BIOME_SOURCE_AUDIT.csv` 65행(파일 경로+SHA+온도·강수·효과 키), `BIOME_OVERRIDE_CASES.csv` 8행(색상·수정자), `SHADER_PATH_AUDIT.csv` 7행, `SHADER_STATIC_AUDIT.json`, `DRY_FOLIAGE_PNG_AUDIT.json`, `SOURCE_LEDGER.csv` 73행, `SUMMARY.json`. 모든 파일은 **이번 단계 R006**만 추가했고, 다른 단계/루트 파일 수정 없음.
