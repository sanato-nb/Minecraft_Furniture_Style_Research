# H7 후속 · Biomes We’ve Gone 설치 상태에서 Adorn 오버레이 재현

Minecraft Java 1.21.11, Fabric Loader 0.19.3, Fabric API 0.141.6에서 Adorn 7.6.0과 7.6.1을 BWG 4.4.2와 함께 실행했다. 추가 JAR 5개에는 TerraBlender 21.11.0.0 베타가 포함된다. [Adorn 입력 핀](../h67/ADORN_PINS.json) · [BWG 및 의존성 입력 핀](MOD_PINS.json)

| 런타임 측정 | BWG 미설치 | BWG 설치 |
|---|---:|---:|
| Adorn 블록 ID | 679 | 1,105 |
| Adorn 블록 상태 | 41,211 | 70,931 |
| 충돌 상자 | 175,032 | 312,924 |
| BWG 호환 블록 ID | 0 | 426 |
| BWG 호환 블록 상태 | 0 | 29,720 |

BWG를 설치한 두 Adorn 버전의 엔진 원장은 바이트 단위로 일치했다. 7.6.1 오버레이의 블록 상태 JSON 426개가 런타임에서 등록된 BWG 호환 ID 426개와 정확히 대응했다. BWG 전용 행을 제외한 원장은 [기존 미설치 실험](../adorn_runtime/README.md)과 바이트 단위로 일치했다. 충돌 상자는 빈 이웃과 기본 충돌 문맥에서 측정했다. [계수와 해시](RESULT.json) · [공통 엔진 원장](engine-states.tsv.xz)

Adorn 7.6.1로 복사한 로컬 월드에서 왼쪽부터 참나무 테이블, 아스펜 테이블, 아스펜 의자를 캡처했다. 서버가 의자 상·하단과 두 테이블의 블록 상태를 확인했다. 아스펜 의자 레시피는 게임 명령으로 해금했다. 시각 확인은 캡처 속 가구에 한정되며 레시피 검증 범위는 해금까지다. [인게임 캡처](aspen-furniture.png) · [명령과 로그](VISUAL_EVIDENCE.txt)

## 재현

Linux에서 Java 21, curl, 소프트웨어 OpenGL, Xvfb 및 Python Pillow를 준비한다. 두 Adorn JAR와 [추가 모드 핀](MOD_PINS.json)에 명시된 JAR를 받는다. 추가 JAR 5개를 `/tmp/mcfr-bwg-mods`에 두고, Adorn JAR를 `/tmp/mcfr-adorn-jars`에 둔다. 엔진 재생기는 추가 모드의 크기와 SHA-256을 확인한 뒤 임시 실행 폴더에 복사한다.

```sh
for version in 7.6.0 7.6.1; do
  python scripts/migration/replay_adorn_runtime.py engine \
    --jar "/tmp/mcfr-adorn-jars/Adorn-${version}+1.21.11-fabric.jar" \
    --bwg-dir /tmp/mcfr-bwg-mods --cache /tmp/mcfr-adorn-cache --work /tmp/mcfr-adorn-bwg
done

python scripts/migration/replay_adorn_runtime.py visual \
  --jar '/tmp/mcfr-adorn-jars/Adorn-7.6.1+1.21.11-fabric.jar' \
  --bwg-dir /tmp/mcfr-bwg-mods --cache /tmp/mcfr-adorn-cache --work /tmp/mcfr-adorn-bwg \
  --world /path/to/creative-world --display :99
```

시각 모드에는 명령을 실행할 수 있는 로컬 월드와 캡처 가능한 디스플레이를 지정한다. 아래 명령과 [배치·검증 명령](VISUAL_EVIDENCE.txt)을 순서대로 실행한다. F1로 HUD를 숨긴 뒤 1,024×684 창을 `/tmp/mcfr-adorn-bwg/updated.png`에 캡처한다.

```text
/gamemode spectator
/tp @s 0.5 120.75 214.5 0 24
/time set noon
/weather clear
/fill -7 119 212 7 124 224 minecraft:air
/fill -8 118 210 8 118 226 minecraft:smooth_stone
/fill -8 119 224 8 125 224 minecraft:white_concrete
```

```sh
python scripts/migration/audit_adorn_bwg.py \
  '/tmp/mcfr-adorn-jars/Adorn-7.6.1+1.21.11-fabric.jar' /tmp/mcfr-adorn-bwg
```
