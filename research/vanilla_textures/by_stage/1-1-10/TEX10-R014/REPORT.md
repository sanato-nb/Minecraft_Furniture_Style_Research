# TEX10-R014 — 원본 블록 아틀라스 디렉터리 → 스프라이트 → PNG/메타데이터 로더 연결 검증

> 2026-11-13, 사용자 추출 Minecraft 1.21.11 자원과 `.class` 직접 검사. **인게임 검증은 사용자 지시로 완료 조건에서 제외**. 공식 Mojang 전체 client.jar SHA1 인증도 제외(인증 성공 아님). 현재 단계 `1-1-10`만 변경.

## 핵심 발견 — 구성 선언과 실제 클래스 코드 연결

R004에서 확인한 **기존** `1.21.11/assets/minecraft/atlases/blocks.json`의 `{"type":"minecraft:directory","source":"block","prefix":"block/"}`를 이번 신규 원본 코드와 연결했다. R004에 이미 조사한 이 JSON을 **새 고유 파일로 재집계하지 않았다.**

- `ilw.class`는 atlas source codec에 `directory`→`ily`를 등록하고, JSON `sources` 목록을 파싱하는 codec을 구성한다.
- `ilv.class`는 `atlases/{id}.json` 파일을 리소스 관리자에서 읽어 정의를 파싱하고, 자원 팩의 여러 소스 정의를 목록으로 결합한다. 실제 팩 우선순위나 적용 후 atlas 결과는 미측정.
- `ily.class`는 `textures/`+`source`+`/` 아래 `.png` 파일을 열거한다. 따라서 이번 선언에서 **`textures/block/*.png`** 후보를 탐색한다.
- `amm.class`가 접두 경로 `textures/block/`과 확장자 `.png`를 분리하며, `ily`는 `prefix="block/"`를 붙여 원본 파일의 atlas sprite id를 만든다. 8종의 예상 id가 `minecraft:block/{id}`가 되는 것은 JSON+class source 근거로 확인.
- `ilu$c.class`의 콜백은 (sprite id, resource)를 공급자에 등록하고, `ilv$1.class`는 맵에 같은 id가 등장하면 `Map.put`으로 이전 공급자를 대체·close한다. 그러므로 폴더에 있다는 사실만으로 최종 atlas 채택·우선순위를 단정하면 안 된다.

## 원본 PNG 및 사이드카를 현재 GitHub 트리와 다시 대조

| 확인 대상 | 원본 추출본 개수 | 의미 |
|---|---:|---|
| `textures/block/*.png` | **1111** | 블록 아틀라스 directory source가 탐색할 수 있는 파일, 최종 실사용 수 아님 |
| `textures/item/*.png` | **792** | 별도 item 디렉터리 보유 원본 PNG |
| `textures/block/*.png.mcmeta` | **99** | 원본 block 텍스처 메타데이터 파일 |
| 이번 지정 8종 block PNG | **8/8** | 대상 전부 `block/` 디렉터리 조건 일치 |
| 해당 8종 중 `.png.mcmeta` 존재 | **6/8** | 잎 6종 `texture.mipmap_strategy=dark_cutout` 직접 재확인 |
| 해당 8종 중 `.png.mcmeta` 부재 | **2/8** | vine/moss: R010 AUTO 기본값 별도 적용 |

8개 `minecraft:block/{id}`에 대한 정확한 경로·sidecar/strategy 결과는 `ATLAS_DIRECTORY_MATCH_8.csv`에서 한 줄씩 확인할 수 있다. 원본 파일 SHA는 이전 R011과 이번 현재 트리 동일성 기준으로 구분한다. **새 PNG 원본 화소 계측=0**이며 R012 680 RGBA 결과를 신규 계산으로 중복 합산하지 않는다.

## 스프라이트의 메타데이터 입력 경로

- 이전 R013에서는 `ilt.class`를 SpriteOpener 인터페이스/팩토리 부분까지만 확인했다. **이번에는 같은 원본 클래스의 299바이트 정적 메서드** `a(Set,Identifier,Resource)`를 새로 디스어셈블해 실제 Resource read 부분까지 검증했다 (기존 경로이므로 신규 고유 클래스 아님).
- `bax.f()`는 리소스 메타데이터 제공자를 지연 로드·캐시한다. `bbb.a(InputStream)`은 UTF-8 JSON 객체를 읽는 경로이며, `ilt`는 `bbb.a(inj.e)`로 `texture` 섹션을 Optional 형태로 요청한다.
- `ilt`는 동일 리소스의 InputStream을 `fyh.a(InputStream)`로 PNG 디코드하고, 프레임 크기 조건을 검사한 뒤 `ilk(SpriteContents)` 생성자에 선택된 메타데이터 Optional과 이미지를 전달한다.
- `ilk`가 이 Optional에서 `mipmap_strategy`와 alpha cutoff bias를 읽어 MipmapHelper로 전달한다는 R013의 확인과 연결됐다. **6개 원본 leaf 사이드카**는 `{"texture":{"mipmap_strategy":"dark_cutout"}}`였고, vine/moss는 동일 이름의 사이드카 부재.
- `ilt` 내부에 별도 메타데이터 조회가 추가로 존재하지만, 애니메이션 분야는 사용자 지시로 연구 범위에서 제외하고 의미 판정하지 않았다.

## 아이템 아틀라스와 혼동 방지

신규 확인한 `atlases/items.json`은 **`item/` directory source**와 갑옷 장식 관련 `paletted_permutations`를 갖는다. 사용자 추출본의 `textures/item/{target}.png`라는 같은 이름의 원본은 8종 모두 없다. 이는 **해당 item 디렉터리에 같은 이름 PNG가 없다는 정적 사실**일 뿐이다. R005에서 확인된 item 모델의 `block/` 텍스처 참조나 바닐라 아이템 렌더링이 불가능하다는 뜻이 아니며, 전체 item model/atlas bake 경로를 이번에 새로 완전 검증한 것은 아니다.

## 검증 한계와 계수

- 신규 직접 조사 고유 원본 경로: **9개** (Java `.class` 8개 + `atlases/items.json` 1개). 과거 누적 153→**162개**. `atlases/blocks.json`과 `ilt.class`·잎 6종 `.mcmeta`는 과거 기록을 재확인했지만 중복 집계하지 않았다.
- 사용자 추출 원본 트리로 확정: 8개 block PNG 존재, directory source 코드와 id 변환, sidecar 6/8, ResourceMetadata Optional 전달.
- 미검증: 실제 실행 시 어떤 팩의 resource가 최종 선택되는지, atlas stitch의 실제 x/y, padding, atlas 크기, 런타임 mip 수준, 원본 JVM 실행과 R012의 완전한 RGBA 바이트 동일성. 이 중 **인게임 스크린샷은 요구하지 않는다**.
- 고유 새 텍스처 0, 신규 raw RGBA/밉맵 파생 픽셀 계측 0, 애니메이션·PZ변환·가구 제작 보류. 전역 `v38`·타 연구단계·기존 R001~R013 수정하지 않음.

## 결과

`ATLAS_DIRECTORY_MATCH_8.csv`, `ARCHIVE_ATLAS_INVENTORY.json`, `ATLAS_RESOURCE_LOADER_TRACE.json`, `SOURCE_LEDGER.csv`, `SUMMARY.json`, 본 보고서. 본 단계 `STATE.json`과 `HANDOFF.md`를 함께 갱신.
