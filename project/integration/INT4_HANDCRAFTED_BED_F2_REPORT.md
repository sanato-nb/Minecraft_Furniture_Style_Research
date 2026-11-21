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
