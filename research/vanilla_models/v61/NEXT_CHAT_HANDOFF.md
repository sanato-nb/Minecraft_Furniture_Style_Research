# v61 → 다음 채팅 1-2-A 이어가기

## GitHub 현재 체크포인트와 다음 시작
- 현재 v61 연구 `research/vanilla_models/v61/`. 먼저 저장소 `main` 실제 HEAD를 새로 조회하고, v61 또는 더 새로운 버전의 `SUMMARY.json`, `REPORT.md`, `07_P1_544_EVIDENCE_LEDGER.csv`, `VALIDATION_POST_RESEARCH_COMMIT.json`를 직접 읽는다.
- P1 **544행×297열**. v60의 이전 **279열×544데이터행(151,776셀)** 셀 값 전부 동일; 이번 새 18열은 선택11개 모델에만 새 근거 기록. 기존 identity SHA는 재검증했지만 새 링크 **0**.
- 이번 1-2-A 심층 재검증 **가마솥 11개** (empty base1 + shared templates3 + material/level leaves7): 원본 own55요소235면, 상속 적용153요소648면, 원본 명시UV0, 결측UV648(엔진 실제 암시UV 미인증), 원본 PNG 경로 해결면645, 추상 부모 독립 #content 미해결3, tintindex=0 내용물 surface 면10. 모든 원본 모델 JSON+SHA `00A_`; face 648 CSV `02_`.
- 원본 blockstates4파일 **8variant** 직접 대조; 레벨1/2/full 내용물 top Y=9/12/15, 원본 `from:[2,4,2]` 공통; `03_`.
- 원본 texture PNG7개 GitHub 경로+SHA+IHDR: 정지5개는 원본 PNG GitSHA1 재계산·Python Pillow 전체 RGBA1,280px (불투명1008 / 투명272) 실검증. **water_still 16×512, lava_still 16×320은 IHDR와 두 mcmeta 선언만 검증**, animated PNG **전체 RGBA/Pillow 색상 검증 안 함**; 원본 mcmeta frametime=2, lava frames 배열 38. `00B_`, `00C_`.
- 이 회차 **원본 UV 0면**이므로 source PNG 파일과 implicit face를 연결했다고 648면별 픽셀 샘플 완료 주장 금지. 상속/face path 직접 기록과 엔진 UV orientation 구분.
- 이전 v53 new175, v57 재검증16, v58 27, v59 35, v60 14를 신규로 다시 세지 않기. 그 밖의 남은 **266개 P1**은 과거 근거도 보유할 수 있으며 의미론 전체 재검토 미완료. 공식 엔진 암시 UV/rotation/UVLOCK/tint/animation, 14개 특수 renderer 확인 계속.
- v61 연구 파일 `01_` geometry + `02_` original 648 face + `04_` observations + `05_` overlap proof + `08_` issues + `REPRODUCE_CAULDRON_V61.py`. 재현 스크립트는 full source checkout에서 실행했다는 증거 없음.
- **1-1 승인 150/150, 상위 1/5 완료**. 1-2-A 및 1-2는 아직 진행중, 실질 완료율 없음, 마크 가구 모델 제작이나 좀보이드 맵 변환 금지.
- 다음 작업은 겹치지 않는 P1 모델 원본 전체/PNG 실제 픽셀/엔진 정의 연구와 v1~v60 의미론 통합. 커밋 직전 HEAD 재확인·fast-forward lease, 사후 GitHub remote readback 및 validation 결과 기록.
