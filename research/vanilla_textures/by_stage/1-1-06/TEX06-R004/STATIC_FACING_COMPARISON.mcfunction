# TEX06-R004: static comparison only; NOT EXECUTED in-game
# For Minecraft Java 1.21.11 datapack function; places 16 glazed blocks at relative y=-1
# Requires controlled screenshots with north direction indicated; no assumed in-game verification
# black_A_right_hand north / west / east / south [TL / TR / BL / BR]
setblock ~ ~-1 ~ minecraft:black_glazed_terracotta[facing=north] replace
setblock ~1 ~-1 ~ minecraft:black_glazed_terracotta[facing=west] replace
setblock ~ ~-1 ~1 minecraft:black_glazed_terracotta[facing=east] replace
setblock ~1 ~-1 ~1 minecraft:black_glazed_terracotta[facing=south] replace
# black_B_opposite_projection north / east / west / south [TL / TR / BL / BR]
setblock ~5 ~-1 ~ minecraft:black_glazed_terracotta[facing=north] replace
setblock ~6 ~-1 ~ minecraft:black_glazed_terracotta[facing=east] replace
setblock ~5 ~-1 ~1 minecraft:black_glazed_terracotta[facing=west] replace
setblock ~6 ~-1 ~1 minecraft:black_glazed_terracotta[facing=south] replace
# white_A_right_hand south / east / west / north [TL / TR / BL / BR]
setblock ~ ~-1 ~5 minecraft:white_glazed_terracotta[facing=south] replace
setblock ~1 ~-1 ~5 minecraft:white_glazed_terracotta[facing=east] replace
setblock ~ ~-1 ~6 minecraft:white_glazed_terracotta[facing=west] replace
setblock ~1 ~-1 ~6 minecraft:white_glazed_terracotta[facing=north] replace
# white_B_opposite_projection south / west / east / north [TL / TR / BL / BR]
setblock ~5 ~-1 ~5 minecraft:white_glazed_terracotta[facing=south] replace
setblock ~6 ~-1 ~5 minecraft:white_glazed_terracotta[facing=west] replace
setblock ~5 ~-1 ~6 minecraft:white_glazed_terracotta[facing=east] replace
setblock ~6 ~-1 ~6 minecraft:white_glazed_terracotta[facing=north] replace
