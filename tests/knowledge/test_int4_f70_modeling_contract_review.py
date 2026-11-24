"""Tests for conservative separation of old F approvals and source-model scope."""
import unittest
from mcfr import int4_f70_modeling_contract_review as m

def decide(id,cohort,tag):
    f={"source_state_and_release_assessment":tag,"cohort":cohort}
    return m.choose_historical(id,f,{"faces":6},None,None,None,None,None,None)

class ModelingScope(unittest.TestCase):
    def test_no_case_population_shrink(self):
        self.assertEqual(len(m.HIST),62)
        self.assertEqual(len(m.RISKS),8)
        self.assertFalse(m.HIST&m.RISKS)

    def test_exact_vanilla_source(self):
        self.assertEqual(decide("V02","VANILLA","OFFICIAL_12111_MODEL_PARENT_BLOCKSTATE_GIT_BLOB_SHA1_MATCH")[0],m.OK)

    def test_exact_hc_source(self):
        self.assertEqual(decide("S10","HC","HC_RESEARCH_AND_FABRIC_RELEASE_SOURCE_SHA_MATCH")[0],m.OK)

    def test_selector_only_af_not_release_identity(self):
        self.assertEqual(decide("S01","AF","EXACT_SERVER_ORIGINAL_STATE_AND_MODEL_SELECTOR_MATCH")[0],m.COND)

    def test_reused_source_not_promoted(self):
        self.assertEqual(decide("S16","HC","HISTORIC_MODEL_STATE_F2_LINK_RECORDED_ORIGINAL_RUN_NOT_FULL_SOURCE_GAME_IDENTITY_PROVED")[0],m.COND)

    def test_special_renderer_registration_not_geometry(self):
        r=m.choose_historical("V11",{"source_state_and_release_assessment":"special","cohort":"VANILLA"},
          {"faces":0},None,None,None,None,{"registration":{"bootstrap_constructor_method_handle_verified":True},"exact_model_geometry_and_per_face_UV_extracted":False},None)
        self.assertEqual(r[0],m.HOLD)

    def test_legacy_and_risk_scope_not_equal(self):
        self.assertNotEqual(m.OK,m.RISK_OK)
        self.assertNotEqual(m.COND,m.RISK_COND)

    def test_duplicate_id_denied(self):
        with self.assertRaisesRegex(ValueError,"duplicate"):
            m.index([{"id":"V01"},{"id":"V01"}],"id")

    def test_no_generic_selector_approval(self):
        self.assertEqual(decide("S27","HC","EXACT_SERVER_ORIGINAL_STATE_AND_MODEL_SELECTOR_MATCH")[0],m.COND)

if __name__=="__main__":
    unittest.main()
