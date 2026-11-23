# INT-4-H7 6개 위험 시나리오 원본 게임 단계별 재감사

- 실제 원본 Actions ZIP 6개 및 재사용 원본 F2 21건의 SHA/CRC·client.log·원본 캡처 JSON을 재열람.
- **R01** S10 단일 사례 정확 서버상태 재확인. 동일 범주 전체 일반화 불가.
- **R02** AF 의자 variant3 4방향 + variant1 2개 대조. 원본 선택 모델/릴리스 차이 확인; UV 인과 미확정.
- **R03** Macaw 테이블 reset→join→remove의 연결 true/false 자동 갱신 확인. 플레이어 아이템 설치는 미시험.
- **R04** Macaw 싱크 water=false/true 정적 두 상태 확인. 애니메이션 미입증.
- **R05** 침대 설치·수면 occupied=true·기상 occupied=false, 별도 게임 실행에서 침대 두 부분 파괴 후 air 확인. 단일 연속 실행 아님.
- **R07** AF variant3 남향이 acacia_1 모델을 선택하고 나머지 세 방향은 acacia_3 선택. R02와 같은 F2 재사용, 버그·의도 판정 보류.
- 기존 70/70 조건부, H03 HOLD·H05 CONDITIONAL, H 범위 통과6/조건부1/보류1, 무조건 종료0 유지.
- 이번 작업은 새 게임 재실행이 아니라 원본 아티팩트의 독립 단계별 증거 교차검증. UV·동적 기능·부품 의미·학습/재배포권 미승인.
