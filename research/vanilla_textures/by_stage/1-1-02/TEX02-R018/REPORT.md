# TEX02-R018 — 석재·벽돌 애니메이션 소스 검증

2026-11-19. 사용자 요청으로 1-1-C의 석재·벽돌 애니메이션 소스 연구 보류를 해제했다. Minecraft Java 1.21.11의 고정 표본 17개를 대상으로 PNG, 대응 메타데이터, 블록 상태와 모델 JSON을 재검사했다.

| 검사 | 결과 |
|---|---|
| 고정 PNG | 17/17이 16×16 단일 이미지. 고정 원장 SHA-256 17/17 일치. RGBA 4,352픽셀 재디코딩 |
| 고정 PNG의 `.png.mcmeta` | JAR 및 저장소 추출본 양쪽에서 0/17. `animation` 선언 0/17 |
| 연결용 상면 PNG | `blackstone_top`, `deepslate_top` 모두 16×16, 대응 메타데이터 없음 |
| 블록 상태·모델·부모 모델 | 블록 상태 17개와 모델 JSON 26개 대조. `animation`, `frames`, `frametime`, `interpolate` 키 0건 |
| 양성 대조군 | `water_still` 16×512에서 서로 다른 RGBA 프레임 32개. 프레임당 2틱, 원본 순서 0–31, 주기 64틱 |

PNG와 JSON은 1.21.11 JAR 및 저장소의 `1.21.11/` 추출본을 바이트 단위로 대조했다. JAR 전체 SHA-1은 저장한 버전 메타데이터의 `downloads.client.sha1`과 일치했고, PNG 무결성 검사를 거쳐 알파 화소와 프레임별 RGBA 해시를 기록했다. 물 대조군의 연속 프레임 사이에는 20–51개 화소가 바뀌었다. 상면 2개와 물은 고정 17개 분모 밖에 있다.

**판정: 고정 표본 17/17 애니메이션 소스 검사 완료. PNG 프레임 애니메이션 0/17.** 석재의 모델 변형이나 방향 선택은 블록 상태·모델 자료에서 확인했다. 실제 게임 렌더링 관측은 0건이며, 외부 리소스팩 또는 셰이더의 화면 효과는 이번 검사 범위 밖이다.

[고정·보조 PNG 원장](TEXTURE_ANIMATION_AUDIT.csv) · [블록 상태·모델 원장](BLOCKSTATE_MODEL_AUDIT.csv) · [양성 대조 프레임](POSITIVE_CONTROL_FRAMES.csv) · [집계](SUMMARY.json) · [재현 스크립트](VERIFY_ANIMATION_SCOPE.py)

저장소 루트에서 Pillow 13.0.0을 사용해 재실행할 수 있다. `--output` 아래에 두 재질의 원장과 집계를 생성한다.

```sh
python research/vanilla_textures/by_stage/1-1-02/TEX02-R018/VERIFY_ANIMATION_SCOPE.py \
    --jar /path/to/1.21.11.jar --output /tmp/animation-audit
```
