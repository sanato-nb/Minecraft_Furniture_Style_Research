# v60 다음 채팅 1-2-A 인수인계 (Minecraft 1.21.11)

- GitHub `main` HEAD를 새로 조회하고 v61 이상이 있으면 최신 우선. `research/vanilla_models/v60/REPORT.md`, `SUMMARY.json`, `07_P1_544_EVIDENCE_LEDGER.csv`, `VALIDATION_POST_RESEARCH_COMMIT.json` 확인.
- P1 **544행×279열** (v59 이전 259열×544행 전 셀 동일). 이번 신규20열 중 14개 P1 모델 행만 값 추가. v53 new175, v57 16, v58 27, v59 35와 겹치지 않는 모델: 랜턴 리프12 + 설치/매달림 추상 템플릿2. **P1 새 신원 링크 0**, 기존 544/544 path/SHA 식별을 완료율로 취급 금지.
- `00A_`/`00B_`: 14개 원본 모델 JSON·Git blob SHA. leaf는 자체 elements 0, 두 템플릿 각 4 elements, 원본 own합 8요소31면. **상속 적용56요소217면** (원본 명시UV217/암시후보0). 0두께28/회전28/U반전28, `cullface=down` 7. `01_` 모델별 구조·상속, `02_` 217면 CSV.
- 리프 12모델의 PNG 6경로 해결 face refs **186개**. 독립 추상 부모 2개 **31면**의 `#lantern` 슬롯은 leaf 없이 미해결; PNG 샘플 완료로 포함 금지.
- `00C_`: 원본 blockstates6파일×2variant=12, 원본 `.png.mcmeta`6개 모두 `animation.frametime=8`. 이는 텍스트 선언이며 런타임 애니메이션/UV 공식 인증 아님.
- `03_`: 실제 GitHub 6 PNG 바이너리 SHA1/SHA256와 Python/Pillow full RGBA 복원. 각 PNG16×48(16×16×3 프레임). 총 4,608 실소스 픽셀, alpha0 2,700/alpha255 1,908, 부분 alpha0. 설치형15면·3프레임×6 + 매달림16면·3프레임×6 = **558 face/frame crop**, 중복 포함 **12,168 실 source RGBA 픽셀 관측** (opaque11,736, 투명432), 중복 제외 **2,088 (파일,x,y)**. `REPRODUCE_PILLOW_LANTERN_AUDIT.py`는 GitHub에 저장, 실제 전체 소스 checkout 환경에서 완성 재실행 여부는 '미실행'; 원본 PNG/face crop은 별도로 실제 Python 수행.
- 원본 명시 UV 중 U 반전 면은 원본 그대로, crop 시 min/max 좌표 정규화. crop은 소스 사각형 대조이지 Minecraft 엔진 UV 방향/회전/광원 렌더 인증이 아님. 일반 스타일 규칙 확정 금지.
- **다음 작업:** v60에서 아직 표본으로 분석하지 않은 P1 277개 선택범위 안에서 가구 비례·평면/요소·UV/PNG를 직접 검증, 이전 v1~v59 의미론적 근거와 실제 원본 코드 교차 통합, 공식 엔진 1.21.11 암시UV/회전/UVLOCK·셜커13/skull1 렌더러 확인. P1 277이라는 수치를 '전부 미검증'으로 오인하지 말 것.
- 보존 규칙: 1-1 승인150/150, 상위1/5, 1-2-A/1-2 진행·실질 완료율 미산정, 모델 제작/좀보이드 변환 아직 시작 금지, v56의49 PNG 등 이전 실적 재집계 금지, 원본 asset key `(asset_type, full_source_path, git_blob_sha)`. commit 직전 최신 HEAD 재확인/임대, commit 이후 원격 readback 및 검증 기록 필수.
