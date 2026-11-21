# INT-2 1-3 원본 3개 가구 모드 독립 기하 감사 보고서

감사일: **2026-11-21**. 기준 `main@176f7f34de2336eb7984c4734e97b6eb156c19f4`.

**범위 판정: `PASS_SOURCE_GEOMETRY_CATALOG_SCOPE`**. [원본 첫 성공 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44861139384) 및 [면·지문 확장 검수](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44861333915)에서 확인했다.

## 실제 원본 확보·고정

- Another Furniture 4.0.3: 공식 저장소 `crispytwig/AnotherFurniture`의 Git 커밋 `57eb624cbb7f408d43398c7434b0d38d312cb55d`.
- Handcrafted 4.0.3: `terrarium-earth/Handcrafted`의 Git 커밋 `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`.
- Macaw’s Furniture 3.4.2 Fabric: Modrinth 버전 `xhmciaUD`, JAR SHA-256 `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e`.
- Mojang Java 1.21.1 공식 client JAR SHA-1 `30c73b1c5da787909b2f73340419fdf13b9def88`; Java 1.21.11 SHA-1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`.

세 모드 원본을 GitHub Actions Runner 임시 디렉터리에 다시 내려받았다. Git 소스의 각 모델 본문은 1-3-B Git blob SHA/크기, Macaw JAR 모델 엔트리는 고정 SHA-256/크기와 대조. 바닐라 부모 6경로의 SHA-256도 1-3-C 보조 원장과 비교. 원본 자산 자체를 저장소에 재업로드하지 않았다.

## 독립 계산과 전수 비교

기존 `analyze_geometry.py` 및 `audit_geometry.py`를 임포트하지 않는 [새 독립 계산기](../../scripts/integration/audit_int2_mod_geometry.py)를 사용했다.

| 검사 항목 | 과거 1-3 | 신규 독립 검산 | 불일치 |
|---|---:|---:|---:|
| Another 모델 원문 | 1,629 | 1,629 | 0 |
| Handcrafted 모델 원문 | 12,394 | 12,394 | 0 |
| Macaw 모델 원문 | 2,549 | 2,549 | 0 |
| **모델별 C 카탈로그·부모 계보 비교** | **16,572** | **16,572** | **0** |
| 모델별 정적 요소 확인 | 16,464 | 16,464 | 0 |
| 정적 요소 미해결 | 108 | 108 | 0 |
| 부모 경로 누락 | 48 | 48 | 0 |
| 고유 형상 제공자 | 300 | 300 | 0 |
| 형상 원본 선언 요소 | 1,911 | 1,911 | 0 |
| 형상 원본 선언 면 | 9,760 | 9,760 | 0 |
| 원본 면별 텍스처·UV·회전·컬링 등 | 9,760 | 9,760 | 0 |
| 순서 보존 형상 지문 종류 | 289 | 289 | 0 |
| 모델 상속 적용 요소 | 105,383 | 105,383 | 0 |
| 모델 상속 적용 면 | 592,312 | 592,312 | 0 |
| 텍스처 슬롯 미결합 적용 면 | 6,202 | 6,202 | 0 |

각 모델의 적용 제공자·자체/상속 요소·면·기하 등급·부모 종단·원본/회전 AABB·텍스처 슬롯·UV 존재 여부를 비교했다. 별도 형상 데이터의 **1,911개 요소**는 원본 from/to·축/각도·rescale·이중 수학식 AABB를 비교했으며 **9,760개 면**은 원본 UV 숫자·텍스처 슬롯·face 회전·cullface·tintindex를 대조했다. 형상 지문 300제공자에서 **289개의 고유 구조 지문**을 재산출해 C의 기존 SHA와 비교했다.

## 보존한 예외와 미해결 범위

- **부모 누락 48경로:** Another Furniture에서 네 경로의 `minecraft:lantern` 부모, Macaw에서 없는 `block/parent/desk` 및 `block/parent/drawer_base` 계보 44경로. 원본이 가리키는 대상을 멋대로 수정하지 않았다.
- **정적 형상 없음·미해결 108경로:** 생성 아이템/런타임 계열 58, 요소 없는 Handcrafted 기반 6, Macaw의 부모 누락 44경로. 여기의 44개는 위 부모 누락 48과 **중복 집계되는 별도 조건**이다.
- **텍스처 슬롯 미결합 6,202면:** 보류 및 템플릿 경로를 포함하므로 게임 화면이 6,202면 틀리다고 단정하지 않는다.
- 1-3-C의 역할 추정 부품 45개는 **시각·의미 정확성 재검수 미수행**이며 AI 제작 규칙으로 자동 승인하지 않는다.

[예외 상세 CSV](INT2_MOD_EXCEPTIONS.csv)는 두 예외 조건을 별도 행으로 보존한다. [재감사 JSON](INT2_MOD_SOURCE_SUMMARY.json)에는 108개 모델 ID·48개 부모 누락 ID·수치·검수 상태·전체 모델별 CSV의 SHA-256을 포함한다. 전체 **16,572개 모델별 CSV**는 GitHub Actions 아티팩트 `int2-1-3-original-model-geometry`에 별도 보존하며, **소스 원본은 포함하지 않는다**. 원장 SHA-256을 Git에 고정했고 매번 CI에서 신규 계산과 비교한다.

## 결과 해석의 경계

이번 `PASS`는 **고정 세 모드의 원본 기반 정적 형상·선언 UV·상속·AABB·지문 계산**의 독립 재현을 뜻한다. 다음은 여전히 이번 검증에 포함되지 않았다.

- 블록 상태 x/y 회전·연결/다칸 배치, 실제 게임 렌더·충돌·행동·물리.
- 원본 PNG 전체 화소 디코딩, 실제 픽셀-UV 대응·텍스처 해석(1-4 재검수 대상).
- 부품의 의미·심미 스타일·가구 기능 재현의 정확성. 데이터가 곧 AI 가구 생성 성능을 입증하지 않는다.
- 소스 라이선스의 AI 훈련/재배포 허용 여부. Macaw 권리 유보와 AF/HC의 비코드 자산에 대한 권리 조건은 별도 심사가 필요하다.
- 최신 모드 버전·새로 추가된 가구 전체에 대한 자동 적용. 이번 범위는 **고정 커밋·JAR**뿐이다.

## 다음

**INT-2 1-4**의 원본 PNG·픽셀 디코딩·UV 대응, 다음 **INT-2 1-5** 비교 규칙·반례 독립 재검수로 이어간다. 이후 INT-3 통합 DB에서 정적 A/B등급 증거와 시각·권한 미승인 상태를 분리한다.
