"""Optional Telegram bot for Arcus Points Tracker."""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from .scheduler import countdown, trade_eligibility, next_distribution
from .config import CONFIG

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cd = countdown()
    text = (
        f"Arcus Points Status\n"
        f"Next distribution: {cd['next_distribution_et']}\n"
        f"Countdown: {cd['human']}\n"
        f"Weekly points: {CONFIG['weekly_points']:,}\n"
        f"Cutoff: Not officially confirmed"
    )
    await update.message.reply_text(text)

async def next_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cd = countdown()
    await update.message.reply_text(
        f"Next distribution\n"
        f"ET: {cd['next_distribution_et']}\n"
        f"UTC: {cd['next_distribution_utc']}\n"
        f"Casablanca: {cd['next_distribution_casablanca']}\n"
        f"Remaining: {cd['human']}"
    )

async def snapshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Snapshot / eligibility cutoff: Not officially confirmed.\n"
        "Confirmed: Points distributed every Wednesday at 3:00 PM America/New_York.\n"
        "Source: https://arcus.xyz/blog/introducing-arcus-points"
    )

async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /trade YYYY-MM-DD HH:MM (UTC)")
        return
    try:
        dt_str = " ".join(context.args)
        trade_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("UTC"))
        res = trade_eligibility(trade_dt)
        text = (
            f"Trade eligibility (estimate)\n"
            f"Qualifies for: {res['qualifies_for']}\n"
            f"Distribution: {res['distribution_time_et']}\n"
            f"Cutoff status: {res['cutoff_status']}\n"
            f"{res['notes']}"
        )
        await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def sources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Official sources:\n" + "\n".join(CONFIG["official_sources"])
    await update.message.reply_text(text)

def main():
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN not set. Skipping bot.")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("next", next_cmd))
    app.add_handler(CommandHandler("snapshot", snapshot))
    app.add_handler(CommandHandler("trade", trade))
    app.add_handler(CommandHandler("sources", sources))
    print("Telegram bot starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
