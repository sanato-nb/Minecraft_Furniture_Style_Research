# v46 — 1-2-A 역사 서술형 근거 검수와 동일 SHA 모델 경로 분리

> **2026-11-14 KST** · 시작 GitHub main `2e3fb007f4cbb400990e5665445ec9ba2b86bb6d` · 사용자 제공 Minecraft Java **1.21.11** 추출본을 기준으로 신규 소스 근거 확인. v1~v45 연구 파일/DB/CSV 보존.

## 이번 회차의 실제 검증

**1. v5~v43 서술형 연구 파일 재조사.** `research/vanilla_models/`의 역사 연구 **Markdown 30개 + JSON 19개 = 49개 원문 전체를 열어** 각 파일의 blob SHA, 명시된 모델 Git SHA(40 hex), 완전한 모델 원본 경로 및 `.json` 이름 참조를 조사했다. [49개 감사 원장](02_HISTORICAL_49_MD_JSON_AUDIT.csv)과 [약한 이름 참조 32건](03_HISTORY_NAME_ONLY_32.csv) 참고. 결과는 정확한 P1 모델 SHA **4번 출현**(모두 기존 v43 `crafter` 4 leaf가 이미 증거 연결된 것), 완전한 모델 파일 경로 문장 **0건**, 단순 `.json` 모델 basename 출현 **32건/21개 이름**이다. 이 기준으로 새 SHA 연결 모델은 **0개**. 이름만 적힌 기록은 **SHA 근거로 자동 승격하지 않았다**. 숫자는 정규식 기반 출처 추출 성과이지 서술의 모든 의미를 재현 검증했다는 뜻이 아니다.

**2. 선택 밖 최근 CSV 30개 재검사.** v35~v43 원본 연구 CSV 중 v44의 17종 및 v45의 86종에 속하지 않았던 나머지 **30개 원문**을 열어 P1 SHA 참조를 교차했다. 기존 모델 조사 SHA 및 UV/상태 자료와 이미 544행을 나열한 **두 인벤토리 CSV**를 구별했다. **신규로 확인된 미연결 모델 SHA 0개.** 30개별 blob SHA는 [최근 CSV 감사](08_RECENT_30_CSV_RECHECK.csv)에 남겼다. 전체 역사 CSV **137개** 중 v34 대량 모집단 인벤토리 4개와 연구 증거 중심 133개(기존 v44 17 + v45 86 + 이번 30)의 검수 범위를 구분한다. SQLite 바이너리와 build 스크립트 및 다른 연구 디렉터리의 의미론적 감사는 남아 있다.

**3. P1에서 새로운 동일 SHA 교차 문제 확인.** 544개 서로 다른 모델 경로 가운데 **서로 다른 blob SHA 539개**임을 확인했다. SHA 그룹 2개가 합계 **7개의 서로 다른 모델 경로**를 공유한다:
- `9406a8491ed2532d4878b0a91b16a0e5f8d93d80`: `banner`, `bed`, `chest`, `oak_sign`, `trapped_chest` (5경로)
- `00c837bfb2e49f00dff93ac37be1b3d17f9f9369`: `bamboo_sign`, `bamboo_hanging_sign` (2경로)

서로 다른 모델명은 **같은 내용의 model JSON blob라도 각자의 전체 파일 경로로 유지**한다. SHA 단독으로 인덱스를 만들어 한 모델로 합치거나 한 파일의 연구 근거를 다른 모델 경로로 자동 전파하는 것은 오류다. 기존 v43의 모델 vs blockstate 같은 이름 충돌 2건 오탐 해결은 그대로 보존한다.

**4. 아홉 원본 모델 직접 열람.** 위 동일 SHA 7경로 + `acacia_sign`, `acacia_hanging_sign` 두 경로에 대해 원본 model JSON **9개를 직접 열고**, 정확한 `(asset_type, full_source_path, git_blob_sha)`를 v45 원장과 **9/9 일치 대조**했다. 그중 `bed`, `chest`, `oak_sign`, `trapped_chest` **4개는 기존 119에 포함되어 재검증만**, 나머지 `banner`, `bamboo_sign`, `bamboo_hanging_sign`, `acacia_sign`, `acacia_hanging_sign` **5개는 새로운 직접 출처 연결**이다.

아홉 model JSON 모두 소스에 **`elements` 키와 `parent` 키가 없고 `textures.particle`만 존재**한다. 따라서 **이 파일 자체에서 3D 큐보이드·면 UV를 결정할 수 없으며** 실제 형상/특수 엔진 렌더러가 검증됐다는 뜻도 아니다. [9개 원본 조사](05_PARTICLE_ONLY_9_ORIGINAL_MODELS.csv) 참고.

**5. 블록상태 타입 분리.** `chest`, `trapped_chest`, `oak_sign`, `bamboo_sign`, `bamboo_hanging_sign`, `acacia_sign`, `acacia_hanging_sign`의 정확한 `blockstates/<name>.json` 원본은 각각 **단일 variant / 해당 모델 참조**를 확인했다. `blockstates/banner.json`, `blockstates/bed.json`는 정확한 해당 경로에서 찾지 못했다. 색상별·별명 상태 파일이 없다는 일반 명제가 아니며 아직 검색하지 않은 경로는 보류한다.

## v45 → v46 수량 (서로 다른 증거 단위)

| 항목 | v45 | v46 |
|---|---:|---:|
| P1 모델 **경로** 전체 | 544 | 544 |
| 원본 경로+SHA로 연결한 모델 **경로** | 119 | **124** |
| 이번 조사 근거에서 아직 미연결인 모델 경로 | 425 | **420** |
| 이번 새로 직접 읽은 원본 모델 JSON 경로 | 7 | **9** |
| 과거 서술형 Markdown/JSON 원문 추가 조사 | — | **49개** |
| v35~v43 최근 CSV 교차 검수 추가 | — | **30개** |
| 신규 PNG RGBA 검사 | 0 | **0** |
| 1-2 전체 기하/UV/상태/렌더 완료율 | 미산정 | **미산정** |

기존 119 + 이번 새 연결 5 = **124**. 동일한 blob 파일 내용이라도 서로 다른 `source_path`는 서로 다른 모델 경로이다. **124는 모델 전체 기하·UV·상태 검사 완료 수가 아니다.** 420은 '단 한 번도 연구되지 않았다'는 뜻이 아니다.

## 현재 제한과 다음 작업

- 원본 모델 파서에서 `elements` 키 부재와 `elements: []` 명시를 별도로 보존해야 한다. `textures.particle`만을 모델 geometry로 확정 금지.
- Markdown/JSON 49 파일은 실제 원문을 확인했지만 원본 SHA 부재의 서술형 명칭 참조를 모두 source-level evidence로 확정하지 않았다. 과거 SQLite·build 스크립트와 소스 참조 연결은 추가 조사 대상.
- v45의 `acacia_shelf` 7 leaf 및 기존 v38 부모/UV 연구는 신규 실적으로 다시 세지 않았다.
- Mojang 압축 client.jar 인증·Minecraft 인게임 렌더/런타임 인증은 필수 완료 조건에서 제외됐고, 실제 수행하지 않았다.
- v42 1-1 승인 원본 텍스처 **150/150 완료**, 전체 상위 세부과제 **1/5 완료 유지**. 가구 모드, Project Zomboid 변환, 실제 가구 모델 제작은 이번 범위 밖.

## 증거 파일
[544행 v46 원장](01_P1_544_MODEL_VERIFICATION_LEDGER.csv) · [49개 서술형 원문 감사](02_HISTORICAL_49_MD_JSON_AUDIT.csv) · [32개 약한 이름 참조](03_HISTORY_NAME_ONLY_32.csv) · [기존 crafter SHA 4개 재발견](04_HISTORY_EXACT_P1_SHA_4.csv) · [아홉 원본 모델](05_PARTICLE_ONLY_9_ORIGINAL_MODELS.csv) · [9개 블록상태 조회](06_BLOCKSTATE_LINK_9.csv) · [7경로 두 SHA 충돌 그룹](07_SHARED_BLOB_PATH_COLLISIONS.csv) · [최근 30 CSV 감사](08_RECENT_30_CSV_RECHECK.csv) · [신규 5개 경로 링크](09_NEW_5_P1_SOURCE_LINKS.csv) · [문제원장](10_ISSUES.csv) · [기계 요약](SUMMARY.json) · [다음 채팅 인계](NEXT_CHAT_HANDOFF.md).
