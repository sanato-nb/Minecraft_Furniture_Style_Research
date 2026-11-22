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
