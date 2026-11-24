"""Synthetic negative controls; these tests do not count as real F2 evidence."""
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile
from PIL import Image
from mcfr import int4_h23_r06_animation_control as m

class H23(unittest.TestCase):
    def make_source(self,root):
        png=io.BytesIO()
        im=Image.new("RGBA",(16,512))
        for i in range(32):
            im.paste((0,i*4,200,255),(0,i*16,16,(i+1)*16))
        im.save(png,format="PNG")
        metadata=b'{"animation":{"frametime":2}}'
        p=root/"test.jar"
        with ZipFile(p,"w") as z:
            z.writestr(m.TEX,png.getvalue())
            z.writestr(m.META,metadata)
            z.writestr("model.json",b'{"unchanged":true}')
            z.writestr("class.class",b"test only")
        return p,png.getvalue(),metadata
    def test_only_meta_changed_and_original_png_unchanged(self):
        with tempfile.TemporaryDirectory() as t:
            p,png,meta=self.make_source(Path(t))
            original=m.sha(p.read_bytes())
            with patch.object(m.k,"MACAW_SHA256",original),patch.object(m,"PNG_SHA",m.sha(png)),patch.object(m,"META_SHA",m.sha(meta)):
                orig=m.freeze(p,"original")
                self.assertEqual(orig["changed_members"],[])
                result=m.freeze(p,"frozen")
            self.assertEqual(result["changed_members"],[m.META])
            self.assertEqual(result["distinct_source_uv_crops"],32)
            self.assertNotEqual(result["runtime_jar_sha256"],original)
            with ZipFile(p) as z:
                self.assertEqual(z.read(m.TEX),png)
                self.assertEqual(z.read("class.class"),b"test only")
                self.assertEqual(z.read("model.json"),b'{"unchanged":true}')
                self.assertEqual(json.loads(z.read(m.META))["animation"]["frames"],[0])
    def test_wrong_official_pin_denied(self):
        with tempfile.TemporaryDirectory() as t:
            p,_,_=self.make_source(Path(t))
            with self.assertRaisesRegex(ValueError,"original JAR pin"):
                m.freeze(p,"frozen")
    def test_bad_mode_denied(self):
        with self.assertRaisesRegex(ValueError,"unknown experiment mode"):
            m.freeze(Path("no.jar"),"invalid")
    def test_static_texture_is_not_animation(self):
        with tempfile.TemporaryDirectory() as t:
            p,_,meta=self.make_source(Path(t))
            buf=io.BytesIO();Image.new("RGBA",(16,512),(0,0,255,255)).save(buf,format="PNG")
            with ZipFile(p,"w") as z:
                z.writestr(m.TEX,buf.getvalue());z.writestr(m.META,meta)
            with patch.object(m.k,"MACAW_SHA256",m.sha(p.read_bytes())),patch.object(m,"PNG_SHA",m.sha(buf.getvalue())),patch.object(m,"META_SHA",m.sha(meta)):
                with self.assertRaisesRegex(ValueError,"no actual source animation changes"):
                    m.freeze(p,"frozen")
if __name__=="__main__":unittest.main()
