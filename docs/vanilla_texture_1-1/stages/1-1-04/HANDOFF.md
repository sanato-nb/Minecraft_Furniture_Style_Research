# 1-1-04 — 직물·양털 전용 채팅 인수인계

> **현재 단계 고유 버전: `TEX04-R001` (2026-11-13)** · 다음 예약 번호: `TEX04-R002` (커밋 전 반드시 다시 확인) · 상위 역사적 체크포인트 `v38` 유지.

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
