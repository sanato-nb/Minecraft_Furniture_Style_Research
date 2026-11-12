# 새로운 ChatGPT 채팅에서 Minecraft 가구 모델링 학습 이어하기

아래 구간의 내용을 새 채팅의 첫 메시지로 그대로 붙여넣으세요.

---

**Minecraft 가구 모델링 디자인 연구를 v13 체크포인트부터 이어서 실제 분석해 줘.**

정본 저장소: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research

반드시 먼저 다음 GitHub 파일을 직접 읽어:
1. `HANDOFF.md`
2. `PROGRESS.md`
3. `SOURCES_AND_LIMITS.md`
4. `research/furniture_mods/v13/00_v13_모드PNG실화소_UV픽셀정렬_보고서.md`
5. `research/furniture_mods/v12/00_v12_Handcrafted_교차분석_보고서.md`
6. `research/furniture_mods/v11/00_v11_AnotherFurniture_모델분석_보고서.md`

**현재 v13 상태:** 바닐라 텍스처 150/150종 표본 측정, 바닐라 3D 모델 분석 v10 진행(공식 `client.jar`/인게임 미검증). 가구 모드 03번은 Another Furniture(1.21.1) 템플릿 69종/완성형 33종, Handcrafted(1.21.x 소스) 원형 120종/생성형 16종/블록 상태 12종을 실제로 읽어 분석함. 04번은 두 모드 PNG 각각 12개씩 **24개 실제 픽셀 분석 완료**, 13개 원형 모델 **UV 571면 모두 픽셀 경계에 정렬**된 것으로 확인했어. **모델 face→PNG의 정확한 화소 대응 및 게임 렌더 검증은 미완료**. 05번은 두 모드 5유형의 사전 비교표만 작성했으며 정식 바닐라/모드 검증은 미착수. **전체 확정 완료 0/5, 임의 완료 퍼센트 금지.**

**바로 이어갈 일:** 기존 69·120 모델을 처음부터 다시 측정하지 말고, 1) 공식 원본으로 검증 가능한 Macaw's Furniture 1.21.11 JAR 또는 소스를 확보해 실제 모델 분석(미검증 제3자 미러 자료는 제외)하거나, 2) Another Furniture·Handcrafted의 v13 PNG 실측 CSV와 UV 571면 결과를 바탕으로 **각 모델 face가 참조하는 PNG 영역과 화소를 직접 연결 검증**하고 다른 재질/색상 표본으로 확대해. 분석 결과를 CSV/MD/DB에 기록하고, 원본 에셋 재배포 없이 GitHub에 업로드한 뒤 `HANDOFF.md`, `PROGRESS.md`, `README.md`, `handoff/STATE.json`을 **다음 체크포인트로 함께 갱신**해 줘.

이번 프로젝트 범위는 **상위 1단계(바닐라·모드 디자인 연구) 및 상위 2단계(근거 기반 디자인 규칙서)**까지만. Project Zomboid 가구 변환이나 실제 3D 가구 제작은 하지 말 것. 분석 근거와 추론/미검증을 항상 분리할 것.

---

만약 GitHub 연결이 없다면 읽기만 먼저 하고, 쓰기 작업은 연결 권한을 확인하세요. Handcrafted/Another Furniture 리소스는 각각 사용권이 제한되어 있으므로 원본 PNG·모델 JSON을 연구 저장소에 그대로 올리지 마세요.
