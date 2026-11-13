# TEX04-R002 — 공식 Mojang 1.21.11 JAR 검증 게이트 (미완료)

## 실제 접근 상태 (2026-11-13)

- `https://piston-meta.mojang.com/mc/game/version_manifest_v2.json` 및 버전 JSON 원본 도메인은 이 채팅의 네트워크 환경에서 열람/다운로드 실패.
- 공식 JAR 후보 주소: `https://piston-data.mojang.com/v1/objects/ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd/client.jar` (제3자 다운로드 목록에서 식별; **공식 주소로부터 파일 자체는 받지 못함**).
- JAR 후보 SHA1: `ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd` (제3자 `Minecraft 1.21.11` 다운로드 인덱스 2개에서 일치하는 값; Mojang 실시간 메타데이터 직접 인증 아님).
- 별도 제3자 파일: `PrismLauncher/meta-upstream/mojang/version_manifest_v2.json`의 2026-11-10 갱신 항목 `1.21.11`은 `sha1=812ee7fdfdf648bb872f7a1dca33718de4e786b4`라는 **버전 메타데이터 JSON 지문**을 가리킴. 오래된 웹 캐시(2026-10-13)는 `718cd84b4912691fe5de829aab6876a4b7f6c5c4`로 다르게 보였음. **이 둘은 클라이언트 JAR SHA1이 아니며, 둘 중 하나를 JAR SHA로 사용하면 안 된다.** 공식 서비스로부터 직접 재확인이 필요하다.

## F를 Verified로 올리는 필수 조건

1. Mojang에서 직접 받은 **버전 매니페스트 + 해당 1.21.11 버전 JSON**의 `sha1`을 교차 검사하고 출처를 기록한다. 클라이언트 JAR URL·`downloads.client.sha1`·`size`도 원본 메타데이터에서 확보.
2. 실제 `client.jar` 바이너리 전체 바이트의 SHA1과 크기를 `downloads.client`와 대조한다.
3. 일치한 그 JAR에서 정확한 9개 `assets/minecraft/textures/block/{color}_wool.png`를 읽어 SHA-256을 R001/R002의 9개 원본 SHA와 대조. 차이가 있으면 그대로 보류하고 어떤 파일이 다른지 기록.
4. JAR에 포함된 실제 모델 JSON/blockstate JSON도 독립 비교하면 E의 공식 근거까지 확대 가능.
5. 실제 게임 안에서 동일 버전·기본 리소스팩·조명 조건을 기록한 **정적** 장면을 캡처한 경우에만 `ingame_static_verified` 개별 갱신. JSON이나 렌더 시뮬레이션은 인게임 스크린샷을 대신하지 않는다.

참고 URL: https://minecraft.wiki/w/Version_manifest.json ; https://github.com/PrismLauncher/meta-upstream/blob/master/mojang/version_manifest_v2.json ; https://mcreference.com/minecraft-versions/1.21.11

## 현 상태

`official_client_jar_authenticated_count = 0`; `ingame_static_render_verified_count = 0`. **F 전체 보류**. 모션/프레임·애니메이션 연구도 계속 보류.
