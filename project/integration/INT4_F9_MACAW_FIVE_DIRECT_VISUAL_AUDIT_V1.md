# INT-4-F9 — Macaw 원본 5사례 Fabric 1.21.11 실제 F2 검증 및 독립 감사

- [실제 Minecraft 1.21.11 Actions #45035905411](https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/actions/runs/45035905411) 성공.
- 네이티브 F2 원본 5장·client.log·manifest GitHub Actions 아티팩트 ID 14759742774, ZIP SHA256 495378b596adb3d99105f45d01613d6366afe19efee9c802913db570a7a0bcb0.
- S08 oak_chair: 실제 F2 등받이 있는 작은 나무 의자, 정확 north 상태·모델/부모 SHA 확인.
- S09 oak_stool_chair: 실제 F2 등받이 없는 낮은 나무 스툴, 속성 없는 게임상태 정확 확인.
- S11 oak_end_table: 실제 F2 목재 소형 테이블, east/north/south/west 모두 false 상태 확인.
- S12 oak_coffee_table: 실제 F2 목제 상판과 기둥, connection=with_leg 상태 확인.
- S23 oak_drawer: 실제 F2 나무무늬 수납형 블록, connection=single/facing=north 상태 확인. 서랍 기능은 미검증.
- 연구 1-5 원본 5사례 / 39요소 / 179면. Macaw 3.4.2 JAR 및 각 state/model/provider SHA256와 네이티브 F2/서버 로그 독립 대조.
- **70개 원장** 조건부 43→48 / HOLD 27→22 / 역사 정확 F2 연결 37/62→42/62 / 무조건 승인 0.
- 남은 보류 Macaw S13·S24·S25·S35·S36 5건, 바닐라 15건, 고위험 R06·R08 2건.
- 이 실험은 명시적 /setblock 기반. 인접 구조 자연 생성, UV 픽셀 인과·기능·부품 의미 및 AI 자산 권리 확인/승인 아님.
