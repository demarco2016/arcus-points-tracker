"""Streamlit dashboard for Arcus Points Tracker."""
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

from .scheduler import countdown, trade_eligibility, next_distribution
from .storage import load_history
from .config import CONFIG

st.set_page_config(page_title="Arcus Points Tracker", layout="wide")

st.title("Arcus Points Tracker")
st.caption("Tracks official @arcus_xyz weekly points program. No token promises.")

col1, col2, col3 = st.columns(3)

cd = countdown()
with col1:
    st.metric("Next Distribution (ET)", cd["next_distribution_et"][:16])
    st.metric("Countdown", cd["human"])

with col2:
    st.metric("Weekly Allocation", f"{CONFIG['weekly_points']:,} pts")
    st.metric("Season 1 Start", CONFIG["season1_start"])

with col3:
    st.metric("Program Ends By", CONFIG["program_end_latest"])
    st.metric("Cutoff Status", "Not officially confirmed")

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
    "Distribution time (Wednesdays 3PM ET) is the only confirmed schedule. "
    "Points allocation is at Arcus's sole discretion based on activity."
)
