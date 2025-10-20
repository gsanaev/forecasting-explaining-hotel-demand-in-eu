"""
covid_cases_download.py
-----------------------
Downloads global COVID-19 case data (Our World in Data),
aggregates monthly totals per 100k population,
and saves a raw country-month CSV (unaltered).

Output:
    data/raw/covid_cases.csv
"""

import pandas as pd
from pathlib import Path
import requests
from io import StringIO

OUT = Path("data/raw/covid_cases.csv")
OUT.parent.mkdir(parents=True, exist_ok=True)

def download_covid_cases():
    print("🦠 Downloading COVID-19 cases from Our World in Data...")

    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        df = pd.read_csv(
            StringIO(r.text),
            usecols=["iso_code", "location", "date", "new_cases", "population"]
        )
        print(f"✅ Successfully loaded data from {url}")
    except Exception as e:
        raise RuntimeError(f"❌ Failed to download OWID data: {e}")

    # --- Clean and aggregate ---
    df = df[df["iso_code"].str.len() == 3]  # keep ISO3 country codes only
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "population"])
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # ⚠️ Removed: fillna(0) to preserve raw missingness
    df["cases_per_100k"] = (df["new_cases"] / df["population"]) * 100_000

    # Monthly aggregation (acceptable transformation)
    monthly = (
        df.groupby(["iso_code", "month"], as_index=False)
        .agg({"cases_per_100k": "sum"})
        .rename(columns={"iso_code": "iso3"})
    )

    # --- Save ---
    monthly.to_csv(OUT, index=False)
    print(f"💾 Saved {len(monthly):,} monthly records → {OUT.resolve()}")

    # --- Quick summary ---
    covid_years = monthly[monthly["month"].dt.year.between(2020, 2022)]
    print("\n📊 Summary (2020–2022):")
    print(covid_years.groupby("month")["cases_per_100k"].mean().head())

if __name__ == "__main__":
    download_covid_cases()
