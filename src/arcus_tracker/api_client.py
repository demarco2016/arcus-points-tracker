"""Client for the official Arcus points API."""
import requests
from typing import Optional, Dict, Any

API_BASE = "https://points-api.arcus.xyz"

def get_meta() -> Dict[str, Any]:
    """Fetch /v1/meta which includes next_drop_at, latest week, etc."""
    try:
        r = requests.get(f"{API_BASE}/v1/meta", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e), "fallback": True}

def get_leaderboard(season: str = "Season 1", limit: int = 10) -> Dict[str, Any]:
    try:
        r = requests.get(
            f"{API_BASE}/v1/leaderboard",
            params={"season": season, "limit": limit},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
