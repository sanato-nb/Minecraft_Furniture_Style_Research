# TEX05-R005 — 미프맵 원본 설정·PNG 저장 형식·일반 셰이더·인게임 증거 경계

| 자료 영역 | 직접 확인한 정적 근거 | 여기서 확정 불가능한 것 |
|---|---|---|
| PNG 사용자 추출본 6개 | SHA-256, CRC, 16×16 IHDR, 8bit alpha, color type 4/6, 실제 4-연결 높은 알파 마스크 | GPU 저장 포맷, 인게임 표면 알파/시각 결과 |
| `glass.png.mcmeta` (R004 계승) | `texture.mipmap_strategy=mean` 원문 | 구현 수식, LOD, 실제 생성 밉 레벨 |
| 착색 5종 sidecar (R004 계승) | 같은 경로의 `*.png.mcmeta` 미존재 | 게임 엔진의 기본 밉맵 전략 |
| R005 2×2 산술 측정 | 비중첩 2×2 4-알파값 단순 평균, 8×8=64칸; 16×16의 *가상* 단일 축소 | Minecraft 밉맵의 실제 결과라고 주장 불가 |
| `atlases/blocks.json` (R004 계승) | `block/` 디렉터리 참조 규칙 | 실제 아틀라스 슬롯 좌표·패딩 |
| `block.fsh/vsh` (R004 계승) | `Sampler0`, 조건부 `ALPHA_CUTOUT`, `UV0`, 광원맵 명시 | 여섯 유리에서 활성화된 shader/program, blend state, depth sort, face culling |
| 인게임 스크린샷/실행 | 제공/측정 없음 | 인게임 투명도·렌더 순서 검증 0/6 유지 |

원본 저장형식 차이(color type 4 vs 6)를 실제 렌더링 경로 차이라고 해석해서는 안 된다. 또한 일반 셰이더에서 `discard`를 발견했다고 유리 6종의 부분투명 픽셀이 게임에서 버려진다고 단언해서도 안 된다.

이 파일은 애니메이션 조사 없이 정적 소스만 대상으로 한다.
