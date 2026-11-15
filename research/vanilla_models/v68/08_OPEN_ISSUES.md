# v68 증거 경계·미해결 사항

- 2차 Java source는 비공식 1.21.11 디컴파일. world BE type 4 / original P1 model5와의 대응, item special mapping, 메서드 레이어 참고만 검증; **공식 client.jar SHA / 실제 render mesh·동작·UV·텍스처 인증 없음**.
- lit candle4 face refs100은 템플릿 재사용의 leaf 적용 참조이며 새로운 고유 원본 면100개 아님. v67 unlit4의100 적용면과 신규 고유 model/geometry 실적 중복 처리 금지.
- candle PNG2 SHA/IHDR 확인은 원본 RGBA texel 새 측정 아님. lit true → 실제 광량/화염/particle을 모델 JSON만으로 인증 금지.
- P1 직접 원본 JSON 조회544/544는 '모든 P1 효과 기하/UV/특수 렌더 전체 완료'가 아님. 1-2-A 완료율 계산/완료 선언 보류.
- SHA 중복 model paths 544, distinct blob539 (2 groups 7 paths) 기존 key 경고 유지: asset_type + path + SHA.
