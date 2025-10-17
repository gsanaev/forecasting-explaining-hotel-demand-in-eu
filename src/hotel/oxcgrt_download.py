"""
oxcgrt_download.py
------------------
Downloads the OxCGRT-equivalent 'stringency_index' from Our World in Data (OWID)
or its GitHub mirror. Falls back to a local file if network access fails.

Output:
    data/raw/oxcgrt.csv
"""

import pandas as pd
import requests
from io import StringIO
from pathlib import Path


def download_oxcgrt():
    print("Downloading OxCGRT (via OWID / fallback mirrors)...")

    urls = [
        # ✅ Primary (GitHub mirror – highly reliable)
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv",
        # Secondary (main OWID domain – may fail on some DNS setups)
        "https://covid.ourworldindata.org/data/owid-covid-data.csv",
    ]

    df = None
    for url in urls:
        try:
            print(f"Trying: {url}")
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            df = pd.read_csv(
                StringIO(r.text),
                usecols=["iso_code", "location", "date", "stringency_index"]
            )
            print(f"✅ Successfully loaded data from {url}")
            break
        except Exception as e:
            print(f"⚠️  Failed to download from {url}: {e}")

    if df is None:
        local_path = Path("data/raw/owid-covid-data.csv")
        if not local_path.exists():
            raise RuntimeError(
                "❌ Could not download OWID data and no local backup found.\n"
                "Please manually download:\n"
                "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv\n"
                f"and place it at {local_path.resolve()}"
            )
        print("⚠️  Using local backup file instead.")
        df = pd.read_csv(local_path, usecols=["iso_code", "location", "date", "stringency_index"])

    # --- Clean and aggregate ---
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["stringency_index"])
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    df_monthly = (
        df.groupby(["iso_code", "month"], as_index=False)
        .agg({"stringency_index": "mean"})
        .rename(columns={
            "iso_code": "CountryCode",
            "stringency_index": "StringencyIndex_Average"
        })
    )

    # --- Save result ---
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    out_path = Path("data/raw/oxcgrt.csv")
    df_monthly.to_csv(out_path, index=False)

    print(f"✅ Saved {len(df_monthly):,} monthly policy records to {out_path.resolve()}")


if __name__ == "__main__":
    download_oxcgrt()
