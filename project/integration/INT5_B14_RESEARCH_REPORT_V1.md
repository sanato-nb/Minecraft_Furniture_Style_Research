# INT-5-B14 — AF123 등받이 원본 index9(5면) 단독 제거, 실제 Minecraft Fabric F2 독립 인과 실험

**기준일 2026-11-25 KST.** 직전 [B13 Draft PR #125](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/125)의 검수된 최종 HEAD `aa2f71fc82b08d051c00ce35e6b7aecedef722c9`에서 새 독립 브랜치로 분기했다. B1~B13 기존 연구 및 `main`은 수정하거나 병합하지 않는다.

## 1. 원본 출처/소스 정체

B3 원본 45요소 텍스처 역할명 증거와 B6 초기 후속 큐 **8순위**의 `AF123 / AF1394 / original_source_element_index=9` 선정. 원본 **5개 face**, `BACKREST_ASSEMBLY`는 원본 형상·`back_10/acacia.png` 텍스처 역할명에 기반한 연구 가설일 뿐 실제 등받이 기능, 재질, 스타일의 최종 승인이 아니다. 원본 증거는 해당 5 face를 사물 기능과 연결하거나 GPU 화면의 개별 원본 픽셀로 독점 귀속하지 않는다.

실제 Minecraft Java **1.21.1 Fabric**, 공식 Another Furniture **Fabric 4.0.2** JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`. 앞선 B5·B12·B13에서 공식 출시판 자식 `assets/another_furniture/models/block/chair/acacia_10_tucked.json`의 Git blob `71fd514e28b36b47b45cc6a38594b4d11059e6ff` 및 공유 부모 `assets/another_furniture/models/block/template/chair_tucked.json`의 Git blob `bbfd54f73fd764015ce320082ba531bd314a6dfd`를 실제 JAR 기준 고정했다. 연구 Git 4.0.3과 공식 실행판 4.0.2 원본 자산이 동일한 바이트라고 가정하지 않는다.

이번 B14은 **공유 부모 JSON을 건드리지 않고** 원래 부모의 전체 **10요소·46면** 중 **index9 요소의 정확 5면만 제외**한 나머지 **9요소·41면**을 `acacia_10_tucked.json` 단일 자식 JSON에 오버라이드한다. 실험용 JAR에서 변경된 uncompressed member가 오직 자식 모델 한 개인지, 동일한 원본 멤버 목록·ZIP CRC인지, 공유 부모·다른 자식·텍스처 등 기타 JAR 멤버의 압축 해제 바이트가 모두 불변인지 확인한다. 원본/임시 JAR·모드 원본 텍스처·원본 모델 JSON은 Git/아티팩트에 보관하거나 재배포하지 않는다.

## 2. 정상 tucked 의자 및 원본 F2 증거

AF123 북향 원본 상태는 `another_furniture:acacia_chair[facing=north,tucked=true,variant=10]`. 해당 상태가 원본 게임에서 유지되려면 **의자 앞의 `minecraft:oak_slab[type=top]` 지지**가 필요하다. 윗반블록을 제거한 tucked=true 의자란 불가능/자연 갱신되는 상태를 정상 대조로 사용하지 않고, 의자+슬랩 → 슬랩만 → 의자+슬랩 복원 → AIR 순서로 검증한다.

기존 [B4 원본 실제 Fabric F2 Actions #45528207751](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751)의 **원본 네이티브 F2 8장** ZIP artifact `14982648778` 전체 SHA256 `4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35`를 다시 내려받아 ZIP CRC, 원본 PNG 개별 SHA, 게임 로그, 원본 의자/슬랩 서버 상태 16쌍, 이미 GitHub에 저장된 B4 영구 감사 JSON과의 재계산 동일성을 확인한다.

신규 별개 공식 Minecraft 1.21.1 Fabric 클라이언트에서 동일 원본 북향 블록·윗반블록·남/북 카메라·시간/환경 조건으로 **신규 F2 8장**, 정확 서버 의자·지지 슬랩 원본 상태 **16쌍**, 새 PNG와 게임 client.log SHA를 기록한다. RGB ROI `[350,275,675,620]`, max RGB 채널 차이 threshold24. 원본·수정의 슬랩만/AIR·수정 A/A 시간 드리프트·원본 의자 전경 밖 화면 차이는 반드시 **0픽셀**, 독립 원본 요소9 제거 응답은 A와 A복원에서 재현돼야 범위 한정 인과 PASS이다.

## 3. 실제 구현 파일

- `src/mcfr/int5_b14_af123_backrest_element9_native_f2.py` — 4.0.2 소스 고정, `AF123/AF1394/9` 소스 정확성, 단일 자식 모델 오버라이드, B4 F2 원본 재개봉·새 게임 인과 픽셀 독립 감사.
- `tests/knowledge/test_int5_b14_af123_backrest_element9_native_f2.py` — **14개** 소스·B6 큐 8순위 정확 소스 ID·5 face·10/46→9/41·정상 tucked/slab·부정대조 및 권리 방어 회귀시험. 실게임 F2의 대체물이 아니라 코드 반증 시험이다.
- `src/mcfr/runtime.py` — 다른 AF121/H15 블록 대신 **AF123** 정상 지지 fixture를 선택하는 전용 `int5-b14-af123-backrest9-native-f2`, 기존 B5~B13 명령을 유지.
- `.github/workflows/integration-int5-b14-af123-backrest-element9-native-f2.yml` — 공식 1.21.1 Fabric 실제 F2·원본 ZIP SHA/CRC 및 기존 영구 감사·16 서버 상태/negative controls/권리 차단.
- [실제 B14 Actions #45562828175](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45562828175) — 성공 판정은 이 Actions가 종료되고 실제 원본 게임 F2/감사를 확인한 경우에만 추가한다.

## 4. 시작 시점의 연구 범위와 승인 경계

원본 모델 출처 검증 **45/45요소**, 원본 face/UV **229/229면**, 원본 역할 가설 연결 **15/15**. 개별 원본 소스 요소의 **실게임 단독 개입→화면 인과 검증 8/45(17.8%)**, 미실험 **37/45(82.2%)**; B14는 실게임 감사 통과 전 누적 증가에 포함하지 않는다. **원본 element/face의 배타적 GPU pixel 소유권 0/45, 부품 기능·재질·스타일 최종 의미 승인 0/45, INT-6 제삼자 자산 학습/재배포 권리 승인 0**, 엄격 H03 HOLD / H05 CONDITIONAL / F70 무조건 승인0/70 유지.

## 5. 실제 결과와 영구 감사

최초 착수 시에는 사전 승인된 화면 변화가 없다. 새 F2 8장 및 기존 B4 8장, 공식 SHA와 서버 16상태, 모든 음성대조를 실제 검수한 후에만 픽셀 수·제한적 PASS 또는 CONDITIONAL을 별도 영구 JSON으로 기록한다.
