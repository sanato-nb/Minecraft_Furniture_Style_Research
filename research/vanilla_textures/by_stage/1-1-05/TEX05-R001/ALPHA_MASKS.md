# TEX05-R001 — 실제 PNG 16×16 RGBA 픽셀 좌표 맵

- x=0..15 왼쪽→오른쪽; y=0..15 위→아래. 한 글자가 한 화소다.
- `1.21.11` 추출 이미지 및 동일 바이트의 InventivetalentDev/minecraft-assets `1.21.11` 미러에서 가져온 PNG 바이너리를 Pillow로 디코딩함. Mojang 공식 JAR 인증과는 별개.
- 정수 RGBA 1,536개 전체는 `PIXEL_RGBA.csv` 참조.

## 1. 무색 glass의 RGBA 실제 맵

`.`=(128,128,128,0) · `A`=(208,234,233,255) · `B`=(168,208,217,255) · `C`=(123,174,183,255) · `D`=(139,193,205,255).

```text
AAAAAAAAAAAAAAAB
A..............B
A...A..........C
A..A...........C
A.B............C
A..............D
A..............C
A..............D
A..............D
A..............D
A..............D
A..............D
B............A.D
A...........A..D
B..............B
BBDBDDDDDDDDDDBB
```

- 원래 RGB=(128,128,128)인 `.`의 191픽셀은 alpha=0이라 **보이지 않는다**.
- 65개 alpha=255 픽셀은 가장자리 60개 + 중앙 강조점 5개이며, 나머지 191개는 중앙 x=1..14, y=1..14의 투명 영역이다.

## 2. 착색 유리 5종의 공통 alpha 위치 맵

`E`=163(바깥 60), `i`=102(중앙 191), `m`=155(강조 5). 다섯 파일은 화소별 동일한 alpha 패턴이다.

```text
EEEEEEEEEEEEEEEE
EiiiiiiiiiiiiiiE
EiiimiiiiiiiiiiE
EiimiiiiiiiiiiiE
EimiiiiiiiiiiiiE
EiiiiiiiiiiiiiiE
EiiiiiiiiiiiiiiE
EiiiiiiiiiiiiiiE
EiiiiiiiiiiiiiiE
EiiiiiiiiiiiiiiE
EiiiiiiiiiiiiiiE
EiiiiiiiiiiiiiiE
EiiiiiiiiiiiimiE
EiiiiiiiiiiimiiE
EiiiiiiiiiiiiiiE
EEEEEEEEEEEEEEEE
```

- red RGB=(153,51,51), black=(25,25,25), blue=(51,76,178), green=(102,127,51), white=(255,255,255). 각 파일의 RGB는 전 화소에서 동일하며 alpha만 위치에 따라 변한다.
- 다섯 개 강조 좌표 (x,y): **(4,2), (3,3), (2,4), (13,12), (12,13)**.
- `glass`의 65개 불투명 픽셀 좌표는 착색 유리의 E+m 65개 좌표와 정확히 같다.
- 착색 유리는 alpha=0 픽셀이 0개이므로 **완전 투명한 구멍은 없다**.
- 실제 게임 내 투명 레이어·인접 유리 컬링·정렬은 공식 런타임 검증 전까지 pending.
