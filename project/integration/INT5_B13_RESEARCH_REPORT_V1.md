# INT-5-B13 — AF123 등받이 source index8(원본 5면) 단독 제거, 실제 Minecraft F2 엄격 검증

2026-11-25 KST. [B12 Draft PR #124](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/124) 최종 HEAD `7165a3d6934276947ec0154b886477466e9b6f94`에서 B13 신규 브랜치로 분기했으며 기존 B1~B12·`main`은 수정하거나 병합하지 않았다.

## 원본에 근거한 대상과 실험 경계

B3 원본 45개 요소 역할명 텍스처 원장과 B6 9개 후속 원본 큐의 **7순위** `AF123 / AF1394 / original element8` 선정. B3 원본 요소8은 **5개 face**, `BACKREST_ASSEMBLY`는 형상·원본 텍스처 역할 이름에 기반한 **가설**이며, 5면은 `back_10/acacia.png` 원본 텍스처명 단서로 연결된다. 출처 추적은 실제 물리적 등받이 기능, 재질, 완성 스타일이나 특정 GPU 렌더 픽셀의 배타적 소유 승인과 다르다.

원본 Another Furniture **Fabric 4.0.2** 공식 JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`; 원본 child `assets/another_furniture/models/block/chair/acacia_10_tucked.json` 원본 Git blob `71fd514e28b36b47b45cc6a38594b4d11059e6ff`, 실제 게임 원본 provider `assets/another_furniture/models/block/template/chair_tucked.json` Git blob `bbfd54f73fd764015ce320082ba531bd314a6dfd`를 고정한다. 연구 소스 4.0.3과 실제 게임 배포판 4.0.2의 JSON/모드 자산은 바이트 일치한다고 가정하지 않는다.

B13 단일 개입은 공식 배포판 공유 부모의 기존 **10요소·46면**에서 **source index8의 5면만** 생략하고 나머지 원본 **9요소·41면**을 딱 하나의 **`acacia_10_tucked.json` 자식 JSON**에 오버라이드한다. 공유 원본 부모 템플릿·다른 모든 모드 리소스·원본 텍스처는 수정 전후 uncompressed bytes 불변, ZIP CRC/멤버 목록 확인. 원본/임시 수정 JAR·제삼자 원본 텍스처·모델 자산은 Git 또는 실험 아티팩트로 배포하지 않는다.

## 정상 tucked 의자+지지 윗반블록 게임 상태

AF123 원본 북향 상태는 `another_furniture:acacia_chair[facing=north,tucked=true,variant=10]`이며, 앞쪽 `minecraft:oak_slab[type=top]`을 먼저 설치하고 그대로 보존해야 정상적인 상태로 유지된다. 슬랩이 없는 tucked=true를 유효한 원본 의자로 간주하지 않는다.

기존 공식 B4 [원본 유효 윗반블록 지원 Minecraft 게임 F2](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45528207751)의 정확 **8개 실제 네이티브 F2** ZIP artifact #14982648778 및 고정 ZIP SHA256 `4a50c784ecc7499546e5f4a23ef2b8de08a0d6fd8899cafc7b885a071d575e35`, ZIP CRC, 각각 PNG·로그 SHA와 원본 16개 chair/slab 서버 상태를 재검증한다. 기존 원본 B4 영구 감사 JSON과 재계산한 원본 실제 게임 감사가 동일해야 한다.

별개의 새 Minecraft Java **1.21.1 Fabric** 클라이언트에서 **남/북 두 카메라 각 4단계 = 새 F2 8장**, 원본 원래 북향 variant10 지원 슬랩을 보존한 `chair+slab → slab-only → chair+slab 복원 → air`을 촬영, 새 서버 의자·슬랩 **16쌍**, 게임 client.log 및 새 F2 SHA 확인한다. RGB 영역 `[350,275,675,620]`, 최대 채널 RGB 변화 임계값24. 슬랩만/AIR/새 게임 A/A 시간 drift/원본 의자 전경 밖 차이 **0**과 독립 요소8 제거 화면 반응을 만족해야 범위 한정 인과로 인정한다.

## 실제 GitHub 구현

- `src/mcfr/int5_b13_af123_backrest_element8_native_f2.py`: 원본 5면·부모와 자식 검증, 인접 슬랩 유효 상태의 원본 B4/F2 독립 감사, source8만 자식에 제외한 JAR 바이트 검수
- `tests/knowledge/test_int5_b13_af123_backrest_element8_native_f2.py`: **13개** 기하10/46→9/41, 원본 queue/B3 소스 역할 가설, 실제 슬랩, 부정대조, 권리/오승인 차단 회귀시험
- `src/mcfr/runtime.py`: `int5-b13-af123-backrest8-native-f2` 정확 명령, 다른 AF121/H15 실험 세계 대신 AF123 원본 tucked/B4 게임 fixture 선택, B5~B12 기존 실행 보존
- `.github/workflows/integration-int5-b13-af123-backrest-element8-native-f2.yml`: 실제 1.21.1 Fabric Minecraft와 공식 출처 고정 F2, 모든 원본 서버 상태와 음성대조를 확인한 후에만 PASS
- [실제 B13 Minecraft Actions #45561411530](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45561411530): 실험 완료 전 결과를 미리 주장하지 않으며, 최종 영구 감사 JSON은 실제 PASS·F2 증거 검사 후에만 생성한다.

## 시작 시점의 INT-5 누적 엄격 상태

원본 45/45 요소·229/229면 출처 연결, 15/15 역할 가설 그룹. 실게임 한정 렌더 인과 검증은 **7/45(15.6%)**, 개별 실험 미진행 **38/45(84.4%)**이며 B13은 아직 미포함. 개별 GPU face→pixel 독점 소유 승인 0/45, 실제 부품 기능/재질/스타일 최종 승인 0/45, INT-6 제삼자 학습/배포 권리 승인 0. H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70 유지.

## 실제 원본 F2 결과

Actions와 원본 SHA·실게임 정상 상태·두 카메라 화면 반응 및 모든 음성대조의 독립 검수를 성공한 경우에만 정확한 수치/판정으로 갱신한다.
