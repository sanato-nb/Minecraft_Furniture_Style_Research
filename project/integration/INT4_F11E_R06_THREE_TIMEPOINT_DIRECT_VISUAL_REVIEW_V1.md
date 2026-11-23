# INT-4-F11E R06 실제 Macaw 싱크 시간차 세 프레임 독립 감사

- Minecraft 1.21.11 Macaw 3.4.2 원본 S43 물 true 싱크 실제 게임 3시점 네이티브 F2, 8초 이상 간격.
- 각 원본 프레임 전 서버 정확 상태 재조회 3회 PASS; 원본 모델 SHA/JAR SHA256 고정.
- 원본 S42 물 false 16요소·55면 대비 S43 물 true 17요소·56면 (면 +1), 애니메이션 인과 별도.
- 시간 간격(초): [10.615, 10.358]
- 수면 샘플 판정: WATER_REGION_CHANGED_AT_SAMPLED_TIMES_NOT_CAUSAL_ANIMATION_PROOF
- 물 ROI 전경 픽셀: {'R06_T0': 778, 'R06_T1': 778, 'R06_T2': 778}, 배경 대조 최대 변경 0px.
- 원본 ZIP SHA256: ddf965f6f87e91a2c4b65f435f36eae5ea6ed1fdee8e7638a0097f1fdb2e938e / Actions 원본 F2 아티팩트 14786478182
- R06 한 행만 HOLD→CONDITIONAL; 조건부 68→69/70 (98.6%), HOLD 2→1 (R08). 역사62/62 유지.
- 최종 무조건 F 승인 0, 물 기능/움직임 코드 인과·UV·부품 의미·학습/재배포권·G/H 보류.
