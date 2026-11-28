# 7-G 3차 보완 — 합성 원본과 DB 기록 대조

T05~T08에 실제 생성한 합성 JSON/PNG 원본의 SHA 및 저장값 비교를 추가했다. fixture_oracle.py는 제한된 모델 상속/요소/면/JSON pointer, RGBA8 필터0 PNG와 프레임 픽셀 SHA, 단순 multipart 조건과 적용 옵션, 렌더 크기 확인용이다. 일반 Minecraft 파서/UV 오라클/실제 렌더 정확성은 아니다. T05는 고정 합성 설계 시험에 한해 PASS 후보이며 T06~T08은 남은 제한을 명시한다. T04에는 REPLACE 우회 차단 및 완료된 시도 append 차단을 추가했다. 기존 16개 분모/19개 입력과 운영 DB는 변경하지 않는다. 실제 CI 전 통과 금지.
