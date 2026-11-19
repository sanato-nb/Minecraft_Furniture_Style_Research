"""Track explicitly checked upstream releases. Downloads and registration are separate."""

from datetime import datetime
import json
import re
from urllib.parse import urlencode
from urllib.request import Request, build_opener

from . import research_db as catalog, research_engine as engine
from .ai_review import RejectRedirect

MOJANG = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
MODRINTH = "https://api.modrinth.com/v2/project"
MAX_FEED_BYTES = 16 * 1024 * 1024


def fetch(url):
    request = Request(url, headers={
        "User-Agent": "sanato-nb/Minecraft_Furniture_Style_Research (https://github.com/sanato-nb/Minecraft_Furniture_Style_Research)",
        "Accept": "application/json",
    })
    with build_opener(RejectRedirect()).open(request, timeout=20) as response:
        raw = response.read(MAX_FEED_BYTES + 1)
    if len(raw) > MAX_FEED_BYTES:
        raise ValueError("Upstream metadata exceeds the response limit")
    return json.loads(raw)


def published_time(value):
    published = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if published.tzinfo is None:
        raise ValueError("Upstream publication timestamp lacks a timezone")
    return published


def digest(value, length):
    if not re.fullmatch(rf"[0-9a-f]{{{length}}}", value):
        raise ValueError("Malformed upstream hash")
    return value


def latest_vanilla(feed):
    version = feed["latest"]["release"]
    row = next((row for row in feed["versions"] if row["id"] == version and row["type"] == "release"), None)
    if row is None:
        raise ValueError("Mojang feed lacks its declared stable release")
    return {
        "id": version, "version": version, "published_at": row["releaseTime"],
        "manifest_sha1": digest(row["sha1"], 40), "manifest_url": row["url"],
    }


def latest_mod(feed, game_version, loader):
    eligible = [
        row for row in feed
        if row["version_type"] == "release" and game_version in row["game_versions"] and loader in row["loaders"]
    ]
    if not eligible:
        raise ValueError("No stable Modrinth version matches this game version and loader")
    row = max(eligible, key=lambda row: (published_time(row["date_published"]), row["id"]))
    files = [{
        "filename": file["filename"], "sha512": digest(file["hashes"]["sha512"], 128),
        "primary": file["primary"], "size": file["size"],
    } for file in row["files"]]
    if not files:
        raise ValueError("Selected Modrinth version has no files")
    return {
        "id": row["id"], "version": row["version_number"], "published_at": row["date_published"],
        "files": sorted(files, key=lambda file: (file["filename"], file["sha512"])),
    }


def target_key(target, game_version="", loader=""):
    if any(not isinstance(value, str) or value != value.strip() for value in (target, game_version, loader)):
        raise ValueError("Watch fields must be strings without surrounding whitespace")
    if target == "vanilla":
        if game_version or loader:
            raise ValueError("Vanilla tracks the latest stable Java release")
    elif not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", target) or not game_version or not loader:
        raise ValueError("Mod checks require a Modrinth project, game version and loader")
    return target, game_version.lower(), loader.lower()


def check(db, target: str, game_version: str = "", loader: str = "", *, load=fetch) -> dict:
    key = target_key(target, game_version, loader)
    target, game_version, loader = key
    if target == "vanilla":
        latest = latest_vanilla(load(MOJANG))
    else:
        query = urlencode({"loaders": json.dumps([loader]), "game_versions": json.dumps([game_version]),
                           "include_changelog": "false"})
        latest = latest_mod(load(f"{MODRINTH}/{target}/version?{query}"), game_version, loader)
    published = published_time(latest["published_at"])
    with catalog.write_transaction(db):
        stored = db.execute(
            "SELECT release_json FROM upstream_observation WHERE target = ? AND game_version = ? AND loader = ? "
            "ORDER BY observation_id DESC LIMIT 1", key,
        ).fetchone()
        previous = json.loads(stored[0]) if stored else None
        if previous is None:
            state = "BASELINE"
        elif latest == previous:
            state = "UNCHANGED"
        elif published < published_time(previous["published_at"]):
            state = "OLDER_FEED"
        else:
            state = "UPDATE_DETECTED"
        if state in {"BASELINE", "UPDATE_DETECTED"}:
            db.execute(
                "INSERT INTO upstream_observation(target, game_version, loader, release_json) VALUES (?, ?, ?, ?)",
                (*key, engine._json(latest)),
            )
    return {"status": state, "target": target, "game_version": game_version, "loader": loader,
            "latest": latest, "previous": previous}


def check_many(db, entries, *, load=fetch) -> dict:
    if not isinstance(entries, list) or not entries:
        raise ValueError("Watch list must be a nonempty JSON array")
    targets = {}
    fields = {"target", "game_version", "loader"}
    for entry in entries:
        if not isinstance(entry, dict) or entry.keys() - fields or "target" not in entry:
            raise ValueError("Watch entries require a target and accept only game_version and loader")
        key = target_key(**entry)
        if key in targets:
            raise ValueError(f"Duplicate watch target: {' / '.join(key)}")
        targets[key] = entry

    reports = []
    for target, game_version, loader in targets:
        try:
            report = check(db, target, game_version, loader, load=load)
        except (KeyError, OSError, TypeError, ValueError) as exc:
            report = {"target": target, "game_version": game_version, "loader": loader,
                      "status": "ERROR", "error": str(exc)}
        reports.append(report)
    return {"status": "FAIL" if any(row["status"] == "ERROR" for row in reports) else "PASS",
            "updates_detected": sum(row["status"] == "UPDATE_DETECTED" for row in reports),
            "targets": reports}
