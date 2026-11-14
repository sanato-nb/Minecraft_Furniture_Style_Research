# v57 — 1-2-A P1 다른 모델 16개 원본·블록상태·PNG 검증

> 2026-11-14 KST · 시작 `main` HEAD `3f2b6098d146eb06771fa7d981ef4309fa6c91b1` · Minecraft Java 1.21.11 사용자 저장소 원본 JSON/PNG. v1~v56 수정·삭제 없음.

## 1. 과거 원장 보존 검증

원본 v55 544×198열, v56 544×209열 Git Blob API를 읽어 v55의 198열이 **544개 모델 전 셀 동일**함을 비교했다. 1-2-A의 원본 모델 식별 544/544 경로·SHA는 그대로 유지하며 이 수치를 의미론/렌더링 완료율로 사용하지 않는다. 이번 회차는 v53 신규175모델/49 PNG 경로와 겹치지 않는 P1 기존 나머지 369모델에서 **16개**를 선별했다. 과거 v5~v34에 SHA 근거가 있던 자료를 최초 발견으로 중복 계산하지 않는다.

## 2. 실제 JSON 소스·부모·면 연구

`00A_ORIGINAL_MODELS_AND_PARENTS.json`, `00B_ORIGINAL_MODELS.json`에 직접 가져온 소스 JSON, 전체 source path, Git blob SHA를 보존했다. `01_P1_16_GEOMETRY_AND_UV.json`과 `02_P1_16_FACE_EVIDENCE.csv`에서는 leaf의 **원본 자체 요소/면**과 부모로부터의 **상속 적용 요소/면**을 분리했다.

| 이번 16 P1 모델만의 측정 | 검사 결과 |
|---|---:|
| 원본 leaf 자체 요소 / 면 선언 | **33 / 156** |
| leaf 기준 상속 적용 요소 / 면 | **44 / 219** |
| 적용 face 원본 명시 UV | **95** |
| 적용 face 계산된 암시 UV 후보 | **124** |
| 적용 제로 두께 요소 | **1** |
| 적용 회전 요소 | **1** |

부모 원형을 상속한 서로 다른 leaf에서 적용 면 수가 반복되면 *적용 횟수*로만 계산한다. `stonecutter.json`의 하단 몸체는 [0,0,0]→[16,9,16], 톱날은 [1,9,8]→[15,16,8]인 양면 0두께 요소다. 톱날은 남·북 두 면에 서로 U 방향이 반대인 **명시 UV**를 선언한다. `lectern.json`에는 3개 요소, 상판 X축 **−22.5° 회전**이 있다. `composter.json`은 5요소/18면에 원본 UV가 생략돼 계산 후보와 반드시 구분한다. `anvil.json`은 자체 elements 없이 `template_anvil.json`의 4요소/21면을 상속하며 중복 원형 선언으로 세지 않는다.

이 계산 UV는 원본 JSON face 키가 없을 때 기하에서 만든 **후보**이며, Minecraft 1.21.11 공식 엔진 UV 계산/전개를 인증한 것이 아니다.

## 3. 원본 블록상태

13개 `1.21.11/assets/minecraft/blockstates/*.json` 원문 및 SHA를 직접 읽어 variants **37개 키**, multipart **68개 규칙**, 모델 apply **105건**을 보존했다. 예컨대 `barrel.json` 12개 variant와 `composter.json` 9개 multipart 규칙은 소스 JSON 데이터로 확인했으며, 실제 월드의 상태 생성·무작위 적용·uvlock 회전의 런타임 확인과 별개다.

## 4. 실제 원본 PNG 바이너리·Pillow RGBA

GitHub 원본 PNG 바이너리 Base64를 직접 얻어 Python에서 표준 base64·hashlib `blob {n}\\0` SHA-1와 SHA-256을 계산하고 Pillow로 RGBA를 전픽셀 복원했다.

| 이번 직접 확인한 PNG | 크기 | 실제 RGBA 픽셀 | alpha0 | alpha255 |
|---|---:|---:|---:|---:|
| `bookshelf.png` | 16×16 | 256 | 0 | 256 |
| `barrel_top_open.png` | 16×16 | 256 | 0 | 256 |
| `stonecutter_saw.png` | 16×48 | 768 | 522 | 246 |
| `composter_side.png` | 16×16 | 256 | 0 | 256 |
| **합계** | | **1,536** | **522** | **1,014** |

원본 SHA 근거는 `04_ORIGINAL_PNG_PILLOW_4.json`. `stonecutter_saw.png`는 16×48 소스이므로 16×16 수직 스트립 3개를 각각 관찰했다. 상단 스트립에서 원본 **명시 UV** [1,9,15,16] 및 반대 방향 [15,9,1,16]의 픽셀은 각각 98개, alpha255 82/alpha0 16개다. 두 면 중복 포함 **196회 소스 픽셀 관측**, 164 불투명·32 투명, 중복 제외 98 좌표. `05_STONECUTTER_ORIGINAL_UV_PIXEL_SAMPLES.json`에 남겼다. 이는 렌더링 결과나 전체 3프레임 애니메이션 재생 확인이 아니다.

## 5. 특수 렌더러 보조 근거

사용자 저장소에 없는 **제3자 1.21.11 디컴파일된 Java 소스**도 별도 조사했다. `ShulkerModel.createBoxLayer`는 lid 16×12×16, base 16×8×16을 선언하며, `ShulkerBoxRenderer`가 뚜껑 위치·회전을 열림 진행률에 따라 변경한다. `SkullModel`의 일반 머리는 8×8×8이고 인간형의 겉모자 팽창 구조가 있으며, `SkullSpecialRenderer`가 종류별 모델을 골라 사용한다. 정확한 커뮤니티 코드 경로·Git SHA는 `09_SECONDARY_RENDERER_JAVA_EVIDENCE.json`에 보존했다. 공식 Mojang 클라이언트 JAR SHA·인게임 출력 확인은 수행하지 않았다. 따라서 이전 **셜커13+skull1=14 렌더러 미해결 상태는 유지**한다.

## 6. 중복·한계 및 다음 이어갈 점

v54~v56 기존 코호트 **49/49 원본 PNG·3,393 source face·51,228 반복 포함 source 픽셀 관측**은 변경·신규 재집계하지 않는다. v55/v56 케이크 암시 UV 168 후보도 엔진 공식 인증으로 승격하지 않았다. 새 4 PNG는 **이번 별도 P1 모델 범위**에서 측정한 파일이며 기존 전체 P1의 PNG/UV 완료율을 나타내지 않는다. 다른 P1 모델·텍스처의 원본 UV·블록상태 결합·스타일 패턴 전수 검사 및 역사 의미론적 근거 통합이 계속 필요하다.

**1-1 150/150 승인 완료, 상위 5개 연구 중 1/5 완료 유지, 1-2-A·1-2 진행 중·실질 완료율 미산정.** 가구 제작 또는 Project Zomboid 변환 시작하지 않았다.
