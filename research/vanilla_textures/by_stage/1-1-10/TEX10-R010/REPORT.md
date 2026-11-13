# TEX10-R010 — 원본 JVM 밉맵 생성 기본값과 잎·덩굴·이끼 8종 정적 전략

Minecraft Java 1.21.11 · 2026-11-13 · 사용자 제공 1.21.11/ 추출본의 원본 Java .class 직접 검증. 인게임 검증과 공식 전체 JAR SHA1은 의무에서 제외되어 있으며 게임 화면을 검증한 것으로 표시하지 않는다.

## 새 1차 원본 파일과 계승 구분

- 신규 고유 클래스 3개: ild.class (MipmapHelper), ile.class (MipmapStrategy), inj.class (TextureResourceMetadata). 각 Git blob SHA는 SOURCE_LEDGER.csv에 기록.
- 기존 R002 마스크 8개와 R007 .png.mcmeta 6개는 계승. 새 대상 PNG=0, 새 RGBA 픽셀 계수=0, 생성한 mipmap 픽셀=0. 신규 원본 경로 3개, 누적 R003–R010 고유 경로 145개.

## 바이트코드 분기

- inj.class의 Codec optionalFieldOf: mipmap_strategy 누락 시 ile.a AUTO, alpha_cutoff_bias 누락 시 0.0F.
- ile.class enum: AUTO, MEAN, CUTOUT, STRICT_CUTOUT, DARK_CUTOUT.
- ild.a(Identifier,NativeImage[],int,MipmapStrategy,float)에서 AUTO를 처리할 때 원본 이미지에서 alpha=0 픽셀이 존재하면 CUTOUT, 없으면 MEAN을 선택.
- ild.a(NativeImage) hasAlpha: 픽셀별 alpha==0 검출 (48바이트 method). 단순히 전체 투명도 255 미만 픽셀을 세는 분기와 구별.
- ild의 mipmap helper는 2×2 상위 mip 픽셀을 downsample한다. DARK_CUTOUT은 별도 blendDarkenedCutout(ild.a(IIII)I)을 호출하며 알파 0 입력색의 기여를 제외하고 어두운 가장자리를 생성한다. 나머지는 bel.a(IIII) 평균 경로.
- CUTOUT, STRICT_CUTOUT, DARK_CUTOUT 모두 opacity-coverage 교정 코드에 연결된다. helper 상수 기본 0.5F, STRICT_CUTOUT 0.3F는 mipmap coverage 내부 값이지 R009 렌더 파이프라인의 shader ALPHA_CUTOUT 정의와 동일한 개념이 아니다.
- 원본 base image에 대한 TextureUtil.solidify 또는 fillEmptyAreasWithDarkColor 호출도 존재하지만, R010은 실제 mipmap 이미지 픽셀을 생성하거나 동일성 검증하지 않았다.

## 8종 효과적 정적 밉맵 선택

| 원본 텍스처 | R002 기존 투명 픽셀 (16×16) | 원본 mcmeta 또는 기본 AUTO | 정적 전략 |
|---|---:|---|---|
| oak_leaves | 84 | dark_cutout | DARK_CUTOUT |
| spruce_leaves | 96 | dark_cutout | DARK_CUTOUT |
| birch_leaves | 112 | dark_cutout | DARK_CUTOUT |
| mangrove_leaves | 44 | dark_cutout | DARK_CUTOUT |
| azalea_leaves | 59 | dark_cutout | DARK_CUTOUT |
| flowering_azalea_leaves | 51 | dark_cutout | DARK_CUTOUT |
| vine | 110 | absent => AUTO | CUTOUT |
| moss_block | 0 | absent => AUTO | MEAN |

기존 6개 잎 텍스처는 각각 원본 metadata에 dark_cutout이 직접 정의되어 있다. 덩굴은 mcmeta 부재+기존 alpha=0 픽셀 110개로 AUTO→CUTOUT, 이끼는 부재+alpha=0 픽셀 0개로 AUTO→MEAN. 이는 코드를 따라간 정적 기본 분기이며 실제 사용자가 선택한 mipmap 레벨 수 또는 GPU 화면 실측이 아니다.

## 범위 및 미해결

R008의 모델/44면·블록 틴트, R009의 SOLID/CUTOUT 렌더 레이어와 R010의 PNG mipmap 전략은 서로 다른 계층이다. 이번 8개 전략 판정은 정적 파일과 원본 alpha mask 교차 검증으로 성립하지만, 실제 생성 mip level별 RGB·알파 픽셀, atlas 동작, GPU 화면 색은 아직 측정하지 않았다. 인게임 검증은 사용자 지시에 따라 필수가 아니며, 애니메이션·PZ 변환·실제 가구 모델 제작은 계속 보류.

결과 파일: MIPMAP_EFFECTIVE_STRATEGY_8.csv, MIPMAP_BRANCH_MATRIX.csv, MIPMAP_CLASS_AUDIT.json, SOURCE_LEDGER.csv, SUMMARY.json. 단계 전용 STATE.json/HANDOFF.md만 갱신하고 전역 v38 및 과거 Rxxx는 수정하지 않는다.
