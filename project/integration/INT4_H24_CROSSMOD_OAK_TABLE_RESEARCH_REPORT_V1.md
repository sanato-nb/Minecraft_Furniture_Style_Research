# INT-4 H24 — 3개 가구 모드 oak_table 선택 모델·UV 교차 연구

## 1. 목적과 연구 범위

H23 Draft PR #105에서 확보한 **별도 모델링 F70 V5 70/70 범위 통과**를 상위 기준으로 삼는다. 새 검증 분모를 임의 확대하거나 기존 조건부 H03/H05를 승인하지 않는다. H24에서는 Another Furniture, Handcrafted, Macaw's Furniture의 **oak_table 6개 서로 다른 상태에서 실제 선택된 모델·상속·면·UV와 기존 원본 F2 신원**을 비교한다.

연구 질문: 이름이 같은 oak_table 모델을 동일하다고 판단하여 재사용해도 되는가? **그렇다고 가정할 수 없다.** 각 모드의 원본 blockstate는 서로 다른 변수로 모델을 선택한다. 동일 조형 의미, 동일 카메라 간 픽셀 일치, GPU별 면 귀속까지 증명한 것은 아니다.

- 상위 부모: [H23 Draft #105](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/105), 원본 SHA 07925fbee8758e64bbbfc532587eb035821c6c3a.
- 원본 H21 [AF 16건 공식 출처 정합성](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/103): 연구 Git 4.0.3 / 실행 Fabric 4.0.2 구분. 증거 JSON Git blob SHA-1 8b6ba58b0fcdd6f6681019dd1f8b58047c8b9d97.
- 원본 H22 [HC·Macaw 12건 공식 출처 정합성](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/104): 릴리스 모델·UV·PNG와 기존 F2 연결. 증거 JSON Git blob SHA-1 b659e12153d0d2c12710bb4e24e236c934b06c14.
- H23 V5의 70행 CSV Git blob SHA-1 95ee0efa5dda895a8ce08e1291286e775d9a73dd; V5 요약 JSON Git blob SHA-1 2c7092534d377cdbb5676fa3b96df2ef6b4615bd.
- 새 Minecraft 세션 **0**, 신규 F2 **0**. 기존 6개 원본 native F2 SHA256을 재사용하며 원본 JAR/PNG/화면을 Git에 복제하지 않는다.

## 2. 여섯 원본 선택 상태의 측정

| 원본 사례 | 모드·MC | 상태의 선택 변수 | 모델 적용 | 요소 | 총면 | UV 측정면 | 0면적 UV |
|---|---|---|---:|---:|---:|---:|---:|
| S14 | AF · 1.21.1 | 다리 4개 true | 5 | 13 | 42 | 42 | 0 |
| S15 | AF · 1.21.1 | 다리 4개 false | 1 | 1 | 6 | 6 | 0 |
| S16 | HC · 1.21.1 | shape=single | 1 | 10 | 60 | 40 | 20 |
| S17 | HC · 1.21.1 | shape=center | 1 | 2 | 12 | 8 | 4 |
| S18 | Macaw · 1.21.11 | east/north/south/west=false | 1 | 6 | 31 | 31 | 0 |
| S19 | Macaw · 1.21.11 | east/north/south/west=true | 1 | 1 | 6 | 6 | 0 |

- **Another Furniture**: S14는 상판 1적용(1요소·6면)과 다리 4적용(각 3요소·9면)으로 13요소·42면. S15는 상판만 1요소·6면. S14−S15는 **+12요소·+36면**, 모델 적용 +4.
- **Handcrafted**: S16은 부모 table/single에서 10요소·60면, S17은 table/center에서 2요소·12면. 차이는 **+8요소·+48면**. 각 상태에 문서화된 UV 0면적 면은 20/4개로 원본대로 기록한다.
- **Macaw**: S18은 부모 table_single에서 6요소·31면, S19는 table_center에서 1요소·6면. 연결 변수가 사방 false→true일 때 선택된 소스 차이는 **+5요소·+25면**(S18−S19).
- 각 수치는 **선택된 원본 모델에 기술된 면**의 개수다. 실제 화면의 가시 면 개수, 화면 픽셀 면적 또는 물리적 조립 단위를 의미하지 않는다.

## 3. 앞으로 재사용할 지식과 금지할 잘못된 가정

1. 동일한 영문 이름 oak_table만으로 모델을 동일시하지 않는다. **리소스 namespace / 모드·Minecraft 버전 / 정확 blockstate / 모델 선택 경로 / 부모 모델 체인**을 하나의 신원으로 관리한다.
2. AF의 다리 플래그 leg_1~leg_4, HC의 shape, Macaw의 동·서·남·북 연결 플래그는 **각자 다른 상태 계약**이다. 모드 간 같은 물리 상태나 동등한 기능이라고 추측하지 않는다.
3. AF의 **복수 모델 동시 적용**과 HC·Macaw의 **상태별 부모 모델 교체**는 구조가 다르다. 재사용 가능한 모델링 설계를 판단하려면 실제 모델 선택과 geometry 및 UV 차이를 함께 봐야 한다.
4. 면 개수와 UV 유효 면 수를 혼동하지 않는다. HC의 ZERO_UV_AREA 20/4는 정확히 보존한다. UV 품질의 모드 간 우열을 해당 개수만으로 판단하지 않는다.
5. 기존 F2를 재사용할 때는 원본 액션 런 ID와 PNG SHA256을 보존한다. 이미 성공한 촬영을 반복하지 않지만, 새 상태/새 모드에 대한 F2 검증을 자동 승인하지 않는다.

## 4. 산출물 및 회귀 검증

- 감사기: src/mcfr/int4_h24_crossmod_oak_table.py — H21/H22/V5 원본 네 파일의 Git blob SHA 독립 검사; 70행 원장과 6개 사례 원본 geometry/UV/F2 동시 대조; 서로 다른 상태 속성 검출 및 모드 내 모델 차이 재계산.
- 원본 사례별 CSV: project/integration/INT4_H24_CROSSMOD_OAK_TABLE_CASES_V1.csv.
- 비교·범위·출처 JSON: project/integration/INT4_H24_CROSSMOD_OAK_TABLE_RESULT_V1.json.
- 회귀시험: tests/knowledge/test_int4_h24_crossmod_oak_table.py — 원본 F2 SHA 오염, 원본 UV 면 오염, HC 0면적 UV 누락, 승인 무단 승격 차단.
- Actions: .github/workflows/integration-int4-h24-crossmod-oak-table.yml에서 결과를 독립 계산해 영구 CSV/JSON과 비교.

## 5. 승인 경계

- **H24 신규 연구 범위**: 세 모드의 원본 검증된 oak_table **6개 상태 / 모드 내부 3쌍 비교**. 이는 기존 F70 모델링 분모의 신규 사례가 아니며 F70 V5 70/70 수치를 승격·변경하지 않는다.
- 기존 F70 엄격 무조건 승인 **0/70**, 조건부 **70/70**; H03 **HOLD**, H05 **CONDITIONAL**. INT5 가구 의미 승인 **0**, INT6 AI 학습·재배포 권리 승인 **0**.
- 모드 간 렌더링 결과 동일성, GPU 개별 텍셀-픽셀 귀속, 모든 가구 모델, 모든 버전, 공식 의미·권리 승인은 **미증명**.
- 다음 후속 연구는 새로운 가구 모드의 공식 원본 선정·버전 SHA 고정부터 진행하며, H24의 6개 교차 비교를 다른 가구의 자동 호환성 증명으로 사용하지 않는다.
