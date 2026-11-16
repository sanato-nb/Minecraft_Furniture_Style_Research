# 1-2-F Entry6 P3 후반 378모델 실제 원본 구조 조사·검산 보고

**기준 main `4f38439e52ae99c20ccab5fe70d293f7f09a5303` · 고정 Queue `F_ENTRY6_QUEUE_378.csv` · Minecraft Java 1.21.11 사용자 제공 추출 원본.**

## 실제 수행
- 모델 원본 JSON 본문과 Git blob SHA **378/378**, 원본 부모 상속·실제 `elements` 제공자 확인 **378/378**. 일반 기하 **371개**, E 소관 예외 **7개**를 별도 처리함.
- 실제 적용 요소 **661개**, face **2,412면**. C 원장과 면수 차이 0. 원본 UV 키·두께·bbox·회전 및 모델마다 기하 제공자·원본 SHA를 보존. C 기존 근거의 **PNG 연결 2,178면 + 미바인딩 234면 = 2,412면**. 이는 C 재참조이며 F에서 픽셀을 신규 검수했다는 뜻 아님.
- D 원본 모델 선택 옵션 **678행**: 원본 blockstate 경로/SHA, variant/multipart/조건 및 x·y·uvlock·weight 키 명시 여부를 기록. **직접 선택 모델334, 직접 미선택44**. 게임 상태 레지스트리 검증을 주장하지 않는다.
- `STYLE_OBSERVATIONS.csv` 378행, `F_GEOMETRY_FEATURES.csv` 378행, `F_GEOMETRY_ELEMENTS.csv` 661행, `F_TEXTURE_VISUAL_EVIDENCE.csv` 378행, `F_ASSEMBLY_LINKS.csv` 378행, `F_UNRESOLVED.csv` 423행 생성.
- **원본 PNG 시각 관찰 0종**. 연결된 PNG의 Git SHA·C RGBA 근거는 보존했으나, 실제 PNG 픽셀·첫 프레임을 확인하지 못해 재질·텍스처 디테일 대조는 미완료임. E 렌더링 미인증은 그대로 보존.
- 독립 파서로 원본 JSON을 다시 읽고 모델 경로/SHA·부모 계보·from/to·UV·두께·기하 요소·bbox·D 참조를 **168 + 210 = 378개** 재산정. 불일치 **0건**. 기존 Entry1~5의 2,012개와 Entry6 378개를 합친 **2,390개 고유 경로/SHA**, **P1 544/P2 1,039/P3 807**, **E86**, **D 직접 2,136**, 요소 **5,689**, face **23,090**, D 원본 옵션 **7,592** 대조 PASS.

## 판정
- Entry6 **원본·구조 판독 378/378**, 독립 수치 검산 PASS.
- Entry6 **PNG 시각·스타일 검증 0/378**. 기존 승인 Entry1~5의 **F 스타일 완료 2,012/2,390 (84.18%) 유지**, 별도 **전체 F 원본·기하 판독 2,390/2,390 (100%)**. 서로 다른 지표를 혼동하지 않는다.
- `F1`(모집단/원본 SHA) PASS, `F2`(정적 기하) PASS, `F3`(**실제 PNG 시각 근거 부족**) BLOCKED, `F4`(D 원문 조립 연결 및 E 예외 구분) PASS, `F5`(독립 검산) SOURCE_AUDIT_PASS / REMOTE_READBACK 별도 기록 예정.
- 따라서 **`F_COMPLETE_SOURCE_STYLE_TAXONOMY_SCOPE` 선언 불가**. 종료 계약에 따라 `F_BLOCKED_AT_ENTRY6_F3_VISUAL_PENDING`로 기록한다. **Entry7 자동 생성 금지**, 상위 1-2-G 및 전체 1-2도 미완료.

## 대표 기하 원형
`mud.json` 1요소·6면 16³ 정적 큐브; `mushroom_block_inside.json` 1요소·1면 0두께 판; `nether_sprouts.json` 2요소·4면 교차 회전 평면; `template_three_candles.json` 9요소·30면 작은 다중 입체. 구체 출처·SHA·한계는 [VANILLA_GEOMETRY_ARCHETYPES.md](VANILLA_GEOMETRY_ARCHETYPES.md)에 기록. 원본의 구조적 성격이 가구의 시각적/기능적 동일성이나 실제 엔진 렌더링을 증명하지는 않는다.

## 자료 보존·인계
원본 JSON snapshot 24개와 부모 51개·C/D 연결의 기계 판독 원장을 `source_snapshots/`와 `F_ENTRY6_ANALYSIS_CONTEXT.json`에 보존하여 독립 재생 가능하게 한다. A/B/C/D/E·v69 기존 원본 수정하지 않는다. 현재 수행하지 않은 PNG 실감 검수와 F3 종료 판단은 [F_NEXT.md](F_NEXT.md)로 인수인계한다. 모든 GitHub 원격 결과는 커밋 후 별도로 재조회해야 한다.
