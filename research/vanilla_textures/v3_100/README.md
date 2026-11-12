# Minecraft 1.21.11 Vanilla Texture Research v3

- 100 16x16 texture measurements. 10 texture classes.
- 83 previous SHA256s cross-checked; 17 newly decoded.
- The ZIP contains no source Minecraft texture PNGs.
- `analyze_vanilla_100.py --client-jar YOUR_OFFICIAL_1.21.11_CLIENT.jar --output OUTPUT` re-computes pixel statistics from a legitimate local client JAR; confirm the jar version yourself.
- Official game asset SHA or in-game rendering tests have NOT yet been performed.
- Some leaves, vine, and grass textures have `tintindex: 0` in Minecraft model JSON, so raw PNG palette is not final game appearance.
