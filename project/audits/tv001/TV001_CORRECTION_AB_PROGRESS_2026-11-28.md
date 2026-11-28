# TV-001 결함 보완 A/B 중간 증거 — 2026-11-28

기준: [결함 보완 실행계획](TV001_CORRECTION_PLAN_2026-11-28.md), 기존 v1.1 고정 12개 사례/25개 이미지.

## A. 종료 판정
수정 커밋 `0a7876952c5c8f819ab46c8e217dd47bfead896c`, t8_close.py Git blob `2d4355590ddf8aa2a6ab0fe4cd6d26c6e2271702`. 범위·P06 방향·T4 FAIL·HOLD·T0 완료 여부를 판정에 반영하고 14개 집계 회귀 검사를 추가했다. 실제 파일 재조회 완료.
- [TV-001 회귀 실행 #46117269034](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/46117269034): 조회 시 Blender 설치 단계 진행 중. 회귀 성공 미확정.
- [기존 하네스 검증 #46117269046](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/46117269046): foundation Job 및 H0/H1 검증 단계 success 확인.
A는 코드 반영 완료, TV-001 전체 회귀 결과는 미확정.

## B. UV 기대값 근거 사전 확인
고정 원본 main `176f7f34de2336eb7984c4734e97b6eb156c19f4`의 Git 트리(비절단)와 버전별 매핑을 대조했다.

| 원본 경로 | Git blob SHA | bytes | 확인한 매핑 |
|---|---|---:|---|
| 1.21.11/hqi.class | 5b64584e8cc09a8db90f802e0021bc0533e81ab1 | 7068 | FaceBakery |
| 1.21.11/inm.class | 672b186c8a8457082fec756114b443a48dc151d1 | 2863 | BlockModelRotation |
| 1.21.11/inm$a.class | 9ca92245d30e41cf4dfe239617ebbec94ad19974 | 2111 | BlockModelRotation.WithUvLock |
| 1.21.11/ioc.class | 6063a49dabf4cda7816dc570babd1a1b2e57e6e0 | 561 | ModelState (메서드 서명 참조 타입) |
| 1.21.11/hqc.class | 17d6188210d69bbebb560a043396bb8eeedd6045 | 2369 | BlockElementFace (메서드 서명 참조 타입) |

참고: [FaceBakery 1.21.11](https://mappings.dev/1.21.11/net/minecraft/client/renderer/block/model/FaceBakery.html), [BlockModelRotation 1.21.11](https://mappings.dev/1.21.11/net/minecraft/client/resources/model/BlockModelRotation.html), [WithUvLock 1.21.11](https://mappings.dev/1.21.11/net/minecraft/client/resources/model/BlockModelRotation%24WithUvLock.html). 매핑은 클래스/메서드 이름과 서명 근거일 뿐 구현 결과 증명이 아니다.

실제 JSON도 확인했다. acacia_stairs_inner.json (blob 323018d55565db0f9914d4e28e3adb157f3c1e7d)은 inner_stairs를 상속하며 bottom/side/top에 acacia_planks를 사용한다. inner_stairs.json (blob 364eff63e057a4abbb74d80f7d5297beba61f751)은 3요소, 명시 UV가 있는 면 15개(6+5+4)로 구성된다. R03-inner의 x=180/uvlock=true는 기존 T4 원본 대조 근거와 일치한다.

### 제약과 다음 실행
GitHub 텍스트 커넥터가 .class 바이너리 읽기를 거부해 메서드 본문 및 실제 UV 좌표를 아직 검증하지 못했다. 매핑 이름만으로 보정 각도를 추정하지 않는다. 다음 B 실행은 기존 고정 원본을 체크아웃한 환경에서 javap -p -c -s로 관련 메서드의 변환 흐름을 읽고, 해당 15면의 독립 기대값을 계산하는 방식으로 진행한다. 실제 게임 실행이나 사례 추가는 필요 없다. C 구현은 B 기대값 확인 후 진행한다.
B는 PARTIAL, C/D/E는 미완료. 기존 CLOSED_PARTIAL 판정과 원본은 보존한다.
