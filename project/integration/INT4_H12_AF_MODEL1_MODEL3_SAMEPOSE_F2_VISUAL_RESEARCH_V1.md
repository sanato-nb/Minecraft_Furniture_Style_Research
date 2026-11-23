# INT-4-H12 — AF 의자 acacia_1/acacia_3 동일 카메라 실제 F2 시각 검증

## 실제 원본 촬영과 연구 목적

Another Furniture 의자 모델 연구 목표에 맞춰 **형상·텍스처·UV·블록상태 선택과 실제 렌더 결과**만 비교했다. 플레이어 앉기, 제작, 파괴, 수면 같은 게임 플레이 성공 여부는 검증하지 않았다.

- 실제 실행: [GitHub Actions #45183488267](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45183488267), 결론 **SUCCESS**.
- 게임 환경: 공식 Minecraft Java **1.21.1 Fabric**, Another Furniture **4.0.2** 실제 JAR SHA-1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`.
- 모델 연구 원본: Another Furniture 4.0.3 Git 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`; H11 전수 원본 UV/텍셀 감사 원장 Git blob `1869ee05afce779bd37233ba1cc74850d736160f`.
- 원본 인게임 상태: `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]` → `acacia_1`; `variant=3` → `acacia_3` 선택을 배포 JAR의 블록상태와 모델 JSON에서 확인.
- 모든 화면에서 **블록 좌표 (-88,120,40), 카메라 `-87.5 122.3 45.5 180 20` 동일**. 단일 실제 Fabric 게임 실행에서 모델1(A) → 모델3(B) → 모델1(A 재촬영) → 공기(AIR) 순서로 네이티브 **F2 PNG 1024×684 네 장**을 획득했다.
- 네 게임 블록상태 모두 통합 서버의 정확한 `/execute if block` 검사 마커 통과. 원본 클라이언트 로그와 PNG 각각의 SHA256, 원본 JAR 모델·텍스처 Git blob SHA, 원본 ROI 색상 차이를 독립 재계산·대조했다.

## 직접 검토한 실제 F2

| 같은 카메라 비교 | RGB 채널 최대 차이 24 이상인 픽셀 |
|---|---:|
| acacia_1 → acacia_3 | **808** |
| acacia_1 촬영 전 → acacia_1 복원 후 | **0** |
| acacia_1 → 공기 | 3,552 |
| acacia_3 → 공기 | 3,432 |
| acacia_1↔acacia_3의 차이 중 의자 전경 마스크 외부 | **0** |

- 측정 영역은 원본 PNG의 `x=350..674, y=275..619`; A/B 변경 픽셀 경계는 **`x=493..530, y=433..461`**.
- 원본 F2 네 장을 직접 열람하여 관찰: 동일한 목재 의자 형상이 유지되면서 **등받이 안쪽 가로판의 색 띠 배열**이 달라진다. 네 번째 AIR 화면은 가구가 없는 동일 바닥/하늘 배경만 보인다.
- H11의 원본 UV 추적에서는 바인딩 이름이 바뀌는 12면 중 **요소 7의 north/south 2면**만 원본 RGBA 변경 텍셀 54개가 UV 후보 범위와 겹쳤다. 이번 실제 화면은 등받이 영역에서 변화를 보였지만, **정확히 어느 화면 픽셀이 어느 UV 면에서 렌더링됐는지**까지 확정한 것은 아니다.

## SHA와 원본 별도 보존

- 성공 Actions 원본 [artifact #14822712371](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45183488267/artifacts/14822712371), ZIP **SHA256 `6b305bda1f8d9e02f417cb2b2f4c3600936ed7bb11e6e3d494d6c448e3a0d2a4`**, ZIP CRC 통과.
- 클라이언트 로그 SHA256 `3e0e08c217e83a2b7022f3db0929ea8f4731334edfde07d9221764f73bb99a9a`.
- `model1_before.png`와 `model1_after.png`의 SHA256가 둘 다 `5e3d5494985e7af7dea54bc8b6ee3443c85a3146e30c3e459fb01d1ca6d2d31e`로 **바이트까지 동일**.
- `model3.png` SHA256 `a989c788990c0853773c4b729a58910896fcd027430ae37db7f4881db371c952`.
- `air.png` SHA256 `559bd5bc8161f5cb3a82a207971bc999f8bd4f1d7c2490d12ea207370288d301`.
- 파생 독립 결과는 `project/integration/INT4_H12_AF_MODEL1_MODEL3_NATIVE_F2_INDEPENDENT_RESULT_V1.json` (Git blob `5e40040a13146ae08b97cf9d4747a6a08bc1d208`). 원본 PNG와 로그, JAR 원문을 GitHub에 커밋하지 않고 원본 아티팩트에만 저장했다.

## 연구 판정과 한계

- **검증 통과:** 원본 소스/배포 JAR에서 acacia_1/acacia_3 블록상태 선택, 동일 10요소·46면·UV 구조 및 12면 텍스처 참조 차이, 실제 Minecraft 화면에서 같은 의자 등받이의 가시적 픽셀 차이, A-B-A 시간 변화 대조.
- **미승인:** 바뀐 텍스처 원본 54개 텍셀의 GPU 실제 샘플링 경로, 특정 화면 픽셀과 원본 2개 UV면의 인과·가시성, 모드 제작자의 남향 예외 의도, Minecraft 버전/릴리스 전체 동등성.
- 기존 F70 **조건부 70/70, 최종 무조건 승인 0** 유지. H03 **HOLD**, H05 **CONDITIONAL**, H 최종 종료 0, INT5 의미·INT6 AI 학습/재배포권 승인 0 유지. 해당 한 사례의 화면 변화 증거를 전체 연구 최종 완료로 승격하지 않는다.

## CI 문제와 수정 이력

초기 [Actions #45182743278](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45182743278)는 10.8MB Mesa 패키지 다운로드 중 설치 180초 제한이 만료되어, **실제 게임 실행 전 환경 오류**로 중단됐다. 환경 준비를 X11 필수 패키지로 최소화하여 후속 **#45183488267 전체 성공**. 원본 F2·로그·검증 산출물은 이 성공 실행에서만 가져왔다.
