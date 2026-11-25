# INT-5-B7 — AF121 기본 의자 4번 소스 요소의 격리 제거·실게임 F2 인과 검증

작성 기준: **2026-11-25 KST**. 직계 [INT-5-B6 Draft PR #118](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/118) head `83d48db20b5da3626944adabcd77d62aa912b403`에서 새로운 누적 브랜치를 분기했다. `main`과 B1~B6 원본/기존 감사 원장은 수정하지 않는다.

## 검증 목표

B6 45개 원본 요소 중 첫 후속 후보 **AF121 기본 의자·연구 제공자 AF1393·element 4·6면·`SEAT_LAYER` 역할 가설**에 대해, Minecraft에서 **정확히 해당 요소를 제거했을 때** 원본 모델의 화면이 달라지는지 반증 가능한 실제 F2 시험을 수행한다. 기존 B5 **AF123 tucked 의자 요소 4**의 관찰을 AF121에 자동 전파하지 않는다.

**특히 공통 부모 템플릿을 제거하면 여러 의자 변형이 함께 수정되는 설계 결함**을 회피한다. 공식 Another Furniture Fabric **4.0.2** 원본 JAR의 `acacia_1.json`이 공유 `template/chair.json`의 10요소·46면을 상속함을 확인한 후, 임시 JAR의 **acacia_1 자식 JSON 한 개에만** 부모 요소를 그대로 나열하되 index 4만 제외한다. 부모 템플릿과 `acacia_3.json` 및 모든 다른 모드 리소스는 *압축 전 바이트*가 같아야 하며, 텍스처 슬롯·UV·나머지 요소도 원형 유지한다. 변경되는 자식만 9요소·40면이 된다.

## 실제 대조 설계와 근거

1. 연구용 B6의 출처 고정 45행 원장 및 후보 1순위를 재확인하고, 공식 JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`와 세 원본 JSON Git blob, 모델/블록상태 선택을 검사한다.
2. 기존 [H15 원본 게임 네이티브 F2 8장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/workflows/integration-int4-h15-af-opposing-real-f2.yml) 아티팩트 **#14851461698** ZIP SHA-256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`를 원본으로 고정한다.
3. 실제 Minecraft Java **1.21.1 Fabric** 새 일회성 월드에서 **같은 의자 좌표·마주보는 남북 카메라**로 각 방향 `AF121 variant1 A → AF variant3 비교 → AF121 A 복원 → AIR`, 총 **새 게임 F2 8장**을 생성한다. 매 단계 게임 서버 원본 블록상태 `/execute if block` 응답과 실제 F2 PNG SHA가 있어야 한다.
4. 두 실제 게임 세션의 동일 `A`를 비교해 제거한 4번 요소의 화면 영향 및 반복성을 측정한다. 공통 부모·`acacia_3`가 불변이므로 **variant3 F2 ↔ variant3 F2**, **AIR ↔ AIR**, 같은 세션의 A 복원, 원본 의자 전경 밖 픽셀 변화가 모두 0인지를 음성대조로 확인한다.
5. 두 방향 중 한 곳 이상에서 재현 가능한 비영(非零) 변화가 확인되고 모든 대조가 성립할 때만 `PASS_AF121_ISOLATED_CHILD_ELEMENT4_REMOVAL_NATIVE_F2_RESPONSE`라고 **범위 한정** 판정한다. 그렇지 않으면 조건부/실패로 표시하며 실제 데이터가 나오기 전 성공 수치를 예고하지 않는다.

원본 H15의 8장은 과거 촬영, B7 새 8장만 신규 촬영이다. 장면 구성·의자 상태는 H15와 같아야 하며, B5와 달리 AF121은 `tucked=false`이므로 임의의 지지 top slab 또는 부적절한 접힌 의자 상태를 만들지 않는다.

## 보안·권리·의미 승인 경계

제삼자 원본 PNG·JAR·수정된 JSON/모드 자산은 Git에 저장하거나 배포하지 않는다. 임시 JAR은 실행 폴더에만 두고, 네이티브 F2·게임 로그·SHA 메타데이터만 만료되는 CI 아티팩트에 보존한다. 본 실험은 **소스 요소 제거에 따른 화면 응답**을 검증하는 것이지 픽셀 각각의 원래 GPU 페이스/UV 소유권, 실제 앉기 기능·구조 역할, 나무 재질·스타일, AI 학습/재배포 권리를 승인하는 것이 아니다.

**현재 기준 기존 유효 실험 1/45(B5 AF123 element4)**, 다른 44개는 원래 미실험. B7 성공을 실제 확인하기 전에는 2/45로 올리지 않는다. INT-5 의미·기능·재질·스타일 최종 승인 0/45, INT-6 권리 승인 0, 원래 엄격한 INT-4 H03 HOLD/H05 CONDITIONAL/F70 무조건 0/70 유지한다.

## 재현 산출물

- `src/mcfr/int5_b7_af121_child_element4_f2.py`: 공식 출시본 사전 고정·자식 단독 패치·실게임 F2·두 세션 독립 감사.
- `src/mcfr/runtime.py`: `int5-b7-af121-child-element4-f2` 실제 클라이언트 명령 연결.
- `tests/knowledge/test_int5_b7_af121_child_element4_f2.py`: 공유 템플릿 유지·변형3 변조 차단·합성 픽셀 부정대조 등 **10개** 회귀시험.
- `.github/workflows/integration-int5-b7-af121-child-element4-native-f2.yml`: 정본 H15 아티팩트 SHA 확인, 새 Fabric 실행·F2 8장, 실제 게임 서버 상태/스크린샷 감사.
- 생성 대기 `project/integration/INT5_B7_AF121_ELEMENT4_INDEPENDENT_CAUSAL_AUDIT_V1.json`: 실제 성공한 Actions 결과만 영구 기록한다.

전용 실제 [Actions #45541214422](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45541214422). **현재 독립 F2 감사 결과 확인 전**이며, 새로운 1건의 인과 승인을 미리 부여하지 않는다.
