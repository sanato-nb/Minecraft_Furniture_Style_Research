# TEX11-R003 — 사용자 제공 Minecraft Java 1.21.11 JAR 추출본 직접 검증

**연구일:** 2026-11-13 · **단계:** 1-1-11 목재·구조부품 · **고정 모수:** 기존 31 PNG · **이전 릴리스:** TEX11-R001/R002 원본 보존 · **다음:** TEX11-R004 · **전역 레거시:** v38 불변

## 출처 정정과 검증 근거 4계층

이전 R001/R002는 외부 비공식 추출 미러 `InventivetalentDev/minecraft-assets@1.21.11`에 대한 독립 연구였다. 사용자 설명에 따르면 현재 GitHub 저장소의 `1.21.11/` 폴더는 사용자가 Minecraft Java Edition 1.21.11 JAR을 직접 압축 해제하여 업로드한 추출본이다. R003에서는 **이 사용자 제공 추출본을 우선 읽어 실제 바이너리/JSON 검사를 수행**하며, 그 출처 주장은 사용자 진술에 근거한다.

1. **사용자 제공 추출본 검증:** 이 저장소 `1.21.11/assets/minecraft/...` 실파일을 직접 읽은 PNG 31/31·JSON 본문 48/48 + 관련 모델/상태 파일의 Git tree SHA 175/175 근거.
2. **미러와 교차 검증:** 사용자 제공 실파일에서 계산한 PNG SHA-256 vs 기존 v4/R001·비공식 미러 값 31/31 일치, 모델/블록상태/템플릿/아이템 정의 Git blob SHA 175/175 일치.
3. **Mojang 공식 원본 인증:** **미완료**. 완전한 원본 client.jar 원시 바이너리와 Mojang 서버에서 직접 검증한 버전 메타데이터를 결합한 SHA-1 검사가 수행되지 않았다. 풀린 파일들의 일치만으로 원본 압축 JAR의 SHA-1을 복원·증명할 수 없다.
4. **실제 인게임 정적 렌더 검증:** **미완료**. 게임 엔진 화면에서 확인한 UV·문양 접합·조명·컬링 데이터 없음. 애니메이션·키프레임·움직임 분석 계속 보류.

## A. 이전 독립 결과와 연결

- GitHub의 최신 단계 `STATE.json`은 R002/다음 R003으로 확인 후, R002 `REPORT.md`/R001 `SOURCE_LEDGER.csv`와 각 개별 JSON·PNG 원본 경로를 다시 확인하였다. 이전 실측(11,776 RGBA 픽셀, 선반 25 UV 크롭, 기존 31 이미지 주기 분석 등)은 이번 신계층 검증의 신규 측정량으로 중복 계산하지 않는다.
- 검증 중 소스는 해당 저장소 커밋 `2a43897b8f605b4e0c96a272bca476ee6b70058e`의 `1.21.11/` 스냅샷으로 고정했다. 경로별 소스 SHA를 CSV에 저장하므로 소스 추적과 재검증이 가능하다.

## B. 사용자 제공 PNG 31개 독립 바이너리·해시 검사

- `1.21.11/assets/minecraft/textures/block/`의 정확히 지정된 31 PNG를 커넥터로 **실제 base64 바이너리** 조회. 디코딩한 bytes로 직접 **SHA-256 독립 재계산** 및 **모든 PNG 청크 CRC32 검증**, PNG signature·IHDR의 폭/높이/bit_depth/color_type 확인.
- **31/31 실제 계산 SHA-256이 v4/R001의 기존 SHA-256과 일치, 31/31 PNG CRC 통과, 31/31 Git blob SHA가 기존 미러 파일 기록과 일치.** 원본 PNG 총 파일 크기 **8,080 바이트**, 16×16 26개·32×32 5개, `bamboo_shelf`만 4-bit palette.
- 사용된 SHA-256 구현은 `abc` 표준 테스트 벡터로 자체 검사한 후 적용. 이 검사는 PNG 원시 바이트의 별도 출처 인증을 추가한 것이며 기존 R001의 원본 화소/색상 측정값을 재측정 완료 수로 부풀리지 않는다.
- 항목별 사용자 저장소 경로, Git blob SHA, 직접 계산 SHA-256, 기존 v4 SHA, byte 수, 크기, PNG 메타데이터·CRC 결과를 `PROVIDED_PNG_SHA256_AUDIT.csv` 31행에 보존.

## C/D. 기존 픽셀·UV 실측을 새 출처에 연결

- 위 검증에서 사용자 제공 PNG 31개가 기존 연구 입력 PNG와 **byte-for-byte 동일한 Git blob SHA 및 계산 SHA-256**을 갖는 것으로 확인되므로, 기존 R001의 RGBA·알파·휘도와 R002의 순환 RGBA 반복/가장자리 측정은 사용자 제공 추출본에도 동일한 바이너리 입력 결과로 연결할 수 있다. **R003 신규 이미지 분석으로 별도 카운트하지 않는다.**
- D1: 문/다락문의 원본 픽셀 경계 및 7 문쌍·12 다락문에 대한 역사적 검사 유지; 실제 UV 회전 후 게임 화면에서 접합되는지 미검증.
- D2: 5종 32×32 선반 atlas의 기존 25개 UV 영역 크롭과 best x shift=16 부분 일치 결과는 **동일 바이트 입력의 과거 검사**로 연결. 새 시각 판정으로 세지 않음.
- D3: 기존 v38 `oak_shelf` 7 leaf는 역사적 참고 자료이고 새 120 leaf 계산에 다시 포함하지 않았다.

## E. 사용자 제공 정적 JSON 직접 검사와 175개 SHA 대조

- 사용자 `1.21.11/assets/minecraft/models/block/`, `blockstates/`, `items/`의 **정확한 175개 JSON**을 비공식 미러의 Git tree와 파일별 SHA-1(blob)·크기로 대조: **175/175 동일**, 누락/상이 없음. 구성: **문 leaf 56**, **다락문 leaf 36**, **비참나무 선반 leaf 28**, **blockstates 23**, **shared template 21**, **shelf item JSON 4**, **기존 참나무 선반 leaf 7 (역사적 참고)**. 따라서 168은 이전 독립 원장에 기록된 대상 소스들이고 7은 기존 v38 참고; 175를 PNG 작업 분모로 추가하지 않는다.
- 사용자 추출본의 블록 상태 JSON 23개, 공통 template JSON 21개, 선반 아이템 JSON 4개를 새로 **직접 열어 유효 JSON 파싱 48/48** 및 R001의 해당 소스 SHA 48/48 일치; 각 파일의 `variants` 키 수 / `multipart` 규칙 수 / 실제 explicit UV면 수 / item model slot을 검증하여 **기존 파일별 명시 수 48/48 일치**.
- 새로 읽은 사용자 추출본 blockstate의 규칙/변형 정의 합: 문 7×32 = **224 variants**, 다락문 12×16 = **192 variants**, 선반 파생 4×24 = **96 multipart rules**. JSON template 21개의 explicit UV면 수 총 **114** (=선반 38 + 문 8×5=40 + 다락문 계열 6×6=36). 이 숫자는 **정적 JSON 출처에서 센 정의 항목**이며 인게임 동시 렌더링된 면 수나 개별 상황 조합 수가 아니다.
- 나머지 **leaf 120개와 기존 참나무 leaf 7개**는 R003에서는 **Git tree SHA/크기로 전체 본문 바이트 동일성**을 대조했다. 이 회차에서 127개의 JSON을 전부 새로 파싱했다고 주장하지 않는다. 모델 JSON 내용의 기존 미러 직접 파싱 내역은 R001/R002에서 계속 인용하되 출처와 회차를 구분한다.
- `PROVIDED_MODEL_JSON_SHA_CENSUS.csv` 175행과 `PROVIDED_STATIC_JSON_AUDIT.csv` 48행에 경로·해시·소스·검증 세부 기록.

## F. Mojang 공식 배포본·실제 게임의 구분

- 사용자 제공 추출본의 PNG·JSON이 기존 미러와 동일해도 **'Mojang 공식 client.jar 인증'은 0/31** 유지. 이전 R002에서 미러에 복제된 `1.21.11.json`이 명시한 예상 client.jar SHA-1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`는 현재 확인된 공식 JAR 파일 해시가 아닌 **추출 미러 메타데이터의 기재 값**이다.
- 추출 폴더만으로는 ZIP 메타데이터, 압축 방법, 원본 파일 순서 등이 보존되었다고 증명할 수 없으므로 원본 `client.jar` SHA-1을 계산할 수 없다. Mojang 서버의 직접 메타데이터 조회·JAR 전체 파일 검사 미수행.
- 인게임 정적 UV 투영/조명/알파 문양 이음선/컬링은 **0/31 확인** 유지. JSON source에서의 모델 상태명 `open`은 정적 상태 매핑이며 애니메이션 분석으로 확대하지 않는다.

## G. 저장 범위와 다음 단계

- 신규 불변 경로: `research/vanilla_textures/by_stage/1-1-11/TEX11-R003/`.
- 새 파일: `REPORT.md`, `PROVIDED_PNG_SHA256_AUDIT.csv`, `PROVIDED_MODEL_JSON_SHA_CENSUS.csv`, `PROVIDED_STATIC_JSON_AUDIT.csv`, `PROVENANCE_LEVELS.json`, `SUMMARY.json`. 갱신은 이 단계의 `STATE.json`, `HANDOFF.md`만 허용.
- 다음 **TEX11-R004** 우선 항목: 공식 원본 `client.jar`의 전체 원본 바이트(가능하면 사용자 제공)를 공식 Mojang 버전 메타데이터와 **독립 SHA-1** 대조, 실제 Minecraft 정적 렌더/UV·문양 접합·컬링 실험 증거가 확보되면 독립 단계로 검증, 그 전에는 미검증 유지.
- 이전 `TEX11-R001`, `TEX11-R002`, v38, 다른 1-1-XX, 프로젝트 공통 루트 문서를 수정하거나 이전 데이터 삭제하지 않음. Project Zomboid 변환·실제 가구 3D 모델 제작·애니메이션 연구 진행하지 않음.

### 고정 소스와 선행 원장
- 사용자 제공 폴더: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11
- 비공식 미러: https://github.com/InventivetalentDev/minecraft-assets/tree/1.21.11
- 이전 R001: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R001
- 이전 R002: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R002
