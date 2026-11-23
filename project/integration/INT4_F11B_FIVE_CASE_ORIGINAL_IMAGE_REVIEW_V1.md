# INT-4-F11B 원본 바닐라 멀티파트 5개 F2 실제 게임 검증 및 독립 감사

- 실제 Minecraft 1.21.11 촬영 Actions: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45098021558
- 원본 아티팩트 ZIP 14784297231 SHA256 14483549b057734fe124c36dc498bdb8a91f781016189707feeb9c9d27e50a9a. 네이티브 F2 5장과 client.log 직접 열어 검증.
- 역사 원본 5개 사례/동시 선택 모델 12개/13요소/45면. V03 울타리 2모델, V08 조각된 책장 7모델 포함.
- 실제 서버 상태 V03 north=true, V04 powered=false, V06 open=true, V08 첫 슬롯 occupied=true, V09 white wool 5/5 PASS.
- V09 흰색 픽셀 관찰 별도 검증. V06 열린 통 상태는 GUI 기능 승인과 구별.
- 고정 70개 조건부 58→63, HOLD 12→7. 원본 역사 연구 F2 연결 52/62→57/62. 최종 무조건 승인 0.
- 남은 대상 V11~V15, R06, R08. UV 인과·자연 상태 전이·기능·부품 의미·AI 학습/재배포권은 별도 보류.
