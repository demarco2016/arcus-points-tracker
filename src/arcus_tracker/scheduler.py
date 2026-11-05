"""Time zone and schedule logic for Arcus points."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Optional, Tuple

from .config import CONFIG

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
CASABLANCA = ZoneInfo("Africa/Casablanca")

def next_distribution(from_dt: Optional[datetime] = None) -> datetime:
    """Return the next Wednesday 15:00 ET distribution time."""
    if from_dt is None:
        from_dt = datetime.now(UTC)
    now_et = from_dt.astimezone(ET)
    # Wednesday = 2
    days_ahead = (2 - now_et.weekday()) % 7
    candidate = now_et.replace(hour=15, minute=0, second=0, microsecond=0) + timedelta(days=days_ahead)
    if candidate <= now_et:
        candidate += timedelta(days=7)
    return candidate

def previous_distribution(from_dt: Optional[datetime] = None) -> datetime:
    nxt = next_distribution(from_dt)
    return nxt - timedelta(days=7)

def countdown(from_dt: Optional[datetime] = None) -> dict:
    """Return countdown in several timezones."""
    if from_dt is None:
        from_dt = datetime.now(UTC)
    nxt = next_distribution(from_dt)
    delta = nxt - from_dt
    return {
        "next_distribution_utc": nxt.astimezone(UTC).isoformat(),
        "next_distribution_et": nxt.astimezone(ET).isoformat(),
        "next_distribution_casablanca": nxt.astimezone(CASABLANCA).isoformat(),
        "seconds_remaining": int(delta.total_seconds()),
        "human": str(delta).split(".")[0],
    }

def trade_eligibility(trade_dt: datetime) -> dict:
    """
    Determine which epoch a trade belongs to.
    Cutoff is NOT officially confirmed; we use distribution time as the reference boundary
    and explicitly flag uncertainty.
    """
    if trade_dt.tzinfo is None:
        trade_dt = trade_dt.replace(tzinfo=UTC)
    nxt = next_distribution(trade_dt)
    prev = previous_distribution(trade_dt)
    # Trades strictly before the distribution time are assumed to count for that distribution
    # (estimate only)
    if trade_dt < nxt:
        epoch_end = nxt
        epoch_start = prev
        qualifies_for = "upcoming distribution"
    else:
        epoch_end = nxt + timedelta(days=7)
        epoch_start = nxt
        qualifies_for = "following distribution"
    return {
        "trade_time_utc": trade_dt.astimezone(UTC).isoformat(),
        "qualifies_for": qualifies_for,
        "distribution_time_et": epoch_end.astimezone(ET).strftime("%Y-%m-%d %H:%M %Z"),
        "epoch_start_et": epoch_start.astimezone(ET).strftime("%Y-%m-%d %H:%M %Z"),
        "cutoff_status": "Not officially confirmed",
        "is_estimate": True,
        "notes": "Official documentation only confirms distribution every Wednesday at 3PM ET. "
                 "Exact snapshot/eligibility cutoff before that time is not published. "
                 "This calculation uses the distribution time as the reference boundary and is an estimate only.",
    }
