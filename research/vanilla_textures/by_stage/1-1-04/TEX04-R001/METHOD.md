# TEX04-R001 — 측정 정의와 재현 절차

- 검증일: 2026-11-13. 범위: 1-1-04 양털 9개만.
- GitHub 연결에서 `InventivetalentDev/minecraft-assets` 저장소의 `1.21.11` ref를 지정하고 9개 PNG 바이너리를 base64 형태로 가져왔다. 문자열의 개행을 제거해 디코딩한 **실제 바이트**의 SHA-256을 표본 v4 CSV와 항목별 대조했다.
- PNG 시그니처(8바이트), IHDR, PLTE, IDAT, IEND를 검사했다. 각 청크의 전송된 CRC-32와 `zlib.crc32(chunk_type + chunk_data)`를 비교하고 PNG를 Pillow로 성공적으로 디코딩했다. PNG 원본은 indexed palette(color type 3)이지만 RGBA로 변환하여 각 16×16=256 픽셀의 알파와 색상을 측정했다.
- 9개 모두 CRC32 검사 통과·디코딩 성공·256개 픽셀의 alpha=255·0개 알파 부분투명이다. 파일별 PNG 바이트 수·해시는 `SOURCE_LEDGER.csv`.
- RGB 평균은 각 채널의 산술평균. `mean_luma_rec709`은 **감마 보정 없이** 8비트 채널에 `0.2126R + 0.7152G + 0.0722B` 적용 후 평균한 분석용 밝기 근사치다. 물리적 선형 휘도나 게임 조명 결과가 아니다.
- 평균 HSV 채도는 각 픽셀별 `(max(R,G,B)-min(R,G,B))/max(R,G,B)`(최대값 0이면 0)을 산술평균.
- `luma_std_population`은 256픽셀 밝기의 모집단 표준편차(ddof=0), `luma_cv`=표준편차/평균.
- 좌우/상하 인접 RGB 변화량은 실제 인접한 240쌍의 픽셀별 3채널 절댓값 차이를 평균한다. 테두리 seam은 각 16쌍의 좌우 끝 / 상하 끝 픽셀의 같은 채널 절댓값 평균. 이 값은 눈에 보이는 반복 경계에 대한 진단 지표일 뿐 렌더링 경계의 매끄러움을 인증하지 않는다.
- RGB 고유색과 정보 엔트로피는 원본 RGBA 디코딩 후 정확한 RGB 빈도 계산. `adjacent_exact_rgb_match_ratio`는 가로/세로 인접 480쌍의 RGB 완전 일치 비율.
- 색 간 무늬 유사성은 256픽셀 동일 좌표의 밝기 순위에 대한 Spearman 상관으로 비교했으며 비대각 36쌍이 0.999237~0.999991. **동일 픽셀/팔레트 인증으로 해석하지 않는다.**
- 정적 모델 연결은 9개 `blockstates/{color}_wool.json`, 9개 `models/block/{color}_wool.json`, 공유 `models/block/cube_all.json`, `models/block/cube.json`을 각각 열어 상속을 추적. 9×6=54면의 full-face UV `[0,0,16,16]`은 `cube.json`에서 UV 배열이 생략된 **기본 면 매핑 규칙을 해석한 값**이다. 명시 UV 배열이 있다는 의미가 아니며 3D 게임 렌더를 직접 샘플링한 것도 아니다.
- `54면 × 256 texel = 13,824`는 동일 원본 PNG가 6면에 참조되는 횟수의 총합이다. **고유 원본 픽셀은 2,304개**로만 계산.
- 공식 Mojang client.jar·런처 메타데이터를 이용한 SHA 인증 및 인게임 정적 장면 비교는 수행하지 못했다. F는 미완료다.
- 원본 PNG는 저작권을 고려해 결과 저장소에 재배포하지 않고 URL, 원본 SHA256, Git blob SHA와 측정 CSV만 저장한다. 실험용 로컬 디코딩/미리보기 이미지는 GitHub 실측 결과와 별도다.

참고: v4 원본 선택 파일 `research/vanilla_textures/v4_150/01_누적150종_픽셀측정.csv`, 150 번호 원장, v35 16PNG 교차표, v36 544모델 과거 SHA 대조표를 확인했다. v35·v36의 후자 표에서는 선택된 `*_wool` 경로가 0건이며 v37/38 연구 주제는 양털과 별도였다.
