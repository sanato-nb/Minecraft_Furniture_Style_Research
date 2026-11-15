# v67 미해결 및 증거 경계

- **V67-I01 엔진 렌더/특수 renderer 실물 미확인:** decorated_pot, ender_chest, oak_hanging_sign, shulker_box, white_shulker_box 소스 leaf+상속 요소0, blockstate 대상 참조 확인. 이 중 어떤 엔진 렌더 클래스가 실제 기하를 내는지는 client runtime/source code 검증 없으므로 **확정 불가**. Minecraft 화면에 객체 없음이라고 해석 금지.
- **V67-I02 암시 UV 후보6면:** cartography_table 원본 부모 cube 6 face의 UV-key absent. 계산후보 [0,0,16,16] 여섯 면, source explicit UV가 아님. 엔진 공식 인증0. 과거 v33 148개 계산후보 별도 유지.
- **V67-I03 PNG Git SHA/IHDR ≠ 픽셀 RGBA:** 9개 원본 PNG 16×16 경로 SHA/IHDR 확인. 전체 RGBA pixel decode 및 Pillow 독립 교차0, UV face pixel sampling0. 과거 v56 candle 49코호트 증거를 중복 신규 성과로 계산하지 않음.
- **V67-I04 blockstate 원본 target refs23 ≠ 화면 렌더 면23개:** candle lit=true 4 상태 모델은 이번 13 원형 leaf 선택에 포함되지 않아 별도 후속 연구. powered rods12 참조의 모델 x/y 원본 규칙을 기록했으나 렌더 출력 UVLOCK·회전 인증 없음.
- **V67-I05 모델 leaf/face 인스턴스와 고유 원본 선언 구분:** candle template 1→4는 소스 적용 face refs 합100, rod 합22, torch6, cartography6 =134. 고유 원본 face 선언134 신규 개가 아님; 부모 재사용/leaf별 집계. zero thickness20, rotations20도 동일 인스턴스 집계.
- **V67-I06 완료 범위:** v66 source JSON 직접 read544/544 및 v67 selected13 원본 재조회 ≠ P1 544 모델 전부 원본 효과 기하/UV/Png/render 완료. 1-2-A 실제 완료율 미산정, 단계 미완료.
- **V67-I07 원본 SHA 식별 복합키:** v65 P1 모델 path544/unique SHA539, 중복2그룹7경로 기존대로. Asset type + full original path + blob SHA 필수.
- **V67-I08 이전 파일 보존:** v1~v66 연구 산출물 변경 금지. v67 only additive plus current status files.
