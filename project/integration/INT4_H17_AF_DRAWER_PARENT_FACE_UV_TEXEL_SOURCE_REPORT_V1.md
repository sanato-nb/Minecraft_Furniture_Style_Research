# INT-4-H17 — Another Furniture 서랍 S20/S21 부모 모델·면 UV·실제 변경 텍셀 원본 감사

## 1. 직계 출처 / 작업 목적
- 부모 연구: [Draft PR #97](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/97) head `cd6ef6fe2d5ffe66517685c75cf88fa3e4e14c2f`. 후속 [Draft PR #98](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/98)는 #97 브랜치를 base로 한다. `main` 미병합.
- 기존 실게임: [F2 성공 Actions #45251124211](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45251124211). 같은 좌표·북쪽 카메라의 **S20 closed / S21 open** 원본 2장과 서버 정확 상태 2/2, 화면 차이 **1,208픽셀(RGB 채널차 24 이상)** 확인.
- 이번 추가 조사: 게임을 다시 띄우지 않고 해당 공식 릴리스 원본 JSON의 blockstate→leaf→parent→elements/faces/UV→실제 16×16 PNG RGBA 차이의 **근거 연결**을 직접 감사.

## 2. 새 GitHub Actions에서 직접 검사한 것
- [H17 성공 Actions #45320157848](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45320157848) · 관련 검사 SHA `3220ca220407d8754abd9e67a60fff3fb857b405` · **9/9 회귀시험 성공**, 공식 JAR SHA1/ZIP CRC 및 출처 분석 통과.
- 공식 **Another Furniture Fabric 4.0.2** JAR SHA1: `c2f992081bdc4795ed6d87771a3b5f7c71103785`.
- 실제 원본에서 생성한 **파생 분석 JSON만** [아티팩트 #14886494724](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45320157848/artifacts/14886494724)에 저장. 다시 내려받아 ZIP CRC 통과, ZIP SHA256 `6818e95873b621445410356fd1dc981ed34881fad1cb6cc838bff9cdc9084c84` 직접 확인. 모드 JAR/PNG 원본 바이트는 업로드하지 않음.
- Git에 남기는 요약 수치·정확 경로·원본 해시: `project/integration/INT4_H17_AF_DRAWER_ORIGINAL_PARENT_FACE_UV_TEXEL_RESEARCH_V1.json`. 원본 분석을 재실행하는 프로그램: `src/mcfr/int4_h17_af_drawer_parent_face_uv.py`.

## 3. S20/S21 원본 모델 상속과 면 구조

| 항목 | 닫힘 S20 | 열림 S21 |
|---|---|---|
| 서버 state | `facing=north,open=false` | `facing=north,open=true` |
| 선택된 leaf | `block/drawer/oak` | `block/drawer/oak_open` |
| 실제 AF 모델 부모 체인 | `template/drawer → oak` | `template/drawer → oak → oak_open` |
| 기하가 정의된 모델 | `template/drawer.json` | 동일 |
| 기하 요소 개수 | **1** | **1** |
| 원본 면 개수 | **6** | **6** |
| `elements` 및 각 면 UV | 서로 **동일** | 서로 **동일** |

- 기하 제공 모델 `assets/another_furniture/models/block/template/drawer.json` SHA256 `0f8b70cff1f722d34e0fbeacd6c107428f9fb30911c5b31e285e6f0fc202506f`.
- S20 leaf `oak.json` SHA256 `52629e833f8c9a66d0c7c5453b548f9fb611d360364ea3ab0300ba108b1c4c67`, S21 leaf `oak_open.json` SHA256 `a70086f68568519f457b27e3ffe9aac2596378b19ddb872e7cdda888a12bfd76`.
- 계보 상단의 바닐라 `minecraft:block/block`은 **외부 부모로 기록하되 이번 AF JAR만으로 그 내용까지 확인했다고 처리하지 않음**. AF 모델에서 실제 elements가 정의된 사실과 별도로 보존한다.

## 4. 서로 달라지는 정확한 소스 면과 원본 텍셀

| 직접 측정 | 결과 |
|---|---|
| 바뀌는 모델 텍스처 변수 | `front`만 |
| 해당 변수에 실제 연결된 변경 면 | **1면** |
| 면 인덱스 / 방향 | **element 0 / north** |
| 해당 면의 명시 UV | **[0, 0, 16, 16]** (회전 0°) |
| 두 원본 앞면 PNG 크기 | 16×16 |
| 바뀐 RGBA 텍셀 | **60개** |
| 알파 채널까지 바뀐 텍셀 | **0개** |
| RGB만 바뀐 텍셀 | **60개** |
| 명시 UV 사각형 안에 포함된 변경 텍셀 | **60/60개** |
| 이번 새 실제 Minecraft 실행/캡처 | **0회 / 0장** |

- S20 앞면: `assets/another_furniture/textures/block/drawer/oak_front.png` SHA256 `d35ccb907f9bdc8167a5cd662e14ebe8dc761c7ab95148a77914ecd5a6eec391`.
- S21 앞면: `assets/another_furniture/textures/block/drawer/oak_front_open.png` SHA256 `8421fd0bd80d188b2f368ff04850c80582a079381df6e4bb5d50ff511f9b899b`.

**범위가 좁혀진 설명:** 동일 형상의 같은 북쪽 면이 blockstate에 따라 서로 다른 16×16 텍스처를 사용한다. 기존 #97에서 보았던 북쪽 카메라 **1,208화면 픽셀 변화**와 원본 선택·UV·텍셀 변경 방향이 일관된다. 반면 **RGB 60텍셀 각각이 F2 화면의 정확히 어느 픽셀에 영향을 주었는지는 GPU 샘플러/프레임 경로로 직접 추적하지 않았고, 60=1,208로 동일한 단위의 수치처럼 환산하지 않는다.**

## 5. 테스트·제약 및 후속
- 회귀시험 9개: 원본 모델 상속과 `#` 텍스처 별칭, 암묵 UV 미확정 보존, 비전면 변경/기하 불일치 거부, 잘못된 JAR SHA 거부, 과거 게임 출처 드리프트 거부, 부모·별칭 순환 탐지, UV 역순/경계 검사, 경로 이탈 거부.
- 초기 CI에서 외부 `minecraft:` 부모를 같은 모드 JAR에 있는 것으로 간주한 문제가 드러나 **미열람 부모와 실제 모드 내부 기하를 분리**했고, 실게임 원장 필드명 `github_actions_run` 정합 후 재검증에 성공. 실패 기록은 기존 Actions에 남김.
- 후속 모델링 연구는 실제 GPU의 개별 면·UV 픽셀 인과가 **필요한 구체 사례에서만** 제한 실험. 같은 70사례 F2 반복 촬영, 서랍 사용자 클릭, 수면/파괴 등 광범위한 게임플레이 검증을 H17 필수조건으로 추가하지 않음.
- **종료 기준 유지:** H03 **HOLD**, H05 **CONDITIONAL**, F70 **70/70 조건부·0/70 무조건**, H 8게이트 **6 범위 통과·1 조건부·1 HOLD**, INT5 의미 승인 **0**, INT6 AI 학습·재배포 권한 승인 **0**. 새 모델 구조 실측은 자동으로 최종 승인이나 사용권 승인이 되지 않음.
