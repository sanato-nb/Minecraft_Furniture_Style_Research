# TEX07-R001 — 측정·UV 검수 방법

PNG: GitHub connector `fetch_file(ref=1.21.11,encoding=base64)` 반환 바이트를 Python Base64로 복호화. SHA256은 `hashlib.sha256`; Git blob SHA1은 `sha1(b'blob '+str(len(data)).encode()+b'\\0'+data)` 방식. PNG 8바이트 서명, 각 청크 CRC32(type+payload), IEND 종료 확인, Pillow `Image.open(...).load().convert('RGBA')` 처리. 16×16 전체 RGB를 배열로 순회함.

Luma Y: RGB8의 0.2126R+0.7152G+0.0722B, 모집단 표준편차. HSV S: 픽셀마다 RGB/255를 `colorsys.rgb_to_hsv`로 변환해 평균. 인접 차이는 RGB 3채널 절대차 평균(가로 240쌍, 세로 240쌍). 좌우/상하 끝선도 각각 16쌍의 RGB 차이. 중심과 테두리: 가운데 (x,y=1..14) 196픽셀 RGB 평균과 가장자리 60픽셀 RGB 평균의 평균 절대 차이.

블록 모델: 7개 state/model/item JSON과 공유 parent `cube_all`,`cube`,`block`의 원본 GitHub 1.21.11 파일을 직접 열어 경로·상속·면 참조를 확인. 각 source face에 숫자 UV가 누락되었으므로 영역 [0,0,16,16]은 큐브 전체 면의 기본 **파생 UV**로만 기록; 개별 방향 최종 화면의 플립/라이팅은 별도 검증 필요. 각 면이 256 위치를 재참조함(동일 소스 중복).

원본 추출 미러와 공식 Mojang client.jar SHA는 별개이며 후자는 이번 작업에서 확인하지 않음. 애니메이션 프레임 조사 없음.
