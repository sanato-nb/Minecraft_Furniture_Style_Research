# TEX04-R004 — 사용자 제공 1.21.11 추출본의 양털 PNG·정적 JSON 30개 서명 메타데이터 SHA-384 연결 검증

> 검사일 2026-11-13 · 단계 1-1-04 직물·양털 9개 · 과거 R001/R002/R003 불변 · 전체 v38 불변 · 애니메이션 연구 보류.

## 새로운 근거 (R003 이후 추가 검증만)

사용자가 직접 client.jar을 압축 해제하여 GitHub에 업로드했다고 밝힌 `1.21.11/`에서, 기존 R003의 파일별 SHA-256 및 모델·UV 검증을 **중복 집계하지 않고**, 새로 발견한 JAR의 `META-INF/MANIFEST.MF`와 `META-INF/MOJANGCS.SF`의 SHA-384 참조를 실제 PNG/정적 JSON과 대조했다.

- `META-INF/MANIFEST.MF`: Git blob `a6f3479fade23b634eba8e18a25a96377b2fb844` (GitHub 파일 3,664,658바이트).
- `META-INF/MOJANGCS.SF`: Git blob `206d3c15590b05c53a565463d3776d0c73231f90` (3,664,852바이트).
- `META-INF/MOJANGCS.RSA`: Git blob `aa52f21923c946644d864d0adb770c642c43f697` (5,453바이트). **존재 확인만 수행. PKCS#7 서명 암호학적 검증을 수행했다는 뜻이 아님.**

파일 범위는 **고정된 9개 양털 색상마다 PNG 1개 + block 모델 JSON 1개 + blockstate JSON 1개 = 27개**, 그리고 공유 부모 모델 `cube_all.json`, `cube.json`, `block.json` **3개**, 총 **30개 서로 다른 파일**이다. 이것은 새 텍스처 30종이 아니라 **기존 양털 9종의 정적 소스 파일 30개**를 뜻한다.

## 직접 검사 결과

| 검사 내용 | 결과 | 계산 방식 |
|---|---:|---|
| 9개 PNG 바이트 → `MANIFEST.MF`의 `SHA-384-Digest` | **9/9 일치** | GitHub 사용자 원본 base64 바이트에 Python `hashlib.sha384`; R003 SHA256 재확인 |
| 9개 색상별 모델 JSON → `MANIFEST.MF` | **9/9 일치** | 동일 내용 템플릿의 Git blob SHA1을 R003 파일별 blob과 먼저 교차 검사한 후 SHA-384 계산 |
| 9개 blockstate JSON → `MANIFEST.MF` | **9/9 일치** | 위와 같은 방식 |
| 부모 JSON 3개 → `MANIFEST.MF` | **3/3 일치** | 실제 GitHub 소스 내용과 Git blob SHA1을 먼저 교차 검사한 뒤 SHA-384 계산 |
| 이 30개 `MANIFEST.MF` 항목 내용 → `MOJANGCS.SF` SHA-384 항목 | **30/30 일치** | JAR 명세의 **CRLF 줄바꿈으로 재구성한 항목 바이트**를 SHA-384로 검사 |
| MANIFEST 주요 속성 `Manifest-Version`/ `Main-Class` → `.SF`의 `SHA-384-Digest-Manifest-Main-Attributes` | **1/1 일치** | CRLF로 재구성한 주요 속성 섹션의 SHA-384 |
| GitHub MANIFEST에 저장된 LF 항목 바이트를 **변환 없이** `.SF`와 직접 비교 | **0/30 일치** | 줄바꿈 형식 차이에 유의. **동일 바이트 그대로 서명이 유효하다는 의미로 오해 금지** |

세부 파일별 원본 경로, Git blob, PNG SHA256(R003에서 계승), MANIFEST SHA384(Base64), SF 항목 SHA384(Base64), 각각의 판정은 `SIGNATURE_MANIFEST_30_FILE_CHAIN.csv`에 기록했다.

## CRLF 재구성의 해석 — 중요한 검증 한계

원본 JAR 매니페스트는 통상 `\r\n`(CRLF)로 작성된다. GitHub에서 읽은 두 개의 대형 `META-INF` 텍스트는 `\n`(LF) 형식이므로 이를 **그대로** SHA-384하면 SF 항목과 맞지 않았다. 반면 매니페스트 각 항목의 줄바꿈을 CRLF로 바꾸고 마지막 빈 줄까지 포함하면 **30/30** 일치하였다. 이는 **서명 메타데이터 체인의 해당 항목 내부 일관성**에 관한 증거다. GitHub에 올리는 과정에서 줄바꿈이 변환됐는지, 실제 업로드 전 JAR의 서명 패키지가 유효했는지는 아직 별도의 확인이 필요하다.

또한 `.SF`에 명시된 digest와 PNG/JSON의 digest가 일치해도 **`MOJANGCS.RSA`의 인증서·PKCS#7 디지털 서명을 검증한 것이 아니다**. 원본 전체 JAR의 바이트가 없는 상태에서는 공식 1.21.11 버전 JSON의 `downloads.client.sha1` 및 `size`와 전체 JAR을 대조할 수 없다.

## A–G 및 네 가지 검증 축

- **A (출처):** R003의 사용자 제공 1.21.11 소스 우선 원칙 유지, 비공식 미러 교차 9/9 계승.
- **B (원본):** PNG 원본 바이너리 9개가 MANIFEST의 SHA-384에 일치함을 *새로 확인*. R003의 PNG SHA-256 9개를 새로운 9개로 중복 계산하지 않음.
- **C·D (RGBA/직물 특성):** R001의 기존 2,304개 픽셀 분석, R002의 36쌍 패턴/9 이음매, D1~D3 원본 사실과 응용 가설 구분 **계승, 신규 측정으로 재가산 안 함**.
- **E (정적 JSON/UV):** 기존 54면의 모델 연결을 구성하는 21개 정적 JSON에서 새 SHA-384 연결 검증. **신규 UV 면 0개**.
- **F:** 공식 client.jar 전체 SHA-1 인증 **0/9**, Mojang 원본 배포 메타데이터 직접 인증 **미완료**, **PKCS#7 RSA 서명 유효성 미검증**, 인게임 정적 렌더 **0/9**.
- **G:** 본 R004의 원장/보고서/재현 코드/상태 인수인계 저장.

검증 축 별칭: (1) `user_provided_extraction_checked` **9/9**, (2) `mirror_binary_crosschecked` **9/9**, (3) `official_mojang_jar_sha1_authenticated` **0/9**, (4) `ingame_static_verified` **0/9**. 이번 SHA-384 검사는 (1)의 **추가 무결성 근거**이고 독립적인 제5의 공식 인증으로 승격하지 않는다.

## 다음 작업

다음 `TEX04-R005` 전에는 GitHub STATE/HANDOFF SHA·current/next·새 릴리스 폴더 존재 여부를 다시 확인할 것. 공식 원본 검증에는 Mojang 버전 매니페스트·버전 JSON의 SHA 검증, 인증 가능한 `client.jar` 전체 파일 SHA-1/크기 대조, (필요 시) JAR 서명 검증, 원본 내부 9개 PNG/JSON의 비교가 필요하다. 인게임 정적 9색 검증은 실제 실행 스크린샷 확보 전까지 미완료.

본 R004는 **R001~R003 원본 불변**. 다른 1-1-xx 및 공통 루트 파일 편집 금지, 애니메이션·Project Zomboid 변환·실제 가구 3D 제작 범위 제외.
