# INT-4-D 고정 블록상태 1,158개·선택 규칙 78,456개와 모델·원본 SHA 전수 인수

역사 1-3-D 독립 원본 JSON 감사와 1-3-F SQLite를 직접 키/출처 SHA/선택 모델/회전/uvlock별 대조했다.
이번 실행에서 upstream JSON 1,158개를 재다운로드·재파싱하거나 Minecraft 게임을 실행한 것은 아니다.

## 정적 원본 선택 검증

- Another Furniture 177 JSON / 9,325 규칙·선택, Handcrafted 267 / 60,921, Macaw 714 / 8,210.
- 1,158 state / 78,456 rule / 78,456 option 개별 키와 원본 model_id·source SHA, 선언 조건과 x/y/uvlock/weight 검산.
- 로컬 78,420선택, 바닐라 1.21.1 모델 32선택, AF unused white_awning 미해결 4선택.
- 역사 원본 declared variants 1,136개 / multipart 22개, 원본 관측 조합 variant 80,787, multipart 2,112.
- 원본 모델 48개 부모 누락은 정적 선택 0개. 이 사실로 동적 런타임 사용 부재까지 단정하지 않음.
- AF birch/spruce chair의 south variant=3→1 모델 선택 2건은 수정하지 않고 intent/F2 검사 보류.
- JSON 상태 중 코드 근거가 기존에 매핑된 500개와 JSON 규칙만 확인된 658개를 구분.
- Handcrafted 회전 각도 원형을 360으로 나누어 별도 보존; 1,736 옵션은 원형이 0~359 범위 밖.
- Macaw uvlock=true 기존 원본 1,132 옵션을 독립 재집계.

## 고정 연구 버전과 배포본 혼용 제한

AF 4.0.3 Git 연구본과 Fabric 4.0.2 JAR의 acacia_chair에서 88 선택 규칙은 이전 연구에서 동등성을 확인했지만 SHA는 다르다.
이를 AF 전체 177 blockstates의 배포본 동일성으로 확대하지 않는다.

## 다음 단계

- 1,158개별 요약 및 78,456 선택의 출처 원장을 각각 신규 파일로 기록.
- 이전 6 예외를 별도 CSV로 유지. model option별 C 6,343면 출처 예외 연결은 모델의 정적 선택 문맥이며 실제 손상 면이라는 뜻이 아님.
- INT-4-D 실게임 도달 가능 상태/커스텀 Java 렌더/릴리스 비교 최종 승인은 보류. 별도 INT-4-F에서 정확한 버전·F2 필요.
- INT-5 의미 승인, INT-6 가구 소스 AI 학습/배포 권한 0 유지.
