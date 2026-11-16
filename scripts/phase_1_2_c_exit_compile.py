"""Compile 1-2-C's fixed scope without changing Entry1–4 evidence."""
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/vanilla_models/phase_1-2-C"
OUT = BASE / "entry5"


def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, items, fields=None):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields or list(items[0]))
        writer.writeheader()
        writer.writerows(items)


def blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def main():
    manifest = rows(BASE / "C_FIXED_SCOPE_2390.csv")
    v69 = rows(ROOT / "research/vanilla_models/v69/07_P1_544_EVIDENCE_LEDGER.csv")
    cfields = [k for k in v69[0] if re.match(r"^v\d+_", k) and
               re.search(r"uv|texture|png|pixel|face_material", k, re.I) and
               not re.search(r"fully_|complete|certified|renderer|source_only", k, re.I)]
    model = {}
    face_counts = defaultdict(Counter)
    binding_counts = Counter()
    pngs = {}
    first_seen = {}
    issues = Counter()
    unbound = []
    for entry in range(1, 6):
        folder = BASE / f"entry{entry}"
        for r in rows(folder / "MODEL_SOURCE_EVIDENCE.csv"):
            assert r["leaf_path"] not in model
            model[r["leaf_path"]] = (entry, r)
        for r in rows(folder / "FACE_UV_EVIDENCE.csv"):
            face_counts[r["leaf_path"]][r["uv_type"]] += 1
            face_counts[r["leaf_path"]][r["texture_status"]] += 1
        for r in rows(folder / "TEXTURE_BINDINGS.csv"):
            binding_counts[r["leaf_path"]] += 1
        for r in rows(folder / "PNG_RGBA_EVIDENCE.csv"):
            key = r["png_path"]
            if key in pngs:
                assert pngs[key]["png_sha"] == r["png_sha"] and pngs[key]["rgba_sha256"] == r["rgba_sha256"]
            else:
                pngs[key] = r
                first_seen[key] = entry
        for r in rows(folder / "UNRESOLVED.csv"):
            issues[r["issue"]] += 1
        if (folder / "UNBOUND_TEMPLATE_EVIDENCE.csv").exists():
            for r in rows(folder / "UNBOUND_TEMPLATE_EVIDENCE.csv"):
                unbound.append(dict(entry=f"ENTRY{entry}", model=r["model"], source_path=r["source_path"],
                                    source_sha=r["source_sha"], face_refs=int(r.get("unbound_face_refs", r.get("face_unbound_slot_count"))),
                                    direct_children=int(r.get("direct_children", r.get("direct_children_count"))),
                                    example_child=r.get("example_child", r.get("sample_child"))))
    assert len(model) == 2304 and sum(face_counts[p]["explicit_source"] + face_counts[p]["implicit_source_absent"] for p in model) == 23090
    assert issues == {"missing_slot": 1500, "missing_png": 6}
    assert sum(r["face_refs"] for r in unbound) == 1500 and len({r["source_path"] for r in unbound}) == len(unbound)
    correction = rows(OUT / "HEAVY_CORE_FACE_ERRATUM.csv")
    assert len(correction) == 6 and len({r["png_path"] for r in correction}) == 1
    heavy_path = correction[0]["png_path"]
    assert heavy_path not in pngs
    with Image.open(ROOT / heavy_path) as im:
        rgba = im.convert("RGBA")
        a = Counter(v[3] for v in rgba.get_flattened_data())
        pngs[heavy_path] = dict(png_path=heavy_path, png_sha=blob(ROOT / heavy_path), width=im.width,
                                height=im.height, mode=im.mode, rgba_sha256=hashlib.sha256(rgba.tobytes()).hexdigest(),
                                opaque_pixels=a[255], transparent_pixels=a[0],
                                partial_alpha_pixels=sum(n for k, n in a.items() if 0 < k < 255),
                                unique_alpha_values=len(a))
        first_seen[heavy_path] = 5
    assert len(pngs) == 1073
    png_rows = []
    for path in sorted(pngs):
        r = pngs[path]
        meta = ROOT / (path + ".mcmeta")
        png_rows.append({**r, "first_C_entry": first_seen[path],
                         "mcmeta_path": str(meta.relative_to(ROOT)) if meta.exists() else "",
                         "mcmeta_sha": blob(meta) if meta.exists() else ""})
    write(OUT / "C_PNG_UNIQUE_ALL.csv", png_rows)
    write(OUT / "C_UNBOUND_TEMPLATE_ALL.csv", unbound)

    prior = {}
    historical = []
    for r in v69:
        active = {k: r[k] for k in cfields if r[k].strip() not in ("", "0", "false", "False", "no", "NO", "null", "None")}
        prior[r["source_path"]] = r
        historical.append(dict(source_path=r["source_path"], source_sha=r["source_git_blob_sha"],
                               evidence_rounds=r["evidence_rounds"], v5_to_v34_source_refs=r["v5_to_v34_matching_source_paths"],
                               prior_C_field_values_json=json.dumps(active, ensure_ascii=False, separators=(",", ":")),
                               adopted_prior_C_semantics="no_current_C_remeasures_source",
                               interpretation="provenance_and_value_index_not_independent_history_semantic_audit"))
    assert len(prior) == len(historical) == 544
    write(OUT / "C_HISTORICAL_P1_544_PROVENANCE.csv", historical)

    status = []
    for r in manifest:
        path = r["full_source_path"]
        item = model.get(path)
        assert (item is None) == (r["C_assignment"] == "E_EXCEPTION")
        if item:
            entry, proof = item
            assert r["C_assignment"] == f"ENTRY{entry}" and r["git_blob_sha"] == proof["leaf_sha"]
        else:
            entry = 0
        status.append(dict(asset_type=r["asset_type"], source_path=path, git_blob_sha=r["git_blob_sha"],
                           priority=r["priority"], C_assignment=r["C_assignment"],
                           C_model_source_checked="true" if item else "false_E_owned",
                           C_applied_faces=sum(face_counts[path].values()) // 2 if item else 0,
                           C_explicit_uv_faces=face_counts[path]["explicit_source"],
                           C_implicit_uv_key_absent_faces=face_counts[path]["implicit_source_absent"],
                           C_bound_png_face_refs=face_counts[path]["resolved"] + (6 if path.endswith("/heavy_core.json") else 0),
                           C_template_unbound_face_refs=face_counts[path]["missing_slot"],
                           C_corrected_bare_slot_refs=6 if path.endswith("/heavy_core.json") else 0,
                           C_binding_rows=binding_counts[path],
                           C_prior_P1_v69_link="path_sha_verified" if path in prior else "not_P1",
                           C_prior_semantic_claim_adopted="false", E_owner=r["C_exception_owner"] or "",
                           C_evidence_path=f"research/vanilla_models/phase_1-2-C/entry{entry}/MODEL_SOURCE_EVIDENCE.csv" if item else ""))
    # Each face increments one UV bucket and one texture-status bucket.
    assert len(status) == 2390 and sum(int(r["C_applied_faces"]) for r in status) == 23090
    assert sum(int(r["C_bound_png_face_refs"]) for r in status) == 21590
    write(OUT / "C_SCOPE_2390_FINAL_STATUS.csv", status)
    summary = dict(schema="C_ENTRY5_COMPILED_SOURCE_SCOPE", model_identity_count=2390,
                   direct_model_count=len(model), E_exceptions=86, applied_face_refs=23090,
                   explicit_uv_faces=sum(face_counts[p]["explicit_source"] for p in model),
                   implicit_uv_key_absent_faces=sum(face_counts[p]["implicit_source_absent"] for p in model),
                   bound_png_face_refs=21590, template_unbound_face_refs=1500,
                   bare_slot_face_erratum=6, unexplained_face_refs=0,
                   unique_bound_png_count=len(pngs),
                   unique_png_rgba_pixels=sum(int(r["width"])*int(r["height"]) for r in pngs.values()),
                   unique_mcmeta_source_paths=sum(bool(r["mcmeta_path"]) for r in png_rows),
                   historical_P1_identity_provenance_rows=len(historical),
                   history_semantics_adopted_from_unverified_values=0,
                   status="SOURCE_AGGREGATE_PENDING_INDEPENDENT_EXIT_AUDIT")
    (OUT / "C_ENTRY5_COMPILED_SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
