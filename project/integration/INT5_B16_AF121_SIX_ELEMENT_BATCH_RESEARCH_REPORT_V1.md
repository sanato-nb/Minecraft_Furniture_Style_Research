# INT-5-B16 — AF121 원본 미검증 6요소를 한 번에 실제 Minecraft F2 비교 연구

작성일: 2026-11-25 KST. 직계: [INT-5-B15 Draft PR #127](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/127) HEAD `886dceab0a9b56f066605df3d413ff9cdb246d04`. 원본 main과 과거 Draft 증거를 병합하지 않고 이 HEAD에서 분기.

## 1. 실제 배치 연구 목적

이전 B15는 AF123 tucked 의자의 미검증 6개 소스 요소를 한 PR/여섯 CI 병렬 실험으로 실제 분석해 **5개 bounded PASS, index5 한 개 두 시점 화면 변화 미검출**을 기록했다. B16에서는 다른 독립 원본 모델인 AF121 기본 의자에서 아직 개별 실게임 개입하지 않은 **6개**(0·1·2·3·5·6)를 **한 개의 PR·Actions 병렬 6 job**으로 연구한다.

| 원본 모델/요소 | 원본 면 수 | B3 기하·텍스처 기반 역할 가설 | B15 기준 상태 |
|---|---:|---|---|
| AF121 / AF1393 / 0 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 1 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 2 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 3 | 5 | LEG_OR_LOWER_POST | 미시험 |
| AF121 / AF1393 / 5 | 4 | LOWER_FRAME | 미시험 |
| AF121 / AF1393 / 6 | 4 | LOWER_FRAME | 미시험 |

기존 B7/B9/B10/B11에서 검증한 AF121 4·7·8·9는 **다시 성공 사례로 더하지 않는다**. 고정 원본 B3 45부품 역할/face 증거 Git blob SHA1 `d314941b950b70fa637536f86182eb4866b7aed1`, 그리고 B15 전체 45행 상태 CSV를 정확 ID로 연결한다. 위 '다리/하부 프레임' 명칭은 **기능·재질 승인 전의 기하 역할 가설**이다.

## 2. 실제 소스와 영구 검증 계약

- Minecraft Java **1.21.1 Fabric**, 공식 Another Furniture **Fabric 4.0.2** JAR 원본 SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`, parent `template/chair` 원본 Git blob `31c643617a7178ac5113702e785620f4d1150adf`, target child `acacia_1` 원본 blob `2261460299d13a15220f4fecfe059628ac28e813`, 음성대조 sibling child `acacia_3` blob `1c5ef86b8413f7c8d246869cb63b21dfd8f6853e`.
- 원본 부모 10 요소·46 faces. 각 CI job은 원본 자식 `acacia_1.json` 단일 리소스만 임시 재정의하고 **해당 인덱스 한 요소만 제거**하여 9 요소·41 또는 42 faces. 나머지 원본 부모·`acacia_3` 비교 자식·텍스처·모든 다른 원본 JAR 멤버는 압축 전 바이트 동일, ZIP CRC 및 Git blob 검증.
- 정상 원본 상태 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`, 비교 컨트롤 `variant=3`, 고정 시점 south/north. 기존 원본 H15 원본 실제 F2 **8장**, artifact `14851461698`, ZIP SHA256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`를 각 job의 기준으로 엄격 재개봉.
- 모든 작업은 별도 창/일회성 세계에서 네 단계 `model1 A → model3 음성대조 → model1 A 복원 → AIR`를 두 대향 시점에서 검사. **job당 새 F2 8장, 원본 서버 상태 마커 8개**, ZIP·PNG·로그 SHA/원본 ROI 픽셀·음성대조·반복 A/A 검사. 화면이 같으면 미검출/조건부로 보존하며 임의로 PASS 처리하지 않는다.
- 시각 변화가 나와도 원본 특정 요소의 화면 변화 **인과 응답**만 한정해 승인한다. 실제 face별 GPU 픽셀 배타적 소유권이나 기능·좌판 착석·재질·스타일·제삼자 AI 학습/재배포 권리를 의미하지 않는다.

## 3. 배치 실행 코드 및 CI

- `src/mcfr/int5_b16_af121_six_element_batch_f2.py`: B11의 실제 원본 H15/Fabric 재검증 경로를 공통화하고 동적 원본 요소 정확 ID/face 수·원본/음성대조 인과를 배치화.
- `src/mcfr/runtime.py`: `int5-b16-af121-batch-f2 --index {0,1,2,3,5,6}` 명령, 동일 공식 AF121 source fixture.
- `tests/knowledge/test_int5_b16_af121_six_element_batch_f2.py`: 13개 원본/음성대조/미승인 회귀시험.
- `.github/workflows/integration-int5-b16-af121-six-element-batch-f2.yml`: **6개 매트릭스 작업, fail-fast false, 병렬 3개**, 각 작업 개별 네이티브 F2/서버/출처 독립 감사.
- 성공 또는 불일치 발생 시 각 job 아티팩트는 자신이 캡처한 실제 PNG/client.log/JSON·메타데이터만 업로드한다. **임시 JAR·타사 텍스처/모델을 배포하지 않는다**.

## 4. 정확한 완료 범위와 다음 단계

- 배치 시작 시 기정 검증 인과 PASS **14/45**, 화면 미검출 **1**, 미시험 **30**.
- B16 여섯 요소 모두 독립 bounded PASS일 때만 **최대 20/45**. 화면 효과 0·실험 실패·양성대조 혼선이 나오면 해당 요소 단위 보류, 이전 검증 결과로 대체하지 않는다.
- B16 이후 아직 HC11210 **12개**, Macaw MACAW67 **12개**(별도 Minecraft 1.21.11/원본 JAR), 기존 AF123 index5 미검출의 원인까지 남는다.
- 기존 엄격 **H03 HOLD, H05 CONDITIONAL, F70 무조건 승인 0/70**, INT-5 최종 부품 의미 승인 0/45, INT6 타사 학습·재배포 허가 0은 불변.

**실제 Actions가 끝나고 PNG·로그·서버 상태·ZIP SHA를 검증하기 전에는 신규 인과 성공 숫자를 기록하지 않는다.**
