# INT-4 H23 — R06 원본 애니메이션 메타데이터 통제 실험 (검증 진행 기록)

## 직계 출처
H22 Draft #104 head 6faf00547f05f0d8a22abe8265920f0dd468318c의 CI 9/9 성공 확인. V4 역사 모델링 62/62, 위험 질문 7/8, 총 69/70. R06은 조건부로 유지한다. 기존 엄격 F70 무조건 0/70, H03 HOLD, H05 CONDITIONAL, INT5/INT6 0.

## 기존 자료 별도 재열람
H23에서 기존 실제 게임 [run 45104714782](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45104714782)의 artifact 14786478182 ZIP을 실제로 다시 내려받아 로컬에서 독립 재계산했다. ZIP SHA256 ddf965f6f87e91a2c4b65f435f36eae5ea6ed1fdee8e7638a0097f1fdb2e938e 일치, CRC 정상, client.log SHA256 824bd93e82298b9474a7b40f8bed886eb673ced475b856764c825fce19f3964b 일치. PNG 3개 모두 1024×684, F11E 원본 SHA 일치. 서버 상태 체크 3회, 간격 10.615초/10.358초.

| 쌍 | 물 ROI RGB24 변화 | 양쪽 청색 물 픽셀 | 싱크 ROI 내 물 외 변화 | 돌 대조 ROI 변화 |
|---|---:|---:|---:|---:|
| T0/T1 | 22 | 22 | 0 | 0 |
| T0/T2 | 8 | 8 | 0 | 0 |
| T1/T2 | 9 | 9 | 0 | 0 |

기존 시간차 변화 재현. 그러나 원래 촬영의 정확한 애니메이션 프레임 인덱스와 GPU 개별 texel 인과는 미확정.

## 신규 통제 실험
[Draft #105](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/pull/105), [실제 GitHub Actions #45339878802](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45339878802), 시작 코드 6c5ae3e1902118f9e83114570901fa90f32e1b7a.
- 공식 Macaw JAR 및 water_still.png·mcmeta SHA preflight. H22의 32개 프레임·UV [1,2,13,11] 재검사.
- 원본 애니메이션: frametime=2. 고정 대조: frametime=2, frames=[0]. 임시 JAR의 .mcmeta 1개 외 모든 uncompressed member 바이트 동일 검증.
- 동일 S43 north water=true fixture와 카메라, 실제 Minecraft F2 각각 3장. 물 픽셀 및 싱크 비수면·돌 대조 비교. 원본은 2쌍 이상 변화, 고정 대조 3쌍 무변화 및 교차 세션 대조 무변화가 통과 기준.
- 실제 실행 완료 및 아티팩트 독립 검수 전에는 새 모델링 승격 금지. 원본 JAR/PNG Git 미커밋.

이 문서는 실험 착수 및 재열람 결과이며 실험 성공 보고가 아니다. 최종 결과는 별도의 JSON/판정 원장으로 기록한다.
