# TEX05-R004 — 유리 6종의 아틀라스·정적 메타데이터·일반 블록 셰이더 소스 추가 감사

> 2026-11-13 | Minecraft Java 1.21.11 | **1-1-05 유리** | 선행 `TEX05-R001/R002/R003` 모두 불변 | 전역 `v38` 불변

## A — 선행 결과에서 미검증인 정적 출처만 선정

- GitHub 현재 단계는 `TEX05-R003`까지 저장되어 있음. 기존 6개의 PNG 실측, 1,536 RGBA, 36면 정적 상속 UV, 사용자 추출본의 PNG·모델·blockstate·item·parent JSON **27파일** 직접 검사는 변경하지 않았다.
- 이번에 새롭게 선택한 파일은 사용자 `1.21.11/assets/minecraft/`의 `textures/block/glass.png.mcmeta`, `atlases/blocks.json`, `shaders/core/block.fsh`, `shaders/core/block.vsh` **4개**. 다른 재질 텍스처나 유리창(pane) 모델을 새 표본에 추가하지 않음.

## B — 실제 원문·지문 대조

- 새 파일 4/4를 GitHub의 사용자 제공 1.21.11 추출본에서 직접 읽고 원문을 파싱/검사. `SOURCE_LEDGER.csv`에 개별 저장 경로·Git blob SHA·길이·정적 근거 저장.
- 대응하는 `InventivetalentDev/minecraft-assets` ref `1.21.11`의 같은 4개 파일도 직접 읽고 Git blob SHA 및 텍스트 일치 **4/4** 확인.
- 사용자 추출본 우선 검증 **기존 27개+새 4개 = 서로 다른 정적 경로 31개**. 새로운 고유 유리 PNG는 **0개**이며 기존 6개를 누적해서 10개로 늘리지 않는다.

## C/D1/D2 — 정적 PNG 알파값과 측정 범위

- R001에서 저장한 alpha0=191/alpha255=65인 `glass`, 착색 5종의 alpha102=191/155=5/163=60, R002 경계 비교 수치는 모두 그대로 사용. 별도 화소 측정·픽셀 재계산을 새 실적에 추가하지 않음.
- 이번 자원 정의 및 일반 셰이더 코드가 이런 알파값을 실제 월드에서 어떻게 혼합하는지 **직접 증명하지 않는다**.

## D — 유리 특화 정적 메타데이터 신규 근거

- `glass.png.mcmeta`의 파싱된 정적 항목은 `texture.mipmap_strategy="mean"`. 실제 파일 Git blob `5cb0fb739d59e745149bd602cc0d3cc2ee4f2d5b`.
- 같은 이름 규칙의 착색 유리 5종 `*.png.mcmeta`는 GitHub에서 각각 조회했지만 **5/5 파일이 존재하지 않음(404)**. 이는 명시 설정 파일의 부재이지 기본 필터 계산 방식의 검증이 아님.
- `mean`이라는 설정 문자열의 구체 구현, mipmap 결과, 전환 수준 또는 렌더 샘플링을 추측하지 않음.
- 세부 증거: `SPRITE_METADATA_MATRIX.csv`, `STATIC_RESOURCE_CONSTRAINTS.md`.

## E — 블록 아틀라스 디렉터리 규칙과 셰이더의 명시적 코드

- `atlases/blocks.json`의 `sources` 중 `type="minecraft:directory"`, `source="block"`, `prefix="block/"` 존재. 이는 6 leaf 모델의 `textures.all="minecraft:block/<id>"`와 **경로 규칙이 정적으로 연결**됨을 뒷받침한다. 다만 출력 아틀라스의 UV rect/해상도/패딩 위치는 없음.
- `shaders/core/block.fsh`: `Sampler0`에서 `texCoord0`의 색을 샘플링하고 `vertexColor`, `ColorModulator`로 변조. `#ifdef ALPHA_CUTOUT`일 때만 `color.a < ALPHA_CUTOUT` 비교 및 `discard` 실행. 이후 `apply_fog` 호출.
- `shaders/core/block.vsh`: `UV0 → texCoord0`, `Sampler2/UV2` 광원맵 샘플을 `Color`에 곱함. 정점 위치에는 `ModelViewMat` 및 `ProjMat` 사용.
- **증거 제한:** 위 두 프로그램은 **일반 block 셰이더의 정적 소스**일 뿐, 현재 6종 유리가 반드시 이 프로그램 또는 `ALPHA_CUTOUT` 정의를 사용한다는 런타임 바인딩 증거는 아니다. `block.fsh` 파일만으로 투명 블렌드·depth sort·인접 면 컬링·실제 조명을 특정하지 않음.
- 이전 R003에서 확인한 `cube_all→cube→block` 상속 구조와 위 아틀라스 규칙은 정적 리소스 수준에서만 상호 보완됨.

## F/D3 — 공식/인게임 검증 미완료 유지

| 구분 | 새 검증 | 단계 누적 |
|---|---:|---:|
| 사용자 제공 추출본 신규 정적 파일 | 4/4 | 구별되는 경로 31개 |
| 기존 미러 신규 정적 파일 대조 | 4/4 | 동일 Git blob 경로 31개 |
| Mojang 공식 1.21.11 client.jar SHA-1 인증 | 0 | 0/6 PNG |
| Minecraft 인게임 정적 렌더 확인 | 0 | 0/6 PNG |

- 아직 JAR 전체 바이트 무결성을 공식 Mojang 버전 메타데이터로 인증하지 않았고 실제 Minecraft 클라이언트를 실행하지 않았다. 따라서 **D3/F = pending**.
- 이 파일들에 런타임 변형 소스나 정의가 추가될 때는 후속 릴리스에서 증거를 구분해 기록해야 한다.

## G — 재현 자료 저장·이어받기

- `SOURCE_LEDGER.csv`: 신규 4개 소스의 사용자 제공 파일 SHA 및 미러 대조 표.
- `SPRITE_METADATA_MATRIX.csv`: 여섯 기존 유리 PNG의 atlas 경로 정적 합치 및 `.png.mcmeta` 명시 존재 여부, 기본값 미확정 분리.
- `STATIC_RESOURCE_CONSTRAINTS.md`: 소스 코드에서 단정 가능한 항목과 인게임 없이는 단정할 수 없는 항목의 경계.
- `SUMMARY.json`: 네 검증 수준, 신규 파일 4개/동일 대상 PNG 6개/기존 1,536 RGBA 등 중복 제거 수치.
- 위 `REPORT.md`, 신규 `TEX05-R004` 폴더 및 해당 단계 `STATE.json/HANDOFF.md`만 갱신. R001/R002/R003, 타 단계, 전역 v38 불변. 애니메이션·Project Zomboid 변환·가구 3D 모델 제작은 보류/제외.
- 다음 새 검증 릴리스 번호는 `TEX05-R005`, 단 반드시 GitHub의 현재 단계 상태·SHA·새 경로 존재 여부를 먼저 확인할 것.
