# INT-4-F5 — 원본 게임 12회 속성 변화 독립 증거 감사

- 원본 Fabric 1.21.1 캡처/클라이언트 로그: [Actions #45026378323](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45026378323)
- 12개 원본 F2 PNG + 서버 로그 아티팩트: [원본 ZIP](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45026378323/artifacts/14755154139)
- **S02 의자** 고립·목재 테이블 동쪽·남쪽 3회 모두 `tucked=false`. 연구 원본 `true`는 유효한 원본 blockstate 속성이나 실제 배치에서 유지되지 않음.
- **S34 소파** 고립/북쪽/남쪽 3회 `single`, 동쪽 단독/동쪽 포함 L형 3회 `right`, 서쪽 단독/서쪽 포함 L형 3회 `left`. `inner_left` 재현 0회.
- 서버 로그를 진단 모드로 독립 재파싱해 실제 전체 속성값과 해시 12장, 연구 모델 경로를 재검증함.
- 실제 F2 비교판을 사람이 열어 가구/이웃 배치를 관찰했으나 형상 차이의 인과·UV 및 모드 의도·AI 권리는 확정하지 않음.
- **기존 70개 판정 유지: 조건부 37 / 보류 33 / 최종 승인 0, 역사 정확 F2 31/62.** 이 진단에 의한 보류 해제 0개.
- 다음: S02 실사용 플레이어 상호작용·책상 위치/방향, S34 이웃의 서로 다른 방향 조합과 실제 코너 구성/호환 블록 로직을 분리 검증.
