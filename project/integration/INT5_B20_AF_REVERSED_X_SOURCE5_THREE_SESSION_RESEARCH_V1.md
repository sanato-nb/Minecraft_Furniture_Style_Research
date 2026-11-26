# INT-5-B20 — Another Furniture 원본 역방향 X 좌표 요소 5 독립 렌더링 연구

기준: [INT-5-B19 Draft PR #131](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/131) HEAD `bfa45e758db7c814cf76d99fd1f6b576f8563dc2`. 직계 후속 브랜치만 생성하고 `main` 및 기존 원본 원장은 수정하지 않는다.

## 1. B19에서 실제 확인한 미해결 사례

| 원본 키 | 출시판 | 원본 from | 원본 to | 소스 face | B19 실제 4방향 제거 실험 |
|---|---|---|---|---:|---|
| `AF121/AF1393/5` | Another Furniture Fabric **4.0.2** | `[13,2,3]` | `[3,4,13]` | 4 | 남·북·동·서 모두 0픽셀 |
| `AF123/AF1394/5` | 동일 출시판 tucked | `[13,2,-6]` | `[3,4,4]` | 4 | 남·북·동·서 모두 0픽셀 |

출처: `project/integration/INT5_B19_FOUR_MODEL_45_ELEMENT_STATUS_V1.csv`, `INT5_B19_FOUR_VIEW_REAL_F2_CAUSAL_AUDIT_FOUR_MODEL_V1.json`; 원본 B19 작업 [Actions #45664823385](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45664823385) 성공.

두 요소 모두 X축 `from.x=13 > to.x=3`이다. **이것이 미검출의 유일 원인인지, 원본 모델 버그인지, 불필요한 부품인지는 검증되지 않았다.** 요소 이름 `LOWER_FRAME`은 기존 B3 원본 텍스처/위치의 역할 가설일 뿐 재질·기능 확정이 아니다.

## 2. B20의 원본·대조·개입 3세션

원본 Minecraft Java **1.21.1 Fabric**, 실제 공식 AF 4.0.2 JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`, B16 AF 기본/ B15 tucked 공식 원본 parent/child Git blob SHA1 검증. 동일 원본 월드를 **매 세션마다 복원**한다.

- **A 원본** — 공식 부모 상속 child 모델, JAR 바이트 불변, 게임 실제 F2 16장
- **B 상속 전개 대조** — 원본 부모 10개 요소·46면을 byte/JSON 의미 동일하게 child의 `elements`에 복사. 부모·텍스처·다른 JAR 리소스 그대로, F2 16장. A와 B의 원본/대조/원본/AIR 각 장면이 픽셀 단위로 동일해야 함
- **C X축 단독 정렬** — B와 다른 부분은 정확 원본 제공자 source index5 `from.x=3,to.x=13`로 바꾼 두 숫자뿐. Z/Y/UV/texture/faces, 나머지 9개 요소, parent·blockstate/모든 비표적 JAR member 동일, F2 16장

대상마다 남·북·동·서 4개 카메라 × 같은 4개 단계. 합계 **2개 대상 × 3클라이언트 × 16장 = 96장 진짜 네이티브 F2 목표**. AF123은 `tucked=true`가 성립하는 윗반블록 지지 상태를 매 캡처에 보존한다. 기존 실제 명령/상태/캡처/게임 로그 확인은 B19에서 검증된 코드를 재사용한다.

인과 해석의 핵심은 **원본 A↔B=0**와 B↔C 변화. 상속 전개만으로 변화가 생기면 C의 차이를 역방향 X 원인이라고 승인하지 않고 조건부 처리한다. B↔C 실제 게임 화면이 바뀌어도 `X 좌표를 교정한 시험용 모델에서 바운드된 시각 변화가 관찰되었다`까지가 허용되는 판정이다. 화면의 새 픽셀이 원래 의자 외곽에 생길 수 있으므로, 원본 외곽만이 아니라 **원본과 C의 의자 실루엣 합집합**에서 벗어난 변화를 검사한다.

실험기: `src/mcfr/int5_b20_af_reversed_x_three_session_f2.py`. 테스트: `tests/knowledge/test_int5_b20_af_reversed_x_three_session_f2.py`. CI: `.github/workflows/integration-int5-b20-af-reversed-x-three-session-f2.yml`.

## 3. 독립 검증 및 종료 경계

- 실제 **3게임 로그 SHA**, 원본 server blockstate 표지, F2 PNG 1024×684와 개별 SHA, 음성대조·시간 안정성·월드복원·한 리소스 수정 여부를 감사
- CI 성공은 연구 PASS가 아님: 세 조건 `PASS_BOUNDED...`, `NO_VISIBLE...`, `CONDITIONAL...` 중 근거에 따라 기록
- 제3자 공식 JAR/원본 PNG/임시 수정 JAR은 Git에도 Actions 결과 아티팩트에도 넣지 않음
- 기존 B19의 43/45 한정 렌더링 인과와 두 미검출 관찰은 **사후적으로 변경하지 않음**
- 부품 기능·재질·스타일 실제 의미 0/45, face/UV의 배타적 GPU 픽셀 소유권 승인 0, 제3자 AI 학습·재배포 승인 0
- 엄격 `H03 HOLD`, `H05 CONDITIONAL`, F70 무조건 승인 `0/70`; 후속 PR Draft 유지 및 `main` 미병합

## 4. 결과 기록

실게임 CI 실행과 산출 ZIP 독립 재검증 이전에는 **B20 결과 미확정**이며 원본 모델 좌표만 근거로 PASS를 허위 선언하지 않는다.

## 5. 실제 GitHub Actions 실행 이력 (중간 체크포인트)

- 최초 [#45737193963](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45737193963): 원본 코드 검사 통과 후 신규 `argparse.add_parser`에 잘못 추가한 위치인자 때문에 **게임 시작 전 CLI 오류**, 연구 증거로 계상하지 않음.
- 후속 [#45737409387](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45737409387): 11개 B20 원본/반증 단위시험 통과 후 `--version/--work/--world/--output` 신규 하위 명령의 공통 등록 누락으로 게임 시작 전 중단. 이 또한 원본 렌더링 인과 실패가 아님.
- 각각 한국어 커밋으로 인자 오류를 고치고, `runtime --help`에 각 필수 옵션이 실제로 표시되는지 검증하는 스모크 단계도 CI에 추가.
- 현재 재검증 대상 [#45737601134](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45737601134), 코드 HEAD `443217ae6b7f05927a236aff408cb299fb4fbef8`. **중간 조회 시 두 AF 대상 모두 실제 Fabric 3세션 촬영 단계 진행 중**. 독립 F2 SHA 검증·원본 vs 상속전개 vs 교정 결과를 확인하기 전에는 B20 실험 완료나 새로운 원인 입증으로 표기하지 않는다.

## 6. AF121/AF1393/5 실제 3세션 결과 — 독립 ZIP 재검증

[GitHub Actions #45737585060](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45737585060) 중 **AF121_5 job 성공**. 해당 실험 실행 커밋 `4677698532936955655837204f89ade000399dfd`. 증거 artifact ID `15080486304` (원본 ZIP SHA-256 `41b6e8da5c97f2aff8a7659c580cf9c0dd4dd9b5098916358166408535f529b3`).

원본 `B19 AF121_5` 32 F2는 독립 재검증에서 ZIP CRC·32개 PNG SHA·원본/수정 각 16 이미지 및 4카메라 전부 0픽셀 확인. B20 3세션 ZIP 재다운로드 후 Python/Pillow/NumPy로 **48개 PNG SHA256, 세 로그 SHA256, 개별 서버 블록상태 marker 48개, ZIP CRC** 재확인.

| 비교 | south | north | east | west |
|---|---:|---:|---:|---:|
| 원본 inherited ↔ flatten 동일 요소·UV parent | 0 | 0 | 0 | 0 |
| flatten ↔ element5 X만 `from:3,to:13` 정렬 | 0 | 0 | 0 | 0 |

모든 A/A 시차·variant3 음성 대조·AIR 차이 0. 실제 감사 판정 **`NO_VISIBLE_RESPONSE_AFTER_ORIGINAL_X_ENDPOINT_NORMALIZATION`**. 실게임 F2에서 원본 X 정렬이 관찰 가능 모델 차이를 만든다는 근거는 얻지 못함. **역방향 좌표의 배타적 원인·원본 요소 사용 여부·원본 엔진 버그·모델 요소 의미/권리 및 부품 픽셀 귀속을 승인하지 않음**.

AF123의 별도 실험 완료/독립 ZIP 감사 전에는 B20 전체 완료를 선언하지 않으며, B19 누적 **43/45** 렌더 가시성 검증 및 2개 미검출 기록을 변경하지 않는다.
