# TEX10-R009 — 잎·덩굴·이끼 8종의 정적 RenderLayer 레지스트리 경로 및 LeavesBlock 상속 검증

> 2026-11-13 · Minecraft Java 1.21.11 · 사용자 제공 JAR 추출본 `1.21.11/`의 실제 .class bytes, JVM constant pool, 클래스 바이트코드 분석. 인게임 검증·Mojang 공식 전체 client.jar SHA1 인증은 사용자 정책상 **필수 조건에서 제외**(인증 성공 의미 아님). 8개 고정 PNG 표본, 기존 R001–R008 및 전역 v38 불변.

## 이번 신규 고유 원본 클래스 6경로

`hoe.class`(BlockRenderLayers), `hth.class`(BlockRenderLayer enum), `eei.class`(LeavesBlock), `eir.class`(TintedParticleLeavesBlock), `eje.class`(UntintedParticleLeavesBlock), `ees.class`(MangroveLeavesBlock). 모두 사용자 저장소 1.21.11/에서 바이너리 직접 조회, constant pool·메서드/클래스 상속·Git blob SHA 확인. 보조 Yarn 1.21.11 이름 매핑은 난독화 이름 해석 용도이며, 아래 수치는 사용자 원본 bytecode에서 얻었다.

이번 **신규 파일 경로 6** + R003–R008 기존 고유 경로 **136** = 누적 **142개**. 기존 `dzs.class`(R008), `hpa.class`(R007), `ggr.class`(R007)은 연결 근거로 다시 사용하되 새 경로로 집계하지 않음. 새 PNG·RGBA/UV 계측 **0개**. 이전 8개 PNG, 44 모델 면 UV(R008), 32 덩굴 상태(R008), 3컬러맵 196,608 RGB 위치(R007)를 그대로 계승.

## 실제 색상 공급자와 분리되는 렌더 레이어 선택

`hoe.a(Leoh;)Lhth;` 원본 바이트코드:
```text
get block = BlockState.getBlock()
if block instanceof eei [LeavesBlock]:
    if hoe.c [cutoutLeaves boolean]:
        return hth.b  // CUTOUT
    return hth.a      // SOLID
else:
    registered = hoe.a[block]  // map lookup
    return registered != null ? registered : hth.a  // default SOLID
```

`hoe.a(Z)V` setter는 단순히 `hoe.c`에 설정을 보관한다. **사용자의 실제 그래픽 설정값 또는 그 실행 상태는 이 파일에서 확인하지 않았으며 이번 필수 연구에서 제외한다.** 설정에 따른 **두 가능한 정적 경로를 모두 기록**했다.

`hoe.b(HashMap)` 3,013바이트 등록 메서드에서 `hth.b`(CUTOUT)를 로컬 변수에 담는 `b2 00 28 4d`(PC 13–16) 확인. 그 CUTOUT 값을 참나무·가문비·자작나무·맹그로브·철쭉·꽃핀철쭉 잎 6개와 덩굴 1개에 Map.put으로 등록한 코드를 확인했다. 블록 레지스트리 필드 이름은 R008 `dzs.class` 문자열 레지스트리 매핑 계승. **잎 블록은 이 CUTOUT 등록값이 있더라도 우선 LeavesBlock 타입 분기에 들어가므로 설정이 false면 SOLID을 반환한다**. 덩굴은 타입 분기가 아닌 등록 맵을 따라 CUTOUT. 이끼 `dzs.ub`는 해당 Map의 정적 등록 원본에 없으므로 기본 SOLID 경로.

`hth.class` 실제 enum 정적 생성자에서 `hth.a` = SOLID → `hpa.c` (SOLID_TERRAIN); `hth.b` = CUTOUT → `hpa.f` (CUTOUT_TERRAIN) 연결 확인. `hpa.f`에는 R007에서 확인한 정적 `withShaderDefine("ALPHA_CUTOUT", 0.5F)`이 있으므로 CUTOUT 경로를 **선택했을 때의** 정적 임계값 `0.5F`와 연결된다. SOLID 경로의 샘플 결과, 실제 게임 GPU 출력은 연구 증거로 가장하지 않는다.

## 잎 여섯 종의 실제 생성자→상속 경로

원본 `dzs.class`의 블록 등록 `<clinit>`에서 각 잎 이름과 `invokedynamic`을 연결하고 클래스 `BootstrapMethods`의 `LambdaMetafactory` 구현 타깃을 추적했다. 생성 결과는 다음과 같다.

| 대상 | 생성 메서드(기존 dzs) | 실제 클래스 체인 |
|---|---|---|
| oak_leaves | dzs.hy | eir → eei |
| spruce_leaves | dzs.hx | eir → eei |
| birch_leaves | dzs.hw | eir → eei |
| mangrove_leaves | dzs.hq | ees → eir → eei |
| azalea_leaves | dzs.hp | eje → eei |
| flowering_azalea_leaves | dzs.ho | eje → eei |

`eei.class`는 `dzq`(Block)에서 상속받는 LeavesBlock, `eir`·`eje`는 `eei` 직접 자식, `ees`는 `eir` 자식임을 **해당 원본 .class의 superclass 인덱스로 재검증**했다. 이로써 **철쭉 잎도 정적 LeavesBlock 설정 분기 대상**임이 코드 체인으로 뒷받침된다.

## 8개 대상별 정적 결론

| texture_id | R008 색상 공급자 | CUTOUT 잎 옵션 TRUE | 잎 옵션 FALSE |
|---|---|---|---|
| `oak_leaves` | biome_foliage | CUTOUT | SOLID |
| `spruce_leaves` | constant_#619961 | CUTOUT | SOLID |
| `birch_leaves` | constant_#80A755 | CUTOUT | SOLID |
| `mangrove_leaves` | biome_foliage | CUTOUT | SOLID |
| `azalea_leaves` | no_model_tint | CUTOUT | SOLID |
| `flowering_azalea_leaves` | no_model_tint | CUTOUT | SOLID |
| `vine` | biome_foliage | CUTOUT | CUTOUT |
| `moss_block` | no_model_tint | SOLID | SOLID |

잎 `SOLID`과 `CUTOUT`은 **모델 재질/색상 코드와 다른 렌더 파이프라인 선택**이다. 해당 PNG의 `dark_cutout` 밉맵 metadata(R007)는 이미지 처리 전략으로, 실제 그래픽 설정의 SOLID/CUTOUT 선택과 동일한 속성이라고 해석하면 안 된다. 특히 모델에 `tintindex`가 없는 철쭉/꽃핀철쭉도 컷아웃 분기 대상으로 들어갈 수 있다. 덩굴에는 바이옴 틴트·양면 평면과 별개로 CUTOUT 적용. 이끼 모델은 기본 SOLID이며 무틴트.

## 보고서 정량 범위 및 남은 정적 과제

- 이번 신규 source path **6개**, 8종 render-layer 결과 **8행**, 잎 종류별 생성 클래스 검증 **6행**, 원본 컷아웃 맵 target **7 등록**. 새로운 대상 PNG·RGBA·UV 측정 **0**. 다른 단계·전역 문서 수정 없음.
- 보류 중인 **정적 소스 과제**: `dark_cutout`, 기본 `auto` 등 mipmap 정책이 실제로 PNG의 알파/색상에 반영되는 알고리즘 구현과 단계별 알파 커버리지. 사용자가 애니메이션을 보류했으므로 시간 변화/애니메이션은 조사하지 않는다.
- 인게임 실행과 스크린샷은 **사용자가 이미 검증 분모에서 제외**했고, 0/8 역사적 수치는 보존. 실제 GPU 화면에서 확인하지 않았어도 원본 정적 렌더 파이프라인·모델 관련 하위 연구는 별도 완료로 표시할 수 있다.
- 공식 Mojang 전체 JAR SHA1은 계속 사용자 지시로 제외(공식 인증 성공이 아님). 실제 가구 모델 제작·Project Zomboid 맵 변환은 수행하지 않음.

## 결과

`RENDER_LAYER_8.csv`, `COLOR_AND_RENDER_8.csv`, `LEAF_FACTORY_INHERITANCE_6.csv`, `CLASS_RENDER_LAYER_AUDIT.json`, `SOURCE_LEDGER.csv`, `SUMMARY.json`. 오직 `1-1-10` 결과 폴더와 단계 라이브 `STATE.json`/`HANDOFF.md`만 갱신.
