# 1-1-11 — 목재·구조부품 별도 채팅 인수인계

## 최신 인수인계: TEX11-R003 — 사용자 제공 추출본 소스 정정 (2026-11-13)

- **현재 `TEX11-R003`**, 다음 `TEX11-R004`, 전역 `v38` 변경 없음. 기존 `R001`/`R002` 분석·커밋·CSV/JSON을 수정하거나 중복 계산하지 않았다.
- **우선 출처:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/1.21.11 — 사용자가 Minecraft Java 1.21.11 JAR을 직접 압축 해제하여 업로드했다고 밝힌 폴더. 해당 사용자 제공 추출본은 Mojang 공식 배포본 무결성 인증과 별도.
- **신규 실제 검증:** 고정 PNG 31개를 이 `1.21.11/` 폴더에서 직접 읽어 SHA-256/PNG CRC 재계산 **31/31 통과**, 기존 v4/R001 PNG 해시 및 미러 blob SHA **31/31 동일**. 31 PNG의 파일 바이트 총 8,080; 16×16 26개, 32×32 5개, `bamboo_shelf` 4bit. 이전 RGB/알파/UV 실측은 동일 바이트라서 입력 자료로만 재사용하며 재측정 새 수량 없음.
- **모델/블록 상태/아이템:** 사용자 추출본과 미러 Git blob SHA·size 대조 **175/175 일치**: 현재 범위 168개(leaf120 + blockstate23 + template21 + shelf item4), 역사적 참나무 선반 7 leaf는 중복 미계상. 추출본 JSON 본문 직접 파싱 **48/48**(블록상태23, 템플릿21, 아이템4), 이전 기록의 rule/UV면 수 **48/48** 동일.
- **4종 검증 층 분리:** ① 사용자 제공 추출본 31 PNG+48 JSON 실파일 / ② 비공식 미러 교차 SHA 31 PNG+175 JSON / ③ **Mojang 공식 원본 JAR 전체 SHA-1 인증 미완료 0/31** / ④ **실제 인게임 정적 렌더 0/31**. 추출 폴더 파일 해시로 원본 JAR 컨테이너 SHA-1을 증명할 수 없음. 애니메이션 계속 보류.
- **R003 새 증거 폴더:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R003/
- **다음 TEX11-R004:** 최신 STATE·HEAD 충돌 검사 후 진짜 원본 JAR bytes + Mojang 직접 버전 메타데이터 확인(가능할 때만), 정적 인게임 UV·접합·컬링 증거 확보. Project Zomboid 변환/가구 3D 모델 생성 금지, 다른 재질 단계와 루트 v38 수정 금지.

---

## 최신 독립 릴리스 — TEX11-R002 (2026-11-13)

- **현재 `TEX11-R002`**, 다음 `TEX11-R003`, 전역 레거시 `v38` 유지. 이전 R001/R000은 아래 역사적 문맥으로 보존.
- 31 PNG 직접 재조회·CRC/zlib/RGBA 파싱 31/31, R001 미러 Git blob SHA 일치 31/31. 모든 PNG는 가로·세로 정확 순환 RGBA 반복 최소 이동이 원본 가로/세로 크기(16 또는 32)와 동일. 좌우 alpha 경계 차이 0/31, 상하 alpha 경계는 cherry_door_bottom(2열), cherry_door_top(6열)만. R001의 서로 다른 문 PNG 경계 4열 비교와 별도.
- 선반 5종 32×32의 가로 16px 순환 픽셀 일치율은 62.695~65.039%이며 완전 반복 아님. 모델 리프 120/120 Git tree SHA/파일 크기 확인(문56, 다락문36, 비참나무 선반28). 그중 12개만 이번 회차 leaf JSON 본문·부모 SHA 독립 확인, 나머지 108개는 Git tree 수준.
- 미러 root `1.21.11.json`에 복사된 예상 Mojang client.jar SHA1 `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd`와 31,152,600바이트 확인했지만 **공식 바이너리 접근 실패**. 공식 JAR 내 PNG 인증 0/31, 인게임 정적 0/31. 애니메이션 금지 계속 유지.
- 근거 저장: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R002/
- **다음 TEX11-R003**에서 STATE/HEAD 충돌 검사 후 Mojang 공식 JAR 획득·전체 SHA1·31 PNG 교차 인증, 인게임 정적 UV 경계부터 진행. 다른 단계·루트 v38·과거 불변 폴더 수정 금지.

---

## 2026-11-13 신규 독립 검증 — TEX11-R001

- 단계 최신 버전 **TEX11-R001**, 다음 **TEX11-R002**. 기존 전역 v38 불변. 아래 R000 계획 문구는 최초 설정 당시 기록이다.
- 실제 비공식 미러 PNG 31/31을 독립 재해시(v4 SHA 대조)·CRC/디코딩/RGBA 확인. 원본 11,776 픽셀(불투명 11,153, 투명 623, 부분 0), 16×16 26개/32×32 선반 5개. bamboo_shelf는 4-bit indexed PNG 예외.
- D1 문 7쌍 알파 경계(cherry만 불일치 4열) 및 다락문 12종 UV; D2 선반 5 atlas×5 UV 영역 25 실화소 크롭; D3/E 파생 선반 28 leaf 및 128개 정적 상태, 문 56 leaf/다락문 36 leaf, 공유 템플릿 21 JSON. 선반 38 explicit UV면/2,304 texel uses 기존 v38과 재대조, oak_shelf v38 7 leaf는 신규 계산에 불포함.
- 공식 Mojang client.jar 인증 **0/31**, 실제 인게임 정적 **0/31**. 반복 주기·실제 UV투영·문양 연결 미검증. 애니메이션 연구 계속 보류.
- 결과: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/tree/main/research/vanilla_textures/by_stage/1-1-11/TEX11-R001/
- 다음 채팅은 GitHub STATE 재조회 후 TEX11-R002에서 공식/인게임 미검증 항목부터 재개.

---

> Minecraft Java 1.21.11 · 사용자 요청에 따라 **새 채팅마다 독립 진행** · 초기 고유 버전 **`TEX11-R000` (계획만 저장)** · 공식 전체 연구 체크포인트 **`v38` 유지**.

## 연구 목표와 정확한 표본

- 담당: **1-1-11 / 목재·구조부품 / 31개 v4 텍스처 경로**.
- 출처: [v4 150개 원본 실측 CSV](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv) 및 [150개 고정 번호 원장](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/1-1_150_texture_numbered_task_ledger.csv).
- 분류별 원본 계획: [1-1-11 A–G 상세 작업 목록](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/1-1-11_목재구조부품.md).
- 새 채팅 첫 메시지: [전용 START_PROMPT.md](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-11/START_PROMPT.md).
- 절대 규칙: [독립 채팅 버전·쓰기 경계](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/ISOLATED_CHAT_VERSIONING.md).
- 이전 통합 성과(역사적 관찰, 새 결과로 중복 계산 금지): **v4 선정 31/31 항목의 측정 기록 존재**; 현재 이 별도 작업의 A–G 체크는 아직 시작하지 않았다. **공식 Mojang 1.21.11 client.jar / 인게임 정적 검증 미완료**, 전체 프로젝트 완료 `0/5`. 기존 `v1`~`v38` 파일 및 수치를 보존한다.

## 해당 단계의 기존 연구 연결 및 주의점

v38 oak_shelf 7개 leaf/7부모·32 정적 상태·38면 2,304 texel uses 소스 검증이 이미 존재. v4 oak_shelf 표본과 중복 카운트하지 말고 4종 다른 목재 선반 모델 연결을 추가 연구할 것.

## 본 단계의 A–G 작업과 결과 판정

| 코드 | 작업 | 독립 단계 현황 |
|---|---|---|
| 1-1-11-A | A 기존 출처·파일·중복 대조 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-B | B PNG 실제 바이너리·SHA·CRC 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-C | C RGBA·밝기·알파·반복 정량 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-D | D 재질 특화 세부 검사 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-E | E 정적 모델 JSON·UV·상태 연결 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-F | F 공식 Mojang client.jar·인게임 정적 검증 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |
| 1-1-11-G | G 근거 보고서·단계 인수인계 저장 | 이 단계에서 신규 완료 확인 전 / v4 증거 별도 존재 |

**D 재질 특화 기준**

- **D1:** 문·다락문 윗/아랫면 알파와 무늬 연결
- **D2:** 32×32 5종 shelf texture atlas와 일반 16×16 비교
- **D3:** v38 oak_shelf 7 leaf·38원본 explicit UV면·32 정적 상태 평가 근거 재사용 후 미검증 파생목재 확대

## 검토할 정확한 텍스처 31개

| 항목 번호 | texture_id | v4 기록 SHA-256 | 원본 추출 미러 PNG 경로 |
|---|---|---|---|
| `1-1-11-001` | `oak_trapdoor` | `7f2d78c69dcfb71d4900b974d40f6e334065f4e4c72aa36fe37ce034df9a2abd` | `assets/minecraft/textures/block/oak_trapdoor.png` |
| `1-1-11-002` | `spruce_trapdoor` | `b22c847ef0810ba5ed6546de8484ad17bc72ea894a42078ca9221aa3c23d8fdf` | `assets/minecraft/textures/block/spruce_trapdoor.png` |
| `1-1-11-003` | `birch_trapdoor` | `48e96dc1f95daee99412dc0724411c3671ab529658f00ca0aa66227ae30a3092` | `assets/minecraft/textures/block/birch_trapdoor.png` |
| `1-1-11-004` | `dark_oak_trapdoor` | `b56fddb418e82004eb6371e85acf9dc7cac608f5230049543159b2ddcc3196ed` | `assets/minecraft/textures/block/dark_oak_trapdoor.png` |
| `1-1-11-005` | `bamboo_trapdoor` | `4b3fc966d9f9c5021a387519a1cee3fd53814d5605e5623b9aacb5930453f3dd` | `assets/minecraft/textures/block/bamboo_trapdoor.png` |
| `1-1-11-006` | `oak_door_bottom` | `a209e7e8611d56d211445d5df23a50c31185a293c51f4e03f3cb691209a49df4` | `assets/minecraft/textures/block/oak_door_bottom.png` |
| `1-1-11-007` | `oak_door_top` | `0cdc592715a8145d1837f551adf774227dedf7650569e7a50f6cb831c7c0a6c6` | `assets/minecraft/textures/block/oak_door_top.png` |
| `1-1-11-008` | `acacia_trapdoor` | `9d8aebedce220ba31aea5b2c67e6180d4eec1e7dbabefc334d341e0a49ee668b` | `assets/minecraft/textures/block/acacia_trapdoor.png` |
| `1-1-11-009` | `cherry_trapdoor` | `21180e8d199bc79d8bf95ae72af08dc4df3ae02519818b13b78ba91af580dc27` | `assets/minecraft/textures/block/cherry_trapdoor.png` |
| `1-1-11-010` | `mangrove_trapdoor` | `65087166442d0a5d9edf1c467d44ab3b4f9969f1bd851c5d9ffa82259b90f1fc` | `assets/minecraft/textures/block/mangrove_trapdoor.png` |
| `1-1-11-011` | `pale_oak_trapdoor` | `5eafb6cfd036b128aea6daca3dba44f9fb3521aacb7f682d774be8c1c9c72c8a` | `assets/minecraft/textures/block/pale_oak_trapdoor.png` |
| `1-1-11-012` | `acacia_door_bottom` | `b38b2d097cac0b7b08efa43045bba368abc4a3b190ccb2e594862766c5e1e8c2` | `assets/minecraft/textures/block/acacia_door_bottom.png` |
| `1-1-11-013` | `acacia_door_top` | `2552920fee394ac3b6d165d5638bc84d2223374d8974bdd668bced3be16e5f3c` | `assets/minecraft/textures/block/acacia_door_top.png` |
| `1-1-11-014` | `spruce_door_bottom` | `5684f6fa01b213babc2ee0a07d8a5b1803fc652fe1bfbf461ff973cb07dffd89` | `assets/minecraft/textures/block/spruce_door_bottom.png` |
| `1-1-11-015` | `spruce_door_top` | `53be462544fd88a451bba74eb699c113c506773fee0243f2c79983cee66acb7d` | `assets/minecraft/textures/block/spruce_door_top.png` |
| `1-1-11-016` | `birch_door_bottom` | `7bd6636532ffc21e9ecc7aa5fc8d975e9d5b4f2e2d32db2cb3c4d00115c29c70` | `assets/minecraft/textures/block/birch_door_bottom.png` |
| `1-1-11-017` | `birch_door_top` | `48b63883ce9a4b4c72b437d5eb5c712f6b2b465ef1bbcb37a52dee9e30d0a4ea` | `assets/minecraft/textures/block/birch_door_top.png` |
| `1-1-11-018` | `cherry_door_bottom` | `08bb521c3bbbe6e5a1891554b4a8dbd6025b563dfc7ffb3dc6e14be75f5042aa` | `assets/minecraft/textures/block/cherry_door_bottom.png` |
| `1-1-11-019` | `cherry_door_top` | `9f81189ffe46f5a3fb31b89f5ae22b15c895920ee297fcce0bbc0e3f0654b47b` | `assets/minecraft/textures/block/cherry_door_top.png` |
| `1-1-11-020` | `bamboo_door_bottom` | `07a38a693f5efaf6a28d1d924ccffe60d453ac55056088c5796777b82e73644c` | `assets/minecraft/textures/block/bamboo_door_bottom.png` |
| `1-1-11-021` | `bamboo_door_top` | `90f8ca7ab7ade430a96fc176de2cfc4294a86136646fb82f24d2159997cfb2b6` | `assets/minecraft/textures/block/bamboo_door_top.png` |
| `1-1-11-022` | `mangrove_door_bottom` | `aa84032ae9968b58dfb347ab4062695caaea4e793ed2b6c20f9f5f909bc145af` | `assets/minecraft/textures/block/mangrove_door_bottom.png` |
| `1-1-11-023` | `mangrove_door_top` | `50a7be61312a2f7ab4ee61e037e5ef7c1b1878a215d50616445c16378927bf1c` | `assets/minecraft/textures/block/mangrove_door_top.png` |
| `1-1-11-024` | `crimson_trapdoor` | `654f72862b0f2c7b84ad11ff53d4b0a7e85d538af1a4d4a568e1cbb34b2fd5cf` | `assets/minecraft/textures/block/crimson_trapdoor.png` |
| `1-1-11-025` | `warped_trapdoor` | `23b02d0bfb47a73c6b8de98520d95f6e598bac2a47ef244c44e2aa122a79c7b1` | `assets/minecraft/textures/block/warped_trapdoor.png` |
| `1-1-11-026` | `jungle_trapdoor` | `cf12b835daed7c1d7e666144c85ff78e94bc41ddc45bbb49c130f89493e51244` | `assets/minecraft/textures/block/jungle_trapdoor.png` |
| `1-1-11-027` | `oak_shelf` | `cb7cf9720f3e50d6cd2e67dd8fde89a4865aa507f84e38d1c0ae0e639dd52c87` | `assets/minecraft/textures/block/oak_shelf.png` |
| `1-1-11-028` | `spruce_shelf` | `74af0ec4272efcadf0bb67e2f19e924c68b50c2a79c3692ec647541083b40dd9` | `assets/minecraft/textures/block/spruce_shelf.png` |
| `1-1-11-029` | `birch_shelf` | `73501db8e785121f52acf25521769da029f1336b0083e46eeb7b6704d904f20e` | `assets/minecraft/textures/block/birch_shelf.png` |
| `1-1-11-030` | `cherry_shelf` | `9aa40570d84cb0dc96fcb14a96ccf524807d8785c17c0b972abfdc9e48e46e53` | `assets/minecraft/textures/block/cherry_shelf.png` |
| `1-1-11-031` | `bamboo_shelf` | `6c8774fa4aa50f99d518fc56e94bea0ee6dd44293357e1876ff846f3e4c8c09d` | `assets/minecraft/textures/block/bamboo_shelf.png` |

> 위 SHA-256은 **레거시 v4 측정 기록의 값**이며 이번 턴 재해시 결과도, Mojang 공식 JAR 인증 해시도 아니다. 새 검사 시 `source SHA256`, Git blob SHA, 실제 렌더 결과를 별개로 기록한다.

## 버전 상태·저장 경로·갱신 규칙

- 현재 **`TEX11-R000`**: 단계 분리/작업 안내만 저장, 실측 신규 완료 0.
- 다음 검증 보고서: **`TEX11-R001`**; 저장 경로 `research/vanilla_textures/by_stage/1-1-11/TEX11-R001/`. 다음은 이 단계만 `TEX11-R002`...
- 이 단계 진행 관리: [STATE.json](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-11/STATE.json)와 이 `HANDOFF.md`만 단계 자체 채팅에서 갱신.
- 다른 번호 단계의 `STATE/HANDOFF` 및 루트 프로젝트 공통 체크포인트·진행 문서는 **수정 금지**. 통합 시 최종 집계 담당자가 별도로 확인.
- 소스 증거의 신뢰도는 최소 `legacy_only`, `mirror_sha_pixel_checked`, `official_jar_authenticated`, `ingame_static_verified`로 구분하되, 서로 상충·불충분하면 `pending` 유지.
- 동일 단계를 다른 채팅에서 동시에 쓰는 것은 회피. 저장 직전 HEAD/SHA와 새 릴리스 경로의 존재 여부를 다시 확인하고, 충돌하면 덮어쓰지 않는다.
- **애니메이션 연구 보류**, 기존 조사 삭제 금지. Project Zomboid 변환, 실제 가구 3D 제작 금지.

## 새 채팅 시작 직후 수행

1. **`STATE.json`을 먼저 직접 읽어** 최신 `current_revision`, 개별 파일의 last status, 다음 릴리스 번호를 확인한다.
2. 과거 v4 측정과 타 버전(해당되면 v35~v38)의 동일 경로 SHA/화소를 대조해 **새로 분석할 실제 빈틈**을 고른다.
3. 자료를 직접 검사하고 `REPORT.md`·`SOURCE_LEDGER.csv`·`SUMMARY.json`을 고유 릴리스 폴더에 보존한다. 미완료 작업은 근거/차단 원인을 기록한다.
4. 마지막으로 이 `HANDOFF.md`·본 단계 `STATE.json`만 갱신하고 다음 채팅에서 그 다음 미완료 부분으로 이어가게 한다.
