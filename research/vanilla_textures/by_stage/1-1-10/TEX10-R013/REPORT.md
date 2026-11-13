# TEX10-R013 — 1.21.11 SpriteContents→SpriteLoader→Sprite 아틀라스 호출·UV·밉맵 한계 정적 조사

> 2026-11-13 / 사용자 제공 `1.21.11/`에서 실제 JVM `.class` 5개 신규 직접 분석. **본 연구는 1-1-10 잎·식생 8종만**. 인게임 렌더 검증은 의무에서 제외. 공식 Mojang 전체 JAR SHA-1은 요구하지 않으며 공식 인증이 완료됐다는 뜻도 아니다.

## 새 원본 1차 자료 5개 — 이전과 중복 집계하지 않음

| 사용자 제공 경로 | Git blob SHA | 실제 확인한 역할 |
|---|---|---|
| `1.21.11/ilk.class` | `71909dbd8a8d20910b3eaa00c9846273068a0c1f` | holds original image, metadata strategy/bias and calls mipmap helper |
| `1.21.11/ill.class` | `246d1344510e5a6e0a2918e291a1c470c31e6e47` | clamps requested mip levels using all stitched sprites and schedules generateMipmaps |
| `1.21.11/ilp.class` | `076a9076dd3aaaf92265a78f07e05addad0449bc` | records atlas padded bounds and maps normalized sprite UV to atlas UV |
| `1.21.11/ilt.class` | `59ad784d006bb046b47ca097de5bd006f2667500` | static source: SpriteContents loader interface, create lambda; loadSprite abstract |
| `1.21.11/bgj.class` | `89604a1a7dfc4e63be8bc0eb170352b59c7f5374` | power-of-two and logarithmic mip-level helper |

- 단순 이름 매핑은 1.21.11 Fabric Yarn 문서를 보조로 확인했지만, 메서드 디스크립터·바이트코드 길이·호출 필드·UV 수식은 **사용자 추출본의 실제 .class**에서 검증.
- R010 `ild.class`, R011 `bel.class`, R012 `fyh.class`, R011 PNG 8종은 계승. **새 원본 고유 경로 5개**, 누적 R003–R012 **148 → R013 153개**. 원본 PNG/신규 RGBA 계측 **0개**, 기존 8종 모두 유지.

## 1. 원본 메타데이터가 밉맵 생성기로 전달되는 실제 경로

`ilk.class`(SpriteContents) 주 생성자(126바이트)는 메타데이터 Optional을 받아
- `strategy` 필드(`ilk.j:Lile;`)에 `TextureResourceMetadata` 전략을 저장하고, 없으면 `ile.a`(**AUTO**)로 기본화
- `cutoffBias` 필드(`ilk.k:F`)에 메타데이터 bias, 없으면 **0.0F**를 저장
- `mipmapLevelsImages` 필드(`ilk.g:[Lfyh;`)를 최초에는 원본 한 장으로 채움

`ilk.a(I)V`(119바이트)는 `ild.a(Identifier,NativeImage[],int,MipmapStrategy,float)` 호출을 통해 **선택된 밉맵 수준 + 위 전략·bias**를 넘기고 계산 결과를 `ilk.g`에 다시 저장한다. 이 연결로 R010의 전략 분류와 R012의 전처리/파생 RGBA 실험이 실제 **스프라이트 콘텐츠 처리 경로와 관련** 있음을 원본으로 확인했으나, **그 실험값이 실제 Java 실행값과 완전히 동일한지 인증한 것은 아님**.

`ilt.class`는 `loadSprite(Identifier,Resource)` 인터페이스를 정의하고 `create(Set)` 동적 람다 팩토리를 포함한다. **구체적인 Resource/metadata 디코딩 람다 구현**은 이번 조사에서 분석하지 않았고 증거에 미완료로 남긴다. 애니메이션은 일절 조사·완료로 표시하지 않았다.

## 2. 실제 밉맵 생성 수준은 아틀라스 로더가 결정

`ill.class`(SpriteLoader) `stitch(List<SpriteContents>, mipLevel, Executor)` 568바이트 메서드를 분석했다. 핵심 의사코드:

```text
desiredScale = 1 << requestedMipLevel
for each sprite in stitching list:
    minImageDimension = min(minImageDimension, sprite.width, sprite.height)
    minPow2PerSprite = min(
        Integer.lowestOneBit(sprite.width),
        Integer.lowestOneBit(sprite.height)
    )
    if minPow2PerSprite < desiredScale:
        reduce desiredScale to minPow2PerSprite
reducedOrRequestedMipLevel =
    select floorLog2 bound and cap by requested mipLevel
// runtime graphics/texture options are also read; actual values not measured
later for sprite in atlas:
    SpriteContents.generateMipmaps(selectedLevel)
```

`bgj.class`의 실제 `e(I)Z` (power-of-two test) 및 `g(I)I` (floor integer log2) 호출을 연결 확인했다. 16×16 텍스처는 `Integer.lowestOneBit(16)=16`, `floorLog2(16)=4`. 따라서 **8개 표본 각각의 단독 16×16 스프라이트에서 가능한 최대 축소 깊이는 L4**다. R012의 `L1~L4` 계산은 이 **국소 입력 규격**과 일치한다.

**중요한 보정:** 이것이 실제 게임이 이 스프라이트에 **반드시 4단계를 생성**한다는 결론은 아니다. `SpriteLoader`는 다수 스프라이트를 함께 조합하고 요청 mip level, 다른 스프라이트의 작은 치수, 런타임 관련 설정 등에 의해 수준을 낮출 수 있다. **실제 선택 값/atlas source 내용/다른 스프라이트의 최소 차원은 이 8종 단독 자료로 결정할 수 없다.** R012 680 RGBA는 **가정한 L1~L4 전체를 계산한 재현 실험**임을 유지한다.

## 3. 실제 아틀라스 UV 좌표계 — 좌표 변환 확인, 숫자 확정은 제외

`ill.class`는 stitching 결과로 `ilp.class`(Sprite) 생성자 `<init>(atlasId,contents,atlasWidth,atlasHeight,x,y,padding)`를 호출. 생성자 바이트코드 97바이트를 계산식으로 풀면:

```text
minU = float(x + padding) / float(atlasWidth)
maxU = float(x + padding + spriteContents.width) / float(atlasWidth)
minV = float(y + padding) / float(atlasHeight)
maxV = float(y + padding + spriteContents.height) / float(atlasHeight)

frameU(t) = minU + t * (maxU - minU)
frameV(t) = minV + t * (maxV - minV)
```

`ilp.a(F)F` 및 `ilp.b(F)F`는 각각 19바이트 보간 메서드. `t`는 이 메서드의 입력인 **정규화된 로컬 UV 변수**이며, 모델 JSON `0..16` 좌표에서 `t`로 변환하는 별도의 baked model 규칙은 R013에서 신규 조사하지 않았다.

**아틀라스의 실제 (atlasWidth,atlasHeight,x,y,padding) 값은 미측정**이므로 잎 6종·덩굴·이끼 8종의 실제 수치화된 아틀라스 UV를 확정하지 않았다. 이 제한은 단순 UV 수식 확인과 실제 게임 배치 인증을 혼동하지 않기 위한 것이다.

## 4. 이번 정량 범위와 다음 연구 한계

- **새로 직접 읽은 고유 원본 클래스** 5개, 8종 16×16 기반 최대 L4 국소 상한 8행, 실제 Sprite UV 식 6개. R012 full RGBA 새 계산 **없음**; 과거 680 파생 픽셀은 별도 실험으로 보존.
- 원본 데이터 기반의 **확정**: 메타데이터 → `SpriteContents` 필드 → `MipmapHelper` 호출; 로더의 밉맵 수준 제한; `Sprite`의 atlas x/y/padding 수식.
- 여전히 **미확정**: 구체적인 `SpriteOpener` 리소스 메타데이터 디코딩 구현, 8종 실제 아틀라스 배치 수치, 정확한 선택된 글로벌 mip level, Java 원본 `NativeImage` 직접 실행과 R012 RGB byte-for-byte 비교. 실제 게임 화면 실측은 사용자 지시로 의무에서 제외.
- 전역 체크포인트 `v38`, 다른 1-1 단계 STATE/HANDOFF, 루트 상태 문서, 기존 `TEX10-R001~R012` 전부 변경하지 않음.

## 파일

`ATLAS_MIP_LIMIT_8.csv` / `ATLAS_UV_FORMULAS.json` / `SPRITE_SOURCE_CALLGRAPH_AUDIT.json` / `SOURCE_LEDGER.csv` / `SUMMARY.json` + 본 보고서. 오직 본 단계 라이브 `STATE.json`과 `HANDOFF.md`만 갱신.
