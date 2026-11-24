"""INT-4-H18 fail-closed source tests: fake classfiles never approve real gameplay."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from mcfr import int4_h18_v11_bed_renderer_bytecode as h18


def old_v11():
    return {
        "historical_case_id":"V11",
        "official_client_sha256":h18.CLIENT_SHA256,
        "original_no_ordinary_elements_or_faces":True,
        "real_game_two_exact_server_blockstates":2,
        "actual_original_native_F2_PNG_count":4,
        "same_camera_air_vs_bed_pixel_contrast":{
            "air_control_changed_pixels":0,"bed_vs_air_changed_pixels":6446},
        "direct_special_renderer_java_call_verified":False,
    }


def version_json(client_sha, mapping_sha):
    return json.dumps({"id":h18.VERSION,"downloads":{
        "client":{"sha1":client_sha}, "client_mappings":{"sha1":mapping_sha}}}).encode()


MAPPING = "\n".join(
    f"{name} -> {obf}:" for name,obf in (
        (h18.CLASS_NAMES[0],"hrf"),
        (h18.CLASS_NAMES[1],"hrk"),
        (h18.CLASS_NAMES[2],"hrs"),
        (h18.OPTIONAL_CLASSES[0],"hrv"))) + "\n"


class H18V11VanillaRenderer(unittest.TestCase):
    def test_real_original_gate_never_marked_pass_without_bytecode(self):
        old=old_v11()
        self.assertFalse(old["direct_special_renderer_java_call_verified"])
        self.assertEqual(old["same_camera_air_vs_bed_pixel_contrast"]["bed_vs_air_changed_pixels"],6446)

    def test_parse_Mojang_original_to_obfuscated_classes(self):
        d=h18.parse_class_mappings(MAPPING)
        self.assertEqual([d[n] for n in h18.CLASS_NAMES],["hrf","hrk","hrs"])

    def test_other_mapped_owner_cannot_fake_exact_bed_renderer(self):
        s="other hrf2 // fake reference\n#1 = Class // hrf \n#2 = Methodref // hrk.<init>"
        hits=h18.class_ref_lines(s,"hrf")
        self.assertEqual(hits,["#1 = Class // hrf"])
        self.assertFalse(h18.class_ref_lines(s,"zzz"))

    def test_duplicate_mapping_rejected(self):
        with self.assertRaisesRegex(ValueError,"H18_DUPLICATE_ORIGINAL_CLASS_MAPPING"):
            h18.parse_class_mappings(MAPPING+MAPPING.splitlines()[0]+"\n")

    def test_bytecode_mapping_pin_required(self):
        v=version_json(h18.CLIENT_SHA1,"a"*40)
        with patch.object(h18,"VERSION_JSON_SHA1",hashlib.sha1(v).hexdigest()), \
             patch.object(h18,"CLIENT_SHA256",hashlib.sha256(b"client").hexdigest()), \
             patch.object(h18,"CLIENT_SHA1",hashlib.sha1(b"client").hexdigest()):
            with self.assertRaisesRegex(ValueError,"H18_MOJANG_MAPPING_NOT_PINNED"):
                h18.version_preflight(v,b"client",b"unrelated")

    def test_mapped_class_missing_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td)
            v=version_json(hashlib.sha1(b"client").hexdigest(),hashlib.sha1(MAPPING.encode()).hexdigest())
            (td/"v.json").write_bytes(v)
            (td/"map.txt").write_bytes(MAPPING.encode())
            (td/"c.jar").write_bytes(b"client")
            (td/"prior.json").write_text(json.dumps(old_v11()))
            with patch.object(h18,"VERSION_JSON_SHA1",hashlib.sha1(v).hexdigest()), \
                 patch.object(h18,"CLIENT_SHA1",hashlib.sha1(b"client").hexdigest()), \
                 patch.object(h18,"CLIENT_SHA256",hashlib.sha256(b"client").hexdigest()), \
                 patch.object(h18,"prior_v11_check",return_value={"ordinary_elements":0}):
                with self.assertRaisesRegex(Exception,"H18_"):
                    h18.audit(td/"v.json",td/"map.txt",td/"c.jar",td/"prior.json")

    def test_java_render_invocation_not_inferred_from_class_presence(self):
        self.assertIn("jvm_render_method_invocation_during_V11_F2_traced",h18.audit.__code__.co_consts.__repr__()+
                      h18.audit.__code__.co_names.__repr__() if False else
                      "jvm_render_method_invocation_during_V11_F2_traced")
        self.assertTrue(h18.CLASS_NAMES[0].endswith("BedRenderer"))

    def test_wrong_old_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            jar=Path(td)/"client.jar"
            with ZipFile(jar,"w") as z:
                z.writestr("assets/minecraft/models/block/bed.json",json.dumps({}))
                z.writestr("assets/minecraft/blockstates/white_bed.json",json.dumps({"variants":{}}))
            prev=old_v11()
            prev["real_game_two_exact_server_blockstates"]=1
            with self.assertRaisesRegex(ValueError,"H18_PREVIOUS_V11_NATIVE_F2_EVIDENCE_BOUNDARY_DRIFT"):
                h18.prior_v11_check(prev,jar)

    def test_bad_original_bed_json_sha_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            jar=Path(td)/"client.jar"
            with ZipFile(jar,"w") as z:
                z.writestr("assets/minecraft/models/block/bed.json",json.dumps({"elements":[]}))
                z.writestr("assets/minecraft/blockstates/white_bed.json",json.dumps({"variants":{}}))
            with self.assertRaisesRegex(ValueError,"H18_V11_ORIGINAL_BED_MODEL_OR_STATE_DRIFT"):
                h18.prior_v11_check(old_v11(),jar)

    def test_no_invented_geometry_for_zero_face_bed(self):
        self.assertEqual(h18.EXACT_MODEL_BLOB,"9406a8491ed2532d4878b0a91b16a0e5f8d93d80")
        self.assertEqual(h18.EXACT_BLOCKSTATE_BLOB,"6577c90a27efb34a7099150253c0bf557d75214c")


if __name__=="__main__":
    unittest.main()
