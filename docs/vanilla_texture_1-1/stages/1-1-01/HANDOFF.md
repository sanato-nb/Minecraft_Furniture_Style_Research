# 1-1-01 목재·원목 전용 인수인계 (TEX01-R002)

Current: TEX01-R002. Next: TEX01-R003. Global legacy v38 unchanged. Fixed scope: 18 wood textures; animation, actual furniture 3D creation, and Project Zomboid conversion are out of scope.

## Immutable results

- R001 original PNG SHA256/CRC/RGBA 18/18 and static JSON 43/source face refs 150: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R001/REPORT.md
- R002 REPORT: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R002/REPORT.md
- R002 72 synthetic rotations CSV: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R002/ROTATED_SEAM_ALL_ANGLES.csv
- R002 18-per-texture seam summary CSV: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R002/ROTATED_SEAM_METRICS.csv
- R002 JSON SHA recheck: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R002/STATIC_JSON_RECHECK.csv
- R002 SUMMARY.json: https://github.com/sanato-nb/Minecraft_Furniture_Style_Research/blob/main/research/vanilla_textures/by_stage/1-1-01/TEX01-R002/SUMMARY.json

## Exact A–G state

A/B/C: R001 mirror/extracted source PNG 18/18 completed. D1: R001 six material comparisons, still partial for missing end textures outside fixed 18. D2: R001 native seams + R002 new 72 synthetic neighbor rotations from the same 18 PNGs. D3/E: 18 source-texture model/UV links, 43 unique JSON and 150 local model faces from R001; 11 original JSON SHA freshly checked R002. F: official Mojang client.jar 0/18, ingame static 0/18 (pending). G: R002 separately committed.

D2 key observation: all 12 planks lowest virtual LR edge at 0° and virtual TB at 180°. Neighbor rotation experiment is NOT a verified in-game texture orientation rule. oak_log_top native 0° LR 16/16 exact matching edge pixels, TB 14/16. Source cube_column_horizontal local up face rotation=180 is a different property from our virtual-neighbor experiment.

## Next TEX01-R003

1. Re-read stage STATE.json current/next revision, Git blob SHA and main HEAD, check R003 path missing before writes. Reject concurrent same-stage conflicts. Do not overwrite R001 or R002.
2. Obtain official Mojang 1.21.11 client.jar through authoritative manifest URL and compare complete JAR SHA1 and size to manifest, then verify 18 internal PNG bytes SHA256. Until actually done, official verification stays 0.
3. If no Minecraft static scene was really observed, do not certify ingame UV, culling, seams or lighting. Do not confuse synthetic rotations with runtime.
4. Update only this stage STATE.json, HANDOFF.md, and new results folder; never root HANDOFF.md/PROGRESS.md/handoff/STATE.json or other stage 1-1-xx.
5. Keep animation study deferred and historical dynamic records preserved.
