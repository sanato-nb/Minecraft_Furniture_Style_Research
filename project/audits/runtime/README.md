# 고정 Mods 런타임 재실행과 인게임 캡처

2026-11-19 KST. 하네스의 Mods 런타임 진입점을 기존 1-3-D 엔진 검사에 연결했다. Minecraft 클라이언트와 모드 JAR은 기존 스크립트가 지정한 SHA-1로 재검사했다.

| Minecraft · Fabric Loader | 모드 | 블록 유형 | 등록 상태 | 충돌 상자 | 충돌 계산 오류 |
|---|---|---:|---:|---:|---:|
| 1.21.1 · 0.18.4 | Another Furniture 4.0.2, Handcrafted 4.0.3 | 441 | 107,424 | 244,266 | 0 |
| 1.21.11 · 0.18.4 | Macaw’s Furniture 3.4.2 | 714 | 8,562 | 19,620 | 0 |
| 합계 | 3개 모드 | 1,155 | 115,986 | 263,886 | 0 |

공기·돌 대조군은 각 버전의 엔진 검사에서 통과했다. 원장 조건을 등록 상태에 대입한 결과 variant 불일치와 매칭 규칙이 없는 multipart 상태는 두 버전 모두 0건이었다. Another Furniture의 원장 리소스 3개는 게임 레지스트리에 등록되지 않았다. 해당 ID는 [1.21.1 결과](engine-1.21.1.json)에 기록했다. [1.21.11 결과](engine-1.21.11.json)도 별도로 보관한다. 충돌 상자 수는 빈 이웃·기본 충돌 문맥에 한정한다.

## 재현

Linux에서 Java 21, curl, 소프트웨어 OpenGL과 Xvfb를 준비하고 저장소 루트에서 실행한다. 이미 실행 중인 X11 디스플레이를 사용하려면 `--display :99`를 추가한다.

```sh
PYTHONPATH=src python -m mcfr.runtime engine --version 1.21.1 \
  --work /tmp/mcfr-engine-cache --output /tmp/mcfr-engine-1.21.1
PYTHONPATH=src python -m mcfr.runtime engine --version 1.21.11 \
  --work /tmp/mcfr-engine-cache --output /tmp/mcfr-engine-1.21.11
```

시각 검증에는 각 버전에서 저장한 창작 모드 평지 월드가 필요하다. 게임의 명령어 사용을 허용한다. 하네스는 해당 월드를 별도 작업 폴더에 복사해 기존 1-3-C/D 데이터팩을 설치하고 연다.

```sh
PYTHONPATH=src python -m mcfr.runtime visual-client --version 1.21.1 \
  --work /tmp/mcfr-visual-1211 --world /path/to/local-creative-world
```

월드에 들어간 뒤 `/reload`, `/gamemode spectator`를 실행한다. 1.21.1은 `/tp @s 0 122 48`, 1.21.11은 `/tp @s 0 122 215`로 이동하여 청크가 열린 뒤 `/function cd_audit:place`와 `/function cd_audit:verify`를 실행한다. 아래 카메라 좌표로 이동한 뒤 F1로 HUD를 숨기고 F2로 저장한다. 로그에서 CD_PLACED, CD_STATES_READ 및 CD_STATE 관찰을 확인한다.

## 실제 촬영 결과

| 인게임 원본 PNG | 카메라 명령 | 관찰 |
|---|---|---|
| [Another Furniture](another-furniture.png) | `/tp @s 4.5 120 37.2 0 20` | 자작나무 의자 변형 1의 좌판과 등받이 |
| [Handcrafted](handcrafted.png) | `/tp @s -6.8 120 52.8 0 18` | 참나무 소파 두 블록의 연결. 서버가 `right`, `left`를 읽음 |
| [Macaw’s Furniture](macaws-furniture.png) | `/tp @s 1.9 120 214.1 0 13` | 참나무 의자·옷장·책상 배치. 서버가 옷장의 `bottom,left`, `top,left`를 읽음 |

촬영에는 기존 실험용 평지 월드의 복사본을 사용했다. 같은 실행에서 데이터팩을 다시 배치하고 서버가 읽은 [1.21.1 상태](visual-1.21.1.log)와 [1.21.11 상태](visual-1.21.11.log)를 확인했다. PNG 세 장은 1024×684로 저장했고, 대표 배치에 대한 화면 확인 범위는 표에 명시한 상태까지다.

[1.21.1 상태 원장](engine-1.21.1.tsv.xz) · [1.21.11 상태 원장](engine-1.21.11.tsv.xz) · [재실행 대조 및 SHA-256](REPLAY_AUDIT.json)

기존 진입점과 새 하네스 진입점으로 각각 실행했다. 버전별 SUMMARY와 압축 해제한 상태 TSV가 두 실행에서 일치했다. TSV를 다시 집계해 상태 중복 0건, 충돌 상자 수, 빈 충돌 형상 수 및 대조군을 확인했다.
