# 1-1-01 목재·원목 전용 인수인계 — TEX01-R003

**현재 TEX01-R003 · 다음 TEX01-R004 · 전체 v38 유지.** R001/R002 파일과 커밋 불변, 고정 범위 18 PNG.

## 최우선 출처 원칙
GitHub `1.21.11/`은 사용자가 **직접 Minecraft Java 1.21.11 client.jar을 압축 해제해 업로드한 사용자 제공 추출본**임을 확인해 주었다. 이 폴더를 원본 소스로 우선 활용. R001에서 이 폴더 PNG 18개 바이트/정적 JSON 43개 직접 검증했음. 이전 미러/추출본 혼재 표기를 R003 보고서에서 정정하되 과거 결과 소급 변경 없음. **사용자 추출본 유래와 Mojang 공식 client.jar SHA1 인증은 절대 동일하지 않음.**

| 검증 계층 | 결과 |
|---|---|
| 사용자 제공 추출본 | R001 실제 PNG SHA·CRC·RGBA 18/18, JSON 43개·모델 로컬면 150. R003 현재 Git blob·크기·PNG IHDR 18/18 재확인. indexed palette 4비트 4개, 8비트 14개. |
| 이전 미러 | 과거 v4 기록 SHA와 R001 PNG SHA 18/18 일치, 별도 미러 바이너리 직접 비교 0 |
| Mojang 원본 공식 JAR | 0/18. 전체 JAR SHA1·size 공식 메타데이터 대조 없음 |
| 인게임 정적 렌더 | 0/18. 실제 엔진 UV·컬링·조명 미확인 |

새 원본 `version.json`에서 id 1.21.11, `atlases/blocks.json`에서 `block/` 정적 아틀라스 디렉터리 선언 검증. **이 메타 JSON 2개를 모델 JSON 43개에 합산하지 않음.** 기존 R002의 72 조건은 가상 인접 회전 실험일 뿐 인게임 배치 규칙이 아님.

[R003 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R003/REPORT.md) · [R003 SOURCE_LEDGER](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R003/SOURCE_LEDGER.csv) · [R003 EXTRACT_METADATA](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R003/EXTRACT_METADATA.json) · [R003 SUMMARY](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R003/SUMMARY.json).

[R001 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/REPORT.md) · [R002 REPORT](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R002/REPORT.md).

다음 작업 `TEX01-R004` 전 STATE.json SHA·current/next revision·main HEAD와 R004 경로 미존재 확인. 실제 신규 근거만 전용 새 폴더. Mojang client JAR 전체 해시/공식 메타데이터 직접 확인 이전 공식 0/18 유지, 실제 게임 장면 없으면 인게임 0/18. 다른 재질 단계, 루트 HANDOFF.md·PROGRESS.md·handoff/STATE.json, v38 수정 금지. 애니메이션·PZ 변환·가구 3D 제작 보류.
