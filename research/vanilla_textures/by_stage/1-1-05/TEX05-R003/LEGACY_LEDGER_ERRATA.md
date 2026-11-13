# TEX05-R003 — 불변 원장 정정 이력

R001과 R002의 원본 보고서·CSV·JSON은 **수정하거나 삭제하지 않는다**. 사용자 제공 1.21.11 파일을 직접 읽는 과정에서 R001 CSV의 유효 길이가 아닌 Git blob 지문 1건을 발견했다.

- **원본 원장**: `research/vanilla_textures/by_stage/1-1-05/TEX05-R001/SOURCE_LEDGER.csv`
- **행**: `1-1-05-005,green_stained_glass`
- **컬럼**: `blockstate_git_blob_sha`
- **기존 CSV 문자열**(39자리): `ca4fec4067cffd89000ee64251f878bf0d530a8`
- **직접 읽은 사용자 추출본 Git blob**(40자리): `ca4fec4067cffd89000ee64251f878bf0d530a8a`
- **동일 경로의 실제 외부 미러 Git blob**(40자리): `ca4fec4067cffd89000ee64251f878bf0d530a8a`
- **검증한 경로**: `1.21.11/assets/minecraft/blockstates/green_stained_glass.json`.
- **원인 분류**: R001의 `SOURCE_LEDGER.csv` 필드에서 마지막 문자 `a` 누락. 현재 사용자 원본·미러의 **실제 파일 불일치가 아니다.**
- **영향**: R001에 기록된 6 PNG SHA-256·픽셀·모델 결론 및 R002 경계 측정은 그대로. Git blob SHA로 자동 대조할 때는 R003 `SOURCE_LEDGER.csv`의 40자리 SHA 사용.
- **범위 검사**: R001 `SOURCE_LEDGER.csv` 전체 6행에서 SHA-256 및 Git blob SHA 컬럼의 유효 자리수 검사 결과, 그 외 길이 오류는 발견되지 않았다.

이 정정은 공식 `client.jar` SHA-1 인증 또는 인게임 검증을 증명하지 않는다.
