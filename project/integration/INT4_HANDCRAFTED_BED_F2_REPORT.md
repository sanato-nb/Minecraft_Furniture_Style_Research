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
