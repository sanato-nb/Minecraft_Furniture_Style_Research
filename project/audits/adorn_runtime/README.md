# H7 후속 · Adorn 런타임과 조건부 오버레이 검증

Minecraft Java 1.21.11에서 [Adorn 7.6.0](https://modrinth.com/mod/adorn/version/MwMpNgec)과 [7.6.1](https://modrinth.com/mod/adorn/version/tyOUUBLZ)의 같은 고정 배포본을 실행했다. Fabric Loader 0.19.3과 Fabric API 0.141.6을 사용했다. 작업 월드는 한 창작 월드를 버전별로 복사해 만들었고 Biomes We’ve Gone은 설치하지 않았다. [배포 입력 핀](../h67/ADORN_PINS.json) · [계수와 해시](RESULT.json)

| 검증 | 7.6.0 | 7.6.1 |
|---|---:|---:|
| Adorn 블록 유형 | 679 | 679 |
| 등록 블록 상태 | 41,211 | 41,211 |
| 충돌 상자 | 175,032 | 175,032 |
| 충돌 문맥 오류 | 0 | 0 |
| Biomes We’ve Gone 관련 파싱 오류 고유 리소스 ID | 1,479 | 0 |
| `/recipe give @s adorn:copper_nugget` | 레시피 1개 해금 | 레시피 ID를 찾지 못함 |

두 엔진 상태 원장은 압축 전에 바이트 단위로 일치했다. 충돌 측정은 빈 이웃과 기본 충돌 문맥으로 제한했다. [공통 엔진 원장 TSV.xz](engine-states.tsv.xz) · [게임 로그 발췌](VISUAL_EVIDENCE.txt)

## 1,503개 경로의 실제 변경

H6~H7에서 기록한 최상위 경로 감소 1,503개를 7.6.1의 `adorn_integration_biomeswevegone/` 아래에서 다시 찾았다. 모델 651개, 블록 상태 426개, 아이템 정의 426개 모두 SHA-256이 7.6.0 원본과 일치했다. 새 JAR의 `pack.mcmeta`는 Fabric의 `all_mods_loaded` 조건에서 `biomeswevegone`이 로드된 경우 이 오버레이를 적용하도록 선언한다. 이번 런타임 실험은 선택 모드가 없는 환경에 한정된다. [원래 증분 연구](../h67/README.md) · [개발자 변경 내역](https://modrinth.com/mod/adorn/version/tyOUUBLZ)

## 인게임 시각 비교

서버가 참나무 의자 상·하단, 참나무 테이블, 붉은 소파 상태를 두 버전에서 읽었다. 동일 카메라의 1,024×684 캡처에서 가구를 포함한 사각형의 93,600픽셀은 모두 동일했다. 전체 화면의 차이 859픽셀은 가구 영역 위쪽에 있었다. 관찰 범위는 이 세 가구의 지정 상태와 고정 카메라다. [7.6.0 화면](baseline.png) · [7.6.1 화면](updated.png)

## 재현

Linux에서 Java 21, curl, 소프트웨어 OpenGL, Xvfb를 준비한다. 분석에는 Pillow가 필요하다. 저장소 루트에서 두 버전의 JAR에 대해 엔진 프로브와 시각 모드를 각각 실행한다. 기존 디스플레이를 사용할 때는 `--display`를 지정한다.

```sh
python scripts/migration/replay_adorn_runtime.py engine \
  --jar '/path/to/Adorn-7.6.0+1.21.11-fabric.jar' \
  --cache /tmp/mcfr-adorn-cache --work /tmp/mcfr-adorn

python scripts/migration/replay_adorn_runtime.py visual \
  --jar '/path/to/Adorn-7.6.0+1.21.11-fabric.jar' \
  --cache /tmp/mcfr-adorn-cache --work /tmp/mcfr-adorn --world /path/to/creative-world
```

명령어가 허용된 로컬 월드에서 아래 배치를 두 버전에 동일하게 실행한다. 완료 후 HUD를 숨기고 1,024×684 창의 프레임을 각각 작업 폴더의 `baseline.png`, `updated.png`에 저장한다.

```text
/gamemode spectator
/tp @s 0.5 120.75 214.5 0 24
/time set noon
/weather clear
/fill -7 119 212 7 124 224 minecraft:air
/fill -8 118 210 8 118 226 minecraft:smooth_stone
/fill -8 119 224 8 125 224 minecraft:white_concrete
/setblock -2 119 219 adorn:oak_chair[facing=north,half=lower]
/setblock -2 120 219 adorn:oak_chair[facing=north,half=upper]
/setblock 0 119 219 adorn:oak_table
/setblock 2 119 219 adorn:red_sofa[facing=north]
/execute if block -2 119 219 adorn:oak_chair[facing=north,half=lower] run say ADORN_CHAIR_LOWER
/execute if block -2 120 219 adorn:oak_chair[facing=north,half=upper] run say ADORN_CHAIR_UPPER
/execute if block 0 119 219 adorn:oak_table run say ADORN_TABLE
/execute if block 2 119 219 adorn:red_sofa[facing=north] run say ADORN_SOFA
/recipe give @s adorn:copper_nugget
```

```sh
python scripts/migration/audit_adorn_runtime.py \
  '/path/to/Adorn-7.6.0+1.21.11-fabric.jar' \
  '/path/to/Adorn-7.6.1+1.21.11-fabric.jar' /tmp/mcfr-adorn
```

[BWG를 설치한 후속 재현](../adorn_bwg/README.md)에서 오버레이 블록 등록과 아스펜 가구 배치를 검증했다.
