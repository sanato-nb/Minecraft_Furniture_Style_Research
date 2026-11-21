# INT-4 — Handcrafted S37/S38 침대 발·머리 구조의 원본 Git ↔ 배포 JAR ↔ 실제 F2

## 원본 연구 출처

기존 INT-4 비의자 대표 사례 15개 가운데 S37/S38은 Minecraft 1.21.1 Handcrafted의 `handcrafted:oak_fancy_bed` 모델이다. 역사 출처는 `research/furniture_mods/phase_1-5/B/APPLICATIONS.csv`와 원본 소스 체크포인트 `INT4_NONCHAIR_15_CASES_AUDIT_RESULT.json`이다.

| 사례 | 블록상태 | 선택 모델 및 직접 상속 기하 | 원본 요소·면 |
|---|---|---|---:|
| S37 | `color=white;facing=north;occupied=false;part=foot;shape=single` | `oak_fancy_bed_single_white_foot` → `fancy_bed/bed_single` | **12요소·72면** |
| S38 | `color=white;facing=north;occupied=false;part=head;shape=single` | `oak_fancy_bed_single_white_head` → `fancy_bed/cushion` | **1요소·6면** |

역사 모델 `bed_single`은 한 블록 경계 밖인 z=-16까지 뻗어 있어, 소스 형상과 실제 두 블록 침대의 설치·연결을 혼동하면 안 된다.

## 독립 원본 대조와 실행 검증

1. 고정 Git 원본 `terrarium-earth/Handcrafted@8d21d1665916850c3fa3bdaf1370c50ec2ca7035`의 실제 JSON을 다시 연다. B 원장 Git blob SHA-1을 재계산한다.
2. 배포 Handcrafted Fabric `1.21.1-4.0.3` 실제 JAR의 SHA-1 `a9579fecd7ed429c282be21d5c921d220197acc6`을 확인한다. 연구 원본과 **파일 본문·JSON 동등성을 구별**해 기록한다.
3. S37/S38 각각의 블록상태 선택자가 실제 배포 JAR에도 있는지, 선택 모델·회전·uvlock·weight 및 자식/부모 모델이 일치하는지 검증한다. 다른 경우 실게임 테스트를 실패 처리하며 허위 동등성을 주장하지 않는다.
4. 기존 공식 Mojang 서버로 *새 임시 평지 월드*를 생성하고, 실제 Fabric 1.21.1 클라이언트에서 발/머리 부분을 **32블록 떨어진 별도 위치에 /setblock**한다. 게임 서버의 두 상태 유지가 확인되어야 F2를 촬영한다.
5. 실제 F2 2장 PNG SHA, 화면 내 전경 존재, 임시 접촉시트를 확인한다. 하늘만 촬영되면 같은 상태를 제한적으로 다시 시도하며, 실패를 은폐하지 않는다.
6. 실제 게임 F2와 로그는 **기한부 GitHub Actions 아티팩트**로만 보존하며, 원본 Git ZIP/JAR·사용자 월드·기존 31,242개 연구 원본 및 main은 변경하지 않는다.

## 미검증 경계

두 블록의 부품을 각각 강제로 배치한 결과는 **자연스럽게 침대 아이템을 설치하여 머리/발이 연결되는 기능**의 검증이 아니다. 완성형 침대 화면, 실제 수면/상호작용, 물리, 텍스처 GPU bake의 면별 UV·색 일치, 가구 부품 역할의 의미와 AI 학습·재배포 권리는 별도 INT-4/INT-5/INT-6 검증 항목이다.

- 현재 공식 단계: INT-4 진행 중.
- INT-5의 45개 개별 역할 후보 의미 승인: 0 유지.
- INT-6 AI용 출처·권리 승인: 0 유지.
- Draft PR, main 병합 금지.

실제 CI 결과가 확인된 뒤 본 보고서에 실행 ID·실측 SHA·실패 예외를 추가한다.

## 실게임 첫 CI 결과 및 **시각 가시성 오류 발견**

[첫 원본 게임 CI #44927754676](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44927754676)에서는 고정 Git 원본/Handcrafted 4.0.3 JAR 선택 모델 및 서버 블록상태 S37/S38 각각 **2/2 일치**, F2 PNG 파일 각각 **2/2 실제 생성**까지 검사했다. 그러나 [첫 아티팩트 14715774857](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44927754676/artifacts/14715774857)의 2장과 접촉시트를 **실제 이미지로 열어 확인**한 결과, 양쪽 모두 **침대가 보이지 않고 하늘·초록 지형만 있었다**.

당시 자동 CI에서 초록 지형을 가구 전경으로 오인한 `specimen_color_pixels` 검사 오류가 있었다. 따라서 **첫 성공 CI는 가구의 실제 가시성을 증명하지 못하고**, 모델/상태 검증과 F2 파일 생성까지만 유효하다. 이 결과를 시각적으로 승인하거나 INT-5 부품 의미 승인으로 승격하지 않는다.

- 첫 시도 F2 PNG: S37 SHA-256 `e050d55010c1d4a002d7e5e4a3b509ce036f8ba9cb646a5c22114e2aa0ad9454`, S38 `17acceab6df2502c49b0a721c83f1898f28e31089948a267b76eb8fc91bd4304`.
- 실제 두 이미지의 가구색 전경 프록시: **0 / 0** (하늘과 잔디 제외).
- 후속 수정: 하늘·잔디색을 제외한 침대 전용 화면 프록시, 촬영 전 청크 로딩 시간 증가, 가짜 하늘/잔디 이미지 회귀 테스트 추가.
- 원본 모델이 실제 안 보인다는 최종 결론은 아직 아니다. 카메라·청크·GUI 촬영 문제 또는 침대의 별도 부품 렌더 특성을 분리해서 조사한다.

**재검증 성공이 확인되기 전 시각적 F2 승인 0/2 유지.**

### 재검증에서 추가로 발견된 CI 환경 오류

강화된 하늘/잔디 배제 검사 추가 후 [CI #44928221190](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44928221190)를 실행했다. 회귀테스트·고정 원본·공식 서버 새 월드 생성은 성공했으나, **실제 Minecraft 클라이언트 GUI가 카메라 텔레포트 명령을 수신하지 않아** 첫 실행과 단독 재실행 모두 텔레포트 대기 시간 초과로 끝났다. 따라서 **새 F2 사진은 0장**, 원본 모델이 렌더되지 않는다는 결론 역시 도출하지 않는다.

실제 클라이언트 합류 완료/GUI 명령 수신 가능성을 분리 검증하도록 대기 및 실패 당시 X11 화면 진단 PNG 보존을 추가했다. 이후 실행에서도 침대가 실제로 보이지 않으면 시각적 실패를 그대로 남기고 가짜 성공 판정을 하지 않는다.

## 실제 동일 카메라 Air 대조 F2 최종 성공 (2026-11-22)

[실제 Minecraft 1.21.1 검증 #44929863978](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44929863978)에서 모델이 있는 F2 2장과, **같은 카메라·동일 월드에서 해당 블록을 서버 명령으로 제거한 후 촬영한 Air 대조 F2 2장**, 총 **4개 원본 F2**를 재검증했다. 먼저 S37/S38 원본 블록상태 2/2를 서버에서 확인했고, 제거한 위치 역시 `minecraft:air` 2/2를 서버에서 확인했다. 원본 Git 모델 및 부모 리소스의 SHA와 실제 배포 Handcrafted 4.0.3 JAR 모델·선택 상태의 **본문·JSON 값이 각 사례 모두 일치**했다.

| 실제 연구 사례 | 요소·면(원본) | F2 화면 직접 관찰 | 같은 카메라 Air 대조와 다른 픽셀 |
|---|---:|---|---:|
| **S37 (발 / foot)** | 12요소·72면 | 목재 프레임, 연한 무늬 침구가 나타나는 침대형 전체 구조 | **7,830** |
| **S38 (머리 / head)** | 1요소·6면 | 평평한 바닥 위 작고 연한 반투명/쿠션형 부분 | **465** |

ROI x=[350,675), y=[275,620)에서 대응하는 F2 두 장의 RGB 채널 중 최대 변화가 **24 이상**인 픽셀만 센 것이다. 하늘·잔디·석재 바닥의 색상만으로 승격하는 기존 오탐을 막기 위한 *가시성 대조 검사*이며, 7,830/465 자체가 부품의 실제 역할이나 GPU 텍스처 UV 매핑을 증명하는 것은 아니다.

- 실제 원본 침대 S37 F2 SHA-256: `bf8936e0ca41bca85cf123f5bd85c3e2390793c59f9e3ac07f0f682e7f552fe3`.
- 실제 원본 침대 S38 F2 SHA-256: `92c1271ab5b2cff6ba71f77517272582d188af81424c5161fe1d4a8608733b61`.
- S37/S38 Air 대조 F2 SHA-256: `559bd5bc8161f5cb3a82a207971bc999f8bd4f1d7c2490d12ea207370288d301`.
- 접촉시트 SHA-256: `6a364158e1b21039528f987ba18ceaa0108ca5feddb63fc49334ce08fe75f10c`.
- 원본 구조·사진·검증 범위가 연결된 [Git 고정 체크포인트](INT4_HANDCRAFTED_BED_F2_SOURCE_RESULT.json).
- 만료되는 [실제 F2 및 로그 아티팩트](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44929863978/artifacts/14717317186) ZIP SHA-256 `e02c603e85ef55da8a140cb1abc362faff363a8c20937f9a34775b8ccf69f9ce`.
- 첫 하늘/잔디 **가짜 F2 시각 성공 판정**, GUI 입력 미수신 두 차례, 후속 픽셀 프록시의 **석재 바닥 오탐 가능성**을 전부 삭제하지 않고 기록한다.

**판정:** Handcrafted `part=foot`/ `part=head` 원본 상태가 실제 게임 서버에서 유지되고, 각 단독 F2에 대응하는 *실제 화면 차이*가 나타나는 것까지 확인했다. 자연스러운 2블록 침대 설치, 인접 블록 갱신, 잠자기 기능·의미·재질/스타일·면별 UV·AI 학습/재배포 권리는 **미검증·미승인**. 이 구분은 다음 INT-4 및 INT-5에서 유지한다.

비의자 대표 15개 사례 중 실제 F2 상태를 새로 확보한 것은 기존 Macaw 주방 3 + 테이블·책장 4 + 이번 침대 2 = **9/15(60%)**. 이는 *대표 표본 F2 획득률*이지 **INT-4 전체 단계 완료율이 아니다**.
