# INT-3 후속 — Another Furniture 4.0.2 ↔ 연구 4.0.3 의자 모델·기하·UV 차이 감사

## 판정

**완료: 고정된 `acacia_chair` 상태/연결 모델 범위에서 의미상 차이 0건.** 실제 Fabric 실행 릴리스 **4.0.2**와 원본 소스 커밋으로 고정된 **연구 4.0.3**을 각각 다시 취득해 비교했다. 과거 PR #33·#34에서 발견한 두 버전의 **블록상태 Git blob SHA 불일치**는 실제로 존재한다. 그러나 양측의 88개 selector/대상 모델/회전 선택 내용은 모두 같고, 참조된 원본 JSON 24개도 파싱 결과가 동일하다. 단순 SHA 불일치를 기하 차이로 오해할 필요는 없다.

| 대조 범위 | 실제 결과 | 판정 |
|---|---:|---|
| 4.0.3 `acacia_chair` 상태 선택 규칙 | 88 | 원본 Git blob SHA 재확인 |
| 4.0.2 실행 JAR의 같은 상태 선택 규칙 | 88 | 고정 JAR SHA-1 검증 |
| 동일한 selector + 선택값(JSON 의미) | **88 / 88** | **차이 0** |
| 실제 F2 촬영에 사용했던 AF 모델 선택 | 8 / 8 | 양쪽 버전 존재 |
| selector가 참조하는 가구 자식 모델 합집합 | 22 | 전체 검사 |
| 전이적 부모 모델을 포함한 JSON | **24 / 24** | JSON 의미 동일 |
| 부모를 풀어 비교한 유효 기하 | **22 / 22** | 변경 0 |
| 부모를 풀어 비교한 면 UV | **22 / 22** | 변경 0 |
| 면별 텍스처 슬롯/대상·cullface 등 | **22 / 22** | 변경 0 |
| 모델 JSON 원본 바이트 완전 동일 | **0 / 24** | 포맷/직렬화 차이가 존재; 실제 내용은 같음 |
| 누락되거나 해석할 수 없는 참조 모델 | **0** | 검사 범위 완결 |

### 고정된 원본 및 재현

- 연구 소스: `crispytwig/AnotherFurniture` commit `57eb624cbb7f408d43398c7434b0d38d312cb55d`. 원본 `common/src/main/resources/assets/another_furniture/blockstates/acacia_chair.json` Git blob SHA-1 `37643398d7a49fdcfc6f2308ca04c13fb0b43aed`.
- 실행 소스: 기존 `research/furniture_mods/phase_1-3/runtime_actions/run_probe.py`의 pinned Modrinth JAR `another_furniture-fabric-4.0.2.jar`. JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`; 내부 `acacia_chair.json` Git blob SHA-1 `3a806533856f169a502373bda43a76eeabc1e689`.
- 고정 4.0.3 부모 모델 Git blob SHA: `block/template/chair` = `d9b64a818021f1a64b0cba13d16d18d6fea65d01`, `block/template/chair_tucked` = `ebcd7af6545ada207ad31720cb831b9ec5eb1dde`.
- 감사 스크립트: `src/mcfr/af_release_version_audit.py`; 회귀 시험: `tests/knowledge/test_af_release_version_audit.py` (4개 모두 통과).
- [**실제 GitHub Actions 성공 #44906927679**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44906927679). 결과 아티팩트 `int3-af402-vs-af403-source-geometry-uv-diff` (ID `14707954093`)에 비교용 메타데이터 JSON 및 상태/모델/유효 기하·UV CSV 3종을 보존. 원본 JAR·상용 리소스 바이트는 아티팩트에 포함하지 않았다.
- 검증 수치와 파일별 SHA-256은 `INT3_AF_RELEASE_VERSION_COMPARISON.json`에 고정했다.

### 결과의 정확한 범위

본 감사가 증명한 것은 **Another Furniture의 `acacia_chair`가 참조하는 22개 자식 모델과 2개 부모 모델의 JSON 의미상 등가성**이다. **Another Furniture 모드의 나머지 모든 블록/모델, 실제 PNG 텍스처 픽셀의 동일성, Minecraft의 baked mesh·실시간 조명·UV atlas 정합, 타 블록과의 상호작용**까지 전체 버전에서 같다는 뜻이 아니다. 게임 클라이언트 F2와 서버 상태 검증 16건은 별도로 완료된 PR #33·#34 증거를 사용하며, 이 감사가 새 F2를 촬영한 것은 아니다.

4.0.2와 연구 4.0.3 모델 JSON 자체는 전부 바이트 불일치였으나 의미상 동일하다. JSON 텍스트 포맷이 다르더라도 geometry·UV가 달라졌다고 단정하면 안 되며, 본 보고서는 실제 파싱·부모 상속 후의 비교에 따라 의미상 동일성을 판정한다.

**계속 보류:** 의자 개별 부품 역할 45개, 사람이 판독한 재질·스타일, 화면의 실제 baked face/UV 확인, 충돌·앉기 동작, 제삼자 원본의 재배포/AI 학습 허가. 이 항목들에 대한 신규 승인 수는 각각 **0**이다. AI 가구 제작용 지식으로 넘길 때도 검증된 정적 기하 근거와 사람 검수/라이선스 대기를 구분한다.

### 기존 연구 보존 및 다음 순서

PR #34의 촬영 사진 SHA·월드 격리 검수와 1단계/INT-2/INT-3 역사 증거는 수정하지 않았다. 본 PR은 PR #34 최종 커밋에서 분기한 Draft로서 `main`을 건드리지 않는다.

다음 검수는 **1-3-C의 45개 부품 역할 후보를 F2 화면의 해당 개별 부품과 실제로 대조**하는 것이다. 전체 의자 화면과 부품 원본을 출처만 연결했다는 사실과 부품별 시각 판정을 혼동하지 말아야 한다. 부품을 개별로 관찰할 수 없는 경우에도 역할 확정 대신 `PENDING / OCCLUDED / INSUFFICIENT_VIEW`로 남긴다.
