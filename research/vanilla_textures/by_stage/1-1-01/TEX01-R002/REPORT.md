# TEX01-R002 | 1-1-01 목재·원목 후속 D2/D3 직접 분석

Date: 2026-11-13. Scope: EXACTLY 18 textures from STATE.items. Global v38 remains untouched. R001 original SHA/CRC/RGBA 18/18 remains valid without double-counting.

## A–C: Source reuse and independent repeated comparison

Re-read R001 SOURCE_LEDGER.csv. Every texture ID and source SHA256 matches fixed STATE.items (18/18). Local 16x16 PNG RGB arrays decoded from 18 R001 source-matched files. New experiment consists of 18 textures times 4 synthetic adjacent-neighbor orientations = 72 cases. These are NEW seam experiments, NOT 72 newly authenticated textures.

For each original tile T, synthesize neighbor N(k)=numpy.rot90(T,k) for k=0,1,2,3 (0/90/180/270 counter-clockwise); compute mean per-channel absolute RGB difference along T's x=15 border versus N's x=0 border (LR), and T's y=15 versus N's y=0 border (TB), 16 RGB pairs per direction. Also count exact RGB-matching edge pairs. Compare k=0 borders against R001 source ledger; 18/18 match. Normalize native k=0 seam to internal per-pixel neighbor mean (for H: 16x15 pairs; V: 15x16).

## D2: Actual new quantitative observations

- All twelve planks textures: minimum LR candidate at 0 degrees, minimum TB candidate at 180 degrees. This is a virtual image placement result ONLY, not an observed blockstate rotation rule.
- oak_planks native LR=12.5417 and TB=56.8333; 180-degree virtual neighbor yields TB=10.8333. Native LR 8/16 RGB edge pairs exactly match, TB 0/16.
- bamboo_planks native LR=3.1875 and internal horizontal delta=7.6958, border/internal ratio=0.4142; TB=33.2917, while hypothetical 180-degree neighbor TB=5.3333.
- oak_log native LR=17.2083 versus virtual 180-degree neighbor LR=6.0.
- oak_log_top native LR=0 with 16/16 exact RGB edge pairs and TB=2.0 with 14/16 exact edge pairs. This is not a claim about Minecraft physical connected-texture behavior.
- birch_log native LR=27.4167 / TB=22.1458, seam/internal ratios H=1.3604, V=0.5413. It retains the bark-pattern exception in R001.
- bamboo_mosaic native LR=26.375 and TB=25.5833; ratios 1.6069 and 1.5898 relative to horizontal/vertical internal neighbor differences. Its texture does not automatically become edge-seamless when tiles are copied unrotated.
Full 72 cases with precise RGB and exact-match counts: ROTATED_SEAM_ALL_ANGLES.csv. One row per texture and best-candidate summaries: ROTATED_SEAM_METRICS.csv.

## D3/E: Source-model cross-check (not engine-render verification)

Freshly re-read 11 named GitHub 1.21.11/assets/minecraft source JSON files, with blob SHAs in STATIC_JSON_RECHECK.csv. Original log blockstates set axis=y default column, axis=z horizontal model x=90, axis=x horizontal model x=90 and y=90. Source cube_column_horizontal model explicitly sets rotation=180 on its LOCAL up face UV; this is NOT the same as rotating an adjacent entire texture by 180 degrees in our D2 experiment. bamboo_mosaic uses cube_all, and its native default blockstate has no empirically verified random tile rotation.

The 11 JSONs are subset rechecks of R001's 43 static JSONs; do not add them to the distinct source count, and retain R001's 150 local model-face references.

## F: Official vs third-party provenance remains unresolved

Mojang metadata endpoint: https://piston-meta.mojang.com/mc/game/version_manifest_v2.json . An external third-party list identifies the 1.21.11 Mojang client URL object by SHA1 ba2df812c2d12e0219c489c4cd9a5e1f0760f5bd (https://github.com/svalked-dev/palmcraftlauncher/blob/main/minecraft-server-jar-downloads.md). In this runtime, downloading official Mojang 1.21.11 client.jar directly was unsuccessful. The client JAR's bytes, total SHA1/size, and its internal 18 PNGs were NOT checked; third-party link metadata is NOT official original authentication.

Hence official client.jar authenticated 0/18; ingame static render verified 0/18. No animation or keyframes studied. No Project Zomboid conversion and no actual furniture 3D modeling.

## G: Stage-specific immutable evidence

Files: ROTATED_SEAM_ALL_ANGLES.csv (72 cases), ROTATED_SEAM_METRICS.csv (18 rows), STATIC_JSON_RECHECK.csv (11 JSON SHA), SUMMARY.json, and REPORT.md. This revision adds genuine D2 static pixel research and does not alter R001, global v38, or other 1-1-xx stages. Next stage-only revision TEX01-R003, created only after further real evidence and pre-write SHA/version check.
