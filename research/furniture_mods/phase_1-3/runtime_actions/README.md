# 1-3-D GitHub Actions 엔진 감사

워크플로 `1-3-D engine state and collision audit`는 공식 Minecraft Java 클라이언트 1.21.1과 1.21.11에 해당 가구 모드를 설치하고 가상 화면에서 실행한다. 플러그인이 실제 블록 레지스트리와 모든 등록 상태를 읽고, Minecraft 엔진이 빈 이웃·기본 충돌 문맥에 반환한 상자 좌표를 저장한다. 같은 상태를 연구 원장의 variants/multipart 조건에도 대입한다.

| 검증 | 의미 |
|---|---|
| 등록 상태 | 게임의 블록 레지스트리가 정의한 상태 조합 |
| 규칙 일치 | 등록 상태를 1-3-D 소스의 variant/multipart 조건에 대입한 결과 |
| 충돌 상자 | 빈 이웃과 기본 충돌 주체 문맥을 사용한 엔진의 실제 충돌 AABB |
| 미등록 원본 | 연구 원장에는 있지만 게임 레지스트리에 없는 블록 상태 리소스 |

상태별 배치 가능 여부, 주변 블록 변경에 따른 전이, 플레이어·엔티티별 충돌과 실제 렌더 모델 선택은 별도다. 실제 월드에서 실행한 대표 조립·낙하 검증은 [선행 실측 보고서](../followup/REPORT.md)에 있다.

모드와 버전은 선행 실측과 동일하다. Another Furniture는 1.21.1 Fabric 4.0.2이며 고정 원본과 상태·모델 JSON 내용이 모두 일치한다. Handcrafted는 1.21.1 Fabric 4.0.3이며 해당 파일이 고정 원본과 바이트 단위로 일치한다. Macaw는 1.21.11 Fabric 3.4.2 고정 JAR이다. 공식 클라이언트와 모드 파일은 고정 SHA-1을 검산한다.

Actions의 각 버전 작업에서 `SUMMARY.json`, `ENGINE_STATES.tsv.gz`, `ENGINE_RULE_EXCEPTIONS.csv` 및 `engine.log`를 내려받을 수 있다. 좌표는 블록을 원점으로 하는 블록 단위이고 순서는 minX, minY, minZ, maxX, maxY, maxZ다. 결과는 공기와 돌 대조군으로 확인한다.

Java 21과 Xvfb가 있는 Linux에서 자체 실행할 수 있다.

```sh
python3 research/furniture_mods/phase_1-3/runtime_actions/run_probe.py \
    --version 1.21.1 --work /tmp/mc-audit --output /tmp/mc-audit-results
```
