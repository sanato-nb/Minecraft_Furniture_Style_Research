# Minecraft Java 1.21.11 — 1-2-G 6개 Entry 독립 종료 감사

**사용자가 추출한 원본** 4,669개 파일 재개방·SHA 및 선행 B~F 원장 교차. 공식 JAR·게임 runtime 인증은 범위 밖.
**원본 통합 감사: G1~G5 정적 전제 PASS, G6 GitHub 원격 readback 별도 진행**

## 총괄
- raw_assets: 4669
- by_type: {'BLOCK_MODEL_JSON': 2390, 'BLOCKSTATE_JSON': 1168, 'BLOCK_TEXTURE_PNG': 1111}
- model_elements: 5689
- faces: 23090
- C_uv_explicit: 18808
- C_uv_implicit: 4282
- C_faces_PNG_bound: 21590
- C_face_template_unbound: 1500
- D_rules: 7592
- D_syntactic_state_cases: 9193
- D_model_option_applications: 19440
- E_special: 86
- PNG_C_prior_matches: 1073
- PNG_outside_C: 38
- mcmeta_sidecars: 99
- F3_PNG: 332
- G_entries_accepted: 6
- F_prior_parent_sha_gaps: 4
- source_errors: 0

## 종료 게이트

- G1: PASS
- G2: PASS
- G3: PASS
- G4: PASS
- G5: PASS
- G6: PENDING_REMOTE_FINAL_READBACK

## 원본 누락·예외 설명
- F6의 sculk_mirrored·stone_mirrored 2모델의 F 선행 cube_mirrored 부모 SHA·provider SHA 4필드가 비어 있었음; G 원본 직접 재검증으로 보완하되 F 원본을 변경하거나 F 과거 소스로 소급 인정하지 않음.
- E86의 실제 renderer는 범위 밖 미인증. 템플릿 face 미바인딩1500, 모델 PNG 불명38, C 바깥 PNG38, D 미직접254는 서로 다른 분모.
- F3 332개는 첫 프레임 화면 확인, 애니메이션 전체 재생 아님.
- 1-2 전체 종료는 G 종료와 별도 단계에서 심사. A~F/v69 원본 수정 금지.

## 오류 목록
