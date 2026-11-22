import unittest

from mcfr import int4_nonchair_runtime as trial


class RuntimeExperimentTests(unittest.TestCase):
    def test_only_six_missing_representatives_are_staged(self):
        rows, _ = trial.applications()
        self.assertEqual(tuple(rows), ("S14", "S15", "S16", "S17", "S39", "S40"))
        self.assertEqual([len(entries) for entries in rows.values()], [5, 1, 1, 1, 1, 1])

    def test_shelf_placement_does_not_set_connection(self):
        stages = trial.stages("1.21.11")
        for commands, _ in stages.values():
            self.assertTrue(all("connection=" not in command for command in commands))

    def test_bed_uses_input_for_installation_and_breaking(self):
        stages = trial.stages("1.21.1", {"part": ["foot", "head"]})
        for name in ("bed_placed", "bed_foot_broken"):
            self.assertEqual(stages[name][0], [])
        self.assertIn("give @s handcrafted:oak_fancy_bed 1", stages["bed_empty"][0])

    def test_server_observations_preserve_negative_and_reject_duplicate(self):
        lines = []
        for name, (_, checks) in trial.stages("1.21.11").items():
            for label in checks:
                lines.append(f"[Server thread/INFO]: {trial.PREFIX}{name} {label} air")
            lines.append(f"[Server thread/INFO]: {trial.PREFIX}check_{name} done")
        log = "\n".join(lines)
        result = trial.read_states(log, "1.21.11", None)
        self.assertEqual(result["shelf_three"]["upper"], {"block": "air"})
        with self.assertRaisesRegex(ValueError, "repeated"):
            trial.read_states(log + "\n" + lines[0], "1.21.11", None)
        with self.assertRaisesRegex(ValueError, "completion"):
            trial.read_states(log.replace("[Server thread/INFO]:", "[Render thread/INFO]:"), "1.21.11", None)

    def test_interaction_bookshelf_stages_only_provision_items_and_step(self):
        stages = trial.stages("1.21.11", interaction=True)
        self.assertEqual(stages["shelf_before"][0], [f"give @s {trial.SHELF} 3"])
        self.assertEqual(stages["shelf_three"][0], ["setblock 0 120 42 minecraft:smooth_stone"])
        for stage in ("shelf_one", "shelf_two", "shelf_remove_middle"):
            self.assertEqual(stages[stage][0], [])

    def test_sleep_probe_reads_state_without_setting_it(self):
        stages = trial.stages("1.21.1", {"occupied": ["true", "false"]}, interaction=True)
        commands, probes = stages["bed_sleeping"]
        self.assertFalse(any("setblock" in cmd for cmd in commands))
        self.assertIn("schedule function mcfr_nonchair:check_bed_sleeping 10s replace", commands)
        self.assertIn("occupied=true", probes["foot_position"])
        self.assertIn("occupied=true", probes["head_position"])

    def test_sleep_timers_require_server_origin_and_unique_pair(self):
        sleeping = f"[Server thread/INFO]: {trial.PREFIX}timer check_bed_sleeping positive"
        awake = f"[Server thread/INFO]: {trial.PREFIX}timer check_bed_awake zero"
        self.assertEqual(trial.read_sleep_timers(sleeping + "\n" + awake),
                         {"check_bed_sleeping": "positive", "check_bed_awake": "zero"})
        with self.assertRaisesRegex(ValueError, "duplicated"):
            trial.read_sleep_timers(sleeping + "\n" + awake + "\n" + awake)
        with self.assertRaisesRegex(ValueError, "missing"):
            trial.read_sleep_timers(sleeping + "\n" + awake.replace("Server thread", "Render thread"))
