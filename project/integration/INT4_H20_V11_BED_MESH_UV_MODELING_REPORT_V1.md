# INT-4 H20 — V11 바닐라 침대 원본 JVM 모델 기하·UV·배치·재질 검증

## 판정
기존 F70 모델링 별도 계약 V1(40/70)에서 유일한 보류 V11을 해소한다. Minecraft Java 1.21.11 공식 Mojang client와 mapping SHA 고정, H19의 BED → BedRenderer 등록 증거 및 F11D 기존 실게임 F2 출처를 계승한다.

## 원본 직접 검증
- [공식 모델 bake 성공 Actions #45335224607](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45335224607): JAR 원본과 공식 라이브러리 55개 SHA1을 검증하고, 원본 BedRenderer.createHeadLayer()/createFootLayer() 및 LayerDefinition.bakeRoot()를 별도 JVM에서 직접 호출했다. root 2개, 실제 자식 파트 6개, 상자 6개, 사각면 36개, 면별 정점 144개. 원본 엔진에서 생성한 좌표·면 방향·정규화 UV·64×64 텍셀 경계 UV를 기록했다. 일반 JSON 요소/면 0/0 기록은 수정하지 않는다.
- 각 머리/발의 main 상자 로컬 크기는 16×16×6, 양쪽 leg 상자는 각각 3×3×3. UV 시작점 head main (0,0), left_leg (50,6), right_leg (50,18); foot main (0,22), left_leg (50,0), right_leg (50,12). 다리 회전은 원본 실제 baked PartPose 기록을 따른다.
- [공식 pose·material 검증 Actions #45335439554](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45335439554): 원본 BedRenderer.preparePose(false, direction), ModelPart.translateAndRotate, Vertex.worldX/Y/Z를 사용하여 사방×머리/발 **576개 변환 정점**을 검사했다. 개별 블록 경계 1×0.5625×1. 북향 F11D 배치(foot 원점, head z-1)의 합성 경계 [0,0,-1,1,0.5625,1], 폭1·높이9/16·길이2 블록. 각 다리 높이 3/16, 몸체 높이 6/16.
- 공식 Sheets.getBedMaterial(DyeColor.WHITE) 직접 호출: sprite minecraft:entity/bed/white, atlas minecraft:textures/atlas/beds.png. 원본 assets/minecraft/atlases/beds.json의 directory 규칙으로 assets/minecraft/textures/entity/bed/white.png에 정확 연결. PNG 64×64, SHA256 1766cde4551a3d91f38628dafe0c76fbb6bf2bc3a8301e715b4a2d149cff980e.
- 기존 [V11 실게임 F11D #45103243455](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45103243455): north, occupied=false 머리·발 정확 상태, AIR 대조 0, BED 대비 6446 픽셀, 원본 F2 4장. 이번 신규 게임/F2 0. 새로운 isolated JVM 모델 빌더/변환 실행은 실제 live renderer 호출 증거가 아니다.
- 초기 검사 오류: 서명된 기본 패키지 충돌 → 별도 mcfrprobe 패키지 사용; Vertex의 vector 필드 예상 오류 → 공식 매핑에 따른 x/y/z scalar 필드 읽기. 원본 JAR 변조 없음.

## 모델링 계약 V2
| 분모 | 범위 통과 | 조건부 | 보류 |
|---|---:|---:|---:|
| 역사 모델 | 34 | 28 | 0 |
| 위험 질문 | 7 | 1 | 0 |
| 모델링 검토 단위 | 41 | 29 | 0 |
| 기존 전체 F 승인 | 0 | 70 | 0 |

V11 행의 modeling_status·사유·증거·다음 작업만 변경한다. V1 및 과거 F/H 원장 보존. H03 HOLD, H05 CONDITIONAL, 기존 F70 무조건0, INT5·INT6 승인0. 전체 GPU 픽셀 원인, 실제 이전 F2 시점 Java submit 호출, 수면/파괴/충돌/의미/권리의 미승인 유지.

## 산출물
- INT4_H20_V11_BED_MESH_UV_RESULT_V1.json : 실제 bake 결과.
- INT4_H20_V11_BED_POSE_MATERIAL_RESULT_V1.json : 추가 배치·재질 해석 결과.
- INT4_F70_MODELING_CONTRACT_CASE_REVIEW_V2.csv / INT4_F70_MODELING_CONTRACT_SUMMARY_V2.json : V11 한 건 승격, 원본 ordinary 면 집계 보존.
- H20 재현용 Java probe 2개, Python 감사 3개 및 Actions. 원본 JAR·PNG·전체 디스어셈블은 저장소에 넣지 않는다.
- [원본 파생 결과 아티팩트 #14893197795](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45335439554/artifacts/14893197795).

## 다음 작업
AF 연구 Git 4.0.3 / 공식 Fabric 4.0.2 16개 사례의 선택 모델·부모·텍스처·UV 비교를 공통 부모별로 묶어 진행한다. 이후 과거 F2 출처 12개, R06 수면 애니메이션 1개. 남은 총 29개.
