# Arcus Points Tracker

A functional tracker for the official Arcus (@arcus_xyz) weekly points program.

## Verified Official Information

- **Distribution**: Every Wednesday at 3:00 PM Eastern Time (America/New_York).
- **Weekly allocation**: Fixed 250,000 points per week (Season 1).
- **Season 1 start**: October 1, 2026.
- **Program end**: No later than the end of H1 2027.
- **Official source**: https://arcus.xyz/blog/introducing-arcus-points
- **Dashboard**: https://app.arcus.xyz/rewards

**Snapshot / trading eligibility cutoff**: Not officially confirmed in public documentation.  
Points are allocated based on activity during the week at Arcus's discretion. The tracker treats the distribution time as the reference boundary and clearly labels anything else as unconfirmed.

## Features

- Weekly snapshot / distribution tracker
- Trading eligibility calculator (with explicit "Not officially confirmed" when needed)
- Live countdown (UTC, America/New_York, Africa/Casablanca)
- Streamlit dashboard
- GitHub Actions daily monitor
- Optional Telegram bot commands: /status /next /snapshot /trade /sources

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill Telegram credentials if desired.

### Run Dashboard

```bash
streamlit run src/arcus_tracker/dashboard.py
```

### Run Telegram Bot

```bash
python -m src.arcus_tracker.telegram_bot
```

### Run Tests

```bash
pytest
```

## Security

- No wallet seed phrases or private keys are requested.
- No trading or on-chain transactions.
- Respects rate limits and terms.
- Points do not guarantee any token rewards.

## Data Sources

All schedule data is derived from official Arcus announcements. The monitor checks the blog and X for changes.
