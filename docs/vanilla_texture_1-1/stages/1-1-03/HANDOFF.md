# 1-1-03 금속·금속부품 — 개별 채팅 인수인계

**현재 TEX03-R003 / 다음 후보 TEX03-R004 / 전역 v38 유지.** 2026-11-13.

## 우선 출처 정정

사용자가 직접 1.21.11 JAR을 압축 해제해 업로드한 [GitHub `1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)을 앞으로 **가장 먼저 직접 검사**할 것. 기존 비공식 `InventivetalentDev/minecraft-assets@1.21.11`는 **교차 검증** 출처다. 사용자 추출본과 미러가 동일해도 Mojang 공식 JAR SHA-1 인증은 아님.

## 누적 보존 실적

- R001 비공식 미러 PNG 16개 SHA256/CRC/RGBA 실측: 4,096픽셀 중 alpha0 321, alpha255 3,775, 부분 알파 0.
- R002 비공식 미러 PNG/정적 모델의 UV를 결합한 **145 모델 템플릿 면** 알파 측정; 투명 샘플 포함 면 **20개**, Heavy Core/모루 상면은 원본 투명 픽셀을 모델 UV가 참조하지 않음.
- **R003 신규 출처:** 사용자 제공 폴더의 PNG **16개** 실제 바이트 SHA256·CRC, blockstate **14개 JSON(63 정적 상태)**, leaf 모델 23 + 부모 모델 16 = **모델 39개 JSON** 실제 재취득·파싱. 총 **69개 고유 파일의 Git Blob SHA-1이 미러와 모두 일치**하고 PNG 16개는 독립 SHA256도 일치. R001 픽셀 및 R002 UV **신규 측정 0건**, 기존 데이터 중복 집계하지 않음.
- 추출본 내부 `version.json` id 1.21.11 확인. 외부 Mojang 인증 기록으로 취급 금지.

## 4가지 검증의 분리

1. **사용자 제공 추출본 검증: 69개 직접 확인** (PNG 16, blockstates 14, models 39)
2. **기존 비공식 미러와 교차 검증: 69/69 Git SHA1 동일** (PNG 16/16 직접 SHA256 동일)
3. **Mojang 공식 client.jar SHA1과 버전 메타데이터 인증: 미완료, 0/16**
4. **마인크래프트 인게임 정적 렌더 검증: 미완료, 0/16**

## 최신 불변 근거

- [R003 REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R003/REPORT.md)
- [R003 PNG 16개 바이너리 검증 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R003/USER_PNG_BINARY_CROSSCHECK.csv)
- [R003 blockstate 14개 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R003/USER_BLOCKSTATE_CROSSCHECK.csv)
- [R003 모델 JSON 39개 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R003/USER_MODEL_JSON_CROSSCHECK.csv)
- [R003 네 가지 검증 분리 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R003/VERIFICATION_TRACKS.json)
- 이전 R001/R002 보고서/CSV/JSON은 **수정 금지**. 전체 공통 `v38` 그대로.

## 다음의 A~G와 엄격한 경계

GitHub 최신 `STATE.json`·`HANDOFF.md`·R003 보고서/HEAD부터 재검증한 후 **실제로 새 증거가 있을 때** R004 작성. 가능하면 원본 `client.jar` 자체와 Mojang 공식 metadata를 대조해 전체 JAR SHA1 인증. 인게임은 실제 정적인 화면 증거에만 근거. **애니메이션, 키프레임, 움직임 분석 보류. Project Zomboid 변환 및 실제 가구 3D 제작 금지.** 단계 `HANDOFF.md`와 `STATE.json`, 새 단계 릴리스 디렉토리 외 절대 쓰기 금지; 루트 파일과 다른 단계, 글로벌 v38 불변 유지.
