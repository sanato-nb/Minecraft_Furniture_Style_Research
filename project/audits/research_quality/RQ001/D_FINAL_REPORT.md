# RQ-001 6-D 전수 파일 검사 종료 기록

검증 커밋 79f3dba821005ff7b1d996e12643b9d19a95a873, Actions #46126625792 / Job 140922530030 / artifact 15255658373. 전체 3,167경로 검사 완료, 해시 3,167/3,167 일치, 형식 3,165/3,167 통과. 16배치, 첫 8배치와 재개 후 새 8배치, 기존 8배치 재사용. 자체 테스트 12/12. 실행 성공과 자료 품질 FAIL 분리.

## 실제 결함
- TEX05-R004/SOURCE_LEDGER.csv: 헤더 14열, 데이터 행 3/4/5가 15/16/16열. static_finding 필드의 인용부호 없는 쉼표 (directory(...), Sampler0,..., vertex_lightmap_color,...). 뒤의 3개 검증 여부 필드가 밀릴 수 있다.
- TEX05-R007/BLOCK_VS_TERRAIN_SHADER.csv: 헤더 5열, 행 2는 6열. texture(Sampler0,texCoord0)의 쉼표 미인용. 비교 필드가 밀릴 수 있다.
- 원문과 해당 REPORT.md를 직접 대조하여 단순 파서 오류가 아닌 원래 CSV의 형식 결함임을 확인. 보고서 내용 자체의 오류를 증명한 것은 아니다.
- 원본 보존: 둘 다 REVALIDATE. 추후 별도 파생 정규화/재검증 후보이며 이번 감사에서 기존 파일 수정·삭제 금지.

[검사 실행](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/46126625792) · [기계 판독 증거](D_FINAL_EVIDENCE.json). 6-E로 진행 가능하되 6-D FAIL 및 두 예외는 종료 심사에 남긴다.
