# INT-4-H14 — AF 의자 등받이의 원본 UV 면 방향과 실제 F2 변화 연결

## 연구 기준

- 선행 기준: [H13 Draft PR #92](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/92), head 052d5dbabe91704c6fe65ca32da31e7333f6fa7e. 본 연구는 해당 커밋의 직계 새 브랜치에서 진행하며 main에 병합하지 않는다.
- 실제 게임 화면: [H12 성공 Actions #45183488267 / 원본 artifact #14822712371](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45183488267/artifacts/14822712371), 원본 ZIP SHA256 6b305bda1f8d9e02f417cb2b2f4c3600936ed7bb11e6e3d494d6c448e3a0d2a4.
- 원본 모델: Another Furniture Git commit 57eb624cbb7f408d43398c7434b0d38d312cb55d, 모델 template/chair.json Git blob d9b64a818021f1a64b0cba13d16d18d6fea65d01.
- 원본 텍스처: back_1/acacia.png blob 55f3bbf986c0c10b731cc0e67038402f30340972 및 back_3/acacia.png blob e2282f2620fc8fbbcfd3bb69ab2a435e5421bbe8.
- 이전 단계 고정: H11 UV/텍셀 감사 blob 1869ee05afce779bd37233ba1cc74850d736160f, H12 실제 F2 감사 blob 5e40040a13146ae08b97cf9d4747a6a08bc1d208.
- 실제 배포 게임: Minecraft Java 1.21.1 Fabric, Another Furniture 4.0.2 JAR SHA1 c2f992081bdc4795ed6d87771a3b5f7c71103785. 연구 소스 4.0.3과 전체 버전 동등성은 주장하지 않는다.

## 1. 원본 모델의 카메라 방향상 면 후보

H11 원본에서 acacia_1과 acacia_3은 형상과 UV가 동일한 10요소·46면이다. 텍스처 참조는 12면이 다르지만, 달라진 원본 RGBA 텍셀 54개와 UV가 겹치는 면은 부모 요소 7의 north와 south **2면**뿐이다.

부모 요소 7은 from=[4,7,13], to=[12,16,13]인 Z축 두께 0의 등받이 중앙 평면이다. 원본 north UV=[0,0,8,9], south UV=[8,0,0,9]이며 south는 U가 반전된다.

실제 H12 의자 블록 좌표 (-88,120,40), 카메라 (-87.5,122.3,45.5), yaw=180°, pitch=20°를 대입하면 등받이 평면 세계 Z는 **40.8125**, 카메라 Z는 **45.5**다. 따라서 카메라는 +Z쪽이며, 원본 south 면(+Z) 1개만 기하학적으로 카메라 쪽을 향하고 north 면(-Z)은 반대 방향이다.

**판정: 원본 UV 2개 후보 → 카메라 방향상 south 1개 후보.** 이것만으로 실제 GPU face 선택·컬링·가시성이나 특정 화면 픽셀의 정확한 UV/텍셀 샘플을 확정하지 않는다.

## 2. 원본 텍스처와 실제 원본 게임 F2 재분석

| 측정 | 결과 |
|---|---:|
| 원본 back_1/back_3 RGBA 변경 | **54텍셀** |
| 알파값이 다른 텍셀 | **38텍셀** |
| 알파는 같고 색만 다른 텍셀 | **16텍셀** |
| 원본 변화 사각형 | x=0..7, y=0..6 |
| 원본 텍스처 y행 변경 수 | 6, 8, 8, 8, 8, 8, 8 |
| 같은 카메라 model1→model3 F2 차이 | **808픽셀** |
| model1→model1 재촬영 시간 대조 | **0픽셀** |
| 화면 변경 영역 | x=493..530, y=433..461 |
| 변경 픽셀 중 의자 전경 외부 | **0픽셀** |
| 변경된 화면 y행 수 | **25행** |
| 원본 네이티브 F2·exact 서버 상태 | **4장 / 4상태** |

알파값이 달라지는 **38개 원본 텍셀**은 배경 노출이 달라지는 가능성을 설명한다. 단, 화면 RGB 색상만으로 정확한 원본 면·텍셀의 GPU 샘플링 인과는 확정할 수 없다.

본 H14에서는 기존 H12 **한 차례 실게임 실행**의 네이티브 F2 원본 4장을 독립적으로 다시 열었다. 새로운 Minecraft 실행 1회 또는 신규 F2를 수행했다고 계산하지 않는다. 스크린샷, 원본 모드 텍스처·JAR·로그 내용을 연구 Git 저장소에 다시 업로드하지 않는다.

## 3. 구현과 검증

- 연구 분석기: scripts/integration/build_int4_h14_af_camera_facing_uv_f2.py
- 회귀시험: tests/integration/test_int4_h14_af_camera_facing_uv_f2.py — 소스 변경·위조 실패 조건, RGB·알파 차이, 카메라 방향, 원본 F2 서버 확인, 잘못된 승인 차단을 포함한 **8개 시험**.
- 결과 메타데이터: project/integration/INT4_H14_AF_CAMERA_FACE_UV_F2_SOURCE_BRIDGE_V1.json.
- CI: .github/workflows/integration-int4-h14-af-camera-facing-uv-f2.yml. 원본 H12 ZIP SHA256/CRC, 네이티브 F2 4개 SHA, client.log SHA와 원본 게임 서버 마커, 원본 Git blob 3개·H11/H12 blob 2개를 재확인하고 결과 JSON의 필드와 값 전체를 비교한다.
- 원본 H12 Actions artifact에는 유효기간이 있다. 만료 이후에는 같은 원본을 재검증했다고 주장하지 않고 신규 원본 또는 별도 합법적 장기 보존을 필요로 한다.

## 연구 승인 경계와 다음 단계

**H14 범위 결과:** source geometry와 camera 위치에서 south 면 1개 후보를 구분했고, 54개 텍셀 중 알파 변화 38개 및 실제 F2 변경 808픽셀을 다시 확인했다.

**미확정:** GPU별 픽셀→UV 면/텍셀 인과, 다른 카메라 각도나 남향 variant3의 실제 원본 F2, 다른 모드·버전 일반화, 모드 제작자 의도.

F70은 **70/70 조건부·무조건 최종 승인 0**, H03 HOLD, H05 CONDITIONAL, INT4 전체 무조건 종료 0, INT5 의미 승인 0, INT6 AI 학습·자산 재배포권 승인 0 유지. 앉기·수면·파괴 등 게임플레이 검사는 모델링 연구의 새 필수조건으로 만들지 않는다.
