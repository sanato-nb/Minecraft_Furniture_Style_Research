# INT-4-H9 Handcrafted 침대 occupied 속성의 모델·면·UV 출처 연구

- 원본 Handcrafted 8d21d1665916850c3fa3bdaf1370c50ec2ca7035의 oak_fancy_bed 블록상태 1,024개 전수 검증.
- 16색×4방향×4형태×2부분×2점유 = 1,024 선택자, occupied 대응 512쌍, 고유 leaf JSON 256개.
- 모델 선택 경로는 512쌍 모두 달라지지만 모델 기하 변경과 동의어가 아님.
- foot 256쌍: 선택 부모가 bed_<shape>에서 bed_<shape>_occupied로 변경, 4형태 모두 요소·면 UV 출처 변화. leaf 텍스처 슬롯 바인딩 동일.
- head 256쌍: occupied 이름으로 모델 경로는 변경되나 실제 leaf JSON은 쌍별 바이트 동일, 같은 cushion 부모 1요소·6면.
- 대표 원본 S37 single foot: 12요소·72면에서 14요소·84면으로 변경. S38 head: 1요소·6면 불변.
- 이전 실제 F2 S37/S38은 occupied=false만 검증했으며 occupied=true F2는 아직 0장.
- 게임 잠자기·깨기·파괴의 연속 동작 검증은 모델링 필수 목록에서 제외. occupied=true의 정적 비교 F2와 UV 인과 검증만 관련.
- H03/H05와 F70 전면 최종 승인, INT5 의미 및 INT6 권리 승인 조건은 변경하지 않음.
