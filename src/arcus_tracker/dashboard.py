"""Streamlit dashboard for Arcus Points Tracker."""
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from .scheduler import countdown, trade_eligibility
from .storage import load_history
from .config import CONFIG
from .api_client import get_meta

st.set_page_config(page_title="Arcus Points Tracker", layout="wide")

st.title("Arcus Points Tracker")
st.caption("Tracks official @arcus_xyz weekly points program. No token promises.")

# Live API data
meta = get_meta()

col1, col2, col3 = st.columns(3)

cd = countdown()
with col1:
    st.metric("Next Distribution (ET)", cd["next_distribution_et"][:16])
    st.metric("Countdown", cd["human"])

with col2:
    st.metric("Weekly Allocation", f"{CONFIG['weekly_points']:,} pts")
    if not meta.get("error"):
        st.metric("Season Total Points", f"{meta.get('season_total_points', 0):,}")
    else:
        st.metric("Season Total Points", "API unavailable")

with col3:
    st.metric("Program Ends By", CONFIG["program_end_latest"])
    st.metric("Cutoff Status", "Not officially confirmed")

if not meta.get("error"):
    st.subheader("Live from Official API")
    st.write(f"**Next drop (UTC)**: {meta.get('next_drop_at')}")
    st.write(f"**Latest week distributed**: {meta.get('latest_week', {}).get('distributed_at')}")
    st.write(f"**Active addresses this season**: {meta.get('season_addresses', 'N/A')}")
    st.write(f"**Current season**: {meta.get('season', {}).get('name')}")
else:
    st.warning("Could not reach points-api.arcus.xyz — using calculated schedule only.")

st.subheader("Live Countdown")
st.write(f"**UTC**: {cd['next_distribution_utc']}")
st.write(f"**America/New_York**: {cd['next_distribution_et']}")
st.write(f"**Africa/Casablanca**: {cd['next_distribution_casablanca']}")

st.subheader("Trading Eligibility Calculator")
trade_date = st.date_input("Trade date")
trade_time = st.time_input("Trade time (UTC)")
if st.button("Check eligibility"):
    trade_dt = datetime.combine(trade_date, trade_time).replace(tzinfo=ZoneInfo("UTC"))
    result = trade_eligibility(trade_dt)
    st.json(result)
    st.warning(result["cutoff_status"] + " — " + result["notes"])

st.subheader("Official Sources")
for url in CONFIG["official_sources"]:
    st.markdown(f"- [{url}]({url})")

hist = load_history()
st.subheader("History / Last Update")
st.write(f"Last update: {hist.get('last_update', 'Never')}")
st.json(hist.get("distributions", []))

st.info(
    "Snapshot cutoff is **not officially confirmed**. "
    "Distribution time (Wednesdays 3PM ET / 20:00 UTC) is the only confirmed schedule. "
    "Points allocation is at Arcus's sole discretion based on activity."
)
