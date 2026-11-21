# INT-4 — Macaw 주방 실제 Fabric 1.21.11 카운터·싱크 3상태 F2 재현

## 왜 이 범위를 먼저 실행하는가

선행 [PR #41](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/41)은 비의자 가구 **15사례·19모델·431면·원본 PNG 431/431**를 소스 수준에서 검증했다. 그러나 게임의 Java/Fabric 모델 bake·서버 상태 유지·실제 F2 스크린샷은 새로 검증하지 않았다.

이번 INT-4는 **인접 상태·특수 렌더 부작용을 분리하기 쉽고 실제 원본 블록상태가 있는 Macaw 주방 대표 3건**을 먼저 실제 게임에서 조사한다. 원본 연구 중 C17(모드측 주방 싱크 변화)·C19(모드측 카운터 구성)과 연결되지만 C17 전체 바닐라 비교를 새로 한 것은 아니다.

## 원본에서 고정한 실제 배치 사례

| 사례 | 배치 블록 | 상태 | 원본 모델 | 기대 기하 |
|---|---|---|---|---|
| S41 | \`mcwfurnitures:oak_counter\` | \`facing=north\` | \`block/counter/oak_counter\` | 2요소·11면 |
| S42 | \`mcwfurnitures:oak_kitchen_sink\` | \`facing=north,water=false\` | \`block/counter/oak_kitchen_sink\` | 16요소·55면 |
| S43 | \`mcwfurnitures:oak_kitchen_sink\` | \`facing=north,water=true\` | \`block/counter/oak_kitchen_sink_filled\` | 17요소·56면 |

모든 모델의 독립 원본 자식·부모 경로/SHA는 역사 1-5 B 원장과 실제 **Macaw Fabric 3.4.2** JAR SHA-256 \`e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e\`에 고정한다. 실제 게임 버전 **Minecraft 1.21.11**, Java 21.

## 실제 실험 방법

1. Minecraft 공식 1.21.11 Java 서버로 신규 평지 Creative 저장 월드를 생성한다. 기존 사용자 월드를 변경하지 않고 이를 신규 게임 워크 폴더에 **복제**한다.
2. \`int4_macaw_kitchen_capture.py\`가 기존 PR #41의 검증 결과/원장 SHA와 실제 설치 JAR SHA를 대조한다. \`variants\` 실제 상태 선택 규칙·모델 경로·x/y 회전·uvlock·weight 및 자식→부모 모델 SHA·기하를 검증한다.
3. 기존 검증된 \`chair_runtime_fixture.make_pack\`의 **임의 source-state 사례 주입 기능만 재사용**한다. 사용자 save를 건드리지 않는 별도 데이터팩에서 x=-24,-8,8 / y=120 / z=40의 독립 블록 3개를 직접 \`/setblock\`한다. 내부 데이터팩 명칭이 \`mcfr_chair\`인 것은 과거 검증 엔진 호환을 위한 것이며 가구 정체를 의자로 해석한 것은 아니다.
4. **실제 Minecraft 클라이언트의 서버 로그**에서 \`/execute if block\` 성공을 **3/3 확인한 경우에만** F2 촬영을 허용한다. 상태가 자동 변경되거나 원본과 다르면 실패 처리하며 실제 게임 결함을 추정해 빈 상태를 PASS로 바꾸지 않는다.
5. 동일 상대 카메라에서 S41/42/43 PNG **세 장**(1024×684)을 F2로 촬영하고 클라이언트 로그·원본 SHA·PNG SHA를 남긴다. 3장 접촉시트를 생성해 향후 사람의 INT-5 시각 검토에 활용한다.

## 검수·권리 경계

- 실제 F2 사진 3장 확보는 **선택된 상태에서 실제 게임 화면 파일이 생성되었다는 사실**이지, 손잡이·수면의 의미/재료, 물결 움직임, 물 사용 기능·충돌이나 원본 PNG 픽셀의 GPU 표시 인과관계가 승인됐다는 뜻이 아니다.
- S42/S43 원본면 수 55→56은 정적 모델의 차이. **실제 애니메이션 프레임 움직임은 따로 측정**해야 한다.
- 각 사진은 서로 다른 x 좌표와 광원/배경을 지니므로 중앙 픽셀의 절대 차이를 원본 텍스처 차이로 바로 단정하지 않는다.
- 본 F2 아티팩트, 원본 JAR/PNG/모델 JSON을 Git에 직접 추가하지 않는다. 원본 외관·저작권·AI 학습 권한은 독립 검토가 필요하다.
- PR #41의 역사 원장·32~40 이전 단계 결과, \`main\`, 사용자 세계는 수정·병합하지 않는다.
- **INT-4 전체 종료=false, INT-5 부품 역할 승인=0, INT-6 AI용 권리 승인=0**.

## 실행 명령

\`\`\`bash
export PYTHONPATH=src
python -m mcfr.chair_runtime_fixture world --version 1.21.11 \
  --path /tmp/int4-macaw-world --cache /tmp/int4-macaw-world-cache
xvfb-run -a -s '-screen 0 1024x684x24' \
  python -m mcfr.runtime macaw-kitchen-capture --version 1.21.11 \
    --work /tmp/int4-macaw-work --world /tmp/int4-macaw-world \
    --output /tmp/int4-macaw-f2
python -m mcfr.int4_macaw_kitchen_capture --directory /tmp/int4-macaw-f2
\`\`\`

## 실행 결과

고정 CI 완료 후 실제 성공·실패를 구별하여 기록한다. 원본 55→56면 외에 실제 Minecraft F2 3장 촬영이 통과했다고 **선행 확정하지 않는다**.

## 실제 Fabric 1.21.11 F2 첫 촬영 성공 — 증거 고정 (2026-11-22)

[**GitHub Actions #44920889453**](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44920889453)에서 Java 21·Macaw 3.4.2 Fabric·Minecraft 1.21.11 게임 클라이언트를 실제 실행했다. 고정 JAR 전체 SHA 및 원본 선택 모델·부모 경로/파일 SHA 검증 뒤 **서버 블록상태 3/3 성공, Minecraft 네이티브 F2 PNG 3/3 성공**.

| 실제 상태 | 서버 확인 | 네이티브 1024×684 F2 | 원본 면 수 |
|---|---|---|---:|
| `S41` 카운터 `facing=north` | PASS | PASS | 11 |
| `S42` 싱크 `facing=north,water=false` | PASS | PASS | 55 |
| `S43` 싱크 `facing=north,water=true` | PASS | PASS | 56 |

특히 게임에서 `water=false`와 `water=true` 블록상태가 모두 실제 유지됐으며 이에 해당하는 원본 모델 파일은 55/56면으로 구분된다. **실제 게임 수면 애니메이션, 물의 사용 기능 및 GPU 픽셀의 인과적 일치는 아직 검증하지 않았다.**

### 변경 불가능한 첫 실행 증거

- [F2 3장·원본 모델 SHA 체크포인트](INT4_MACAW_KITCHEN_F2_SOURCE_RESULT.json) (첫 실행 F2 SHA-256과 접촉시트 SHA 기록)
- F2 S41: `600c03c6caf90c9788c80b8bd0132a839aa2cbc9a0e00e17930e52d16df26010`
- F2 S42: `8db5143963699aa7b89dab6efcb4bc71b82204769ad8eaee13b8e530d1805f7f`
- F2 S43: `300ce307dbad187e84a5abf977e5946992df28ecea3db8d362313c717c7f2b93`
- 실제 F2 manifest SHA-256: `1c0429fda6b949748fdf3ae414da8409a51c01fd37bafb32d31726369e98af5a`
- 3장 접촉시트 SHA-256: `5e789e98337d6a71e7da38712c994d89e28b539fd39b36da3404ec74b518df5c`
- 실제 게임 F2 3장, 3장 접촉시트, 클라이언트 로그 및 런타임 manifest는 GitHub Actions 아티팩트 `int4-macaw-kitchen-actual-fabric-three-f2` (ID 14713339690; ZIP SHA-256 `9b68f7ae007c59c54a8e27401698ba53f43a411d461f5a95d61222903144f98a`).
- 게임 설치/월드·원본 JAR/PNG/기존 연구 파일은 저장소에 포함/덮어쓰지 않았고, F2 바이너리는 **임시 아티팩트로만** 보존했다.
- 신규 촬영 결과는 수동 INT-5 시각 검수가 끝난 상태가 아님. 그 의미·스타일·자료 사용 권리 승인 0 유지.
- 새 CI는 실행마다 실제 F2/원본 SHA를 검증하고 최초 증거 체크포인트의 **상태·한계·건수**를 재대조한다. JPEG처럼 스크린샷 자체는 다른 실행 간 바이트 동일성을 강제하지 않는다.

**후속 INT-4**: 이어서 인접 상태를 고려한 연결 테이블·책장, Handcrafted 침대의 head/foot을 실제 상태·촬영 환경으로 분리 검증. 현재 INT-4 전체 완료 아님.
