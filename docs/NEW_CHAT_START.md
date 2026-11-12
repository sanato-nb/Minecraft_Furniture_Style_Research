# 새로운 ChatGPT 채팅에서 이어하기

아래 내용을 **복사해 새 채팅의 첫 메시지로 보내세요.** 같은 ChatGPT 프로젝트에 있으면 좋지만 필수는 아닙니다. GitHub 연결 권한이 있어야 자동 업로드가 가능합니다.

---

이전 채팅에서 진행하던 **Minecraft 가구 모델링 디자인 학습 프로젝트**를 이어서 진행해 줘.

**정본 GitHub 저장소:** https://github.com/sanato-nb/Minecraft_Furniture_Style_Research

**반드시 먼저 읽을 파일:**
1. https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/HANDOFF.md
2. https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/PROGRESS.md
3. https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/SOURCES_AND_LIMITS.md
4. https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_models/v10/00_v10_누적DB_통합검증_보고서.md

**현재 체크포인트는 v10.** 바닐라 텍스처 150종 표본 분석 완료(공식 JAR·인게임 검증은 미완료), 바닐라 3D 모델 구조 분석 02번 진행 중, 가구 모드 분석 03~05번 미시작. 완료 0/5. v8 SQLite + v10 SQL migration으로 최신 DB를 재구성 가능. **전체 완료율을 임의로 만들지 마.**

**해야 할 일:** 기존 파일을 먼저 확인하고 같은 분석을 반복하지 말 것. 02번의 미검증·미완성 부분에 대해 검증 가능한 실제 모델/렌더 데이터를 추가 분석하고, 근거가 부족하면 보류로 표시할 것. 필요한 경우 가구 모드 조사에 착수할 수 있으나 02를 완료 처리하지 말 것. 분석 결과를 보고서·CSV/DB로 보존하고 GitHub에 업로드한 뒤 `HANDOFF.md`, `PROGRESS.md`, `README.md`를 업데이트해 줘.

**프로젝트 범위:** 상위 1단계(바닐라+가구모드 학습)와 상위 2단계(모델링 디자인 규칙서)까지만. **Project Zomboid 가구 변환 또는 실제 3D 가구 제작 제외.** 원본 Minecraft/모드 에셋 무단 재배포 금지.

계획만 말하지 말고 실제 분석 작업을 진행하고 진행도를 보여줘.

---

새 채팅에서 파일 접근에 제한이 있으면 GitHub 저장소의 **기존 보고서·CSV/SQL을 우선 사용**하세요. v10 바이너리가 없으면 `python scripts/rebuild_v10_db.py`로 재구성할 수 있습니다. GitHub 연결이 없는 새 채팅에서는 로그인/연결을 요청받을 수 있습니다.
