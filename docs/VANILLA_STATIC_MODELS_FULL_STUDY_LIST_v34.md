# 바닐라 블록 모델 전체 2,390종 — 정적 모델링 연구 검토 예정 목록 (v34 기준)

**기준 자료:** 사용자 저장소 `1.21.11/assets/minecraft/models/block/*.json`의 Git 트리에서 실제 확인한 **2,390개 모든 파일 경로와 Git blob SHA**. 소스 [v34 원본 전체 인벤토리](../research/vanilla_models/v34/01_inventory_2390_block_model_paths_git_shas.csv). 2026-11-13.

> 이 문서는 **앞으로 검토할 전체 후보 큐**로, 각 파일을 **이미 완전 분석했다거나 전부 새롭게 미조사 상태라고 판정한 목록이 아니다**. v5–v34에 선행 검토 기록이 있는 항목도 포함되어 있으며, 실제 재검증·중복 대조 결과에 따라 상태를 갱신한다. 분류는 **파일명 규칙에 따른 1차 자동 묶음(휴리스틱)**이라 실제 기능/3D 형상이 아닌 이름만으로 구분한 것이며 특히 기타 분류는 추가 조사할 예정이다.

**연구 우선순위:** P1 가구에 가까운 수납·작업·조명·실내 장식 → P2 건축 부품·문/연결 구조·장치·기술 템플릿 → P3 자연·기본 재질·특수표현·기타 후보. **애니메이션 프레임/시간에 따른 움직임은 사용자 요청으로 전면 보류**. 다만 `lit`/`powered`/`open` 같은 정적 블록 상태 선택 규칙 자체는 분석 범위에 포함한다.

**모든 모델 파일을 깊이 똑같이 조사한다는 뜻은 아님:** 고유 3D 원형·재질·UV·blockstate의 대표 모델과 leaf 상속을 비교하며, 동일 템플릿을 사용하는 색상/목재 반복 변형은 **원형은 정밀검사, 반복 leaf는 실제 파일 참조·텍스처 차이 검증** 방식으로 중복 분석을 줄일 예정이다. 파일 경로 수 2,390개와 가구 전용 모델의 완료율 분모는 다른 개념이다.

## 분류별 전체 수

| 단계 | 파일명 기반 분류 | 포함 모델 파일 |
|---|---|---:|
| P1 | 01. 수납·선반·책장·상자·용기 | 169 |
| P1 | 02. 제작·작업대·도구·가공 설비 | 32 |
| P1 | 03. 조명·촛불·램프·장식 막대 | 227 |
| P1 | 04. 침대·표지판·현수막·화분·실내 장식 | 116 |
| P2 | 05. 문·다락문·울타리 문 | 257 |
| P2 | 06. 계단·반블록·형상 변형 | 284 |
| P2 | 07. 울타리·담장·유리판·난간·연결 | 277 |
| P2 | 08. 레드스톤·기계·스위치·레일 | 198 |
| P3 | 09. 식물·작물·잎·꽃·버섯·산호 | 241 |
| P3 | 10. 유체·포털·불·자연 특수 표현 | 38 |
| P3 | 11. 기본 재질·석재·광물·목재·색상 | 375 |
| P2 | 12. 엔진 원형·인벤토리용 기술 모델 | 23 |
| P3 | 13. 기타 원본 모델·형태별 재분류 대상 | 153 |
| **합계** | **모든 블록 모델 JSON 파일이 정확히 한 번만 분류됨** | **2,390** |

## 각 분류에 포함되는 파일명 전부

### 01. 수납·선반·책장·상자·용기 — 169개 (P1)

- `acacia_shelf_center.json`, `acacia_shelf_inventory.json`, `acacia_shelf_left.json`, `acacia_shelf_right.json`, `acacia_shelf_unconnected.json`, `acacia_shelf_unpowered.json`, `acacia_shelf.json`, `bamboo_shelf_center.json`
- `bamboo_shelf_inventory.json`, `bamboo_shelf_left.json`, `bamboo_shelf_right.json`, `bamboo_shelf_unconnected.json`, `bamboo_shelf_unpowered.json`, `bamboo_shelf.json`, `barrel_open.json`, `barrel.json`
- `bee_nest_empty.json`, `bee_nest_honey.json`, `beehive_empty.json`, `beehive_honey.json`, `birch_shelf_center.json`, `birch_shelf_inventory.json`, `birch_shelf_left.json`, `birch_shelf_right.json`
- `birch_shelf_unconnected.json`, `birch_shelf_unpowered.json`, `birch_shelf.json`, `black_shulker_box.json`, `blue_shulker_box.json`, `bookshelf.json`, `brown_shulker_box.json`, `cauldron.json`
- `cherry_shelf_center.json`, `cherry_shelf_inventory.json`, `cherry_shelf_left.json`, `cherry_shelf_right.json`, `cherry_shelf_unconnected.json`, `cherry_shelf_unpowered.json`, `cherry_shelf.json`, `chest.json`
- `chiseled_bookshelf_empty_slot_bottom_left.json`, `chiseled_bookshelf_empty_slot_bottom_mid.json`, `chiseled_bookshelf_empty_slot_bottom_right.json`, `chiseled_bookshelf_empty_slot_top_left.json`, `chiseled_bookshelf_empty_slot_top_mid.json`, `chiseled_bookshelf_empty_slot_top_right.json`, `chiseled_bookshelf_inventory.json`, `chiseled_bookshelf_occupied_slot_bottom_left.json`
- `chiseled_bookshelf_occupied_slot_bottom_mid.json`, `chiseled_bookshelf_occupied_slot_bottom_right.json`, `chiseled_bookshelf_occupied_slot_top_left.json`, `chiseled_bookshelf_occupied_slot_top_mid.json`, `chiseled_bookshelf_occupied_slot_top_right.json`, `chiseled_bookshelf.json`, `composter_contents_ready.json`, `composter_contents1.json`
- `composter_contents2.json`, `composter_contents3.json`, `composter_contents4.json`, `composter_contents5.json`, `composter_contents6.json`, `composter_contents7.json`, `composter.json`, `copper_chest.json`
- `crimson_shelf_center.json`, `crimson_shelf_inventory.json`, `crimson_shelf_left.json`, `crimson_shelf_right.json`, `crimson_shelf_unconnected.json`, `crimson_shelf_unpowered.json`, `crimson_shelf.json`, `cyan_shulker_box.json`
- `dark_oak_shelf_center.json`, `dark_oak_shelf_inventory.json`, `dark_oak_shelf_left.json`, `dark_oak_shelf_right.json`, `dark_oak_shelf_unconnected.json`, `dark_oak_shelf_unpowered.json`, `dark_oak_shelf.json`, `decorated_pot.json`
- `ender_chest.json`, `exposed_copper_chest.json`, `flower_pot_cross_emissive.json`, `flower_pot_cross.json`, `flower_pot.json`, `gray_shulker_box.json`, `green_shulker_box.json`, `hopper_side.json`
- `hopper.json`, `jungle_shelf_center.json`, `jungle_shelf_inventory.json`, `jungle_shelf_left.json`, `jungle_shelf_right.json`, `jungle_shelf_unconnected.json`, `jungle_shelf_unpowered.json`, `jungle_shelf.json`
- `lava_cauldron.json`, `light_blue_shulker_box.json`, `light_gray_shulker_box.json`, `lime_shulker_box.json`, `magenta_shulker_box.json`, `mangrove_shelf_center.json`, `mangrove_shelf_inventory.json`, `mangrove_shelf_left.json`
- `mangrove_shelf_right.json`, `mangrove_shelf_unconnected.json`, `mangrove_shelf_unpowered.json`, `mangrove_shelf.json`, `oak_shelf_center.json`, `oak_shelf_inventory.json`, `oak_shelf_left.json`, `oak_shelf_right.json`
- `oak_shelf_unconnected.json`, `oak_shelf_unpowered.json`, `oak_shelf.json`, `orange_shulker_box.json`, `oxidized_copper_chest.json`, `pale_oak_shelf_center.json`, `pale_oak_shelf_inventory.json`, `pale_oak_shelf_left.json`
- `pale_oak_shelf_right.json`, `pale_oak_shelf_unconnected.json`, `pale_oak_shelf_unpowered.json`, `pale_oak_shelf.json`, `pink_shulker_box.json`, `powder_snow_cauldron_full.json`, `powder_snow_cauldron_level1.json`, `powder_snow_cauldron_level2.json`
- `purple_shulker_box.json`, `red_shulker_box.json`, `shulker_box.json`, `spruce_shelf_center.json`, `spruce_shelf_inventory.json`, `spruce_shelf_left.json`, `spruce_shelf_right.json`, `spruce_shelf_unconnected.json`
- `spruce_shelf_unpowered.json`, `spruce_shelf.json`, `template_cauldron_full.json`, `template_cauldron_level1.json`, `template_cauldron_level2.json`, `template_chiseled_bookshelf_slot_bottom_left.json`, `template_chiseled_bookshelf_slot_bottom_mid.json`, `template_chiseled_bookshelf_slot_bottom_right.json`
- `template_chiseled_bookshelf_slot_top_left.json`, `template_chiseled_bookshelf_slot_top_mid.json`, `template_chiseled_bookshelf_slot_top_right.json`, `template_shelf_body.json`, `template_shelf_center.json`, `template_shelf_inventory.json`, `template_shelf_left.json`, `template_shelf_right.json`
- `template_shelf_unconnected.json`, `template_shelf_unpowered.json`, `tinted_flower_pot_cross.json`, `trapped_chest.json`, `warped_shelf_center.json`, `warped_shelf_inventory.json`, `warped_shelf_left.json`, `warped_shelf_right.json`
- `warped_shelf_unconnected.json`, `warped_shelf_unpowered.json`, `warped_shelf.json`, `water_cauldron_full.json`, `water_cauldron_level1.json`, `water_cauldron_level2.json`, `weathered_copper_chest.json`, `white_shulker_box.json`
- `yellow_shulker_box.json`

### 02. 제작·작업대·도구·가공 설비 — 32개 (P1)

- `anvil.json`, `blast_furnace_on.json`, `blast_furnace.json`, `brewing_stand_bottle0.json`, `brewing_stand_bottle1.json`, `brewing_stand_bottle2.json`, `brewing_stand_empty0.json`, `brewing_stand_empty1.json`
- `brewing_stand_empty2.json`, `brewing_stand.json`, `cartography_table.json`, `chipped_anvil.json`, `crafter_crafting_triggered.json`, `crafter_crafting.json`, `crafter_triggered.json`, `crafter.json`
- `crafting_table.json`, `damaged_anvil.json`, `enchanting_table.json`, `fletching_table.json`, `furnace_on.json`, `furnace.json`, `grindstone.json`, `jukebox.json`
- `lectern.json`, `loom.json`, `note_block.json`, `smithing_table.json`, `smoker_on.json`, `smoker.json`, `stonecutter.json`, `template_anvil.json`

### 03. 조명·촛불·램프·장식 막대 — 227개 (P1)

- `beacon.json`, `black_candle_cake_lit.json`, `black_candle_cake.json`, `black_candle_four_candles_lit.json`, `black_candle_four_candles.json`, `black_candle_one_candle_lit.json`, `black_candle_one_candle.json`, `black_candle_three_candles_lit.json`
- `black_candle_three_candles.json`, `black_candle_two_candles_lit.json`, `black_candle_two_candles.json`, `blue_candle_cake_lit.json`, `blue_candle_cake.json`, `blue_candle_four_candles_lit.json`, `blue_candle_four_candles.json`, `blue_candle_one_candle_lit.json`
- `blue_candle_one_candle.json`, `blue_candle_three_candles_lit.json`, `blue_candle_three_candles.json`, `blue_candle_two_candles_lit.json`, `blue_candle_two_candles.json`, `brown_candle_cake_lit.json`, `brown_candle_cake.json`, `brown_candle_four_candles_lit.json`
- `brown_candle_four_candles.json`, `brown_candle_one_candle_lit.json`, `brown_candle_one_candle.json`, `brown_candle_three_candles_lit.json`, `brown_candle_three_candles.json`, `brown_candle_two_candles_lit.json`, `brown_candle_two_candles.json`, `campfire_off.json`
- `campfire.json`, `candle_cake_lit.json`, `candle_cake.json`, `candle_four_candles_lit.json`, `candle_four_candles.json`, `candle_one_candle_lit.json`, `candle_one_candle.json`, `candle_three_candles_lit.json`
- `candle_three_candles.json`, `candle_two_candles_lit.json`, `candle_two_candles.json`, `conduit.json`, `copper_lantern_hanging.json`, `copper_lantern.json`, `copper_torch.json`, `copper_wall_torch.json`
- `cyan_candle_cake_lit.json`, `cyan_candle_cake.json`, `cyan_candle_four_candles_lit.json`, `cyan_candle_four_candles.json`, `cyan_candle_one_candle_lit.json`, `cyan_candle_one_candle.json`, `cyan_candle_three_candles_lit.json`, `cyan_candle_three_candles.json`
- `cyan_candle_two_candles_lit.json`, `cyan_candle_two_candles.json`, `end_rod.json`, `exposed_copper_lantern_hanging.json`, `exposed_copper_lantern.json`, `exposed_lightning_rod.json`, `glowstone.json`, `gray_candle_cake_lit.json`
- `gray_candle_cake.json`, `gray_candle_four_candles_lit.json`, `gray_candle_four_candles.json`, `gray_candle_one_candle_lit.json`, `gray_candle_one_candle.json`, `gray_candle_three_candles_lit.json`, `gray_candle_three_candles.json`, `gray_candle_two_candles_lit.json`
- `gray_candle_two_candles.json`, `green_candle_cake_lit.json`, `green_candle_cake.json`, `green_candle_four_candles_lit.json`, `green_candle_four_candles.json`, `green_candle_one_candle_lit.json`, `green_candle_one_candle.json`, `green_candle_three_candles_lit.json`
- `green_candle_three_candles.json`, `green_candle_two_candles_lit.json`, `green_candle_two_candles.json`, `jack_o_lantern.json`, `lantern_hanging.json`, `lantern.json`, `light_blue_candle_cake_lit.json`, `light_blue_candle_cake.json`
- `light_blue_candle_four_candles_lit.json`, `light_blue_candle_four_candles.json`, `light_blue_candle_one_candle_lit.json`, `light_blue_candle_one_candle.json`, `light_blue_candle_three_candles_lit.json`, `light_blue_candle_three_candles.json`, `light_blue_candle_two_candles_lit.json`, `light_blue_candle_two_candles.json`
- `light_gray_candle_cake_lit.json`, `light_gray_candle_cake.json`, `light_gray_candle_four_candles_lit.json`, `light_gray_candle_four_candles.json`, `light_gray_candle_one_candle_lit.json`, `light_gray_candle_one_candle.json`, `light_gray_candle_three_candles_lit.json`, `light_gray_candle_three_candles.json`
- `light_gray_candle_two_candles_lit.json`, `light_gray_candle_two_candles.json`, `lightning_rod_on.json`, `lightning_rod.json`, `lime_candle_cake_lit.json`, `lime_candle_cake.json`, `lime_candle_four_candles_lit.json`, `lime_candle_four_candles.json`
- `lime_candle_one_candle_lit.json`, `lime_candle_one_candle.json`, `lime_candle_three_candles_lit.json`, `lime_candle_three_candles.json`, `lime_candle_two_candles_lit.json`, `lime_candle_two_candles.json`, `magenta_candle_cake_lit.json`, `magenta_candle_cake.json`
- `magenta_candle_four_candles_lit.json`, `magenta_candle_four_candles.json`, `magenta_candle_one_candle_lit.json`, `magenta_candle_one_candle.json`, `magenta_candle_three_candles_lit.json`, `magenta_candle_three_candles.json`, `magenta_candle_two_candles_lit.json`, `magenta_candle_two_candles.json`
- `ochre_froglight_horizontal.json`, `ochre_froglight.json`, `orange_candle_cake_lit.json`, `orange_candle_cake.json`, `orange_candle_four_candles_lit.json`, `orange_candle_four_candles.json`, `orange_candle_one_candle_lit.json`, `orange_candle_one_candle.json`
- `orange_candle_three_candles_lit.json`, `orange_candle_three_candles.json`, `orange_candle_two_candles_lit.json`, `orange_candle_two_candles.json`, `oxidized_copper_lantern_hanging.json`, `oxidized_copper_lantern.json`, `oxidized_lightning_rod.json`, `pearlescent_froglight_horizontal.json`
- `pearlescent_froglight.json`, `pink_candle_cake_lit.json`, `pink_candle_cake.json`, `pink_candle_four_candles_lit.json`, `pink_candle_four_candles.json`, `pink_candle_one_candle_lit.json`, `pink_candle_one_candle.json`, `pink_candle_three_candles_lit.json`
- `pink_candle_three_candles.json`, `pink_candle_two_candles_lit.json`, `pink_candle_two_candles.json`, `purple_candle_cake_lit.json`, `purple_candle_cake.json`, `purple_candle_four_candles_lit.json`, `purple_candle_four_candles.json`, `purple_candle_one_candle_lit.json`
- `purple_candle_one_candle.json`, `purple_candle_three_candles_lit.json`, `purple_candle_three_candles.json`, `purple_candle_two_candles_lit.json`, `purple_candle_two_candles.json`, `red_candle_cake_lit.json`, `red_candle_cake.json`, `red_candle_four_candles_lit.json`
- `red_candle_four_candles.json`, `red_candle_one_candle_lit.json`, `red_candle_one_candle.json`, `red_candle_three_candles_lit.json`, `red_candle_three_candles.json`, `red_candle_two_candles_lit.json`, `red_candle_two_candles.json`, `redstone_lamp_on.json`
- `redstone_lamp.json`, `redstone_torch_off.json`, `redstone_torch.json`, `redstone_wall_torch_off.json`, `redstone_wall_torch.json`, `sea_lantern.json`, `shroomlight.json`, `soul_campfire.json`
- `soul_lantern_hanging.json`, `soul_lantern.json`, `soul_torch.json`, `soul_wall_torch.json`, `template_cake_with_candle.json`, `template_campfire.json`, `template_candle.json`, `template_hanging_lantern.json`
- `template_lantern.json`, `template_lightning_rod.json`, `template_redstone_torch_wall.json`, `template_redstone_torch.json`, `template_torch_unlit.json`, `template_torch_wall_unlit.json`, `template_torch_wall.json`, `template_torch.json`
- `torch.json`, `verdant_froglight_horizontal.json`, `verdant_froglight.json`, `wall_torch.json`, `weathered_copper_lantern_hanging.json`, `weathered_copper_lantern.json`, `weathered_lightning_rod.json`, `white_candle_cake_lit.json`
- `white_candle_cake.json`, `white_candle_four_candles_lit.json`, `white_candle_four_candles.json`, `white_candle_one_candle_lit.json`, `white_candle_one_candle.json`, `white_candle_three_candles_lit.json`, `white_candle_three_candles.json`, `white_candle_two_candles_lit.json`
- `white_candle_two_candles.json`, `yellow_candle_cake_lit.json`, `yellow_candle_cake.json`, `yellow_candle_four_candles_lit.json`, `yellow_candle_four_candles.json`, `yellow_candle_one_candle_lit.json`, `yellow_candle_one_candle.json`, `yellow_candle_three_candles_lit.json`
- `yellow_candle_three_candles.json`, `yellow_candle_two_candles_lit.json`, `yellow_candle_two_candles.json`

### 04. 침대·표지판·현수막·화분·실내 장식 — 116개 (P1)

- `acacia_hanging_sign.json`, `acacia_sign.json`, `bamboo_hanging_sign.json`, `bamboo_sign.json`, `banner.json`, `bed.json`, `bell_between_walls.json`, `bell_ceiling.json`
- `bell_floor.json`, `bell_wall.json`, `birch_hanging_sign.json`, `birch_sign.json`, `black_carpet.json`, `blue_carpet.json`, `brown_carpet.json`, `cake_slice1.json`
- `cake_slice2.json`, `cake_slice3.json`, `cake_slice4.json`, `cake_slice5.json`, `cake_slice6.json`, `cake.json`, `carpet.json`, `cherry_hanging_sign.json`
- `cherry_sign.json`, `crimson_hanging_sign.json`, `crimson_sign.json`, `cyan_carpet.json`, `dark_oak_hanging_sign.json`, `dark_oak_sign.json`, `dead_sea_pickle.json`, `glow_item_frame_map.json`
- `glow_item_frame.json`, `gray_carpet.json`, `green_carpet.json`, `item_frame_map.json`, `item_frame.json`, `jungle_hanging_sign.json`, `jungle_sign.json`, `light_blue_carpet.json`
- `light_gray_carpet.json`, `lime_carpet.json`, `magenta_carpet.json`, `mangrove_hanging_sign.json`, `mangrove_sign.json`, `moss_carpet.json`, `mossy_carpet_side.json`, `oak_hanging_sign.json`
- `oak_sign.json`, `orange_carpet.json`, `pale_moss_carpet_side_small.json`, `pale_moss_carpet_side_tall.json`, `pale_moss_carpet.json`, `pale_oak_hanging_sign.json`, `pale_oak_sign.json`, `pink_carpet.json`
- `piston_head_short_sticky.json`, `piston_head_short.json`, `piston_head_sticky.json`, `piston_head.json`, `potted_acacia_sapling.json`, `potted_allium.json`, `potted_azalea_bush.json`, `potted_azure_bluet.json`
- `potted_bamboo.json`, `potted_birch_sapling.json`, `potted_blue_orchid.json`, `potted_brown_mushroom.json`, `potted_cactus.json`, `potted_cherry_sapling.json`, `potted_closed_eyeblossom.json`, `potted_cornflower.json`
- `potted_crimson_fungus.json`, `potted_crimson_roots.json`, `potted_dandelion.json`, `potted_dark_oak_sapling.json`, `potted_dead_bush.json`, `potted_fern.json`, `potted_flowering_azalea_bush.json`, `potted_jungle_sapling.json`
- `potted_lily_of_the_valley.json`, `potted_mangrove_propagule.json`, `potted_oak_sapling.json`, `potted_open_eyeblossom.json`, `potted_orange_tulip.json`, `potted_oxeye_daisy.json`, `potted_pale_oak_sapling.json`, `potted_pink_tulip.json`
- `potted_poppy.json`, `potted_red_mushroom.json`, `potted_red_tulip.json`, `potted_spruce_sapling.json`, `potted_torchflower.json`, `potted_warped_fungus.json`, `potted_warped_roots.json`, `potted_white_tulip.json`
- `potted_wither_rose.json`, `purple_carpet.json`, `red_carpet.json`, `sea_pickle.json`, `skull.json`, `slightly_cracked_turtle_egg.json`, `spruce_hanging_sign.json`, `spruce_sign.json`
- `template_item_frame_map.json`, `template_item_frame.json`, `template_piston_head_short.json`, `template_piston_head.json`, `template_potted_azalea_bush.json`, `template_turtle_egg.json`, `turtle_egg.json`, `very_cracked_turtle_egg.json`
- `warped_hanging_sign.json`, `warped_sign.json`, `white_carpet.json`, `yellow_carpet.json`

### 05. 문·다락문·울타리 문 — 257개 (P2)

- `acacia_door_bottom_left_open.json`, `acacia_door_bottom_left.json`, `acacia_door_bottom_right_open.json`, `acacia_door_bottom_right.json`, `acacia_door_top_left_open.json`, `acacia_door_top_left.json`, `acacia_door_top_right_open.json`, `acacia_door_top_right.json`
- `acacia_fence_gate_open.json`, `acacia_fence_gate_wall_open.json`, `acacia_fence_gate_wall.json`, `acacia_fence_gate.json`, `acacia_trapdoor_bottom.json`, `acacia_trapdoor_open.json`, `acacia_trapdoor_top.json`, `bamboo_door_bottom_left_open.json`
- `bamboo_door_bottom_left.json`, `bamboo_door_bottom_right_open.json`, `bamboo_door_bottom_right.json`, `bamboo_door_top_left_open.json`, `bamboo_door_top_left.json`, `bamboo_door_top_right_open.json`, `bamboo_door_top_right.json`, `bamboo_fence_gate_open.json`
- `bamboo_fence_gate_wall_open.json`, `bamboo_fence_gate_wall.json`, `bamboo_fence_gate.json`, `bamboo_trapdoor_bottom.json`, `bamboo_trapdoor_open.json`, `bamboo_trapdoor_top.json`, `birch_door_bottom_left_open.json`, `birch_door_bottom_left.json`
- `birch_door_bottom_right_open.json`, `birch_door_bottom_right.json`, `birch_door_top_left_open.json`, `birch_door_top_left.json`, `birch_door_top_right_open.json`, `birch_door_top_right.json`, `birch_fence_gate_open.json`, `birch_fence_gate_wall_open.json`
- `birch_fence_gate_wall.json`, `birch_fence_gate.json`, `birch_trapdoor_bottom.json`, `birch_trapdoor_open.json`, `birch_trapdoor_top.json`, `cherry_door_bottom_left_open.json`, `cherry_door_bottom_left.json`, `cherry_door_bottom_right_open.json`
- `cherry_door_bottom_right.json`, `cherry_door_top_left_open.json`, `cherry_door_top_left.json`, `cherry_door_top_right_open.json`, `cherry_door_top_right.json`, `cherry_fence_gate_open.json`, `cherry_fence_gate_wall_open.json`, `cherry_fence_gate_wall.json`
- `cherry_fence_gate.json`, `cherry_trapdoor_bottom.json`, `cherry_trapdoor_open.json`, `cherry_trapdoor_top.json`, `copper_door_bottom_left_open.json`, `copper_door_bottom_left.json`, `copper_door_bottom_right_open.json`, `copper_door_bottom_right.json`
- `copper_door_top_left_open.json`, `copper_door_top_left.json`, `copper_door_top_right_open.json`, `copper_door_top_right.json`, `copper_trapdoor_bottom.json`, `copper_trapdoor_open.json`, `copper_trapdoor_top.json`, `crimson_door_bottom_left_open.json`
- `crimson_door_bottom_left.json`, `crimson_door_bottom_right_open.json`, `crimson_door_bottom_right.json`, `crimson_door_top_left_open.json`, `crimson_door_top_left.json`, `crimson_door_top_right_open.json`, `crimson_door_top_right.json`, `crimson_fence_gate_open.json`
- `crimson_fence_gate_wall_open.json`, `crimson_fence_gate_wall.json`, `crimson_fence_gate.json`, `crimson_trapdoor_bottom.json`, `crimson_trapdoor_open.json`, `crimson_trapdoor_top.json`, `dark_oak_door_bottom_left_open.json`, `dark_oak_door_bottom_left.json`
- `dark_oak_door_bottom_right_open.json`, `dark_oak_door_bottom_right.json`, `dark_oak_door_top_left_open.json`, `dark_oak_door_top_left.json`, `dark_oak_door_top_right_open.json`, `dark_oak_door_top_right.json`, `dark_oak_fence_gate_open.json`, `dark_oak_fence_gate_wall_open.json`
- `dark_oak_fence_gate_wall.json`, `dark_oak_fence_gate.json`, `dark_oak_trapdoor_bottom.json`, `dark_oak_trapdoor_open.json`, `dark_oak_trapdoor_top.json`, `door_bottom_left_open.json`, `door_bottom_left.json`, `door_bottom_right_open.json`
- `door_bottom_right.json`, `door_top_left_open.json`, `door_top_left.json`, `door_top_right_open.json`, `door_top_right.json`, `exposed_copper_door_bottom_left_open.json`, `exposed_copper_door_bottom_left.json`, `exposed_copper_door_bottom_right_open.json`
- `exposed_copper_door_bottom_right.json`, `exposed_copper_door_top_left_open.json`, `exposed_copper_door_top_left.json`, `exposed_copper_door_top_right_open.json`, `exposed_copper_door_top_right.json`, `exposed_copper_trapdoor_bottom.json`, `exposed_copper_trapdoor_open.json`, `exposed_copper_trapdoor_top.json`
- `iron_door_bottom_left_open.json`, `iron_door_bottom_left.json`, `iron_door_bottom_right_open.json`, `iron_door_bottom_right.json`, `iron_door_top_left_open.json`, `iron_door_top_left.json`, `iron_door_top_right_open.json`, `iron_door_top_right.json`
- `iron_trapdoor_bottom.json`, `iron_trapdoor_open.json`, `iron_trapdoor_top.json`, `jungle_door_bottom_left_open.json`, `jungle_door_bottom_left.json`, `jungle_door_bottom_right_open.json`, `jungle_door_bottom_right.json`, `jungle_door_top_left_open.json`
- `jungle_door_top_left.json`, `jungle_door_top_right_open.json`, `jungle_door_top_right.json`, `jungle_fence_gate_open.json`, `jungle_fence_gate_wall_open.json`, `jungle_fence_gate_wall.json`, `jungle_fence_gate.json`, `jungle_trapdoor_bottom.json`
- `jungle_trapdoor_open.json`, `jungle_trapdoor_top.json`, `mangrove_door_bottom_left_open.json`, `mangrove_door_bottom_left.json`, `mangrove_door_bottom_right_open.json`, `mangrove_door_bottom_right.json`, `mangrove_door_top_left_open.json`, `mangrove_door_top_left.json`
- `mangrove_door_top_right_open.json`, `mangrove_door_top_right.json`, `mangrove_fence_gate_open.json`, `mangrove_fence_gate_wall_open.json`, `mangrove_fence_gate_wall.json`, `mangrove_fence_gate.json`, `mangrove_trapdoor_bottom.json`, `mangrove_trapdoor_open.json`
- `mangrove_trapdoor_top.json`, `oak_door_bottom_left_open.json`, `oak_door_bottom_left.json`, `oak_door_bottom_right_open.json`, `oak_door_bottom_right.json`, `oak_door_top_left_open.json`, `oak_door_top_left.json`, `oak_door_top_right_open.json`
- `oak_door_top_right.json`, `oak_fence_gate_open.json`, `oak_fence_gate_wall_open.json`, `oak_fence_gate_wall.json`, `oak_fence_gate.json`, `oak_trapdoor_bottom.json`, `oak_trapdoor_open.json`, `oak_trapdoor_top.json`
- `oxidized_copper_door_bottom_left_open.json`, `oxidized_copper_door_bottom_left.json`, `oxidized_copper_door_bottom_right_open.json`, `oxidized_copper_door_bottom_right.json`, `oxidized_copper_door_top_left_open.json`, `oxidized_copper_door_top_left.json`, `oxidized_copper_door_top_right_open.json`, `oxidized_copper_door_top_right.json`
- `oxidized_copper_trapdoor_bottom.json`, `oxidized_copper_trapdoor_open.json`, `oxidized_copper_trapdoor_top.json`, `pale_oak_door_bottom_left_open.json`, `pale_oak_door_bottom_left.json`, `pale_oak_door_bottom_right_open.json`, `pale_oak_door_bottom_right.json`, `pale_oak_door_top_left_open.json`
- `pale_oak_door_top_left.json`, `pale_oak_door_top_right_open.json`, `pale_oak_door_top_right.json`, `pale_oak_fence_gate_open.json`, `pale_oak_fence_gate_wall_open.json`, `pale_oak_fence_gate_wall.json`, `pale_oak_fence_gate.json`, `pale_oak_trapdoor_bottom.json`
- `pale_oak_trapdoor_open.json`, `pale_oak_trapdoor_top.json`, `spruce_door_bottom_left_open.json`, `spruce_door_bottom_left.json`, `spruce_door_bottom_right_open.json`, `spruce_door_bottom_right.json`, `spruce_door_top_left_open.json`, `spruce_door_top_left.json`
- `spruce_door_top_right_open.json`, `spruce_door_top_right.json`, `spruce_fence_gate_open.json`, `spruce_fence_gate_wall_open.json`, `spruce_fence_gate_wall.json`, `spruce_fence_gate.json`, `spruce_trapdoor_bottom.json`, `spruce_trapdoor_open.json`
- `spruce_trapdoor_top.json`, `template_custom_fence_gate_open.json`, `template_custom_fence_gate_wall_open.json`, `template_custom_fence_gate_wall.json`, `template_custom_fence_gate.json`, `template_fence_gate_open.json`, `template_fence_gate_wall_open.json`, `template_fence_gate_wall.json`
- `template_fence_gate.json`, `template_orientable_trapdoor_bottom.json`, `template_orientable_trapdoor_open.json`, `template_orientable_trapdoor_top.json`, `template_trapdoor_bottom.json`, `template_trapdoor_open.json`, `template_trapdoor_top.json`, `warped_door_bottom_left_open.json`
- `warped_door_bottom_left.json`, `warped_door_bottom_right_open.json`, `warped_door_bottom_right.json`, `warped_door_top_left_open.json`, `warped_door_top_left.json`, `warped_door_top_right_open.json`, `warped_door_top_right.json`, `warped_fence_gate_open.json`
- `warped_fence_gate_wall_open.json`, `warped_fence_gate_wall.json`, `warped_fence_gate.json`, `warped_trapdoor_bottom.json`, `warped_trapdoor_open.json`, `warped_trapdoor_top.json`, `weathered_copper_door_bottom_left_open.json`, `weathered_copper_door_bottom_left.json`
- `weathered_copper_door_bottom_right_open.json`, `weathered_copper_door_bottom_right.json`, `weathered_copper_door_top_left_open.json`, `weathered_copper_door_top_left.json`, `weathered_copper_door_top_right_open.json`, `weathered_copper_door_top_right.json`, `weathered_copper_trapdoor_bottom.json`, `weathered_copper_trapdoor_open.json`
- `weathered_copper_trapdoor_top.json`

### 06. 계단·반블록·형상 변형 — 284개 (P2)

- `acacia_slab_top.json`, `acacia_slab.json`, `acacia_stairs_inner.json`, `acacia_stairs_outer.json`, `acacia_stairs.json`, `andesite_slab_top.json`, `andesite_slab.json`, `andesite_stairs_inner.json`
- `andesite_stairs_outer.json`, `andesite_stairs.json`, `bamboo_mosaic_slab_top.json`, `bamboo_mosaic_slab.json`, `bamboo_mosaic_stairs_inner.json`, `bamboo_mosaic_stairs_outer.json`, `bamboo_mosaic_stairs.json`, `bamboo_slab_top.json`
- `bamboo_slab.json`, `bamboo_stairs_inner.json`, `bamboo_stairs_outer.json`, `bamboo_stairs.json`, `birch_slab_top.json`, `birch_slab.json`, `birch_stairs_inner.json`, `birch_stairs_outer.json`
- `birch_stairs.json`, `blackstone_slab_top.json`, `blackstone_slab.json`, `blackstone_stairs_inner.json`, `blackstone_stairs_outer.json`, `blackstone_stairs.json`, `brick_slab_top.json`, `brick_slab.json`
- `brick_stairs_inner.json`, `brick_stairs_outer.json`, `brick_stairs.json`, `cherry_slab_top.json`, `cherry_slab.json`, `cherry_stairs_inner.json`, `cherry_stairs_outer.json`, `cherry_stairs.json`
- `cobbled_deepslate_slab_top.json`, `cobbled_deepslate_slab.json`, `cobbled_deepslate_stairs_inner.json`, `cobbled_deepslate_stairs_outer.json`, `cobbled_deepslate_stairs.json`, `cobblestone_slab_top.json`, `cobblestone_slab.json`, `cobblestone_stairs_inner.json`
- `cobblestone_stairs_outer.json`, `cobblestone_stairs.json`, `crimson_slab_top.json`, `crimson_slab.json`, `crimson_stairs_inner.json`, `crimson_stairs_outer.json`, `crimson_stairs.json`, `cut_copper_slab_top.json`
- `cut_copper_slab.json`, `cut_copper_stairs_inner.json`, `cut_copper_stairs_outer.json`, `cut_copper_stairs.json`, `cut_red_sandstone_slab_top.json`, `cut_red_sandstone_slab.json`, `cut_sandstone_slab_top.json`, `cut_sandstone_slab.json`
- `dark_oak_slab_top.json`, `dark_oak_slab.json`, `dark_oak_stairs_inner.json`, `dark_oak_stairs_outer.json`, `dark_oak_stairs.json`, `dark_prismarine_slab_top.json`, `dark_prismarine_slab.json`, `dark_prismarine_stairs_inner.json`
- `dark_prismarine_stairs_outer.json`, `dark_prismarine_stairs.json`, `deepslate_brick_slab_top.json`, `deepslate_brick_slab.json`, `deepslate_brick_stairs_inner.json`, `deepslate_brick_stairs_outer.json`, `deepslate_brick_stairs.json`, `deepslate_tile_slab_top.json`
- `deepslate_tile_slab.json`, `deepslate_tile_stairs_inner.json`, `deepslate_tile_stairs_outer.json`, `deepslate_tile_stairs.json`, `diorite_slab_top.json`, `diorite_slab.json`, `diorite_stairs_inner.json`, `diorite_stairs_outer.json`
- `diorite_stairs.json`, `end_stone_brick_slab_top.json`, `end_stone_brick_slab.json`, `end_stone_brick_stairs_inner.json`, `end_stone_brick_stairs_outer.json`, `end_stone_brick_stairs.json`, `exposed_cut_copper_slab_top.json`, `exposed_cut_copper_slab.json`
- `exposed_cut_copper_stairs_inner.json`, `exposed_cut_copper_stairs_outer.json`, `exposed_cut_copper_stairs.json`, `granite_slab_top.json`, `granite_slab.json`, `granite_stairs_inner.json`, `granite_stairs_outer.json`, `granite_stairs.json`
- `inner_stairs.json`, `jungle_slab_top.json`, `jungle_slab.json`, `jungle_stairs_inner.json`, `jungle_stairs_outer.json`, `jungle_stairs.json`, `mangrove_slab_top.json`, `mangrove_slab.json`
- `mangrove_stairs_inner.json`, `mangrove_stairs_outer.json`, `mangrove_stairs.json`, `mossy_cobblestone_slab_top.json`, `mossy_cobblestone_slab.json`, `mossy_cobblestone_stairs_inner.json`, `mossy_cobblestone_stairs_outer.json`, `mossy_cobblestone_stairs.json`
- `mossy_stone_brick_slab_top.json`, `mossy_stone_brick_slab.json`, `mossy_stone_brick_stairs_inner.json`, `mossy_stone_brick_stairs_outer.json`, `mossy_stone_brick_stairs.json`, `mud_brick_slab_top.json`, `mud_brick_slab.json`, `mud_brick_stairs_inner.json`
- `mud_brick_stairs_outer.json`, `mud_brick_stairs.json`, `nether_brick_slab_top.json`, `nether_brick_slab.json`, `nether_brick_stairs_inner.json`, `nether_brick_stairs_outer.json`, `nether_brick_stairs.json`, `oak_slab_top.json`
- `oak_slab.json`, `oak_stairs_inner.json`, `oak_stairs_outer.json`, `oak_stairs.json`, `outer_stairs.json`, `oxidized_cut_copper_slab_top.json`, `oxidized_cut_copper_slab.json`, `oxidized_cut_copper_stairs_inner.json`
- `oxidized_cut_copper_stairs_outer.json`, `oxidized_cut_copper_stairs.json`, `pale_oak_slab_top.json`, `pale_oak_slab.json`, `pale_oak_stairs_inner.json`, `pale_oak_stairs_outer.json`, `pale_oak_stairs.json`, `petrified_oak_slab_top.json`
- `petrified_oak_slab.json`, `polished_andesite_slab_top.json`, `polished_andesite_slab.json`, `polished_andesite_stairs_inner.json`, `polished_andesite_stairs_outer.json`, `polished_andesite_stairs.json`, `polished_blackstone_brick_slab_top.json`, `polished_blackstone_brick_slab.json`
- `polished_blackstone_brick_stairs_inner.json`, `polished_blackstone_brick_stairs_outer.json`, `polished_blackstone_brick_stairs.json`, `polished_blackstone_slab_top.json`, `polished_blackstone_slab.json`, `polished_blackstone_stairs_inner.json`, `polished_blackstone_stairs_outer.json`, `polished_blackstone_stairs.json`
- `polished_deepslate_slab_top.json`, `polished_deepslate_slab.json`, `polished_deepslate_stairs_inner.json`, `polished_deepslate_stairs_outer.json`, `polished_deepslate_stairs.json`, `polished_diorite_slab_top.json`, `polished_diorite_slab.json`, `polished_diorite_stairs_inner.json`
- `polished_diorite_stairs_outer.json`, `polished_diorite_stairs.json`, `polished_granite_slab_top.json`, `polished_granite_slab.json`, `polished_granite_stairs_inner.json`, `polished_granite_stairs_outer.json`, `polished_granite_stairs.json`, `polished_tuff_slab_top.json`
- `polished_tuff_slab.json`, `polished_tuff_stairs_inner.json`, `polished_tuff_stairs_outer.json`, `polished_tuff_stairs.json`, `prismarine_brick_slab_top.json`, `prismarine_brick_slab.json`, `prismarine_brick_stairs_inner.json`, `prismarine_brick_stairs_outer.json`
- `prismarine_brick_stairs.json`, `prismarine_slab_top.json`, `prismarine_slab.json`, `prismarine_stairs_inner.json`, `prismarine_stairs_outer.json`, `prismarine_stairs.json`, `purpur_slab_top.json`, `purpur_slab.json`
- `purpur_stairs_inner.json`, `purpur_stairs_outer.json`, `purpur_stairs.json`, `quartz_slab_top.json`, `quartz_slab.json`, `quartz_stairs_inner.json`, `quartz_stairs_outer.json`, `quartz_stairs.json`
- `red_nether_brick_slab_top.json`, `red_nether_brick_slab.json`, `red_nether_brick_stairs_inner.json`, `red_nether_brick_stairs_outer.json`, `red_nether_brick_stairs.json`, `red_sandstone_slab_top.json`, `red_sandstone_slab.json`, `red_sandstone_stairs_inner.json`
- `red_sandstone_stairs_outer.json`, `red_sandstone_stairs.json`, `resin_brick_slab_top.json`, `resin_brick_slab.json`, `resin_brick_stairs_inner.json`, `resin_brick_stairs_outer.json`, `resin_brick_stairs.json`, `sandstone_slab_top.json`
- `sandstone_slab.json`, `sandstone_stairs_inner.json`, `sandstone_stairs_outer.json`, `sandstone_stairs.json`, `slab_top.json`, `slab.json`, `smooth_quartz_slab_top.json`, `smooth_quartz_slab.json`
- `smooth_quartz_stairs_inner.json`, `smooth_quartz_stairs_outer.json`, `smooth_quartz_stairs.json`, `smooth_red_sandstone_slab_top.json`, `smooth_red_sandstone_slab.json`, `smooth_red_sandstone_stairs_inner.json`, `smooth_red_sandstone_stairs_outer.json`, `smooth_red_sandstone_stairs.json`
- `smooth_sandstone_slab_top.json`, `smooth_sandstone_slab.json`, `smooth_sandstone_stairs_inner.json`, `smooth_sandstone_stairs_outer.json`, `smooth_sandstone_stairs.json`, `smooth_stone_slab_double.json`, `smooth_stone_slab_top.json`, `smooth_stone_slab.json`
- `spruce_slab_top.json`, `spruce_slab.json`, `spruce_stairs_inner.json`, `spruce_stairs_outer.json`, `spruce_stairs.json`, `stairs.json`, `stone_brick_slab_top.json`, `stone_brick_slab.json`
- `stone_brick_stairs_inner.json`, `stone_brick_stairs_outer.json`, `stone_brick_stairs.json`, `stone_slab_top.json`, `stone_slab.json`, `stone_stairs_inner.json`, `stone_stairs_outer.json`, `stone_stairs.json`
- `tuff_brick_slab_top.json`, `tuff_brick_slab.json`, `tuff_brick_stairs_inner.json`, `tuff_brick_stairs_outer.json`, `tuff_brick_stairs.json`, `tuff_slab_top.json`, `tuff_slab.json`, `tuff_stairs_inner.json`
- `tuff_stairs_outer.json`, `tuff_stairs.json`, `warped_slab_top.json`, `warped_slab.json`, `warped_stairs_inner.json`, `warped_stairs_outer.json`, `warped_stairs.json`, `weathered_cut_copper_slab_top.json`
- `weathered_cut_copper_slab.json`, `weathered_cut_copper_stairs_inner.json`, `weathered_cut_copper_stairs_outer.json`, `weathered_cut_copper_stairs.json`

### 07. 울타리·담장·유리판·난간·연결 — 277개 (P2)

- `acacia_fence_inventory.json`, `acacia_fence_post.json`, `acacia_fence_side.json`, `andesite_wall_inventory.json`, `andesite_wall_post.json`, `andesite_wall_side_tall.json`, `andesite_wall_side.json`, `bamboo_fence_inventory.json`
- `bamboo_fence_post.json`, `bamboo_fence_side_east.json`, `bamboo_fence_side_north.json`, `bamboo_fence_side_south.json`, `bamboo_fence_side_west.json`, `birch_fence_inventory.json`, `birch_fence_post.json`, `birch_fence_side.json`
- `black_stained_glass_pane_noside_alt.json`, `black_stained_glass_pane_noside.json`, `black_stained_glass_pane_post.json`, `black_stained_glass_pane_side_alt.json`, `black_stained_glass_pane_side.json`, `blackstone_wall_inventory.json`, `blackstone_wall_post.json`, `blackstone_wall_side_tall.json`
- `blackstone_wall_side.json`, `blue_stained_glass_pane_noside_alt.json`, `blue_stained_glass_pane_noside.json`, `blue_stained_glass_pane_post.json`, `blue_stained_glass_pane_side_alt.json`, `blue_stained_glass_pane_side.json`, `brain_coral_wall_fan.json`, `brick_wall_inventory.json`
- `brick_wall_post.json`, `brick_wall_side_tall.json`, `brick_wall_side.json`, `brown_stained_glass_pane_noside_alt.json`, `brown_stained_glass_pane_noside.json`, `brown_stained_glass_pane_post.json`, `brown_stained_glass_pane_side_alt.json`, `brown_stained_glass_pane_side.json`
- `bubble_coral_wall_fan.json`, `chain_command_block_conditional.json`, `chain_command_block.json`, `cherry_fence_inventory.json`, `cherry_fence_post.json`, `cherry_fence_side.json`, `cobbled_deepslate_wall_inventory.json`, `cobbled_deepslate_wall_post.json`
- `cobbled_deepslate_wall_side_tall.json`, `cobbled_deepslate_wall_side.json`, `cobblestone_wall_inventory.json`, `cobblestone_wall_post.json`, `cobblestone_wall_side_tall.json`, `cobblestone_wall_side.json`, `copper_chain.json`, `coral_wall_fan.json`
- `crimson_fence_inventory.json`, `crimson_fence_post.json`, `crimson_fence_side.json`, `custom_fence_inventory.json`, `custom_fence_post.json`, `custom_fence_side_east.json`, `custom_fence_side_north.json`, `custom_fence_side_south.json`
- `custom_fence_side_west.json`, `cyan_stained_glass_pane_noside_alt.json`, `cyan_stained_glass_pane_noside.json`, `cyan_stained_glass_pane_post.json`, `cyan_stained_glass_pane_side_alt.json`, `cyan_stained_glass_pane_side.json`, `dark_oak_fence_inventory.json`, `dark_oak_fence_post.json`
- `dark_oak_fence_side.json`, `dead_brain_coral_wall_fan.json`, `dead_bubble_coral_wall_fan.json`, `dead_fire_coral_wall_fan.json`, `dead_horn_coral_wall_fan.json`, `dead_tube_coral_wall_fan.json`, `deepslate_brick_wall_inventory.json`, `deepslate_brick_wall_post.json`
- `deepslate_brick_wall_side_tall.json`, `deepslate_brick_wall_side.json`, `deepslate_tile_wall_inventory.json`, `deepslate_tile_wall_post.json`, `deepslate_tile_wall_side_tall.json`, `deepslate_tile_wall_side.json`, `diorite_wall_inventory.json`, `diorite_wall_post.json`
- `diorite_wall_side_tall.json`, `diorite_wall_side.json`, `end_stone_brick_wall_inventory.json`, `end_stone_brick_wall_post.json`, `end_stone_brick_wall_side_tall.json`, `end_stone_brick_wall_side.json`, `exposed_copper_chain.json`, `fence_inventory.json`
- `fence_post.json`, `fence_side.json`, `fire_coral_wall_fan.json`, `glass_pane_noside_alt.json`, `glass_pane_noside.json`, `glass_pane_post.json`, `glass_pane_side_alt.json`, `glass_pane_side.json`
- `granite_wall_inventory.json`, `granite_wall_post.json`, `granite_wall_side_tall.json`, `granite_wall_side.json`, `gray_stained_glass_pane_noside_alt.json`, `gray_stained_glass_pane_noside.json`, `gray_stained_glass_pane_post.json`, `gray_stained_glass_pane_side_alt.json`
- `gray_stained_glass_pane_side.json`, `green_stained_glass_pane_noside_alt.json`, `green_stained_glass_pane_noside.json`, `green_stained_glass_pane_post.json`, `green_stained_glass_pane_side_alt.json`, `green_stained_glass_pane_side.json`, `horn_coral_wall_fan.json`, `iron_bars_cap_alt.json`
- `iron_bars_cap.json`, `iron_bars_post_ends.json`, `iron_bars_post.json`, `iron_bars_side_alt.json`, `iron_bars_side.json`, `iron_chain.json`, `jungle_fence_inventory.json`, `jungle_fence_post.json`
- `jungle_fence_side.json`, `ladder.json`, `light_blue_stained_glass_pane_noside_alt.json`, `light_blue_stained_glass_pane_noside.json`, `light_blue_stained_glass_pane_post.json`, `light_blue_stained_glass_pane_side_alt.json`, `light_blue_stained_glass_pane_side.json`, `light_gray_stained_glass_pane_noside_alt.json`
- `light_gray_stained_glass_pane_noside.json`, `light_gray_stained_glass_pane_post.json`, `light_gray_stained_glass_pane_side_alt.json`, `light_gray_stained_glass_pane_side.json`, `lime_stained_glass_pane_noside_alt.json`, `lime_stained_glass_pane_noside.json`, `lime_stained_glass_pane_post.json`, `lime_stained_glass_pane_side_alt.json`
- `lime_stained_glass_pane_side.json`, `magenta_stained_glass_pane_noside_alt.json`, `magenta_stained_glass_pane_noside.json`, `magenta_stained_glass_pane_post.json`, `magenta_stained_glass_pane_side_alt.json`, `magenta_stained_glass_pane_side.json`, `mangrove_fence_inventory.json`, `mangrove_fence_post.json`
- `mangrove_fence_side.json`, `mossy_cobblestone_wall_inventory.json`, `mossy_cobblestone_wall_post.json`, `mossy_cobblestone_wall_side_tall.json`, `mossy_cobblestone_wall_side.json`, `mossy_stone_brick_wall_inventory.json`, `mossy_stone_brick_wall_post.json`, `mossy_stone_brick_wall_side_tall.json`
- `mossy_stone_brick_wall_side.json`, `mud_brick_wall_inventory.json`, `mud_brick_wall_post.json`, `mud_brick_wall_side_tall.json`, `mud_brick_wall_side.json`, `nether_brick_fence_inventory.json`, `nether_brick_fence_post.json`, `nether_brick_fence_side.json`
- `nether_brick_wall_inventory.json`, `nether_brick_wall_post.json`, `nether_brick_wall_side_tall.json`, `nether_brick_wall_side.json`, `oak_fence_inventory.json`, `oak_fence_post.json`, `oak_fence_side.json`, `orange_stained_glass_pane_noside_alt.json`
- `orange_stained_glass_pane_noside.json`, `orange_stained_glass_pane_post.json`, `orange_stained_glass_pane_side_alt.json`, `orange_stained_glass_pane_side.json`, `oxidized_copper_chain.json`, `pale_oak_fence_inventory.json`, `pale_oak_fence_post.json`, `pale_oak_fence_side.json`
- `pink_stained_glass_pane_noside_alt.json`, `pink_stained_glass_pane_noside.json`, `pink_stained_glass_pane_post.json`, `pink_stained_glass_pane_side_alt.json`, `pink_stained_glass_pane_side.json`, `polished_blackstone_brick_wall_inventory.json`, `polished_blackstone_brick_wall_post.json`, `polished_blackstone_brick_wall_side_tall.json`
- `polished_blackstone_brick_wall_side.json`, `polished_blackstone_wall_inventory.json`, `polished_blackstone_wall_post.json`, `polished_blackstone_wall_side_tall.json`, `polished_blackstone_wall_side.json`, `polished_deepslate_wall_inventory.json`, `polished_deepslate_wall_post.json`, `polished_deepslate_wall_side_tall.json`
- `polished_deepslate_wall_side.json`, `polished_tuff_wall_inventory.json`, `polished_tuff_wall_post.json`, `polished_tuff_wall_side_tall.json`, `polished_tuff_wall_side.json`, `prismarine_wall_inventory.json`, `prismarine_wall_post.json`, `prismarine_wall_side_tall.json`
- `prismarine_wall_side.json`, `purple_stained_glass_pane_noside_alt.json`, `purple_stained_glass_pane_noside.json`, `purple_stained_glass_pane_post.json`, `purple_stained_glass_pane_side_alt.json`, `purple_stained_glass_pane_side.json`, `red_nether_brick_wall_inventory.json`, `red_nether_brick_wall_post.json`
- `red_nether_brick_wall_side_tall.json`, `red_nether_brick_wall_side.json`, `red_sandstone_wall_inventory.json`, `red_sandstone_wall_post.json`, `red_sandstone_wall_side_tall.json`, `red_sandstone_wall_side.json`, `red_stained_glass_pane_noside_alt.json`, `red_stained_glass_pane_noside.json`
- `red_stained_glass_pane_post.json`, `red_stained_glass_pane_side_alt.json`, `red_stained_glass_pane_side.json`, `resin_brick_wall_inventory.json`, `resin_brick_wall_post.json`, `resin_brick_wall_side_tall.json`, `resin_brick_wall_side.json`, `sandstone_wall_inventory.json`
- `sandstone_wall_post.json`, `sandstone_wall_side_tall.json`, `sandstone_wall_side.json`, `scaffolding_stable.json`, `scaffolding_unstable.json`, `spruce_fence_inventory.json`, `spruce_fence_post.json`, `spruce_fence_side.json`
- `stone_brick_wall_inventory.json`, `stone_brick_wall_post.json`, `stone_brick_wall_side_tall.json`, `stone_brick_wall_side.json`, `template_chain.json`, `template_glass_pane_noside_alt.json`, `template_glass_pane_noside.json`, `template_glass_pane_post.json`
- `template_glass_pane_side_alt.json`, `template_glass_pane_side.json`, `template_wall_post.json`, `template_wall_side_tall.json`, `template_wall_side.json`, `tube_coral_wall_fan.json`, `tuff_brick_wall_inventory.json`, `tuff_brick_wall_post.json`
- `tuff_brick_wall_side_tall.json`, `tuff_brick_wall_side.json`, `tuff_wall_inventory.json`, `tuff_wall_post.json`, `tuff_wall_side_tall.json`, `tuff_wall_side.json`, `wall_inventory.json`, `warped_fence_inventory.json`
- `warped_fence_post.json`, `warped_fence_side.json`, `weathered_copper_chain.json`, `white_stained_glass_pane_noside_alt.json`, `white_stained_glass_pane_noside.json`, `white_stained_glass_pane_post.json`, `white_stained_glass_pane_side_alt.json`, `white_stained_glass_pane_side.json`
- `yellow_stained_glass_pane_noside_alt.json`, `yellow_stained_glass_pane_noside.json`, `yellow_stained_glass_pane_post.json`, `yellow_stained_glass_pane_side_alt.json`, `yellow_stained_glass_pane_side.json`

### 08. 레드스톤·기계·스위치·레일 — 198개 (P2)

- `acacia_button_inventory.json`, `acacia_button_pressed.json`, `acacia_button.json`, `acacia_pressure_plate_down.json`, `acacia_pressure_plate.json`, `activator_rail_on_raised_ne.json`, `activator_rail_on_raised_sw.json`, `activator_rail_on.json`
- `activator_rail_raised_ne.json`, `activator_rail_raised_sw.json`, `activator_rail.json`, `bamboo_button_inventory.json`, `bamboo_button_pressed.json`, `bamboo_button.json`, `bamboo_pressure_plate_down.json`, `bamboo_pressure_plate.json`
- `birch_button_inventory.json`, `birch_button_pressed.json`, `birch_button.json`, `birch_pressure_plate_down.json`, `birch_pressure_plate.json`, `button_inventory.json`, `button_pressed.json`, `button.json`
- `calibrated_sculk_sensor_active.json`, `calibrated_sculk_sensor_inactive.json`, `calibrated_sculk_sensor.json`, `cherry_button_inventory.json`, `cherry_button_pressed.json`, `cherry_button.json`, `cherry_pressure_plate_down.json`, `cherry_pressure_plate.json`
- `comparator_on_subtract.json`, `comparator_on.json`, `comparator_subtract.json`, `comparator.json`, `copper_bulb_lit_powered.json`, `copper_bulb_lit.json`, `copper_bulb_powered.json`, `copper_bulb.json`
- `crimson_button_inventory.json`, `crimson_button_pressed.json`, `crimson_button.json`, `crimson_pressure_plate_down.json`, `crimson_pressure_plate.json`, `dark_oak_button_inventory.json`, `dark_oak_button_pressed.json`, `dark_oak_button.json`
- `dark_oak_pressure_plate_down.json`, `dark_oak_pressure_plate.json`, `daylight_detector_inverted.json`, `daylight_detector.json`, `deepslate_redstone_ore.json`, `detector_rail_on_raised_ne.json`, `detector_rail_on_raised_sw.json`, `detector_rail_on.json`
- `detector_rail_raised_ne.json`, `detector_rail_raised_sw.json`, `detector_rail.json`, `dispenser_vertical.json`, `dispenser.json`, `dropper_vertical.json`, `dropper.json`, `exposed_copper_bulb_lit_powered.json`
- `exposed_copper_bulb_lit.json`, `exposed_copper_bulb_powered.json`, `exposed_copper_bulb.json`, `heavy_weighted_pressure_plate_down.json`, `heavy_weighted_pressure_plate.json`, `jigsaw.json`, `jungle_button_inventory.json`, `jungle_button_pressed.json`
- `jungle_button.json`, `jungle_pressure_plate_down.json`, `jungle_pressure_plate.json`, `lever_on.json`, `lever.json`, `light_weighted_pressure_plate_down.json`, `light_weighted_pressure_plate.json`, `mangrove_button_inventory.json`
- `mangrove_button_pressed.json`, `mangrove_button.json`, `mangrove_pressure_plate_down.json`, `mangrove_pressure_plate.json`, `moving_piston.json`, `oak_button_inventory.json`, `oak_button_pressed.json`, `oak_button.json`
- `oak_pressure_plate_down.json`, `oak_pressure_plate.json`, `observer_on.json`, `observer.json`, `oxidized_copper_bulb_lit_powered.json`, `oxidized_copper_bulb_lit.json`, `oxidized_copper_bulb_powered.json`, `oxidized_copper_bulb.json`
- `pale_oak_button_inventory.json`, `pale_oak_button_pressed.json`, `pale_oak_button.json`, `pale_oak_pressure_plate_down.json`, `pale_oak_pressure_plate.json`, `piston_base.json`, `piston_extended.json`, `piston_inventory.json`
- `piston.json`, `polished_blackstone_button_inventory.json`, `polished_blackstone_button_pressed.json`, `polished_blackstone_button.json`, `polished_blackstone_pressure_plate_down.json`, `polished_blackstone_pressure_plate.json`, `powered_rail_on_raised_ne.json`, `powered_rail_on_raised_sw.json`
- `powered_rail_on.json`, `powered_rail_raised_ne.json`, `powered_rail_raised_sw.json`, `powered_rail.json`, `pressure_plate_down.json`, `pressure_plate_up.json`, `rail_corner.json`, `rail_curved.json`
- `rail_flat.json`, `rail_raised_ne.json`, `rail_raised_sw.json`, `rail.json`, `redstone_block.json`, `redstone_dust_dot.json`, `redstone_dust_side_alt.json`, `redstone_dust_side_alt0.json`
- `redstone_dust_side_alt1.json`, `redstone_dust_side.json`, `redstone_dust_side0.json`, `redstone_dust_side1.json`, `redstone_dust_up.json`, `redstone_ore.json`, `repeater_1tick_locked.json`, `repeater_1tick_on_locked.json`
- `repeater_1tick_on.json`, `repeater_1tick.json`, `repeater_2tick_locked.json`, `repeater_2tick_on_locked.json`, `repeater_2tick_on.json`, `repeater_2tick.json`, `repeater_3tick_locked.json`, `repeater_3tick_on_locked.json`
- `repeater_3tick_on.json`, `repeater_3tick.json`, `repeater_4tick_locked.json`, `repeater_4tick_on_locked.json`, `repeater_4tick_on.json`, `repeater_4tick.json`, `resin_clump.json`, `sculk_sensor_active.json`
- `sculk_sensor_inactive.json`, `sculk_sensor.json`, `sculk_shrieker_can_summon.json`, `sculk_shrieker.json`, `spruce_button_inventory.json`, `spruce_button_pressed.json`, `spruce_button.json`, `spruce_pressure_plate_down.json`
- `spruce_pressure_plate.json`, `sticky_piston_inventory.json`, `sticky_piston.json`, `stone_button_inventory.json`, `stone_button_pressed.json`, `stone_button.json`, `stone_pressure_plate_down.json`, `stone_pressure_plate.json`
- `target.json`, `template_daylight_detector.json`, `template_piston.json`, `template_rail_raised_ne.json`, `template_rail_raised_sw.json`, `template_sculk_shrieker.json`, `tnt.json`, `tripwire_attached_n.json`
- `tripwire_attached_ne.json`, `tripwire_attached_ns.json`, `tripwire_attached_nse.json`, `tripwire_attached_nsew.json`, `tripwire_hook_attached_on.json`, `tripwire_hook_attached.json`, `tripwire_hook_on.json`, `tripwire_hook.json`
- `tripwire_n.json`, `tripwire_ne.json`, `tripwire_ns.json`, `tripwire_nse.json`, `tripwire_nsew.json`, `warped_button_inventory.json`, `warped_button_pressed.json`, `warped_button.json`
- `warped_pressure_plate_down.json`, `warped_pressure_plate.json`, `weathered_copper_bulb_lit_powered.json`, `weathered_copper_bulb_lit.json`, `weathered_copper_bulb_powered.json`, `weathered_copper_bulb.json`

### 09. 식물·작물·잎·꽃·버섯·산호 — 241개 (P3)

- `acacia_leaves.json`, `acacia_sapling.json`, `allium.json`, `attached_melon_stem.json`, `attached_pumpkin_stem.json`, `azalea_leaves.json`, `azalea.json`, `bamboo_block_x.json`
- `bamboo_block_y.json`, `bamboo_block_z.json`, `bamboo_block.json`, `bamboo_large_leaves.json`, `bamboo_mosaic.json`, `bamboo_planks.json`, `bamboo_sapling.json`, `bamboo_small_leaves.json`
- `bamboo1_age0.json`, `bamboo1_age1.json`, `bamboo2_age0.json`, `bamboo2_age1.json`, `bamboo3_age0.json`, `bamboo3_age1.json`, `bamboo4_age0.json`, `bamboo4_age1.json`
- `beetroots_stage0.json`, `beetroots_stage1.json`, `beetroots_stage2.json`, `beetroots_stage3.json`, `big_dripleaf_full_tilt.json`, `big_dripleaf_partial_tilt.json`, `big_dripleaf_stem.json`, `big_dripleaf.json`
- `birch_leaves.json`, `birch_sapling.json`, `blue_orchid.json`, `brain_coral_block.json`, `brain_coral_fan.json`, `brain_coral.json`, `brown_mushroom_block_inventory.json`, `brown_mushroom_block.json`
- `brown_mushroom.json`, `bubble_coral_block.json`, `bubble_coral_fan.json`, `bubble_coral.json`, `bush.json`, `cactus_flower.json`, `cactus.json`, `carved_pumpkin.json`
- `cherry_leaves.json`, `cherry_sapling.json`, `chorus_flower_dead.json`, `chorus_flower.json`, `closed_eyeblossom.json`, `cocoa_stage0.json`, `cocoa_stage1.json`, `cocoa_stage2.json`
- `coral_fan.json`, `cornflower.json`, `crimson_fungus.json`, `crimson_roots.json`, `crimson_stem.json`, `dandelion.json`, `dark_oak_leaves.json`, `dark_oak_sapling.json`
- `dead_brain_coral_block.json`, `dead_brain_coral_fan.json`, `dead_brain_coral.json`, `dead_bubble_coral_block.json`, `dead_bubble_coral_fan.json`, `dead_bubble_coral.json`, `dead_bush.json`, `dead_fire_coral_block.json`
- `dead_fire_coral_fan.json`, `dead_fire_coral.json`, `dead_horn_coral_block.json`, `dead_horn_coral_fan.json`, `dead_horn_coral.json`, `dead_tube_coral_block.json`, `dead_tube_coral_fan.json`, `dead_tube_coral.json`
- `dried_kelp_block.json`, `fern.json`, `fire_coral_block.json`, `fire_coral_fan.json`, `fire_coral.json`, `firefly_bush.json`, `flowering_azalea_leaves.json`, `flowering_azalea.json`
- `glow_lichen.json`, `grass_block_snow.json`, `grass_block.json`, `hanging_roots.json`, `horn_coral_block.json`, `horn_coral_fan.json`, `horn_coral.json`, `jungle_leaves.json`
- `jungle_sapling.json`, `kelp_plant.json`, `kelp.json`, `large_fern_bottom.json`, `large_fern_top.json`, `leaf_litter_1.json`, `leaf_litter_2.json`, `leaf_litter_3.json`
- `leaf_litter_4.json`, `leaves.json`, `lilac_bottom.json`, `lilac_top.json`, `lily_of_the_valley.json`, `lily_pad.json`, `mangrove_leaves.json`, `mangrove_propagule_hanging_0.json`
- `mangrove_propagule_hanging_1.json`, `mangrove_propagule_hanging_2.json`, `mangrove_propagule_hanging_3.json`, `mangrove_propagule_hanging_4.json`, `mangrove_propagule.json`, `mangrove_roots.json`, `melon_stem_stage0.json`, `melon_stem_stage1.json`
- `melon_stem_stage2.json`, `melon_stem_stage3.json`, `melon_stem_stage4.json`, `melon_stem_stage5.json`, `melon_stem_stage6.json`, `melon_stem_stage7.json`, `melon.json`, `moss_block.json`
- `muddy_mangrove_roots.json`, `mushroom_block_inside.json`, `mushroom_stem_inventory.json`, `mushroom_stem.json`, `nether_sprouts.json`, `nether_wart_block.json`, `nether_wart_stage0.json`, `nether_wart_stage1.json`
- `nether_wart_stage2.json`, `oak_leaves.json`, `oak_sapling.json`, `open_eyeblossom.json`, `orange_tulip.json`, `oxeye_daisy.json`, `pale_hanging_moss_tip.json`, `pale_hanging_moss.json`
- `pale_moss_block.json`, `pale_oak_leaves.json`, `pale_oak_sapling.json`, `peony_bottom.json`, `peony_top.json`, `pink_petals_1.json`, `pink_petals_2.json`, `pink_petals_3.json`
- `pink_petals_4.json`, `pink_tulip.json`, `pitcher_crop_bottom_stage_0.json`, `pitcher_crop_bottom_stage_1.json`, `pitcher_crop_bottom_stage_2.json`, `pitcher_crop_bottom_stage_3.json`, `pitcher_crop_bottom_stage_4.json`, `pitcher_crop_top_stage_0.json`
- `pitcher_crop_top_stage_1.json`, `pitcher_crop_top_stage_2.json`, `pitcher_crop_top_stage_3.json`, `pitcher_crop_top_stage_4.json`, `pitcher_plant_bottom.json`, `pitcher_plant_top.json`, `poppy.json`, `pumpkin_stem_stage0.json`
- `pumpkin_stem_stage1.json`, `pumpkin_stem_stage2.json`, `pumpkin_stem_stage3.json`, `pumpkin_stem_stage4.json`, `pumpkin_stem_stage5.json`, `pumpkin_stem_stage6.json`, `pumpkin_stem_stage7.json`, `pumpkin.json`
- `red_mushroom_block_inventory.json`, `red_mushroom_block.json`, `red_mushroom.json`, `red_tulip.json`, `rose_bush_bottom.json`, `rose_bush_top.json`, `seagrass.json`, `short_dry_grass.json`
- `short_grass.json`, `small_dripleaf_bottom.json`, `small_dripleaf_top.json`, `sniffer_egg_not_cracked.json`, `sniffer_egg_slightly_cracked.json`, `sniffer_egg_very_cracked.json`, `sniffer_egg.json`, `spruce_leaves.json`
- `spruce_sapling.json`, `stem_fruit.json`, `stem_growth0.json`, `stem_growth1.json`, `stem_growth2.json`, `stem_growth3.json`, `stem_growth4.json`, `stem_growth5.json`
- `stem_growth6.json`, `stem_growth7.json`, `stripped_bamboo_block_x.json`, `stripped_bamboo_block_y.json`, `stripped_bamboo_block_z.json`, `stripped_bamboo_block.json`, `stripped_crimson_stem.json`, `stripped_warped_stem.json`
- `sugar_cane.json`, `sweet_berry_bush_stage0.json`, `sweet_berry_bush_stage1.json`, `sweet_berry_bush_stage2.json`, `sweet_berry_bush_stage3.json`, `tall_dry_grass.json`, `tall_grass_bottom.json`, `tall_grass_top.json`
- `tall_seagrass_bottom.json`, `tall_seagrass_top.json`, `template_azalea.json`, `template_chorus_flower.json`, `template_leaf_litter_1.json`, `template_leaf_litter_2.json`, `template_leaf_litter_3.json`, `template_leaf_litter_4.json`
- `template_seagrass.json`, `tube_coral_block.json`, `tube_coral_fan.json`, `tube_coral.json`, `vine.json`, `warped_fungus.json`, `warped_roots.json`, `warped_stem.json`
- `wheat_stage0.json`, `wheat_stage1.json`, `wheat_stage2.json`, `wheat_stage3.json`, `wheat_stage4.json`, `wheat_stage5.json`, `wheat_stage6.json`, `wheat_stage7.json`
- `white_tulip.json`

### 10. 유체·포털·불·자연 특수 표현 — 38개 (P3)

- `blue_ice.json`, `end_gateway.json`, `end_portal_frame_filled.json`, `end_portal_frame.json`, `end_portal.json`, `fire_floor0.json`, `fire_floor1.json`, `fire_side_alt0.json`
- `fire_side_alt1.json`, `fire_side0.json`, `fire_side1.json`, `fire_up_alt0.json`, `fire_up_alt1.json`, `fire_up0.json`, `fire_up1.json`, `frogspawn.json`
- `frosted_ice_0.json`, `frosted_ice_1.json`, `frosted_ice_2.json`, `frosted_ice_3.json`, `ice.json`, `lava.json`, `nether_portal_ew.json`, `nether_portal_ns.json`
- `packed_ice.json`, `powder_snow.json`, `soul_fire_floor0.json`, `soul_fire_floor1.json`, `soul_fire_side_alt0.json`, `soul_fire_side_alt1.json`, `soul_fire_side0.json`, `soul_fire_side1.json`
- `template_fire_floor.json`, `template_fire_side_alt.json`, `template_fire_side.json`, `template_fire_up_alt.json`, `template_fire_up.json`, `water.json`

### 11. 기본 재질·석재·광물·목재·색상 — 375개 (P3)

- `acacia_log_horizontal.json`, `acacia_log.json`, `acacia_planks.json`, `acacia_wood.json`, `amethyst_block.json`, `amethyst_cluster.json`, `ancient_debris.json`, `andesite.json`
- `basalt.json`, `bedrock_mirrored.json`, `bedrock.json`, `birch_log_horizontal.json`, `birch_log.json`, `birch_planks.json`, `birch_wood.json`, `black_concrete_powder.json`
- `black_concrete.json`, `black_glazed_terracotta.json`, `black_stained_glass.json`, `black_terracotta.json`, `black_wool.json`, `blackstone.json`, `block.json`, `blue_concrete_powder.json`
- `blue_concrete.json`, `blue_glazed_terracotta.json`, `blue_stained_glass.json`, `blue_terracotta.json`, `blue_wool.json`, `bone_block.json`, `brown_concrete_powder.json`, `brown_concrete.json`
- `brown_glazed_terracotta.json`, `brown_stained_glass.json`, `brown_terracotta.json`, `brown_wool.json`, `budding_amethyst.json`, `calcite.json`, `cherry_log_x.json`, `cherry_log_y.json`
- `cherry_log_z.json`, `cherry_log.json`, `cherry_planks.json`, `cherry_wood.json`, `chiseled_copper.json`, `chiseled_deepslate.json`, `chiseled_polished_blackstone.json`, `chiseled_quartz_block.json`
- `chiseled_resin_bricks.json`, `chiseled_stone_bricks.json`, `chiseled_tuff_bricks.json`, `chiseled_tuff.json`, `clay.json`, `coal_block.json`, `coal_ore.json`, `coarse_dirt.json`
- `cobbled_deepslate.json`, `cobblestone.json`, `command_block_conditional.json`, `command_block.json`, `copper_bars_cap_alt.json`, `copper_bars_cap.json`, `copper_bars_post_ends.json`, `copper_bars_post.json`
- `copper_bars_side_alt.json`, `copper_bars_side.json`, `copper_block.json`, `copper_golem_statue.json`, `copper_grate.json`, `copper_ore.json`, `cracked_deepslate_bricks.json`, `cracked_deepslate_tiles.json`
- `cracked_polished_blackstone_bricks.json`, `cracked_stone_bricks.json`, `crimson_nylium.json`, `crimson_planks.json`, `crying_obsidian.json`, `cut_copper.json`, `cyan_concrete_powder.json`, `cyan_concrete.json`
- `cyan_glazed_terracotta.json`, `cyan_stained_glass.json`, `cyan_terracotta.json`, `cyan_wool.json`, `dark_oak_log_horizontal.json`, `dark_oak_log.json`, `dark_oak_planks.json`, `dark_oak_wood.json`
- `dark_prismarine.json`, `deepslate_bricks.json`, `deepslate_coal_ore.json`, `deepslate_copper_ore.json`, `deepslate_diamond_ore.json`, `deepslate_emerald_ore.json`, `deepslate_gold_ore.json`, `deepslate_iron_ore.json`
- `deepslate_lapis_ore.json`, `deepslate_mirrored.json`, `deepslate_tiles.json`, `deepslate.json`, `diamond_block.json`, `diamond_ore.json`, `diorite.json`, `dirt_path.json`
- `dirt.json`, `dripstone_block.json`, `emerald_block.json`, `emerald_ore.json`, `end_stone_bricks.json`, `end_stone.json`, `exposed_chiseled_copper.json`, `exposed_copper_bars_cap_alt.json`
- `exposed_copper_bars_cap.json`, `exposed_copper_bars_post_ends.json`, `exposed_copper_bars_post.json`, `exposed_copper_bars_side_alt.json`, `exposed_copper_bars_side.json`, `exposed_copper_golem_statue.json`, `exposed_copper_grate.json`, `exposed_copper.json`
- `exposed_cut_copper.json`, `farmland_moist.json`, `farmland.json`, `gilded_blackstone.json`, `glass.json`, `gold_block.json`, `gold_ore.json`, `granite.json`
- `gravel.json`, `gray_concrete_powder.json`, `gray_concrete.json`, `gray_glazed_terracotta.json`, `gray_stained_glass.json`, `gray_terracotta.json`, `gray_wool.json`, `green_concrete_powder.json`
- `green_concrete.json`, `green_glazed_terracotta.json`, `green_stained_glass.json`, `green_terracotta.json`, `green_wool.json`, `hay_block_horizontal.json`, `hay_block.json`, `honey_block.json`
- `honeycomb_block.json`, `iron_block.json`, `iron_ore.json`, `jungle_log_horizontal.json`, `jungle_log.json`, `jungle_planks.json`, `jungle_wood.json`, `lapis_block.json`
- `lapis_ore.json`, `large_amethyst_bud.json`, `light_blue_concrete_powder.json`, `light_blue_concrete.json`, `light_blue_glazed_terracotta.json`, `light_blue_stained_glass.json`, `light_blue_terracotta.json`, `light_blue_wool.json`
- `light_gray_concrete_powder.json`, `light_gray_concrete.json`, `light_gray_glazed_terracotta.json`, `light_gray_stained_glass.json`, `light_gray_terracotta.json`, `light_gray_wool.json`, `lime_concrete_powder.json`, `lime_concrete.json`
- `lime_glazed_terracotta.json`, `lime_stained_glass.json`, `lime_terracotta.json`, `lime_wool.json`, `magenta_concrete_powder.json`, `magenta_concrete.json`, `magenta_glazed_terracotta.json`, `magenta_stained_glass.json`
- `magenta_terracotta.json`, `magenta_wool.json`, `magma_block.json`, `mangrove_log_horizontal.json`, `mangrove_log.json`, `mangrove_planks.json`, `mangrove_wood.json`, `medium_amethyst_bud.json`
- `mossy_cobblestone.json`, `mossy_stone_bricks.json`, `mud_bricks_north_west_mirrored.json`, `mud_bricks.json`, `mud.json`, `mycelium.json`, `nether_gold_ore.json`, `nether_quartz_ore.json`
- `netherite_block.json`, `netherrack.json`, `oak_log_horizontal.json`, `oak_log.json`, `oak_planks.json`, `oak_wood.json`, `obsidian.json`, `orange_concrete_powder.json`
- `orange_concrete.json`, `orange_glazed_terracotta.json`, `orange_stained_glass.json`, `orange_terracotta.json`, `orange_wool.json`, `oxidized_chiseled_copper.json`, `oxidized_copper_bars_cap_alt.json`, `oxidized_copper_bars_cap.json`
- `oxidized_copper_bars_post_ends.json`, `oxidized_copper_bars_post.json`, `oxidized_copper_bars_side_alt.json`, `oxidized_copper_bars_side.json`, `oxidized_copper_golem_statue.json`, `oxidized_copper_grate.json`, `oxidized_copper.json`, `oxidized_cut_copper.json`
- `packed_mud.json`, `pale_oak_log_horizontal.json`, `pale_oak_log.json`, `pale_oak_planks.json`, `pale_oak_wood.json`, `pink_concrete_powder.json`, `pink_concrete.json`, `pink_glazed_terracotta.json`
- `pink_stained_glass.json`, `pink_terracotta.json`, `pink_wool.json`, `podzol.json`, `polished_andesite.json`, `polished_basalt.json`, `polished_blackstone_bricks.json`, `polished_blackstone.json`
- `polished_deepslate.json`, `polished_diorite.json`, `polished_granite.json`, `polished_tuff.json`, `prismarine_bricks.json`, `prismarine.json`, `purple_concrete_powder.json`, `purple_concrete.json`
- `purple_glazed_terracotta.json`, `purple_stained_glass.json`, `purple_terracotta.json`, `purple_wool.json`, `purpur_block.json`, `purpur_pillar_horizontal.json`, `purpur_pillar.json`, `quartz_block.json`
- `quartz_bricks.json`, `quartz_pillar_horizontal.json`, `quartz_pillar.json`, `raw_copper_block.json`, `raw_gold_block.json`, `raw_iron_block.json`, `red_concrete_powder.json`, `red_concrete.json`
- `red_glazed_terracotta.json`, `red_sand.json`, `red_stained_glass.json`, `red_terracotta.json`, `red_wool.json`, `reinforced_deepslate.json`, `repeating_command_block_conditional.json`, `repeating_command_block.json`
- `resin_block.json`, `resin_bricks.json`, `rooted_dirt.json`, `sand.json`, `slime_block.json`, `small_amethyst_bud.json`, `smooth_basalt.json`, `smooth_quartz.json`
- `smooth_stone.json`, `snow_block.json`, `snow_height10.json`, `snow_height12.json`, `snow_height14.json`, `snow_height2.json`, `snow_height4.json`, `snow_height6.json`
- `snow_height8.json`, `soul_sand.json`, `soul_soil.json`, `sponge.json`, `spruce_log_horizontal.json`, `spruce_log.json`, `spruce_planks.json`, `spruce_wood.json`
- `stone_bricks.json`, `stone_mirrored.json`, `stone.json`, `stripped_acacia_log_horizontal.json`, `stripped_acacia_log.json`, `stripped_acacia_wood.json`, `stripped_birch_log_horizontal.json`, `stripped_birch_log.json`
- `stripped_birch_wood.json`, `stripped_cherry_log_x.json`, `stripped_cherry_log_y.json`, `stripped_cherry_log_z.json`, `stripped_cherry_log.json`, `stripped_cherry_wood.json`, `stripped_crimson_hyphae.json`, `stripped_dark_oak_log_horizontal.json`
- `stripped_dark_oak_log.json`, `stripped_dark_oak_wood.json`, `stripped_jungle_log_horizontal.json`, `stripped_jungle_log.json`, `stripped_jungle_wood.json`, `stripped_mangrove_log_horizontal.json`, `stripped_mangrove_log.json`, `stripped_mangrove_wood.json`
- `stripped_oak_log_horizontal.json`, `stripped_oak_log.json`, `stripped_oak_wood.json`, `stripped_pale_oak_log_horizontal.json`, `stripped_pale_oak_log.json`, `stripped_pale_oak_wood.json`, `stripped_spruce_log_horizontal.json`, `stripped_spruce_log.json`
- `stripped_spruce_wood.json`, `stripped_warped_hyphae.json`, `structure_block_corner.json`, `structure_block_data.json`, `structure_block_load.json`, `structure_block_save.json`, `structure_block.json`, `suspicious_gravel_0.json`
- `suspicious_gravel_1.json`, `suspicious_gravel_2.json`, `suspicious_gravel_3.json`, `suspicious_sand_0.json`, `suspicious_sand_1.json`, `suspicious_sand_2.json`, `suspicious_sand_3.json`, `template_command_block.json`
- `template_farmland.json`, `template_glazed_terracotta.json`, `terracotta.json`, `test_block_accept.json`, `test_block_fail.json`, `test_block_log.json`, `test_block_start.json`, `test_instance_block.json`
- `thin_block.json`, `tinted_glass.json`, `tuff_bricks.json`, `tuff.json`, `warped_nylium.json`, `warped_planks.json`, `warped_wart_block.json`, `weathered_chiseled_copper.json`
- `weathered_copper_bars_cap_alt.json`, `weathered_copper_bars_cap.json`, `weathered_copper_bars_post_ends.json`, `weathered_copper_bars_post.json`, `weathered_copper_bars_side_alt.json`, `weathered_copper_bars_side.json`, `weathered_copper_golem_statue.json`, `weathered_copper_grate.json`
- `weathered_copper.json`, `weathered_cut_copper.json`, `wet_sponge.json`, `white_concrete_powder.json`, `white_concrete.json`, `white_glazed_terracotta.json`, `white_stained_glass.json`, `white_terracotta.json`
- `white_wool.json`, `yellow_concrete_powder.json`, `yellow_concrete.json`, `yellow_glazed_terracotta.json`, `yellow_stained_glass.json`, `yellow_terracotta.json`, `yellow_wool.json`

### 12. 엔진 원형·인벤토리용 기술 모델 — 23개 (P2)

- `cross_emissive.json`, `cross.json`, `cube_all_inner_faces.json`, `cube_all.json`, `cube_bottom_top_inner_faces.json`, `cube_bottom_top.json`, `cube_column_horizontal.json`, `cube_column_mirrored.json`
- `cube_column_uv_locked_x.json`, `cube_column_uv_locked_y.json`, `cube_column_uv_locked_z.json`, `cube_column.json`, `cube_directional.json`, `cube_mirrored_all.json`, `cube_mirrored.json`, `cube_north_west_mirrored_all.json`
- `cube_north_west_mirrored.json`, `cube_top.json`, `cube.json`, `orientable_vertical.json`, `orientable_with_bottom.json`, `orientable.json`, `tinted_cross.json`

### 13. 기타 원본 모델·형태별 재분류 대상 — 153개 (P3)

- `air.json`, `azure_bluet.json`, `barrier.json`, `bricks.json`, `carrots_stage0.json`, `carrots_stage1.json`, `carrots_stage2.json`, `carrots_stage3.json`
- `cave_vines_lit.json`, `cave_vines_plant_lit.json`, `cave_vines_plant.json`, `cave_vines.json`, `chiseled_nether_bricks.json`, `chiseled_red_sandstone.json`, `chiseled_sandstone.json`, `chorus_plant_noside.json`
- `chorus_plant_noside1.json`, `chorus_plant_noside2.json`, `chorus_plant_noside3.json`, `chorus_plant_side.json`, `chorus_plant.json`, `cobweb.json`, `cracked_nether_bricks.json`, `creaking_heart_awake_horizontal.json`
- `creaking_heart_awake.json`, `creaking_heart_dormant_horizontal.json`, `creaking_heart_dormant.json`, `creaking_heart_horizontal.json`, `creaking_heart.json`, `crimson_hyphae.json`, `crop.json`, `cut_red_sandstone.json`
- `cut_sandstone.json`, `dragon_egg.json`, `dried_ghast_hydration_0.json`, `dried_ghast_hydration_1.json`, `dried_ghast_hydration_2.json`, `dried_ghast_hydration_3.json`, `dried_ghast.json`, `flowerbed_1.json`
- `flowerbed_2.json`, `flowerbed_3.json`, `flowerbed_4.json`, `four_dead_sea_pickles.json`, `four_sea_pickles.json`, `four_slightly_cracked_turtle_eggs.json`, `four_turtle_eggs.json`, `four_very_cracked_turtle_eggs.json`
- `heavy_core.json`, `light_00.json`, `light_01.json`, `light_02.json`, `light_03.json`, `light_04.json`, `light_05.json`, `light_06.json`
- `light_07.json`, `light_08.json`, `light_09.json`, `light_10.json`, `light_11.json`, `light_12.json`, `light_13.json`, `light_14.json`
- `light_15.json`, `lodestone.json`, `nether_bricks.json`, `pointed_dripstone_down_base.json`, `pointed_dripstone_down_frustum.json`, `pointed_dripstone_down_middle.json`, `pointed_dripstone_down_tip_merge.json`, `pointed_dripstone_down_tip.json`
- `pointed_dripstone_up_base.json`, `pointed_dripstone_up_frustum.json`, `pointed_dripstone_up_middle.json`, `pointed_dripstone_up_tip_merge.json`, `pointed_dripstone_up_tip.json`, `pointed_dripstone.json`, `potatoes_stage0.json`, `potatoes_stage1.json`
- `potatoes_stage2.json`, `potatoes_stage3.json`, `red_nether_bricks.json`, `red_sandstone.json`, `respawn_anchor_0.json`, `respawn_anchor_1.json`, `respawn_anchor_2.json`, `respawn_anchor_3.json`
- `respawn_anchor_4.json`, `sandstone.json`, `sculk_catalyst_bloom.json`, `sculk_catalyst.json`, `sculk_mirrored.json`, `sculk_vein.json`, `sculk.json`, `smooth_red_sandstone.json`
- `smooth_sandstone.json`, `spawner.json`, `spore_blossom.json`, `structure_void.json`, `sunflower_bottom.json`, `sunflower_top.json`, `template_bars_cap_alt.json`, `template_bars_cap.json`
- `template_bars_post_ends.json`, `template_bars_post.json`, `template_bars_side_alt.json`, `template_bars_side.json`, `template_four_candles.json`, `template_four_turtle_eggs.json`, `template_single_face.json`, `template_three_candles.json`
- `template_three_turtle_eggs.json`, `template_two_candles.json`, `template_two_turtle_eggs.json`, `template_vault.json`, `three_dead_sea_pickles.json`, `three_sea_pickles.json`, `three_slightly_cracked_turtle_eggs.json`, `three_turtle_eggs.json`
- `three_very_cracked_turtle_eggs.json`, `torchflower_crop_stage0.json`, `torchflower_crop_stage1.json`, `torchflower.json`, `trial_spawner_active_ominous.json`, `trial_spawner_active.json`, `trial_spawner_ejecting_reward_ominous.json`, `trial_spawner_ejecting_reward.json`
- `trial_spawner_inactive_ominous.json`, `trial_spawner.json`, `twisting_vines_plant.json`, `twisting_vines.json`, `two_dead_sea_pickles.json`, `two_sea_pickles.json`, `two_slightly_cracked_turtle_eggs.json`, `two_turtle_eggs.json`
- `two_very_cracked_turtle_eggs.json`, `vault_active_ominous.json`, `vault_active.json`, `vault_ejecting_reward_ominous.json`, `vault_ejecting_reward.json`, `vault_ominous.json`, `vault_unlocking_ominous.json`, `vault_unlocking.json`
- `vault.json`, `warped_hyphae.json`, `weeping_vines_plant.json`, `weeping_vines.json`, `wildflowers_1.json`, `wildflowers_2.json`, `wildflowers_3.json`, `wildflowers_4.json`
- `wither_rose.json`

## 분석 완료를 판정하는 조건(계획)

1. 해당 소스 파일의 실제 JSON과 Git blob SHA 확인
2. `parent` 상속/모든 요소 `from`·`to`·rotation·face 선언/텍스처 슬롯 추적
3. 참조 PNG를 획득해 실제 RGBA 전체 해독, 명시/암시 UV를 분리 검증(애니메이션 프레임 제외)
4. 관련 blockstate 상태·회전·조합을 원본 규칙에 따라 검수
5. 공식 Mojang 클라이언트 원본 대조 및 실제 게임의 정적 화면·UV 회전·컬링/조명 검증(현재 미완료)
6. 기존 v5–v34 결과와 중복을 대조하고 근거 파일 링크와 검증 등급 기록

## 다른 전체 기초 목록

- [블록 상태 JSON 1,168개 전체 경로·SHA](../research/vanilla_models/v34/02_inventory_1168_blockstate_paths_git_shas.csv)
- [블록 텍스처 PNG 1,111개 전체 경로·SHA](../research/vanilla_models/v34/03_inventory_1111_block_texture_png_paths_git_shas.csv)
- 실제 인게임 특수 렌더러는 모델 JSON만으로 판정 불가능. Mojang 1.21.11 공식 client.jar 미인증. 정적 가구 전용의 최종 범위는 이 파일목록에서 별도 검증을 거쳐 확정할 예정이다.
