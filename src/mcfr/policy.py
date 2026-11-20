"""Executable policy gates for manual registration and paid AI dispatch.

Legacy importers are purposefully separate: their pinned historic evidence
can be replayed without requiring a newly authored evidence report per asset.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import research_db as catalog


def configuration(root: Path | None = None) -> dict:
    root = catalog.ROOT if root is None else Path(root)
    config = json.loads((root / "harness/shared/config.json").read_text(encoding="utf-8"))
    if type(config.get("require_evidence")) is not bool or type(config.get("ai_api_enabled")) is not bool:
        raise ValueError("Required harness policy flags must be explicit booleans")
    return config


def check_registration(manifest: dict, root: Path | None = None) -> dict:
    """Require a repository evidence file before manually registering new assets."""
    root = (catalog.ROOT if root is None else Path(root)).resolve()
    if not configuration(root)["require_evidence"]:
        return manifest
    if not isinstance(manifest, dict) or not isinstance(manifest.get("assets"), list):
        raise ValueError("Manifest requires a list of assets")
    fallback = manifest.get("evidence_path")
    assets = []
    for asset in manifest["assets"]:
        if not isinstance(asset, dict):
            raise ValueError("Asset must be a JSON object")
        evidence = asset.get("evidence_path") or fallback
        if not evidence:
            raise ValueError("New registration requires an evidence_path for each asset or the manifest")
        evidence = catalog.relative_path(evidence)
        full = (root / evidence).resolve()
        if not full.is_relative_to(root) or not full.is_file():
            raise ValueError(f"Evidence file missing or outside repository: {evidence}")
        assets.append({**asset, "evidence_path": evidence})
    if not assets:
        raise ValueError("Manual registration requires at least one evidenced asset")
    return {**manifest, "assets": assets}


def require_api_permission(*, explicitly_approved: bool = False) -> None:
    """Default-off gate; explicit per-call opt-in still needs the approval hash."""
    if configuration()["ai_api_enabled"] is True or explicitly_approved is True:
        return
    raise ValueError("AI API is disabled by harness policy; use review-send --enable-api for one approved request")
