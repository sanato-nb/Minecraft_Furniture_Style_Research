# TEX01-R008 · 목재 관련 원본 애니메이션 재개: 21 정적 표본 분리, 4종 18프레임 실측

2026-11-13 · Minecraft Java 1.21.11 · 사용자 명시 지시 **「보류한 애니메이션하자」**. 이번 연구부터 **1-1-01의 애니메이션 분석 보류 해제**. R001–R007 불변, 기존 인게임·공식 JAR 검증 제외 유지. 사용자 제공 GitHub `1.21.11/assets/minecraft/` 최우선.

## 1. 원래 21 PNG에 애니메이션이 있는가?

고정 18 + R007 확장 단면 3 = **21개**를 원본 `textures/block/` Git tree(1,210개 직접 엔트리)와 대조. **21/21 PNG 존재, 21/21 대응 `*.png.mcmeta` 없음**. 이전 R001/R007의 원본 디코딩에서 이 21개가 각각 **16×16 단일 프레임 이미지**임을 확인했다. 이번에는 추가 고유 픽셀로 중복 가산하지 않는다. 파일마다 원본 blob SHA와 `.mcmeta` 부재 여부는 `STATIC_21_ANIMATION_AUDIT.csv`에 기록한다.

**판정:** 해당 21종에는 Minecraft의 통상적인 PNG+animation mcmeta 프레임열이 없다. 이것만으로 런타임의 모든 효과/동적 모델 현상을 부정하는 것은 아니다. 원본 `block/`에는 `*.png.mcmeta` 파일이 **99개** 있으나 그중 일부(예: `oak_leaves.png.mcmeta`)는 `texture.mipmap_strategy=dark_cutout` 설정일 뿐 **애니메이션이 아니다**. 99개를 모두 애니메이션으로 간주하지 않는다.

## 2. 목재 연관 보조 애니메이션 소스 4개 신규 실측

원본 JSON `animation`의 `frametime`, `interpolate`를 직접 읽고, 원본 PNG **4종 바이너리 SHA256 + 총 16개 PNG 청크 CRC32**를 검증. RGB 16×16 프레임을 세로 스프라이트 시트에서 순서대로 분리했다(알파 전체 255, 추가 원본 **4 PNG, 18 프레임, 4,608 텍셀**). 명시 `frames`가 없어 **0..n−1 순차 재생 메타데이터**로 분류. 20 tick/s 가정 아래의 초 환산은 엔진 내부 실행 계측이 아니라 관례적 명목 환산이다.

| 텍스처 | 원본 크기 | 고유 프레임 | `frametime` | 한 주기 | `interpolate` |
|---|---|---:|---:|---:|---|
| `crimson_stem` | 16×80 | 5 | 10틱 | 50틱(명목 2.5초) | true |
| `warped_stem` | 16×80 | 5 | 10틱 | 50틱(명목 2.5초) | true |
| `campfire_log_lit` | 16×64 | 4 | 20틱 | 80틱(명목 4초) | true |
| `soul_campfire_log_lit` | 16×64 | 4 | 20틱 | 80틱(명목 4초) | true |

네 PNG는 전부 각각 서로 다른 4/5개 프레임이며, 4개의 개별 `.png.mcmeta`를 직접 조회했다. **프레임 사이 보간을 실제 게임 화면에서 측정한 것은 아님.**

## 3. 새 직접 RGB 픽셀 실측 및 색상 교차검증

모든 원본의 각 프레임 i와 다음 프레임 (i+1)%n 사이 같은 (x,y)를 256좌표×RGB 3채널로 대조: **18개 전환행×256=4,608 좌표 비교**, **13,824 채널 비교**. 변경 픽셀(어떤 RGB 채널이라도 불일치), RGB MAE, 각 프레임 픽셀 SHA-256 전부 `ANIMATION_FRAME_TRANSITIONS.csv`에 기록.

- 진홍빛 자루와 뒤틀린 자루는 프레임마다 **변경 픽셀 수 [33,42,33,38,42]**; 대응 전환 **5/5**에서 변경 **좌표 마스크가 완전히 같다**. 색상값 자체는 서로 다르다.
- 일반 모닥불 장작/영혼 모닥불 장작은 **[63,65,51,62]**; 대응 전환 **4/4**에서 변경 좌표 마스크가 완전히 같다. 소스에서 같은 움직임 배치로 다른 색조를 구현한 증거다.
- 쌍별 프레임 변화 마스크 불일치 좌표 **0개 (5+4=9회, 총 2,304개 위치 비교)**. `MATCHED_FRAME_CHANGE_MASKS.csv`에 각각 기록. 이 수치는 새 원본 프레임/텍셀 개수가 아니다.

## 4. 정적 모델 JSON·블록상태와 실제 사용 슬롯 연결

- `models/block/crimson_stem.json`, `warped_stem.json`은 `cube_column` 부모를 상속하고 **`#side`에 해당 애니메이션 PNG**를 지정; `#end`는 별도 `*_stem_top`. 각각 `axis=x/y/z` 3종 blockstate 변형이 이 모델을 참조.
- `blockstates/campfire.json`, `soul_campfire.json`은 **`lit=true` 4방향에 켜진 모델**, `lit=false` 4방향에 꺼진 모델을 지정한다. `models/block/campfire.json`과 `soul_campfire.json`은 공유 `template_campfire`의 **`#lit_log` 9면**에 애니메이션 장작 PNG를 연결. **`#fire` 4면은 별도 불 애니메이션 텍스처**이며 이번 장작 4종과 혼동하지 않았다.
- 위 연결은 원본 모델/블록상태 JSON 직접 열람에 근거. 인게임 재생, 베이크된 최종 UV, 발광량, 실제 시간 샘플링은 주장하지 않는다.

## 연구 진척·경계

- **기존 18 기본 + D1 보조 단면 3 = 21개의 정적 표본**과 **이번 추가 애니메이션 PNG 4개**를 서로 분리하여 관리. 앞서 분석된 4,608 기본 원본 픽셀/768 D1 단면 픽셀/기존 RGB·UV 실적 재가산 없음.
- `crimson_stem`은 `crimson_planks`와 이름/재질 계열만 연관되며, **기존 21 PNG의 구성원이 아님**. 모닥불과 영혼 모닥불 역시 별도의 보조 연구 대상.
- `block/`의 99 `.png.mcmeta` 중 나머지 항목 전체·다른 재질 단계의 애니메이션은 이번에 연구 완료로 선언하지 않는다.
- 사용자 지시대로 인게임 정적·동적 관찰 및 공식 Mojang JAR 인증은 완료 조건에서 제외. 소스 메타데이터/프레임 분석만 인증한다.
- 범위 내 애니메이션 신규 분석 완료. 더 넓은 애니메이션 분류 연구를 하려면 **다음 단계**에서 별도 범위/상태를 새로 확인; 현재 stage 1-1-01 외 STATE/HANDOFF 및 전역 v38 수정 금지. 사용자가 `계속해줘`만 반복하더라도 새로운 소스 근거 없이 무의미한 버전 증가 금지.

## 산출물

`ANIMATION_SOURCE_LEDGER.csv` · `ANIMATION_FRAME_TRANSITIONS.csv` · `MATCHED_FRAME_CHANGE_MASKS.csv` · `ANIMATION_MODEL_LINKS.csv` · `STATIC_21_ANIMATION_AUDIT.csv` · `REPRODUCE_ANIMATION.py` · `SUMMARY.json`.
