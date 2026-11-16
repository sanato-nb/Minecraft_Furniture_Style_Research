# 1-2-F Entry4 실제 조사 결과

- 시작 `main` `6706b611c790b33e7ad44fd30c658bdf0c1398b9`. 고정 P2 후반 494개, 첫 `mangrove_fence_post.json`, 마지막 `yellow_stained_glass_pane_side.json`. Entry1~3의 1,139개와 중복 없이 처리했다.
- 원본 모델 JSON 494/494의 본문·Git blob SHA와 부모 제공자를 확인했다. 일반 기하 494, E 예외 0. 적용 요소 1,067, 면 4,811로 C 선행 face와 일치한다. 요소의 from/to·회전과 bbox는 개별 원장에 보존했다. `EXACT_FULL_CUBE` 20, `MULTI_ELEMENT` 194, `THIN_ELEMENT` 63, `ZERO_THICKNESS` 46, `ROTATED_ELEMENT` 19로 중복 태그를 허용했다.
- 고유 원본 PNG 122종의 첫 프레임을 3장 접촉 시트에서 직접 확인했다. 454개 모델에 바인딩 PNG를 연결했고, 40개는 자체 적용 면에 바인딩된 PNG가 없어 외형 판단을 보류했다. 텍스처 미해결 슬롯 42건과 미바인딩 40건을 각각 원장에 남겼다. 시트로 판독할 수 없는 재질과 실제 렌더 결과는 확정하지 않았다.
- D blockstate 원문 선택은 직접 422모델, 미직접 72모델, 옵션 2,436건이다. variants/multipart 조건, 대안과 x/y/uvlock/weight 키 존재·값을 보존했다. 등록 가능한 게임 상태 전체와 렌더는 검증하지 않았다.
- 대표 구조와 시각 외형의 분담은 `VANILLA_GEOMETRY_ARCHETYPES.md`에 정리했다. 가구 이전은 설계 후보로 표시하고 모델 이름을 기능 확정 근거로 쓰지 않았다.
- 독립 감사에서 494개 경로/SHA, 부모 제공자, 요소 좌표·회전·면·bbox, C 면수, PNG 링크/SHA, D 원문의 조건·옵션·flag 및 SHA를 재계산해 불일치 0. A/B/C/D/E 및 v69 파일 변경 0.

Entry4 소스 스타일 조사 **494/494**. F 누적 **1,633/2,390 (68.33%)**, 잔여 **757**. F 전체와 상위 1-2는 미완료. 다음 고정 Entry5는 P3 전반 379개, 첫 `acacia_leaves.json`이다. 공식 JAR 인증·실게임 렌더·PZ 변환은 수행하지 않았다.
