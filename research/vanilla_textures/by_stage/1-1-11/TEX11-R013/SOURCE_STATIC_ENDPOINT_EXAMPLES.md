# TEX11-R013 — 정적 상태 끝점 예시 (애니메이션 프레임 아님)

아래는 제공된 Java 1.21.11 원본 `blockstates/*.json`에서 선택된 **전·후 두 상태**이다. 각 항목은 연속적인 시간축이나 부드러운 애니메이션의 중간 프레임을 말하지 않는다.

## 1. door / oak

- 시작 상태: `facing=east,half=lower,hinge=left,open=false`
- 끝 상태: `facing=east,half=lower,hinge=left,open=true`
- 시작 모델 + 고정 회전: `oak_door_bottom_left|0|0|0|false`
- 끝 모델 + 고정 회전: `oak_door_bottom_left_open|0|90|0|false`

## 2. door / oak

- 시작 상태: `facing=east,half=lower,hinge=right,open=false`
- 끝 상태: `facing=east,half=lower,hinge=right,open=true`
- 시작 모델 + 고정 회전: `oak_door_bottom_right|0|0|0|false`
- 끝 모델 + 고정 회전: `oak_door_bottom_right_open|0|270|0|false`

## 3. trapdoor / spruce

- 시작 상태: `facing=north,half=top,open=false`
- 끝 상태: `facing=north,half=top,open=true`
- 시작 모델 + 고정 회전: `spruce_trapdoor_top|0|0|0|false`
- 끝 모델 + 고정 회전: `spruce_trapdoor_open|180|180|0|false`

## 4. shelf / oak

- 시작 상태: `facing=north,powered=false,side_chain=left`
- 끝 상태: `facing=north,powered=true,side_chain=left`
- 시작 모델 + 고정 회전: `oak_shelf|0|0|0|false+oak_shelf_unpowered|0|0|0|false`
- 끝 모델 + 고정 회전: `oak_shelf|0|0|0|false+oak_shelf_left|0|0|0|false`

**표현 규칙:** `모델이름|x도|y도|z도|uvlock여부`. `+`는 여러 블록 모델의 multipart 조합이다.

## 해석 규칙
- 문에서 `open`에 따른 `y` 변경은 원본의 정적 상태 회전이지 실제 게임의 easing duration/hinge world pivot이 아니다.
- 다락문은 closed 수평 요소 bounds에서 opened 수직 요소 bounds로 바뀐다. 회전값 `x=180`을 갖는 orientable top 모델도 원본 정적 x회전 값이다.
- 선반의 `powered` 및 `side_chain`은 본체에 추가되는 한 장의 전면 UV overlay의 종류를 선택한다. 멀티파트 모델의 정적 변환이며 자동 키프레임 생성 규칙이 아니다.
- 실제 텍스처 시간 프레임/animation metadata가 연구 대상 PNG에는 없다. 이 연구는 작동·보간 엔진을 실행하거나 변형하지 않았다.
