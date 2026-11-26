"""B30 targeted CI infrastructure tests: no gameplay additions."""
import unittest
from types import SimpleNamespace

from mcfr.int4_bed_exterior import wait_for_exact_client_join


class ClientJoinGuardTest(unittest.TestCase):
    def test_first_gui_client_join_has_exact_original_server_proof(self):
        server = SimpleNamespace(read=lambda: "[Server thread/INFO] RenderAudit joined the game")
        client = SimpleNamespace(proc=SimpleNamespace(poll=lambda: None),
                                 read=lambda: "")
        wait_for_exact_client_join(server, client, "RenderAudit", timeout=1, clock=lambda: 0, pause=lambda _: None)

    def test_native_early_exit_is_not_misreported_as_slow_game_join(self):
        server = SimpleNamespace(read=lambda: "")
        client = SimpleNamespace(proc=SimpleNamespace(poll=lambda: 1),
                                 read=lambda: "java.lang.UnsatisfiedLinkError: Failed to locate library: liblwjgl_opengl.so")
        with self.assertRaisesRegex(RuntimeError, "liblwjgl_opengl.so"):
            wait_for_exact_client_join(server, client, "RenderAudit", timeout=1,
                                       clock=lambda: 0, pause=lambda _: None)

    def test_silent_alive_process_still_times_out_in_bounded_period(self):
        times = iter((0, 2))
        server = SimpleNamespace(read=lambda: "")
        client = SimpleNamespace(proc=SimpleNamespace(poll=lambda: None), read=lambda: "")
        with self.assertRaisesRegex(TimeoutError, "bounded 1s"):
            wait_for_exact_client_join(server, client, "BedObserver", timeout=1,
                                       clock=lambda: next(times), pause=lambda _: None)

    def test_staggered_second_client_can_join_without_unverified_success(self):
        calls = [0]
        def read():
            calls[0] += 1
            return "BedObserver joined the game" if calls[0] >= 3 else ""
        server = SimpleNamespace(read=read)
        client = SimpleNamespace(proc=SimpleNamespace(poll=lambda: None), read=lambda: "")
        wait_for_exact_client_join(server, client, "BedObserver", timeout=2,
                                   clock=lambda: 0, pause=lambda _: None)
        self.assertEqual(calls[0], 3)


if __name__ == "__main__":
    unittest.main()
