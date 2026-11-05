# Arcus Points Tracker

A functional tracker for the official Arcus (@arcus_xyz) weekly points program.

## Verified Official Information

- **Distribution**: Every Wednesday at 3:00 PM Eastern Time (America/New_York) = 20:00 UTC.
- **Weekly allocation**: Fixed 250,000 points per week (Season 1).
- **Season 1 start**: ~September 30 / October 1, 2026.
- **Program end**: No later than the end of H1 2027.
- **Official blog**: https://arcus.xyz/blog/introducing-arcus-points
- **Points Dashboard**: https://app.arcus.xyz/rewards
- **Official Points API**: https://points-api.arcus.xyz/ (GET /v1/meta for next_drop_at, totals, etc.)

**Snapshot / trading eligibility cutoff**: **Not officially confirmed** in public documentation.  
Points are allocated based on activity during the week at Arcus's sole discretion. This tracker treats the distribution time as the reference boundary and clearly labels all cutoff calculations as estimates.

## Features

1. Weekly Snapshot Tracker (monitors official sources + API)
2. Wednesday Trading Eligibility Calculator (explicitly shows "Not officially confirmed")
3. Live Countdown (UTC, America/New_York, Africa/Casablanca) with correct DST handling via ZoneInfo
4. Streamlit Points Dashboard (live API data + calculator)
5. GitHub Actions daily automated monitoring + alerts
6. Optional Telegram bot (`/status` `/next` `/snapshot` `/trade` `/sources`)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and optionally fill Telegram credentials.

### Run Dashboard

```bash
streamlit run src/arcus_tracker/dashboard.py
```

### Run Telegram Bot (optional)

```bash
python -m src.arcus_tracker.telegram_bot
```

### Run Tests

```bash
pytest
```

### GitHub Actions

The workflow in `.github/workflows/monitor.yml` runs daily and can send Telegram alerts when official sources or API meta change. Add these secrets:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## Security

- Does not request wallet seed phrases or private keys.
- No automatic trading or wallet transactions.
- Respects API rate limits and website terms.
- Never promises token rewards. Points are a participation metric only.

## Data Sources

All schedule data is derived from official Arcus announcements and the public points API. The monitor detects changes in the blog and key API fields.
