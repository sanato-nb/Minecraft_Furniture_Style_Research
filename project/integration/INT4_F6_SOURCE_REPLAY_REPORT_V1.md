# INT-4-F6 실제 Fabric 소스 조건 기반 원본 특수 상태 재현

- Minecraft 1.21.1 Fabric 실제 실행 원본 F2 10장, 1024x684, PNG 10개 고유 SHA 및 client.log 독립 검증.
- S02: 북쪽 앞 참나무 테이블과 위쪽 반 블록 배치에서 tucked=true 유지 각 1회. 동쪽 대조와 전방 받침 제거 시 tucked=false.
- S34: 북쪽 이웃 소파 facing=west일 때 shape=inner_left 정확 유지. east/남쪽/차단 이웃 대조는 다른 shape로 판독.
- 사용한 원본 Java 코드: AnotherFurniture ChairBlock/TuckableBlock, Handcrafted ModularSeatBlock 고정 Git SHA. 코드 기대 결과와 게임 서버 결과를 구분해 검증.
- 최초 게임 실행의 실패 상태는 실제 촬영 후 감사 프로그램의 sorted-JSON-key-order 검증 오류. 원본 게임 로그와 PNG를 별도로 재파싱하여 증거만 수용.
- 70 대상 37조건부/33HOLD -> 39조건부/31HOLD, 최종 승인 0. 원본 역사 F2 31/62 -> 33/62.
- 미해결 31: 바닐라15, AF3, HC1, Macaw10, 위험R06/R08 2.
- 실제 플레이어 상호작용, 픽셀 UV 인과, 부품 의미, AI 원본 이용권 및 INT4-G/H 최종 승인은 아직 보류.
