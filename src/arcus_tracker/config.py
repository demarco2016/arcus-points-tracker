"""Arcus Points Tracker configuration."""
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent.parent / "data" / "points_config.json"

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)

CONFIG = load_config()
