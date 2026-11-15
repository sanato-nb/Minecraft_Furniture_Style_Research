# v69 → 다음 채팅 1-2-A 인수인계

처음에는 **실시간 GitHub main HEAD** 읽기. v69 `SUMMARY.json`, `REPORT.md`, `07_P1_544_EVIDENCE_LEDGER.csv`, `VALIDATION_POST_RESEARCH_COMMIT.json` 확인하고 최신이 v70+라면 최신을 이어받기.

v69 실제 원본 새 검증:
- `1.21.11/assets/minecraft/models/block/brewing_stand{,_bottle0..2,_empty0..2}.json` **7개 P1 모델 실물 JSON/SHA 재조회**, `blockstates/brewing_stand.json` 1개 SHA/내용 조회. v66 source JSON 판독 이력이 있던 6개 bottle/empty 모델의 원본 JSON/sha **6/6 일치**. 새로운 고유 P1 모델 신원0, 누적 직접 원본 JSON 544/544 유지.
- 원본 multipart 7 rule (unconditional body1, each of 3 slots bottle true or empty false), **8개 boolean 조합을 원본 when 객체로 전수 평가**: 모든 상태에서 4모델(본체1+각 자리3), 요소7개·source face refs30개·0두께 평면3개·rotated elements2개. 8조합 적용면 합 **240은 상태별 참조 인스턴스**; 원본 선언 face는 7모델 **36개 모두 명시 UV**. 실제 엔진 계산 UV/출력 메시 인증 아님.
- 병/빈 pair3개는 같은 자리 `from/to`와 `rotation` 같고 원본 `uv`만 다름. slot0 회전 없음, slot1 y -45°, slot2 y +45°. 원본 0두께 양면 plane6개. body4 요소24 face, 6 optional leaf 각 1요소2 face.
- source texture `brewing_stand.png`, `brewing_stand_base.png` Git blob SHA + PNG IHDR **16×16/8-bit/color-type3 palette indexed** 확인. **새 실제 RGBA 픽셀 복호화0**, 렌더 화면/전용 모드 제작0.
- 증거: `00_ORIGINAL_BREWING_7_MODELS_1_BLOCKSTATE.json`, `00_BREWING_7_MODELS_8_STATE_240FACE_PROOF.json`, `01_BREWING_SOURCE_36_DECLARED_FACES.csv`, `02_BREWING_8_EXHAUSTIVE_MULTIPART_STATES.csv`, `03_BREWING_240_STATE_APPLIED_FACE_REFERENCES.csv`, `00_BREWING_TWO_PNG_ORIGINAL_SHA_IHDR.json`.
- P1 544행×393열, v68 이전 **206,176 데이터셀 전부 보존**. source review 544행×70열, 기존 **34,816셀 전부 보존**. 모든 원장/기존 1-2 A 판정과 상태 보존. 과거 v31 양조기 본체 소스연구, v66 bottle6 직접 모델 JSON 조회와 **중복 실적 합산 금지**.
- 다음 다른 상태/가구 **독립 모델 패밀리** 원본 JSON + 실제 multipart/variants + UV 슬롯 + PNG SHA/헤더 체크 (예: 1-2-A의 미검수 상태 표본), 조립·UVLOCK의 Minecraft 실제 렌더 공식을 입증하려면 별도 공식 엔진/바이너리 증거를 확보. 지난 49 PNG 재검수 피하고 source explicit UV vs derived 후보 vs real texel 구분. 기존 v68 비공식 Java 2차 렌더러 코드 인증을 공식 클라이언트로 승격하지 말기.
- **1-1 승인150/150, 상위5단계 중1 완료, 1-2-A/1-2 미완료, 실질완료율 null, Minecraft 가구 제작·Project Zomboid 변환 아직 없음**.
- 작업 지속: 이전 v1~v69 파일 수정 삭제 금지, 최신 HEAD 확인/expected SHA lease commit → GitHub 원격 원본 readback·old-cell 보존 검증 → 별도 validation commit/최종 HEAD 체크.
