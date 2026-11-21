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
