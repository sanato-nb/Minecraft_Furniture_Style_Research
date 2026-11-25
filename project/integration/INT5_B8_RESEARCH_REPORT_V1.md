# INT-5-B8 — Handcrafted 검은 쿠션 의자 12번 요소, 원본/단일 제거 실게임 F2 연구

작성일: 2026-11-25 (KST). 직계 [INT-5-B7 Draft PR #119](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/119) head `26784200843b9ad50b7cc105a0df2bff0ec14608`에서 분기했다. `main`, 이전 연구 소스, 기존 B5~B7 감사 JSON 및 DB는 수정/병합하지 않는다.

## 1. 기존 누적 증거와 B8 정확한 목표

B7까지 원본 의자 부품 **45/45**, 소스 UV **229면**, 역할 그룹 **15개**가 별도 출처로 연결되었다. 독립 단일 소스 요소 제거→실게임 렌더 변화는 **B5 AF123 element4**와 **B7 AF121 element4**의 **2/45건**만 성공했다. 부품 기능·재질·스타일 최종 승인 **0/45**, 배타적 GPU 요소 픽셀 소유 확인 **0/45**, INT-6 원본 제삼자 AI 학습/재배포 권리 승인 **0**.

B8의 대상은 **Handcrafted `HC11210` / 소스 제공자 `HC13` / element index `12` / 소스 6면**, 기존 B3 원본 역할 가설 `SEAT_LAYER` 및 `chair/cushion/black_cushion` 텍스처 단서다. **실제 착석 가능·쿠션 재질·화면 pixel ownership을 여전히 증명하지 않는다.**

## 2. 공식 출시판 상속·텍스처 독립 원본 검사 완료

[**GitHub Actions #45542452464 SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45542452464). 실제 공식 Modrinth Handcrafted **Fabric 1.21.1-4.0.3** 출시 JAR의 전체 SHA-1 `a9579fecd7ed429c282be21d5c921d220197acc6`를 검증한 다음 JAR 내부 모델 자식→부모의 실제 경로와 136개 state variant를 열었다.

- 원본 블록상태 `handcrafted:warped_chair[facing=north,color=black,waterlogged=false]` → `handcrafted:block/warped_chair_black` 자식 → 공통 `handcrafted:block/chair/chair` 부모 **원본 13요소·78면**.
- 원본 element 12: 위치 `from=[3,9,2]`, `to=[13,11,14]`, **6면 모두** 실제 texture alias를 `handcrafted:block/chair/cushion/black_cushion`으로 해결.
- **부모 모델 Git blob SHA-1 `c5d9fbc054a897673f972fe2559376123751ba9b`는 연구 원본과 실행 JAR byte SHA가 실제 일치**. 검은 의자 자식의 출시판 SHA `2d989c0059a633a55ebe1386bf5c9547ccd86de7`.
- 별도 독립 대조 상태 `handcrafted:warped_chair[facing=north,color=white,waterlogged=false]` → `handcrafted:block/warped_chair_white` 자식; original white child Git blob `6000caa39ce50c3b71632e59cfb49d0dfe2c9737`. 두 자식은 같은 부모를 상속하지만 서로 다른 JSON. 역할 가설과 실착석 기능은 구분.

## 3. 실제 인과 실험 방법 및 판정 조건

- 동일하게 생성한 Minecraft Java 1.21.1 Fabric 일회성 세계를 **원본 공식 모드 JAR**로 첫 실제 클라이언트 실행하여 네이티브 F2 **8장** 촬영한다. 좌표 `(40,120,40)`, 두 대향 카메라 `south=(40.5,122.3,45.5,180,20)`, `north=(40.5,122.3,35.5,0,20)`.
- 각 카메라에서 **검은색 black 이전 → 미수정 white → 검은색 black 복원 → AIR**, 정확히 4단계 F2. 기존 게임 월드와 바이트 손상을 방지하기 위해 원본 세계 스냅샷을 저장 후 첫 세션 종료 시 재복사.
- 공식 출시 JAR의 내부 **검은 의자 자식 `assets/handcrafted/models/block/warped_chair_black.json` 한 파일만** 임시 교체해 부모의 element 12만 제외한 **12요소·72면 오버라이드**로 고정한다. 공통 `chair/chair` 부모, white 자식, 타 모드/텍스처 원본은 모두 uncompressed JAR member byte 불변·ZIP CRC로 재확인. 임시 모드 JAR/모델은 Git과 Actions 결과 아티팩트에 넣지 않는다.
- 동일 세계 초기 상태를 복원한 별도 게임 세션으로 두 카메라 F2 **추가 8장**, 합계 **원본8+수정8=16장**, 원본 Minecraft 서버 정확한 상태 **16건**, 게임 로그와 16개 PNG SHA를 독립 재확인한다.
- RGB ROI `(350,275)-(675,620)`에 임계값 24로 원본↔수정 검은 쿠션의 차이를 세고, **미수정 white / AIR 화면 두 세션 차이 모두 0**, 각 세션 black 반복 A/A 차이 0, 원래 검은 의자 전경 밖 변화 0을 요구한다.
- 모든 음성대조가 성립하고 두 관찰 시점 중 하나 이상에서 재현 가능한 비영(非零) 픽셀 변화가 실제 확인되면 **한정 렌더 인과 PASS**로만 기록한다. 그렇지 않으면 `CONDITIONAL` 또는 실패, B7 누적 기존 인과 **2/45 유지**.

## 4. 실제 작업과 파일
- `src/mcfr/int5_b8_hc_cushion_source_preflight.py`: 출시판 JAR 원본 핀, 선택 state/자식-부모 13요소·78면/6면 black 쿠션 texture 전개.
- `.github/workflows/integration-int5-b8-hc-source-preflight.yml`: [원본 검사 성공 Actions #45542452464](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45542452464).
- `src/mcfr/int5_b8_hc_cushion_element12_native_f2.py`: 같은 공식 출시판의 두 실제 클라이언트 실행, 16장 네이티브 F2, 검은 자식 하나만 수정, 백색/AIR 부정대조.
- `src/mcfr/runtime.py`: `int5-b8-hc-cushion12-native-f2` 실제 게임 명령 추가.
- `tests/knowledge/test_int5_b8_hc_cushion_element12_native_f2.py`: 11개 재현/반증용 테스트.
- `.github/workflows/integration-int5-b8-hc-cushion12-real-native-f2.yml`: [실제 Fabric 게임 F2 실행 Actions #45542711431](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45542711431).
- 실제 게임 PASS 및 음성대조 재검증 후에만 `project/integration/INT5_B8_HC11210_CUSHION12_REAL_F2_CAUSAL_AUDIT_V1.json` 영구 저장.

**기존 엄격한 INT-4 H03 HOLD, H05 CONDITIONAL, F70 무조건 승인 0/70 유지**. 이번 단계는 원본 모델·광원·화면 변화의 제한된 개입 인과만 다루며, 실제 앉기 기능·재질·스타일·GPU 각 face 픽셀 귀속·제삼자 AI 학습/재배포 권리를 승인하지 않는다. 본 PR은 Draft로 유지한다.
