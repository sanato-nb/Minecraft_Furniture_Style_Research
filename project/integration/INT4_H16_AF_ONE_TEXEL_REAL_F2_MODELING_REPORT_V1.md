# INT-4-H16 — Another Furniture 원본 텍스처 1텍셀 개입과 실제 F2의 인과 실험

## 목적: 원본 모델·UV에서 화면 픽셀까지 한정된 인과 입증

- 상위 연구는 프로젝트 좀보이드 → 마인크래프트 맵을 위한 바닐라 및 가구 모드의 **부모 모델·형상·블록상태·텍스처·UV·실제 렌더링 관계**를 반복 검증하는 것이다. 가구 기능 전체 플레이시험은 이번 범위에 추가하지 않는다.
- 선행 직계: [H15 Draft PR #94](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/94), head `ddb368f38bfed18f51e43554362ae1b9e7e10c4a`. 이번 H16은 독립 [Draft PR #95](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/95)로 작성했으며 `main` 미병합.
- 게임: **Minecraft Java 1.21.1 Fabric**, Another Furniture **4.0.2** 원본 공식 JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`. 원본 소스 연구 버전 4.0.3과 전체 동일성을 주장하지 않는다.
- 원본 의자 `another_furniture:acacia_chair[facing=north,tucked=false,variant=1]`, 변형 리프 `another_furniture:block/chair/acacia_1`과 음성 대조 리프 `acacia_3`. 블록 좌표 (-88,120,40)와 H15 카메라 위치 그대로 유지.
- H11/H14 소스 원장에 따르면 양 리프는 **10요소·46면·동일 형상과 UV**이고, 등받이 텍스처 바인딩 12면이 다르지만 차이 텍셀과 UV가 겹치는 원본 면은 요소7의 north/south 2면이다. 이 면의 기하학적 가시 방향은 카메라의 남북 위치로 좁혀지지만 GPU 픽셀별 UV 확정과는 다르다.

## 1. 변경한 원본 텍셀 딱 1개

| 출처·필드 | 원본 | H16 실험용 변경 |
|---|---|---|
| 소스 파일 | `textures/block/chair/back_1/acacia.png` | 동일 파일의 스크래치 복사본 |
| 원본 Git blob SHA1 | `55f3bbf986c0c10b731cc0e67038402f30340972` | 원본 blob은 변경하지 않음 |
| 텍셀 좌표 | **x=3, y=1** | 동일 |
| RGBA | **(173,93,50,255)** | **(255,0,255,255)** |
| 변한 RGBA 텍셀 수 | — | **1개** |
| 변경된 모드 JAR 내부 자원 | — | **해당 PNG 1개** |
| 그 밖의 원본 JAR 내부 압축 해제 파일 바이트 | — | **모두 동일** |

원본 공식 JAR를 먼저 SHA·내부 소스·원본 UV 자료로 검증한 뒤, **GitHub Runner가 만드는 폐기 전용 게임 폴더의 JAR 복사본만 임시 수정**했다. 따라서 실제 촬영 게임의 JAR SHA1은 `87d75176a8f87520463f5adc1238b8167a07bc7d`로 원본 배포 SHA와 다르다. 이는 의도한 스크래치 실험 변경으로, 수정 JAR·PNG 자체는 **Git 커밋이나 Actions 아티팩트에 담지 않았다**. 원본 공식 JAR, 소스 형상·UV·블록상태는 변경하지 않았다.

## 2. 최초 실패의 원본 검증과 원인 분리

- 먼저 별도의 임시 리소스팩을 이용했다. [최초 Actions #45243047820](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45243047820)은 실게임 F2 6장을 촬영했지만 **조건부 실패**로 종료했다.
- 실제 클라이언트 리소스 목록은 `vanilla, file/MCFR_H16_SINGLE_TEXEL_TEMP, fabric, another_furniture, ...` 순서였다. 리소스팩 **로드 로그는 존재했으나** 기존 H15와 비교한 모델1 화면이 남북 모두 **0픽셀 차이**였다. 즉 이 방법으로 **텍셀 개입 효과는 입증되지 않았다**.
- 단순 옵션에 리소스팩이 선택됐다는 사실이나 로그 로드만으로 GPU가 해당 자산을 사용했다고 승인하면 안 된다. 리소스 우선순위는 가능한 원인이지만 내부 구현의 확정된 인과로 승격하지 않았다.
- 해당 실패의 원본 F2·로그 아티팩트 [#14853290355](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45243047820/artifacts/14853290355), ZIP SHA256 `a32bfc58a9cdc9645ea5bb5d907b6680da77efb1636961e71a4a121a81b0fced`; 이 실패를 덮어쓰지 않고 남긴다.
- 후속으로 원본 배포 JAR를 사전검증한 뒤 스크래치 실행용 JAR의 텍스처 **RGBA 1텍셀만 변경**하는 방법을 사용했다. 나머지 JAR 자원들은 원문 바이트 비교로 동일함을 검사했다.

## 3. 최종 실제 Minecraft 실행 성공

- [**실제 Actions #45244056373 — SUCCESS**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45244056373), 실행 코드 커밋 `0d6a86aa72072d7704a3bcfb6be02be4b631ef82`. 새로운 실제 Fabric 게임 실행 **1회**, 네이티브 **F2 PNG 6장**, 각 단계 원본 통합 서버의 정확한 블록상태 **6개 확인**.
- H16 원본 텍셀 수정·출처 테스트 **8개**, H15 양면 카메라 원본 회귀시험 **8개**, H13 GUI 카메라 명령 회귀시험 **7개**. 총 **23개 성공**.
- 원본 성공 아티팩트 [**#14852517947**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45244056373/artifacts/14852517947), ZIP SHA256 **`58e2203b6a8ba849105555fee0898d184b8125d79da9cf47c319a0af481055cb`**. 원본 ZIP을 별도로 다운로드하여 **CRC 통과**, F2 6개 SHA256·PNG 1024×684 형식·클라이언트 로그 SHA·서버 exact-state 마커 6/6을 직접 재계산했다.
- 이전 정상 원본 대조군: [H15 아티팩트 #14851461698](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45239516512/artifacts/14851461698), ZIP SHA256 `4d674a097a2403f34da5c878c78f8a17e2b786a3d50fd945b5fca64fa755f462`. 두 실게임 실행 사이 의자 위치·원본 상태·시점·마인크래프트 버전은 고정되며 **변경 대상 파일·텍셀과 모델**만 구분한다.

## 4. 실제 F2 원본의 1텍셀 개입 효과

| 원본 F2 대비 조건 | 남쪽 카메라 (+Z) | 북쪽 카메라 (-Z) |
|---|---:|---:|
| **원본 모델1 ↔ 딱 1텍셀 변경한 모델1** | **20픽셀 변화** | **16픽셀 변화** |
| 변형하지 않은 모델3 음성 대조군 ↔ 원본 H15 모델3 | **0픽셀** | **0픽셀** |
| 변경한 모델1의 A-B-A 시간 대조 | **0픽셀** | **0픽셀** |
| 변경 픽셀 중 H15 원본 의자 전경 밖 | **0픽셀** | **0픽셀** |
| 개입으로 변한 화면 픽셀 경계 | **x512..516, y437..440** | **x508..511, y412..415** |
| 변경한 1텍셀의 새 픽셀과 H15 모델1↔모델3 임계 차이 픽셀의 겹침 | **0픽셀** | **0픽셀** |

- 화면 변경의 측정은 H15와 동일한 원본 **1024×684 네이티브 F2**, ROI x350..674 / y275..619, **RGB 채널 차이 24 이상** 기준을 사용했다.
- 특정 한 원본 텍셀의 색을 바꾸자 남쪽에서는 **5×4**, 북쪽에서는 **4×4**의 서로 다른 위치 화면 픽셀 덩어리가 바뀌었고, 변경하지 않은 다른 모델은 바이트 단위로 원본 H15 화면과 동일했다. 원본 텍셀의 화면 영향이 실제 렌더 클라이언트에서 관찰된 것이다.
- 매우 중요: 이번 새 화면 변화 **20/16픽셀은 기존 H15 모델1↔모델3의 808/692픽셀 변화 마스크(채널 임계 24)에 속하지 않는다**. 따라서 원본 모델1↔모델3 전체 차이를 이번 선택한 1텍셀로 설명하거나 808/692 전체를 UV 하나에 무조건 귀속해서는 안 된다.
- 새 게임 렌더와 원본 모델의 직접 대조는 **해당 1텍셀의 변화가 F2 해당 화면 영역에 영향을 주었다**는 한정된 개입 인과의 증거다. 반면 **특정 GPU 면 선택, UV 좌표의 정확한 보간 경로, 픽셀별 실제 텍셀 샘플/광원**은 아직 직접 추적되지 않았다.

## 5. 작업 산출물과 승인 경계

- 실행/감사 코드: `src/mcfr/int4_h16_af_single_texel_f2.py`; 런처: `src/mcfr/runtime.py`.
- 단위 회귀시험: `tests/knowledge/test_int4_h16_af_single_texel_f2.py`.
- 실게임 CI: `.github/workflows/integration-int4-h16-af-single-texel-real-f2.yml`.
- 실패·성공 원본 출처/픽셀/SHA 수치 원장: `project/integration/INT4_H16_AF_ONE_TEXEL_REAL_F2_CONTROLLED_SOURCE_RESULT_V1.json`.
- 원본 JAR 및 임시 수정 JAR·모드 텍스처는 Git/아티팩트로 배포하지 않았고, 실제 F2·게임 로그는 45일 보존 아티팩트에서 추적 가능하다.
- **F70 70/70 조건부, 무조건 승인 0/70**, H03 **HOLD**, H05 **CONDITIONAL**, INT-4 무조건 종료 0, INT5 가구 부품 의미 승인 0, INT6 AI 학습·원본 자산 재배포권 승인 0을 유지한다. GPU 인과 미검증과 라이선스 승인을 섞지 않는다.

### 다음 연구 방향

한 원본 텍셀 개입의 화면 영향은 남북 양쪽에서 확인했다. 후속으로 원본 요소7의 **north/south 개별 면에만 텍셀 참조를 달리하는 임시 모델 복사본**을 만들고, 원본 UV·면 방향별로 제한적인 재시험을 수행하면 면별 영향 범위를 좁힐 수 있다. 이 경우에도 실제 원본 JAR 구조의 임시 변경과 의도한 실험적 변경을 구분하고 모든 원본 자산을 보호해야 한다.
