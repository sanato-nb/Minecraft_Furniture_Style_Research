# INT-4 Another Furniture variant=3 남쪽 모델 선택·원본 등받이 텍스처 교차검증

## 공식 INT 단계

본 작업은 INT-4 '연구 결과 간 교차 검증'의 남은 **원본 모델 선택 규칙 이상 1건(관련 검토방향 4행)**을 깊이 조사한다. 완료하더라도 INT-4 전체 종료, INT-5 실제 게임 개별 부품 역할 검증, INT-6 AI 학습 적격성 승인으로 승격하지 않는다.

## 실제 원본에서 발견한 사항

원본 연구 4.0.3 Git commit: \`57eb624cbb7f408d43398c7434b0d38d312cb55d\` (변경 금지).
정확한 원본 JSON: \`common/src/main/resources/assets/another_furniture/blockstates/acacia_chair.json\`, Git blob \`37643398d7a49fdcfc6f2308ca04c13fb0b43aed\`.

| 원본 선택자 | 실제 지정 모델 | y |
|---|---|---:|
| \`facing=north,tucked=false,variant=3\` | \`acacia_3\` | 0 |
| \`facing=east,tucked=false,variant=3\` | \`acacia_3\` | 90 |
| **\`facing=south,tucked=false,variant=3\`** | **\`acacia_1\`** | 180 |
| \`facing=west,tucked=false,variant=3\` | \`acacia_3\` | 270 |

이전 INT-3 보고서의 4는 서로 비교한 **검토대상 원본 상태 4행**을 뜻하며, 실제 방향별 *선택 불연속*은 **남쪽 1건**이다. 원본이 의도한 디자인인지 수정 누락인지는 아직 알 수 없으므로 임의 교정하지 않는다.

- \`acacia_1.json\` Git blob: \`609dea1eda246be610ed0a5762f3bb5f0ce9db92\`.
- \`acacia_3.json\` Git blob: \`ef6b6e633205b62768cbc60d1c1731ab7d219c66\`.
- 두 자식 모델 모두 동일한 원본 부모 \`another_furniture:block/template/chair\` (Git blob \`d9b64a818021f1a64b0cba13d16d18d6fea65d01\`)를 참조한다.
- 원본 모델 JSON의 \`textures.bottom\`/ \`textures.seat\` 결합은 동일하며, \`textures.back\`은 \`back_1/acacia\` / \`back_3/acacia\`로 달라진다.
- 원본 등받이 PNG Git blob: \`back_1/acacia.png\` = \`55f3bbf986c0c10b731cc0e67038402f30340972\`, \`back_3/acacia.png\` = \`e2282f2620fc8fbbcfd3bb69ab2a435e5421bbe8\`. 바이트/해시 불일치와 실제 RGBA 픽셀 차이는 **다른 주장**이다.

## 이번 원본 독립 실행 비교 항목

\`src/mcfr/int4_af_variant3_texture_audit.py\`:
- 연구 4.0.3 고정 Git commit에서 6개 원본 파일을 SHA-1 검증해 수집.
- PR #35와 같은 4.0.2 실행 JAR을 원본 고정 SHA-1로 재다운로드하고, 내부 6개 소스 파일 비교.
- 블록상태 88개 전체 의미상 동일 여부 및 \`variant=3,tucked=false\`의 4방향 실제 선택 검증.
- \`acacia_1\` / \`acacia_3\` 두 자식 모델과 상속된 10요소·46면의 기하·UV 및 각 면의 실제 해석된 텍스처 바인딩을 비교.
- 원본 \`back_1\`/ \`back_3\` PNG 양측 릴리스 화소 디코딩 후 RGBA 및 검정/흰색 배경 합성으로 다른 픽셀 개수 계산. 릴리스 간 PNG 원본의 동일성도 별도로 측정.
- 비유사 원본 JAR/PNG/JSON 재배포 금지: 방향·면별 메타데이터 CSV 2종, SHA·카운트 JSON만 Actions 아티팩트로 보존.

테스트: \`tests/knowledge/test_int4_af_variant3_texture_audit.py\`.
Actions: \`.github/workflows/integration-int4-af-variant3.yml\`.

## 판정 범위

- **정적 원본 소스 수준의 남쪽 모델/등받이 참조 차이**를 확인하더라도 실제 게임에서 그 면이 관찰·조명·컬링되어 다른 색으로 보인다는 뜻은 아니다.
- PR #33/34의 16방향 F2는 \`variant=1\`과 \`variant=10,tucked=true\` 등을 촬영했지, **이번 \`variant=3\`의 4방향을 촬영한 자료가 아니다.** 새 런타임 이미지를 촬영하지 않았으면 \`int5_screenshot_variant3_taken=false\`로 유지한다.
- 부품 역할/재료/스타일/라이선스/AI 학습 승인 수 0. 기존 1단계 원본 31,242개·INT-0~3 결과·PR #36 근거는 무수정.
- CI 확인 전에는 실제 PNG의 서로 다른 픽셀 수를 예단하지 않는다. 성공 CI의 실행 SHA·카운트는 추후 별도 고정 체크포인트로 기록한다.

**다음:** 원본 픽셀 비교에서 의미 있는 차이가 발견되면, INT-5에서 실제 Minecraft \`variant=3\` 4방향을 동일 촬영 조건으로 F2 재현하여 화면에 나타나는 차이를 별도로 관찰한다. 원본 의도(버그인지 연출인지)는 제작자 근거 없이 확정하지 않는다.

## 실제 원본 JAR/PNG 독립 CI 결과 — 2026-11-21

[GitHub Actions #44910385797](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44910385797) **성공**, 독립 오프라인 회귀테스트 **8/8 통과**.

| 검사 범위 | 실제 확정값 |
|---|---:|
| 연구 4.0.3·실행 4.0.2 선택 규칙 | 88/88 의미상 일치 |
| 4개 방향 검토 원본 상태 | 4 |
| 서로 다른 모델이 선택되는 방향 | 남쪽 **1건** |
| 두 모델의 원본 요소/면 | 10요소 / 46면 |
| 두 모델 간 기하·UV 차이 | **0** |
| 등받이 텍스처 바인딩이 달라지는 면 | **12/46** (요소 7·8·9) |
| 같은 바인딩을 유지하는 면 | 34/46 |
| `back_1` ↔ `back_3` 실제 RGBA 화소 차이 | **54/256픽셀** (16×16) |
| 불투명 검정/흰색 배경 합성에서 차이 | 각 **54/256픽셀** |
| 4.0.2와 4.0.3의 `back_1` PNG 화소 차이 | **0/256** |
| 4.0.2와 4.0.3의 `back_3` PNG 화소 차이 | **0/256** |

즉 기존 4.0.2 대 4.0.3 **버전 간 차이는 없는 반면**, 동일한 버전에서 남쪽의 `acacia_1` 선택 때문에 등받이 텍스처 참조가 다른 현상은 실제 원본 RGBA 수준으로 확인되었다.

**판정:** `SOURCE_CONFIRMED_DIRECTIONAL_BACK_TEXTURE_DISCONTINUITY` (원본 정적 선택·화소 차이 확정). 부품 의미 확정이나 실제 Minecraft 3번 변형 화면 검증이 아니라서 INT-5 승인으로 승격하지 않는다.

- 원본 Git/JAR 모델·PNG는 저장소에 복제하거나 공개 아티팩트로 배포하지 않았음.
- 비교 CSV 2종의 SHA와 전체 JAR·모델·원본 PNG SHA의 재현 정보는 [영구 고정 결과](INT4_AF_VARIANT3_PIXEL_AUDIT_RESULT.json)에 보존.
- 액션 아티팩트 `int4-af-variant3-original-back-texture-difference`, ID 14709259524, ZIP SHA-256 `81d661cf88543fa9ac0b8b06725d5b22f23f6dd00b60a57a872f17bddc34765c`.
- 이후 CI에서는 동일한 원본 취득·픽셀 비교 결과가 고정 체크포인트와 **완전히 동일**해야만 통과한다.
- **미완:** 3번 변형의 4방향 실제 F2, 제작자의 선택 의도, 실제 baked UV/렌더, INT-4 전체 가구 유형 교차검증, 제3자 권리 확인.
