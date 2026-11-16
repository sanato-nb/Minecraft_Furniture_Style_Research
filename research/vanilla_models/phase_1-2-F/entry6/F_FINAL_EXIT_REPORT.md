# 1-2-F — Minecraft Java 1.21.11 바닐라 모델 원본 기반 스타일 조사 최종 종료 보고

**2026-11-17 · 계약상 최종 상태: `F_COMPLETE_SOURCE_STYLE_TAXONOMY_SCOPE`**

이 완료 표시는 **사용자 제공 1.21.11 추출 파일 2,390개에 대한 JSON 기하·C 텍스처 첫 프레임·D 정적 조립 근거를 분류해 기록하는 F의 소스 범위**에 한정한다. **마인크래프트 공식 JAR 인증, 엔진 렌더링 실행, 좀보이드 가구 기능·정체 판정, 가구 모드·맵 제작은 포함하지 않는다.** E 예외 86개 renderer 미인증은 그대로 유지한다.

## 완료 원장과 6회 분모
| Entry | 고정 모델 수 | 누적 |
|---:|---:|---:|
| 1 | 150 | 150 |
| 2 | 494 | 644 |
| 3 | 495 | 1,139 |
| 4 | 494 | 1,633 |
| 5 | 379 | 2,012 |
| 6 | 378 | **2,390** |

- **2,390개 고유 모델 경로 및 Git SHA** 대조, P1 544 / P2 1,039 / P3 807. C의 일반 기하 모델 **2,304개**와 E 소관 **86개** 분리 유지.
- 선행 B와 맞는 적용 요소 **5,689개**, 선행 C의 적용 face **23,090개**, D 정적 원본 모델 선택 옵션 **7,592행** 대조. D 직접 참조 모델 **2,136개**, 미직접 **254개**를 구분한다.
- Entry6는 새로 **378개** 원본 JSON·SHA·상속·기하를 독립 검산했다. 그중 일반 기하 **371개** / E 예외 **7개**, 요소 **661개** / face **2,412개**, D 원문 모델 선택 **678행**. 소스 대조 불일치 **0건**.

## F3 시각 증거 보완 — 원본 PNG에서 직접 생성한 8장
- Entry6의 C 바인딩 참조에서 **원본 PNG 경로 332개**를 추려 원본 Git blob SHA **332/332**, RGBA SHA-256 **332/332** 일치 검증.
- 해당 332개 PNG **첫 프레임**으로 42개 단위 이미지 접촉시트 **8장**을 생성하여 직접 열람. 원본 이미지 바이트→RGBA·프레임·파일 SHA·행별 알파 비율을 기록했다.
- 이 중 **200개 첫 프레임은 알파 빈 영역이 없고**, **132개는 부분/빈 영역이 있으며**, **16개는 세로 프레임 확장 PNG**로 애니메이션 전체가 아닌 첫 프레임만 확인했다. 32개 대표 PNG는 직접 보인 색·윤곽·격자·선·구멍 등을 서술했고, 나머지 300개는 접촉시트 열람과 검증 가능한 픽셀 지표만 기록했다. 이 **332개 시트 스크리닝 자체가 PNG 332개의 물체 정체 인증은 아님**.
- Entry6 **340개 모델**은 원본 PNG 첫 프레임과 직접 연결되어 구조 vs 픽셀 세부 표현 후보를 기록했다. **38개**는 해당 leaf 모델에 바인딩된 PNG가 없으므로 개별 시각 스타일을 **미결정**으로 명시한 채 소스 범위 원장에 포함했다. 38개를 “PNG까지 검수한 모델”로 부르지 않는다.
- E 특수 모델 렌더러, 게임 내 실제 알파/컬러 틴트/발광, 애니메이션 전 프레임, 물체 이름 및 기능은 **독립적으로 인증하지 않는다**.

### 직접 근거 연결 예시
- `mud.json`(16³ 1요소 6면) + `mud.png`(회갈색 불투명 얼룩): 입체 부피는 JSON, 표면 반점은 PNG 픽셀.
- `oxidized_copper_grate.json`(16³ 1요소) + `oxidized_copper_grate.png`(녹청색 격자·알파 구멍): 빈 칸은 이미지 알파로 보이며 게임 충돌/광투과는 별도 미인증.
- `mushroom_block_inside.json`(0두께 한 면) + 불투명 황토색 픽셀: 얇은 도안과 두꺼운 가구 패널은 구별해야 함.
- `nether_sprouts.json`(0두께 회전 교차 2요소) + 배경이 대부분 비어 있는 청록색 싹 픽셀: 2개의 단단한 가구판이라고 볼 수 없음.
- `template_three_candles.json`(9요소 30면): 직접 바인딩 PNG가 없어 기하만 확정, 표면 무늬 미결정.

## 최종 F1~F5
| 게이트 | 소스 범위 판정 | 증거 |
|---|---|---|
| F1 모집단·원본 SHA | **PASS** | 2,390 경로/SHA, P1~P3, C/E/D 소관 |
| F2 두께·회전·비례·기하 | **PASS** | from/to·요소 5,689·면 23,090, E86 예외 |
| F3 PNG·UV·스타일 | **PASS / 한계 명시** | 원본 PNG 332개 첫 프레임 실물 열람, 연결 모델 340·바인딩 없는 38은 미결정 |
| F4 D 조립·전용 후보 | **PASS / 정적 소스** | D 선택 7,592, D 직접2,136/미직접254, 가구 적용은 가설 |
| F5 독립·원격 감사 | **PASS** | 원본 JSON 두 배치 독립 재계산, F3 신규 CSV 332·378·2,390행 및 이미지 8개 SHA, 보호 대상 변경0 |

## 주요 산출물
- 전체 고유 모델 통합: [F_ALL_2390_STYLE_SOURCE_COMPLETE.csv](../F_ALL_2390_STYLE_SOURCE_COMPLETE.csv) · [F_ALL_2390_SOURCE_STYLE_FINAL_AUDIT.json](../F_ALL_2390_SOURCE_STYLE_FINAL_AUDIT.json)
- F3 원본 이미지 증거: [visual_contact/](visual_contact/) (PNG 8장 및 검증 CSV/JSON) · [F3_GALLERY_INSPECTION_REPORT.md](F3_GALLERY_INSPECTION_REPORT.md)
- 332 PNG 시각 스크리닝: [F3_PNG_FIRST_FRAME_332.csv](F3_PNG_FIRST_FRAME_332.csv)
- 378모델의 구조-표면 교차: [F3_MODEL_TEXTURE_GEOMETRY_378.csv](F3_MODEL_TEXTURE_GEOMETRY_378.csv) · [STYLE_OBSERVATIONS_F3_ACCEPTED_378.csv](STYLE_OBSERVATIONS_F3_ACCEPTED_378.csv)
- 의도적 미확정 38모델: [F3_UNBOUND_OR_TEMPLATE_38.csv](F3_UNBOUND_OR_TEMPLATE_38.csv)
- 독립 종료 근거: [F_FINAL_INDEPENDENT_EXIT_AUDIT.json](F_FINAL_INDEPENDENT_EXIT_AUDIT.json) · [F_FINAL_GATE_AUDIT.json](F_FINAL_GATE_AUDIT.json)
- 다음 단계: [F_NEXT_FOR_1_2_G.md](F_NEXT_FOR_1_2_G.md)

**Entry7은 자동 생성하지 않는다. 다음은 별도 1-2-G 통합 원본 일관성 감사·인수인계이며 아직 시작하지 않았다. 전체 1-2 완결 선언도 G 완료와 별도 게이트 전까지 하지 않는다.**
