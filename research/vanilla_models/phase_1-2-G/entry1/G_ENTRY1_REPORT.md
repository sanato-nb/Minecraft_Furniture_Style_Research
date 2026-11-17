# 1-2-G Entry1 — PNG 원본 바이너리 후속 실검증 (2026-11-17)

**최종 Entry1 판정: PASS — 원본 347/347 직접 내용 감사 및 185/185 PNG 원본 바이너리·독립 RGBA 재검산 PASS, 원격 증거 파일 선행 readback PASS. Entry2 진행 허용(미착수), 전체 G는 여전히 진행 중.** 이전 부분 보고서의 `0/185`는 아래에 이력으로 보존했으며 현재 수치가 아니다. 기존 150 model JSON + 12 blockstate JSON 및 face/기하/D 재검산은 재작업하거나 중복 실적으로 계산하지 않았다.

## 신규 실행 근거
- **바이너리 차단 해결:** GitHub `fetch_file(encoding="base64")`로 **185/185 PNG 원본 bytes**를 직접 받고, Base64 → 원본 bytes를 복원. 텍스트 방식 `fetch_blob` 및 `fetch` API는 `UnicodeDecodeError` 및 UTF-8 전용 오류였고 로컬 `git ls-remote`/curl은 DNS 해석 불가였음. 바이너리 접근은 별도 인코딩 반환 방식으로 실제 우회 성공.
- **185/185** PNG 헤더 시그니처, 185개 원본 byte 길이(**총 40,518 bytes**), `SHA1(blob <len>\\0<bytes>)` Git SHA 재계산, PNG 각 chunk CRC32, zlib inflate+Adler32, PNG scanline filter 복원, 전체 RGBA 픽셀 해독·SHA-256 **전부 일치/정상**. 이 분석은 파일 이름이나 트리 해시만 확인한 작업이 아니다.
- **C 기존 검증 177종:** 원본 C 독립 원장의 RGBA SHA-256과 새 G 원본 픽셀 SHA-256이 **177/177 일치**, 치수·원본 mode·알파 픽셀 수 및 알파 고유값도 **177/177 일치**. **C 범위 밖 8종**은 본 G에서 신규 실증했으나 과거 C 검증으로 소급 등록하지 않음.
- **PNG 분포(185종):** 치수 16×16 174, 32×32 4, 16×32 1, 16×64 5, 16×128 1; 파일 형식 P 149, RGBA 26, RGB 4, L 4, LA 2. 투명 픽셀 포함 84, 전부 불투명 101. **F 기존 첫 프레임 시각 근거 38 PNG**는 신규 G의 픽셀 해독과 별도 증거 등급으로 유지.
- **.mcmeta 원문 17종:** Git tree에 연결된 원문 텍스트·SHA **17/17** 직접 검증. 애니메이션 sidecar **7종** (blast furnace 2프레임, campfire fire 8, campfire log lit 4, chain command block 4종 각 4프레임), 나머지 10종은 애니메이션 설정 없음. 프레임 수는 원본 raster 분할+JSON 설정의 정적 계산이다. **런타임 재생·게임 렌더링은 미시험.**
- **G 기존 미결정 원장 203행:** 과거 바이너리 접근 차단 185개는 신규 검증으로 **해결**. 남는 18행은 C 밖 PNG 8개, E 특수 renderer 미인증 모델 8개, C 미바인딩 face 집계 135의 소관 1행, F 스타일↔게임 렌더 차이 1행으로, 소관별로 계속 보존. 각각 `G_ENTRY1_UNRESOLVED_DISPOSITION.csv`에서 명시하며 역사 원장 `G_UNRESOLVED.csv`는 덮어쓰지 않음.

## 신규 증거 파일
- `G_ENTRY1_PNG_AUDITOR.js`: 전용 독립 JS 디코더, zlib/PNG CRC 검사, SHA-1/SHA-256 및 Base64 byte 복원 재현 코드.
- `binary_batches/G_ENTRY1_PNG_BINARY_BATCH_000.json`부터 `182.json`까지 **14개 작업 체크포인트**. 각 배치에 원본 파일별 SHA/픽셀/에러 기록.
- `G_ENTRY1_PNG_BINARY_AUDIT.csv`: 185개 파일별 경로, 원본 bytes, Git SHA, CRC/Adler/디코드, RGBA, C/F/sidecar 교차 근거 **185행**.
- `G_ENTRY1_PNG_MCMETA_AUDIT.json`: 17 sidecar 원문·SHA·애니메이션 JSON.
- `G_ENTRY1_PNG_BINARY_INDEPENDENT_RECOUNT.json`: 완성 CSV를 다시 읽고 고정 큐·G 교차 원장·C 원본 검증 집합에 재교차하는 별도 검산 (**오차 0**).
- `G_ENTRY1_UNRESOLVED_DISPOSITION.csv`: 이력 203행에 후속 해결/소관 상태를 추가해 덮어쓰기 없이 보존. `G_SOURCE_CROSSWALK.csv`는 G PNG 직접 검증 필드만 185개 갱신.

**불변/범위:** G Entry1 **347 = 150 model JSON + 12 blockstate JSON + 185 PNG** 원본 본문 확인. 일반 기하142/E특수8, 371요소, 1,373면(PNG연결1,238/템플릿 미바인딩135), UV1,142, D원본 선택167/고유 모델49는 기존 G 원본 재검산을 계승. G 전체 4,669개, 6 Entry, 글로벌 G1~G6 0/6, A~F 및 v69 원본·승인150/150·상위 1/5 불변. **공식 JAR·엔진 renderer·전체 애니메이션 재생·가구 기능을 인증하지 않음.** 원격 선행 SHA/행수/본문 재조회는 8개 주요 파일에서 PASS; 이 최종 보고서 및 상태 갱신도 별도 readback을 수행하며 기록은 G_ENTRY1_REMOTE_READBACK.json을 참조. Entry2는 진행 허용되지만 이 회차에서 시작하지 않음.

---

## 이전 Entry1 부분 보고서 (당시 PNG 바이너리 0/185, 현재 최신 상태 아님)

# 1-2-G Entry1 — 347개 원본 자산 교차 감사 중간 보고서

**2026-11-17 · 기준 GitHub main `88d9da945953e80597faa6e91a7c79078a5da819` · 사용자 제공 추출 Minecraft Java 1.21.11.**

**정식 판정: `G_ENTRY1_PARTIAL_JSON_COMPLETE_PNG_BINARY_PENDING`.** 원본 집합 경로·SHA 확인과 JSON 본문 검산은 완료했지만, 원본 PNG 바이너리 직접 재조회는 수행하지 못했다. **Entry1 완료, Entry2 착수, G1~G6 최종 통과, 상위 1-2 완료를 선언하지 않는다.**

## 실제 새로 수행한 검사 (선행 A~F 실적 재집계 금지)
| 항목 | 실제 이번 G 원본 근거 | 결과 |
|---|---|---|
| Entry1 고정 자산 | 원본 git tree `0d11841d8b48f8b7dae3fee2821ef7cfa72aff56`의 자산 path/blob SHA 대조 | **347/347** (0 차이) |
| 모델 원본 JSON | GitHub `1.21.11/assets/minecraft/models/block/` 소스 본문 직접 재조회, 10×15 원본 스냅샷 | **150/150**, SHA 불일치0 |
| 원본 상속 계보 | 직접 parent 64행, 추가 조상 3행 원문 재판독; 중복 포함 파일 레코드 217개에서 고유 JSON path **214개** | **150/150 모델 원본 계보 완료** |
| blockstate JSON | 실제 원본 12개 `variants` / `multipart` 재파싱, x/y/uvlock/weight 명시 여부 | **12/12**, D 선택 옵션 **167/167** |
| 상태→모델 근거 | 원문에서 선택한 모델 49개 고유 경로가 A/F 2,390 원장 및 최신 Git SHA에 연결됨 | **167참조**, 미확인 참조0 |
| 기하 | 원본 `elements`의 실제 제공자(부모 상속 포함) 재산정 | 일반 **142**, E 예외 **8**, 적용 요소 **371**, face **1,373** |
| face→텍스처 | 실제 JSON에서 슬롯 우선순위와 `#` 연속 참조를 재계산해 C face 원장에 독립 대조 | **1,373/1,373** 일치, PNG 결합 **1,238면**, 미바인딩 **135면**, 원문 명시 UV **1,142면** |
| PNG 원본 path/SHA | GitHub **tree SHA**를 A 경로목록과 검증하고 C `rgba_sha256` 및 F 기존 첫 프레임 근거를 별도 연결 | **185/185** SHA 일치, C 기검증 **177** / C 밖 **8**, F 기존 시각증거 일치 **38** |
| PNG 원본 바이너리 직접 재검증 | GitHub UTF-8 파일 인터페이스가 PNG 바이너리 decode를 거부 | **0/185 — 미완료** |

**단위 구분:** 1,373은 face 인스턴스이고 1,238은 face→PNG 연결 수이다. PNG 원본 185개 경로·SHA 검증과 RGBA 177개 과거 C 원장을 다시 읽은 것을 신규 PNG 픽셀 검증 185개로 기록하지 않는다. E 모델 8개는 원본에 일반 `elements`가 없으며 게임 특수 renderer·Runtime 인증은 여전히 대상 외 미검증이다.

## 독립 검산 결과
- `G_SOURCE_CROSSWALK.csv`: 타입·경로·SHA 기준 정확히 **347행**, 중복0. A→B/C/E/F 모델 원본 Git SHA 통합0차이.
- `G_ENTRY1_FACE_PNG_CROSS_LINKS.csv`: 실제 geometry 공급자/face index/direction/texture `#` chain/UV 명시 여부와 C SHA 링크 **1,373행** 독립 재산정 결과0차이. 고유 PNG 경로가 곧 face 행 수라는 뜻이 아니다.
- `G_ENTRY1_D_RULE_MODEL_LINKS.csv`: 원문 D 선택 모델 **167행**(유니크49 모델), 모델 URL과 SHA를 원본 Git tree·A/F 모집단에 확인. D의 기존 상태·모델 적용 19,440건을 이번 Entry1에서 재조사했다고 주장하지 않는다.
- `G_INDEPENDENT_AUDIT.json`: 347개 SHA 신원, 원문 JSON 162개, 371 elements/1,373 faces, C 미바인딩 135, D167, C PNG177/기검증 밖8, E8을 독립 재검산하여 **경로·수량 불일치0** 기록.
- `G_UNRESOLVED.csv`: 각 PNG **185개 원본 바이너리 신규 미열람**, 그중 C 검증 밖 8개, E 엔진 미인증 8개, face 미바인딩 135의 별도 소관, F의 시각 스타일≠런타임 렌더 인증 범위를 구분해서 총 **203행**. 같은 PNG가 2개 소관 행에 등장할 수 있으므로 행수를 서로 다른 자산 수로 읽지 않는다.

## 이번 회차에서 증명되지 않은 것
원본 PNG 185개를 바이너리로 직접 열어 RGBA/원본 픽셀/애니메이션 프레임을 독립 검증하지 않았다. 기존 C의 177개 RGBA SHA와 기존 F의 38개 시각 관찰 기록은 **연결된 선행 증거**이다. 공식 Minecraft 배포 JAR 인증, 게임 렌더링·state registry·E renderer, 모든 PNG의 물리 재질·실제 가구 정체를 판단하지 않는다.

## 수치 및 진행 상태 계약
- Entry1 **자산 identity SHA 검수: 347/347**, JSON 원본 본문 검사 **162/162**, PNG 원본 바이너리 **0/185**, Entry1 **최종 승인 0/1 회차**.
- **G 전체 4,669개 중 원본 본문 재판독 162개**(3.47%); **347개 원본 path SHA 검사**(7.43%). 서로 다른 지표이므로 둘을 더하지 않는다.
- **G1~G6 글로벌 종료 게이트: 0/6**. Entry2 진입은 Entry1의 원본 바이너리 증거 확보/명시적 계약 심사 후에만 허용.
- A~F 완료 선언 및 원본/v69 불변 유지. v69 승인150/150·상위5단계 중1단계 완료 상태는 G에서 변경하지 않는다.
- **Entry7 추가 없음**. 이번 커밋은 새로운 소스 조사에 대한 *부분 감사 체크포인트*이며 1-2-G 완료가 아니다.

상세 원본 자료 및 Git SHA는 `G_ENTRY1_SOURCE_INDEX.json`, `source_snapshots/`, `G_SOURCE_CROSSWALK.csv`, `G_ENTRY1_FACE_PNG_CROSS_LINKS.csv`, `G_ENTRY1_D_RULE_MODEL_LINKS.csv`, `G_INDEPENDENT_AUDIT.json` 참조. 원격 커밋 이후 검증 내역은 추가 감사 파일에 기록한다.
