# 1-1-11 — 목재·구조부품 별도 채팅 인수인계

## 최신: TEX11-R013 — 애니메이션 보류 해제 및 원본 31 PNG 애니메이션 에셋 조사 완료 (2026-11-13)

- **현재 R013, 다음 R014는 명시적 독립 신규 목표가 있을 때만.** 사용자가 보류된 애니메이션 연구 재개를 요청했다. `animation_study_deferred=false`. **인게임 검증 제외·공식 JAR SHA-1 제외는 유지**.
- **실측:** 고정 31 PNG 전부 원본 바이트 CRC 통과, 26개16×16+5개32×32. APNG 프레임 표시 chunk 없음, 대응 `.png.mcmeta` **0/31**. 같은 Minecraft 블록 텍스처 디렉터리에는 다른 대상 `.png.mcmeta` 99개가 있어 absence 검사 의미 있음.
- **원본 JSON 166개**(blockstate24, model leaf122, template20) Git tree blob SHA 전부 일치. 애니메이션 frame/timing/easing 관련 JSON 키 0.
- **이산 상태 비교:** 문7종 open 112쌍, 다락문12종 open96쌍, 선반5종 powered80쌍 = **핵심 정적 끝점 288쌍**. 선반 side_chain 조합240쌍 추가하여 **528 원본 상태 변화 후보**(모델 선택 실제 변경408, 불변120=unpowered shelf). 임의 side_chain 조합은 게임 내 직접 발생 보장이 없는 수학적 후보.
- **기하/UV:** 문112쌍 local element bounds 유지, 정적 Y회전/UV변화. 다락문96쌍 수평↔수직 geometry 바뀜, source Xrotation변화40, Yrotation변화52. 선반 powered80쌍 본체/전면 형상과 각도 불변, 전면 UV선택 변화80. **실제 시간 프레임·부드러운 회전·hinge pivot·duration·easing은 원본 PNG/JSON만으로 나오지 않는다**. 게임 엔진 실행·모션 클립 제작 없음.
- **근거:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R013/ — REPORT, SUMMARY, 6개의 CSV(31PNG,166JSON,528전환,4그룹,288끝점,3그룹), SOURCE_STATIC_ENDPOINT_EXAMPLES, REPRODUCIBILITY.
- **1-1-11 source-only 완료 31/31** 유지. R009–R011의 596모델-면 RGBA patch/68,960 참조는 역사적 근거로 유지(이번 R013 신규 pix 수 아님). 과거 source 544상태+v38 oak_shelf32=576이라는 의미도 구분한다. 이전 릴리스/전역 v38/다른 단계 불변.
- **연속작업 규칙:** 사용자 `계속해줘`만이면 고정 31개 PNG의 소스 기반 텍스처/정적 상태/애니메이션 원본 연구가 끝났음을 알리고 멈춘다. 실제 부드러운 개폐 **애니메이션을 별도 제작**하려면 새 작업 범위를 정해야 하며, 그때 재생시간·pivot·easing은 Minecraft 원본 인증값이라고 하지 않는다. 사용자 인게임 스크린샷은 **요구하지 않음**.

---

## 최신 범위 변경: TEX11-R012 — 인게임 검증 제외·소스 기반 31/31 완료 (2026-11-13)

- **현재 `TEX11-R012` / 다음 `TEX11-R013`은 새로운 독립 과제·원본·확장 범위가 있을 때만.** 사용자가 명시적으로 **“인게임 검증은 제외해줘 어차피 모델링이랑 텍스텨있는데 필요없을거같아”**라고 요청했으므로 Minecraft 게임 화면/스크린샷/실제 GPU 컬링·조명 테스트를 **단계 1-1-11 필수 완료 조건에서 제외**했다. 사용자가 `계속해줘`만 말해도 스크린샷을 요구하지 않는다.
- **R012는 관리자 범위 변경 전용이며 새로운 PNG·JSON 원본 측정 0건.** 단계 고정 31 PNG의 원본 바이너리 검증·CRC/색상/RGBA·전체 모델 면 UV·블록상태 정적 근거는 이전 R001–R011 기록 그대로 계승한다.
- **새 source-only 완료 정의는 31/31개**: R009 다락문12 PNG/216면/25,344 UV 참조 + R010 선반5 PNG/100면/6,880 참조 + R011 문14 PNG/280면/36,736참조 = 고정 **31 PNG /596개 모델·면 전체 RGBA UV 패치/68,960 소스 텍셀 참조**. 여기서 면과 텍셀 참조는 렌더링도, 추가 고유 PNG도 아니다. 각 31 item에서 원본 추출·CRC와 모델 면 연구 완료 플래그를 확인했다.
- **기존 `ingame_static_render_verified_count=0` 및 개별 item의 `ingame_static_render_verified=false`는 사실대로 유지.** 이제 **미완료 장애물/완료 분모에 포함되지 않음**. 실제 게임 검증을 성공한 것으로 주장하면 안 된다. 정적 PNG와 모델 JSON만으로 실제 화면 품질·조명·GPU 동작을 확인한 것은 아님.
- **공식 Mojang client.jar SHA-1 원본 인증은 R005부터 이미 사용자 결정으로 필수 범위 제외**. 역사적 v38 oak_shelf 32상태, leaf127·rule512·544상태·672인스턴스·4,320회전면 등 수치 불변. 프로젝트 전체 완성도 `null` 유지.
- 증거: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R012/ (`SCOPE_CHANGE.md`, `SUMMARY.json`). R000–R011 연구 불변이며 루트 v38·다른 단계 변경 없음. 애니메이션 연구 유예, 좀보이드 변환·실제 가구 3D 모델링 제한 유지.
- **중단 규칙:** 다음 `계속해줘` 요청 시 소스 기반 고정 단계가 완료되었다고 안내하고 멈춘다. **인게임 자료는 필요하지 않다.** 새로운 과제·새 원본·다른 단계/연구 범위에 대한 사용자 지시가 있을 때만 새 리비전을 시작한다. 과거 인수인계 중 “실게임 스크린샷 필요”라는 문구는 R011 당시 기준을 설명하는 역사적 기록이며 **R012 이후 적용되지 않음**.

---

## 최신 연구: TEX11-R011 — 문 7종 모든 면 RGBA/UV 완료, 31 PNG 소스 면 분석 완료 (2026-11-13)

- **현재 `TEX11-R011` / 다음 `TEX11-R012`은 사용자 실게임 증거 등 독립 신규 근거가 생길 때만.** 사용자 제공 `1.21.11/` 원본 **문 위/아래 PNG14개 직접 CRC·디코딩 14/14**, 문 leaf JSON56·template JSON8·blockstate JSON7 직접 조회/검증. 56모델×5면=**280 전체 UV source RGBA 실화소 패치/36,736 참조**, 그중 **168 얇은 면 신규 패치/8,064 참조**, 넓은 면 전체 처음 정밀 샘플 112패치/28,672 참조. 기존 R007 112원본 경계 픽셀 및 R008 224 넓은 면 접합 관계를 중복 새로운 원본 texel로 가산하지 않는다.
- **상태 원장:** 7목재×32=224 정적 blockstate variant, **1,120 상태·면 투영(146,944 반복 UV 참조)**. 112 위·아래 상태 쌍×4면=**448 소스 경계 비교**, 그중 **신규 얇은 north/south 면 접합 224 상태-면 행/672 경계 픽셀 사용, 알파 불일치 0**. 원본 facing 회전을 중복 제거하면 얇은 면 56모델-면 패턴/168 모델-열 참조. 넓은 면에서 벚나무 원본 4경계 열 때문에 128 상태·면 알파 불일치 **반복** 검출(기존 R008).
- **PNG source face:** 전체 문 모델 280면 중 알파0 포함 면 **48개**, 모두 넓은 west/east 면. 얇은 모델면 168개에는 알파0 없음, 전면 부분투명(1..254) 0. 원본 56개 문 템플릿은 `east`면 `cullface` 미지정, source 필드만 검증했지 실제 가림/엔진 오류 아님.
- **정적 소스 31 PNG 모델 면 full RGBA/UV 샘플 범위 완료:** R009 다락문12 PNG /216면 /25,344참조 + R010 선반5 PNG /100면 /6,880참조 + R011 문14 PNG /280면 /36,736참조 = **총31개 원본 PNG, 596 모델-면 패치, 68,960 참조**. R007 선택패치 71개는 중복 가산하지 않음. 과거 127 leaf·512규칙·544 상태·672 instance·4,320면 및 v38 oak shelf32는 계속 역사적 결과로 계승만.
- **증거:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R011/ — REPORT/SUMMARY, 5 CSV, 얇은 면 원본 UV source SVG, 재현 규약. R000–R010 버전, 전체 v38, 타 단계 불변.
- **핵심 미완료: 실제 Minecraft 정적 화면 검증은 여전히 0/31.** **사용자 협조 필요:** 기본 리소스팩 Minecraft Java 1.21.11에서 (1) 벚나무 문 위·아래+힌지/open/방향 (2) 뒤틀린 및 정글 다락문 열린 upper/lower 동일 facing 비교 (3) 선반 powered, side_chain left/center/right 예시가 상태 확인 가능한 실제 스크린샷. 공식 Mojang JAR SHA-1 인증은 사용자 지시대로 필수 단계에서 제외. 애니메이션 보류, PZ 변환·가구3D·타단계 변경 금지.
- **사용자 요청에 따른 중단 규칙:** 이제 고정 31개 대상의 **전체 정적 모델 면 소스 실화소 조사**를 마쳤으므로 새로 독립적이고 검증 가능한 소스 측정 과제가 없는 한 같은 파일의 반복 분석으로 R012를 만들지 말 것. 이후 사용자가 **`계속해줘`만 말하면 작업을 멈추고, 실제 인게임 확인을 위한 사용자 화면 증거가 필요하다고 정확히 안내**할 것. 새 PNG/모델/스크린샷 등 별도 증거가 제공되면 재개.

---

## 최신 연구: TEX11-R010 — 선반 5종의 32×32 원본 전체 UV면·연결 조건·전면 경계 측정 (2026-11-13)

- **현재 `TEX11-R010` / 다음 `TEX11-R011`.** 사용자 제공 `1.21.11/` 원본 **shelf 5 PNG, leaf 30 JSON, template 6 JSON, blockstate 5 JSON** 직접 분석. PNG 5/5 CRC 검증 통과, 5,120 기존 원본 RGBA 텍셀, 완전/부분 투명 없음. 기존 PNG 총31개 변경·추가 없음.
- 모델 **100 UV 면 패치/6,880 PNG texel 참조**, 그중 R007에서 이미 조사한 35 패치/4,720참조를 제외해 **신규 본체 면 패치 65개/2,160 texel 참조**. 프런트 5역할(각16×8) 전부 PNG 실픽셀 추출.
- 원본 multipart **120규칙**, 5재질 × 4facing × 2powered × 4side_chain = **160 논리 정적 상태**, 각 body+overlay 모델2개·16면·864 texel 참조 → **2,560 state-face 참조 / 138,240 반복 UV 참조**. 원본 signature 중복제거하면 **100 모델·회전 조합**(powered=false의 side_chain 반복 때문). **160상태나100서명이 160/100개 별도 인게임 시각 인증을 뜻하지 않음**. R006 4목재 128상태, 역사적 v38 oak_shelf 32 상태를 새로 중복 가산하지 않음.
- **overlay 구조 25개**의 소스 geometry 8항목씩 검증, 25/25 통과. center front는 Z=13 두께0, Y4..12; 상·하단 부재 경계와 정렬. 본체15면 중 cullface 지정11면, 전면1면은 미지정. 게임 런타임 z-fighting/cull 테스트 아님.
- **25개 가상 패널 인접·총 200 경계 텍셀 쌍 실측**. left→center의 두 번째 패널 반전 점수는 4목재(참나무·가문비·자작·벚나무) RGB L1=0, 대나무104. 독립 atlas 영역 간 유사도 수치이지 인게임 연결 방향 확정 아님. `SHELF_FRONT_EDGE_CANDIDATES.csv`에 전 후보 보존.
- **증거 폴더:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R010/ (REPORT/SUMMARY, 5 CSV, source atlas SVG, 재현 규약). R000–R009 이전 버전과 전역 v38/타단계 불변. PNG31·leaf127·원본 rule512·기존 544 state·672 instances·4320 faces 등 과거 실적 계승.
- **인게임 정적 검증 0/31.** 공식 Mojang JAR SHA-1 인증은 사용자 결정에 따라 필수 검증에서 제외(인증했다고 하지 않음). 애니메이션 보류, PZ 변환·실제 3D 가구 제작 금지.
- **다음 R011:** 7종 목재 문 상·하단 총 14 PNG에 대해 이미 수행한 원본 경계/UV 연동 검사와 중복하지 않는 **전체 문 모델 5면 실 RGBA UV 패치·alpha/cullface/평면 감도** 등 추가 independent source-only 연구가 가능. 즉, 현재 사용자의 추가 도움 없이는 진행할 수 없는 상태가 아니다. 다만 실제 게임 정적 판정이 필수로 바뀌거나 더 이상 신규 독립 실측이 없으면, 사용자가 `계속해줘`라고 해도 멈추고 구체적인 필요 자료를 알려준다.

---

## 최신 연구: TEX11-R009 — 다락문 12종 모든 면 UV·192상태·180도 알파 마스크 (2026-11-13)

- **현재 `TEX11-R009`, 다음 `TEX11-R010`.** 사용자 직접 추출본 `1.21.11/` **다락문 blockstate 12 JSON·leaf 36 JSON·template 6 JSON·PNG 12개** 실제 다시 읽어 검사. PNG 실화소 12/12 CRC 통과. 원본 192상태×6면=**1,152 상태·면 투영**, 12×3 모델×6면=**216 실제 UV 패치**, **25,344 면별 UV 텍셀 참조**. R007에서 이미 수행한 36 면 패치를 제외한 **180개의 새로운 고유 모델·면 패치 / 16,128 UV 참조**만 신규로 집계; 물리 PNG 픽셀을 새로 추가한 것은 아님.
- **얇은 측면 144 UV 패치 alpha=0 픽셀 0건, 부분투명도 0건.** 전체 216 UV 면도 부분투명 0건. 방향형 10종의 `open=true,half=top` X180° 회전 40 상태, 일반형 oak/dark_oak 2종은 0°; 정적 모델 `north` front world 법선 상·하 **48/48 수학 투영 일치**.
- **180° PNG RGBA/alpha 직접 재검사:** 12×256=3,072개 원본 텍셀 대조 중 warped 투명 알파 불일치 **38/256**, jungle **20/256**, 나머지 10종은 alpha=0 차이. SVG는 **정적 PNG 마스크**, 실제 게임 스크린샷 아님. 방향형 top-open X180과의 연관은 검증 후보이지 인게임 시각 확정 아님.
- **근거** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R009/ — REPORT, SUMMARY, 216면 CSV, 1,152상태 CSV, 180° 마스크 CSV/SVG, 재현 규약. R000–R008 전부 불변. scope 31 PNG, 127 leaf, 512 blockstate rule, 544 state, 672 instances, 4,320 oriented faces, 문 112 기하 쌍 및 전역 v38 oak shelf 기존 기록 계속 계승(중복 가산 금지).
- **실제 인게임 정적 검증 0/31**. 공식 Mojang JAR SHA-1 인증은 사용자 결정으로 필수 범위/분모 제외(인증 완료 아님). 애니메이션 전면 보류. 좀보이드 변환·가구 3D 제작 금지, 다른 단계 및 root v38 수정 금지.
- **다음 TEX11-R010:** 신규 source-only 연구 가능: 5종 32×32 선반 아틀라스의 모델별 UV 접합/좌우·상하 상태, 면 변환 및 실화소 오류 후보 연구. **만약 연구를 모두 마치거나 실제 인게임 증거/사용자 조작이 필요한 막힘에 도달하면 `계속해줘`만으로 무작정 반복하지 말고 사용자에게 멈춤 이유와 필요한 자료를 알려준다.**

---

## 최신 연구: TEX11-R008 — 문 상태·면 UV 접합과 다락문 RGB/alpha 대칭 보완 (2026-11-13)

- **현재 `TEX11-R008`, 다음 `TEX11-R009`.** 원본 `1.21.11/`의 문 blockstate 7 JSON(총224 variants)·공유 템플릿 8 JSON·문 PNG blob14개 직접 재조회. R007 문 경계 RGBA 112원본 픽셀 쌍을 **재사용**해 112문 상태 쌍×2 넓은 면=**224 상태·면 UV/cullface 대응**, 56개 중복제거 면 구성×16열=**896 model-UV-texel 참조**를 확인. 상태별 복제 **3,584 픽셀 사용**은 독립 신규 픽셀 수가 아님.
- **상·하 UV U/V 대응 및 cullface 지정 불일치 0/224**. 체리문 PNG의 alpha 다른 원본 x열 4/6/9/11은 여러 회전/면 상태에서 반복되어 **128개의 파생 상태·면·픽셀 불일치 사용**으로 나타남. 독립 물리 오류 128개도, 인게임 문제 확정도 아님.
- **R007 CSV 필드 누락 보완:** `UV_ORIENTATION_CANDIDATES.csv`의 12 다락문 행에 대칭값 열이 비어 있던 문제를 발견하고, 원본 사용자 PNG **12개 직접 CRC·RGBA 디코딩(12/12 통과, 3,072 원본 텍셀)**해 새 `TRAPDOOR_SYMMETRY_REMEASURED.csv`로 실제 실측 복구. 알파 좌우 대칭 11/12·상하 대칭 10/12, RGBA 완전 대칭 H/V 모두 0/12. `warped_trapdoor`: alpha H38/V30; `jungle_trapdoor`: V20. 기존 R007 결과물 불변.
- **이번 릴리스 근거:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R008/ — REPORT/SUMMARY, 3 CSV, UV 경계 SVG, 재현 규약. 타 단계와 루트 문서 불변. 과거 31 PNG·127모델 리프·512 규칙·544상태·672인스턴스·4,320면·112문 기하 정렬 및 역사적 v38 oak shelf 별도 계승.
- **인게임 정적 검증 0/31** 유지. 공식 Mojang JAR 전체 SHA-1/메타데이터 인증은 완료 분모에서 제외(완료 주장 아님). 애니메이션 전면 보류, 기존 기록 삭제 금지. 좀보이드 변환/실제 가구 3D 모델링 금지.
- **다음 TEX11-R009:** 스크린샷/실제 게임 상태가 있으면 벚나무 문 alpha 이음새·warped/jungle 다락문 방향 비대칭을 게임 정적 장면에서 검증. 없으면 계속 source-only로 색상/UV/면 배치의 검증 가능한 빈틈에 집중하고 인게임 완료 0 유지.

---

## 최신 연구: TEX11-R007 — 실제 사용자 추출본 PNG 경계·정적 UV 텍셀 연구 (2026-11-13)

- **현재 `TEX11-R007` / 다음 `TEX11-R008`.** 사용자 제공 `1.21.11/` 원본 31 PNG를 다시 바이너리 디코딩, PNG CRC/SHA-256 기존 기록과 **31/31 일치**. 이전 확보한 31 PNG의 재검증이며 새로운 고유 텍스처 31개를 추가한 것이 아님.
- **신규 문 실화소 연구:** 7종 문 위/아래 경계 16열씩, 총 **112개 실제 RGBA 쌍**. 상단 파일 y15 ↔ 하단 파일 y0 비교; **벚나무 문에서 alpha 차이 4/16열**, 나머지 6재질 0/16. x반전 후보 점수도 보존. R006의 112개 기하 정렬과 다른 검사.
- **신규 UV 정적 면 픽셀 연구:** 사용자 제공 원본 템플릿 JSON **12개**·리프 JSON **24개** 직접 읽고, 다락문 12종×3면=36 패치 및 선반 5종×7면=35 패치, 총 **71 UV face patch / 13,936 텍셀 참조** 샘플. 다락문 12개 수평/수직 RGB·알파 대칭 및 선반 5종 left/right 반전 후보 **17개** 비교. 선반 5종은 RGB L1에서 수평반전 후보의 차이가 더 작았으나, 이는 **독립 UV 영역의 수치 비교만으로 실제 방향 판정이 아님**.
- **정적 소스 이미지 증거:** [문 조립 SVG](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R007/DOOR_SOURCE_SEAM_PREVIEW.svg) · [선반 UV 픽셀 패치 SVG](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R007/SHELF_FACE_UV_RASTER.svg). **실제 Minecraft 게임 스크린샷이 아니며** UV 면의 엔진 카메라 투영/가림/컬링 검증도 아님.
- **기존 연구 실적 별도 보존:** 31 PNG/127 leaf/512 blockstate 규칙/544 정적 상태/672 모델 인스턴스/4,320 회전 면/112 문 기하 정렬. 역사적 v38 참나무 선반 32 정적 상태는 중복 가산하지 않았고, 루트 v38 변경도 없음.
- **실제 인게임 정적 검증 0/31** 그대로 유지. Mojang 원본 JAR 전체 SHA-1/공식 메타데이터 인증은 사용자 결정에 따라 필수 항목과 분모에서 제외(공식 인증 성공 주장 아님). 애니메이션은 계속 전면 보류, 기존 기록 삭제 없음. PZ 변환·실제 가구 3D 모델링은 하지 않음.
- **증거 결과:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R007/ — REPORT, SUMMARY, CSV 4개, SVG 2개. 이전 R000–R006 불변.
- **다음 TEX11-R008:** 실제 Minecraft 게임에서 재현 가능한 정적 facing/hinge/half/열림 상태와 스크린샷이 확보되면 벚나무 문 RGBA 이음새·다락문 오리엔테이션·선반 전면 후보의 엔진 화면 실측. 그렇지 않으면 소스 위주의 자산/면 투영을 더 검증하되 **인게임 검증을 0에서 올리지 말 것**.

---

## 최신 연구: TEX11-R006 — 정적 상태별 회전·UV 투영 (2026-11-13)

- **현재 `TEX11-R006`**, 다음 **`TEX11-R007`**. 주 원본은 사용자가 게임 설치본 JAR에서 추출해 업로드한 `1.21.11/`. 이전 R001~R005 및 전역 v38 불변.
- 사용자 추출본을 직접 파싱한 R003/R004 소스 근거를 결합해 **문 224 + 다락문 192 + 비참나무 선반 128 = 544 정적 모델 상태**에 대해 회전 좌표·world-facing normal/cullface·PNG 픽셀 UV 범위 계산. **672개 모델 인스턴스 / 4,320개의 face 투영** 생성. source 오류·좌표 범위 초과·미해결 재질 **0건**.
- **새 문 상·하 연결 공간 검증 112/112 정렬.** 힌지·방향·열림 상태가 같은 아래/위 문 모델의 XZ footprint, 회전, 블록 높이 경계 일치. 이는 **픽셀 무늬 접합/게임 화면 확인이 아님**.
- 선반은 현재 단계 독립 4종 128 상태만 새로 투영했으며, 기존 참나무 선반의 역사적 v38 7 leaf/32상태는 중복 추가하지 않는다. 고정 PNG31개 테스트 매트릭스에는 참나무 선반도 포함.
- **실제 인게임 정적 테스트 0/31**: 문14 PNG/다락문12/선반5를 `INGAME_STATIC_TEST_MATRIX.csv`에 전부 시각 검수 대기로 표시. 소스에서 계산한 회전·UV 좌표는 실제 엔진 GPU 렌더 검증과 구분.
- **Mojang 원본 JAR 인증은 R005 사용자 결정에 따라 필수 연구 범위 밖.** 앞으로도 원본 JAR SHA-1을 요청/미완료 항목 계산하지 않는다.
- **결과:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R006/
- **다음 R007:** PNG 실제 RGB·알파 픽셀로 UV를 따라 정적 샘플링한 시각 접합 후보 추출 → 실제 게임 화면·상태 근거가 제공되면 개별 인게임 검증. 애니메이션·PZ 변환·가구 모델 제작 금지.

---


## 최신 운영 기준: TEX11-R005 — 공식 원본 JAR 인증 단계 제외 (2026-11-13)

- **현재 `TEX11-R005`**, 다음 **`TEX11-R006`**. 이 버전은 **사용자가 명시적으로 요청한 범위 변경**이며 신규 PNG/JSON 실측은 없음.
- **제외:** Mojang 공식 `client.jar` 전체 SHA-1과 버전 메타데이터 인증을 **필수 단계, 완료율 분모, 다음 작업에서 모두 제거**. 사용자의 직접 설치본에서 압축 해제한 `1.21.11/`를 **사용자 진술에 기반한 주 원본**으로 사용한다. 파일 출처에 대한 진술을 존중하되 SHA-1 인증을 수행했다고 주장하지 않는다.
- **유지:** 사용자 추출본 소스 검증 PNG 31/31 (R003), 리프 JSON127/127·UV 114면·blockstate512규칙·정적 선반128조건 (R004). **실제 게임 내 정적 렌더 실측은 여전히 0/31**이며, 검증 완료라고 표시하지 않는다.
- **다음 R006:** 소스에서 회전된 정적 모델·UV 투영 검증 및 가능한 범위의 화면 비교. 실제 인게임 증거가 있으면 정적 UV/문양 접합/컬링·빛을 검증. 원본 JAR 파일이나 SHA-1을 다시 요구하지 않는다.
- **이번 의사결정 문서:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R005/SCOPE_CHANGE.md
- **이후 작업 지시 우선순위:** 현재 `STATE.json`과 이 인수인계의 최신 R005 결정이 R001~R004의 "공식 SHA-1 확인 예정"이라는 오래된 작업 계획보다 우선한다. 기존 기록·전역 v38·다른 단계는 수정하지 않음.

---


## 최신 결과: TEX11-R004 — 정적 리프·UV·블록 상태 실제 검증 (2026-11-13)

- **현재 `TEX11-R004`**, 다음 **`TEX11-R005`**. 고정 목표 목재·구조부품 **31 PNG**, 전역 `v38` 및 역사적 R001·R002·R003 파일·결과 모두 불변.
- 우선 출처는 사용자 제공 `1.21.11/` JAR 추출본. R003에서 이미 직접 PNG 바이트 SHA256/CRC 검증 31/31 완료했으므로 이번 신규 PNG 해시 측정은 중복 계상하지 않음.
- **신규 실제 파싱:** 사용자 추출본 모델 리프 JSON **127/127개** 직접 읽고 Git blob SHA·parent 템플릿·texture 슬롯·leaf elements 유무 확인, **전부 일치**. 현재 독립 단계 범위는 문56+다락문36+비참나무 선반28=**120**; 옛 v38 참나무 선반 leaf **7**은 역사적 참고.
- **새 템플릿 검사:** 공유 모델 21개 **114 explicit UV면**의 UV 0~16 범위, 16px/32px 텍셀 정수 경계, 면적·슬롯·90° 회전 **114/114 통과**. 형상 요소 25/25 좌표·faces 유효; 두께0 선반 전면 패널 **5개**는 평면 요소로 정상 분리. UV 정의를 검사했을 뿐 화면 UV 렌더링을 관찰한 게 아님.
- **새 정적 연결:** 사용자 추출본 blockstate 23개 **512개 규칙/variant 모두** 참조 leaf·회전·상태에 따른 이름 검사 통과(문224, 다락문192, 선반96). 선반 4종 ×32조건 = **128/128 본체+전면 요소** 소스 조건 평가 통과. 이는 R001의 비공식 미러 정적 검사를 사용자 추출본에서 별도로 확인한 것, 고유 128개를 중복 집계하지 않음.
- **31/31 PNG 실제 material 슬롯 참조:** leaf `bottom/top/texture/all`에 총 **183번** 사용(문112·다락문36·선반35). `particle`이 가리키는 외부 5종 stripped block/log PNG는 범위 밖이라 원본 픽셀 해시 미인증.
- **4개 층의 판정 유지:** ① 사용자 제공 추출본 소스 검증 진행 ② 미러 교차 대조 이전 R003 31 PNG·175 JSON SHA 기록 유지 ③ **Mojang 전체 JAR SHA-1 공식 인증 0/31** ④ **실제 인게임 정적 화면 관찰 0/31**. 애니메이션·PZ변환·3D 모델 제작 모두 보류/미착수.
- **불변 보고서:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R004/
- 다음 TEX11-R005에서는 실제 공식 클라이언트 JAR 바이트/공식 메타데이터 또는 인게임 정적 장면 증거를 확보하면 해당 분리 층만 갱신. 증거 없을 때는 source 회전 UV·정적 조립 추론을 화면 검증과 분리. 다른 단계 및 루트 v38 변경하지 않기.

---

## 최신 인수인계: TEX11-R003 — 사용자 제공 추출본 소스 정정 (2026-11-13)

- **현재 `TEX11-R003`**, 다음 `TEX11-R004`, 전역 `v38` 변경 없음. 기존 `R001`/`R002` 분석·커밋·CSV/JSON을 수정하거나 중복 계산하지 않았다.
- **우선 출처:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11 — 사용자가 Minecraft Java 1.21.11 JAR을 직접 압축 해제하여 업로드했다고 밝힌 폴더. 해당 사용자 제공 추출본은 Mojang 공식 배포본 무결성 인증과 별도.
- **신규 실제 검증:** 고정 PNG 31개를 이 `1.21.11/` 폴더에서 직접 읽어 SHA-256/PNG CRC 재계산 **31/31 통과**, 기존 v4/R001 PNG 해시 및 미러 blob SHA **31/31 동일**. 31 PNG의 파일 바이트 총 8,080; 16×16 26개, 32×32 5개, `bamboo_shelf` 4bit. 이전 RGB/알파/UV 실측은 동일 바이트라서 입력 자료로만 재사용하며 재측정 새 수량 없음.
- **모델/블록 상태/아이템:** 사용자 추출본과 미러 Git blob SHA·size 대조 **175/175 일치**: 현재 범위 168개(leaf120 + blockstate23 + template21 + shelf item4), 역사적 참나무 선반 7 leaf는 중복 미계상. 추출본 JSON 본문 직접 파싱 **48/48**(블록상태23, 템플릿21, 아이템4), 이전 기록의 rule/UV면 수 **48/48** 동일.
- **4종 검증 층 분리:** ① 사용자 제공 추출본 31 PNG+48 JSON 실파일 / ② 비공식 미러 교차 SHA 31 PNG+175 JSON / ③ **Mojang 공식 원본 JAR 전체 SHA-1 인증 미완료 0/31** / ④ **실제 인게임 정적 렌더 0/31**. 추출 폴더 파일 해시로 원본 JAR 컨테이너 SHA-1을 증명할 수 없음. 애니메이션 계속 보류.
- **R003 새 증거 폴더:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R003/
- **다음 TEX11-R004:** 최신 STATE·HEAD 충돌 검사 후 진짜 원본 JAR bytes + Mojang 직접 버전 메타데이터 확인(가능할 때만), 정적 인게임 UV·접합·컬링 증거 확보. Project Zomboid 변환/가구 3D 모델 생성 금지, 다른 재질 단계와 루트 v38 수정 금지.

---

## 최신 독립 릴리스 — TEX11-R002 (2026-11-13)

- **현재 `TEX11-R002`**, 다음 `TEX11-R003`, 전역 레거시 `v38` 유지. 이전 R001/R000은 아래 역사적 문맥으로 보존.
- 31 PNG 직접 재조회·CRC/zlib/RGBA 파싱 31/31, R001 미러 Git blob SHA 일치 31/31. 모든 PNG는 가로·세로 정확 순환 RGBA 반복 최소 이동이 원본 가로/세로 크기(16 또는 32)와 동일. 좌우 alpha 경계 차이 0/31, 상하 alpha 경계는 cherry_door_bottom(2열), cherry_door_top(6열)만. R001의 서로 다른 문 PNG 경계 4열 비교와 별도.
- 선반 5종 32×32의 가로 16px 순환 픽셀 일치율은 62.695~65.039%이며 완전 반복 아님. 모델 리프 120/120 Git tree SHA/파일 크기 확인(문56, 다락문36, 비참나무 선반28). 그중 12개만 이번 회차 leaf JSON 본문·부모 SHA 독립 확인, 나머지 108개는 Git tree 수준.
- 미러 root `1.21.11.json`에 복사된 예상 Mojang client.jar SHA1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`와 31,152,600바이트 확인했지만 **공식 바이너리 접근 실패**. 공식 JAR 내 PNG 인증 0/31, 인게임 정적 0/31. 애니메이션 금지 계속 유지.
- 근거 저장: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R002/
- **다음 TEX11-R003**에서 STATE/HEAD 충돌 검사 후 Mojang 공식 JAR 획득·전체 SHA1·31 PNG 교차 인증, 인게임 정적 UV 경계부터 진행. 다른 단계·루트 v38·과거 불변 폴더 수정 금지.

---

## 2026-11-13 신규 독립 검증 — TEX11-R001

- 단계 최신 버전 **TEX11-R001**, 다음 **TEX11-R002**. 기존 전역 v38 불변. 아래 R000 계획 문구는 최초 설정 당시 기록이다.
- 실제 비공식 미러 PNG 31/31을 독립 재해시(v4 SHA 대조)·CRC/디코딩/RGBA 확인. 원본 11,776 픽셀(불투명 11,153, 투명 623, 부분 0), 16×16 26개/32×32 선반 5개. bamboo_shelf는 4-bit indexed PNG 예외.
- D1 문 7쌍 알파 경계(cherry만 불일치 4열) 및 다락문 12종 UV; D2 선반 5 atlas×5 UV 영역 25 실화소 크롭; D3/E 파생 선반 28 leaf 및 128개 정적 상태, 문 56 leaf/다락문 36 leaf, 공유 템플릿 21 JSON. 선반 38 explicit UV면/2,304 texel uses 기존 v38과 재대조, oak_shelf v38 7 leaf는 신규 계산에 불포함.
- 공식 Mojang client.jar 인증 **0/31**, 실제 인게임 정적 **0/31**. 반복 주기·실제 UV투영·문양 연결 미검증. 애니메이션 연구 계속 보류.
- 결과: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R001/
- 다음 채팅은 GitHub STATE 재조회 후 TEX11-R002에서 공식/인게임 미검증 항목부터 재개.

---

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX11-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-11 / 목재·구조부품 / 31개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-11 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-11_목재구조부품.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-11/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 31/31 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

v38 oak_shelf 7개 leaf/7부모·32 정적 상태·38면 2,304 texel uses 소스 검증이 이미 존재. v4 oak_shelf 표본과 중복 카운트하지 말고 4종 다른 목재 선반 모델 연결을 추가 연구할 것.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-11-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 문·다락문 윗/아랫면 알파와 무늬 연결
- **D2:** 32×32 5종 shelf texture atlas와 일반 16×16 비교
- **D3:** v38 oak_shelf 7 leaf·38원본 explicit UV면·32 정적 상태 평가 근거 재사용 후 미검증 파생목재 확대

## 검토할 정확한 텍스처 31개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-11-001` | `oak_trapdoor` | `7f2d78c69dcfb71d4900b974d40f6e334065f4e4c72aa36fe37ce034df9a2abd` | `assets/minecraft/textures/block/oak_trapdoor.png` |
| `1-1-11-002` | `spruce_trapdoor` | `b22c847ef0810ba5ed6546de8484ad17bc72ea894a42078ca9221aa3c23d8fdf` | `assets/minecraft/textures/block/spruce_trapdoor.png` |
| `1-1-11-003` | `birch_trapdoor` | `48e96dc1f95daee99412dc0724411c3671ab529658f00ca0aa66227ae30a3092` | `assets/minecraft/textures/block/birch_trapdoor.png` |
| `1-1-11-004` | `dark_oak_trapdoor` | `b56fddb418e82004eb6371e85acf9dc7cac608f5230049543159b2ddcc3196ed` | `assets/minecraft/textures/block/dark_oak_trapdoor.png` |
| `1-1-11-005` | `bamboo_trapdoor` | `4b3fc966d9f9c5021a387519a1cee3fd53814d5605e5623b9aacb5930453f3dd` | `assets/minecraft/textures/block/bamboo_trapdoor.png` |
| `1-1-11-006` | `oak_door_bottom` | `a209e7e8611d56d211445d5df23a50c31185a293c51f4e03f3cb691209a49df4` | `assets/minecraft/textures/block/oak_door_bottom.png` |
| `1-1-11-007` | `oak_door_top` | `0cdc592715a8145d1837f551adf774227dedf7650569e7a50f6cb831c7c0a6c6` | `assets/minecraft/textures/block/oak_door_top.png` |
| `1-1-11-008` | `acacia_trapdoor` | `9d8aebedce220ba31aea5b2c67e6180d4eec1e7dbabefc334d341e0a49ee668b` | `assets/minecraft/textures/block/acacia_trapdoor.png` |
| `1-1-11-009` | `cherry_trapdoor` | `21180e8d199bc79d8bf95ae72af08dc4df3ae02519818b13b78ba91af580dc27` | `assets/minecraft/textures/block/cherry_trapdoor.png` |
| `1-1-11-010` | `mangrove_trapdoor` | `65087166442d0a5d9edf1c467d44ab3b4f9969f1bd851c5d9ffa82259b90f1fc` | `assets/minecraft/textures/block/mangrove_trapdoor.png` |
| `1-1-11-011` | `pale_oak_trapdoor` | `5eafb6cfd036b128aea6daca3dba44f9fb3521aacb7f682d774be8c1c9c72c8a` | `assets/minecraft/textures/block/pale_oak_trapdoor.png` |
| `1-1-11-012` | `acacia_door_bottom` | `b38b2d097cac0b7b08efa43045bba368abc4a3b190ccb2e594862766c5e1e8c2` | `assets/minecraft/textures/block/acacia_door_bottom.png` |
| `1-1-11-013` | `acacia_door_top` | `2552920fee394ac3b6d165d5638bc84d2223374d8974bdd668bced3be16e5f3c` | `assets/minecraft/textures/block/acacia_door_top.png` |
| `1-1-11-014` | `spruce_door_bottom` | `5684f6fa01b213babc2ee0a07d8a5b1803fc652fe1bfbf461ff973cb07dffd89` | `assets/minecraft/textures/block/spruce_door_bottom.png` |
| `1-1-11-015` | `spruce_door_top` | `53be462544fd88a451bba74eb699c113c506773fee0243f2c79983cee66acb7d` | `assets/minecraft/textures/block/spruce_door_top.png` |
| `1-1-11-016` | `birch_door_bottom` | `7bd6636532ffc21e9ecc7aa5fc8d975e9d5b4f2e2d32db2cb3c4d00115c29c70` | `assets/minecraft/textures/block/birch_door_bottom.png` |
| `1-1-11-017` | `birch_door_top` | `48b63883ce9a4b4c72b437d5eb5c712f6b2b465ef1bbcb37a52dee9e30d0a4ea` | `assets/minecraft/textures/block/birch_door_top.png` |
| `1-1-11-018` | `cherry_door_bottom` | `08bb521c3bbbe6e5a1891554b4a8dbd6025b563dfc7ffb3dc6e14be75f5042aa` | `assets/minecraft/textures/block/cherry_door_bottom.png` |
| `1-1-11-019` | `cherry_door_top` | `9f81189ffe46f5a3fb31b89f5ae22b15c895920ee297fcce0bbc0e3f0654b47b` | `assets/minecraft/textures/block/cherry_door_top.png` |
| `1-1-11-020` | `bamboo_door_bottom` | `07a38a693f5efaf6a28d1d924ccffe60d453ac55056088c5796777b82e73644c` | `assets/minecraft/textures/block/bamboo_door_bottom.png` |
| `1-1-11-021` | `bamboo_door_top` | `90f8ca7ab7ade430a96fc176de2cfc4294a86136646fb82f24d2159997cfb2b6` | `assets/minecraft/textures/block/bamboo_door_top.png` |
| `1-1-11-022` | `mangrove_door_bottom` | `aa84032ae9968b58dfb347ab4062695caaea4e793ed2b6c20f9f5f909bc145af` | `assets/minecraft/textures/block/mangrove_door_bottom.png` |
| `1-1-11-023` | `mangrove_door_top` | `50a7be61312a2f7ab4ee61e037e5ef7c1b1878a215d50616445c16378927bf1c` | `assets/minecraft/textures/block/mangrove_door_top.png` |
| `1-1-11-024` | `crimson_trapdoor` | `654f72862b0f2c7b84ad11ff53d4b0a7e85d538af1a4d4a568e1cbb34b2fd5cf` | `assets/minecraft/textures/block/crimson_trapdoor.png` |
| `1-1-11-025` | `warped_trapdoor` | `23b02d0bfb47a73c6b8de98520d95f6e598bac2a47ef244c44e2aa122a79c7b1` | `assets/minecraft/textures/block/warped_trapdoor.png` |
| `1-1-11-026` | `jungle_trapdoor` | `cf12b835daed7c1d7e666144c85ff78e94bc41ddc45bbb49c130f89493e51244` | `assets/minecraft/textures/block/jungle_trapdoor.png` |
| `1-1-11-027` | `oak_shelf` | `cb7cf9720f3e50d6cd2e67dd8fde89a4865aa507f84e38d1c0ae0e639dd52c87` | `assets/minecraft/textures/block/oak_shelf.png` |
| `1-1-11-028` | `spruce_shelf` | `74af0ec4272efcadf0bb67e2f19e924c68b50c2a79c3692ec647541083b40dd9` | `assets/minecraft/textures/block/spruce_shelf.png` |
| `1-1-11-029` | `birch_shelf` | `73501db8e785121f52acf25521769da029f1336b0083e46eeb7b6704d904f20e` | `assets/minecraft/textures/block/birch_shelf.png` |
| `1-1-11-030` | `cherry_shelf` | `9aa40570d84cb0dc96fcb14a96ccf524807d8785c17c0b972abfdc9e48e46e53` | `assets/minecraft/textures/block/cherry_shelf.png` |
| `1-1-11-031` | `bamboo_shelf` | `6c8774fa4aa50f99d518fc56e94bea0ee6dd44293357e1876ff846f3e4c8c09d` | `assets/minecraft/textures/block/bamboo_shelf.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX11-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX11-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-11/TEX11-R001/`. 다음은 이 단계만 `TEX11-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-11/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
