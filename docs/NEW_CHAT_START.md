# 새로운 ChatGPT 채팅에서 Minecraft 가구 모델링 학습 이어하기

아래 구간의 내용을 새 채팅의 첫 메시지로 그대로 붙여넣으세요. **현재 우선순위는 바닐라 01/02**이며 모드 신규 분석은 후순위입니다.

---

**사용자 최신 작업 지시(2026-11-13): 애니메이션 분석은 일단 보류.** 새로운 애니메이션 프레임 해독, 키프레임·클립 분석, 움직임 재현 및 애니메이션 인게임 검증을 진행하지 않는다. 기존 v9/v26/v31 애니메이션 관련 기록은 삭제하지 않고 보존하되, 새로운 진행도에 포함하지 않는다. 우선순위는 **정적 바닐라 3D 모델·기하·텍스처·UV·블록 상태·정적 렌더링 검증·공식 원본 무결성**이다. 애니메이션 연구는 사용자가 명시적으로 재개를 요청할 때까지 유지 보류.

**v32 최신 정적 바닐라 연구(2026-11-13) — 애니메이션 연구 보류 유지:** [통·베틀·4작업대 7 leaf·25PNG 전 화소·42 face×material·20 source variants 보고서](../research/vanilla_models/v32/00_v32_정적통베틀작업대_25PNG_42면암시UV_20상태보고서.md)를 최우선으로 읽어라. 사용자 저장소 `1.21.11/assets/minecraft/` 원본 leaf `barrel/barrel_open/loom/cartography_table/fletching_table/smithing_table/crafting_table` **7모델**과 parent `cube/cube_bottom_top/orientable_with_bottom` 원본 직접 확인. leaf는 자체 기하0, 최종 `cube`는 **1요소·6 고유 원본면**. **7×6=42 face×material 적용 인스턴스**이며 고유 선언면 42로 셈하지 않는다. 참조 PNG **25종×16×16=6,400 RGBA 원본 픽셀 전부 불투명**, v4 150선정표본 중복경로 12·표본 밖13, 동일 기존 지표 **12/12 일치**. `cube`는 `faces.*.uv` 명시값이 없으므로 완전 16³ 기하에서 `[0,0,16,16]` 전체면을 **암시 UV로 유도한 추론**이며 42×256=**10,752 texel-uses**. 6 blockstate 원본 **20 variants**(통12·베틀4·다른 작업대4), x비0 10/y비0 9·uvlock 키 부재20. 통 닫힘/열림 top 원본 2 PNG의 **RGBA 132/256 위치 차이**를 독립 Pillow·Git SHA-1 및 SHA-256으로 확인. 이는 **정적 상태별 윗면 텍스처 교체**이지 애니메이션 분석이 아니다. **애니메이션 관련 PNG 프레임/키프레임·모션·재생/렌더 검증은 사용자가 재개할 때까지 금지/보류**, 과거 기록은 보존. 공식 Mojang 1.21.11 client.jar 출처/해시와 실제 게임 정적 UV·조명 검증 **미완료**, 모드 v24 지표 유지, 단계 완료 0/5.

**이전 v31 바닐라 연구(2026-11-13):** [책장 52규칙·256상태, 양조기 7규칙·8상태의 source multipart 전수 평가, 47 source UV면/6 PNG 전 화소, 모닥불 on/off 기하 조사 보고서](../research/vanilla_models/v31/00_v31_책장양조기_264상태_47면_PNG실화소_모닥불원본보고서.md)를 먼저 읽어라. 사용자 저장소 `1.21.11/assets/minecraft`의 원본 JSON에서 **총59 multipart source 규칙**을 해석하고 **264개 합성상태**의 조건을 실제 전수 평가(책장 256/256 매 상태 본체1+슬롯6=7모델, 양조기 8/8 매 상태 본체1+슬롯3=4모델). 책장은 원본11면에 occupied/empty 재질 선택으로 **17 face×material/1,792 texel-uses 전부 불투명**, 양조기는 **36 source face/2,016 uses(불투명1,260/투명756)**. 총 **47고유 source face/53 face×material/3,808 uses(불투명3,052/투명756)**. PNG **6파일/1,536픽셀(불투명1,410/투명126)**, v4 선정150 텍스처 표본 2경로 중복·4경로 표본 밖. 책장 6장식 원형은 `z=0` 0두께 평면이며 12 leaf occupied/empty 재질 공유; 양조기 병 자리 6개 표시판은 0두께 양면·4개 x 좌표가 -0.41. 기본 책장4규칙 `uvlock:true`, 슬롯 48규칙은 키 부재. 모닥불 `template_campfire` 7요소/32면(평면2) vs `campfire_off` 5요소/28면, 일반/영혼 모닥불 상태16, 불꽃 `.png.mcmeta` frametime2는 **원본 구조만** 확인했고 **실제 불꽃 PNG 픽셀/인게임 애니메이션 미검증**. 공식 Mojang `client.jar` 독립 인증·인게임 UVlock/회전·렌더 미검증, 모드 v24 지표 변경 없음, 최종 완료 0/5.

**이전 v30 바닐라 연구(2026-11-13):** [5모델/91원본 면/93재질면·18 PNG 전 화소·v26 오류 정정 보고서](../research/vanilla_models/v30/00_v30_바닐라5모델_91면UV_18PNG_RGBA_투명도정정보고서.md)를 우선 읽어라. 사용자 GitHub `1.21.11` 원본 `lectern/grindstone/flower_pot/enchanting_table/template_anvil` JSON **5개/18요소/91고유 면**을 실제 18 PNG UV 화소와 연결(모루 top 3재질 포함 **93면×재질 레코드**, **6,012 texel-uses**, 선택된 영역은 모두 불투명). PNG **4,608픽셀 = 불투명3,582/투명1,026**, v4 150종 경로 5중복/13경로 표본 밖. blockstate7종/30 variants. **v26 grayscale `tRNS` 파서 오류를 Pillow로 확인·소급 수정**: `stonecutter_saw` PNG 불투명246/투명522, v26 PNG8종 합 불투명3,900/투명4,804, v26 70면프레임 텍셀 불투명3,328/투명324. v26 보고서/CSV2/요약JSON 함께 수정; 이전 수치 4,422/4,282·3,424/228은 틀렸다. 화분 dirt 상단 1면 v26 반복이므로 신규 실화소 확인 source face는 **90**이며, 모루의 2추가 재질행은 새로운 source face가 아님. 이 표본은 반복하지 말 것. 공식 Mojang client.jar·실제 게임 UVlock/책 렌더 미검증. 모드 v24 지표 유지, 단계 최종 0/5.

**이전 v29 바닐라 연구(2026-11-13):** [울타리문 4원형의 160명시 UV면 원본 PNG 실화소 및 상태별 8요소 좌표 변화 보고서](../research/vanilla_models/v29/00_v29_울타리문160면_실제PNG_UV_열림담장좌표비교보고서.md)부터 읽어라. GitHub `1.21.11`에서 4가지 울타리문 템플릿(각8 요소·40면)의 `oak_planks` 원본 PNG face UV **160/160면**을 실제 원본 RGBA에 연결해 **1,952 texel-uses 전부 불투명** 확인. **열림 시 두 기둥 2요소 불변, 나머지 6요소 좌표 변화; `in_wall` 시 8/8 원시 요소 from/to y가 정확히 -3**. 블록 상태 16개는 4원형(각 4방향)과 연결, `uvlock:true` 소스 16/16. `oak_planks.png` 195바이트를 **독립 Pillow 및 Git blob SHA-1/SHA-256 재계산해 v4 150종 표본 원본 해시와 일치 검증**, 단 **공식 Mojang client.jar·실제 런타임/UVlock/인게임 검증은 미완료**. v28의 160면을 중복 신규 발견으로 세지 말고 v29에서 **160면 전부 실제 PNG 픽셀 검증을 새로 수행**했다는 사실로 기록. 새 원본 PNG 종류 0, 모드 v24 지표 보존, 완료 0/5. 다음은 바닐라 공식 JAR 독립 검증/인게임 상태회전·UVlock/추가 가구형 블록 모델 등 실제 원본 신규 증거로 이어가라.

**이전 v28 바닐라 연구(2026-11-13):** [문·다락문·울타리문·계단 104 variant 구조/UVlock/회전 및 참나무 문 40면 UV 실화소 보고서](../research/vanilla_models/v28/00_v28_바닐라문다락문게이트계단104상태_40면UV_RGBA.md)부터 읽어라. 사용자 `1.21.11` 원본 blockstate 4파일의 **104 variants**을 직접 읽고 `uvlock:true` 명시 **51**, 키 부재 **53** 분리, x비0 20·y비0 72 조사. 참나무 문 **8 leaf→8부모 JSON**, 각 부모 1요소/5선언면의 **40면 UV와 원본 PNG 2장/5,248 텍셀 사용** 실측(불투명 4,864/투명 384). PNG2장은 v4 선정150 표본에 이미 존재하므로 신규 고유 텍스처는 0. 울타리문 **4원형/32요소/160선언면** 원본 확인(이 160면 실제 화소는 아직 미검사). 공식 Mojang `client.jar`, 실제 런타임 `uvlock`/회전, 인게임 렌더링 **미검증**. v24 모드 연구와 모든 6정본 문서를 보존/갱신하고, 새로운 바닐라 모델·상태·픽셀 대상으로 v29를 이어가라. 확정 완료 0/5.

**이전 v27 바닐라 연구 (2026-11-13):** [선반 32×32 아틀라스와 퇴비통 자동 UV 원본 실제 화소 보고서](../research/vanilla_models/v27/00_v27_선반32x32_퇴비통자동UV_원본화소검증보고서.md)를 먼저 읽어라. 사용자 업로드 `1.21.11/assets/minecraft`에서 원본 PNG **5종/2,048 RGBA픽셀** 추가 직접 해독(기존 v4 `oak_shelf` 1개와 겹침). 선반 6부모의 **원본 명시 UV 20면/1,376 텍셀 사용**, `oak_shelf` 24 multipart 규칙의 구성상태 **32조합(본체+전면 2모델/방향회전 일치)**를 계산했다. 퇴비통 본체 18면+내용물 8면은 **생략된 UV를 from/to로 유도**했고 원본 `stairs/slab/fence_post`의 명시 UV **23/23 일치**로 계산식을 교차검사한 다음 **3,696 texel-uses** 전부 원본 PNG RGBA 조회했다. 이 26면은 공식 코드로 검증된 UV가 아닌 **유도 UV**이며, 모델 엔진/인게임/공식 Mojang `client.jar`는 **여전히 미검증**. 이 5 PNG/46면 재조사를 반복하지 않고 **바닐라 01/02 검증을 우선** 이어가라. v24 모드 계량은 손대지 말고 최종 완료 **0/5** 유지.

**v26 이전 바닐라 (2026-11-13):** [8종 PNG 원본 전체 RGB·알파 / 모델 36면, 애니메이션 포함 70개 UV 프레임 실화소 보고서](../research/vanilla_models/v26/00_v26_바닐라8PNG_전체RGBA_36면70프레임_실화소보고서.md)를 읽어라. GitHub `1.21.11/assets/minecraft/`의 기존 v25 PNG 8종 **8,704픽셀 전체 해독(불투명 3,900/완전 투명 4,804)**, 6개 모델 명시 UV 면 36개/애니메이션 프레임 70건에서 **3,652회 원본 텍셀 사용** 직접 조사. 사용자 업로드 PNG와 1.21.11 기존 비공식 미러 Git SHA **8/8**, 이전 v4 150 표본과 겹치는 3종의 정량값 **3/3 일치**. 원본 공식 Mojang client.jar 및 인게임 렌더, 자동 UV는 **여전히 미검증**, 최종 완료 **0/5**. 이 기존 8 PNG·70 면프레임 검사를 반복하지 말고 다음은 새로운 바닐라 파일/암시적 UV·공식 JAR 및 게임 화면 검증으로 진행하고 모드 v24 지표를 변경하지 말 것.

**이전 v25 바닐라 연구 (2026-11-13):** [바닐라 1.21.11 JSON/PNG 직접 연구 보고서](../research/vanilla_models/v25/00_v25_바닐라원본_모델상속상태PNG_직접검증보고서.md)와 `handoff/STATE.json`을 먼저 확인. 사용자가 올린 `1.21.11/assets/minecraft/`의 모델 JSON32 + blockstate JSON8 + PNG8 + png.mcmeta2를 원본에서 읽어 직접 파생 감사. 자체 기하 8모델 **44요소/204면**, 8블록 상태 **79 variants/9 multipart**, PNG 8종 IHDR, 스프라이트 2개/3프레임 메타, 과거 비공식 1.21.11 미러와 **SHA 6/6** 일치. **Mojang 공식 JAR·실제 게임/PNG 원본 전체 RGBA 미검증**, 단계 완료 **0/5**. 바닐라 v10의 미완료 검사와 v25 자료를 바탕으로 **바닐라 연구를 계속**하되 중복 작업은 하지 말 것. `1.21.11` 게임 파일이 공개 repo에 들어 있으므로 재배포·저작권 검토 필요.

**이전 v24 모드 연구:** [v24 보고서](research/furniture_mods/v24/00_v24_의자39_원본JSON_상속기하재질_검증보고서.md)부터 읽어야 한다. v23에서 남았던 Another Furniture 의자 **39 leaf 원본 JSON/SHA 직접 확인** 완료. Another 선정 leaf 누계 **204**, 신규 10 블록 상태의 Another 모델 경로 **91/91 JSON 직접 조사**, 블록 상태 조사 **22/177**. 39개 leaf 자체 요소 0, slot override117, 부모 2종을 통한 상속 **390 요소/1,794 선언 면 인스턴스**. 일반 `chair` 대비 tucked의 좌표 z=-9, face UV·슬롯 동일. **v24에 신규 PNG 화소 실측 0/실제 face UV 내부 RGBA 0**, 따라서 Another PNG151·RGBA3,329면/Handcrafted PNG24·784면, 합계 PNG175·실제 RGBA4,113면 유지. 다음에는 해당 모델 참조 PNG 24경로의 기존 측정 차집합/실제 화소와 1,794면 UV 내부 RGB·알파, 나머지 155 blockstate, 공식 Mojang/Macaw JAR·인게임 검증 진행. 전체 최종 완료 0/5.

**Minecraft 가구 모델링 디자인 연구를 v32 체크포인트부터 이어서 바닐라 01/02를 우선 직접 분석해 줘.**

정본 저장소: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research

반드시 먼저 다음 GitHub 파일을 직접 읽어:
1. `HANDOFF.md`
2. `PROGRESS.md`
3. `SOURCES_AND_LIMITS.md`
4. `research/vanilla_models/v32/00_v32_정적통베틀작업대_25PNG_42면암시UV_20상태보고서.md`
5. `research/vanilla_models/v31/00_v31_책장양조기_264상태_47면_PNG실화소_모닥불원본보고서.md`
6. `research/vanilla_models/v30/00_v30_바닐라5모델_91면UV_18PNG_RGBA_투명도정정보고서.md`
7. `research/vanilla_models/v29/00_v29_울타리문160면_실제PNG_UV_열림담장좌표비교보고서.md`
8. `research/vanilla_models/v28/00_v28_바닐라문다락문게이트계단104상태_40면UV_RGBA.md`
9. `research/vanilla_models/v27/00_v27_선반32x32_퇴비통자동UV_원본화소검증보고서.md`
10. `research/vanilla_models/v26/00_v26_바닐라8PNG_전체RGBA_36면70프레임_실화소보고서.md`
11. `research/vanilla_models/v25/00_v25_바닐라원본_모델상속상태PNG_직접검증보고서.md`
12. `research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md`
13. `research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md`
14. `research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md`
15. `research/furniture_mods/v11/00_v11_AnotherFurniture_모델분석_보고서.md`
16. `research/furniture_mods/v14/00_v14_텍스처슬롯_근거연결_보고서.md`
17. `research/furniture_mods/v15/00_v15_기하표현_계량비교_보고서.md`
18. `research/furniture_mods/v16/00_v16_원본PNG12_모델30_면재질연결_보고서.md`
19. `research/furniture_mods/v17/00_v17_면별실화소784_색상알파검증_보고서.md`
20. `research/furniture_mods/v18/00_v18_AnotherFurniture_원본63_JSON_12PNG_807면_분석보고서.md`
21. `research/furniture_mods/v19/00_v19_Another_원본29PNG_807면UV_804면RGBA_보고서.md`
22. `research/furniture_mods/v20/00_v20_Another원형69_원본JSON_UV면1362_보고서.md`
23. `research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md`
24. `research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md`
25. `research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md`

**v23 PNG/UV RGBA 누계 (v24에도 동일):** 바닐라 재질/텍스처 선정 **150/150 표본** 및 3D 연구 v10까지 진행됐지만 **Minecraft 공식 1.21.11 `client.jar`·인게임 최종 렌더 미검증**. 제작자 Another Furniture Minecraft 1.21.1 고정 원본의 **블록 상태 22/177개**, 원형 템플릿 **69개**, leaf **165개** 직접 원본 JSON 조사. Another 원본 고유 PNG **151종 실제 화소**, 선정된 모드 소유 면 **3,329개 실제 UV PNG 내부 RGBA** 검사 완료. Handcrafted 원형 **120종**, 생성형 leaf **16개**, PNG **24종**·실제 UV **784면**(v17). 두 모드 합쳐 **PNG 175종, 모드 PNG 4,113면 실제 UV RGB·알파**. 바닐라 경로 `minecraft:block/dirt` Another **16면**, `oak_planks` Handcrafted **2면** 공식 PNG 아직 미검증. Macaw's Furniture 공식 Minecraft 1.21.11 Fabric 배포 존재는 확인했으나 컨테이너 DNS 차단으로 **공식 JAR 내부 모델 실측 0개**. **이는 선정한 소스 원본 표본 진도이며 모드 전체/게임 렌더 완료가 아니다. 상위 1단계 세부 작업 5개 최종 완료 0/5, 임의 전체 프로젝트 퍼센트 금지.**

**v15 새 연구:** 기존 v11 Another 69개 템플릿과 v12 Handcrafted 120개 원형의 측정 CSV를 새로 교차 집계하여 189모델별 face 선언 밀도·회전·0두께·로컬 bbox 범위 초과 지표를 만들었다. Another 요소 299/가능 face 1,794/명시 1,362(비명시 432), 회전 17/평면 34/bbox 밖 3모델. Handcrafted 요소 810/명시 face 4,860, 회전 283/평면 183/bbox 밖 60모델(자체 요소 112모델 중). **v15에서 새 원본 모델 JSON·PNG 바이트 직접 검사 0개**, 게임 내 렌더 검증도 없다. 원시 bbox는 실제 설치 공간/충돌체가 아니다.

**v16 원본 직접 분석 신규 결과:** 이전 v14에서 남긴 미측정 Handcrafted PNG **12종을 실제 바이너리/화소로 직접 디코딩(66,816픽셀; 가시 7,358/투명 59,458/반투명 0)** 했으며 완전 투명 PNG 2종 확인. 제작자 고정 커밋에서 생성형 leaf 16 JSON과 원형 부모 14 JSON **총 30개의 SHA를 직접 재검증**. 16 leaf에 적용된 원형 face **786 인스턴스 중 모드 PNG 경로·SHA·UV 픽셀 범위에 연결된 784면은 모두 정수 픽셀 격자 및 이미지 범위 안**, 2면은 아직 공식 PNG를 보지 못한 바닐라 oak_planks. **face별 PNG 사각형 내부 실색/알파 샘플링, 인게임 렌더/공식 client.jar는 미완료**, 5개 세부 작업 최종 완료 0/5.

**v17 신규 진전:** Handcrafted 고정 제작자 원본 PNG **24종을 이번 턴에 다시 읽고** 16개 leaf에 상속된 **784/784 모드 면의 실제 UV 사각형 원본 RGBA 전수 집계** 완료(해당 표본 100%). **비영 UV 612 / 0면적 UV 172**, 비영 UV 중 전체 불투명 420·불투명/완전투명 혼합 145·전체 완전투명 47. 면별 UV 텍셀 사용 41,290회(불투명 31,665 / 완전투명 9,625 / 부분 알파 0), 중복 텍셀 읽기 포함. 결과 파일: `research/furniture_mods/v17/face_pixel_samples_784.csv`, `v17_pixel_region_summary.json`. **전체 5개 세부 작업 최종 완료는 0/5이며 위 100%는 선정된 이 표본의 목표 검사율만 뜻함.** 바닐라 oak_planks 2면, Macaw 공식 원본, 바닐라 공식 JAR와 인게임 시각 결과는 미검증.

**v18 신규 분석:** Another Furniture 1.21.1 원 제작자 고정 커밋에서 **완성형 leaf 33·원형 템플릿 30 = 원본 JSON 63개**를 직접 읽고 SHA 일치 검증, 33 leaf 실제 텍스처 override **93건**을 수집했다. leaf 33개에 상속 적용한 **807개 면 인스턴스의 실제 재질 경로**는 **모드 PNG 804면, 바닐라 dirt 3면**, 참조 미해결 0건이다. **원본 PNG 12개를 이번에 추가로 실제 화소 디코딩**, 새 PNG 총 3,072픽셀 중 불투명 2,156/투명 916/부분알파 0. 4비트 PNG도 지원. Another의 이 33 leaf가 사용하는 모드 PNG **53종 중 24종 실화소(45.28%)**, 나머지 29종은 추가 작업 필요. 모드 두 종류 합계 PNG 실화소 표본 **48종**. **807면의 UV 픽셀 실제 영역 검증·Minecraft 공식 client.jar·Macaw 공식 JAR·인게임 렌더 아직 미완료**. 상위 1단계 완료 판정 0/5.

**v19 신규 원본 분석:** Another Furniture의 v18 선정 **33 leaf에서 참조하는 고유 모드 PNG 53종** 중 전 단계까지 남은 **29종을 이번에 새로 직접 디코딩**, 표본 PNG **53/53(100%)**. 53 PNG 원본 전체 17,408픽셀(불투명 11,536·투명 5,872·부분 알파 0), 52종 16×16/1종 64×64. 제작자 고정 커밋 템플릿 JSON 30종 원본을 다시 읽고 SHA 확인 후 **807개 상속 면의 UV 원본**을 펼쳐, Another 모드 PNG에 해당하는 **804/804면(100%)의 실제 UV 사각형 RGBA**를 직접 검사. 비영 UV 중 **712면 전체 불투명/88면 혼합/0면 전체 투명**, **4면 0면적**; 픽셀 사용 중복 포함 32,531회(불투명 31,545/투명 986/반투명 0), 역방향 UV 221면. 바닐라 dirt 3면은 공식 PNG 미검증. Handcrafted v17 선정 모드 면 784/784와 합해 **1,588개 모드 PNG 참조 면 인스턴스**가 원본 UV 사각형 실제 RGBA 검증 완료. 모드 PNG 고유 실화소 총 77종(Another 53 + Handcrafted 24). **이 100%는 선정된 모델/PNG 표본 내 달성률**이며 전체 모드·인게임 렌더·Macaw 공식 JAR 미완료, 5개 세부 작업 최종 완료 0/5.

**v20 신규 원본 분석:** 제작자 Another Furniture 고정 1.21.1 원본에서 **v11 원형으로 선정했던 JSON 69/69개를 새로 전부 직접 읽어 원본 Git SHA·요소/면 수 일치 검증**. 기존 v18 선정 부모 30개 외 **39개는 이번에 직접 상세 조사**. 전체 **299 요소·1,362 선언 면**의 UV/회전/cullface/원시 bbox 분석 완료(역방향 UV **422면**, UV 회전 **134면**, cullface **443면**, 0면적 UV **4면**, 회전 요소 **17개**, 0두께 요소 **34개**, 0~16 밖 raw bbox 요소 **11개/3원형**). 이 **69/69은 선택 원형 집합 100%**일 뿐 원본 Git 트리의 1,451 모델 경로 전수가 아니다. 39개 새 직접 실측 부모는 **653면 raw UV**, 아직 leaf/PNG 실제 화소와 추가 연결하지 않음. **Macaw 공식 1.21.11 Fabric 3.4.2 Modrinth 릴리스 URL은 확인했으나 바이너리 다운로드 DNS 불가**, 실제 JAR 내부 모델 측정 **0개**. 기존 Another v19 선택 모드 면 804/804 UV RGBA와 Handcrafted v17 784/784 UV RGBA는 그대로. 전체 최종 완료 **0/5**.

**v21 신규 원본 학습:** Another Furniture 제작자 1.21.1 고정 커밋 **블록 상태 12개 SHA/802 model apply/114 고유 모델 경로**를 직접 재검증. 기존 선정 leaf 33에 없는 **새 leaf 38개 원본 JSON**을 직접 읽고 원형 부모 21종(이전 33 leaf 외 신규 부모 19종), 재질 override 97 슬롯 확인. 부모 상속 face **1,197인스턴스** 중 **모드 PNG 면 1,192/1,192 UV 실제 RGBA**, **바닐라 dirt 5면 공식 PNG 미검증**. 원본 모드 PNG 34종 재디코딩(이전 20/신규 14). 새 1,192 모드 면 1,086 전체 불투명/106 혼합, UV 참조 텍셀 32,784회(불투명 30,480/투명 2,304), SHA/원본 경계/픽셀 합계 검사 통과. **Another 누적 leaf 71종/PNG 67종/UV RGBA 1,996모드 면**, Handcrafted 합쳐 **원본 PNG 91종, RGBA 면 2,780개**. 기존 v20 69 원형 원본도 계속 유효. 바닐라 dirt Another 8면/oak_planks Handcrafted 2면 미검증, Macaw 공식 1.21.11 Fabric 3.4.2 JAR 실측 0, 인게임 검증 0. 전체 5 세부 작업 최종 완료 0/5. 원본 출처: `research/furniture_mods/v21/00_v21_블록상태12_신규완성형38_신규PNG14_면1192_RGBA_보고서.md`와 `research/furniture_mods/v21/v21_blockstate_new_leaf_rgba_audit.json`.

**v22 신규 원본 조사:** v21의 원본 블록 상태 12개(802 model apply, 114 고유 모델 경로) 중 `oak_shutter` 관련 이전 v18에서 읽은 1개 제외 **새 셔터 43 leaf 원본 JSON 직접 조회·Git SHA 기록**, 원형 템플릿 4종 재질 상속으로 **214/214모드 face UV 실제 PNG RGBA** 직접 조사. 43 PNG 원본 다시 읽기, 기존 1종·**신규 42종** 픽셀 조사. 모든 43 PNG **16×16 RGBA8 / 전체 11,008 픽셀 알파 255**, 모든 214면 원본 PNG UV 영역 불투명. 누적 Another **완성형 leaf 114개(33+38+43), PNG 109종(53+14+42), 모드 PNG 실제 UV RGBA 2,210면**. Handcrafted 24 PNG/784면 합계 **133종 원본 PNG / 2,994모드 면 실제 RGBA**. 이전 선정 블록 상태 12개 내 Another 모델 참조 **113/113 경로**(111 leaf, 2 template) 전부 제작자 JSON 근거 확보, 별도 Minecraft air 1 경로. **12/약177 상태만** 조사함. 공식 Macaw 1.21.11 Fabric JAR 다운로드 다시 시도했으나 cdn.modrinth.com DNS 실패, 실제 모델 0. 바닐라 dirt 8면/Handcrafted oak_planks 2면 공식 Mojang PNG·인게임 미검증. 최종 5 세부 작업 완료 0/5. 정본은 [v22 보고서](research/furniture_mods/v22/00_v22_셔터43모델_신규PNG42_UV214면_원본실측_보고서.md) 및 감사 JSON `research/furniture_mods/v22/v22_shutter_source_original_complete_audit.json`.

**v23 신규 원본 실측:** 이전 12 상태 밖 **10개 제작자 블록 상태 JSON 원본 직접 읽기/SHA**(386 model apply, 92 고유 경로: Another 91 + air 1), 신규 완성형 **51개 leaf JSON 직접 SHA 검사**(벤치16/소파12/커튼7/서랍2/테이블2/꽃상자8/의자4). leaf 자체 elements 0, 부모 원형 34개, `drawer/birch_open` 2단계 상속. 총 1,127 face의 상속·재질/UV 경로 해결(Another 자체 PNG **1,119면**, 바닐라 dirt **8면** 제외), PNG 참조 원본 51종 직접 조회(**42종 최초 실화소/기존9 재검증**, PNG 16×16 49종/64×64 2종), **1,119/1,119 모드 면 실제 UV PNG 내부 RGBA 확인**(전체불투명 **1,063면**/혼합 **56면**, UV 면적0/완전투명 0). UV 픽셀 사용 **41,666회** 중 불투명 **39,304/투명 2,362**(반복 텍스처 사용 포함). 빨강·파랑 소파 229쌍, 자작/가문비 벤치 116쌍, 의자 등받이2번 92쌍 원시 기하/UV와 면 알파가 같고 텍스처를 공유·교체하는 방식을 직접 비교. **누적 Another leaf 165/PNG151/모드 면3,329**, Handcrafted 합쳐 PNG175종/모드 면4,113. 신규 상태 모델 중 아직 JSON 직접 검증하지 않은 의자 leaf **39개**, 상태 파일 **155개** 남음. **공식 Macaw JAR/Mojang client.jar/인게임 미검증**. [v23 보고서](research/furniture_mods/v23/00_v23_추가블록상태10_신규51모델_42PNG_1119면실화소_보고서.md) · `research/furniture_mods/v23/v23_new_blockstate_leaf_png_face_original_audit.json`.

**바로 이어갈 일(애니메이션 보류):** v32에서 통·베틀·4작업대 7 leaf의 공통 `cube` 6면 상속, 42면 재질 연결, 원본 PNG25종 6,400 RGBA 픽셀과 6 blockstate/20 variants, 통 윗면 실제 132픽셀 차이를 검증했다. 다음은 **새로운 정적 가구형 3D 복합 요소 모델의 구조/명시·암시 UV/텍스처**와 **공식 Minecraft 1.21.11 client.jar 원본·게임의 정적 렌더/UV 방향·조명·컬링**을 조사. 사용자 재개 전까지 **모든 애니메이션 관련 새로운 조사 금지**, v32 암시 UV는 실제 게임 로더 검증 전까지 추론이라고 표시. 기존 모드 v24 자료 보존, 최종 완료 0/5.

이번 프로젝트 범위는 **상위 1단계(바닐라·모드 디자인 연구) 및 상위 2단계(근거 기반 디자인 규칙서)**까지만. Project Zomboid 가구 변환이나 실제 3D 가구 제작은 하지 말 것. 분석 근거와 추론/미검증을 항상 분리할 것.

---

만약 GitHub 연결이 없다면 읽기만 먼저 하고, 쓰기 작업은 연결 권한을 확인하세요. Handcrafted/Another Furniture 리소스는 각각 사용권이 제한되어 있으므로 원본 PNG·모델 JSON을 연구 저장소에 그대로 올리지 마세요.
