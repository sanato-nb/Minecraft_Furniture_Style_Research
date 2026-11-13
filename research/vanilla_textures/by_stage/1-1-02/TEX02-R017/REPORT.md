# TEX02-R017 — 17종 석재·벽돌 블록 아틀라스·모델 스프라이트 정적 소스 검증 최종 보고서

작성일: 2026-11-13. 기준: 사용자가 직접 추출해 GitHub에 저장한 Minecraft Java 1.21.11 원본. 연구 단계 1-1-02. 기존 TEX02-R001~R016 결과는 보존.

## 최종 판정

**17/17개 지정 텍스처의 정적 소스 연구 범위 완료.** 아틀라스 디렉터리 선언, 모델 JSON 19개, 부모 모델 JSON 7개, 원본 PNG 19개, 31 블록상태 모델 선택 선언 및 각 6면(186면)을 연결했다. 사용자가 연구 완료조건에서 제외한 공식 Mojang JAR SHA-1 인증과 실제 인게임 렌더 검증을 수행한 것처럼 말하지 않는다. 애니메이션도 별도 보류한다.

## 1. 원본 모델·스프라이트·PNG 증거

블록 아틀라스 선언 원본: 1.21.11/assets/minecraft/atlases/blocks.json, Git blob 541ce56ad0b09f258963dd2bf3e3cb6e786d2d79. directory source=block, prefix=block/인 규칙을 원본 JSON에서 읽었다. 따라서 textures/block/X.png 파일은 minecraft:block/X라는 스프라이트 후보 ID로 연결된다. 이것은 런타임 stitch 성공을 의미하지 않는다.

선행 고정 TEX02-R013/BLOCKSTATE_CHOICE_SLOTS_31.csv(SHA 18f02c6f44fd18f2a522fca81b2f73ba7409f829)에서 모델 선택 선언 31개와 서로 다른 모델 19개를 얻었다. 그 19개 leaf 모델 파일을 다시 직접 읽고 7개 원본 parent JSON(cube_all, cube_mirrored_all, cube_column, cube_column_mirrored, cube, cube_mirrored, block)을 추적했다. face별 #all, #side, #end 등 texture alias를 parent→child 순서로 푼 결과 31×6=186개 로컬면의 스프라이트와 원본 PNG 경로가 전부 존재했다(누락 0). #particle은 실제 렌더 면으로 중복 계산하지 않았다.

기존 대상 PNG 17개에 별도 보조 표면 PNG 2개가 필요하다: blackstone_top(Git SHA 0dbc81f6e3045cfdfb1b58aa32d710f6fbaa286b)와 deepslate_top(Git SHA a560ccfb90cae70a1df6d2fd89d0c6405c2c4347). 이 19종 모두 원본 GitHub 트리에서 확인되었고, 19종의 .png.mcmeta 사이드카는 원본 트리에 없다. 면 사용 횟수는 stone 24, deepslate 측면 48 + deepslate_top 24, blackstone 측면 4 + blackstone_top 2, 나머지 14종×6=84, 합계 186이다.

## 2. 자바 원본 아틀라스 로더·베이크 경로

직접 열람한 사용자 원본 .class 9개와 Git blob SHA는 SOURCE_LEDGER_56.csv에 보존했다. ilw는 atlas source directory codec, ilv는 atlas JSON resource parsing, ily와 amm은 textures/block/*.png 목록과 sprite ID 변환, ilu$c는 sprite 공급자 연결, ilt는 PNG/optional metadata SpriteContents 생성, inx$c는 기본 model bake sprite resolver, hqn은 face별 resolver 호출과 hqi bake 입력, hqm은 atlas/sprite 수용 검사 및 미지원 경로에서 경고·fallback을 담당한다. 실제 근거 13개를 ATLAS_LOADER_SOURCE_CHAIN_13.csv에 기록한다.

주의: 소스 경로 존재/codec 입력 확인과 실제 게임 런타임의 리소스팩 선택, 아틀라스 크기, UV 좌표 배치, GPU 텍스처 필터링, 조명/인접 seam 성공은 다른 문제이다. 마지막 항목들은 실행 측정하지 않았다.

## 3. 증거물과 재현 범위

ATLAS_PNG_RESOURCE_MATCH_19.csv — 19 sprite↔원본 PNG 경로, SHA, face 참조 사용량, mcmeta 여부.
MODEL_PARENT_SPRITE_RESOLUTION_19.csv — 19 leaf의 parent chain·particle 및 6개 면별 texture ID.
MODEL_FACE_SPRITE_BINDINGS_186.csv — 31 모델 선택 슬롯별 여섯 local faces의 sprite resolution.
SOURCE_LEDGER_56.csv — 19 leaf JSON + 7 parent JSON + 19 PNG + 1 atlas JSON + 9 .class + R013 CSV = 56개 원본 SHA 원장.
ATLAS_LOADER_SOURCE_CHAIN_13.csv — 13개 원본 code/data 경로 증거.
VERIFY_R017_ATLAS_CLOSURE.py — 로컬 전체 원본으로 소스 SHA와 모델/face/PNG 개수 재현 가능. GitHub connector 기반 직접 JSON·클래스 분석은 실행했지만 이 독립 Python 검증기 자체는 전체 원본이 로컬 장착되지 않아 종단 간 실행하지 않았다.

## 4. 전체 진행도와 종료 원칙

R017 종료 후 석재·벽돌 17개 정적 소스 완료 17/17(100%), 인게임 확인 0/17, 공식 JAR 인증 제외, 애니메이션 보류. 새 고유 PNG 또는 픽셀 측정은 없고 앞선 기존 분석 결과를 중복 집계하지 않는다.
1-1 전체 11분류/150종 중 독립 단계 소스 범위 완료: 10분류/132종 = 88.0%. 미종결 1-1-01 목재·원목 18종. 전역 v39 통합 133/150은 다른 지표이며 기존 전역 v39를 수정하지 않았다. 저장소의 상위 5대 과제 최종 완료는 여전히 0/5로, 실제 좀보이드 가구 제작 진행률의 근거가 아니다.
R017은 이 17종의 최종 정적 소스 완료판이다. 새 독립 원본 증거나 사용자의 범위 변경 없이 R018을 임의 생성하지 않는다. 다른 단계/전역 v38·v39/과거 R001~R016을 수정하지 않는다.
