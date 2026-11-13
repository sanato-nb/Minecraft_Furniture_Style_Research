#!/usr/bin/env python3
"""TEX04-R004: offline integrity-chain check for 9 wool PNG + 21 static JSON.

Input: the user-provided unzipped client JAR folder containing
assets/minecraft/... and META-INF/{MANIFEST.MF,MOJANGCS.SF}.
This checks SHA-384 digest links only. It does NOT validate the PKCS#7 RSA
signature, Mojang's live distribution SHA-1, the complete original JAR,
or an actual in-game render.
"""
import argparse
import base64
import csv
import hashlib
import json
from pathlib import Path

COLORS=("white","red","blue","black","green","yellow","purple","cyan","orange")
TARGETS=tuple(
    entry for color in COLORS for entry in (
        f"assets/minecraft/textures/block/{color}_wool.png",
        f"assets/minecraft/models/block/{color}_wool.json",
        f"assets/minecraft/blockstates/{color}_wool.json"
    )
)+tuple(f"assets/minecraft/models/block/{name}.json"
         for name in ("cube_all","cube","block"))

def sha384_base64(data):
    return base64.b64encode(hashlib.sha384(data).digest()).decode("ascii")

def sections(raw):
    """Normalize GitHub LF vs original JAR CRLF for structural lookup."""
    text=raw.replace(b"\r\n",b"\n")
    return [s for s in text.split(b"\n\n") if s.strip()]

def attributes(section):
    result={}
    last=None
    for raw in section.split(b"\n"):
        if raw.startswith(b" "):
            if last is None: raise ValueError("orphan continuation line")
            result[last]+=raw[1:].decode("ascii")
        elif b": " in raw:
            key,value=raw.split(b": ",1)
            last=key.decode("ascii")
            result[last]=value.decode("ascii")
        elif raw.strip():
            raise ValueError(f"invalid manifest attribute {raw!r}")
    return result

def indexed_sections(raw):
    mapping={}
    chunks=sections(raw)
    for s in chunks[1:]:
        v=attributes(s)
        if "Name" in v:
            if v["Name"] in mapping: raise ValueError("duplicate entry "+v["Name"])
            mapping[v["Name"]]=s
    return chunks,mapping

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("extracted_root",type=Path)
    ap.add_argument("--out",type=Path,default=Path("."))
    args=ap.parse_args()
    root=args.extracted_root
    manifest_raw=(root/"META-INF/MANIFEST.MF").read_bytes()
    signature_raw=(root/"META-INF/MOJANGCS.SF").read_bytes()
    manifest_chunks,manifest=indexed_sections(manifest_raw)
    sig_chunks,signature=indexed_sections(signature_raw)
    sig_main=attributes(sig_chunks[0])

    manifest_main=(manifest_chunks[0]+b"\n\n").replace(b"\n",b"\r\n")
    main_expected=sig_main["SHA-384-Digest-Manifest-Main-Attributes"]
    main_matches=sha384_base64(manifest_main)==main_expected

    rows=[]
    for path in TARGETS:
        source=(root/path).read_bytes()
        if path not in manifest or path not in signature:
            raise ValueError("missing manifest/SF record for "+path)
        manifest_entry=manifest[path]
        man=attributes(manifest_entry)["SHA-384-Digest"]
        sf=attributes(signature[path])["SHA-384-Digest"]
        # Signed JAR manifest paragraphs use CRLF, even if a Git text checkout
        # or GitHub blob has normalized the stored text file to LF.
        reconstructed=(manifest_entry+b"\n\n").replace(b"\n",b"\r\n")
        uploaded_as_lf=(manifest_entry+b"\n\n")
        m1=sha384_base64(source)==man
        m2=sha384_base64(reconstructed)==sf
        same_lf=sha384_base64(uploaded_as_lf)==sf
        rows.append({
            "source_path":path,
            "source_bytes":len(source),
            "git_blob_sha1":hashlib.sha1(b"blob "+str(len(source)).encode()+b"\0"+source).hexdigest(),
            "source_sha256":hashlib.sha256(source).hexdigest(),
            "computed_file_sha384_b64":sha384_base64(source),
            "manifest_file_sha384_b64":man,
            "file_to_manifest_match":m1,
            "computed_manifest_section_crlf_sha384_b64":sha384_base64(reconstructed),
            "signature_file_section_sha384_b64":sf,
            "manifest_crlf_to_sf_match":m2,
            "manifest_lf_to_sf_match":same_lf
        })

    all_file_match=all(row["file_to_manifest_match"] for row in rows)
    all_sf_match=all(row["manifest_crlf_to_sf_match"] for row in rows)
    summary={
        "stage_id":"1-1-04","source_file_count":len(TARGETS),
        "source_file_to_manifest_sha384_matches":sum(row["file_to_manifest_match"] for row in rows),
        "manifest_section_crlf_to_sf_sha384_matches":sum(row["manifest_crlf_to_sf_match"] for row in rows),
        "manifest_main_attributes_match":main_matches,
        "sha384_file_to_manifest_pass":all_file_match,
        "sha384_manifest_to_sf_pass":all_sf_match,
        "pkcs7_rsa_signature_cryptographically_verified":False,
        "official_mojang_client_jar_sha1_verified":False,
        "ingame_static_verified":False,
        "note":"These are integrity-link checks, NOT an authenticated full-JAR provenance or signature validation."
    }
    args.out.mkdir(parents=True,exist_ok=True)
    with (args.out/"REPRODUCE_MANIFEST_CHAIN.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=tuple(rows[0].keys()))
        w.writeheader();w.writerows(rows)
    (args.out/"REPRODUCE_MANIFEST_CHAIN.json").write_text(
        json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))
    if not (main_matches and all_file_match and all_sf_match):
        raise SystemExit("FAIL: one or more SHA-384 links do not match")

if __name__=="__main__":
    main()
