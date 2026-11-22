# INT-4-F3 — 원본 모드 7개 실게임 F2 직접 검수 및 70개 판정 재정합

- 실제 Fabric Minecraft 1.21.1 CI 실행: S20/S21/S26/S27/S44/S45/S46 **7개 모두 원본 서버 블록 상태·선택 모델·원본 F2 PNG SHA 검수 성공**.
- 새 네이티브 F2 원본 이미지: 7발생/고유해시 6; GIF/합성 이미지가 아닌 원본 1024×684 F2를 직접 육안 확인.
- 연구 원본 1-5-B의 30요소·144면 일치. 기존 역사 자료는 수정하지 않음.
- **중요 반례:** S20 \`open=false\` / S21 \`open=true\` 서로 다른 모델 키와 서버 상태를 갖지만 두 실제 F2는 PNG SHA까지 완전히 동일함. '서랍 열림 외형 입증'으로 승격하지 않음.
- AF 6건은 연구 Git 4.0.3과 실제 실행 JAR 4.0.2의 원본 JSON 바이트가 다르며 선택 규칙만 맞음. HC S27은 연구/릴리스 state/model/provider 바이트 동일.
- S44/S45 조명은 원본 F2 차이가 있지만 광원 인과·시간 변화·UV 검증 아님.
- 전체 고정 분모 70: 기존 조건부 25+신규 7=**조건부 32, HOLD 38, 최종 수용 0**. 역사 사례 F2 26/62, 나머지 36 미매핑.
- HOLD 38: 바닐라 15, AF 7, HC 4, Macaw 10, 위험 R06/R08 2.
- 원본 캡처 ZIP/PNG는 Actions 보관기한 제한. Git에는 source SHA·사진 관찰·조건부 검증 기록만 커밋.
- INT-4-F 전체 종료 및 INT-4-G/H 최종 승인 **보류**. INT-5 의미/INT-6 권리 승인 **0 유지**.

## 산출 파일
- \`INT4_F3_70_TARGET_EVIDENCE_DISPOSITIONS_V3.csv\` : 수정 사례 7개 외 기존 증거 원장 그대로
- \`INT4_F3_38_PENDING_EXACT_F2_CASES_V1.csv\` : 남은 보류 사례·우선순위
- \`INT4_F3_3_RENDER_SOURCE_EXCEPTIONS_V1.csv\` : 동일 이미지, AF 릴리스 차이, 조명 인과 미확정
- \`INT4_F3_7_DIRECT_IMAGE_VISUAL_AUDIT_V1.json\` : 원본 상태별 해시·그림 관찰·수용 제한
- \`INT4_F3_SOURCE_REPORT_V1.md\` : 경계 보고
