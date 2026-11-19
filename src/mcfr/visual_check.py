"""Compare a reference and candidate PNG pixel by pixel."""

import hashlib
import io
from pathlib import Path


def load_png(path):
    from PIL import Image

    raw = Path(path).read_bytes()
    with Image.open(io.BytesIO(raw), formats=["PNG"]) as image:
        if getattr(image, "n_frames", 1) != 1:
            raise ValueError("Visual comparison requires a single-frame PNG")
        pixels = image.convert("RGBA")
    return pixels, hashlib.sha256(raw).hexdigest()


def compare(reference, candidate, *, reference_sha256=None):
    from PIL import ImageChops

    baseline, baseline_digest = load_png(reference)
    current, current_digest = load_png(candidate)
    if reference_sha256 is not None and baseline_digest != reference_sha256:
        raise ValueError("Reference PNG does not match its pinned SHA-256")
    result = {
        "evidence_class": "CAPTURE_PIXEL_COMPARISON",
        "reference_sha256": baseline_digest, "candidate_sha256": current_digest,
        "reference_size": list(baseline.size), "candidate_size": list(current.size),
    }
    if baseline.size != current.size:
        return {**result, "status": "INCOMPARABLE"}

    red, green, blue, alpha = ImageChops.difference(baseline, current).split()
    difference = ImageChops.lighter(ImageChops.lighter(red, green), ImageChops.lighter(blue, alpha))
    total = baseline.width * baseline.height
    changed = total - difference.histogram()[0]
    bounds = difference.getbbox()
    return {**result, "status": "DIFFERENCE" if changed else "MATCH", "changed_pixels": changed,
            "total_pixels": total, "difference_box": list(bounds) if bounds else None}
