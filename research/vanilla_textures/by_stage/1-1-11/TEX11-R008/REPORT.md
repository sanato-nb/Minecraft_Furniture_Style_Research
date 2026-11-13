# TEX11-R008 — 문 112상태의 원본 면 UV 접합 및 다락문 RGBA 대칭 보완

**날짜:** 2026-11-13 · **단계:** 1-1-11 목재·구조부품 (고정 31 PNG) · **이전:** TEX11-R007 · **다음:** TEX11-R009

## 1. 출처 / 작업 경계
- **원본:** 사용자가 Minecraft Java 1.21.11 JAR에서 추출해 GitHub에 제공한 `1.21.11/`. 이번 회차에 실파일 **7개 문 blockstate JSON, 8개 문 모델 템플릿 JSON, 문 14 PNG blob**, 다락문 PNG 12개를 조회했다. 14개 문 PNG의 경계 RGBA 샘플은 **R007의 실제 픽셀 원장** `DOOR_SEAM_PIXEL_DETAIL.csv`를 재사용하며, 이번 버전의 독립 신규 PNG 전체 재해시·재디코딩 수에 합산하지 않는다. 다락문 12 PNG는 **이번 회차에 CRC와 실제 RGBA를 새로 디코딩했다**.
- **과거 근거는 계승만:** 31 PNG, 모델 리프127, blockstate 규칙512, 정적 조합544, 모델 배치672, 회전 면4,320, 기하 정렬 문 112쌍, R007 문 원본 112개 경계 픽셀 쌍 및 71 UV 패치. `v38`의 참나무 선반 32상태는 이번 계측 분모에도 들어가지 않는다.
- **이번 신규 증거:** 문 상·하 상태 쌍 **112개**에 대해 상/하 모델 참조와 각 모델 **2개 넓은 면(west/east)의 실제 JSON UV·회전/cullface 대응**을 결합한 **224개 상태·면 검사**, 모델 UV에 매핑한 **56개 고유 면 구성×16열=896 모델-픽셀 결합 검사**, 각 facing으로 4배 복제한 **3,584 상태·면 픽셀 투영 사용**. 이 3,584는 새로운 독립 PNG 픽셀이 아니라 **R007 실화소 결과를 상태별로 반복 참조한 수**다.
- 별도 개선: R007 `UV_ORIENTATION_CANDIDATES.csv`의 다락문 행은 CSV 첫 행(선반)의 열 스키마를 사용한 탓에 **다락문 특유 대칭값 칸이 빠져 있었다**. R007 불변 보존, 이번 `TRAPDOOR_SYMMETRY_REMEASURED.csv`에 사용자 PNG를 직접 재샘플해 기록했다.

## 2. 문 상/하 모델 넓은 면 대응 — 이번 새 정적 소스 검증
- **입력 JSON:** `1.21.11/assets/minecraft/blockstates/{oak,acacia,spruce,birch,cherry,bamboo,mangrove}_door.json`의 **224 상태 variant**. 각 재질의 `facing` 4 × `hinge` 2 × `open` 2 상태에서 lower/upper를 쌍으로 만들었고, 양측 모델에 지정된 X/Y 회전이 동일한지 확인. 리프명은 해당 재질/half/hinge/open에 따라 8개 공유 템플릿 중 하나에 연결하고, 현재 파일의 source blob SHA를 CSV에 보존.
- 각 면 `west/east`의 모델 `faces[].uv = [u0,v0,u1,v1]`에서 상단 PNG y15와 하단 PNG y0의 x 대응을 `floor(u0 + (u1-u0)·(x+0.5)/16)`으로 계산. 두 half의 대응 U 순서, V [0,16], 동일 회전, cullface 상태를 면별로 대조.
- **224/224 상태·면 UV 정렬**, **224/224 cullface 지정 일치**. 단, 한쪽 면의 `cullface`가 비어 있는 구성도 원본 정의대로 기록했으므로, 실제 가려짐을 확인했다는 뜻은 아니다.
- 평행 면의 법선은 블록상태 Y 회전을 **오른손좌표계 중심 (8,8,8)의 단위 90° 회전**으로 소스 투영해 world-face를 기록. 엔진 실측/렌더링과는 별개.
- 아래 표의 alpha 불일치 사용 수는 16개 상·하 상태 쌍×2면×16열(재질별 512픽셀 투영 참조)에 대한 값이며 **동일 물리 원본 텍셀을 방향마다 중복 참조**한다.

| 목재 | 면 상태 검사 | alpha 불일치 상태·면 픽셀 사용 수 | R007 원본 경계 열 |
|---|---:|---:|---|
| oak | 32 | 0 | — |
| acacia | 32 | 0 | — |
| spruce | 32 | 0 | — |
| birch | 32 | 0 | — |
| cherry | 32 | 128 | 4|6|9|11 |
| bamboo | 32 | 0 | — |
| mangrove | 32 | 0 | — |

- 벚나무는 R007의 독립 원본 경계 `x=4,6,9,11` 4열이 **모델 face의 U 반전에 따라 위치만 역전**되고, 112 상태의 재질별 복제 시 **총 128개의 alpha 불일치 투영 사용**으로 기록된다. **새로 발견한 128개 물리 픽셀 결함이 아니며**, 서로 다른 실제 인게임 얼굴/빛/가림에서 보이는 결함이 입증된 것도 아니다.
- 증거: `DOOR_FACE_STATE_UV_SEAMS.csv`(224 상태·면), `DOOR_FACE_PIXEL_UV_BINDINGS.csv`(56 고유 모델-면 구성×16열), `CHERRY_DOOR_UV_EDGE_DIAGNOSTIC.svg`(원본 RGBA를 face UV 순서로 배치한 정적 이미지).

## 3. 다락문 PNG RGB/alpha 반전 대칭 — 누락값 직접 복구
- 사용자 제공 `1.21.11/assets/minecraft/textures/block/*_trapdoor.png` **12종 모두**를 바이트 수준에서 열어 CRC 검증 **12/12**, 16×16, **3,072개 고유 RGBA 텍셀** 디코딩. 각 256픽셀에 대해 좌우 반전과 상하 반전의 RGBA 완전 동일 여부, alpha 불일치 및 RGB 채널 L1 합계를 계산해 **6,144방향별 픽셀 비교 사용** 기록.
- **alpha 완전 좌우 대칭 11/12, alpha 완전 상하 대칭 10/12**. 예외: `warped_trapdoor`은 좌우 alpha 불일치 **38**, 상하 **30**; `jungle_trapdoor`은 상하 **20**.
- **실제 RGBA 전채널 완전 대칭인 PNG는 좌우 0/12, 상하 0/12**. 구멍의 알파 마스크 대칭과 RGB 목재 무늬/색상 대칭은 별개라서 방향 판정은 PNG와 UV를 동시에 봐야 한다.

| 원본 PNG | 투명 텍셀 | 좌우 알파 차이 | 상하 알파 차이 | 좌우 일치 RGBA /256 | 상하 일치 RGBA /256 |
|---|---:|---:|---:|---:|---:|
| acacia_trapdoor | 60 | 0 | 0 | 170 | 172 |
| bamboo_trapdoor | 44 | 0 | 0 | 190 | 164 |
| birch_trapdoor | 0 | 0 | 0 | 150 | 110 |
| cherry_trapdoor | 36 | 0 | 0 | 148 | 126 |
| crimson_trapdoor | 40 | 0 | 0 | 138 | 148 |
| dark_oak_trapdoor | 0 | 0 | 0 | 120 | 104 |
| jungle_trapdoor | 42 | 0 | 20 | 212 | 126 |
| mangrove_trapdoor | 32 | 0 | 0 | 222 | 162 |
| oak_trapdoor | 36 | 0 | 0 | 156 | 152 |
| pale_oak_trapdoor | 0 | 0 | 0 | 126 | 130 |
| spruce_trapdoor | 0 | 0 | 0 | 106 | 122 |
| warped_trapdoor | 55 | 38 | 30 | 98 | 122 |

- **주의:** 이미지 자체의 반전 대칭은 게임에서 `facing`·`half`·`open` 상태가 어떻게 그려지는지 증명하지 않는다. 열림 상태는 정적 상태만 검토하며 **애니메이션/시간 흐름은 이번에도 전면 보류**.

## 4. 보존·다음 연구
- **실제 인게임 정적 렌더링 증거: 0/31** 유지. 이번 source-face 검증 결과는 실제 엔진 GPU UV, alpha test, blending, culling, 광원/그림자, 스크린샷 인증이 아니다.
- **Mojang 공식 원본 client.jar 전체 SHA-1과 공식 메타데이터 인증은 필수 연구/완료 분모에서 제외.** 이를 검증 성공이라 하지 않는다.
- 다른 1-1 재질 단계, `v38`, 루트 HANDOFF/PROGRESS, 애니메이션 기록, 프로젝트 좀보이드 변환, 실제 가구 3D 제작에는 손대지 않음.
- 다음 R009에서는 가능하다면 **실제 게임 정적 화면**과 특정 상태(yaw/hinge/open/half)를 캡처하여 warped/jungle 다락문 alpha 비대칭 및 벚나무 door seam을 대조. 스크린샷 없는 경우 source-only 측정으로 따로 유지하며 게임 검증 수를 늘리지 않는다.
