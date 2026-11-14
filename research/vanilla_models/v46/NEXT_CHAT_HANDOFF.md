# v46 1-2-A 다음 채팅 인수인계

## 최신 우선 원칙
GitHub `main`의 **현재 HEAD부터** 확인한 후 `handoff/STATE.json`, `research/vanilla_models/v46/REPORT.md`, `v46/01_P1_544_MODEL_VERIFICATION_LEDGER.csv`를 열어라. 이전 v45 인수인계의 119는 이전 시점 수치.

## 계승해야 할 현황
- P1 **544개 모델 경로**, 출처 path+SHA 근거 연결 **124개**, 검사 범위 SHA 미연결 **420개** (미분석 확정 아님). 진정한 1-2 완료율 **미산정**, 1-2-A 계속 진행 중.
- v45 이전 119 유지. v46 **아홉 original model JSON 직접 읽기**: 기존 연결 `bed`, `chest`, `oak_sign`, `trapped_chest` 4 재검증, 신규 `banner`, `bamboo_sign`, `bamboo_hanging_sign`, `acacia_sign`, `acacia_hanging_sign` 5 source path+SHA 연결. 이 9개는 `parent`와 `elements` 키 부재, `textures.particle`만 명시. 실제 3D/UV/렌더러 미확정.
- P1 SHA는 **539개 고유 내용**. `banner/bed/chest/oak_sign/trapped_chest` 5 모델 경로가 한 SHA, `bamboo_sign/bamboo_hanging_sign` 두 모델 경로가 또 한 SHA 공유. `(asset_type, full_source_path, git_blob_sha)`를 모델 ID로 유지하고 **SHA 단독으로 증거 전파·중복 병합 절대 금지**.
- v5~v43 `research/vanilla_models`의 **Markdown 30개/JSON 19개** 전수 원문 재열람 및 SHA/path/name 스캔: SHA 일치 4개 모두 이미 연결된 v43 crafter; basename-only 32건/21모델은 약한 근거. 추가 연구 CSV 30개 직접 검사(인벤토리와 직접 증거 구분), 기존 v44 17개·v45 86개를 중복 신규 실적으로 만들지 않기.
- 블록상태 원본 7개에서 단일 `variants` / 해당 모델 참조 확인. 정확한 `banner.json`, `bed.json` blockstate basename은 조회 404; **색상별 파일 존재 여부 미검증**.
- 다음은 역사 SQLite와 build scripts, 이름만 남은 21개 모델의 원본 SHA 연결 증거를 조사하고, 그 뒤 가구 연관성이 큰 남은 P1 경로의 원본 모델/UV·special renderer 증거를 추가 검증하라.
- v43 SHA 자산 유형 오탐 2개 정정 유지, v38 오크 선반 원형/v45 아카시아 선반 원형 재활용. 공식 JAR 및 인게임 렌더 성공 주장 금지.
- v42 1-1 승인 소스 150/150 완료, 상위 1/5 완료 유지. 1-2 전체 미완료. PZ 변환/실제 모델 제작 제외.
