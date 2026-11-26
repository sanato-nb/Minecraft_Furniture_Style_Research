# INT-5-B22 — AF 원본 요소5+6 이중 조립 원형 렌더링 검증

작성: 2026-11-26 KST · 상위 B21 Draft PR #133 최종 검증 상태에서 새 적층 분기. **이번 작업은 실제 실험 코드/게임 F2/감사 수행 대상이며 연구 계획만을 뜻하지 않는다.**

## 1. 직계 선행 원본 증거 및 질문

- B19 45/45 원본 요소 제거 시험 중 43/45에서 한정 렌더 픽셀 변화가 관찰됐다. 미검출 2개는 AF121/AF1393/5·AF123/AF1394/5. 남·북·동·서 4방향에서도 모두 0픽셀.
- B20에서 원본 부모를 자식으로 전개하고 역방향 X의 from/to 숫자만 정렬해도 원래 10요소 의자 화면은 변하지 않았다.
- B21 [Actions #45746846169](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45746846169) **2/2 PASS, 두 ZIP 전량 독립 재감사**: 두 AF의 원본 요소5 단독 네 방향 중 최소 한 방향은 실제 게임에 보인다. X정렬 요소5 단독은 원본 요소6 단독의 정식 의자 before·after 8/8 PNG와 바이트 해시까지 동일하다. 원본 source5+source6의 경계 상자가 같지만 단독 원본 출력은 다르다. [최종 기계 근거](INT5_B21_AF_SOURCE5_ISOLATED_TWO_MODEL_FINAL_INDEPENDENT_REAL_F2_RESULT_V1.json).
- **다음 필수 질문:** 요소5 원본과 요소6 원본을 **두 개만 동시에 남겼을 때** 원본 요소5의 독립 가시성이 요소6과의 중첩/가림으로 화면에 추가되지 않는지 실제 실험으로 분리한다.

## 2. 고정 원본·세 가지 정확한 게임 구성

- 공식 Another Furniture Fabric **4.0.2 SHA1 `c2f992081bdc4795ed6d87771a3b5f7c71103785`**, Minecraft Java **1.21.1 Fabric**. 정확 child 모델 `acacia_1.json` / `acacia_10_tucked.json`만 자식 단독 덮어쓰기, 부모 JSON·기타 JAR 모든 구성원 바이트 불변, 시험용 JAR 재배포 없음.
- 부모 원본 10요소/46면을 먼저 검증, source5의 역방향 X·4면과 source6의 정방향 X·4면, 원본 face/UV/텍스처 전체를 보존. 동일 초기 월드 스냅샷 복원.

| 독립 클라이언트 | 실제 child `elements` | 원본 면 | 관찰 목적 |
|---|---|---:|---|
| `original_5` | 원본 index5 하나 | 4 | 원본 source5 단독으로 보이는지 다시 대조 |
| `positive_6` | 원본 index6 하나 | 4 | 원본 source6 단독 양성대조 |
| `pair_5_6` | 원본 index5, index6 두 개 순서 그대로 | 8 | source5와6 동시 배치 시 추가 화면 차이 검증 |

각 클라이언트에서 남·북·동·서 4방향 × 원본 전/다른 변형 또는 슬랩만/원본 후/AIR의 4단계 촬영, **16장 네이티브 F2**. 두 모델 **3게임×2 = 6클라이언트, 총 96개 F2**. 원본 AF123은 법적으로 유효한 `tucked=true` 지지 top-slab 유지, 서버 정확 상태 **추가 48건**. 모두 원본 ZIP·실제 client.log·서버 마커와 SHA256 검수.

## 3. 독립 감사 및 범위 한정 판단

- 세 클라이언트의 원본5 vs 원본6, 이중조립 vs 원본6, 이중조립 vs 원본5 화면 차이를 같은 카메라/동일 상태의 before와 after에서 독립 측정. 각각의 실제 다른 모델/슬랩·AIR·시간 A/A 음성대조 0 요구. 양성 source6와 원본5 단독 화면이 실제 보이며 서로 다를 때만 인과 판정.
- `PASS_PAIR5_6_MATCHES_ORIGINAL6_ONLY_AT_FOUR_CARDINAL_VIEWS`: 원본5는 홀로 보이지만 원본6과 동시에 있을 때 원본6 단독과 4방향 화면이 같다. **이 두 원본 요소의 조립체 렌더 결과에 관한 한정된 화면 중복/억제 증거**만 인정. GPU 픽셀 귀속이나 가림의 배타적 원인은 아님.
- `PASS_PAIR5_6_HAS_ADDITIONAL_RENDER_PIXELS_OVER_ORIGINAL6_ONLY`: 이중 조립에서 원본6 단독 대비 안정적인 추가 픽셀 발생. 해당 방향/상태의 한정 렌더 결과만 인정.
- `CONDITIONAL...`: 양성대조 실패, 시간·다른 모델·AIR 차이, 원본 SHA 불일치, 실게임 캡처 누락 시 연구 인과 미승인.

## 4. 실제 재현 코드·검증 자동화

- `src/mcfr/int5_b22_af_source5_source6_pair_four_view_f2.py` — 부모 원본 5·6만 붙이는 순수 child JSON 개입, 임시 one-member JAR 설치, 3게임/48F2, 원본 PNG·로그·서버 검증, 조건부/한정 결과 구분.
- `tests/knowledge/test_int5_b22_af_source5_source6_pair_four_view_f2.py` — 12개 정적 소스/픽셀/음성 대조/가짜 긍정 차단 회귀시험.
- `.github/workflows/integration-int5-b22-af-source5-source6-pair-overlap-f2.yml` — 두 대상 병렬 공식 Minecraft 1.21.1 Fabric 3세션 실게임 CI, F2 ZIP, 48 서버 상태 및 샘플 근거 재감사.

실제 GitHub Actions 결과 및 ZIP 재개봉 전에는 PASS·새 픽셀·원인 확정 수치를 쓰지 않는다. B19 원본 미검출 두 건, 누적 43/45, H03 HOLD/H05 CONDITIONAL/엄격 F70 무조건0/70, 의미·원본 face GPU 독점·제삼자 AI 학습/재배포 권리 승인0을 변경하지 않는다. 브랜치는 **Draft PR**로 남기고 main을 병합하지 않는다.
