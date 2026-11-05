"""Tests for Arcus Points Tracker."""
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from src.arcus_tracker.scheduler import next_distribution, trade_eligibility, countdown

def test_next_distribution_is_wednesday_3pm_et():
    dt = next_distribution()
    assert dt.weekday() == 2  # Wednesday
    assert dt.hour == 15
    assert dt.minute == 0
    assert str(dt.tzinfo) == "America/New_York" or "EST" in str(dt) or "EDT" in str(dt)

def test_trade_eligibility_flags_unconfirmed():
    trade = datetime(2026, 11, 5, 12, 0, tzinfo=ZoneInfo("UTC"))
    res = trade_eligibility(trade)
    assert res["cutoff_status"] == "Not officially confirmed"
    assert res["is_estimate"] is True
    assert "Not officially confirmed" in res["notes"] or "estimate" in res["notes"].lower()

def test_countdown_has_timezones():
    cd = countdown()
    assert "next_distribution_utc" in cd
    assert "next_distribution_et" in cd
    assert "next_distribution_casablanca" in cd
    assert cd["seconds_remaining"] > 0
