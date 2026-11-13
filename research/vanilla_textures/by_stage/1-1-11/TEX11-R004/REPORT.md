# TEX11-R004 — 사용자 제공 추출본 정적 모델 리프·상태·UV 연결 심화 검증

**날짜:** 2026-11-13 · **범위:** 1-1-11 / 목재·구조부품 31 PNG · **이전:** TEX11-R003 · **다음:** TEX11-R005 · **상위 체크포인트:** v38 변경 없음

## 새로 수행한 분석의 범위와 출처 등급

이번 R004는 R001/R002의 외부 미러 분석과 R003의 **사용자 제공 `1.21.11/` 추출본 PNG 31개 실바이트 SHA-256·CRC/관련 JSON 175개 Git SHA 대조 및 JSON 48개 직접 파싱** 결과를 모두 보존하며, **R003에서 사용자 제공 추출본의 실제 JSON 본문을 열지 않았던 모델 리프 127개** 및 UV의 명시 좌표·정적 상태 참조를 추가 검증한다.

주 분석 입력은 **`sanato-nb/Minecraft_Furniture_Style_Research/1.21.11/assets/minecraft` 사용자 제공 추출본**이다. 모델·상태 관련 SHA-1은 Git blob 내용 무결성 체크 및 과거 Git 원장 대조이며, 실제 Mojang 배포 JAR 컨테이너의 SHA-1과 전혀 다른 개념이다.

## A. 계승 및 중복 방지

- 고정 대상 PNG **31개**, R003의 사용자 제공 PNG 31/31 SHA-256/CRC 대조 유지. R004에서는 PNG 전체 바이트를 **다시 SHA-256 계산하지 않았으므로 신규 PNG 검증 0건**. 원본 픽셀 11,776개, 선반 25 UV 크롭, 이전 주기 분석을 신규로 추가 집계하지 않는다.
- R003의 175개 관련 JSON Git SHA 기록을 입력 원장으로 사용하되, 이번 회차에 **127 leaf JSON 본문 직접 읽기**와 **23 blockstates 모델 연결 직접 재평가**, **21 template UV 및 geometry 직접 좌표 검사**를 각각 새 증거로 만들었다.
- v38의 참나무 선반 leaf 7개는 여기서도 **역사적 참고 그룹**으로 고정. R004의 새로운 독립 1-1-11 leaf 본문 검증 수는 **120**이다(문56, 다락문36, 비참나무 선반28). 참고 leaf 7개는 신규 표본에 더하지 않는다.

## B/C. 텍스처 파일 자체

- 출처는 R003에서 독립 SHA-256을 계산하여 확인한 사용자 제공 PNG 31개로 고정. R004의 새 바이트/색상/알파 반복 측정은 없으며, 이 동일한 바이트의 R001/R002 측정을 출처별로 계승했다.
- PNG가 실제 모델 리프의 `#bottom/#top/#texture/#all` 슬롯으로 참조되는지 새로 확인한 결과는 뒤의 E와 `TEXTURE_REFERENCE_COVERAGE.csv`에 있다.

## D1/D3 / E1. 127개 리프 JSON 본문 직접 검사

- `1.21.11/assets/minecraft/models/block/`의 총 **127/127개 모델 리프 JSON 본문**을 이번 회차 실제 조회·JSON 파싱. 각 파일의 Git blob SHA가 R003 기록과 일치하는지, `parent`가 해당 문/다락문/선반 형태 템플릿인지, 실제 `textures` 슬롯 값이 지정 재질 경로와 정확히 일치하는지, leaf가 예상 밖의 독립 `elements`를 추가하지 않았는지 검사: **각 항목 127/127 통과, 오류 0**.
- 구성: 문 7재질×8 = **56 leaf**; 다락문 12재질×3 = **36 leaf**; 비참나무 선반 4재질×7 = **28 leaf**; 별도 v38 참고 oak_shelf 7 leaf.
- 문 leaf의 `bottom/top` 2 PNG 슬롯은 정확히 해당 목재의 문 상하 PNG를 가리키며, 다락문 `texture` 슬롯은 각 목재의 다락문 PNG, 선반 `all` 슬롯은 5종 32×32 PNG와 대응한다. 선반 `particle` 슬롯은 `stripped_...log/block` 텍스처를 따로 참조하며 고정 31 PNG 외부이므로 이 회차에 추가 PNG 샘플로 넣거나 별도 해시하지 않았다.
- **`LEAF_MODEL_DIRECT_AUDIT.csv`**: 127개 실파일별 경로·SHA·실제 parent·textures·예상값·개별 판정(참나무 역사적 그룹 포함).

## D2/D3 / E2. 공유 템플릿 21개 UV 좌표를 실제 재판정

- 직접 사용자 제공 템플릿 JSON 21개를 다시 열고 해당 재질의 PNG 실원본 크기(문/다락문 **16×16**, 선반 **32×32**)에 따라 원본 좌표의 UV=0~16을 픽셀 단위(16px에서 1:1, 32px에서 1:2)로 변환하여 **명시 UV 114개 면 전부** 다음을 계산: ① UV 네 좌표 0~16 범위 내, ② UV 면적 양수, ③ 원본 PNG 픽셀 경계 정렬(스케일 반영한 정수 좌표), ④ 예상 leaf 슬롯(`#bottom/#top/#texture/#all`)와 일치, ⑤ 회전은 90°의 정수배, ⑥ 이전 Git SHA와 일치.
- **114/114면 모든 정적 검증 통과, 범위 밖/슬롯 미해결 0건**. 그룹별 명시 면은 선반 38, 문 40, 다락문 36. `TEMPLATE_UV_FACE_VALIDATION.csv`에 면별 좌표, 역전 여부를 재계산할 수 있는 원값, cullface, 회전, 소스 텍셀 UV 면적을 남겼다.
- 공통 템플릿 그룹별 UV 참조 면적 총합(**중복 샘플 포함**)은 선반 2,304 texel-uses(32×32 PNG 기준), 문 5,248, 다락문 4,224. **파일의 고유 PNG 픽셀 수나 화면 실제 보이는 면 수가 아니며**, UV가 같은 부분을 여러 번 참조하면 누적 집계된다. 합계 11,776이라는 숫자가 과거 원본 31 PNG의 총 픽셀 수 11,776과 우연히 같더라도 분자·측정 정의가 전혀 다르므로 동일시하지 않는다.
- 모델 `elements`도 **총 25개** 직접 점검하여 `from/to` 범위 0~16, `from<=to` 및 실제 faces 존재 여부 **25/25 통과**. 이 중 `template_shelf_center/left/right/unconnected/unpowered` 5개는 앞뒤 깊이가 **0인 평면**으로, 면 렌더용 소스 구조이며 임의 오류로 처리하지 않았다. `MODEL_ELEMENT_GEOMETRY.csv`에 좌표 및 판정 기록.
- 위 판정은 JSON 소스 UV 좌표의 정확성이지 GPU 샘플링/조명/컬링/이미지의 실제 접합 결과가 아니다.

## E3. 23개 블록상태의 총 512개 모델 참조 직접 검증

- 사용자 제공 추출본의 실제 **blockstate 23개 JSON**을 열어 총 **512개** source 규칙/variant를 전수 판정: 문 7×32=224, 다락문 12×16=192, 비참나무 선반 4×24=96. 각 모델 참조가 추출본 리프 목록에 존재하는지, 상태 속성에 따른 예상 leaf 이름과 일치하는지, x/y 회전이 90°의 정수배인지, 소스 SHA가 R003과 일치하는지 전수 검사: **512/512 통과**.
- 선반 4재질에 대해 facing4 × powered2 × side_chain4 = **128 정적 입력 조건을 실제 multipart 규칙으로 재평가**: 본체 모델 1개와 조건별 전면 모델 1개가 선택되는지 **128/128 통과**. 이미 R001의 외부 미러에서 정적 조건 평가 증거가 있으므로 이는 **사용자 제공 추출본 직접 소스 재검증**이며 새로운 고유 조합 128개가 추가로 생긴 것이 아니다.
- 512는 **정적 JSON 매핑 정의 건수**, 128은 **multipart 평가 입력 조합 수**로서 서로 더하지 않으며 인게임 렌더 수를 뜻하지 않는다.
- `STATIC_STATE_MODEL_LINKS.csv`는 규칙별 원본 경로/상태 조건/실제 모델명/예상 leaf/정적 회전/해시·존재 판정을 기록.

## E4. 모든 31 PNG를 실제 모델 슬롯에 연결

- 새로 직접 읽은 리프 127개의 `textures`에서 화면 재질에 사용하는 `bottom/top/texture/all` 슬롯만 추출: 총 **183개 leaf→소스 PNG 재질 슬롯 참조**(문 56×2=112, 다락문36×1=36, 선반 (28+7)×1=35). 고정 **31/31 PNG 모두 하나 이상의 모델 리프에서 사용됨** 확인. 미해결 재질 PNG 링크 0개.
- 선반 `particle` 5종(각 재질의 `stripped_...log/block`)은 별도로 출처를 표시하되, 고정 31 PNG 이외이므로 실제 PNG 바이트 무결성은 이 회차에서 검증하지 않았다.
- `TEXTURE_REFERENCE_COVERAGE.csv`: 31 PNG별 모델 참조 수·슬롯·대표 경로 저장.

## F. 인증·실제 화면 확인 (미완료)

- ① **사용자 제공 압축 해제 추출본 소스 검증**: 위 127 leaf, 23 blockstates, 21 templates, R003 31 PNG SHA-256 근거를 출처 등급 1로 기록.
- ② **비공식 미러와 교차 검증**: R003의 관련 JSON 175/175·PNG31/31 해시 일치 및 이번 leaf의 R003 SHA 일치를 출처 등급 2로 기록.
- ③ **Mojang 공식 원본 JAR 인증**: 사용자가 압축 해제한 폴더 자체는 압축 `client.jar`의 SHA-1을 증명할 수 없다. 독립 공식 배포 메타데이터/전체 client.jar 바이트의 SHA-1 검증 **0/31 미완료**.
- ④ **인게임 렌더링 검증**: 게임 실행/정적 UV 회전·컬링·조명·문 문양 접합의 실제 관찰 **0/31 미완료**. 파일 기반의 정적 추론과 구별한다.
- 애니메이션, Project Zomboid 변환 및 가구 3D 모델 생성은 **시도하지 않음**.

## G. 저장·다음 단계

- 이전 R001, R002, R003 불변. 이 단계 이외의 보고서/STATE/HANDOFF/전역 v38 변경 금지.
- 이번 독립 릴리스 결과 경로: `research/vanilla_textures/by_stage/1-1-11/TEX11-R004/`.
- 다음 `TEX11-R005` 연구는 **공식 Mojang 원본 client.jar의 바이트·공식 메타데이터 확보 가능 시** 완전 SHA-1 인증, 그리고 **실제 게임 화면·정적 테스트 장면 증거 확보 시** UV·투명 경계·컬링 확인에 집중. 증거가 없으면 미검증을 유지하되 source UV의 회전 적용 후 정적 배치 추론과 관찰값을 분리 기록한다.

### 기존 근거
- 사용자 제공 추출본: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11
- R003 PNG 원본 바이너리 SHA: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R003/PROVIDED_PNG_SHA256_AUDIT.csv
- R003 175 JSON SHA: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R003/PROVIDED_MODEL_JSON_SHA_CENSUS.csv
- 원래 R001 mirror 실측: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R001
