# INT-5-B1 — 45개 의자 부품 후보와 원본 텍스처·네이티브 F2 16장 교차 연결

기준일: 2026-11-25 (KST). 직계 [INT-5-A Draft PR #112](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/112) head `449558482330f016f2c1c9637eba1a58179b5150`. 본 연구의 새 결과는 기존 1-3/INT-3/INT-4 감사 결과를 **원본 SHA·상태 키로 직접 재연결**한 것이다.

## 1. 실제 수행

원본 의자 역할 후보 45행(`INT5_A_45_ELEMENT_GEOMETRY_ROLE_REVIEW_V1.csv`)과 1-3 기하 시각 검토 45행(`INT3_45_CHAIR_GEOMETRY_REVIEW.csv`)을 동일 **모드·원본 모델 SHA·요소 번호**로 연결했다. 다시 4개 자식 모델의 부모 Git SHA·원본 face UV/PNG 집계(`INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json`) 및 해당 자식의 **실제 Minecraft 네이티브 F2 16개 원본 사례**(`INT3_CLIENT_RUNTIME_16_F2_EVIDENCE.json`)를 모델/상태/회전 방향·이미지 SHA로 대조했다.

각 부품의 원래 1-3 역할 후보는 바꾸지 않았다. 이 단계에서 **원본 가구 전체가 실게임에서 캡처된 기록**과 해당 원본 부품의 구조적 계보까지 연결할 수 있지만, **사진의 어느 픽셀이 특정 요소인지**는 아직 모른다. '이미지를 추가로 직접 본 것'이 아니라 과거 원본 F2 감사 JSON의 신원·SHA·서버 상태를 **다시 검증하는 작업**이다.

| 고정 원본 검증 단위 | 검증 결과 | 의미 |
|---|---:|---|
| 원래 의자 부품 후보 | **45/45** | 원본 provider SHA·요소 ID·기하 역할 가설·자식 모델 연결 |
| 부모 의자 제공자 모델 | **4/4** | AF 기본, AF tucked, HC, Macaw |
| 자식 모델 텍스처 source UV 면 | **229면** | AF 46+46, HC 78, Macaw 59; 소스 수준 기하·원본 PNG 연구에서 재사용 |
| 중복 제거 원본 PNG | **8종** | 자식별 참조 수 3/3/2/2 합계 10은 고유 PNG 수가 아님 |
| 원래 Minecraft 네이티브 F2 | **16/16** | 각 자식 모델별 북/동/남/서 4방향 서버 상태와 정확 PNG SHA |
| 이번 실행에서 원본 PNG를 새로 다운로드해 직접 시각 판정 | **0** | 과거 시각 근거의 **기계적인 출처 재연결**이며 새 육안 의미 승인 아님 |
| 개별 부품 → 실제 F2 화면 픽셀 대응 승인 | **0/45** | INT-5-B2에서 실제 화면/가림·텍스처 관찰 필요 |
| 부품 기능·재질·스타일 의미 신규 승인 | **0/45** | INT-5 전체 최종 의미 승인 미완료 |

## 2. 모델별 정확 근거와 한계

| 원본 제공자 | 부품 가설 | 원본 자식 텍스처·면 | 실게임 F2 | 중요한 제한 |
|---|---:|---:|---:|---|
| Another Furniture 기본 chair provider | **10** | AF121 Acacia `acacia_1`; 46면 | 북·동·남·서 **4장** | 연구 Git 4.0.3과 Fabric 4.0.2 실행본 blockstate SHA **서로 다름** |
| Another Furniture tucked provider | **10** | AF123 Acacia `acacia_10_tucked`; 46면 | 북·동·남·서 **4장** | 같은 버전 차이. 북쪽/남쪽 외 추가 선택자는 개별 조건 대조 |
| Handcrafted chair provider | **13** | HC11210 warped_chair_black; 78면 | 북·동·남·서 **4장** | 연구와 실행본 **blockstate SHA 일치**. 부모 JSON 런타임 바이트 전체 동등성은 별도 |
| Macaw chair provider | **12** | MACAW67 acacia_chair; 59면 | 북·동·남·서 **4장** | 연구와 실행본 **blockstate SHA 일치**. 1.21.11·4방향 선택에 한정 |

실행 F2의 Minecraft 버전은 **1.21.1 12장**, **1.21.11 4장**이다. 1-3 소스/기하가 제공하는 역할 후보는 다리·하부기둥 **16**, 등받이 조립 **16**, 하부 프레임 **7**, 좌판 **6**으로 유지했다. 일부 자식의 소스 blockstate가 실행 JAR와 동일하더라도 그것만으로 모든 부모 JSON·각 요소의 게임 내 표현·동적 행위를 증명하지 않는다.

**별도 원본 격리 촬영 16장(`INT3_ISOLATED_F2_FINAL_SUMMARY.json`)**은 실제 F2를 추가로 확보했던 기록이다. 이번 새 연구에서 16장의 독립 새 시각 판독을 했다고 계산하지 않고, 배경 가림 검사의 제한을 그대로 보존한다.

## 3. 기계 검증의 신뢰 경계

- 원본 Git blob SHA **7개** 고정: INT-5-A 결과와 과거 geometry/texture/runtime/isolated/selector 원장. 정확 45부품 **원본 부품 후보·모델 SHA·요소 번호**, 4 부모 SHA, 4 자식 source SHA, 16 F2 **사례 ID·파일 SHA·선택 모델·Y 방향·blockstate 연구/실행 SHA**를 직접 독립 대조한다.
- 기존 `INT3_45_CHAIR_GEOMETRY_REVIEW.csv`의 '양각 기하상 그룹 역할이 그럴듯함'은 **가구 부품 기능으로 해석할 가설**이지 재승인된 실제 목재/좌판 기능이나 시각적 관찰이 아니다.
- H03/H05 모델링 전용 범위 PASS와 INT-5 의미 PASS를 혼합하지 않는다. F2가 진짜라는 기록, source face/UV·텍스처가 근거 있다는 기록, 실제 부품 역할을 안다는 기록은 각각 다르다.
- 실제 F2 원본 ZIP·PNG 바이너리 자체는 이번 CI에서 새로 다운로드하지 않았다. 결과 원장은 **메타데이터/해시/판정**만 영구 저장하며 제삼자 미술 자산·JAR·게임 화면을 재배포하지 않는다.

## 4. 검증 코드, 실제 Actions 및 인계

- `src/mcfr/int5_chair_visual_source_bridge.py` — 45개 기하 원형·원본 텍스처 source face 229·16 F2·런타임 2버전 교차검증.
- `tests/knowledge/test_int5_chair_visual_source_bridge.py` — 잘못된 PNG SHA, 모델 부모, AF 릴리스 동등성 위장 등을 차단하는 **10개** 독립 회귀시험.
- `project/integration/INT5_B_45_ELEMENT_TEXTURING_F2_SOURCE_BRIDGE_V1.csv` — 사례별 원본/자식/방향 F2 연결 **45행**.
- `project/integration/INT5_B_16_NATIVE_F2_DIRECTION_SOURCE_BRIDGE_V1.csv` — 실제 원본 F2 16개 정확 버전·블록상태·이미지 SHA **16행**.
- `project/integration/INT5_B_VISUAL_SOURCE_BRIDGE_RESULT_V1.json` — 연결 집계와 SHA 및 승격 방지 판정.
- `.github/workflows/integration-int5-chair-real-f2-bridge.yml` — 고정 원본 독립 검사, 새 CSV/JSON 생성, 이력 보존과 영구 파일 재계산.

첫 성공 [GitHub Actions #45441762426](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45441762426): **10/10 테스트**, 45/45 소스→실게임 맥락 근거, 16/16 정확 방향 F2 대응, 거짓 의미 승인 0. 최초 실행에서 INT5-A 요약 Git blob SHA를 갱신된 원장의 실제 SHA로 수정한 실패 기록을 유지한다. 영구 새 원장 커밋 후 다시 재생성 일치 검사 필요.

## 5. 상태 및 다음 단계

**INT-5-B1: 전체 가구 외형 실게임 F2에 대한 출처 연결 범위 완료. INT-5-B2 실제 부품별 시각·의미 판정 미완료.**

다음에는 원본 캡처를 실제 개봉·관찰하고 그 장면의 부품별 가림·실제 텍스처 표면을 모델 요소에 대응해야 한다. 어려운 경우 새로운 F2를 무조건 45개 찍는 대신 기존 4모델 4방향 이미지를 다시 검토하고 **한 장에서도 특정할 수 없는 부품만** 최소 재촬영한다. 전제는 실제 원본/버전/선택 상태 일치다.

기존 INT-3·INT-4 원본 역사 파일 불변, `main` 미병합, INT-6 AI 학습·제삼자 자산 재배포 승인 0.
