# INT-4 — 부모 누락 48개 원본 모델의 블록상태 사용 여부 독립 재검증

## 착수 근거

[이전 PR #39](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/39)는 Another Furniture 랜턴 4건, Macaw 책상 22건과 서랍 22건, 총 48개 모델에서 **부모 모델 파일 누락**을 실제 원본 SHA·파일 내용으로 확인했다. 그런데 모델 파일 존재 자체만으로 인게임에 쓰인다고 말할 수 없다.

이번 INT-4의 목적은 **원본 블록상태 선택 표에 해당 48개 자식 모델이 나타나는지, 직접/부모 경로로 연결 가능한지**를 전수 판정한 뒤 실제 Minecraft F2 촬영 대상을 근거에 맞게 고르는 것이다.

## 독립 검사

- `scripts/integration/audit_int4_parent_reachability.py`에서 AF 고정 Git 소스, Macaw Fabric 3.4.2 JAR의 **전체 assets/{namespace}/blockstates/*.json, models/**/*.json, items/**/*.json**을 읽는다.
- `variants`와 `multipart` 모든 명시적 정적 모델 옵션을 읽어 직접 참조를 구성하고, 모델 parent 체인을 원본 JSON대로 순회한다. 1.21.11의 아이템 정의 모델 참조와 `models/item/` 후보는 블록상태와 별도 분모로 관리한다.
- 역사 원본 부모 누락 48개를 전부 원본 모델 소스 B 원장에 기록된 SHA와 바이트 크기로 다시 대조한다.
- 각 대상별 직접 blockstate 선택 건수, blockstate 상속 계보 경유 도달 여부, 아이템에서 참조 가능 여부, 고정 48건과 정적 미해결 108건의 중복을 보고한다.
- 원본 ZIP/JAR/PNG/JSON 본문은 Git/아티팩트에 복제하지 않고 **원본 경로·참조·집계·SHA 메타데이터만** 저장한다.
- `tests/integration/test_int4_parent_reachability.py`: 가중 variant 옵션, multipart, 부모 체인·순환, 최신 아이템 정의, 잘못된 모델 참조 등의 회귀 테스트.
- `.github/workflows/integration-int4-parent-reachability.yml`: 실제 원본 다운로드 → 테스트 → 정적 참조 전수 분석 → 역대 SHA 체크포인트 일치 검사.

## 판정 경계

**블록상태 참조가 없다는 결과**는 정적 블록상태 목록에서 도달하지 못한다는 뜻이다. 실제 동적 Java 렌더·등록, 커스텀 모델 로더, 리소스팩 오버라이드, 아이템 동작까지 사용되지 않는다는 증거는 아니다.

**정적 블록상태에 참조되는 결과**도 실제 해당 블록이 등록되고 플레이어에게 배치·렌더됐다는 뜻은 아니다. 해당 경우에만 원본 블록 ID·속성·선택 모델을 별도 확인하고 실제 Minecraft Fabric 화면을 테스트한다.

- 원본 소스 조작·부모 경로 자동 교정: **하지 않음**
- INT-5 부품 의미·스타일 최종 승인: **0 유지**
- INT-6 AI용 저작권·학습 권리 승인: **0 유지**
- INT-4 전체 통합 종료: **아직 아님**

## 결과

실제 원본 CI 실행 결과를 근거로 추가한다. 아직 원본 블록상태 참조 건수를 단정하지 않는다.
