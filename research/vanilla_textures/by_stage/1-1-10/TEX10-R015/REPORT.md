# TEX10-R015 — 잎·식생 애니메이션 소스 검증

2026-11-19. 사용자 요청으로 1-1-C의 잎·식생 애니메이션 소스 연구 보류를 해제했다. Minecraft Java 1.21.11의 고정 표본 8개를 대상으로 PNG, 대응 메타데이터, 블록 상태와 모델 JSON을 재검사했다.

| 검사 | 결과 |
|---|---|
| 고정 PNG | 8/8이 16×16 단일 이미지. 고정 원장 SHA-256 8/8 일치. RGBA 2,048픽셀 재디코딩 |
| 잎 6종 메타데이터 | 모두 `texture.mipmap_strategy: dark_cutout`만 선언. `animation` 0/6 |
| 이끼 블록·덩굴 메타데이터 | JAR 및 저장소 추출본 양쪽에서 대응 `.png.mcmeta` 없음 |
| 블록 상태·모델·부모 모델 | 블록 상태 8개와 모델 JSON 12개 대조. `animation`, `frames`, `frametime`, `interpolate` 키 0건 |
| 양성 대조군 | `kelp` 16×320에서 서로 다른 RGBA 프레임 20개. 프레임당 2틱, 원본 순서 0–19, 주기 40틱 |

PNG와 JSON은 1.21.11 JAR 및 저장소의 `1.21.11/` 추출본을 바이트 단위로 대조했다. JAR 전체 SHA-1은 저장한 버전 메타데이터의 `downloads.client.sha1`과 일치했다. 켈프는 `texture.alpha_cutoff_bias`와 별개로 `animation`을 선언하며 연속 프레임 사이에서 9–44개 화소가 바뀌었다. 켈프는 고정 8개 분모 밖의 대조군이다.

**판정: 고정 표본 8/8 애니메이션 소스 검사 완료. PNG 프레임 애니메이션 0/8.** 덩굴의 면별 모델 선택과 잎의 밉맵 설정은 각각 블록 상태·텍스처 설정에 해당한다. 실제 게임 화면의 흔들림·성장과 외부 셰이더·리소스팩 효과는 이번 검사 범위 밖이다.

[고정·보조 PNG 원장](TEXTURE_ANIMATION_AUDIT.csv) · [블록 상태·모델 원장](BLOCKSTATE_MODEL_AUDIT.csv) · [양성 대조 프레임](POSITIVE_CONTROL_FRAMES.csv) · [집계](SUMMARY.json) · [재현 방법](../../1-1-02/TEX02-R018/REPORT.md)
