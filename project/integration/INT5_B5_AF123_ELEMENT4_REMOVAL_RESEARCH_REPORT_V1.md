# INT-5-B5 — AF123 의자 element 4 단일 제거·실제 Minecraft F2 인과 대조

검증일: **2026-11-25 (KST)** · 직계 [B4 Draft PR #116](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/116) head `d055d1dcacab751330cfe49d8b33224759484d76` → 후속 [B5 Draft PR #117](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/117). `main` 직접 변경/병합 없음.

## 1. 연구 질문과 실험 한계

B3에서 고정된 AF123 실제 원본 연구의 **provider AF1394, element index 4, 역할 가설 SEAT_LAYER, 6면**에 대한 화면별 출처 인과를 좁혀 확인했다. 기존 B4는 유효한 `tucked=true`에 **인접 top slab 지지 구조**가 필요한 것을 확인하고, 그 구조를 변경하지 않은 대향 카메라 F2 8장/서버 상태 16건을 획득했다.

B5는 출시된 **Another Furniture Fabric 4.0.2**의 원본 JAR을 확인한 다음, 실제 모델 상속 체인의 제공자 JSON에서 element 4 하나만 임시 제거한 게임을 새로 실행해 B4 원본과 비교했다. **원본 모델에 변형을 가한 인과 시험이며, 원래 모델에 속한 픽셀을 물리적으로 단독 추출한 시험은 아니다.**

## 2. 실제 소스·버전·수정 범위

| 검증 항목 | 실제 결과 |
|---|---|
| 실행 버전 | Minecraft Java 1.21.1 Fabric · Another Furniture Fabric **4.0.2** |
| 원본 JAR SHA-1 | `c2f992081bdc4795ed6d87771a3b5f7c71103785` |
| 임시 JAR SHA-1 | `ae95bacde791e5f0c62e31f4654463fcfb5e33e6` |
| 실제 하위 선택 모델 | `another_furniture:block/chair/acacia_10_tucked` |
| 실제 제공자 상속 모델 | `assets/another_furniture/models/block/template/chair_tucked.json` |
| 원본 모델 기하 | **10요소 · 46면** |
| 임시 수정 모델 기하 | **9요소 · 40면** (index 4의 6면만 제외) |
| 실제 바뀐 JAR 내부 비압축 리소스 | **JSON 1개** |
| 수정 JAR/제3자 PNG 소스 Git 커밋 | **0개** |

원래 연구용 Another Furniture **Git 4.0.3**과 이번 실행 **Fabric 4.0.2**의 소스·블록상태가 자동 동등하다고 주장하지 않는다. 실제 출시 JAR에서 모델 부모 체인을 독립적으로 따라가 4번 요소의 구조를 확인했고, ZIP CRC·내부 멤버 차이 1개를 검증했다.

## 3. 실제 GitHub Actions와 네이티브 F2

- [**B5 검증 Actions #45538471626 — SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45538471626). 수정된 실행에서 **새 F2 8/8장**, 의자·슬랩 **서버 정확 상태 16/16건**, 모델 제거·대조 독립 감사 성공.
- [**B4 원본 Actions #45528207751 — SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751) 원본 F2 **8/8장**의 SHA·서버 상태·원본 감사 JSON이 기존 Git 원장과 동일함을 새 CI에서 다시 확인. 원본 게임을 변경하지 않음.
- 총 **2개 독립 실게임 세션**, 원본 기준 8장 + 임시 수정 8장. 모두 원본 게임의 1024×684 PNG 네이티브 F2다. B4는 기존 세션이므로 '신규 F2 16장'이 아니라 **이번 신규 8장**이다.
- 원본/수정 장면의 **남·북 카메라 좌표와 촬영 상태가 완전히 동일한지 검사**했다. 각 시점의 `A(의자+슬랩) → B(슬랩만) → A복원 → AIR`를 사용했다.
- B5 원본 스크린샷·게임 로그·사례별 SHA/감사 파일은 임시 만료 아티팩트 [**#14988835814**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45538471626/artifacts/14988835814)에만 보관하고, 수정한 게임 JAR는 아티팩트에도 포함하지 않았다.

## 4. 화면 변화와 음성대조 — 실제 독립 감사 결과

원본과 수정본 F2에서 동일 카메라·같은 게임상태를 비교했다. 화면 ROI `x=[350,675), y=[275,620)`, RGB 채널 임계값 24, 실제 PNG SHA 검증 후 비교한다.

| 동일 카메라·상태의 픽셀 차이 | 남쪽 카메라 | 북쪽 카메라 |
|---|---:|---:|
| **원본 의자 A ↔ index4 제거 의자 A** | **751px** | **0px** |
| **원본 A복원 ↔ 제거 A복원** | **751px** | **0px** |
| 슬랩만 남긴 B ↔ 수정본의 슬랩만 B | **0px** | **0px** |
| 의자·슬랩 모두 없는 AIR ↔ 수정본 AIR | **0px** | **0px** |
| 임시 수정 세션 A ↔ A복원 (시간 변동) | **0px** | **0px** |
| 개입 픽셀 중 기존 원본 의자 전경 **바깥** | **0px** | **0px** |

**실제로 확인된 결론:** 정상적인 법적 지지 슬랩을 보존한 AF123 모델에서 정확한 4번 원본 요소를 임시 제거하면, **남쪽 시점에만 751픽셀의 재현 가능한 의자 전경 변화가 발생**했다. 북쪽은 해당 ROI에서 0픽셀이다. 네 종류의 무변경/재촬영 음성대조가 0이므로 무관한 슬랩·빈 월드 픽셀이나 시간 변화로 751픽셀을 설명하지 못한다. 실제 감사 판정은 `PASS_BOUNDED_AF123_ELEMENT4_REMOVAL_RENDER_RESPONSE`다.

**과장 금지:** 북쪽 0픽셀만으로 원본 좌판이 완전히 가려졌다고 단정할 수 없다. 요소 제거는 차폐, 광원·AO, 뒤쪽 면 노출에도 영향을 줄 수 있기 때문에, **남쪽 751픽셀 전부가 원본 element4 자체에 직접 속한 픽셀**이라는 뜻도 아니다. 이번 연구는 **'정확한 소스 요소 제거 → 화면 변화'의 범위 한정 인과**를 확인한 것이다.

## 5. 영구 산출물과 엄격한 승인 경계

- `src/mcfr/int5_af_element4_removal_f2.py`: 공식 출시 JAR SHA 고정, 실제 상속 부모 모델 판독, 오직 요소 하나만 임시 제거, 실제 두 세션 F2·서버로그·음성대조 독립 감사.
- `src/mcfr/runtime.py`: `int5-b5-af-element4-removal` 격리 런처.
- `tests/knowledge/test_int5_af_element4_removal_f2.py`: **9개** 부정대조·원본 모델 회귀시험, 기존 B4의 7개 회귀시험과 함께 성공. 합성 PNG 시험은 실제 F2라고 간주하지 않음.
- `.github/workflows/integration-int5-b5-af-element4-removal-native-f2.yml`: 원본 B4 Actions 아티팩트 재검사, 실제 새 Fabric 1.21.1 실행, 직접 F2/로그/픽셀 감사.
- **`project/integration/INT5_B5_AF123_ELEMENT4_NATIVE_F2_CAUSAL_AUDIT_V1.json`**: 실제 Actions 감사의 영구 보존 메타데이터 (개별 PNG SHA/원본 JAR/화소 변화/부정대조). PNG와 JAR 자체는 보존하지 않음.

| 범주 | 판정 |
|---|---|
| B5 범위 한정 단일 요소 제거 → 실제 F2 인과 | **PASS** |
| 원본 JSON 요소의 배타적 화면 픽셀 소유 확정 | **미승인** |
| 개별 45개 부품 기능·재질·스타일 최종 승인 | **0/45 유지** |
| INT-6 AI 학습·재배포 권리 승인 | **0 유지** |
| 기존 INT-4 원래 엄격 게이트 | **H03 HOLD / H05 CONDITIONAL / F70 무조건 0/70 유지** |
| INT-4 별도 모델링 범위 한정 승인 | **기존 70/70 유지**, B5와 다른 분모 |

## 6. 후속 연구에 전달할 지식

AF123의 소스 요소 4(6면)는 **정확히 소스 모델에서 제거했을 때 남쪽 F2의 의자 전경을 바꾸는 요소**라는 재사용 가능한 제한된 사실이 확보됐다. 해당 요소에 대한 `SEAT_LAYER`는 원본 PNG 경로·기하에 근거한 역할 가설이며 사용 기능은 아직 미확정. 다음 단계에서는 기존 B3의 45부품 원장에 **개입에 따른 화면 반응 / 가림으로 무반응 / 미실험**을 별도 근거 칼럼으로 연결하고, 필요하면 AF 기본 의자 등 더 잘 노출된 다른 하나의 요소에만 같은 검증을 확장할 수 있다. 동일 소스가 제공하지 않는 의미·권리 승인을 추가하지 않는다.
