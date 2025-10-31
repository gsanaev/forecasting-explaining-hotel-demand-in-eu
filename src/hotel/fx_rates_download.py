"""
fx_rates_download.py
--------------------------
Downloads monthly EUR/USD and EUR/GBP exchange rates
from Yahoo Finance (raw values, single header, Python-friendly format).

Output:
    data/raw/fx_rates.csv
"""

import sys
import pandas as pd
import yfinance as yf
from pathlib import Path

RAW = Path("data/raw")
OUT = RAW / "fx_rates.csv"
RAW.mkdir(parents=True, exist_ok=True)


def download_exchange_rates():
    print("📡 Downloading monthly exchange rates from Yahoo Finance...")

    # Download both tickers at once (EUR/USD, EUR/GBP)
    data = yf.download(
        ["EURUSD=X", "EURGBP=X"],
        start="2010-01-01",
        interval="1mo",
        progress=False
    )

    if not isinstance(data, pd.DataFrame) or data.empty:
        raise ValueError("❌ Yahoo Finance returned no data for EURUSD=X or EURGBP=X")

    # Flatten MultiIndex and keep 'Close' prices
    if isinstance(data.columns, pd.MultiIndex):
        data = data["Close"].copy()

    # If single ticker, convert to DataFrame
    if isinstance(data, pd.Series):
        data = data.to_frame()

    # Rename columns for clarity
    data = data.rename(columns={"EURUSD=X": "eurusd", "EURGBP=X": "eurgbp"}).reset_index()

    # Normalize date column
    data["month"] = pd.to_datetime(data["Date"], errors="coerce") + pd.offsets.MonthBegin(0)
    data = data.drop(columns=["Date"])

    # Keep only useful columns
    data = data[["month", "eurusd", "eurgbp"]]

    # 🧭 Trim to analysis period (2015–2025)
    data = data[data["month"].between("2015-01-01", "2025-08-01")]

    # Format month as string YYYY-MM-DD
    data["month"] = data["month"].dt.strftime("%Y-%m-%d")

    # Sort and reset
    data = data.sort_values("month").reset_index(drop=True)

    # Save
    data.to_csv(OUT, index=False)
    print(f"💾 Saved → {OUT.resolve()} ({len(data):,} rows)")
    print(f"📆 Coverage: {data['month'].min()} → {data['month'].max()}")
    print(data.head(3))


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
