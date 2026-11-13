# TEX04-R009 — 보류 애니메이션 재개: 양털 9종 비애니메이션 텍스처 소스 검증

> 2026-11-13 · **사용자가 애니메이션 연구 재개를 명시적으로 지시한 후 신규 검사 수행**. 대상은 1-1-04의 사용자 제공 Minecraft Java 1.21.11 추출 양털 9종. R001–R008 및 정적 연구 완료 보고서는 불변. 인게임 증거는 여전히 필수 제외.

## 결론

**9종 양털 모두 원본 1.21.11 소스에 정의된 텍스처 애니메이션이 없음(0/9).** 소스 내 `<color>_wool.png.mcmeta` 9개를 직접 경로 조회했으나 **전부 GitHub 404**. 실제 PNG 9개를 바이너리로 다시 읽어 PNG 시그니처/IHDR/청크 구조를 검사한 결과 모두 **16×16 단일 PNG 이미지(수직 다중 프레임 없음)**였고 **APNG 관련 `acTL`, `fcTL`, `fdAT` 청크도 0**.

이는 **사용자 추출본에 정의된 바닐라 리소스 텍스처 애니메이션이 없다**는 판정이며, Minecraft 엔진의 모든 시간 의존 효과·게임 화면·모드/외부 리소스팩 효과가 없음을 의미하지 않는다.

## 실제 조사 항목

1. **9개 정확한 메타데이터 경로**: `1.21.11/assets/minecraft/textures/block/{white,red,blue,black,green,yellow,purple,cyan,orange}_wool.png.mcmeta` 각각 경로 조회. **파일 존재 0/9**.
2. **9개 원본 PNG 실제 바이너리**: 각 파일 Git blob SHA를 기록, 바이트 해석에서 PNG IHDR = 16×16, PNG color type = 3(Indexed palette), bit depth = 8, 청크 순서 모두 `IHDR → PLTE → IDAT → IEND`. APNG chunk 부재. PNG 9종 크기 360~399바이트, 각 16×16 프레임을 단 하나 보유.
3. **9개 블록 leaf 모델**: `parent: minecraft:block/cube_all` + `textures.all: minecraft:block/<same_color>_wool`; JSON leaf의 다른 필드는 0.
4. **9개 blockstate**: 빈 키 `""` 하나의 고정 variant로 해당 leaf 모델 참조; 추가 상태 분기 0.
5. **9개 item 정의**: `model.type=minecraft:model`, `model.model=minecraft:block/<same_color>_wool`로 단일 모델 참조. 애니메이션/프레임/시간 분기 0.
6. **공통 상속**: `cube_all→cube→block`의 정적 모델 face/텍스처 슬롯 상속을 다시 확인; 블록/아이템이 따로 애니메이션 모델을 참조하는 증거 없음.
7. **1.21.11 block atlas**: `assets/minecraft/atlases/blocks.json`이 `source:block`, `prefix:block/` 디렉터리 소스를 포함. 따라서 일반 block atlas의 소스 대상임을 확인. 별도 양털 애니메이션 스프라이트 선언은 관찰되지 않음.

## 대조군: 같은 추출본에 실제 존재하는 애니메이션 3개

| 텍스처 | 원본 PNG 크기 | 16×16 프레임 수 | 해당 `.png.mcmeta` | 설정 |
|---|---|---:|---|---|
| `water_still` | 16×512 | 32 | 있음 | `animation.frametime=2`; `frames` 미기재 → 기본 프레임 순서 |
| `lava_still` | 16×320 | 20 | 있음 | `frametime=2`, **38개의 명시적 재생 프레임 항목**(20개 고유 프레임 반복) |
| `fire_0` | 16×512 | 32 | 있음 | `frames` **32개**, `frametime` 기본 1, 재생 순서 16~31→0~15 |

대조군의 PNG에는 APNG chunk가 없음에도 .png.mcmeta/세로 스프라이트 시트로 애니메이션이 정의된다. 따라서 `APNG 여부` **하나만으로** 일반 Minecraft 텍스처 애니메이션을 판단해서는 안 되며, **메타데이터+PNG 프레임 구조를 같이 확인**했다.

Minecraft Wiki의 Java Resource pack 설명 또한 `texture.png.mcmeta`의 `animation`이 없으면 해당 텍스처는 정적으로 취급됨을 설명한다: https://minecraft.wiki/w/Resource_packs#Texture_animation . 이 일반 형식 설명은 **외부 참고 문헌**이고, 위 파일 존재 여부/바이트 크기/JSON 연결은 **사용자 제공 1.21.11 원본 직접 검사 결과**다.

## 애니메이션 연구와 이전 결과 관계

- 1-1-04 양털 9종은 **기존 정적 소스 분석 R001–R008 완료** 및 **추가 애니메이션 대상 없음(9/9 증명 범위)**.
- 이 단계에서 애니메이션 연구는 사용자의 재개 지시에 따라 실제 파일 실사로 수행해 **완료(애니메이션 자원 검출 0)**. 새 프레임 합계 0. **새 고유 양털 PNG 0, 새로운 고유 원본 픽셀 0, 새 model face 0**. R001의 원본 2,304픽셀, R003 54면을 다시 신규 계수하지 않는다.
- 실제 게임의 UI·광원·리소스팩·모드 렌더링을 실행하거나 관찰하지 않았고, 인게임 0/9 역사적 숫자는 그대로 **필수 제외**.
- 공식 배포 JAR 전체 SHA1과 공식 Mojang 메타데이터 인증 역시 필수 범위 제외이며 성공을 주장하지 않는다.
- 다른 종류의 블록(물·용암·불 등)의 **전체 애니메이션 연구**는 이 1-1-04에서 하지 않았다. 위 3종은 진단 정확성을 점검하기 위한 대조군이지 이 단계의 완료 대상에 포함되지 않는다.
- Project Zomboid 변환, 실제 마인크래프트 가구 3D 모델 제작, 다른 1-1 단계는 이 결과 범위 밖.

## 저장된 산출물

- `WOOL_ANIMATION_SOURCE_AUDIT_9.csv`: 9종 메타 부재/PNG 구조/모델·아이템 연결을 행별로 기록.
- `ANIMATED_POSITIVE_CONTROLS_3.csv`: 물·용암·불 대조군 프레임·메타데이터 진단.
- `REPRODUCE_ANIMATION_AUDIT_R009.py`: 사용자 추출본 `1.21.11/` 위치를 인수로 받아 PNG CRC/IHDR/프레임/APNG chunk, 메타 존재 여부, static model/item 연결, 대조군을 자동 재검사하는 표준 라이브러리 Python 코드. 발표 이후 외부 사용자 환경에서 전 과정을 재실행했다고 주장하지 않음.
- `SUMMARY.json`: 범위·검증 수·제외 기준.

**최종:** 양털 애니메이션 연구는 사용자 소스 범위에서 **완료**. 9개 모두 애니메이션 프레임 전환 정의 없음. 다음 R010 후보는 새로운 원본 범위/반례가 생긴 경우에만. `계속해줘` 입력만으로 이 범위에서 반복 검증을 무의미하게 늘리지 않는다.
