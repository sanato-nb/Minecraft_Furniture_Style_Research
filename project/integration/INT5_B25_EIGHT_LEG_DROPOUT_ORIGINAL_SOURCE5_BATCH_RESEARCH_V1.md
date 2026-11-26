# INT-5-B25 — 원본 하부 요소 0·1·2·3 단일 제외 8병렬 실게임 F2 실험

- 작성: 2026-11-26 KST. 기준은 [B23+B24 누적 실험 PR #135](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/135) Draft head에서 실제 GitHub 코드 분기.
- **이번에는 모델 하나씩 순차 실험하지 않음.** AF121/AF123 × 원본 하부 요소 4개 중 하나를 제외하는 **8 GitHub Actions 병렬 실험**을 단일 workflow로 작성·실행.
- 공식 Minecraft Java 1.21.1 Fabric + Another Furniture 4.0.2 official JAR SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785` 원본, 수정 JAR/텍스처/소스 배포 없음. 원래 index5의 X 역방향·UV·faces 원본 그대로.

## 1. 왜 B25가 필요한가
B21에서는 원본 index5만 남기면 독립 Fabric GUI에서 보였다. B22에서 source6만으로 source5가 완전히 가려지지는 않았다. B23에서 AF121 원형 source6+(0..3)은 source5 추가에 따라 남/북/동/서 286/218/294/227픽셀이 관찰된 반면, source6+(0..4)는 0/0/0/0, source6+4는 2/0/2/0이었다. 첫 원본 그룹들 단독의 화면 반응과 다르게 하부 `0..4` 조합에서 가림 효과가 나타난다.

**B25 질문:** 전체 0..4 맥락에서 0,1,2,3 원본 요소 중 하나를 제거하면 source5의 화면 기여가 다시 나타나는가? 나타나면 해당 인덱스가 *그 조합 안에서* 가림 상태에 기여하는 한정 증거이고, 아니면 한 요소만 빼도 다른 요소가 가림 상태를 유지할 가능성이 있다.

## 2. 네 실험 맥락 × 두 실제 AF 모델 = 8 jobs

| B25 맥락 | source6 고정 + 원본에서 남기는 다른 요소들 | 비교하는 원본 요소 |
|---|---|---|
| `without_leg0` | `1,2,3,4` | source5 **on/off** |
| `without_leg1` | `0,2,3,4` | source5 **on/off** |
| `without_leg2` | `0,1,3,4` | source5 **on/off** |
| `without_leg3` | `0,1,2,4` | source5 **on/off** |

- 위 명칭의 "leg"는 **기존 B3 역할 가설**을 상속할 뿐 구조의 실제 다리 기능으로 승인한 것이 아니다.
- 총 **8 jobs × 2독립 공식 게임 클라이언트 = 16 실제 Minecraft Fabric 세션 × 4카메라 × 4단계 = 256 원본 native F2** 목표.
- B23 검수 완료된 두 모드 `without_5`/`with_5` 실험을 재사용하고 매 게임마다 원본 월드 스냅샷 복원. 원본 10요소/46면 부모의 source5·6 포함 모든 원형 인덱스·face/UV·source 텍스처 변경 금지. 원본 자식 JSON 한 구성원만 임시 교체.
- **엄격 성공:** 공식 JAR SHA1·Git 원본 blob 고정, 32 PNG SHA+2게임 로그+서버 정확 블록 상태32(접힌 의자는 support slab32 추가)·네 방향 이전/재현/다른 의자·AIR 대비 비교, 시간/음성대조0 및 source5 차이의 foreground 한정.
- 해석은 `SOURCE5_ADDS_PIXELS_WHEN_ORIGINAL_LEG_OMITTED` 또는 `SOURCE5_STILL_NOT_VISIBLE_WITH_THIS_LEG_OMITTED`와 실제 남·북·동·서 픽셀수. 유일 원인·물리적 기능·재질·스타일·face GPU 독점 pix 소유/AI 학습권리를 판정하지 않는다.

## 3. 실제 구현 파일
- `src/mcfr/int5_b25_leg_dropout_source5_batch_f2.py` — B23 확정 소스 capture/원본 리소스 교체/F2 감사 코드를 **재사용**, B25 네 조합을 원본 소스 인덱스 차집합으로 강제, 엄격 결과 JSON 생성.
- `tests/knowledge/test_int5_b25_leg_dropout_source5_batch_f2.py` — 7개 모든 맥락/2모델/원본 UV 불변/부정·권리 승인0 회귀시험.
- `.github/workflows/integration-int5-b25-8leg-dropout-256-native-f2.yml` — 두 의자 × 4조합 총 8잡 CI, 4잡 동시 실행, 개별 native F2/서버/로그/audit artifact 보존.
- [B25 Actions 실행 현황](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45784956570) — 실게임 완료·원본 ZIP 재개봉 전까지 모델별 인과 수치를 확정하지 않음.

## 4. 누적 연구 게이트
- B19 원본 45요소 중 한정된 원형 F2 제거 인과 43/45, 무반응 원본 두 index5는 B21/B22/B23/B25의 다른 조합 대조 결과가 나와도 원본 전체 의자 결과를 직접 교체하지 않는다.
- 역할 후보 원장 B24: 45요소·229원본 face 전수 출처 교차·texture cue 10/weak shared 35; 엄격 `part_function_verified=0/45`, `material_or_style_approved=0/45`, GPU 원본 face/UV 배타 픽셀 귀속0, 제3자 AI 학습·재배포 권리 승인0.
- `H03 HOLD`, `H05 CONDITIONAL`, 엄격 `F70` 무조건0/70. 모든 증거는 stacked **Draft PR**로 남기고 `main` 원본을 병합·수정하지 않는다.
