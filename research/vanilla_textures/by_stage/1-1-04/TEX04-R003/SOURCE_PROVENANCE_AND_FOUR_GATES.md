# TEX04-R003 — 4개 독립 인증 채널 및 파일 출처

## 실제 사용한 사용자 제공 원본

- 저장소: `sanato-nb/Minecraft_Furniture_Style_Research`, `main` → `1.21.11/` 디렉터리 (사용자가 직접 1.21.11 클라이언트 JAR을 압축 해제했다고 설명한 업로드본).
- 확인 파일: `assets/minecraft/textures/block/{white,red,blue,black,green,yellow,purple,cyan,orange}_wool.png` 9개, 대응 `models/block/{color}_wool.json` 9개, `blockstates/{color}_wool.json` 9개, 공통 `models/block/cube_all.json`, `models/block/cube.json`, `models/block/block.json`, 루트 `version.json`.
- `version.json`의 `id`와 `name`은 `1.21.11`, `world_version`은 `4671`, `protocol_version`은 `774`, `build_time`은 `2025-12-09T12:20:42+00:00`. 이 값은 **제공된 추출본 내부 메타데이터**일 뿐 Mojang 공식 배포 인증이 아니다. `version.json`의 Git blob SHA: `b49974d3ebd6cb73291d9e4c92d23b3192dadd66`.
- 사용자 제공 출처 자체는 **이 업로드본이 원본 JAR에서 추출됐다는 설명을 신뢰**하되 원본 JAR/다운로드 버전의 외부 무결성은 아직 독립 확인되지 않은 상태로 기록.

## 4개 독립 검증 항목

| 검증 축 | 실제 결과 | 상태 |
|---|---|---|
| **1. 사용자 제공 추출본** | 사용자 GitHub의 PNG 9개 바이트를 base64로 조회·디코딩, SHA-256 9개 재계산, PNG 시그니처·IHDR·PLTE·IDAT·IEND·청크 CRC32 검사; 모델 JSON 9개/블록 상태 JSON 9개 및 공통 부모 3개 파싱/참조 확인 | **9/9 소스 검증** (`user_provided_extraction_checked`) |
| **2. 기존 미러와 교차 검증** | PNG Git blob SHA **9/9 동일**, 모델 JSON 바이너리 **9/9 동일**(블랙 양털 과거 기록 오기 정정), blockstate JSON blob **9/9 동일**, `cube_all`/`cube` 같은 Git 객체; 9개 PNG SHA-256 모두 R001/v4와 동일 | **9/9 교차 검증** (`mirror_binary_crosschecked`) |
| **3. Mojang 공식 원본 인증** | 실제 원본 **client.jar** 전체 바이트·원본 SHA-1·Mojang 공식 version JSON 배포 해시 증빙 미확보 | **0/9, pending** |
| **4. 인게임 정적 검증** | 1.21.11 게임 실행·리소스팩·조명·카메라 고정 스크린샷 등 미확보 | **0/9, pending** |

### SHA 구분

- `user_extracted_png_sha256`: 9개 *PNG 파일 내용 자체*를 사용하여 계산한 SHA-256 (64자리).
- `git_blob_sha`: Git 저장소가 개별 경로 파일 바이트에 대해 부여하는 Git **blob SHA-1** (40자리, 헤더 포함 객체 식별자). JAR 전체 SHA-1과 무관함.
- `Mojang client.jar SHA-1`: 원본 JAR 전체 바이너리의 해시로, 위 두 유형과 비교해선 안 된다. 현 채팅에서 **계산하지 못함**.
- `R001/R002`에 기재된 미러 SHA와도 사용자 제공 소스 SHA를 독립적으로 비교했고, 불일치 0건.
- `R001/R002`의 2304개 RGBA 계측·36쌍 공간상관·9개 이음매 분석은 파일 내용이 같으므로 **재사용**. 새 텍스처/새 독립 픽셀 분석 결과로 중복 집계하지 않음.

애니메이션 프레임·움직임 연구는 계속 보류. Project Zomboid 변환 및 실제 가구 모델 제작도 범위에서 제외.
