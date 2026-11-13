# TEX10-R004 — 1-1-10 잎·식생: 추출본 색상표 2종의 PNG 화소 직접 실측 + 블록 아틀라스·버전 연결

> Minecraft Java 1.21.11, 2026-11-13. 대상 텍스처 **8종 유지**. 새로 검사한 2개 `colormap` 이미지는 **보조 증거**이며 v4 선정 8개에 더해 10개로 집계하지 않는다. `TEX10-R001`~`R003` 파일 불변, 공통 `v38` 불변. 애니메이션 금지.

## 조사 경위 및 새로 검사한 경로

사용자 제공 JAR 추출본의 `1.21.11/`을 최우선으로 사용했다. 기존 R001은 8개의 블록 PNG·44 선언 면/UV, R002는 128행 알파·덩굴 32 상태, R003은 블록 상태→모델→PNG 연결 28개 경로와 4개 검증 축을 기록. **이번에는 그 동일 측정을 재집계하지 않고**, 다음 **신규 4개 파일 경로**를 직접 읽었다.

- `1.21.11/assets/minecraft/textures/colormap/foliage.png` (Git blob `d58fce229108e9e6e188ed13baa75bc432ead19a`)
- `1.21.11/assets/minecraft/textures/colormap/grass.png` (Git blob `f2e783063d40120245cd7141349681305e773831`)
- `1.21.11/assets/minecraft/atlases/blocks.json` (Git blob `541ce56ad0b09f258963dd2bf3e3cb6e786d2d79`)
- `1.21.11/version.json` (Git blob `b49974d3ebd6cb73291d9e4c92d23b3192dadd66`)

이 4개 경로는 R003에서 완료한 28개 고유 경로와 중복하지 않아, R003–R004 누적 **32개 고유 리소스 경로 조회**에 해당한다. **연구 표본 수는 계속 8개**.

## D2 / B–C: 색상표 PNG 실바이트 검증 결과

GitHub 연결을 통해 각 PNG **Base64를 실제로 읽고**, JavaScript에서 PNG 청크·CRC32·zlib/DEFLATE 압축·Adler-32·필터를 해제해 실제 **256×256 RGB 값 65,536픽셀/파일**을 검사했다. 두 색상표 합계 **131,072개 RGB 픽셀**은 R001/R002의 대상 블록 PNG 2,048 RGBA 픽셀과 완전히 다른 **보조 자료 실측**으로 구분.

| 색상표 | 원본 PNG 바이트 | 이미지 크기 | 모드 | 색상 수(고유 RGB) | 평균 RGB | CRC·Adler32 |
|---|---:|---|---|---:|---|---|
| `foliage.png` | 14,154 | 256×256 | 8-bit RGB (alpha 없음) | **8,837** | (95.121, 162.376, 70.843) | 둘 다 통과 |
| `grass.png` | 5,930 | 256×256 | 8-bit RGB (alpha 없음) | **4,536** | (196.219, 221.512, 176.053) | 둘 다 통과 |

- foliage RGB 채널 최소 **[26,147,0]**, 최대 **[174,191,147]**. RGB 값은 좌표마다 다르며 보편적인 단일 잎 녹색으로 축약하면 안 된다.
- grass RGB 최소 **[71,180,51]**, 최대 **[255,255,255]**. 정확하게 흰색 `#FFFFFF`인 위치가 **32,640개**(전체의 약 **49.8047%**). 이 숫자는 정적 화소 분포일 뿐, 게임이 이 영역을 실제 선택하는지의 여부를 입증하지 않는다.
- 색상표 샘플 비교: (128,128) foliage `#5BAB47`, grass `#7CBD6C`; (0,0) foliage `#1ABF00`, grass `#47CD33`; (255,255) foliage `#60A17B`, grass `#80B497`. 전 24개 샘플을 [COLORMAP_SAMPLE_PIXELS.csv](COLORMAP_SAMPLE_PIXELS.csv)에 기록.
- 두 PNG의 필터 분포와 주요 5색·원본 해시·표본 좌표를 [COLORMAP_AUDIT.json](COLORMAP_AUDIT.json)에 보존. **최종 biome RGB나 나무 종별 tint 계산을 재현한 결과가 아니다**.

## E: 블록 아틀라스 정적 포함 조건 직접 확인

`atlases/blocks.json` 실제 JSON에는 총 4개 `sources`가 있으며, 하나가 `{"type":"minecraft:directory","prefix":"block/","source":"block"}`이다. 따라서 기존 8개 텍스처의 경로 `textures/block/{id}.png`는 이 **디렉터리 선택 규칙**에 해당한다. 각 파일이 atlas JSON에 한 줄씩 이름으로 명시된 것은 아니다.

반대로 `textures/colormap/foliage.png`와 `grass.png`는 이 **블록 디렉터리 규칙 밖**이며 `atlases/blocks.json`에 `colormap/` 디렉터리 소스가 나타나지 않았다. 이것은 **이 아틀라스 선언에 명시되지 않았다**는 사실이지 게임에서 색상표를 로드하지 않는다거나 바이옴 tint에 쓰이지 않는다는 뜻이 아니다. 런타임 코드/렌더 확인은 F에서 아직 미완료.

## 부록: extracted version.json과 공식 인증 구분

사용자 추출본의 `version.json`은 `id:"1.21.11"`, world version **4671**, protocol **774**, resource pack major **75**, Java **21**, build time `2025-12-09T12:20:42+00:00`으로 기록한다. 이것은 압축 해제 자료 내부의 **버전 표지 메타데이터**로써 확인한 것이다. Mojang이 배포한 **전체 `client.jar` SHA-1**을 직접 확보해 공식 버전 매니페스트의 `downloads.client.sha1`과 대조했다는 뜻이 아니다.

## A–G / 네 단계 독립 검증 판정

1. **사용자 제공 추출본 직접 검사:** 기존 8개 대상 파일의 정적 검사 **8/8 유지** + 이번 신규 색상표 **2개 PNG 바이트/픽셀 실측**, 아틀라스·내부 버전 JSON 조회. 사용자 제공 JAR 추출이라는 출처는 **사용자 진술**.
2. **기존 비공식 미러와 비교:** 이전 R001에서 대상 PNG **8/8 동일** 확인 결과 계승, 새 미러 다운로드 **0건**. 색상표 2종의 미러 교차 여부는 이번에 별도로 확인하지 않았음.
3. **Mojang 공식 전체 JAR SHA-1 인증:** **0/8 미완료**. 전체 JAR 바이트와 Mojang 공식 버전 메타데이터 대조 필요.
4. **인게임 정적 검증:** **0/8 미완료**. 해당 클라이언트의 정적 생물군계 tint·텍스처 아틀라스·렌더/색상·그래픽 프리셋·mipmap 변수를 관측해야 함. [Mojang 1.21.11 릴리스 노트](https://www.minecraft.net/en-us/article/minecraft-java-edition-1-21-11)는 그래픽 프리셋과 블록 mipmap 변경을 설명하므로, 향후 실험에서 설정을 함께 기록하는 편이 타당하다.

**애니메이션/움직임/프레임 분석은 계속 금지**. Project Zomboid 변환 또는 실제 가구 3D 모델 제작 없음. 새로운 완료 단계에 대한 독립 근거가 있을 때만 다음 `TEX10-R005`로 진행. 본 결과를 기존 8개 텍스처를 다시 검수한 8/8 신규 완료로 누적하지 말 것.
