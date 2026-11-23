# INT-4-H12 — Another Furniture 의자 variant 1/3 동일 방향·카메라 실제 시각 모델 검증

## 결론: 단일 모델링 비교 범위 통과

**실제 Minecraft Java 1.21.1 / Fabric / Another Furniture 4.0.2 원본 배포**에서 동일 세계 좌표·북향·`tucked=false`를 유지하고 블록상태 `variant=1 → variant=3 → variant=1(반복 대조) → minecraft:air` 순서로 네이티브 F2를 촬영했다. 세 번의 의자 상태는 게임 서버가 `/execute if block`으로 확인했고 네 번째 공기 상태도 서버 검증됐다. 수면, 파괴, 아이템 상호작용은 실험하지 않았다.

- [GitHub Actions 실제 실행 #45188982312](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45188982312): **전체 SUCCESS**. 신규 H12 9건 + 기존 H11 9건 회귀시험, Minecraft 클라이언트/서버 상태, 이미지·로그 SHA와 독립 감사, Draft 브랜치 안전 커밋까지 성공.
- [원본 이미지·클라이언트 로그 아티팩트 #14824678589](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45188982312/artifacts/14824678589): `v1.png`, `v3.png`, `v1_repeat.png`, `air.png`, `client.log`, 원본 실행 JSON, 독립 감사 JSON, 접촉시트. Git에는 게임 원본 PNG/JAR을 복사하지 않음.
- 실제 게임 원본 배포 SHA-1: `another_furniture-fabric-4.0.2.jar` = `c2f992081bdc4795ed6d87771a3b5f7c71103785`.
- 이전 H11 기준 원본 Git SHA: `57eb624cbb7f408d43398c7434b0d38d312cb55d`, H11 감사 Git blob SHA-1: `1869ee05afce779bd37233ba1cc74850d736160f`.
- 고정 카메라 `0.5 122.3 45.5 180 20`, 의자 좌표 `0 120 40`, 북향, Y 회전 0도. 두 모델의 실제 배포 JSON과 원본 4.0.3 연구 JSON은 해당 리프/부모/상태/텍스처에 한해 의미가 일치한다.

## 원본 비교 모델

| 항목 | A: variant=1 | B: variant=3 |
|---|---|---|
| 블록 ID | `another_furniture:acacia_chair` | 동일 |
| 방향, tucked | `north, false` | 동일 |
| 리프 모델 | `another_furniture:block/chair/acacia_1` | `another_furniture:block/chair/acacia_3` |
| 요소 수 | 10 | 10 |
| 면 수 | 46 | 46 |
| 기하·UV | 동일 | 동일 |
| 다른 바인딩 | `back_1/acacia` | `back_3/acacia` |
| 원본 RGBA 서로 다른 텍셀 | \- | 다른 54개 텍셀 |

H11에서 텍스처 바인딩이 다른 면은 12개였지만, 실제 차이 텍셀과 UV 겹침이 있는 면은 **2개**였다. 이 숫자는 원본 16×16 텍스처의 수학적 후보 범위이며, 실제 GPU 면별 픽셀 매칭이 아니다.

## 실제 네이티브 F2 독립 측정

RGB 채널 차이 임곗값은 **최댓값 24 이상**이며, 1024×684 PNG 원본에서 전체 화면 및 공기 대비 전경 마스크를 비교했다.

| 비교 | 원본 F2 차이 픽셀 수 |
|---|---:|
| A(variant1) ↔ B(variant3) | **808** |
| A(variant1) ↔ A(variant1 반복 통제) | **0** |
| A(variant1) ↔ 공기 | 3,552 |
| B(variant3) ↔ 공기 | 3,432 |
| A↔B 차이 중 의자 전경 마스크 안 | **808/808** |
| A↔B 차이 중 공기 전경 마스크 밖 | **0** |

- 실제 F2를 재열람하여 차이 픽셀 경계가 **화면 x=493~530, y=433~461**로, 화면 중앙의 의자 등받이 부분에 집중됨을 확인했다.
- `v1.png`과 `v1_repeat.png`는 **동일 SHA-256** `5e3d5494985e7af7dea54bc8b6ee3443c85a3146e30c3e459fb01d1ca6d2d31e`이다. 반복 대조에서는 촬영 노이즈가 0개였다.
- B의 SHA-256은 `a989c788990c0853773c4b729a58910896fcd027430ae37db7f4881db371c952`, 공기의 SHA-256은 `559bd5bc8161f5cb3a82a207971bc999f8bd4f1d7c2490d12ea207370288d301`.
- 실제 게임 클라이언트 로그 SHA-256: `39e826d0ac3bd1942c9a600ef555386c8e571871c557b0e19c31f62eb1880387`.
- 독립 감사 결과 `project/integration/INT4_H12_AF_NORTH_VARIANT_REAL_F2_AUDIT_V1.json`, 상태 `PASS_REAL_GAME_SOURCE_SELECTORS_AND_CONTRAST_SCREENED`. 해당 JSON은 GitHub Actions가 자동 생성·커밋한 실제 실행 결과다.

## 재사용 가능한 모델링 결론과 한계

**확인됨:** 같은 실제 게임 조건에서 `acacia_1`과 `acacia_3` 선택은 모델 기하나 UV 좌표를 바꾸지 않고, **등받이 텍스처 참조가 화면상 다른 외형을 만들어낸다**. 원본 소스 UV·픽셀 54개 차이, 게임 서버 상태, 동일 카메라 F2 808픽셀 변화를 함께 연결했다.

**미확인:** GPU의 각 화면 픽셀이 정확히 어느 부모 모델 요소·면·원본 16×16 텍셀로부터 나왔는지의 1:1 역투영. 모드 제작자의 남향 선택 의도나 설계 오류 여부. H11의 12면을 모두 각각 눈으로 검증한 것이 아님. 다른 색·회전·광원에서 동일한 픽셀 수가 나올 것이라고 주장하지 않는다.

**기존 판정 유지:** F70의 70/70 조건부·무조건 승인 0, H03 HOLD, H05 CONDITIONAL, H 전체 무조건 종료 0, INT5 실제 부품 의미 승인 0, INT6 AI 학습·원본 재배포권 승인 0. 과거 연구 원본과 `main` 변경·병합 없음. 신규 모드 업데이트는 고정 H12 범위를 덮어쓰지 않고 별도 회차에서 조사.
