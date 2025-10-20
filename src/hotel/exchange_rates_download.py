"""
exchange_rates_download.py
--------------------------
Downloads monthly EUR/USD and EUR/GBP exchange rates
from Yahoo Finance (raw values, single header).
"""

import sys
import pandas as pd
import yfinance as yf
from pathlib import Path

RAW = Path("data/raw")
OUT = RAW / "exchange_rates.csv"
RAW.mkdir(parents=True, exist_ok=True)


def download_exchange_rates():
    print("📡 Downloading monthly exchange rates from Yahoo Finance...")

    # Download both tickers at once to ensure consistent index
    data = yf.download(["EURUSD=X", "EURGBP=X"], start="2010-01-01", interval="1mo", progress=False)

    if not isinstance(data, pd.DataFrame) or data.empty:
        raise ValueError("❌ Yahoo Finance returned no data for EURUSD=X or EURGBP=X")

    # Flatten potential MultiIndex and keep only 'Close' prices
    if isinstance(data.columns, pd.MultiIndex):
        data = data["Close"].copy()

    # If selecting 'Close' returned a Series (single ticker), convert to DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame()

    # Rename columns for clarity
    data = data.rename(columns={"EURUSD=X": "eurusd", "EURGBP=X": "eurgbp"}).reset_index()

    # Parse dates as returned (no resampling or shifting)
    data["time"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.drop(columns=["Date"])

    print(f"✅ Download complete: {len(data):,} rows ({data['time'].min().date()} → {data['time'].max().date()})")
    data.to_csv(OUT, index=False)
    print(f"💾 Saved → {OUT.resolve()} ({len(data):,} rows)")


def main(force: bool = False):
    if OUT.exists() and not force:
        print(f"✅ Using cached file → {OUT.resolve()}")
        return
    try:
        download_exchange_rates()
    except Exception as e:
        print(f"❌ Yahoo Finance fetch failed: {e}")
        print("⚠️ No data fetched. Please check your internet connection or Yahoo API status.")


if __name__ == "__main__":
    force = "--force" in sys.argv
    main(force=force)
