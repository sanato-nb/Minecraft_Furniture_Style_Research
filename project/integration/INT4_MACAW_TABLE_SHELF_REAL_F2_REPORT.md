# INT-4 — Macaw 연결형 테이블·책장 네 상태의 실제 Minecraft F2 검증

## 앞선 원본 연구 근거

선행 [PR #41](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/41)은 1-5 연구의 테이블·책장·침대·주방 15사례·19모델 적용 및 431면 원본 PNG 참조를 확인했고, [PR #42](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/42)는 Macaw 주방 S41·S42·S43의 실제 Minecraft 1.21.11 F2 사진 3장을 검증했다.

이번에는 **같은 고정 Macaw 3.4.2 Fabric 1.21.11 런타임에서 테이블·책장 연결형 모델의 블록상태를 명시적으로 배치**하여, 원본 모델 선택이 서버에 유지되고 게임 클라이언트 F2에 나타나는지 검증한다.

## 고정된 출처 사례

| 사례 | 원본 블록 ID 및 명시적 상태 | 원본 면 수 | 출처 제공자 |
|---|---|---:|---|
| S18 | `mcwfurnitures:oak_table[east=false,north=false,south=false,west=false]` | 31 | `table_single` |
| S19 | `mcwfurnitures:oak_table[east=true,north=true,south=true,west=true]` | 6 | `table_center` |
| S28 | `mcwfurnitures:oak_bookshelf[connection=base,facing=north]` | 31 | `bookshelf_base` |
| S29 | `mcwfurnitures:oak_bookshelf[connection=middle,facing=north]` | 19 | `bookshelf_middle` |

모두 역사 `research/furniture_mods/phase_1-5/B/APPLICATIONS.csv`의 고정 원본 블록상태·선택자 index·모델 및 제공자 SHA·요소/면 수를 직접 검수한다.

## 실제 CI 검증 계약

- 원본 JAR SHA256: `e55d7a78b878043af82875cb8738941b0bba1a3c77652dea3d75a434dbba1a0e`. 실제 실행 mods/의 JAR 파일을 확인한 다음 JSON 원본 4사례를 SHA로 검증.
- 공식 Mojang 서버에서 임시 1.21.11 평지 월드를 생성. 원본 연구용 월드/기존 F2·PNG/모드 바이너리는 절대 덮어쓰지 않음.
- 가구 네 상태를 x=-32,-16,8,24, y=120, z=40에 16블록 간격으로 **개별 `/setblock` 배치**. `/execute if block`로 서버 블록 상태 네 건 전부 유지되는지 확인.
- 실제 Fabric 클라이언트가 4개 가구의 F2 이미지 각각 1024×684로 저장했는지 PNG 완전성 및 SHA 확인. 중앙 전경 색상 프록시가 150픽셀보다 작으면 화면이 하늘만 나왔을 수 있으므로 잠깐 다시 촬영(최대 3회)하고 끝내 나타나지 않으면 실패 처리.
- 네 이미지 접촉시트와 로그, 해시·원본 연결 메타데이터를 **만료되는 GitHub Actions 아티팩트**에만 보존. 이미지나 원본 JAR은 Git에 커밋하지 않음.
- 이전 Macaw 주방·의자 검증용 명령은 무수정. 런처에 새 `macaw-table-shelf-capture` 명령만 추가.

## 반드시 분리할 주장

**실제 네 상태가 F2로 촬영되는 사실**과 **연결형 가구가 주변 블록에 따라 자연히 연결되는 동작**은 다른 문제다. 이번 실험은 고정된 원본 상태를 명령으로 명시적으로 지정한다. 재료·부품 역할, 연결 감지 구현, 플레이어 상호작용, 실제 렌더된 텍스처 면별 UV·색상, 라이선스/AI 학습권한은 승인하지 않는다.

기존 정적 부품 역할 후보 45개는 이번 실험에서 의미 승인으로 승격하지 않으며, INT-4 전체·INT-5 전체 종료로 주장하지 않는다.

## 재현 명령

```bash
export PYTHONPATH=src
python -m mcfr.chair_runtime_fixture world --version 1.21.11 \
  --path /tmp/int4-table-shelf-world --cache /tmp/int4-table-shelf-cache
xvfb-run -a -s '-screen 0 1024x684x24' \
  python -m mcfr.runtime macaw-table-shelf-capture \
    --version 1.21.11 --world /tmp/int4-table-shelf-world \
    --work /tmp/int4-table-shelf-client --output /tmp/int4-table-shelf-f2
python -m mcfr.int4_macaw_table_shelf_capture --directory /tmp/int4-table-shelf-f2
```

CI 완료 전 실제 성공/문제 여부는 별도 결과로 남긴다.

## 실제 Fabric CI·원본 F2 시각 관찰 (성공)

[실제 Minecraft 1.21.11 실행 #44923726837](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44923726837)의 첫 시도는 **카메라 teleport 대기 시간 초과**로 중단됐다. 기존 전체 CI와 병렬로 실행되던 해당 작업만 **단독 재실행(두 번째 시도)**했고, 그 결과 **4/4 서버 상태·4/4 네이티브 F2** 및 원본 JAR·모델·부모 SHA 검증이 모두 성공했다. 첫 실패를 삭제하거나 가구 모델 오류라고 판정하지 않았다.

| 원본 상태 | F2 증거 | 전경 채도화소 | 화면에서 직접 관찰한 모습 |
|---|---:|---:|---|
| S18 연결 없는 테이블 | 1/1 | 5,575 | 상판과 지지 다리가 보이는 작은 탁자형 목재 구조 |
| S19 사방 연결 테이블 | 1/1 | 4,756 | 다리가 드러나지 않는 낮은 평판·상판형 목재 부분 |
| S28 책장 base | 1/1 | 8,062 | 길고 좁은 수직 목재 부분; 책이나 선반 전체는 구별하기 어려움 |
| S29 책장 middle | 1/1 | 5,124 | 더 낮은 목재 부분과 얇게 올라온 일부 구조; 완성형 책장은 확인 불가 |

각 F2 파일은 실제 원본 클라이언트의 1024×684 PNG이며, 모든 사진·접촉시트를 아티팩트에서 **직접 열어 관찰**했다. 특히 S28/S29의 모델명은 bookshelf지만 단독 분리된 상태를 찍었으므로 **완성된 책장의 시각적 역할 승인은 하지 않는다**. S18/S19의 테이블형 외관 관찰 또한 자연 연결 기능 검증은 아니다.

- 성공 F2 첫 증거 아티팩트: [Actions 아티팩트 14715440464](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/44923726837/artifacts/14715440464), 압축 SHA-256 `cc8cc849a400ba851fc20b197728898ac2118cc856983bc02b53fa096f3f5c78`.
- 위 F2 4장 SHA와 원본 모드 JAR·원본 적용 CSV SHA는 [INT4_MACAW_TABLE_SHELF_F2_SOURCE_RESULT.json](INT4_MACAW_TABLE_SHELF_F2_SOURCE_RESULT.json)에 고정.
- 이전 Macaw 주방 F2 3장과 이번 테이블·책장 F2 4장을 합쳐, 기존 비의자 대표 15사례 중 **7개 사례의 명시적 상태에 대한 실제 F2**가 확보됨. 이는 **7/15 사례 범위의 F2 수집**이지 INT-4 전체 47%나 INT-5 47%라는 뜻은 아니다.
- 원본 모드 JAR·PNG, 실제 스크린샷 바이너리는 Git 이력에 넣지 않음.
- **미완:** 자연스럽게 연결/분리되는 업데이트 로직, 완성된 다블록 형태의 시각 검증, Handcrafted 침대의 머리/발 블록 상태 실험, GPU 면별 UV 검증, 부품 역할·권리 승인.
