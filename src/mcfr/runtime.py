"""Run the pinned 1-3-D engine probe or open its in-game visual fixture."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
from urllib.parse import unquote

from .foundation import preview_runtime

ROOT = Path(__file__).resolve().parents[2]
WORLD_NAME = "MCFR Visual Fixture"


def _scratch_path(value: str) -> Path:
    path = Path(value).resolve()
    if ROOT.resolve() == path or ROOT.resolve() in path.parents:
        raise argparse.ArgumentTypeError("Use a scratch path outside the research repository")
    return path


def open_visual_client(args: argparse.Namespace, script: Path, prepare) -> dict | None:
    """Copy an offline creative world and open it with the original pinned input set."""
    world = args.world.resolve()
    if not (world / "level.dat").is_file():
        raise ValueError("The visual fixture needs a saved local creative world")
    game = args.work / args.version / "probe_game"
    copied_world = game / "saves" / WORLD_NAME
    if world == copied_world or world in copied_world.parents:
        raise ValueError("The source world must be outside the disposable destination")
    if copied_world.exists():
        raise FileExistsError(f"Choose a new visual work directory: {copied_world}")

    _, client, assets, index, libraries = prepare(args.version, args.work, args.client_cache)
    if args.command=="int4-f11f-r08-fabric-pair":
        from .int4_f11f_r08_af_dual_fabric_capture import install_research_jar
        install_research_jar(args,game)
    shutil.copytree(world, copied_world, ignore=shutil.ignore_patterns("session.lock", "datapacks"))
    fixture = script.parent.parent / "followup/build_runtime_fixture.py"
    subprocess.run(
        [sys.executable, str(fixture), "--version", args.version,
         "--pack", str(copied_world / "datapacks/cd_audit")],
        check=True,
    )
    if args.command in ("chair-capture", "af-variant3-capture", "macaw-kitchen-capture", "macaw-table-shelf-capture", "int4-f9-macaw-five", "int4-f10-macaw-connected-five", "int4-f11-vanilla-five", "int4-f11b-vanilla-multipart-five", "int4-f11c-vanilla-decor-four", "int4-f11d-vanilla-bed", "int4-f11e-r06-temporal-sink", "int4-f11f-r08-fabric-pair", "hc-bed-capture", "int4-h10-hc-bed-occupied", "int4-h12-af-chair-samepose", "int4-h15-af-opposing-f2", "int4-h16-af-one-texel-f2", "int5-b4-af-tucked-slab", "int5-b5-af-element4-removal", "int5-b7-af121-child-element4-f2", "int5-b8-hc-cushion12-native-f2", "int5-b17-hc-twelve-batch-f2", "int5-b9-af121-backrest7-native-f2", "int5-b10-af121-backrest8-native-f2", "int5-b11-af121-backrest9-native-f2", "int5-b12-af123-backrest7-native-f2", "int5-b13-af123-backrest8-native-f2", "int5-b14-af123-backrest9-native-f2", "int5-b15-af123-batch-f2", "int5-b16-af121-batch-f2"):
        from .chair_runtime_fixture import make_pack
        selected=None
        if args.command=="af-variant3-capture":
            from .int4_af_variant3_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="macaw-kitchen-capture":
            from .int4_macaw_kitchen_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="macaw-table-shelf-capture":
            from .int4_macaw_table_shelf_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f9-macaw-five":
            from .int4_f9_macaw_five_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f10-macaw-connected-five":
            from .int4_f10_macaw_connected_five_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f11-vanilla-five":
            from .int4_f11_vanilla_five_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f11b-vanilla-multipart-five":
            from .int4_f11b_vanilla_multipart_five_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f11c-vanilla-decor-four":
            from .int4_f11c_vanilla_kitchen_decor_four_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f11d-vanilla-bed":
            from .int4_f11d_vanilla_white_bed_special_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f11e-r06-temporal-sink":
            from .int4_f11e_r06_macaw_sink_temporal_capture import capture_cases
            selected=capture_cases(args.version)
        elif args.command=="int4-f11f-r08-fabric-pair":
            from .int4_f11f_r08_af_dual_fabric_capture import original_case
            selected=original_case()
        elif args.command=="hc-bed-capture":
            from .int4_handcrafted_bed_capture import cases
            selected=cases(args.version)
        elif args.command=="int4-h10-hc-bed-occupied":
            from .int4_h10_hc_bed_occupied_f2_capture import capture_case
            selected=capture_case()
        elif args.command in ("int4-h12-af-chair-samepose","int4-h15-af-opposing-f2","int4-h16-af-one-texel-f2", "int5-b7-af121-child-element4-f2", "int5-b9-af121-backrest7-native-f2", "int5-b10-af121-backrest8-native-f2", "int5-b11-af121-backrest9-native-f2", "int5-b16-af121-batch-f2"):
            from .int4_h12_af_chair_samepose_f2_capture import original_case
            selected=original_case()
        elif args.command in ("int5-b4-af-tucked-slab", "int5-b5-af-element4-removal", "int5-b7-af121-child-element4-f2", "int5-b12-af123-backrest7-native-f2", "int5-b13-af123-backrest8-native-f2", "int5-b14-af123-backrest9-native-f2", "int5-b15-af123-batch-f2", "int5-b16-af121-batch-f2"):
            from .int5_af_tucked_slab_control import target_case
            selected=(target_case(),)
        elif args.command=="int5-b8-hc-cushion12-native-f2":
            from .int5_b8_hc_cushion_element12_native_f2 import pinned_chair_case
            selected=(pinned_chair_case(),)
        elif args.command=="int5-b17-hc-twelve-batch-f2":
            from .int5_b17_hc_twelve_element_batch_f2 import pinned_chair_case
            selected=(pinned_chair_case(),)
        make_pack(args.version, copied_world / "datapacks/mcfr_chair",
                  selected_cases=selected)
        if args.command=="int4-f11b-vanilla-multipart-five":
            from .int4_f11b_vanilla_multipart_five_capture import prepare_fence_neighbor_datapack
            prepare_fence_neighbor_datapack(copied_world/"datapacks/mcfr_chair")
        if args.command=="int4-f11d-vanilla-bed":
            from .int4_f11d_vanilla_white_bed_special_capture import prepare_bed_datapack
            prepare_bed_datapack(copied_world/"datapacks/mcfr_chair")
        if args.command=="int4-f11e-r06-temporal-sink":
            from .int4_f11e_r06_macaw_sink_temporal_capture import prepare_r06_datapack
            prepare_r06_datapack(copied_world/"datapacks/mcfr_chair")
    if args.command in ("macaw-neighbor-capture","int4-h8-r03-player-gui"):
        from .int4_macaw_neighbor_capture import make_pack as make_neighbor_pack
        make_neighbor_pack(args.version,copied_world/"datapacks/mcfr_neighbor")
    (game / "options.txt").write_text(
        "renderDistance:4\nsimulationDistance:5\nmaxFps:30\nguiScale:2\n", encoding="utf-8"
    )
    env = {**os.environ, "LIBGL_ALWAYS_SOFTWARE": "1", "ALSOFT_DRIVERS": "null"}
    if args.display:
        env["DISPLAY"] = args.display
    command = [
        "java", "-Xmx2G", "-XX:ActiveProcessorCount=4", "-cp", os.pathsep.join(map(str, [client, *libraries])),
        "net.fabricmc.loader.impl.launch.knot.KnotClient", "--username", "RenderAudit",
        "--version", args.version, "--gameDir", str(game), "--assetsDir", str(assets),
        "--assetIndex", index, "--accessToken", "0", "--width", "1024", "--height", "684",
        "--quickPlaySingleplayer", WORLD_NAME,
    ]
    if args.command == "visual-capture":
        from .runtime_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command in ("chair-capture", "af-variant3-capture"):
        from .chair_runtime_capture import capture_chairs
        if args.command=="af-variant3-capture":
            from .int4_af_variant3_capture import capture_cases, exact_expected_models
            return capture_chairs(
                command, env, game, args.output, args.version,
                selected_cases=capture_cases(args.version),
                expected_case_models=exact_expected_models(),
                report_name="INT4_AF_VARIANT3_REAL_F2_CAPTURE.json")
        return capture_chairs(command, env, game, args.output, args.version)
    if args.command=="macaw-kitchen-capture":
        from .int4_macaw_kitchen_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="macaw-table-shelf-capture":
        from .int4_macaw_table_shelf_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f9-macaw-five":
        from .int4_f9_macaw_five_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f10-macaw-connected-five":
        from .int4_f10_macaw_connected_five_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f11-vanilla-five":
        from .int4_f11_vanilla_five_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f11b-vanilla-multipart-five":
        from .int4_f11b_vanilla_multipart_five_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f11c-vanilla-decor-four":
        from .int4_f11c_vanilla_kitchen_decor_four_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f11d-vanilla-bed":
        from .int4_f11d_vanilla_white_bed_special_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f11e-r06-temporal-sink":
        if os.environ.get("MCFR_H23_MODE"):
            from .int4_h23_r06_animation_control import capture
        else:
            from .int4_f11e_r06_macaw_sink_temporal_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-f11f-r08-fabric-pair":
        from .int4_f11f_r08_af_dual_fabric_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="hc-bed-capture":
        from .int4_handcrafted_bed_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-h10-hc-bed-occupied":
        from .int4_h10_hc_bed_occupied_f2_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-h12-af-chair-samepose":
        from .int4_h12_af_chair_samepose_f2_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-h15-af-opposing-f2":
        from .int4_h15_af_opposing_f2_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-h16-af-one-texel-f2":
        from .int4_h16_af_single_texel_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b4-af-tucked-slab":
        from .int5_af_tucked_slab_control import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b5-af-element4-removal":
        from .int5_af_element4_removal_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b12-af123-backrest7-native-f2":
        from .int5_b12_af123_backrest_element7_native_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b13-af123-backrest8-native-f2":
        from .int5_b13_af123_backrest_element8_native_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b14-af123-backrest9-native-f2":
        from .int5_b14_af123_backrest_element9_native_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b15-af123-batch-f2":
        from .int5_b15_af123_six_element_batch_f2 import capture
        return capture(command,env,game,args.output,args.version,args.index)
    if args.command=="int5-b16-af121-batch-f2":
        from . import int5_b16_af121_six_element_batch_f2 as b16
        b16.select_index(args.index)
        return b16.capture(command,env,game,args.output,args.version)
    if args.command=="int5-b7-af121-child-element4-f2":
        from .int5_b7_af121_child_element4_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b8-hc-cushion12-native-f2":
        from .int5_b8_hc_cushion_element12_native_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b17-hc-twelve-batch-f2":
        from . import int5_b17_hc_twelve_element_batch_f2 as b17
        b17.select_index(args.index)
        return b17.capture(command,env,game,args.output,args.version)
    if args.command=="int5-b9-af121-backrest7-native-f2":
        from .int5_b9_af121_backrest_element7_native_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b10-af121-backrest8-native-f2":
        from .int5_b10_af121_backrest_element8_native_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int5-b11-af121-backrest9-native-f2":
        from .int5_b11_af121_backrest_element9_native_f2 import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="macaw-neighbor-capture":
        from .int4_macaw_neighbor_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command=="int4-h8-r03-player-gui":
        from .int4_h8_r03_player_gui_capture import capture
        return capture(command,env,game,args.output,args.version)
    if args.command == "int4-nonchair-capture":
        from .int4_nonchair_runtime import capture
        return capture(command, env, game, args.output, args.version, interaction=args.interaction)
    if args.command == "int4-f-missing-capture":
        from .int4_f_missing_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f3-mod-capture":
        from .int4_f3_storage_shelf_light_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-h03-h05-drawer-front-f2":
        from .int4_h03_h05_s20_s21_drawer_front import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f4-mod-capture":
        from .int4_f4_chair_bench_couch_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f5-state-diagnostic":
        from .int4_f5_state_diagnostic import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f6-causal-replay":
        from .int4_f6_source_causal_replay import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-f7-source-cases":
        from .int4_f7_four_source_cases_capture import capture
        return capture(command, env, game, args.output, args.version)
    if args.command == "int4-bed-exterior":
        from .int4_bed_exterior import capture
        return capture(command, env, game, args.output, args.version, uv_probe=args.uv_probe, expanded=args.uv_faces)
    subprocess.run(command, cwd=game, env=env, check=True)
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    engine = sub.add_parser("engine", help="run the historical registry and collision probe")
    visual = sub.add_parser("visual-client", help="open a copied local world for in-game capture")
    capture = sub.add_parser("visual-capture", help="capture and compare pinned in-game scenes on an isolated X11 display")
    chairs = sub.add_parser("chair-capture", help="capture 4 source chairs x 4 facings with verified Minecraft F2 screenshots")
    af3 = sub.add_parser("af-variant3-capture", help="capture AF variant3 four directions plus variant1 controls")
    kitchen = sub.add_parser("macaw-kitchen-capture", help="actual pinned Macaw 1.21.11 kitchen 3-state F2")
    table_shelf = sub.add_parser("macaw-table-shelf-capture", help="actual pinned Macaw 1.21.11 table/bookshelf four source states F2")
    f9macaw = sub.add_parser("int4-f9-macaw-five", help="INT-4-F9 five original Macaw 1.21.11 source states actual native F2")
    f10macaw = sub.add_parser("int4-f10-macaw-connected-five", help="INT-4-F10 five historical connected Macaw 1.21.11 states actual F2")
    f11vanilla = sub.add_parser("int4-f11-vanilla-five", help="INT-4-F11A five official 1.21.11 vanilla historical states source SHA F2")
    f11bvanilla = sub.add_parser("int4-f11b-vanilla-multipart-five", help="INT-4-F11B actual five vanilla including V03/V08 multipart states official F2")
    f11cvanilla = sub.add_parser("int4-f11c-vanilla-decor-four", help="INT-4-F11C official vanilla V12-V15 source SHA actual F2")
    f11dbed = sub.add_parser("int4-f11d-vanilla-bed", help="INT-4-F11D official V11 two-part bed special-render vs AIR paired F2")
    f11esink = sub.add_parser("int4-f11e-r06-temporal-sink", help="INT-4-F11E Macaw source water=true 3 real time-separated F2 and server stability")
    f11fr08 = sub.add_parser("int4-f11f-r08-fabric-pair", help="INT-4-F11F same-loader 4.0.2 official vs 4.0.3 Git source-built acacia north original F2")
    hcbed = sub.add_parser("hc-bed-capture", help="pinned Handcrafted 1.21.1 bed foot/head individual native F2")
    h10 = sub.add_parser("int4-h10-hc-bed-occupied", help="actual Fabric same-camera Handcrafted bed foot occupied false, true, and air native F2")
    h12 = sub.add_parser("int4-h12-af-chair-samepose", help="actual Fabric same-coordinate north AF acacia_1/acacia_3/AIR native F2 controlled model-only A-B-A")
    h15 = sub.add_parser("int4-h15-af-opposing-f2", help="real Fabric AF chair fixed north model1/3 A-B-A-air from south and north cameras")
    h16 = sub.add_parser("int4-h16-af-one-texel-f2", help="real Fabric AF single-texel transient resource-pack two-camera F2")
    b4 = sub.add_parser("int5-b4-af-tucked-slab", help="real official Fabric tucked chair vs fixed support slab control, two camera A-B-A-air native F2")
    b5 = sub.add_parser("int5-b5-af-element4-removal", help="disposable exact AF123 source element4 removal, two-camera real F2 against pinned B4 baseline")
    b7 = sub.add_parser("int5-b7-af121-child-element4-f2", help="AF121 child-only source element4 removal vs official H15 real F2 original 8-frame baseline")
    b8 = sub.add_parser("int5-b8-hc-cushion12-native-f2", help="two independent original and modified Handcrafted black-cushion element12 real Fabric F2 sessions")
    b17 = sub.add_parser("int5-b17-hc-twelve-batch-f2", help="12 original HC11210 child model source elements each two Fabric 1.21.1 native F2 sessions")
    b17.add_argument("--index",type=int,choices=tuple(range(12)),required=True)
    b9 = sub.add_parser("int5-b9-af121-backrest7-native-f2", help="AF121 original backrest element7 isolated child model native Minecraft F2 vs H15")
    b10 = sub.add_parser("int5-b10-af121-backrest8-native-f2", help="AF121 original backrest element8 isolated child model native Minecraft F2 vs pinned H15")
    b11 = sub.add_parser("int5-b11-af121-backrest9-native-f2", help="AF121 original backrest element9 isolated child model actual Minecraft F2 vs pinned H15")
    b12 = sub.add_parser("int5-b12-af123-backrest7-native-f2", help="AF123 tucked variant10 backrest index7 child-only real F2 vs B4 legal support slab")
    b13 = sub.add_parser("int5-b13-af123-backrest8-native-f2", help="AF123 tucked variant10 backrest index8 child-only native F2 vs pinned B4 original support slab")
    b14 = sub.add_parser("int5-b14-af123-backrest9-native-f2", help="AF123 tucked variant10 original backrest index9 child-only native F2 vs anchored B4 support slab")
    b15 = sub.add_parser("int5-b15-af123-batch-f2", help="six independent AF123 original source element removals on real Fabric F2")
    b15.add_argument("--index", type=int, choices=(0,1,2,3,5,6), required=True)
    b16 = sub.add_parser("int5-b16-af121-batch-f2", help="six independent AF121 source elements isolated child/variant3 original H15 F2")
    b16.add_argument("--index", type=int, choices=(0,1,2,3,5,6), required=True)
    neighbor = sub.add_parser("macaw-neighbor-capture", help="actual Macaw table placement/removal adjacent block update trial")
    h8 = sub.add_parser("int4-h8-r03-player-gui", help="actual Fabric 1.21.11 Macaw table player right-click join and left-click break")
    nonchair = sub.add_parser("int4-nonchair-capture", help="remaining source states and actual shelf/bed transitions")
    fmissing = sub.add_parser("int4-f-missing-capture", help="INT-4-F2 four original 1-5 study cases with native F2")
    f3mod = sub.add_parser("int4-f3-mod-capture", help="INT-4-F3 seven source storage/shelf/lamp cases native F2")
    drawer_front = sub.add_parser("int4-h03-h05-drawer-front-f2", help="H03 H05 original AF drawer open/closed at front north observer native F2")
    f4mod = sub.add_parser("int4-f4-mod-capture", help="INT-4-F4 seven chair/bench/couch/pot cases native F2")
    f5mode = sub.add_parser("int4-f5-state-diagnostic", help="INT-4-F5 S02/S34 server property diagnosis and native F2")
    f6mode = sub.add_parser("int4-f6-causal-replay", help="INT-4-F6 S02/S34 source-coded tucked/inner-left game replay")
    f7mode = sub.add_parser("int4-f7-source-cases", help="INT-4-F7 AF variant3, bench double and HC vanilla parent 4 original F2")
    exterior = sub.add_parser("int4-bed-exterior", help="observe occupied bed from an independent client")
    for command in (engine, visual, capture, chairs, af3, kitchen, table_shelf, f9macaw, f10macaw, f11vanilla, f11bvanilla, f11cvanilla, f11dbed, f11esink, f11fr08, hcbed, h10, h12, h15, h16, b4, b5, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, neighbor, h8, nonchair, fmissing, f3mod, drawer_front, f4mod, f5mode, f6mode, f7mode, exterior):
        command.add_argument("--version", required=True)
        command.add_argument("--work", type=_scratch_path, required=True)
        command.add_argument("--client-cache", type=_scratch_path)
        command.add_argument("--display", help="X11 display, for example :99")
    engine.add_argument("--output", type=_scratch_path, required=True)
    engine.add_argument("--ecj", type=Path)
    for command in (visual, capture, chairs, af3, kitchen, table_shelf, f9macaw, f10macaw, f11vanilla, f11bvanilla, f11cvanilla, f11dbed, f11esink, f11fr08, hcbed, h10, h12, h15, h16, b4, b5, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, neighbor, h8, nonchair, fmissing, f3mod, drawer_front, f4mod, f5mode, f6mode, f7mode, exterior):
        command.add_argument("--world", type=Path, required=True)
    capture.add_argument("--output", type=_scratch_path, required=True)
    chairs.add_argument("--output", type=_scratch_path, required=True)
    af3.add_argument("--output", type=_scratch_path, required=True)
    kitchen.add_argument("--output", type=_scratch_path, required=True)
    table_shelf.add_argument("--output", type=_scratch_path, required=True)
    f9macaw.add_argument("--output", type=_scratch_path, required=True)
    f10macaw.add_argument("--output", type=_scratch_path, required=True)
    f11vanilla.add_argument("--output", type=_scratch_path, required=True)
    f11bvanilla.add_argument("--output", type=_scratch_path, required=True)
    f11cvanilla.add_argument("--output", type=_scratch_path, required=True)
    f11dbed.add_argument("--output", type=_scratch_path, required=True)
    f11esink.add_argument("--output", type=_scratch_path, required=True)
    f11fr08.add_argument("--output", type=_scratch_path, required=True)
    f11fr08.add_argument("--af-source-jar", type=Path, help="Pinned Git 4.0.3 self-built Fabric JAR; omit for official Fabric 4.0.2")
    hcbed.add_argument("--output", type=_scratch_path, required=True)
    h10.add_argument("--output", type=_scratch_path, required=True)
    h12.add_argument("--output", type=_scratch_path, required=True)
    h15.add_argument("--output", type=_scratch_path, required=True)
    h16.add_argument("--output", type=_scratch_path, required=True)
    b4.add_argument("--output", type=_scratch_path, required=True)
    b5.add_argument("--output", type=_scratch_path, required=True)
    b7.add_argument("--output", type=_scratch_path, required=True)
    b8.add_argument("--output", type=_scratch_path, required=True)
    b17.add_argument("--output", type=_scratch_path, required=True)
    b9.add_argument("--output", type=_scratch_path, required=True)
    b10.add_argument("--output", type=_scratch_path, required=True)
    b11.add_argument("--output", type=_scratch_path, required=True)
    b12.add_argument("--output", type=_scratch_path, required=True)
    b13.add_argument("--output", type=_scratch_path, required=True)
    b14.add_argument("--output", type=_scratch_path, required=True)
    b15.add_argument("--output", type=_scratch_path, required=True)
    b16.add_argument("--output", type=_scratch_path, required=True)
    neighbor.add_argument("--output", type=_scratch_path, required=True)
    h8.add_argument("--output", type=_scratch_path, required=True)
    nonchair.add_argument("--interaction", action="store_true", help="run player placement and sleeping trials")
    nonchair.add_argument("--output", type=_scratch_path, required=True)
    fmissing.add_argument("--output", type=_scratch_path, required=True)
    f3mod.add_argument("--output", type=_scratch_path, required=True)
    drawer_front.add_argument("--output", type=_scratch_path, required=True)
    f4mod.add_argument("--output", type=_scratch_path, required=True)
    f5mode.add_argument("--output", type=_scratch_path, required=True)
    f6mode.add_argument("--output", type=_scratch_path, required=True)
    f7mode.add_argument("--output", type=_scratch_path, required=True)
    exterior.add_argument("--uv-probe", action="store_true", help="override the observer texture with a four-tag UV calibration")
    exterior.add_argument("--uv-faces", action="store_true", help="add three exposed occupied-bed faces")
    exterior.add_argument("--output", type=_scratch_path, required=True)
    args = parser.parse_args(argv)

    try:
        plan = preview_runtime(ROOT, args.version)
        script = ROOT / plan["command"][1]
        # The old launcher loads every file under mods/. Keep each run on the pinned inputs.
        mods = args.work / args.version / "probe_game/mods"
        prepare = runpy.run_path(str(script))

        pinned = {unquote(path.rsplit("/", 1)[-1]) for path, _ in prepare["MODS"][args.version]}
        if args.command == "engine":
            pinned.add("research-probe.jar")  # the probe overwrites its own JAR before launch
        if mods.is_symlink() or any(child.name not in pinned or child.is_symlink() for child in mods.glob("*")):
            raise ValueError(f"Use a dedicated work directory containing only the pinned Mods inputs: {mods}")

        if args.command != "engine":
            if not (args.display or os.environ.get("DISPLAY")):
                raise ValueError("An X11 display is required for visual capture")
            if args.command in ("visual-capture", "chair-capture", "af-variant3-capture", "macaw-kitchen-capture", "macaw-table-shelf-capture", "int4-f9-macaw-five", "int4-f10-macaw-connected-five", "int4-f11-vanilla-five", "int4-f11b-vanilla-multipart-five", "int4-f11c-vanilla-decor-four", "int4-f11d-vanilla-bed", "int4-f11e-r06-temporal-sink", "int4-f11f-r08-fabric-pair", "hc-bed-capture", "int4-h10-hc-bed-occupied", "int4-h12-af-chair-samepose", "int4-h15-af-opposing-f2", "int4-h16-af-one-texel-f2", "int5-b4-af-tucked-slab", "int5-b5-af-element4-removal", "int5-b7-af121-child-element4-f2", "int5-b8-hc-cushion12-native-f2", "int5-b17-hc-twelve-batch-f2", "int5-b9-af121-backrest7-native-f2", "int5-b10-af121-backrest8-native-f2", "int5-b11-af121-backrest9-native-f2", "int5-b12-af123-backrest7-native-f2", "int5-b13-af123-backrest8-native-f2", "int5-b14-af123-backrest9-native-f2", "int5-b15-af123-batch-f2", "int5-b16-af121-batch-f2", "macaw-neighbor-capture", "int4-h8-r03-player-gui", "int4-nonchair-capture", "int4-f-missing-capture", "int4-f3-mod-capture", "int4-h03-h05-drawer-front-f2", "int4-f4-mod-capture", "int4-f5-state-diagnostic", "int4-f6-causal-replay", "int4-f7-source-cases", "int4-bed-exterior"):
                if shutil.which("xdotool") is None:
                    raise ValueError("Automatic visual capture requires xdotool")
                if args.output.exists():
                    raise FileExistsError(f"Choose a new capture output directory: {args.output}")
            report = open_visual_client(args, script, prepare["prepare"])
            if report is not None:
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return int(report["status"] not in ("MATCH", "CAPTURED_SOURCE_STATES_NOT_VISUALLY_APPROVED", "SERVER_NEIGHBOR_STATES_RECORDED_NO_ASSUMED_CONNECTION", "SERVER_STATES_AND_F2_RECORDED", "ACTUAL_V11_BED_AIR_CONTROL_AND_TWO_PART_F2_NOT_YET_INDEPENDENTLY_AUDITED", "CAPTURED_REAL_S43_THREE_TIME_SEPARATED_F2_NOT_YET_INDEPENDENTLY_AUDITED", "ONE_REAL_FABRIC_SOURCE_RELEASE_F2_CAPTURED_NOT_CROSS_RELEASE_APPROVED", "REAL_PLAYER_ITEM_RIGHT_CLICK_JOIN_AND_LEFT_CLICK_REMOVE", "CAPTURED_OCCUPIED_F2_SOURCE_STATES_WITH_NONZERO_ROI_DIFF", "CAPTURED_OCCUPIED_F2_BUT_VISIBLE_SOURCE_DIFF_NOT_PROVEN", "ACTUAL_NATIVE_F2_MODEL_TEXTURE_CONTRAST_CANDIDATE", "REAL_GAME_F2_BUT_VISUAL_DIFFERENCE_NOT_YET_PROVEN", "ORIGINAL_REAL_FABRIC_TWO_CAMERA_F2_CAPTURED_REQUIRES_INDEPENDENT_AUDIT", "H16_SIX_ACTUAL_F2_TEMP_JAR_ONE_TEXEL_REQUIRES_INDEPENDENT_AUDIT", "ACTUAL_NATIVE_F2_8_SERVER_STATES_REQUIRES_INDEPENDENT_AUDIT", "ACTUAL_SOURCE_ELEMENT4_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT", "TWO_ACTUAL_NATIVE_F2_SESSIONS_PENDING_INDEPENDENT_REOPEN", "ACTUAL_SOURCE_ELEMENT7_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT", "ACTUAL_SOURCE_ELEMENT8_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT", "ACTUAL_SOURCE_ELEMENT9_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT", "ACTUAL_SOURCE_ELEMENT_SELECTED_PATCHED_CHILD_NATIVE_F2_NEEDS_INDEPENDENT_AUDIT"))
        else:
            command = [sys.executable, str(script), "--version", args.version,
                       "--work", str(args.work), "--output", str(args.output)]
            for option in ("client_cache", "display", "ecj"):
                value = getattr(args, option)
                if value is not None:
                    command.extend(("--" + option.replace("_", "-"), str(value)))
            subprocess.run(command, check=True)
    except (ImportError, KeyError, OSError, ValueError, subprocess.SubprocessError) as error:
        parser.exit(1, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
