"""Monitor official sources for changes (used by GitHub Actions)."""
import hashlib
import json
from datetime import datetime

import requests

from .storage import load_history, save_history
from .config import CONFIG

SOURCES = [
    "https://arcus.xyz/blog/introducing-arcus-points",
]

def fetch_and_hash() -> dict:
    results = {}
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            content = r.text
            results[url] = {
                "hash": hashlib.sha256(content.encode()).hexdigest(),
                "status": r.status_code,
                "length": len(content),
            }
        except Exception as e:
            results[url] = {"error": str(e)}
    return results

def check_for_changes() -> dict:
    hist = load_history()
    current = fetch_and_hash()
    previous = hist.get("source_hashes", {})
    changes = []
    for url, data in current.items():
        if "hash" in data and data["hash"] != previous.get(url):
            changes.append(url)
    hist["source_hashes"] = {k: v.get("hash") for k, v in current.items() if "hash" in v}
    hist["last_monitor"] = datetime.utcnow().isoformat() + "Z"
    save_history(hist)
    return {
        "changes_detected": bool(changes),
        "changed_sources": changes,
        "current": current,
        "config_snapshot": CONFIG,
    }

if __name__ == "__main__":
    print(json.dumps(check_for_changes(), indent=2))
