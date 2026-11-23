# INT-4-F11C 원본 연구 범위 고정 및 실게임 검증 경계

## 출처와 고정 분모

- 원본: `research/furniture_mods/phase_1-5/B/APPLICATIONS.csv` (Git blob SHA1 `56e6f4c21c50714b97079ec61f7219bea845f179`).
- 동반 집계: `research/furniture_mods/phase_1-5/B/CASES.csv`.
- 선행 F11B 독립 감사: 70개 중 조건부 63개 / HOLD 7개 / 최종 무조건 승인 0개.
- 이 문서는 원본 CSV에서 확인되는 정적 사실을 고정한 **시험 전 범위 메모**이며 실게임 F2 완료 증거가 아니다.

| 대상 | 연구 원본 블록상태 | 모델 원본 / 기하 제공자 | 요소 | 면 | 원본 텍스처 프레임 특징 |
|---|---|---|---:|---:|---|
| V12 | `minecraft:cauldron` | `cauldron.json` / 동일 | 13 | 58 | 정적 58 |
| V13 | `minecraft:water_cauldron[level=3]` | `water_cauldron_full.json` / `template_cauldron_full.json` | 14 | 59 | 정적 58 + 애니메이션 프레임 연관 1 |
| V14 | `minecraft:lantern[hanging=false]` | `lantern.json` / `template_lantern.json` | 4 | 15 | 애니메이션 프레임 연관 15 |
| V15 | `minecraft:flower_pot` | `flower_pot.json` / 동일 | 5 | 22 | 정적 22 |
| **합계** | **역사 연구 사례 4** | **모델 적용 4개** | **36** | **154** | **정적/애니메이션 근거 분리** |

### 예외 1 — V11 침대

- 원본 `V11 white_bed`의 `APPLICATIONS.csv`에 `geometry_status=NO_ORDINARY_ELEMENTS`가 기재되어 있고, `CASES.csv`에서는 **일반 모델 요소 0·면 0**이다.
- 일반 가구 모델·기하 JSON과 같은 1-5 검사만 수행하면 V11을 정확하게 심사할 수 없다. 실제 렌더러 및 렌더 단계의 별도 증거가 필요하므로 **HOLD**.
- 현재 F11C 일반 모델 촬영 대상(V12~V15)과 분리한다.

### 예외 2 — 정지 F2 ≠ 시간차 검증

- V13 수면의 프레임 관련 면 1개, V14 랜턴의 프레임 관련 면 15개는 원본 연구의 텍스처 분류 근거이다. `STATIC_SOURCE` 기하라는 표현만으로 이미지의 시간 변화를 부정할 수 없다.
- F11C는 네이티브 F2 **단일 화면과 정확한 서버 블록상태**를 획득하는 단계다. 렌더링 시간차·픽셀별 UV·수면 파동·랜턴 불빛 변화의 인과 승인은 별개이다.
- 고위험 R06(물이 있는 Macaw 싱크의 두 시점 화면) 및 R08(서로 다른 AF 릴리스 실제 게임의 동일 상태 비교)도 별도 HOLD.

### 실게임 진입 게이트

1. 원본 연구 파일 SHA, 공식 Minecraft 1.21.11 클라이언트 SHA1 및 SHA256 고정.
2. 선택 state/leaf/provider/부모의 Git blob SHA1과 rule/option/방향·요소·면 비교.
3. 실제 Minecraft 블록 배치 후 서버 상태 정확 재판독.
4. 실게임 원본 F2 PNG 4장과 client.log의 바이트 해시 확인 및 직접 시각 검토.
5. 독립 감사에서 변경된 70행이 정확히 V12~V15뿐인지 확인. 증거 불충분 사례는 HOLD.

**위 게이트 통과 이전에는 원장을 67/70으로 변경하지 않는다.** F 최종 승인, INT5 부품 의미, INT6 학습·재배포권, G/H 종료 심사도 모두 미승인 상태로 유지한다.
