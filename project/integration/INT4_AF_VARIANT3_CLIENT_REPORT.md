# INT-4 AF variant=3 실제 Minecraft 클라이언트 F2 촬영 실험

## 목적과 기존 연구 연결

[PR #37](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/37)에서는 연구 4.0.3 및 실행 4.0.2 원본에서 Another Furniture의 acacia_chair variant=3이 남쪽에서 acacia_1, 북/동/서에서 acacia_3을 선택하는 **출처 불연속 1건**을 검증했다. 두 자식의 기하·UV는 동일하지만 등받이 관련 **12/46면**의 원본 PNG 바인딩이 바뀌고, back_1/back_3 텍스처는 **54/256 RGBA 픽셀**이 실제로 다르다.

본 후속 INT-4는 원본 출처 검증과 별도로, **실제 Fabric 게임에서 variant3의 네 방향이 존재하고 지정 블록상태가 서버에 유지되며 F2 네 장이 나오는지** 실험한다. 더불어 같은 북/남 방향의 variant1 두 장을 대조군으로 촬영하여 실제 화면 관찰용 자료를 마련한다.

## 실제 실험 범위

| 케이스 | 원본 모델 선택 | 블록상태 y | 용도 |
|---|---|---:|---|
| AFV3_north | acacia_3 | 0 | variant3 북향 |
| AFV3_east | acacia_3 | 90 | variant3 동향 |
| AFV3_south | **acacia_1** | 180 | 남향 모델 선택 불연속 |
| AFV3_west | acacia_3 | 270 | variant3 서향 |
| AFV1_north | acacia_1 | 0 | 북향 비교 대조 |
| AFV1_south | acacia_1 | 180 | 남향 비교 대조 |

대상: Minecraft 1.21.1 + 고정 Fabric 0.18.4 + 기존 고정 Another Furniture 4.0.2. 원본 JAR SHA와 원본 연구 4.0.3 SHA를 다시 대조한다. 서버 생성 평지 월드를 **임시 복제하여 수정**, 사용자 저장 월드나 역사 증거를 수정하지 않는다.

모든 케이스를 동일 z=40, x간 16블록 간격 이상에 배치. 실제 게임의 \`/setblock\`, \`/execute if block\`로 블록상태를 확인한 후 실제 클라이언트 \`F2\` 출력 PNG를 1024×684로 보존하고 SHA를 기록한다. 기존 PR #34의 배경 간섭 검사를 해당 새 케이스에 적용한다.

## 구현·보존 원칙

- \`src/mcfr/int4_af_variant3_capture.py\`: 새 여섯 개 케이스의 정확한 원본 상태·모델·y 및 개별 사진 SHA/클라이언트 관찰용 접촉시트 검증.
- 기존 \`src/mcfr/chair_runtime_fixture.py\`와 \`chair_runtime_capture.py\`: 선택 케이스를 **선택적으로 주입할 수 있는 확장**만 적용해 PR #33/34의 16개 기본 케이스 유지.
- \`src/mcfr/runtime.py\`: \`af-variant3-capture\` 명령 하나만 추가. 기존 다운로드 및 GUI 캡처 엔진 그대로 사용.
- \`tests/knowledge/test_int4_af_variant3_capture.py\`: 원본 선택자·월드 격리·해시·자료 범위 오승격 회귀테스트. 합성 이미지로 작성한 테스트는 CI의 실제 F2 증거로 간주하지 않음.
- \`.github/workflows/integration-int4-af-variant3-runtime.yml\`: GitHub Actions에서 실제 Java 21·Fabric 1.21.1 실행, 임시 평지 월드 생성, 여섯 장 F2 촬영과 확인.
- 산출물: \`INT4_AF_VARIANT3_REAL_F2_CAPTURE.json\`, \`INT4_AF_VARIANT3_CLIENT_AUDIT.json\`, \`INT4_AF_VARIANT3_REAL_F2_STATES.csv\`, \`INT4_AF_VARIANT3_F2_6_CONTACT_SHEET.png\` 및 F2 PNG 6장, 런타임 로그.

원본 PNG·JAR·모델 JSON, 실제 게임 스크린샷 바이너리는 **Git 저장소에 직접 커밋하지 않는다.** GitHub Actions 아티팩트에서 단기 보존하고, Git에는 결과 SHA·건수·범위만 고정한다.

## 명시적 판정 경계

실제 F2 파일 6장이 검증되더라도 남쪽 의자가 다른 등을 보여준다고 **자동 확정하지 않는다**. 촬영마다 배경의 풀 텍스처·광원 등 픽셀이 달라지므로 동일 상대 카메라의 중앙 픽셀 차이는 인과관계가 아니라 **진단 데이터**다. 원본 모델 선택이 다른 북쪽 대조군과 모델 선택이 동일한 남쪽 대조군을 이용해 **사람의 시각적 검수**를 계속해야 한다.

- \`INT4 전체 가구 교차검증 완료=false\`
- \`INT5 부품 역할 승인=0\`
- \`실제 화면 54픽셀 동일성 승인=false\`
- \`사용자 정의 모델·스타일 규칙 승인=0\`
- \`AI 학습/권리 승인=0\`

## 실행 명령

\`\`\`bash
export PYTHONPATH=src
python -m mcfr.chair_runtime_fixture world --version 1.21.1 \
  --path /tmp/mcfr-af-v3-world --cache /tmp/mcfr-af-v3-world-cache
xvfb-run -a -s '-screen 0 1024x684x24' \
  python -m mcfr.runtime af-variant3-capture --version 1.21.1 \
  --work /tmp/mcfr-af-v3-client --world /tmp/mcfr-af-v3-world \
  --output /tmp/mcfr-af-v3-f2
python -m mcfr.int4_af_variant3_capture --root . --directory /tmp/mcfr-af-v3-f2
\`\`\`

**CI에서 클라이언트가 실제로 성공하기 전에는 F2 촬영 완료 수치를 확정하지 않는다.**
