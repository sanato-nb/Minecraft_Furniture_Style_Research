# INT-4 H25 — 신규 가구 모드 Adorn 7.6.1 공식 JAR·원본 21개 상태 모델/UV 연구

## 1. 확정 범위와 직계 출처

기존 [H24 Draft PR #106](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/106)의 head SHA a6e7b82399c2d412d155f8f29db94c177e01e1b9에서 분기한다. H23 모델링 전용 F70 V5 70/70은 이미 종료된 기존 심사 분모이므로 **신규 Adorn 사례를 해당 70건에 몰래 추가하거나 F70 최종 승인을 승격하지 않는다.**

이번 연구 모드: [Juuxel/Adorn](https://github.com/Juuxel/Adorn), 공식 소스 [태그 7.6.1](https://github.com/Juuxel/Adorn/tree/7.6.1), commit 6bfee0ee1ec2c259a577c5cde0b038641874fb2c. 공식 Fabric 배포 [릴리스 7.6.1](https://github.com/Juuxel/Adorn/releases/tag/7.6.1)의 Adorn-7.6.1+1.21.11-fabric.jar. 배포 JAR SHA-256 **d431be4ee89d0d71b1ababedaa5275f478cfff5de94eba1165f5cd10d1b676d3** (6,676,304바이트; ZIP 멤버 13,538개). 내장 fabric.mod.json: id=adorn, version=7.6.1+1.21.11, Minecraft 정확히 =1.21.11. 원본 ZIP CRC 통과.

공식 배포 JAR에서 모델·블록상태·애니메이션 메타데이터를 직접 읽고 소스 태그의 **정확한 10개 Git blob SHA-1**을 별도로 검증했다. 각 JSON/MCMeta 원본의 **파싱된 내용 10/10 일치**, 원시 파일 바이트는 10/10 불일치(직렬화 포맷 차이). 바이트 동일성으로 잘못 주장하지 않는다. Git의 모드 원본을 복제해 저장하지 않으며, 실제 릴리스 파일도 Git에 저장하지 않는다.

## 2. 원본 모델 5종의 직접 측정

| 원본 모델 | 요소 | 선언 면 | 명시 UV | 기본 UV (미 bake) | 모드 외부 바닐라 텍스처 참조 면 |
|---|---:|---:|---:|---:|---:|
| acacia_coffee_table | 12 | 56 | 0 | 56 | 56 |
| iron_shelf | 3 | 16 | 0 | 16 | 16 |
| brewer | 3 | 16 | 16 | 0 | 0 |
| brewer_active | 3 | 16 | 16 | 0 | 0 |
| brewer_mug | 8 | 35 | 0 | 35 | 0 |

**커피 테이블**은 모델 잎 acacia_coffee_table → templates/coffee_table → 바닐라 block/block 상속이다. 부모 원본의 12요소·56면을 사용하고 텍스처를 acacia_log 44면, acacia_planks 10면, orange_stained_glass 2면으로 바인딩한다. 바닐라 텍스처 3종은 Adorn JAR 외부이며 Mojang 원본 PNG SHA와 실제 UV bake를 이번 단계에 연결하지 않았다. 상속 원본의 bounding 범위 [0,0,0]~[16,12,16]은 모델 요소 기준으로만 기록한다. **배포 JAR에 생성된 blockstates/acacia_coffee_table.json이 있으며 단일 기본 variant만 선택**한다. 이 파일은 위 소스 태그의 일반 정적 assets/adorn/blockstates 폴더에 없었으므로 소스 미존재를 모델 부재로 오판하면 안 된다.

**철제 선반**은 iron_shelf → templates/shelf → 바닐라 block/block 상속. 3요소·16면, 그중 2요소는 원본 요소 회전이 선언되어 있다. 셀렉터는 north=270°, east=0°, south=90°, west=180°로 **4방향별 모델 회전**이다. 텍스처는 iron_block 6면, stone 10면으로 모두 바닐라 외부 출처를 사용한다. 모델의 정적 요소 from/to bounds [0,0,0]~[7,6,16]을 회전 적용 후 세계 AABB로 간주하지 않는다.

**커피 제조기(brewer)**는 blockstate multipart 12개 원본 규칙으로 동작한다. 4방향 × active 2 × has_mug 2 = **16개 정확한 상태**를 독립 선택 평가했다. inactive 기본 모델과 active 모델은 모두 3요소·16면이며 active는 brewer 원본 형상을 상속하고 front 텍스처 참조만 활성 텍스처로 바꾼다. has_mug=true이면 brewer_mug 8요소·35면이 독립 overlay로 추가되어 합계 11요소·51면(2 model applications). 방향별 y 회전은 north 0°, east 90°, south 180°, west 270°이다. 이는 원본 선택/면 개수 근거이며 실게임 장면의 GPU 렌더링 결과 확정이 아니다.

전체 조사한 **정확한 원본 블록상태 21개**: 커피 테이블 기본 1, 선반 방향 4, 제조기 활성·머그잔·방향 조합 16. 원장에서는 29회 모델 적용, 총 656면의 *상태별 중복 포함 선택 소스 면 기록*을 집계한다. 그중 **명시 UV 256면 / 암묵 기본 UV 400면**, 바닐라 외부 참조 120면이다. 이 656면은 서로 다른 고유 모델의 면을 656개 새로 발견했다는 뜻이 아니다.

## 3. 활성 텍스처 애니메이션의 정확한 원본

공식 JAR의 brewer_front_active.png 크기 **16×96**, 원본 16×16 프레임 6장 구조. 별도의 brewer_front_active.png.mcmeta를 7.6.1 태그 Git blob **2197c0e9c49f74854bed7c290e5ad1e8911ea30d**와 공식 릴리스 JSON으로 대조했으며 애니메이션 출처를 아래와 같이 확인했다.

- 서로 다른 프레임 인덱스 0~5, 시간순 원본 지정 **[0,1,2,3,4,5,5,4,3,2,1,0]**, 총 12단계 왕복 시퀀스
- 원본 메타데이터: **frametime=5 tick**, **interpolate=true**
- 원본 릴리스 메타데이터 SHA-256 **9bcf6603fc15f88817aa0b85940a16885a3736e57584bde73335bec6f4a418ea**
- 배포 PNG SHA-256 **c779804917d17b97a140a8ac2057fec4bd84432d7008cddec5035e69f725e0d6**
- 실제 특정 시점 F2가 몇 번 프레임을 보여 주는지, GPU 보간 결과의 개별 픽셀 인과는 **미검증**.

선택 모델의 모드 내부 PNG **7종**은 JAR 원본 byte SHA-256 및 크기 확인. 바닐라 minecraft:block/ 참조 **5종**은 별도 Mojang 리소스 검증 대상으로 분리했다.

## 4. 재현 검증 및 GitHub 산출물

- 공식 JAR 다운로드 및 태그 신원 사전 검증: [Actions #45354894734](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45354894734) 성공.
- 실제 공식 JAR·원본 9개 JSON 대조, 최초 21 상태/5 모델 독립 실행: [Actions #45355380656](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45355380656) 성공.
- 최종 애니메이션 .mcmeta까지 10개 source blob으로 확장하고 영구 JSON·CSV를 재생성, 독립 회귀시험으로 일치 검증한다. 최종 Actions URL은 PR 검증 기록에 추가한다.
- 원본 출처 감사 코드: src/mcfr/int4_h25_adorn_release_source.py.
- 원본 21개 상태의 검색 가능한 표: project/integration/INT4_H25_ADORN_761_STATE_SELECTOR_CASES_V1.csv.
- 실제 공식 JAR 기반 구조·상속·텍스처 SHA·애니메이션 메타데이터 결과: project/integration/INT4_H25_ADORN_761_SELECTED_MODEL_SOURCE_V1.json.
- 11개 부정대조/회귀시험: tests/knowledge/test_int4_h25_adorn_release_source.py.
- GitHub Actions: .github/workflows/integration-int4-h25-adorn-source.yml 및 preflight workflow.

## 5. 재사용 규칙, 한계와 다음 작업

새 모드 Adorn에 대해서는 **공식 원본만으로 재현 가능한 기하·블록상태 선택·명시 UV·텍스처 경로·애니메이션 메타데이터**까지 조사한다. 이름이 같은 다른 모드의 커피 테이블, 선반, 주방 도구와 3D 모델 상태가 같다고 자동 매칭하지 않는다.

범위 외 항목: Mojang 공식 텍스처의 개별 바이트 연결, 암묵 UV의 실제 bake, 렌더러 GPU 면↔픽셀 인과, 실제 게임 F2, 원본 모델을 AI 학습/재배포할 권리와 전체 Adorn 모델 전수 조사. 신규 게임 실행 **0**, 신규 F2 **0**. 모드 소스 저장소 MIT 표시만으로 각 원본 아트의 독립 학습·배포 권리까지 자동 승인하지 않는다.

**H25의 종료 판정은 신규 5모델·21원본 선택 상태의 source-level 감사 통과이지 실게임·렌더링 전체 완료가 아니다.** 기존 엄격 F70 무조건 0/70, H03 HOLD, H05 CONDITIONAL, INT5 0, INT6 0 유지. 별도 F70 모델링 범위 H23 70/70도 유지. H26에서 바닐라 외부 자산·암묵 UV를 공식 Mojang bake와 연결하거나 원본 Adorn 실게임 F2를 최소 촬영하고, 이후 Adorn의 새로운 가구 종류로 확대한다.
