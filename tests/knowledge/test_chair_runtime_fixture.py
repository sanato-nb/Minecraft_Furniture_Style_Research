"""INT-3 real-world fixture source states and evidence gate regression tests."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase,main
from unittest.mock import patch
from zipfile import ZipFile

from mcfr import chair_runtime_fixture as f
from mcfr import chair_runtime_capture as c

class PinnedChairWorldFixture(TestCase):
    def test_all_chair_case_ids_unique_and_have_exact_four_facings(self):
        self.assertEqual(len(f.cases("1.21.1")),12)
        self.assertEqual(len(f.cases("1.21.11")),4)
        for version in f.CHAIRS:
            entries=f.cases(version)
            self.assertEqual({x.facing for x in entries},set(f.DIRS))
            self.assertEqual(len({x.case_id for x in entries}),len(entries))
            self.assertTrue(all(x.model_key in c.RESOURCE_BY_MODEL for x in entries))

    def test_16_exact_source_state_targets_not_generic_chair_guesses(self):
        af=[x for x in f.cases("1.21.1") if x.model_key=="AF123"]
        self.assertEqual(len(af),4)
        self.assertTrue(all("variant=10" in x.state() and "tucked=true" in x.state() for x in af))
        hc=[x for x in f.cases("1.21.1") if x.model_key=="HC11210"]
        self.assertTrue(all("color=black" in x.state() and "waterlogged=false" in x.state() for x in hc))
        self.assertEqual(c.MODELS_YPOS["MACAW67"],(90,180,270,0))
        self.assertEqual(c.MODELS_YPOS["AF121"],(0,90,180,270))

    def test_datapack_has_actual_server_commands_and_no_auto_confirmation(self):
        with TemporaryDirectory() as root:
            for version in ("1.21.1","1.21.11"):
                path=Path(root)/version
                result=f.make_pack(version,path)
                self.assertEqual(result["real_client_screenshots"],0)
                self.assertEqual(result["runtime_state_confirmations"],0)
                self.assertEqual(result["study_visual_role_approved"],0)
                placed=(path/"data/mcfr_chair/function/place.mcfunction").read_text()
                observed=(path/"data/mcfr_chair/function/verify.mcfunction").read_text()
                self.assertIn("forceload add",placed)
                self.assertEqual(placed.count("setblock "),
                                 len(f.cases(version))+(4 if version=="1.21.1" else 0))
                if version=="1.21.1":
                    self.assertEqual(placed.count("minecraft:oak_slab[type=top]"),4,
                                     "AF tucked requires one top slab directly ahead per facing")
                self.assertEqual(observed.count("=PASS"),len(f.cases(version)))
                self.assertEqual(observed.count("=FAIL"),len(f.cases(version)))
                self.assertTrue(observed.endswith("say MCFR_CHAIR_STATES_READ\n"))
                for case in f.cases(version):
                    self.assertIn(case.state(),placed)
                    self.assertIn(case.state(),observed)
                with self.assertRaises(FileExistsError):
                    f.make_pack(version,path)

    def test_source_pin_hash_algorithms_and_disallowed_selectors(self):
        msg=b'{"variants":{"facing=north":{"model":"foo:block/x"}}}'
        self.assertEqual(f.digest_bytes(msg,"SHA256"),hashlib.sha256(msg).hexdigest())
        self.assertEqual(f.digest_bytes(msg,"GIT_BLOB_SHA1"),hashlib.sha1(
            b"blob "+str(len(msg)).encode()+b"\0"+msg).hexdigest())
        with self.assertRaises(ValueError):
            c.property_map("facing=north,facing=south")

    def test_pinned_source_runtime_jar_target_validation_in_synthetic_fixture(self):
        # Fake *only* the source digest expectation in a test: build exactly
        # the selectors the app expects, then prove a corrupted target fails.
        with TemporaryDirectory() as dirname:
            d=Path(dirname)
            expected={}
            for version in f.CHAIRS:
                for block,meta in f.ORIGINAL_BLOCKSTATE[version].items():
                    ns=block.split(":")[0]
                    variants={}
                    for case in f.cases(version):
                        if case.block_id != block:continue
                        selector="facing="+case.facing+(","+case.selector if case.selector else "")
                        variants[selector]={
                            "model":c.RESOURCE_BY_MODEL[case.model_key],
                            "y":c.MODELS_YPOS[case.model_key][f.DIRS.index(case.facing)]
                        }
                    raw=json.dumps({"variants":variants}).encode()
                    internal=f"assets/{ns}/blockstates/{meta['file']}"
                    with ZipFile(d/(ns+".jar"),"w") as jar:
                        jar.writestr(internal,raw)
                    expected[block]={**meta,"sha":f.digest_bytes(raw,meta["algorithm"])}
                with patch.dict(f.ORIGINAL_BLOCKSTATE,{version:expected},clear=True):
                    outputs,sources=c.validate_source_targets(version,d)
                self.assertEqual(len(outputs),len(f.cases(version)))
            # Synthetic invalid source model target must fail even if its
            # JAR bytes are cryptographically pinned to a changed test hash.
            p=d/"another_furniture.jar"
            with ZipFile(p) as jar:
                item=next(x for x in jar.namelist() if x.endswith("/acacia_chair.json"))
                doc=json.loads(jar.read(item))
            doc["variants"]["facing=north,tucked=false,variant=1"]["model"]="another_furniture:block/chair/acacia_999"
            blob=json.dumps(doc).encode()
            p.unlink()
            with ZipFile(p,"w") as jar:jar.writestr(item,blob)
            mock={**f.ORIGINAL_BLOCKSTATE["1.21.1"]}
            mock["another_furniture:acacia_chair"]={
                **mock["another_furniture:acacia_chair"],
                "sha":f.digest_bytes(blob,"GIT_BLOB_SHA1")
            }
            with patch.dict(f.ORIGINAL_BLOCKSTATE,{"1.21.1":mock}):
                with self.assertRaises(ValueError):
                    c.validate_source_targets("1.21.1",d)

if __name__=="__main__":
    main()
