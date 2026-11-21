"""Storage layer: JSON (legacy) + SQLite for distributions and reminders."""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).parent.parent.parent / "data"
JSON_PATH = DATA_DIR / "history.json"
DB_PATH = DATA_DIR / "points.db"

def _get_conn():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS distributions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week TEXT UNIQUE,
                points INTEGER,
                notes TEXT,
                recorded_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                chat_id INTEGER PRIMARY KEY,
                username TEXT,
                created_at TEXT
            )
        """)
        conn.commit()

# ---------- JSON (legacy, kept for compatibility) ----------
def load_history() -> Dict[str, Any]:
    if not JSON_PATH.exists():
        return {"distributions": [], "last_update": None}
    with open(JSON_PATH) as f:
        return json.load(f)

def save_history(data: Dict[str, Any]) -> None:
    data["last_update"] = datetime.utcnow().isoformat() + "Z"
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)

# ---------- SQLite ----------
def record_distribution(week: str, points: int = 250000, notes: str = "") -> None:
    init_db()
    with _get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO distributions (week, points, notes, recorded_at) VALUES (?, ?, ?, ?)",
            (week, points, notes, datetime.utcnow().isoformat() + "Z")
        )
        conn.commit()
    # also keep JSON in sync
    hist = load_history()
    if not any(d["week"] == week for d in hist["distributions"]):
        hist["distributions"].append({"week": week, "points": points, "notes": notes, "recorded_at": datetime.utcnow().isoformat() + "Z"})
        save_history(hist)

def get_distributions(limit: int = 10) -> List[Dict]:
    init_db()
    with _get_conn() as conn:
        rows = conn.execute("SELECT * FROM distributions ORDER BY week DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]

def add_reminder(chat_id: int, username: str = "") -> None:
    init_db()
    with _get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO reminders (chat_id, username, created_at) VALUES (?, ?, ?)",
            (chat_id, username, datetime.utcnow().isoformat() + "Z")
        )
        conn.commit()

def get_reminders() -> List[Dict]:
    init_db()
    with _get_conn() as conn:
        rows = conn.execute("SELECT * FROM reminders").fetchall()
        return [dict(r) for r in rows]
