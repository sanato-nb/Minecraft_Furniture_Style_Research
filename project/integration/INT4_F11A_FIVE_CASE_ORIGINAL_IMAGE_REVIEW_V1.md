# INT-4-F11A 바닐라 1.21.11 5개 사례 실제 F2 독립 감사

- 공식 Minecraft 1.21.11 실제 게임 Actions #45095295065 성공. 아티팩트 #14783186548에 원본 F2 5개·client.log 보관.
- V01 계단(2요소·11면), V02 하단 반 블록, V05 닫힌 통, V07 책장, V10 참나무 판자(각 1요소·6면). 총 5역사 사례/6요소/35면.
- 원본 selected leaf/parent/source state Git blob SHA1, 공식 클라이언트 SHA256/1, 서버 상태, PNG 및 로그 원본 해시 모두 검증.
- V05: barrel → cube_bottom_top → cube. V07: bookshelf → cube_column → cube. V10: oak_planks → cube_all → cube. 직접 부모와 기하 제공자 구분.
- 실제 PNG 다섯 장을 재열람해 계단 단차·반 블록 얇은 두께·통의 고리·책장 책·나무 판자 큐브를 확인함.
- 고정 F70 조건부 53→58/70, HOLD 17→12/70. 역사 원본 사례 조건부 F2 47→52/62. 최종 무조건 승인 0.
- 남은 V03 V04 V06 V08 V09 V11 V12 V13 V14 V15 및 R06 R08은 별도. 기능/UV/의미/AI 이용권 최종 승인 없음.
