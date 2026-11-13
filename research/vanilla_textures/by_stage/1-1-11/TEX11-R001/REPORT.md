# TEX11-R001 — 목재·구조부품 31개 독립 소스 검증 보고서

검증일: 2026-11-13. Minecraft Java Edition 1.21.11 표기 비공식 추출 미러 InventivetalentDev/minecraft-assets를 직접 읽은 결과다. 공식 Mojang client.jar 인증 또는 인게임 정적 관찰과 동일시하지 않는다.

## A. 출처·번호 원장
본 단계 STATE.json, v4의 150개 PNG 실측 CSV와 150개 고정번호 원장을 직접 교차 대조. 31/31 texture_id·path·v4 SHA 기록 일치. 신규로 미러 PNG 바이트를 직접 SHA-256 재해시하여 31/31 SHA 일치. Git blob SHA-1, 원본 파일 SHA-256을 별도 열에 보존. 역사적 v38 oak_shelf 7 leaf/7부모/38 UV면/32상태는 신규 분석 수량에 더하지 않았다.

## B. PNG 바이너리
PNG 서명·청크 CRC32·압축 픽셀 RGBA 복원 31/31 통과. 일반 문/다락문 26개 16×16, 선반 5개 32×32. acacia_trapdoor는 PNG 8-bit truecolor RGBA 타입 6, 나머지는 indexed palette 타입 3. bamboo_shelf는 예외적인 4-bit indexed 팔레트이므로 최초 8-bit 한정 디코더 실패 후 독립 Pillow 디코딩/SHA/CRC 통과. 공식 JAR에서 온 파일임은 인증되지 않았다.

## C. 화소·알파·휘도·반복
31개 신규 소스 PNG를 구성하는 원본 RGBA 픽셀 수 총 11,776 = 완전불투명(alpha255) 11,153 + 완전투명(alpha0) 623 + 부분알파 0. SOURCE_LEDGER.csv에 파일별 고유 가시 RGBA 색, sRGB 채널의 BT.709 가중 평균 휘도(선형광이 아님), 수평/수직 인접 RGB+A 채널 절대차 평균을 보존. 전체 반복 주기·타일 연결·회전 후 정합성은 별도 정적 검증 필요.

## D1. 문과 다락문
문 7쌍 top y=15와 bottom y=0의 알파 존재 열을 직접 비교. 알파 불일치 x열 수: oak0 / acacia0 / spruce0 / birch0 / cherry4 / bamboo0 / mangrove0. 같은 경계에서 양측 불투명 열 채널별 RGB 절대차 평균: 11.31/40.56/27.62/9.21/7.83/38.00/11.46 (0~255). DOOR_SEAM_D1.csv에 원값 보존. 알파 경계 일치는 문양 경계 일치가 아니다.
다락문 12종의 알파 및 bottom/top/open 모델 부모와 UV를 확인. 기하 source 범위는 bottom [0,0,0]→[16,3,16], top [0,13,0]→[16,16,16], open [0,0,13]→[16,16,16], 각 shared template 6 explicit UV faces. oak/dark_oak 2종은 일반 template_trapdoor_* 부모, 나머지 10종은 별도 template_orientable_trapdoor_*를 사용하며 상하면 UV 배열이 다르다. 문 7종 8리프/종은 8개 shared door 부모가 가진 [0,0,0]→[3,16,16] 5 explicit UV faces 및 top/bottom PNG 텍스처 슬롯을 참조.

## D2. 선반 32×32 atlas
oak/spruce/birch/cherry/bamboo_shelf 전부 32×32 alpha255 1,024픽셀. 모델 JSON의 UV 좌표는 0–16이므로 1 source UV=2 PNG 픽셀. 전면 overlay 5영역 unpowered[0,2,8,6], left[0,8,8,12], right[8,8,16,12], center[0,12,8,16], unconnected[8,12,16,16]. 각 16×8=128 original texels. 5종×5영역=25 직접 RGBA 크롭 평균 휘도는 SHELF_UV_REGIONS_D2.csv. 일반 16×16 타일보다 픽셀 수가 4배지만 단순 4조각 텍스처 배치라고 단정할 수 없다.

## D3/E. 정적 모델·상태·UV
신규 파생 spruce/birch/cherry/bamboo shelf 4×7=28 leaf 모델 JSON 직접 조회, 모든 leaf 자체 elements=0, 공유 template_shelf_* 7개 상속. 4종의 blockstates 24 multipart 규칙 각각 facing4×powered2×side_chain4=32조건, 총 128/128 source 정적 상태가 본체1/전면패널1을 선택한다. 4 item JSON은 shelf_inventory 모델을 참조. oak_shelf 7 leaf는 v38 기존 측정 재사용으로 중복 계산하지 않음.
공유 shelf template 7개 정의 합계 11 요소·38 explicit UV faces·2,304 UV texel-uses(한 PNG를 면별로 반복 크롭한 용량), UV 역전 x8/y8·cullface 23면. 이 숫자는 한 상태의 동시 렌더 면 수가 아니다. 문 blockstate 7×32=224 source variants/56 leaf 모델, 다락문 12×16=192 source variants/36 leaf 모델 직접 조회. 신규 leaf 총 120 JSON, blockstates 23 JSON, 공통 parent template 21 JSON, item JSON 4개. 각 상태/공통템플릿/아이템 JSON의 SHA는 MODEL_SOURCE_AUDIT.csv. 열린/닫힌 값은 정적 source 상태명이지 애니메이션 연구가 아니다.

## F. 공식 인증·실제 화면 한계
공식 Mojang 1.21.11 client.jar 파일 SHA 인증 0/31. 실제 인게임 정적 렌더 UV/컬링/조명/문 무늬 경계 확인 0/31. 현재 검증은 비공식 미러 자체의 파일 무결성·정적 JSON 연결 수준이다. 인게임 모습, UV 투영, 시각적 연결 여부는 pending. 애니메이션·키프레임·움직임 연구는 사용자 해제 전 보류.

## G. 저장/다음 릴리스
이번 독립 결과는 불변 경로 research/vanilla_textures/by_stage/1-1-11/TEX11-R001/의 SOURCE_LEDGER/DOOR_SEAM_D1/SHELF_UV_REGIONS_D2/MODEL_SOURCE_AUDIT/SUMMARY 및 본 REPORT에 기록. 수정 파일은 자기 단계 STATE/HANDOFF뿐이다. 전역 v38·다른 1-1-xx 및 루트 HANDOFF/PROGRESS/handoff STATE를 유지. A–G 전체 완료 또는 공식 게임 인증으로 표기하지 않는다.
다음 TEX11-R002에서는 공식 JAR 대조, 실제 게임 정적 모델 UV·알파·컬링 및 문양 연결, 원본 120 leaf별 상세 SHA 원장, 반복 주기·인접 무늬 정량성 검증을 이어갈 것.

### 근거 경로
- v4: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv
- v38: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_models/v38
- 미러: https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11/assets/minecraft
