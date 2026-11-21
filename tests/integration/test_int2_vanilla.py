"""Isolated INT-2 verifier tests; full 4,768 asset pass runs in the workflow."""
import io
import runpy
import unittest
from pathlib import Path

from PIL import Image

AUDIT = runpy.run_path(str(Path(__file__).resolve().parents[2] / "scripts/integration/audit_int2_vanilla.py"))
crc = AUDIT["_png_crc"]
imcheck = AUDIT["_image"]
strict_json = AUDIT["_strict_json"]


class TestIndependentSourceAudit(unittest.TestCase):
    def test_png_crc_and_rgba_decode(self):
        im = Image.new("RGBA", (2, 2))
        im.putdata([(2, 3, 4, 0), (2, 3, 4, 127), (5, 6, 7, 255), (8, 9, 10, 255)])
        stream = io.BytesIO()
        im.save(stream, format="PNG")
        raw = stream.getvalue()
        stats = imcheck(raw, "sample.png")
        self.assertEqual(stats["pixels"], 4)
        self.assertEqual(stats["alpha_zero"], 1)
        self.assertEqual(stats["alpha_partial"], 1)
        self.assertEqual(stats["alpha_opaque"], 2)
        self.assertEqual(stats["unique_rgba"], 4)
        self.assertEqual(stats["png_crc_failures"], 0)
        self.assertGreaterEqual(stats["chunk_count"], 3)

    def test_crc_corruption_is_rejected(self):
        image = Image.new("RGB", (1, 1), (42, 21, 1))
        stream = io.BytesIO()
        image.save(stream, format="PNG")
        raw = bytearray(stream.getvalue())
        raw[20] ^= 0x1
        with self.assertRaisesRegex(ValueError, "CRC mismatch"):
            crc(bytes(raw), "corrupt.png")

    def test_json_duplicate_keys_fail(self):
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            strict_json(b'{"parent":"block/a","parent":"block/b"}', "duplicate.json")

    def test_json_non_finite_number_fails(self):
        with self.assertRaises(ValueError):
            strict_json(b'{"from": NaN}', "bad.json")


if __name__ == "__main__":
    unittest.main()
