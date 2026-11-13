# 1-1-04 — 직물·양털 전용 채팅 인수인계

> **현재 단계 고유 버전: `TEX04-R006` (2026-11-13)** · 다음 후보 `TEX04-R007` · 전역 역사적 `v38` 유지.

## TEX04-R006 — 신규 아이템 JSON 9개 정적 모델 경로 + R005 재현 코드 정오표 (2026-11-13)

- [R006 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R006/REPORT.md) · [9개 JSON 증거 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R006/ITEM_MODEL_9_SOURCE_LINKS.csv) · [수정 재현 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R006/REPRODUCE_R005_FIXED_PLUS_ITEM_GATE.py) · [요약](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R006/SUMMARY.json).
- 사용자 추출 `1.21.11/assets/minecraft/items/<color>_wool.json` **9개 새 소스 파일** 직접 확인. `minecraft:model`이 각각 기존 `minecraft:block/<color>_wool`을 참조하며, 새로운 고유 PNG/픽셀/face는 **0**.
- R005 불변 `REPRODUCE_R005.py`에서 17바이트로 잘못 이스케이프된 PNG signature 버그 발견. **기존 R005는 덮어쓰지 않고** 수정 리터럴 8바이트 확인 및 아이템 JSON 검사를 추가한 수정판을 R006에 별도 저장. 수정판 전체의 사용자 환경 재실행 성공은 주장하지 않음.
- 인게임 정적 **0/9**, 공식 배포 SHA1 인증 **필수 제외(인증 성공 아님)**, 애니메이션 및 다른 단계 작업 보류.
- 다음 `TEX04-R007`은 라이브 STATE/HEAD/새 폴더 확인 후 새 실측 증거 있을 때만.

---

## TEX04-R005 — 9색 양털 색상치환·명도 부호·D4 패턴·정적 상태 신규 비교 (2026-11-13)

[새 R005 보고서](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/REPORT.md) · [요약 JSON](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/SUMMARY.json) · [색상 치환 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/COLOR_SUBSTITUTION.csv) · [D4 방향성 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/D4_ORIENTATION.csv) · [36색쌍 인접부호 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/PAIRWISE_GRADIENT_SIGNS.csv) · [정적 모델 상태 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/MODEL_STATE_COMPARISON.csv) · [재현 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R005/REPRODUCE_R005.py).

- 라이브 전 릴리스 `TEX04-R004`의 SHA-384 MANIFEST/SF 30파일 내부 체인 결과 계승; 9 PNG를 사용자 제공 `1.21.11/`에서 다시 직접 바이트로 열고 SHA256·CRC 검증. **신규 고유 PNG 0, 고유 2,304픽셀·54면 계승(추가 집계 금지)**.
- 새 지표 **126행**: 색상별 9행·D4 72행·36쌍 인접 명도부호·9종 모델/상태 비교. 36쌍 × 480 = 17,280 후보 중 두 쪽 모두 명도차가 있는 **16,404 비교(가로 7,933+세로 8,471) 전부 부호 일치**, 876건 무변화 포함 비교 제외.
- D4 8공간변환 검사에서 **9색 모두 회전/반사 없는 상태가 최고 상관**. 그러나 색상별 RGB 팔레트가 같지 않고, 채널별 1차 치환 잔차가 있으므로 RGB 값 자체를 동일하다고 보지 않는다.
- 9 leaf 모델/9 blockstate/3 부모 JSON을 직접 재열람: 동일 `cube_all→cube→block`, 단일 기본 blockstate variant, 정적 JSON의 추가 기하·UV 회전·색상별 orientation 차이 0. **실제 게임 3D face의 샘플링과 조명은 확인 안 됨**.
- 사용자 변경 정책: Mojang 배포 client.jar **전체 SHA-1/공식 메타데이터 인증은 필수 연구·완료 분모에서 제외**, 역사적 인증 실패/미검증 상태 0 유지. **인게임 정적 0/9**, RSA/PKCS7 서명 인증 주장 금지. 애니메이션·PZ·가구 제작 제외.
- **다음 번호 `TEX04-R006`**: 새 정적 소스 반례나 실제 통제된 게임 정적 스크린샷 등 *새 근거* 확보 시에만, 새 채팅 HEAD/STATE/폴더 재확인 후 발행.

---
## TEX04-R004 — 원본 추출본의 JAR 서명 메타데이터 SHA-384 연결 신규 검증 (2026-11-13)

**이번 신규 연구는 R003 이후 실제 미검증 범위만 추가했다.** 사용자 제공 `1.21.11/META-INF/MANIFEST.MF` (Git blob `a6f3479fade23b634eba8e18a25a96377b2fb844`), `MOJANGCS.SF` (blob `206d3c15590b05c53a565463d3776d0c73231f90`)를 읽어 9개 양털 PNG + 9개 모델 leaf JSON + 9개 blockstates JSON + 3개 상속 부모 JSON = **30개 실제 파일**의 SHA-384을 대조했다.

- **[R004 신규 결과 폴더](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R004)**: [REPORT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R004/REPORT.md), [30파일 digest 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R004/SIGNATURE_MANIFEST_30_FILE_CHAIN.csv), [검증 재현 코드](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R004/VERIFY_SIGNED_MANIFEST_CHAIN.py), [인증 한계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R004/SIGNATURE_LIMITATIONS_AND_NEXT_GATE.md), [SUMMARY.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R004/SUMMARY.json).
- **PNG 9/9 + 정적 JSON 21/21 = 30/30**: 원본 파일 내용의 SHA-384가 `MANIFEST.MF`의 각 SHA-384-Digest와 일치. 9개 PNG는 R003 SHA256과 동일; 모델 JSON 21개는 R003 저장소 Git blob(3개 공통 부모 포함)과 동일한 소스 바이트로 검사. **새 텍스처 0종**, 기존 9종 유지.
- 이 30개의 MANIFEST 항목을 원래 JAR 형식인 **CRLF**로 복원하면 `MOJANGCS.SF`에 적힌 항목 SHA-384와 **30/30 일치**. GitHub LF 텍스트를 그대로 해시하면 **0/30 일치**. MAIN 속성 섹션도 CRLF 복원 시 **1/1 일치**. 줄바꿈 형식 변환으로 인한 차이를 정확히 보존.
- `MOJANGCS.RSA` 파일(5,453바이트, Git blob `aa52f21923c946644d864d0adb770c642c43f697`) 존재만 확인. **RSA PKCS#7 전자서명 유효성은 확인하지 않았다.** 공식 Mojang 배포 `client.jar`의 전체 SHA-1+크기 및 공식 버전 메타데이터 검증도 **미완료 0/9**. 인게임 정적 관찰 **0/9**.
- R001의 2,304 RGBA 픽셀, R002의 색상쌍 36개/이음매 9개, R003의 모델/UV 54면은 **계승만** 하며 신규 연구량에 중복 가산하지 않는다.
- 다음 **`TEX04-R005` 예정**: 작업 전 반드시 `STATE.json` SHA/current/next/새 폴더 존재 여부 재확인. 가능하다면 PKCS#7 서명 실물 유효성→Mojang 공식 version JSON→원본 전체 JAR SHA1/size→9개 PNG 추출→인게임 정적 증거 순으로 진행. 새 근거 없으면 버전 증가 금지.
- 애니메이션·프레임 연구 보류, 실제 가구 3D 제작·PZ 변환 제외. 기존 R001~R003, 타 1-1 단계, 루트 `HANDOFF.md`/`PROGRESS.md`/`handoff/STATE.json`, 전역 `v38` **수정하지 않음**.

## TEX04-R003 사용자 제공 1.21.11 추출본 우선 검증 (2026-11-13)

**이번 연구의 기준 원본 변경:** 사용자 GitHub 저장소 [`1.21.11/`](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11)은 사용자가 직접 Minecraft Java Edition 1.21.11 JAR을 압축 해제해 업로드했다고 설명한 자료다. 이번 채팅은 **이 폴더의 실제 PNG 9개 / 색상별 모델 JSON 9개 / blockstate JSON 9개 / 공통 부모 JSON 3개 / version.json**을 직접 열람했다.

- [**TEX04-R003 검증 폴더**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R003) — 보고서, 원본 9행 원장, 면별 54행 UV 재검증, 4가지 독립 인증 등급, 역사적 SHA 정오표, 기계 판독 요약, 로컬 재현 코드.
- **사용자 제공 PNG 9개 SHA-256 새 재계산 9/9 모두 R001/v4 값과 일치**. PNG 시그니처/청크 CRC/16×16 색인 PNG도 9/9 확인. 기존 미러의 Git blob SHA와도 9/9 일치.
- 사용자 제공 모델 leaf JSON 9개, 블록상태 JSON 9개 각각 미러와 동일한 파일 내용; `cube_all → cube → block` 정적 상속 확인, 기존 54면의 텍스처 매핑·implicit UV 전체 범위를 **사용자 제공 추출본 기준으로 추가 교차 검증**. R001에서 미러로 측정한 9개를 별도 9개로 중복 집계 금지.
- **R001 전사 오류 발견:** `black_wool`의 모델 blob SHA가 R001 출처 CSV 1행/UV 6면에서 **39자리**로 기록됨. 실제 사용자 제공 파일·미러의 올바른 **40자리** 값은 `7fea63ff530cad3b51435e662daa2c4d6324bd8a`. R001 원본은 수정하지 않고 [R003 정오표](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R003/ERRATA_R001_BLACK_WOOL_MODEL_SHA.md)와 새 원장에서 정정.
- **4분리 검증:** 사용자 추출본 직접검사 9/9, 미러 교차검증 9/9, Mojang 공식 원본 `client.jar` 전체 SHA1 인증 **0/9**, 실제 인게임 정적 장면 **0/9**. `version.json`이 `1.21.11`이라도 파일 추출본이 Mojang 배포 바이너리와 인증됐다는 뜻은 아님.
- 다음 버전은 **`TEX04-R004` 예정**. 새 채팅마다 GitHub `STATE.json` SHA/current/next와 새 결과 폴더 충돌 먼저 조회. 공식 Mojang version manifest→version JSON→full client.jar SHA1/size→JAR 내부 9 PNG/JSON SHA→인게임 고정 조건 정적 관찰만 미완료 범위로 진행.
- 정지 명령 유지: 애니메이션/프레임·움직임 연구, 실제 가구 3D 제작, Project Zomboid 변환. **기존 R001/R002, 다른 1-1 단계, 루트 공통 문서, 전역 v38 불변.**

## 이전 기록 (역사적 참고): TEX04-R002 후속 픽셀 실측 (2026-11-13)

R001의 **동일한 양털 9개** 미러 PNG를 SHA-256 재검사해 모두 기존 SHA와 일치했다. 이번 새 분석은 9색의 **36개 서로 다른 색쌍**에 대한 공간 명도 Spearman/Pearson 상관과 팔레트 인덱스 일치 수, **9개 이미지의 좌우/상하 반복 경계**를 재측정한 것이다. 고유 원본을 18개로 부풀리지 말 것.

- R002 [결과 폴더](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-04/TEX04-R002)에는 REPORT.md, PAIRWISE_COLOUR_PATTERN.csv (36행), SEAM_REPEAT_AUDIT.csv (9행), REPRODUCE_R002.py, OFFICIAL_VERIFICATION_GATE.md, SUMMARY.json이 있다.
- 36색쌍 밝기 순위 상관 0.99923735~0.99999140, Pearson 0.90303542~0.99886194. 노랑/주황 색상은 인덱스 254/256 일치하지만 PNG별 RGB 팔레트는 별개다.
- 좌우 경계/가로 내부 평균 RGB 차이 비 1.760824~1.823939. 인게임 시각적 이음매 여부를 인증한 것은 아니다.
- F 공식 원본 검증: 제3자 버전 인덱스에 Mojang client.jar 후보 SHA1 ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd가 있으나, 공식 메타데이터·JAR 직접 입수 실패. **공식 JAR 0/9, 인게임 정적 화면 0/9**로 유지.
- R001의 A~E 정적 JSON/UV 54면 증거는 보존·재사용; R002에서 인게임 54면을 렌더링한 것으로 주장하지 않는다.
- 다음 R003은 STATE.json SHA/버전/폴더 충돌 확인 후 공식 버전 메타데이터의 SHA1/size 인증, 실제 client.jar 바이트 인증, JAR 내부 9개 PNG SHA-256 대조, 인게임 정적 화면 근거 순서로 진행. 새 검증 없으면 버전 증가 금지. 애니메이션 및 실제 가구 제작 보류. 글로벌 v38 유지.

## 읽을 파일 / 쓰기 경계

- [단계 STATE.json](STATE.json): 9개 item_id·원본 SHA·완료/미완료·다음 번호.
- [상세 A–G 작업표](../../1-1-04_직물양털.md) · [독립 버전 규칙](../../ISOLATED_CHAT_VERSIONING.md)
- [v4 실측 150종](../../../../research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) · [150개 번호 원장](../../../../research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv)
- **이번 고유 체크포인트:** [TEX04-R001 보고서](../../../../research/vanilla_textures/by_stage/1-1-04/TEX04-R001/REPORT.md), [출처 원장](../../../../research/vanilla_textures/by_stage/1-1-04/TEX04-R001/SOURCE_LEDGER.csv), [RGBA 계측](../../../../research/vanilla_textures/by_stage/1-1-04/TEX04-R001/RGBA_METRICS.csv), [54면 UV](../../../../research/vanilla_textures/by_stage/1-1-04/TEX04-R001/UV_FACE_LEDGER.csv), [SUMMARY](../../../../research/vanilla_textures/by_stage/1-1-04/TEX04-R001/SUMMARY.json), [METHOD](../../../../research/vanilla_textures/by_stage/1-1-04/TEX04-R001/METHOD.md).
- 수정할 수 있는 경로는 이 `HANDOFF.md`, 이 `STATE.json`, `research/vanilla_textures/by_stage/1-1-04/`의 **새 불변 릴리스 폴더**뿐. 루트 `HANDOFF.md`, `PROGRESS.md`, `handoff/STATE.json`, 타 `1-1-xx` 전부 수정 금지.

## 대상 및 실제 완료 성과

**대상 고정 9종:** `white_wool`, `red_wool`, `blue_wool`, `black_wool`, `green_wool`, `yellow_wool`, `purple_wool`, `cyan_wool`, `orange_wool` (`assets/minecraft/textures/block/{name}.png`).

- **A:** v4 선택 파일 및 번호별 원장 9개 교차 확인, v35·v36 관련 보고서에 동일 `*_wool` 항목 0건 확인.
- **B:** `1.21.11` 비공식 추출 미러 9개 PNG를 새로 가져와 SHA-256 직접 계산, v4 해시 9/9 일치, PNG 전 청크 CRC32 9/9 통과.
- **C:** PNG indexed color 디코딩 후 16×16 RGBA 총 2,304 고유 픽셀 실측. 9개 모두 alpha=255 (각 256픽셀), RGB 다양성·밝기·채도·인접 변화량·entropy 등 저장.
- **D1:** 9색 상대 밝기·채도 정량 비교. **D2:** 세로 인접 RGB 변동이 가로 대비 1.7648~1.8116배; 픽셀 밝기 순위 상관 모든 색 쌍 0.9992 이상, 방향성 유의. **D3:** 패브릭 응용은 디자인 가설로만 보관.
- **E:** 9개 blockstate + 9개 leaf 모델 + 2개 상속 부모 JSON 실제 읽음. `cube` 전체 면 6개×9개=54개 텍스처 슬롯/암시적 UV `[0,0,16,16]` 연결 확인. 총 13,824 texel 참조량은 유일 픽셀과 중복 합산 금지.
- **F: 미완료.** Mojang 공식 `client.jar` 인증 0/9, 인게임 정적 렌더 검증 0/9. `mirror_sha_pixel_checked`를 `official_jar_authenticated`로 잘못 표시하지 말 것.
- **G:** 단계 보고서·출처 및 RGBA·UV CSV·SUMMARY JSON·방법기록을 R001 폴더에 불변으로 저장. 기존 v4/v35~v38 데이터 보존.

## 다음 채팅이 가장 먼저 해야 할 일

1. GitHub의 현재 `STATE.json` 및 현재 단계 `HANDOFF.md`를 직접 읽고 `current_revision`/blob SHA를 확인한다. `TEX04-R002`는 **예정**이지 충돌 회피를 위한 고정 약속이 아니다.
2. 이번 `TEX04-R001` 결과를 덮어쓰지 말고 재사용. 최대 미검증은 **Mojang 공식 1.21.11 client.jar 파일 SHA 인증**과 **인게임 정적 9색 관찰**이다.
3. 공식 JAR 접근이 가능할 때는 런처 버전 메타데이터 SHA/다운로드 경로 확인 후 공식 JAR 내부의 9 PNG를 추출하여 미러의 SHA와 별도로 비교하고 불일치를 기록한다. 인게임 정적 장면은 조명·리소스팩 조건과 스크린샷 증거를 보존한다.
4. 새 실제 검증이 발생한 경우에만 해당 단계의 **다음 고유 `TEX04-Rxxx`**를 만들고 결과·다음 STATE를 쓰기. 같은 단계 다른 채팅과의 SHA/HEAD 충돌이 있으면 쓰지 말고 다시 확인.
5. **애니메이션 연구 전면 보류.** 물리적인 실·쿠션 재질을 이미지 단독으로 확정 금지. PZ 변환/실제 가구 3D 제작은 이 단계가 아니다.

**진행도 오해 주의:** v4 9/9는 기존 측정 기록; TEX04-R001 9/9는 비공식 미러의 새 바이너리·픽셀 및 정적 모델 근거. 공식 인증/인게임 시각 확정은 **여전히 0/9**. 단계 전체 완료 %는 추정하지 않는다.
