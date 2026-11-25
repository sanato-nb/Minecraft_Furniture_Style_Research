# INT-5-B19 — 화면 변화 미검출 원본 4요소를 동·서·남·북 실게임 F2로 한 번에 재시험

기준: 직전 [B18 Draft PR #130](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/130), 원본 45요소(229 faces) 전부 개별 소스 제거 시험 수행, 제한적 화면 반응 41/45, 남북 0픽셀 반응 미검출 4/45. 기준 HEAD `d1bf76be3178e9968c9b8b5362d0dfc4994e2d84`.

## 1. 한 번의 4개 소스 독립 배치

| 기존 미검출 원본 부품 ID | 모드 | 원본 face | 기존 남북 화면 픽셀 |
|---|---|---:|---|
| AF121/AF1393/5 | Another Furniture 4.0.2, 기본 acacia 의자 | 4 | 0 / 0 |
| AF123/AF1394/5 | Another Furniture 4.0.2, tucked acacia 의자 | 4 | 0 / 0 |
| HC11210/HC13/3 | Handcrafted 4.0.3, 검정 워프드 의자 | 6 | 0 / 0 |
| HC11210/HC13/4 | Handcrafted 4.0.3, 검정 워프드 의자 | 6 | 0 / 0 |

4개의 기존 미검출 개입 실험과 원본 45요소 source ID·원본 얼굴 수·역할 가설을 B3/B18 CSV에 고정. **원본 부품을 쓸모없는 요소 또는 렌더 버그로 단정하지 않는다**.

## 2. 4카메라 원본+수정 두 Minecraft 세션과 정확 대조군

- 정확 Java **1.21.1 Fabric** 공식 런타임. AF 4.0.2 JAR SHA1 / 부모 10요소 46면/child 하나만 격리(B15/B16 검증 코드 재사용). HC 4.0.3 JAR SHA1 / 부모 13요소 78면/black child 하나만 격리(B17 검증 코드 재사용). 임시 수정 JAR은 Git·Actions 아티팩트에 절대 배포하지 않음.
- 서로 다른 소스 네 개를 한 CI 매트릭스(max-parallel 4)에서, 각 job 원본 게임 1개와 원본 세계로 복원한 수정 게임 1개(**2세션**)로 촬영. 매 세션마다 **남·북·동·서 4방향 × 원본 A/음성대조/원본 A 복귀/AIR 4단계 = 16장 F2**. 전체 성공하면 **4요소 × 2세션 × 16 = 128개 실제 F2**, 정확 원본 블록 서버 확인 128개(기본), AF123은 지지 슬랩까지 매 프레임 검증.
- AF121: `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]` vs **미수정 variant3** 음성대조·AIR.
- AF123: `tucked=true,variant=10` 게임 원본 형태를 지키도록 **북쪽 앞칸 `minecraft:oak_slab[type=top]` 유지**; 원본과 slab-only, chair-with-slab 반복, 모두 빈 상태. chair 모델 실험을 위해 지지 슬랩을 제거하거나 불법 unsupported tucked 상태를 주장하지 않음.
- HC: 원본 `handcrafted:warped_chair[facing=north,color=black,waterlogged=false]` vs **미수정 흰색 의자** 음성대조·AIR. B8/B17 기존 확인 이슈인 색상 변경에 따른 드롭 아이템 엔티티를 **매 F2 전에 제거하고 원본 서버에서 entity 없음**을 검증.
- 모든 화면은 `1024×684` 정식 Minecraft F2, 출처 PNG SHA256·로그 SHA256·정확 서버 `[RenderAudit]` 표지. `ROI=(350,275,675,620)` 채널 차 임계값 24. 같은 뷰의 원본 A/B/A 시간 변화·변형 A/B/A 시간 변화·variant3/white/slab-only 음성대조·AIR·원본 전경 밖 변화는 모두 0이어야 한정 인과 PASS.
- 동/서에서 새 변화를 검출하면 **PASS_NEW_EAST_WEST_NATIVE_F2_BOUNDED_SOURCE_CAUSAL_RESPONSE**, 동서0이지만 남북 새 변화라면 별도 판정, 전부 0이면 **NO_VISIBLE_SOURCE_RESPONSE_WITH_STABLE_FOUR_VIEW_CONTROLS**, 통제 불안정·PNG 누락이면 실게임 근거 보류. **CI 성공과 실제 인과 PASS를 혼동하지 않는다**.

## 3. 실제 산출 코드·CI·독립 감사

- `src/mcfr/int5_b19_four_unresolved_four_view_f2.py`: 기존 AF/HC 검증된 모델 격리 함수를 정확 원본별로 선택하고 4방향/2세션 캡처·검증.
- `src/mcfr/runtime.py`: `int5-b19-four-unresolved-four-view-f2 --target AF121_5|AF123_5|HC11210_3|HC11210_4`; target별로 원본 게임 월드의 한 가구 블록 상태만 생성.
- `tests/knowledge/test_int5_b19_four_unresolved_four_view_f2.py`: 원본 상태·좌표·4방향·HF 드롭 아이템·slab 법적 지원·작업 범위 및 음성/반증 테스트.
- `.github/workflows/integration-int5-b19-four-unresolved-four-camera-f2.yml`: 4개 독립 작업을 병렬로 실제 Minecraft 실행. 수행된 신뢰할 수 있는 서버/화면 증거는 zip 아티팩트만 45일 임시 보존하고 영구 Git에는 SHA와 판정만 보존.

## 4. 승인 경계

이번 후속 실험은 **이전 B18의 남북 미검출을 정정해서 덮어쓰는 것이 아니라**, 새 동서 관찰을 별도 기록하는 방식. 화면에서 원본 부품 제거의 특정 위치 변화가 확인되어도 **원본 face/UV별 픽셀의 배타적 귀속·실제 가구 착석/물리 기능·재질·스타일·모델/텍스처의 AI 학습 및 재배포 권한**을 승인하지 않는다. 기존 엄격 **H03 HOLD / H05 CONDITIONAL / F70 무조건 승인 0/70**, 최종 의미 승인 0/45·INT6 제삼자 권리 승인 0을 유지한다.

실게임 완료 후 각각의 엄격 판정·실제 F2 ZIP 전체 CRC/PNG SHA·기존 45요소 원장의 **별도 4카메라 재검증 열**을 업데이트한다. 결과가 나오기 전에 새 인과 PASS 개수를 미리 집계하지 않는다.

## 5. B19 4요소 × 동서남북 × 공식·변형 두 게임 실제 F2 최종 확정

[최종 GitHub Actions #45664823385 (4/4 SUCCESS)](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45664823385), 실제 코드 HEAD `14246d3f0494f96a2387ec9a61f01d0ed4bb3bd4` 실행. 4개의 미검출 원본 요소를 각각 공식 마크 Java 1.21.1 Fabric 1게임 + 정확 한 원본 요소만 제거한 모델로 1게임, **8개 독립 클라이언트·128장의 신규 실제 F2·정확 서버 원본 블록상태 160건(AF123 지원 slab 32건 추가)·Handcrafted 아이템 엔티티 0개 서버 증명 64건** 검증.

| 원본 요소 | 기존 남쪽 | 기존 북쪽 | 신규 동쪽 px | 신규 서쪽 px | 새로운 4카메라 엄격 판정 |
|---|---:|---:|---:|---:|---|
| `AF121/AF1393/5` | 0 | 0 | **0** | **0** | **안정적 미검출** |
| `AF123/AF1394/5` | 0 | 0 | **0** | **0** | **안정적 미검출** |
| `HC11210/HC13/3` | 0 | 0 | **452** | **0** | **한정 인과 PASS** |
| `HC11210/HC13/4` | 0 | 0 | **0** | **390** | **한정 인과 PASS** |

**최종 4개 CI ZIP을 전부 새로 다운로드하여** ZIP CRC/중복, 원본과 변형 F2 **128개 개별 PNG SHA256·1024×684**, 8개의 원본·변형 게임 `client.log` SHA, 매 이미지 서버 `[RenderAudit]` 블록상태와 HC drop-item 없음, 정확 원본 모델 provenance, RGB ROI 24 경계·네 음성대조·A/A 시간변화 및 foreground 외 변화 수치를 독립 Python·Pillow/NumPy 코드로 재계산했다. **4 ZIP 전부 독립 재계산 결과=CI audit JSON, 음성대조 0**.

### 원본 형상과 동·서 신규 화면을 직접 대조한 연구 발견

- **HC11210/HC13/3**: 원본 `from=[14,6,4], to=[14,9,13]` → X축 두께 0인 평면. 이전 남북 0/0픽셀, **신규 동쪽 452픽셀**, 서쪽0. 원본 F2와 수정 F2를 직접 겹쳐보니 의자 좌면 아래 프레임의 시각 변화가 있다.
- **HC11210/HC13/4**: 원본 `from=[2,6,4], to=[2,9,13]` → X축 두께 0인 평면. 남북 0/0, 동쪽0, **신규 서쪽 390픽셀**, 반대쪽 하부 프레임의 변형이 확인됨. **X면 위치와 측면 관찰 방향이 가시성에 중요하다는 강한 증거**이나, face별 독점 GPU 픽셀 소유권이나 엔진의 유일한 원인 해석은 아니다.
- AF121 기본 의자 5번 `from=[13,2,3],to=[3,4,13]`; AF123 접힌 의자 5번 `from=[13,2,-6],to=[3,4,4]`. **두 원본 모두 X축 from 13 > to 3 역방향**. 공식 원본·변형 4방향 두세션에서 각각 **남·북·동·서 모두 0픽셀**이며 대조군 정상. 이전 source6이 화면에 반응했던 것과 달리, 역방향 소스5의 화면 미검출 원인은 **별도 B20 실험 필요**. 미사용·버그·face culling 확정 불가.

### 기존 45요소 상태 보존 후 B19 누적 결과

| 원본 가구 | source 요소/면 | 한정 렌더 인과 PASS | 4방향 포함 화면 변화 미검출 | 미시험 |
|---|---:|---:|---:|---:|
| AF121 기본 | 10/46 | 9 | 1 | 0 |
| AF123 tucked | 10/46 | 9 | 1 | 0 |
| HC11210 | 13/78 | **13** | **0** | 0 |
| MACAW67 | 12/59 | 12 | 0 | 0 |
| **총합** | **45/229** | **43** | **2** | **0** |

**한정 렌더 인과 43/45=95.56%**, 45/45 단일요소 개입 시도, 가시성 미검출 2/45. **물리적 부품 기능·재질·스타일 의미 0/45, 원본 UV/face 배타적 픽셀 귀속 0, INT6 제삼자 AI 학습/재배포 권리 승인 0, 엄격 H03 HOLD / H05 CONDITIONAL / F70 무조건 PASS 0/70** 불변.

이전 두 실패 Actions는 [회귀시험의 과거 0픽셀 공란 보정 필요 #45662975773](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45662975773), [128장 실제 F2는 촬영했지만 새 감사대기 상태를 CLI가 exit1로 반환한 #45663184282](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45663184282). 두 문제를 수정 후 `#45664823385` 최종 4/4 초록, 4개 새 ZIP 일괄 독립 감사 완료.

영구 메타데이터 결과 `project/integration/INT5_B19_FOUR_VIEW_REAL_F2_CAUSAL_AUDIT_FOUR_MODEL_V1.json`, `project/integration/INT5_B19_FOUR_MODEL_45_ELEMENT_STATUS_V1.csv`와 이 보고서. 이전 B18 원장의 남북 픽셀 기록은 **새 동서 결과로 덮어쓰지 않고 별도 B19 열에 보존**한다.
