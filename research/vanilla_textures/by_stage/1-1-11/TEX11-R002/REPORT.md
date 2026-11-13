# TEX11-R002 — 1-1-11 목재·구조부품 정적 PNG 반복·모델 JSON SHA 근거 보강

> 2026-11-13 · 독립 범위 31 PNG, Minecraft Java 1.21.11 표기 비공식 추출 미러 검증. **전역 v38 / 이전 TEX11-R001 불변.** Mojang 공식 client.jar 또는 실제 게임에서 검증한 결과가 아님.

## A — 원본·이력 대조
- GitHub 단계 `STATE.json`과 R001의 `SOURCE_LEDGER.csv` 실제 조회. 신규로 31 PNG 미러 Git blob SHA를 다시 확인했으며 **31/31이 R001과 일치**.
- 미러 `InventivetalentDev/minecraft-assets` 1.21.11 ref의 Git tree SHA `0c2358f50e81e34def33b75af34fc65409893dc0` (24,439 entries, truncated=false). 지정 31 PNG와 연결되는 120개 leaf JSON 경로를 실제 Git tree에서 조회.

## B — PNG 바이너리 새 검사
- 31/31 PNG 직접 다시 가져와 서명·chunk CRC32·zlib IDAT 압축 해제·PNG scanline 필터 복원 및 RGBA 픽셀 전체 복원 성공.
- 16×16 26개, 32×32 선반 5개. 특히 `bamboo_shelf`의 **4-bit 팔레트**도 nibble 디코딩으로 검사하여 누락 없음. 이전 R001 SHA-256 및 RGBA 기본 측정은 별도 기록으로 재사용.

## C — 새 RGBA 전체 정확 주기 및 가장자리 정량
- 각 이미지의 RGBA 픽셀에 `(dx,0)`, `(0,dy)` **순환 이동(toroidal wrap)**을 시행하고 전체 픽셀이 100% 정확히 일치하는 최소 양의 이동을 검출. 31종 모두 가로·세로 최소 완전 일치 순환 이동이 각각 **원본 너비·높이(16 또는 32)**와 같고, 더 작은 완전 일치 주기는 **0/31**.
- 같은 PNG 안에서 끝열 `x=w-1`과 첫열 `x=0`의 알파(0/비0) 불일치가 있는 텍스처 **0/31**. RGBA 전체가 행별로 같은 좌우 경계: `oak_trapdoor`, `spruce_trapdoor`, `acacia_trapdoor` 3개.
- 같은 PNG 안에서 끝행 `y=h-1`과 첫행 `y=0`의 알파(0/비0) 불일치는 **`cherry_door_bottom` 2열, `cherry_door_top` 6열**만 확인. RGBA 전체가 열별로 같은 상하 경계는 `oak_trapdoor` 1개.
- 선반 5종 아틀라스의 부분 일치율이 최대인 비영 수평 순환 이동은 **dx=16**이며 RGBA 일치율: oak 64.063% / spruce 65.039% / birch 62.695% / cherry 63.867% / bamboo 64.844%. **정확한 16px 반복이라는 뜻이 아님**(전부 100% 미만).
- 실제 31개 파일별 주기, 최선 이동량·일치율, 경계 평균 RGBA 차이, 알파 차이는 `PERIODICITY_C.csv`에 기록. 이 비교는 PNG 배열의 원시 픽셀에 대한 분석이며, 모델 UV·회전·조명·컬링·실제 게임에서의 이음새와 별개.
- **구분할 반례**: R001의 `cherry_door_top(y15)↔cherry_door_bottom(y0)` **서로 다른 PNG 사이** 경계 알파 불일치 4열과, R002의 `cherry_door_top` **같은 PNG 안** 끝행 불일치 6열 및 `bottom` 같은 PNG 안 2열은 측정 정의가 다르므로 서로 대체할 수 없다.

## D3/E — 120개 모델 leaf Git SHA 원장
- 문 7종×8개 leaf = **56**, 다락문 12종×3개 leaf = **36**, 참나무 선반을 제외한 비참나무 선반 4종×7개 leaf = **28**, 합계 **120/120** JSON 경로·Git blob SHA-1·파일 크기 모두 미러 Git tree에서 직접 확인 후 `LEAF_SHA_CENSUS.csv`에 보존. 경로 누락 없음.
- 그중 대표 **12/120개만 이번 릴리스에서 JSON 본문을 다시 fetch/parse**하여 실제 `parent`, `textures` 및 tree SHA 일치 **12/12** 직접 확인. 나머지 **108개는 이번 회차에 Git tree 메타데이터 수준만 확인**. R001의 '120개 직접 JSON 확인'과 달리 R002의 직접 본문 재검사 수는 12로 구분 기록.
- 선반 공유 template 38 explicit UV면, 2,304 texel-uses, 128개 비참나무 선반 정적 상태 검사는 R001/v38의 역사적 근거로 유지하며 R002 새 수치처럼 이중 계상하지 않음.
- `open`·`powered` 등의 JSON 상태명 분석은 정적 소스 검사이고 애니메이션 프레임/키프레임/움직임 분석이 아님.

## F — 공식 Mojang 1.21.11 client.jar 인증 경계
- 미러 루트 `1.21.11.json` Git blob SHA `b3abe8da90018d855f57dc76f51256df75dea68e` 내용을 실제 조회. **미러에 복사된 메타데이터**가 공식 JAR의 예상 SHA-1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`, 예상 크기 **31,152,600 바이트**, `piston-data.mojang.com` URL을 기재하고 있음을 확인.
- 그러나 `piston-meta.mojang.com`/직접 JAR 획득은 실행 환경에서 실패. **Mojang에서 직접 가져온 버전 메타데이터의 인증도 없고, 공식 JAR 전체 바이트 SHA-1 계산도 없음.** 비공식 메타데이터를 공식 검증 근거로 승격하지 않는다.
- 공식 `client.jar` 내부 PNG 31개 인증 **0/31**, 인게임 정적 렌더/UV/컬링 확인 **0/31**. 애니메이션 연구 전면 보류, 기존 동적 연구 삭제 금지.

## G — 이번 결과 저장 / 다음 작업
- 이번 전용 불변 폴더: `research/vanilla_textures/by_stage/1-1-11/TEX11-R002/`.
- 파일: `REPORT.md`, `PERIODICITY_C.csv`(31행), `LEAF_SHA_CENSUS.csv`(120행), `SOURCE_PROVENANCE.json`, `SUMMARY.json`.
- 다음 **TEX11-R003**에서는 Mojang 공식 client.jar 전체 SHA-1 및 내장 31 PNG 독립 SHA-256 확인, 실제 **정적** 인게임 UV/알파 이음선/컬링 검사, 필요 시 미재파싱 108 leaf JSON 본문 확인을 최우선으로 한다.
- 전체 고유 PNG 31개 외의 모델 JSON 수량을 완료 분자·분모에 합산하지 않는다. 전역 v38과 다른 단계는 수정하지 않으며 단계 A–G 전체 완료율을 추정하지 않는다.

## 출처
- [TEX11-R001 기존 실측](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R001)
- [추출 미러 1.21.11](https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11)
- [추출 미러의 복제 버전 메타데이터](https://github.com/InventivetalentDev/minecraft-assets/blob/1.21.11/1.21.11.json)
