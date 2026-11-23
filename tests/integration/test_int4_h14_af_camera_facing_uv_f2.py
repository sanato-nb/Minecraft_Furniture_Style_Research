"""INT-4-H14 original source/screenshot attribution boundary regression tests."""
from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from PIL import Image
from scripts.integration import build_int4_h14_af_camera_facing_uv_f2 as h14


def png_image(img: Image.Image) -> bytes:
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def fake_texture_pair() -> tuple[bytes, bytes]:
    a = Image.new("RGBA", (16, 16), (80, 40, 20, 255))
    b = a.copy()
    changed = sorted({(x,y) for y in range(7) for x in range(8)}-{(0,0),(7,0)})
    for i, (x,y) in enumerate(changed):
        b.putpixel((x,y), (90,50,30,0 if i<38 else 255))
    return png_image(a),png_image(b)


def fake_parent() -> dict:
    items = [{"faces":{}} for _ in range(10)]
    items[7] = {
        "from":[4,7,13], "to":[12,16,13],
        "faces":{"north":{"uv":[0,0,8,9]},"south":{"uv":[8,0,0,9]}},
    }
    return {"elements":items}


def fake_h11() -> dict:
    return {"counts":{"changed_binding_faces_with_any_different_texel":2}}


def fake_h12() -> dict:
    return {"same_camera":h14.EXPECTED_CAMERA,
            "same_source_coordinates":list(h14.XYZ),
            "source_54_RGBA_changed_texels":54,
            "source_12_different_texture_binding_faces":12}


def fake_original_f2() -> tuple[bytes,dict]:
    a = Image.new("RGB",(1024,684),(180,185,188))
    b = a.copy()
    air = Image.new("RGB",(1024,684),(180,185,188))
    # Exactly 808 changed pixels spanning the pinned original H12 bounds.
    locs = [(x,y) for y in range(433,462) for x in range(493,531)]
    coords = locs[:807]+[locs[-1]]
    assert len(coords)==808
    for x,y in coords:
        a.putpixel((x,y),(90,50,25))
        b.putpixel((x,y),(30,100,75))
    log=b"[RenderAudit] MCFR_H12_TEST_A_EXACT_SERVER=PASS\n"
    docs={}
    for name,im in [("model1_before",a),("model3",b),("model1_after",a),("air",air)]:
        docs[name]=png_image(im)
    states={name:{"sha256":h14.sha(docs[name]),"exact_server_verified":True,
                  "server_marker":"MCFR_H12_TEST_A_EXACT_SERVER=PASS"}
            for name in h14.STAGES}
    manifest={"fixed_camera":h14.EXPECTED_CAMERA,"source_model_coordinates":list(h14.XYZ),
              "real_game_single_session":True,"same_position_facing_camera_all_four":True,
              "states":states}
    manifest_raw=json.dumps(manifest).encode()
    stream=io.BytesIO()
    with ZipFile(stream,"w") as z:
        z.writestr("INT4_H12_AF_SAME_CAMERA_REAL_NATIVE_F2_SOURCE_MANIFEST_V1.json",manifest_raw)
        z.writestr("client.log",log)
        for name,data in docs.items():
            z.writestr(name+".png",data)
    evidence={"original_manifest_sha256":h14.sha(manifest_raw),
              "original_client_log_sha256":h14.sha(log),
              "native_original_F2_sha256":{k:h14.sha(v) for k,v in docs.items()},
              "pixel_measurement":{"model1_to_model3":808,
                 "model1_before_to_model1_after_temporal_control":0,
                 "model_difference_outside_foreground":0,
                 "changed_pixel_bounds":[493,433,530,461]}}
    return stream.getvalue(),evidence


class H14SourceCameraF2(unittest.TestCase):
    def test_source_54_texels_split_into_alpha_and_rgb(self):
        a,b=fake_texture_pair()
        result=h14.original_back_texel_delta(a,b)
        self.assertEqual(result["changed_RGBA_texels"],54)
        self.assertEqual(result["changed_texels_with_alpha_change"],38)
        self.assertEqual(result["changed_texels_only_RGB_change"],16)
        self.assertEqual(result["diff_texels_by_texture_row_y"]["0"],6)

    def test_camera_south_of_two_sided_source_center_plane(self):
        delta={"changed_RGBA_texels":54}
        result=h14.source_camera_face(fake_parent(),fake_h11(),delta)
        self.assertEqual(result["source_faces_on_camera_side"],1)
        self.assertEqual(result["camera_side_source_face_candidate"],"south")
        self.assertEqual(result["camera_opposite_source_face"],"north")
        self.assertFalse(result["gpu_raster_face_visibility_or_exact_pixel_attribution_proven"])
        self.assertFalse(any(x["exact_screen_pixel_to_face_approved"] for x in result["faces"]))

    def test_source_model_change_fail_closed(self):
        changed=fake_parent()
        changed["elements"][7]["faces"]["south"]["uv"]=[0,0,8,9]
        with self.assertRaisesRegex(ValueError,"CENTER_UV_DRIFTED"):
            h14.source_camera_face(changed,fake_h11(),{"changed_RGBA_texels":54})

    def test_source_texture_shape_fail_closed(self):
        a,_=fake_texture_pair()
        with self.assertRaisesRegex(ValueError,"ORIGINAL_54"):
            h14.original_back_texel_delta(a,a)

    def test_actual_f2_metrics_independent_and_original_zip_required(self):
        archive,provenance=fake_original_f2()
        with patch.object(h14,"ARCHIVE_SHA256",h14.sha(archive)):
            result=h14.original_f2_archive_metrics(archive,provenance)
            self.assertEqual(result["variant1_variant3_changed_pixels"],808)
            self.assertEqual(result["variant1_repeat_temporal_changed_pixels"],0)
            self.assertEqual(result["variant1_variant3_changed_pixels_outside_foreground_mask"],0)
            self.assertFalse(result.get("gpu_face_attribution_approved",False))
            with self.assertRaisesRegex(ValueError,"ZIP"):
                h14.original_f2_archive_metrics(archive+b"bad",provenance)

    def test_f2_integrated_server_marker_cannot_be_fabricated(self):
        archive,provenance=fake_original_f2()
        provenance["original_client_log_sha256"]="f"*64
        with patch.object(h14,"ARCHIVE_SHA256",h14.sha(archive)):
            with self.assertRaisesRegex(ValueError,"SERVER_LOG_MISMATCH"):
                h14.original_f2_archive_metrics(archive,provenance)

    def test_does_not_change_F70_or_H03_H05_approval(self):
        a,b=fake_texture_pair()
        archive,provenance=fake_original_f2()
        prev=fake_h12()|provenance|{"real_runtime_AF_JAR_sha1":"verified-example"}
        with patch.object(h14,"ARCHIVE_SHA256",h14.sha(archive)):
            result=h14.research(fake_h11(),prev,fake_parent(),a,b,archive)
        self.assertFalse(result["conclusion"]["source_face_to_screen_pixel_GPU_causality_approved"])
        self.assertEqual(result["conclusion"]["F70_unconditional_approvals"],0)
        self.assertFalse(result["conclusion"]["H03_exit_approved"])
        self.assertFalse(result["conclusion"]["H05_exit_approved"])
        self.assertEqual(result["conclusion"]["INT6_training_or_redistribution_rights_approved"],0)

    def test_source_bytes_must_match_git_blob_pins(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)
            for name in h14.PINS:
                p=folder/name
                p.parent.mkdir(parents=True,exist_ok=True)
                p.write_bytes(name.encode())
            with self.assertRaisesRegex(ValueError,"UNPINNED_AF_ORIGINAL_SOURCE"):
                h14.source_inputs(folder)


if __name__=="__main__":
    unittest.main()
