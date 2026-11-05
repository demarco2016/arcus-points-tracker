"""Simple JSON storage for historical points and last update."""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

STORAGE_PATH = Path(__file__).parent.parent.parent / "data" / "history.json"

def load_history() -> Dict[str, Any]:
    if not STORAGE_PATH.exists():
        return {"distributions": [], "last_update": None, "config_hash": None}
    with open(STORAGE_PATH) as f:
        return json.load(f)

def save_history(data: Dict[str, Any]) -> None:
    data["last_update"] = datetime.utcnow().isoformat() + "Z"
    STORAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STORAGE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def record_distribution(week: str, points: int = 250000, notes: str = "") -> None:
    hist = load_history()
    entry = {"week": week, "points": points, "notes": notes, "recorded_at": datetime.utcnow().isoformat() + "Z"}
    # avoid duplicates
    if not any(d["week"] == week for d in hist["distributions"]):
        hist["distributions"].append(entry)
        save_history(hist)
