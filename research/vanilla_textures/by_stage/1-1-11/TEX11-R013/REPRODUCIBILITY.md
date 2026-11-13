# TEX11-R013 — 재현 절차

1. 원본 Git tree `textures/block/` (`9a7172896d4a28b405b990733d51b77dcb50930c`)에서 R012 `STATE.json` target 31 PNG가 모두 존재하는지 확인하고 각 이름의 `.png.mcmeta` 부재를 검증. 타 블록의 `.png.mcmeta`는 대상 수치에 넣지 않는다.
2. 저장된 `PNG_ANIMATION_METADATA_AUDIT.csv`에서 31 PNG chunk CRC, IHDR, 26×16/5×32 이미지 크기, `acTL/fcTL/fdAT` 부재를 재확인.
3. `JSON_ANIMATION_FIELDS_AUDIT.csv`는 현재 Git tree SHA 일치 24 blockstate,122 leaf,20 template 총166 JSON. 재귀 검색 대상 키 `animation,animations,frames,frame,frametime,interpolate,interpolation,duration,duration_ticks,ticks,keyframes,loop`, 발견 수 0.
4. `open` 전후 door7×4facing×2half×2hinge=112, trapdoor12×4facing×2half=96, `powered` 전후 shelf5×4facing×4side_chain=80. 총 288 static endpoint comparisons.
5. 선반 `side_chain` 4종 중 pair6 × 5woods × 4facing × 2powered=240 논리 조합 후보. 전체 528개 후보 중 모델 참조 차이408, 차이 없음120(전원 꺼진 shelf).
6. `variants`와 `multipart[].when`을 실제 원본 JSON 규칙으로 매칭하여 모델 이름·정적 xyz·uvlock를 저장. leaf `parent`→template `elements[].from/to`, `faces[].uv`를 대조하여 core 288쌍의 geometry/UV 변동을 집계. `x/y`는 static property, smooth timeline 생성 아님.
7. 이 자료는 **소스 기반 증거**다. 게임 실행/스크린샷, 실제 runtime duration·easing·pivot, 새 애니메이션 클립 제작은 수행하지 않는다. 해당 실험은 사용자가 완료 필수 범위에서 제외했다.
