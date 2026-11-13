# 1-1-03 금속·금속부품 — 독립 채팅 인수인계

**최신 단계 릴리스: TEX03-R002. 다음 후보: TEX03-R003. 공통 프로젝트 전체 버전 v38 유지.** 2026-11-13.

## 정확한 대상 / 진행 기록

- 고정 대상: `STATE.json`의 Minecraft Java 1.21.11 금속 PNG **16개**뿐. 다른 1-1-xx 단계의 실적을 더하지 않는다.
- **TEX03-R001**: 비공식 추출 미러 PNG 16/16 독립 SHA256·PNG CRC·RGBA 4,096픽셀 확인. 알파0 321 / 255 3,775 / 부분알파 0. 정적 blockstate JSON 14개·부모 모델/UV 연결. R001 릴리스 자체는 불변.
- **TEX03-R002 (신규)**: 위 독립 PNG 데이터의 **진짜 알파 마스크**와 추출 미러 **13개 부모/직접 모델 JSON**에서 면별 UV를 다시 교차 측정해, 16개 텍스처를 사용하는 **145개 템플릿 모델 면**에 대해 픽셀 샘플 근거 확보. 이 중 **20개 면**에서 투명 픽셀을 샘플. 이는 고유 텍스처 개수·상태 변형 수·게임 실제 노출 면적과는 다른 수량.
- 특히 `heavy_core` PNG의 **64개 투명픽셀**이 모델의 어느 면 UV에도 참조되지 않음(6면 중 투명 참조 0). `anvil_top` PNG의 **96개 투명픽셀**도 상면 UV [3,0,13,16]에서는 0개. `iron_trapdoor`는 넓은 판면만 alpha0=36/면이고 측면은 0. `iron_door_top`도 넓은 면 alpha0=48/면, 측면은 0.

## 최신 불변 결과

- [TEX03-R002 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R002/REPORT.md)
- [145개 UV 면별 알파 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R002/UV_ALPHA_FACE_CENSUS.csv)
- [16개 항목별 요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R002/UV_ALPHA_SUMMARY.json)
- [13개 모델 원본 SHA 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R002/SOURCE_MODEL_MANIFEST.json)
- [선행 TEX03-R001 결과](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-03/TEX03-R001)

## A–G 상태

- A/B/C: 16개 비공식 미러 PNG SHA/CRC/RGBA 실측 — R001 결과 보존.
- D1: 금속 팔레트 단계 — R001 소스 근거. D2: 모델 UV 기준 실제 알파 샘플 범위 145면 — R002 새 실측. D3: 정적 블록 상태별 텍스처 참조 — R001+R002.
- E: 16개 텍스처의 정적 모델·부모·UV·알파 교차 근거 — 미러 소스 수준 확대 완료.
- **F: 공식 1.21.11 client.jar 인증 0/16, 인게임 정적 검증 0/16; pending 유지.** 여기까지 미러 실측을 공식 인증과 혼동 금지.
- G: R002 전용 보고서·원장·상태/인수인계 갱신.

## 다음 채팅의 정확한 우선순위

1. GitHub의 최신 이 `STATE.json`/ `HANDOFF.md`를 다시 읽어 **TEX03-R003** 후보와 SHA를 검증. 동시 변경·존재하는 릴리스 폴더 덮어쓰기 금지.
2. **공식 Mojang 1.21.11 client.jar 원본 확보** 후 JAR을 공식 메타데이터와 검증하고, 내부 16개 PNG SHA/bytes 및 models/blockstates 재대조. 해당 원본을 확보하지 못하면 검증 0/16 유지.
3. 게임 내 원본 정적 배치/동일 상태 화면의 알파·UV·조명 비교만 수행. **애니메이션·프레임·키프레임·움직임 연구 전면 보류**. 기존 동적 기록 삭제하지 않음.
4. `TEX03-R001`, `TEX03-R002` 불변 릴리스 유지. 새 증거가 있어야만 R003 생성. 전역 `v38`, 루트 `HANDOFF.md`·`PROGRESS.md`·`handoff/STATE.json`, 다른 단계 모든 폴더 수정 금지.
