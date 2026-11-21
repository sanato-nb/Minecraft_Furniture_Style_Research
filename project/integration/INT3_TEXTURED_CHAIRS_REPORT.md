# INT-3 텍스처 적용 가구 외형 연구 — 원본 의자 4종 229면

기준 연구: 1-3-C/F 기하 모델 및 부품 역할 후보, INT-2 1-4 원본 PNG·UV 독립 감사, PR #29 원본 모델 검수, PR #30 부품별 기하 시각화.

**완료 범위:** AF 기본/넣은 의자, HC 의자, Macaw 의자의 **실제 텍스처가 지정된 자식 모델 4개**를 선택하고 원본 PNG 픽셀로 그린 두 방향 정사영 진단 렌더를 생성했다. 부모 템플릿에는 텍스처가 선언되지 않을 수 있으므로, 자식 모델의 부모 체인을 신원·SHA로 검증한 후 슬롯을 해석한다.

## 근거와 검증 방법

- GitHub 원본 저장소 AF commit `57eb624cbb7f408d43398c7434b0d38d312cb55d`, HC commit `8d21d1665916850c3fa3bdaf1370c50ec2ca7035`, 공식 Macaw Fabric v3.4.2 JAR SHA-256 `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e`, 바닐라 클라이언트 1.21.1/1.21.11의 고정 JAR을 그대로 사용했다.
- 기존 PR #29의 `render_int3_chair_geometry.read_providers`로 **4개 부모 기하 모델 45개 요소**의 실제 원본 JSON·원장 정합 검사를 재사용한다. 장면 조립을 새 추정 좌표로 대체하지 않는다.
- 자식 원본 JSON과 `lineage`의 전체 상속 모델 JSON을 SHA 대조한 후 텍스처 슬롯/별칭 병합. 슬롯이 해결되지 않거나 원래 `face`의 UV·회전이 F 원장과 달라지면 실패한다.
- 각 텍스처 원본 PNG는 F 원장이 가리키는 정확한 파일 경로에서 다시 열어 **소스별 Git blob SHA-1 또는 SHA-256**과 PNG CRC를 검증한다. 소수와 분수로 달리 표기된 UV는 좌표의 수학적 값으로 비교하고, 미선언 기본 UV는 INT-2에서 1.21.1 게임 바이트코드와 대조한 방향별 공식으로 계산한다.
- **총 229개 면의 슬롯·UV·회전·원본 텍스처 SHA를 전수 확인**. 8개 고유 PNG를 연결. 4개 자식 모델의 모든 229개 면은 기존 독립 INT-3 지식 DB에서도 `SOURCE_REGION_REMEASURED`로 표기되어 있으며 이번 재실행에서도 누락·오류를 발견하지 못했다.

## 원본 자식 모델별 결과

| 모드 / 자식 모델 | 원본 부모 | 검증 면 | 소스 PNG | 정사영 그림에서 관찰한 외형 |
|---|---|---:|---:|---|
| Another Furniture `AF121` — acacia_1 | `AF1393` | 46 | 3 | 갈색·주황빛 목재 무늬처럼 보이는 좌판과 등받이·다리, 프레임 연결 |
| Another Furniture `AF123` — acacia_10_tucked | `AF1394` | 46 | 3 | 같은 계열 질감이지만 등받이 모양과 일부 부품 위치가 다른 의자 |
| Handcrafted `HC11210` — warped_chair_black | `HC13` | 78 | 2 | 청록빛 조립 프레임과 검은색 시트의 시각적 분리 |
| Macaw `MACAW67` — acacia_chair | `MACAW1424` | 59 | 2 | 회갈색 기둥·등받이 프레임과 주황·갈색 좌판의 대비 |
| **합계** | 4개 부모 | **229** | 고유 8개 | 화면 8개(모델당 두 시점) |

위 기록은 **출처가 고정된 픽셀에 대한 진단 그림의 관찰**이며, 물리적 소재를 확인하거나 해당 모드의 모든 가구에 보편화하는 `MATERIAL_VERIFIED` 판정이 아니다. 원본 텍스처 이름과 실제 소재는 구분한다.

## 실제 생성 증거

- `scripts/integration/render_int3_textured_chairs.py` — 원본 5개 아카이브를 읽어 기하·부모 체인·원본 면·텍스처·UV 전체 교차감사, 진단용 최근접 픽셀 투영.
- `tests/integration/test_int3_textured_chairs.py` — 소수·분수, UV 반전과 회전, 합성 원본 픽셀과 4개 자식 범위 검증.
- `project/integration/INT3_TEXTURED_CHAIRS_SOURCE_SUMMARY.json` — 자식별 모델·원본 SHA·8개 PNG 경로/해시·229면 수·진단 출력 이미지 SHA 및 CSV SHA.
- CI 아티팩트 `int3-four-textured-chair-source-uv-diagnostic` — 원본 데이터 본문 대신 결과 미리보기 PNG, 229면 출처 CSV, 생성 JSON을 보관.
- [원본 아카이브를 직접 확인한 최초 성공 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44887449048).

검수 이미지 SHA: `ede6e7a6407f1432ab3e07e49c2397dfeffc33789b1e1352fb772d73bb02207d`. 원본 229면 CSV SHA: `dc790656f4df32f66e21ef46b7db7c1027cd01be504ebc4b2a2b78f289074783`.

## 한계 및 다음 단계

**이것은 실제 게임 구동 스크린샷이 아니다.** 그림은 원본 PNG에서 샘플링한 면을 정사영으로 칠한 진단 이미지다. Minecraft의 UV lock, 블록상태 회전, 모델 베이크/아틀라스, 주변광 및 반투명 처리, 특수 렌더, 좌표별 게임 오브젝트 상태, 충돌·앉기 기능은 검증되지 않았다.

현재 승인:
- 원본 역할 기능 최종 확정 0
- 재료·스타일 검증 완료 라벨 0
- 게임 런타임 검사 0
- 저작권 사용·모델 학습/재배포 승인 0

원본 PNG/JAR/모델 JSON 바이트는 GitHub 새 커밋이나 CI 아티팩트에 넣지 않았으며, 출력 이미지는 원본 픽셀을 응용한 연구용 진단 자료로만 취급한다.

다음 진행은 **원본 실제 인게임 스크린샷 또는 모드/바닐라 블록상태 bake 결과와 이 진단 그림을 방향별 대조**하고, 반례·텍스처 회전/가림 문제를 실제로 확인하는 단계다. 그전에는 45개 후보 역할과 14개 비교 판정을 보편 규칙으로 승인하지 않는다.
