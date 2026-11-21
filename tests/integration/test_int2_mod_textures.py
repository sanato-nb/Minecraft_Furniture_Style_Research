"""Regress the independent PNG/UV 1-4 re-audit rules."""
from pathlib import Path
import io
import json
import runpy
import unittest

from PIL import Image
f=runpy.run_path(str(Path(__file__).resolve().parents[2]/"scripts/integration/audit_int2_mod_textures.py"))
metrics=f["png_metrics"]
crc=f["verify_png_crc"]
sh=f["raw_source_sha"]
png_source=f["SIGNATURE"]


class TestIndependentPNGChecks(unittest.TestCase):
    def sample(self):
        im=Image.new("RGBA",(2,2))
        im.putdata([(0,0,0,0),(4,5,6,255),(4,5,6,255),(8,7,6,127)])
        stream=io.BytesIO()
        im.save(stream,format="PNG")
        return stream.getvalue()

    def test_decode_pixels_and_alpha(self):
        d=metrics(self.sample(),"test.png")
        self.assertEqual((d["width"],d["height"],d["pixels"]),(2,2,4))
        self.assertEqual((d["transparent"],d["partial_alpha"],d["opaque"]),(1,1,2))
        self.assertEqual(d["visible_rgb_colors"],2)
        self.assertTrue(d["top4_visible_rgba_counts"].startswith("040506ff:2"))

    def test_png_crc_failure(self):
        data=bytearray(self.sample())
        data[21]^=1
        with self.assertRaisesRegex(ValueError,"PNG CRC differs"):
            crc(bytes(data),"bad.png")

    def test_trailing_bytes_rejected(self):
        with self.assertRaises(ValueError):
            crc(self.sample()+b"injected","bad.png")

    def test_git_blob_matches_historic_kind(self):
        d=b"hello"
        import hashlib
        expected=hashlib.sha1(b"blob 5\x00hello").hexdigest()
        self.assertEqual(sh(d,"GIT_BLOB_SHA1"),expected)

    def test_reject_unknown_hash(self):
        with self.assertRaisesRegex(ValueError,"Unrecognized"):
            sh(b"x","UNKNOWN")


if __name__=="__main__":
    unittest.main()
