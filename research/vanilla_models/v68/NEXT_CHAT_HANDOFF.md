# v68 → 다음 채팅 1-2-A 인수인계

**최초:** GitHub main HEAD를 먼저 조회. v68 `SUMMARY.json`, `REPORT.md`, `07_P1_544_EVIDENCE_LEDGER.csv`, `VALIDATION_POST_RESEARCH_COMMIT.json` 직접 읽기; v69+ 발견 시 최신 버전 적용.

v68 실제 원본: 촛불 점등4 leaf의 1.21.11 원본 JSON 경로 SHA와 v67 템플릿4 재조회 + 원본 blockstates/candle 8 variants 정적 대조. lit4 leaf own elements0, 상속 요소 인스턴스30, source 적용 face100, 원본 명시 UV100. v67 unlit4 각 동일 부모 template, 텍스처 `candle_lit.png` vs `candle.png`만 소스상 차이. 원본 PNG2 SHA·16×16 IHDR 직접 확인, 새 RGBA 픽셀 복호화0. 점등의 인게임 밝기/particle/불꽃 동작 미인증. 신규 모델 신원0·고유 원본 JSON direct flags0.

v67 geometry0 5모델 (decorated_pot, ender_chest, oak_hanging_sign, shulker_box, white_shulker_box): **1.21.11로 표기된 2차 비공식 디컴파일 Java** `H1lkaaaGD/Minecraft_1.21.11_Source` source7파일 실제 조회·SHA 확인(조사 당시 main `fb136698ca0ae1f6e6e5a1b0c964740fb2f6dd18`). `BlockEntityRenderers`의 world BE class 등록4 unique, `SpecialModelRenderers`의 item mappings와 renderer class detail 메서드 교차 확인5모델. decorated_pot → DecoratedPotRenderer; ender_chest → ChestRenderer; oak_hanging_sign → HangingSignRenderer; shulker variants 2 → ShulkerBoxRenderer. source geometry hints recorded, **official client.jar 바이너리/세계 렌더 출력 테스트 아님**. Original model JSON 0 elements는 '안 보인다'는 확정이 아님.

파일: `00_CANDLE_4_LIT_LEAF_4_TEMPLATE_1_BLOCKSTATE_SOURCE.json`, `00_CANDLE_LIT_4_PARENT_100_FACE_AND_8_STATE_PROOF.json`, `00_SECONDARY_RENDERER_5_CODE_EVIDENCE.json`, `01_ORIGINAL_CANDLE_EIGHT_STATES.csv`, `02_ORIGINAL_LIT_CANDLE_SOURCE_FACE_100.csv`, `03_ORIGINAL_CANDLE_PNG_TWO_SHA_IHDR.json`; P1 원장 544×379, old v67 365×544 = **198560 모든 셀 원값 보존**, source-review 544×64 old56×544 = **30464 모두 동일**. 직접 모델 JSON 조회544/544 누적 유지, 1-2-A/1-2 완료 아님.

**다음 실제 연구:** P1 전체 자체/부모 effective geometry·texture slot·UV 누락 및 blockstate 연결의 미해결 모델을 원장으로 찾아 별도 신규 소스 검증; 게임 엔진 공식 암시 UV/renderer geometry가 필요한 예외 계속 추적. 2차 Java를 원본 공식 리소스와 혼합하거나 완전한 런타임 인증이라고 주장 금지. 기존 v1~v68 파일 원장 삭제/덮어쓰기 금지; source SHA identity는 asset_type+path+sha 복합키. prior 49 PNG 전체 반복 검수 금지. 1-1 승인 150/150, 상위 1/5 완료, 1-2-A 진척률 미산정, 제작/변환 아직 시작하지 않기. Commit fresh HEAD lease → remote readback old-cells → separate validation commit.
