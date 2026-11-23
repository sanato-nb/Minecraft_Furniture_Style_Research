"""INT-4-H13: real-chair camera commands must be acknowledged, never inferred."""
from unittest import TestCase

from mcfr.chair_runtime_capture import send_minecraft_command, confirmed_camera_teleport


class ChairCameraCommandRecovery(TestCase):
    def test_slash_opens_command_input_without_chat_focus_dependency(self):
        calls=[]
        pauses=[]
        send_minecraft_command(lambda *args:calls.append(args),
                               "/tp @s 0.5 124 42.5 180 20",
                               pause=pauses.append)
        self.assertEqual(calls,[
            ("key","--clearmodifiers","slash"),
            ("type","--clearmodifiers","--delay","14","tp @s 0.5 124 42.5 180 20"),
            ("key","--clearmodifiers","Return"),
        ])
        self.assertEqual(pauses,[0.45])

    def test_noncommand_is_rejected_without_x11_input(self):
        calls=[]
        with self.assertRaises(ValueError):
            send_minecraft_command(lambda *args:calls.append(args),"tp @s 1 2 3",
                                   pause=lambda _:None)
        self.assertEqual(calls,[])

    def test_first_missing_ack_is_retried_once_with_new_log_checkpoint(self):
        calls=[]
        log=["[RenderAudit: Teleported RenderAudit to OLD]"]
        def waiter(proc, predicate, description, timeout):
            calls.append(("wait",timeout))
            self.assertFalse(predicate(), "Stale log acknowledgement must not count")
            if timeout==25:
                raise ValueError("Timed out waiting for original-source chair camera teleport")
            log[0]+="\n[RenderAudit: Teleported RenderAudit to 0.5 124 42.5]"
            self.assertTrue(predicate())
            return True
        confirmed_camera_teleport(
            object(),lambda:log[0],lambda cmd:calls.append(("command",cmd)),
            lambda:calls.append(("focus",)), "0.5 124 42.5 180 20",
            pause=lambda _:calls.append(("stable",)),waiter=waiter)
        self.assertEqual(calls,[
            ("focus",),("command","/tp @s 0.5 124 42.5 180 20"),("wait",25),
            ("focus",),("command","/tp @s 0.5 124 42.5 180 20"),("wait",35),
            ("stable",),
        ])

    def test_two_missing_acks_must_fail_without_approval(self):
        calls=[]
        def waiter(*_):
            raise ValueError("Timed out waiting for original-source chair camera teleport")
        with self.assertRaisesRegex(ValueError,"unconfirmed after two focused"):
            confirmed_camera_teleport(
                object(),lambda:"",lambda _:calls.append("command"),
                lambda:calls.append("focus"),"0.5 124 42.5 180 20",
                pause=lambda _:None,waiter=waiter)
        self.assertEqual(calls,["focus","command","focus","command"])

    def test_process_exit_is_not_retried(self):
        calls=[]
        def waiter(*_):
            raise ValueError("Minecraft exited before original-source chair camera teleport")
        with self.assertRaisesRegex(ValueError,"Minecraft exited"):
            confirmed_camera_teleport(
                object(),lambda:"",lambda _:calls.append("command"),
                lambda:calls.append("focus"),"0.5 124 42.5 180 20",
                pause=lambda _:None,waiter=waiter)
        self.assertEqual(calls,["focus","command"])


if __name__=="__main__":
    import unittest
    unittest.main()
