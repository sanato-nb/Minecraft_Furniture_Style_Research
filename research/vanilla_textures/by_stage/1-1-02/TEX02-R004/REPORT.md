# TEX02-R004 — 정적 상태 변형 31개를 186면으로 전개한 UV·면 슬롯 연구

**범위:** Minecraft Java 1.21.11, 재질 단계 `1-1-02` 석재·벽돌 17개만. 사용자 제공 [`1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/2a43897b8f605b4e0c96a272bca476ee6b70058e/1.21.11) 1차 원본, pinned commit `2a43897b8f605b4e0c96a272bca476ee6b70058e`; R001/R002 미러 및 R003 바이트 교차 검증은 역사적 증거로 보존한다. 공식 JAR 인증과 실제 인게임 검증은 계속 미완료.

## 신규 D3/E 실증: 31개 원문 상태 → 186개 변형별 면 레저

R002의 17종×6면 **기본 모델 102개**와 R002의 **31개 JSON 상태 배열 레저**를 교차 결합하고, R003에서 각 텍스처/모델/상태 소스의 SHA를 사용자 추출본과 대조한 근거를 사용했다. 이 과정에서 사용자 `1.21.11/`의 `stone.json`, `deepslate.json`, 부모 `cube.json`, `cube_all.json`, `cube_column.json`, `cube_mirrored.json`을 직접 다시 읽어 선택적 교차 확인했다. 나머지 15종의 JSON은 R003의 직접 대조 결과를 승계했다.

- 전체 source variant **31**, 정확한 중복 **2**, 구조상 고유 **29**.
- `31×6=186` **variant×model-local-face** 전개: `#all` **108**, `#side` **52**, `#end` **26**면.
- 명시적인 `[16,0,0,16]` U 반전 소스 **48면** (stone mirrored 12 + deepslate mirrored 36); UV 필드 생략/기본 생성 **138면**.
- 이번 결과는 **새 PNG나 RGBA 측정이 아닌 변형별 정적 모델 소스의 재구성**. R001의 4,352 RGBA 픽셀, R002의 102 기본 모델 면, R003의 사용자 추출본 PNG 17종 해시를 새 성과로 중복 집계하지 않는다.

### Deepslate axis=x의 원문 상태 중복

`1.21.11/assets/minecraft/blockstates/deepslate.json`에 명시된 `axis=x` 원본 4개 선언은 다음과 같다.

| 배열 인덱스 | 모델 | X | Y | 동일 선언 |
|---|---|---:|---:|---|
| 0 | deepslate | 90 | 90 | 기준 |
| 1 | deepslate_mirrored | 90 | 90 | 기준 |
| 2 | deepslate | 90 | 90 | **index 0과 동일** |
| 3 | deepslate_mirrored | 90 | 90 | **index 1과 동일** |

이로써 deepslate의 12개 블록상태 선언 중 구조적으로 **10개**가 고유하다(원본 x축 4개 중 2개 중복). stone의 4개 선언은 4개 모두 구분된다. 게임 실행에서 무작위 선택 확률이나 실제 스크린샷을 검증한 것은 아니다.

외부 [Mojang 버그 리포트 MC-312924](https://bugs.mojang.com/browse/MC-312924)에도 X축 deepslate의 유사 현상이 언급되어 있지만, 본 1.21.11 결론은 외부 보고가 아닌 **사용자 추출본의 실제 JSON 중복**에 기반한다.

### 모델 face → 예상 world face는 독립 계산 가설

`EXPANDED_VARIANT_FACES.csv`는 R002 모델 면의 슬롯과 R002 변형 각도를 합쳐 186개 행에 source-model/texture/각도 및 계산된 예상 방향을 보존한다. 가정은 X=east/Y=up/Z=south, X90에서 up→south, Y90에서 north→east, X 회전 적용 후 Y 회전이다. 이 모형은 deepslate `#end` 면이 `axis=x/y/z` 조건과 동일한 축을 차지한다는 필수 일관성 검사를 통과했다.

**유의:** 모델 원문의 면/슬롯 및 UV 유무는 소스 근거, `expected_world_face_math_hypothesis` 열은 수학적 추론이다. Blender/게임 엔진 렌더링 및 Minecraft 정적 화면을 실제 실행하거나 UV 꼭짓점/조명/uvlock 결과를 재현했다고 주장하지 않는다.

## F: 공식 게임 JAR 인증 — 계속 보류

Mojang 공식 `piston-meta.mojang.com` 매니페스트 및 `piston-data.mojang.com` 원본 JAR를 확인하려 했으나 현재 컨테이너 DNS 해석 실패, 웹에서도 공식 원문 취득 실패. 제3자 다운로드 색인에서 공개된 1.21.11 client.jar SHA-1 **후보** `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`는 비교 대상 정보일 뿐 공식 메타데이터/다운로드 파일 SHA-1을 인증하지 못했다. 사용자 추출본 폴더를 압축해 생성한 해시로 원본 JAR 바이트 SHA-1을 인증할 수도 없다.

- 사용자 제공 추출본 / 기존 미러 교차 검증: R003에서 **17/17**, 유지
- 원본 JAR SHA-1·Mojang 공식 메타데이터 인증: **0/17, 대기**
- 실제 인게임 정적 텍스처·UV·조명 검증: **0/17, 대기**
- A–G 전체 완료: **0/17, 대기**

## 다음 버전과 쓰기 경계

`TEX02-R005`에서는 공식 `client.jar` 압축본+버전 JSON 입수 및 SHA-1 실제 대조가 가능할 때 진행하고, 정적 게임 화면에 근거한 접합·UV 검사를 추가한다. 버전 R001/R002/R003과 통합 v38, 다른 재질/채팅 단계는 수정하지 않는다. 애니메이션·Project Zomboid 변환·실제 가구 3D 제작은 보류.
