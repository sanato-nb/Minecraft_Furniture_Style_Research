# 1-4-E 후속 검증 — 텍스처의 실제 참조 경로와 연구 DB

2026-11-19 KST. 기존 E의 누락 텍스처 8개·대체 후보 16개를 Minecraft Java 1.21.1과 Another Furniture Fabric 4.0.2에서 확인했다. 모드 JAR은 고정 SHA-1로 확인했다. 그래픽 클라이언트의 초기 리소스 로드가 끝난 뒤 블록 아틀라스와 실제 베이크된 모델의 면·파티클 스프라이트를 읽었다. 클라이언트를 다시 실행한 결과 217개 관측 행이 바이트 단위로 일치했다.

| 대상 | 확인 결과 |
|---|---|
| 원래 경로 미확정 8개 | 고정 Fabric JAR의 정확한 PNG 경로가 모두 없고, 아틀라스에서 해당 ID를 조회하면 **8/8개가 `minecraft:missingno`**로 해석된다. 원본 PNG 누락 결함으로 확정했다. |
| 참나무 의자 대체 후보 13개 | `back_1/oak`~`back_11/oak`, `bottom/oak`, `seat/oak`를 실제 의자 면에서 확인했다. 등록된 의자 상태 **176개**의 면 텍스처가 고정 블록 상태 선택 조건 **88개**의 모델·슬롯과 모두 일치했다. |
| 식탁보·묘비 대체 후보 3개 | 각 PNG의 해시와 아틀라스 적재를 확인했다. 고정 모드 모델에는 이 `unused/` 경로를 쓰는 슬롯이 없었다. 기존 경로에 대한 자동 대체도 없었다. |
| 선행 연구 DB | 선언 전용 77개와 기존 면 연결 3,937행을 보존했다. 기존 UV 영면적 176행을 C 보완 원장에 연결해 **선 172행·점 4행**의 원본 화소 근거를 추가했다. |

## 실제 영향

구버전 참조가 붙은 모델의 면 **139개**가 기존 원장에 있다. 이 모델들을 직접 선택하는 고정 블록 상태는 0건이다. 묘비 아이템 모델 파일은 존재하지만, 조사한 게임의 `another_furniture:stone_tombstone` 블록·아이템 ID는 등록되지 않았다. 아틀라스 조회에서 확인한 `missingno`는 해당 ID에 대한 폴백이며 139개 면이 전부 실제 게임에서 그려진다는 뜻은 아니다.

서비스 벨의 구형 템플릿 파티클 `another_furniture:block/iron_block`도 누락이다. 등록된 서비스 벨 블록의 4개 상태는 파티클에 `another_furniture:block/service_bell`을 사용한다. 아이템은 파티클에 바닐라 `minecraft:block/iron_block`을 쓰고, 면은 서비스 벨 PNG를 사용한다.

참나무 의자의 PNG는 같은 템플릿에서 자식 모델이 실제 변형별 경로를 지정하므로, 등받이 11개를 구형 `oak_back` 하나에 대한 일괄 치환으로 처리할 수 없다. 고정 DB에 대체 후보에서 실제 모델·슬롯으로 이어지는 연결 92행을 기록했다.

## 연구 DB와 범위

[갱신 SQLite 압축본](research_texture_uv_runtime.sqlite.xz)에는 기존 E DB의 테이블과 이번 누락·후보·참조·실행 기록 및 영면적 보완 링크가 들어 있다. SQLite 무결성·외래키 검사를 통과했다. 리소스팩은 설치된 고정 모드의 기본 설정으로 확인했다. NeoForge 4.0.3의 PNG 경로 대조는 선행 C 근거를 따르며, 이번 클라이언트 엔진 실측은 Fabric 4.0.2에 한정한다. 셰이더 적용 화면과 외부 리소스팩의 경로 재정의는 별도 범위다.

[누락 경로 결과](MISSING_SPRITE_RUNTIME.csv) · [후보별 사용 증거](ALTERNATE_SPRITE_RUNTIME.csv) · [모델·슬롯 연결](ALTERNATE_SPRITE_MODEL_BINDING.csv) · [의자 상태별 대조](OAK_CHAIR_RUNTIME_BINDING.csv) · [엔진 원시 기록](ATLAS_RUNTIME.tsv) · [집계](SUMMARY.json)

## 재현

Linux에서 Java 21과 Xvfb를 사용한다. 테스트 클라이언트는 연구용 캐시·프로필에서 실행한다.

```sh
entry=research/furniture_mods/phase_1-4/E_followup
python "$entry/run_atlas_probe.py" --work /tmp/af-atlas --output /tmp/af-runtime.tsv
python "$entry/audit_references.py" --atlas /tmp/af-runtime.tsv \
  --fabric /tmp/af-atlas/1.21.1/probe_game/mods/another_furniture-fabric-4.0.2.jar \
  --out /tmp/af-atlas-result
```
