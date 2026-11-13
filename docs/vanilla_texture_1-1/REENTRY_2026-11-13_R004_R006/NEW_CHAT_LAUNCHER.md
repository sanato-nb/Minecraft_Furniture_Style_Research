# 새 채팅용 11개 재질별 연구 재개 허브

> 2026-11-13 GitHub 독립 단계 상태 기준 **인수인계 스냅샷**. 아래의 버전은 이 문서를 작성할 때의 상태이며, **새 채팅에서는 반드시 라이브 `STATE.json`을 다시 확인**해 더 최근 버전이 존재하면 그 버전부터 이어간다.

- 이전 전체 프로젝트 통합 기준: `v38` (독립 재질 연구 버전과 별개).
- 사용자 제공 게임 자료: `1.21.11/`은 사용자가 직접 설치한 Minecraft Java Edition 1.21.11 JAR을 압축 해제해 저장소에 올린 것. **사용자 제공 추출본 1차, 이전 비공식 추출 미러는 교차용**.
- **공식 Mojang JAR 전체 SHA-1 인증은 사용자의 최신 지시로 현재 필수 연구 및 완료 조건에서 제외**. 제외를 '공식 인증 완료'로 기록하지 않으며, 과거 숫자·과거 보고서를 수정하지 않는다.
- 실제 **인게임 정적 시각 검증은 전 단계 현재 0건**. 게임 실행 화면 등 실제 근거 없으면 0 유지.
- **애니메이션·키프레임·움직임 연구 계속 보류**, Project Zomboid 변환 및 실제 가구 3D 제작은 범위 제외.
- 이전 R001~Rxxx 릴리스·기존 채팅별 수치 유지. 단순 재진입 프롬프트/스냅샷을 만들었다는 이유로 단계 버전을 증가시키지 않는다.

## 새 채팅에서 사용하는 방법

1. 아래 표에서 원하는 **시작 프롬프트**를 열어 **내용 전체를 복사한 뒤 새 채팅의 첫 메시지로 보낸다.**
2. 새 채팅은 **그 단계의 GitHub 라이브 `STATE.json`과 `HANDOFF.md`**, 최신 릴리스 보고서를 직접 읽은 다음 실제 분석을 수행한다.
3. 완료 후 **오직 해당 단계**의 결과 폴더 및 라이브 `HANDOFF.md`, `STATE.json`만 갱신한다. 다른 단계·루트 `HANDOFF.md/PROGRESS.md/handoff/STATE.json`은 수정 금지. 저장 충돌 시 최신 HEAD를 다시 읽고 재시도.

## 11개 독립 시작 링크

| 단계 | 재질 | 대상 | 스냅샷 당시 버전 | 다음 예정 | 새 채팅 프롬프트 | 이관 스냅샷 | 라이브 상태 |
|---|---|---:|---|---|---|---|---|
| `1-1-01` | 목재·원목 | 18 | `TEX01-R004` | `TEX01-R005` | [시작 프롬프트](1-1-01/START_PROMPT.md) | [인수인계](1-1-01/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-01/STATE.json) |
| `1-1-02` | 석재·벽돌 | 17 | `TEX02-R005` | `TEX02-R006` | [시작 프롬프트](1-1-02/START_PROMPT.md) | [인수인계](1-1-02/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-02/STATE.json) |
| `1-1-03` | 금속·금속부품 | 16 | `TEX03-R004` | `TEX03-R005` | [시작 프롬프트](1-1-03/START_PROMPT.md) | [인수인계](1-1-03/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-03/STATE.json) |
| `1-1-04` | 직물·양털 | 9 | `TEX04-R004` | `TEX04-R005` | [시작 프롬프트](1-1-04/START_PROMPT.md) | [인수인계](1-1-04/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-04/STATE.json) |
| `1-1-05` | 유리 | 6 | `TEX05-R004` | `TEX05-R005` | [시작 프롬프트](1-1-05/START_PROMPT.md) | [인수인계](1-1-05/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-05/STATE.json) |
| `1-1-06` | 도기·유광도기 | 8 | `TEX06-R004` | `TEX06-R005` | [시작 프롬프트](1-1-06/START_PROMPT.md) | [인수인계](1-1-06/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-06/STATE.json) |
| `1-1-07` | 콘크리트·색면 | 7 | `TEX07-R005` | `TEX07-R006` | [시작 프롬프트](1-1-07/START_PROMPT.md) | [인수인계](1-1-07/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-07/STATE.json) |
| `1-1-08` | 복합·기능면 | 21 | `TEX08-R004` | `TEX08-R005` | [시작 프롬프트](1-1-08/START_PROMPT.md) | [인수인계](1-1-08/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-08/STATE.json) |
| `1-1-09` | 토양·지면 | 9 | `TEX09-R004` | `TEX09-R005` | [시작 프롬프트](1-1-09/START_PROMPT.md) | [인수인계](1-1-09/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-09/STATE.json) |
| `1-1-10` | 잎·식생 | 8 | `TEX10-R004` | `TEX10-R005` | [시작 프롬프트](1-1-10/START_PROMPT.md) | [인수인계](1-1-10/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-10/STATE.json) |
| `1-1-11` | 목재·구조부품 | 31 | `TEX11-R006` | `TEX11-R007` | [시작 프롬프트](1-1-11/START_PROMPT.md) | [인수인계](1-1-11/HANDOFF_SNAPSHOT.md) | [STATE](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/docs/vanilla_texture_1-1/stages/1-1-11/STATE.json) |

## 저장 경계·재사용 주의

이 문서는 새 연구 실측을 하지 않고 **11개 채팅의 접근·인수인계만 재정리**한 것이다. 단계의 `Rxxx` 번호 또는 전체 `v38`을 증가시키지 않는다. 스냅샷 숫자는 작성 당시의 상태일 뿐 최신 STATE를 대신할 수 없다. 각 연구 채팅은 자기 단계 폴더만 갱신해야 하며, 동일 단계 복수 채팅의 동시 쓰기를 피해야 한다.

**이관 기준 JSON:** [SNAPSHOT_MANIFEST.json](SNAPSHOT_MANIFEST.json). **버전 정책:** [ISOLATED_CHAT_VERSIONING.md](../ISOLATED_CHAT_VERSIONING.md).
