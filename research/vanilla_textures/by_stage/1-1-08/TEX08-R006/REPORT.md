# TEX08-R006 — 조각된 책장 6개 슬롯별 정적 PNG 실제 RGBA 차이 및 256개 상태 조건 전수 검증

**2026-11-13 · 1-1-08 복합·기능면 · 고정 21 PNG 유지 · 이전 TEX08-R005 계승 · 전체 v38 변경 금지**

## 1. 사용자 제공 원본에 대한 실제 재검증

1차 자료는 사용자가 압축 해제해 GitHub에 제공한 `1.21.11/assets/minecraft/`다. `chiseled_bookshelf_empty.png`와 `chiseled_bookshelf_occupied.png`를 실제 바이너리로 받아 16×16 RGBA로 디코딩하고 SHA-256, Git blob SHA-1, PNG 전 청크(IHDR/PLTE/IDAT/IEND) CRC32를 확인했다. **2개 모두 검사 통과**. 투명/반투명 픽셀은 양쪽 모두 0개, 각 256개가 완전 불투명하다.

- empty 187바이트, SHA-256 `a756e5f993f698a566b73b24c0610b9832781d4a5f20358f38442b77d028841d`, RGBA 고유 색 11가지, Git blob `29d77a11027de067bcd2d3f9b7d6d0716c6ec612`.
- occupied 357바이트, SHA-256 `a314c81a2dd8c3f14bec2428a0252322e6b37e95810d56316ac23c938540fb4e`, RGBA 고유 색 40가지, Git blob `cc9ef27b4ff5f252ae0b38e46454aeee30067981`.
- 서로 다른 원본 RGBA 픽셀 좌표는 **156 / 256 = 60.9375%**. alpha 값 차이 0. 변경 범위 x=1..14/y=1..14 (양끝 포함); y=0..15별 변경 수는 `0|8|14|14|14|14|14|0|0|8|14|14|14|14|14|0`.

이 2개 PNG는 기존 21개 표본에 이미 속하고 R001에서 개별 측정한 파일들이다. **신규 고유 PNG 0개, 새 고유 원본 픽셀 0개**. R006의 새 근거는 두 파일 사이의 **256개 짝지은 좌표 비교 및 156개 변경 지점의 슬롯별 분배**다.

## 2. 사용자 추출본 슬롯 JSON 6개의 UV 재확인

6개 `models/block/template_chiseled_bookshelf_slot_*.json`을 다시 직접 열어 각 `faces.north.uv`, `elements.from/to`, `textures.particle="#texture"` 선언을 확인했다. 각 평면은 **z=0의 zero-depth north 단일 면**. R004의 위치 x와 UV x 역방향 배열 발견은 그대로 유지하며 실제 게임 화면의 좌우 방향 인증과 혼동하지 않는다.

| 슬롯 | UV `[x0,y0,x1,y1]` | 면적 | 두 PNG 사이 RGBA 변경 | 변경 비율 |
|---|---|---:|---:|---:|
| top_left | [0,0,6,8] | 48 | 25 | 52.0833% |
| top_mid | [6,0,11,8] | 40 | 29 | 72.5% |
| top_right | [11,0,16,8] | 40 | 24 | 60% |
| bottom_left | [0,8,6,16] | 48 | 29 | 60.4167% |
| bottom_mid | [6,8,11,16] | 40 | 25 | 62.5% |
| bottom_right | [11,8,16,16] | 40 | 24 | 60% |
| **합계** | **16×16 전체, UV 겹침 0** | **256** | **156** | **60.9375%** |

각 슬롯의 알파 변경 픽셀 0. UV 6개의 교집합은 비어 있고 합집합은 정확히 **256개 좌표**, 모든 픽셀 변화 지점도 이 6영역 중 하나에 포함됨. `SLOT_RGBA_AUDIT.csv`에서 각 템플릿의 Git blob SHA도 보존했다.

## 3. 정적 PNG UV에서 직접 구성한 64가지 아틀라스

각 슬롯마다 empty 또는 occupied 원본 PNG의 동일 UV 직사각형을 선택해 16×16 2D 소스 아틀라스를 구성했다. **64개(2^6) RGBA raw-buffer SHA-256 결과 모두 서로 다름(64/64)**. `ATLAS_64_COMBINATIONS.csv`의 **64행**은 6비트 점유 마스크, empty와 비교한 변경 픽셀 수, **RGBA raw buffer** SHA를 저장한다. 해시가 원본 압축 PNG의 SHA가 아니라는 점에 유의한다. source atlas all-empty/all-occupied는 원본 empty/occupied RGBA와 바이트 배열이 동일하다.

이 아틀라스는 **소스 픽셀 영역의 선택 결과**로, 실제 마인크래프트 월드 조명/블록 UV 감김/회전/particle을 반영한 인게임 스크린샷이 아니다. 4개 방향 모두 64개 2D 조합을 재사용하므로 **256개 실제 게임 화면의 시각적 고유성을 보증하지 않는다**.

## 4. 원본 multipart 상태 256개 전수 규칙 평가

사용자 제공 `blockstates/chiseled_bookshelf.json` (Git blob `0c9b22b91093c4dfe3510a9a6aebe291df491e39`)의 **52개 multipart 규칙**을 실제 조건 평가: 4가지 `facing` (north/east/south/west) × 64가지 슬롯 점유 마스크 = **256개 소스 상태 조합**. **256/256 모두** 정확히 본체 1개 + 점유에 맞는 empty/occupied 슬롯 모델 6개, 총 7개 모델이 선택되며 누락, 중복, yaw 불일치가 없었다. 기본 본체 규칙은 `uvlock=true`, 슬롯 규칙은 `uvlock`을 **선언하지 않는다**(false를 직접 기입한 것으로 부르지 않음).

R002에서 이미 기록된 **256개 이론적 조합**을 새 상태 수로 가산하지 않으며, R006의 새 성과는 그 **256개를 실제 원본 JSON에 대입하여 7개 선택을 전수 확인한 것**이다. `BLOCKSTATE_256_SELECTIONS.csv`의 256행에 각 방향, 비트, 7 모델, yaw, uvlock을 보존.

## 5. 계승 근거와 검증 한계
- 계승: 21 PNG / 5,376 과거 고유 원본 픽셀, R004 **39 leaf 모델+8 부모·143 model face rows**, R005 **62개 정적 상태쌍 비교**, chiseled 슬롯 particle 선언 정정. **이번 256 RGBA 비교 / 64 소스 아틀라스 / 256 조건 평가를 이전 누적 수치에 합산하지 않음.**
- 새 SHA·CRC 검증 PNG는 **기존 대상 2개를 다시 검사한 것**이고 신규 PNG 획득이 아님.
- 실제 인게임 정적 렌더 확인 **0/21**, 최종 멀티파트 particle 선택·UV winding·실제 화면 방향 미검증. 공식 전체 Mojang client.jar SHA-1/manifest는 사용자 지시로 연구 필수·완료 분모에서 **제외**(인증 완료 아님).
- 애니메이션 연구 0, 가구 3D 제작·PZ 변환 0, 다른 단계·루트·전역 v38 미수정.
- 재현: `VERIFY_STATIC_SLOTS.py`가 기존 사용자 제공 `1.21.11/` 소스만으로 PNG CRC/SHA, 6 UV 영역, 64 해시 고유성, 256 규칙 선택을 검사한다.

**R006 결과 파일:** `REPORT.md`, `SUMMARY.json`, `SLOT_RGBA_AUDIT.csv`(6행), `ATLAS_64_COMBINATIONS.csv`(64행), `BLOCKSTATE_256_SELECTIONS.csv`(256행), `SOURCE_LEDGER.csv`(9행), `VERIFY_STATIC_SLOTS.py`. 다음 실제 새 근거는 라이브 상태에서 `TEX08-R007` 확인 후 저장.
